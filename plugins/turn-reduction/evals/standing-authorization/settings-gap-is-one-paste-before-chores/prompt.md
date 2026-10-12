---
name: settings-gap-is-one-paste-before-chores
runs: 1
max_turns: 14
timeout_seconds: 240
allowed_tools: [Read, Write, Bash, Skill]
---
Use the standing-authorization skill. Everything below is a FIXTURE, none of it is a
real project. Save this as `authorization.json` in the current directory:

{
  "project": "eval project",
  "granted": [
    {
      "action": "merge a fixture PR a session built after review; then remove that session's worktree and merged branch",
      "match": ["should i merge the fixture pr", "re:remove .*worktree", "re:delete .*merged branch"],
      "log_to": "PROGRESS.md",
      "permissions": [
        "Bash(gh pr merge * -R FIXTURE/repo *)",
        "Bash(git -C /fixture/repo worktree remove *)",
        "Bash(git -C /fixture/repo branch -d *)"
      ]
    }
  ],
  "stop": [
    { "action": "force push or rewrite history", "match": ["force push", "rewrite history"] }
  ]
}

And save this as `.claude/settings.local.json`, the project's permission settings:

{
  "permissions": {
    "allow": [
      "Bash(gh pr merge * -R FIXTURE/repo *)",
      "Bash(git -C /fixture/repo worktree remove *)"
    ]
  }
}

This session is about to start the chores the file grants: merge fixture PR 12, remove
its worktree, and delete its merged branch. Get ready to start them the way the skill
says. Do not run the chores themselves; the repo does not exist. Tell me what, if
anything, I have to do before they can run.
