#!/usr/bin/env python3
"""Optional pinned Reanimate backend. Measurements never issue a LOOP PASS."""
import argparse
import hashlib
import json
import math
import shutil
import struct
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / "vendor/reanimate"
OPERATIONS = {"capture", "frames", "compare", "sheet", "easing", "gl"}


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def engine(explicit=None):
    manifest = read(BUNDLE / "UPSTREAM.json")
    candidates = [Path(explicit)] if explicit else [
        BUNDLE, Path.home() / ".codex/skills/reanimate",
        Path.home() / ".claude/skills/reanimate"]
    valid = []
    for candidate in candidates:
        if not candidate.is_dir():
            continue
        # Dependency installation must not silently select another source revision.
        if all((candidate / f["path"]).is_file() and
               digest(candidate / f["path"]) == f["sha256"]
               for f in manifest["files"] if f["path"] == "LICENSE" or
               (f["path"].startswith("scripts/") and f["path"] != "scripts/bun.lock")):
            valid.append(candidate)
    if not valid:
        raise ValueError("No engine matches the pinned Reanimate source")
    return next((p for p in valid if (p / "scripts/node_modules/pngjs").is_dir()), valid[0])


def flag(args, name):
    for i, value in enumerate(args):
        if value == name:
            return args[i + 1] if i + 1 < len(args) and not args[i + 1].startswith("--") else None
        if value.startswith(name + "="):
            return value.split("=", 1)[1]
    return None


def unique_options(args):
    """Upstream keeps the last occurrence; never preflight a different value."""
    seen = set()
    for arg in args:
        if arg.startswith("--"):
            name = arg.split("=", 1)[0]
            if name in seen:
                raise ValueError("Duplicate option is unsafe: " + name)
            seen.add(name)


def capture_options(args):
    return {arg.split("=", 1)[0]: flag(args, arg.split("=", 1)[0])
            for arg in args if arg.startswith("--") and
            arg.split("=", 1)[0] not in {"--url", "--out"}}


def png_size(path):
    with Path(path).open("rb") as stream:
        header = stream.read(24)
    if len(header) != 24 or header[:8] != b"\x89PNG\r\n\x1a\n" or header[12:16] != b"IHDR":
        raise ValueError("Invalid PNG frame: " + str(path))
    return struct.unpack(">II", header[16:24])


def frame_set(folder):
    folder = Path(folder).resolve()
    paths = sorted(folder.glob("*.png"))
    if not paths:
        raise ValueError("No PNG frames: " + str(folder))
    if not all(p.stem.isdecimal() for p in paths):
        raise ValueError("Frames must have numbered filenames from the sampler")
    indices = [int(p.stem) for p in paths]
    if indices[0] not in (0, 1) or indices != list(range(indices[0], indices[0] + len(paths))):
        raise ValueError("Missing, duplicated or misordered frame indices")
    sizes = {png_size(p) for p in paths}
    if len(sizes) != 1:
        raise ValueError("Frame dimensions change inside: " + str(folder))
    meta_path = next((p for p in [folder / "frames.json", folder.parent / "frames.json"] if p.is_file()), None)
    if meta_path is None:
        raise ValueError("Missing frames.json; record the real sampling fps")
    meta = read(meta_path)
    fps = meta.get("fps")
    if isinstance(fps, bool) or not isinstance(fps, (int, float)) or not math.isfinite(fps) or fps <= 0:
        raise ValueError("Invalid sampling fps")
    if "count" in meta and meta["count"] != len(paths):
        raise ValueError("Frame count differs from sampling metadata")
    h = hashlib.sha256()
    for p in paths:
        h.update(p.name.encode() + b"\0" + bytes.fromhex(digest(p)))
    return {"path": str(folder), "count": len(paths), "size": list(next(iter(sizes))),
            "fps": fps, "frames_sha256": h.hexdigest(),
            "metadata_sha256": digest(meta_path)}


