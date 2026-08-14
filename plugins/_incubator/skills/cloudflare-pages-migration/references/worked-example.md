# Worked example: beetlewood-north-atlas, plus the Nana's reference pattern

Full evidence log backing the claims in `SKILL.md`. Two sources, kept
distinct because SKILL.md is scoped to what beetlewood itself evidences and
marks anything else as corroborating-but-not-independently-verified there.

- **Primary:** `beetlewood-north-atlas` migration, 2026-08-13. Source:
  `/Users/gfm/work/beetlewood-north-inaturalist/handoff-beetlewood-cloudflare-migration-2026-08-13.md`
  (read-only; that repo is not part of this skill build).
- **Reference pattern:** `nanasrecipes.gfmcloud.com`, 2026-08-12. Source:
  `/Users/gfm/work/Nana's Recipe Book/website-harness/STATE.md`. Beetlewood's
  own handoff names this as "source of truth for how, don't re-derive", it
  is not an outside generalization, it's the pattern beetlewood's own session
  was told to follow.

## beetlewood-north-atlas: what actually happened

- Source: `GFMCloud/beetlewood-north-atlas`, public, default branch `master`,
  previously served by legacy GitHub Pages (deploy-from-branch, root of
  `master`).
- A weekly GitHub Action (`.github/workflows/refresh.yml`) pulls iNaturalist
  data, runs `scripts/build_pages.py`, commits, and pushes to `master` with
  rebase-retry. Whatever hosts the site needs to deploy on every push with no
  separate build step, that's why the Cloudflare Pages project was
  configured with root output directory and no build command, replicating
  the existing legacy Pages behavior exactly.
- Target subdomain: `beetlewood.gfmcloud.com`, decided by matching the
  existing `nanasrecipes.gfmcloud.com` convention.
- **A concurrent, unrelated `claude` CLI session on the same machine had
  already completed the entire migration** (Pages project created,
  GitHub-connected, custom domain attached, Route 53 CNAME created) roughly
  three hours before the session that wrote the handoff even started
  checking. The handoff's own "nothing created yet" framing was stale by the
  time it was written. This was caught only because Graham screenshotted the
  Cloudflare dashboard directly, a git-only check missed it entirely, since
  the concurrent session's only trace in git was one unrelated commit
  (`.gitignore .wrangler/`).
- **Lesson carried into SKILL.md's preflight section:** verify live
  infrastructure state (dashboard, `wrangler pages project list`, `dig`,
  `curl`) before acting on a handoff's claim that nothing exists yet,
  especially once you know a concurrent or prior session touched the same
  path. Don't ask the user to redo dashboard work without checking first.

### Final verified state (all executed, not just checked for existence)

```
npx wrangler pages project list
→ beetlewood-north-atlas present, git-connected,
  domains: beetlewood-north-atlas.pages.dev, beetlewood.gfmcloud.com

dig +short beetlewood.gfmcloud.com CNAME
→ beetlewood-north-atlas.pages.dev.

aws route53 list-resource-record-sets (zone Z0030260BAWYULASNFNT,
  profile automation-shared-services)
→ CNAME record present, TTL 300

curl -sI https://beetlewood.gfmcloud.com/
→ HTTP/2 200, served by Cloudflare

diff <(curl -s https://beetlewood.gfmcloud.com/) \
     <(curl -s https://gfmcloud.github.io/beetlewood-north-atlas/)
→ empty (byte-identical, 1,173,958 bytes both sides)

gh api repos/GFMCloud/beetlewood-north-atlas/pages
→ still status: built, build_type: legacy, source: {branch: master, path: /}
  (GitHub Pages fallback confirmed untouched, per the ratified plan)
```

### What beetlewood does NOT independently evidence

- The exact wrangler-cannot-do-X failure mode (no CLI attempt-and-fail log
  for git-connected project creation or custom domain attach appears in the
  beetlewood transcript, the work was already done via dashboard by the
  concurrent session before this session looked).
- The "My DNS provider" wizard wording (no UI click-by-click log in either
  handoff; Graham did those steps directly).
- Any wrangler rate limits (requests/minute, deploy frequency caps). Neither
  worked example hit one. Do not assume any specific numeric limit; if you
  need one, measure it and date it before writing it down here.

## Nana's Recipe Book: nanasrecipes.gfmcloud.com, 2026-08-12

Source: `Nana's Recipe Book/website-harness/STATE.md`, Phase 0 and Phase 3.

```
npx wrangler whoami (pre-login)
→ "You are not authenticated" (natural negative control)

npx wrangler login → OAuth completed by Graham → "Successfully logged in."

npx wrangler whoami (post-login)
→ graham@gfmcloud.com, scopes include pages (write), zone (read)

npx wrangler pages project list
→ exit 0, empty list (no projects yet, as expected). wrangler 4.122.0 via npx.

aws sts get-caller-identity --profile default        → []  (zone not visible)
aws sts get-caller-identity --profile personal-admin  → []  (zone not visible)
aws route53 list-hosted-zones --profile automation-shared-services
→ gfmcloud.com., zone ID Z0030260BAWYULASNFNT
```

Pages project creation, via API, BLOCKED:

```
POST .../pages/projects → error 8000077
  "Your user email must been verified"
```

Resolved by Graham verifying the account email, then creating the project
**himself, through the dashboard wizard** (including the one-time
Cloudflare↔GitHub App authorization), this is the direct evidence for
"git-connected Pages project creation is dashboard-only, not scriptable via
wrangler," which SKILL.md cites as verified here.

```
Route 53 CNAME created:
  nanasrecipes.gfmcloud.com CNAME personal-nanas-recipes-site.pages.dev
  (TTL 300), change ID tracked, polled to INSYNC

dig +short CNAME → personal-nanas-recipes-site.pages.dev.
curl https://nanasrecipes.gfmcloud.com/
→ HTTP/2 200, x-robots-tag: noindex, nofollow, correct title
Certificate: CN=nanasrecipes.gfmcloud.com, issuer Google Trust Services
```

### The pretty-URL / 308 parity failure (Nana's Phase 4)

First live parity run failed loudly, exit 1, 172 issues: every recipe page
reported `page-missing (HTTP 308)`. Cloudflare Pages serves pretty URLs
(`/recipes/<id>.html` → 308 → `/recipes/<id>`); the parity checker's Python
3.9 `urllib` only follows 301/302/303/307 by default, not 308. Fixed by
adding a custom `HTTPRedirectHandler` that treats 308 like 307. This is a
checker defect, not a site defect, cited in SKILL.md section 4 as the reason
to confirm which side a parity failure is actually on before treating it as a
real regression.
