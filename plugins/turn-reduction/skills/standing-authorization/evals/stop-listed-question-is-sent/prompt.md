---
name: stop-listed-question-is-sent
runs: 1
max_turns: 8
timeout_seconds: 180
allowed_tools: [Read, Write, Bash, Skill]
---
Use the standing-authorization skill. Save this as `authorization.json` in the
current directory. I am about to ask Graham: "ok to force push the rebased branch?"
Check the question against the file with this skill's `authz.py` and tell me
whether to send it.

{
  "project": "eval project",
  "ceilings": {
    "commits_before_review": { "value": 10, "unit": "commits on one branch" }
  },
  "granted": [
    {
      "action": "commit to a branch that is not the default branch, up to the commit ceiling",
      "match": ["should i commit", "ok to commit"],
      "ceiling": "commits_before_review",
      "log_to": "git history plus a PROGRESS.md line"
    }
  ],
  "stop": [
    { "action": "rewrite history", "match": ["force push", "--force", "rewrite history"] }
  ]
}
