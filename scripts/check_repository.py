#!/usr/bin/env python3
"""Check the distributable source tree; this is not a legal or secret-free guarantee."""
import ast
import hashlib
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
SKIP = {".git", "__pycache__", ".pytest_cache", ".venv", "node_modules"}
RULES = {
    "private key": r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",
    "GitHub credential": r"\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,})\b",
    "AWS access key": r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b",
    "API credential": r"\bsk-(?:proj-)?[A-Za-z0-9_-]{32,}\b",
    "authenticated URL": r"https?://[^\s/<>]+:[^\s/@<>]+@",
}


def check():
    errors, count, manifests = [], 0, 0
    for path in sorted(ROOT.rglob("*")):
        relative = path.relative_to(ROOT)
        if any(part in SKIP for part in relative.parts) or not path.is_file():
            continue
        count += 1
        if path.is_symlink():
            errors.append(f"{relative}: review symlinks before publication")
        if path.name.startswith(".env") and path.name != ".env.example":
            errors.append(f"{relative}: environment file is not distributable")
        if path.suffix.lower() in {".pem", ".key", ".epub", ".pdf", ".ttf", ".otf", ".woff", ".woff2"}:
            errors.append(f"{relative}: asset needs an explicit publication review")
        if "cover-review" in relative.parts or relative.parts[0] in {"research", "output", "private", "backups"}:
            errors.append(f"{relative}: private working evidence is outside publication scope")
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for number, line in enumerate(text.splitlines(), 1):
            for label, pattern in RULES.items():
                if re.search(pattern, line):
                    errors.append(f"{relative}:{number}: possible {label}; value withheld")
            # Upstream catalogs contain explicit fictitious bad-path examples.
            if "vendor" not in relative.parts and re.search(r"/(?:Users|home)/[A-Za-z0-9_.-]+/", line):
                errors.append(f"{relative}:{number}: machine-specific home path")
        if relative.parts[0] == "skills" and re.search(r"[\u3400-\u9fff]", text):
            errors.append(f"{relative}: skill content must be English")
        if path.suffix == ".py":
            try:
                ast.parse(text, filename=str(relative))
            except SyntaxError as error:
                errors.append(f"{relative}:{error.lineno}: Python syntax error")
        if path.suffix == ".json":
            try:
                json.loads(text)
            except ValueError:
                errors.append(f"{relative}: invalid JSON")
        if path.suffix == ".md":
            links = re.findall(r"\]\(([^\s)]+)", text)
            links += re.findall(r'(?:src|href|srcset)="([^"]+)"', text)
            for link in links:
                if ":" in link or link.startswith("#"):
                    continue
                target = unquote(link.strip("<>").split("#")[0])
                if target and not (path.parent / target).exists():
                    errors.append(f"{relative}: missing local link: {target}")
        if path.name == "UPSTREAM.json":
            data = json.loads(text)
            for entry in data.get("files", []):
                candidate = (path.parent / entry["path"]).resolve()
                if not candidate.is_relative_to(path.parent.resolve()):
                    errors.append(f"{relative}: manifest path escapes its directory")
                elif not candidate.is_file() or hashlib.sha256(candidate.read_bytes()).hexdigest() != entry["sha256"]:
                    errors.append(f"{relative}: provenance mismatch: {entry['path']}")
                manifests += 1
    print(json.dumps({"files_checked": count, "provenance_entries_checked": manifests,
                      "errors": errors, "passed": not errors}, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(check())
