# Contributing

Hola-Design is a collection of four sibling skills, not an application framework.
Keep changes tied to a concrete distillation, design or review failure. Explain
the problem, the resulting behavior and the evidence behind the change.

## Where to work

- `skills/design-distill/` routes a brief; it does not implement the scene skills.
- `skills/{ppt,ui,web}-design-distill/` hold each scene's independent workflow.
- `shared/` is the single source for files every scene carries: method, record
  and LOOP references, starter files and common scripts. Edit them there, then run
  `python3 scripts/sync_shared.py`; the scene copies keep installed and generated
  skills portable. Tests fail when a copy drifts.
- Inside a scene, `references/` is grouped by role: `method/`, `records/`,
  `scene/`, `loop/`, `toolkit/` and `lessons/`. Packaging copies all but `scene/`.
- `assets/readme/` holds the final cover, its editable source, licensed source
  image and workflow artwork. Keep temporary studies and browser captures local.

Skill instructions, tools, metadata and supporting documents use English. Update
both README editions when public usage changes. Artifact copy can use the language
required by its brief.

## Checks

Python 3.9+ is sufficient for the core checks; no Python packages are required:

```sh
python3 scripts/check_repository.py
python3 scripts/sync_shared.py --check
python3 -m unittest discover -s tests
```

Installed Chrome or Chromium enables the browser capture tests. Those tests skip
when no browser is available; report that boundary. The legacy web extraction
pipeline additionally needs Node.js 18+ and its documented browser adapters.

For a visual change, render and inspect the relevant whole, details and
relationships. Record the actual contexts and final revision in your local LOOP
journal. Automated checks do not establish aesthetic quality or usability.

## Source and privacy boundaries

Preserve copyright notices and licenses. For a vendored change, update its
`UPSTREAM.json`, documenting both the upstream bytes and local modification. A
source link alone is not redistribution permission. Do not contribute reference
books, captured third-party pages, font binaries, private briefs, browser sessions,
credentials or task journals. See [the publication review](docs/PUBLICATION_REVIEW.md).

Use Issues for reproducible, non-sensitive problems and pull requests for focused
changes. The maintainer reviews scope and evidence before merging. Do not put a
credential or private source in an issue; revoke an exposed credential first and
contact the maintainer through an already established private channel.
