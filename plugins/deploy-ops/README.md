# deploy-ops

Part of [skill-library](../../README.md). If the words skill, pack or agent are new to you, that page explains them first.

## What problem this solves

Getting a change onto a running website or service is where the back-and-forth starts. The deploy tool prints success and the page is still broken. Claude Code hands you a file and asks you to upload it. You check one address, it answers, and the thing a visitor actually sees is wrong anyway. Each round costs another message, and you end up being the one carrying the work across.

This pack gives Claude Code a way to run that loop itself. Deploy, then check the result at the address a person would really use, work out the cause from the actual output, fix it, and deploy again, without stopping to ask between rounds. It also carries one specific move, step by step: putting a website on Cloudflare Pages with your own domain name.

## When would I use this?

- You asked for a change to go live and want it checked at the real address, not signed off on a success message.
- A deploy keeps failing and you are tired of passing files and error messages back and forth.
- You want the work tried on a test copy of the site first, and to approve it yourself before it reaches the real one.
- You are moving a website to Cloudflare Pages and want the old host left running until the new one is proven.
- You want to put your own domain name on a site without handing your whole domain over to a new provider.
- A deploy needs a rollback plan written down before anything is pushed.

## What's inside

<!-- generated:whats-inside by maintainers/scripts/generate-inventory.sh from plugins/deploy-ops/reader-table.tsv; edit the source, never this block -->
| Skill | What it does | What you say to trigger it | What you get | On your computer |
| :--- | :--- | :--- | :--- | :--- |
| [cloudflare-pages-migration](skills/cloudflare-pages-migration/README.md) | Walks through moving a website from its current host onto Cloudflare Pages, keeping the old host live until the new one is proven, and changing one DNS record rather than the whole domain. | "move this site to Cloudflare Pages" | The migration carried out step by step, with the commands and their real output shown, including a comparison of the old and new site. | Runs Cloudflare's `wrangler` tool and the AWS command-line tool on your computer under sign-ins you already have, changes one DNS record in your domain's settings, and fetches both the old and new site to compare them. |
| [deploy-verify-fix](skills/deploy-verify-fix/README.md) | Runs your project's own deploy, checks the result at the address a visitor would use, works out what went wrong from the real output, and redeploys, round after round. | "deploy this and keep going until it actually works" | A working deploy, or a diagnosis and a recommendation if it does not converge, plus a one-line record of each round. | Runs the deploy, verification and rollback commands your project has already defined, edits your project files to fix what it finds, and reaches the address it is verifying over the internet. |

This pack also ships agents. An **agent** is a helper that Claude Code hands a whole job to; it works on its own and reports back.

| Agent | What it does | What you say to trigger it | What you get | On your computer |
| :--- | :--- | :--- | :--- | :--- |
| [deploy-loop-owner](agents/deploy-loop-owner.md) | Takes over a whole deploy job and keeps going on its own, so you are not carrying files back and forth between the work and the place it has to run. | "take this to staging and don't come back until it's verified" | A verified deploy, or the diagnosis and a recommendation, never a file handed back for you to try. | Nothing restricts which tools it uses, so it can run commands, change your project files and use the network by itself until it succeeds or hits one of the two stop points in its instructions. |
<!-- /generated:whats-inside -->

Use `deploy-verify-fix` for any deploy, whatever the host: it has no commands of its own and runs the ones your project already has. Use `cloudflare-pages-migration` only for the one job it describes. Ask for the `deploy-loop-owner` agent when you want the whole job taken over rather than a method applied inside your current conversation.

The migration skill is written from two of its author's own moves, both with the domain's DNS records held at Amazon Route 53. The commands it gives are the ones that worked there. If your domain is managed somewhere else, the shape of the move still holds, but you would supply your own provider's way of adding a DNS record in place of the AWS commands it shows.

## What this does on your computer

