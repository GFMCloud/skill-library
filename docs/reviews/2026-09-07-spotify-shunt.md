---
contract: v1
source: https://github.com/spotify/portal-ai-plugins (plugins/shunt) and https://engineering.atspotify.com/2026/9/portal-by-spotify-cut-my-claude-code-token-usage-by-90
type: code-repo (plus article)
pin: 3c24ca30ff63e1f5bbad1c43fe5324daff579123; article sha256 a340d975c732e5254349ac58... fetched 2026-09-08T00:24Z
reviewed: 2026-09-07
verdict: HARVEST
recheck: n/a
applied: none yet; rows proposed to /phase ratify in claude-scout-weekly (Q-2026-09-07-6)
evidence: docs/reviews/2026-09-07-spotify-shunt/
---

# spotify-shunt

**Verdict:** HARVEST. The PreToolUse-hook-as-router idea and four one-line fragments for
llama-offload are worth taking; the plugin itself needs a Spotify Portal instance, has a
bypassable bash-read hook, no secrets denylist, and a hook output shape this library's
prove-hooks.sh scores as an error.

**Ancestry:** none.

## What landed

nothing yet. Rows 1 to 5 proposed; rows 6 to 9 out.

## What was declined, and why

- Installing the plugin: assumes Portal and AiKA modes, blocks every Read over 350 lines
  repo-wide with no local fallback, unpinned `npx --yes` on every delegation.
- code-write's write-then-review: contradicts llama-offload's sample gate.
- The exclusion list: llama-offload's version names the escalation target per exclusion.

## Flags

disclosed agent-directed content only (AGENTS.md validator instructions, the article's
install line, hook-injected routing text); see decisions file.

## Re-review trigger

A local worker backend that does not need Portal (which would make row 1 a whole-plugin
question), or the hook output contract being corrected upstream.
