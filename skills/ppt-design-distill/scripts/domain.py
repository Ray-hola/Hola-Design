"""PPT domain invariants, independent of UI/web fields."""
SCENE = "ppt"
USE_CASE = "presentations, slide layouts and presentation sequences"
DESIGN_RECORDS = ("visual_rules", "slide_patterns", "sequence_rules")


def consumer_scope(profile):
    if not profile.get("slide_patterns"):
        return "presentation visual styling; page selection and sequence are unverified"
    if not profile.get("sequence_rules"):
        return "slide layouts; cross-slide organization is unverified"
    return USE_CASE


def validate(profile, review, evidence):
    context = profile.get("context", {})
    if not isinstance(context, dict):
        review.error("context", "context", "Expected audience and presentation mode context")
    elif not context.get("presentation_mode"):
        review.warn("viewing-context", "context", "Live talk, self-read or remote viewing not specified")
    patterns = profile.get("slide_patterns", [])
    for i, pattern in enumerate(patterns if isinstance(patterns, list) else []):
        for field in ["purpose", "when", "structure"]:
            review.text(pattern, field, f"slide_patterns[{i}]")
        if not pattern.get("capacity"):
            review.warn("capacity-unknown", f"slide_patterns[{i}]", "New-content capacity not established")
    sequences = profile.get("sequence_rules", [])
    pattern_ids = {p.get("id") for p in patterns if isinstance(p, dict)} if isinstance(patterns, list) else set()
    for i, sequence in enumerate(sequences if isinstance(sequences, list) else []):
        review.text(sequence, "purpose", f"sequence_rules[{i}]")
        order = sequence.get("pattern_order", [])
        if not isinstance(order, list) or any(x not in pattern_ids for x in order):
            review.error("pattern-order", f"sequence_rules[{i}]", "Sequence references an unknown slide pattern")
    if not patterns:
        review.warn("style-only", "slide_patterns", "Visual rules alone do not establish page selection")
    if not sequences:
        review.warn("sequence-unverified", "sequence_rules", "No cross-slide organization recorded")
    return {"slide_patterns": len(patterns), "sequence_rules": len(sequences),
            "scope": "presentation rules; no UI-state or web-section requirement"}
