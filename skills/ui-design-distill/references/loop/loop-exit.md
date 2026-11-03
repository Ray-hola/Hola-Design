# LOOP exit protocol

Use for iterative distillation, design, writing, code and analysis. Exit semantics
are shared; quality criteria belong to the task. This protocol does not authorize
publishing, installing, sending or other external actions.

```text
::LOOP_EXIT{state:PASS|scope:<explicit scope>|revision:<final revision>|record:<review record>|basis:author_or_independent}
```

Use PASS only on actual exit, not repeatedly in progress reports. Other states:

| State | Meaning |
|---|---|
| PASS | The specified scope/revision has completed checks and supported quality judgment |
| HOLD | A known failure, unresolved candidate or worthwhile in-scope improvement remains |
| UNVERIFIED | Required evidence or coverage is missing, stale or insufficient |
| BLOCKED | A necessary input, permission or tool is unavailable; report the affected work |
| INTERRUPTED | The user stopped work or an explicit limit was reached; record unfinished work |

The tool calculates PASS/HOLD/UNVERIFIED. Blocked/interrupted claims need real
causes, not fatigue or number of attempts. Drafts can be shown with accurate status.
Absent markers do not imply approval. PASS is revocable and scoped; it is neither
user acceptance, independent certification nor proof of absolute perfection.

## Seven exit conditions

1. **Intent:** satisfy the original task, audience, purpose and boundaries, not just
   the aspects recently edited.
2. **Quality:** give positive reasons to retain the result. For design, inspect
   focus, reading path, type character/relationships, expression and identity; for
   code, actual behavior and maintenance; for analysis, evidence and inference.
   No-overflow, no-errors and complete fields cannot substitute.
3. **Coverage:** actually check whole, critical details, relationships and relevant
   contexts. Do not skip the most prominent identity-bearing subject. Local success
   cannot establish whole-deliverable or whole-skill success.
4. **Challenge:** test the strongest reason to reject the result, including the
   weakest subject; record whether it holds, the response and observed effect.
5. **Revision:** bind observations to the final artifact and current record; after
   edits recheck affected scope and the whole.
6. **Integrity:** declared objects, the ground, every display context and the
   exported file stay complete and intact. See "Integrity gate" below.
7. **Convergence:** resolve known failures, required unknowns, undecided candidates
   and worthwhile in-scope improvements. Explain the retained choice; rounds,
   tokens, patience or "better than before" are not stopping evidence.

Do not delete failing subjects, lower standards or narrow the original task to earn
PASS. Record actual user scope changes and unfinished original requirements.
Subjective judgment cannot be automated: compare promising type/composition choices
when expression is important, including intuitive/random residuals when useful.
No fixed round/candidate quota or numerical beauty score. Exit means supported
choice within declared comparisons, not proof that no better work is possible.

A retained tradeoff needs benefit, cost, scope and evidence. Missing required checks,
violations and untreated improvements cannot be renamed "style" or "residual."
New user objections reopen affected decisions without rewriting inspection history.

## Compact injection

```text
::GATE{loop_exit|default:UNVERIFIED}
  SCOPE: original task + declared subjects + relevant contexts
  REQUIRE: intent_supported AND quality_supported AND coverage_closed
           AND strongest_objection_resolved AND integrity_closed AND final_revision_verified
           AND no_known_worthwhile_work_open
  REVIEW: whole -> critical_details -> relationships -> whole_again
  IF failure_or_worthwhile_improvement => HOLD; PATCH_OR_CHANGE_DIRECTION; REENTER
  IF missing_or_stale_evidence => UNVERIFIED; VERIFY; REENTER
  IF user_stop_or_explicit_limit => INTERRUPTED; RECORD_UNFINISHED
  IF necessary_input_or_tool_unavailable => BLOCKED; RECORD_BLOCKER
  IF all_requirements_supported => PASS(scope, revision, review_record)
  INVALIDATE: relevant_edit OR changed_brief OR new_contradicting_evidence
```

This is an ordinary workflow instruction, not special priority syntax. Writing a
marker does not produce approval.

## Challenge the same question

Form judgments before recording states. **Never prefill pass values in generation
scripts or batch-fill approvals and invent reasons afterward.** Scripts may transport
actual judgments, references and hashes; unknown template values stay unanswered.

Make critical/disputed choices concrete in `review_plan.parts`; relation items need
at least two parts and a result criterion. For a split wordmark, compare glyph width,
face, density, color, position and negative space together; mechanical equal width
is not required. "Same font" or "intended space" is a hypothesis, not an observation.

`quality.plan_ids` selects the actual questions. Supporting evidence must cover the
same subjects, questions and contexts. Each `challenge.tests` entry supplies
plan_ids, reject_if, method, evidence_ids, observation and result:

- `confirmed`: rejection still holds -> HOLD; `unresolved`: insufficient evidence ->
  UNVERIFIED; `refuted`: actual observation contradicts the rejection condition.
- `direct` checks an observable fact/requirement. `comparison` is needed for disputed
  subjective relations, crucial expression or reopened questions requiring alternatives.
- Comparison `experiment_ids` refer to experiments bound by the same plan_ids and
  actual `variant_evidence.baseline` / `candidate`, in each relevant context. The
  candidate must be the retained version. An angle comparison does not prove width
  balance; mobile evidence does not establish desktop balance.

Same-question comparisons remain open until performed. Do not use an unrelated
candidate, intention or renamed tradeoff to dismiss them. The purpose is supported
expression, not forcing symmetry, centering or equal-width letters.

## Integrity gate

