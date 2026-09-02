#!/usr/bin/env bash
# scaffold.sh — deterministic repo bones for a new project.
#
# Two phases, deliberately separated:
#   init     lays down directories, ignore rules, hooks, licence and DOC STUBS, then `git init`.
#   publish  refuses to run while stubs are unfilled, scans for secrets, makes the first
#            commit and creates + pushes the GitHub repo.
#
# The gap between them is where Claude conducts the interview and writes README.md,
# CLAUDE.md, SPEC.md and KICKOFF.md. That ordering is the whole point: a repo whose
# CLAUDE.md is an empty template is worse than no CLAUDE.md, because everyone learns
# to ignore it.
set -euo pipefail

VERSION="1.0.0"
MARKER="<!-- SCAFFOLD-TODO -->"
DEFAULT_ROOT="${GFM_PROJECT_ROOT:-$HOME/work/GitHub}"
DOCS=(README.md CLAUDE.md SPEC.md KICKOFF.md)

die()  { printf '\033[31merror:\033[0m %s\n' "$*" >&2; exit 1; }
warn() { printf '\033[33mwarn:\033[0m  %s\n' "$*" >&2; }
info() { printf '  %s\n' "$*"; }
ok()   { printf '\033[32m✓\033[0m %s\n' "$*"; }
hdr()  { printf '\n\033[1m%s\033[0m\n' "$*"; }

usage() {
  cat <<'USAGE'
scaffold.sh — repo bones for a new project

  scaffold.sh init --name <slug> --type <infra|homelab|python|site> [options]
      --dir <path>        parent directory      (default: $GFM_PROJECT_ROOT or ~/work/GitHub)
      --desc "<text>"     one-line description  (used in README + repo description)
      --license <mit|apache2|none>              (default: mit)
      --no-git            skip `git init` (for testing)

  scaffold.sh publish [--path <repo>] [options]
      --public            create the repo public (default: private)
      --no-scan           proceed without gitleaks (records why in the commit trailer)
      --dry-run           print the git/gh commands instead of running them

  scaffold.sh doctor      check prerequisites
  scaffold.sh version
USAGE
}

# ---------------------------------------------------------------- helpers

need() { command -v "$1" >/dev/null 2>&1; }

valid_slug() { [[ "$1" =~ ^[a-z0-9]([a-z0-9-]*[a-z0-9])?$ ]]; }

# Package name for python: slug with hyphens -> underscores.
pkg_name() { echo "${1//-/_}"; }

write() { # write <path> ; body on stdin
  mkdir -p "$(dirname "$1")"
  cat > "$1"
  info "$1"
}

keep() { mkdir -p "$1"; : > "$1/.gitkeep"; info "$1/"; }

# ---------------------------------------------------------------- doctor

cmd_doctor() {
  hdr "prerequisites"
  local fail=0
  for c in git gh; do
    if need "$c"; then ok "$c  $(command -v "$c")"; else printf '\033[31m✗\033[0m %s  MISSING (required)\n' "$c"; fail=1; fi
  done
  for c in gitleaks pre-commit; do
    if need "$c"; then ok "$c  $(command -v "$c")"
    else warn "$c missing — install it (brew install $c). publish will refuse to push without gitleaks unless you pass --no-scan."; fi
  done
  if need gh; then
    if gh auth status >/dev/null 2>&1; then ok "gh authenticated as $(gh api user --jq .login 2>/dev/null || echo '?')"
    else printf '\033[31m✗\033[0m gh not authenticated — run: gh auth login\n'; fail=1; fi
  fi
  hdr "project root"
  if [[ -d "$DEFAULT_ROOT" ]]; then ok "$DEFAULT_ROOT"; else warn "$DEFAULT_ROOT does not exist yet (init will create it)"; fi
  [[ $fail -eq 0 ]] || die "fix the items marked ✗ before running init"
}

# ---------------------------------------------------------------- ignore files

gitignore_base() {
  cat <<'EOF'
# --- OS / editor ---------------------------------------------------------
.DS_Store
Thumbs.db
.vscode/
.idea/
*.swp

# --- Secrets -------------------------------------------------------------
# Nothing here should ever hold a credential. Secrets live in the password
# manager and are injected at runtime (`op run -- ...`). These patterns are a
# backstop, not the control.
.env
.env.*
!.env.example
.envrc
*.pem
*.key
*.p12
id_rsa*
credentials
credentials.json

# --- Scratch -------------------------------------------------------------
*.tar.gz
_scratch/
.scaffold
EOF
}

