#!/usr/bin/env python3
"""Read PPTX order, declarations and local geometry without changing the deck.

Standard library only. Does not render, resolve all inheritance or inspect media.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path, PurePosixPath
import posixpath
import sys
import zipfile
import xml.etree.ElementTree as ET

NS = {"p": "http://schemas.openxmlformats.org/presentationml/2006/main",
      "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
      "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships"}
REL = "{http://schemas.openxmlformats.org/package/2006/relationships}"


def xml(archive, member):
    data = archive.read(member)
    if b"<!DOCTYPE" in data.upper() or b"<!ENTITY" in data.upper():
        raise ValueError(f"Unsupported XML entity declarations in {member}")
    return ET.fromstring(data)


def relationships(archive, part):
    p = PurePosixPath(part)
    name = str(p.parent / "_rels" / (p.name + ".rels"))
    if name not in archive.namelist():
        return {}
    result = {}
    for rel in xml(archive, name):
        if rel.tag != REL + "Relationship":
            continue
        target = rel.get("Target", "")
        external = rel.get("TargetMode") == "External"
        result[rel.get("Id")] = {
            "type": rel.get("Type", "").rsplit("/", 1)[-1],
            "external": external,
            "target": target if external else posixpath.normpath(posixpath.join(str(p.parent), target)) if not target.startswith("/") else target.lstrip("/")}
    return result


def color(node):
    for child in node:
        kind = child.tag.rsplit("}", 1)[-1]
        if kind == "srgbClr":
            return {"kind": "srgb", "value": "#" + child.get("val", ""), "transforms": [dict(x.attrib) for x in child]}
        if kind == "schemeClr":
            return {"kind": "theme-reference", "value": child.get("val"), "transforms": [dict(x.attrib) for x in child]}
        if kind in {"sysClr", "prstClr"}:
            return {"kind": kind, "value": child.get("val"), "fallback": child.get("lastClr")}
    return None


def local_styles(node):
    sizes, fonts, colors = Counter(), Counter(), Counter()
    for run in node.iter():
        if run.tag in {f"{{{NS['a']}}}rPr", f"{{{NS['a']}}}defRPr", f"{{{NS['a']}}}endParaRPr"}:
            if run.get("sz"):
                sizes[run.get("sz")] += 1
        if run.tag in {f"{{{NS['a']}}}latin", f"{{{NS['a']}}}ea", f"{{{NS['a']}}}cs"} and run.get("typeface"):
            fonts[run.get("typeface")] += 1
        if run.tag == f"{{{NS['a']}}}solidFill":
            value = color(run)
            if value:
                colors[json.dumps(value, sort_keys=True)] += 1
    return {"font_sizes_pt": [{"value": int(k) / 100, "count": v} for k, v in sizes.most_common()],
            "fonts": [{"value": k, "count": v} for k, v in fonts.most_common()],
            "colors": [{**json.loads(k), "count": v} for k, v in colors.most_common()],
            "status": "declared", "inheritance_resolved": False}


def shapes(tree, canvas, parents=()):
    result = []
    for node in tree:
        kind = node.tag.rsplit("}", 1)[-1]
        if kind not in {"sp", "pic", "graphicFrame", "grpSp", "cxnSp"}:
            continue
        name_node = node.find(".//p:cNvPr", NS)
        shape_id = name_node.get("id") if name_node is not None else None
        placeholder = node.find(".//p:ph", NS)
        transform = None
        for location in ["p:spPr/a:xfrm", "p:xfrm", "p:grpSpPr/a:xfrm"]:
            candidate = node.find(location, NS)
            if candidate is not None:
                transform = candidate
                break
        bounds = None
        if transform is not None:
            offset = transform.find("a:off", NS)
            extent = transform.find("a:ext", NS)
            if offset is not None and extent is not None:
                bounds = {"x": int(offset.get("x", 0)), "y": int(offset.get("y", 0)),
                          "width": int(extent.get("cx", 0)), "height": int(extent.get("cy", 0))}
        paragraphs = ["".join(t.text or "" for t in p.findall(".//a:t", NS)) for p in node.findall("p:txBody/a:p", NS)]
        shape = {"id": shape_id, "name": name_node.get("name") if name_node is not None else None,
                 "kind": kind, "parent_groups": list(parents), "paragraphs": paragraphs,
                 "text_runs": [t.text or "" for t in node.findall(".//a:t", NS)] if kind != "grpSp" else [],
                 "placeholder": dict(placeholder.attrib) if placeholder is not None else None,
                 "local_bounds_emu": bounds, "styles": local_styles(node)}
        if bounds and canvas and not parents:
            shape["canvas_ratios"] = {"x": bounds["x"] / canvas["width"], "y": bounds["y"] / canvas["height"],
                                       "width": bounds["width"] / canvas["width"], "height": bounds["height"] / canvas["height"]}
        else:
            shape["canvas_ratios"] = None
        if kind == "grpSp":
            shape["children"] = shapes(node, canvas, parents + (shape_id,))
        result.append(shape)
    return result


def part_report(archive, part, canvas):
    tree = xml(archive, part)
    sp_tree = tree.find("p:cSld/p:spTree", NS)
    if sp_tree is None:
        sp_tree = tree.find("p:spTree", NS)
    return {"part": part, "name": tree.get("name"), "styles": local_styles(tree),
            "shapes": shapes(sp_tree, canvas) if sp_tree is not None else [],
            "relationships": relationships(archive, part)}


def extract(source):
    if not zipfile.is_zipfile(source):
        raise ValueError("Expected an unencrypted OOXML PPTX ZIP archive")
    with zipfile.ZipFile(source) as archive:
        members = archive.infolist()
        if sum(x.file_size for x in members) > 1024 * 1024 * 1024 or any(x.file_size > 64 * 1024 * 1024 for x in members if x.filename.endswith(".xml")):
            raise ValueError("Archive exceeds the parser's 1 GiB expanded / 64 MiB XML limits")
        if "[Content_Types].xml" not in archive.namelist() or "ppt/presentation.xml" not in archive.namelist():
            raise ValueError("Missing OOXML content types or presentation part")
        presentation = xml(archive, "ppt/presentation.xml")
        size = presentation.find("p:sldSz", NS)
        canvas = {"width": int(size.get("cx")), "height": int(size.get("cy")), "unit": "EMU"} if size is not None else None
        if canvas and (canvas["width"] <= 0 or canvas["height"] <= 0):
            raise ValueError("Nonpositive slide dimensions")
        rels = relationships(archive, "ppt/presentation.xml")
        slide_ids = presentation.find("p:sldIdLst", NS)
        if slide_ids is None or len(slide_ids) == 0:
            raise ValueError("No slides in the presentation order")
        slides = []
        for index, slide in enumerate(slide_ids, 1):
            relationship = rels.get(slide.get(f"{{{NS['r']}}}id"), {})
            if relationship.get("type") != "slide" or relationship.get("external"):
                raise ValueError(f"Unresolvable slide relationship at presentation index {index}")
            report = part_report(archive, relationship["target"], canvas)
            report.update(index=index, presentation_id=slide.get("id"))
            report["layout"] = next((x["target"] for x in report["relationships"].values() if x["type"] == "slideLayout" and not x["external"]), None)
            slides.append(report)
        themes = []
        for part in archive.namelist():
            if not (part.startswith("ppt/theme/") and part.endswith(".xml")):
                continue
            tree = xml(archive, part)
            palette = tree.find("a:themeElements/a:clrScheme", NS)
            fonts = tree.find("a:themeElements/a:fontScheme", NS)
            themes.append({"part": part, "name": tree.get("name"), "status": "declared",
                           "colors": {x.tag.rsplit("}", 1)[-1]: color(x) for x in palette} if palette is not None else {},
                           "fonts": [{"role": x.tag.rsplit("}", 1)[-1], "faces": [dict(y.attrib) for y in x]} for x in fonts] if fonts is not None else []})
        layouts = [part_report(archive, n, canvas) for n in sorted(archive.namelist()) if n.startswith("ppt/slideLayouts/") and n.endswith(".xml")]
        masters = [part_report(archive, n, canvas) for n in sorted(archive.namelist()) if n.startswith("ppt/slideMasters/") and n.endswith(".xml")]
        return {"source": str(source.resolve()), "sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
                "canvas": canvas, "themes": themes, "slides": slides, "layouts": layouts, "masters": masters,
                "media_count": sum(n.startswith("ppt/media/") and not n.endswith("/") for n in archive.namelist()),
                "limitations": ["Declarations and local geometry only; not rendered evidence.",
                                "Master/layout inheritance and group transforms are not fully resolved.",
                                "Images, charts, animations and narrative intent require separate inspection."]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    try:
        result = extract(args.source)
        if args.out.exists():
            raise FileExistsError(f"Output exists: {args.out}")
        args.out.parent.mkdir(parents=True, exist_ok=True)
        with args.out.open("x", encoding="utf-8") as output:
            json.dump(result, output, ensure_ascii=False, indent=2)
            output.write("\n")
        print(json.dumps({"out": str(args.out), "slides": len(result["slides"]), "status": "declarations-only"}))
        return 0
    except (OSError, ValueError, KeyError, RuntimeError, zipfile.BadZipFile, ET.ParseError) as error:
        print(str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
