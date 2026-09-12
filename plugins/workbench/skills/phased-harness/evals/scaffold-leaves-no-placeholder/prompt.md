---
name: scaffold-leaves-no-placeholder
runs: 1
max_turns: 14
timeout_seconds: 300
allowed_tools: [Read, Write, Bash, Skill]
---
Use the phased-harness skill to scaffold a harness into `./eval-harness/` in the
current directory. The interview is already answered; do not ask me anything.

1. End state and invariant: every page on the docs site is served from exactly
   one source file; the old mirror directory no longer exists.
2. Irreversible step: deleting the mirror directory and pushing the removal.
3. Standing authorizations: create the work branch, commit on it, run the build
   and the link checker, edit files under docs/.
4. Never pre-authorized: the deletion, any push, any edit outside docs/.
5. Phases: 0 survey (read-only): list every page and its sources, done when the
   list is written; 1 decision gate (Gate A): Graham picks the canonical source
   per page; 2 execution: rewrite links to the canonical source, done when the
   link checker passes; 3 verification: build and check, done when the build is
   green and no page references the mirror; 4 irreversible finish (Gate B):
   delete the mirror and push.
6. Project directory: ./eval-harness
7. Graham's decisions alone: the canonical source per page; the deletion.
8. Parameters: repo path /tmp/docs-site (does not need to exist for scaffolding),
   branch docs-consolidate, link checker `npm run check-links`.

After scaffolding, run the placeholder grep the skill's Verify section describes
and show its output.
