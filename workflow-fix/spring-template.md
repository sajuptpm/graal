# Workflow Fix & Audit Documentation: `spring-template.yml`

## 1. Workflow Overview & Triggers
- **Workflow Name**: Weekly Spring Tests (Template)
- **File Path**: `.github/workflows/spring-template.yml`
- **Original Purpose**: Reusable template providing the orchestration to build GraalVM and run native integration tests on the Spring PetClinic application. Invoked by `spring.yml` and `spring-future-defaults.yml`.
- **Triggers**:
  - `workflow_call`: Receives optional input `NATIVE_IMAGE_OPTIONS`.
- **Job Dependency Graph**:
  - `build-graalvm` -> `build-and-test-spring` (`Native Tests`).

---

## 2. Upstream Architecture & Root Cause Analysis

### Issue 1: Repository Guard Restriction
- **Error**: Workflow skipped on schedule triggers because `if: (github.event_name == 'schedule' && github.repository == 'oracle/graal')`.
- **Root Cause**: Upstream restricted execution strictly to `oracle/graal`.

### Issue 2: Gradle 9 CycloneDX Conflict
- **Error**:
  ```text
  Execution failed for task ':cyclonedxBom'.
  Cannot query the value of this property because it has no value available.
  ```
- **Root Cause**: Spring Petclinic's latest `build.gradle` applies `org.cyclonedx.bom`, which fails lazy property mapping on Gradle 9.

### Issue 3: Thymeleaf Reflection Missing in Native Image Mode
- **Error**:
  ```text
  org.graalvm.nativeimage.MissingReflectionRegistrationError:
  The program tried to reflectively invoke method public java.util.List org.thymeleaf.expression.Numbers.sequence(java.lang.Integer,java.lang.Integer) without it being registered.
  HTTP 500 Internal Server Error when loading /owners?lastName=
  ```
- **Root Cause**: In `ownersList.html`, Thymeleaf executes `#numbers.sequence(1, totalPages)` reflectively for pagination links. Native Image AOT build had no reflection metadata for `org.thymeleaf.expression.Numbers`.

---

## 3. Step-by-Step Fix Implementation

1. **Step 1: Relax Repository Guard**:
   Updated condition to:
   ```yaml
   if: (github.event_name == 'schedule' && (github.repository == 'oracle/graal' || github.repository == 'sajuptpm/graal')) || (github.event_name != 'schedule')
   ```

2. **Step 2: Inline CycloneDX Sanitization**:
   Stripped the broken CycloneDX plugin tasks from `build.gradle` using python regex before test execution:
   ```bash
   python3 -c "
   import re
   p = 'build.gradle'
   c = open(p).read()
   c = re.sub(r'id\s+[\'\"]org\.cyclonedx\.bom[\'\"].*', '', c)
   open(p, 'w').write(c)
   "
   ```

3. **Step 3: Programmatic Reflection Configuration Injection**:
   Injected full reachability reflection configuration covering all 16 Thymeleaf expression helpers (`Numbers`, `Strings`, `Temporals`, `Lists`, `Dates`, `Maps`, `Sets`, `Objects`, etc.) and Petclinic model entities (`Owner`, `Pet`, `Visit`, etc.) into `reflect-config.json`.

4. **Step 4: Hook into Native Image Build Args**:
   Added `-H:ReflectionConfigurationFiles=...` to `graalvmNative.binaries.all.buildArgs` in `build.gradle`.

5. **Step 5: Runner & Java Pinning**:
   Pinned runner to `ubuntu-22.04` and `actions/setup-java` with `distribution: 'graalvm'`, `java-version: '21'`.

---

## 4. Verification Evidence & Run Logs
- **Verified Runs**:
  - `spring.yml`: [Run 44184945397](https://github.com/sajuptpm/graal/actions/runs/44184945397) — **100% SUCCESS** in 16m 53s.
    - `build-graalvm`: 7m 25s (`success`)
    - `Native Tests`: 7m 45s (`success`) — All 26 JUnit Jupiter tests passed cleanly.
  - `spring-future-defaults.yml`: [Run 44188037563](https://github.com/sajuptpm/graal/actions/runs/44188037563) — **100% SUCCESS** in 18m 54s.
    - `build-graalvm`: 7m 25s (`success`)
    - `Native Tests`: 10m 22s (`success`) — All 26 JUnit Jupiter tests passed natively with future defaults.

---

## 5. Deliverable Files & Clean Diff Check
- **Diff File**: `workflow-fix/spring-template.diff`
- **Reverse Apply Verification**: `git apply --check --reverse workflow-fix/spring-template.diff` exits with code 0.
