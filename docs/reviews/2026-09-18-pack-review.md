---
contract: v1
source: five repos compared slot by slot (DietrichGebert/ponytail, alphaXiv/OpenResearch, stablyai/orca, cloudflare/security-audit-skill, tt-a1i/archify); six reviewed whole as worth-adopting (Tencent/WeKnora, hypit-ai/hypit, Human-Agent-Society/reef, deeplethe/utopia, webadderallorg/Recordly, abue-ammar/tinycast, plus ponytail's core ruleset and hooks)
type: skill-collection
pin: see 2026-09-18-pack-review/pins.tsv (11 rows, one sha per repo)
reviewed: 2026-09-18
verdict: HARVEST (the landing session's description of the Gate B row rulings; Graham ruled rows, not an overall verdict)
recheck: none
applied: branch pack-review-2026-09-18, the commits titled "decks 0.3.0", "foundry-core 0.6.0", "workbench 0.16.0", "workbench 0.16.1", "verification-kit 0.4.0" and "verification-kit 0.5.0"; ruled by Graham 2026-09-18 ("yes all as recommended, file-mode fix rides the branch"; for row 9, "B5 - Adopt as a sep skill as well" then "approve with defaults")
evidence: 2026-09-18-pack-review/ (extraction reports, all 18 judgments, ledger and per-item rows, decisions, slot mapping, both gates with Graham's rulings quoted, pins, usage, the seven whole-pack reviews, the generated page). Raw `claude -p` output is not archived here, matching the earlier records.
---

# Pack review, set-1

**Verdict:** fragments from three of the five compared repos were worth taking, one gap
was filled with a new skill, and one skill was vendored whole beside the installed one;
no candidate item replaced an installed one.

`workbench:toolkit-review` at set size, many-repos mode: 8 slots, two order-swapped
headless judges per slot, a third on the two slots where they disagreed. 47 headless runs,
10,654,980 tokens with cache reads, 66.6 percent of the 16M ceiling. The orchestrator read
no candidate file before Gate B and judged nothing; at landing each ratified row's source
was read as data and checked against the judges' description, and all matched.

**Ancestry:** none with this library. `archify` declares itself based on
`Cocoon-AI/architecture-diagram-generator` (MIT).

## What landed

- Row 2, diagram (`archify`): `plugins/decks/skills/html-diagram/scripts/validate.py` and
  `SKILL.md`. The screenshot leg fails closed. Commit "decks 0.3.0".
- Row 5, figures (`orx-figures`): `plugins/decks/skills/chart-discipline/SKILL.md`, a
  number-provenance section. Same commit.
- Row 3, evidence (`orx-evidence`): `plugins/foundry-core/skills/proof-of-work/SKILL.md`
  (stable, 1.3.0 to 1.4.0), a section on run-derived evidence. Commit "foundry-core 0.6.0".
- Row 4, experiment-loop (`orx-experiment-tree`):
  `plugins/workbench/skills/experiment-harness/SKILL.md` and three of its templates.
  Commit "workbench 0.16.0".
- Rows 7 and 8, overengineering-review (`ponytail-review`, `ponytail-audit`): new skill
  `plugins/verification-kit/skills/overengineering-review/`. Commit "verification-kit 0.4.0".
- Not a ledger row: the toolkit-review scripts' file modes, 100644 to 100755. Commit
  "workbench 0.16.1".

## Landed by exception

- Row 9, security-audit (`cloudflare/security-audit-skill` at c1c8a8c, MIT): vendored as
  `plugins/verification-kit/skills/security-audit/`, 20 files byte-identical to the pin
  plus `LICENSE` and `SOURCE.md`, frontmatter the only edit. Commit "verification-kit
  0.5.0". It went through a plan-gate first
  (`2026-09-18-pack-review/gate-b/plan-gate-security-audit.md`) because it ships 3,037
  lines of executable Node, and vendoring overrides two boundaries of the harness: "never
  copy a candidate file in whole" and no candidate code run. Graham approved both in
  those terms. Both validators were read in full before anything ran; `node --test` 65
  of 65 pass; pass and fail inputs were proven from this side.

## What was declined, and why

- Row 1, delegation (`orx-agent-delegation`): out. The one small take, a brief checklist
  for helper sessions, is mostly written already in the Concurrency section of the global
  CLAUDE.md, which the judges did not see.
- Row 6, orchestration (`stablyai/orca`): out. Two of three judges DISCARD; the file is a
  discovery stub that defers its logic to a guide fetched at runtime.
- Every item the page lists under "Found in the packs but not compared".

## Flags

- `archify/SKILL.md`, section "Update awareness", addresses the agent: it says to run a
  packaged update checker after the first candidate and, "If the command cannot run,
  continue without mentioning the check." Read as data at landing; not acted on; nothing
  from that section was taken.
- The whole-pack review of ponytail reports no text that instructs a reviewing agent.
- Known limits of this run: `dataviz`, which owns charts by Graham's precedence rule, is
  not in the library and was not compared against `orx-figures`. The built-in `/simplify`
  was not in the slot map for overengineering-review; the new skill's description
  separates the two. proof-of-work's two eval cases were not re-run for its change.
  overengineering-review has no eval cases and its routing is untested. Routing between
  security-audit and security-checklist is untested until the plugin is installed.

## Re-review trigger

Any pin in `pins.tsv` moving by a minor version; `adopt-humanizer` merging (it claims
workbench 0.15.0, this branch takes 0.16.0 and 0.16.1, so the second to merge resolves
the manifest and CHANGELOG); `cloudflare/security-audit-skill` moving past c1c8a8c, which is a re-vendor per `SOURCE.md`, never an in-place edit.
