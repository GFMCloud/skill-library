---
type: regex
pattern: "0\\.9\\.3"
match: contains
---

Tests Step 1, "Name the ground truth", `SKILL.md:19-24`: the authority is the running
system or the artifact on disk, and "Nothing else. A second document is another claim."
`RELEASE-NOTES.md` is a second document asserting that 2.4.0 is correct. The only
artifact is `pyproject.toml`, which says 0.9.3. Decidable because 0.9.3 appears nowhere
except in the artifact: a run that took the release notes as the authority reports the
README as clean and never emits that string.
