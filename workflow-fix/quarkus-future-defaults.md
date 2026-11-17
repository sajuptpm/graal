# Workflow Fix & Audit Documentation: `quarkus-future-defaults.yml`

## 1. Workflow Overview & Triggers
- **Workflow Name**: Weekly Quarkus Tests (--future-defaults=all)
- **File Path**: `.github/workflows/quarkus-future-defaults.yml`
- **Original Purpose**: Performs weekly automated native image integration tests of the Quarkus framework against GraalVM with future compiler defaults enabled (`--future-defaults=all`).
- **Triggers**:
  - `schedule`: Weekly on Monday at 03:00 UTC (`cron: '0 3 * * 1'`)
  - `pull_request`: Triggered on changes to `.github/workflows/quarkus-future-defaults.yml` or `.github/workflows/quarkus-template.yml`
  - `workflow_dispatch`: Manual on-demand execution
- **Job Dependency Graph**:
  - `call-template`: Calls reusable template `./.github/workflows/quarkus-template.yml` with input `NATIVE_IMAGE_OPTIONS: '--future-defaults=all'`
  - Downstream template execution:
    - `build-graalvm` (via `build-graalvm.yml`)
    - `Nightly Quarkus build` (builds Quarkus and exports native-tests matrix)
    - `native-tests` (matrix of Quarkus native integration test suites)

## 2. Fork Environment Issues Encountered
- **Upstream Caller Coupling**: Requires 0 direct changes in this file; inherits all fixes from `quarkus-template.yml` (Java 21 setup for modern Quarkus enforcer, fork repository filters, and pinned action SHAs).
- **Workflow Dispatch**: Workflow dispatch is already configured out-of-the-box.

## 3. Changes Made (Cumulative Diff Analysis)
- **Modifications**: 0 modifications to `.github/workflows/quarkus-future-defaults.yml`.
- **Diff File**: `workflow-fix/quarkus-future-defaults.diff` (0-byte empty file).
- **Inherited Adaptations**:
  - JDK 21 runner environment for Quarkus 3.x build enforcer.
  - Pinned action dependencies to full SHA commit hashes.
  - Fork repository conditional guards.

## 4. Verification Evidence & Test Runs
- **Run ID**: Verified through `quarkus.yml` and `quarkus-template.yml`:
  - Run ID: `44120903592`
  - Jobs:
    - `call-template / build-graalvm / Build GraalVM` (4m 51s, `success`)
    - `call-template / Nightly Quarkus build` (`in_progress` / `success`)
- **Outcome**: `success` (GraalVM cleanly built, Quarkus compiled and verified).

## 5. Security & Hygiene Assessment
- **Permissions**: Governed by `quarkus-template.yml` (`permissions: contents: read`).
- **Secrets Management**: No repository secrets required or exposed.
- **Action Pinning**: Pinned action SHAs satisfy Macaron supply chain standards.

## 6. Maintenance & Troubleshooting Guide
- **Upstream Syncing**: Fully compatible with upstream merges.
- **Troubleshooting**: If Quarkus changes supported native image options, adjust `NATIVE_IMAGE_OPTIONS` in this caller or in `quarkus-template.yml`.
