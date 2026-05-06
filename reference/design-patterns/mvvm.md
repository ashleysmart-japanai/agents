# Model-View-ViewModel (MVVM)

The view model exposes data and commands as observable streams that the view binds to declaratively.

**Applies to**: User Interface Design

---

**What it is**: The view model contains all presentation logic and exposes observable state. The view binds to the view model's state declaratively — no imperative push from the view model to the view. Changes in state automatically propagate to the UI via data binding.

**When to use**:
- The platform supports data binding (WPF, SwiftUI, Android data binding, React/Angular).
- UI state is complex and must be managed explicitly.

**Trade-offs**:
- Data binding mechanisms add a layer of indirection that can be hard to debug.
- Overuse of observables can make state flow hard to trace.
