"""Verify ownership-aware synchronization with isolated scene trees."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest

REPO = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('shared_sync', REPO / 'scripts/sync_shared.py')
sync = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sync)


class SharedOwnership(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'shared').mkdir()
        (self.root / 'scripts').mkdir()
        (self.root / 'scripts/shared-manifest.json').write_text(json.dumps({'version': 1, 'files': {}}))
        (self.root / 'shared/common.md').write_text('old')
        self.assertEqual(self.run_sync(False), 0)
        for scene in sync.SCENES:
            (self.scene(scene) / 'specific.md').write_text(scene)

    def scene(self, name):
        return self.root / 'skills' / (name + '-design-distill')

    def run_sync(self, check):
        with contextlib.redirect_stdout(io.StringIO()):
            return sync.sync(check, self.root)

    def test_deleted_source_is_detected_and_only_owned_copies_are_removed(self):
        (self.root / 'shared/common.md').unlink()
        self.assertEqual(self.run_sync(True), 1)
        self.assertTrue((self.scene('ppt') / 'common.md').exists())
        self.assertEqual(self.run_sync(False), 0)
        for scene in sync.SCENES:
            self.assertFalse((self.scene(scene) / 'common.md').exists())
            self.assertEqual((self.scene(scene) / 'specific.md').read_text(), scene)
        self.assertEqual(self.run_sync(True), 0)

    def test_rename_removes_old_name_and_copies_new_name(self):
        (self.root / 'shared/common.md').rename(self.root / 'shared/renamed.md')
        self.assertEqual(self.run_sync(True), 1)
        self.assertEqual(self.run_sync(False), 0)
        for scene in sync.SCENES:
            self.assertFalse((self.scene(scene) / 'common.md').exists())
            self.assertEqual((self.scene(scene) / 'renamed.md').read_text(), 'old')

    def test_edited_retired_copy_blocks_all_mutation(self):
        (self.root / 'shared/common.md').unlink()
        (self.root / 'shared/new.md').write_text('new')
        (self.scene('ui') / 'common.md').write_text('user edit')
        manifest = (self.root / 'scripts/shared-manifest.json').read_bytes()
        self.assertEqual(self.run_sync(False), 1)
        self.assertEqual((self.scene('ui') / 'common.md').read_text(), 'user edit')
        self.assertEqual((self.root / 'scripts/shared-manifest.json').read_bytes(), manifest)
        for scene in sync.SCENES:
            self.assertTrue((self.scene(scene) / 'common.md').exists())
            self.assertFalse((self.scene(scene) / 'new.md').exists())

    def test_update_and_missing_copy_are_repaired(self):
        (self.root / 'shared/common.md').write_text('updated')
        (self.scene('web') / 'common.md').unlink()
        self.assertEqual(self.run_sync(True), 1)
        self.assertEqual(self.run_sync(False), 0)
        self.assertEqual(self.run_sync(True), 0)
        for scene in sync.SCENES:
            self.assertEqual((self.scene(scene) / 'common.md').read_text(), 'updated')

    def test_path_escape_and_symlink_are_rejected(self):
        (self.root / 'scripts/shared-manifest.json').write_text(json.dumps({'version': 1, 'files': {'../outside': 'x'}}))
        with self.assertRaises(ValueError):
            self.run_sync(False)
        (self.root / 'scripts/shared-manifest.json').write_text(json.dumps({'version': 1, 'files': {}}))
        (self.scene('ui') / 'common.md').unlink()
        (self.scene('ui') / 'common.md').symlink_to(self.root / 'shared/common.md')
        with self.assertRaises(ValueError):
            self.run_sync(False)
        self.assertEqual((self.root / 'shared/common.md').read_text(), 'old')


if __name__ == '__main__':
    unittest.main()
