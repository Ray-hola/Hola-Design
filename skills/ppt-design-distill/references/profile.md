# Presentation profile contract

Use a JSON object with scene "ppt". Evidence metadata follows evidence.md.
Required: identity.name, sources and evidence. Domain collections are optional
when unobserved; omitted pattern/sequence coverage produces warnings.

- context: audience, presentation_mode (live-talk/self-read/remote/unknown),
  intended_output and canvas where known. These are usage facts or assumptions.
- visual_rules: id, status, evidence_ids, property/role, value, scope and exceptions.
- slide_patterns: id, status, evidence_ids, purpose, when, structure (text),
  capacity (observed limits/unknown), optional avoid/parameters/variations.
- sequence_rules: id, status, evidence_ids, purpose, pattern_order (array of
  recorded slide-pattern IDs), optional conditions/variations.
- decisions, checks, unknowns and artifacts use evidence.md.

A style-only profile is valid with a coverage warning. Do not fabricate a
sequence to silence it. An observed rule must cite observed evidence; a value
read from OOXML is declared until its actual rendering was inspected.

Suggested check IDs: source-visual, page-fit, narrative, native-file, transfer.
Only record passes after the named check was actually performed. The structural
validator does not establish readability, narrative quality or native editability.

Package with scripts/profile_tools.py package; the consumer gets profile.json,
patterns.md, evidence.md, decisions.json, coverage.json and any declared artifacts.
Relative artifact paths are preserved under assets/reference/.


For evidence-graded product interpretation and visual relationships, read
[analysis-contract.md](analysis-contract.md). `intent` enriches existing context;
its optional fields do not merge the domain pattern schemas. `visual_rules` may
record representation, unit, relative_to, scope, precision and ratio basis.
The generated skill gets intent.json and the methodological references.
