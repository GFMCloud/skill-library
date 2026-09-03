#!/usr/bin/env node
// x-read: fetch full X posts, long-form X Articles, threads, and search results.
// Auth: AUTH_TOKEN + CT0 from env, else macOS keychain (x-read-*, then last30days-*).
// Cookie values are never printed. Engine: vendored @steipete/bird 0.8.0 (MIT).

import { execFileSync } from 'node:child_process';
import { TwitterClientBase } from './vendor/bird/lib/twitter-client-base.js';
import { withSearch } from './vendor/bird/lib/twitter-client-search.js';
import { withTweetDetails } from './vendor/bird/lib/twitter-client-tweet-detail.js';
import { extractTweetId } from './vendor/bird/lib/extract-tweet-id.js';

const Client = withSearch(withTweetDetails(TwitterClientBase));
const KEYCHAIN_SERVICES = ['x-read', 'last30days'];
const TIMEOUT_MS = 30_000;

const USAGE = `usage:
  x-read <post-url-or-id> [--json]        full post or X Article body
  x-read thread <post-url-or-id> [--json] whole conversation thread, oldest first
  x-read search "<query>" [-n N] [--json] latest posts matching an X search query
  x-read auth-check                       report whether credentials resolve (no values)

exit codes: 0 ok, 1 fetch failed, 2 usage, 3 no credentials`;

function fail(msg, code = 1) {
  process.stderr.write(`x-read: ${msg}\n`);
  process.exit(code);
}

function keychain(service, key) {
  try {
    return execFileSync(
      'security',
      ['find-generic-password', '-a', process.env.USER ?? '', '-s', `${service}-${key}`, '-w'],
      { encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore'], timeout: 5000 },
    ).trim();
  } catch {
    return '';
  }
}

function resolveCredentials() {
  const envAuth = (process.env.AUTH_TOKEN ?? '').trim();
  const envCt0 = (process.env.CT0 ?? '').trim();
  if (envAuth && envCt0) return { authToken: envAuth, ct0: envCt0, source: 'env' };
  if (process.platform === 'darwin') {
    for (const service of KEYCHAIN_SERVICES) {
      const authToken = keychain(service, 'AUTH_TOKEN');
      const ct0 = keychain(service, 'CT0');
      if (authToken && ct0) return { authToken, ct0, source: `keychain:${service}` };
    }
  }
  return null;
}

function requireClient() {
  const creds = resolveCredentials();
  if (!creds) {
    fail(
      'no X credentials. Run scripts/x-read-auth.sh in your own terminal to store auth_token and ct0 in the keychain, or export AUTH_TOKEN and CT0.',
      3,
    );
  }
  return { client: new Client({ cookies: creds, timeoutMs: TIMEOUT_MS, quoteDepth: 1 }), source: creds.source };
}

function fmtDate(iso) {
  if (!iso) return 'unknown date';
  const d = new Date(iso);
  return Number.isNaN(d.getTime()) ? iso : d.toISOString().slice(0, 10);
}

export function renderTweet(t, { heading = true } = {}) {
  const lines = [];
  const title = t.article?.title;
  let body = (t.text ?? '').trim();
  if (title && body.startsWith(title)) body = body.slice(title.length).replace(/^\s+/, '');
  if (heading) lines.push(`# ${title ?? `@${t.author.username} on X`}`, '');
  lines.push(`**@${t.author.username}** (${t.author.name}) · ${fmtDate(t.createdAt)} · https://x.com/${t.author.username}/status/${t.id}`);
  const stats = [
    ['likes', t.likeCount],
    ['reposts', t.retweetCount],
    ['replies', t.replyCount],
  ]
    .filter(([, v]) => v != null)
    .map(([k, v]) => `${v} ${k}`)
    .join(' · ');
  if (stats) lines.push(stats);
  if (title) lines.push(`Type: X Article (${body.length} chars of body)`);
  lines.push('', body || '(no text)');
  if (t.quotedTweet) {
    lines.push('', '> **Quoting:**');
    for (const l of renderTweet(t.quotedTweet, { heading: false }).split('\n')) lines.push(`> ${l}`);
  }
  if (t.media?.length) {
    lines.push('', ...t.media.map((m) => `- ${m.type}: ${m.url}`));
  }
  return lines.join('\n');
}

function renderList(tweets, header) {
  const out = [`# ${header}`, ''];
  tweets.forEach((t, i) => {
    out.push(`## ${i + 1}. @${t.author.username} · ${fmtDate(t.createdAt)}`, '');
    out.push(renderTweet(t, { heading: false }), '');
  });
  return out.join('\n');
}

function parseArgs(argv) {
  const flags = { json: false, n: 20 };
  const positional = [];
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--json') flags.json = true;
    else if (a === '-n' || a === '--count') flags.n = Number.parseInt(argv[++i] ?? '', 10);
    else if (a === '-h' || a === '--help') { console.log(USAGE); process.exit(0); }
    else if (a.startsWith('-')) fail(`unknown flag ${a}\n${USAGE}`, 2);
    else positional.push(a);
  }
  if (Number.isNaN(flags.n) || flags.n < 1) fail('-n must be a positive integer', 2);
  return { flags, positional };
}

function tweetIdFrom(input) {
  if (/x\.com\/i\/article\//i.test(input)) {
    fail('that is an Article page URL. Use the post URL that carries the article (x.com/<user>/status/<id>).', 2);
  }
  const id = extractTweetId(input);
  if (!/^\d+$/.test(id)) fail(`cannot find a post id in "${input}"`, 2);
  return id;
}

async function main() {
  const { flags, positional } = parseArgs(process.argv.slice(2));
  if (positional.length === 0) fail(USAGE, 2);
  const [cmd, ...rest] = positional;

  if (cmd === 'auth-check') {
    const creds = resolveCredentials();
    console.log(creds ? `credentials: found (${creds.source})` : 'credentials: none');
    process.exit(creds ? 0 : 3);
  }

  if (cmd === 'search') {
    const query = rest.join(' ').trim();
    if (!query) fail('search needs a query', 2);
    const { client } = requireClient();
    const result = await client.search(query, flags.n);
    if (!result.success) fail(`search failed: ${result.error}`);
    if (flags.json) console.log(JSON.stringify(result.tweets, null, 2));
    else console.log(renderList(result.tweets, `X search: ${query}`));
    return;
  }

  if (cmd === 'thread') {
    if (!rest[0]) fail('thread needs a post URL or id', 2);
    const id = tweetIdFrom(rest[0]);
    const { client } = requireClient();
    const result = await client.getThread(id);
    if (!result.success) fail(`thread fetch failed: ${result.error}`);
    if (flags.json) console.log(JSON.stringify(result.tweets, null, 2));
    else console.log(renderList(result.tweets, `Thread containing ${id}`));
    return;
  }

  // default: read one post / article
  const id = tweetIdFrom(cmd);
  const { client } = requireClient();
  const result = await client.getTweet(id);
  if (!result.success) fail(`read failed: ${result.error}`);
  if (flags.json) console.log(JSON.stringify(result.tweet, null, 2));
  else console.log(renderTweet(result.tweet));
}

if (import.meta.url === `file://${process.argv[1]}`) {
  main().catch((err) => fail(err?.message ?? String(err)));
}
