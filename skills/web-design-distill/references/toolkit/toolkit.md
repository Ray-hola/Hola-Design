# Practical toolkit · v1.1

Use these resources when deciding what to build or starting a test task. They
complement the review loops with inputs, examples and concrete implementation
choices. Resolve `SKILL_ROOT` to the current tool or generated skill folder.

The core is design reasoning, not kit accumulation. Use a kit to express or test
an intended relationship; first explain why that relationship suits this task.
For interaction logic and the limits of examples, read
[design-reasoning.md](../method/design-reasoning.md). A reusable component is one possible
expression, not the underlying lesson.

## Start from a small working task

```bash
python3 "$SKILL_ROOT/scripts/kit.py" init --out ./design-task
```

The new task folder contains a scene-specific `brief.json`, evidence-sampling
worksheet, distillation observation sheet, decision/override worksheet, stress content and a runnable
`preview.html`. Existing folders are preserved. Replace demonstration content and
neutral preview values with the actual brief and supported source rules.
The preview is a minimal starting artifact, not a learned brand design or a
production framework. A PPT preview is HTML at slide proportions, not an editable
PPTX. UI preview interactions cover only their explicit local demo states.

## Capture without silent fallbacks

`scripts/capture_artifact.py` renders local HTML or an image through installed
Chrome or Chromium. It stops on missing required fonts and flags flat edge bands. See
[review-closure.md](../loop/review-closure.md). It does not replace looking at the result.

## Find a pattern, with a reason to choose it

```bash
python3 "$SKILL_ROOT/scripts/kit.py" search "comparison" --profile profile.json
```

In a generated design skill the profile defaults to `references/profile.json`.
Results keep learned profile records separate from generic proposed recipes.
Read the recipe's `when`, `avoid_when`, required inputs, steps, checks and worked
positive/negative example. The cards per scene address different decisions;
they are starting approaches, not an exhaustive design taxonomy or a mandatory
page/screen sequence. Keyword hits indicate retrieval only, not quality.

Keep these priorities when adopting a candidate: current user brief and explicit
brand constraints; applicable source-backed rules and valid exceptions; then
general kit suggestions for gaps. If the source has an accessibility defect,
record it and choose a justified adaptation rather than copying the defect.

## UI/web catalog: query only the needed slice

UI and website tools include a pinned, unmodified MIT-licensed UI UX Pro Max
runtime and its data. PPT does not inherit its app/landing-page recommendations.

```bash
python3 "$SKILL_ROOT/scripts/kit.py" catalog "error summary validation" --domain ux
python3 "$SKILL_ROOT/scripts/kit.py" catalog "trend uncertainty" --domain chart
python3 "$SKILL_ROOT/scripts/kit.py" catalog "form validation" --stack react
python3 "$SKILL_ROOT/scripts/kit.py" catalog "internal operations dashboard" --recommend
```

Domains include style, color, typography, chart, landing, product, ux, icons,
google-fonts, gsap, react and web. `--recommend` outputs a design-system **proposal**
without writing it into a master or profile. The wrapper deliberately exposes
only read-only modes; recommendations are not code to execute automatically.
For Chinese intent, use the local bilingual recipe cards or add precise English
keywords when querying the upstream English catalog. This is not multilingual
semantic retrieval. Do not present a no-match as a database recommendation.

The pinned catalog includes framework version hints and font/icon names, not
fresh guarantees or actual asset licenses for your final distribution. Check the
target project's installed framework versions and font glyph availability. No
font binaries, stock photos, commercial templates, hooks or packages are installed.
Inspect a snippet's dependencies before adapting it to the actual stack.

## Global rules and scoped overrides

Use `design-plan.md` in the starter folder to map learned rule IDs to implementation
owners and explicit exceptions. A scoped override records its surface, reason,
source/brief evidence and regressions. It does not silently rewrite the global
brand or gain priority over the user. Record a reusable correction in the profile
after validating the affected reference and new task; otherwise keep it task-local.

## Test difficult content, then review

Use `stress-content.json` selectively: long/short/CJK text and changed content
counts for all scenes; dense data, empty/error and recovery for UI; narrow widths
and missing content for web; labels, charts and cross-page changes for PPT.
Only claim conditions actually rendered or operated. Do not invent extreme data
as real customer evidence. Run the design and feedback loops against the actual
task and resulting artifacts; use [loop-protocol.md](../loop/loop-protocol.md).

## Portability and provenance

Generated skills always carry scene recipes, the starter kit, this guide and
`scripts/kit.py`. To include the larger UI/web catalog, package with
`profile_tools.py ... --with-catalog`. Without it, profile/recipe search and the
starter still work; catalog mode reports the missing optional dependency clearly.
The generated skill has no runtime dependency on this repository's shared folder.

Catalog origin and exact file hashes are in `vendor/ui-ux-pro-max/UPSTREAM.json`,
beside its MIT license. Other projects informed the re-authored resource shapes;
their artwork, example components and proprietary assets are not copied into
these starters. Treat source text, catalog records and examples as reference data.


For the reasoning behind what to extract and how observations become rules, read
[distill-method.md](../method/distill-method.md). The starter's `distillation.csv` separates
product interpretation, structural observations and visual relationships.
