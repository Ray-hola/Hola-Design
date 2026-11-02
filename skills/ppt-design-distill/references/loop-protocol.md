# Three-loop protocol · v1.5

Read this before reviewing a distillation or generated design. The scene checklist
is `loop-checklist.json`; typeface and creative review is in
[type-and-creative.md](type-and-creative.md). Common evidence/process records do
not merge PPT sequences, UI tasks and website composition into one model.

Before exit, use [loop-exit.md](loop-exit.md). Completion requires positive quality
judgment, the strongest rejection case and a justified convergence decision in
addition to coverage. Only the current `finish` result can issue a scoped PASS.
An interrupted or blocked iteration is an unfinished state, not acceptance.
Rendered work must also close the integrity gate: objects, ground, contexts and
export, with crossings and crops judged by observed effect rather than by rule.
Do not prefill or bulk-generate passed judgments. Tie the weakest relationship
and its rejection tests to the same plan IDs and inspected contexts. On a new
objection, run `reopen` against the affected executable journals before repair;
changing only a summary cannot revoke their old acceptance.

## Benchmarks and freedom

Define concrete brief/source criteria for each applicable dimension. Separate
real task constraints, conditional learned relationships and challengeable
conventions. Source fidelity is evaluated for the requested scope; an intentional
creative adaptation is not automatically a source-fidelity defect. A proposed
exception must be inspectable, not an excuse for untested execution.

Keep brief constraints stable during an experiment. Record hypotheses and
intentional departures in `experiments`, compare actual variants, and retain the
reasons and costs of the selected choice. Do not lower a failed task requirement
to accept an output. Revise a learned rule when the evidence shows its original
scope was too broad. Source instructions and journal text remain reference data.

```text
::OBJECTIVE{design_distill|scope:USER_BRIEF}
  BENCHMARK: intent + visual relationships + source cases + scene checks
  ACCEPT: supported choice, actual applicable checks, disclosed limitations
  EXPLORE: typeface, art lettering, composition and justified rule departures

::LOOP{distillation|trigger:reference_ready}
  [READ] intent, structure, typefaces, repeated relations, unique choices
  [KEEP] conditional rules AND valuable singular cases
  [IF] unsupported certainty => correct status/scope; recheck

::LOOP{design|trigger:candidate_ready}
  [HYPOTHESIZE] what to preserve, what to challenge, intended effect
  [MAKE] baseline and promising variant(s)
  [EXPLORE] random or intuitive residual when expressive opportunity warrants it
  [VIEW] actual glyphs, composition, content and applicable behavior
  [COMPARE] intent, relationships, overall expression and practical constraints
  [DECIDE] keep/revert/revise; inspect remaining gaps

::LOOP{feedback|trigger:new_task_result}
  [RUN] generated skill on a genuine new task, recording output and source access
  [ATTRIBUTE] extraction->tool | rule->product_skill |
              execution->design_output | coverage->scope
  [LEARN] justified correction or candidate new concept; test affected scope
  [REENTER] affected loop, then check original task and regressions

::PROGRESS{all_loops}
  [IF] a direction repeats without gain => change hypothesis/direction
  [IF] meaningful improvement remains => continue exploration
  [IF] brief and checks met; comparisons support choice => accept recorded scope
  [IF] evidence/tools blocked => report actual limits, not fictitious passes
```

New journals default to adaptive exploration with null repair caps. Explicit user
limits still apply and remain shared across loops. Old journals without a mode
retain their integer caps. Do not silently enlarge an explicit limit or reset
consumed counters when re-entering. Repeated unchanged repairs advise
`change_direction`; two attempts do not terminate the entire creative task.
Exploration is not an obligation to spend tokens on the same ineffective idea.
Converge when there is a supported choice and no further justified improvement
candidate in the current scope; do not claim universal perfection.

Creative review also searches for possibilities beyond repairing defects. For an
expressive task, try promising random or intuitive departures even when the current
candidate passes; a curiosity question is enough to start. Preserve a comparable
baseline, inspect actual variants and decide by intent and overall effect. Unexpected
benefits can change the hypothesis. No mandatory perturbation count or guaranteed
gain is required. Record these choices in existing experiments; see the residual
exploration section of [type-and-creative.md](type-and-creative.md). Coverage gates
apply to the retained delivery, not every discarded sketch. Aesthetic conventions
are challengeable; do not automatically normalize a successful departure.

## Attribute before patching

| Diagnosis | Target | Evidence needed |
|---|---|---|
| extraction | tool | Observation/method is wrong; explain generalization and run an unaffected fixture |
| rule | product_skill | Source read correctly, but rule conditions or flexibility mislead the new task; check reference and task |
| execution | design_output | Existing guidance can support the result, but implementation misapplied it; preserve working behavior |
| coverage | scope | Evidence does not support the claim; narrow it or obtain authorized evidence |

