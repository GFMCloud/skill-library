# Decisions: spotify-shunt (portal-ai-plugins and the companion Spotify engineering post)

contract: v1
source: https://github.com/spotify/portal-ai-plugins (plugins/shunt) and https://engineering.atspotify.com/2026/9/portal-by-spotify-cut-my-claude-code-token-usage-by-90
type: code-repo (plus article)
pin: 3c24ca30ff63e1f5bbad1c43fe5324daff579123 (cloned 2026-09-08T00:24:37Z); article fetched 2026-09-08T00:24:41Z sha256 a340d975c732e5254349ac58...
reviewed: 2026-09-07
verdict: HARVEST
recheck: n/a
evidence: docs/reviews/2026-09-07-spotify-shunt/cleanroom-review-repo.md, cleanroom-review-article.md, comparison.md

## Verdict reasoning

The plugin cannot be installed here: it assumes a Spotify Portal instance and its AiKA
worker modes, its bash-read hook is a speed bump (sed, awk, xargs cat pass), it ships any
readable file to a remote model with no secrets denylist, and its hook output shape
(`{"decision":"allow"}`) is one this library's own prove-hooks.sh would score as an error.
The idea is the deliverable: a PreToolUse hook as a router, whose block message carries the
cheaper path and the escape hatch, is the tool-layer form of a rule llama-offload states only
in prose. Four S-effort fragments improve llama-offload directly. The 90% figure is a
per-read ratio from an unpublished benchmark and is not to be quoted as fact. What would
change the verdict: nothing short of a local equivalent of Portal, which nobody here wants.

## Ancestry

none. Independent convergence on model-tier routing at the tool boundary; no shared strings,
no merge notes, no inventory overlap.

## Rows

Legend for Ruling: `proposed` | `ratified` | `overridden: <text>` | `out`.
Effort: `S` under an hour | `M` an afternoon, one PR | `L` multi-session (phased-harness).
Adoption cost is mandatory and never "none".

| # | Item | Class | Proposal | Source (path, lines) | Target (one library file) | Effort | Adoption cost | Ruling | Owner |
|---|---|---|---|---|---|---|---|---|---|
| 1 | A PreToolUse hook as a router: block the expensive read and hand back the cheaper path in the block reason, with an escape hatch for the case that needs exact bytes | COMPLEMENT (the tool-layer form of llama-offload's prose rules) | A `PreToolUse` Read hook that fires on files over a threshold when a batch-transform task is in flight and points at `/llama-offload`; correct output contract (`hookSpecificOutput.permissionDecision`); a fixture in `scripts/prove-hooks.d/`; proven by both controls before it is wired | `plugins/shunt/hooks/check-file-size:33` | `~/.claude/settings.json` plus a hook script under `~/.claude/hooks/`; fixture in `~/skill-library/scripts/prove-hooks.d/` | M | a process before every Read; a wrong threshold blocks ordinary large reads repo-wide (the review's own failure mode); removal is deleting the entry | ratified 2026-09-07 as a second hook in claude-scout-weekly `docs/runbooks/2026-09-03-hooks-and-permissions.md`; both controls before wiring | Graham |
| 2 | A silently unapplied constraint is a failure, not a result: check the response's `model` field against the model requested | INGESTIBLE FRAGMENT | One sentence in llama-offload step 4 (Verify): confirm Ollama's response `model` matches the request; a silent fallback to another local model is a failure | `plugins/shunt/scripts/lib/aika.sh:147-157` | `plugins/workbench/skills/llama-offload/SKILL.md` step 4 | S | one line; no runtime | ratified 2026-09-07; applied 2026-09-07 (llama-offload SKILL.md) | scout |
| 3 | Refuse the input that would produce confident nonsense: validate each input exists and is well formed before the batch runs | INGESTIBLE FRAGMENT | One line in llama-offload step 1 (Design): fail loudly on a missing or empty input record rather than send it | `plugins/shunt/scripts/bulk-read:30-37`, `scripts/code-write:28-33` | `plugins/workbench/skills/llama-offload/SKILL.md` step 1 | S | one line | ratified 2026-09-07; applied 2026-09-07 (llama-offload SKILL.md) | scout |
| 4 | Low temperature for reproducible batch output | INGESTIBLE FRAGMENT | One line in llama-offload Implementation notes: set `temperature` 0.1 to 0.2 in the `/api/generate` body | article, mode config `resourceLimits: temperature: 0.2` | `plugins/workbench/skills/llama-offload/SKILL.md` Implementation notes | S | one line | ratified 2026-09-07; applied 2026-09-07 (llama-offload SKILL.md) | scout |
| 5 | Secrets inside per-item text: ask before forwarding verbatim; never silently redact and never silently forward | INGESTIBLE FRAGMENT | One line in llama-offload Hard rules | `plugins/portal/skills/feedback/SKILL.md:24-25` | `plugins/workbench/skills/llama-offload/SKILL.md` Hard rules | S | one line | ratified 2026-09-07; applied 2026-09-07 (llama-offload SKILL.md) | scout |
| 6 | Never let the model ask for a credential, restated at each point of temptation | COMPLEMENT (no credentialed-CLI skill exists here yet) | Boilerplate clause for the next skill that wraps an authenticated CLI; nothing to land today | `plugins/portal/skills/setup/SKILL.md:12,66`, `doctor/SKILL.md:56` | none today | S | none until consumed | out (no consumer) | Graham |
| 7 | Stub the external binary so the transport suite needs no credentials | COMPLEMENT | llama-offload treats batch scripts as disposable by design; no persistent transport to test | `plugins/shunt/evals/transport-evals.sh` | none | n/a | n/a | out (no consumer) | scout |
| 8 | Enumerate what must not be delegated | REDUNDANT | llama-offload's Hard rules already name the escalation target per exclusion, which is better than a generic category list | `plugins/shunt/README.md:157-163` | none | n/a | n/a | out | scout |
| 9 | code-write: generate and write to the target before any human sees a sample | DISCARD (philosophy conflict) | Actively rejected: llama-offload's sample gate ("run 5 to 10 items, HARD STOP, wait for approval") governs any delegation here | `plugins/shunt/scripts/code-write:53` | none | n/a | n/a | out | scout |

