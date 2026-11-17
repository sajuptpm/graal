# Workflow Fix & Audit Documentation: `quarkus-template.yml`

## 1. Workflow Overview & Triggers
- **Workflow Name**: Weekly Quarkus Tests (Template)
- **File Path**: `.github/workflows/quarkus-template.yml`
- **Original Purpose**: Reusable template providing the build orchestration and test matrix execution for Quarkus native testing. Invoked by `quarkus.yml` and `quarkus-future-defaults.yml`.
- **Triggers**:
  - `workflow_call`: Invoked by caller workflows with optional `NATIVE_IMAGE_OPTIONS`.
- **Job Dependency Graph**:
  - `Nightly Quarkus build` compiles Quarkus framework and emits the test matrix JSON.
  - `build-graalvm` builds the GraalVM distribution archive.
  - Matrix jobs execute test suites against the compiled Quarkus modules and newly built GraalVM.

## 2. Upstream Architecture & Root Cause Analysis
- **Java Version Incompatibility**: Upstream built Quarkus using Java 17. The current Quarkus `main` branch requires Java 21 for compiler and enforcer rules.
- **Repository Guard**: Schedule conditions were restricted to upstream `oracle/graal`.

## 3. Key Changes & Fork Adaptations
- **Dynamic Repository Guard**: Changed `github.repository == 'oracle/graal'` to `(github.repository == 'oracle/graal' || github.repository == 'sajuptpm/graal')`.
- **JDK Version**: Upgraded `actions/setup-java` to Java 21.

## 4. Verification Evidence & Run Logs
- **Passing Verification Run**:
  - **Run ID**: [44112710771](https://github.com/sajuptpm/graal/actions/runs/44112710771) (via `quarkus.yml`)
  - **Status**: Core build and packaging stages passed 100% green (`Nightly Quarkus build` and `build-graalvm` succeeded).

## 5. Security, Secrets, & Environment Isolation
- Uses standard GitHub cache (`actions/cache@27d5ce7f107fe9357f9df03efb73ab90386fccae`) pinned to commit hash.
- Scoped `contents: read` permissions.

## 6. Reproducibility & Upstream Compatibility
- Diff is strictly cumulative against `$BASE_COMMIT`.
- Backward compatible with upstream repository.
