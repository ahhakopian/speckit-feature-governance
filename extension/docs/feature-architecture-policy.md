# Global Feature Architecture Policy

Version: 1.0.0

## Scope

This policy governs **Spec Kit feature work only**. It is loaded by the `feature-governance` Spec Kit preset and the `feature-governance-guard` extension. It MUST NOT be treated as a general Codex rule outside Spec Kit workflows.

The purpose is to make sequential Feature development evolve forward by default while still allowing a narrowly controlled backward change when no correct forward-only architecture can satisfy the requirements.

## Definitions

- **Current Feature**: the Feature being specified, planned, analyzed, tasked, or implemented.
- **Earlier Feature**: an established Feature with a lower sequential Feature number than the Current Feature.
- **Established Feature**: a Feature whose boundary has already been accepted through prior Spec Kit work and is being consumed as upstream architecture by later Features.
- **Backward propagation**: a later Feature causing an Earlier Feature to absorb newly discovered responsibility, semantics, validation, state ownership, downstream-specific knowledge, or contract changes primarily to accommodate the later Feature.
- **Forward-only solution**: a solution that preserves Earlier Feature boundaries and implements new behavior in the Current Feature or a later layer through composition, adaptation, translation, orchestration, a new downstream contract, or a new Feature.

Sequential numeric Feature prefixes (`001-...`, `002-...`, and so on) are the canonical ordering when present.

## 1. Feature Boundary Design

Feature decomposition MUST be designed so that normal system evolution can proceed forward.

A Feature SHOULD own one coherent capability or responsibility. While the Current Feature is still being designed, the agent MUST actively reconsider its boundary if the proposed split would predictably force later work to rewrite upstream Features.

Each new `spec.md` MUST contain a concise `## Feature Boundary` section with:

- **Owns** — responsibilities introduced and owned by this Feature.
- **Does Not Own** — adjacent responsibilities deliberately kept outside this Feature.
- **Upstream Dependencies** — Earlier Features/contracts consumed by this Feature.
- **Forward Extension Model** — how later Features are expected to compose with or extend this capability.
- **Downstream-Specific Knowledge** — downstream concepts this Feature knows; normally `None` for concepts belonging to later Features.

The goal is stable ownership, not speculative generalization. Do NOT widen an Earlier Feature into a universal abstraction merely to anticipate unknown future requirements.

## 2. Dependency Direction and Downstream Ignorance

The preferred dependency direction is:

`Earlier Feature -> stable capability/contract -> Current/Later Feature`

A later Feature MAY consume, compose, adapt, translate, validate, or orchestrate an Earlier Feature's established output.

An Earlier Feature SHOULD NOT need knowledge of a later Feature's UI, transport, adapter details, workflow, terminology, integration mechanism, or downstream-only state.

If a proposed Current Feature requires an Earlier Feature to understand downstream-specific concepts, treat that as a boundary warning and seek a forward-only design first.

## 3. Boundary Stability

Before a boundary is established, decomposition may be revised freely.

After an Earlier Feature becomes established upstream architecture, its specification, plan, contract, responsibility ownership, and established behavior MUST be treated as stable by default.

A later Feature discovering that a different greenfield decomposition would now look cleaner is NOT sufficient reason to rewrite the Earlier Feature.

## 4. Evolutionary Architecture over Greenfield Re-optimization

When working in an established project, optimize from the accepted architecture forward.

The operative question is:

> What is the cleanest correct forward evolution of the accepted architecture?

Do NOT substitute this question:

> How would I redesign the whole system if I were starting from scratch today?

Historical architecture is an input constraint unless it makes a binding requirement impossible to satisfy or itself violates a binding project/global rule.

## 5. Forward-Only Feature Evolution

Project evolution MUST be forward-only by default.

When a Current Feature conflicts with an Earlier Feature boundary, evaluate remedies in this order where applicable:

1. Use the Earlier Feature's existing contract as defined.
2. Adapt the Current Feature to that contract.
3. Add translation, normalization, validation, compatibility, or adapter logic at the Current Feature boundary.
4. Introduce a new forward-facing contract owned by the Current Feature or a later layer.
5. Move the new responsibility into a distinct later Feature when it is independently coherent.

A later Feature MUST NOT modify an Earlier Feature merely because doing so is cleaner, shorter, more elegant, reduces adapters, avoids duplication, simplifies ownership, or requires less implementation work.

If a viable forward-only solution satisfies all binding requirements, it MUST be preferred over a backward change even when it is somewhat less convenient.

When uncertain, preserve the Earlier Feature and surface the conflict for review rather than propagating the change backward.

## 6. Backward Exception Protocol

Backward modification is an architectural exception, not a normal refinement mechanism.

A backward exception MAY be proposed only when every viable forward-only architecture would necessarily violate at least one of:

- an explicit requirement of the Current Feature;
- an established contract that cannot be adapted around correctly;
- a binding project Constitution principle;
- this Global Feature Architecture Policy;
- a demonstrated technical impossibility that is material to the required behavior.

The following are NOT sufficient justification by themselves:

- cleaner architecture;
- fewer lines of code;
- fewer adapters or translation layers;
- less duplication;
- simpler naming;
- more elegant ownership;
- implementation convenience;
- preference for a greenfield redesign.

### Required exception artifact

If planning establishes that backward impact is unavoidable, create `backward-exception.md` in the Current Feature directory with this structure:

```markdown
# Backward Exception

**Current Feature:** <feature>
**Affected Earlier Feature(s):** <feature(s)>
**Status:** PROPOSED

## Architectural Conflict
<Concrete contradiction that cannot be resolved forward.>

## Binding Requirement or Constraint
<Requirement/contract/Constitution/policy/technical constraint that forces the conflict.>

## Forward Alternatives Considered

### Alternative A
<Architecture>

**Why it fails:** <binding reason, not convenience>

### Alternative B
<Architecture>

**Why it fails:** <binding reason, not convenience>

## Minimum Backward Change
<Exact smallest Earlier Feature change required.>

## Scope Boundaries
<What MUST remain unchanged.>

## Human Decision
**Status:** PROPOSED
```

The agent MUST NOT mark an exception `APPROVED` on its own. Approval requires an explicit human decision. Until approval is explicit, Earlier Feature artifacts MUST remain unchanged and executable backward tasks MUST NOT be treated as ready for implementation.

After approval, only the minimum documented backward scope may be changed. Any material scope expansion requires renewed human review.

## Stage Expectations

### Specify

Design the Current Feature boundary to support forward evolution. Do not rewrite Earlier Features during specification merely to make the new Feature easier to express.

### Plan

Perform an explicit `Forward Evolution Check`. Prefer forward-only architecture. If and only if no correct forward-only solution exists, create a `backward-exception.md` with status `PROPOSED` and stop before changing Earlier Features.

### Tasks

Tasks targeting Earlier Features are prohibited unless an approved exception exists. Approved backward tasks MUST be marked `[BACKWARD]` and reference `backward-exception.md`.

### Analyze / Governance Review

Treat unauthorized backward propagation as a blocking governance violation. Review both direct file changes and semantic responsibility transfer.
