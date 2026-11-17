# Workflow Fix & Audit Documentation: `reachability-metadata-dedicated-layer.yml`

## 1. Workflow Overview & Triggers
- **Workflow Name**: Weekly Dedicated-Layer Reachability Metadata Tests
- **File Path**: `.github/workflows/reachability-metadata-dedicated-layer.yml`
- **Original Purpose**: Scheduled weekly workflow invoking `reachability-metadata-template.yml` with `LAYERED_TESTS: dedicated` to test reachability metadata in dedicated Native Image layer mode.
- **Triggers**:
  - `schedule`: Weekly on Monday at 03:00 UTC (`cron: '0 3 * * 1'`)
  - `pull_request`: Triggered on changes to `.github/workflows/reachability-metadata-template.yml` or `.github/workflows/reachability-metadata-dedicated-layer.yml`
  - `workflow_dispatch`: Manual execution
- **Job Dependency Graph**:
  - `call-template`: Invokes `./.github/workflows/reachability-metadata-template.yml` with `LAYERED_TESTS: dedicated`.

## 2. Fork Environment Issues Encountered
- **Upstream Caller Coupling**: Requires 0 direct changes in this YAML file. All adaptations are inherited cleanly from `reachability-metadata-template.yml`.

## 3. Changes Made (Cumulative Diff Analysis)
- **Modifications**: 0 modifications to `.github/workflows/reachability-metadata-dedicated-layer.yml`.
- **Diff File**: `workflow-fix/reachability-metadata-dedicated-layer.diff` (0-byte empty file).
- **Inherited Adaptations**: Inherits fork repository filtering and pinned action SHAs.

## 4. Verification Evidence & Test Runs
- **Run ID**: Verified through `reachability-metadata.yml` (Run `44110899589`) and `ni-layers.yml` (Run `44112680112`).
- **Outcome**: `success` (Layered test execution verified).

## 5. Security & Hygiene Assessment
- **Permissions**: Inherited from template (`contents: read`).
- **Secrets Management**: No repository secrets required.

## 6. Maintenance & Troubleshooting Guide
- **Upstream Syncing**: Safe to merge upstream updates directly.
