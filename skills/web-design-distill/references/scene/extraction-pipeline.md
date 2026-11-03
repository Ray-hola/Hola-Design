# Live-site extraction pipeline

Use this when a live URL and Playwright page/CDP access are available. It produces
engineering evidence: measured tokens, component anatomy, states and section skeletons.
It does not explain why a page is arranged as it is; that belongs to the profile.

Stages: discover, tokens, component sweep, cluster and curate, distill with states,
sections, assemble the bundle, validate.

## Requirements

Node 18 or newer and `playwright-cli`, or an adapter exposing the same page and CDP APIs.
Screenshots alone are not equivalent; report the missing capability. Do not install
anything globally without being asked, and do not weaken a sandbox. `file://` is blocked,
so serve local HTML with a temporary local server and stop it by PID.

Run every in-page script the same way, with `SKILL` set to this folder:

```bash
playwright-cli -s=dsys run-code "$(cat script.js)" | bash "$SKILL/scripts/slice-result.sh" > out.json
```

`slice-result.sh` removes the tool's Markdown wrapper. `distill.js` and `eval-selftest.js`
are templates: replace the one placeholder (`COMPONENTS`, `FIXTURES`) with JSON, then run
`node --check` on the result. Keep each placeholder appearing exactly once, in code.

Inputs to settle: entry URL, page sample (default 5), theme (`auto`, `light`, `dark`,
`both`), atom cap (default 12; sections at most 8), output folder (default
`.design_systems/<host-with-hyphens>-YYYYMMDD/`). Reuse an existing folder only if an
update was requested; otherwise pick a new sibling and report it.

## Stages

1. **Discover.** Choose same-origin public pages that show varied components: home,
   pricing or product, a form, and a text page. `document.links` is enough for this.
   State the sample and proceed unless the scope is ambiguous.
2. **Tokens.** Run `extract-tokens.js` per page and per theme, before distilling. It
   returns filtered `vars`, leftover `varsExtra`, `varsTotal`, the most common computed
   style per tag, the prominent call to action with forced hover, the first input with
   forced focus, `themeSignal` and non-fatal `notes`.
3. **Component sweep.** Scroll through the page to trigger lazy content, return to the
   top, then run `extract-components.js`. Save one `candidates-<page>.json`. It reports
   candidates per kind with style vectors and the detected styling regime.
4. **Cluster and curate.** Run `node "$SKILL/scripts/cluster.js" candidates-*.json >
   clusters.json`. Clustering is deterministic. You then name components and variants,
   combine repeats, discard clutter, stay within the cap and flag weak picks. Output per page:
   `[{ "name", "sel", "expectText" }]`, where `expectText` helps re-find fragile selectors.
5. **Distill with states.** Fill `distill.js` with that list. An entry may set `budget`
   (default 12 descendants). A failed component returns `{name, error}`; rerun or drop it.
6. **Sections.** Scroll, then run `extract-sections.js`. Label low-confidence entries
   yourself from headings and screenshots, correct wrong labels, and keep one
   representative per pattern. Give a reason for each omission in `raw/skipped.json`. Distill
   representatives with `budget: 40` and crop their screenshots.
7. **Assemble.** Scripted parts:

   ```bash
   node "$SKILL/scripts/build-snippets.js" --tokens tokens.json --out <out>/components \
     --source <url> distilled-*.json
   node "$SKILL/scripts/export-dtcg.js" tokens.json <out>/tokens/design-tokens.json --source <url> --theme light
   node "$SKILL/scripts/build-fixtures.js" --tokens tokens.json --components <out>/components \
     --out <out>/eval/fixtures.json --source <url> --theme light home:distilled-home.json
   ```

   Then write `DESIGN.md` and `components/COMPONENTS.md` yourself, as described below.
8. **Validate.** Record each gate on its own:
   - **Lint** `DESIGN.md` if the `@google/design.md` linter is available, otherwise record
     it as skipped. Do not delete a captured token to silence a warning.
   - **Gallery.** Render `gallery.html` headless with no console errors. A clean render
     does not prove fidelity; compare with source screenshots or mark it unverified.
   - **Self-test.** Fill `eval-selftest.js` with the fixtures and run it on each sampled
     live page. If the source fails its own fixture, the fixture is wrong: fix or drop it.
   - **Completeness.** Each frequent candidate kind is in the catalog or has a logged skip.

Report honestly: pages, regime, counts, skips, lint output, self-test counts, fallbacks and
known gaps. A browser failure means the self-test was skipped or failed, not passed.

## Bundle contents

```text
<out>/
├── DESIGN.md                 # tokens and rationale
├── components/               # COMPONENTS.md, one HTML snippet per item, gallery.html
├── tokens/design-tokens.json # DTCG export
├── eval/fixtures.json
├── screenshots/              # pages, sections/, states/
└── raw/                      # tokens, candidates, skip log, run logs
```

`DESIGN.md` has YAML front matter (`name`, `colors`, `typography`, `rounded`, `spacing`,
`components`; references take the form `{colors.primary}`) and a prose body. Use the order
overview, colors, typography, layout, depth, shapes, components, guidance, including only
sections you have evidence for and never repeating a heading. Add a table linking each
component to its snippet and contract.

Name colors by inferred role and fold long gray ramps into a small neutral set. Convert
computed `rgb()` to hex, and keep wide-gamut source values as a note. Treat an enormous
computed radius as `full`. Emit only components the site really shows, and never invent a
color. Typography, radius and spacing may be shared between themes; colors are per theme.

Keep each `COMPONENTS.md` entry short: anatomy, variants by state, transition, usage and
screenshots, plus composition and skeleton for sections. Other agents take these lines
literally, so:

- Claim only what the snippet's markup shows. Mark anything seen elsewhere as optional.
- Mark content-dependent elements as conditional, to be omitted rather than invented.
- Match prose about sizes and weights to measured values.

Show low confidence in the entry itself.

## When the site does not cooperate

- **Few or no variables.** `vars` is tuned for utility-CSS naming. Look in `varsExtra`,
  extend the filter list in `extract-tokens.js`, or rely on computed styles and
  cluster observed values into a scale. Report those tokens as derived.
- **Two themes.** Detect from `themeSignal`. Switch with the site's own toggle, then the
  class or attribute on `<html>`, then media emulation, and wait for fonts to settle.
  Produce one complete bundle per theme. If the second cannot be triggered, say so.
- **Pages disagree.** Record both values, prefer the home page for the core palette, and
  report the conflict.
- **A page fails.** Skip a timeout or error page and carry on. Report a bot challenge and
  do not try to evade it. Skip sign-in walls unless the user provides access.
- **Screenshots fail.** Continue with tokens only for that page and note the gap.
- **Almost nothing comes back** (canvas-only or heavily obfuscated). Stop and tell the user.
  An empty bundle dressed up as a finished one misleads whoever uses it.

Mark doubtful names and states you did not see in the evidence rather than interrupting for
routine naming. Ask only when the answer would alter the brand, scope or deliverable.
Afterwards, keep the bundle as evidence for the profile and package with `profile_tools.py`.