gitignore_for() {
  case "$1" in
    infra) cat <<'EOF'

# --- Terraform -----------------------------------------------------------
.terraform/
*.tfstate
*.tfstate.*
.terraform.tfstate.lock.info
crash.log
crash.*.log
override.tf
override_*.tf
# tfvars can carry account IDs, CIDRs and occasionally worse. Commit the
# .example, never the real one. Note: .terraform.lock.hcl IS committed on
# purpose — it pins provider hashes.
*.tfvars
!*.tfvars.example
EOF
;;
    python) cat <<'EOF'

# --- Python --------------------------------------------------------------
__pycache__/
*.py[cod]
*.egg-info/
.venv/
venv/
build/
dist/

# --- Tooling caches ------------------------------------------------------
.pytest_cache/
.ruff_cache/
.mypy_cache/
.ipynb_checkpoints/

# --- Data ----------------------------------------------------------------
# Raw pulls and derived artefacts are reproducible from the pipeline; keeping
# them out of git keeps the repo cloneable and avoids committing anything the
# upstream source considers private. Note `data/*` not `data/` — git cannot
# re-include a file whose parent directory is excluded, so the directory itself
# has to stay visible for the .gitkeep negation to work.
data/*
!data/.gitkeep
EOF
;;
    site) cat <<'EOF'

# --- Build ---------------------------------------------------------------
node_modules/
__pycache__/
*.py[cod]
shots/

# --- Source data ---------------------------------------------------------
# Generated pages are committed (that's what gets served); the raw exports
# they are built from are not — exports routinely carry more fields than the
# published product does.
data/*.csv
data/raw/
EOF
;;
    homelab) cat <<'EOF'

# --- Runtime state -------------------------------------------------------
volumes/
data/
config/secrets/
backup/*
!backup/.gitkeep
*.env
!.env.example
EOF
;;
  esac
}

# ---------------------------------------------------------------- doc stubs

stub_readme() { # $1 name $2 desc $3 type
  cat <<EOF
# $1

$2

$MARKER Replace everything below with the real thing. This is the human front
door: what it is, how to run it, and what state it is in. Keep it short — depth
belongs in SPEC.md.

## What this is

## Running it

## State

EOF
}

stub_claude() { # $1 name $2 type
  local rules
  case "$2" in
    infra)   rules=$'8. **Plan before apply, always.** Never `terraform apply` without showing me the plan\n   first. Never `-auto-approve` outside CI. Destroy operations need explicit sign-off.\n9. **State is not in git.** Backend config lives in `envs/<env>/backend.tf`; `*.tfvars` are\n   local. If you find state or tfvars staged, stop and tell me.' ;;
    python)  rules=$'8. **Pin exactly, upgrade deliberately.** Dependencies use `==`, not `>=`. Bumping a pin is\n   its own change with its own test run.\n9. **Every fetcher gets a `--check` mode** that hits the source, prints what it found, and\n   writes nothing. It is how I sanity-check the upstream before a real run.' ;;
    site)    rules=$'8. **Edit templates, never generated output.** `scripts/templates/*` -> build script -> the\n   published files. Hand edits to generated output get overwritten.\n9. **Do not read large generated files.** They are mostly inlined data you can query in two\n   lines of Python. Read the template instead.' ;;
    homelab) rules=$'8. **`compose.yml` is the source of truth for the host.** No changes made by hand on the box\n   that are not reflected here. If they diverge, the file wins and we re-apply.\n9. **Every service documents its restore path** in `docs/runbook.md`. A backup nobody has\n   restored from is not a backup.' ;;
  esac
  cat <<EOF
# $1

Auto-loaded context for Claude Code. **\`SPEC.md\` is the single source of truth** for
decisions, data model and verification. Read it before writing code.

## What this is

$MARKER One paragraph. What the thing is, who it is for, and the one sentence
of context a newcomer needs that is not obvious from the name.

## State

$MARKER What exists, what works, what is half-built. Name the files that matter
and say which are generated. Keep this current — a stale State section is the
fastest way to make an agent do the wrong thing confidently.

## Hard rules

1. **No credentials, ever.** Secrets live in the password manager and are injected at
   runtime via \`op run\`. Assume CLI-native auth already exists. If a task seems to need a
   raw credential, stop and say so rather than inventing a workaround.
2. **Show evidence.** Command output, diffs, screenshots, test results. Assertions of
   success are not success. If verification was skipped, say which step and why.
3. **Push back.** If a direction looks wrong, say so before building it. I want a
   colleague, not an order-taker.
4. **Bottom line first.** Lead with the answer, then the reasoning.
5. **Ask before irreversible or expensive.** Deletes, force-pushes, anything that spends
   money or touches production. Low-stakes work: just do it.
6. **Do not relax an assertion to make a change pass.** If a check fails, either the change
   is wrong or the check is — decide which, out loud.
7. **Counts and versions in docs are dated snapshots.** Verify against the live thing rather
   than trusting a number written here.
$rules

$MARKER Add the rules specific to this project — the things you would have to
tell a competent stranger to stop them breaking something on day one.
EOF
}

stub_spec() { # $1 name
  cat <<EOF
# $1 — spec

Single source of truth. When this file and any other doc disagree, this one wins;
fix the other. When reality and this file disagree, fix this file.

$MARKER Fill in every section. Sections that genuinely have no answer yet get
\`TBD (<what would settle it>)\` — an explicit unknown is useful, a blank is not.

## 1. Problem

What is broken or missing, and who feels it.

## 2. Decisions

The choices already made and why, so they are not relitigated every session.
One line each, with the reason.

| # | Decision | Why | Date |
|---|----------|-----|------|
| 1 |          |     |      |

## 3. Scope

**In:**

**Out (deliberately):** — with the reason, so it can be revisited on purpose

## 4. Design

Data model, interfaces, the shape of the thing.

## 5. Dependencies and access

What it talks to. Which auth each needs, and where that auth comes from
(never the credential itself).

## 6. Verification

How we know it works. The concrete commands, and what their output should look
like. This section is what the agent runs before claiming done.

## 7. Open questions

What would settle each one.
EOF
}

stub_kickoff() { # $1 name
  cat <<EOF
# Claude Code kickoff — $1

Paste the block below into a fresh Claude Code session opened in this repo.
\`CLAUDE.md\` is auto-loaded and points at \`SPEC.md\`.

$MARKER Write the real prompt. A good one names the goal, the order of work, the
guardrails, and what evidence to show at each step — and tells Claude to stop and
show you the result between steps rather than running to the end.

**Before you paste it**, run the checks in SPEC.md §6 so you know the starting state
is what the docs claim.

---

<the prompt goes here>

---

Notes for me (not part of the prompt):

-
EOF
}

# ---------------------------------------------------------------- archetypes

lay_infra() { # $1 root
  local r="$1"
  keep "$r/modules"
  for e in dev prod; do
    mkdir -p "$r/envs/$e"
    write "$r/envs/$e/main.tf" <<EOF
# $e environment. Composes modules from ../../modules — resources are not
# declared directly here, so that dev and prod stay structurally identical and
# differ only in tfvars.
EOF
    write "$r/envs/$e/variables.tf" <<'EOF'
variable "region" {
  description = "AWS region"
  type        = string
}
EOF
    write "$r/envs/$e/outputs.tf" <<'EOF'
EOF
    write "$r/envs/$e/backend.tf.example" <<EOF
# Copy to backend.tf and fill in. Kept as an example because bucket/table names
# are account-specific; the real file is gitignored along with tfvars.
terraform {
  backend "s3" {
    bucket       = "<state-bucket>"
    key          = "$e/terraform.tfstate"
    region       = "<region>"
    use_lockfile = true
  }
}
EOF
    write "$r/envs/$e/terraform.tfvars.example" <<'EOF'
region = "us-east-1"
EOF
  done
  write "$r/versions.tf" <<'EOF'
terraform {
  required_version = ">= 1.9"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}
EOF
  write "$r/.github/workflows/terraform.yml" <<'EOF'
name: terraform
on: [push, pull_request]
permissions:
  contents: read
jobs:
  check:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        env: [dev, prod]
    steps:
      - uses: actions/checkout@v4
      - uses: hashicorp/setup-terraform@v3
      - run: terraform fmt -check -recursive
      - name: init (no backend — validate only)
        run: terraform -chdir=envs/${{ matrix.env }} init -backend=false
      - run: terraform -chdir=envs/${{ matrix.env }} validate
EOF
}

lay_python() { # $1 root $2 name $3 desc
  local r="$1" pkg; pkg="$(pkg_name "$2")"
  mkdir -p "$r/$pkg" "$r/tests"
  write "$r/$pkg/__init__.py" <<'EOF'
EOF
  write "$r/tests/test_smoke.py" <<EOF
"""Smoke test. Exists so \`pytest\` is green from the first commit — a test suite
that has never passed gives you no signal when it later fails."""


def test_imports() -> None:
    import $pkg  # noqa: F401
EOF
  write "$r/pyproject.toml" <<EOF
[project]
name = "$2"
version = "0.1.0"
description = "$3"
requires-python = ">=3.12"

# Pin exactly, not floored. A floored pin means a dependency can change under
# you between two runs of the same commit; upgrading is then its own change with
# its own test run.
dependencies = []

[project.optional-dependencies]
dev = [
    "pytest==8.3.4",
    "ruff==0.9.4",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["$pkg"]

[tool.ruff]
line-length = 100
target-version = "py312"

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B", "SIM", "ANN"]

[tool.ruff.lint.per-file-ignores]
"tests/*" = ["ANN"]

[tool.pytest.ini_options]
testpaths = ["tests"]
markers = [
    "network: hits an external endpoint; skipped by default, run with -m network",
]
addopts = "-m 'not network'"
EOF
  keep "$r/data"
  write "$r/.env.example" <<'EOF'
# Copy to .env for local runs. Real values come from the password manager:
#   op run --env-file=.env -- python -m <pkg>
# Never paste a real value into this file.
EXAMPLE_API_BASE=https://api.example.com
EOF
  write "$r/.github/workflows/ci.yml" <<'EOF'
name: ci
on: [push, pull_request]
permissions:
  contents: read
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v5
      - run: uv pip install --system -e ".[dev]"
      - run: ruff check .
      - run: ruff format --check .
      - run: pytest
EOF
}

lay_site() { # $1 root
  local r="$1"
  keep "$r/scripts/templates"
  write "$r/scripts/build.py" <<'EOF'
#!/usr/bin/env python3
"""Build the published output from scripts/templates/ + data/.

Everything served is generated by this script. Hand edits to the output are
overwritten on the next build, which is why the templates are the thing you edit.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATES = ROOT / "scripts" / "templates"
DATA = ROOT / "data"


def main() -> None:
    raise SystemExit("not implemented yet — see SPEC.md §4")


if __name__ == "__main__":
    main()
EOF
  chmod +x "$r/scripts/build.py"
  keep "$r/data"
  write "$r/.github/workflows/pages.yml" <<'EOF'
name: build-and-publish
on:
  schedule:
    - cron: "17 7 * * 1"   # weekly, Monday — offset off the hour to dodge the stampede
  workflow_dispatch:
  push:
    branches: [main]
    paths: ["scripts/**", "data/**"]

# Pages must be in "Deploy from a branch" mode for this to publish. A commit made
# with the default GITHUB_TOKEN does not trigger other workflows, so an
# Actions-based Pages deploy would never fire from this job.
permissions:
  contents: write

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: python scripts/build.py
      - name: commit if changed
        run: |
          git config user.name  "github-actions[bot]"
          git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
          git add -A
          git diff --staged --quiet || git commit -m "chore: rebuild $(date -u +%F)"
          git push
EOF
}

lay_homelab() { # $1 root $2 name
  local r="$1"
  write "$r/compose.yml" <<EOF
# Source of truth for this host. Nothing gets changed by hand on the box that is
# not reflected here — when they diverge, this file wins and we re-apply.
services:
  $2:
    image: <image>:<pinned-tag>   # pin the tag; :latest makes rollback guesswork
    container_name: $2
    restart: unless-stopped
    env_file: .env
    ports: []
    volumes:
      - ./config:/config
EOF
  write "$r/.env.example" <<'EOF'
# Copy to .env on the host. Real values come from the password manager —
# `op inject -i .env.example -o .env` if you want it scripted.
TZ=America/New_York
PUID=1000
PGID=1000
EOF
  keep "$r/config"
  keep "$r/backup"
  write "$r/docs/runbook.md" <<EOF
# $2 — runbook

## Where it runs

Host, ports, reverse-proxy entry, DNS name.

## Start / stop

\`\`\`bash
docker compose up -d
docker compose logs -f $2
\`\`\`

## Backup

What is backed up, where to, how often.

## Restore

The actual steps, and the date they were last **tested end to end**. A backup
nobody has restored from is not a backup — put the date here and keep it honest.

Last tested: never
EOF
}

# ---------------------------------------------------------------- init

cmd_init() {
  local name="" type="" dir="$DEFAULT_ROOT" desc="" lic="mit" no_git=0
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --name) name="${2:-}"; shift 2 ;;
      --type) type="${2:-}"; shift 2 ;;
      --dir) dir="${2:-}"; shift 2 ;;
      --desc) desc="${2:-}"; shift 2 ;;
      --license) lic="${2:-}"; shift 2 ;;
      --no-git) no_git=1; shift ;;
      -h|--help) usage; exit 0 ;;
      *) die "unknown option: $1" ;;
    esac
  done

  [[ -n "$name" ]] || die "--name is required"
  valid_slug "$name" || die "--name must be a lowercase slug (a-z, 0-9, hyphens): got '$name'"
  case "$type" in infra|homelab|python|site) ;; *) die "--type must be one of: infra homelab python site" ;; esac
  case "$lic" in mit|apache2|none) ;; *) die "--license must be mit, apache2 or none" ;; esac
  [[ -n "$desc" ]] || desc="TBD — one line on what $name does."

  local root="$dir/$name"
  [[ ! -e "$root" ]] || die "$root already exists — pick another name or remove it first"

  hdr "scaffolding $name ($type) in $root"
  mkdir -p "$root"
  keep "$root/docs"
  keep "$root/_archive"

  { gitignore_base; gitignore_for "$type"; } > "$root/.gitignore"; info "$root/.gitignore"

  write "$root/.pre-commit-config.yaml" <<'EOF'
# Installed by scaffold.sh. gitleaks runs on every commit so a credential never
# reaches history in the first place — purging one after the fact means a
# rewrite, a force-push, and rotating the secret anyway.
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.24.0
    hooks:
      - id: gitleaks
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: check-merge-conflict
      - id: check-added-large-files
        args: ["--maxkb=5000"]
      - id: end-of-file-fixer
      - id: trailing-whitespace
EOF

  case "$lic" in
    mit) write "$root/LICENSE" <<EOF
MIT License

Copyright (c) $(date +%Y) Graham

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
EOF
;;
    apache2) write "$root/LICENSE" <<EOF
Apache License 2.0 — Copyright $(date +%Y) Graham

Full text: https://www.apache.org/licenses/LICENSE-2.0
Replace this stub with the full text before making the repo public.
EOF
;;
  esac

  stub_readme  "$name" "$desc" "$type" > "$root/README.md";  info "$root/README.md"
  stub_claude  "$name" "$type"         > "$root/CLAUDE.md";  info "$root/CLAUDE.md"
  stub_spec    "$name"                 > "$root/SPEC.md";    info "$root/SPEC.md"
  stub_kickoff "$name"                 > "$root/KICKOFF.md"; info "$root/KICKOFF.md"

  case "$type" in
    infra)   lay_infra   "$root" ;;
    python)  lay_python  "$root" "$name" "$desc" ;;
    site)    lay_site    "$root" ;;
    homelab) lay_homelab "$root" "$name" ;;
  esac

  printf 'name=%s\ntype=%s\ndesc=%s\ncreated=%s\nscaffold_version=%s\n' \
    "$name" "$type" "$desc" "$(date -u +%FT%TZ)" "$VERSION" > "$root/.scaffold"

  if (( ! no_git )); then
    if need git; then
      git -C "$root" init -q -b main 2>/dev/null || { git -C "$root" init -q && git -C "$root" checkout -q -b main; }
      ok "git repo initialised on main"
      if need pre-commit; then
        (cd "$root" && pre-commit install >/dev/null 2>&1) && ok "pre-commit hook installed" \
          || warn "pre-commit install failed — run it yourself in $root"
      else
        warn "pre-commit not installed — hooks are configured but inert. brew install pre-commit"
      fi
    else
      warn "git not found — skipping init"
    fi
  fi

  hdr "next"
  info "Docs are stubs. Claude fills README.md, CLAUDE.md, SPEC.md and KICKOFF.md next."
  info "Then: scaffold.sh publish --path $root"
  echo "$root"
}

# ---------------------------------------------------------------- publish

cmd_publish() {
  local path="." public=0 no_scan=0 dry=0
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --path) path="${2:-}"; shift 2 ;;
      --public) public=1; shift ;;
      --no-scan) no_scan=1; shift ;;
      --dry-run) dry=1; shift ;;
      -h|--help) usage; exit 0 ;;
      *) die "unknown option: $1" ;;
    esac
  done

  path="$(cd "$path" 2>/dev/null && pwd)" || die "no such directory: $path"
  [[ -d "$path/.git" ]] || die "$path is not a git repo — run init first"

  local name type desc
  name="$(basename "$path")"; type="unknown"; desc=""
  if [[ -f "$path/.scaffold" ]]; then
    # shellcheck disable=SC1090
    name="$(sed -n 's/^name=//p'  "$path/.scaffold")"
    type="$(sed -n 's/^type=//p'  "$path/.scaffold")"
    desc="$(sed -n 's/^desc=//p'  "$path/.scaffold")"
  fi

  hdr "pre-flight for $name"

  # 1. Stubs must be filled. This is the gate that makes the whole two-phase
  #    design worth having.
  local unfilled=()
  for d in "${DOCS[@]}"; do
    [[ -f "$path/$d" ]] || { unfilled+=("$d (missing)"); continue; }
    grep -qF "$MARKER" "$path/$d" && unfilled+=("$d")
  done
  if (( ${#unfilled[@]} )); then
    printf '\033[31m✗\033[0m these docs still contain scaffold placeholders:\n' >&2
    printf '    %s\n' "${unfilled[@]}" >&2
    die "fill them in (or delete the '$MARKER' lines if a section genuinely does not apply), then re-run"
  fi
  ok "all four docs filled in"

  # 2. Nothing that looks like a live secret.
  if [[ -f "$path/.env" ]]; then
    git -C "$path" check-ignore -q .env || die ".env exists and is NOT gitignored — stop"
    ok ".env present but ignored"
  fi
  if need gitleaks; then
    if gitleaks detect --source "$path" --no-git --redact --exit-code 1 >/dev/null 2>&1; then
      ok "gitleaks: clean"
    else
      printf '\033[31m✗\033[0m gitleaks found something. Re-run for detail:\n' >&2
      printf '    gitleaks detect --source %q --no-git --redact -v\n' "$path" >&2
      die "refusing to publish"
    fi
  elif (( no_scan )); then
    warn "gitleaks not installed and --no-scan given — publishing UNSCANNED"
  else
    die "gitleaks not installed. brew install gitleaks — or pass --no-scan to publish unscanned."
  fi

  # 3. gh ready. Under --dry-run this is a warning, not a stop, so the gate logic
  #    above can be rehearsed on a machine without gh.
  if need gh && gh auth status >/dev/null 2>&1; then
    ok "gh authenticated"
  elif (( dry )); then
    warn "gh missing or unauthenticated — fine for a dry run, not for a real publish"
  else
    need gh || die "gh not installed (brew install gh)"
    die "gh not authenticated — run: gh auth login"
  fi

  git -C "$path" remote get-url origin >/dev/null 2>&1 && \
    die "origin already exists ($(git -C "$path" remote get-url origin)) — nothing to do"

  local vis="--private"; (( public )) && vis="--public"
  hdr "publishing ($([[ $vis == --private ]] && echo private || echo PUBLIC))"

  local msg="chore: scaffold $name ($type)

Structure, ignore rules, hooks and the four project docs. No implementation yet —
this commit is the clean baseline every later diff is read against."
  (( no_scan )) && msg="$msg

Note: published without a gitleaks scan (--no-scan)."

  if (( dry )); then
    info "[dry-run] git -C $path add -A"
    info "[dry-run] git -C $path commit -m '<scaffold message>'"
    info "[dry-run] gh repo create $name $vis --source=$path --push --description \"$desc\""
    ok "dry run complete — nothing was created"
    return 0
  fi

  git -C "$path" add -A
  git -C "$path" commit -q -m "$msg"
  ok "first commit: $(git -C "$path" rev-parse --short HEAD)"

  gh repo create "$name" $vis --source="$path" --push --description "$desc"
  ok "pushed → $(gh repo view "$name" --json url --jq .url 2>/dev/null || echo "$name")"

  if [[ "$type" == "site" ]]; then
    hdr "site archetype — Pages settings that fail silently if wrong"
    info "1. repo must be public (free tier)"
    info "2. Pages source = 'Deploy from a branch'"
    info "3. Actions workflow permissions = read AND write"
    info "   Wrong on #3 and the weekly job runs green, commits nothing, and the site quietly stops updating."
  fi
}

# ---------------------------------------------------------------- main

case "${1:-}" in
  init)    shift; cmd_init "$@" ;;
  publish) shift; cmd_publish "$@" ;;
  doctor)  shift; cmd_doctor "$@" ;;
  version) echo "scaffold.sh $VERSION" ;;
  -h|--help|"") usage ;;
  *) die "unknown command: $1 (try --help)" ;;
esac
