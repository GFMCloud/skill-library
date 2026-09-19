# Glossary

Part of [skill-library](../README.md).

Every term used on the main page or on a pack page, with a plain definition. Alphabetical. If a word you met is not here, open an [issue](https://github.com/GFMCloud/skill-library/issues) and it will be added.

**Accessibility**
Whether a web page can be used by someone relying on a screen reader, on a keyboard alone, or on poor eyesight. `site-review` gives a site a score for it.

**Agent**
A helper that Claude Code hands a whole job to. It has its own instructions, works on its own, and reports back when it is done. It does not see your conversation unless it is told about it. Some packs here include one or two.

**Branch**
A separate copy of the work kept by git. Changes made on a branch leave the main copy as it was, until you choose to merge the branch in. `site-review` fixes a site on a branch for that reason.

**Claude Code**
A program you run in a terminal window on your own computer. You type a request in ordinary English and it does the work on your files. It is made by Anthropic. Everything in this repository is an add-on for it and does nothing without it.

**Command line tool**
A program you use by typing its name, rather than by clicking. `git`, `gh`, `curl`, `dig`, `diff` and `jq` are all command line tools named on pack pages here.

**Commit**
A saved point in a project's history, recorded by git, with a short note saying what changed. Committing is how a change becomes part of the record.

**Context**
The limited amount of text Claude Code can hold in mind at one time. Every installed pack takes a small share of it in every turn, which is one reason to install one pack rather than all of them.

**Dependency**
A pack that another pack needs in order to work. Claude Code installs it for you when you install the pack that names it, and the install message says so, for example `+ 1 dependency: foundry-core`.

**Deploy**
To put a change onto a running website or service, so that other people see it.

**Description**
The one sentence at the top of a skill saying what it does and when to use it. Claude Code reads every installed skill's description to decide which skill fits your request.

**direnv**
A small program that switches a project's development tools on when you enter its folder. `devshell-init` uses it together with Nix.

**DNS record**
One line in the public address book of the internet, turning a domain name into the location of the computer that serves it. `cloudflare-pages-migration` changes one of these rather than moving a whole domain.

**Docker**
A program that runs other software inside a contained copy of an operating system. `toolkit-review` needs it for its largest size only.

**Domain name**
The name people type to reach a website, such as `example.com`.

**gh**
GitHub's own command line tool. Several skills use it, and they need you to be signed in to it already.

**git**
The tool programmers use to track changes to files. It records what changed, when, and by whom. A repository is a folder that git is tracking.

**gitleaks**
A program that searches a project for text that looks like a password or a key. See **Secret scan**.

**GitHub**
A website for storing and sharing projects kept in git. This repository is on GitHub, at `GFMCloud/skill-library`.

**Home folder**
The folder on your computer holding your own files and settings. It is written as `~` in a path, so `~/security-audit-skill/` means a folder of that name inside it.

**Hook**
A small program that Claude Code runs by itself at a set moment, without being asked. The `verification-kit` pack installs one. Its page says what it does and what it misses.

**Incubator and stable**
Two labels used in [inventory.md](inventory.md). `incubator` means a skill is newer and less proven. `stable` means it has settled.

**Install**
Copying a pack onto your computer so Claude Code can use it. One command per pack.

**Issue**
A public report on a project's GitHub page: a fault, a question or a request. Anyone can open one.

**jq**
A command line tool for reading and reshaping data in JSON format. `toolkit-review` uses it.

**Keychain**
The place macOS stores passwords and other secrets on your behalf. `x-read` reads one saved sign-in value from it, which you put there yourself.

**LibreOffice**
A free office suite. `cd-to-pptx` uses it to convert slides, and installs it if it is missing.

**Lighthouse and linkinator**
Two free programs that check a website, one for speed and accessibility, one for broken links. `site-review` downloads them from npm the first time it runs.

**Markdown**
A way of writing plain text with simple marks for headings, lists and links. Files ending in `.md` are written in it, including every skill here and this page.

**Marketplace**
A list of packs that Claude Code can install from. This repository is one marketplace, named `skill-library`. Adding a marketplace installs nothing on its own. It tells Claude Code where to look.

**Mermaid**
A way of writing a diagram as text. Some places that display these pages draw it as a picture, and some show the text instead.

**Model**
The version of Claude doing the work. Faster ones cost less, more capable ones cost more. `model-effort-advisor` recommends one for a given task.

**Nix**
A package manager, meaning a program that installs other programs. It pins them to exact versions, so every computer working on a project gets the same ones. `devshell-init` uses it.

**Node**
A program that runs software written in JavaScript outside a web browser. Several skills need it. It is free.

**npm**
The public download site for Node tools, and the command that fetches from it.

**npx**
A command that comes with Node and runs a Node tool once, without installing it permanently.

**Ollama**
A free program that runs an AI model on your own computer, so the text you give it does not leave the machine. `llama-offload` needs it, with a model already downloaded.

**Pack**
Our word for a folder of related skills that install together. Claude Code calls the same thing a plugin.

**Package**
A piece of software someone else wrote, which another program installs and uses. `python-pptx` and PyYAML are Python packages named on pack pages here.

**Playwright**
A tool that drives a web browser automatically. `html-diagram` installs it, along with its own copy of the Chromium browser, to take screenshots.

**Plugin**
Claude Code's own word for a pack. They are the same object. The commands use the official word, which is why you type `/plugin install`.

**poppler**
A set of small programs for reading PDF files. `cd-to-pptx` uses it, and installs it if it is missing.

**pre-commit**
A tool that runs checks on a project every time you commit, and stops the commit if a check fails. `new-project` sets one up.

**Pull request**
A set of proposed changes offered on GitHub for someone to review before it joins the main copy. Often shortened to PR. `orch-review` can review one.

**Python**
A programming language, and the program that runs it. Several packs here ship small Python programs. Many computers set up for programming already have it.

**README**
The file most projects include to describe themselves. It is the first thing shown on a project's GitHub page.

**Reload**
`/reload-plugins` makes Claude Code notice a pack you have installed during this session, without restarting. Claude Code usually runs it for you.

**Repository**
A project folder tracked by git and usually published on GitHub. Often shortened to repo. This one's address is `GFMCloud/skill-library`: the owner's name, then the repository's name.

**Rollback**
Putting a service back to the version it was running before a change, when the change turned out to be wrong.

**Sandbox**
A restricted area set up by your operating system, where a program can run without reaching the rest of your computer. `security-audit` builds and runs the code it is auditing only inside one, with no internet and set limits on time and memory.

**Scope**
Where an installed pack applies. Claude Code asks you to choose one at install time. **User** means every folder you work in, which is what most people want. **Project** means one repository, for everyone working in it. **Local** means one repository, for you alone.

**Script**
A small program written as plain text and run as it is, without being built first. The packs here ship scripts written in Python, shell and Node.

**Secret scan**
A search through a project for text that looks like a password, a key or a token, run before anything is published. `new-project`, `folder-to-repo` and `repo-handoff` each run one. `gitleaks` is the program two of them use.

**Shell, or bash**
The program inside a terminal that reads what you type and runs it. `bash` is the most common one. Some skills here ship shell scripts.

**Skill**
A short set of written instructions that teaches Claude Code how to do one specific job. A skill is a plain text file, not a program. You do not run it yourself. Claude Code reads it when the job comes up.

**SKILL.md**
The file a skill lives in. You will find it at `plugins/<pack>/skills/<skill>/SKILL.md` in this repository, and you can read any of them in your browser before installing anything.

**Slash command**
Text you type in Claude Code that begins with `/`. It runs something directly instead of asking Claude to work out what you meant. `/plugin install` is one. So is `/consistency-checker:spec-artifact-diff`.

**Terminal**
The window where you type commands instead of clicking. On a Mac it is called Terminal. On Windows it is usually Windows Terminal or PowerShell. You start Claude Code from there, and once it is running you type into Claude Code, not into the terminal itself. That difference matters: every install command here goes into Claude Code.

**Token**
The unit that Claude Code's reading and writing is counted in, roughly a short word or part of one. Both what a conversation costs and how much can be held at once are measured in tokens.

**Transcript**
The saved record of a past Claude Code conversation, kept on your computer. `retro`, `skill-discovery` and the `transcript-scanner` agent read them.

**Version**
A number such as `1.0.0` on a pack. It goes up when the pack changes, and Claude Code uses it to tell whether an update is waiting.

**wrangler**
Cloudflare's command line tool for their hosting service. `cloudflare-pages-migration` runs it through `npx`.

## Where to next

- [skill-library](../README.md), the main page, with the list of packs.
- [how-a-skill-works.md](how-a-skill-works.md), what happens when a skill runs.
- [which-pack.md](which-pack.md), which pack to install.
- [install-help.md](install-help.md), when something goes wrong.
