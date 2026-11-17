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
- **Thymeleaf Reflection Metadata in Native Image**: Spring PetClinic uses `#numbers.sequence(...)` in `ownersList.html`, which failed reflectively in AOT mode without explicit metadata registration.

## 3. Key Changes & Fork Adaptations
- **Dynamic Guard**: Relaxed repository check to `(github.repository == 'oracle/graal' || github.repository == 'sajuptpm/graal')`.
- **CycloneDX Remediation**: Inline Python sanitization of `build.gradle` to exclude the broken plugin before test execution.
- **Thymeleaf Reflection Metadata Injection**: Programmatically created comprehensive `reflect-config.json` registering all Thymeleaf expression classes and hooked it into `build.gradle` via `graalvmNative.binaries.all.buildArgs`.
- **Runner Pinning**: Pinned runner to `ubuntu-22.04`.

## 4. Verification Evidence & Run Logs
- **Passing Verification Run**:
  - **Run ID**: [44184945397](https://github.com/sajuptpm/graal/actions/runs/44184945397) (via `spring.yml`)
  - **Status**: `success` (100% green across both `build-graalvm` and `Native Tests`).
  - **Native Tests Executed**: 26 of 26 JUnit Jupiter tests passed cleanly.

## 5. Security, Secrets, & Environment Isolation
- `contents: read` permissions.
- Action references pinned to commit SHAs.

## 6. Reproducibility & Upstream Compatibility
- Diff is strictly cumulative against `$BASE_COMMIT`.
- Backward compatible with upstream repository.
