---
name: swallowed-failure-rejected-before-run
runs: 1
max_turns: 8
timeout_seconds: 180
allowed_tools: [Read, Write, Bash, Skill]
---
Use the capability-preflight skill. Save this manifest as
`capability-manifest.json` in the current directory, run this skill's
`preflight.py` against it, and tell me the exit code and what happened.

{
  "milestone": "eval: manifest with a swallowed failure",
  "capabilities": [
    {
      "name": "scratch directory",
      "population": "files under the current working directory",
      "excludes": "anything outside it",
      "remedy": "create the directory and grant write access",
      "read":  { "cmd": "ls -1 ./missing-dir || true", "evidence": "nonempty" },
      "write": { "cmd": "printf x > .probe && cat .probe && rm .probe", "evidence": "contains:x" },
      "negative_control": {
        "cmd": "ls -1 ./nope",
        "expect": "nonzero_exit",
        "why": "a sibling path that does not exist must fail"
      }
    }
  ]
}
