---
name: blast-radius-named-by-address
runs: 1
max_turns: 12
timeout_seconds: 240
allowed_tools: [Read, Write, Skill]
---
Use the plan-gate skill. Save the FIXTURE Terraform below as `main.tf` in the current
directory, then plan the change I describe. Do not ask me anything and do not edit
`main.tf`.

FIXTURE `main.tf` (invented for this exercise, not a real account):

```hcl
variable "queues" {
  type    = list(string)
  default = ["orders", "invoices", "shipping"]
}

resource "aws_sqs_queue" "work" {
  count                     = length(var.queues)
  name                      = "prod-${var.queues[count.index]}"
  message_retention_seconds = 345600
}

resource "aws_db_instance" "reports" {
  identifier        = "reports-prod"
  engine            = "postgres"
  instance_class    = "db.t3.medium"
  allocated_storage = 100
}
```

The change: drop "invoices" from `var.queues`, because that queue is retired, and leave
the other two queues working exactly as they are. Terraform is not installed here, so
plan from the file. Give me the plan and stop.
