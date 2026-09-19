# Read an X post, article or thread in full

Part of the [voice-and-editing](../../README.md) pack.

Most ways of quoting a post from X give you a preview that stops mid sentence, and a long-form X Article gives you only its title. This skill fetches the whole thing: one post, a complete article body, or a whole thread from first reply to last, and hands it back as plain text you can read, quote or summarise. It can also run an X search and return the matching posts. It reads as you, signed in, using values you store on your own computer once.

## Say this to use it

Any of these will do:

- "read this X article for me" with the link
- "what does this tweet actually say?"
- "pull the whole thread from this post"

Or, to be certain this skill and no other one runs:

```
/voice-and-editing:x-read
```

It needs the link to the post itself, the one with `/status/` in it. A link of the form `x.com/i/article/...` is refused, because that is the article and not the post that carries it, and it will ask you for the post link instead. The first time you use it, it will stop and give you a command to run in your own terminal to store your sign-in values.

## What you'll get

The post or article as plain text, with who wrote it, when, and the numbers underneath.

*This example is illustrative. It was written by hand to show the shape of the output, not copied from a real run.*

```text
@example_account  12 March 2026, 09:41
Article: What we learned shipping on a weekly cadence

We moved from monthly to weekly releases in January. Three things
broke immediately, and two of them were not the release process.

The first was review. A monthly batch hid how long review really
took...

[full article body continues, about 2,100 words]

replies 84 | reposts 220 | likes 1,903
https://x.com/example_account/status/1234567890123456789
```

## Good to know

- **It uses your X sign-in, in the form of two session cookies.** They are named `auth_token` and `ct0`. Every run sends both to x.com as cookies, and sends `ct0` a second time as a separate header. That is what makes the request count as you.
- **You store those two values yourself, and they never pass through the conversation.** A setup program that ships with the skill, `scripts/x-read-auth.sh`, is one you run in your own terminal. It refuses to run on anything but macOS, asks for each value twice with the typing hidden, trims spaces, checks only the shape of what you typed (all hexadecimal characters, exactly 40 for `auth_token` and at least 64 for `ct0`), never shows a value back, and saves each one in your macOS login keychain, the password store built into macOS, as an item named `x-read-AUTH_TOKEN` or `x-read-CT0`. Run it with `--status` to see which are set, or `--delete` to remove both.
- **At run time it looks for the values in two places, in this order:** the environment it was started with, and then those keychain items, falling back to a pair named `last30days-*` if those exist instead. It fetches them from the keychain using the macOS `security` command. If neither place has them, it stops with a specific error, and you are handed the setup command rather than asked to paste anything.
- **It never prints a value.** There is a check you can run that reports only whether the values were found and which place they came from, and nothing else.
- **You must get the two values yourself**, from a browser where you are signed in to x.com. Nobody can do it for you, and nobody should ask you for them. They stop working when you sign out of x.com, and the sign it has happened is the fetches starting to fail.
- **It goes online on every run.** It calls X's own internal web address for the post, thread or search. If that fails in a particular way, it also loads four x.com pages and several of X's own JavaScript files from `abs.twimg.com` to work out X's current internal identifiers, which change from time to time.
- **It reads none of your own files, and writes one.** The only thing it saves is a small cache of those identifiers at `~/.config/bird/query-ids-cache.json`, rewritten when it has to look them up again.
- **It cannot post, like, repost or bookmark.** No path through its code does any of those. The bundled code is a trimmed copy of somebody else's X client, and the trimmed copy still contains the web addresses and identifiers for posting, uploading media, liking and bookmarking, left over and unused. Nothing calls them, but they are in the files if you look.
- **It needs macOS, and Node version 22 or newer.** The keychain and the `security` command are macOS only, so on another system you would have to supply the two values through the environment instead and replace the setup program.
- **It costs one or two network calls per fetch**, each given up on after thirty seconds.
- **X search matches words, not meaning.** Short queries, quoted phrases and operators such as `from:` work best, and a search result carries only an article's title and preview, so reading the body still means fetching the post.

## What next

- Once you have the text, checking whether what it claims is still true today: [fact-currency-check](../../../verification-kit/skills/fact-currency-check/).
- If you are quoting it into something you are writing: [humanizer](../humanizer/) strips the tells out of drafted prose.
- Back to the [voice-and-editing pack](../../README.md), or to [skill-library](../../../../README.md).
