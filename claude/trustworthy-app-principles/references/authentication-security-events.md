# Authentication Security Event Logging

Use this pattern when adding login history, security analytics, abuse detection, or an administrator-facing authentication audit trail.

## Model events, not a mutable login-history row

Prefer an append-only `auth_security_events` stream. A minimal durable shape is:

```text
id
occurred_at
event_type
user_id                     nullable
identifier_fingerprint      nullable
success
failure_code                nullable
auth_method
ip_fingerprint              nullable
ip_prefix                    optional
user_agent                   nullable
session_id                   nullable
request_id                   nullable
metadata                     constrained JSON
```

Recommended event names include:

- `auth.login.succeeded`
- `auth.login.failed`
- `auth.logout`
- `auth.password_reset.requested`
- `auth.password_reset.completed`
- `auth.email_verified`
- `auth.session.revoked`
- `auth.mfa.succeeded` / `auth.mfa.failed`

## Identity rules

- Use the provider's immutable user UUID for successful authenticated events; usernames and email addresses can change.
- Keep `user_id` nullable because failed attempts may target nonexistent accounts.
- When correlation is needed before authentication, normalize the submitted identifier and store an HMAC fingerprint rather than duplicating the plaintext identifier.
- Never expose whether the account exists in the browser response. Store precise internal failure categories while returning a neutral public message.

## IP-address privacy

Do not retain raw IP addresses indefinitely.

- Derive the client address only through the deployment's configured trusted proxy boundary. Do not blindly trust an arbitrary `X-Forwarded-For` chain.
- For long-lived correlation, store `HMAC-SHA256(normalized_ip, dedicated_pepper)`.
- Optionally retain a truncated network prefix for coarse investigation.
- If incident response requires raw IPs, encrypt them and apply a short explicit retention period, then delete them while keeping the nonreversible fingerprint.
- Keep the HMAC pepper server-only and separate from public environment variables.

## Authorization and integrity

- Insert events only from trusted server code or a narrowly scoped database function.
- Deny direct writes to anonymous and ordinary authenticated clients.
- Make the stream append-only in normal operation; corrections should themselves be auditable.
- Restrict reads to a dedicated permission such as `security.audit.read`.
- Do not place secrets in `metadata`. Never log passwords, attempted passwords, access tokens, refresh tokens, OTPs, recovery links, cookies, or authorization headers.
- Constrain metadata keys and size so the event table does not become an uncontrolled log sink.

## Useful indexes

Index `(user_id, occurred_at desc)`, `(ip_fingerprint, occurred_at desc)`, and `(identifier_fingerprint, occurred_at desc)`. A partial time index for `success = false` helps abuse investigations. Avoid indexing unnecessary plaintext PII.

## Detection patterns

Alert or surface review queues for:

- many failures against one identifier;
- one IP fingerprint targeting many identifiers;
- a success immediately following repeated failures;
- privileged-account login from a previously unseen fingerprint;
- repeated recovery or MFA failures;
- impossible event sequences, such as a password-change success without a valid recovery or reauthentication event.

Detection should complement—not replace—rate limiting, provider-side audit logs, MFA, session revocation, and compromised-password controls.

## Retention and user access

Define retention by data sensitivity and operational need. Raw or reversible network data should generally have the shortest lifetime; pseudonymous aggregate/security fingerprints may live longer when justified. Document the purpose, apply automatic deletion, and include the table in privacy/export/deletion policy decisions.

When the product owner sets an absolute maximum such as six months, enforce it in multiple layers:

1. derive `expires_at` in trusted code or the database rather than accepting an arbitrary caller value;
2. add a database constraint requiring `expires_at <= occurred_at + interval '6 months'`;
3. hard-delete where `expires_at <= now()` from an authenticated scheduled job;
4. test both boundary rejection and cleanup transactionally.

Do not add a legal-hold or preservation flag that can silently exceed an explicitly absolute product limit. A Git branch does not isolate a database: develop migrations in a local, preview, or disposable Supabase environment and review them before production application.

If users can see their own login history, show useful human-readable details without exposing internal fingerprints, failure intelligence, or other users' events.

## Existing business audit table versus a separate auth stream

