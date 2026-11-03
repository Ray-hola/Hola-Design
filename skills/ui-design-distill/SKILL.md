---
name: ui-design-distill
description: >-
  Distill an existing product interface into reusable task, component and state
  design rules for a product-specific skill. Use for dashboards, editors, forms,
  settings or mobile/desktop app references, from code, screens or observed
  interaction. Screenshots alone yield partial visual guidance; public marketing
  pages belong to web-design-distill.
---

# UI Design Distill

Extract how a person works with a product, as well as its visual system. Keep
objects, user tasks, component semantics and state transitions separate from
the CSS that presents them.

Resolve `SKILL_ROOT` to the absolute folder containing this file. Profile tools
need Python 3.9+; browser capture needs an existing Playwright page adapter.

## LOOP gate: open it before extracting

The three loops are how this skill works, not a release step after it. Open them
for every distillation, whatever its destination: a profile or package, a change
to this or another skill's references, recipes or method notes, a report or notes.

1. Before parsing, capturing or rendering any source, read
   [loop-protocol.md](references/loop-protocol.md) and
   [loop-exit.md](references/loop-exit.md). Create the working profile, then the
   journal with `scripts/loop_tools.py init`.
2. Record every source-derived statement in the profile first, with evidence IDs
   and status. This includes recipe cards, method notes and summaries. Write any
   derived text from checked records, not from memory of the sources. Do not file
   source-derived lessons as generic proposals: that bypasses evidence status.
3. Private or restricted sources change where records live, not whether they
   exist. Keep the profile, evidence and journal in a local folder outside any
   published tree, and publish only own-words text derived from checked records.
4. Several references form one profile with a source set per file. A rule cites
   evidence from each reference it claims to cover. Files from one template family
   or author are dependent evidence, not independent repetition.
5. Run the distillation loop before writing derived text, the design loop on an
   actual new artifact that applies it, and the feedback loop on a new task.
6. Start the final report with the current `finish` state: PASS for its recorded
   scope, or HOLD, UNVERIFIED, BLOCKED or INTERRUPTED with the reason. Without a
   journal the state is UNVERIFIED; say so first, not in a limitations list.

None of these waives a loop: labeling output "candidate", "proposed" or
"untested"; repository checks or unit tests passing; source volume, tool setup or
time spent; editing a skill instead of packaging one. Only the user can narrow or
skip a loop. Record that as a scope change and report the unrun loops as unfinished.

## Distillation method

Before interpreting a reference, read [distill-method.md](references/distill-method.md):
product theme/audience/function/purpose/context → domain structure → visual roles
and relationships → conditional rules → new-content validation. Record reference
intent separately from the new brief. Inspect size relationships, color roles,
spacing rhythm, frame versus text alignment and relevant media/information/motion.
Use exact, relative, ranged, categorical or qualitative expressions as evidence
allows; do not invent precision. A repeated value is a candidate, not a universal rule.
See [analysis-contract.md](references/analysis-contract.md) for evidence-graded
`intent` and optional visual relationship fields. Narrow style-only requests can
remain partial; record unknowns instead of filling all dimensions.

## 1. Set the task boundary

Establish the product surface, actor, objects, primary job, platform and input
method from available context. A narrow component request needs only that
component's scope. Preserve existing identity and the user's chosen stack.

## 2. Inspect the real product

Read [extraction.md](references/extraction.md). Trace the requested surface to
the components/theme owners actually used. Record declared, used and computed
values separately; preserve documented exceptions and conflicts.

With a Playwright page adapter, [capture-ui.js](scripts/capture-ui.js) captures
visible controls, accessible-name candidates, local geometry/styles and landmarks
at the current state. It does not click, submit, read field values or prove a
workflow. Observe permitted actions or supplied recordings separately and save
action-result traces. Do not perform account mutations just to gather examples.

## 3. Extract task and component patterns

Read [patterns.md](references/patterns.md). Distinguish components that look
alike but serve different purposes. Record actual states and transitions, data
ranges and recovery routes. Mark disabled/loading/permission/error states not
inspected as unknown. A static screen does not prove interaction behavior.
Read [design-reasoning.md](references/design-reasoning.md) when learning interaction
logic: connect intention, expectation, action, feedback and continuity; explain
when disclosure helps and when simultaneous information is necessary. Preserve the
mechanism and its conditions rather than accumulating component appearances.
For type, color, space, information and motion evidence distinctions read
[visual-evidence.md](references/visual-evidence.md) when relevant.

For a screenshot-only reference, produce a useful visual subset and identify
the missing task evidence. Do not ask for unavailable interaction merely to
fill fields. Read [evidence.md](references/evidence.md) and
[profile.md](references/profile.md) when authoring the UI profile.

## 4. Package

```bash
python3 "$SKILL_ROOT/scripts/profile_tools.py" validate profile.json
python3 "$SKILL_ROOT/scripts/profile_tools.py" package profile.json \
  --name example-product-ui --out ./distilled-skills
```

Observed task paths must be backed by recorded states and observed transitions;
the validator rejects static evidence promoted to a proven interaction. It still
cannot certify usability or the truth of manually supplied observations.

## 5. Test a new operation

Read [evaluation.md](references/evaluation.md). Give the consumer a new task in
the product's domain and check its path, meaningful states, errors, keyboard or
platform behavior and visual consistency. Reuse existing native/headless controls
before implementing custom behavior. Accessibility gaps in a source are recorded
as gaps, not copied as binding design constraints.

