import contextlib
import importlib.util
import io
import json
from pathlib import Path
import shutil
import tempfile
import unittest

SOURCE = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('setup', SOURCE / 'scripts/setup.py')
setup = importlib.util.module_from_spec(spec)
spec.loader.exec_module(setup)


class SetupTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'plugin space'
        self.root.mkdir()
        shutil.copytree(SOURCE / 'templates', self.root / 'templates')
        (self.root / 'skills/setup').mkdir(parents=True)
        self.app = Path(self.temp.name) / 'Open Design.app'
        self.resources = self.app / 'Contents/Resources/open-design'
        for folder in ('skills/example', 'design-systems', 'design-templates'):
            (self.resources / folder).mkdir(parents=True)
        (self.resources / 'skills/example/SKILL.md').write_text('local content')
        self.cli = self.app / 'Contents/Resources/app/prebundled/daemon/daemon-cli.mjs'
        self.cli.parent.mkdir(parents=True)
        self.cli.write_text('// fixture')

    def run_setup(self, dry_run=False):
        with contextlib.redirect_stdout(io.StringIO()):
            setup.configure(self.root, self.app, '/node path/node', dry_run)

    def test_fresh_install_and_idempotence(self):
        self.run_setup()
        first = (self.root / setup.STATE).read_text()
        self.run_setup()
        self.assertEqual(first, (self.root / setup.STATE).read_text())
        self.assertTrue((self.root / 'skills/example').is_symlink())
        self.assertEqual((self.root / 'skills/example/SKILL.md').read_text(), 'local content')
        config = json.loads((self.root / 'mcp_config.json').read_text())
        self.assertEqual(config['mcpServers']['open-design']['args'][0], str(self.cli))
        self.assertIn(str(self.root), (self.root / 'rules/AGENTS.md').read_text())

    def test_missing_resources_and_dry_run_write_nothing(self):
        self.run_setup(dry_run=True)
        self.assertFalse((self.root / setup.STATE).exists())
        self.assertFalse((self.root / 'design-systems').exists())
        shutil.rmtree(self.resources / 'design-templates')
        with self.assertRaises(ValueError):
            self.run_setup()
        self.assertFalse((self.root / 'skills/example').exists())

    def test_preserve_unmanaged_content(self):
        target = self.root / 'skills/example'
        target.mkdir()
        (target / 'mine').write_text('keep')
        with self.assertRaises(ValueError):
            self.run_setup()
        self.assertEqual((target / 'mine').read_text(), 'keep')
        self.assertFalse((self.root / 'mcp_config.json').exists())

    def test_preserve_modified_generated_content(self):
        self.run_setup()
        target = self.root / 'mcp_config.json'
        target.write_text('custom config')
        with self.assertRaises(ValueError):
            self.run_setup()
        self.assertEqual(target.read_text(), 'custom config')

    def test_relocation_and_removed_skills(self):
        self.run_setup()
        old_app = self.app
        self.app = old_app.with_name('Moved App.app')
        old_app.rename(self.app)
        shutil.rmtree(self.app / 'Contents/Resources/open-design/skills/example')
        new_skill = self.app / 'Contents/Resources/open-design/skills/new'
        new_skill.mkdir()
        (new_skill / 'SKILL.md').write_text('new')
        self.run_setup()
        self.assertFalse((self.root / 'skills/example').is_symlink())
        self.assertEqual((self.root / 'skills/new').resolve(), new_skill.resolve())
        self.assertTrue((self.root / 'design-systems').is_dir())

    def test_refuse_symlinked_parent(self):
        outside = Path(self.temp.name) / 'outside'
        outside.mkdir()
        (self.root / 'rules').symlink_to(outside, target_is_directory=True)
        with self.assertRaises(ValueError):
            self.run_setup()
        self.assertEqual(list(outside.iterdir()), [])

    def test_legacy_cli_and_ambiguity(self):
        self.cli.unlink()
        chunks = self.cli.parent / 'chunks'
        chunks.mkdir()
        (chunks / 'cli-one.mjs').write_text('// fixture')
        self.run_setup()
        (chunks / 'cli-two.mjs').write_text('// fixture')
        with self.assertRaises(ValueError):
            self.run_setup()

    def test_reserved_skill_conflict(self):
        (self.resources / 'skills/setup').mkdir()
        (self.resources / 'skills/setup/SKILL.md').write_text('conflict')
        with self.assertRaises(ValueError):
            self.run_setup()
        self.assertFalse((self.root / setup.STATE).exists())


if __name__ == '__main__':
    unittest.main()
