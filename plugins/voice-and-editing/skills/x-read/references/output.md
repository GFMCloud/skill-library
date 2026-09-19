# x-read output contract (v1)

## Markdown (default)

Single post or Article:

```
# <Article title, or "@handle on X">

**@handle** (Display Name) · YYYY-MM-DD · https://x.com/handle/status/<id>
<likes> likes · <reposts> reposts · <replies> replies
Type: X Article (<n> chars of body)        <- only for Articles

<full body text>

> **Quoting:** ...                          <- only when the post quotes another
- photo: https://pbs.twimg.com/...          <- only when media is attached
```

`thread` and `search` print `# <header>` then one `## N. @handle · date` block per post,
each block in the single-post shape without the title line. Threads are oldest first.
Search returns X's "Latest" product for the query, so X search operators work
(`from:handle`, `since:YYYY-MM-DD`, `"exact phrase"`, `OR`, `-word`).

## JSON (`--json`)

The tweet object from the vendored bird client, unchanged. One object for a read,
an array for `thread` and `search`. Fields:

| field | meaning |
|---|---|
| `id` | post id (snowflake) |
| `text` | full text. For an Article: `title\n\nbody`, with body pulled via TweetDetail rich content, falling back to the author's `UserArticlesTweets` plain text |
| `createdAt` | X's `created_at` string |
| `likeCount`, `retweetCount`, `replyCount` | engagement at fetch time |
| `conversationId`, `inReplyToStatusId` | thread linkage |
| `author.username`, `author.name`, `authorId` | author |
| `article` | `{ title, previewText }` when the post carries an Article, else absent |
| `quotedTweet` | nested object, one level deep |
| `media` | `[{ type, url, width?, height? }]` when present |

Field additions are non-breaking. Renames or removals bump the major version here.
