#!/usr/bin/env python3
"""Real optional-runtime smoke: owned HTML only, no accounts or reference sites."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / 'shared/scripts/motion_tools.py'


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--cache-dir')
    args = p.parse_args()
    if args.cache_dir:
        os.environ['HOLA_DESIGN_CACHE'] = str(Path(args.cache_dir).resolve())
    with tempfile.TemporaryDirectory(prefix='hola-motion-smoke-') as temporary:
        t = Path(temporary)
        page = t / 'motion.html'
        page.write_text('''<!doctype html><style>body{margin:0;background:#17343c}i{display:block;width:20px;height:20px;background:#ff7055;animation:m .2s .08s linear forwards}@keyframes m{to{transform:translateX(90px)}}</style><i></i>''')
        results = []
        def run(*options, expected=0):
            result = subprocess.run([sys.executable, str(TOOL), *map(str, options)], capture_output=True, text=True)
            if result.returncode != expected:
                raise RuntimeError(result.stderr[-2500:] + result.stdout[-2500:])
            receipt = json.loads(result.stdout)
            results.append({'operation': options[0], 'exit_code': result.returncode})
            return receipt
        assert run('doctor', '--allow-browser')['ready'] is True
        for name in ['reference', 'clone']:
            run('capture', '--allow-browser', '--', '--url', page, '--out', t / name,
                '--viewport', '160x96', '--clock', 'virtual', '--fps', '25', '--duration', '400', '--pre-roll', '0')
        compared = run('compare', '--fidelity', 'pixel-faithful', '--', '--ref', t / 'reference/frames',
                      '--clone', t / 'clone/frames', '--out', t / 'comparison')
        assert compared['assessment']['metric_result'] == 'MEASUREMENTS_WITHIN_LIMITS'
        assert compared['loop_acceptance'] == 'UNASSESSED'
        run('frames', '--', '--in', t / 'reference/video.mp4', '--out', t / 'sampled', '--fps', '25')
        run('sheet', '--allow-browser', '--', 'filmstrip', '--frames', t / 'sampled', '--out', t / 'sheets')
        print(json.dumps({'runtime_smoke': 'passed', 'operations': results}, indent=2))


if __name__ == '__main__':
    main()
