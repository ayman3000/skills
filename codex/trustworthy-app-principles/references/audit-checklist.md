# Trustworthy Application Audit Checklist

Use this checklist for pre-release reviews and focused trust audits. Mark non-applicable items explicitly and record why.

- [ ] **1. Responsiveness:** Every action receives prompt, meaningful acknowledgment. **Red flags:** frozen controls, feedback only after completion, or fixed delays used as readiness checks.
- [ ] **2. Stable rendering:** Known structure remains visible while unresolved data loads. **Red flags:** full-interface placeholders, distracting animation, layout shifts, or stale content presented as current.
- [ ] **3. Retry behavior:** Transient and deterministic failures are handled differently. **Red flags:** unbounded retries, retries of invalid input or permissions, or discarded root causes.
- [ ] **4. Terminal states:** Every operation can end in success, partial success, empty, cancelled, or failed. **Red flags:** permanent loading, errors represented as “no data,” or logging without a user-visible consequence.
- [ ] **5. Honesty:** Success and completion claims are backed by verified outcomes. **Red flags:** invented output, fake records hiding empty states, partial failure reported as success, tests that do not exercise the claim, or labels, entities, or relationships distorted to fit storage rather than the real domain.
- [ ] **6. Safe actions:** Irreversible and outward-facing actions receive proportional confirmation and preview. **Red flags:** generic “Are you sure?” prompts, no target shown, avoidable confirmation friction, or no undo where one is practical.
- [ ] **7. Cancellation:** Long work can be cancelled safely when feasible. **Red flags:** Cancel hides rather than stops work, leaked resources, undeclared committed side effects, or a fake Cancel control.
- [ ] **8. State ownership:** Critical state remains authoritative outside the rendered interface. **Red flags:** UI-only state, optimistic state shown as saved, or no rollback/reconciliation path.
- [ ] **9. Persistence:** User-entered data survives realistic interruption and recovery scenarios. **Red flags:** drafts lost on navigation, drafts cleared before confirmed save, destructive migrations, or recovery tested only after clean shutdown.
- [ ] **10. Decision UX:** Meaningful choices are numbered with exactly one contextual recommendation. **Red flags:** choices buried in prose, overlapping options, no rationale, or a recommendation unsupported by user context.
- [ ] **11. Risk proportionality:** Principles are applied according to actual user harm and justified exceptions are recorded. **Red flags:** mechanical requirements on trivial surfaces or missing protections on destructive, stateful, financial, or outward-facing workflows.
- [ ] **12. Evidence:** The audit distinguishes verified behavior, assumptions, and unresolved risk. **Red flags:** claims based only on static inspection, omitted failure paths, or no reproduction evidence.

## Audit result

Report findings by severity:

1. **Critical:** fake success, data loss, unsafe irreversible action, or deception
2. **High:** silent failure, missing recovery, ineffective cancellation, or missing confirmation
3. **Medium:** unclear state, slow acknowledgment, misleading freshness, or weak persistence
4. **Low:** polish or consistency issues with limited user harm

For each finding, include the affected workflow, observed evidence, user impact, recommended fix, and verification step.