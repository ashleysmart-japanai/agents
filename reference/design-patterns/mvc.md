# Model-View-Controller (MVC)

Separate data (model), display (view), and user input handling (controller) into distinct components.

**Applies to**: User Interface Design

---

**What it is**: The model holds application state and business logic. The view renders the model. The controller handles user input, updates the model, and selects the next view. Changes in the model notify the view to re-render.

**When to use**:
- Any application with a user interface that must be independently testable from business logic.
- Multiple views need to display the same underlying data.

**Trade-offs**:
- Controllers can grow large (massive view controller problem) if not further decomposed.
- Tight coupling between view and controller in many implementations.
