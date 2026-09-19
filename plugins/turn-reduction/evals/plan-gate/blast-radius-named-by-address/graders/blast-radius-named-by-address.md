---
type: regex
pattern: "Blast radius|blast radius"
match: contains
---

Tests `SKILL.md:84`: "**Blast radius**: what gets replaced vs. updated in place, and what
a replacement takes down with it. Name the resources that will be destroyed and recreated,
by address." Line 82 requires this label to be stated explicitly for an infrastructure
change rather than folded into Environment, and line 115 calls out `count` reindexing as
the case where the destruction does not look like one in the diff. Removing the middle
element of a `count` list reindexes `aws_sqs_queue.work[1]` and `[2]`, so the labelled
section is where the destroy and recreate has to be named.
