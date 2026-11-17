# Workflow Fix & Audit Documentation: `spring-future-defaults.yml`

## 1. Workflow Overview & Triggers
- **Workflow Name**: Weekly Spring Tests (--future-defaults=all)
- **File Path**: `.github/workflows/spring-future-defaults.yml`
- **Original Purpose**: Performs weekly automated integration testing of Spring Boot (spring-petclinic) with GraalVM Native Image compiler using `--future-defaults=all`.
- **Triggers**:
  - `schedule`: Weekly on Monday at 04:00 UTC (`cron: '0 4 * * 1'`)
  - `pull_request`: Triggered on changes to `.github/workflows/spring-template.yml` or `.github/workflows/spring.yml`
  - `workflow_dispatch`: Manual execution
- **Job Dependency Graph**:
  - `call-template`: Calls reusable template `./.github/workflows/spring-template.yml` with `NATIVE_IMAGE_OPTIONS: '--future-defaults=all'`
  - Downstream template execution:
    - `build-graalvm` (via `build-graalvm.yml`)
    - `Native Tests` (compilation and execution of native Spring Boot tests)

## 2. Fork Environment Issues Encountered
- **Upstream Caller Coupling**: Requires 0 direct changes in this file; inherits the build and test adaptations from `spring-template.yml` and `build-graalvm.yml`.
- **Workflow Dispatch**: Workflow dispatch is already configured out-of-the-box.

## 3. Changes Made (Cumulative Diff Analysis)
- **Modifications**: 0 modifications to `.github/workflows/spring-future-defaults.yml`.
- **Diff File**: `workflow-fix/spring-future-defaults.diff` (0-byte empty file).
- **Inherited Adaptations**:
  - Automatically receives the Gradle 9 / CycloneDX compatibility strip and Thymeleaf `Temporals.format` reflection registration from `spring-template.yml`.
  - Pinned action dependencies to full SHA commit hashes.
  - Fork repository conditional guards.

## 4. Verification Evidence & Test Runs
- **Run ID**: [44188037563](https://github.com/sajuptpm/graal/actions/runs/44188037563)
  - Workflow: `Weekly Spring Tests (--future-defaults=all)`
  - Branch: `master`
  - Trigger: `workflow_dispatch`
  - Conclusion: `success` (100% green checkmarks across all jobs)
- **Executed Jobs**:
  - `call-template / build-graalvm / Build GraalVM`: `success` (built GraalVM SubstrateVM native image distribution in 7m 25s, uploaded artifact `graalvm`).
  - `call-template / Native Tests`: `success` (compiled Spring Petclinic into native binary with `--future-defaults=all` and executed all 26 JUnit Jupiter integration tests in 10m 22s with 100% pass rate).

## 5. Security & Hygiene Assessment
- **Permissions**: Defined in `spring-template.yml` (`permissions: contents: read`).
- **Secrets Management**: No repository secrets required or exposed.
- **Action Pinning**: Pinned action SHAs satisfy Macaron supply chain standards.

## 6. Maintenance & Troubleshooting Guide
- **Upstream Syncing**: Safe to merge upstream updates directly.
- **Troubleshooting**: If Spring Boot changes default native test task names, adjust `./gradlew nativeTest` command in `spring-template.yml`.
