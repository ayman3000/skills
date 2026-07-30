---
name: trustworthy-app-principles
description: Audit and enforce trust-building principles for desktop and web applications — responsiveness, honest failure, cancellation, persistence, safe actions, and clear decision UX.
version: 2.1.0
---

# Trustworthy Application Principles

Ten principles for building and auditing applications that users can trust — desktop or web. Use this skill when building, auditing, or reviewing any application.

## When to use

- Before shipping a new feature, run the checklist below
- When auditing an existing codebase for trust issues
- When reviewing a PR that touches I/O, error handling, or user actions
- When designing a new screen or interaction flow
- When designing or auditing login history, authentication telemetry, abuse detection, or security-event retention

## The principles

### 1. Responsiveness is the product

Never block the UI on I/O or computation. The app should always feel instant.

- Offload genuinely heavy work to background tasks, web workers, or server functions
- Give immediate feedback without replacing real UI with generic loaders: render the stable shell, preserve existing data, and mark only the changing field
- Target < 100ms for perceived response; investigate any navigation over 1s before adding progress UI
- **Performance is a quality gate:** benchmark the existing path before refactoring and the production build afterward. A principle-driven refactor that makes navigation slower must be rolled back or redesigned

### 2. Render first, refine in the background

Show something useful immediately, then improve it progressively. Don't make users wait for perfect results.

- **Never use shimmering/pulse placeholders.** Render the actual layout immediately: static text, headings, labels, borders, buttons, table headers, card structure, icons, and all non-dynamic content. Users should see the real page, not a gray ghost of it. If a card has an icon and a label, render the icon and label — only the number waits. If a table has column headers, render the headers and borders — only the rows wait.
- Only dynamic data fields (numbers, rows, list items, chart values) should show a loading state — and that state should be a simple "Loading…" text or a small spinner next to the specific field, not a full-page skeleton.
- Show cached/stale data immediately only when it is already available **without adding a slower execution path**. Refresh in the background with a subtle "Updating…" badge.
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

### 8. State is the source of truth, not the UI

The UI reflects state, it doesn't own it. Every action updates a persistent or recoverable state first, then the UI reacts. If the app crashes, the user loses nothing.

- Separate state management from rendering — state store, then UI subscribes
- Form data should survive navigation away and back
- Don't store critical data only in component state — lift it to a store or persistence layer
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
- [ ] **Cached data**: If caching is used, does it preserve or improve uncached first-load performance, remain scoped by user/workspace, and avoid extra roundtrips?
- [ ] **Retry/fail**: Are errors classified as transient or deterministic?
- [ ] **No silent failures**: Do all error states show a message, not an empty result?
- [ ] **Honesty**: Does any code pretend success when something partially failed?
- [ ] **Semantic honesty**: Are collection names, routes, cards, and destinations faithful to the real domain, with no fake records hiding empty states?
- [ ] **Warnings**: Do irreversible actions require proportional confirmation?
- [ ] **Cancellable**: Can long operations be cancelled with proper cleanup?
- [ ] **State ownership**: Is state separate from UI rendering?
- [ ] **Persistence**: Does user-entered data survive crashes and reloads?
- [ ] **Decision UX**: When the app/agent offers a choice, are options numbered with exactly one marked recommended?
- [ ] **Deployment auth**: Are legacy/shared-password fallbacks actually disabled, with a verified owner path available?
- [ ] **Financial semantics**: Are totals separated by currency or converted using recorded rates rather than summing incompatible minor units?
- [ ] **Environment isolation**: Are production and preview/staging secrets separated?
- [ ] **Authentication auditability**: Are auth events append-only, server-written, privacy-minimized, enumeration-safe, and retained under an explicit policy?

## How to run an audit

1. **Inventory before editing** — inspect every affected route and record its current architecture, query count, and navigation timing. A delegated scan may identify candidates, but subagent findings are hypotheses until verified.
2. **Triage by user harm** — critical (fake success, data loss), high (swallowed errors, missing confirmations), medium (poor loading/error feedback), low (polish).
3. **Prototype one representative route** — apply the proposed pattern to one high-traffic page first. Do not fan out an unmeasured architectural change across the application.
4. **Measure in a production build** — compare uncached first load, client navigation, query count, and interaction readiness against the baseline. Dev-mode compilation timing is not evidence.
5. **Roll out only after the prototype wins** — then convert similar routes in small batches, verifying after each batch. If it regresses latency, revert the architecture rather than masking it with loaders.
6. **Run correctness gates** — linters, type checks, production build, route tests, and security checks.
7. **Commit in reversible batches** — keep authorization, data fetching, and visual loading-state changes separate so regressions can be isolated quickly.

**Apply principles proactively, but not blindly.** After validating one implementation, audit the rest of the backend and frontend for the same class of issue. Broad consistency is required; broad unbenchmarked rewrites are forbidden. Static shells, caches, polling, and listeners are optional mechanisms—not goals.

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
11. `animate-pulse` or shimmering skeletons — keep real static UI visible and mark only unresolved values
12. Offering a decision as a wall of prose or a buried alternative instead of numbered options with one marked recommended