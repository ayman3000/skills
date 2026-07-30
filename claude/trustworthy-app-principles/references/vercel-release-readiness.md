# Vercel Release-Readiness Audit for Next.js + Supabase

Use this reference when the user asks whether a database-backed Next.js application is ready for Vercel. The audit is read-only unless the user explicitly requests remediation.

## 1. Preserve the source tree

- Record `git status`, current commit, remotes, and branch tracking before testing.
- If the user says “review without modifying,” do not build or install in the working repository. Clone every claimed publication repository into a temporary directory.
- Compare commit and tree hashes. Two remotes having similar names is not proof they contain the same release.
- Run tests in the fresh clone and remove temporary clones/processes afterward.
- Recheck the original working tree at the end.

## 2. Repository and release provenance

For each repository, verify:

- visibility and default branch;
- the remote `main` commit matches the reviewed commit;
- no `.env`, build output, dependency directory, or service-role credential is tracked;
- CI workflows and branch protection exist or are explicitly noted as absent;
- one repository is designated canonical for the production Vercel project.

Do not connect duplicate mirror repositories to competing production projects for one domain. Keep mirrors synchronized explicitly, but let Vercel track one canonical source.

## 3. Fresh-install reproducibility

Use the strict installer first:

```bash
npm ci
npm run lint
npx tsc --noEmit
npm run build
```

If `npm ci` fails but `npm install` succeeds, the build is not reproducible. A permissive host installer may mask a stale lockfile; that is a release blocker, not evidence of readiness. Regenerate and commit the lockfile, then repeat the strict fresh-clone sequence.

A zero-exit Next.js build is necessary but not sufficient. Read the complete build log for swallowed data/configuration errors such as `getSiteSettings failed`, `getCollection failed`, or generic fallback rendering. Run two clearly labeled passes when practical:

1. **Strict clone pass without private environment files** — proves install/compile reproducibility and reveals whether missing configuration is honestly surfaced.
2. **Configured isolated pass** — copy the existing environment into the temporary clone without printing secrets, then rebuild to verify the real data path. Remove the copied environment file afterward.

If the configured build logs a CMS/database error but still exits successfully, report the build as compiled with a data-path warning—not fully clean. Do not let fallback HTML turn a failed production read into release evidence.

Also record:

- production-only dependency audit findings;
- the Node version used locally;
- whether `engines.node` or the Vercel project runtime pins a compatible major;
- the framework’s minimum supported Node version.

Never apply a forced audit fix blindly when it proposes a framework downgrade or unrelated major change.

## 4. Runtime and route QA

Test a production server from the fresh build:

- public routes, detail routes, auth pages, account redirects, admin redirects, and 404s;
- dark and light themes;
- browser console errors;
- external-link protocols and targets;
- honest empty states;
- CTA destinations (a primary CTA must not lead to an empty catalog when a real offering exists elsewhere);
- custom error and loading behavior;
- warm response times for representative routes.

For streamed Next.js routes, do not classify a route from HTTP status or raw HTML alone. A response can contain a loading shell, an embedded not-found boundary, and later streamed content in one document. Inspect the settled browser DOM and visible route state. Conversely, a raw `200` is not proof that meaningful content rendered. When testing suspected unpublished-content exposure, verify the final heading/status/body in a browser rather than matching fallback text in the response source.

Review visible content as release data, not only code. Directional copy (“above”/“below”), malformed Markdown quotes, TBD dates, and obsolete footer claims can undermine an otherwise correct deployment.

## 5. Supabase and database release path

Verify both current production state and replayability:

- required RPCs, views, buckets, and migrations exist in production;
- the full migration chain replays against a fresh provider-compatible database;
- SQL test suites pass;
- important migrations are idempotent where reruns are expected;
- production catalog counts and classifications match the product model;
- service-role RPCs are not executable by public roles.

Trace view semantics before reporting a public-content leak. A helper named `published_content` may itself restrict rows to `published` and intentionally direct-linkable `unlisted` records. A detail query that lacks an extra `.eq("status", "published")` does **not** automatically expose drafts or archived records if the underlying view excludes them. Inspect the actual `CREATE VIEW`, distinguish `unlisted` semantics from draft/archive exposure, query the live status distribution read-only, and verify the settled browser route. Treat delegated audit findings as hypotheses until this full path is checked.

When checking operational readiness through the live REST API, summarize only non-sensitive state—counts, lifecycle statuses, active method codes, cohort dates/capacity, and outbox result counts. Never print service-role keys, recipient identifiers, payment destinations, or user IDs in the report.

A bare PostgreSQL image may lack Supabase-managed `auth` or `storage` schemas. Add only the provider compatibility fixtures needed by the harness, and report that adaptation separately. Do not mislabel a missing managed schema as an application migration defect.

### Multi-currency rule

Never sum minor units from different currencies into one headline total. Return per-currency totals or convert using a recorded exchange rate. A currency breakdown does not make an invalid combined headline safe.

## 6. Authentication and secrets

Inspect not just whether secrets exist, but whether fallback paths are active.

- A legacy shared-password admin path is unsafe when its activation condition is currently true, even if a stronger membership system also exists.
- Verify a real owner membership works before removing the fallback.
- Do not copy a weak local legacy password to Vercel. Prefer disabling the fallback and using Supabase membership/RBAC.
- Production and Preview should use separate secrets. Ideally Preview uses a staging Supabase project; do not casually expose the production service-role key to branch previews.
- `SUPABASE_SERVICE_ROLE_KEY` must never have a `NEXT_PUBLIC_` prefix.
- Rotate any credential that was shared or found weak; never print its value in the audit report.

Verify Supabase Auth Site URL and allowed callback URLs for the canonical production domain and exact preview environment.

## 7. Security and platform configuration

Check for explicit application headers:

- Content Security Policy / `frame-ancestors`;
- `X-Content-Type-Options`;
- Referrer Policy;
- Permissions Policy;
- clickjacking protection.

The hosting platform may provide HTTPS/HSTS, but it does not design an application-specific CSP.

For Vercel:

- use the canonical private GitHub repository;
- pin a tested Node major in Project Settings or `package.json`;
- place functions near the Supabase region;
- configure Production and Preview environments separately;
- deploy Preview first, then promote only after auth, email, registration, admin, cache invalidation, and rate-limit tests pass.

## 8. Domain cutover with external DNS and email

When DNS is hosted outside Vercel:

1. Add apex and `www` in Vercel.
2. Use the exact records Vercel displays; do not guess records that may change.
3. Add only the website records in the existing DNS provider.
4. Preserve SES/DKIM/SPF/DMARC/custom-MAIL-FROM records.
5. Choose one canonical host and redirect the other.
6. After DNS and TLS succeed, update Supabase Auth Site URL/callbacks and repeat real-domain email tests.

## 9. Verdict format

Give two separate decisions:

- **Preview readiness** — can the host build and safely exercise the app?
- **Production readiness** — are auth, secrets, financial semantics, domain callbacks, and launch UX safe?

Rank findings:

- **Blocker:** reproducibility failure, active weak auth fallback, exposed secret, invalid financial reporting, broken migration/build.
- **Before paid traffic:** latent commerce/accounting defect or incomplete payment/auth flow.
- **Before public announcement:** wrong CTA, visibly malformed copy, missing canonical domain setup.
- **Follow-up:** CI, branch protection, dependency warnings, and polish.

A successful permissive build is not enough to declare production readiness.