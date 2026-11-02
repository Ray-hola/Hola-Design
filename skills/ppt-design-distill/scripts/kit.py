#!/usr/bin/env python3
"""Scene starter kits, learned-pattern lookup and optional pinned Pro Max catalog."""
import argparse
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def search(query, profile=None, limit=5):
    spec = read(ROOT / "references/recipes.json")
    words = set(re.findall(r"[\w]+", query.casefold()))
    if not words:
        raise ValueError("Provide a nonempty search query")

    def score(value):
        haystack = json.dumps(value, ensure_ascii=False).casefold()
        return sum(1 for word in words if word in haystack)

    learned = []
    if profile:
        data = read(profile)
        if data.get("scene") != spec["scene"]:
            raise ValueError("Profile scene does not match this kit")
        for key in spec["profile_collections"]:
            for item in data.get(key, []):
                hits = score(item)
                if hits:
                    learned.append({"keyword_hits": hits, "collection": key, "record": item,
                                    "source": str(profile) + "#" + key + "/" + str(item.get("id")),
                                    "meaning": "Profile record: retain its own evidence status and conditions"})
    recipes = [{"keyword_hits": score(card), "record": card} for card in spec["cards"] if score(card)]
    return {"scene": spec["scene"], "query": query,
            "learned": sorted(learned, key=lambda x: -x["keyword_hits"])[:limit],
            "recipes": sorted(recipes, key=lambda x: -x["keyword_hits"])[:limit],
            "meaning": "Keyword retrieval, not a quality score. Recipe cards are proposed approaches; learned evidence retains priority within the user's brief."}


def starter(destination):
    destination = destination.resolve()
    if destination.exists() or destination.is_symlink():
        raise FileExistsError("Preserve existing task folder: " + str(destination))
    source = ROOT / "assets/starter"
    destination.parent.mkdir(parents=True, exist_ok=True)
    # Exclusive destination prevents overwriting prior or concurrent work.
    destination.mkdir()
    try:
        shutil.copytree(source, destination, dirs_exist_ok=True)
    except Exception:
        shutil.rmtree(destination)
        raise
    return {"task_folder": str(destination), "files": [str(p.relative_to(destination)) for p in sorted(destination.rglob("*")) if p.is_file()],
            "status": "template", "meaning": "Example content and neutral preview values are proposals, not observations of your source."}


def catalog(query, domain=None, stack=None, recommend=False, limit=3):
    scene = read(ROOT / "references/recipes.json")["scene"]
    if scene == "ppt":
        raise ValueError("This PPT kit has no UI/web catalog; use its presentation recipes and reference evidence")
    vendor = ROOT / "vendor/ui-ux-pro-max"
    if not (vendor / "scripts/search.py").is_file():
        raise ValueError("Optional catalog is absent; use local profile/recipes or the distillation tool's catalog")
    metadata = read(vendor / "UPSTREAM.json")
    command = [sys.executable, "-B", str(vendor / "scripts/search.py"), query, "--json", "--max-results", str(limit)]
    if recommend:
        command.append("--design-system")
    elif stack:
        command.extend(["--stack", stack])
    elif domain:
        command.extend(["--domain", domain])
    else:
        raise ValueError("Choose --domain or --stack explicitly; catalog intent must not be guessed")
    # Read-only modes only. No persistence, hooks, installation or generated-code execution.
    with tempfile.TemporaryDirectory(prefix="design-distill-catalog-") as isolated:
        result = subprocess.run(command, cwd=isolated, capture_output=True, text=True, timeout=45)
    if result.returncode:
        raise ValueError(result.stderr.strip() or result.stdout.strip() or "Catalog search failed")
    payload = json.loads(result.stdout)
    if isinstance(payload, dict) and payload.get("error"):
        raise ValueError(payload["error"])
    return {"scene": scene, "status": "proposed", "source": {"repo": metadata["repo"], "commit": metadata["commit"], "license": metadata["license"]},
            "result": payload, "meaning": "General catalog recommendation, not source evidence. Check version/platform fit, actual assets and current brief; compare with learned rules before adoption. No profile or master file was modified."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="operation", required=True)
    init = commands.add_parser("init"); init.add_argument("--out", type=Path, required=True)
    lookup = commands.add_parser("search"); lookup.add_argument("query"); lookup.add_argument("--profile", type=Path); lookup.add_argument("--limit", type=int, choices=range(1, 21), default=5)
    cat = commands.add_parser("catalog"); cat.add_argument("query"); intent = cat.add_mutually_exclusive_group(required=True)
    intent.add_argument("--domain"); intent.add_argument("--stack"); intent.add_argument("--recommend", action="store_true"); cat.add_argument("--limit", type=int, choices=range(1, 21), default=3)
    args = parser.parse_args()
    try:
        if args.operation == "init":
            result = starter(args.out)
        elif args.operation == "search":
            profile = args.profile
            if profile is None and (ROOT / "references/profile.json").is_file():
                profile = ROOT / "references/profile.json"
            result = search(args.query, profile, args.limit)
        else:
            result = catalog(args.query, args.domain, args.stack, args.recommend, args.limit)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, KeyError, TypeError, subprocess.TimeoutExpired) as error:
        print(json.dumps({"error": str(error)}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
