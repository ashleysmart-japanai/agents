## Secure by Query (not Fetch-and-Filter)

Encode the full access predicate in the database query so only authorized rows are ever returned. The query *is* the authorization gate. Never fetch a superset and filter it in application code.

**Fetch-then-check** (avoid):
```
row = db.findFirst({ id, orgId })   // coarse filter — may return unauthorized rows
if !canAccess(row, caller) → deny   // real decision in app code, after data is in memory
```

**Check-in-the-query** (prefer):
```
row = db.findFirst({ id, orgId, ...accessPredicates })  // query IS the gate
// if a row comes back, it is authorized by construction
```

**Rules**:
- Encode access rules (ownership, visibility, tenancy, placement) in the WHERE clause, not as a post-fetch filter.
- The query returns only rows the caller may see — never a superset discarded in app code.
- On list/search, visibility filters (user-private vs shared vs org-wide) are part of the query, not a `.filter()` after.
- Cover every access dimension in the predicate: org, project, user ownership, placement/visibility enum.
- Unknown or unrecognized access values (e.g. a new placement enum variant) are excluded by the query, not passed through and checked later.
- A post-fetch check is allowed only as a defense-in-depth *second* layer — never as the only gate.

**Why**:
- **Scales** — the database filters; application code does not scan and discard.
- **No information leakage** — unauthorized rows never enter memory, logs, or error messages.
- **Single source of truth** — the query defines authorization; no second code path drifts out of sync.
- **Auditable** — `EXPLAIN` shows exactly which rows are considered.

---
