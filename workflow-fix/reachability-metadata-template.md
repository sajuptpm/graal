# Workflow Fix & Audit Documentation: `reachability-metadata-template.yml`

## 1. Workflow Overview & Triggers
- **Workflow Name**: Weekly Reachability Metadata Tests (Template)
- **File Path**: `.github/workflows/reachability-metadata-template.yml`
- **Original Purpose**: Reusable template providing orchestration to dynamically query the top 256 coordinates in `oracle/graalvm-reachability-metadata`, compile GraalVM Native Image, and execute JUnit/Gradle native tests across up to 256 parallel library matrix jobs.
- **Invoked By**:
  - `reachability-metadata.yml` (Top coordinates)
  - `reachability-metadata-future-defaults.yml` (`--future-defaults=all`)
  - `reachability-metadata-dedicated-layer.yml` (Dedicated layers)
  - `reachability-metadata-layered.yml` (Shared base layer)
  - `reachability-metadata-layered-future-defaults.yml` (Shared base layer + future defaults)
- **Triggers**:
  - `workflow_call`: Accepts `NATIVE_IMAGE_OPTIONS` and `LAYERED_TESTS`.

---

## 2. Upstream Architecture & Root Cause Analysis

### Issue 1: Upstream Guard Restriction
- **Error**: Workflow matrix population skipped because `if: (github.event_name == 'schedule' && github.repository == 'oracle/graal')`.
- **Root Cause**: Upstream restricted execution strictly to `oracle/graal`.

### Issue 2: Matrix Coordinates Limits & Python Parsing
- **Error**: Actionlint and matrix expressions validation errors when JSON output format was improperly delimited.
- **Root Cause**: Python script dynamically writes `matrix={"coordinates": [...]}` to `$GITHUB_OUTPUT`. Handled by strict JSON serialization.

---

## 3. Step-by-Step Fix Implementation

1. **Step 1: Relax Repository Guard**:
   Updated condition in `populate-matrix` to:
   ```yaml
   if: (github.event_name == 'schedule' && (github.repository == 'oracle/graal' || github.repository == 'sajuptpm/graal')) || (github.event_name != 'schedule')
   ```

2. **Step 2: Pin Immutable Action SHAs**:
   Pinned `actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd` (v6.0.2) and `actions/download-artifact@3e5f45b2cfb9172054b4087a40e8e0b5a5461e7c` (v8.0.1).

3. **Step 3: Explicit Permissions Scope**:
   Added `permissions: contents: read`.

4. **Step 4: Non-Blocking Matrix Isolation**:
   Maintained `fail-fast: false` so that independent library compatibility findings do not abort sibling test executions.

---

## 4. Verification Evidence & Run Logs
- **Verified Run ID**: [Run 44194643159](https://github.com/sajuptpm/graal/actions/runs/44194643159)
  - `Populate matrix`: **SUCCESS** (dynamically resolved and validated top coordinates)
  - `Build GraalVM`: **SUCCESS**
  - **Passed Test Coordinates**:
    - `it.unimi.dsi:fastutil:8.1.1` — **SUCCESS**
    - `org.springframework:spring:2.5` — **SUCCESS**
    - `org.springframework:spring-core:5.3.15` — **SUCCESS**
    - `org.apache.tomcat.embed:tomcat-embed-core:10.0.20` — **SUCCESS**
    - `org.apache.tomcat.embed:tomcat-embed-core:11.0.22` / `11.0.23` — **SUCCESS**
    - `org.hibernate.orm:hibernate-core:6.1.1.Final` — **SUCCESS**
    - `org.hibernate:hibernate-core:5.6.14.Final` — **SUCCESS**
    - `org.hibernate.orm:hibernate-core:7.2.0.Final` / `7.3.0.Final` — **SUCCESS**
    - `org.modelmapper:modelmapper:3.2.0` — **SUCCESS**
    - `org.apache.pulsar:pulsar-client-all:4.2.5` — **SUCCESS**

---

## 5. Deliverable Files & Clean Diff Check
- **Diff File**: `workflow-fix/reachability-metadata-template.diff`
- **Reverse Apply Verification**: `git apply --check --reverse workflow-fix/reachability-metadata-template.diff` exits with code 0.
