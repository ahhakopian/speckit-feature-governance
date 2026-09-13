
# Global Feature Governance — Tasks Addendum

These instructions apply in addition to the standard `speckit.tasks` workflow.

## 1. Load the installed native policy

Read the policy shipped with the installed `feature-governance-guard`
extension:

`.specify/extensions/feature-governance-guard/docs/feature-architecture-policy.md`

If that native extension policy cannot be loaded, STOP.

## 2. Keep tasks inside the approved Feature direction

Generate tasks from the approved `spec.md` and `plan.md`. Do not silently turn a later-Feature requirement into work owned by an Earlier Feature.

A task is backward-impacting when it requires changing an established Earlier Feature's specification, contract, responsibility ownership, established behavior, or upstream semantics to accommodate the Current Feature.

Backward-impacting tasks are prohibited unless all of the following are true:

1. `plan.md` declares backward impact;
2. `backward-exception.md` exists in the Current Feature directory;
3. the exception's human decision is explicitly `APPROVED`;
4. the task is within the minimum approved scope.

Any approved backward task MUST be visibly marked and reference the exception, for example:

```text
T042 [BACKWARD] Modify Feature 003 DeliveryReceipt contract — Exception: backward-exception.md
```

If an exception is only `PROPOSED`, missing, rejected, or broader than the approved scope, do not present backward work as executable. Surface the blocking governance issue instead.

## 3. Self-check before finishing

Before declaring `tasks.md` complete, scan the generated tasks for:

- explicit references to lower-numbered Features;
- changes to contracts or responsibilities owned by Earlier Features;
- upstream components being taught Current-Feature-specific concepts;
- refactors justified only by cleanliness or convenience.

Resolve any such item forward, or require the Backward Exception Protocol.
