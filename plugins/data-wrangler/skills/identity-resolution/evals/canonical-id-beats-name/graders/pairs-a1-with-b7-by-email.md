---
type: regex
pattern: "A1[^\\n]*B7|B7[^\\n]*A1"
match: contains
---

A1 and B7 share the canonical identifier and must land in one mapping row, even though their names differ. Rule 1 (exact match on canonical identifier) wins over the name match between A1 and B8.
