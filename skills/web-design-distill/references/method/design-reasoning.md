# Learn design reasoning, not a catalogue of appearances

Read when extracting interaction logic, comparing award winners, or deciding what
can transfer between products. The learning target is a conditional explanation
of **why a relationship works for a particular intention**. Examples and kits make
that explanation inspectable; their count is not learning progress.

## From an instance to a mechanism

Keep these layers distinct:

| Layer | Question | Evidence needed |
|---|---|---|
| Intention | What does this person need to understand, feel, decide or accomplish here? | Source statement, actual content/task, or a labelled inference |
| Relationship | What relates to what: objects, words, images, actions, time, space, feedback? | Specific positions, contrasts, groupings and state pairs |
| Mechanism | How could that relationship produce the intended understanding or action? | Explain a causal hypothesis, not an adjective or an award badge |
| Conditions and cost | For whom, with which content, device, frequency and constraints could it work or fail? | Counterexample, missing state, competing need, access cost |
| Transfer | Would the same reasoning choose a sensible expression for a changed task? | New content/task; distinguish a reasoned proposal from an operated test |

Useful explanation: “Selecting a language first narrows the collection to an
identified object; expanding it then reveals unfamiliar metadata with adjacent
explanations. The sequence may reduce the amount a first-time visitor must parse
at once. Test whether someone can still compare two languages.”

Insufficient explanation: “Use a globe, rounded cards and progressive disclosure.”
The latter names appearances and a label without saying what is hidden, why, when
it returns, or what the person loses.

## Interrogate relationships before choosing a component

Choose questions relevant to the source, rather than running a universal checklist:

- **Meaning and attention:** Which distinction is meaningful? How do scale,
  type character, empty space, color, alignment or motion make it perceptible?
  Remove the distinction mentally: what would become ambiguous?
- **Expectation and causality:** What does an affordance promise? Compare the
  actual before/action/after. Did the meaningful object or task change, or did
  something merely animate? An input value or changed URL proves less than a
  useful result. Inspect delayed completion separately.
- **Context and continuity:** What remains stable during a change so people can
  locate themselves? What is intentionally replaced? Can they return, recover,
  compare or resume with the information they still need?
- **Visibility and timing:** Which information is essential now and which is
  deferred? Hiding can simplify an initial decision while making comparison or
  repeated work harder. Determine where disclosure helps and where simultaneous
  information is necessary.
- **Agency and effort:** Does the interaction give useful control? What must be
  learned, scrolled, remembered or waited for? A playful discovery task and a
  frequent lookup can justify different routes within the same identity.
- **Expression and semantics:** Why this type, image, gesture or material? Does
  it express the subject, clarify structure, establish tone, or produce a valuable
  experience? Preserve meaningful unusual choices; unfamiliarity is not failure.

Do not require every design to maximize every relationship. A revealing surprise
can deliberately postpone information; an operational task may need immediate
clarity. State the trade-off and check its consequences in that context.

## Comparisons that teach something

Compare cases with a shared question and different constraints. For example:

| Question | Contrast | Possible learning, still to test |
|---|---|---|
| Should the visitor follow a story? | Lando's narrative and direct Calendar menu; Language Inclusion and its separate Explorer | Narrative can build meaning while a direct route serves an already formed intention; their relationship matters more than either section template |
| How much information should be visible? | Explorer's object-to-details sequence; Tide Guide's simultaneous weather/tide overview | Disclosure depends on whether people are learning an object or coordinating several variables; fewer visible items is not universally better |
| What makes typography expressive? | Dropbox's width/weight demonstrations; Lando's serif/sans calendar composition | Glyph character, width, contrast and placement can express relationships rather than merely decorate a box |
| Is an action complete? | Explorer reaches an identified language and definitions; Pentagram text search remained loading in this visit | Judge the promised semantic result; do not turn an input response into successful task completion |
| Must an identity use one information density? | Scout's vehicle atmosphere and its actual Dimensions view | Keep the object recognizable while changing precision for feeling versus measurement; uniform styling can conceal the distinction the task needs |
| Can an experience itself provide evidence? | Bruno's declared playable portfolio; Dropbox's font demonstrations | Where the skill being presented is the experience itself, interaction may participate in the argument; its learning cost may be unjustified for an unrelated lookup task |
| Which data deserves emphasis? | Watch Duty's observed map/list with states and update times; Tide Guide's illustrated overview | Weight distinctions by the decision they inform; temporal freshness does not establish authority, and more data does not establish completeness |
| What must an alternative sensory form preserve? | Guitar Wiz's pictured finger positions and declared spoken guidance | Preserve the relationships and control needed for the same task, not merely a list of visual elements; spoken order and information volume still require testing |

The narrow Lando Calendar check adds another distinction: its list action reached
the intended rows, while persistent Store/Menu controls overlapped part of the
landing header/first row. Reaching a destination and reading its necessary content
are separate judgments. Inspect the actual action destination under the relevant
constraints; this observation does not justify a universal ban on fixed navigation.

