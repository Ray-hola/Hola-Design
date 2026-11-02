#!/usr/bin/env python3
"""Index a supplied font; optionally copy an explicitly redistributable asset/license."""
import argparse
import hashlib
import html
import json
from pathlib import Path
import shutil
import sys

FORMATS = {b"\x00\x01\x00\x00": "ttf", b"OTTO": "otf", b"ttcf": "ttc", b"wOFF": "woff", b"wOF2": "woff2"}


def collect(source, output, source_note, family, role, rights="unknown", license_file=None, sample_text="Letterforms, relationships, expression"):
    source = source.resolve()
    blob = source.read_bytes()
    format = FORMATS.get(blob[:4])
    if format is None:
        raise ValueError("Unrecognized font container signature")
    if output.exists() or output.is_symlink():
        raise FileExistsError("Preserve existing font entry: " + str(output))
    license_text = None
    if rights == "allowed":
        if license_file is None:
            raise ValueError("Copying requires the actual --license-file and a supported rights declaration")
        license_text = license_file.read_text(encoding="utf-8")
        if not license_text.strip():
            raise ValueError("License file is empty")
    data = {"family_label": family or source.stem, "identification": "unverified", "roles": [role],
            "source": source_note, "original_file": str(source), "sha256": hashlib.sha256(blob).hexdigest(),
            "container": format, "rights": rights, "asset": None,
            "meaning": "File signature/hash observed; family label is unverified. No font installation or complete font/coverage/license validation performed."}
    output.parent.mkdir(parents=True, exist_ok=True)
    output.mkdir()
    try:
        if rights == "allowed":
            name = "font." + format
            (output / name).write_bytes(blob)
            (output / "LICENSE.txt").write_text(license_text, encoding="utf-8")
            data.update(asset=name, license_file="LICENSE.txt")
        (output / "font.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        face = "@font-face{font-family:'Collected Typeface';src:url('" + data["asset"] + "')}" if data["asset"] else ""
        specimen = "<!doctype html><html lang='en'><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Typeface study</title><style>" + face + "body{margin:0;padding:clamp(20px,4vw,32px)}main{font-family:'Collected Typeface',serif}h1{font-size:clamp(32px,8vw,64px);line-height:1.15;overflow-wrap:anywhere}p{font-size:22px}</style><header>" + html.escape(data["family_label"]) + " · unverified specimen; inspect actual rendered glyph fonts</header><main><h1>" + html.escape(sample_text) + "</h1><p>Aa Bb — 0123456789 / punctuation, spacing &amp; contrast.</p><p>A longer heading should prompt another check of line breaks and letter spacing.</p></main></html>"
        if not data["asset"]:
            specimen = specimen.replace("<main>", "<p>Font binary not included: the text below uses fallback, not a verified specimen of the named face.</p><main>")
        (output / "specimen.html").write_text(specimen, encoding="utf-8")
    except Exception:
        shutil.rmtree(output)
        raise
    return data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--source", required=True)
    parser.add_argument("--family")
    parser.add_argument("--role", required=True)
    parser.add_argument("--rights", choices=["unknown", "restricted", "allowed"], default="unknown")
    parser.add_argument("--license-file", type=Path)
    parser.add_argument("--sample-text", default="Letterforms, relationships, expression", help="Actual copy in the intended writing system for a font specimen")
    args = parser.parse_args()
    try:
        print(json.dumps(collect(args.file, args.out, args.source, args.family, args.role, args.rights, args.license_file, args.sample_text), ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError) as error:
        print(json.dumps({"error": str(error)}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
