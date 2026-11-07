"""Negative cases for the optional measurement adapter, not aesthetic tests."""
import importlib.util
import json
from pathlib import Path
import struct
import subprocess
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("motion_tools", ROOT / "shared/scripts/motion_tools.py")
motion = importlib.util.module_from_spec(spec)
spec.loader.exec_module(motion)


class StrictMotionMeasurements(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def frames(self, name, count=3, fps=25, width=80):
        folder = self.root / name
        folder.mkdir()
        for i in range(count):
            # Only the PNG header is read by the dimension preflight; real PNG
            # decoding is covered by the executed Bun integration fixture.
            (folder / (str(i).zfill(4) + ".png")).write_bytes(
                b"\x89PNG\r\n\x1a\n" + struct.pack(">I", 13) + b"IHDR" + struct.pack(">II", width, 60))
        (folder / "frames.json").write_text(json.dumps({"fps": fps, "count": count}))
        return folder

    def report(self):
        return {"frames": 3, "compared": 3, "offset": 0, "setupWarnings": [],
                "frameDetails": [{"mismatch": 0.0}] * 3,
                "motion": {"reference": {"first": 1}, "timingError":
                           {"startS": 0, "endS": 0, "durationS": 0, "peakS": 0}},
                "activity": {"reference": [0, .1, .1]}}

    def assess(self, report, fidelity="pixel-faithful"):
        return motion.assess(report, {"reference": {"count": 3}}, fidelity)

    def test_equal_full_frame_sets_are_comparable(self):
        a, b = self.frames("ref"), self.frames("clone")
        self.assertEqual(motion.comparable(a, b)["reference"]["count"], 3)

    def test_duplicate_options_rejected_before_running_or_creating_output(self):
        for args in [["--out", "fresh", "--out", "existing"],
                     ["--ref=checked", "--ref", "unchecked"],
                     ["--clone", "checked", "--clone=unchecked"]]:
            with self.subTest(args=args), self.assertRaisesRegex(ValueError, "Duplicate option"):
                motion.execute("compare", args)

    def test_capture_time_and_output_identity_can_differ(self):
        for name, time in [("one", "yesterday"), ("two", "today")]:
            parent = self.root / name; parent.mkdir()
            self.frames(name + "-frames").rename(parent / "frames")
            (parent / "capture.json").write_text(json.dumps(
                {"url": name, "out": name, "capturedAt": time, "fps": 25}))
        self.assertEqual(motion.comparable(self.root / "one/frames", self.root / "two/frames")
                         ["reference"]["count"], 3)

    def test_capture_options_cover_settings_omitted_by_upstream_metadata(self):
        for name, steps in [("one", "12"), ("two", "20")]:
            parent = self.root / name; parent.mkdir()
            self.frames(name + "-frames").rename(parent / "frames")
            (parent / "capture.json").write_text('{"fps":25}')
            (parent / "motion-receipt.json").write_text(json.dumps(
                {"capture_options": {"--scroll-steps": steps}}))
        with self.assertRaisesRegex(ValueError, "command options differ"):
            motion.comparable(self.root / "one/frames", self.root / "two/frames")

    def test_missing_tail_and_wrong_fps_or_size_are_rejected(self):
        for key, kwargs in [("tail", {"count": 2}), ("fps", {"fps": 30}), ("size", {"width": 90})]:
            with self.subTest(key=key):
                a, b = self.frames("ref-" + key), self.frames("clone-" + key, **kwargs)
                with self.assertRaisesRegex(ValueError, "Capture mismatch"):
                    motion.comparable(a, b)

    def test_missing_middle_is_not_hidden_by_renaming(self):
        a = self.frames("gap")
        (a / "0001.png").rename(a / "0003.png")
        with self.assertRaisesRegex(ValueError, "frame indices"):
            motion.frame_set(a)

    def test_missing_fps_is_not_guessed(self):
        a = self.frames("no-fps")
        (a / "frames.json").write_text('{"count":3}')
        with self.assertRaisesRegex(ValueError, "fps"):
            motion.frame_set(a)

    def test_capture_configuration_change_is_not_a_warning_only(self):
        a, b = self.frames("ref"), self.frames("clone")
        # Capture metadata normally lives above frames/; use two separate parents.
        ca = self.root / "one"; cb = self.root / "two"
        ca.mkdir(); cb.mkdir()
        a.rename(ca / "frames"); b.rename(cb / "frames")
        (ca / "capture.json").write_text('{"url":"ref","reducedMotion":"reduce"}')
        (cb / "capture.json").write_text('{"url":"clone","reducedMotion":"no-preference"}')
        with self.assertRaisesRegex(ValueError, "settings differ"):
            motion.comparable(ca / "frames", cb / "frames")

    def test_partial_overlap_and_alignment_cannot_pass(self):
        for update in [{"compared": 2}, {"offset": 5}]:
            r = self.report(); r.update(update)
            self.assertEqual(self.assess(r)["metric_result"], "FAIL")

    def test_mean_does_not_hide_worst_or_resting_frame(self):
        for values in [[0, .051, 0], [.006, 0, 0]]:
            r = self.report();r["frameDetails"] = [{"mismatch": v} for v in values]
            self.assertEqual(self.assess(r)["metric_result"], "FAIL")

    def test_peak_timing_is_checked(self):
        r = self.report(); r["motion"]["timingError"]["peakS"] = .2
        self.assertEqual(self.assess(r)["metric_result"], "FAIL")

    def test_upstream_green_does_not_override_missing_measurements(self):
        r = self.report();r["pass"] = {"pixels": True, "timing": True};r["frameDetails"] = []
        self.assertEqual(self.assess(r)["metric_result"], "FAIL")

    def test_valid_measurements_never_issue_loop_acceptance(self):
        result = self.assess(self.report())
        self.assertEqual(result["metric_result"], "MEASUREMENTS_WITHIN_LIMITS")
        self.assertEqual(result["loop_acceptance"], "UNASSESSED")

    def test_static_reference_does_not_prove_motion(self):
        r = self.report();r["motion"]["reference"]["first"] = -1
        self.assertEqual(self.assess(r, "motion-faithful")["metric_result"], "FAIL")

    def test_input_changed_during_backend_cannot_pass(self):
        a, b = self.frames("ref"), self.frames("clone")
        out = self.root / "comparison"

        def backend(command, **kwargs):
            (out / "report.json").write_text(json.dumps(self.report()))
            (b / "0000.png").write_bytes((b / "0000.png").read_bytes() + b"changed")
            return subprocess.CompletedProcess(command, 0, stdout="", stderr="")

        with patch.object(motion.shutil, "which", return_value="fixture-bun"), \
             patch.object(motion.subprocess, "run", side_effect=backend):
            code = motion.execute("compare", ["--ref", str(a), "--clone", str(b), "--out", str(out)])
        receipt = json.loads((out / "motion-receipt.json").read_text())
        self.assertEqual(code, 2)
        self.assertFalse(receipt["inputs_unchanged"])
        self.assertEqual(receipt["assessment"]["metric_result"], "FAIL")
        self.assertEqual(receipt["loop_acceptance"], "UNASSESSED")


if __name__ == "__main__":
    unittest.main()
