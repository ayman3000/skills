# Next.js Platform Audit Patterns

Use these patterns when auditing a Next.js + Supabase CMS/SaaS. They are candidate fixes, not mandates: validate one representative route and measure a production build before site-wide rollout.

## 1. Silent failure masquerading as no data

PostgREST commonly returns `{ data: null, error }` without throwing. Always inspect `error`; return a discriminated failure or render an error state. Logging alone is insufficient when the operator needs to distinguish an empty table from a failed query.

An ambiguous relationship such as `PGRST201` often requires an explicit foreign-key hint:

```ts
.select("offering_packages!offering_packages_offering_workspace_fk(id,...)")
```

## 2. Auth actions that report fake success

Password-reset and verification actions must inspect returned auth errors as well as thrown failures. Preserve account-enumeration privacy with neutral wording, but return operational failure for rate limits or unavailable infrastructure.

## 3. Reports hiding partial failures

Run independent report queries in parallel, inspect every error, collect failed sections in `partialFailures`, and show a warning while retaining successful sections. Never silently turn failed report sources into zeros.

## 4. Consequential transitions without confirmation

Archive, suspend, remove, cancel, and no-show operations require target-specific confirmation and explicit handling of unsuccessful action results. Preserve immutable historical records when deletion would damage auditability.

## 5. Full document reload after mutation

Use `router.refresh()` when server data must be revalidated without discarding the whole client document. Preserve form state intentionally; clear drafts only after confirmed success.

## 6. Loading architecture can create regressions

Do not infer that every async route needs `loading.tsx`, Suspense wrappers, or duplicated fallback components. First measure:

- middleware/proxy identity verification,
- layout and page authorization duplication,
- serial membership/role/permission lookups,
- serial page queries,
- extra hydration/API requests,
- dev compilation versus production latency.

Fix the blocking path before adding loading UI. If a fallback remains justified, never shimmer; keep stable labels, icons, borders, and existing data visible. A shared fallback shaped like another route is misleading, while one duplicated fallback per route can add substantial complexity without making navigation faster.

## 7. Authenticated navigation waterfall

A route may execute:

`getUser → workspace → invitation → membership → member-role links → roles → grants → page data`

on every link. Collapse active workspace, membership, roles, and grants into one joined query or RPC. Run invitation activation only when no active membership exists. Use request-scoped memoization so layout and page share context inside one render, but remember this cache resets on the next navigation. See `admin-navigation-performance.md`.

## 8. Client caching can make first load slower

Never replace direct server data with:

`hydration → effect → API route → repeated auth → database`

merely to show cached values and `Updating…`. If live updates are required, render a server snapshot first and subscribe only to relevant events. Scope caches by user/workspace, set a TTL, clear on logout, deduplicate refreshes, and avoid polling by default.

## 9. Content editor draft persistence

Auto-save new drafts with a debounce, key them by user/workspace/content type, validate restored data, and clear only after successful persistence. Restore from the event handler opening the form rather than synchronously setting state inside an effect.

## 10. Immutable price versions

Deactivate current price rows and insert new versions. If insertion fails, restore prior active rows. Never rewrite historical prices referenced by orders or receipts.

## 11. Proactive but controlled rollout

1. Inventory all occurrences of the pattern.
2. Capture current production timings/query counts.
3. Fix one representative route.
4. Verify correctness, authorization, and latency.
5. Roll out in small backend/frontend batches only after a measured win.
6. Run lint, TypeScript, production build, route tests, and credential scan after each batch.
7. Keep architecture and visual loading changes in separate reversible commits.

Proactivity means finding and addressing the whole class of issue after validation—not converting every page to an unproven pattern at once.