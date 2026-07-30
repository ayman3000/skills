---
name: trustworthy-app-principles
description: Audit and enforce trust-building principles for desktop and web applications — responsiveness, honest failure, cancellation, persistence, safe actions, and clear decision UX.
version: 2.0.0
---

# Trustworthy Application Principles

Ten principles derived from real AI-assisted development work, covering responsiveness, honest failure, cancellation, persistence, safe actions, and user-facing decision UX. Use this skill when building, auditing, or reviewing any application — desktop or web.

## When to use

- Before shipping a new feature, run the checklist below
- When auditing an existing codebase for trust issues
- When reviewing a PR that touches I/O, error handling, or user actions
- When designing a new screen or interaction flow
- When deciding whether a Next.js/Supabase application is ready for Vercel Preview or Production
- When the user requests a read-only release audit across one or more publication repositories
- When designing or auditing login history, authentication telemetry, abuse detection, or security-event retention

## The principles

### 1. Responsiveness is the product

Never block the UI on I/O or computation. The app should always feel instant.

- Offload genuinely heavy work to background tasks, web workers, or server functions
- Give immediate feedback without replacing real UI with generic loaders: render the stable shell, preserve existing data, and mark only the changing field
- Target < 100ms for perceived response; investigate any navigation over 1s before adding progress UI
- On web, treat streaming and Suspense as tools—not defaults. They are accepted only when production measurements show they improve first paint or interaction latency
- **Performance is a quality gate:** benchmark the existing path before refactoring and the production build afterward. A principle-driven refactor that makes navigation slower must be rolled back or redesigned

### 2. Render first, refine in the background

Show something useful immediately, then improve it progressively. Don't make users wait for perfect results.

- **Never use shimmering/pulse placeholders.** Render the actual layout immediately: static text, headings, labels, borders, buttons, table headers, card structure, icons, and all non-dynamic content. Users should see the real page, not a gray ghost of it. If a card has an icon and a label, render the icon and label — only the number waits. If a table has column headers, render the headers and borders — only the rows wait.
- Only dynamic data fields (numbers, rows, list items, chart values) should show a loading state — and that state should be a simple "Loading…" text or a small spinner next to the specific field, not a full-page skeleton.
- Show cached/stale data immediately only when it is already available **without adding a slower execution path**. Refresh in the background with a subtle "Updating…" badge.
- **Never move a fast Server Component query behind hydration + `useEffect` + a browser API request merely to add caching.** That adds an HTTP roundtrip, may repeat authentication, and makes first load slower. Prefer direct server rendering, request-scoped memoization, database aggregation, and mutation-driven invalidation.
- Before adding stale-while-revalidate, benchmark the current path and the proposed path in a production build. Caching is rejected if uncached first-load latency regresses.
- Scope any client cache by user and workspace, add a timestamp/TTL, deduplicate overlapping requests, clear it on logout, and do not poll unless genuinely live data is required.
- Never silently swap content — the user should know the first version was preliminary
- The page should look 90% complete on first paint; the remaining 10% is just the data filling in

### 3. Retry transient failures, fail fast on deterministic ones

Retry timeouts and temporary network issues. Don't keep retrying invalid credentials or broken configurations.

- Classify errors explicitly: transient vs deterministic — the error type should make this structural, not interpretive
- Retry strategy: exponential backoff, max 3 attempts, jitter
- Deterministic failures (401, 403, 400, validation errors): surface immediately with actionable message
- Never retry on auth errors, schema errors, or permission denials

### 4. Never fail silently

Every operation should end with either a result or a clear, actionable message. A permanent "Loading…" state is a bug.

- No empty catch blocks — if you swallow an error, log it AND surface it
- No functions that return `[]` or `null` on error without the caller knowing why
- Empty states must distinguish between "no data exists" and "data failed to load"
- Loading states must have timeouts — a spinner that never resolves is a silent failure
- Admin dashboards: show the error message, not an empty table