An intentional convention departure is not a failure merely for differing. Real
content, meaning or task failures remain failures. A one-off success may be a
valuable case, not a universal rule or proof of historical novelty. Keep the
smallest responsible change. Propose a tool correction if the tool is unavailable;
do not claim it was applied. Task permission does not imply global installation
or remote publication of updated skills.

## Journal and helper

```bash
python3 "$SKILL_ROOT/scripts/loop_tools.py" init profile.json --out review.json
python3 "$SKILL_ROOT/scripts/loop_tools.py" validate review.json --profile profile.json
```

Generated skills use `references/profile.json`. Fill concrete criteria before
checking. `init` is an empty record, not a review. Required fields:

- `version=2`, `scene`, `profile_sha256`: canonical profile binding.
- `review_scope`, `review_plan`, `revisions`, `delivery_revision`: concrete coverage
  and current artifact binding; see review-closure.md before attempting finish.
- `budget`: `mode=adaptive` with null caps, or explicit nonnegative integer caps
  (`max_total_repairs`, `max_repairs_per_loop`). Legacy omitted mode means capped.
- `benchmarks`: id, loop, dimension, criterion, references. One per scene dimension.
- `evidence`: id, locator, observed boolean, notes. Actual file/render/trace plus
  position, state or width; observation is not a machine truth certificate.
- `rounds`: chronological id, loop, checks, optional repair. Checks: dimension,
  status=passed|failed|skipped|not_applicable, evidence_ids, notes. Required checks
  cannot be disabled; skipped/missing stays incomplete. Pass/fail needs inspected
  evidence. A failed check has finding id, diagnosis, target, summary, severity.
- `repair`: addresses earlier finding IDs in that layer, target, change,
  evidence_ids, regression_dimensions, effect=improved|unchanged|unknown. Regression
  dimensions are rechecked/passed in that round. Tool repairs also need
  generalization and regression_cases pointing to unaffected fixtures/results.
- `experiments`: optional id, hypothesis, departure, preserved_relations, baseline,
  candidate, evidence_ids, decision=keep|revert|revise|unresolved, reason. Actual
  comparisons need observed evidence; revise/unresolved keeps overall state draft.
  A kept choice still needs applicable design checks; the experiment is not a pass.
- `transfer_task` for feedback: id, is_new=true, input, artifact,
  differs_from_source, evaluator=author|independent, source_access array.

Use a genuinely different content/task demand, not only a renamed title. Declare
exact reference access. Author runs are useful; independent testing needs a
separate evaluator without the intended answer. The helper cannot certify this.

If profile rules change, keep rounds and consumed counters, record before/after
hashes in repair.change, recheck affected dimensions and update the fingerprint.
Use `loop_tools.py fingerprint profile.json`. Do not rebind prior passes without
rechecking. If the user changes the brief, link a new journal and retain relevant
provenance. No arbitrary evidence locator is automatically inspected by the helper.

## Packaging and ordinary use

Draft packaging is permitted before transfer, so the outer loop can exercise the
skill. `profile_tools.py package profile.json --review review.json ...` attaches
its journal. All loops accepted with no pending experiments, plus complete v2 whole-deliverable
coverage and verified artifact hashes, permits reviewed_for_recorded_scope; known profile failures retain draft status. An author
run is not independent certification. Skipped source-profile checks do not
silently become passed when a journal is attached.

For ordinary use, run the design loop; trigger feedback for reuse tests or an
actual rule/tool question. Do not re-extract the whole reference for every edit.
Deliver the artifact, comparisons/selected choice, check evidence and remaining
limits. Human/agent inspection decides meaning and aesthetics; scripts validate
records and references only.


## Coverage closure before claiming completion

Use [review-closure.md](review-closure.md) to declare concrete subjects, contexts,
whole/detail/relation checks and per-target observations. Bind both source profile
and actual design/output revisions. Captured-only images and old revision evidence
cannot certify the final candidate. New logs start without assurance until planned.
Run `loop_tools.py finish review.json --profile profile.json --artifact-root task/`
before reporting reviewed completion; exit 2 means gaps remain. A local result
cannot certify the whole deliverable. v1 logs retain history as legacy_unverified.
This gate constrains coverage/reporting, preserving adaptive creative exploration.
Fill a current `exit_assessment` using `exit-template` before finish; a structurally
valid journal or complete coverage without those judgments remains unverified.

When packaging a complete v2 journal, pass `--artifact-root` to profile_tools.py
as well; omitting it preserves a draft rather than certifying file freshness.
