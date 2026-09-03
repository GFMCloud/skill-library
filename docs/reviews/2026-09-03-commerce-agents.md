---
contract: v1
source: https://github.com/anthropics/commerce-agents (+ claude.com anatomy article)
type: code-repo
pin: fd4d59224ab96b43c6dc6888207c67b3bd5a24cf
reviewed: 2026-09-03
verdict: HARVEST
recheck: n/a
applied: row 2 in ~/.claude commit e81d4d6 (2026-09-03); row 1 lands in the next scout Phase 2; row 3 is a runbook
evidence: docs/reviews/2026-09-03-commerce-agents/
---

# commerce-agents

**Verdict:** HARVEST. Not a commerce build; the portable principles are the deliverable:
cost per completed task, the scope of subagent fan-out, a consistency checker as a CI
gate, snapshot-eval case design, and a set of tool-contract conventions held for a
future product-agent build.

**Ancestry:** none.

## What landed

nothing yet. Rows 1 to 4 proposed; rows 5 to 8 out.

## What was declined, and why

- The placement rule (a third of traffic): governs a different object than the CLAUDE.md
  economy rule.
- Memory as typed facts: no consumer on this machine.
- Tool contracts and cache-prefix mechanics: held until a product-agent build exists.

## Flags

none.

## Re-review trigger

A product-agent build on this machine, or the pin moving with a maintained release.
