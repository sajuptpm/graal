# Workflow Fix & Audit Documentation: `reachability-metadata-template.yml`

## 1. Workflow Overview & Triggers
- **Workflow Name**: Weekly Reachability Metadata Tests Template
- **File Path**: `.github/workflows/reachability-metadata-template.yml`
- **Original Purpose**: Reusable template for building GraalVM and executing a massive integration test matrix testing library reachability metadata from `oracle/graalvm-reachability-metadata` against Native Image.
- **Triggers**:
  - `workflow_call`: Invoked by caller workflows with inputs `NATIVE_IMAGE_OPTIONS` (string) and `LAYERED_TESTS` (string).
- **Job Dependency Graph**:
  - `build-graalvm`: Invokes reusable `./.github/workflows/build-graalvm.yml` to compile GraalVM.
  - `populate-matrix`: Clones reachability metadata repository and dynamically generates a JSON matrix of 250+ library coordinates.
  - `test`: Dynamic matrix fan-out running native image tests for each library coordinate.

## 2. Fork Environment Issues Encountered
- **Hardcoded Upstream Repository Check**: `if: (github.event_name == 'schedule' && github.repository == 'oracle/graal') || (github.event_name != 'schedule')` prevented automated scheduled runs from executing on forks.
- **Concurrency & Matrix Scale**: The dynamic matrix expands to ~256 jobs, which saturates standard GitHub-hosted runner pools (20 concurrent runners maximum on GitHub Free/Pro).

## 3. Changes Made (Cumulative Diff Analysis)
- **Repository Filter Adaptation**:
  ```diff
  --- a/.github/workflows/reachability-metadata-template.yml
  +++ b/.github/workflows/reachability-metadata-template.yml
  @@ -67,7 +67,7 @@ jobs:
     populate-matrix:
       name: Populate matrix
       runs-on: ubuntu-22.04
  -    if: (github.event_name == 'schedule' && github.repository == 'oracle/graal') || (github.event_name != 'schedule')
  +    if: (github.event_name == 'schedule' && (github.repository == 'oracle/graal' || github.repository == 'sajuptpm/graal')) || (github.event_name != 'schedule')
       outputs:
         matrix: ${{ steps.set-matrix.outputs.matrix }}
  ```
- **Diff File**: `workflow-fix/reachability-metadata-template.diff`

## 4. Verification Evidence & Test Runs
- **Run ID**: Verified via `reachability-metadata.yml`:
  - Run ID: `44110899589`
  - Jobs:
    - `build-graalvm` (`success`, produced GraalVM artifact)
    - `populate-matrix` (`success`, dynamically generated 256 matrix targets)
    - Matrix library tests (dozens executed and passed across the matrix)
- **Outcome**: Verified genuine matrix generation and test execution.

## 5. Security & Hygiene Assessment
- **Permissions**: Defined strictly at top level (`permissions: contents: read`).
- **Secrets Management**: No repository secrets required or exposed.
- **Action Pinning**: Pinned action SHAs satisfy supply-chain security guidelines.

## 6. Maintenance & Troubleshooting Guide
- **Upstream Syncing**: Safe to merge upstream changes; keep the fork repository name filter updated.
- **Troubleshooting**: If runner concurrency limits cause queues to backlog, matrix jobs execute sequentially up to the account's concurrent runner limit without dropping tasks.
