# Model-View-Presenter (MVP)

Like MVC but the presenter takes full control of the view; the view is passive.

**Applies to**: User Interface Design

---

**What it is**: The view is a thin interface with no logic. The presenter reads from the model, formats data, and tells the view what to display. The view forwards all user events to the presenter. The presenter and view are connected through a defined interface.

**When to use**:
- The view must be fully testable in isolation (the presenter can be tested without a real view).
- The platform makes it hard to test the view directly (mobile, desktop UI frameworks).

**Trade-offs**:
- Requires a view interface per screen — more boilerplate than MVC.
- Presenter can still grow large without further decomposition.