Inventory the current audit model before creating a table, but do not force authentication telemetry into it merely to avoid “two places to look.” Prefer a separate auth-security stream when failed attempts have no actor/workspace, require identifier/IP fingerprints, need a shorter retention policy, have different read privileges, or can spike under attack. Existing workspace audit tables remain appropriate for attributable business operations such as payment approvals and role changes.

A unified investigation experience can query both streams or correlate them by user/request ID. Schema separation is often safer than mixing anonymous attack telemetry into tenant-scoped business history. Reuse an existing permission only after checking who receives it; a broad business `audit.read` grant may be too permissive for authentication intelligence.

## Reuse before reimplementation

Before adding a new pepper or IP parser, inspect existing abuse-control utilities. Reuse or extract established HMAC normalization, domain separation, trusted-proxy selection, IP validation, and canonicalization. Verify actual API fit: a private digest limited to `ip | email`, an `"unknown"` sentinel, or a rate-limit-only domain is a foundation—not proof that the auth-event writer already exists. Keep the writer server-only, metadata allowlisted, and logging best-effort so observability cannot break valid authentication.

Rate limiting and security logging are complementary. Rate limiting prevents or slows abuse; event logging supports detection, correlation, incident reconstruction, and verification that controls activated. Provider logs are also complementary because application telemetry may miss direct Auth API calls, while provider logs may miss local validation, CAPTCHA, membership, redirect, and post-login application outcomes.

## Launch sequencing and test strategy

Do not automatically fan comprehensive instrumentation across every auth path immediately before launch. First ask what incident-response question the feature answers and compare that value with regression risk. For a newly launched commerce or enrollment site, a real browser-level journey—fresh signup, email verification, login, registration, payment evidence, admin approval, account status, and delivered email—is often a higher-value release gate than a full auth dashboard.

If provider logs are accessible and the end-to-end journey passes, it can be reasonable to defer the comprehensive system. A minimal privileged-auth slice may still be justified when there is a concrete detection need. Build comprehensive coverage afterward in a feature branch plus an isolated database.

Do not equate “no package.json test script” with “no tests.” Inventory SQL contract suites, transactional rollback tests, Node harnesses, and local Supabase configuration. Prefer:

- transactional SQL tests for schema constraints, RLS, ACLs, append-only behavior, and retention;
- unit tests for normalization, HMAC domain separation, sanitization, and failure mapping;
- a small number of hosted Auth integration probes only for provider behavior that cannot be simulated locally;
- no destructive or debris-prone testing against production.

Tests that clean up in `finally` are useful but not equivalent to transaction rollback; a process crash can still leave hosted debris.

## Credential handling during review

If a user pastes a live provider token while asking only for an opinion, do not use it merely because it is available. Treat it as exposed, advise immediate revocation/rotation, avoid repeating it, and continue with repository evidence when sufficient. Do not create a branch or connect to production when the latest instruction explicitly says not to implement.

## Audit checklist

- [ ] Immutable user UUID is used where available; mutable username/email is not the primary identity.
- [ ] Failed attempts can be recorded without inventing a user relation.
- [ ] Public failure messages prevent account enumeration.
- [ ] IP handling respects trusted proxies, minimization, and retention.
- [ ] Event inserts are server-only and records are append-only.
- [ ] The existing business audit schema was evaluated; auth events are separated when actor/workspace, retention, volume, or access semantics differ.
- [ ] Audit reads require an explicit administrative permission whose current role grants were inspected.
- [ ] Existing HMAC/IP utilities are reused or extracted only after verifying their actual API and sentinel behavior.
- [ ] No credentials, tokens, OTPs, cookies, or raw auth headers are logged.
- [ ] Request/session correlation exists without turning logs into a secret store.
- [ ] Retention and deletion are automated, database-constrained, documented, and cannot exceed an explicit absolute maximum.
- [ ] The Git branch is paired with an isolated non-production database for migration and destructive testing.
- [ ] SQL/unit/integration tests are chosen by boundary; production is not used as a disposable test target.
- [ ] Logging is distinguished from rate limiting and provider logs rather than presented as a replacement for either.
- [ ] Alerts cover credential stuffing, account targeting, recovery abuse, and privileged logins.