Report the task/component coverage, unknowns, inferred rules, package path and
per-check evidence. Do not infer task completeness from a good-looking screenshot.

## Three-loop review and release

Keep [loop-protocol.md](references/loop-protocol.md) open from the LOOP gate onward.
Use [loop-checklist.json](references/loop-checklist.json) for this scene's checks.
Run the distillation loop before packaging, the design loop on actual output, and
feedback on a new task using the generated skill. Attribute failures before
changing the tool, product skill, output or supported scope. Apply the shared
repair budget across re-entry; skipped tests remain incomplete.

```bash
python3 "$SKILL_ROOT/scripts/loop_tools.py" init profile.json --out review.json
# Fill concrete benchmarks, evidence, checks and any repairs; inspect real artifacts.
python3 "$SKILL_ROOT/scripts/loop_tools.py" validate review.json --profile profile.json
python3 "$SKILL_ROOT/scripts/profile_tools.py" package profile.json --review review.json \
  --name example-reviewed-reference --out ./distilled-skills
```

## Sharing a distilled package

Packaging copies the profile, evidence values, selected artifacts and any supplied
review journal. It does not redact private data or grant redistribution rights.
Before sharing the result, inspect that exact output for credentials, signed URLs,
local paths, private content and source assets. Share only the materials permitted
for the intended audience; retain applicable licenses and attribution. Keep
restricted captures local and transfer the design reasoning in your own words.
A design LOOP PASS is not a privacy or copyright clearance.

Draft packages are testable before the outer loop. Call a package reviewed only
for its recorded scope when all three loops are accepted. Author-run tests do not
establish independent transfer. Report outstanding failures and source coverage
alongside review state; never use a package's existence as proof of design quality.

## Practical resources

For questions about objects, controls, states, grouping, errors or recovery, read
[design-principles.md](references/design-principles.md). Use `scripts/principles.py`
to find a question or create an unanswered worksheet. Test actual paths; these
questions do not establish behavior, current compliance, or observed brand rules.

Read [toolkit.md](references/toolkit.md) when starting a new task or looking for a
concrete implementation approach. Use `scripts/kit.py init --out ./design-task`
for the scene's editable brief, evidence worksheet, scoped-decision plan, stress
content and runnable neutral preview. Search the conditional
[recipe cards](references/recipes.json) with `scripts/kit.py search "keywords"
--profile profile.json`; learned records and generic proposals stay separate.
Do not adopt a template's demo content or neutral values as source facts.

For an uncovered implementation choice, `scripts/kit.py catalog "error summary
validation" --domain ux` queries the bundled pinned UI UX Pro Max catalog.
`--stack react` retrieves stack guidance, and `--recommend` returns a proposed
design system. Inspect only relevant results. Keep source identity and current
brief constraints; recommendations do not alter a profile. Use
`profile_tools.py package ... --with-catalog` to include the optional catalog in
a portable generated skill. The upstream MIT license and file provenance remain
inside `vendor/ui-ux-pro-max/`.

## Typeface study and creative departures

Read [type-and-creative.md](references/type-and-creative.md) for source typography,
art lettering, specimen collection and creative comparison. Record typefaces and
valuable unique design_cases even without repetition. Interpret departures through
intent and visual relationships; do not penalize novelty for failing a familiar
pattern. When designing, explore promising alternative type/composition choices
and compare actual outputs. New review journals use adaptive exploration, with
explicit user limits honored. Two unchanged attempts prompt a new direction,
not a global stop. Keep font verification and inferred design concepts distinct.

## Required review closure

Before claiming a result has been reviewed, read
[review-closure.md](references/review-closure.md). Declare subjects and actual
contexts, check whole/detail/relations, and bind observations to final artifact
hashes. After changes recheck affected neighbours and contexts. Captured is not
inspected, and local review is not whole-deliverable review. Run
`scripts/loop_tools.py finish review.json --profile profile.json --artifact-root
./design-task`; report its scope and remaining gaps if it does not close. Creative
departures remain hypotheses to compare, not automatic failures.

For expressive design work, actively try promising random or intuitive residuals,
even on a passing candidate. Preserve a baseline, inspect actual alternatives and
choose by intent and whole composition; unexpected gains may open a new direction.
Use existing experiments and the residual exploration section of
[type-and-creative.md](references/type-and-creative.md). No perturbation quota or
required gain; keep rigorous coverage for the retained delivery without automatically
normalizing departures from convention.

Before declaring completion, use [loop-exit.md](references/loop-exit.md). Record
positive quality reasons, inspect the weakest subject and resolve the strongest
objection. Close its integrity gate on rendered work: ground, objects, every display
context and the export, with crossings and crops tested by their observed effect. Only a current `finish` result with `loop_exit.state=PASS` permits a
scoped completion claim. HOLD, UNVERIFIED, BLOCKED and INTERRUPTED are unfinished
states; coverage alone does not establish quality.

On a new quality objection, follow loop-exit.md and run `reopen` on every
affected review journal before repair. Do not bulk-fill passed judgments or
substitute intent explanations/unrelated comparisons for the actual question.

## Method lessons from Impeccable

When scoping ambition, reviewing a render or closing repairs, read
[impeccable-lessons.md](references/impeccable-lessons.md): adopted lessons with source
locators and limits, plus what was deliberately not adopted. They are method
candidates, not rules of a learned reference.
