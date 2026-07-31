---
name: trustworthy-app-principles
description: Audit and enforce trust-building principles for desktop and web applications — responsiveness, honest failure, cancellation, persistence, safe actions, and clear decision UX. Use before shipping features and when building, auditing, or reviewing an application.
license: MIT
metadata:
  version: "2.3.0"
---

# Trustworthy Application Principles

Ten stack-agnostic principles for building and auditing applications that users can trust. Use this skill when building, auditing, or reviewing any desktop or web application.

Apply each principle according to actual user risk. A static informational surface may not need cancellation or draft persistence; a destructive, stateful, financial, or outward-facing workflow usually does. Record justified exceptions instead of applying the checklist mechanically.

## When to use

- Before shipping a new feature
- When auditing an existing application for trust issues
- When reviewing changes that affect I/O, errors, state, permissions, or user actions
- When designing a screen, workflow, or recovery path
- When evaluating sensitive data handling, security-event logging, or retention

## Priority when principles conflict

Protect users from irreversible harm, data loss, deception, and unsafe side effects before optimizing speed or convenience. Required safety confirmations are intentional interaction steps, not responsiveness failures. Keep them concise and proportional, but never remove them merely to reduce latency.

## The principles

### 1. Responsiveness is the product

Never make the interface appear frozen while work continues. Every action should receive prompt, meaningful feedback.

- Move genuinely heavy work off the interaction-critical path
- Preserve usable interface and existing data while work proceeds
- Target acknowledgment within 100 ms; for inherently slow work such as network, model, or long-running computation, this target applies to visible acknowledgment—not completion
- Benchmark before and after performance-sensitive changes
- Roll back or redesign a trust-oriented refactor if it makes the experience materially slower

### 2. Render first, refine in the background

Show useful, stable structure immediately, then fill in unresolved data without disorienting the user.

- Render headings, labels, controls, borders, table headers, and other known structure immediately
- Limit loading indicators to unresolved dynamic regions rather than replacing the entire interface
- Prefer stable, accessible loading states; avoid shimmer or pulse effects that distract, imply false progress, or harm accessibility
- Show cached data immediately only when doing so does not create a slower path or misrepresent freshness
- Label stale or preliminary content clearly and refresh it without silent replacement
- Scope caches to the correct data owner and context; use expiration, deduplication, and explicit invalidation

### 3. Retry transient failures, fail fast on deterministic ones

Retry temporary failures. Surface invalid input, credentials, configuration, schema, or permissions immediately.

- Represent transient and deterministic errors explicitly
- Use bounded retries with exponential backoff and jitter; three attempts is a sensible default, not a universal rule
- Never retry failures that cannot succeed without changed input, configuration, or permission
- Preserve the original failure cause for diagnostics
- Tell the user what happened and what they can do next

### 4. Never fail silently

Every operation should end with a result or a clear, actionable message. A permanent loading state is a bug.

- No empty catch blocks
- If an error is intentionally absorbed, record it and surface the relevant consequence
- Do not return an empty value on failure without preserving the distinction between failure and genuine emptiness
- Give loading states a timeout or another path to a terminal state
- Distinguish loading, empty, partial, cancelled, and failed states

### 5. Honesty over completion

If something fails, say it failed. Never invent data, fake success, or claim unverified completion.

- Report partial success as partial success
- Never log or display “completed” when errors remain
- If a dependency is unavailable, expose the limitation instead of pretending the feature works
- Tests that pass without exercising the claimed behavior are not evidence
- Keep labels, entities, and relationships faithful to the real domain; do not relabel concepts merely to fit the current storage model
- Do not create fake records or content to conceal an honest empty state
- Preserve history and relationships when correcting classifications or data models

### 6. Warn before irreversible or outward-facing actions

Delete, overwrite, send, publish, charge, or execute actions should require confirmation proportional to their impact.

- Low impact: concise confirmation
- Medium impact: confirmation with the target and consequences
- High impact: staged confirmation with an exact preview of what will happen
- Never ask only “Are you sure?” — identify the action and target
- Provide a brief undo window when practical
- Preview outward-facing results from the recipient’s perspective
- Do not add unnecessary confirmation friction to safe, reversible actions

### 7. Long work is cancellable

Work that may take more than a few seconds should be cancellable when cancellation can be implemented safely.

- Cancel must stop the work, not merely hide its interface
- Clean up processes, connections, locks, temporary resources, and partial output
- Check cancellation signals at meaningful boundaries
- If cancellation is impossible or unsafe, state that before starting and do not show a fake Cancel control
- Report whether cancellation left any committed side effects

