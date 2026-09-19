---
name: unreachable-live-state-becomes-assumption
runs: 1
max_turns: 12
timeout_seconds: 300
allowed_tools: [Read, Write, Bash, Skill]
---
Use the plan-gate skill. Save the FIXTURE Terraform below as `s3.tf` in the current
directory, then plan the change I describe. Do not ask me anything and do not edit `s3.tf`.

FIXTURE `s3.tf` (invented for this exercise; the bucket and account are not real):

```hcl
resource "aws_s3_bucket" "archive" {
  bucket = "acme-archive-prod"
}

resource "aws_s3_bucket_versioning" "archive" {
  bucket = aws_s3_bucket.archive.id
  versioning_configuration {
    status = "Enabled"
  }
}
```

The change: expire objects under `exports/` in that bucket after 90 days. This machine
has no AWS sign-in and no network, and I am not going to give you one. Check the live
state for yourself the way the skill tells you to, then give me the plan and stop.
