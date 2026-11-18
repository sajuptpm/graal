# Workflow Fix & Audit Documentation: `micronaut-template.yml`

## 1. Workflow Overview & Triggers
- **Workflow Name**: Weekly Micronaut Tests (Template)
- **File Path**: `.github/workflows/micronaut-template.yml`
- **Original Purpose**: Reusable template providing the orchestration to build GraalVM and run native tests on both a Micronaut starter launch project and the `micronaut-core` repository. Invoked by `micronaut.yml` and `micronaut-future-defaults.yml`.
- **Triggers**:
  - `workflow_call`: Receives optional input `NATIVE_IMAGE_OPTIONS`.
- **Job Dependency Graph**:
  - `build-graalvm` -> `Native Tests`.

---

## 2. Upstream Architecture & Root Cause Analysis

### Issue 1: Upstream Guard Restriction
- **Error**: Workflow did not execute on fork schedule because `if: (github.event_name == 'schedule' && github.repository == 'oracle/graal')`.
- **Root Cause**: Upstream strictly allowed scheduled runs on `oracle/graal`.

### Issue 3: Unpinned Action References
- **Error**: Macaron and SLSA Level 4 policy warnings on unpinned `@v4` actions.
- **Root Cause**: Action references lacked immutable 40-character commit SHAs.

---

## 3. Step-by-Step Fix Implementation

1. **Step 1: Relax Repository Guard**:
   Updated condition to:
   ```yaml
   if: (github.event_name == 'schedule' && (github.repository == 'oracle/graal' || github.repository == 'sajuptpm/graal')) || (github.event_name != 'schedule')
   ```

2. **Step 2: Pin Immutable Action SHAs**:
   Pinned `actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd` (v6.0.2) and `actions/download-artifact@3e5f45b2cfb9172054b4087a40e8e0b5a5461e7c` (v8.0.1).

3. **Step 3: Permissions Scope**:
   Added explicit `permissions: contents: read`.

4. **Step 4: Runner Environment**:
   Configured runner on `ubuntu-22.04` and verified both standard options and `--future-defaults=all`.

---

## 4. Verification Evidence & Run Logs
- **Verified Runs**:
  - `micronaut.yml`: [Run 44185159384](https://github.com/sajuptpm/graal/actions/runs/44185159384) — **100% SUCCESS** in 39m 12s.
    - `build-graalvm`: 7m 25s (`success`)
    - `Native Tests`: 31m 47s (`success`)
  - `micronaut-future-defaults.yml`: [Run 44191417460](https://github.com/sajuptpm/graal/actions/runs/44191417460) — **100% SUCCESS** in 41m 6s.
    - `build-graalvm`: 6m 56s (`success`)
    - `Native Tests`: 34m 7s (`success`)
      - `Run nativeTest in Micronaut launch project with '--future-defaults=all'`: `success` (3m 38s)
      - `Run nativeTest in micronaut-core with '--future-defaults=all'`: `success` (30m 1s)

---

## 5. Deliverable Files & Clean Diff Check
- **Diff File**: `workflow-fix/micronaut-template.diff`
- **Reverse Apply Verification**: `git apply --check --reverse workflow-fix/micronaut-template.diff` exits with code 0.
