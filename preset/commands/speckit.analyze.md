
# Global Feature Governance — Analyze Addendum

These instructions apply in addition to the standard read-only `speckit.analyze` workflow.

## 1. Synchronize and load governance

Run:

```bash
python3 "${SPECKIT_FEATURE_GOVERNANCE_HOME:-$HOME/.config/speckit-feature-governance}/bootstrap/specify-governed.py" ensure-project --project-root . --quiet
```

If it reports `GOVERNANCE_UPDATED_RESTART_REQUIRED` (exit code 75), STOP and ask the user to re-run the command. If governance cannot be loaded, STOP.

Read:

`<governance-home>/extension/docs/feature-architecture-policy.md`

## 2. Add a Feature Governance analysis category

In addition to normal spec/plan/tasks consistency analysis, check:

- whether `spec.md` defines a coherent `## Feature Boundary`;
- whether `plan.md` preserves established Earlier Feature boundaries;
- whether dependency direction remains earlier -> stable contract -> current/later;
- whether an Earlier Feature has gained downstream-specific knowledge or newly discovered Current-Feature responsibility;
- whether `tasks.md` contains hidden or explicit backward work;
- whether any backward exception is genuinely necessary, human-approved, and limited to minimum scope;
- whether the plan is attempting greenfield re-optimization of accepted historical architecture.

Use relevant Earlier Feature artifacts as evidence, but inspect only those needed to resolve the suspected boundary/ownership question.

## 3. Severity

Classify unauthorized backward propagation as `CRITICAL` because it violates binding global Feature governance.

Examples include:

- changing an Earlier Feature solely to simplify the Current Feature;
- moving newly discovered responsibility upstream without an approved exception;
- widening an Earlier Feature contract because a later consumer wants richer data when a correct adapter/downstream contract is viable;
- `[BACKWARD]` tasks without an approved `backward-exception.md`;
- an exception justified only by cleanliness, convenience, fewer adapters, or less duplication.

Keep this command read-only. Report findings; do not rewrite specs, plans, tasks, Earlier Features, or exception approval status.
