# Workflow Fix & Audit Documentation: `micronaut-template.yml`

## 1. Workflow Overview & Triggers
- **Workflow Name**: Weekly Micronaut Tests (Template)
- **File Path**: `.github/workflows/micronaut-template.yml`
- **Original Purpose**: Reusable template providing the orchestration to build GraalVM and run native integration tests on Micronaut applications. Invoked by `micronaut.yml` and `micronaut-future-defaults.yml`.
- **Triggers**:
  - `workflow_call`: Receives optional input `NATIVE_IMAGE_OPTIONS`.
- **Job Dependency Graph**:
  - `build-graalvm` -> `build-and-test-micronaut` (`Native Tests`).

## 2. Upstream Architecture & Root Cause Analysis
- **Upstream Guard Restriction**: Scheduled executions were blocked on non-oracle repositories due to hardcoded check `github.repository == 'oracle/graal'`.

## 3. Key Changes & Fork Adaptations
- **Dynamic Guard**: Relaxed repository check to `(github.repository == 'oracle/graal' || github.repository == 'sajuptpm/graal')`.
- **Runner Pinning**: Pinned runner to `ubuntu-22.04`.

## 4. Verification Evidence & Run Logs
- **Passing Verification Run**:
  - **Run ID**: [44110812632](https://github.com/sajuptpm/graal/actions/runs/44110812632) (via `micronaut.yml`)
  - **Status**: `build-graalvm` succeeded in 7m37s, `Native Tests` executing.

## 5. Security, Secrets, & Environment Isolation
- `contents: read` permissions.
- Action references pinned to commit SHAs.

## 6. Reproducibility & Upstream Compatibility
- Diff is strictly cumulative against `$BASE_COMMIT`.
- Backward compatible with upstream repository.
