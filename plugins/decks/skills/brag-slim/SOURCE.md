# Source

Taken from `latent-spaces/brag` 0.4.0, at commit `cb89b9f` (pushed 2026-10-01). MIT,
Copyright (c) 2026 Shunit Haviv Hakimi; the licence text is `LICENSE` in this directory.

`SKILL.md` is the upstream `skills/brag-slim/SKILL.md` with three local changes: the
frontmatter gained `license`, the `metadata` block and a description tail with its
negative scope and cost; the four contract sections were added at the end; and the
upstream description's closing clause "it hands off here on Opus 5.5" was dropped,
because this library's `/brag` no longer hands off (Graham, 2026-10-02).

Upstream also bundles a copy of this file inside `/brag` as `slim.md`; this library
removed it with the handoff, so this directory is the only copy.

This skill ships no media and no code. It builds the video with whatever is on the
machine (Node, FFmpeg, a headless Chrome).

To update: compare against a newer upstream commit, carry the local changes listed above across,
and change the commit above and the `metadata.upstream` line in `SKILL.md`.
