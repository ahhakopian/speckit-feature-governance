---
description: "Mandatory read-only Feature governance gate"
---

# Feature Governance Review

This command is a mandatory, read-only governance gate. It MUST NOT edit `spec.md`, `plan.md`, `tasks.md`, Earlier Feature artifacts, source code, or exception approval status.

## 1. Load the installed native policy

Read the policy shipped with this installed extension:

`.specify/extensions/feature-governance-guard/docs/feature-architecture-policy.md`

If that policy cannot be loaded, return `FEATURE_GOVERNANCE: BLOCK` and stop.
Do not silently fall back to a project copy.

## 2. Resolve the Current Feature

Use normal Spec Kit project state (`.specify/feature.json`, active Feature context, `SPECIFY_FEATURE_DIRECTORY`, or equivalent current Spec Kit context) to identify the Current Feature directory.

When sequential numeric prefixes are present, treat lower-numbered Feature directories as Earlier Features. Do not guess Feature ordering when it cannot be resolved from project state/naming; report the ambiguity as blocking if it prevents a reliable governance decision.

## 3. Read the minimum evidence needed

Always inspect the Current Feature's available:

- `spec.md`;
- `plan.md`;
- `tasks.md`.

Inspect `backward-exception.md` when present or referenced.

For Earlier Features, first inspect only relevant `## Feature Boundary` sections and the contracts/artifacts directly implicated by the Current Feature. Expand to additional Earlier Feature content only when needed to resolve ownership or semantics. Avoid broad unrelated archaeology.

If Git is available, use the current diff/status only as supplementary evidence for direct edits to lower-numbered Feature artifacts. Git evidence is helpful but not required for a semantic verdict.

## 3A. Apply Greenfield foundation checks conditionally

At the start of every review invocation, check for both
`architecture/baseline.md` and `ROADMAP.md` at the project root.

If either file is absent, skip this section completely and preserve the
existing Feature Governance evaluation and verdict behavior below.

If both files exist, read the Approved Architecture Baseline and only the
Current Feature's ROADMAP entry plus the entries needed to evaluate its
dependencies and order. These checks are additional mandatory conditions for
`FEATURE_GOVERNANCE: PASS`:

1. The Current Feature is linked to an actionable, unblocked ROADMAP entry.
2. `spec.md`, `plan.md`, and `tasks.md` remain within that entry's outcome and
   scope boundary.
3. The artifacts preserve the entry's assigned architecture responsibility and
   conform to the Approved Architecture Baseline.
4. The entry's declared dependencies and ordering constraints are satisfied.
5. `plan.md` records the architecture compatibility result `COMPATIBLE`.
6. `tasks.md` introduces no new product decision and no new material
   architecture decision.

Evaluate these conditions from the current files on every invocation; do not
reuse an earlier result. This makes the `before_implement` invocation repeat
compatibility review after `analyze` or any intervening edits.

If correct delivery requires changing product scope, capability, actor,
authority, ownership, or a product boundary, return
`FEATURE_GOVERNANCE: BLOCK`, route the decision to the Canonical PRD, and stop.
Do not repair or reinterpret the product decision in Feature artifacts.

If correct delivery requires a material change to the Approved Architecture
Baseline, return `FEATURE_GOVERNANCE: BLOCK`, report
`BASELINE_CHANGE_REQUIRED`, and stop until Controlled Architecture Change is
complete and the Feature is again `COMPATIBLE`.

An existing Feature Governance backward exception or approval does not
authorize either kind of upstream change. Do not modify the baseline, ROADMAP,
Canonical PRD, or Feature artifacts during this review.

## 4. Evaluate the governance invariants

Answer these questions:

1. **Boundary cohesion** — Does the Current Feature own a coherent responsibility with clear `Owns` / `Does Not Own` boundaries?
2. **Dependency direction** — Does the design primarily consume Earlier Feature capabilities rather than push Current-Feature responsibility upstream?
3. **Downstream ignorance** — Are Earlier Features free of Current/Later-Feature-specific UI, transport, adapter, workflow, terminology, and downstream-only state unless inherently required by their established domain responsibility?
4. **Forward evolution** — Did planning seriously prefer existing contracts, current-layer adaptation, adapters/translation, new downstream contracts, or later Features before proposing upstream changes?
5. **No greenfield rewrite** — Is any upstream change justified by actual necessity rather than "this would be cleaner if redesigned today"?
6. **Task direction** — Do tasks avoid unauthorized work on Earlier Feature specifications, contracts, responsibilities, or semantics?
7. **Exception validity** — If backward impact exists, is `backward-exception.md` present, materially justified by binding constraints, explicitly human-approved, and limited to the minimum scope?

Convenience, fewer adapters, less code, less duplication, cleaner ownership, preferred naming, or architectural elegance alone MUST NOT satisfy exception necessity.

## 5. Verdict

Return exactly one leading status line:

```text
FEATURE_GOVERNANCE: PASS
```

or

```text
FEATURE_GOVERNANCE: EXCEPTION_REQUIRED
```

or

```text
FEATURE_GOVERNANCE: BLOCK
```

Then give a concise evidence-based explanation.

### PASS

Use only when no unauthorized backward propagation exists, or when a genuinely necessary backward exception is explicitly human-approved and the proposed work stays within its minimum scope.

### EXCEPTION_REQUIRED

Use when backward impact may be architecturally necessary but is missing a valid, approved exception. Identify the exact conflict and the forward alternatives that still need to be ruled out or documented.

### BLOCK

Use when the Current Feature violates the policy and a correct forward-only solution exists, when an exception is justified only by convenience/cleanliness, when Feature ordering/evidence is too ambiguous for a safe decision, or when the global policy cannot be loaded.

For `EXCEPTION_REQUIRED` or `BLOCK`, explicitly instruct the parent Spec Kit workflow to STOP. Do not continue into implementation and do not repair the artifacts automatically. Human review decides the next action.
