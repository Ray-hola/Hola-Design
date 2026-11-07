#!/usr/bin/env python3
"""User-local, pinned cross-platform runtime for the optional motion backend."""
import hashlib
import json
import os
import platform
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / 'vendor/reanimate'
VERSION = '1.4.4'
BINARIES = {
    'darwin-arm64': ('bun-darwin-aarch64', 'c240d7f0ccb90c263a849fcdb09b7ee62630d921348ed6aafda86b9d577bc510'),
    'darwin-x64': ('bun-darwin-x64-baseline', 'd4a155adfbfd09155eb3ba05c9e3a544f39297d7a68616d3c7759f67ab5c47dc'),
    'linux-arm64': ('bun-linux-aarch64', 'baa6bb36f51d6e58561e02bbea825038a9df454f673d6d776e8bbf86f8c7850e'),
    'linux-x64': ('bun-linux-x64-baseline', 'e0446eb55995772eb9894bebae9a6be368d985a8b9271ee124486f9946eedd76'),
    'windows-x64': ('bun-windows-x64-baseline', '0f20ce6674d4f2dbcc8c5d59fdf99f7ba45f8c3b367e0f5781cbfa30a1c78d99'),
}


def manifest():
    return json.loads((BUNDLE / 'UPSTREAM.json').read_text())


