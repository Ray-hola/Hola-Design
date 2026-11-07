#!/usr/bin/env python3
"""Exercise the integrity exit gate in every scene branch: python3 -m unittest discover tests"""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import struct
import subprocess
import sys
import tempfile
import unittest
import zlib

REPO = Path(__file__).resolve().parents[1]
SCENES = ("ppt", "ui", "web")
CONTEXTS = ("wide", "phone")
ASPECTS = {"content": "detail", "continuity": "relation", "layering": "relation", "whole": "whole"}


def load(scene):
    scripts = REPO / "skills" / (scene + "-design-distill") / "scripts"
    sys.path.insert(0, str(scripts))
    try:
        spec = importlib.util.spec_from_file_location("loop_tools_" + scene, scripts / "loop_tools.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    finally:
        sys.path.pop(0)
    return module


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build(tools, root):
    spec = tools.checklist()
    for name, body in {"src.html": "<svg/>", "out.jpg": "export", "wide.png": "capture-wide", "phone.png": "capture-phone"}.items():
        (root / name).write_text(body)
    profile = {"scene": spec["scene"], "brief": "fixture"}
    journal = tools.initial(profile, spec)
    revision = tools.coverage_tools.snapshot(root, ["out.jpg", "src.html"])
    journal["revisions"], journal["delivery_revision"] = [revision], revision["id"]
    journal["review_scope"] = {"claim": "local", "summary": "Fixture cover", "subjects": ["field", "title"],
                               "contexts": list(CONTEXTS), "dimensions": {"design": ["integrity"]}}
    rendered = {f["path"]: f["sha256"] for f in revision["files"]}
    journal["review_plan"], journal["evidence"] = [], []
    for context in CONTEXTS:
        plans = []
        for aspect, level in ASPECTS.items():
            pid = aspect + "-" + context
            plans.append(pid)
            journal["review_plan"].append({"id": pid, "loop": "design", "dimension": "integrity", "subjects": ["field", "title"],
                                           "parts": ["curve", "title"], "context": context, "method": "visual", "level": level,
                                           "criterion": "Objects remain complete and intended"})
        journal["evidence"].append({"id": "e-" + context, "locator": context + ".png", "observed": True, "notes": "Viewed",
                                    "revision_id": revision["id"], "file": context + ".png", "sha256": sha(root / (context + ".png")),
                                    "method": "visual", "context": context, "inspection": "inspected", "coverage_ids": plans,
                                    "rendered_from": rendered, "observations": {p: "Observed at " + context for p in plans}})
    for benchmark in journal["benchmarks"]:
        if benchmark["id"] == "design.integrity":
            benchmark.update(criterion="Nothing lost or interrupted", references=["brief"])
    journal["rounds"] = [{"id": "r1", "loop": "design", "checks": [{"dimension": "integrity", "status": "passed", "notes": "Inspected",
                                                                    "evidence_ids": ["e-wide", "e-phone"]}]}]
    both = ["e-wide", "e-phone"]
    relations = ["continuity-wide", "continuity-phone"]
    assessment = tools.exit_template(journal)
    assessment["gates"]["intent"].update(status="pass", reason="Serves the brief", evidence_ids=both)
    assessment["gates"]["convergence"].update(status="pass", reason="Nothing open", evidence_ids=both)
    assessment["gates"]["quality"].update(status="pass", reason="The relation carries it", evidence_ids=both,
                                          weakest_subject="title", plan_ids=relations)
    assessment["gates"]["challenge"].update(status="pass", reason="Tested", evidence_ids=both, objection="The curve breaks",
                                            response="Checked at each size",
                                            tests=[{"plan_ids": relations, "evidence_ids": both, "reject_if": "A visible gap",
                                                    "observation": "No gap", "result": "refuted", "method": "direct"}])
    checks = [{"id": a + "-" + c, "aspect": a, "context": c, "item_ids": ["ground", "curve", "title"], "plan_ids": [a + "-" + c],
               "evidence_ids": ["e-" + c], "observation": "Viewed " + a + " at " + c, "result": "closed"} for c in CONTEXTS for a in ASPECTS]
    assessment["gates"]["integrity"].update(
        status="pass", reason="Every object holds", evidence_ids=both,
        inventory=[{"id": "ground", "role": "ground", "subject": "field", "summary": "Paper background"},
                   {"id": "curve", "role": "graphic", "subject": "field", "summary": "Open curve"},
                   {"id": "title", "role": "content", "subject": "title", "summary": "Wordmark"}],
        checks=checks, treatments=[],
        exports=[{"output": "out.jpg", "sources": ["src.html"], "method": "Rendered and compared", "plan_ids": ["whole-wide"],
                  "evidence_ids": ["e-wide"], "observation": "Export matches the source composition", "result": "matches"}])
    journal["exit_assessment"] = assessment
    return journal, profile


class IntegrityGate(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.addCleanup(self.temporary.cleanup)

    def outcome(self, scene, change=None):
        tools = load(scene)
        journal, profile = build(tools, self.root)
        if change:change(journal, tools)
        journal["exit_assessment"]["review_sha256"] = tools.review_fingerprint(journal)
        return tools.validate(journal, tools.checklist(), profile, self.root)["loop_exit"]

    def assertState(self, change, expected, fragment=None):
        for scene in SCENES:
            with self.subTest(scene=scene):
                signal = self.outcome(scene, change)
                self.assertEqual(signal["state"], expected, signal["reasons"])
                if fragment:
                    self.assertTrue(any(fragment in r for r in signal["reasons"]), signal["reasons"])

    @staticmethod
    def gate(journal):
        return journal["exit_assessment"]["gates"]["integrity"]

    def test_complete_record_passes(self):
        self.assertState(None, "PASS")

    def test_justified_crossing_overlap_rotation_and_clip_pass(self):
        def change(journal, _):
            self.gate(journal)["treatments"] = [
                {"id": kind, "kind": kind, "item_ids": ["curve", "title"], "intent": "The curve binds the two words",
                 "must_preserve": "The wordmark stays legible", "reject_if": "A letter becomes ambiguous",
                 "results": [{"context": c, "plan_ids": ["layering-" + c], "evidence_ids": ["e-" + c], "result": "holds",
                              "observation": "Every letter stays recognisable at " + c} for c in CONTEXTS]}
                for kind in ("crossing", "overlap", "rotation", "clip")]
        self.assertState(change, "PASS")

    def test_intent_alone_does_not_pass(self):
        def change(journal, _):
            self.gate(journal)["treatments"] = [{"id": "t", "kind": "crossing", "item_ids": ["curve"], "intent": "Intentional design"}]
        self.assertState(change, "UNVERIFIED", "stated intent alone")

    def test_repeating_intent_as_observation_does_not_pass(self):
        def change(journal, _):
            self.gate(journal)["treatments"] = [
                {"id": "t", "kind": "crossing", "item_ids": ["curve"], "intent": "Intentional", "must_preserve": "Text", "reject_if": "Illegible",
                 "results": [{"context": c, "plan_ids": ["layering-" + c], "evidence_ids": ["e-" + c], "result": "holds", "observation": "Intentional"} for c in CONTEXTS]}]
        self.assertState(change, "UNVERIFIED", "observation of the effect")

    def test_treatment_that_fails_holds(self):
        def change(journal, _):
            self.gate(journal)["treatments"] = [
                {"id": "t", "kind": "crossing", "item_ids": ["curve"], "intent": "Binds the words", "must_preserve": "Text", "reject_if": "Illegible",
                 "results": [{"context": c, "plan_ids": ["layering-" + c], "evidence_ids": ["e-" + c], "result": "fails", "observation": "The n is lost"} for c in CONTEXTS]}]
        self.assertState(change, "HOLD", "does not hold")

    def test_defect_holds(self):
        def change(journal, _):
            self.gate(journal)["checks"][1].update(result="defect", observation="A rectangle interrupts the curve")
        self.assertState(change, "HOLD", "rectangle interrupts")

    def test_export_difference_holds(self):
        def change(journal, _):
            self.gate(journal)["exports"][0].update(result="differs", observation="Export predates the source")
        self.assertState(change, "HOLD", "differs from its source")

    def test_omitted_background_layer_fails(self):
        def change(journal, _):
            gate = self.gate(journal)
            gate["inventory"] = [i for i in gate["inventory"] if i["role"] != "ground"]
            for check in gate["checks"]:
                check["item_ids"].remove("ground")
        self.assertState(change, "UNVERIFIED", "background/ground")

    def test_unchecked_object_fails(self):
        def change(journal, _):
            self.gate(journal)["checks"][1]["item_ids"].remove("curve")
        self.assertState(change, "UNVERIFIED", "not checked")

    def test_omitted_display_size_fails(self):
        def change(journal, _):
            gate = self.gate(journal)
            gate["checks"] = [c for c in gate["checks"] if c["context"] != "phone"]
        self.assertState(change, "UNVERIFIED", "phone")

    def test_stale_revision_screenshot_fails(self):
        def change(journal, _):
            old = copy.deepcopy(journal["revisions"][0])
            old["files"][0]["sha256"] = "0" * 64
            old["id"] = load("ui").coverage_tools.digest(old["files"])
            journal["revisions"].append(old)
            journal["evidence"][0]["revision_id"] = old["id"]
        self.assertState(change, "UNVERIFIED", "stale revision")

    def test_relabelled_old_screenshot_fails(self):
        def change(journal, _):
            older = copy.deepcopy(journal["evidence"][0])
            older.update(id="e-older", rendered_from={"src.html": "0" * 64}, coverage_ids=[], observations={})
            journal["evidence"].append(older)
        self.assertState(change, "UNVERIFIED", "old screenshot")

    def test_capture_from_outdated_source_fails(self):
        def change(journal, _):
            journal["evidence"][1]["rendered_from"] = {"src.html": "0" * 64}
        self.assertState(change, "UNVERIFIED", "rendered_from")

    def test_edit_after_review_fails(self):
        def change(_, __):
            (self.root / "src.html").write_text("<svg>edited</svg>")
        self.assertState(change, "UNVERIFIED", "changed after review")

    def test_new_revision_without_recheck_fails(self):
        def change(journal, tools):
            (self.root / "src.html").write_text("<svg>edited</svg>")
            revision = tools.coverage_tools.snapshot(self.root, ["out.jpg", "src.html"])
            journal["revisions"].append(revision)
            journal["delivery_revision"] = revision["id"]
            journal["exit_assessment"]["revision_id"] = revision["id"]
        self.assertState(change, "UNVERIFIED", "stale revision")

    def test_export_not_inspected_from_file_fails(self):
        def change(journal, _):
            for evidence in journal["evidence"]:
                evidence["rendered_from"] = {k: v for k, v in evidence["rendered_from"].items() if k != "out.jpg"}
        self.assertState(change, "UNVERIFIED", "exported file itself")

    def test_earlier_pass_record_does_not_inherit(self):
        def change(journal, _):
            del journal["exit_assessment"]["gates"]["integrity"]
        self.assertState(change, "UNVERIFIED", "do not inherit")

    def test_earlier_journal_stays_readable_but_unaccepted(self):
        for scene in SCENES:
            with self.subTest(scene=scene):
                tools = load(scene)
                journal, profile = build(tools, self.root)
                journal["benchmarks"] = [b for b in journal["benchmarks"] if b["id"] != "design.integrity"]
                journal["review_plan"] = []
                journal["rounds"] = []
                del journal["exit_assessment"]["gates"]["integrity"]
                journal["exit_assessment"]["review_sha256"] = tools.review_fingerprint(journal)
                result = tools.validate(journal, tools.checklist(), profile, self.root)
                self.assertTrue(result["valid"], result["errors"])
                self.assertNotEqual(result["loop_exit"]["state"], "PASS")

    def test_source_only_review_is_not_asked_for_renders(self):
        tools = load("ui")
        journal, _ = build(tools, self.root)
        journal["review_scope"]["dimensions"] = {"distillation": ["fidelity"]}
        self.assertFalse(tools.coverage_tools.integrity_required(journal["review_scope"]))
        journal["review_scope"]["claim"] = "whole_deliverable"
        self.assertTrue(tools.coverage_tools.integrity_required(journal["review_scope"]))

    def test_template_asks_for_the_gate(self):
        tools = load("web")
        journal, _ = build(tools, self.root)
        gate = tools.exit_template(journal)["gates"]["integrity"]
        self.assertEqual(gate["status"], "unknown")
        self.assertEqual({"inventory", "checks", "treatments", "exports"} - set(gate), set())


class Friction(unittest.TestCase):
    """Each case repeats a failure met while reviewing the real README cover."""

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.addCleanup(self.temporary.cleanup)

    def test_rejection_names_the_coverage_gap(self):
        for scene in SCENES:
            with self.subTest(scene=scene):
                tools = load(scene)
                journal, profile = build(tools, self.root)
                journal["evidence"][0]["revision_id"] = "stale"
                journal["exit_assessment"]["review_sha256"] = tools.review_fingerprint(journal)
                reasons = tools.validate(journal, tools.checklist(), profile, self.root)["loop_exit"]["reasons"]
                self.assertTrue(any("Review requirement incomplete" in r for r in reasons), reasons)

    def test_integrity_plan_leaves_answers_open(self):
        for scene in SCENES:
            with self.subTest(scene=scene):
                tools = load(scene)
                journal = tools.initial({"scene": scene}, tools.checklist())
                journal["review_scope"] = {"claim": "local", "summary": "s", "subjects": ["a"], "contexts": ["wide", "phone"], "dimensions": {"design": []}}
                planned = tools.integrity_plan(journal)
                self.assertEqual(len(planned["review_plan"]), 8)
                self.assertTrue(all(p["criterion"] == "" for p in planned["review_plan"]))
                self.assertEqual(planned["review_scope"]["dimensions"]["design"], ["integrity"])
                self.assertEqual(len(tools.integrity_plan(planned)["review_plan"]), 8)
                checks = tools.exit_template(planned)["gates"]["integrity"]["checks"]
                self.assertEqual(len(checks), 8)
                self.assertTrue(all(c["result"] == "unknown" for c in checks))

    @staticmethod
    def png(path, rows):
        raw = b"".join(b"\x00" + bytes(v for pixel in row for v in pixel) for row in rows)
        chunk = lambda kind, body: struct.pack(">I", len(body)) + kind + body + struct.pack(">I", zlib.crc32(kind + body))
        path.write_bytes(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", len(rows[0]), len(rows), 8, 2, 0, 0, 0)) + chunk(b"IDAT", zlib.compress(raw)) + chunk(b"IEND", b""))

    def capture_module(self, scene):
        spec = importlib.util.spec_from_file_location("capture_" + scene, REPO / "skills" / (scene + "-design-distill") / "scripts/capture_artifact.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_black_band_is_flagged(self):
        varied = [[(x * 7 % 255, y * 3 % 255, 9) for x in range(40)] for y in range(36)]
        self.png(self.root / "band.png", varied + [[(0, 0, 0)] * 40] * 4)
        self.png(self.root / "full.png", varied)
        for scene in SCENES:
            module = self.capture_module(scene)
            self.assertEqual(module.edge_bands(self.root / "band.png")["flat_edge_bands"], {"bottom": 4})
            self.assertEqual(module.edge_bands(self.root / "full.png")["flat_edge_bands"], {})

    def test_missing_font_refuses_the_capture(self):
        module = self.capture_module("ui")
        try:
            module.find_chrome()
        except ValueError:
            self.skipTest("No Chrome or Chromium")
        page = self.root / "page.html"
        page.write_text("<!doctype html><meta charset='utf-8'><p>x</p>")
        with self.assertRaisesRegex(ValueError, "fonts did not load"):
            module.capture(page, self.root / "shot.png", 300, 200, require_fonts=["Not A Real Family"])
        self.assertFalse((self.root / "shot.png").exists())

    def test_broken_image_refuses_the_capture_and_good_relative_image_passes(self):
        module = self.capture_module("ui")
        try:
            module.find_chrome()
        except ValueError:
            self.skipTest("No Chrome or Chromium")
        self.png(self.root / "real.png", [[(x * 7 % 255, y * 3 % 255, 9) for x in range(40)] for y in range(36)])
        (self.root / "bad.html").write_text("<body><img src='nope.png'>")
        with self.assertRaisesRegex(ValueError, "images failed"):
            module.capture(self.root / "bad.html", self.root / "bad.png", 300, 200)
        (self.root / "good.html").write_text("<body style='margin:0'><img src='real.png' width=300 height=200>")
        self.assertEqual(module.capture(self.root / "good.html", self.root / "good.png", 300, 200)["flat_edge_bands"], {})
        self.assertEqual([f.name for f in self.root.iterdir() if f.name.startswith(".capture-")], [])


class GeneratedSkill(unittest.TestCase):
    def test_package_carries_a_working_gate(self):
        for scene in SCENES:
            with self.subTest(scene=scene), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                profile = {"scene": scene, "identity": {"name": "Fixture"},
                           "sources": [{"id": "s1", "kind": "file", "locator": "fixture", "access": "local"}],
                           "evidence": [{"id": "e1", "source_id": "s1", "location": "top", "method": "inspection", "status": "observed", "value": "fixture"}]}
                (root / "profile.json").write_text(json.dumps(profile))
                scripts = REPO / "skills" / (scene + "-design-distill") / "scripts"
                run = subprocess.run([sys.executable, "-B", str(scripts / "profile_tools.py"), "package", str(root / "profile.json"),
                                      "--name", "fixture-" + scene, "--out", str(root / "out")], capture_output=True, text=True)
                self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
                skill = root / "out" / ("fixture-" + scene)
                # Check the installed artifact, not only the source-tree links.
                for document in skill.rglob("*.md"):
                    content = document.read_text()
                    links = re.findall(r"\]\(([^\s)]+)\)", content)
                    if document.name == "SKILL.md":
                        links += re.findall(r"`(references/[^`\s]+\.(?:md|json))`", content)
                    for link in links:
                        if ":" not in link and not link.startswith("#"):
                            self.assertTrue((document.parent / link.split("#")[0]).is_file(),
                                            str(document.relative_to(skill)) + ": " + link)
                for command in [
                    ["kit.py", "init", "--out", str(root / "task")],
                    ["kit.py", "search", "typography"],
                    ["principles.py", "search", "typography", "--scene", scene],
                ]:
                    run = subprocess.run([sys.executable, "-B", str(skill / "scripts" / command[0]), *command[1:]],
                                         capture_output=True, text=True)
                    self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
                self.assertTrue((root / "task/preview.html").is_file())
                self.assertIn("integrity", (skill / "SKILL.md").read_text())
                self.assertIn("Integrity gate", (skill / "references/loop/loop-exit.md").read_text())
                self.assertTrue((skill / "scripts/capture_artifact.py").is_file())
                self.assertTrue((skill / "scripts/motion_tools.py").is_file())
                self.assertTrue((skill / "references/toolkit/motion-reconstruction.md").is_file())
                vendor = skill / "vendor/reanimate"
                manifest = json.loads((vendor / "UPSTREAM.json").read_text())
                self.assertEqual(manifest["license"], "MIT")
                self.assertEqual({str(p.relative_to(vendor)) for p in vendor.rglob("*") if p.is_file()},
                                 {item["path"] for item in manifest["files"]} | {"UPSTREAM.json"})
                for item in manifest["files"]:
                    self.assertEqual(sha(vendor / item["path"]), item["sha256"])
                self.assertEqual(sha(skill / "LICENSE-APACHE"), sha(REPO / "LICENSE"))
                self.assertIn("Ray-hola", (skill / "NOTICE").read_text())
                if scene != "ppt":
                    run = subprocess.run([sys.executable, "-B", str(scripts / "profile_tools.py"), "package", str(root / "profile.json"),
                                          "--name", "catalog-" + scene, "--out", str(root / "out"), "--with-catalog"], capture_output=True, text=True)
                    self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
                    self.assertTrue((root / "out" / ("catalog-" + scene) / "vendor/ui-ux-pro-max/LICENSE").is_file())
                run = subprocess.run([sys.executable, "-B", str(skill / "scripts/loop_tools.py"), "init", str(skill / "references/profile.json"),
                                      "--out", str(root / "review.json")], capture_output=True, text=True)
                self.assertEqual(run.returncode, 0, run.stderr)
                journal = json.loads((root / "review.json").read_text())
                self.assertTrue(any(b["id"] == "design.integrity" for b in journal["benchmarks"]))
                run = subprocess.run([sys.executable, "-B", str(skill / "scripts/loop_tools.py"), "exit-template", str(root / "review.json")],
                                     capture_output=True, text=True)
                self.assertIn("integrity", json.loads(run.stdout)["gates"])
                run = subprocess.run([sys.executable, "-B", str(skill / "scripts/loop_tools.py"), "finish", str(root / "review.json"),
                                      "--profile", str(skill / "references/profile.json")], capture_output=True, text=True)
                self.assertEqual(run.returncode, 2, run.stdout + run.stderr)


class BranchSync(unittest.TestCase):
    def test_scene_copies_match_shared_source(self):
        run = subprocess.run([sys.executable, "-B", str(REPO / "scripts/sync_shared.py"), "--check"], capture_output=True, text=True)
        self.assertEqual(run.returncode, 0, run.stdout)
        self.assertTrue((REPO / "shared/references/loop/loop-exit.md").is_file())

    def test_loop_gate_precedes_extraction(self):
        for scene in SCENES:
            with self.subTest(scene=scene):
                text = (REPO / "skills" / (scene + "-design-distill") / "SKILL.md").read_text()
                self.assertIn("## LOOP gate", text)
                self.assertLess(text.index("## LOOP gate"), text.index("## Distillation method"))
                self.assertLess(text.index("## LOOP gate"), text.index("## 1."))

    def test_skills_hold_no_book_index_or_packaging_converter(self):
        banned_paths = ["scripts/convert-design-system.mjs"]
        banned_text = ["pdf_pages"]
        for name in ["design-distill", "ppt-design-distill", "ui-design-distill", "web-design-distill"]:
            skill = REPO / "skills" / name
            for path in banned_paths:
                self.assertFalse((skill / path).exists(), name + "/" + path)
            for path in skill.rglob("*"):
                if path.is_file() and path.suffix in {".md", ".json", ".py", ".yaml", ".csv"}:
                    text = path.read_text(encoding="utf-8", errors="ignore")
                    for term in banned_text:
                        self.assertNotIn(term, text, str(path))

    def test_bundled_catalog_keeps_its_license_and_is_declared(self):
        for name in ["ui-design-distill", "web-design-distill"]:
            vendor = REPO / "skills" / name / "vendor/ui-ux-pro-max"
            self.assertTrue((vendor / "LICENSE").is_file())
            self.assertTrue((vendor / "UPSTREAM.json").is_file())
        for readme in ["README.md", "README.zh-CN.md"]:
            self.assertIn("vendor/ui-ux-pro-max", (REPO / readme).read_text(encoding="utf-8"))

    def test_every_skill_carries_the_license(self):
        for name in [s + "-design-distill" for s in SCENES] + ["design-distill"]:
            with self.subTest(name=name):
                self.assertEqual(sha(REPO / "skills" / name / "LICENSE-APACHE"), sha(REPO / "LICENSE"))
                self.assertIn("Apache License", (REPO / "skills" / name / "NOTICE").read_text())

    def test_every_scene_requires_integrity(self):
        for scene in SCENES:
            data = json.loads((REPO / "skills" / (scene + "-design-distill") / "references/loop/loop-checklist.json").read_text())
            self.assertTrue(any(d["id"] == "integrity" and d["required"] for d in data["design"]), scene)


if __name__ == "__main__":
    unittest.main()
