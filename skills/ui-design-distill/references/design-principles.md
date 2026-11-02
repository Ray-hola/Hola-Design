# Design principles: review questions

Use only when relevant to the current brief. PPT, UI and web keep separate tasks and
acceptance criteria. Do not run every entry as a completion quota.

[principles.json](principles.json) holds short questions in this project's own words,
each with a limit and a scope label. They draw on widely taught design and perception
ideas. They contain no quotations and no book page references, and they are not a
substitute for reading primary sources on a subject that matters to the task.

## Select by the actual question

| Question | Group |
|---|---|
| Purpose and priorities | `purpose` |
| Information structure, entry and wayfinding | `structure` |
| Grouping, alignment, color and emphasis | `relations` |
| Letterforms and reading | `type` |
| What can be removed | `reduction` |
| Motion and traceable change | `motion` |
| Controls, effort and recovery | `operation` |
| Bad input, extremes and changed scale | `robustness` |
| Teaching and remembering | `learning` |
| Borrowed forms and physical analogies | `transfer` |
| Review bias and unsupported conclusions | `judgment`, `process` |
| Expressive departures | `appeal` |
| Manipulative or stereotyped cues | `bias` |

## Scope labels

- `conditional`: consider only after checking current applicability.
- `hypothesis`: compare an expressive or behavioral candidate; do not prescribe it.
- `context_only`: a physical or domain finding that needs separate screen evidence.
- `research_only`: recognize the claim or bias in review; not a generation default.

The labels are not a scientific ranking. Nothing here has been revalidated by this
project, and lookup or packaging does not change that. These questions do not verify
current standards, statistical claims, font identity or actual interface behavior.

Do not turn memory capacity into menu-count limits, physical space studies into CSS
spacing rules, optical balance into equal-width letters, or a liking for curves into
rounded corners everywhere. Print-era guidance is not a modern accessibility threshold.
Familiarity is not a ceiling on invention. Keep useful exceptions and intentional
residuals; missing text and omitted checks remain failures.

## Use within the existing LOOP

Form a task-specific question first. Put concrete subjects, parts and contexts into
`review_plan`; put a rejection condition and actual evidence into same-question
`challenge.tests`. Keep general ideas, project interpretation and current artifact
observations separate. Do not prefill worksheet decisions.

PPT needs claims and evidence, content pressure, viewing conditions and native-file
checks when delivered. UI needs actual tasks, states, focus and recovery. Web expression
needs whole, detail and neighbor review at supported widths, including layout transitions.
Originality can justify unfamiliar composition; it cannot replace actual inspection.

When a new task fails, attribute it to source applicability, distillation, execution
or coverage and repair that layer. A principle cannot emit PASS by itself; use
[the current exit protocol](loop-exit.md).

```bash
python3 "$SKILL_ROOT/scripts/principles.py" search "alignment" --scene web
python3 "$SKILL_ROOT/scripts/principles.py" show line-up legible-letters
python3 "$SKILL_ROOT/scripts/principles.py" worksheet \
  --ids line-up near-means-related legible-letters --scene web --out ./type-study.json
```

Search is literal keyword ranking, not semantic retrieval or exhaustive recall. Empty
searches can browse scene and adoption filters. Worksheets carry the question, its limit
and unanswered task fields. They preserve existing files and do not modify profiles or
certify design quality.
