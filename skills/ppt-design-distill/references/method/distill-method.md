# Distillation: intent -> structure -> relationships -> rules and cases -> transfer

Read when beginning reference analysis or investigating a failed transfer. This
is the project's synthesis of source measurement, semantic roles, conditional
patterns and tradeoff analysis; it is not an upstream certification of the method.

The core output is design judgment: explain intention, relationships, interaction
causality and the conditions under which they work. Case collections, tokens and
kits support that reasoning; accumulating them is not the objective. When learning
from interactions or award winners, read [design-reasoning.md](design-reasoning.md)
and retain mechanisms, costs and counterexamples before proposing a reusable form.

## 1. Understand intent

Describe the reference and the new task separately. Identify theme, audience,
function, purpose, use context and success criteria. A useful sentence is:
**For whom, in which situation, about which object, helping with which task,
toward which outcome?** A blue palette is not a product theme; a table is not a
user task. Do not invent personas, author motives or achieved outcomes from appearance.

Mark answers observed / declared / inferred / unknown / proposed. Confirm behavior
by executing it; an inferred purpose is not measured effectiveness. Preserve a
visual-only or otherwise narrow scope when that is what the user requested.
Record supported interpretations in `intent`; retain domain background in `context`.
Never overwrite source intent with the new brief.

### Books and theory

Track actual chapters, body text, examples, captions and reading coverage. Read
text and illustrations separately; extraction is not reading. Distinguish source
claims, factual summaries, project interpretations and current-task evidence.
Convert concepts into conditional application questions, boundaries and tests.
Physical analogies, historical parameters and unreviewed studies are not screen
defaults. Evaluate reading coverage, toolkit behavior and design quality separately.
See [the principle questions](design-principles.md); do not run all of them per task.

### Choose expression before composing

Derive a testable direction from theme, audience and purpose. Make labels such as
minimal, editorial or experimental concrete: focal point, reading rhythm, density,
text roles, type character, boundaries, decorative purpose and deliberate omissions.
Do not assemble every component first and add a style label afterward.

Retain text for information, action, tone or an observable formal relationship.
Test removing unsupported microcopy, numbers, coordinates and decorative labels.
Minimal does not mean a word-count limit: necessary identity, time, place and
conditions stay. A useful surprise can revise the direction; consistency alone
cannot justify meaningless filler or suppress innovation.

## 2. Explain structure

Locate samples at whole -> page/screen/slide -> section/component -> element.
For each level identify its role, grouping, first attention and next step.

| Scene | Structures and relationships |
|---|---|
| PPT | Claims, evidence, comparisons, steps, page types, transitions across slides |
| UI | Objects, tasks, screens, components, states, transitions, errors, permissions |
| Web | Page purpose, section roles, media/content prerequisites, reading and action order |

Name a section's purpose before its geometry: comparing three actual options
explains more than "three cards." One card layout does not require enclosing all
content in cards.

## 3. Observe visual relationships

Bind each observation to a role, location, size and state. Different roles with the
same measured size need not share a token. Do not invent absent motion or states.

| Dimension | Inspect and retain |
|---|---|
| Type | Glyph character, family, weight/axes, size, leading, tracking, line length, breaks; display/body/annotation/numeral roles and relative scale |
| Color | Background/surface/text/accent/state roles, foreground pairs, opacity, themes and chart meanings; area alone does not establish identity |
| Spacing | Margins, padding, within/between-group gaps, section and cross-page rhythm; preserve exceptions to a grid |
| Container alignment | Canvas position, grid, shared edges, width, nesting and column relationships |
| Text alignment | Start/end/left/center/right/justify, direction, baseline, numeral/unit comparison and optical alignment |
| Composition | Focus, reading order, balance, density, negative space, text/media proportions and response to changed content |
| Boundaries | Window shell, controls, information groups, image crops and artwork edges separately; framing, corners, shadow and layering need role-specific reasons |
| Media | Function, subject, crop, focal point, scale, stroke and text/media relationship; a particular photograph is not automatically mandatory |
| Information encoding | Correct data, units, axes, order, groups, emphasis and redundant cues |
| Motion | Trigger, before/after states, purpose, timing, easing, interruption and reduced motion; static images do not prove behavior |

Text may be a spatial form: study orientation, rotation, paths, anchors, overlap,
layering, cropping and scale, not only rectangular text blocks. Typography includes
art lettering and editable graphic text, without presuming an installed font.

Use `absolute`, `ratio`, `range`, `categorical` or `qualitative` representations.
Retain source values, units, relative objects, precision and basis. Separate sample
ranges from allowed design or stress-test ranges. Do not mix screenshot pixels,
CSS pixels and PPT points, or claim CSS family declarations prove rendered glyph fonts.
A centered container can contain left-aligned text; store these separately.

Treat boundaries as composition. First ask whether a frame is needed. A rounded
editor shell does not prescribe the poster's edge; neither all-rounded nor all-square
rules follow from scene names.

## 4. Derive conditional rules and preserve unique cases

Sample meaningful variations: representative types, repeated roles, changed
content and exceptions. Responsive or behavioral claims need the same subject
at relevant sizes/states. Sparse samples narrow a claim; no universal sample quota.

Check repetition, role consistency, counterexamples/conditions and tradeoffs.
Repetition supports broader scope; one exceptional choice may still be valuable.
Store it as `design_cases`, with intent, departure, relationships, cost, evidence,
scope and next test. Do not call novelty a defect or claim historical originality.
See [typography and creativity](type-and-creative.md).

An executable rule states: **Under these conditions, for this purpose, use this
structure/relationship; preserve these invariants, allow these changes, and switch
to this alternative at this boundary.** Include locator, evidence status, rationale,
unknowns and a new-content check. A two-option extension from a three-option source
is proposed until tested. Do not invent universal proportions, maximum counts,
prohibitions or motives; vague "premium" labels cannot replace actual relationships.

## 5. Test transfer

Render promising type/composition alternatives when expression warrants them.
Compare intent, relationships and overall effect; keep, revert or revise with reasons.
Change a real stress condition: longer title, different counts/units, error state,
or presentation versus self-reading. Preserve applicable relationships while
allowing justified structure changes rather than defaulting to generic catalog style.

Inspect intent, content/task structure, visual relationships and actual file/render/
behavior separately. Use scene-appropriate checks. Attribute failures to method,
rule, implementation or missing coverage through [the LOOP protocol](../loop/loop-protocol.md).
Valid JSON and similar replication are partial evidence, not successful transfer.

Record observations in `distillation.csv` and supported interpretations in the profile.
[The analysis contract](../records/analysis-contract.md) documents incremental fields. Missing
evidence stays unknown; older/narrow profiles may validate with coverage warnings.
Generated skills carry intent, domain patterns, visual roles, conditions, decisions,
references and unknowns. Catalog suggestions and neutral starters remain proposed.
