#!/usr/bin/env python3
"""Coverage and artifact-freshness checks. Does not certify a visual judgment."""
import hashlib
import json
from pathlib import Path
import re

METHODS = {"visual", "measurement", "interaction", "file", "semantic"}
LEVELS = {"whole", "detail", "relation"}
VISUAL_DIMENSIONS = {"typography", "whitespace", "hierarchy", "color", "visual", "render"}
INTEGRITY_ASPECTS = ("content", "continuity", "layering", "whole")


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def confined(root, relative):
    path = Path(relative)
    resolved = (root / path).resolve()
    if path.is_absolute() or ".." in path.parts or not resolved.is_relative_to(root.resolve()):
        raise ValueError("Review artifact must stay inside --artifact-root: " + str(relative))
    return resolved


def snapshot(root, paths):
    root = Path(root).resolve()
    if not paths or len(set(paths)) != len(paths):
        raise ValueError("Snapshot requires unique relative file paths")
    files = [{"path": p, "sha256": hashlib.sha256(confined(root, p).read_bytes()).hexdigest()} for p in sorted(paths)]
    return {"id": digest(files), "files": files}


def audit(journal, spec, artifact_root=None):
    errors, gaps = [], []
    if journal.get("version") == 1:
        return {"valid": True, "complete": False, "state": "legacy_unverified", "errors": [],
                "gaps": ["Legacy journal lacks coverage/inspection/artifact binding; retain its history but do not claim a complete current review"]}

    def text(x):
        return isinstance(x, str) and bool(x.strip())

    def strings(x):
        return isinstance(x, list) and bool(x) and all(text(v) for v in x) and len(set(x)) == len(x)

    def table(key):
        rows = journal.get(key, [])
        if not isinstance(rows, list) or any(not isinstance(x, dict) for x in rows):
            errors.append(key + " must be an array of objects");return {}
        ids = [r.get("id") for r in rows]
        if any(not text(x) for x in ids) or len(set(map(str, ids))) != len(ids):
            errors.append(key + " requires unique string ids");return {}
        return {x["id"]: x for x in rows}

    scope = journal.get("review_scope")
    if not isinstance(scope, dict) or not scope:
        return {"valid": True, "complete": False, "state": "not_planned", "errors": [], "gaps": ["Declare review_scope, review_plan and the final artifact revision before claiming coverage"]}
    for field in ["summary", "claim"]:
        if not text(scope.get(field)):errors.append("review_scope needs " + field)
    if scope.get("claim") not in {"local", "whole_deliverable"}:errors.append("Scope claim is local or whole_deliverable")
    for field in ["subjects", "contexts"]:
        if not strings(scope.get(field)):errors.append("Scope needs unique nonempty " + field)
    dimensions = scope.get("dimensions", {})
    if not isinstance(dimensions, dict) or not dimensions:
        errors.append("Scope needs dimensions grouped by loop");dimensions = {}
    for loop, dims in dimensions.items():
        known = {x["id"] for x in spec.get(loop, [])}
        if not strings(dims) or any(x not in known for x in dims):errors.append("Unknown/empty scoped dimensions in " + loop)
        if scope.get("claim") == "whole_deliverable" and isinstance(dims, list):
            if not {x["id"] for x in spec.get(loop, []) if x["required"]}.issubset(dims):
                errors.append("Whole-deliverable scope omitted required dimensions in " + loop)
    plan, revisions = table("review_plan"), table("revisions")
    subjects = scope.get("subjects", []) if isinstance(scope.get("subjects"), list) else []
    contexts = scope.get("contexts", []) if isinstance(scope.get("contexts"), list) else []
    for pid, item in plan.items():
        if not strings(item.get("subjects")) or any(x not in subjects for x in item.get("subjects", [])):errors.append(pid + ": unknown/missing subjects")
        if item.get("context") not in contexts:errors.append(pid + ": unknown context")
        if item.get("loop") not in dimensions or item.get("dimension") not in dimensions.get(item.get("loop"), []):errors.append(pid + ": dimension outside declared scope")
        if item.get("method") not in METHODS or item.get("level") not in LEVELS:errors.append(pid + ": declare method and whole/detail/relation level")
        if item.get("loop") == "design" and item.get("dimension") in VISUAL_DIMENSIONS and item.get("method") != "visual":errors.append(pid + ": a visual design judgment requires visual inspection")
        if not text(item.get("criterion")):errors.append(pid + ": concrete criterion required")
    for loop, dims in dimensions.items():
        if not isinstance(dims, list):continue
        for context in contexts:
            rows = [p for p in plan.values() if p.get("loop") == loop and p.get("context") == context]
            for dim in dims:
                if not any(p.get("dimension") == dim for p in rows):gaps.append(f"Unplanned dimension/context: {loop}/{dim}/{context}")
            for level in LEVELS:
                if not any(p.get("level") == level for p in rows):gaps.append(f"Unplanned {level} review: {loop}/{context}")
                if loop == "design" and any(d in VISUAL_DIMENSIONS or d == "responsive" for d in dims):
                    if not any(p.get("level") == level and p.get("method") == "visual" for p in rows):gaps.append(f"No actual visual {level} pass planned: {context}")
            for subject in subjects:
                if not any(subject in p.get("subjects", []) and p.get("level") != "whole" for p in rows):gaps.append(f"Subject only glanced at or unplanned: {subject}/{context}")
    for rid, rev in revisions.items():
        files = rev.get("files")
        good = isinstance(files, list) and bool(files) and all(isinstance(f, dict) and text(f.get("path")) and text(f.get("sha256")) for f in files)
        if not good or rid != digest(files):errors.append("Invalid artifact snapshot: " + rid)
    delivery = journal.get("delivery_revision")
    if delivery not in revisions:gaps.append("No known final delivery_revision")
    root = Path(artifact_root).resolve() if artifact_root is not None else None
    if root is None:
        gaps.append("Final artifact hashes not verified; pass --artifact-root")
    elif delivery in revisions:
        for entry in revisions[delivery].get("files", []):
            try:
                if hashlib.sha256(confined(root, entry["path"]).read_bytes()).hexdigest() != entry["sha256"]:
                    gaps.append("Final output changed after review: " + entry["path"])
            except (OSError, ValueError, KeyError) as e:errors.append(str(e))
    if spec.get("scene") == "web" and "responsive" in dimensions.get("design", []):
        widths = scope.get("viewport_widths", {})
        valid_widths = isinstance(widths, dict) and all(type(widths.get(c)) is int and widths[c] > 0 for c in contexts)
        if not valid_widths:
            gaps.append("Responsive scope needs actual viewport_widths for every declared context")
        else:
            values = {widths[c] for c in contexts}
            low, high = min(values), max(values)
            if high-low > 2 and not any(low < w < high for w in values):gaps.append("Responsive scope omitted an interior viewport")
            probes = set()
            if root is not None and delivery in revisions:
                for entry in revisions[delivery].get("files", []):
                    if Path(entry["path"]).suffix.lower() not in {".html", ".css", ".scss"}:continue
                    try:source = confined(root, entry["path"]).read_text(encoding="utf-8")
                    except (OSError, ValueError):continue
                    for header in re.findall(r"@media\b([^{}]+)\{", source, re.I):
                        for kind, boundary in re.findall(r"(min|max)-width\s*:\s*(\d+)px", header, re.I):
                            boundary = int(boundary)
                            pair = [boundary-1, boundary] if kind.lower() == "min" else [boundary, boundary+1]
                            probes.update(w for w in pair if low <= w <= high)
            missing = sorted(probes-values)
            if missing:gaps.append("Declared CSS transition probes missing: " + ", ".join(map(str, missing)))
    evidence = {e.get("id"): e for e in journal.get("evidence", []) if isinstance(e, dict) and text(e.get("id"))}
    latest = {}
    for round in journal.get("rounds", []):
        if not isinstance(round, dict):continue
        loop = round.get("loop")
        latest[loop] = round
        repair = round.get("repair")
        if repair is not None:
            impact = repair.get("impact", {}) if isinstance(repair, dict) else {}
            if not isinstance(impact, dict):impact = {}
            changed, affected = impact.get("subjects"), impact.get("contexts")
            if not strings(changed) or any(x not in subjects for x in changed or []):gaps.append("Repair lacks known changed subjects: " + str(round.get("id")));continue
            if not strings(affected) or any(x not in contexts for x in affected or []):gaps.append("Repair lacks known affected contexts: " + str(round.get("id")));continue
            expected = {pid for pid,p in plan.items() if p.get("loop") == loop and p.get("context") in affected and (p.get("level") == "whole" or any(s in p.get("subjects", []) for s in changed))}
            regressions = impact.get("regression_ids", [])
            if not isinstance(regressions, list) or not expected.issubset(set(map(str, regressions))):gaps.append("Repair did not plan affected detail/relations/whole regressions: " + str(round.get("id")))

    hash_results = {}

    def inspected(e, pid, item):
        if e.get("revision_id") != delivery:return False, "stale_revision"
        if e.get("context") != item.get("context"):return False, "wrong_context"
        if pid not in e.get("coverage_ids", []):return False, "not_targeted"
        if e.get("method") != item.get("method"):return False, "wrong_method"
        status = e.get("inspection")
        if item.get("method") == "visual" and status != "inspected":return False, "captured_not_inspected"
        if item.get("method") != "visual" and status not in {"inspected", "executed"}:return False, "not_executed"
        if not text(e.get("notes")):return False, "no_observation_notes"
        observations = e.get("observations", {})
        if not isinstance(observations, dict) or not text(observations.get(pid)):return False, "no_target_observation"
        path, sha = e.get("file"), e.get("sha256")
        if not text(path) or not text(sha):return False, "unbound_evidence_file"
        if root is None:return False, "artifact_root_unverified"
        key = (path, sha)
        if key not in hash_results:
            try:hash_results[key] = hashlib.sha256(confined(root, path).read_bytes()).hexdigest() == sha
            except (OSError, ValueError):hash_results[key] = False
        return (True, "inspected") if hash_results[key] else (False, "evidence_file_changed")

    cells = []
    for pid, item in plan.items():
        checks = latest.get(item.get("loop"), {}).get("checks", [])
        check = next((c for c in checks if isinstance(c, dict) and c.get("dimension") == item.get("dimension")), {})
        matched, reasons, matched_evidence = False, set(), []
        if check.get("status") == "passed":
            for eid in check.get("evidence_ids", []):
                e = evidence.get(eid, {})
                ok, why = inspected(e, pid, item)
                reasons.add(why)
                if ok:
                    matched = True;matched_evidence.append(eid)
        else:reasons.add("missing_or_unpassed_check")
        cells.append({"id": pid, "covered": matched, "evidence_ids": matched_evidence,
                      "reasons": [] if matched else sorted(reasons)})
        if not matched:gaps.append("Review requirement incomplete: " + pid)
    for ex in journal.get("experiments", []):
        if isinstance(ex, dict) and ex.get("decision") == "keep" and ex.get("candidate_revision") != delivery:
            gaps.append("Kept experiment does not bind the final candidate: " + str(ex.get("id")))
    complete = not errors and not gaps and bool(plan)
    return {"valid": not errors, "complete": complete,
            "state": ("complete_local" if scope.get("claim") == "local" else "complete_declared_deliverable") if complete else "incomplete",
            "claim": scope.get("claim"), "errors": errors, "gaps": gaps, "cells": cells,
            "meaning": "Checks declared coverage, inspection metadata and local hashes; cannot prove the inventory is exhaustive, inspection occurred, or a design judgment is correct."}


