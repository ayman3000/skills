# Authenticated Admin Navigation Performance

Use this when every admin link takes seconds even though individual page queries appear simple.

## Diagnose in the right order

1. Run an optimized production build; do not use dev-mode compilation delays as the baseline.
2. Measure authenticated client navigation, not only unauthenticated redirects.
3. Trace the full request path: middleware/proxy auth, root layout auth, page permission check, then page data.
4. Count network/database roundtrips and identify serial chains.
5. Benchmark authorization separately from page data.

## Common hidden waterfall

A permission resolver may perform these serial calls on every navigation:

- verify user remotely,
- load default workspace,
- check pending invitation,
- load membership,
- load member-role links,
- load roles,
- load permission grants.

A loading shell does not fix this; it only makes the wait visible.

## Durable fix

- Keep remote identity verification where security requires it.
- Resolve active membership, workspace, roles, and grants with one joined query or one database RPC.
- Filter roles to the resolved workspace even if relational integrity already exists.
- Move invitation acceptance/bootstrap work to a one-time slow path used only when no active membership exists.
- Use React `cache()` or equivalent request-scoped memoization so layout and page share authorization within one render.
- Remember that request-scoped memoization does **not** persist across navigations; the underlying query still must be efficient.
- Preserve permission checks at every protected action/page. Optimize lookup shape, not security semantics.

## PostgREST joined-query shape

```ts
const { data, error } = await admin
  .from("workspace_memberships")
  .select(`
    id,
    status,
    workspace_id,
    workspace:workspaces!inner(id,is_default),
    member_roles(
      role:roles(id,code,workspace_id,role_permissions(permission_code))
    )
  `)
  .eq("user_id", verifiedUser.id)
  .eq("status", "active")
  .eq("workspace.is_default", true)
  .maybeSingle();
```

Use the verified identity id—not an arbitrary request parameter—and a trusted server client. Check and surface query errors.

## Cache/listener rule

Do not change:

`Server Component → database`

into:

`Server page → hydration → effect → API route → repeated auth → database`

just to cache data or show `Updating…`. That regresses first load. If live updates are needed, render a server snapshot first, pass it as client state, and subscribe only to relevant events. Polling is opt-in, not a default.

## Acceptance criteria

- Compare old and new authorization latency against the same production database.
- Record roundtrip count and median timing over multiple runs.
- Uncached first-load and client-navigation timing must improve or stay neutral.
- Existing permissions and role codes must resolve identically.
- Suspended, removed, uninvited, and wrong-workspace users remain denied.
- Invitation activation still works as a one-time fallback.
- Lint, typecheck, production build, and credential scan pass.
- Keep the performance fix in a focused, reversible commit.