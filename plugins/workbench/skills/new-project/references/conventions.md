# Repo conventions

These are derived from what already works in Graham's repos, not invented. Two things
were inconsistent across them and are now settled here: the spec document was called
`BUILD_SPEC.md` in one repo and `DESIGN.md` in another, and the kickoff prompt was
`KICKOFF.md` in one and `KICKOFF_PROMPT.md` in another. Fixed names are `SPEC.md` and
`KICKOFF.md`. Existing repos do not need renaming; new ones use these.

## The four documents

Four files, all at the repo root. Root matters for `CLAUDE.md` (that is where Claude Code
auto-loads it from) and is worth keeping for the others so the whole picture is visible
in one `ls`.

The division is by **audience**, and the failure mode when it blurs is duplication that
drifts into contradiction. Two docs that disagree are worse than one doc that is
incomplete, because now nobody knows which to trust.

### README.md — for a human who just landed

What it is, how to run it, what state it is in. Short. If you are writing a fifth
paragraph, the content belongs in `SPEC.md` and the README should link to it.

Not: rationale, alternatives considered, data models, decision history.

### CLAUDE.md — auto-loaded agent context

Three sections, in this order:

1. **What this is** — one paragraph, including the non-obvious context. Name the thing
   an agent would otherwise get subtly wrong.
2. **State** — what exists, what works, what is half-built, and which files are
   *generated*. This is the section that goes stale fastest and does the most damage
   when it does: a stale State section makes an agent confidently rebuild something that
   already works, or build against a superseded prototype.
3. **Hard rules** — numbered, imperative, each with the reason attached. The reason is
   what makes a rule survive contact with a situation its author did not foresee.

`CLAUDE.md` should **point at `SPEC.md`, not restate it**. One sentence: "SPEC.md is the
single source of truth for decisions, data model and verification — read it before
writing code."

A good hard rule names the failure it prevents:

> **Edit templates, never generated HTML.** `scripts/templates/*.html` → `build_pages.py`
> → `index.html`. Hand edits to the output are overwritten.

A bad one is a vibe: "write clean code", "follow best practices". It cannot be violated
in a way anyone would notice, so it is noise crowding out the rules that can.

### SPEC.md — the arbiter

The single source of truth. When another doc disagrees with it, this one wins and the
other gets fixed. When *reality* disagrees with it, this file gets fixed.

Sections are in the stub. Two are load-bearing:

- **§2 Decisions** — the choices already made, with reasons and dates. Without this the
  same debate reopens every session and gets resolved differently each time.
- **§6 Verification** — the actual commands, and what their output should look like. This
  is what an agent runs before claiming done. A spec without it reliably produces
  confident false completion claims, because "done" has no definition. For a bug fix
  the verification is the reproducing test: written first, seen to fail for the expected
  reason, committed before the fix, and left untouched by the fix commit.

Specs accrete. A 40 KB `SPEC.md` on a mature project is healthy; a 40 KB one on day zero
is fiction. On day zero it is mostly `TBD (<what would settle it>)`, and that is correct.

### KICKOFF.md — the prompt to paste

The block the user pastes into a fresh Claude Code session. A good one:

- names the goal and the order of work,
- says **show me the result at each step before moving on** — this is what keeps a long
  session steerable,
- lists the guardrails and what evidence to produce,
- and ends with "push back if any step looks wrong."

Keep a `Notes for me (not part of the prompt)` section below the block for things the
user needs but Claude should not be told — parked ideas, knobs worth tuning later,
what changes if a hosting decision changes.

## Structure

| Path | Purpose |
|---|---|
| `docs/` | investigations, runbooks, anything long-form that is not the spec |
| `_archive/` | superseded prototypes kept for reference, explicitly not part of the product |
| `.github/workflows/` | CI |

`_archive/` earns its place: the alternative is deleting a prototype and losing the
reference, or leaving it in place where an agent builds against it by mistake. Naming it
`_archive` and saying "not part of the product" in `CLAUDE.md` State closes that hole.

## Secrets

Nothing in any repo holds a credential. Secrets live in the password manager and are
injected at runtime (`op run -- ...`). `.gitignore` patterns and the gitleaks hook are a
backstop, not the control — the control is that credentials are never written down.

The hook runs at commit time rather than at push time on purpose. Once a secret is in a
commit, removing it means rewriting history, force-pushing, and rotating the secret
anyway; catching it before the commit costs nothing.

## Naming

- Repo, directory and GitHub repo name all match, lowercase slug: `beetlewood-north-atlas`.
- Python package name is the slug with underscores: `beetlewood_north_atlas`.
- Repos live under `~/work/GitHub/` (override with `$GFM_PROJECT_ROOT`).
- Default visibility is private. Public is a deliberate choice made at publish time —
  and if it is public, re-read `.gitignore` first, because public plus a data export is
  how private coordinates end up on the internet.
