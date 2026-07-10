# Gold Plating

Also known as **Over-Engineering**. Adding durability, abstraction, or protection far beyond what the requirement justifies — building an elaborate solution for a low-value or low-probability risk.

**Applies to**: Software Design

---

**What it is**: Investing engineering effort to guard against a cost that is small, brief, or unlikely to occur — polishing past the point where the requirement is met. The extra code has real, permanent cost; the risk it defends against does not warrant it.

**Why not**: The build/maintain/remove cost of the gold plating exceeds the cost of the thing it protects against. It also adds surface area — more code to review, test, understand, and eventually delete — for no proportional benefit. When the requirement did not ask for it and no stated constraint demands it, it is speculative work.

---

## Signature case: deploy-gap scaffold

The most common form in this codebase is **temporary scaffolding to bridge a deploy transition** — an alias, re-export, dual-read/write, or "handle both shapes" branch added inside a single refactor PR to survive the brief window when old and new revisions run at once during a rolling deploy.

**Why it is gold plating**:

- **The cost exceeds the gap.** For most services the old revision drains within seconds of the new one going healthy. Building, reviewing, testing, and later removing scaffolding to protect a seconds-long window is more work — and more risk — than the window itself carries.
- **It's speculative.** Unless a specific stated requirement demands zero dropped requests across the transition (an SLA, a long-draining consumer, an irreversible migration), the scaffold defends a failure mode that will not occur.
- **The scaffold becomes permanent.** The "temporary" alias rarely gets removed — there is no forcing function to delete it, so it decays into [Lava Flow](lava-flow.md): dead weight nobody dares touch.
- **Citing the design rule is circular.** "The spec says no shims" is not the argument. The argument is the trade-off above: the scaffold's lifetime cost is larger than the cost of the gap it protects.

**Related process anti-pattern — unplanned ad-hoc migration**: smuggling transition/migration steps into an unrelated refactor PR instead of running them as a deliberate, staged migration. The scaffold is the symptom; the ad-hoc migration is the cause.

**The correct tool when the transition genuinely matters** — deliberate two-PR **expand/contract**, not a shim inside one refactor PR:

1. **Additive (expand) PR** — add the new route/field/shape *alongside* the old one. Deploy. Both now exist; nothing is removed.
2. **Contract PR** — once the new path is live and traffic has moved, remove the old route/field/shape and the bridging code.

Each stage is independently reviewable and revertible, and the removal is a tracked, scheduled step — not an orphaned "temporary" alias.

**Rejecting the scaffold — say this, not "the rule forbids it"**: *"Adding layers of temporary scaffold for a deploy transition where the gap is seconds at worst is over-engineering: the scaffold's build/track/remove cost exceeds the cost of the gap. If this transition genuinely warrants zero-downtime handling, it should be a deliberate two-PR expand/contract — an additive stage adding both, then a contract stage removing the old — not a shim in a single refactor PR."*
