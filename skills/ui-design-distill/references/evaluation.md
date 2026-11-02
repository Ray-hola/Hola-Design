# UI transfer test

Use a new product task or object condition within the extracted system, such as
turning a recorded order-view path into a return-review path. State proposed new
behavior as requested design, distinct from what the source was observed to do.

Give the consumer its generated skill and new task/content. Ask it to identify
which existing patterns apply and what is genuinely missing. Test with recorded
or synthetic data in a sandbox; do not touch production accounts.

Evaluate separately:
- Can the intended actor complete the main task with plausible data?
- Are recorded states, transitions and applicable recovery paths complete?
- Do keyboard/focus, control naming, platform affordances and device behavior
  match the target use? Inspect actual behavior, not just DOM appearance.
- Does visual hierarchy help find the next action and distinguish meaningful data?
- Are source values and documented exceptions respected without inventing claims?

Test minimum/typical/large content where it materially changes the chosen pattern.
Take screenshots at relevant widths; a desktop-only source cannot establish mobile
rules. Record guessed extensions. Fix the strongest defects, then re-run affected
paths. Repeated unchanged attempts call for a new hypothesis; report any actual remaining gap. No screenshot
alone establishes task or accessibility success; untested paths stay skipped.


For the executable review record, follow [loop-protocol.md](loop-protocol.md).
New logs use adaptive exploration without default four/two repair quotas; explicit
user limits and legacy journal limits remain applicable. Use
[type-and-creative.md](type-and-creative.md) for typeface and creative comparisons.
A convention departure is evaluated by purpose and overall relationships, not
marked failed merely for differing. Record unsupported/missing evidence honestly.
