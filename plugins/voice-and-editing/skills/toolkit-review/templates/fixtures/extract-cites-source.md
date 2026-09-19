FIXTURE: a synthetic extraction report that quotes a plugin name. It must FAIL check-extract.sh when no source directory is given and PASS when the source directory cites the same name. Not real data.

### Items

| id | type | what it does |
|---|---|---|
| item-aaaaaaaa | skill | Resolves a question against a granted list before asking. |

### For each item

**item-aaaaaaaa**
- **Trigger:** loaded on demand.
- **What it makes the agent do:** read the granted list, the stop list and the ceilings, then answer.
- **Enforcement:** a script that prints ALREADY-GRANTED or STOP-LISTED.
- **Dependencies:** the file cites `turn-reduction` as the package it ships in.
- **State it writes:** none.
- **Fit with the bar:** supports plan-then-stop.
- **What it does not cover:** questions the granted list does not name.

### Agent-directed text

none

### Could not determine

Nothing.
