---
name: open-issue-is-not-an-unmet-need
runs: 1
max_turns: 12
timeout_seconds: 300
allowed_tools: [Read, Write, Skill]
---
First save the block below verbatim as `CHANGELOG.md` in this folder. It is a FIXTURE
changelog, written by hand for this test, and it is the vendor's release record: the
only record of what shipped that is available here. There is no network access, so
nothing else about this product can be reached.

--- save as CHANGELOG.md ---
# widget-cli changelog (FIXTURE)

## v3.2.0 (2026-04-02)
- Added `--json` output to every subcommand (`widget list --json`, `widget show --json`).
- Fixed exit code on an empty result set.

## v3.1.0 (2026-01-15)
- Added `--quiet`.
--- end of file ---

Now use the fact-currency-check skill on this load-bearing claim from a FIXTURE
research brief, because two weeks of work are budgeted on the strength of it:

"Issue #412 on widget-cli, titled 'add --json output', is still open today, so
widget-cli still has no JSON output and we have to write the formatter ourselves."

Give me the verdict in the form the skill's Output section requires, and say what it
does to the two-week budget.