### 5. Honesty over completion

If something fails, say it failed. Never invent data, fake success, or pretend work was completed.

- Never substitute fabricated output for real results
- Never report "success" when an operation partially failed — report the partial state
- Never log "completed" when the process exited with errors
- If a dependency is unavailable, say so — don't pretend the feature works without it
- Tests that pass by not testing anything are worse than failing tests
- **Semantic honesty matters as much as data honesty.** Do not rename or merge product categories merely to fit the records currently available. A workshop is not a course because it was stored in a course collection; fix the taxonomy, route, and migration.
- Never seed fake public catalog cards to avoid an empty page. Show an honest empty state until real titles, destinations, and URLs are supplied.
- Preserve history when correcting classification: reclassify the real record, migrate dependent discriminators, archive placeholders, and retain redirects/foreign-key relationships.

### 6. Warn before irreversible or outward-facing actions

Delete, overwrite, send, or execute actions should require clear confirmation. Preview before applying changes.

- Make the warning proportional to the damage:
  - Low stakes (delete a draft): simple confirm
  - Medium stakes (overwrite unsaved work): confirm with preview
  - High stakes (send email to 1000 subscribers, execute shell on production): multi-step confirm showing exactly what will happen
- Never use generic "Are you sure?" — show the specific action and its target
- Irreversible actions should have a brief undo window where possible
- Outward-facing actions (emails, webhooks, payments) should show a preview of what the recipient will see

### 7. Long work is cancellable

Anything that might take more than a few seconds should provide a Cancel button and clean up properly when cancelled.

- Cancel must actually stop the work, not just hide the UI
- Cleanup: kill processes, close connections, remove partial files, release locks
- If cancellation is not possible, say so honestly — don't show a Cancel button that does nothing
- Background tasks should check for cancellation signals periodically
- On web: AbortController for fetch, clearTimeout for timers, unsubscribe from streams

### 8. State is the source of truth, not the UI

The UI reflects state, it doesn't own it. Every action updates a persistent or recoverable state first, then the UI reacts. If the app crashes, the user loses nothing.

- Separate state management from rendering — state store, then UI subscribes
- Form data should survive navigation away and back
- Don't store critical data only in component state — lift it to a store or persistence layer
- On web: use URL state for shareable views, localStorage/sessionStorage for drafts
- Optimistic updates: update UI immediately, but persist first or have a rollback plan

### 9. Persistence is a feature, not an afterthought

If the user entered data, it should survive a crash, a restart, or an accidental close. Auto-save is not a nice-to-have.

- Auto-save drafts every few seconds
- On desktop: persist window state, unsaved documents, and session context
- On web: persist in-progress forms to sessionStorage; restore on page reload
- Never rely on "don't close this tab" as a data-preservation strategy
- Migrations and schema changes must be reversible or at least non-destructive

### 10. Present numbered options with a recommended choice

When the app or agent offers the user a decision (action, configuration, recovery path, or any branching choice), present the options as a numbered list and mark one as recommended. The user should be able to pick by number or accept the recommendation.

- Number every option (1, 2, 3, …) — no wall of prose, no buried alternatives
- Mark exactly one as **recommended**, with a one-line rationale
- The recommended option must be the genuinely safest/best default for the user's context — not a guess
- Keep option text short and distinct; overlap between options defeats the purpose
- If new information arrives mid-choice, reissue the list rather than silently switching

## Audit checklist

Run this against any application before shipping:

