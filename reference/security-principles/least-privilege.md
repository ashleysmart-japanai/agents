## Least Privilege

Every principal — user, service, credential, token — is granted the minimum access needed for its task, and no more. Scope narrows to the smallest boundary that still works.

**Rules**:
- A credential scoped to a project is not resolvable for another project; org-wide scope is used only where the spec requires it.
- Grant the narrowest role that satisfies the operation; do not reach for admin/superuser because it is convenient.
- Prefer per-resource or per-record scope over blanket access when the data model supports it.
- Tokens and credentials carry the smallest capability set and the shortest lifetime that works.
- Removing a privilege should break exactly one intended path — if it breaks many, the grant was too broad.

**Why**:
- A compromised or misused principal can only reach what it was scoped to — the blast radius is bounded by the grant.
- Broad grants accumulate silently and become impossible to reason about or revoke safely.

---
