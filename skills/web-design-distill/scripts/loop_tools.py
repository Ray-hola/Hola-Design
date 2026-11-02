#!/usr/bin/env python3
"""Create/check three-loop review journals; standard library, no aesthetic grading."""
import argparse
import hashlib
import importlib.util
import json
import copy
import os
from pathlib import Path
import sys
import tempfile

LOOPS = ("distillation", "design", "feedback")
GATES = ("intent", "quality", "challenge", "integrity", "convergence")
TARGETS = {"extraction": "tool", "rule": "product_skill", "execution": "design_output", "coverage": "scope"}
_coverage_spec = importlib.util.spec_from_file_location("_review_coverage", Path(__file__).with_name("review_coverage.py"))
coverage_tools = importlib.util.module_from_spec(_coverage_spec)
_coverage_spec.loader.exec_module(coverage_tools)


def fingerprint(profile):
    return hashlib.sha256(json.dumps(profile, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def review_fingerprint(journal):
    """Bind the exit judgment to the review, excluding its own assessment."""
    return fingerprint({k: v for k, v in journal.items() if k != "exit_assessment"})


def exit_template(journal):
    result = {"revision_id": journal.get("delivery_revision"),
            "review_sha256": review_fingerprint(journal), "evaluator": "author",
            "gates": {key: {"status": "unknown", "reason": "", "evidence_ids": []}
                      for key in GATES},
            "remaining": []}
    result["gates"]["quality"]["weakest_subject"] = ""
    result["gates"]["quality"]["plan_ids"] = []
    result["gates"]["challenge"].update(objection="", response="", tests=[])
    scope = journal.get("review_scope") if isinstance(journal.get("review_scope"), dict) else {}
    contexts = scope.get("contexts") if isinstance(scope.get("contexts"), list) else []
    plan = {p.get("id") for p in journal.get("review_plan", []) if isinstance(p, dict)}
    # Open rows to answer: every result stays unknown until someone has looked.
    result["gates"]["integrity"].update(
        inventory=[{"id": "ground", "role": "ground", "subject": "", "summary": ""}], treatments=[], exports=[],
        checks=[{"id": aspect + "@" + context, "aspect": aspect, "context": context, "item_ids": [],
                 "plan_ids": [aspect + "@" + context] if aspect + "@" + context in plan else [],
                 "evidence_ids": [], "observation": "", "result": "unknown"}
                for context in contexts for aspect in coverage_tools.INTEGRITY_ASPECTS])
    return result


def integrity_plan(journal):
    """Add unanswered integrity plan items for each declared context; criteria stay blank."""
    scope = journal.get("review_scope")
    if not isinstance(scope, dict) or not scope.get("contexts") or not scope.get("subjects"):
        raise ValueError("Declare review_scope subjects and contexts before planning integrity")
    result = copy.deepcopy(journal)
    dimensions = result["review_scope"].setdefault("dimensions", {}).setdefault("design", [])
    if "integrity" not in dimensions:dimensions.append("integrity")
    plan = result.setdefault("review_plan", [])
    known = {p.get("id") for p in plan if isinstance(p, dict)}
    levels = {"content": "detail", "continuity": "relation", "layering": "relation", "whole": "whole"}
    for context in scope["contexts"]:
        for aspect, level in levels.items():
            if aspect + "@" + context not in known:
                plan.append({"id": aspect + "@" + context, "loop": "design", "dimension": "integrity",
                             "subjects": list(scope["subjects"]), "parts": [], "context": context,
                             "method": "visual", "level": level, "criterion": ""})
    return result


def reopen(journal, spec, loop, dimension, plan_ids, reason, source="reviewer", probe_method="direct"):
    """Persist an unresolved review objection using existing findings/repair history."""
    if not isinstance(journal, dict) or journal.get("scene") != spec["scene"]:
        raise ValueError("Journal scene mismatch")
    if not isinstance(reason, str) or not reason.strip():raise ValueError("reopen requires a concrete reason")
    if dimension not in {d["id"] for d in spec.get(loop, [])}:raise ValueError("Unknown reopened dimension")
    plans = {p.get("id"):p for p in journal.get("review_plan", []) if isinstance(p, dict)}
    if not plan_ids or any(pid not in plans or plans[pid].get("loop") != loop or plans[pid].get("dimension") != dimension for pid in plan_ids):
        raise ValueError("reopen needs plan IDs in the selected loop/dimension")
    result = copy.deepcopy(journal)
    rid = "reopen-" + str(len(result.get("rounds", [])) + 1) + "-" + fingerprint([reason, plan_ids])[:10]
    eid = rid + "-report"
    result.setdefault("evidence", []).append({"id":eid,"locator":source + ":" + rid,"observed":True,
        "notes":"Received objection, not proof that its aesthetic/content allegation is true: " + reason})
    latest = next((r for r in reversed(result.get("rounds", [])) if r.get("loop") == loop), {})
    checks = copy.deepcopy(latest.get("checks", []))
    check = next((c for c in checks if c.get("dimension") == dimension), None)
    if check is None:
        check = {"dimension":dimension};checks.append(check)
    check.update(status="failed", evidence_ids=[eid], notes="Review coverage reopened: " + reason,
        finding={"id":rid,"diagnosis":"coverage","target":"scope","severity":"material",
                 "summary":"Unresolved objection: " + reason,"plan_ids":list(plan_ids),
                 "required_probe_method":probe_method})
    result.setdefault("rounds", []).append({"id":rid,"loop":loop,"checks":checks,
        "source":source,"revoked_exit_assessment":result.get("exit_assessment")})
    result["exit_assessment"] = None
    return result


def exit_gate(journal, result, profile_verified=False, artifact_root=None):
    """Issue a scoped signal, not an aesthetic certificate or authorization."""
    gaps, work = [], []
    scope = journal.get("review_scope")
    if not isinstance(scope, dict):scope = {}
    assessment = journal.get("exit_assessment")
    if not isinstance(assessment, dict):
        assessment = {};gaps.append("Missing exit_assessment; a checklist alone cannot authorize exit")
    if not profile_verified:gaps.append("Source-profile binding not verified")
    if not result.get("valid"):gaps.append("Review record is invalid")
    coverage = result.get("coverage_review", {})
    if not coverage.get("complete"):
        gaps.append("Coverage or final-version evidence is incomplete")
        gaps.extend(coverage.get("gaps", [])[:8])
    if result.get("experiments", {}).get("pending"):work.append("Unresolved experiments remain")
    dimensions = scope.get("dimensions") if isinstance(scope.get("dimensions"), dict) else {}
    if any(result.get("loops", {}).get(loop) == "needs_repair" for loop in dimensions):
        work.append("A scoped loop still has a failed check")
    if scope.get("claim") == "whole_deliverable" and any(result.get("loops", {}).get(loop) != "accepted" for loop in dimensions):
        gaps.append("Whole-deliverable exit requires acceptance of every scoped loop")
    if assessment.get("revision_id") != journal.get("delivery_revision") or not assessment.get("revision_id"):
        gaps.append("Exit assessment is not bound to the final revision")
    if assessment.get("review_sha256") != review_fingerprint(journal):
        gaps.append("Review changed after exit assessment; reassess before exit")
    if assessment.get("evaluator") not in {"author", "independent"}:gaps.append("Declare evaluator kind")
    evidence = {e.get("id"): e for e in journal.get("evidence", []) if isinstance(e, dict) and isinstance(e.get("id"), str)}
    plan = {p.get("id"): p for p in journal.get("review_plan", []) if isinstance(p, dict) and isinstance(p.get("id"), str)}
    covered = {c.get("id") for c in coverage.get("cells", []) if c.get("covered")}
    verified_refs = {eid for c in coverage.get("cells", []) if c.get("covered") for eid in c.get("evidence_ids", [])}
    cell_evidence = {c["id"]:set(c.get("evidence_ids", [])) for c in coverage.get("cells", []) if c.get("covered")}

    def text(value):
        return isinstance(value, str) and bool(value.strip())

    def bound_refs(item):
        refs = item.get("evidence_ids")
        return (isinstance(refs, list) and bool(refs) and all(isinstance(x, str) and x in evidence for x in refs)
                and all(evidence[x].get("observed") is True and evidence[x].get("revision_id") == journal.get("delivery_revision")
                        and evidence[x].get("inspection") in {"inspected", "executed"} for x in refs)
                and all(x in verified_refs for x in refs))

    def focused_refs(ids, refs):
        return (isinstance(ids, list) and bool(ids) and all(isinstance(pid, str) and pid in covered for pid in ids)
                and isinstance(refs, list) and all(isinstance(eid, str) for eid in refs)
                and all(cell_evidence.get(pid, set()).intersection(refs) for pid in ids))

    gates = assessment.get("gates", {})
    if not isinstance(gates, dict):gates = {}
    needs_integrity = coverage_tools.integrity_required(scope)
    for key in GATES:
        if key == "integrity" and not needs_integrity:continue
        gate = gates.get(key, {})
        if not isinstance(gate, dict):gate = {}
        if gate.get("status") == "fail":work.append("Exit judgment failed: " + key)
        elif gate.get("status") != "pass":gaps.append("Exit judgment not established: " + key)
        if not text(gate.get("reason")) or not bound_refs(gate):gaps.append("Exit judgment needs reasons and current inspected evidence: " + key)
        if key == "quality":
            weakest = gate.get("weakest_subject")
            subjects = scope.get("subjects") if isinstance(scope.get("subjects"), list) else []
            refs = gate.get("evidence_ids") if isinstance(gate.get("evidence_ids"), list) else []
            if not isinstance(weakest, str) or weakest not in subjects:
                gaps.append("Quality judgment must identify the weakest declared subject")
            elif not any(weakest in plan[pid].get("subjects", []) and plan[pid].get("level") != "whole"
                         for cell in coverage.get("cells", []) if cell.get("covered")
                         and any(eid in cell.get("evidence_ids", []) for eid in refs if isinstance(eid, str))
                         for pid in [cell["id"]] if pid in covered and pid in plan):
                gaps.append("Weakest subject lacks detail/relation evidence in the quality judgment")
        if key == "challenge" and not all(text(gate.get(k)) for k in ("objection", "response")):
            gaps.append("Challenge judgment needs the strongest rejection case and its actual resolution")
    # Quality evidence must answer the selected questions, not merely be a current screenshot.
    quality = gates.get("quality") if isinstance(gates.get("quality"), dict) else {}
    focus = quality.get("plan_ids")
    focus = focus if isinstance(focus, list) and all(isinstance(x, str) for x in focus) else []
    if not focused_refs(focus, quality.get("evidence_ids")):
        gaps.append("Quality needs plan_ids and evidence covering each exact question/context")
    weakest = quality.get("weakest_subject")
    if not any(pid in plan and plan[pid].get("level") == "relation" and weakest in plan[pid].get("subjects", []) for pid in focus):
        gaps.append("Quality must examine the weakest subject's relationship, not only its presence/readability")
    for pid in focus:
        item = plan.get(pid, {})
        parts = item.get("parts")
        if not isinstance(parts, list) or not parts or any(not text(p) for p in parts) or (item.get("level") == "relation" and len(set(parts)) < 2):
            gaps.append("Quality question must name concrete parts; a relationship needs at least two: " + pid)
    challenge = gates.get("challenge") if isinstance(gates.get("challenge"), dict) else {}
    tests = challenge.get("tests")
    if not isinstance(tests, list) or not tests or any(not isinstance(t, dict) for t in tests):
        gaps.append("Challenge needs executed rejection tests, not an intent explanation");tests = []
    experiments = {e.get("id"):e for e in journal.get("experiments", []) if isinstance(e, dict)}
    tested, compared = set(), set()

    def baseline_bound(eid, pid):
        e = evidence.get(eid, {})
        if not (e.get("observed") is True and e.get("context") == plan[pid].get("context")
                and e.get("method") == plan[pid].get("method") and e.get("inspection") in {"inspected", "executed"}
                and (e.get("method") != "visual" or e.get("inspection") == "inspected")
                and e.get("revision_id") in {r.get("id") for r in journal.get("revisions", []) if isinstance(r, dict)}
                and isinstance(e.get("observations"), dict) and text(e["observations"].get(pid))):return False
        try:
            return artifact_root is not None and hashlib.sha256(coverage_tools.confined(Path(artifact_root), e["file"]).read_bytes()).hexdigest() == e["sha256"]
        except (OSError, ValueError, KeyError, TypeError):return False

    for test in tests:
        ids = test.get("plan_ids", [])
        refs = test.get("evidence_ids", [])
        good = focused_refs(ids, refs)
        if not good or not bound_refs(test):gaps.append("Rejection test needs evidence for its exact plan questions")
        if not text(test.get("reject_if")) or not text(test.get("observation")):
            gaps.append("Rejection test needs a falsifying condition and actual observed result")
        outcome = test.get("result")
        if outcome == "confirmed":work.append("Rejection condition still holds: " + str(test.get("reject_if")))
        elif outcome != "refuted":gaps.append("Rejection test is unresolved")
        method = test.get("method")
        if method not in {"direct", "comparison"}:gaps.append("Rejection test method is direct or comparison")
        if good:tested.update(ids)
        if method == "comparison" and good:
            refs_ex = test.get("experiment_ids", [])
            if not isinstance(refs_ex, list):refs_ex = []
            for pid in ids:
                found = False
                for exid in refs_ex:
                    ex = experiments.get(exid, {}) if isinstance(exid, str) else {}
                    variants = ex.get("variant_evidence", {})
                    if not isinstance(variants, dict) or not isinstance(ex.get("plan_ids"), list) or pid not in ex["plan_ids"] or ex.get("decision") not in {"keep", "revert"}:continue
                    bases, candidates = variants.get("baseline", []), variants.get("candidate", [])
                    if not isinstance(bases, list) or not isinstance(candidates, list):continue
                    for candidate in candidates:
                        if not isinstance(candidate, str) or candidate not in refs or candidate not in cell_evidence.get(pid, set()):continue
                        for base in bases:
                            if isinstance(base, str) and baseline_bound(base, pid) and evidence[base].get("sha256") != evidence[candidate].get("sha256"):
                                found = True
                if found:compared.add(pid)
                else:gaps.append("Comparison must test the same question/context with distinct inspected variants: " + pid)
    if not set(focus).issubset(tested):gaps.append("Quality questions were not all subjected to rejection tests")
    for r in journal.get("rounds", []):
        for check in r.get("checks", []) if isinstance(r, dict) else []:
            finding = check.get("finding", {})
            if isinstance(finding, dict) and finding.get("required_probe_method"):
                required = finding.get("plan_ids", [])
                if not isinstance(required, list) or any(not isinstance(p, str) or p not in plan for p in required):
                    gaps.append("A reopened concern disappeared from the current plan")
                elif not set(required).issubset(compared if finding["required_probe_method"] == "comparison" else tested):
                    gaps.append("A reopened concern lacks its required targeted recheck")
    remaining = assessment.get("remaining")
    if not isinstance(remaining, list) or any(not isinstance(x, dict) for x in remaining):
        gaps.append("remaining must list outstanding work or justified tradeoffs");remaining = []
    for item in remaining:
        if item.get("kind") == "tradeoff" and item.get("disposition") == "retained":
            if not text(item.get("summary")) or not text(item.get("reason")) or not bound_refs(item):
                gaps.append("Retained tradeoff needs its cost, reason and current evidence")
        else:
            work.append("Outstanding work: " + str(item.get("summary", "unspecified")))
    integrity = coverage_tools.integrity_audit(journal, coverage, artifact_root) if needs_integrity else {"state": "not_applicable", "reasons": []}
    if integrity["state"] == "HOLD":work.extend(integrity["reasons"])
    elif integrity["state"] == "UNVERIFIED":gaps.extend(integrity["reasons"])
    state = "HOLD" if work else "UNVERIFIED" if gaps else "PASS"
    signal = {"state": state, "scope": scope.get("claim", "undeclared"), "integrity": integrity,
              "revision": journal.get("delivery_revision"), "record": fingerprint(journal),
              "evaluator": assessment.get("evaluator"), "reasons": work + gaps}
    signal["record_gate"] = "ready" if not gaps and not work else "not_ready"
    signal["quality_basis"] = "recorded_reviewer_judgment_not_machine_aesthetic_certification"
    signal["marker"] = "::LOOP_EXIT{state:%s|scope:%s|revision:%s|record:%s|basis:%s}" % (
        signal["state"], signal["scope"], signal["revision"], signal["record"], signal["evaluator"])
    return signal


def checklist():
    return json.loads((Path(__file__).resolve().parents[1] / "references/loop-checklist.json").read_text())


def initial(profile, spec):
    return {"version": 2, "scene": spec["scene"], "profile_sha256": fingerprint(profile),
            "budget": {"mode": "adaptive", "max_total_repairs": None, "max_repairs_per_loop": None},
            "review_scope": None, "review_plan": [], "revisions": [], "delivery_revision": None,
            "benchmarks": [{"id": loop + "." + item["id"], "loop": loop,
                            "dimension": item["id"], "criterion": "", "references": []}
                           for loop in LOOPS for item in spec[loop]],
            "evidence": [], "experiments": [], "rounds": [], "exit_assessment": None}


def validate(journal, spec, profile=None, artifact_root=None):
    errors = []

    def require(condition, message):
        if not condition:
            errors.append(message)

    def text(value):
        return isinstance(value, str) and bool(value.strip())

    def strings(value, nonempty=True):
        return isinstance(value, list) and (bool(value) or not nonempty) and all(text(x) for x in value)

    def records(key):
        value = journal.get(key, [])
        if not isinstance(value, list) or any(not isinstance(x, dict) for x in value):
            errors.append(key + " must be an array of objects")
            return []
        ids = [x.get("id") for x in value]
        require(all(text(x) for x in ids) and len(ids) == len(set(map(str, ids))), key + " needs unique string IDs")
        return value

    if not isinstance(journal, dict):
        return {"valid": False, "errors": ["Journal must be an object"]}
    require(journal.get("version") in {1, 2}, "Unsupported journal version")
    require(journal.get("scene") == spec["scene"], "Journal scene mismatch")
    require(text(journal.get("profile_sha256")) and len(journal.get("profile_sha256", "")) == 64, "Missing profile fingerprint")
    if profile is not None:
        require(journal.get("profile_sha256") == fingerprint(profile), "Profile fingerprint mismatch; review this profile revision")
    budget = journal.get("budget", {})
    if not isinstance(budget, dict):
        budget = {}
    mode = budget.get("mode", "capped")  # Old explicit limits retain their meaning.
    require(mode in {"adaptive", "capped"}, "Budget mode is adaptive or capped")
    for key in ("max_total_repairs", "max_repairs_per_loop"):
        value = budget.get(key)
        require((mode == "adaptive" and key in budget and value is None) or (type(value) is int and value >= 0), "Budget needs a nonnegative limit or adaptive null: " + key)
    benchmarks = records("benchmarks")
    by_pair = {}
    expected = {(loop, item["id"]) for loop in LOOPS for item in spec[loop]}
    for b in benchmarks:
        pair = (str(b.get("loop")), str(b.get("dimension")))
        require(pair in expected and pair not in by_pair, "Unknown or duplicate benchmark dimension: " + str(pair))
        by_pair[pair] = b
    # Earlier journals stay readable; without this benchmark their design loop stays incomplete.
    require(set(by_pair) in (expected, expected - {("design", "integrity")}), "Benchmarks must cover the scene checklist")
    evidence = records("evidence")
    evidence_by_id = {str(e.get("id")): e for e in evidence}
    for e in evidence:
        require(text(e.get("locator")) and type(e.get("observed")) is bool and text(e.get("notes")), "Evidence needs locator, observed boolean and notes")

    def evidence_refs(obj, label):
        refs = obj.get("evidence_ids")
        valid = strings(refs) and all(x in evidence_by_id for x in refs)
        require(valid, label + " needs known evidence_ids")
        require(valid and any(evidence_by_id[x].get("observed") is True for x in refs), label + " needs observed evidence")

    experiments = records("experiments")
    for experiment in experiments:
        for field in ("hypothesis", "departure", "preserved_relations", "baseline", "candidate", "reason"):
            require(text(experiment.get(field)), "Experiment needs " + field)
        require(experiment.get("decision") in {"keep", "revert", "revise", "unresolved"}, "Experiment decision must be keep/revert/revise/unresolved")
        evidence_refs(experiment, "Experiment")
        # Departure from a convention is an exploration record, not a failed check.

    rounds = records("rounds")
    latest, findings, addressed, last_status = {}, {}, set(), {}
    counts = dict.fromkeys(LOOPS, 0)
    effects = []
    for r in rounds:
        loop = r.get("loop")
        if loop not in LOOPS:
            errors.append("Unknown round loop")
            continue
        dimensions = {x["id"]: x for x in spec[loop]}
        repair = r.get("repair")
        if repair is not None:
            if not isinstance(repair, dict):
                errors.append("repair must be an object")
                repair = {}
            counts[loop] += 1
            refs = repair.get("addresses", [])
            good = strings(refs) and all(x in findings and x not in addressed for x in refs)
            require(good, "Repair must address known, earlier, unaddressed findings")
            if good:
                require(all(findings[x]["target"] == repair.get("target") for x in refs), "Repair target does not match diagnosed layer")
                addressed.update(refs)
            require(text(repair.get("change")), "Repair needs concrete change")
            evidence_refs(repair, "Repair")
            require(strings(repair.get("regression_dimensions")), "Repair needs regression dimensions")
            if repair.get("target") == "tool":
                require(text(repair.get("generalization")) and strings(repair.get("regression_cases")), "Tool repair needs generalization and unaffected regression cases")
            require(repair.get("effect") in {"improved", "unchanged", "unknown"}, "Repair effect must be improved/unchanged/unknown")
            effects.append(repair.get("effect"))
        checks = r.get("checks", [])
        if not isinstance(checks, list) or any(not isinstance(c, dict) for c in checks):
            errors.append("Round checks must be an array of objects")
            checks = []
        seen = set()
        for c in checks:
            dim, status = c.get("dimension"), c.get("status")
            if not isinstance(dim, str) or dim not in dimensions:
                errors.append("Unknown check dimension")
                continue
            require(dim not in seen, "Duplicate round dimension: " + dim)
            seen.add(dim)
            b = by_pair.get((loop, dim), {})
            require(text(b.get("criterion")) and strings(b.get("references")), "Checked dimension needs a concrete benchmark and references: " + dim)
            require(status in {"passed", "failed", "skipped", "not_applicable"}, "Unknown check status")
            require(text(c.get("notes")), "Check needs explanatory notes")
            if status == "not_applicable":
                require(not dimensions[dim]["required"], "Required check cannot be not_applicable: " + dim)
            if status in {"passed", "failed"}:
                evidence_refs(c, "Check " + dim)
            pair = (loop, dim)
            if status in {"passed", "not_applicable"}:
                require(all(fid in addressed for fid, finding in findings.items() if finding["_pair"] == pair), "Failed check cannot be cleared without an attributed repair: " + dim)
            if status == "failed":
                f = c.get("finding", {})
                if not isinstance(f, dict):
                    f = {}
                fid = f.get("id")
                valid_id = text(fid) and fid not in findings
                require(valid_id, "Failure needs unique finding ID")
                require(f.get("diagnosis") in TARGETS and TARGETS.get(f.get("diagnosis")) == f.get("target"), "Finding diagnosis/target mismatch")
                require(f.get("severity") in {"material", "minor"} and text(f.get("summary")), "Finding needs severity and summary")
                if valid_id:
                    findings[fid] = dict(f, _pair=pair)
            last_status[pair] = c
        if repair:
            regressions = repair.get("regression_dimensions", [])
            require(strings(regressions) and all(any(c.get("dimension") == d and c.get("status") == "passed" for c in checks) for d in regressions), "Repair regressions must be rechecked and passed in the same round")
        latest[loop] = {c["dimension"]: c for c in checks if isinstance(c.get("dimension"), str)}
    if "feedback" in latest:
        task = journal.get("transfer_task", {})
        if not isinstance(task, dict):
            task = {}
        require(task.get("is_new") is True, "Feedback needs an actual new task")
        for field in ("id", "input", "artifact", "differs_from_source"):
            require(text(task.get(field)), "Transfer task needs " + field)
        require(task.get("evaluator") in {"author", "independent"}, "Declare evaluator kind")
        require(strings(task.get("source_access"), nonempty=False), "Declare evaluator source access")
    states = {}
    for loop in LOOPS:
        checks = latest.get(loop)
        if checks is None:
            states[loop] = "not_run"
        elif any(c.get("status") == "failed" for c in checks.values()):
            states[loop] = "needs_repair"
        elif any(d["id"] not in checks or checks[d["id"]].get("status") not in {"passed", "not_applicable"} for d in spec[loop]):
            states[loop] = "incomplete"
        else:
            states[loop] = "accepted"
    total = sum(counts.values())
    total_limit = budget.get("max_total_repairs")
    loop_limit = budget.get("max_repairs_per_loop")
    total_cap = total_limit if type(total_limit) is int else None
    loop_cap = loop_limit if type(loop_limit) is int else None
    require((total_cap is None or total <= total_cap) and (loop_cap is None or all(n <= loop_cap for n in counts.values())), "Repair budget exceeded")
    pending_experiments = any(x.get("decision") in {"revise", "unresolved"} for x in experiments)
    coverage = coverage_tools.audit(journal, spec, artifact_root)
    errors.extend(coverage["errors"])
    accepted = not errors and not pending_experiments and all(x == "accepted" for x in states.values()) and coverage["complete"] and coverage.get("claim") == "whole_deliverable"
    stop = "accepted_for_recorded_scope" if accepted else "evidence_or_work_remaining"
    if not accepted and ((total_cap is not None and total >= total_cap) or (loop_cap is not None and any(counts[l] >= loop_cap and states[l] == "needs_repair" for l in LOOPS))):
        stop = "budget_exhausted"
    elif not accepted and len(effects) >= 2 and effects[-2:] == ["unchanged", "unchanged"]:
        stop = "change_direction"
    result = {"valid": not errors, "errors": errors, "loops": states, "repairs": counts,
            "coverage_review": coverage,
            "release_state": "reviewed_for_recorded_scope" if accepted else "draft", "stop": stop,
            "experiments": {"recorded": len(experiments), "pending": pending_experiments},
            "evaluator": journal.get("transfer_task", {}).get("evaluator") if isinstance(journal.get("transfer_task"), dict) else None,
            "meaning": "Checks journal claims and coverage, not evidence truth, aesthetics, causal attribution or evaluator independence."}
    result["loop_exit"] = exit_gate(journal, result, profile_verified=profile is not None, artifact_root=artifact_root)
    if result["loop_exit"]["state"] != "PASS":
        result["release_state"] = "draft"
        if result["stop"] == "accepted_for_recorded_scope":result["stop"] = "exit_assessment_remaining"
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("operation", choices=["init", "validate", "finish", "fingerprint", "snapshot", "exit-template", "reopen", "integrity-plan"])
    p.add_argument("input", type=Path)
    p.add_argument("--profile", type=Path)
    p.add_argument("--out", type=Path)
    p.add_argument("--artifact-root", type=Path)
    p.add_argument("--files", nargs="+", default=[])
    p.add_argument("--loop", choices=LOOPS, default="design")
    p.add_argument("--dimension")
    p.add_argument("--plan-ids", nargs="+", default=[])
    p.add_argument("--reason")
    p.add_argument("--source", choices=["user", "reviewer"], default="reviewer")
    p.add_argument("--probe-method", choices=["direct", "comparison"], default="direct")
    args = p.parse_args()
    if args.operation == "finish" and not args.profile:
        p.error("finish requires --profile to verify the source-profile revision")
    try:
        if args.operation == "snapshot":
            result = coverage_tools.snapshot(args.input, args.files)
            if args.out:
                with args.out.open("x", encoding="utf-8") as file:
                    json.dump(result, file, ensure_ascii=False, indent=2);file.write("\n")
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return 0
        data = json.loads(args.input.read_text())
        spec = checklist()
        if args.operation == "reopen":
            data = reopen(data, spec, args.loop, args.dimension, args.plan_ids, args.reason, args.source, args.probe_method)
            if args.out:
                with args.out.open("x", encoding="utf-8") as file:
                    json.dump(data, file, ensure_ascii=False, indent=2);file.write("\n")
            else:
                temporary = None
                try:
                    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=args.input.parent, delete=False) as file:
                        temporary = Path(file.name)
                        json.dump(data, file, ensure_ascii=False, indent=2);file.write("\n")
                    os.replace(temporary, args.input)
                finally:
                    if temporary is not None:temporary.unlink(missing_ok=True)
            result = {"journal":str(args.out or args.input),"state":"HOLD","finding":data["rounds"][-1]["id"],
                      "meaning":"Review reopened, not proof that the objection is true; resolve it with the required targeted test before exit."}
        elif args.operation == "integrity-plan":
            if not isinstance(data, dict) or data.get("scene") != spec["scene"]:
                raise ValueError("Journal scene mismatch")
            data = integrity_plan(data)
            target = args.out or args.input
            target.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            result = {"journal": str(target), "state": "unanswered",
                      "meaning": "Plan items added. Fill each criterion and parts from the actual task, then inspect."}
        elif args.operation == "exit-template":
            if not isinstance(data, dict):raise ValueError("Journal must be an object")
            result = exit_template(data)
            if args.out:
                with args.out.open("x", encoding="utf-8") as file:
                    json.dump(result, file, ensure_ascii=False, indent=2);file.write("\n")
        elif args.operation == "fingerprint":
            if not isinstance(data, dict) or data.get("scene") != spec["scene"]:
                raise ValueError("Profile scene mismatch")
            result = {"profile_sha256": fingerprint(data)}
        elif args.operation == "init":
            if not args.out:
                p.error("init requires --out")
            if not isinstance(data, dict) or data.get("scene") != spec["scene"]:
                raise ValueError("Profile scene mismatch")
            with args.out.open("x", encoding="utf-8") as f:
                json.dump(initial(data, spec), f, ensure_ascii=False, indent=2)
                f.write("\n")
            result = {"journal": str(args.out), "state": "not_run"}
        else:
            profile = json.loads(args.profile.read_text()) if args.profile else None
            result = validate(data, spec, profile, args.artifact_root)
            if args.operation == "finish":
                ready = result["loop_exit"]["state"] == "PASS"
                result["completion"] = result["coverage_review"]["state"] if ready else "blocked_by_review_gaps"
                print(json.dumps(result, ensure_ascii=False, indent=2))
                return 0 if ready else 2
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result.get("valid", True) else 1
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(json.dumps({"error": str(error)}), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
