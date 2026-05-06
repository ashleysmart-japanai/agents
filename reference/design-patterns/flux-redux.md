# Flux / Redux

Unidirectional data flow — actions describe what happened, a dispatcher routes them, a store updates state, the view re-renders from state.

**Applies to**: User Interface Design

---

**What it is**: State is stored in a single store. The view dispatches actions (plain objects describing events). Reducers are pure functions that compute the next state from the current state and the action. The store notifies the view of state changes.

**When to use**:
- Complex UI state shared across many components.
- State changes must be traceable, replayable, and testable.
- Time-travel debugging or undo/redo is needed.

**Trade-offs**:
- Significant boilerplate for simple state.
- Async actions require middleware, adding complexity.
- Overkill for applications with simple, local UI state.
