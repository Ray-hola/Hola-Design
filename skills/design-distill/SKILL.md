---
name: design-distill
description: >-
  Route reference-to-design-skill distillation when the intended deliverable is
  unspecified or mixes presentations, product interfaces and websites. Select
  PPT, UI or web by audience and use, preserving each branch's own evidence,
  patterns and evaluation. For an already clear scene use its branch directly.
---

# Design Distill router

## Input and output

Input: intended future design work and accessible references.
Output: selected scene skill(s), preserved scope and explicit routing reason.
This router does not implement extraction or authorize external actions.

## Choose by use, not file extension

| Future task | Load relative to this file |
|---|---|
| Explain or present through a slide sequence | `../ppt-design-distill/SKILL.md` |
| Complete a product task through objects, controls and states | `../ui-design-distill/SKILL.md` |
| Understand a public site, read content or decide and act from it | `../web-design-distill/SKILL.md` |

- IF the future task is clear: state the route and load that branch now.
- IF an unresolved ambiguity changes the branch: ask one focused question; reuse
  available context rather than asking again.
- IF mixed: use separate scene profiles and consumer skills. Share only explicit
  brand evidence, not domain checks. A dashboard image on a marketing page does
  not prove a working product flow. Keep the user's shared task limits.
- IF a sibling is absent: report the exact missing branch; do not improvise its
  implementation. Install the sibling scene folders to use this router.

## Handoff

Read the chosen branch's LOOP gate before extracting, including when the output
is only notes or an update to an existing skill. The branch's execution contract
separates DISTILL, APPLY, REPAIR and MAINTAIN and owns its evidence/exit requirements.
A book's reading coverage and a new design's acceptance are separate claims.
A draft package can support testing but cannot establish transfer quality.

For mixed-source examples read [routing.md](references/routing.md).
Each scene is independently installable and includes its own scripts/references.
