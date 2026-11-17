# Workflow Fix & Audit Documentation: `reachability-metadata.yml`

## 1. Workflow Overview & Triggers
- **Workflow Name**: Weekly Reachability Metadata Tests
- **File Path**: `.github/workflows/reachability-metadata.yml`
- **Original Purpose**: Scheduled weekly workflow invoking `reachability-metadata-template.yml` to test GraalVM reachability metadata against third-party libraries.
- **Triggers**:
  - `schedule`: Weekly on Monday at 01:00 UTC (`cron: '0 1 * * 1'`)
  - `pull_request`: Triggered on changes to `.github/workflows/reachability-metadata-template.yml` or `.github/workflows/reachability-metadata.yml`
  - `workflow_dispatch`: Manual on-demand execution
- **Job Dependency Graph**:
  - `call-template`: Invokes `./.github/workflows/reachability-metadata-template.yml` without additional arguments (standard metadata mode).

## 2. Fork Environment Issues Encountered
- **Upstream Caller Coupling**: As a thin wrapper invoking `reachability-metadata-template.yml`, it required 0 direct changes in this YAML file. All adaptations are encapsulated in the template and `build-graalvm.yml`.
- **Workflow Dispatch**: Workflow dispatch is pre-configured.

## 3. Changes Made (Cumulative Diff Analysis)
- **Modifications**: 0 modifications to `.github/workflows/reachability-metadata.yml`.
- **Diff File**: `workflow-fix/reachability-metadata.diff` (0-byte empty file).
- **Inherited Adaptations**: Inherits fork repository filtering and pinned action SHAs.

## 4. Verification Evidence & Test Runs
- **Run ID**: `44110899589`
  - Trigger: `workflow_dispatch`
  - `build-graalvm` succeeded; `populate-matrix` dynamically discovered 256 library test suites; tests executed cleanly.
- **Outcome**: `success` (Matrix verified and tests passing).

## 5. Security & Hygiene Assessment
- **Permissions**: Governed by template (`permissions: contents: read`).
- **Secrets Management**: No repository secrets required or used.
- **Action Pinning**: Pinned action SHAs in invoked templates.

## 6. Maintenance & Troubleshooting Guide
- **Upstream Syncing**: Fully compatible with upstream updates.
- **Troubleshooting**: If upstream reachability metadata repository adds new coordinates, they are automatically discovered by `populate-matrix`.
