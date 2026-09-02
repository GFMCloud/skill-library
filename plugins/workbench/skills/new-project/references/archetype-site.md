# Archetype: site (static / generated)

Layout: `scripts/templates/` → `scripts/build.py` → published output. `data/` holds the
inputs. The generated output **is** committed — that is what gets served — while the raw
exports it is built from are not.

## What SPEC.md needs

- **§2 Decisions** — who the audience is and what they can be assumed to handle (this
  decides far more than it looks like it does), hosting, refresh cadence, and whether the
  output must work offline.
- **§4 Design** — the template → build → output chain, and which files are generated.
  Name them explicitly; it is the single most useful thing in the spec for an agent.
- **§6 Verification** — the real commands: run the build, check for console errors,
  screenshot the result. Visual output that has not been looked at is unverified,
  regardless of exit codes.

## Traps worth a hard rule

- **Hand-editing generated output.** It gets overwritten on the next build. The rule is
  "edit templates, never generated output", and it needs to be stated because the
  generated file is the one that is obviously wrong when something looks off.
- **Reading large generated files.** A self-contained page is mostly inlined data and
  vendored libraries. Opening one burns a large slice of context on a blob you can query
  in two lines of Python. Read the template instead; grep the output.
- **CDN links in something that must work offline.** If "opens by double-click, no
  network" is a requirement, assert it in the build script rather than trusting it.
- **`localStorage` / `sessionStorage`.** Not available in every context these pages get
  opened in. Keep state in memory.

## GitHub Pages settings that fail silently

Three settings produce no error when wrong, which is what makes them expensive:

1. **Repo must be public** (on the free tier).
2. **Pages source must be "Deploy from a branch"** — not "GitHub Actions". A commit made
   with the default `GITHUB_TOKEN` does not trigger other workflows, so an Actions-based
   Pages deploy would never fire from a scheduled rebuild job.
3. **Actions workflow permissions must be read *and* write.** This is the nastiest one:
   set wrong, the weekly job runs green, commits nothing, and the site quietly stops
   updating. Nothing is red. You find out weeks later.

`scaffold.sh publish` prints these after pushing a `site` repo. Put them in `KICKOFF.md`
too, as part of the deploy step's verification.
