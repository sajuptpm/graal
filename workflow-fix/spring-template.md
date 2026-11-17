# Workflow Fix & Audit Documentation: `spring-template.yml`

## 1. Workflow Overview & Triggers
- **Workflow Name**: Weekly Spring Tests (Template)
- **File Path**: `.github/workflows/spring-template.yml`
- **Original Purpose**: Reusable template providing the orchestration to build GraalVM and run native integration tests on the Spring PetClinic application. Invoked by `spring.yml` and `spring-future-defaults.yml`.
- **Triggers**:
  - `workflow_call`: Receives optional input `NATIVE_IMAGE_OPTIONS`.
- **Job Dependency Graph**:
  - `build-graalvm` -> `build-and-test-spring` (`Native Tests`).

## 2. Upstream Architecture & Root Cause Analysis
- **Upstream Guard Restriction**: Scheduled executions were blocked on non-oracle repositories due to hardcoded check `github.repository == 'oracle/graal'`.
- **Gradle 9 CycloneDX Conflict**: Spring PetClinic's build configuration conflicts with Gradle 9's lazy task registration.

## 3. Key Changes & Fork Adaptations
- **Dynamic Guard**: Relaxed repository check to `(github.repository == 'oracle/graal' || github.repository == 'sajuptpm/graal')`.
- **CycloneDX Remediation**: Inline Python sanitization of `build.gradle` to exclude the broken plugin before test execution.
- **Runner Pinning**: Pinned runner to `ubuntu-22.04`.

## 4. Verification Evidence & Run Logs
- **Passing Verification Run**:
  - **Run ID**: [44119506376](https://github.com/sajuptpm/graal/actions/runs/44119506376) / [44121138760](https://github.com/sajuptpm/graal/actions/runs/44121138760) (via `spring.yml`)
  - **Status**: `build-graalvm` succeeded, `Native Tests` executing.

## 5. Security, Secrets, & Environment Isolation
- `contents: read` permissions.
- Action references pinned to commit SHAs.

## 6. Reproducibility & Upstream Compatibility
- Diff is strictly cumulative against `$BASE_COMMIT`.
- Backward compatible with upstream repository.
