FIXTURE: a synthetic comparison judgment that must PASS check-judgment.sh (rubric v2). Not real data.

### Steelman X
X blocks destructive commands at the tool layer, so it holds even when the agent is careless.

### Steelman Y
Y gives the agent a concrete test-first routine with stop conditions, which X does not attempt.

### Scores

| Criterion | X | Y |
|---|---|---|
| Fit with the bar | 3, neutral to all three behaviors per its report | 3, reinforces executed evidence |
| Enforcement mechanism | 3, a script that denies | 0, prose only |
| Context cost | 3, nothing loaded into context | 2, loaded on demand, 60 lines |
| Maintenance burden | 3, python3 is present | 3, no dependencies |
| Specificity | 2, a fixed pattern list | 3, named steps and stop conditions |

### Per-item rows

| Item | Class | Note |
|---|---|---|
| item-aaaaaaaa | COMPLEMENT | Fills the gap that the other set has no enforcement at all. |
| item-bbbbbbbb | COMPLEMENT | Fills the gap that the other set has no build routine. |

### Deciding criteria
Enforcement mechanism and Specificity.

### What I could not assess from reading alone
Whether item-bbbbbbbb actually triggers on a bug-fix request.
