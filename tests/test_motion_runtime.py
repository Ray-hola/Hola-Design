"""Cold setup and cache invariants; the runtime workflow executes real binaries."""
import importlib.util
import os
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
s = importlib.util.spec_from_file_location('runtime_test', ROOT / 'shared/scripts/motion_runtime.py')
r = importlib.util.module_from_spec(s); s.loader.exec_module(r)


class RuntimeBootstrap(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()

    def test_supported_targets_and_rejection(self):
        for system, machine, expected in [('Darwin','arm64','darwin-arm64'),('Darwin','x86_64','darwin-x64'),('Linux','aarch64','linux-arm64'),('Linux','x86_64','linux-x64'),('Windows','AMD64','windows-x64')]:
            self.assertEqual(r.target(system,machine),expected)
        with self.assertRaisesRegex(ValueError,'Unsupported'):r.target('Windows','ARM64')

    def test_cache_overlay_is_exact_and_tampering_is_preserved(self):
        with patch.object(r,'cached_engine',return_value=self.root/'engine'):
            engine = r.prepare_engine(); self.assertTrue(r.valid_engine(engine))
            p=engine/'scripts/lib.ts';p.write_text('tampered')
            self.assertFalse(r.valid_engine(engine))
            with self.assertRaisesRegex(ValueError,'differs'):r.prepare_engine()
            self.assertEqual(p.read_text(),'tampered')

    def test_ancestor_and_dangling_symlinks_cannot_escape_cache(self):
        if os.name=='nt':self.skipTest('symlink creation may require Windows administrator privileges')
        for kind in ['ancestor','dangling']:
            with self.subTest(kind=kind):
                engine=self.root/kind;engine.mkdir();outside=self.root/(kind+'-outside')
                if kind=='ancestor':
                    outside.mkdir();(engine/'scripts').symlink_to(outside,target_is_directory=True)
                else:
                    (engine/'scripts').mkdir();(engine/'scripts/bun.lock').symlink_to(outside)
                with patch.object(r,'cached_engine',return_value=engine),self.assertRaisesRegex(ValueError,'symlink'):
                    r.prepare_engine()
                self.assertFalse(outside.exists() and (outside.is_file() or any(outside.iterdir())))

    def test_missing_runtime_never_reports_ready(self):
        with patch.object(r,'bun_path',return_value=None):
            result=r.doctor(self.root/'absent',browser=True)
        self.assertFalse(result['ready']);self.assertFalse(result['dependencies'])

    def test_setup_without_browser_permission_does_not_install(self):
        with patch.object(r,'ensure_bun') as install,self.assertRaisesRegex(ValueError,'allow-browser'):
            r.setup()
        install.assert_not_called()

    def test_runtime_overlays_preserve_original_unicode(self):
        for name in ['scripts/lib.ts', 'scripts/capture.ts', 'scripts/sheet.ts']:
            original = (r.BUNDLE / name).read_bytes().decode('utf-8')
            overlay = r.runtime_bytes(name).decode('utf-8')
            self.assertEqual(''.join(c for c in original if ord(c) > 127),
                             ''.join(c for c in overlay if ord(c) > 127))


if __name__=='__main__':unittest.main()
