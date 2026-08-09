# Project configuration

Fill these in before running Phase 0. Sessions must stop and ask if any value is `TBD`.

| Key | Value | Notes |
|-----|-------|-------|
| `github_org` | `GFMCloud` | GitHub org/user that will own the library repo (github.com/GFMCloud) |
| `repo_name` | `skill-library` | Name of the canonical marketplace repo |
| `local_clone_path` | `~/skill-library` | Where the repo lives on this machine |
| `repo_visibility` | `private` | `private` or `public` |
| `use_github_actions` | `yes` | If `no`, validator runs locally only (pre-commit) |
| `stale_review_months` | `6` | `reviewed:` older than this triggers a validator warning |
| `machines` | `none` | Other machines that will consume the marketplace (for Phase 4/5 notes); `none` if just this one |

## Standing authorizations (for continuous runs)

These grant `/phase` permission up front so the run doesn't stop to ask. Set to `no`
to force a pause at that step instead.

| Key | Value | Covers |
|-----|-------|-------|
| `auth_create_repo_and_push` | `yes` | `gh repo create`, commits, and pushes to the library repo |
| `auth_install_plugins` | `yes` | Registering the marketplace, installing/uninstalling plugins, deregistering superseded marketplaces (Phase 4) |
| `auth_edit_global_claude_md` | `yes` | Adding the consumption section to `~/.claude/CLAUDE.md` (Phase 4); the diff is logged in STATE.md either way |

**Never pre-authorizable:** the Phase 5 deletion list. Deletion always requires
explicit confirmation of the enumerated list — that is one of the two designed
stop points.
