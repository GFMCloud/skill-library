# Application security: FAIL and PASS patterns

Reference for `security-checklist`. Examples are TypeScript and SQL because that is what
the source used; the patterns hold in any language. Every row is a question to answer
from the code, not an instruction to change anything. Remediation goes through the stop
gate in `SKILL.md`.

## 1. Secrets

```typescript
// FAIL: a secret in source
const apiKey = "sk-live-...";

// PASS: read from the environment, fail loudly when absent
const apiKey = process.env.PAYMENTS_API_KEY;
if (!apiKey) throw new Error("PAYMENTS_API_KEY not configured");
```

- [ ] No key, token or password literal in source, config, fixtures or examples
- [ ] Secret files (`.env*`) are ignored by git, and the ignore rule is not the only check: the history was scanned
- [ ] A missing secret stops startup with a named error, never a silent default
- [ ] Production secrets live in the platform's secret store

If a real secret is found: stop. Report the location, not the value. Rotation is the
remediation and it is the user's to perform.

## 2. Input validation

```typescript
// PASS: schema first, allow-list, typed result
const CreateUser = z.object({
  email: z.string().email(),
  name: z.string().min(1).max(100),
});
const input = CreateUser.parse(body); // throws on anything else
```

File uploads: check size, MIME type and extension, all three, against an allow-list.

- [ ] Every external input (body, query, headers, files, webhooks) passes a schema before use
- [ ] Allow-list, not block-list
- [ ] Uploads limited by size, type and extension
- [ ] Validation errors do not echo internals

## 3. Injection

```typescript
// FAIL: string-built SQL
db.query(`SELECT * FROM users WHERE email = '${email}'`);

// PASS: parameters
db.query("SELECT * FROM users WHERE email = $1", [email]);
```

- [ ] Every query is parameterized or goes through a query builder used as designed
- [ ] No user input concatenated into SQL, shell commands, file paths or templates
- [ ] A command-line argument from a user is validated to a type (an integer, an enum) before it reaches a shell

## 4. Authentication and authorization

```typescript
// FAIL: token readable by any script on the page
localStorage.setItem("token", token);

// PASS: cookie the page's scripts cannot read
res.setHeader("Set-Cookie", `token=${token}; HttpOnly; Secure; SameSite=Strict; Max-Age=3600`);
```

```typescript
// PASS: authorization decided before the sensitive operation, server side
if (requester.role !== "admin") return forbidden();
await db.users.delete({ where: { id } });
```

```sql
-- PASS: row-level security, for databases that support it
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
CREATE POLICY users_select_own ON users FOR SELECT USING (auth.uid() = id);
```

- [ ] Session tokens are not in script-readable storage
- [ ] Every sensitive operation checks authorization on the server, before acting
- [ ] Row-level or tenant-level isolation is enforced in the data layer, not only the UI
- [ ] Sessions expire and can be revoked

## 5. XSS

```typescript
// PASS: sanitize user HTML to a small allow-list before rendering it
const clean = DOMPurify.sanitize(html, { ALLOWED_TAGS: ["b", "i", "em", "strong", "p"], ALLOWED_ATTR: [] });
```

A strict Content-Security-Policy: `default-src 'self'; base-uri 'self'; object-src
'none'; frame-ancestors 'none'; script-src 'self'; style-src 'self'`. Treat
`'unsafe-inline'` and `'unsafe-eval'` as temporary debt with a written removal plan.

- [ ] User-provided HTML is sanitized before render
- [ ] CSP is set and does not rely on `unsafe-inline` or `unsafe-eval`
- [ ] No raw-HTML escape hatch (`dangerouslySetInnerHTML`, `v-html`, `|safe`) on unsanitized data

## 6. CSRF

- [ ] State-changing requests require a CSRF token (or the framework's equivalent)
- [ ] Cookies are `SameSite=Strict` or `Lax` with a stated reason
- [ ] No state change on GET

## 7. Rate limiting

```typescript
// PASS: a general limit, and a tighter one where a request is expensive
app.use("/api/", rateLimit({ windowMs: 15 * 60 * 1000, max: 100 }));
app.use("/api/search", rateLimit({ windowMs: 60 * 1000, max: 10 }));
```

- [ ] All public endpoints are limited
- [ ] Expensive operations (search, export, auth attempts) have tighter limits
- [ ] Limits apply per user when authenticated, per address otherwise

## 8. Sensitive data exposure

```typescript
// FAIL
console.log("login", { email, password });
return json({ error: err.message, stack: err.stack }, 500);

// PASS
console.log("login", { userId });
console.error("internal error", err);          // server log only
return json({ error: "Something went wrong." }, 500);
```

- [ ] No passwords, tokens, card data or personal data in logs
- [ ] Users see generic errors; detail stays in server logs
- [ ] No stack traces in responses

## 9. Dependencies

Read-only checks the reviewer may run: `npm audit`, `npm outdated`, `pip-audit`,
`pip list --outdated`. Commands that change the tree (`npm audit fix`, `npm update`) are
proposed actions, never run as part of the review.

- [ ] A lock file is committed and CI installs from it (`npm ci`, not `npm install`)
- [ ] The audit is clean, or each open advisory has a stated reason
- [ ] Automated update PRs are enabled (not verifiable from code alone: say where to look)

## Tests worth asking for

Four cheap tests that prove the controls exist: an unauthenticated request gets 401; a
non-admin token on an admin route gets 403; invalid input gets 400; request 101 in a
100-request window gets 429. If the repo has none of these, that is a finding.

## Pre-deployment summary

Secrets, input validation, injection, XSS, CSRF, authentication, authorization, rate
limiting, HTTPS enforced, security headers, error handling, logging, dependencies,
row-level security, CORS restricted to known origins, file uploads. Each is PASS, FAIL
or NOT VERIFIABLE with evidence; none is ticked from memory.

Further reading: OWASP Top 10 (owasp.org/www-project-top-ten), PortSwigger Web Security
Academy (portswigger.net/web-security).
