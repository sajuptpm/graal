# GraalVM Reachability Metadata Workflow Analysis & Architecture Evolution

## Executive Summary

This document addresses the workflow identity, history, and architectural relationship between:
1. **`reachability-metadata-compatibility-preserve-crema.yml`**
2. **`reachability-metadata-template.yml`**
3. **`reachability-metadata.yml`**

It also clarifies whether `reachability-metadata-template.yml` is the "new downsized version" of `reachability-metadata-compatibility-preserve-crema.yml`, details the technical reasons for GitHub Larger Runner (`ubuntu-8core-32gb`) allocation, and explains the cost optimization decisions made upstream and for customer/fork models.

---

## 1. Was `reachability-metadata-compatibility-preserve-crema.yml` an actual Graal GitHub Workflow?

**Yes.** It was an authentic, upstream GraalVM workflow located at `.github/workflows/reachability-metadata-compatibility-preserve-crema.yml`.

### Key Characteristics:
* **Workflow Name:** `Weekly Reachability Metadata Tests (-H:+CompatibilityMode -H:Preserve=all -H:+RuntimeClassLoading)`
* **Code Name "Crema":** In Oracle Labs / GraalVM engineering, **Crema** was the internal project codename for experimental Native Image runtime class loading and backwards compatibility support (`-H:+CompatibilityMode -H:Preserve=all -H:+RuntimeClassLoading`).
* **Origin:** Introduced in commit [`d6c0c17cccd`](https://github.com/oracle/graal/commit/d6c0c17cccd) (*"The -H:+CompatibilityMode for Native Image"*).
* **Schedule:** Weekly cron (`0 1 * * 1`) on Monday mornings at 01:00 UTC, plus pull request path triggers and manual dispatch.

### Exact Workflow Definition:
```yaml
name: Weekly Reachability Metadata Tests (-H:+CompatibilityMode -H:Preserve=all -H:+RuntimeClassLoading)

on:
  pull_request:
    paths:
      - '.github/workflows/reachability-metadata-template.yml'
      - '.github/workflows/reachability-metadata-compatibility-preserve.yml'
  schedule:
  - cron: '0 1 * * 1'
  workflow_dispatch:

jobs:
  call-template:
    uses: './.github/workflows/reachability-metadata-template.yml'
    with:
      NATIVE_IMAGE_OPTIONS: '-H:+UnlockExperimentalVMOptions -H:+ReportExceptionStackTraces -H:+CompatibilityMode -H:Preserve=all -H:+RuntimeClassLoading -H:-UnlockExperimentalVMOptions'
```

---

## 2. Is `reachability-metadata-template.yml` the "new downsized version" of `reachability-metadata-compatibility-preserve-crema.yml`?

### The Short Answer:
* **Architecturally:** **No.** `reachability-metadata-template.yml` is **not a replacement file** for `reachability-metadata-compatibility-preserve-crema.yml`. Rather, `reachability-metadata-template.yml` is the **underlying reusable engine (template)** that `reachability-metadata-compatibility-preserve-crema.yml` invoked via `workflow_call`.
* **Operationally & Functionally:** **Yes, the workload was downsized and consolidated.** Oracle **deleted** the expensive Crema caller workflow completely, **downsized the template** itself by capping the matrix and stripping out 8-core Larger Runner support, and consolidated standard weekly runs into **`reachability-metadata.yml`** running on standard 2-core `ubuntu-latest` runners.

---

### Architectural Relationship Diagram

```
BEFORE (Commits d6c0c17cccd -> 3d85109e72c):

 [reachability-metadata.yml]                     [reachability-metadata-compatibility-preserve-crema.yml]
  (Default options: standard tests)              (Options: -H:Preserve=all -H:+CompatibilityMode)
               │                                                              │
               └──────────────────────┬───────────────────────────────────────┘
                                      ▼
                   [reachability-metadata-template.yml]
                   • Matrix: All third-party library coordinates
                   • Runner Logic:
                     if options contain '-H:Preserve=all':
                         runs-on: ubuntu-8core-32gb  <-- High cost ($0.032/min)
                     else:
                         runs-on: ubuntu-latest

────────────────────────────────────────────────────────────────────────────────────────────

AFTER (Commits 3d85109e72c & 7459dae7847):

 [reachability-metadata.yml]                     [reachability-metadata-compatibility-preserve-crema.yml]
  (Active standard public gate)                                    ❌ DELETED
               │
               ▼
 [reachability-metadata-template.yml] (DOWNSIZED)
  • Matrix Capped: Max 256 coordinates (listTopCoordinatesByMetric)
  • Runner Logic Stripped: Hardcoded 'runs-on: ubuntu-latest' (2-core standard runner)
  • 8-core Larger Runner completely removed
```

---

## 3. Timeline of Upstream Commits

| Commit | Date | Author | Action & Significance |
|---|---|---|---|
| [`d6c0c17cccd`](https://github.com/oracle/graal/commit/d6c0c17cccd) | Dec 22, 2025 | Vojin Jovanovic | **Added Crema Workflow:** Added `reachability-metadata-compatibility-preserve-crema.yml` to test Native Image compatibility mode with `-H:Preserve=all`. |
| [`3d85109e72c`](https://github.com/oracle/graal/commit/3d85109e72c) | Jun 11, 2026 | Vojin Jovanovic | **Deleted Crema Workflow & Capped Matrix:** Deleted `reachability-metadata-compatibility-preserve-crema.yml` and modified `reachability-metadata-template.yml` to cap coordinates to top 256 instead of all coordinates. |
| [`7459dae7847`](https://github.com/oracle/graal/commit/7459dae7847) | Jun 15, 2026 | Vojin Jovanovic | **Removed 8-Core Larger Runner:** Stripped `ubuntu-8core-32gb` conditional expression from `reachability-metadata-template.yml#L82`, replacing it with `runs-on: ubuntu-latest`. |

---

## 4. Why did `-H:Preserve=all` require an 8-Core Runner?

1. **Native Image Static Analysis Memory Consumption:**
   GraalVM Native Image ahead-of-time compilation uses points-to analysis to determine reachable code. Dynamic Java features (reflection, dynamic proxies, JNI, serialization) normally require explicit configuration.
2. **Preserve Mode Impact:**
   The option `-H:Preserve=all` instructs the compiler to retain all reflection metadata, method symbols, and class data in the native image heap. For large third-party libraries (e.g. Netty, Spring, Jackson, Logback), this causes JVM compiler heap requirements to spike beyond 16–24 GB RAM.
3. **Standard Runner OOM Failure:**
   On standard GitHub Linux runners (7 GB RAM), static analysis runs out of memory and is terminated by the Linux Out-Of-Memory (OOM) killer. Upstream solved this by provisioning `ubuntu-8core-32gb` (32 GB RAM).

---

## 5. Cost Breakdown & Fork Model Recommendations

### Upstream Commercial Cost (Before Removal):
* **Matrix Size:** Up to 256 coordinates.
* **Runner Type:** `ubuntu-8core-32gb` ($0.032 / minute).
* **Execution Time:** ~30–45 minutes per coordinate job.
* **Single Weekly Run:** $256 \times 30\text{ min} \times \$0.032/\text{min} = \mathbf{\$245.76}$ to $\mathbf{\$368.64}$ per run.
* **Monthly Cost:** **`$980 – $1,475+ / month`** ($11,700 – $17,700 / year).

### Fork & Customer Model (Workbook Sheet3):
As documented in **`infra_tool_estimate.xlsx` (Sheet3 Row 12, Row 72, Row 118)**:
* Running 256 coordinates every week on paid runners is disproportionate for a fork.
* Instead, maintain a **Release Quality Gate** that tests **15 critical coordinates** (e.g., Netty, Jackson, Guava, Slf4j) on an 8-core runner **4 times per year** before major releases.
* **Budgeted Annual Cost:** **`$100 / year`** (at current 8-core rate of $0.022/minute).
* **Zero-Cost Alternative:** Standard runner (`ubuntu-latest`, $0) with 10 GB Linux swap expansion and `-J-Xmx6g` heap limits.
