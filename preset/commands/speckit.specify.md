
# Global Feature Governance — Specify Addendum

These instructions apply in addition to the standard `speckit.specify` workflow.

## 1. Synchronize governance first

Before doing specification work, run the global governance bootstrap in `ensure-project` mode. Resolve the governance home from `SPECKIT_FEATURE_GOVERNANCE_HOME` when set; otherwise use `~/.config/speckit-feature-governance`.

Preferred command on Unix-like systems:

```bash
python3 "${SPECKIT_FEATURE_GOVERNANCE_HOME:-$HOME/.config/speckit-feature-governance}/bootstrap/specify-governed.py" ensure-project --project-root . --quiet
```

If the bootstrap reports `GOVERNANCE_UPDATED_RESTART_REQUIRED` (exit code 75), STOP and ask the user to invoke the same Spec Kit command again so the refreshed command/skill is loaded. If governance cannot be loaded, STOP rather than silently continuing without it.

Then read the global policy from:

`<governance-home>/extension/docs/feature-architecture-policy.md`

Treat that file as binding for this Spec Kit invocation. Do not apply it to ordinary Codex work outside Spec Kit.

## 2. Apply Feature Boundary Design while running the core workflow

When defining the Current Feature:

- prefer one coherent responsibility;
- distinguish what the Feature owns from what it explicitly does not own;
- identify established Earlier Features/contracts it consumes;
- keep downstream-specific concepts out of Earlier Features;
- prefer a decomposition that allows later work to extend through composition, adaptation, orchestration, or a later Feature;
- do not over-generalize an Earlier Feature merely to anticipate unknown future needs.

If the Current Feature itself is still being designed and its boundary is poor, revise the Current Feature decomposition now. Do not use a later requirement as a reason to casually rewrite an already established Earlier Feature.

## 3. Required `spec.md` section

Before `speckit.specify` is considered complete, ensure the resulting `spec.md` contains this concise section:

```markdown
## Feature Boundary

### Owns
- ...

### Does Not Own
- ...

### Upstream Dependencies
- ...

### Forward Extension Model
- ...

### Downstream-Specific Knowledge
- None / ...
```

Keep the section architectural and concise. Do not turn `spec.md` into an implementation plan.

If the requested behavior appears to require changing an Earlier Feature, record the potential conflict in the Current Feature specification, preserve the Earlier Feature, and defer the architectural necessity decision to planning. Do not create or approve a backward exception during specification merely for convenience.