- [ ] **Responsiveness**: Does every user action show feedback within 100ms?
- [ ] **Render first**: Do all data-dependent screens show real layout (borders, icons, labels) on first paint? No shimmer/pulse?
- [ ] **Cached data**: If caching is used, does it preserve or improve uncached first-load performance, remain scoped by user/workspace, and avoid extra hydration/API/auth roundtrips?
- [ ] **Retry/fail**: Are errors classified as transient or deterministic?
- [ ] **No silent failures**: Do all error states show a message, not an empty result?
- [ ] **Honesty**: Does any code pretend success when something partially failed?
- [ ] **Semantic honesty**: Are collection names, routes, cards, and destinations faithful to the real domain, with no fake records hiding empty states?
- [ ] **Warnings**: Do irreversible actions require proportional confirmation?
- [ ] **Cancellable**: Can long operations be cancelled with proper cleanup?
- [ ] **State ownership**: Is state separate from UI rendering?
- [ ] **Persistence**: Does user-entered data survive crashes and reloads?
- [ ] **Decision UX**: When the app/agent offers a choice, are options numbered with exactly one marked recommended?
- [ ] **Release provenance**: Does a strict fresh clone (`npm ci`) reproduce the reviewed build, and do all claimed remotes point to that exact commit/tree?
- [ ] **Deployment auth**: Are legacy/shared-password fallbacks actually disabled, with a verified owner path available?
- [ ] **Financial semantics**: Are totals separated by currency or converted using recorded rates rather than summing incompatible minor units?
- [ ] **Environment isolation**: Are Production and Preview secrets separated, with no production service-role key casually exposed to branch previews?
- [ ] **Authentication auditability**: Are auth events append-only, server-written, privacy-minimized, enumeration-safe, and retained under an explicit policy?

## How to run an audit

1. **Inventory before editing** — inspect every affected route and record its current architecture, query count, and production navigation timing. A delegated scan may identify candidates, but subagent findings are hypotheses until verified.
2. **Triage by user harm** — critical (fake success, data loss), high (swallowed errors, missing confirmations), medium (poor loading/error feedback), low (polish).
3. **Prototype one representative route** — apply the proposed pattern to one high-traffic page first. Do not fan out an unmeasured architectural change across the application.
4. **Measure in a production build** — compare uncached first load, client navigation, query count, and interaction readiness against the baseline. Dev-mode compilation timing is not evidence.
5. **Roll out only after the prototype wins** — then convert similar routes in small batches, verifying after each batch. If it regresses latency, revert the architecture rather than masking it with loaders.
6. **Run correctness gates** — ESLint, TypeScript, production build, route tests, and security checks.
7. **Commit in reversible batches** — keep authorization, data fetching, and visual loading-state changes separate so regressions can be isolated quickly.

### Read-only deployment audits

When the user asks for review without modification, preserve that boundary literally: record the source status, clone claimed publication repositories into temporary directories, run strict installation/build/QA there, clean up temporary processes and files, and prove the original tree is unchanged. Separate **Preview readiness** from **Production readiness**; a permissive host build does not override a failed `npm ci`, active weak auth fallback, invalid multi-currency total, or unsafe Preview secret configuration. Read the complete build log even when the command exits zero, repeat a configured build in the isolated clone when possible, and report swallowed CMS/data fallback errors. Verify streamed Next.js routes from the settled browser DOM rather than raw status/source alone. Before claiming unpublished content exposure, inspect the underlying Supabase view semantics and distinguish intentionally direct-linkable `unlisted` rows from drafts or archives.

Load **`references/vercel-release-readiness.md`** for the complete Next.js + Supabase + Vercel protocol: dual-repository provenance, fresh-clone reproducibility, provider-compatible database replay, runtime QA, auth fallback checks, security headers, environment isolation, and Route 53/domain cutover without damaging email DNS.

**Apply principles proactively, but not blindly.** After validating one implementation, audit the rest of the backend and frontend for the same class of issue. Broad consistency is required; broad unbenchmarked rewrites are forbidden. Static shells, Suspense, caches, polling, and listeners are optional mechanisms—not goals.

## Next.js-specific patterns

Load **`references/nextjs-inline-patterns.md`** for concrete Next.js + Supabase implementation patterns: public CMS navigation, `router.refresh()` migration, loading/error boundaries, dashboard rendering, `useEffect`+`setState` lint workaround, admin query error handling, partial-failure banners, auth action honesty, and content editor draft persistence.

