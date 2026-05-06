# Data Clumps

The same group of data items (e.g.

**Applies to**: Object-Oriented Design

---

**What it is**: The same group of data items (e.g. `street`, `city`, `postcode`) appear together repeatedly across parameters, fields, and returns but are never encapsulated into a single type.

**Why not**: Related data belongs in one type. Without encapsulation, validation and behaviour are scattered, and the relationship between the fields is implicit.
