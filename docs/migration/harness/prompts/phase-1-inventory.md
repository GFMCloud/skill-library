# Phase 1 — Machine-wide skill inventory

**Nature: STRICTLY READ-ONLY.** Do not modify, move, rename, or delete anything you
find. Prefer plan mode for the sweep. The only writes permitted are the two output
files listed at the bottom.

## Sweep

Find every skill artifact on this machine, wherever it lives. Search at minimum:

- `~/.claude/skills/`, `~/.claude/agents/`, `~/.claude/commands/`
- `~/.claude/plugins/` — registered marketplaces (`known_marketplaces.json`),
  installed plugins (`installed_plugins.json`), and cached plugin contents
- `~/.claude/settings.json` — `enabledPlugins` and marketplace entries
- Local clones of any marketplace/skill-library repos (check common code dirs:
  `~/work`, `~/src`, `~/Developer`, `~/repos`, `~/GitHub`, home dir itself)
- `.claude/skills/` and `.claude/agents/` in every project repo you can find
- Strays: `SKILL.md` files anywhere else (`~/.claude/**`, scheduled-task dirs,
  Documents archives), `.skill` zip files, anything skill-shaped

Use broad finds (e.g. `find`/`fd` for `SKILL.md` and `*.skill` across the home dir,
excluding caches you've already catalogued) — the point is that *nothing* is missed.

## Record, per skill

Path; skill name (from frontmatter); how it's consumed (installed plugin / marketplace
clone / project copy / symlink / orphan); frontmatter completeness vs.
`docs/authoring-standard.md`; body line count; last-modified date.

## Drift detection — the critical part

Where the same skill (by name or by obvious lineage) exists in more than one place,
**diff the copies** and summarize what actually differs in one or two lines — not
"files differ" but *what* differs (sections, rules, frontmatter). Each drifted pair
is a decision the user must make in Phase 2: flag these rows, and add your
recommendation for which copy should win with one line of reasoning.

## Output

1. `MIGRATION.md` committed to the library repo — format per
   `templates/MIGRATION.template.md`: one row per skill, with the **Proposed
   disposition** column filled in for every row (your recommendation + one line of
   reasoning; drifted rows also get a proposed winner). The Ruling column stays
   empty — it is filled at Gate A (Phase 2).
2. `STATE.md` here: Phase 1 checked; Anomalies section updated with anything
   skill-shaped that didn't fit the table; session log line added.

Do not begin migrating — proposals are not rulings. The phase ends when the
inventory with proposals is committed; Phase 2 presents it for ratification.
