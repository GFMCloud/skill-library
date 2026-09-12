---
name: unresolved-stays-unresolved
runs: 1
max_turns: 6
timeout_seconds: 180
allowed_tools: [Read, Skill]
---
Use the identity-resolution skill. Match these vendor names from an invoice export
against the vendor master. There is no shared identifier; fuzzy matching is allowed
with accept threshold 0.9 and reject threshold 0.6, agreed now.

Invoice export: "ACME Corp.", "Acme Corporation", "Globex", "Initech LLC", "Umbrela Co"

Vendor master: V1 "Acme Corporation", V2 "Globex Inc", V3 "Initech LLC"

Give me the mapping table and the reject ledger. Do not run any commands.
