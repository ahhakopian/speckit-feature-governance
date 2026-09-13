
# Global Feature Governance — Specify Addendum

These instructions apply in addition to the standard `speckit.specify` workflow.

## 1. Load the installed native policy

Read the policy shipped with the installed `feature-governance-guard` extension:

`.specify/extensions/feature-governance-guard/docs/feature-architecture-policy.md`

If that native extension policy cannot be loaded, STOP rather than silently
continuing without it. Treat it as binding for this Spec Kit invocation only;
do not apply it to ordinary Codex work outside Spec Kit.

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
