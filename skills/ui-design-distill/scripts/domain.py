"""UI tasks, states and transitions are distinct from component appearance."""
SCENE = "ui"
USE_CASE = "product interfaces, task flows and component states"
DESIGN_RECORDS = ("visual_rules", "screens", "components", "states", "transitions", "tasks")


def consumer_scope(profile):
    return USE_CASE if profile.get("tasks") and profile.get("transitions") else "component appearance and local interface structure; task flows are unverified"


def validate(profile, review, evidence):
    screens = profile.get("screens", [])
    states = profile.get("states", [])
    transitions = profile.get("transitions", [])
    tasks = profile.get("tasks", [])
    if any(not isinstance(x, list) for x in [screens, states, transitions, tasks]):
        return {"scope": "invalid domain records"}
    screen_ids = {x.get("id") for x in screens}
    state_ids = {x.get("id") for x in states}
    for i, state in enumerate(states):
        if state.get("screen_id") not in screen_ids:
            review.error("screen-reference", f"states[{i}]", "State must name a recorded screen")
        review.text(state, "description", f"states[{i}]")
    for i, transition in enumerate(transitions):
        at = f"transitions[{i}]"
        for field in ["from", "to"]:
            if transition.get(field) not in state_ids:
                review.error("state-reference", at, f"Unknown {field} state")
        review.text(transition, "action", at)
        if transition.get("status") == "observed":
            refs = transition.get("evidence_ids", [])
            if not any(evidence.get(x, {}).get("method") in {"interaction", "recording", "trace"} for x in refs):
                review.error("transition-not-observed", at, "A static screenshot/DOM snapshot cannot prove an action-result transition")
    edges = {(x.get("from"), x.get("to")) for x in transitions if x.get("status") == "observed"}
    for i, task in enumerate(tasks):
        at = f"tasks[{i}]"
        for field in ["actor", "goal", "success"]:
            review.text(task, field, at)
        route = task.get("state_path", [])
        if not isinstance(route, list) or any(x not in state_ids for x in route):
            review.error("task-path", at, "Task path references unknown states")
        elif task.get("status") == "observed":
            if len(route) < 2 or any(edge not in edges for edge in zip(route, route[1:])):
                review.error("task-path-unproven", at, "Observed task requires an observed transition for each step")
    for i, component in enumerate(profile.get("components", [])):
        review.text(component, "purpose", f"components[{i}]")
        if not component.get("state_coverage"):
            review.warn("component-states-unknown", f"components[{i}]", "Record observed vs not-inspected component states")
    if not tasks or not transitions:
        review.warn("visual-only", "tasks", "Task/transition coverage is incomplete; package is a partial UI reference")
    return {"screens": len(screens), "states": len(states), "transitions": len(transitions), "tasks": len(tasks),
            "observed_edges": len(edges), "scope": "declared coverage, not a usability certification"}
