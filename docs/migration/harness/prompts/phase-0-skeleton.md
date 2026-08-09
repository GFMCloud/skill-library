# Phase 0 — Build the library repo skeleton

**Nature:** greenfield build. Touches nothing in the existing Claude setup.
**Prerequisite:** every `CONFIG.md` field filled in (stop and ask if any is `TBD`).

## Steps

1. Create the repo at `local_clone_path`, init git, create the GitHub repo
   `<github_org>/<repo_name>` (visibility per CONFIG.md) and set it as origin.
   Covered by `auth_create_repo_and_push` in CONFIG.md — if `no`, pause and ask
   before `gh repo create` / first push.
2. Build the layout from `docs/end-state.md`:
   - `.claude-plugin/marketplace.json` — valid marketplace metadata, initially
     listing one plugin: `_incubator` (empty plugin dirs are fine at this stage).
   - `plugins/_incubator/` with its plugin manifest.
   - `scripts/validate-skills.sh` — copy from `templates/validate-skills.sh`,
     make executable.
   - `.github/workflows/validate.yml` — copy from `templates/validate.yml`
     (skip if `use_github_actions: no`).
   - `docs/authoring-standard.md` — copy from this project's
     `docs/authoring-standard.md`.
   - `CLAUDE.md` — authoring rules per the "Library repo CLAUDE.md" bullet in
     `docs/end-state.md`.
   - `CHANGELOG.md` — header + one entry: repo created.
   - `templates/SKILL.template.md` — copy from this project's templates.
3. **Prove the validator** (deliberate-failure test from `docs/validator-spec.md`):
   create a fixture skill violating F3, F5, and F10; run the validator; confirm it
   exits non-zero and reports all three; fix/remove the fixture; confirm clean exit 0.
   Record the observed output in `STATE.md` — this is the evidence the gate works.
4. Commit (small commits: layout, validator, CI) and push.

## Done when

- Fresh clone of the repo passes `scripts/validate-skills.sh` with exit 0.
- The deliberate-failure test demonstrably failed, and its output is logged.
- CI workflow present (if enabled) — it will be exercised on a real PR in Phase 5.
- `STATE.md` here: Phase 0 checked, session log line added.
