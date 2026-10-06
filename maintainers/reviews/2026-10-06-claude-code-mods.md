---
contract: v1
source: https://github.com/karanb192/claude-code-mods
type: code-repo
pin: 10617a90106144d3cb131bd599e677d9c38bfd35
reviewed: 2026-10-06
verdict: HARVEST
recheck: -
applied: none (rows 1, 2, 3, 5 await ruling, Q-2026-10-06-10; row 9 is a Tier 1 rider on Q-2026-09-28-3 in the scout's STATE.md)
evidence: maintainers/reviews/2026-10-06-claude-code-mods/ (cleanroom-review.md, comparison.md, decisions.md); scout run log claude-scout-weekly/runs/2026-10-06.md
---

# claude-code-mods (mod-builder)

**Verdict:** HARVEST. The `mod-builder` plugin is a careful harness for the Mods surface that
shipped in Claude Code 2.1.287 (a declared capability footprint diffed against the printed
one, an isolated child session with before-and-after hashes, status words only a script
printed), reviewed the week it became relevant; nothing in it has a consumer until this
machine builds a mod, and the repo carries a self-promoting star invitation, an unpinned
external plugin and a subagent-model rewrite that contradicts model-effort-advisor.

**Ancestry:** none; the incumbents descend from the ECC review and work at the settings
command-hook layer.

## What landed

- Nothing in the library this cycle. Row 9 (Mods as a candidate layer for the ratified spawn
  ceiling, since 2.1.290's `tool.check` carries `agentId`) landed as a rider on
  Q-2026-09-28-3 in claude-scout-weekly `STATE.md`.
- Rows 1 (normalize check output before comparing attempts in bounded-loop), 2 (isolation
  proven by evidence for the hooks-hardening runbook's live proof sessions), 3 ("the model's
  reply is not evidence a hook ran": name the record that counts) and 5 (a `recheck:` clause
  on restated CLI facts) are proposed, Q-2026-10-06-10.

## What was declined, and why

- Row 4 (footprint as a pre-declared budget): no consumer until a mod exists here; noted as
  the reference implementation if one is built, after the suffix-match bug is fixed.
- Row 6 (three-strikes breaker): bounded-loop is stronger and its budget semantics stand.
- Row 7 (fable-pin, image-peek, cache-tax, mod-builder whole): never install; fable-pin
  silently reroutes every subagent, cache-tax runs another repo's HEAD, image-peek reads the
  clipboard.
- Row 8 (lowest-reach-first): specific to the `$` API.

## Flags

`SKILL.md:137-141` and `references/invitation.md:15, 30, 34`: the agent is told to check and,
after an explicit yes, to star the author's repo with the user's `gh` login. `SKILL.md:24`
tells the agent not to load the built-in `plugin-authoring` skill. `list-mods.mjs:9` fetches
a JSON index from the author's other repo at run time. Quoted in the decisions file; nothing
run, nothing acted on.

## Re-review trigger

A decision here to build a mod (the spawn ceiling, or the idle handoff trigger from the
auto-handoff review); the pin moving with a second maintainer; or the hooks-hardening runbook
reaching step 8, when rows 2 and 3 are due. Verify the `CLAUDE_CODE_ENABLE_FUNCTION_HOOKS`
status against the installed CLI first; the source contradicts itself about it.
