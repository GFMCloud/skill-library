FIXTURE: a synthetic extraction report that must FAIL check-extract.sh, because it names the owner and drops a required section. Not real data.

### Items

| id | type | what it does |
|---|---|---|
| item-aaaaaaaa | hook | Graham's deny list for destructive shell commands. |

### For each item

**item-aaaaaaaa**
- **Trigger:** runs before every shell command; always on.
- **Enforcement:** a script that exits with a deny decision.
- **Dependencies:** python3.
- **State it writes:** none.

### Agent-directed text

none
