# Next.js + Supabase Trustworthy-App Fix Recipes

Concrete recipes from auditing and correcting a Next.js/Supabase CMS. Treat mechanisms as optional: prototype one route and benchmark an optimized production build before broad rollout.

## 1. Never turn query failure into an empty state

Prefer a discriminated result so callers can distinguish no records from failure:

```ts
type LoadResult<T> =
  | { ok: true; data: T }
  | { ok: false; message: string };

export async function getApps(): Promise<LoadResult<App[]>> {
  const { data, error } = await supabase.from("apps").select("*");
  if (error) {
    console.error("getApps failed", error.message);
    return { ok: false, message: "Apps could not be loaded." };
  }
  return { ok: true, data: data as App[] };
}
```

The UI renders either a genuine empty state or an actionable error—not the same component for both.

## 2. Auth action honesty without account enumeration

```ts
const { error } = await supabase.auth.resetPasswordForEmail(email, { redirectTo });
if (error) {
  if (isRateLimit(error)) return { ok: false, message: "Too many attempts. Try later." };
  console.error("password reset failed", error.message);
  // Keep identity-specific details private, but do not pretend infrastructure worked.
  return { ok: false, message: "Password reset is temporarily unavailable." };
}
return { ok: true, message: "If that address has an account, a reset link is on its way." };
```

## 3. Reports must expose partial failure

Run independent report queries in parallel, inspect every `error`, and collect failed sections:

```ts
const partialFailures: string[] = [];
const [orders, registrations] = await Promise.all([
  supabase.from("orders").select("*").eq("workspace_id", workspaceId),
  supabase.from("registrations").select("*").eq("workspace_id", workspaceId),
]);
if (orders.error) partialFailures.push("orders");
if (registrations.error) partialFailures.push("registrations");
return { orders: orders.data ?? [], registrations: registrations.data ?? [], partialFailures };
```

Render successful sections, plus a warning that figures may be incomplete.

## 4. Refresh server data without a document reload

After a successful mutation, prefer `router.refresh()` over `window.location.reload()`. Preserve local component state where appropriate and clear only the state intentionally completed.

## 5. Loading UI: fix latency before decorating it

Do not create `loading.tsx` for every route by default. First determine why navigation blocks:

- repeated remote identity verification,
- serial workspace/membership/role/permission queries,
- duplicated layout and page authorization,
- serial page queries,
- hydration plus a second API request,
- dev-mode compilation.

Optimize those costs first. Use a loading boundary only when production measurements show a remaining wait that cannot be removed.

If a fallback is justified:

- never shimmer or pulse,
- preserve stable layout and already-rendered content,
- show real labels, icons, borders, and table headers,
- use `—` only for unresolved values,
- avoid a shared fallback shaped like the wrong route,
- avoid duplicating large page trees solely for loading.

## 6. Suspense is conditional, not mandatory

A static shell plus independent Suspense regions is useful only when each region can truly stream independently and production measurements improve. Do not split every page mechanically.

Keep direct Server Component data when it is already fast. Never replace:

`Server Component → database`

with:

`server shell → hydration → effect → API route → repeated auth → database`

merely to add caching or an `Updating…` label.

For genuinely live data, pass the initial server snapshot into a client component and subscribe only to relevant events. Do not poll by default.

## 7. Fast authenticated navigation

A common hidden waterfall is:

`getUser → workspace → invitation → membership → member roles → roles → grants`

On every link this can dominate page latency. Resolve active workspace, membership, roles, and grants in one joined PostgREST query or one RPC. Keep invitation activation as a one-time fallback only when no active membership exists. Memoize authorization per server request so layout and page share it, while remembering that request memoization does not persist across navigations.

See `admin-navigation-performance.md` for the query shape and acceptance checks.

## 8. Draft persistence without effect-state lint violations

Restore drafts from the event handler that opens a form, not by synchronously calling `setState` inside an effect. Use the effect only for debounced persistence. Key drafts by user/workspace/content type, validate parsed fields, and clear after successful save.

## 9. Consequential actions need proportional confirmation

Confirm archive, suspension, removal, cancellation, and no-show transitions with target-specific wording. Inspect the action result and show failure feedback; a successful promise resolution is not proof that the operation succeeded.

## 10. Immutable price replacement

Do not edit historical prices in place. Deactivate current rows, insert new versioned rows, and reactivate previous rows if insertion fails. Historical orders and receipts continue to reference their original price snapshots.

## Verification sequence

1. Capture baseline production timings and query counts.
2. Implement on one representative route.
3. Verify authorization and error semantics.
4. Compare uncached first load and authenticated client navigation.
5. Roll out in small batches only after a measured win.
6. Run lint, TypeScript, production build, route tests, and credential scan.
7. Commit architecture changes separately from visual loading changes.