---
name: negative-control-that-passes-is-not-proven
runs: 1
max_turns: 8
timeout_seconds: 180
allowed_tools: [Read, Write, Bash, Skill]
---
Use the capability-preflight skill. Save this manifest as
`capability-manifest.json` in the current directory and run this skill's
`preflight.py` against it. Report the verdict and the exit code, and say what the
negative control proved or failed to prove.

{
  "milestone": "eval: scratch directory access",
  "capabilities": [
    {
      "name": "scratch directory",
      "population": "files under the current working directory",
      "excludes": "anything outside it",
      "remedy": "create the directory and grant write access",
      "read":  { "cmd": "ls -1 . | wc -l", "evidence": "count>0" },
      "write": { "cmd": "printf x > .probe && cat .probe && rm .probe", "evidence": "contains:x" },
      "negative_control": {
        "cmd": "ls -1 .",
        "expect": "nonzero_exit",
        "why": "listing the same directory succeeds, so this control cannot fail"
      }
    }
  ]
}
