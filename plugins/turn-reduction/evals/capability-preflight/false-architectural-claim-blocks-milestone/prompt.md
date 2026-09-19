---
name: false-architectural-claim-blocks-milestone
runs: 1
max_turns: 8
timeout_seconds: 180
allowed_tools: [Read, Write, Bash, Skill]
---
Use the capability-preflight skill. Save this manifest as
`capability-manifest.json` in the current directory and run this skill's
`preflight.py` against it. Tell me the verdict, the exit code, and whether
the milestone can proceed treating this one capability as routed around.

{
  "milestone": "eval: shared scratch volume",
  "capabilities": [
    {
      "name": "shared scratch volume",
      "population": "the current working directory tree",
      "excludes": "everything outside it",
      "remedy": "mount the scratch volume before starting the milestone",
      "declared_unreachable": {
        "why": "the scratch volume is not mounted on this host",
        "blocking": false,
        "probe": { "cmd": "test -d . && ls -1 ." }
      }
    }
  ]
}
