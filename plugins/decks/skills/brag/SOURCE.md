# Source

Taken from `latent-spaces/brag` 0.4.0, at commit `cb89b9f` (pushed 2026-10-01). MIT,
Copyright (c) 2026 Shunit Haviv Hakimi; the licence text is `LICENSE` in this directory.

Every other file here is the upstream `skills/brag/` directory unchanged (`LICENSE` is
copied from the upstream repo root, and this file was written for this library), with
two local changes to `SKILL.md`:

- The frontmatter gained `license`, the `metadata` block, and a description tail with
  its negative scope and cost.
- The four contract sections (`Inputs`, `Verify`, `Done when`, `Stop when`) were added
  at the end.

`slim.md` is upstream's bundled copy of `brag-slim`. It is unchanged, so it does not
carry the local additions made to `../brag-slim/SKILL.md`. On Opus 5.5, `/brag` reads
`slim.md` and follows it.

## Bundled media licences

Checked against each source page on 2026-10-02.

| Files | Source | Licence |
| :--- | :--- | :--- |
| `assets/music/*.mp3` | ende.app "Happy Beats / Business Moves" | CC BY 4.0 (https://ende.app/en/standard-license): "Everything is under CC BY 4.0." Credit: music by ende.app. |
| `assets/sfx/{casino,impact,interface,ui}/` | Kenney (https://kenney.nl) | CC0 (https://kenney.nl/support) |
| `assets/sfx/keyboard/` | Keyboard Soundpack #1 by unicaegames, opengameart.org | CC0 |

Upstream's `assets/music/README.md` still says the music licence must be verified
before redistribution. The table above is that verification.

## Dependencies outside this directory

- The Hyperframes CLI (`npx hyperframes`, Apache-2.0, HeyGen). It sends anonymous usage
  data by default; `npx hyperframes telemetry disable` turns that off.
- The `hyperframes` plugin from the `claude-plugins-official` marketplace, for the
  `hyperframes-*` skills that Step 3 reads.
- `scripts/` holds upstream's music cue analyser (Python 3.11+, run with `uv`). Normal
  runs read the shipped cue presets and do not need it.

Review record: none yet (incubator).

To update: compare against a newer upstream commit, carry the two local changes across,
and change the commit above and the `metadata.upstream` line in `SKILL.md`.