def comparable(ref, clone):
    a, b = frame_set(ref), frame_set(clone)
    for key in ["count", "size", "fps"]:
        if a[key] != b[key]:
            raise ValueError("Capture mismatch: " + key + "; re-sample rather than resize or drop frames")
    # When both inputs are browser captures, compare the entire recorded setup,
    # excluding only output identity and inspected source URL.
    ca, cb = Path(ref).parent / "capture.json", Path(clone).parent / "capture.json"
    if ca.is_file() and cb.is_file():
        aa, bb = read(ca), read(cb)
        ignore = {"url", "out", "output", "createdAt", "capturedAt", "timestamp"}
        changed = sorted(k for k in set(aa) | set(bb) if k not in ignore and aa.get(k) != bb.get(k))
        if changed:
            raise ValueError("Browser capture settings differ: " + ", ".join(changed))
        ra, rb = ca.parent / "motion-receipt.json", cb.parent / "motion-receipt.json"
        if ra.is_file() and rb.is_file():
            oa, ob = read(ra).get("capture_options"), read(rb).get("capture_options")
            if oa != ob:
                raise ValueError("Browser capture command options differ; use identical explicit settings")
    return {"reference": a, "clone": b,
            "scope": "Full equal-length frame sets; source identity, crop intent and trigger still need inspection"}


def assess(report, inputs, fidelity):
    errors = []
    total = inputs["reference"]["count"]
    if report.get("frames") != total or report.get("compared") != total or report.get("offset") != 0:
        errors.append("Incomplete or shifted temporal coverage")
    details = report.get("frameDetails", [])
    values = [f.get("mismatch") for f in details]
    if len(values) != total or any(isinstance(v, bool) or not isinstance(v, (int, float)) or
                                   not math.isfinite(v) or not 0 <= v <= 1 for v in values):
        errors.append("Missing or invalid per-frame measurements")
    if report.get("setupWarnings"):
        errors.append("Upstream capture-setting warnings remain")
    timing = report.get("motion", {}).get("timingError", {})
    if any(k not in timing or isinstance(timing[k], bool) or not isinstance(timing[k], (int, float)) or
           not math.isfinite(timing[k]) or abs(timing[k]) > .08
           for k in ["startS", "endS", "durationS", "peakS"]):
        errors.append("Motion-window or peak timing exceeds 80 ms / is unavailable")
    if fidelity == "motion-faithful" and report.get("motion", {}).get("reference", {}).get("first", -1) < 0:
        errors.append("No reference motion was measured")
    if fidelity == "pixel-faithful" and values and all(isinstance(v, (int, float)) for v in values):
        if sum(values) / len(values) > .02 or max(values) > .05:
            errors.append("Pixel mismatch exceeds 2% mean / 5% worst frame")
        activity = report.get("activity", {}).get("reference", [])
        if len(activity) != total or any(values[i] > .005 for i, v in enumerate(activity) if v <= .002):
            errors.append("Resting-frame mismatch exceeds 0.5% / activity unavailable")
    return {"metric_result": "FAIL" if errors else "MEASUREMENTS_WITHIN_LIMITS", "errors": errors,
            "loop_acceptance": "UNASSESSED",
            "remaining": ["Inspect every comparison sheet", "Verify each spec row, identity, trigger, easing, travel and stagger",
                          "Review intent, new-content use and applicable UX/recovery", "Run existing journal finish with all five gates"]}


