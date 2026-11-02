# Product UI profile contract

JSON scene is "ui"; shared evidence semantics are in evidence.md. Required:
identity.name, sources and evidence. Collect only the scope supported by inputs.

- context: actor(s), product objects, primary job, platform, input method and
  observed data ranges. Unknown roles stay unknown.
- visual_rules: id/status/evidence_ids plus property/role/value/scope.
- screens: id/status/evidence_ids, purpose and relevant structure.
- components: id/status/evidence_ids, purpose, anatomy, variants and
  state_coverage (map state names to observed/not-inspected/not-applicable with
  evidence where observed). This is not a claim that every component needs all states.
- states: id/status/evidence_ids, screen_id and description. Each is a recorded
  product surface condition, e.g. list-ready, detail-ready, validation-error.
- transitions: id/status/evidence_ids, from/to state IDs, action and optional
  preconditions/actor/input_method. Observed transitions require observed evidence
  with method interaction, recording or trace.
- tasks: id/status/evidence_ids, actor, goal, success, state_path (state IDs),
  optional error/recovery/permission conditions. Every adjacent pair in an
  observed task must have an observed transition.
- decisions, checks, unknowns, artifacts as in evidence.md.

A profile with only visual/components is valid but warns that task evidence is
partial. Package it accurately as a limited UI reference. Never invent task paths
just to pass a validator. Geometry, source citations and check results do not
prove usability. Suggested checks: task, states, recovery, platform, visual, transfer.


For evidence-graded product interpretation and visual relationships, read
[analysis-contract.md](analysis-contract.md). `intent` enriches existing context;
its optional fields do not merge the domain pattern schemas. `visual_rules` may
record representation, unit, relative_to, scope, precision and ratio basis.
The generated skill gets intent.json and the methodological references.
