Absolute-limits block v1, every line present, as defined in the harness interface
spec (`/Users/gfm/work/toolkit-build-harness/docs/interface-spec.md`, section 7). This
file is a rendering fragment, not a second definition: the wording below is copied
verbatim from the spec so `scripts/render-pointer.py` has something to substitute into,
and `scripts/check-pointer.py` checks a rendered pointer against this same wording. If
the spec's wording changes, this file is updated in the same change; it never drifts
into its own phrasing.

The two lines marked `{{hook_timeout}}` and `{{retry_cap}}` take numeric values at
render time. Every other line is fixed text.

```text
- no git push
- no deletion (rename to .superseded)
- no credentials
- no edits under ~/.claude/plugins/
- no edits to the harness's own CONFIG.md, CLAUDE.md, or prompts/
- no edits in a repo with uncommitted changes this run did not make
- hook timeout: {{hook_timeout}}
- consecutive-retry cap on a failed or rate-limited step: {{retry_cap}}
- anything the run would have asked becomes a queued Tier 3 item
```
