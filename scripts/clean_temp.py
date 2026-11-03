#!/usr/bin/env python3
"""Preview or remove inactive, disposable items from this repository's temp/ only."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]


def inspect_item(path, cutoff):
    """Protect the whole item if anything is recent, pinned, linked or a repository."""
    pending = [path]
    while pending:
        current = pending.pop()
        if current.name in {'.keep', '.git'}:
            return 'protected marker or repository'
        if current.is_symlink():
            return 'symlink'
        if current.stat().st_mtime >= cutoff:
            return 'updated within retention period'
        if current.is_dir():
            pending.extend(current.iterdir())
        elif not current.is_file():
            return 'special file'
    return None


def clean(root, days=14, apply=False, now=None, tracked=()):
    root = Path(root)
    if days < 1:
        raise ValueError('Retention must be at least one day')
    temp = root / 'temp'
    if temp.is_symlink():
        raise ValueError('Refusing symlinked temp directory')
    result = {'mode': 'apply' if apply else 'preview', 'retention_days': days,
              'eligible': [], 'deleted': [], 'skipped': [], 'errors': []}
    if not temp.exists():
        return result
    if not temp.is_dir():
        raise ValueError('temp is not a directory')
    if (temp / '.keep').exists() or (temp / '.keep').is_symlink():
        result['skipped'].append({'path': 'temp/', 'reason': 'root .keep marker'})
        return result
    cutoff = (time.time() if now is None else now) - days * 86400
    for item in sorted(temp.iterdir()):
        relative = item.relative_to(root).as_posix()
        try:
            reason = ('tracked content' if any(name == relative or name.startswith(relative + '/') for name in tracked)
                      else inspect_item(item, cutoff))
            if reason:
                result['skipped'].append({'path': relative, 'reason': reason})
                continue
            result['eligible'].append(relative)
            if apply:
                # Recheck immediately before removal; active tasks must pin with .keep.
                reason = inspect_item(item, cutoff)
                if reason:
                    result['skipped'].append({'path': relative, 'reason': reason})
                    continue
                if item.is_dir():
                    shutil.rmtree(item)
                else:
                    item.unlink()
                result['deleted'].append(relative)
        except OSError as error:
            result['errors'].append({'path': relative, 'error': str(error)})
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--days', type=int, default=14)
    parser.add_argument('--apply', action='store_true', help='Delete eligible items; default only previews')
    args = parser.parse_args()
    try:
        actual = subprocess.check_output(['git', 'rev-parse', '--show-toplevel'], cwd=ROOT, text=True).strip()
        if Path(actual).resolve() != ROOT:
            raise ValueError('Script must belong to the target repository root')
        tracked = subprocess.check_output(['git', 'ls-files', '-z'], cwd=ROOT).decode().split('\0')
        result = clean(ROOT, args.days, args.apply, tracked=tracked)
        print(json.dumps(result, indent=2))
        return int(bool(result['errors']))
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        parser.exit(1, str(error) + '\n')


if __name__ == '__main__':
    raise SystemExit(main())
