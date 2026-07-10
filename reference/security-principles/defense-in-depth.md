## Defense in Depth

No single control is the only thing standing between an attacker and the asset. Independent layers back each other up, so one failed or bypassed control does not mean full compromise.

**Rules**:
- The primary gate is the strongest one (e.g. [secure-by-query](secure-by-query.md) at the data layer); additional checks are backups, not substitutes.
- A defense-in-depth layer is additive — it never *weakens* or replaces the primary control to justify its own existence.
- Do not add a redundant layer that has no consumer, no threat it uniquely covers, and no way to configure it — that is [gold plating](../anti-patterns/gold-plating.md), not depth.
- Each layer should fail independently: bypassing one must not automatically bypass the next.

**Why**:
- Real systems have bugs; a second independent layer converts a single-point failure into a near-miss.
- But depth is justified by a distinct threat each layer covers — layering for its own sake is cost without security.

---
