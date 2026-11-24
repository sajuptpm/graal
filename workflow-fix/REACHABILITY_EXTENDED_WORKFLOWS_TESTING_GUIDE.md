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
| 1 | Weekly Dedicated-Layer Tests | **Running** | [45461118315](https://github.com/sajuptpm/graal/actions/runs/45461118315) | In Progress (Populate matrix & build-graalvm passed; test-layered-metadata executing) | Testing upstream configuration |
| 2 | Weekly Layered Tests | Pending Step 1 | TBD | Pending | Will execute after Step 1 |
| 3 | Weekly Layered Future Defaults | Pending Step 2 | TBD | Pending | Will execute after Step 2 |
| 4 | Weekly Reachability Future Defaults | Pending Step 3 | TBD | Pending | Will execute after Step 3 |
