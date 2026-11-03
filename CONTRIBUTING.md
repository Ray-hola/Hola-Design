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
  skills portable. Tests fail when a copy drifts. The ownership manifest at
  `scripts/shared-manifest.json` also tracks removals and renames. Sync deletes
  only retired copies matching their last synchronized hash; an edited retired
  copy stops the operation before any writes. Resolve that conflict explicitly,
  then rerun sync. Do not manually reset the manifest to hide drift.
- Inside a scene, `references/` is grouped by role: `method/`, `records/`,
  `scene/`, `loop/`, `toolkit/` and `lessons/`. Packaging copies all but `scene/`.
- `assets/readme/` holds the final cover, its editable source, licensed source
  image and workflow artwork. Keep temporary studies and browser captures local.

Skill instructions, tools, metadata and supporting documents use English. Update
both README editions when public usage changes. Artifact copy can use the language
required by its brief.

## Local storage and commit attribution

- `private/`: local private repositories, source materials, journals, recovery
  backups and validation receipts. Never publish or automatically clean it.
- `temp/`: disposable task output. Pin an active or retained task with a `.keep`
  file inside its top-level task directory. Move evidence needed for later review
  into `private/` before cleanup eligibility.
- Both folders are ignored by Git. The publication checker skips their contents
  but fails if either folder has been forced into the Git index. Gitignore does
  not clear already published data; inspect history separately before publication.
- Do not add AI model or assistant `Co-authored-by` trailers to this project's
  commits. Preserve legitimate human authorship and third-party license notices.

Preview cleanup with `python3 scripts/clean_temp.py`. Use `--apply` to remove only
items in this repository's `temp/` whose entire contents have been unchanged for
14 days. `.keep`, nested Git repositories, symlinks and tracked items protect the
whole task directory. Private files are never candidates. A local Codex automation
may invoke this daily; cloning the repository does not install a scheduled task.

## Instruction changes

Keep selection and task scope in each `SKILL.md`. Put common execution decisions
in `shared/references/loop/execution.md`; keep domain knowledge in the scene's
references. State inputs, action, required evidence, next condition and failure
route. Use existing status/schema names; decorative syntax is not an executable
validator. Link details at the decision where they are needed. Keep creative
choices open and evidence/completion requirements explicit.

Maintenance checks validate files and behavior, not design acceptance. Learning
new references requires DISTILL records even when the result only updates a skill.
Preserve unverified historical learning as such; do not backfill an invented PASS.

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