Integrity asks whether the delivered work is whole: no content is missing, no
background, line or graphic breaks by accident, masks, clips and overlaps do what
was intended, the whole still holds after local edits, and the export matches the
inspected source. Rendered work needs it: any `design` scope or whole-deliverable
claim. A source-only distillation review does not.

| Result | Meaning |
|---|---|
| PASS | The current revision, each declared object and each display context have inspected evidence, and every issue is closed |
| HOLD | A known integrity defect remains: a `defect` check, a `fails` treatment or a `differs` export |
| UNVERIFIED | A check is missing, evidence is insufficient, or evidence belongs to an older revision or source |

Crossing text, overlap, rotation, bleed and cropping are legitimate. The gate
never rejects a technique for what it is, and never accepts one because it is
called intentional. Record the intent, what must survive, what would falsify it,
and what you actually saw in each context.

Plan items use `loop=design`, `dimension=integrity`. After declaring the scope, run
`loop_tools.py integrity-plan review.json` to add unanswered items for each context,
then fill their criteria and parts. `exit-template` opens one `unknown` check row per
aspect and context. Fill `gates.integrity` with status, reason, evidence_ids and:

- `inventory`: id, role, subject, summary for each object that could go missing.
  Include one `role=ground` for the background/field, even when it is a plain or
  transparent surface. Every scope subject needs at least one object.
- `checks`: id, aspect, context, item_ids, plan_ids, evidence_ids, observation,
  result=closed|defect|unknown. Each context needs all four aspects covering every
  object: `content` (present and complete), `continuity` (no accidental break),
  `layering` (masks, clips and overlaps as intended), `whole` (the composition
  rechecked after edits, using a whole-level plan item). Continuity, layering and
  whole require visual inspection.
- `treatments`: optional id, kind, item_ids, intent, must_preserve, reject_if, and
  per-context `results` of context, plan_ids, evidence_ids, observation and
  result=holds|fails|unknown. Needed for crossing, overlap, rotation, cropping and
  anything hidden in one context. Repeating the intent is not an observation.
- `exports`: output, sources, method, plan_ids, evidence_ids, observation and
  result=matches|differs|unknown. Output and sources must be in the final revision.
  At least one cited evidence item must have been captured from the output itself.
  When source and delivery are the same file, name it in both fields.

Integrity evidence adds `rendered_from`: path to sha256 for each input of that
capture. All must match the final revision. The same capture bytes recorded for
different inputs count as an old screenshot. Editing a file invalidates evidence
until it is recaptured and the whole is rechecked.

`loop_exit.integrity` reports this gate separately. Earlier assessments have no
integrity record, so they stay UNVERIFIED and keep their history; earlier journals
stay readable, but their design loop remains incomplete. Records prove bindings,
not honesty: the tool cannot find an object nobody declared or a context nobody
listed, so choose the inventory and contexts from the actual delivery.

## Reopen executable approval

A new objection may prove unfounded, but requires review. Reopen all affected actual
journals before updating summaries:

```bash
python3 "$SKILL_ROOT/scripts/loop_tools.py" reopen review.json \
  --loop design --dimension typography --plan-ids logo-wide-type logo-narrow-type \
  --reason 'Width and optical weight of the two groups are disputed' \
  --source user --probe-method comparison
```

Use real plan ids; clarify their parts/criteria. Reopen records a coverage failure,
previous assessment and needed method in rounds/findings, and invalidates current
exit_assessment. Continue repair/impact/regression. New hashes or relabeled tradeoffs
cannot replace required comparisons. If the objection is refuted, explain the actual
finding; successful work need not be changed merely to show activity.

Old finish output records history. Run finish again for the current delivery and
point summaries to that result; never reuse revoked markers as current conclusions.

## Use the journal tools

```bash
python3 "$SKILL_ROOT/scripts/loop_tools.py" exit-template review.json --out exit-draft.json
```

Fill the draft with actual judgments and place it in `exit_assessment`:

- `revision_id` and `review_sha256` bind artifact and journal excluding the assessment.
  Reassess after changes; refreshing a hash alone cannot preserve old judgments.
- `evaluator`: author / independent as actually performed; no mandatory subagent.
- `gates.intent / quality / challenge / integrity / convergence`: status
  pass|fail|unknown, reason and evidence_ids tied to actual observations.
- `quality.weakest_subject`: declared subject with detail/relation evidence.
- `quality.plan_ids`: concrete questions including a relation item with actual parts.
- `challenge.objection / response`: strongest rejection reason and actual handling.
- `challenge.tests`: same-question tests covering every quality.plan_id; comparisons
  also require experiment_ids.
- `integrity.inventory / checks / treatments / exports`: see "Integrity gate".
- `remaining`: summary, kind and disposition per entry. Only a retained tradeoff
  with reason and current evidence_ids can coexist with PASS. Other unfinished work
  keeps HOLD. An empty array means rechecked and clear, not skipped review.

```bash
python3 "$SKILL_ROOT/scripts/loop_tools.py" finish review.json \
  --profile profile.json --artifact-root ./design-task
```

Use its marker only when exit code is 0 and loop_exit.state is PASS. Exit 2 means
inspect reasons, coverage_review.gaps and failures. Structural validate code 0 is
not exit approval. Local PASS remains local; a reviewed whole skill needs three
accepted loops. Legacy records do not acquire new approval automatically.

`record_gate=ready` means the record supports assessment; `quality_basis` identifies
human/agent judgment. Different hashes do not prove a meaningful comparison.
The tool checks bindings, evidence files and reopened states, not honesty, sufficient
conditions or beauty. Never describe mechanical validation as machine-certified quality.
