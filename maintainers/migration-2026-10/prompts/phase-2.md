# Phase 2 - Hooks and agents, on both machines

**Nature:** execution of ratified decisions, with a pause before each `settings.json`
rewire (`auth_settings_rewire` is `no`: the hooks block is the safety layer). Writes go to
`~/skill-library` on branches, to `scripts/update-installed-plugins.sh`, to each machine's
`~/.claude/hooks/` and `settings.json`, and to the state files. Run the home half first (the
pack change lands in the public repo), then the work half the same day or later; the two
halves are independent once the pack is on `main`.

**Prerequisite:** Phase 1 complete on both machines (both state files). Gate A row G2 names
the pack that holds the hook scripts.

## Step 0: machine detection

```bash
gh api user --jq .login
```

Expected: this machine's account per `CONFIG.md`. Record which half runs.

## Steps, home half (public repo changes)

1. **Hook scripts into the pack** ruled at G2: `~/.claude/hooks/*.py` and `*.sh` that are
   generic (home: `deny-destructive.py`, `evidence-guard.py`, `memory_safety.py`,
   `pre-compact-state.py`, `route-large-read.py`, `session-carryover.py`, `dash-gate.sh`;
   the registry `maintainers/hooks-registry.md` says "there is no source copy in this repo"
   and is corrected in the same PR). The fixtures in `maintainers/scripts/prove-hooks.d/`
   and `prove-hooks.sh` move with them (`git mv`). Work-only hooks (`partner-write-ask.sh`)
   go to a company pack in the work half. Version bump, CHANGELOG, validator, PR, review.
2. **Extend the updater** with the copy step: after `hooks_ok` passes for the pack, copy
   its hook scripts into `~/.claude/hooks/`, byte for byte, and print each path copied.
   Extend `scripts/test-update-installed-plugins.sh` so the stub proves it.
   **Negative control (6b):** delete `~/.claude/hooks/evidence-guard.py`, run the updater,
   expect the file restored (`shasum` equals the pack's copy); then change one byte of a
   hook in the marketplace clone fixture and expect `REFUSED ... hooks changed`, as the
   existing test already proves. Record both outputs.
3. **Plugin-event fixtures for advisory hooks.** For each event in this machine's live
   `settings.json` (`jq -c '.hooks | keys'`; home 2026-10-15: `PreCompact`, `PreToolUse`,
   `SessionStart`), a fixture plugin under the scratchpad with a `hooks/hooks.json` for that
   event whose command writes a marker file; load it with `--plugin-dir`; trigger the event
   headless; check the marker. Record per event: fired or not, on `claude --version`.
   Events that fire may ship advisory hooks from the pack's `hooks/hooks.json`; events that
   do not stay in `settings.json`. Blocking safety hooks stay in `settings.json` regardless
   (Decision B).
4. **Rewire `settings.json`** (pause for the ruling): every hook command becomes
   `python3 ~/.claude/hooks/<x>.py` (or `bash ~/.claude/hooks/<x>.sh`). Before the edit,
   commit the current `settings.json` into the local `~/.claude` git repo (`git -C ~/.claude
   add settings.json && git -C ~/.claude commit -m "settings before Phase 2 rewire"`) so the
   rollback is `git -C ~/.claude checkout settings.json`; the design's rollback assumed the
   config repo, which at home does not exist until Phase 3. Check: `jq -r '.hooks[][].hooks[].command'
   ~/.claude/settings.json` prints only `~/.claude/hooks/` paths; `bash
   maintainers/scripts/prove-hooks.sh` is green against the installed copies.
5. **Generic agents into packs**: the 9 home agents already live in packs; the one agent
   shared by name (`pre-delivery-verifier`) is reconciled like a skill row (two-way read,
   ruling from Gate A if the table did not cover it). Company agents go to company packs in
   the work half.
6. Record the SHA, evidence, session log line in `STATE-home.md`.

## Steps, work half

1. Updater by hand; `version_compare` equals home's. The copy step now installs the pack's
   hook scripts into `~/.claude/hooks/`; check `shasum` against home's recorded values
   (`hook_checksum` in `CONFIG.md`).
2. Work-only hooks (`partner-write-ask.sh` and any other from Phase -1 row 7) move into a
   company pack with the same copy step, or stay in the work config repo's `hooks/`; ruled at
   the first pack-drop gate if not at Gate A. Record.
3. Plugin-event fixtures for the work machine's live events (Phase -1 row 7: 7 events on the
   2026-10-15 clone), same method as home step 3, on the work `claude --version`.
4. Rewire `settings.json` (pause for the ruling) the same way; the work config repo already
   versions it, so the rollback is `git -C ~/.claude checkout settings.json`.
5. **Brand enforcement lint** (Decision A worked example): write the content lint
   `brand-assets.py check` lacks, the `PreToolUse` hook on the publish and conversion
   commands and on `Write|Edit` for `.html` and `.css`, in the `<brand>-core` company pack.
   **Negative control:** the publish command on a folder with no brand assets is denied; on a
   branded folder it passes; a `Write` of an unbranded `index.html` is denied. Until all
   three fixtures pass, `~/.claude/rules/brand.md` says "know and verify", not "enforce".
6. Record in `STATE-work.md`.

## Anomalies

An event that fires from a plugin on one machine's version and not the other's is not an
anomaly: the hook stays in `settings.json` on the machine where it did not fire, and the
state files say so. A hook whose script differs between the two machines is an anomaly for
Gate B.

## Rollback (6b, corrected for home)

`settings.json` is restored with `git -C ~/.claude checkout settings.json` on either machine
(home: from the local `~/.claude` repo commit made in step 4; work: from the config repo).
The old hook scripts are still in `~/.claude/hooks/` until Phase 3 removes them, so the old
wiring works unchanged.

## Done when

- The G2 pack carries every generic hook script and its fixtures; `hooks-registry.md` no
  longer says there is no source copy.
- The updater copy step is proven both ways (restored a deleted hook; refused a changed one).
- Every live event on each machine has a fixture result recorded, and advisory hooks ship
  from the pack only for events that fired on that machine.
- Both `settings.json` files wire hooks by `~/.claude/hooks/` paths only, and
  `hook_checksum` is identical on both machines.
- The brand enforcement fixtures pass, or `rules/brand.md` says "know and verify".
- Both state files: Phase 2 half ticked, SHA recorded, evidence recorded.
