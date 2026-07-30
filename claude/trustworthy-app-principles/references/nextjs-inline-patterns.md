# Next.js-specific patterns

Concrete implementation patterns for applying the trustworthy principles in Next.js + Supabase applications. Load this when building or auditing a Next.js app.

## Public CMS navigation — stable shell + persistent server cache

For database-driven public sites, do not put stable page identity on the uncached database critical path. Render the title, permanent description, navigation, and section structure immediately; stream only records that can change.

Use persistent server caching for public CMS data and mutation-driven tag invalidation. Keep list projections slim (never fetch full Markdown for cards), combine homepage featured queries, and separate detail-page content from personalized/live regions. Public workshop curriculum must not wait for authentication, reviews, pricing, or cohort availability.

Measure both full HTML responses and actual Next.js `?_rsc=` client-navigation requests in a production build. React `cache()` only deduplicates one render; it is not a cross-navigation cache. Never cache a swallowed query error or false empty result.

See `references/public-cms-navigation-performance.md` for the architecture, tag model, failure-safe cache wrapper, detail-page split, and benchmark protocol.

## window.location.reload() → router.refresh()

Admin clients that call `window.location.reload()` after a successful mutation cause a full page reload, discard all client state, and block the UI. Replace with:

```tsx
import { useRouter } from "next/navigation";
const router = useRouter();
// After successful action:
router.refresh();
```

This revalidates server data without a full reload. Add the `useRouter` import and hook at the top of each admin client component.

## Loading and error boundaries — performance-first model

Next.js `loading.tsx` and Suspense boundaries are not automatically improvements. They add fallback trees and can conceal slow authorization or query waterfalls.

1. **Measure the blocking path first.** Determine whether latency comes from authentication, serial database calls, server rendering, bundle loading, or hydration.
2. **Fix the bottleneck before adding UI.** Collapse serial authorization/query fan-out, remove duplicate requests, and move invitation/setup work to one-time slow paths.
3. **Keep static UI visible when it is already mounted.** During client navigation, preserve the admin shell and existing content where practical; update only the dynamic region.
4. **Use `loading.tsx` only when route-transition evidence justifies it.** Never create one mechanically for every subroute. A shared fallback that mismatches the destination page is worse than no fallback.
5. **Use Suspense only around a genuinely independent async region.** Do not split every page into wrappers merely to satisfy a visual principle; extra boundaries can duplicate work and complicate navigation.
6. **Never shimmer.** If a fallback is justified, show real static labels, icons, borders, table headers, and `—` only for unresolved values.
7. Add `error.tsx` boundaries with a clear retry action where failures can be recovered.

For authenticated admin routes, remember that the layout and page may both request authorization. Use request-scoped memoization to deduplicate work inside one render, then optimize the authorization query itself because each navigation is still a new request. See `references/admin-navigation-performance.md`.

## Dashboard rendering pattern

Prefer direct Server Component data when it is already fast. A static shell plus Suspense can help only when:

- the shell can render before authorization/data without duplicating work,
- the dynamic regions are truly independent,
- production measurements improve first paint or interaction readiness, and
- no extra browser API/auth roundtrip is introduced.

Do not replace direct server rendering with `hydration → useEffect → API route` merely to show cached numbers. If live updates are genuinely required, pass the server snapshot into a client component, subscribe only to relevant events, and show `Updating…` during reconciliation.

## useEffect + setState lint rule

Next.js ESLint flags `setState` called synchronously inside `useEffect` as `react-hooks/set-state-in-effect`. To restore a localStorage draft:

- **Wrong**: call `setForm(restored)` inside the effect body
- **Right**: call a `restoreDraft()` callback from the event handler that opens the form (e.g., `startCreate`), then use the effect only for debounced auto-save

## Admin query error pattern

Supabase queries that destructure `{ data }` without checking `error` will silently render an empty table on failure. Always:

```tsx
const { data, error } = await supabase.from("table").select("...");
if (error) {
  console.error("PageName: query failed", error.message);
  return <ErrorBanner message="Could not be loaded. Please try again." />;
}
```

## Reports partial-failure pattern

When a dashboard aggregates multiple queries, track failures in an `errors: string[]` array. Return it as `partialFailures` in the result type. Surface a warning banner when non-empty:

```tsx
{data.partialFailures.length > 0 && (
  <div className="amber-warning">
    Some data sources could not be loaded ({data.partialFailures.join(", ")}).
  </div>
)}
```

## Auth action honesty

Password reset and verification resend actions that catch all errors and return `{ ok: true }` violate Principle 5. Distinguish:
- Rate-limit errors → return `{ ok: false, message: "Too many attempts..." }`
- Transient/infra errors → return `{ ok: false, message: "Temporarily unavailable..." }`
- Auth API errors (e.g. "email not registered") → log but return neutral success to prevent account enumeration

## Content editor draft persistence

Auto-save form state to `localStorage` with a 1-second debounce. Restore on form open via a callback (not an effect). Clear on successful save. See `references/nextjs-audit-fix-recipes.md` for the exact implementation pattern.