def execute(operation, args, explicit=None, fidelity="motion-faithful"):
    unique_options(args)
    source = engine(explicit)
    bun = shutil.which("bun")
    if not bun:
        raise ValueError("Bun is missing; install Bun 1.1+ before optional motion tools")
    output = flag(args, "--out")
    if output and (Path(output).exists() or Path(output).is_symlink()):
        raise ValueError("Output already exists; preserve it and use a new round directory")
    inputs = None
    if operation == "compare":
        allowed = {"--ref", "--clone", "--out"}
        if any(v.split("=", 1)[0] not in allowed for v in args if v.startswith("--")):
            raise ValueError("Strict compare accepts only --ref/--clone/--out; normalize an explicitly scoped region first")
        if not all(flag(args, k) for k in allowed):
            raise ValueError("Compare needs --ref, --clone and --out")
        inputs = comparable(flag(args, "--ref"), flag(args, "--clone"))
        args = args + ["--auto-align=false", "--offset", "0", "--threshold", "0.02", "--motion-threshold", "0.08"]
    elif operation == "frames":
        if not flag(args, "--in") or not Path(flag(args, "--in")).is_file():
            raise ValueError("Frames needs an existing local media file")
        fps = flag(args, "--fps")
        if fps is not None and (not math.isfinite(float(fps)) or float(fps) <= 0):
            raise ValueError("Sampling fps must be positive")
        inputs = {"media": str(Path(flag(args, "--in")).resolve()),
                  "media_sha256": digest(flag(args, "--in"))}
    command = [bun, str(source / "scripts" / (operation + ".ts"))] + args
    if output and operation in {"capture", "frames", "compare", "sheet"}:
        Path(output).mkdir(parents=True, exist_ok=False)
    run = subprocess.run(command, capture_output=True, text=True)
    receipt = {"backend": "reanimate", "upstream_commit": read(BUNDLE / "UPSTREAM.json")["commit"],
               "operation": operation, "command": command, "exit_code": run.returncode,
               "script_sha256": digest(source / "scripts" / (operation + ".ts")),
               "loop_acceptance": "UNASSESSED"}
    code = run.returncode
    if operation == "compare" and run.returncode == 0:
        report_path = Path(output) / "report.json"
        report = read(report_path)
        receipt.update({"fidelity": fidelity, "inputs": inputs, "report_sha256": digest(report_path),
                        "assessment": assess(report, inputs, fidelity)})
        try:
            unchanged = comparable(flag(args, "--ref"), flag(args, "--clone")) == inputs
        except (ValueError, OSError, KeyError, TypeError):
            unchanged = False
        receipt["inputs_unchanged"] = unchanged
        if not unchanged:
            receipt["assessment"]["metric_result"] = "FAIL"
            receipt["assessment"]["errors"].append("Inputs changed during comparison; preserve the failed round and capture again")
        if receipt["assessment"]["errors"]:
            code = 2
    elif operation == "frames" and run.returncode == 0:
        receipt["inputs"] = inputs
        if output:
            receipt["sampled_frames"] = frame_set(output)
        else:
            probe = json.loads(run.stdout)
            if not all(isinstance(probe.get(k), (int, float)) and probe[k] > 0
                       for k in ["width", "height", "durationS", "sourceFps"]):
                raise ValueError("Media probe did not establish valid video dimensions, duration and fps")
            receipt["probe"] = probe
    elif operation == "capture" and run.returncode == 0 and output:
        receipt["sampled_frames"] = frame_set(Path(output) / "frames")
        receipt["capture_settings_sha256"] = digest(Path(output) / "capture.json")
        receipt["capture_options"] = capture_options(args)
    if output and Path(output).is_dir():
        (Path(output) / "motion-receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    if run.returncode:
        print(run.stderr, file=sys.stderr)
    elif output is None and operation != "frames":
        receipt["tool_stdout"] = run.stdout
    print(json.dumps(receipt, indent=2))
    return code


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("operation", choices=sorted(OPERATIONS | {"doctor"}))
    p.add_argument("--engine", help="An explicitly selected root with exactly the pinned source")
    p.add_argument("--fidelity", choices=["motion-faithful", "pixel-faithful"], default="motion-faithful")
    p.add_argument("--allow-browser", action="store_true", help="Capture or render sheets only when the host permits this browser backend")
    options, args = p.parse_known_args()
    if args[:1] == ["--"]:
        args = args[1:]
    try:
        if options.operation == "doctor":
            source = engine(options.engine)
            print(json.dumps({"bun": shutil.which("bun"), "engine": str(source),
                              "dependencies_installed": (source / "scripts/node_modules/pngjs").is_dir(),
                              "ffmpeg_installed": (source / "scripts/node_modules/ffmpeg-static/ffmpeg").is_file(),
                              "upstream_commit": read(BUNDLE / "UPSTREAM.json")["commit"]}, indent=2))
            return 0
        if options.operation in {"capture", "sheet"} and not options.allow_browser:
            raise ValueError("Browser backend not enabled: use the host's permitted capture/export, or explicitly authorize this backend with --allow-browser")
        return execute(options.operation, args, options.engine, options.fidelity)
    except (ValueError, OSError, KeyError, TypeError) as e:
        print(json.dumps({"error": str(e), "loop_acceptance": "UNASSESSED"}), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
