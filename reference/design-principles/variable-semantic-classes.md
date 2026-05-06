## Variable Semantic Classes

Variables carry meaning beyond their type. Classify them to make intent explicit and prevent misuse.

| Class | Meaning | Examples |
|-------|---------|---------|
| **Identity** | Uniquely names an entity; never transformed | `user_id`, `order_sid`, `node_key` |
| **State** | Current condition of an entity; mutates over time | `status`, `phase`, `is_active` |
| **Value** | A quantity or measurement; may be calculated | `count`, `total_price`, `duration_ms` |
| **Flag** | A boolean decision point; names start with `is_`, `has_`, `can_` | `is_valid`, `has_flag`, `can_retry` |
| **Accumulator** | Collects values across iterations | `results`, `errors`, `seen` |
| **Cursor / Index** | Tracks position in a sequence | `i`, `offset`, `cursor` |
| **Sentinel** | A special value signalling a boundary condition | `None`, `EOF`, `-1` as "not found" |
| **Intermediate** | A temporary result in a multi-step computation; should be short-lived | `raw`, `parsed`, `filtered` |
| **Config / Constant** | A fixed parameter; does not change at runtime | `MAX_RETRIES`, `DEFAULT_TIMEOUT` |

Rules:
- Name the variable after its semantic class, not its type. `user_id: str`
not `user_string: str`.
- Sentinels must be documented. A bare `None` return is ambiguous — prefer
a typed `Optional` or result type with an explicit absent case.
- Accumulators are initialised before the loop that fills them and consumed
after it — they should not escape further than necessary.

---