| | |
| :--- | :--- |
| Files read | `deploy-verify-fix` and the `deploy-loop-owner` agent read whatever your own deploy produces while they work: logs, error output, the content a server sends back. No fixed file.<br>`cloudflare-pages-migration` reads one file of its own inside the pack, a written record of two past migrations. |
| Files written | No skill here writes a file of its own.<br>`deploy-verify-fix` adds one line per round to whatever running log your project already keeps.<br>The `deploy-loop-owner` agent edits your project's files, because fixing and redeploying is its job, and its instructions say nothing may be deployed that has not been committed first.<br>`cloudflare-pages-migration` writes no local file. It changes one DNS record, which is a setting held by your domain's provider rather than anything on your computer. |
| Files deleted or moved | None. |
| Programs and scripts | No programs ship with this pack. It is written instructions only.<br>`deploy-verify-fix` and the agent name no commands of their own. They run your project's deploy, verification and rollback commands, exactly as you wrote them, so what runs is whatever you put there.<br>`cloudflare-pages-migration` does name real commands and runs them: `npx wrangler whoami`, `npx wrangler login` and `npx wrangler pages project list`, which are Cloudflare's own `wrangler` tool; `aws sts get-caller-identity`, `aws route53 list-hosted-zones`, `aws route53 change-resource-record-sets` and `aws route53 get-change`, which are Amazon's command-line tool. The third of those changes a DNS record rather than only reading one. It also runs `dig`, `curl` and `diff`, three small tools already on most computers, and `gh api`, GitHub's command-line tool, to confirm the old host is untouched. |
| Internet access | Yes, and it is the point.<br>`deploy-verify-fix` and the agent reach the network every round, because verifying means loading the thing at its real address instead of trusting a tool's own report.<br>`cloudflare-pages-migration` talks to Cloudflare, to Amazon's DNS service, to the DNS system itself, and to both the old and the new site, which it downloads and compares. |
| Accounts, keys or passwords | No skill here asks you to type a key or a password.<br>`cloudflare-pages-migration` acts through sign-ins you already hold: your Cloudflare account, through `npx wrangler login`, which sends you to a browser to sign in rather than asking for a token, and your AWS sign-in, through a named profile of the AWS command-line tool that can reach your domain's DNS records. It also expects you to have allowed Cloudflare to see your GitHub account once, in a browser.<br>`deploy-verify-fix` and the agent use no accounts. Both treat "this fix needs a credential" as a reason to stop and come back to you. |

Two limits. First, the stopping points are written instructions, not something your computer enforces. The `deploy-loop-owner` agent has nothing set on it restricting which tools it may use, so it can run commands, change files and use the network on its own; what holds it back is its own text, which says to return to you before anything reaches the real site and to stop at anything "beyond the agreed ceilings". Those ceilings are meant to be written down in your project, and the agent's file does not define them, so if your project has not written them down, that stop has nothing specific behind it. Second, `cloudflare-pages-migration` marks some of what it tells you as not fully confirmed, including the exact wording of the Cloudflare screens you will be clicking through and one claim about what the `wrangler` tool cannot do. Those come from a single past migration, so read the screen in front of you rather than assuming it matches.

## How the skills work together

1. **Any deploy, any host:** `deploy-verify-fix`. It is the method. Before the first round it has you settle five things: the exact deploy command, the address that counts as proof, anything odd about your setup, the rollback command, and how many failed rounds are too many.
2. **When you want the whole job taken off your hands:** ask for the `deploy-loop-owner` agent instead. It follows the same loop, but as a separate helper that keeps going without checking in, and returns to you at two points: before anything goes from the test copy to the real site, and at anything on the stop list.
3. **For one particular move:** `cloudflare-pages-migration`, when the job is putting a site on Cloudflare Pages with your own domain. It is a sequence of its own, and the loop above still applies to the deploys inside it.

## Install

Inside a running Claude Code session:

```
/plugin marketplace add GFMCloud/skill-library
/plugin install deploy-ops@skill-library
```

The first line is only needed once, however many packs you install.

This pack needs the `foundry-core` pack, so Claude Code installs that one at the same time. The install message says `+ 1 dependency: foundry-core`.

`cloudflare-pages-migration` needs two other programs already on your computer and already signed in: Cloudflare's `wrangler`, which runs through `npx`, part of Node, and Amazon's `aws` command-line tool. It also uses `dig`, `curl` and `diff`, which most computers already have, and `gh`, GitHub's command-line tool, for one check. `deploy-verify-fix` and the `deploy-loop-owner` agent need nothing extra beyond whatever your own project's deploy command needs.

## Back to the main page

[skill-library](../../README.md) lists all the packs and explains the terms used here.
