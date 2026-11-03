#!/usr/bin/env python3
"""Synchronize owned shared files; refuse to delete edited retired copies."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import shutil

ROOT = Path(__file__).resolve().parents[1]
SCENES = ("ppt", "ui", "web")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def safe_path(root, relative):
    parts = PurePosixPath(relative)
    if parts.is_absolute() or ".." in parts.parts or not parts.parts or chr(92) in relative:
        raise ValueError("Invalid managed path: " + relative)
    path = root
    for part in parts.parts:
        path = path / part
        if path.is_symlink():
            raise ValueError("Refusing symlink: " + str(path))
    return path


def sync(check, root=None):
    root = Path(root) if root is not None else ROOT
    shared, manifest = root / "shared", root / "scripts/shared-manifest.json"
    if not shared.is_dir() or shared.is_symlink():
        raise ValueError("Missing or symlinked shared source directory")
    data = json.loads(manifest.read_text(encoding="utf-8"))
    if data.get("version") != 1 or not isinstance(data.get("files"), dict):
        raise ValueError("Invalid ownership manifest")
    previous = data["files"]
    current = {}
    for source in sorted(shared.rglob("*")):
        if source.is_symlink():
            raise ValueError("Refusing shared symlink: " + str(source))
        if source.is_file():
            current[source.relative_to(shared).as_posix()] = digest(source)
    updates, removals, conflicts = [], [], []
    for relative in sorted(set(previous) | set(current)):
        safe_path(shared, relative)
        for scene in SCENES:
            scene_root = safe_path(root, "skills/" + scene + "-design-distill")
            target = safe_path(scene_root, relative)
            if relative in current:
                if target.exists() and not target.is_file():
                    conflicts.append(str(target.relative_to(root)))
                elif not target.is_file() or digest(target) != current[relative]:
                    updates.append((shared / relative, target))
            elif target.exists():
                if not target.is_file() or digest(target) != previous[relative]:
                    conflicts.append(str(target.relative_to(root)))
                else:
                    removals.append(target)
    # Preflight every target before modifying any scene or the manifest.
    if conflicts:
        print("Resolve edited retired files or path conflicts: " + ", ".join(conflicts))
        return 1
    changed = bool(updates or removals or current != previous)
    if check:
        for _, target in updates:
            print("Out of sync: " + str(target.relative_to(root)))
        for target in removals:
            print("Retired shared copy: " + str(target.relative_to(root)))
        if current != previous:
            print("Ownership manifest needs synchronization")
    else:
        for source, target in updates:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
        for target in removals:
            target.unlink()
        manifest.write_text(json.dumps({"version": 1, "files": current}, indent=2) + "\n", encoding="utf-8")
    print("Shared source and scene copies match." if not changed else
          ("Run sync after reviewing the changes." if check else
           "Updated %d files; removed %d unchanged retired copies." % (len(updates), len(removals))))
    return int(check and changed)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        raise SystemExit(sync(args.check))
    except (OSError, ValueError) as error:
        parser.exit(1, str(error) + "\n")
