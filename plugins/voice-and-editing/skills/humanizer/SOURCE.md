# Source

Taken from `blader/humanizer` 3.0.0, at commit
`9862685f575c65a8247f90369951df1b3416e3d6`. MIT, Copyright (c) 2025 Siqi Chen; the
licence text is `LICENSE` in this directory.

`SKILL.md` is the upstream text with these local changes, which its own closing section
also lists: file mode stops for a yes before it overwrites, embedded mode is stated to
never write, the four contract sections were added, and the description gained its
negative scope and cost. Everything else is as the upstream author wrote it. That
includes the rule that names the em dash and the en dash, and the Before examples that
show them: they are the patterns the skill removes, so they stay. Text added locally
uses no em dashes.

`README.md` in this directory was written for this library and is not upstream text.

Review record: `maintainers/reviews/2026-09-18-humanizer.md` in the library.

To update: compare against a newer upstream release, carry the local changes across, and
change the version and commit above and the `metadata.upstream` line in `SKILL.md`.
