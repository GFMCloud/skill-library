# Validator specification — validate-skills.sh

What the library repo's validator must check. A reference implementation lives at
[templates/validate-skills.sh](../templates/validate-skills.sh); copy it into the
library repo's `scripts/` in Phase 0 and keep this spec as its source of truth.

## Scope

Every directory matching `plugins/*/skills/*/` in the library repo.

## Checks — FAIL (exit non-zero, blocks the PR)

| # | Check |
|---|-------|
| F1 | Skill directory has a `SKILL.md` |
| F2 | `SKILL.md` starts with a parseable YAML frontmatter block (`---` … `---`) |
| F3 | `name` present and non-empty |
| F4 | `description` present and ≥ 40 characters (heuristic against vague one-liners) |
| F5 | `name` equals the skill's directory name |
| F6 | No duplicate skill `name` across all plugins in the repo |
| F7 | Body (after frontmatter) ≤ 500 lines |
| F8 | Every relative markdown link/reference in `SKILL.md` resolves to an existing file |
| F9 | `metadata.maturity` present and one of `incubator` / `stable` / `deprecated` |
| F10 | `maturity: stable` ⇒ `metadata.version` (semver) and `metadata.reviewed` (ISO date) present |
| F11 | `maturity: deprecated` ⇒ `metadata.supersedes` present and names an existing skill |
| F12 | Skills under `plugins/_incubator/` must NOT be marked `stable` |

## Checks — WARN (reported, exit 0 unless STRICT=1)

| # | Check |
|---|-------|
| W1 | `metadata.reviewed` older than `stale_review_months` (CONFIG.md; default 6) on a stable skill |
| W2 | `disable-model-invocation: true` present — confirm slash-command-only is intended |
| W3 | Skill directory contains files >100 KB (bloats the plugin for every consumer) |

## Behavior

- Report every failure found, not just the first; summary line with counts; exit 1
  if any FAIL, exit 0 otherwise (exit 1 on warnings too when `STRICT=1`).
- Runs with no arguments from the repo root; accepts an optional path argument to
  check a single plugin.
- CI: `.github/workflows/validate.yml` runs it on every PR and push to main
  (reference copy in `templates/validate.yml`).

## Deliberate-failure test (Phase 0 and Phase 5)

Prove the validator actually gates: add a fixture skill violating F3/F5/F10, confirm
the script (and in Phase 5, CI on a throwaway PR) fails, then remove the fixture.
A validator that has never failed is untested.
