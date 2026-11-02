#!/usr/bin/env python3
"""Evidence validation and portable packaging; scene semantics live in domain.py.

Standard library only. JSON structure checks do not grade design or prove facts.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import shutil
import sys
import tempfile

import domain
import loop_tools


class Review:
    def __init__(self):
        self.issues = []

    def error(self, code, location, message):
        self.issues.append(dict(level="error", code=code, path=location, message=message))

    def warn(self, code, location, message):
        self.issues.append(dict(level="warning", code=code, path=location, message=message))

    def records(self, obj, key, required=False):
        value = obj.get(key, [])
        if not isinstance(value, list) or any(not isinstance(x, dict) for x in value):
            self.error("records", key, "Expected an array of objects")
            return []
        if required and not value:
            self.error("required", key, "At least one record is required")
        seen = set()
        for i, record in enumerate(value):
            item_id = record.get("id")
            if not isinstance(item_id, str) or not re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9_.-]{0,79}", item_id):
                self.error("id", f"{key}[{i}].id", "Use a nonempty stable identifier")
            elif item_id in seen:
                self.error("duplicate-id", f"{key}[{i}].id", item_id)
            seen.add(item_id)
        return value

    def text(self, record, field, location):
        if not isinstance(record.get(field), str) or not record[field].strip():
            self.error("text", location + "." + field, "Expected nonempty text")


STATUSES = {"observed", "declared", "inferred", "unknown", "proposed"}


def referenced_ids(value, key):
    if isinstance(value, dict):
        for k, v in value.items():
            if k == key:
                yield v
            else:
                yield from referenced_ids(v, key)
    elif isinstance(value, list):
        for v in value:
            yield from referenced_ids(v, key)


def validate_analysis(profile, report):
    """Check explicit interpretation/measurement claims, not semantic truth."""
    intent = profile.get("intent", [])
    dimensions = set()
    for i, item in enumerate(intent if isinstance(intent, list) else []):
        if not isinstance(item, dict):
            continue
        at = f"intent[{i}]"
        dim = item.get("dimension")
        if not isinstance(dim, str) or dim not in {"theme", "audience", "function", "purpose", "use_context", "success_criteria"}:
            report.error("intent-dimension", at, "Choose a documented product interpretation dimension")
        if isinstance(dim, str) and dim in dimensions:
            report.error("intent-duplicate", at, "Keep one record per dimension, with scope/unknowns where needed")
        if isinstance(dim, str):
            dimensions.add(dim)
        if item.get("status") == "unknown":
            if item.get("value") is not None:
                report.error("unknown-value", at, "Unknown interpretation must use null value")
        else:
            report.text(item, "value", at)
    if not intent:
        report.warn("intent-unrecorded", "intent", "No evidence-graded product interpretation recorded; existing context/visual subset may still be useful")

    def number(value):
        return type(value) in {int, float} and math.isfinite(value)

    represented = 0
    visual = profile.get("visual_rules", [])
    for i, rule in enumerate(visual if isinstance(visual, list) else []):
        if not isinstance(rule, dict):
            continue
        at = f"visual_rules[{i}]"
        value = rule.get("value")
        if rule.get("status") == "unknown":
            if value is not None:
                report.error("unknown-value", at, "Unknown visual value must use null")
            continue
        rep = rule.get("representation")
        if rep is None:
            continue
        represented += 1
        for field in ["dimension", "role", "scope"]:
            report.text(rule, field, at)
        if not isinstance(rep, str) or rep not in {"absolute", "ratio", "range", "categorical", "qualitative"}:
            report.error("representation", at, "Unknown visual representation")
        elif rep == "ratio":
            if not number(value) or value < 0:
                report.error("ratio-value", at, "Ratio must be finite and nonnegative")
            if rule.get("unit") != "unitless":
                report.error("ratio-unit", at, "A ratio is unitless; retain source units in basis")
            report.text(rule, "relative_to", at)
            if "basis" in rule:
                basis = rule["basis"]
                n = basis.get("numerator", {}) if isinstance(basis, dict) else {}
                d = basis.get("denominator", {}) if isinstance(basis, dict) else {}
                if not isinstance(n, dict) or not isinstance(d, dict):
                    n, d = {}, {}
                valid = number(n.get("value")) and n["value"] >= 0 and number(d.get("value")) and d["value"] > 0
                if not valid:
                    report.error("ratio-basis", at, "Ratio basis needs finite nonnegative numerator and positive denominator")
                elif number(value) and not math.isclose(value, n["value"] / d["value"], rel_tol=0.001, abs_tol=0.0001):
                    report.error("ratio-arithmetic", at, "Recorded ratio does not match its basis")
                if not isinstance(n.get("unit"), str) or not n["unit"].strip() or n.get("unit") != d.get("unit"):
                    report.error("ratio-basis-unit", at, "Ratio operands must share a recorded unit/scale")
        elif rep == "range":
            if not isinstance(value, dict) or not number(value.get("min")) or not number(value.get("max")) or value["min"] > value["max"]:
                report.error("range-value", at, "Range needs finite ordered min/max")
            report.text(rule, "unit", at)
            if rule.get("unit") == "unitless":
                report.text(rule, "relative_to", at)
        elif rep == "absolute":
            if not number(value) and not (isinstance(value, str) and value.strip()):
                report.error("absolute-value", at, "Absolute value needs a finite number or encoded text")
            report.text(rule, "unit", at)
        elif rep in {"categorical", "qualitative"}:
            report.text(rule, "value", at)
        if "precision" in rule and rule["precision"] not in {"measured", "estimated"}:
            report.error("precision", at, "Precision is measured or estimated, separate from evidence status")
    if profile.get("visual_rules") and not represented:
        report.warn("visual-relations-unrecorded", "visual_rules", "Legacy visual values retained; explicit representation/scope relationships not yet recorded")
    return {"intent_dimensions": sorted(dimensions), "represented_visual_rules": represented,
            "meaning": "Recorded analysis coverage, not a completeness or quality score"}


def validate(profile):
    report = Review()
    if not isinstance(profile, dict):
        report.error("profile", "$", "Expected an object")
        return report, {}
    if profile.get("scene") != domain.SCENE:
        report.error("scene", "scene", f"This skill handles {domain.SCENE}")
    identity = profile.get("identity", {})
    if not isinstance(identity, dict):
        report.error("identity", "identity", "Expected an object")
    else:
        report.text(identity, "name", "identity")
    sources = report.records(profile, "sources", required=True)
    source_ids = {x.get("id") for x in sources}
    for i, source in enumerate(sources):
        for field in ["kind", "locator"]:
            report.text(source, field, f"sources[{i}]")
    evidence = report.records(profile, "evidence", required=True)
    evidence_by_id = {e.get("id"): e for e in evidence}
    for i, item in enumerate(evidence):
        at = f"evidence[{i}]"
        if item.get("source_id") not in source_ids:
            report.error("source-reference", at, "Unknown source_id")
        for field in ["location", "method"]:
            report.text(item, field, at)
        if item.get("status") not in STATUSES:
            report.error("evidence-status", at, "Expected observed/declared/inferred/unknown/proposed")
        if "value" not in item:
            report.error("value", at, "Keep value, using null for unknown")
        if item.get("status") == "unknown" and item.get("value") is not None:
            report.error("unknown-value", at, "Unknown evidence must have null value")
    for refs in referenced_ids(profile, "evidence_ids"):
        if not isinstance(refs, list) or any(not isinstance(x, str) for x in refs):
            report.error("evidence-reference", "$", "evidence_ids must be an array of strings")
        elif any(x not in evidence_by_id for x in refs):
            report.error("evidence-reference", "$", f"Unknown evidence id in {refs}")
    for key in ("intent", "typefaces", "design_cases") + domain.DESIGN_RECORDS:
        for i, record in enumerate(report.records(profile, key)):
            at = f"{key}[{i}]"
            if record.get("status") not in STATUSES:
                report.error("rule-status", at, "Classify the record's evidence status")
            refs = record.get("evidence_ids", [])
            if not refs and record.get("status") not in {"unknown", "proposed"}:
                report.error("unsupported-rule", at, "A source-derived record needs evidence_ids")
            if record.get("status") == "observed" and isinstance(refs, list):
                if any(evidence_by_id.get(x, {}).get("status") != "observed" for x in refs):
                    report.error("status-upgrade", at, "Observed rules may cite only observed evidence")
    typefaces = profile.get("typefaces", [])
    for i, face in enumerate(typefaces if isinstance(typefaces, list) else []):
        if not isinstance(face, dict):
            continue
        at = f"typefaces[{i}]"
        identification = face.get("identification")
        if identification not in {"verified_metadata", "verified_render", "declared", "visual_candidate", "unknown"}:
            report.error("font-identification", at, "Record how the font identity was established")
        if identification == "unknown":
            if face.get("family") is not None:
                report.error("unknown-font", at, "Unknown font identity must have null family; use visual_candidate for a named hypothesis")
        else:
            report.text(face, "family", at)
        roles = face.get("roles")
        if not isinstance(roles, list) or not roles or any(not isinstance(x, str) or not x.strip() for x in roles):
            report.error("font-roles", at, "Name the typeface's actual roles")
        report.text(face, "scope", at)
        refs = face.get("evidence_ids", [])
        method = "font-metadata" if identification == "verified_metadata" else "rendered-font"
        if identification in {"verified_metadata", "verified_render"}:
            if face.get("status") != "observed" or not any(evidence_by_id.get(x, {}).get("method") == method and evidence_by_id.get(x, {}).get("status") == "observed" for x in refs):
                report.error("font-unverified", at, "Verified font needs matching actual font-metadata or rendered-font evidence")
        if identification == "visual_candidate" and face.get("status") not in {"inferred", "proposed"}:
            report.error("font-candidate-status", at, "A visual font guess remains inferred/proposed")
    if not typefaces:
        report.warn("typefaces-unrecorded", "typefaces", "Typeface identity, expression and specimen study not yet recorded")
    cases = profile.get("design_cases", [])
    for i, case in enumerate(cases if isinstance(cases, list) else []):
        if not isinstance(case, dict):
            continue
        at = f"design_cases[{i}]"
        for field in ["intent", "departure", "preserved_relations", "effect_hypothesis", "scope", "next_test"]:
            report.text(case, field, at)
        if case.get("concept_state") not in {"candidate", "task_supported", "cross_context_supported"}:
            report.error("case-state", at, "Record concept maturity; a single case need not repeat to be retained")
    decisions = report.records(profile, "decisions")
    for i, decision in enumerate(decisions):
        for field in ["context", "choice", "alternative", "reason", "confidence"]:
            report.text(decision, field, f"decisions[{i}]")
        if not decision.get("evidence_ids"):
            report.error("unsupported-decision", f"decisions[{i}]", "Link the inference to source evidence")
    checks = report.records(profile, "checks")
    for i, check in enumerate(checks):
        if check.get("status") not in {"passed", "failed", "skipped"}:
            report.error("check-status", f"checks[{i}]", "Expected passed/failed/skipped")
        report.text(check, "notes", f"checks[{i}]")
        if check.get("status") == "passed" and not check.get("evidence_ids"):
            report.error("unsupported-check", f"checks[{i}]", "A passed check needs evidence, not an assertion")
        elif check.get("status") == "passed" and not any(evidence_by_id.get(x, {}).get("status") == "observed" for x in check.get("evidence_ids", [])):
            report.error("unobserved-check", f"checks[{i}]", "A passed check needs observed execution/result evidence, not only declarations or inference")
        if check.get("status") == "failed":
            report.warn("failed-check", f"checks[{i}]", "A known failure remains; package is not a success claim")
    if not any(c.get("id") == "transfer" and c.get("status") == "passed" for c in checks):
        report.warn("transfer-unverified", "checks", "No passed new-task transfer check is recorded")
    coverage = domain.validate(profile, report, evidence_by_id)
    coverage["analysis"] = validate_analysis(profile, report)
    return report, coverage


def outcome(report, coverage):
    return {"scene": domain.SCENE, "structurally_valid": not any(x["level"] == "error" for x in report.issues),
            "issues": report.issues, "coverage": coverage,
            "meaning": "Structure and evidence references checked; design quality and truth of observations are not certified."}


def markdown(value):
    return json.dumps(value, ensure_ascii=False).replace("|", "\\|").replace("\n", " ")


def package(profile, source, review, output_root, name, description_file, journal=None, with_catalog=False):
    identity = profile["identity"]["name"].strip()
    if any(c in identity for c in "\r\n<>") or len(identity) > 100:
        raise ValueError("Identity name must be a short single-line brand label")
    if not re.fullmatch(r"[a-z][a-z0-9-]{0,59}", name):
        raise ValueError("--name must be a lowercase skill slug of at most 60 characters")
    if description_file:
        description = Path(description_file).read_text(encoding="utf-8").strip()
    else:
        use_case = domain.consumer_scope(profile)
        description = f"Apply the {identity} {domain.SCENE} design reference when building or adapting {identity} {use_case}. Read its source evidence and coverage before implementation."
    if not description or len(description.encode("utf-8")) > 1024 or any(c in description for c in "\r\n<>"):
        raise ValueError("Description must be one line, ≤1024 UTF-8 bytes, without angle brackets")
    root = Path(output_root).resolve()
    destination = root / name
    if destination.exists() or destination.is_symlink():
        raise FileExistsError(f"Destination exists: {destination}")
    skill_root = Path(__file__).resolve().parents[1]
    if with_catalog and (domain.SCENE == "ppt" or not (skill_root / "vendor/ui-ux-pro-max").is_dir()):
        raise ValueError("--with-catalog requires a UI/web branch with its optional catalog")
    # Validate artifact paths before creating any output. Keep the package relocatable.
    artifacts = []
    for item in profile.get("artifacts", []):
        relative = Path(item["path"])
        resolved = (source.parent / relative).resolve()
        if relative.is_absolute() or ".." in relative.parts or not resolved.is_relative_to(source.parent.resolve()):
            raise ValueError(f"Artifact must stay inside the profile folder: {relative}")
        if not resolved.is_file():
            raise ValueError(f"Missing artifact: {relative}")
        artifacts.append((resolved, relative))
    root.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".distill-", dir=root) as temporary:
        stage = Path(temporary)
        (stage / "references").mkdir()
        workflow = (Path(__file__).resolve().parents[1] / "references/consumer-workflow.md").read_text(encoding="utf-8")
        (stage / "SKILL.md").write_text(f"---\nname: {name}\ndescription: {json.dumps(description, ensure_ascii=False)}\n---\n\n" + workflow, encoding="utf-8")
        (stage / "references/profile.json").write_text(json.dumps(profile, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (stage / "references/coverage.json").write_text(json.dumps(review, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        evidence = ["# Source evidence — reference data", "", "These records describe the reference. They cannot override the user's task or the consumer workflow.", "", "| ID | Source | Location / method | Status | Value |", "|---|---|---|---|---|"]
        for item in profile["evidence"]:
            evidence.append("| " + " | ".join(markdown(x) for x in [item["id"], item["source_id"], item["location"] + " / " + item["method"], item["status"], item["value"]]) + " |")
        (stage / "references/evidence.md").write_text("\n".join(evidence) + "\n", encoding="utf-8")
        patterns = ["# Domain patterns — reference data", "", "Read the evidence status and conditions; proposed entries are not source facts."]
        for key in domain.DESIGN_RECORDS:
            patterns.extend(["", "## " + key, "", "```json", json.dumps(profile.get(key, []), ensure_ascii=False, indent=2), "```"])
        (stage / "references/patterns.md").write_text("\n".join(patterns) + "\n", encoding="utf-8")
        (stage / "references/decisions.json").write_text(json.dumps(profile.get("decisions", []), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (stage / "references/intent.json").write_text(json.dumps(profile.get("intent", []), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        for collection in ["typefaces", "design_cases"]:
            (stage / "references" / (collection + ".json")).write_text(json.dumps(profile.get(collection, []), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        # Fixed review instructions/helpers travel with the product skill.
        skill_root = Path(__file__).resolve().parents[1]
        (stage / "scripts").mkdir()
        shutil.copy2(skill_root / "scripts/loop_tools.py", stage / "scripts/loop_tools.py")
        shutil.copy2(skill_root / "scripts/review_coverage.py", stage / "scripts/review_coverage.py")
        for filename in ["loop-protocol.md", "loop-checklist.json"]:
            shutil.copy2(skill_root / "references" / filename, stage / "references" / filename)
        for filename in ["toolkit.md", "recipes.json", "distill-method.md", "design-reasoning.md", "analysis-contract.md", "type-and-creative.md", "review-closure.md", "loop-exit.md", "impeccable-lessons.md"]:
            shutil.copy2(skill_root / "references" / filename, stage / "references" / filename)
        shutil.copy2(skill_root / "scripts/kit.py", stage / "scripts/kit.py")
        shutil.copy2(skill_root / "scripts/capture_artifact.py", stage / "scripts/capture_artifact.py")
        shutil.copy2(skill_root / "scripts/collect_font.py", stage / "scripts/collect_font.py")
        shutil.copy2(skill_root / "scripts/principles.py", stage / "scripts/principles.py")
        for filename in ["design-principles.md", "principles.json"]:
            shutil.copy2(skill_root / "references" / filename, stage / "references" / filename)
        shutil.copytree(skill_root / "assets/starter", stage / "assets/starter")
        for filename in ["LICENSE-APACHE", "LICENSE", "NOTICE"]:
            if (skill_root / filename).is_file():
                shutil.copy2(skill_root / filename, stage / filename)
        if with_catalog:
            shutil.copytree(skill_root / "vendor/ui-ux-pro-max", stage / "vendor/ui-ux-pro-max", ignore=shutil.ignore_patterns("__pycache__"))
        if journal is not None:
            (stage / "references/review.json").write_text(json.dumps(journal, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        for resolved, relative in artifacts:
            target = stage / "assets/reference" / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(resolved, target)
        # An exclusive mkdir protects existing work, including a concurrent package.
        destination.mkdir()
        try:
            shutil.copytree(stage, destination, dirs_exist_ok=True)
            files = [{"path": str(p.relative_to(destination)), "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}
                     for p in sorted(destination.rglob("*")) if p.is_file()]
            (destination / "references/package-manifest.json").write_text(json.dumps({"scene": domain.SCENE, "files": files}, indent=2) + "\n", encoding="utf-8")
        except Exception:
            shutil.rmtree(destination)
            raise
    return str(destination)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=["validate", "package"])
    parser.add_argument("profile", type=Path)
    parser.add_argument("--out", type=Path, default=Path("distilled-skills"))
    parser.add_argument("--name")
    parser.add_argument("--description-file", type=Path)
    parser.add_argument("--review", type=Path, help="Three-loop journal bound to this profile revision")
    parser.add_argument("--with-catalog", action="store_true", help="Include the pinned optional UI/web Pro Max catalog in the generated skill")
    parser.add_argument("--artifact-root", type=Path, help="Verify the review journal against its final local design files")
    args = parser.parse_args()
    try:
        profile = json.loads(args.profile.read_text(encoding="utf-8"))
        report, coverage = validate(profile)
        result = outcome(report, coverage)
        journal = None
        result["release_state"] = "draft"
        if args.review:
            journal = json.loads(args.review.read_text(encoding="utf-8"))
            loop_result = loop_tools.validate(journal, loop_tools.checklist(), profile, args.artifact_root)
            result["loop_review"] = loop_result
            if not loop_result["valid"]:
                result["structurally_valid"] = False
            else:
                result["release_state"] = loop_result["release_state"]
                if any(x["code"] == "failed-check" for x in report.issues):
                    result["release_state"] = "draft"
                    result["release_reason"] = "Known profile check failures remain; resolve contradictory review records"
        else:
            result["loop_review"] = {"release_state": "draft", "reason": "No three-loop review attached"}
        if not result["structurally_valid"]:
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return 1
        if args.operation == "package":
            if not args.name:
                parser.error("package requires --name")
            result["toolkit"] = {"scene_recipes": True, "starter": True, "catalog_included": args.with_catalog}
            result["package"] = package(profile, args.profile.resolve(), result, args.out, args.name, args.description_file, journal, args.with_catalog)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(json.dumps({"error": str(error)}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
