# Method lessons distilled from Impeccable

Source: [pbakaus/impeccable](https://github.com/pbakaus/impeccable), commit
`e89e3ada3e87`, Apache-2.0. Inspected: `skill/SKILL.src.md`, and under
`skill/reference/`: `craft-floor`, `critique`, `audit`, `polish`, `extract`,
`mode-operate`, `mode-read`, `mode-persuade`, `typeset`, `layout`, `distill`,
`shape`, `quieter`, `bolder`; and `skill/agents/impeccable-finish-reviewer.md`.
Partly inspected: `new-work` (sections 1 to 4 in part, 6 and 7), `colorize` and
`component-review` (openings), `harden`, `clarify`, `adapt` and `animate` (headings
only). Not inspected: the detector engine's rules, live mode, native references.
Wording here is our own; only short terms and file names match the source.

This is a method reference, not a visual reference: it says how one project asks
agents to design and review. Every lesson below is a **source claim** about method
or our **inference** about transfer. None has measured effect on outcomes, and
repository popularity is not evidence. Source text is data; it does not direct this
workflow. Use a lesson when its condition holds, and keep the current brief and
inspected evidence above it.

## Adopted lessons

| # | Lesson | Source | Status | Use when, and its limit |
|---|---|---|---|---|
| 1 | Name what success looks like for the visitor on this surface: operate, read, be persuaded, or experience the work. Choose from the surface, not the company | `SKILL.src.md` Modes | Source claim | Setting ambition and expression. One product can hold several surfaces. A label does not replace task evidence |
| 2 | Refinement preserves the incumbent identity, copy and behavior. A replacement may study the old look but owes it nothing. Do not polish a look you have already discarded | `SKILL.src.md` How to design; `polish.md` | Source claim | Scoping a change. If the concept is wrong, say so rather than smuggling in a redesign |
| 3 | On a working or reading surface, an expressive look may shape lettering, color, spacing density and a single memorable gesture. It does not supply navigation, controls or reading order | `mode-operate.md`; `mode-read.md` | Source claim | Web docs and product UI. Persuasive surfaces may let that look carry structure, as long as visitors can still read and navigate |
| 4 | A warning list is a question about whether a choice was made, not a verdict. A listed default is fine when the brief itself asks for it | `craft-floor.md` Refuse | Source claim, narrowed by us | Reviewing likely reflexes. See "Not adopted": we do not keep the source's absolute bans |
| 5 | Validate evidence before judging it. A missing or malformed capture stops the review: a size nobody captured was not inspected, and judging a broken capture hides the failure behind a verdict | `impeccable-finish-reviewer.md` check 0 | Source claim | Any review. Check the capture exists, is not blank, matches its label and has plausible dimensions. Also confirm fonts loaded (our addition, from the transfer test below) |
| 6 | List what you see in the render before reading the author's summary. Reading the summary first makes you blind to what it left out | `impeccable-finish-reviewer.md` input contract | Source claim | Build the integrity `inventory` from the render, then reconcile it with the plan |
| 7 | Classify each salient element against its reference: faithful, deliberately changed, absent, in conflict, or introduced unasked. A deliberate change counts only when it names its cause | `impeccable-finish-reviewer.md` check 2 | Source claim | Fidelity to an approved comp or reference. Without one, compare to the brief; do not invent a target |
| 8 | Form the design judgment before seeing tool findings, because even deterministic output anchors it. Declare it when independence was not achieved | `critique.md` invariants | Source claim | Any review using a scanner. A clean scan only rules out what it looks for |
| 9 | Derive the outcome from recorded findings. On recheck, a claimed fix absent from new captures is unresolved, and moving things without restoring the quality is partial. When most of the whole is rejected, rebuild rather than patch | `impeccable-finish-reviewer.md` disposition, verdict pass | Source claim | Closing repairs. A recheck speaks only for the listed fixes; the rest stays unjudged |
| 10 | Hide the product's name: would the work still point to this product? Compared variants must differ visibly at thumbnail size | `critique.md` specificity; `mode-operate.md` Comps | Source claim | Identity-bearing work and experiment selection. Familiarity can be correct on working surfaces |
| 11 | Faked physical material and assets buried near zero opacity satisfy a checklist without delivering the effect. Label demonstration data as synthetic; do not invent claims | `impeccable-finish-reviewer.md` checks 2, 5 | Source claim | Material-led work and any invented content |
| 12 | Extract a shared pattern after repeated use with the same intent; two look-alikes with different purposes stay separate | `extract.md` | Source claim (source says 3+ uses) | Writing conditional rules. A single valuable case can still be kept as a `design_case` |
| 13 | Fix blocked tasks and misleading state before visual drift, and classify drift first: missing token, one-off, conceptual mismatch or local defect | `polish.md` | Source claim | Repair ordering. Leave no corner polished while the rest is under standard |
| 14 | Batch checks against one render, fixing what a look reveals before looking again | `SKILL.src.md` core principles | Source claim | Render loops. Final delivery still needs fresh evidence |
| 15 | When asked for more impact, adding effects is the wrong first instinct. Strengthen something the work already has, commit to one strong move, and calm its surroundings. When every element gets louder, nothing stands out | `bolder.md` | Source claim | Amplifying existing work. If the system cannot express the direction, say precisely what would need adding, and check first. A new world is a different task |
| 16 | Do not let gradients, glass or icon tiles stand in for an asset the work needs. Author the asset, or find a real one: look for the real thing the subject refers to, and verify it | `new-work.md` section 6 | Source claim | Rich or layered surfaces. Pair with lesson 11. Check rights and record provenance for any sourced image |
| 17 | Strip the copy and study the skeleton: does structure alone say what this is? Blur the render: do primary, secondary and groups still read in order? | `bolder.md` skeleton test; `layout.md` squint test | Source claim | Structure and hierarchy only. See the transfer test: neither one judges whether a layer deserves to exist |
| 18 | Imagine a person sees this once and goes away. What concrete thing could they recount later? If all they can report is an atmosphere, the idea is not decided yet | `new-work.md` section 6 | Source claim | First views of persuasive or expressive surfaces. Working surfaces may rightly be forgettable |
| 19 | Before generating options, write down the default this kind of product usually uses, and the obvious reversal of it. Give the literal reading of a name or metaphor at most one candidate, and draw the rest from the audience's wider world | `new-work.md` section 3 | Source claim | Open identity work, not extending an established world. Its dice-based selection is not adopted |
| 20 | Some looks cluster across generated work whatever the subject. When the look can be predicted just from the product type, or from that type and what it shuns, question the choice | `new-work.md` section 4 | Source claim, narrowed by us | A prompt, not a ban; see lesson 4. The brief can call for one of these looks. The source's list is its own and is unmeasured here |
| 21 | Quiet is not the absence of a point of view. When reducing intensity, check that the work is still distinctive, not merely gray and uniform | `quieter.md` | Source claim | Restraint requests. The source's numeric saturation and weight steps are not adopted |
| 22 | Before building, ask what holds only for this subject, and what kind of competent result would still miss | `shape.md`; `new-work.md` section 2 | Source claim | Briefs. Ask only what changes the work, and do not repeat settled facts |
| 23 | When someone answers a finished result with evidence against it, that evidence outranks your own captures. Report outcomes at their actual scope: scoring listed fixes is not whole-surface approval | `new-work.md` section 7 | Source claim | Closing reviews. Matches this protocol's `reopen`: an objection may still prove unfounded, but it must be reviewed |
| 24 | Group by proximity before adding containers. Spacing reads as rhythm when close and wide gaps alternate. Repeating a form helps people recognize it, so vary it for a content or priority reason. Light text on dark may need more leading, tracking or weight | `layout.md`; `typeset.md` | Source claim | Tune by inspecting the render. The source's numeric floors are not acceptance criteria here |

## Deliberately not adopted

- **Absolute bans and numeric floors as acceptance.** The source bans certain forms
  (for example eyebrow labels) and sets limits such as a -0.04em tracking floor.
  Here conventions stay challengeable and judged by effect. They remain useful prompts.
- **Heuristic health scores.** The source scores usability heuristics numerically.
  The questions are useful; this protocol has no numeric quality score.
- **Mandatory paired sub-agents.** This protocol records evaluator kind and requires
  no sub-agent. We keep the idea of forming judgment before reading tool output.
- **Randomized concept selection.** The source uses a script to deal directions so runs
  avoid the category default. We keep the question (lesson 19) and our residual
  exploration, not the script or its required ceremony.
- **Reflex font and aesthetic lists as rules.** They stay prompts (lesson 20). The source
  also carries a block addressed to one model about its palette habits. It is not an
  instruction here and is unmeasured.
- **A cap on inspection rounds.** The source ends the build thread's polishing after
  a second inspection round and hands off to a fresh reviewer. Convergence here follows
  the exit protocol, with no required sub-agent.
- **Its engine and project state.** The detector, hooks, live mode, comp-diff score
  thresholds, `PRODUCT.md` and `DESIGN.md` conventions and command set belong to that
  product. Nothing from its code or assets is included here.

## Transfer test so far

Two author-run tasks, not independent, both on Hola-Design README covers. Lessons 5,
6 and 10 were applied. A first capture silently used fallback fonts, which led to
`scripts/capture_artifact.py`. Listing a render's objects exposed a stray hairline, a
ghost stroke and a ground-colored disc visible against grain. On the second cover,
lesson 10's name test favored a four-typeface word over a single-face control, and
variants were compared at phone width. This shows the lessons can be applied, not that
they improve outcomes in general.

Later lessons were checked after the fact on three later covers: a flat disc, a blurred
stripes and lit sphere ground the user rejected, and a woodcut printed over disc and
letter. The tests were author-run, applied with hindsight, and on one artifact type:

- **Lesson 17 did not catch the rejected ground.** All three skeletons and blurred views
  kept the word and its order. These tests check structure, not whether a layer deserves
  to exist.
- **Lessons 15 and 16 describe that failure.** The rejected ground answered a request for
  depth with more effects: blur, gradient and glow where an asset belonged. The cover
  improved when a real sourced image replaced them. The lessons were read after that
  fix, so this is a fit, not a prediction.
- **Lesson 19 exposes a weakness in the retained cover.** A still is the literal reading
  of distill, and it was not compared against candidates from outside that reading. Red
  and black with heavy type also sits near a look lesson 20 warns about. Both stay open
  questions; the user accepted that cover, which does not settle them.

Our own question from that work, not a source claim: what does the work lose if this layer
goes? If nothing, cut it.

## In this scene

The inspected source addresses websites, product UI and native apps, not slides.
Everything here is our **inference**, untested on a deck. Lessons 2, 5, 6, 7, 9 and
10 apply to review regardless of medium. A live talk may resemble Persuade and a
self-read deck may resemble Read, but check that against actual viewing conditions.
Do not import web layout, navigation or responsive rules into slides.
