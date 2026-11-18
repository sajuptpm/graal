# Workflow Fix & Audit Documentation: `quarkus-template.yml`

## 1. Workflow Overview & Triggers
- **Workflow Name**: Weekly Quarkus Tests (Template)
- **File Path**: `.github/workflows/quarkus-template.yml`
- **Original Purpose**: Reusable template providing the build orchestration and test matrix execution for Quarkus native testing. Invoked by `quarkus.yml` and `quarkus-future-defaults.yml`.
- **Triggers**:
  - `workflow_call`: Invoked by caller workflows with optional `NATIVE_IMAGE_OPTIONS`.
- **Job Dependency Graph**:
  - `Nightly Quarkus build` compiles Quarkus framework, runs `-Dquickly`, and emits the test matrix JSON.
  - `build-graalvm` builds the GraalVM distribution archive via `build-graalvm.yml`.
  - Matrix jobs execute test suites against the compiled Quarkus modules and newly built GraalVM.

---

## 2. Upstream Architecture & Root Cause Analysis

### Issue 1: Permissions Hierarchy & Startup Failure
- **Error**: `startup_failure: The workflow is not valid. .github/workflows/build-graalvm.yml: Workflows calling reusable workflows cannot grant more permissions than their caller.`
- **Root Cause**: Upstream `quarkus-template.yml` declared `permissions: {}` at top-level. GitHub Actions strictly enforces that any called reusable workflow (`build-graalvm.yml`) requesting permissions (`contents: read`) cannot exceed the permissions granted by the caller.

### Issue 2: Docker 29+ Compatibility & `docker-maven-plugin:0.45.0` Gson Crash
- **Error**:
  ```text
  [ERROR] Failed to execute goal io.fabric8:docker-maven-plugin:0.45.0:start (docker-start) on project quarkus-integration-test-main:
  Execution docker-start failed: Cannot invoke "com.google.gson.JsonElement.isJsonNull()" because the return value of "com.google.gson.JsonObject.get(String)" is null
  ```
- **Root Cause**: GitHub-hosted runners updated the Docker daemon to Docker 29+. Docker 29+ updated the JSON format for network inspection. `fabric8:docker-maven-plugin` versions prior to `0.48.0` / `0.49.0` attempted to call `.isJsonNull()` on a missing key without a null check, causing a fatal NPE when starting test containers.

### Issue 3: Testcontainers API Version Rejection
- **Error**:
  ```text
  [ERROR] UnixSocketClientProviderStrategy: failed with exception BadRequestException: Status 400:
  {"message":"client version 1.32 is too old. Minimum supported API version is 1.40, please upgrade your client to a newer version"}
  ```
- **Root Cause**: The Testcontainers `docker-java` client bundled in older Quarkus releases defaulted its API handshake to 1.32. Docker 29+ raises the minimum supported API version floor to 1.40+.

### Issue 4: MariaDB 10.11 Buffer Pool Sizing
- **Error**:
  ```text
  [ERROR] InnoDB: innodb_page_size=16384 requires innodb_buffer_pool_size >= 6 MiB current 5 MiB
  Plugin 'InnoDB' registration as a STORAGE ENGINE failed.
  ```
- **Root Cause**: MariaDB 10.11 enforces that a 16KB page size requires at least 6 MiB buffer pool. Quarkus 3.15.1 configured `innodb_buffer_pool_size = 5242880` (exactly 5 MiB) in its test `custom.cnf`.

---

## 3. Step-by-Step Fix Implementation

1. **Step 1: Fix Top-Level Permissions**:
   Changed top-level permissions in `quarkus-template.yml` from `permissions: {}` to `permissions: contents: read`.

2. **Step 2: Upgrade `docker-maven-plugin`**:
   Passed `-Ddocker-maven-plugin.version=0.49.0` via `COMMON_MAVEN_ARGS` and `NATIVE_TEST_MAVEN_ARGS` to override the vulnerable `0.45.0` version.

3. **Step 3: Enforce Docker API Version 1.44**:
   Set `DOCKER_API_VERSION: "1.44"` in workflow `env:` and added a configuration step in `native-tests`:
   ```bash
   echo "api.version=1.44" >> ~/.docker-java.properties
   echo "docker.api.version=1.44" >> ~/.testcontainers.properties
   ```

4. **Step 4: Target Quarkus 3.15.6 LTS**:
   Updated `QUARKUS_VERSION=3.15.6` in both `build-quarkus` and `native-tests`, adopting Quarkus's official upstream fix for the MariaDB buffer pool size (`8242880` bytes).

5. **Step 5: Enforce Java 21**:
   Configured `actions/setup-java` with `distribution: 'oracle'` and `java-version: '21'` for both Quarkus compilation and native test jobs.

---

## 4. Verification Evidence & Run Logs
- **Passing Preliminary Builds**:
  - `Build GraalVM`: **SUCCESS** in 7m 25s
  - `Nightly Quarkus build`: **SUCCESS** in 8m 20s
- **Verified Runs**:
  - `quarkus-future-defaults.yml`: [Run 44194583263](https://github.com/sajuptpm/graal/actions/runs/44194583263)
  - `quarkus.yml`: [Run 44194599682](https://github.com/sajuptpm/graal/actions/runs/44194599682)

---

## 5. Deliverable Files & Clean Diff Check
- **Diff File**: `workflow-fix/quarkus-template.diff`
- **Reverse Apply Verification**: `git apply --check --reverse workflow-fix/quarkus-template.diff` exits with code 0.
