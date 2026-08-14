---
name: cloudflare-pages-migration
description: >-
  Migrate a static or git-built site from GitHub Pages (or another host) onto
  Cloudflare Pages with a custom domain on external DNS (e.g. Route 53), without
  breaking the old host or the weekly/CI rebuild. Use when the user says "move
  this site to Cloudflare Pages", "put a custom domain on this", "migrate off
  GitHub Pages", or is repeating the Nana's Recipe Book / beetlewood pattern for
  a new site. Carries the wrangler CLI limits, the DNS-provider trap, the CNAME
  change-batch flow, parity verification, and why the push itself is the deploy
  proof, five things three separate sessions each re-derived by hand.
metadata:
  maturity: incubator
---

# Cloudflare Pages migration

Three sessions on this machine each rediscovered the same five facts by hand
before finishing this exact migration. This skill exists so a fourth session
does not. It is written against one fully-verified worked example
(`beetlewood-north-atlas`, 2026-08-13) plus one prior migration
(`nanasrecipes.gfmcloud.com`, 2026-08-12) that beetlewood's own session named as
its reference pattern. Every claim below states which of the two it comes from.
See [references/worked-example.md](references/worked-example.md) for the full
evidence log with commands and actual output.

## When this applies

- Source is a git repo that already builds and pushes static output to a
  branch (a CI job, a weekly Action, or a plain `git push`).
- Target is Cloudflare Pages, git-connected, with a custom domain on a DNS
  zone Cloudflare does not host (Route 53 in both worked examples).
- The old host stays live as a fallback until the new one is proven, not torn
  down as part of the migration.

If the site needs a real Cloudflare build step (not "commit static output,
serve as-is"), the auto-deploy assumptions below still hold, but this skill
does not cover configuring a build command, that part is unverified here.

## 1. Preflight: what wrangler cannot do (measured, not remembered)

Verified in `nanasrecipes.gfmcloud.com`, Phase 3, 2026-08-12
(`Nana's Recipe Book/website-harness/STATE.md`): `npx wrangler pages project
list` and `npx wrangler whoami` work fine (wrangler 4.122.0 via `npx`,
account `graham@gfmcloud.com`, scopes include `pages (write)`). But creating a
**git-connected** Pages project failed via the API path (`8000077 "Your user
email must been verified"`) and required the dashboard wizard regardless:
the one-time Cloudflare↔GitHub App authorization is a browser step, not a CLI
one. Attaching the **custom domain** was likewise done through the dashboard,
not `wrangler`.

Consistent with beetlewood: the final verified state
(`handoff-beetlewood-cloudflare-migration-2026-08-13.md`, RESOLUTION section)
shows the Pages project git-connected with both `*.pages.dev` and the custom
domain attached, but the session that did that work did it through the
dashboard, not a `wrangler` command captured in the log. Beetlewood's own
transcript does not re-attempt the CLI path and fail it directly, so treat
"wrangler cannot create git-connected projects or attach custom domains
via CLI" as verified in the Nana's session and **consistent with, not
independently reproduced by,** beetlewood.

**What this means for you:** budget one human-in-the-loop browser step for
project creation (GitHub App authorization) and one for the domain wizard.
Don't try to script around it, it's dashboard-only by design, and matches
the no-raw-credentials rule (OAuth, not a token you'd otherwise have to
handle). Preflight both logins before you start:

```bash
npx wrangler whoami                                    # Cloudflare
aws sts get-caller-identity --profile <route53-profile> # AWS
```

Both should fail loudly pre-login (natural negative control) and succeed
after `npx wrangler login` / `aws sso login`. If either succeeds pre-login
without you having logged in this session, stop and check who else has an
active session on this machine before proceeding (see
[references/worked-example.md](references/worked-example.md) for why that
check matters here specifically).

## 2. The "My DNS provider" trap

**This is the specific stumble the skill exists for.** When Cloudflare Pages
asks how to route a custom domain whose zone is not already active in your
Cloudflare account, it offers a path that looks like "just let Cloudflare
handle DNS", accepting that path migrates the **entire zone**'s nameservers
to Cloudflare, not just the one subdomain you're adding. For a zone like
`gfmcloud.com` carrying unrelated records (mail, other subdomains), that is
not what you want.

The correct path in both worked examples: decline the "Cloudflare DNS" /
nameserver-change option, keep the zone on its existing DNS provider (Route
53 here), and add **one CNAME record** yourself pointing the subdomain at the
Pages project's `*.pages.dev` target. That is what both `nanasrecipes` and
`beetlewood` actually ended up with, a single CNAME in an unmoved Route 53
zone, nothing else touched.

**Evidentiary status:** this trap is recorded from the cross-session review
that this skill's backlog item traces to
(`claude-improvements-harness/docs/claude-session-review-2026-08-13.md`), not
from a UI screenshot or click log inside the beetlewood transcript itself:
the dashboard clicks in both migrations were done by Graham directly and
aren't narrated step-by-step in either handoff. Treat the trap as real (it's
why three sessions independently flagged it) but treat the exact wizard
wording as unverified until you're looking at the screen yourself. If you
land on a "change your nameservers" prompt instead of a "add this CNAME"
prompt, that's the signal you took the wrong branch, back out and look for
the manual-DNS / "I'll add records myself" option instead.