## Concrete audit patterns

Load **`references/nextjs-platform-audit-patterns.md`** for real-world violations and fixes found when auditing a Next.js + Supabase CMS/SaaS platform. Includes: silent PostgREST PGRST201 failures, fake auth success, reports hiding partial failures, missing confirmations, `window.location.reload()` → `router.refresh()`, loading/error boundaries, localStorage draft persistence (with React 19 ESLint pitfall), and immutable price-version replacement.

Load **`references/stale-while-revalidate-pattern.md`** before adding cached background refresh. It defines the performance-first decision order, preferred server-snapshot architecture, cache isolation requirements, and rejection criteria for extra hydration/API/auth roundtrips.

Load **`references/admin-navigation-performance.md`** when authenticated navigation is slow. It covers production measurement, serial authorization waterfalls, request-scoped memoization limits, joined membership/role/permission queries, and one-time invitation slow paths.

Load **`references/authentication-security-events.md`** when implementing or deciding whether to implement login history or security telemetry. It defines event modeling, the business-audit-versus-auth-stream decision, append-only and pre-auth identity handling, enumeration-safe failure logging, trusted-proxy/IP minimization, provider-log boundaries, hard retention controls, launch sequencing, isolated-database testing, and leaked-credential handling.

## Common violations to look for

1. `catch (error) { return []; }` — silent failure masquerading as "no data"
2. `catch { return null; }` — empty catch block with no logging
3. `if (error) console.log(error);` — logged but not surfaced to user
4. Loading spinners without timeouts
5. Delete buttons without confirmation
6. Forms that lose all data on accidental navigation
7. Background tasks with no cancellation mechanism
8. Empty state UI that doesn't distinguish "loading" from "error" from "genuinely empty"
9. "Success" messages when a batch operation had partial failures
10. Hardcoded timeouts instead of polling for readiness
11. `window.location.reload()` in React components — use `router.refresh()` instead
12. Adding `loading.tsx` or Suspense boundaries mechanically without measuring the blocking path
13. Supabase queries that destructure `{ data }` without checking `error`
14. `setState` called synchronously inside `useEffect` — use event-handler callbacks or initialize state lazily
15. `animate-pulse` or shimmering skeletons — keep real static UI visible and mark only unresolved values
16. Splitting every page into wrapper components and fallback trees without a production performance win
17. Generic or per-route fallback components duplicated across the app while authorization/query waterfalls remain unfixed
18. `loading.tsx` rendering dark boxes or gray bars that do not match stable, meaningful UI
19. Moving direct Server Component queries behind hydration, `useEffect`, an API route, repeated auth, or polling just to add a cache
20. Serial authorization calls (workspace → invitation → membership → roles → grants) on every navigation — collapse to one joined query/RPC and keep invitation setup as a one-time fallback
21. Treating request-scoped memoization as a cross-navigation cache — it only deduplicates calls within one server render
22. Rolling an architectural pattern across every route before one representative route passes production benchmarks
23. Renaming a collection or route to disguise a taxonomy mismatch instead of migrating the content type correctly
24. Publishing placeholder catalog records or invented external URLs to avoid an honest empty state
25. Declaring deployment readiness because `npm install` builds while strict fresh-clone `npm ci` fails
26. Treating two repository remotes as synchronized without comparing exact commit and tree hashes
27. Uploading a local legacy admin password to Production without checking whether the fallback path is active or a real owner path exists
28. Summing EGP minor units, USD cents, or other currencies into one headline total without conversion
29. Giving branch Preview deployments the production service-role key by default
30. Replacing Route 53 records for a website cutover without preserving SES, DKIM, SPF, DMARC, and MAIL FROM records
31. Offering a decision as a wall of prose or a buried alternative instead of numbered options with one marked recommended