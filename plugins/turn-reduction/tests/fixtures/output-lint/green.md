Approve the staging migration, or say which table to hold back.

Everything below has already been run against the staging copy; nothing has been run
against production.

The schema diff came back with 4 files changed, from `git diff --name-only staging | wc -l`:

- `schema/accounts.sql`
- `schema/entitlements.sql`
- `schema/sessions.sql`
- `schema/audit_log.sql`

To reproduce, from the repo root:

```bash
cd ~/work/GitHub/example-project
./scripts/schema-diff.sh --target staging
git diff --stat staging
```

The row-count reconciliation ran as Python, tagged as Python:

```python
import csv

with open("out/reconciliation.csv") as handle:
    rows = list(csv.DictReader(handle))
print(len(rows), "rows reconciled")
```

Recursive matching used ripgrep's own glob, quoted so the shell leaves it alone:

```bash
cd ~/work/GitHub/example-project
rg --files -g "**/*.sql" schema
```

Staging is reconciled and the diff is attached above. Production is untouched and stays
untouched until you answer.
