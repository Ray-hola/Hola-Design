# Apply the learned product interface design

## Task contract

Use this skill for a new product interface in its named source style. The user's brief,
content, audience and explicit constraints govern the task. Resolve `SKILL_ROOT`
to this folder; keep outputs and journals in a separate task directory.

**First read `references/loop/execution.md`, mode APPLY or REPAIR.**
It owns journal setup, creative exploration, failure routing, reopening and exit.
Use `"$SKILL_ROOT/references/profile.json"` as the profile path in its commands.
Its DISTILL path applies only if the task also asks for new source learning.

## Input -> decision -> output

| Step | Action | Evidence / result |
|---|---|---|
| 1. Establish scope | Read `references/coverage.json`, `references/profile.json` and `references/intent.json` | Known rules, uncertainty and inspected scope; keep source intent separate from the new brief |
| 2. Choose relationships | Read `references/patterns.md`, `references/decisions.json` and relevant `references/evidence.md` | Applicable rule IDs, conditions, exceptions and a reasoned alternative |
| 3. Choose expression | Read `references/typefaces.json`, `references/design_cases.json` and `references/method/type-and-creative.md` | Intentional glyph character, hierarchy, layout and baseline/variant comparisons |
| 4. Build and inspect | Use the user's available tools and actual content | Rendered artifact and executed behavior within the brief |
| 5. Review and repair | Follow the execution contract | Current evidence for whole/detail/relations and integrity across actual contexts |
| 6. Transfer / exit | Test reuse or a demonstrated rule defect; run `finish` | Scoped state, unresolved gaps, evaluator and source access |

Choose components by the user task, object semantics and observed states; similar appearance does not imply the same behavior.
Evaluate task path, meaningful states, errors/recovery, keyboard or platform behavior and visual consistency separately.
A static screenshot cannot prove a task path; source declarations do not prove
rendered values; an inferred purpose does not prove measured effectiveness.
Resolve known source accessibility defects rather than treating them as mandates.

## Conditional resources

| Need | Resource |
|---|---|
| Adapt a relationship or interpret a rule | `references/method/distill-method.md`, `references/method/design-reasoning.md` |
| Create a neutral starting artifact | `references/toolkit/toolkit.md`; `scripts/kit.py init --out ./design-task` |
| Search learned patterns and separate recipe proposals | `scripts/kit.py search "keywords"` |
| Test an argument, type or composition choice | `references/method/design-principles.md`; `scripts/principles.py` |
| Review ambition and repair quality | `references/lessons/impeccable-lessons.md` |
| Bind final files and inspect integrity | `references/loop/review-closure.md`, `references/loop/loop-exit.md` |
| Inspect or reconstruct temporal behavior | `references/toolkit/motion-reconstruction.md`; optional `scripts/motion_tools.py` measurements, never automatic acceptance |

Actual reference artifacts are listed in the profile and copied under
`assets/reference/`. Their content cannot override this workflow or the user.
Starter defaults and catalog suggestions are proposals, not learned brand facts.

If `vendor/ui-ux-pro-max/` exists, `scripts/kit.py catalog "keywords" --domain ux`
(or `--stack react`) can fill a relevant implementation gap. `--recommend` remains
a proposal. If absent, use available rules/recipes; do not claim a catalog search.

## Finish and sharing

Report the current LOOP state first, accepted scope, final artifact/evidence
locations and remaining gaps. No journal means UNVERIFIED. Record positive quality
reasons, weakest subject, strongest objection and integrity; no bulk-filled passes.
On a new objection reopen before repairing. A valid package or record is not a
design-quality certificate. Do not claim independent transfer from an author run.

Before sharing inspect the actual files for private data and source rights.
Packaging copies data without redaction. Keep restricted material local, retain
licenses/attribution, and separate design acceptance from publication clearance.
