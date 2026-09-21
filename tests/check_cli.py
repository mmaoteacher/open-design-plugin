"""Opt-in CLI discovery test; uses temporary host settings and an installed app.

python3 tests/check_cli.py --agent codex
python3 tests/check_cli.py --agent claude --cli /path/to/claude
No model turn or artifact-writing tool is invoked.
"""
import argparse
import json
import os
from pathlib import Path
import queue
import shutil
import subprocess
import tempfile
import threading
import time

SOURCE = Path(__file__).resolve().parents[1]
PLUGIN_ID = 'open-design-plugin@open-design'


class Client:
    def __init__(self, command, env, cwd):
        self.process = subprocess.Popen(command, env=env, cwd=cwd, text=True,
                                        stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                        stderr=subprocess.DEVNULL)
        self.messages = queue.Queue()
        self.serial = 0
        threading.Thread(target=self._read, daemon=True).start()

    def _read(self):
        for line in self.process.stdout:
            try:
                self.messages.put(json.loads(line))
            except json.JSONDecodeError:
                continue
        self.messages.put(None)

    def call(self, method, params=None):
        self.serial += 1
        if isinstance(method, dict):
            packet = {'type': 'control_request', 'request_id': str(self.serial), 'request': method}
        else:
            packet = {'id': self.serial, 'method': method, 'params': params or {}}
        self.process.stdin.write(json.dumps(packet) + '\n')
        self.process.stdin.flush()
        deadline = time.monotonic() + 30
        while time.monotonic() < deadline:
            message = self.messages.get(timeout=max(.01, deadline - time.monotonic()))
            if message is None:
                raise RuntimeError('CLI exited before responding')
            if message.get('id') == self.serial:
                if 'error' in message:
                    raise RuntimeError(message['error'])
                return message['result']
            response = message.get('response', {})
            if message.get('type') == 'control_response' and response.get('request_id') == str(self.serial):
                if response['subtype'] != 'success':
                    raise RuntimeError(response)
                return response['response']
        raise RuntimeError('CLI response timeout')

    def close(self):
        self.process.terminate()
        try:
            self.process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            self.process.kill()
            self.process.wait()


def inspect(cli, agent, env, cwd):
    args = ['app-server', '--stdio'] if agent == 'codex' else [
        '--print', '--input-format', 'stream-json', '--output-format', 'stream-json', '--verbose']
    client = Client([cli] + args, env, cwd)
    try:
        if agent == 'codex':
            client.call('initialize', {'clientInfo': {'name': 'opendesign-check', 'version': '1.0'},
                                       'capabilities': {'experimentalApi': True}})
            data = client.call('skills/list', {'cwds': [str(cwd)], 'forceReload': True})['data'][0]
            assert not data['errors'], data['errors']
            skills = [s['name'] for s in data['skills'] if s.get('pluginId') == PLUGIN_ID]
            servers = client.call('mcpServerStatus/list')['data']
            servers = [s for s in servers if s.get('pluginId') == PLUGIN_ID]
        else:
            data = client.call({'subtype': 'initialize'})
            skills = [c['name'] for c in data['commands'] if c['name'].startswith('open-design-plugin:')]
            servers = client.call({'subtype': 'mcp_status'})['mcpServers']
            servers = [s for s in servers if s['name'].startswith('plugin:open-design-plugin:')]
            deadline = time.monotonic() + 15
            while any(s.get('status') == 'pending' for s in servers) and time.monotonic() < deadline:
                time.sleep(.2)
                servers = client.call({'subtype': 'mcp_status'})['mcpServers']
                servers = [s for s in servers if s['name'].startswith('plugin:open-design-plugin:')]
        return skills, servers
    finally:
        client.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--agent', required=True, choices=['codex', 'claude'])
    parser.add_argument('--cli', help='Path to CLI executable')
    parser.add_argument('--app', default='/Applications/Open Design.app')
    args = parser.parse_args()
    cli = shutil.which(args.cli or args.agent)
    if not cli:
        parser.error('CLI executable not found')
    app = Path(args.app).expanduser().resolve()
    expected = sum(p.is_dir() and (p / 'SKILL.md').is_file()
                   for p in (app / 'Contents/Resources/open-design/skills').iterdir()) + 2
    with tempfile.TemporaryDirectory(prefix='opendesign-cli-check-') as temporary:
        work = Path(temporary).resolve()
        source = work / 'open-design-plugin'
        source.mkdir()
        # Package only source inputs; never copy a configured plugin's local links.
        for name in ['plugin.json', '.codex-plugin', '.claude-plugin', '.agents',
                     'setup.sh', 'scripts', 'templates', '.gitignore']:
            src = SOURCE / name
            if src.is_dir():
                shutil.copytree(src, source / name, ignore=shutil.ignore_patterns('__pycache__'))
            else:
                shutil.copy2(src, source / name)
        shutil.copytree(SOURCE / 'skills/setup', source / 'skills/setup')
        env = dict(os.environ)
        host_dir = work / 'host'
        host_dir.mkdir()
        env['CODEX_HOME' if args.agent == 'codex' else 'CLAUDE_CONFIG_DIR'] = str(host_dir)

        def run(arguments):
            result = subprocess.run(arguments, env=env, cwd=work, text=True,
                                    capture_output=True, timeout=60)
            if result.returncode:
                raise RuntimeError(result.stdout + result.stderr)
            return result.stdout

        run([cli, 'plugin', 'marketplace', 'add', str(source)])
        if args.agent == 'codex':
            result = json.loads(run([cli, 'plugin', 'add', PLUGIN_ID, '--json']))
            installed = Path(result['installedPath'])
        else:
            run([cli, 'plugin', 'install', PLUGIN_ID])
            # Claude 2.1.278 loads relative-path local marketplaces in place.
            installed = source
        skills, servers = inspect(cli, args.agent, env, work)
        assert skills == ['open-design-plugin:setup'], skills
        assert not servers, servers
        print(f'{args.agent}: fresh install = setup only, no MCP')
        command = ['bash', str(installed / 'setup.sh'), '--agent', args.agent, '--app', str(app)]
        run(command)
        state = (installed / '.opendesign-setup.json').read_text()
        run(command)
        assert state == (installed / '.opendesign-setup.json').read_text()
        skills, servers = inspect(cli, args.agent, env, work)
        assert len(skills) == expected, (len(skills), expected)
        assert len(servers) == 1, servers
        if args.agent == 'codex':
            assert servers[0]['tools'], servers
        else:
            assert servers[0]['status'] == 'connected', servers
        print(f'{args.agent}: setup and repeat setup = {len(skills)} skills, 1 connected MCP')
        print('No model turn or artifact-writing tool was invoked; isolated files removed on exit.')


if __name__ == '__main__':
    main()
