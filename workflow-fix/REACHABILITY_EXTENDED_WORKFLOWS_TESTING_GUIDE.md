# Extended Reachability Metadata Workflows: Execution, Testing & Remediation Plan

**Repository**: `sajuptpm/graal` (forked from `oracle/graal`)  
**Baseline Commit**: `cd3747b70d9ece13c37de1471a7917af49652822`  
**Active Branches**: `master` & `workflow-fix/audit-all-workflows`  
**Date**: November 25, 2026  

---

## 1. Overview of the 4 Extended Reachability Workflows

Upstream GraalVM defines four specialized reachability metadata test workflows that validate reflection, proxy, and JNI configurations under advanced Native Image compilation modes:

| # | Workflow File | Workflow Name | Advanced Mode Tested | Job Structure |
|:---:|:---|:---|:---|:---:|
| 1 | [reachability-metadata-dedicated-layer.yml](file:///e:/projects/graal/.github/workflows/reachability-metadata-dedicated-layer.yml) | Weekly Dedicated-Layer Reachability Tests | Builds dedicated, isolated native image layers per library (`LAYERED_TESTS: dedicated`) | 3 Sequential Jobs |
| 2 | [reachability-metadata-layered.yml](file:///e:/projects/graal/.github/workflows/reachability-metadata-layered.yml) | Weekly Layered Reachability Tests | Shared base layer multi-tier architecture (`LAYERED_TESTS: shared`) | 4 Sequential Jobs |
| 3 | [reachability-metadata-layered-future-defaults.yml](file:///e:/projects/graal/.github/workflows/reachability-metadata-layered-future-defaults.yml) | Weekly Layered Future Defaults Tests | Shared base layer combined with `--future-defaults=all` optimization flags | 4 Sequential Jobs |
| 4 | [reachability-metadata-future-defaults.yml](file:///e:/projects/graal/.github/workflows/reachability-metadata-future-defaults.yml) | Weekly Reachability Future Defaults Tests | Standalone dynamic matrix testing across 258 community libraries under `--future-defaults=all` | 260 Matrix Jobs |

---

## 2. Key Architectural Discovery: Sequential vs Matrix Execution

Inspection of [reachability-metadata-template.yml](file:///e:/projects/graal/.github/workflows/reachability-metadata-template.yml) reveals a critical architectural design:

1. **`LAYERED_TESTS == 'dedicated'` or `'shared'`**:
   * Does **not** spawn 258 parallel runner jobs.
   * Instead, it builds the base native image layer once (`build-base-layer`), then runs `test-layered-metadata` sequentially inside a single container job using Gradle tasks (`testDedicatedLayer` or `testSharedLayer`).
   * This means **Workflows 1, 2, and 3 only consume 3 to 4 runner jobs each**, placing virtually zero concurrency pressure on GitHub runner limits!

2. **`LAYERED_TESTS == 'none'` (`reachability-metadata-future-defaults.yml`)**:
   * Spawns the dynamic matrix of 258 parallel jobs under `test-all-metadata`.
   * Requires batch queue processing across standard runners.

---

## 3. Sequential Execution Schedule

The four workflows are executed in the following sequential order:

```
[Step 1] Weekly Dedicated-Layer Tests (Workflow ID: 421420147)
   │
   ▼ (Verify result, diagnose any layer errors, patch if needed)
[Step 2] Weekly Layered Reachability Tests (Workflow ID: 421420153)
   │
   ▼ (Verify result, diagnose base-layer build & shared layer linking)
[Step 3] Weekly Layered Future Defaults Tests (Workflow ID: 421420150)
   │
   ▼ (Verify forward-compatibility of shared layers under strict optimization flags)
[Step 4] Weekly Reachability Future Defaults Matrix (Workflow ID: 421420149)
   │
   ▼ (Execute 258 library coordinates under --future-defaults=all)
[Completed] Complete Verification Evidence Documented
```

---

## 4. Live Tracking Log & Status

| Step | Workflow Name | Trigger Status | Run ID | Outcome | Changes / Fixes Made |
|:---:|:---|:---:|:---:|:---:|:---|
| 1 | Weekly Dedicated-Layer Tests | **Completed** | [45461118315](https://github.com/sajuptpm/graal/actions/runs/45461118315) | ⏱️ **Canceled (Timeout 360m)**: 43 coordinates tested before 6-hour runner limit hit. All 42 completed coordinates failed with Native Image layer layout mismatch (`monitorOffset` mismatch). | Diagnosed SubstrateVM layout verification bug & missing `dedicated-layer-test-exclusions.txt` flag |
| 2 | Weekly Layered Tests | **In Progress** | [45523145309](https://github.com/sajuptpm/graal/actions/runs/45523145309) | 🟡 **Running**: `Populate matrix` (1m15s) ✅, `build-graalvm` (8m22s) ✅, `Build layered base` (7m57s) ✅. Base layer verified & uploaded. Currently executing `testSharedLayer` loop. | Live execution verified base layer construction |
| 3 | Weekly Layered Future Defaults | **In Progress** | [45527017023](https://github.com/sajuptpm/graal/actions/runs/45527017023) | 🟡 **Running**: `build-graalvm` and `Populate matrix` actively executing with `--future-defaults=all`. | Triggered in sequence |
| 4 | Weekly Reachability Future Defaults | **In Progress** | [45527086227](https://github.com/sajuptpm/graal/actions/runs/45527086227) | 🟡 **Running**: `build-graalvm` and `Populate matrix` executing, preparing 258-job parallel test matrix under `--future-defaults=all`. | Triggered in sequence |

---

## 5. Detailed Diagnostic Analysis: Workflow 1 (Dedicated Layers)

* **Run ID**: `45461118315`
* **Duration**: Exactly 6 hours (360 minutes, GitHub Actions runner ceiling)
* **Execution Breakdown**:
  * `Populate matrix`: Passed in 1m 17s (identified top coordinates).
  * `build-graalvm`: Passed in 9m 11s (built GraalVM CE distribution artifact).
  * `Layered metadata tests`: Ran sequentially from 18:44:28Z to 00:44:45Z (6 hours).
* **Test Metrics**:
  * Total Coordinates Attempted: 43
  * Passed: 0
  * Failed: 42
  * Interrupted / Timed Out: 1 (`ant:ant:1.6`)
* **Key Root Causes Identified**:
  1. **SubstrateVM Layout Assertion Failure**:
     * Primary Error: `Error: Should not reach here: Object layout differs across image layers for org.assertj.core.configuration.Services: monitorOffset is 4 in the shared layer but 0 in the current layer.`
     * Class affected: `AssertJ` / `OpenTelemetry` (present on the test classpath of almost every JUnit test).
     * Root origin: Commit `062d701e8cc` ("Validate object layouts across image layers") introduced `SVMImageLayerLoader.verifyObjectLayoutCompatibility` which enforces identical monitor offsets between base layer and upper layer.
  2. **Upstream Exclusion Flag Omission**:
     * Upstream repository `oracle/graalvm-reachability-metadata` maintains `tests/tck-build-logic/src/main/resources/dedicated-layer-test-exclusions.txt` with 492 known problematic coordinates.
     * However, `.github/workflows/reachability-metadata-template.yml` line 245 omitted passing `-Ptck.excludedCoordinatesFile=tests/tck-build-logic/src/main/resources/dedicated-layer-test-exclusions.txt`.
  3. **Sequential Monolithic Runner Ceiling**:
     * Building a dedicated base layer and compiling a native test image takes 10 to 11 minutes per coordinate.
     * Sequentially running 256 coordinates would require ~42 hours on a single standard runner, guaranteeing a timeout at 6 hours (360m).
