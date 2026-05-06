# Presentation Model

Extract all UI logic into a presentation model object; the view is a thin rendering shell.

**Applies to**: User Interface Design

---

**What it is**: A plain object mirrors the state of the UI — checkboxes, enabled states, formatted strings, validation messages. The view reads from and writes to the presentation model. Logic lives in the model, not the view.

**When to use**:
- UI logic must be unit tested without a running UI framework.
- The same presentation logic must drive different view technologies.

**Trade-offs**:
- The presentation model must stay in sync with the view's structure.
- Can produce a large number of properties for complex screens.
