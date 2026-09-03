# Repo handoff checklist

Mirror of the SKILL.md gates. Every box is proven by a recorded command and its
output, not by a checkmark.

## Preflight

- [ ] Recipient named; destination account ruled by Graham (theirs, or his with them as collaborator)
- [ ] Identifier list shown to Graham and confirmed (name, employer, phone, email, league and team names, account ids, named file classes)
- [ ] `command -v gitleaks` prints a path

## Inventory

- [ ] Every identifier grepped in the working tree and in history (`git log --all -S`)
- [ ] Every file in one bucket: shareable, sanitize, exclude
- [ ] Copyrighted media and transcripts are in exclude, whatever their format

## Cut

- [ ] Clean commit extracted with `git archive`, or sanitized subset copied to a fresh directory
- [ ] Graham's history does not travel (new `git init` in the delivered tree)

## Sanitize

- [ ] Hardcoded specifics moved to a config the recipient fills in
- [ ] The generator was edited, not its outputs
- [ ] `.env.example` carries names only

## Prove clean (gate)

- [ ] Identifier grep on the delivered tree: every count 0, output recorded
- [ ] `gitleaks detect --source . --no-git --redact` exit 0, output recorded
- [ ] `find` for `.env`, `*.pem`, `credentials*`, `*.tfvars` empty
- [ ] Any hit fixed and all three rerun before continuing

## Repo

- [ ] Created private; `gh repo view --json visibility` recorded
- [ ] Graham's original `origin` untouched
- [ ] `upstream` added when the source was a fork of a public framework

## Walkthrough (gate)

- [ ] `AGENT-WALKTHROUGH.md` written in the delivered tree
- [ ] Every command in it executed against the delivered tree; outputs pasted; figures match the doc
- [ ] Three recipient prompts included: run it, extend it, debug it

## Report

- [ ] URL and visibility, exclude list with reasons, clean-proof output, walkthrough run, recipient-supplied items

## Patterns that caught the misses (2026-08-28 to 2026-09-02)

- A public fork was about to receive personal data: check `gh repo view --json visibility,isFork` before the first write, and privatize or re-point first.
- A second user's copy had to start before the owner's data entered history: `git log --all -S'<name>'` found the single commit that introduced it, and the tree before it was extracted and grepped to zero hits.
- A handoff doc stated a dataset depth of "about 225" where the real values were 267, 225, and 218: running the doc's own commands caught it. Never deliver a walkthrough you have not executed.
- Exit codes lie in pipelines: a trailing `grep -c` or `[ ... ]` returns 1 on a benign zero match. Read the output, not only the code.
