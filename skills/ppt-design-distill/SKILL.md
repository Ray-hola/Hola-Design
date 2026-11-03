---
name: ppt-design-distill
description: >-
  Distill reference PPTX decks, slide PDFs or slide images into a reusable
  presentation design skill: visual language, slide-type selection, content
  capacity and cross-slide organization. Use for learning a deck's design or
  extracting a presentation style for new content. This is a reference-learning
  workflow, not a generic request to write slide content or design product UI.
---

# PPT Design Distill

Learn how a presentation organizes meaning across pages, then package rules
that can guide a different topic. Keep visual style, page patterns and deck
organization distinct. Source assets and brand constraints take precedence over
generic recommendations.

Resolve `SKILL_ROOT` to the absolute folder containing this file. Its parser,
profile validator and packager need Python 3.9+ standard library only.

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

## 1. Establish the viewing situation

Use known audience, purpose, live-talk/self-read/remote mode, canvas and delivery
format. State reasonable assumptions; ask only if the choice changes the task.
Honor a narrow style-only request without forcing narrative reconstruction.

## 2. Collect evidence

Read [extraction.md](references/extraction.md) for the input path. PPTX has a
standard-library parser:

```bash
python3 "$SKILL_ROOT/scripts/extract_pptx.py" reference.pptx --out evidence.json
```

It reads actual presentation order, theme declarations, masters/layouts, local
text/shape geometry and style statistics. XML declarations are not final rendered
values. Render/view the cover and representative content pages when tools permit;
inspect the full sequence for narrative claims. PDF/images use visual evidence
and relative geometry, not fabricated font names, master rules or animation.

## 3. Extract rules and patterns

Use [patterns.md](references/patterns.md). Record page purposes and when they
fit, what content they require, what changes with text length, and observed
relations across pages. A single exceptional slide is not a global constraint.
Capture data encoding and image selection alongside typography and composition.
Reasons inferred from a deck remain inferences, even when plausible. For subtle
measurement/role distinctions read [visual-evidence.md](references/visual-evidence.md).

Read [evidence.md](references/evidence.md) and [profile.md](references/profile.md)
when writing the presentation profile. Leave unknowns explicit; do not fill
animation, illustration or sequence sections merely to complete a template.

## 4. Package a consumer skill

```bash
python3 "$SKILL_ROOT/scripts/profile_tools.py" validate profile.json
python3 "$SKILL_ROOT/scripts/profile_tools.py" package profile.json \
  --name example-presentation --out ./distilled-skills
```

The package holds a trusted presentation workflow, domain patterns, evidence,
decisions, coverage and declared reference artifacts. A structure-valid partial
profile can be packaged with warnings; report its limited scope. The output is
a normal agent skill, independent of any one presentation application.

## 5. Test new content

Read [evaluation.md](references/evaluation.md). Generate an original short deck
or the requested sample using a new topic/content shape, choosing page types for
that content. Validate story, readability, page fit, consistency and editability
separately. A preview validates only the patterns it exercises.

Report source coverage, inferred decisions, package location and each check as
passed/failed/skipped. Do not claim transfer success if only XML/JSON was checked.

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

For questions about argument structure, comparison, typography, learning or creative
composition, read [design-principles.md](references/design-principles.md). Use
`scripts/principles.py` to find a question or create an unanswered worksheet. These
questions are not observed evidence of the current reference.

Read [toolkit.md](references/toolkit.md) when starting a new task or looking for a
concrete implementation approach. Use `scripts/kit.py init --out ./design-task`
for the scene's editable brief, evidence worksheet, scoped-decision plan, stress
content and runnable neutral preview. Search the fourteen conditional
[recipe cards](references/recipes.json) with `scripts/kit.py search "keywords"
--profile profile.json`; learned records and generic proposals stay separate.
Do not adopt a template's demo content or neutral values as source facts.

## Lessons from a business presentation corpus

When choosing density, a title system, cross-page navigation or page patterns, read
[presentation-corpus-lessons.md](references/presentation-corpus-lessons.md). It holds
anonymized lessons from 34 private decks, with their limits. They are candidates to
test, not facts about the current reference or a house style.

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
