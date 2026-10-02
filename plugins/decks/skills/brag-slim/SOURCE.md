# Source

Taken from `latent-spaces/brag` 0.4.0, at commit `cb89b9f` (pushed 2026-10-01). MIT,
Copyright (c) 2026 Shunit Haviv Hakimi; the licence text is `LICENSE` in this directory.

`SKILL.md` is the upstream `skills/brag-slim/SKILL.md` with two local changes: the
frontmatter gained `license`, the `metadata` block and a description tail with its
negative scope and cost, and the four contract sections were added at the end.

`../brag/slim.md` is upstream's copy of this file inside `/brag`, kept unchanged, so it
does not carry the local additions.

This skill ships no media and no code. It builds the video with whatever is on the
machine (Node, FFmpeg, a headless Chrome).

To update: compare against a newer upstream commit, carry the two local changes across,
and change the commit above and the `metadata.upstream` line in `SKILL.md`.
