
# Global Feature Governance — Plan Addendum

These instructions apply in addition to the standard `speckit.plan` workflow.

## 1. Synchronize and load the global policy

Run the governance bootstrap before planning. Resolve `SPECKIT_FEATURE_GOVERNANCE_HOME` when set; otherwise use `~/.config/speckit-feature-governance`.

```bash
python3 "${SPECKIT_FEATURE_GOVERNANCE_HOME:-$HOME/.config/speckit-feature-governance}/bootstrap/specify-governed.py" ensure-project --project-root . --quiet
```

If it reports `GOVERNANCE_UPDATED_RESTART_REQUIRED` (exit code 75), STOP and ask the user to invoke the command again. If governance cannot be loaded, STOP.

Read and apply:

`<governance-home>/extension/docs/feature-architecture-policy.md`

## 2. Treat Earlier Features as established upstream architecture

Use the Current Feature's `## Feature Boundary` and relevant Earlier Feature specifications as architectural constraints.

Do not reason from a hypothetical greenfield redesign. Optimize from the accepted architecture forward.

When a conflict appears, evaluate forward remedies before any backward change:

1. use the Earlier Feature's existing contract;
2. adapt the Current Feature;
3. add adapter/translation/normalization/validation/compatibility logic at the Current Feature boundary;
4. add a new forward-facing contract owned by the Current Feature or a later layer;
5. split a genuinely independent responsibility into a later Feature.

Convenience, fewer lines of code, fewer adapters, less duplication, cleaner naming, or a more elegant greenfield ownership model are not architectural necessity.

## 3. Required `plan.md` section

Before planning is considered complete, ensure `plan.md` contains:

```markdown
## Forward Evolution Check

**Earlier Feature boundaries preserved:** Yes | No
**Backward impact:** None | Detected
**Forward mechanism:** <existing contract / composition / adapter / translation / new downstream contract / later Feature / other>
**Exception:** None | `backward-exception.md`

### Rationale
<Brief explanation of why this is the correct forward evolution.>
```

## 4. Backward exception handling

If a viable forward-only solution satisfies all binding requirements, select it and set `Backward impact: None`.

Only when every viable forward-only architecture fails a binding requirement/contract/Constitution/policy constraint or demonstrated technical impossibility MAY you create `backward-exception.md` in the Current Feature directory using the structure defined by the global policy.

When creating it:

- set status to `PROPOSED`;
- identify the exact Earlier Feature(s) affected;
- document at least the viable forward alternatives considered and the binding reason each fails;
- define the minimum backward change and scope boundaries;
- DO NOT modify Earlier Feature artifacts yet;
- DO NOT mark the exception `APPROVED` yourself.

If approval is required, surface the exception to the user and stop at the architectural decision boundary.
