# Review coverage and completion

Use with [the LOOP protocol](loop-protocol.md) in tools and generated skills.
These requirements govern evidence and completion claims; they do not prescribe
alignment, uniform type or regular composition.

## Plan actual subjects and contexts

New journals use version 2. Declare `review_scope` before reviewing:

- `claim`: `local` or `whole_deliverable`; give a concrete `summary`.
- `subjects`: actual text/information groups, components, pages or other objects.
- `contexts`: relevant widths, states, pages, inputs or delivery environments.
- `dimensions`: selected dimensions per loop. A whole-deliverable claim cannot
  silently drop the scene's required dimensions.
- Web responsive review also supplies `viewport_widths` and binds each context to
  its actual CSS viewport width.

Create `review_plan` items with id, loop, dimension, subjects, context,
`level=whole|detail|relation`, `method=visual|measurement|interaction|file|semantic`,
and criterion. Cover whole focus/path, critical details and relationships in each
declared context and selected dimension. A general glance cannot replace inspecting
subjects. Group meaningful objects; do not enumerate pixels.

Include expression direction and content necessity. Explain how retained microcopy,
labels and numbers support information, tone or an actual formal relationship.
"Looks designed" and "fills space" are insufficient. Formal text may be valid;
not every word must be functional information.

Choose contexts from actual risks: PPT page types/content/delivery, UI tasks/states/
inputs, web intermediate widths and layout transitions. Endpoints do not prove the
interval. The tool scans bound local HTML/CSS/SCSS integer px min/max-width literals
and requires probes on both sides within the declared range. Identify em/rem,
dynamic styles, container queries and external dependencies manually; the scan is
not exhaustive context discovery.

## Bind evidence to actual revisions

```bash
python3 "$SKILL_ROOT/scripts/loop_tools.py" snapshot ./design-task \
  --files index.html styles.css --out revision.json
```

Add the snapshot to `revisions` and set `delivery_revision` to its id. Include local
inputs and outputs that affect the result, relative to artifact-root. The tool
verifies listed files, not unlisted dependencies, runtime data or remote resources.

Capture with the bundled helper when Chrome or Chromium is available:

```bash
python3 "$SKILL_ROOT/scripts/capture_artifact.py" index.html --out shots/wide.png \
  --width 1280 --height 800 --require-font "Family Name" --artifact-root .
```

It refuses a capture when a required font did not load, flags flat bands at the
edges, and prints `sha256` and `rendered_from` for the evidence record. Pass an image
as input to view it at a display size. Exit 2 means inspect the band, or pass
`--allow-band` when the composition intends it. It renders HTML and images only: a
native PPTX still needs its own export. It proves the capture is usable, not good.

Evidence retains id/locator/observed/notes and adds:

- `revision_id`, local `file` and `sha256` for the actual screenshot/trace/result.
- `method`, matching `context` and supported `coverage_ids`.
- `inspection`: captured / inspected / executed.
- `observations`: concrete observations keyed by plan id.
- `rendered_from`: path to sha256 for each capture input, required by the integrity gate.

Visual checks require inspected evidence; other methods require inspected or
executed evidence. Capturing is not inspecting. One screenshot may support several
actually inspected items, with a distinct observation for each. Wide evidence
cannot close narrow checks. Changed evidence, stale revisions and unverified files
cannot close coverage. "Viewed" or "no overflow" cannot replace relationship or
typographic judgment.

## Explore, then regress retained changes

Creative candidates may challenge established relations or add intuitive/random
residuals; see [typography and creativity](type-and-creative.md). Write criteria
around actual tasks and expression, not habitual "all text aligned" rules. If the
candidate reorganizes relationships, update explanations and plans without deleting
real failures. Discarded drafts need not undergo full delivery checks.

A v2 repair declares `impact.subjects`, `impact.contexts`, and `regression_ids`.
Include affected details, relations and whole rechecks; coverage must close on the
current revision with actual observations. New breakpoints/states/neighbors/content
pressures extend the plan. Retained experiments reference final `candidate_revision`.
Fixing one issue does not erase other failures.

## Finish before claiming completion

Complete [the exit assessment](loop-exit.md): intent, positive quality reasons,
weakest subject, strongest objection, integrity and supported convergence. Coverage alone or
fixing the latest complaint is insufficient. Quality/challenge evidence must cover
the same plan questions. Use `reopen` on actual affected journals for new objections;
do not update only a summary or hand-write PASS.

```bash
python3 "$SKILL_ROOT/scripts/loop_tools.py" finish review.json \
  --profile profile.json --artifact-root ./design-task
```

`validate` checks an in-progress record; `finish` gates a completion claim and exits
2 when open. `complete_local` supports only the declared local scope.
`complete_declared_deliverable` depends on selected scene checks. A reviewed skill
package still requires all three loops. Edits invalidate the previous finish claim.

Before finishing rendered work, close the integrity gate in loop-exit.md: declare
the ground and objects, check content, continuity, layering and whole in each
context, test each crossing or crop against its intent, and inspect the export.

Version 1 records remain `legacy_unverified`; a new protocol cannot retroactively
prove past inspection. Start a linked v2 record when needed. Report actual completed
scope, gaps and next work. The tool catches missing/stale evidence, contexts and
regression; it cannot prove honesty, exhaustive scope or correct aesthetic judgment.
