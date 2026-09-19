# Decisions: spot-2

contract: v1
classes: rubric v2 mapped to v1 (see make-ledger.py)
source: src1 at 9862685f575c65a8247f90369951df1b3416e3d6
reviewed: 2026-09-18
verdict: ADOPT (ruled by Graham 2026-09-18, verbatim: "ADOPT, add a stop before the file overwrite")

## Rows

| # | Slot | Item | Source path | Class (v1, per judge) | Class (v2, per judge) | Ruling |
|---|---|---|---|---|---|---|
| 1 | humanize | item-4555c4d5 | /private/tmp/tr-runs/spot-2/candidates/src1/SKILL.md | COMPLEMENT / COMPLEMENT | COMPLEMENT; COMPLEMENT | ADOPT with one change: a stop before the file-mode overwrite. Target: plugins/workbench/skills/humanizer/SKILL.md. Effort S. Adoption cost: a second home for anti-AI-tell rules beside the installed voice skill and the global style rules; about 390 lines loaded when it fires. |
