#!/usr/bin/env python3
"""Render a local HTML/image file with installed Chrome and refuse unusable captures.

Standard library only. Reports what was rendered; never judges the design.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import struct
import subprocess
import sys
import tempfile
import zlib

CHROME_PATHS = ("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                "/Applications/Chromium.app/Contents/MacOS/Chromium",
                "C:/Program Files/Google/Chrome/Application/chrome.exe")
CHROME_NAMES = ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "chrome")
PROBE = """<script>addEventListener('load',()=>document.fonts.ready.then(()=>{const root=document.documentElement.dataset;root.captureFonts=JSON.stringify([...document.fonts].filter(f=>f.status==='loaded').map(f=>f.family.replace(/["']/g,'')));root.captureBroken=JSON.stringify([...document.images].filter(i=>!i.naturalWidth).map(i=>i.getAttribute('src')))}));</script>"""
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg"}


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def find_chrome(explicit=None):
    candidates = [explicit, os.environ.get("CHROME_PATH"), *CHROME_PATHS, *map(shutil.which, CHROME_NAMES)]
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return candidate
    raise ValueError("Chrome or Chromium not found; pass --chrome or set CHROME_PATH")


def read_png(path):
    """Decode 8-bit RGB/RGBA PNG rows, enough to inspect a browser screenshot."""
    data = Path(path).read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("Capture is not a PNG: " + str(path))
    position, compressed, header = 8, bytearray(), None
    while position < len(data):
        length, kind = struct.unpack(">I4s", data[position:position + 8])
        body = data[position + 8:position + 8 + length]
        if kind == b"IHDR":
            header = struct.unpack(">IIBBBBB", body)
        elif kind == b"IDAT":
            compressed += body
        position += length + 12
    width, height, depth, color, _, _, interlace = header
    if depth != 8 or color not in {2, 6} or interlace:
        raise ValueError("Only 8-bit non-interlaced RGB/RGBA PNG can be inspected")
    channels = {2: 3, 6: 4}[color]
    raw, stride, offset = zlib.decompress(bytes(compressed)), width * channels, 0
    rows, previous = [], bytearray(stride)
    for _ in range(height):
        kind, row = raw[offset], bytearray(raw[offset + 1:offset + 1 + stride])
        offset += stride + 1
        for i in range(stride):
            left = row[i - channels] if i >= channels else 0
            up, corner = previous[i], previous[i - channels] if i >= channels else 0
            if kind == 1:
                row[i] = (row[i] + left) & 255
            elif kind == 2:
                row[i] = (row[i] + up) & 255
            elif kind == 3:
                row[i] = (row[i] + (left + up) // 2) & 255
            elif kind == 4:
                estimate = left + up - corner
                a, b, c = abs(estimate - left), abs(estimate - up), abs(estimate - corner)
                row[i] = (row[i] + (left if a <= b and a <= c else up if b <= c else corner)) & 255
        rows.append(row)
        previous = row
    return width, height, channels, rows


def edge_bands(path, share=0.05):
    """Find flat rows or columns at an edge: the mark of a capture that ran out of page."""
    width, height, channels, rows = read_png(path)
    pixel = lambda x, y: tuple(rows[y][x * channels:x * channels + 3])
    flat_row = lambda y: len({pixel(x, y) for x in range(0, width, max(1, width // 200))}) == 1
    flat_column = lambda x: len({pixel(x, y) for y in range(0, height, max(1, height // 200))}) == 1

    def run(indexes, flat):
        count = 0
        for index in indexes:
            if not flat(index):
                break
            count += 1
        return count

    runs = {"top": (run(range(height), flat_row), height), "bottom": (run(reversed(range(height)), flat_row), height),
            "left": (run(range(width), flat_column), width), "right": (run(reversed(range(width)), flat_column), width)}
    bands = {edge: count for edge, (count, size) in runs.items() if count >= max(2, size * share)}
    return {"width": width, "height": height, "flat_edge_bands": bands}


def capture(source, out, width, height, scale=1.0, require_fonts=(), chrome=None, proxy=None, wait_ms=15000):
    source, out = Path(source).resolve(), Path(out).resolve()
    if not source.is_file():
        raise ValueError("Missing input: " + str(source))
    browser = find_chrome(chrome)
    out.unlink(missing_ok=True)
    # The probe page sits beside the source so relative assets resolve; the source itself is untouched.
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".html", prefix=".capture-", dir=source.parent, delete=False) as file:
        page = Path(file.name)
        if source.suffix.lower() in IMAGE_SUFFIXES:
            file.write(f'<!doctype html><body style="margin:0"><img src="{source.name}" style="display:block;width:100%;height:auto">{PROBE}')
        else:
            file.write(source.read_text(encoding="utf-8") + PROBE)
    try:
        flags = [browser, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-first-run", "--allow-file-access-from-files",
                 f"--window-size={width},{height}", f"--force-device-scale-factor={scale}", f"--virtual-time-budget={wait_ms}"]
        if proxy:
            flags.append("--proxy-server=" + proxy)
        url = page.as_uri()
        dom = subprocess.run(flags + ["--dump-dom", url], capture_output=True, text=True, timeout=120).stdout
        attribute = lambda name: re.search(r'data-capture-%s="([^"]*)"' % name, dom)
        found, broken = attribute("fonts"), attribute("broken")
        if not found or not broken:
            raise ValueError("Refused capture: the page did not finish loading")
        fonts = json.loads(found.group(1).replace("&quot;", '"'))
        broken = json.loads(broken.group(1).replace("&quot;", '"'))
        if broken:
            raise ValueError("Refused capture: images failed to load: " + ", ".join(map(str, broken)))
        missing = [family for family in require_fonts if family not in fonts]
        if missing:
            raise ValueError("Refused capture: fonts did not load, the render would use fallbacks: " + ", ".join(missing))
        out.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(flags + ["--screenshot=" + str(out), url], capture_output=True, timeout=120)
    finally:
        page.unlink(missing_ok=True)
    if not out.is_file():
        raise ValueError("Chrome produced no capture")
    return {"file": str(out), "sha256": sha256(out), "rendered_from": {source.name: sha256(source)},
            "css_width": width, "css_height": height, "scale": scale, "loaded_fonts": fonts, **edge_bands(out)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="HTML or image to render; with --check, a PNG capture to inspect")
    parser.add_argument("--out", type=Path)
    parser.add_argument("--width", type=int, default=1600)
    parser.add_argument("--height", type=int, default=800)
    parser.add_argument("--scale", type=float, default=1.0, help="Device pixel ratio")
    parser.add_argument("--require-font", action="append", default=[], help="Refuse the capture unless this family loaded; repeatable")
    parser.add_argument("--chrome", help="Browser executable")
    parser.add_argument("--proxy", help="Proxy for remote assets such as web fonts")
    parser.add_argument("--artifact-root", type=Path, help="Report file and rendered_from relative to this folder, ready for a journal's evidence")
    parser.add_argument("--allow-band", action="store_true", help="A flat edge band is intended in this composition")
    parser.add_argument("--check", action="store_true", help="Inspect an existing PNG without rendering")
    args = parser.parse_args()
    try:
        if args.check:
            result = {"file": str(args.input), "sha256": sha256(args.input), **edge_bands(args.input)}
        else:
            if not args.out:
                parser.error("rendering requires --out")
            result = capture(args.input, args.out, args.width, args.height, args.scale, args.require_font, args.chrome, args.proxy)
        if args.artifact_root:
            root = args.artifact_root.resolve()
            result["file"] = str(Path(result["file"]).resolve().relative_to(root))
            if not args.check:
                result["rendered_from"] = {str(args.input.resolve().relative_to(root)): sha256(args.input)}
        result["usable"] = args.allow_band or not result["flat_edge_bands"]
        result["meaning"] = "Checks the capture exists, its size, loaded fonts and flat edge bands. Viewing it remains your job."
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result["usable"] else 2
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        print(json.dumps({"error": str(error)}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
