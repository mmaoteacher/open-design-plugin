#!/usr/bin/env python3
"""Connect this plugin to locally installed Open Design resources."""
import argparse
import json
import os
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parent.parent
STATE = '.opendesign-setup.json'


def configure(root, app, node, dry_run=False):
    resources = app / 'Contents/Resources/open-design'
    for name in ('skills', 'design-systems', 'design-templates'):
        if not (resources / name).is_dir():
            raise ValueError(f'Missing local resource: {resources / name}')
    cli = app / 'Contents/Resources/app/prebundled/daemon/daemon-cli.mjs'
    if not cli.is_file():
        chunks = sorted(cli.parent.glob('chunks/cli-*.mjs'))
        if len(chunks) != 1:
            raise ValueError('Cannot identify one daemon CLI; update Open Design or check its installation.')
        cli = chunks[0]
    skills = sorted(p for p in (resources / 'skills').iterdir()
                    if p.is_dir() and (p / 'SKILL.md').is_file())
    if not skills:
        raise ValueError('No local SKILL.md files found.')
    reserved = {'setup', 'opendesign-systems'}
    if any(p.name in reserved for p in skills):
        raise ValueError('Local skills conflict with setup or opendesign-systems.')
    links = {f'skills/{p.name}': str(p) for p in skills}
    links.update({name: str(resources / name) for name in ('design-systems', 'design-templates')})
    files = {
        'mcp_config.json': json.dumps({'mcpServers': {'open-design': {
            'type': 'command', 'command': node,
            'args': [str(cli), 'mcp', '--daemon-url', 'http://127.0.0.1:7456']
        }}}, indent=2) + '\n',
        'rules/AGENTS.md': (root / 'templates/AGENTS.md').read_text().replace(
            '~/.gemini/config/plugins/open-design-plugin', str(root)),
        'skills/opendesign-systems/SKILL.md': (root / 'templates/design-systems.md').read_text().replace(
            '~/.gemini/config/plugins/open-design-plugin', str(root)),
    }
    state_path = root / STATE
    previous = json.loads(state_path.read_text()) if state_path.exists() else {'links': {}, 'files': {}}
    # Only touch paths managed by this installer; never follow destination symlinks.
    all_names = set(links) | set(files) | set(previous['links']) | set(previous['files'])
    for name in all_names:
        relative = Path(name)
        if relative.is_absolute() or '..' in relative.parts or name == STATE:
            raise ValueError(f'Invalid managed path: {name}')
        dest = root / relative
        for parent in dest.parents:
            if parent == root:
                break
            if parent.is_symlink() or (parent.exists() and not parent.is_dir()):
                raise ValueError(f'Unsafe destination directory: {parent}')
        if dest.is_symlink():
            if str(dest.readlink()) != previous['links'].get(name):
                raise ValueError(f'Unmanaged or modified symlink: {dest}')
        elif dest.exists():
            if not dest.is_file() or dest.read_text() != previous['files'].get(name):
                raise ValueError(f'Unmanaged or modified file: {dest}; move it aside and rerun setup.')
    print(f'Open Design: {app}')
    print(f'Skills: {len(skills)} local skills + opendesign-systems + setup')
    print(f'MCP entrypoint: {cli}')
    if dry_run:
        print('Dry run: validation passed; no files changed.')
        return
    for name in set(previous['links']) - set(links):
        (root / name).unlink(missing_ok=True)
    for name in set(previous['files']) - set(files):
        (root / name).unlink(missing_ok=True)
    for name, target in links.items():
        dest = root / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        if dest.is_symlink():
            dest.unlink()
        dest.symlink_to(target, target_is_directory=True)
    for name, content in files.items():
        dest = root / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(content)
    state_path.write_text(json.dumps({'app': str(app), 'links': links, 'files': files}, indent=2) + '\n')
    print('Configuration complete. Open Open Design.app and restart agy to reload skills and MCP.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--app', help='Explicit Open Design.app path (also OPEN_DESIGN_APP_PATH)')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    explicit = args.app or os.environ.get('OPEN_DESIGN_APP_PATH')
    candidates = [Path(explicit).expanduser()] if explicit else [
        Path('/Applications/Open Design.app'), Path.home() / 'Applications/Open Design.app']
    app = next((p.resolve() for p in candidates if p.is_dir()), None)
    if app is None:
        raise ValueError('Open Design.app not found. Install it locally or supply --app /path/to/Open Design.app.')
    node = shutil.which('node')
    if not node:
        raise ValueError('Node.js is required; install it and rerun setup.')
    configure(ROOT, app, node, args.dry_run)


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, KeyError) as exc:
        print(f'Setup failed: {exc}', file=sys.stderr)
        sys.exit(1)
