# N+1 Query Problem

Fetching a list of N items and then making one additional database query per item — N+1 queries total instead of one or two.

**Applies to**: Database Design

---

**What it is**: Fetching a list of N items and then making one additional database query per item — N+1 queries total instead of one or two.

**Why not**: Query latency compounds linearly with the list size. What works in development with 10 items breaks in production with 10,000. Use eager loading, joins, or batched queries.
