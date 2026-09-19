# Moving a website to Cloudflare Pages

Part of the [deploy-ops](../../README.md) pack.

This skill walks Claude Code through moving a website onto Cloudflare Pages, a free host for sites made of ready-built files, and putting your own domain name on it. It is built from two moves the author did by hand, and it carries the parts that went wrong both times. The main one is a choice Cloudflare offers you partway through that, if you take it, hands your entire domain over to Cloudflare rather than the one address you meant to move. The skill has you decline that and add a single DNS record instead, leaves the old host running until the new one is proven, and compares the two sites before calling it done.

## Say this to use it

Any of these will do:

- "move this site to Cloudflare Pages"
- "put a custom domain on this site"
- "migrate this off GitHub Pages without breaking it"

Or, to be certain this skill and no other one runs:

```
/deploy-ops:cloudflare-pages-migration
```

It will ask which repository builds the site, which address you want it served at, and where your domain's DNS records are held. It will also check both your sign-ins before starting, and tell you where you have to click through a browser yourself, because two steps cannot be done any other way.

## What you'll get

The move carried out in order, each step with the command and its real output, ending in a comparison of the old and new site.

*This example is illustrative. It was written by hand to show the shape of the output, not copied from a real run.*

```
Preflight
  npx wrangler whoami                     -> signed in, pages (write)
  aws sts get-caller-identity --profile X -> signed in

Over to you, in a browser: create the Pages project, connect it to the
repository, attach the domain. When the wizard asks about DNS, choose the
option that lets you add records yourself. Do NOT accept the one that
changes your nameservers: that moves the whole domain, mail included.

DNS
  change-resource-record-sets -> change id C1234, PENDING
  get-change                  -> INSYNC
  dig +short www.example.com CNAME -> example-site.pages.dev.

Parity
  curl -sI https://www.example.com/   -> 200, served by Cloudflare
  diff old vs new                     -> no differences, 1,173,958 bytes

Old host left running and untouched. Every future push deploys the site
by itself; there is no separate deploy step to run.
```

## Good to know

- **It changes a DNS record for real.** One command adds or replaces a single record pointing your chosen address at the new host. It touches no other record, and the change is undone the same way it was made.
- **It runs two outside programs on your computer:** Cloudflare's `wrangler`, through `npx`, which comes with Node, and Amazon's `aws` command-line tool. Both must already be installed. It also uses `dig`, `curl` and `diff`, which most computers already have. It signs in to AWS with `aws sso login` if your sign-in has lapsed.
- **It signs in through your browser, never through a pasted key.** `npx wrangler login` opens your Cloudflare account's own sign-in page. The AWS side uses a named profile you already have set up.
- **Two steps cannot be automated and it says so up front:** creating the project with the repository connected, and attaching your domain, are both done by you in Cloudflare's website.
- **It goes online throughout.** It talks to Cloudflare, to your DNS provider, to the DNS system, and it downloads both the old and the new site to compare them byte for byte.
- **It writes no file on your computer.** The only thing it changes is the DNS record and the settings held in your Cloudflare account.
- **It is written for domains whose DNS lives at Amazon Route 53.** Both of the moves it is built from were like that, and the DNS commands it gives are Amazon's. If your domain is managed elsewhere, the shape still holds but you supply your own provider's way of adding one record.
- **Parts of it are marked unconfirmed, by the skill itself.** The exact wording of the Cloudflare screens, and the claim that `wrangler` cannot create a repository-connected project, come from a single past move. Read the screen in front of you rather than assuming it matches.
- **After the move there is no deploy step.** Once the project is connected to your repository, every push to the tracked branch is the deploy, so proof comes from loading the site, not from looking for a green build.

## What next

- Before you move anything, and for every deploy after: [deploy-verify-fix](../deploy-verify-fix/), the check-and-fix loop this pack is built around.
- To hand a whole deploy job to a separate helper that keeps going on its own: the [deploy-loop-owner](../../agents/deploy-loop-owner.md) agent in this pack.
- For what counts as proof that something really worked: [proof-of-work](../../../foundry-core/skills/proof-of-work/).
- To check the moved site is fast and has no broken links: [site-review](../../../verification-kit/skills/site-review/).
- Back to the [deploy-ops pack](../../README.md), or to [skill-library](../../../../README.md).