def integrity_required(scope):
    """Rendered work needs the gate; a source-only distillation review does not."""
    dimensions = scope.get("dimensions") if isinstance(scope, dict) else None
    return isinstance(scope, dict) and (scope.get("claim") == "whole_deliverable" or (isinstance(dimensions, dict) and "design" in dimensions))


def integrity_audit(journal, coverage, artifact_root=None):
    """Return PASS/HOLD/UNVERIFIED for declared objects, contexts and the final revision.

    Crossing, overlap, rotation and clipping stay allowed: each is judged by its
    stated intent and observed result. Records cannot prove honesty or exhaustiveness.
    """
    work, gaps = [], []
    scope = journal.get("review_scope") if isinstance(journal.get("review_scope"), dict) else {}
    assessment = journal.get("exit_assessment") if isinstance(journal.get("exit_assessment"), dict) else {}
    gates = assessment.get("gates") if isinstance(assessment.get("gates"), dict) else {}
    gate = gates.get("integrity") if isinstance(gates.get("integrity"), dict) else {}

    def text(x):
        return isinstance(x, str) and bool(x.strip())

    def ids(x):
        return x if isinstance(x, list) and all(isinstance(v, str) for v in x) else []

    def rows(key):
        value = gate.get(key)
        return [x for x in value if isinstance(x, dict)] if isinstance(value, list) else []

    def result():
        state = "HOLD" if work else "UNVERIFIED" if gaps else "PASS"
        return {"state": state, "reasons": work + gaps}

    if not gate:
        gaps.append("Integrity not established; earlier records do not inherit this gate")
        return result()
    subjects = scope.get("subjects") if isinstance(scope.get("subjects"), list) else []
    contexts = scope.get("contexts") if isinstance(scope.get("contexts"), list) else []
    delivery = journal.get("delivery_revision")
    revisions = {r.get("id"): r for r in journal.get("revisions", []) if isinstance(r, dict)}
    files = {f.get("path"): f.get("sha256") for f in revisions.get(delivery, {}).get("files", []) if isinstance(f, dict)}
    plan = {p.get("id"): p for p in journal.get("review_plan", []) if isinstance(p, dict)}
    evidence = {e.get("id"): e for e in journal.get("evidence", []) if isinstance(e, dict)}
    cells = {c.get("id"): c for c in coverage.get("cells", []) if c.get("covered")}
    root = Path(artifact_root).resolve() if artifact_root is not None else None
    for path, sha in files.items():
        try:
            if root is not None and hashlib.sha256(confined(root, path).read_bytes()).hexdigest() != sha:
                gaps.append("Final file changed after review; recheck it: " + str(path))
        except (OSError, ValueError, TypeError):gaps.append("Final file unavailable: " + str(path))

    def evidence_problem(eid):
        """Name why evidence cannot show the delivered bytes; None when it can."""
        e = evidence.get(eid)
        if not isinstance(e, dict):return "unknown evidence " + str(eid)
        if e.get("revision_id") != delivery:return "stale revision in " + eid
        sources = e.get("rendered_from")
        if not isinstance(sources, dict) or not sources:return "no rendered_from in " + eid
        if any(files.get(path) != sha for path, sha in sources.items()):return "rendered_from differs from the final revision in " + eid
        if root is None:return "artifact root unverified for " + eid
        try:
            if hashlib.sha256(confined(root, e["file"]).read_bytes()).hexdigest() != e["sha256"]:return "evidence file changed: " + eid
        except (OSError, ValueError, KeyError, TypeError):return "evidence file unavailable: " + eid
        # The same capture bytes recorded for other inputs are an old screenshot, whatever its label says.
        for other in evidence.values():
            if other is not e and other.get("sha256") == e.get("sha256") and other.get("rendered_from") != sources:
                return "capture bytes were recorded for other inputs (old screenshot): " + eid
        return None

    def bound(record, label, context=None, aspect=None):
        pids, refs = ids(record.get("plan_ids")), ids(record.get("evidence_ids"))
        if not pids or not refs:
            gaps.append(label + " needs plan_ids and evidence_ids");return False
        good = True
        for pid in pids:
            item = plan.get(pid)
            if pid not in cells or not isinstance(item, dict):
                gaps.append(label + " rests on an uncovered plan item: " + pid);good = False;continue
            if item.get("loop") != "design" or item.get("dimension") != "integrity":
                gaps.append(label + " must use a design/integrity plan item: " + pid);good = False
            if context is not None and item.get("context") != context:
                gaps.append(label + " uses evidence from another context: " + pid);good = False
            if aspect in {"continuity", "layering", "whole"} and item.get("method") != "visual":
                gaps.append(label + " requires visual inspection: " + pid);good = False
            if aspect == "whole" and item.get("level") != "whole":
                gaps.append(label + " must recheck the whole composition: " + pid);good = False
            if not set(cells[pid].get("evidence_ids", [])).intersection(refs):
                gaps.append(label + " evidence does not cover " + pid);good = False
        for eid in refs:
            problem = evidence_problem(eid)
            if problem:
                gaps.append(label + ": " + problem);good = False
        return good

    inventory = rows("inventory")
    item_ids = {i.get("id") for i in inventory if text(i.get("id")) and text(i.get("summary"))}
    if len(item_ids) != len(inventory) or not inventory:gaps.append("Integrity inventory needs unique objects with id and summary")
    if not any(i.get("role") == "ground" for i in inventory):gaps.append("Integrity inventory omitted the background/ground layer")
    listed = {i.get("subject") for i in inventory}
    for subject in subjects:
        if subject not in listed:gaps.append("Integrity inventory omitted a declared subject: " + str(subject))
    for i in inventory:
        if i.get("subject") not in subjects:gaps.append("Integrity object has no declared subject: " + str(i.get("id")))

    seen = {(c, a): set() for c in contexts for a in INTEGRITY_ASPECTS}
    for n, check in enumerate(rows("checks")):
        context, aspect, label = check.get("context"), check.get("aspect"), "Integrity check %s" % check.get("id", n)
        if aspect not in INTEGRITY_ASPECTS or context not in contexts:
            gaps.append(label + " needs a known aspect and declared context");continue
        outcome = check.get("result")
        if outcome == "defect":
            work.append(label + " found a defect: " + str(check.get("observation", "unspecified")));continue
        if outcome != "closed":
            gaps.append(label + " is unresolved");continue
        if not text(check.get("observation")):
            gaps.append(label + " needs an observed result");continue
        if bound(check, label, context, aspect):seen[(context, aspect)].update(ids(check.get("item_ids")))
    for (context, aspect), items in seen.items():
        missing = item_ids - items
        if missing:gaps.append("Integrity not checked for %s/%s: %s" % (context, aspect, ", ".join(sorted(missing))))

    for n, treatment in enumerate(rows("treatments")):
        label = "Treatment %s" % treatment.get("id", n)
        items = ids(treatment.get("item_ids"))
        if not items or not set(items).issubset(item_ids):gaps.append(label + " must name known objects")
        for field in ("kind", "intent", "must_preserve", "reject_if"):
            if not text(treatment.get(field)):gaps.append(label + " needs " + field + "; stated intent alone cannot pass")
        results = {r.get("context"): r for r in treatment.get("results", []) if isinstance(r, dict)} if isinstance(treatment.get("results"), list) else {}
        for context in contexts:
            row = results.get(context)
            if row is None:
                gaps.append(label + " has no observed result in " + str(context));continue
            if row.get("result") == "fails":
                work.append(label + " does not hold in %s: %s" % (context, row.get("observation", "unspecified")));continue
            if row.get("result") != "holds":
                gaps.append(label + " is unresolved in " + str(context));continue
            if not text(row.get("observation")) or row.get("observation").strip() == str(treatment.get("intent")).strip():
                gaps.append(label + " needs an observation of the effect in " + str(context));continue
            bound(row, label, context)

    exports = rows("exports")
    if not exports:gaps.append("Integrity needs export records comparing final output with its source")
    for n, export in enumerate(exports):
        label = "Export %s" % export.get("output", n)
        output, sources = export.get("output"), ids(export.get("sources"))
        if output not in files or not sources or any(s not in files for s in sources):
            gaps.append(label + " output and sources must belong to the final revision");continue
        outcome = export.get("result")
        if outcome == "differs":
            work.append(label + " differs from its source: " + str(export.get("observation", "unspecified")));continue
        if outcome != "matches" or not text(export.get("observation")) or not text(export.get("method")):
            gaps.append(label + " needs a method, an observation and a match result");continue
        if bound(export, label):
            if not any(output in evidence.get(eid, {}).get("rendered_from", {}) for eid in ids(export.get("evidence_ids"))):
                gaps.append(label + " was not inspected from the exported file itself")
    return result()
