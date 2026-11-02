# Website profile contract

JSON scene is "web"; evidence semantics follow evidence.md. Required:
identity.name, sources and evidence. Keep domain concepts separate from UI tasks
and presentation sequences.

- context: audience, visitor intent, intended new page and known brand constraints.
- visual_rules: id/status/evidence_ids plus role/property/value/scope/exceptions.
- sections: id/status/evidence_ids, purpose, when, structure (text),
  content_requirements, optional parameters/avoid/variations/source instances.
- page_patterns: id/status/evidence_ids, visitor_goal, section_order (known section
  IDs), optional ordering_reason and page-specific exceptions.
- responsive_rules: id/status/evidence_ids, subject, affected pattern/property and change.
  An observed rule needs observed evidence at two viewport_width values from the
  same relevant source page/content; each evidence record has the same subject.
  The validator checks widths and subject keys; the agent checks that captures
  actually show that subject and change. Stylesheet declarations remain declared
  until inspected.
- decisions, checks, unknowns and artifacts as in evidence.md.

Omitted page patterns warn that whole-page logic is unknown; omitted responsive
rules warn that responsive behavior is unverified. Source-only or screenshot-only
profiles remain useful as partial references. Suggested checks: source, content,
responsive, browser, transfer. Conversion uplift requires behavioral data.

Package relevant engineering snippets/images by listing relative artifact paths.
The package includes profile.json, domain patterns, evidence, decisions and coverage;
it does not need the original website extractor installed to be consumed.


For evidence-graded product interpretation and visual relationships, read
[analysis-contract.md](analysis-contract.md). `intent` enriches existing context;
its optional fields do not merge the domain pattern schemas. `visual_rules` may
record representation, unit, relative_to, scope, precision and ratio basis.
The generated skill gets intent.json and the methodological references.