These are interpretations from the 2026-10-30 research batch, not measured effects,
universal rules, or proof of independent transfer. The Tide Guide illustration is
from a 2024 article; its 2026 award does not make that image a current-build capture.

Primary reference entry points: [Lando](https://landonorris.com/),
[Language Explorer](https://sites.research.google/languages/language-explorer),
[Dropbox typography](https://brand.dropbox.com/typography),
[Pentagram Archive](https://www.pentagram.com/archive),
[Scout Traveler](https://www.scoutmotors.com/traveler),
[Bruno's FWA entry](https://thefwa.com/cases/brunos-portfolio),
[Watch Duty web counterpart](https://app.watchduty.org/),
[Guitar Wiz interview](https://developer.apple.com/news/?id=5zi5a25j),
[Tide Guide's 2024 story](https://developer.apple.com/news/?id=4r9b23wx).

One exceptional case can generate a valuable mechanism hypothesis. Repetition
alone cannot prove causality. Preserve disagreement and counterexamples: if the
same mechanism chooses the same appearance regardless of task, investigate whether
it is merely a stylistic habit.

## A compact reasoning record

Use this shape inside existing profile decisions/design_cases or a research note;
it supplements the existing schema rather than adding another compulsory form:

```text
Source instance and evidence status:
Intention and meaningful distinction:
Observed relationship / before -> action -> actual result:
Mechanism hypothesis and plausible alternative explanation:
Conditions, cost, counterexample and unknowns:
New context: what stays true, what should change, why:
Rejection test and actual outcome (or UNVERIFIED):
```

A useful rejection test could be: “Returning from a result loses the person's
selection, so they cannot continue comparing.” It should be able to overturn the
proposed design. “Looks professional” or “uses the winner's layout” cannot.

## Award and observation boundaries

An award is a sampling lead and evidence of a particular recognition. Record the
year, category and level: annual/day/month, jury/People's Voice, winner/finalist
are different facts. Do not infer universal superiority or success metrics.

Distinguish the award site's presentation, the maker's declared rationale, a
promotional screenshot/recording, and the real product build inspected now.
Record browser, platform, viewport and language where they affect interpretation.
Computed font-family is a declaration, not proof of the glyph font actually used.
Do not redistribute proprietary fonts or award artwork as starter assets.

Missing outcomes, a loader, denied access or an inspection-tool timeout remain
coverage limits. They can motivate a fallback/recovery hypothesis, but do not
establish that the underlying product is broken for its actual users.

For a complete website, inspect meaningful later content and an action destination.
For UX, observe the promised result and the relevant return/recovery path. For a
static surface or PPT, study reading and conceptual relationships without inventing
interaction. Do not import app shells, corner radii or web motion into other media
without a task-specific reason.

## Expanded comparisons from the 100-case study

The expanded research contains 100 distinct products/projects: ten baseline cases
plus ninety individually analyzed additions. Fifty additions are native apps and
interactive works studied through official/maker materials; forty are websites,
seven with additional scoped current-browser observations. These are conditional
interpretations, not 100 operated products or validated causal findings.

Use opposing cases to select a mechanism for the brief:

| Decision | Cases that disagree productively | Condition and rejection question |
|---|---|---|
| Reveal a control or preserve uninterrupted input? | Shapr3D added visible directional handles; Procreate uses draw-and-hold; StaffPad separates touch movement from Pencil notation | Is the main cost guessing what is possible or interrupting a known action? Check first-use discoverability, mode ambiguity and accidental activation; do not declare gestures universally intuitive |
| Recommend one route or preserve choice? | Duolingo's single learning path; stitch.'s selectable hoops; Universe's editable grid | A prerequisite sequence differs from open composition. Can the person with a formed intention bypass an irrelevant recommendation? |
| Defer details or keep them together? | Headspace's Today/Explore routes; Crouton's current step with quantities; Spotify's Library beside ongoing playback | If the task requires simultaneous comparison or keeping hands occupied, hiding related values can increase memory cost. Can the person proceed without moving between screens to reconstruct a relationship? |
| Adapt tools or keep their location stable? | StaffPad's instrument-specific tools; Halide's stable camera gestures | Adaptation can reduce irrelevant choices while disrupting learned movement. Does a frequent action move or change meaning unexpectedly? |
| Amplify feedback or let attention settle? | (Not Boring) Habits' deliberate press and layered completion; Pok Pok's repeatable gentle sounds; Loona's willingness to let the listener stop | Frequency, desired arousal and the meaning of completion differ. Can the person reduce intensity or leave without penalty? Engagement time is not a universal success measure |
| Unify identity or distinguish objects? | Igloo's maker replaced indistinguishable ice blocks with distinct forms; Rijksmuseum couples expressive artwork with precise object data | Shared material is compatible with different silhouettes and densities. Can adjacent objects be distinguished, compared and found again? |
| Keep text straight and regular or use it as form? | grug's custom stroke system; AW's narrow display letters, serif narrative and character texture; Searching for Birds' radial labels | Inspect whole words, actual strings, spatial rhythm and reading routes. Radial or displaced type may express a relationship; check that the required label/object relation survives |
| Follow a brand's type rules or preserve another voice? | Docusign Indigo guidance limits uppercase within its identity; Netflix Ads and AW visibly use uppercase display composition | A brand-specific prohibition is not an aesthetic law. Test role, scale, word shape, tone and the actual reading conditions; do not import one winner's bans into another brand |
| Simulate physical space or expose comparison? | Taobao's declared multi-product viewing; NBA's simultaneous game/data space; Feather's drawing/viewpoint controls; djay's staged entry into spatial performance | A 3D object is useful only insofar as the intended relation becomes understandable or experience valuable. Check scale, reference frame, synchronization, control and physical effort separately |
| Use metaphor in data or keep literal charts? | Searching for Birds' eggs and illustrated line chart; Blue Corridors' shared geographic layers; NBC Big Board's presenter/viewer demands | Illustration can participate in meaning, but quantity, denominator, time and uncertainty must remain interpretable. Do readers confuse search interest with population, geographic area with people, or missing data with low scores? |
| Break a familiar convention or preserve it? | Gibbon's hold-to-grasp/release-to-jump; Song of Bloom's changing styles with a persistent return; Flighty's airport-signage familiarity | A departure can be the meaning of an artwork. Keep a recoverable orientation/control contract, then test the expressive departure. Do not replace an unfamiliar but meaningful relationship with generic UI merely to satisfy consistency |
| Showcase an experience or promise a service? | Aether 1's explicitly fictional product demonstration; DICH's course-built fashion concept; SUPERSHINE's service terms | A concept can prove expressive possibilities, not commercial outcomes. Can viewers tell what exists, what is demonstrative, and what the next action commits them to? |

### Typography is a system of relationships

Read expressive type at three scales: glyph shape and spacing; word/line silhouette;
composition across the canvas and through states. A font name alone explains none
of their fit. In the scoped Google Fonts check, one custom preview phrase updated
the specimens together: control the text to compare faces, then use the actual
brief's strings and constraints to challenge the chosen face.

grug's maker describes evaluating newly drawn letters in real sentences and
extending that stroke language to layout and states. The current Docusign type
page presents glyph outlines/control points and explains custom Indigo, hierarchy
and fallback contexts. Neither supplies a reusable right to redistribute its font.

AW's visible character texture and playful microcopy can contribute tone rather
than convey literal task facts. Do not require every artistic mark to be a label.
Ask what perceptual, emotional or semantic role it plays and whether it competes
with necessary content. Conversely, calling random text "texture" cannot excuse
an unreadable headline or a broken information relationship.

### Check the settled outcome

The Renaissance Edition initially showed a low-contrast transition after the
Developer link changed the URL; later inspection showed the destination title,
description and selected chapter. The AW Work click was captured during movement,
so final arrival remains unverified. Rijksmuseum's initial object click was
blocked by a cookie notice; after dismissal/retry, The Milkmaid and its metadata
were inspected. Return changed the URL, but restored scroll/context was not checked.
These differences must survive the distillation instead of being flattened into
"navigation works."

Further primary reading:
[Shapr3D](https://developer.apple.com/news/?id=i6qdbzn9),
[Procreate](https://developer.apple.com/news/?id=e409h6ja),
[StaffPad](https://developer.apple.com/news/?id=5z97xxqw),
[Habits](https://developer.apple.com/news/?id=9ab1g4r3),
[grug](https://developer.apple.com/news/?id=ux44ymcr),
[Docusign type](https://brand.docusign.com/typography),
[Google Fonts](https://fonts.google.com/),
[AW](https://wodniack.dev/),
[Birds — maker account](https://www.visualcinnamon.com/portfolio/searching-for-birds/),
[Blue Corridors](https://ode.partners/en/projects/blue-corridors),
[Igloo — maker account](https://www.awwwards.com/igloo-inc-case-study.html),
[Gibbon](https://developer.apple.com/news/?id=0yia4yw7),
[Song of Bloom](https://developer.apple.com/news/?id=q9fq8jkq).

## Feed the three loops

- Distillation: can the explanation be traced to the actual instance, with
  declarations and hypotheses separated?
- Design: does a new expression make the intended relationships perceptible and
  its promised actions intelligible? Inspect the actual result, not just the plan.
- Feedback: when a changed task fails, was the mechanism wrong, its conditions
  missing, its expression poorly implemented, or the relevant context uninspected?

The number of cases, rules or kit entries cannot close a loop. Keep the existing
review/exit protocol and its evidence binding; author-written reasoning records
alone do not grant PASS.