## Conflicts for the user to rule on

- Sample gate versus write-then-review (row 9): llama-offload mandates approval before the
  batch; shunt's code-write writes first and reviews after. Not a question; recorded so the
  ruling is visible. Alternative: none recommended.
- Routing surface (row 1): a bare "this file is huge, route it somewhere cheaper" sits in
  the trigger space of model-effort-advisor, llama-offload, and any bulk-reader skill. If row
  1 is built, its block message must name llama-offload, not a new skill.

## Corrections at ingest

- Hook output contract: `{"decision":"allow"}` is not a value Claude Code's PreToolUse
  contract or this library's prove-hooks.sh recognizes; any port emits
  `hookSpecificOutput.permissionDecision` and ships a fixture.
- `check-bash-read` matches only `^(cat|head|tail|less|more) `; label any port a speed bump
  or harden it.
- bulk-read has no secrets denylist; a port adds one before any remote send.
- `sed '/^```/d'` in code-write deletes every fence-starting line; not to be copied.
- The 82 to 94 percent and 90 percent savings figures are unreproducible; do not cite.
- Everything assumes Portal and AiKA; retarget fragments at Ollama's `/api/generate`.
- Article prose uses em dashes and marketing register; restyle any quoted sentence.

## Flags

Disclosed, not injection: `AGENTS.md` directs execution of a validator outside the repo
(`uv run --with pyyaml python ~/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py .`)
and of `bash plugins/shunt/evals/run.sh`; the article's install line
`claude plugin marketplace add spotify/portal-ai-plugins` is addressed to the reader; the
hooks inject routing text into the agent's context on every blocked call by design. None
acted on; nothing addressed the reviewing agent adversarially.

## Rulings log

2026-09-07: proposed by the scout cycle (cycle 2); nothing ratified. Tier 2 is off; rows 2
to 5 are incubator skill body edits and would have needed the widened Tier 2 anyway. Row 1 is
settings.json territory (hooks-and-permissions runbook). Recorded in claude-scout-weekly
STATE.md as Q-2026-09-07-6.
2026-09-07: ratified in claude-scout-weekly `/phase ratify` (Graham, interactive). Rows 2 to 5 applied to llama-offload the same evening (workbench 0.9.2). Row 1 into the hooks-and-permissions runbook (Step 4). Recorded as Q-2026-09-07-6 ruling.
