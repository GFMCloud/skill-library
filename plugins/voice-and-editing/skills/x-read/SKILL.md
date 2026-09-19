---
name: x-read
description: >-
  Fetch the full text of an X (Twitter) post, a long-form X Article, or a whole
  thread from a URL, or run an X search, and return it as Markdown or JSON using
  Graham's own X session cookies from the macOS keychain. Use whenever Graham pastes
  an x.com or twitter.com link and wants it read, summarized, quoted, or checked,
  or says "read this X article", "what does this tweet say", "pull this thread",
  "get the full post", or "search X for ...". Not for multi-source last-30-days
  research briefs (that is last30days), not for posting or liking, and not for
  reading browser cookie stores. Costs one or two network calls per fetch; needs a
  one-time keychain setup that only Graham can run.
metadata:
  maturity: incubator
---

# x-read

Read X posts and X Articles in full from the terminal. Search results and the
bundled clients in other tools truncate to a preview; this skill makes the
`TweetDetail` GraphQL call with the article field toggles set, so an Article comes
back as title plus its complete body.

Engine: a vendored, read-only subset of `@steipete/bird` 0.8.0 (MIT) under
`scripts/vendor/bird/`. The npm package is deprecated upstream, which is why the
code is vendored and pinned; never edit the vendored files, re-vendor instead.

## Run

All commands take a post URL (`x.com/<user>/status/<id>`, `twitter.com/...`) or a
bare post id. Paths are relative to this skill directory.

```bash
node scripts/x-read.mjs <url-or-id>            # one post or Article, Markdown
node scripts/x-read.mjs <url-or-id> --json     # raw tweet object
node scripts/x-read.mjs thread <url-or-id>     # whole conversation, oldest first
node scripts/x-read.mjs search "<query>" -n 30 # X search, Latest product, operators allowed
node scripts/x-read.mjs auth-check             # do credentials resolve, and from where
```

Output shapes and the JSON field list are in [references/output.md](references/output.md).

## Rules

- **Credentials never pass through Claude.** The script reads `AUTH_TOKEN` and `CT0`
  from the environment, else from keychain items `x-read-AUTH_TOKEN` / `x-read-CT0`
  (falling back to `last30days-*` if those exist). Exit code 3 means none resolved.
  Then stop and hand Graham this to run in his own terminal, do not ask him to paste
  cookie values into chat:

  ```bash
  bash "<absolute path to this skill>/scripts/x-read-auth.sh"
  ```

  It prompts with hidden input and stores both items in the login keychain.
  `--status` lists what is set, `--delete` clears it. Cookies die when he signs out of
  x.com; a run that starts returning HTTP 401 or 403 means re-run the auth script.
- **An `x.com/i/article/<id>` URL is not a post id.** The script refuses it; ask for
  the post URL that carries the Article (the author's `status/<id>` link).
- **Quote from the fetched text, not from memory.** If the body is short and the post
  has `article.title`, the fallback also failed; say so rather than summarizing the
  preview as if it were the article.
- **Search is literal.** X search matches words, not meaning. Prefer short queries,
  quoted phrases, `from:` and `since:` operators; retry narrower before retrying wider.
  To find Article posts, search `"x.com/i/article" <topic>`; `filter:article` is not
  an accepted operator. Search hits carry only an Article's title and preview, so
  follow up with a read on the post URL for the body.
- Exit codes: 0 ok, 1 fetch failed (message on stderr), 2 usage, 3 no credentials.

## When the user wants more than a read

- A dated, multi-source research brief across Reddit, X, HN, and the web: that is
  `last30days`, not this skill.
- Posting, liking, bookmarking: out of scope on purpose; the vendored subset has no
  write endpoints.
