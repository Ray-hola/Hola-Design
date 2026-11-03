# Product interface evidence

Identify one coherent surface and task. Establish actual theme/component owners
by imports, props, runtime style or supplied design documentation. Separate
current implementation from drafts and abandoned systems. Record exceptions.

Source code exposes declarations and potential behavior. Inspect rendered and
used values when possible; neither file proximity nor a shared class name proves
a connection. DOM capture supports local appearance, not intent or full state.

scripts/capture-ui.js is a Playwright run-code expression. Run at a recorded
viewport for each inspected state. It scans semantic controls and explicit roles,
not a marketing-section taxonomy or minimum viewport-width threshold. It skips
field values, hidden elements and password content. Still treat visible product
text as potentially private and keep captures in the authorized workspace.

Observe permitted actions and record action, precondition, before/after state,
visible result, input method, role and evidence. Prefer supplied recordings or a
sandbox fixture for mutations. Do not execute a payment, delete, send or account
change merely to collect its state. Mark those transitions uninspected instead.

A screenshot can establish a visible empty/error state. It cannot prove which
action caused it, that a control works, or which role can access it. A recording
or observed action-result pair can support transitions; document incomplete cases.
When only pictures exist, distill a partial visual/structural reference and keep
the missing workflow coverage in unknowns. Do not reconstruct imaginary behavior.