def digest(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def target(system=None, machine=None):
    system = (system or platform.system()).lower()
    machine = (machine or platform.machine()).lower()
    arch = {'x86_64': 'x64', 'amd64': 'x64', 'aarch64': 'arm64', 'arm64': 'arm64'}.get(machine, machine)
    key = system + '-' + arch
    if key not in BINARIES:
        raise ValueError('Unsupported native runtime platform: ' + key + '; use a supported host/VM. No installation attempted.')
    return key


def cache_root():
    if os.environ.get('HOLA_DESIGN_CACHE'):
        return Path(os.path.abspath(os.path.expanduser(os.environ['HOLA_DESIGN_CACHE'])))
    if platform.system() == 'Windows':
        return Path(os.environ.get('LOCALAPPDATA', str(Path.home() / 'AppData/Local'))) / 'Hola-Design/Cache'
    if platform.system() == 'Darwin':
        return Path.home() / 'Library/Caches/Hola-Design'
    return Path(os.environ.get('XDG_CACHE_HOME', str(Path.home() / '.cache'))) / 'hola-design'


def runtime_dir():
    return cache_root() / ('reanimate-' + manifest()['commit'][:12] + '-v1') / target()


def cached_engine():
    return runtime_dir() / 'engine'


def safe_write_path(path):
    path = Path(path).absolute()
    if any(p.is_symlink() for p in [path, *path.parents]):
        raise ValueError('Runtime cache contains a symlink; choose a real writable cache directory')
    return path


def patched_lib(data):
    old = '"ffmpeg-static", "ffmpeg"'
    new = '"ffmpeg-static", process.platform === "win32" ? "ffmpeg.exe" : "ffmpeg"'
    if data.count(old) != 1:
        raise ValueError('Pinned ffmpeg compatibility patch no longer matches upstream')
    return data.replace(old, new)


def runtime_bytes(name):
    source = BUNDLE / name
    if name == 'scripts/lib.ts':
        return patched_lib(source.read_text()).encode()
    if name == 'scripts/capture.ts':
        data = source.read_text().replace('chromium.launch({ headless:', 'chromium.launch({ channel: "chromium", headless:')
        data = 'import { pathToFileURL } from "node:url";\n' + data
        data = data.replace('if (!/^[a-z]+:/i.test(url)) url = "file://" + abs(url);',
                            'if (!/^(https?|file|data|about):/i.test(url)) url = pathToFileURL(abs(url)).href;')
        return data.encode()
    if name == 'scripts/sheet.ts':
        return source.read_text().replace('chromium.launch()', 'chromium.launch({ channel: "chromium" })').encode()
    return source.read_bytes()


def valid_engine(path):
    path = Path(path)
    for item in manifest()['files']:
        name = item['path']
        if not (name == 'LICENSE' or name.startswith('scripts/')):
            continue
        p = path / name
        if not p.is_file() or p.is_symlink():
            return False
        expected = item['sha256']
        if path == cached_engine():
            expected = hashlib.sha256(runtime_bytes(name)).hexdigest()
        elif name == 'scripts/lib.ts' and digest(p) != expected:
            expected = hashlib.sha256(runtime_bytes(name)).hexdigest()
        if digest(p) != expected:
            return False
    return True


def bun_path():
    own = runtime_dir() / 'bin' / ('bun.exe' if platform.system() == 'Windows' else 'bun')
    if own.is_file():
        return str(own)
    return shutil.which('bun')


def env_for(engine):
    env = dict(os.environ)
    bun = bun_path()
    if bun:
        env['PATH'] = str(Path(bun).parent) + os.pathsep + env.get('PATH', '')
    if Path(engine).resolve() == cached_engine().resolve():
        env['PLAYWRIGHT_BROWSERS_PATH'] = str(runtime_dir() / 'browsers')
    return env


def run(command, cwd=None, env=None, timeout=900):
    result = subprocess.run(command, cwd=cwd, env=env, capture_output=True, text=True, timeout=timeout)
    if result.returncode:
        raise ValueError('Runtime command failed: ' + ' '.join(map(str, command[:3])) + '\n' + result.stderr[-1800:])
    return result.stdout


def ensure_bun(download=False):
    bun = None if download else bun_path()
    if bun:
        try:
            if run([bun, '--version'], timeout=15).strip() == VERSION:
                return bun
        except (ValueError, OSError, subprocess.TimeoutExpired):
            pass
    key = target()
    name, sha = BINARIES[key]
    binary = runtime_dir() / 'bin' / ('bun.exe' if key.startswith('windows') else 'bun')
    safe_write_path(binary)
    binary.parent.mkdir(parents=True, exist_ok=True)
    url = 'https://github.com/oven-sh/bun/releases/download/bun-v' + VERSION + '/' + name + '.zip'
    with tempfile.TemporaryDirectory(prefix='bun-', dir=str(binary.parent)) as t:
        archive = Path(t) / 'bun.zip'
        request = urllib.request.Request(url, headers={'User-Agent': 'Hola-Design runtime bootstrap'})
        with urllib.request.urlopen(request, timeout=90) as source, archive.open('wb') as dest:
            shutil.copyfileobj(source, dest)
        if digest(archive) != sha:
            raise ValueError('Bun archive SHA-256 mismatch; downloaded code was not executed')
        with zipfile.ZipFile(archive) as z:
            member = name + '/' + binary.name
            with z.open(member) as source, binary.open('wb') as dest:
                shutil.copyfileobj(source, dest)
        binary.chmod(0o755)
    if run([str(binary), '--version'], timeout=15).strip() != VERSION:
        raise ValueError('Downloaded Bun version does not match the pinned runtime')
    return str(binary)


def prepare_engine():
    out = cached_engine()
    safe_write_path(out)
    out.mkdir(parents=True, exist_ok=True)
    for item in manifest()['files']:
        source = BUNDLE / item['path']
        if source.is_symlink() or digest(source) != item['sha256']:
            raise ValueError('Bundled source hash mismatch: ' + item['path'])
        dest = out / item['path']
        safe_write_path(dest)
        data = runtime_bytes(item['path'])
        if dest.exists() and (dest.is_symlink() or dest.read_bytes() not in {data, source.read_bytes()}):
            raise ValueError('Existing runtime source differs; preserve it and select a fresh HOLA_DESIGN_CACHE')
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
    safe_write_path(out / 'UPSTREAM.json').write_bytes((BUNDLE / 'UPSTREAM.json').read_bytes())
    safe_write_path(out / 'RUNTIME.json').write_text(json.dumps({'upstream_commit': manifest()['commit'],
        'adaptation': 'Windows ffmpeg.exe and file URLs; capture/sheet/probe use the same full Chromium channel. Vendored source unchanged.',
        'overlay_sha256': {name: digest(out / name) for name in ['scripts/lib.ts','scripts/capture.ts','scripts/sheet.ts']}, 'bun_version': VERSION}, indent=2) + '\n')
    return out


PROBE = r'''
import { existsSync } from 'node:fs';
import { join } from 'node:path';
import { spawnSync } from 'node:child_process';
const result = {dependencies:false, ffmpeg:false, browser:'not_probed', pixel_comparison:false};
try {
  const {PNG} = await import('pngjs');
  const {default:pixelmatch} = await import('pixelmatch');
  const {chromium} = await import('playwright');
  result.dependencies = true;
  const ff = join(process.cwd(),'node_modules','ffmpeg-static',process.platform==='win32'?'ffmpeg.exe':'ffmpeg');
  result.ffmpeg = existsSync(ff) && spawnSync(ff,['-version']).status===0;
  if (process.env.HOLA_PROBE_BROWSER==='1') {
    const b=await chromium.launch({channel:'chromium',headless:true});
    try {const p=await b.newPage({viewport:{width:64,height:64}});
      await p.setContent('<body style="margin:0;background:#19323a"><div style="width:32px;height:32px;background:#fe7055"></div>');
      const data=PNG.sync.read(await p.screenshot());
      const again=PNG.sync.read(await p.screenshot());
      const color=(x,y)=>Array.from(data.data.slice((y*64+x)*4,(y*64+x)*4+3)).join(',');
      result.pixel_comparison = data.width===64 && data.height===64 && color(8,8)==='254,112,85' && color(48,48)==='25,50,58' && pixelmatch(data.data,again.data,null,64,64)===0;
      result.browser=true;
    } finally {await b.close();}
  }
} catch(e) {result.error=String(e).slice(0,1800); if(process.env.HOLA_PROBE_BROWSER==='1')result.browser=false;}
console.log(JSON.stringify(result));
'''


def doctor(engine=None, browser=False):
    source = Path(engine) if engine else cached_engine()
    bun = bun_path()
    result = {'platform': target(), 'bun': bun, 'engine': str(source), 'cache': str(runtime_dir()),
              'upstream_commit': manifest()['commit'], 'source_verified': valid_engine(source),
              'dependencies': False, 'ffmpeg': False, 'browser': 'not_probed', 'pixel_comparison': False}
    if bun:
        try:
            result['bun_version'] = run([bun, '--version'], timeout=15).strip()
            if result['source_verified']:
                env = env_for(source); env['HOLA_PROBE_BROWSER'] = '1' if browser else '0'
                result.update(json.loads(run([bun, '-e', PROBE], cwd=source / 'scripts', env=env, timeout=90)))
        except (ValueError, OSError, subprocess.TimeoutExpired) as e:
            result['error'] = str(e)
    result['ready'] = bool(result['source_verified'] and result.get('bun_version') == VERSION and
                           result['dependencies'] and result['ffmpeg'] and result['browser'] is True and result['pixel_comparison'])
    return result


def setup(browser=False, system_deps=False, download_bun=False):
    if not browser:
        raise ValueError('Full setup launches an owned browser smoke test; pass --allow-browser where permitted')
    print('runtime: verify/install pinned Bun', file=sys.stderr, flush=True)
    bun = ensure_bun(download_bun)
    source = prepare_engine(); env = env_for(source)
    print('runtime: install frozen dependencies in user cache', file=sys.stderr, flush=True)
    run([bun, 'install', '--frozen-lockfile', '--ignore-scripts'], cwd=source / 'scripts', env=env)
    ff = source / 'scripts/node_modules/ffmpeg-static' / ('ffmpeg.exe' if platform.system() == 'Windows' else 'ffmpeg')
    if not ff.is_file():
        print('runtime: install ffmpeg', file=sys.stderr, flush=True)
        run([bun, 'node_modules/ffmpeg-static/install.js'], cwd=source / 'scripts', env=env)
    if system_deps and platform.system() == 'Linux':
        run([bun, 'node_modules/playwright/cli.js', 'install-deps', 'chromium'], cwd=source / 'scripts', env=env)
    print('runtime: install Chromium', file=sys.stderr, flush=True)
    run([bun, 'node_modules/playwright/cli.js', 'install', '--no-shell', 'chromium'], cwd=source / 'scripts', env=env)
    print('runtime: launch browser, check pixels and compare repeated capture', file=sys.stderr, flush=True)
    result = doctor(source, browser=True)
    safe_write_path(runtime_dir() / 'setup-receipt.json').write_text(json.dumps(result, indent=2) + '\n')
    if not result['ready']:
        raise ValueError('Runtime is not ready: ' + json.dumps(result) + '\nOn supported Linux, install browser OS libraries with setup --with-system-deps (requires apt/root permission).')
    return result
