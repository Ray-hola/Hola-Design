"""Website patterns describe communication and composition, not UI task graphs."""
SCENE = "web"
USE_CASE = "web pages, content sections and responsive layouts"
DESIGN_RECORDS = ("visual_rules", "sections", "page_patterns", "responsive_rules")


def consumer_scope(profile):
    return USE_CASE if profile.get("page_patterns") else "local web components and visual styling; whole-page composition is unverified"


def validate(profile, review, evidence):
    sections = profile.get("sections", [])
    patterns = profile.get("page_patterns", [])
    responsive = profile.get("responsive_rules", [])
    if any(not isinstance(x, list) for x in [sections, patterns, responsive]):
        return {"scope": "invalid domain records"}
    section_ids = {x.get("id") for x in sections}
    for i, section in enumerate(sections):
        for field in ["purpose", "when", "structure"]:
            review.text(section, field, f"sections[{i}]")
        if not section.get("content_requirements"):
            review.warn("content-fit-unknown", f"sections[{i}]", "Record which content/assets this pattern needs")
    for i, pattern in enumerate(patterns):
        review.text(pattern, "visitor_goal", f"page_patterns[{i}]")
        order = pattern.get("section_order", [])
        if not isinstance(order, list) or not order or any(x not in section_ids for x in order):
            review.error("section-order", f"page_patterns[{i}]", "A page must reference recorded sections in order")
    for i, rule in enumerate(responsive):
        if rule.get("status") == "observed":
            refs = [evidence.get(x, {}) for x in rule.get("evidence_ids", [])]
            widths = {x.get("viewport_width") for x in refs if isinstance(x.get("viewport_width"), (int, float))}
            if len(widths) < 2:
                review.error("responsive-unproven", f"responsive_rules[{i}]", "Observed responsive change needs evidence from two viewport widths")
            subject = rule.get("subject")
            if not subject or any(x.get("subject") != subject for x in refs):
                review.error("responsive-subject", f"responsive_rules[{i}]", "Responsive evidence must refer to the same identified page/content region")
    if not patterns:
        review.warn("page-logic-unverified", "page_patterns", "Local tokens/sections do not establish whole-page order")
    if not responsive:
        review.warn("responsive-unverified", "responsive_rules", "Responsive behavior not inspected")
    return {"sections": len(sections), "page_patterns": len(patterns), "responsive_rules": len(responsive),
            "scope": "website communication patterns; conversion uplift needs separate behavioral data"}
