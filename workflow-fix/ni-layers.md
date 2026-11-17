# Workflow Fix & Audit Documentation: `ni-layers.yml`

## 1. Workflow Overview & Triggers
- **Workflow Name**: Weekly Native Image Layer Building Tests
- **File Path**: `.github/workflows/ni-layers.yml`
- **Original Purpose**: Build a GraalVM distribution including Native Image and Native Image Configure Tool, populate an execution matrix combining pairs of popular Java/Kotlin libraries, and test layered native image builds for each library pair to ensure layer isolation and compatibility.
- **Triggers**:
  - `schedule`: Weekly on Monday at 02:00 UTC (`cron: '0 2 * * 1'`).
  - `workflow_dispatch`: Manual trigger.
  - `pull_request`: Triggered on PR modifications to `vm/tests/gh_workflows/NILayerTests/**` and `.github/workflows/ni-layers.yml`.
- **Job Dependency Graph**:
  - `build-graalvm` (reusable workflow `build-graalvm.yml`) runs first.
  - `populate-matrix` generates dynamic JSON matrix coordinates for library pairs.
  - `test-native-image-layer-build` executes in parallel for every library pair coordinate from the populated matrix, downloading and testing with the built GraalVM distribution.

## 2. Upstream Architecture & Root Cause Analysis
- **Hardcoded Upstream Repository Guards**: Upstream restricted `build-graalvm` and `populate-matrix` jobs with `if: (github.repository=='oracle/graal')`. In a fork environment (`sajuptpm/graal`), this prevented all jobs from executing.
- **Runner & Python Toolcache Incompatibility**: Upstream specified `runs-on: ubuntu-latest` with `PYTHON_VERSION: 3.12.3`. When GitHub hosted runners migrated `ubuntu-latest` toward Ubuntu 26, patch-level point release `3.12.3` was not present in the toolcache image, causing `actions/setup-python` to fail with `The version '3.12.3' with architecture 'x64' was not found for Ubuntu 26.04`. Pinning `runs-on: ubuntu-22.04` and using major.minor version `'3.12'` guarantees instantaneous toolcache availability.

## 3. Key Changes & Fork Adaptations
- **Dynamic Repository Guard**: Replaced hardcoded `(github.repository=='oracle/graal')` checks with `${{ github.repository == 'sajuptpm/graal' || github.repository == 'oracle/graal' }}` across `build-graalvm` and `populate-matrix`.
- **Python Versioning**: Updated `PYTHON_VERSION` from `3.12.3` to `'3.12'` to leverage pre-cached versions across runner pools.
- **Runner Pinning**: Pinned runners in `populate-matrix` and `test-native-image-layer-build` to `ubuntu-22.04`.

## 4. Verification Evidence & Run Logs
- **Passing Verification Run**:
  - **Run ID**: [44112680112](https://github.com/sajuptpm/graal/actions/runs/44112680112)
  - **Workflow**: `Weekly Native Image Layer Building Tests`
  - **Branch**: `workflow-fix/audit-all-workflows`
  - **Event**: `workflow_dispatch`
- **Executed Jobs**:
  - `build-graalvm / Build GraalVM`: `success` (8m16s, produced `graalvm` artifact).
  - `Populate matrix`: `success` (24s, generated pairwise library matrix).
  - `org.slf4j:slf4j-api:2.0.16 && org.jetbrains.kotlin:kotlin-stdlib:2.0.20`: `success`.
  - `org.apache.logging.log4j:log4j-api:2.24.0 && org.jetbrains.kotlin:kotlin-reflect:2.0.20`: `success`.
  - `joda-time:joda-time:2.12.7 && org.junit.jupiter:junit-jupiter:5.11.0`: `success`.
  - `commons-logging:commons-logging:1.3.4 && org.testng:testng:7.10.2`: `success`.
  - `org.jetbrains.kotlin:kotlin-stdlib-js:1.9.25 && org.apache.commons:commons-collections4:4.4`: `success`.
  - `org.apache.maven:maven-core:3.9.9 && org.yaml:snakeyaml:2.3`: `success`.
  - `com.google.inject:guice:7.0.0 && org.easymock:easymock:5.4.0`: `success`.

## 5. Security, Secrets, & Environment Isolation
- **Permissions**: Scoped read-only permissions (`contents: read`).
- **Artifacts**: Uses standard GitHub Actions artifacts (`actions/upload-artifact` and `actions/download-artifact`) for sharing the GraalVM archive across jobs without exposing sensitive data.
- **No Third-Party Secrets Required**: The workflow operates fully on public repositories and standard dependencies.

## 6. Reproducibility & Upstream Compatibility
- **Minimal Surgical Changes**: Exactly 6 lines modified in `.github/workflows/ni-layers.yml`.
- **Upstream Mergeable**: Dynamic repository checks preserve full functionality in `oracle/graal` while enabling fork execution.
- **Clean Diff Application**: The diff applies cleanly with `git apply --check` against the baseline commit.
