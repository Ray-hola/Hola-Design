# Typography, unique cases and creative exploration

## Treat type as expressive material

Choose an expression direction and decide which text belongs before selecting a
font; see [the method](distill-method.md#choose-expression-before-composing).
A better font does not give meaningless filler a role. Inspect microcopy, numbering,
labels and annotations for information, tone or a concrete formal relationship.

Study glyph character and typography together. Record verified family, weight/axes,
source and specimens; uncertain identities stay candidates. Distinguish declared CSS,
computed properties, catalog suggestions and actual rendered glyph fonts. Font
metadata/native file records or browser rendered-font reports can support identity;
installation alone cannot prove use.

Inspect terminals, contrast, width, counters, x-height/face size and curves; display,
body, annotation, numeral and identity roles; pairing, tracking, deliberate breaks,
leading, scale, optical alignment and relationships to images. Art lettering may
be custom outlines, ligatures, handwriting, crops, overprints, texture or graphic
text. Preserve editable/alternative assets without inventing a font family.

Try real titles, CJK text, numbers and long/short content. Reading and frequent
operations need their own acceptance criteria; expressive text can explore more.
If display treatment deliberately reduces direct reading, identify where essential
meaning remains available. No mandatory serif, art lettering or single-family rule.
Default system fonts need task reasons, not merely presence in the template.
Choose CJK short copy, signatures and notes deliberately too; a Latin display face
does not justify accidental CJK fallback. Verify coverage, loading, pairing and
PPT embedding/substitution in the actual environment.

## Compose text in space

Text can serve reading, navigation, image and composition roles. Inspect horizontal,
vertical, diagonal and path text, rotation, scale jumps, scattering, anchors, overlap,
layering, cropping and scroll changes. Bind transformations and reading paths to
canvas/viewport relationships when measurable; fixed-window coordinates alone do
not describe a system. Check semantic order separately from visual order.

Evaluate how each word changes weight, tension, grouping and overall meaning.
Alignment, baselines and rectangles may be broken deliberately. Relations are a
lens that new cases can revise, not fixed style laws. Do not score creativity by
rotation count, asymmetry or animation intensity. Compare whole compositions at
relevant widths, with glyphs and reading/action paths visible. DOM completeness
cannot substitute for checking the displayed expression. A poster-like hero and
continuous reading area may use different organizations.

## Inspect boundaries by role

Distinguish editor/browser shells, controls, content groups, image masks and artwork
edges. View the artwork outside its presentation shell: has it accidentally become
a product card? Compare useful unframed, hard, curved or mixed edges by their effect
on weight, extension, layers and reading. Do not flatten roles with global corner
rules. Neither posters nor UI prescribe one universal contour.

## Collect typefaces from supplied references

Use `typefaces` for family/candidates, roles, features, pairing, composition,
specimens, scope and evidence. `type-study.json` supplies blank questions.
A wordmark does not establish possession of a font binary.

```bash
python3 "$SKILL_ROOT/scripts/collect_font.py" source.ttf \
  --source "reference deck, slide 3" --family "Family label" \
  --role "display title" --out ./font-library/sample
```

Default behavior indexes source, hash and declarations without copying or installing.
Use `--rights allowed --license-file LICENSE.txt` only with actual permission to
redistribute; retain the license. The helper checks container signatures, not legal
rights or family identity. Unknown/restricted assets can remain research records.
Validate actual rendering, glyph coverage and fallback separately.

## Retain rules and singular choices

Store valuable one-off `design_cases`: intent, departure, preserved/reorganized
relationships, cost, evidence, scope and next experiment. No repetition threshold.
A candidate concept is neither proof of historical novelty nor universal superiority.

Consider hierarchy/contrast, connection/distinction, density/rhythm, balance/tension,
whole/variation and form/intent. Asymmetry or overlap can establish a new useful
relationship; do not automatically repair it back to the old rule. Missing content,
wrong meaning and failed tasks still require correction.

## Explore and compare actual candidates

1. Identify a promising expressive question or useful intuitive/random residual.
2. Save a real baseline and make the candidate; retain revision-specific evidence.
3. View whole, affected details and neighbors under the actual content/contexts.
4. Compare intended benefit, observed result, unexpected value and tradeoff.
5. Keep / revert / revise / unresolved; recheck retained changes in the final version.
6. Feed promising discoveries into candidate cases or revise the hypothesis.

Do not require intuition to prove its value before trying it. A useful residual can
change the direction; neither novelty nor rule compliance earns automatic approval.
No quota requires improvement every round or a retained residual in every design.
Discarded sketches need proportionate inspection; the delivered version needs closed
coverage and regression. Do not manufacture failures to justify exploration.

Use existing `experiments`: id, hypothesis, departure, preserved_relations, baseline,
candidate, evidence_ids, decision and reason. Separate intent from observation and
surprise; retained candidates bind `candidate_revision` to the final artifact.
Do not retrofit an unexpected benefit as an original prediction.

New journals use adaptive exploration with no default four-total/two-per-loop cap.
Honor explicit user limits and old journals' numeric budgets. Two unchanged attempts
suggest a new direction, not termination of the entire task. Converge on supported
choices after required checks; unresolved experiments keep draft status. Neither
elapsed rounds nor claims that no conceivable improvement exists establish exit.

For disputed text groups inspect role, phrasing, breaks, leading, angle, anchor,
negative space and neighbors. Compare actual surrounding compositions and relevant
intermediate widths. Technical checks, actual viewing and aesthetic comparison are
different evidence. The web spatial starter is one optional candidate, not a style
prescription. Review software cannot decide beauty.

Font collection defaults to an English specimen. Supply `--sample-text` with the
actual copy and writing system from the brief; language of instructions does not
restrict the language of a designed artifact. Inspect its rendered glyphs rather
than treating the default specimen as coverage evidence.
