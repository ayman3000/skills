# Public CMS Navigation Performance

Use this pattern when a database-driven public site feels slow during client navigation even though its page titles and layout are stable.

## Core architecture

### 1. Keep route identity outside async boundaries

Render these synchronously from code or route metadata:

- page title and eyebrow
- permanent description
- navigation and section headings
- known labels, controls, borders, and layout

Only the records that can actually change belong behind Suspense. A Workshops page should immediately render `Workshops` and its permanent description, then stream workshop cards.

Do not manufacture a duplicated card skeleton. Prefer a localized text fallback such as `Loading workshops…` if a fallback is genuinely visible.

### 2. Distinguish request memoization from persistent caching

- React `cache()` deduplicates calls during one server render.
- Next.js `unstable_cache()` persists public CMS results across requests and navigations.
- Neither replaces authoritative authorization for protected data.

Good persistent-cache candidates:

- site identity and About settings
- default public workspace
- public collection summaries
- public item detail records
- app catalog
- public offering/package/price snapshots
- approved review lists and aggregate statistics

Keep truly live or personalized data separate: session state, the current user's review, seats being reserved, account data, and permissions.

### 3. Query only what the view renders

Collection cards should not select Markdown bodies, revisions, or detail-only fields. Define separate summary and detail projections.

For a homepage with multiple featured sections, issue one combined query, group the rows in memory, and use request memoization so sibling Server Components share one promise. Avoid one query per section/type/limit.

### 4. Split detail pages by stability

A public workshop detail page should render cached stable content first:

- title and description
- tags
- curriculum/Markdown
- permanent section structure

Stream independently:

- authentication/session state
- current user's review
- reviews and ratings
- package prices
- cohort availability
- registration controls

Never make public curriculum wait for `getUser()`, review aggregation, or a live capacity RPC.

### 5. Invalidate on successful mutations

Long server cache lifetimes are safe only with mutation-driven invalidation. Tag by domain and entity, for example:

- `site:settings`
- `content:list:courses`
- `content:item:courses:<slug>`
- `content:featured`
- `apps:list`
- `offerings:public`
- `reviews:course:<id>`
- `cohorts:<offering-id>`

Call `updateTag()` only after the database mutation has succeeded. If a slug changes, invalidate both old and new item tags plus the list and featured tags.

Do not cache a swallowed failure. The function inside `unstable_cache()` should throw on query failure; catch outside the cached function to log/surface the error. Otherwise a transient failure or false empty list can be persisted as valid data.

### 6. Preserve authoritative dynamic checks

Never persist cross-user permission or session results in a public cache. Cache public catalog data only. Keep user/workspace authorization authoritative and request scoped unless there is a deliberately signed, user-scoped design.

## Measurement protocol

1. Start from a production build, never dev mode.
2. Record cold and warm HTML TTFB and total response time.
3. Measure real Next.js client-navigation RSC requests (`?_rsc=`), not only full page loads.
4. Record query count and payload shape.
5. Prototype on one representative list page and one detail page.
6. Roll out only if the production prototype wins.
7. Run lint, TypeScript, production build, browser QA, and console-error checks.

Suggested acceptance targets for a local production server:

- stable shell visible immediately
- warm public list-route server response below 100 ms
- warm detail shell below 100 ms before personalized/live regions
- no hydration + `useEffect` + API detour added to obtain cached public data
- no shimmer, pulse, or generic dark placeholder cards

## Common regressions

- Putting the database-backed site header on every route's uncached critical path
- Treating request-scoped React `cache()` as a cross-navigation cache
- Fetching full Markdown bodies for list cards
- Running one featured query per homepage section
- Blocking public workshop content on authentication and live registration data
- Caching `[]` after catching a transient query failure
- Adding 24-hour caching without invalidating after admin mutations
- Measuring curl HTML only while ignoring slow RSC navigation requests
