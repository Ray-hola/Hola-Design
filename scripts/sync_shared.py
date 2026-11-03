#!/usr/bin/env python3
"""Copy shared/ into every scene skill, or with --check report copies that drifted."""
import filecmp
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
SHARED = ROOT / "shared"
SCENES = ("ppt", "ui", "web")


def sync(check):
    drift = []
    for source in sorted(p for p in SHARED.rglob("*") if p.is_file()):
        relative = source.relative_to(SHARED)
        for scene in SCENES:
            target = ROOT / "skills" / (scene + "-design-distill") / relative
            if target.is_file() and filecmp.cmp(source, target, shallow=False):
                continue
            drift.append(str(target.relative_to(ROOT)))
            if not check:
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, target)
    print(("Out of sync with shared/:\n  " if check else "Updated:\n  ") + "\n  ".join(drift) if drift else "All scene copies match shared/.")
    return 1 if check and drift else 0


if __name__ == "__main__":
    sys.exit(sync("--check" in sys.argv[1:]))