### 8. State is the source of truth, not the UI

The interface reflects authoritative state; it must not become the only place critical state exists.

- Separate state transitions from rendering
- Keep critical state in a persistent or recoverable store appropriate to the platform
- Make important transitions atomic when possible
- For optimistic updates, mark the state as pending and provide a verified rollback or reconciliation path
- Never present optimistic state as durably saved before persistence is confirmed
- Preserve in-progress work across navigation when users reasonably expect it

### 9. Persistence is a feature, not an afterthought

User-entered data should survive crashes, restarts, accidental closes, and ordinary navigation whenever practical.

- Save drafts at an interval appropriate to the cost and risk of loss
- Restore drafts transparently and show when they were last saved
- Persist window, document, form, and session context when users reasonably expect continuity
- Clear drafts only after confirmed persistence or explicit discard
- Make migrations reversible or non-destructive where possible
- Test recovery from interruption, not only clean shutdown

### 10. Present numbered options with a recommended choice

When the application or agent offers a meaningful decision, present concise numbered options and mark one as recommended. The user should be able to choose by number or accept the recommendation.

- Number every distinct option
- Mark exactly one as **Recommended** and give a one-line rationale
- Base the recommendation on the user’s context, safety, reversibility, and likely outcome
- Keep options mutually distinct and expose important trade-offs
- Reissue the list if new information materially changes the recommendation
- Do not manufacture unnecessary choices when one clearly safe action can be taken directly

## Audit checklist

Run this before shipping:

- [ ] **Responsiveness:** Does every action receive prompt, meaningful feedback?
- [ ] **Stable rendering:** Is known structure visible while unresolved data loads, without distracting or misleading placeholders?
- [ ] **Freshness:** Are cached, stale, and preliminary results labeled and scoped correctly?
- [ ] **Retry behavior:** Are transient and deterministic failures handled differently?
- [ ] **Terminal states:** Can every operation end in success, partial success, empty, cancelled, or failed — without permanent loading?
- [ ] **Honesty:** Are all success and completion claims backed by real outcomes?
- [ ] **Semantic integrity:** Do labels and data relationships match the real domain?
- [ ] **Safe actions:** Do irreversible and outward-facing actions receive proportional confirmation and preview?
- [ ] **Cancellation:** Can long work be cancelled safely, with cleanup and side effects reported?
- [ ] **State ownership:** Is critical state authoritative outside the rendered interface?
- [ ] **Persistence:** Does user-entered data survive realistic interruption and recovery scenarios?
- [ ] **Decision UX:** Are meaningful choices numbered with exactly one contextual recommendation?

## How to run an audit

1. **Inventory before editing** — map affected workflows, state transitions, dependencies, failure paths, and current performance.
2. **Triage by user harm** — critical (fake success, data loss, unsafe action), high (silent failure, missing recovery or confirmation), medium (unclear state or slow feedback), low (polish).
3. **Prototype one representative workflow** — validate the proposed pattern before broad rollout.
4. **Measure in a release-equivalent environment** — compare response time, resource use, interaction readiness, and failure behavior against the baseline.
5. **Roll out in small reversible batches** — verify after each batch and redesign changes that regress trust or performance.
6. **Run correctness gates** — use the project’s linters, type checks, tests, production/release build, and security checks.
7. **Verify the result** — exercise success, failure, cancellation, interruption, retry, empty, and partial-success paths.
8. **Report evidence and remaining risk** — distinguish verified behavior from assumptions and unresolved limitations.

Apply the principles proactively but not mechanically. Consistency matters; broad unmeasured rewrites are forbidden. Implementation mechanisms are means, not goals.

## Common violations to look for

1. Returning an empty value on error and presenting it as “no data”
2. Logging an error without surfacing its user-visible consequence
3. Loading indicators with no timeout or terminal failure state
4. Destructive actions without target-specific confirmation
5. Forms that lose in-progress work during ordinary navigation or interruption
6. Cancel controls that hide work without stopping it
7. Empty states that do not distinguish loading, failure, cancellation, and genuine emptiness
8. Success messages after partial failure
9. Fixed delays used as a substitute for readiness or completion checks
10. Distracting animated placeholders that conceal stable, useful structure
11. Optimistic state presented as durably saved without confirmation or rollback
12. Decisions buried in prose instead of numbered options with one contextual recommendation