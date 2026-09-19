# skill-library

[![validate-skills](https://github.com/GFMCloud/skill-library/actions/workflows/validate.yml/badge.svg)](https://github.com/GFMCloud/skill-library/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

Add-ons for Claude Code that make it check its own work, plan before risky changes, keep long projects on track, and handle a few specific jobs, such as building slide decks and designing web pages.

## What this is

**Claude Code** is a program you run in a terminal window on your own computer. You type a request in plain English, and it does the work on your files.

A **skill** is a short set of written instructions that teaches Claude Code how to do one specific job, such as checking that a README still matches the code it describes. You do not run a skill yourself. Claude Code reads it when the job comes up.

A **pack** (Claude Code calls it a *plugin*) is a folder of related skills that install together.

A **repository** is a project folder published on GitHub, a website for sharing code. You are reading one now. Its address is `GFMCloud/skill-library`: the owner's name, then the repository's name.

An **agent** is a helper that Claude Code hands a whole job to. It works on its own, with its own instructions, and reports back. Some packs include one or two.

<!-- generated:counts by maintainers/scripts/generate-inventory.sh from the plugins/ tree; edit the source, never this block -->
This repository has 12 packs, holding 67 skills and 9 agents.
<!-- /generated:counts -->

A **hook** is a small program that Claude Code runs by itself at a set moment, without being asked. One pack here installs one. It is described in full under [Is this safe?](#is-this-safe-what-does-it-do-on-my-computer)

A **marketplace** is a list of packs that Claude Code can install from. This repository is one marketplace, called `skill-library`.

A **slash command** is text you type in Claude Code that begins with `/`. It runs something directly instead of asking Claude to decide what to do. Every command below that starts with `/` is a slash command.

## Who this is for, and what you need first

This is for people who use Claude Code for real work, mostly software work, and want it to be more careful and need less hand-holding. You do not need to have installed a pack before. Most skills here assume you are working in a project folder with code or documents in it.

Before you start you need:

1. **Claude Code, installed and signed in.** If you have never installed it, follow the official guide at [code.claude.com/docs](https://code.claude.com/docs/en/quickstart) first. Nothing here works without it.
2. **A terminal window with Claude Code running.** When Claude Code is running you will see a prompt where you can type. That is where every command below goes.

Nothing here needs an account with us or a payment. A few skills need other free software, such as Node or Python, which are tools many programmers already have. Each pack page says which skill needs what. If you do not have it, that one skill will not work and the rest still will.

## Install

Everything below is typed **inside a running Claude Code session**, at the prompt where you normally type your requests. Do not type them at the ordinary terminal prompt, before Claude Code has started. They only work inside Claude Code.

**Step 1. Add this marketplace.** This tells Claude Code where to find our packs. It does not install anything yet.

```
/plugin marketplace add GFMCloud/skill-library
```

You should see a confirmation that the marketplace `skill-library` was added.

**Step 2. Install one pack.** Start with one. You can add others later.

```
/plugin install consistency-checker@skill-library
```

Claude Code opens a details screen and asks you to pick where to install it. Choose **User scope** if you want the pack available in every folder you work in. Press Enter to confirm.

This pack needs one other pack, `foundry-core`, so Claude Code installs that too and the message says `+ 1 dependency: foundry-core`. That is expected.

**Step 3. Check the install message.** If it says `Run /reload-plugins to activate.`, Claude Code usually runs that for you. If the pack does not seem to be there, type `/reload-plugins` yourself.

If any step did not go as described, see [docs/install-help.md](docs/install-help.md).

**If you installed a pack called `workbench` or `graham-voice` from here before 19 September 2026:** those two were reorganized. Claude Code moves you to their replacements, `long-projects` and `voice-and-editing`, by itself. Some `workbench` skills now live in two new packs, `project-starters` and `agent-tooling`, which you add yourself with the install command above. [CHANGELOG.md](CHANGELOG.md) has the full list.

## Try your first skill

Start Claude Code inside a project folder. To do that, open a terminal, type `cd` followed by a space and the folder's location, press Enter, then type `claude` and press Enter. Pick a folder that has a README, the file most projects include to describe themselves. Then type this and press Enter:

```
/consistency-checker:spec-artifact-diff
```

Claude Code will ask which document to check. Answer in plain English, for example: *check the README against this folder*.

What you get back is a list of the claims the README makes that a command can test, such as how many files there are, which commands exist, and what the version is. Each one comes with the command that tested it and whether it held. This skill only looks. It changes nothing unless you then ask it to correct the document.

You can also just describe what you want, with no slash command at all: *"does this README still match the code?"* Claude Code reads the skill descriptions and picks the right one on its own. The slash command is there for when you want to be certain which skill runs.

## Which pack do I need?

Answer the first question that matches you.

| If you want... | Install | A good skill to start with |
| :--- | :--- | :--- |
| Claude Code to prove work is done before it says so | `foundry-core` | [proof-of-work](plugins/foundry-core/skills/proof-of-work/) |
| Fewer questions and fewer wasted rounds | `turn-reduction` | [plan-gate](plugins/turn-reduction/skills/plan-gate/), then [output-lint](plugins/turn-reduction/skills/output-lint/) |
| To check claims, changes, deploys or a website before trusting them | `verification-kit` | [fact-currency-check](plugins/verification-kit/skills/fact-currency-check/) |
| Documents that stay true to the files they describe | `consistency-checker` | [spec-artifact-diff](plugins/consistency-checker/skills/spec-artifact-diff/) |
| Work that lasts many sessions to stay on track | `long-projects` | [handoff](plugins/long-projects/skills/handoff/) |
| To start a new project with the basics in place | `project-starters` | See the pack page |
| Deploys that get checked and fixed, not just pushed | `deploy-ops` | See the pack page |
| To clean data or match records across sources | `data-wrangler` | See the pack page |
| Better-looking websites and app screens | `frontend-design` | [minimalist-ui](plugins/frontend-design/skills/minimalist-ui/) |
| Slide decks planned, built and critiqued | `decks` | See the pack page |
| Help choosing a model, or sending bulk text work to a local model | `agent-tooling` | See the pack page |
| To see how one person set up their own writing voice and personal tools | `voice-and-editing` | Read its page first. Much of it is tied to the author's own computer. |
| More than one of the above | Install them one at a time, starting with the one you will use this week | |

Longer version, including what each pack does **not** do: [docs/which-pack.md](docs/which-pack.md).

## The packs

<!-- generated:pack-map by maintainers/scripts/generate-inventory.sh from .claude-plugin/marketplace.json and the plugin.json files; edit the source, never this block -->
![Map of the 12 packs. 5 packs (turn-reduction, data-wrangler, verification-kit, consistency-checker, deploy-ops) each have an arrow to foundry-core, the pack they need. The other 6 (decks, frontend-design, long-projects, project-starters, agent-tooling, voice-and-editing) install on their own. Each box gives the pack's number of skills and agents.](docs/images/pack-map.svg)
<!-- /generated:pack-map -->

The map is drawn from the same files as the table below. If it does not show, the table says the same thing, and each pack page says whether the pack needs `foundry-core`.

<!-- generated:catalog by maintainers/scripts/generate-inventory.sh from .claude-plugin/marketplace.json and the plugins/ tree; edit the source, never this block -->
| Pack | What it helps you do | Skills inside | Install |
| :--- | :--- | :--- | :--- |
| [foundry-core](plugins/foundry-core/README.md) | Makes Claude Code prove its work: run the real checks before saying done, show the evidence, write the whole file and not a fragment, and stop a fix loop after a set number of tries. | 6 | `/plugin install foundry-core@skill-library` |
| [turn-reduction](plugins/turn-reduction/README.md) | Cuts the back-and-forth: check access before starting, plan before risky work, agree up front what Claude Code may do without asking, and catch broken instructions before they reach you. | 4 | `/plugin install turn-reduction@skill-library` |
| [data-wrangler](plugins/data-wrangler/README.md) | Move and clean data between files and systems, and match records that mean the same person or thing under different spellings. | 1, and 1 agent | `/plugin install data-wrangler@skill-library` |
| [verification-kit](plugins/verification-kit/README.md) | Check before trusting: whether a claim is still true, whether a change is safe to ship, whether a deploy is really up, whether a website is fast and unbroken, and what code could be deleted. | 7, and 2 agents | `/plugin install verification-kit@skill-library` |
| [consistency-checker](plugins/consistency-checker/README.md) | Check documents against the files they describe, and against each other, one claim at a time. | 1, and 1 agent | `/plugin install consistency-checker@skill-library` |
| [deploy-ops](plugins/deploy-ops/README.md) | Deploy, check the result the way a visitor would, fix, and repeat until it works. Includes a step-by-step move of a website to Cloudflare Pages. | 2, and 1 agent | `/plugin install deploy-ops@skill-library` |
| [decks](plugins/decks/README.md) | Plan, build and critique slide decks: outlines, charts, clickable diagrams, PowerPoint export, and reviews of layout and sales message. | 6 | `/plugin install decks@skill-library` |
| [frontend-design](plugins/frontend-design/README.md) | Design judgment for websites and apps: a distinctive look for new builds, mobile screens, minimal interfaces, polish, and upgrades to a site that already exists. | 7, and 1 agent | `/plugin install frontend-design@skill-library` |
| [long-projects](plugins/long-projects/README.md) | Keep work that spans many sessions on track: step-by-step project plans that pause for your approval, handoff notes between sessions, a review routine for everyday changes, and second opinions on hard decisions. | 11, and 2 agents | `/plugin install long-projects@skill-library` |
| [project-starters](plugins/project-starters/README.md) | Start a new project properly: a project folder set up with a check for leaked passwords, a repeatable set of development tools, a project knowledge base, and pipeline and systems design before any code. | 6 | `/plugin install project-starters@skill-library` |
| [agent-tooling](plugins/agent-tooling/README.md) | Choose the right model and effort level for a task, send bulk mechanical text work to a local model, and mine past session transcripts for facts. | 3, and 1 agent | `/plugin install agent-tooling@skill-library` |
| [voice-and-editing](plugins/voice-and-editing/README.md) | One person's writing voice and editing tools, plus skills tied to the author's own computer and habits. Most useful as an example to copy and change: swap in your own voice, schedule and sources. | 13 | `/plugin install voice-and-editing@skill-library` |
<!-- /generated:catalog -->

Each pack's own page lists its skills, what you say to trigger each one, what you get back, and what it does on your computer. Read that page before you install. The install screen may not list what a pack contains.

## Is this safe? What does it do on my computer?

Read this before installing anything, here or anywhere else.

**The general warning first.** Installing a pack means trusting it completely. A pack can run programs on your computer with your own user permissions. Anthropic does not check what is inside a third-party pack and cannot promise it does what it says. Only install packs from a source you trust, and only after you have read what it says it does. That warning applies to this repository as much as any other.

**What these packs do.** This is the summary across every pack. Many skills here exist to run your tests, write files, or check a live website, so they do those things. Each pack page has its own table, and each skill that does more than talk has its own page.

| | |
| :--- | :--- |
| Files read | The project folder you are working in and any file you point at. A few skills read more: `retro`, `skill-discovery` and the `transcript-scanner` agent read your past Claude Code conversations, which are stored on your computer. `bounded-loop` reads every file in your project to notice changes. |
| Files written | Most skills that write, write into the project you are working in: reports, plans, check scripts, new code.<br>`new-project`, `experiment-harness`, `phased-harness`, `sweep-harness` and `rulings-harness` create a new folder where you tell them to.<br>`security-audit` writes its reports to `~/security-audit-skill/` (`~` means your home folder).<br>`x-read` keeps one small file in `~/.config/bird`, the settings folder of the program it uses to read X. |
| Files deleted or moved | No skill deletes your files as its job. Skills that change code (`orch-pipeline`, `review-pair`, `redesign-existing-projects`, the design skills) edit files in place, and `capability-preflight` and `deploy-verify-fix` run commands you wrote, which do whatever you wrote. Two small exceptions:<br>A script in `html-diagram` removes two screenshot images beside your diagram before it takes new ones.<br>`folder-to-repo` removes a file named `START_HERE.md` from the folder if one is there. |
| Programs and scripts | These packs ship small programs of their own, written in Python, shell or Node: `foundry-core`, `turn-reduction`, `verification-kit`, `decks`, `long-projects`, `project-starters` and `voice-and-editing`. Each pack page lists them.<br>Skills also run tools already on your computer, such as `git` and your project's own tests.<br>Four skills can install software:<br>`cd-to-pptx` installs LibreOffice and poppler, which convert slides, if they are missing.<br>`html-diagram` installs Playwright and its Chromium browser to take screenshots.<br>`site-review` downloads Lighthouse and linkinator, two website-checking tools, from npm, the public download site for Node tools.<br>`devshell-init` downloads a set of development tools through Nix, a package manager. |
| Internet access | Some skills go online because that is their job:<br>`fact-currency-check` looks claims up.<br>`site-review` and `smoke-gate` contact the website you name.<br>`source-intake` downloads the repository or article you point at.<br>`x-read` reads posts from X.<br>The deploy skills talk to your hosting provider.<br>Web pages made by `html-diagram` and `scrollback` load a font from Google when opened.<br>No pack sends your files to us. We run no service and collect nothing. Claude Code itself sends what it reads to the AI service that powers it, with or without any pack. |
| Accounts, keys or passwords | No skill asks you to paste a key or password into the conversation. Some act through programs you are already signed in to on your computer:<br>`new-project`, `folder-to-repo` and `repo-handoff` create a repository under your GitHub account.<br>`orch-review`, `source-intake` and `toolkit-review` use your GitHub sign-in.<br>The deploy skills and `plan-gate` use your cloud sign-ins.<br>`x-read` reads a sign-in cookie for X from your Mac's keychain, where you store it once yourself.<br>One more thing to know: `proof-of-work` searches your project for text that looks like a key or password and saves what it finds in its log folder. You choose that folder when you run it. Treat it as private. |
| Background activity | The `verification-kit` pack installs one hook. It runs before every command Claude Code is about to run on your computer, in every session. It only acts inside six agents that are meant to look and not change anything: `pre-delivery-verifier`, `silent-failure-hunter`, `cross-document-checker`, `transcript-scanner`, `loop-operator` and Claude Code's built-in `Explore`. There it refuses the usual commands that write, move or delete files. It does not catch every way of writing a file, and its pack page lists what it misses.<br>`bounded-loop` and `smoke-gate` can set up a check that runs each time Claude Code finishes a turn, only if you set it up.<br>`change-watch` and `schedule-harness` help you create scheduled jobs, which you register yourself.<br>`devshell-init` makes its development tools switch on whenever you enter that project folder. |

**How to check that for yourself.** Every skill in this repository is a plain text file you can read in your browser before installing. Open `plugins/<pack>/skills/<skill>/SKILL.md` in this repository. Programs a skill ships are in the same folder, usually under `scripts/`. If something does what you did not expect, do not install it, and please open an issue, which is a public report on this repository's GitHub page.

**What we do not promise.** These skills can get things wrong. A check can pass when it should fail. A security review that finds nothing does not mean the code is secure. Check anything that matters before acting on it.

## Status and help

This library is maintained by one person and used daily. It changes often. There is no support commitment. Skills marked `incubator` in the [inventory](docs/inventory.md) are newer and less proven than those marked `stable`.

<!-- generated:eval-status by maintainers/scripts/generate-inventory.sh from the plugins/*/evals/ tree; edit the source, never this block -->
19 of the 67 skills have at least three evaluation cases, which are written tests of whether a skill does its job. The other 48 have fewer than three, or none.
<!-- /generated:eval-status -->

The cases for the seven skills this page sends a first-time reader to were all run on 2026-09-19. Not every case passed, four cases were corrected afterwards and have not been run again, and the results are kept with the maintainer's records, not in this repository. The one case added to each of the other twelve suites that day has not been run yet.

If something is wrong or confusing:

- Open an issue at [github.com/GFMCloud/skill-library/issues](https://github.com/GFMCloud/skill-library/issues).
- For install trouble specifically, check [docs/install-help.md](docs/install-help.md) first. It also explains how to remove a pack.
- For a security problem, do not open a public issue. [SECURITY.md](SECURITY.md) says how to report it privately.

Other pages that may help:

- [docs/glossary.md](docs/glossary.md): every term used here, in one place.
- [docs/how-a-skill-works.md](docs/how-a-skill-works.md): what actually happens when a skill runs.
- [CHANGELOG.md](CHANGELOG.md): what changed and when.
- [CONTRIBUTING.md](CONTRIBUTING.md): for people who want to write or change a skill.
- [maintainers/](maintainers/): where each skill that was adapted from someone else's work came from, with the dated review behind it.

## License

MIT. See [LICENSE](LICENSE). You can use, copy and change anything here, including in your own projects.
