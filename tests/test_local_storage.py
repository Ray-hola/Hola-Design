"""Local-only storage must stay outside publication and bounded cleanup."""
import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

REPO = Path(__file__).resolve().parents[1]


def module(name):
    spec = importlib.util.spec_from_file_location(name, REPO / 'scripts' / (name + '.py'))
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


class LocalStorage(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        (self.root / 'temp').mkdir()
        (self.root / 'private').mkdir()
        self.cleanup = module('clean_temp')
        self.now = 2000000000

    def old(self, path):
        os.utime(path, (self.now - 30 * 86400,) * 2)

    def file(self, relative):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text('keep contents')
        self.old(path)
        return path

    def test_preview_does_not_delete_and_apply_only_removes_old_temp(self):
        old = self.file('temp/old.txt')
        private = self.file('private/evidence.txt')
        recent = self.file('temp/recent.txt')
        os.utime(recent, (self.now,) * 2)
        result = self.cleanup.clean(self.root, now=self.now)
        self.assertEqual(result['eligible'], ['temp/old.txt'])
        self.assertTrue(old.exists())
        result = self.cleanup.clean(self.root, apply=True, now=self.now)
        self.assertEqual(result['deleted'], ['temp/old.txt'])
        self.assertTrue(private.exists() and recent.exists())

    def test_nested_protections_and_tracked_content(self):
        for name, marker in [('pinned', '.keep'), ('repo', '.git'), ('active', 'new.txt')]:
            path = self.file('temp/' + name + '/' + marker)
            if name == 'active':os.utime(path, (self.now,) * 2)
            self.old(path.parent)
        target = self.file('private/target')
        linked = self.root / 'temp/linkdir'
        linked.mkdir()
        (linked / 'link').symlink_to(target)
        self.old(linked)
        tracked = self.file('temp/tracked.txt')
        result = self.cleanup.clean(self.root, apply=True, now=self.now, tracked=['temp/tracked.txt'])
        self.assertEqual(result['deleted'], [])
        self.assertTrue(target.exists() and tracked.exists())
        self.assertEqual(len(result['skipped']), 5)

    def test_old_directory_removed_as_a_unit(self):
        child = self.file('temp/done/result.txt')
        self.old(child.parent)
        result = self.cleanup.clean(self.root, apply=True, now=self.now)
        self.assertEqual(result['deleted'], ['temp/done'])

    def test_root_pin_and_symlinked_temp(self):
        self.file('temp/old')
        self.file('temp/.keep')
        self.assertEqual(self.cleanup.clean(self.root, apply=True, now=self.now)['deleted'], [])
        (self.root / 'temp').rename(self.root / 'saved')
        (self.root / 'temp').symlink_to(self.root / 'private')
        with self.assertRaises(ValueError):self.cleanup.clean(self.root, apply=True, now=self.now)

    def test_publication_prunes_private_but_rejects_forced_tracking(self):
        scanner = module('check_repository')
        scanner.ROOT = self.root
        subprocess.run(['git', 'init', '-q', str(self.root)], check=True)
        (self.root / '.gitignore').write_text('/private/\n/temp/\n')
        self.file('private/raw.pdf')
        self.file('temp/raw.pdf')
        self.file('README.md')
        with contextlib.redirect_stdout(io.StringIO()):self.assertEqual(scanner.check(), 0)
        subprocess.run(['git', 'add', '-f', 'private/raw.pdf', 'temp/raw.pdf'], cwd=self.root, check=True)
        output = io.StringIO()
        with contextlib.redirect_stdout(output):self.assertEqual(scanner.check(), 1)
        errors = json.loads(output.getvalue())['errors']
        self.assertEqual(len(errors), 2)
        self.assertTrue(all('local-only content is tracked' in e for e in errors))

    def test_publication_excludes_worktree_git_metadata_file(self):
        scanner = module('check_repository')
        self.file('.git')
        self.file('README.md')
        self.assertEqual([p.relative_to(self.root).as_posix()
                          for p in scanner.publication_files(self.root)], ['README.md'])


if __name__ == '__main__':
    unittest.main()