## 3. The CNAME change-batch flow (executable sequence)

Both migrations used a Route 53 CNAME, not a Cloudflare-managed zone. Evidenced
end-to-end in beetlewood's RESOLUTION section and Nana's Phase 3:

```bash
# 1. Confirm which profile actually sees the zone, do not assume the default
aws route53 list-hosted-zones --profile <profile-a>   # may return []
aws route53 list-hosted-zones --profile <profile-b>   # the real one
# Both worked examples needed a NON-default profile
# (automation-shared-services), the default profile saw an empty zone list.

# 2. Submit the change batch (one CNAME, not a zone cutover)
aws route53 change-resource-record-sets \
  --profile <profile> \
  --hosted-zone-id <zone-id> \
  --change-batch '{
    "Changes": [{
      "Action": "UPSERT",
      "ResourceRecordSet": {
        "Name": "<subdomain>.<domain>",
        "Type": "CNAME",
        "TTL": 300,
        "ResourceRecords": [{"Value": "<project>.pages.dev"}]
      }
    }]
  }'
# Returns a change ID, status PENDING.

# 3. Poll until INSYNC before trusting it
aws route53 get-change --id <change-id> --profile <profile>

# 4. Confirm resolution independent of the AWS API
dig +short <subdomain>.<domain> CNAME
```

Both migrations used TTL 300 and a plain `UPSERT`. Neither touched any other
record in the zone.

## 4. Parity verification before cutover

Verify the new host serves the **same bytes** as the old one before treating
the migration as done, not just that it returns 200.

Evidenced in beetlewood (RESOLUTION section), the simplest form that's
directly reproducible:

```bash
curl -sI https://<new-domain>/                 # status, headers, TLS
diff <(curl -s https://<new-domain>/) <(curl -s https://<old-host>/)
# beetlewood: empty diff, 1,173,958 bytes identical both sides
```

Nana's Recipe Book went further with a purpose-built `parity_check.py`
(page/title/line/image counts, redirect-following, noindex header checks),
useful if the site has more than one page, but that tooling is project-specific
and unverified as a general pattern here; treat the `curl`/`diff` form above as
the minimum bar, and build a real checker only if the site is bigger than a
handful of pages.

**Watch for a redirect mismatch specifically:** Nana's Phase 4 hit a real
failure here, Cloudflare Pages serves "pretty URLs" (a 308 from
`/page.html` to `/page`), and their first parity run failed loudly because
Python's `urllib` doesn't follow 308 by default. That's a checker defect, not
a site defect, but it's exactly the kind of false alarm parity checking is
supposed to catch, don't wave off a failure without confirming which side
it's actually on.

## 5. Push-as-auto-deploy-proof

If the Pages project is git-connected with **no build command and the output
directory set to the repo root** (or wherever the existing CI already writes
static output), then **every push to the tracked branch is the deploy**.
There is no separate "trigger a deploy" step and no build log worth reading:
the CI/Action that already builds and pushes is doing all the work it needs to.

Evidenced directly in beetlewood: the weekly `refresh.yml` Action rebuilds and
pushes to `master`; the Cloudflare Pages project was configured to track
`master` with no build command; verification was `curl`, `dig`, and `diff`
against the live domain, never a Cloudflare build-log inspection.

**What this means for you:** when you're asked "did the deploy work," the
answer comes from hitting the deployed URL, not from checking Cloudflare's
dashboard for a green build. If you do want machine-checkable deploy status,
use the API, not the log:

```bash
npx wrangler pages project list           # confirm project + attached domains
# or, per Nana's Phase 3:
# GET the Pages deployment via the Cloudflare API and check
# latest deployment stage == "deploy", status == "success"
```

But the deployed URL is the source of truth either way, verify against it,
not against a proxy for it.

## Output contract

N/A, this skill produces executed migration steps and verification output in
the conversation, not a structured artifact consumed by another skill or
agent.
