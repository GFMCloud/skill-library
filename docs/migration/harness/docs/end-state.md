# End state — what "compliant" means

This document is the contract the migration works toward. When any phase prompt is
ambiguous, this doc is the tiebreaker.

## The model in one paragraph

One GitHub repo (`<github_org>/<repo_name>` from CONFIG.md) is the canonical home of
every reusable skill, structured as a **plugin marketplace** and consumed on every
machine as installed plugins via `/plugin`. Project-specific skills live in their
project's `.claude/skills/`, committed with that project. Every skill has exactly one
editable home. No symlinks, no copies, no skills in `~/.claude/skills/`, no edits to
plugin caches.

## Why plugins, not symlinks or copies

Drift comes from the consumption layer. The plugin system eliminates it structurally:

- **Namespacing** — plugin skills resolve as `plugin-name:skill-name`, so a name
  collision with a project skill is impossible rather than discouraged.
- **Pinning** — each machine's install is pinned to a commit; "what version am I
  running?" has an inspectable answer.
- **One update verb** — updating is a pull through the plugin system, identical on
  every machine.

Symlinks (though officially supported) track whatever branch the checkout is on and
must be reproduced by hand per machine. Copies fork silently on first edit. Neither
is used in the end state.

## Library repo layout

```text
<repo_name>/
├── .claude-plugin/
│   └── marketplace.json          # THE catalog — no parallel catalog files
├── plugins/
│   ├── core/                     # skills wanted on ~every project
│   │   └── skills/<skill>/
│   │       ├── SKILL.md
│   │       ├── references/       # long material lives here
│   │       └── templates/
│   ├── <domain>/                 # one plugin per coherent capability area
│   └── _incubator/               # new/unproven skills; no stability promise
├── .github/workflows/validate.yml
├── scripts/validate-skills.sh
├── CLAUDE.md                     # authoring rules for sessions editing this repo
├── CHANGELOG.md                  # behavior changes, not wording tweaks
├── MIGRATION.md                  # produced by Phase 1; kept as historical record
└── docs/authoring-standard.md
```

Plugins are grouped by **install unit** — the set of skills you'd enable or disable
together — not by topic taxonomy. Prefer ~3–7 plugins over one mega-plugin or twenty
single-skill plugins.

## The two-homes rule

| Skill kind | Home | Consumed via |
|---|---|---|
| Reusable across projects | Library repo, under a plugin | Installed plugin |
| Specific to one project | That project's `.claude/skills/` | Committed with the project |

Never both. A project skill must never share a name with a library skill. When a
project skill proves reusable, it is **promoted** — moved into the library (starting
in `_incubator/`), with the project then consuming the plugin version.

## The skill contract

Defined in full in [authoring-standard.md](authoring-standard.md). Summary: required
`name` + router-style `description`; a `metadata:` block carrying `maturity`
(incubator | stable | deprecated), `version`, `reviewed`, and `supersedes` when
deprecating; body under 500 lines with long material in `references/`.

## Enforcement

`scripts/validate-skills.sh` (spec: [validator-spec.md](validator-spec.md)) runs on
every PR via GitHub Actions and locally before commit. Discipline the validator can't
check lives in the library repo's CLAUDE.md, which governs authoring sessions.

## CLAUDE.md at both scopes

- **Library repo CLAUDE.md** (authoring): this repo is the only editable surface;
  follow the authoring standard; new skills start in `_incubator/`; stable-skill
  changes bump `version` + `reviewed` and get a CHANGELOG line; run the validator
  before committing; never duplicate an existing skill name.
- **Global `~/.claude/CLAUDE.md`** (consumption, short section added in Phase 4):
  reusable skills live in the library repo and are edited only there — never in
  plugin caches; skill-creation requests route project-specific → project
  `.claude/skills/`, reusable → library `_incubator/`; flag any project-local skill
  duplicating a library skill as drift.

## Definition of done (Phase 5 gate)

1. Every skill in the machine-wide inventory appears in exactly one home.
2. All library plugins installed via the registered marketplace; skills resolve and
   slash commands work in a fresh session.
3. Auto-invocation fires for a prompt matching a migrated skill's description.
4. Validator green locally and in CI; a deliberately broken PR fails CI.
5. Global CLAUDE.md carries the consumption rules; library CLAUDE.md carries the
   authoring rules.
6. All `.migrated-off` locations removed — the only deletion step in the project.
