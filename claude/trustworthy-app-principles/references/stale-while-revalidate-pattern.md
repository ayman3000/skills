# Stale-While-Revalidate Without First-Load Regressions

Use cached data only when it improves perceived speed **without moving a fast server query behind hydration and another HTTP request**.

## Decision order

1. Measure the current route in a production build.
2. Remove duplicate auth/database work first.
3. Keep initial data in Server Components when it is already available during rendering.
4. Use request-scoped `cache()` for repeated server authorization/context lookups.
5. Prefer one aggregate database query/RPC over multiple browser API requests.
6. Add a client cache only for truly live, frequently revisited data when a browser request already exists or realtime events update an existing server snapshot.

## Preferred architecture

- Server renders the latest known data directly.
- Client receives that initial snapshot as props.
- Optional realtime subscription or mutation invalidation updates it.
- Show a subtle `Updating…` label only during an actual background reconciliation.
- Do not poll by default.

```tsx
// Server component
const initial = await getDashboardData(workspaceId);
return <DashboardClient initial={initial} workspaceId={workspaceId} />;
```

```tsx
// Client component
"use client";

export function DashboardClient({ initial }: { initial: DashboardData }) {
  const [data, setData] = useState(initial);
  const [updating, setUpdating] = useState(false);

  // Subscribe only when the product genuinely needs live updates.
  // Reconcile after a relevant event, deduplicate requests, and abort on unmount.
  return <Dashboard data={data} updating={updating} />;
}
```

## Never do this

Do not replace a direct server query with:

`Server page → hydration → useEffect → API route → repeated auth → database`

That architecture makes uncached first load slower, adds another network roundtrip, and can duplicate permission resolution. A `sessionStorage` hit on later visits does not justify regressing every first visit.

## Client-cache requirements

If a client cache is genuinely justified:

- Key by authenticated user and workspace.
- Store a timestamp and enforce a TTL.
- Clear on logout/account switch.
- Deduplicate overlapping refreshes.
- Use `AbortController` on unmount.
- Do not retry 401/403/validation errors.
- Do not poll unless explicitly required.
- Keep and display stale data if refresh fails, with an actionable warning.
- Benchmark before and after in a production build.

## Acceptance criteria

- Uncached first-load time does not regress.
- No additional full authorization pass is introduced.
- No duplicate data query is introduced.
- Cached data is never shared across users/workspaces.
- Background refresh is visible but non-blocking.
- The cache can be invalidated by successful mutations.