# Fact-currency check (as of 2026-09-02, via `gh api` against github.com, system of record)

| Claim | Primary source | Status | Detail |
|---|---|---|---|
| (a) Repo effectively unmaintained since 2026-04-20 | `gh api repos/.../branches` + `commits/<branch>`; `pulls/N` merged_by; issue timeline events | CONFIRMED, stronger than stated | Newest commit on any of the five branches is main at 2026-04-20. Every PR closed since April (#173, #182, #183, #185, #193, #194, #199) was closed by its own author, unmerged, with zero maintainer comments. 129 open items, the 15 newest all at 0 comments. Stars 209,665, forks 21,334. |
| (b) PRs #183, #188, #196 are unmet needs | `pulls/N` state today; grep of the pinned tree for the shipped behavior | CHANGED in one detail | #183 is CLOSED (by its author, 2026-07-13, unmerged), not open. #188 and #196 open, 0 comments. The test that matters: none of the three asks is present in main at pin `2c60614` (no no-test fallback, no self-check, no honest-reporting section; `EXAMPLES.md:480` still carries the false "non-deterministic" comment). Unmet, proven by absence from the tree, not by ticket state. |
| (c) No LICENSE file despite MIT claims | `contents/` listing; `gh api repos/.../license` (404); tree at pin | CONFIRMED | No LICENSE file. MIT asserted in README.md:171, .claude-plugin/plugin.json:8, and SKILL.md frontmatter `license: MIT`. PR #193 offered a LICENSE file and was closed unmerged. The frontmatter grant on SKILL.md itself is the strongest license statement in the repo. |

Executed checks of two clean-room factual claims (python3, this machine, 2026-09-02):
- EXAMPLES.md "reproduce first" test passes 10/10 against the unfixed `sorted(key=-score)`; tie order deterministic (Alice, Bob). CONFIRMED: the example reproduces nothing.
- `functools.lru_cache` on `async def`: second await raises `RuntimeError: cannot reuse already awaited coroutine`. CONFIRMED.
