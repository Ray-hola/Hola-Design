---
name: design-distill
description: >-
  Route reference-to-design-skill distillation when the intended deliverable is
  unspecified or mixes presentations, product interfaces and websites. Select
  PPT, UI or web by audience and use, preserving each branch's own evidence,
  patterns and evaluation. For an already clear scene use its branch directly.
---

# Design Distill

Identify what future work the distilled skill should guide. Route by use, not
file extension: a web dashboard is product UI, a SaaS public site is a website,
and slides hosted on a site can still be a presentation.

| Intended future work | Load sibling skill |
|---|---|
| Present or explain in a sequence of slides | `../ppt-design-distill/SKILL.md` |
| Complete a product task using objects, controls and states | `../ui-design-distill/SKILL.md` |
| Read/understand a site or decide and act from its content | `../web-design-distill/SKILL.md` |

Resolve these paths relative to this file. Load only the applicable branch.
When multiple scenes are requested, produce separate profiles and consumer
skills; reuse only explicit shared brand evidence. A dashboard pictured in a
marketing page is not evidence of its working product flow.

If the outcome is clear, state the routing and proceed. Ask one focused question
only if missing context would change the branch or requested scope. Do not ask
again for information already provided.

Each branch contains its own scripts and references and works without this
router. If a sibling is missing, report the exact missing branch; do not claim
the router itself implements it. Install all four sibling folders to use the router.

For examples and mixed-source cases read [routing.md](references/routing.md).

For a cross-disciplinary book, keep source-reading coverage separate from
application and design acceptance; route by the future task rather than by the
book's file format. Each branch includes `references/method/design-principles.md` and
`scripts/principles.py`: review questions in our own words, not mandatory rules or
observed evidence of a new reference.


Open the selected branch's LOOP gate before extracting from any source, even
when the result will only edit a skill or produce notes. The branch owns three
bounded loops: distillation against source,
design against brief and learned rules, and new-task feedback with layer-specific
diagnosis. Mixed tasks keep separate domain checks and share the task's repair
budget. A generated skill carries its own review protocol and helper. A draft
package is usable for testing; packaging alone never establishes transfer quality.

Each branch also carries `references/loop/loop-exit.md`: use its scoped LOOP_EXIT
signal before completion, including its integrity gate for rendered work. A
checklist, package or partial repair alone cannot establish acceptance.
