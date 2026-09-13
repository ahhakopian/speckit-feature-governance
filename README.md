# Feature Governance for SpecKit

This package provides forward-oriented Feature governance for SpecKit through
the `feature-governance` Preset and the `feature-governance-guard` Extension.
The Extension runs mandatory, read-only governance checkpoints at `after_tasks`
and `before_implement`.

## Components

- `preset/` — `feature-governance@1.0.1`
- `extension/` — `feature-governance-guard@1.0.1`

## Installation from GitHub

Use SpecKit `0.16.2` and run the installation commands from an initialized
SpecKit project (a directory containing `.specify/`). Clone the pinned source
tag, then install both components with the native local/dev mechanism:

```bash
git clone --branch v1.0.1 \
  https://github.com/ahhakopian/speckit-feature-governance.git \
  ~/tools/speckit-feature-governance

cd /path/to/your-spec-kit-project
specify extension add --dev ~/tools/speckit-feature-governance/extension --priority 10
specify preset add --dev ~/tools/speckit-feature-governance/preset --priority 10
```

This installation uses the checked-out source directly; it does not require a
ZIP artifact, GitHub Release, catalog, custom installer, or bootstrap command.

## Verification

```bash
cd /path/to/your-spec-kit-project
specify preset list
specify extension list
```

The lists should show `feature-governance` at `v1.0.1` and enabled, and
`feature-governance-guard` at `v1.0.1` with status `Enabled`.

## Greenfield integration

This package can be used independently. [SpecKit Greenfield Governance](https://github.com/ahhakopian/speckit-greenfield-governance)
uses it as a dependency. When both `architecture/baseline.md` and `ROADMAP.md`
exist, the Extension additionally applies Greenfield foundation checks; without
them, legacy Feature Governance behavior is preserved.
