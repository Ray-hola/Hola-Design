# Incremental analysis fields

These fields enrich each scene's existing profile. PPT/UI/web domain records
remain distinct. Existing profiles may omit them; omission is a coverage warning,
not permission to invent facts. Read [distill-method.md](distill-method.md) first.

## Product interpretation: intent

An optional array of `{id, dimension, value, status, evidence_ids}`. Dimensions:
`theme`, `audience`, `function`, `purpose`, `use_context`, `success_criteria`.
`value` is nonempty text, or null for unknown. Use one record per dimension.
The source reference's intent and the new task's brief are different inputs.

Source-derived statements need evidence; observed interpretations may cite only
observed evidence. Author purpose unsupported by an explicit source stays inferred.
Expected outcomes do not prove measured conversion or usability. Proposed success
criteria should be clearly task-specific, not retrospectively attributed to source.
No script can decide whether a semantic interpretation is actually true.

## Visual rules: representation

The existing id/status/evidence_ids/role/property/value remain usable. When using
`representation`, also provide `dimension`, `role` and `scope`; scope names the
inspected surface/conditions rather than implying a brand-wide rule.

| representation | value | Additional fields |
|---|---|---|
| absolute | finite number or nonempty encoded text | unit, e.g. css-px, pt, sRGB-hex |
| ratio | finite nonnegative number | unit=unitless, relative_to; optional basis |
| range | object with finite min <= max | unit; if unitless, relative_to; state range meaning in scope |
| categorical | nonempty text | writing direction/context when interpreting alignment |
| qualitative | nonempty text | concrete locatable relationship; estimated precision where appropriate |

Optional `precision`: measured / estimated. `status` is the evidence status;
precision records a different fact. Screenshot estimates must stay estimates.
`scope`, `conditions`, `exceptions`, `unknowns` can describe where the relation
holds and which content changes have/have not been inspected.

Optional ratio `basis` is:

```json
{
  "numerator": {"value": 48, "unit": "css-px"},
  "denominator": {"value": 18, "unit": "css-px"}
}
```

The validator checks same units, finite nonnegative numerator, positive denominator
and arithmetic agreement (relative tolerance 0.001, absolute tolerance 0.0001).
This is not evidence that the values belong to the right roles or were really
measured. Unknown rules use null value and need not fill representation metadata.
Do not mix source px, screenshot pixels and PPT pt to construct a ratio.

Example rule — only valid with matching actual evidence records:

```json
{
  "id": "hero-body-scale-wide",
  "dimension": "typography",
  "property": "font-size",
  "role": "hero title relative to body",
  "representation": "ratio",
  "value": 2.6667,
  "unit": "unitless",
  "relative_to": "body text size",
  "basis": {
    "numerator": {"value": 48, "unit": "css-px"},
    "denominator": {"value": 18, "unit": "css-px"}
  },
  "scope": "reference hero at inspected 1440px viewport only",
  "precision": "measured",
  "status": "observed",
  "evidence_ids": ["actual-wide-capture"]
}
```

An absolute value, relative relation and rationale may have different evidence
statuses. Split them into separate records/decisions rather than giving the
whole explanation the strongest available status.


## Typefaces and unique design cases

`typefaces` is an optional array of id/status/evidence_ids plus family, roles
(nonempty string array), scope and identification: verified_metadata,
verified_render, declared, visual_candidate or unknown. Unknown identity has null
family. Named visual guesses remain inferred/proposed. Verification needs observed
font-metadata or rendered-font evidence respectively, not only CSS or a screenshot.
Keep glyph features, pairings, actual sample, languages/fallback, source/asset and
license notes where known. Generic directory recommendations are proposals.

`design_cases` keeps valuable one-off choices. Each has id/status/evidence_ids,
intent, departure, preserved_relations, effect_hypothesis, scope, next_test and
concept_state=candidate|task_supported|cross_context_supported. One instance is
sufficient for a candidate case; no repetition count is required. Hypothesized
intent/effect stay inferred. Record case-specific tradeoffs and alternative
explanations, and do not claim global novelty from local evidence.

Both collections are copied as reference JSON into generated skills and searchable
alongside their learned profile. See [type-and-creative.md](type-and-creative.md).
