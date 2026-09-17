# Cloud and infrastructure security: FAIL and PASS patterns

Reference for `security-checklist`. Most rows here describe the state of an account, not
of a repository, so many will come out **NOT VERIFIABLE from the code**. Say so and name
the read-only command or console page that shows it. Every change to IAM, a secrets
manager, MFA or a network rule is the user's to make (see the stop gate in `SKILL.md`);
infrastructure with real blast radius goes through `turn-reduction:plan-gate` first.

## 1. IAM and access

```json
// FAIL: everything on everything
{ "Effect": "Allow", "Action": "*", "Resource": "*" }

// PASS: the actions needed, on the resource needed
{ "Effect": "Allow", "Action": ["s3:GetObject"], "Resource": "arn:aws:s3:::app-assets/*" }
```

- [ ] No wildcard action on wildcard resource in any policy in the repo
- [ ] Workloads use roles, not long-lived access keys
- [ ] Root is not used for operations (not verifiable from code: `aws iam get-account-summary`)
- [ ] MFA on privileged accounts (not verifiable from code; the user checks and enables)
- [ ] Unused credentials are removed on a schedule (user action)

Note: `sts:GetCallerIdentity` succeeding proves identity, not authorization.

## 2. Secrets in the cloud

- [ ] Secrets are in a secrets manager or the platform's encrypted settings, referenced by name in templates
- [ ] No secret value in a template, a parameter default, a CI variable printed to logs, or an error message
- [ ] Rotation is configured for database credentials (not verifiable from code unless the template declares it)
- [ ] Access to secrets is audit-logged

Finding a secret in a template is a hard stop. Rotation is the fix and the user performs it.

## 3. Network

```yaml
# FAIL: database port open to the internet
- IpProtocol: tcp
  FromPort: 5432
  ToPort: 5432
  CidrIp: 0.0.0.0/0

# PASS: only from the application's security group
- IpProtocol: tcp
  FromPort: 5432
  ToPort: 5432
  SourceSecurityGroupId: !Ref AppSecurityGroup
```

- [ ] No data store is publicly accessible (`PubliclyAccessible: false`; no public bucket policy)
- [ ] SSH and RDP are not open to `0.0.0.0/0`
- [ ] Security groups allow the specific ports and sources needed
- [ ] Flow logs are enabled where the platform offers them

## 4. Logging and monitoring

- [ ] Logging is enabled for every service in the template, with a retention period set on purpose
- [ ] Failed authentication and admin actions are logged
- [ ] At least one alarm exists for something a human would want to know about
- [ ] Logs cannot be deleted by the workload that writes them

## 5. CI/CD

```yaml
# PASS: short-lived credentials by OIDC, minimal permissions, pinned actions
permissions:
  id-token: write
  contents: read
steps:
  - uses: aws-actions/configure-aws-credentials@<pinned-sha>
    with:
      role-to-assume: arn:aws:iam::<account>:role/deploy
```

- [ ] CI authenticates by OIDC, not stored long-lived keys
- [ ] Workflow `permissions` are declared and minimal
- [ ] Third-party actions are pinned to a commit
- [ ] A secret scan and a dependency audit run in the pipeline
- [ ] The default branch is protected and review is required (not verifiable from code: `gh api repos/<owner>/<repo>/branches/<branch>/protection`)

## 6. CDN and edge

- [ ] TLS is strict end to end
- [ ] Managed WAF rules and rate limiting are on (not verifiable from code unless declared)
- [ ] Security headers are set at the edge or the origin, and the two do not conflict

## 7. Backups and recovery

- [ ] Automated backups with a retention period are declared for every stateful resource
- [ ] Point-in-time recovery is on where offered
- [ ] A restore has actually been performed and timed. A backup that has never been restored is unverified.
- [ ] Deletion protection or a retain policy is set on stateful resources

## Common misconfigurations to search for

```bash
# read-only searches over templates
grep -rn "0.0.0.0/0" .
grep -rn -i "PubliclyAccessible: *true" .
grep -rn '"Action": *"\*"' .
grep -rn -i "BlockPublic.*false" .
```

## Pre-deployment summary

IAM, secrets, network, logging, monitoring, CI/CD, CDN and WAF, encryption at rest and in
transit, backups, compliance obligations if any apply, runbooks, an incident plan. Each
is PASS, FAIL or NOT VERIFIABLE with evidence. Anything the agent could not see is
listed, not assumed.
