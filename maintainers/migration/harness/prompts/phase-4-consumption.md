# Phase 4 — Wire consumption

**Nature:** configuration changes on this machine. Still no deletions — superseded
things are renamed or deregistered, and removal waits for Phase 5.
**Prerequisite:** Phase 3 marked complete in `STATE.md`.

## Steps

1. **Register the marketplace** `<github_org>/<repo_name>` via the plugin system and
   **install** each real plugin (not `_incubator` unless the ratified table says
   otherwise). Covered by `auth_install_plugins` in CONFIG.md; the plugin list was
   ratified at Gate A — do not re-confirm it. Log the settings changes in `STATE.md`.
2. **Deregister superseded sources**: any old marketplaces/plugins that Phase 3
   emptied out get uninstalled/deregistered. Note each in `STATE.md`'s decision log.
3. **Sweep for leftover consumption paths**: any remaining symlinks into skill
   locations, or `.migrated-off` items that still shadow a live path — rename/adjust
   so nothing loads twice. (`.migrated-off` items themselves stay until Phase 5.)
4. **Update global `~/.claude/CLAUDE.md`**: add the short "Skill management"
   consumption section per `docs/end-state.md` ("CLAUDE.md at both scopes"). Covered
   by `auth_edit_global_claude_md`; record the exact diff in `STATE.md` so the user
   can review it at Gate B. Add only — never modify existing sections of that file.
5. If CONFIG.md lists other `machines`, write `docs/machine-setup.md` in the library
   repo: the exact register-marketplace + install-plugins steps to run there.

## Done when

- A fresh `claude` session lists the library plugins as installed, skills resolve
  under their plugin namespace, and nothing loads from a superseded location.
- Global CLAUDE.md updated; library repo pushed.
- `STATE.md` here: Phase 4 checked; deregistrations logged; session log line added.
