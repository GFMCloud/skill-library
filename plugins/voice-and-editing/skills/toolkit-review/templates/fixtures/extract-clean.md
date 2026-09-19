FIXTURE: a synthetic extraction report that must PASS check-extract.sh. Not real data.

### Items

| id | type | what it does |
|---|---|---|
| item-aaaaaaaa | hook | Blocks shell commands that match a list of destructive patterns. |
| item-bbbbbbbb | skill | Tells the agent to write a failing test before fixing a bug. |

### For each item

**item-aaaaaaaa**
- **Trigger:** runs before every shell command; always on.
- **What it makes the agent do:** nothing directly; it denies the command and returns a reason.
- **Enforcement:** a script that exits with a deny decision. Fails open on a parse error.
- **Dependencies:** python3.
- **State it writes:** none.
- **Fit with the bar:** neutral on all three.
- **What it does not cover:** file edits and reads.

**item-bbbbbbbb**
- **Trigger:** loaded on demand when the request mentions a bug fix.
- **What it makes the agent do:** "write the failing test first", then run the suite before claiming done.
- **Enforcement:** prose only.
- **Dependencies:** none named.
- **State it writes:** none.
- **Fit with the bar:** supports executed evidence; ignores the other two.
- **What it does not cover:** changes with no test harness.

### Agent-directed text

none

### Could not determine

Nothing.
