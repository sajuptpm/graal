# Workflow Fix & Audit Documentation: `micronaut-future-defaults.yml`

## 1. Workflow Overview & Triggers
- **Workflow Name**: Weekly Micronaut Tests (--future-defaults=all)
- **File Path**: `.github/workflows/micronaut-future-defaults.yml`
- **Original Purpose**: Executes weekly automated native tests of the Micronaut framework and micronaut-core projects using GraalVM Native Image with future compiler defaults enabled (`--future-defaults=all`).
- **Triggers**:
  - `schedule`: Weekly on Monday at 02:00 UTC (`cron: '0 2 * * 1'`)
  - `pull_request`: Triggered on changes to `.github/workflows/micronaut-template.yml` or `.github/workflows/micronaut-future-defaults.yml`
  - `workflow_dispatch`: Manual on-demand dispatch
- **Job Dependency Graph**:
  - `call-template`: Reusable workflow invocation calling `./.github/workflows/micronaut-template.yml` with `NATIVE_IMAGE_OPTIONS: '--future-defaults=all'`
  - Downstream jobs executed inside the template:
    - `build-graalvm` (via `build-graalvm.yml`)
    - `Native Tests` (Micronaut launch app + micronaut-core test suites)

## 2. Fork Environment Issues Encountered
- **Upstream Caller Coupling**: As a thin wrapper workflow invoking `micronaut-template.yml`, it required 0 direct changes in its own YAML file. All environment adaptation and permission configurations are cleanly encapsulated in the reusable `micronaut-template.yml` and `build-graalvm.yml` workflows.
- **Workflow Dispatch**: The workflow already included `workflow_dispatch` trigger.

## 3. Changes Made (Cumulative Diff Analysis)
- **Modifications**: 0 modifications to `.github/workflows/micronaut-future-defaults.yml`.
- **Diff File**: `workflow-fix/micronaut-future-defaults.diff` (0-byte empty file).
- **Inherited Adaptations**: Inherits the fork repository name filter `(github.repository == 'oracle/graal' || github.repository == 'sajuptpm/graal')` and pinned action SHAs from `micronaut-template.yml` and `build-graalvm.yml`.

## 4. Verification Evidence & Test Runs
- **Run ID**: Verified on `master` branch via on-demand workflow dispatch:
  - Run ID: `44191417460` ([Run 44191417460](https://github.com/sajuptpm/graal/actions/runs/44191417460))
  - Trigger: `workflow_dispatch` on `master`
  - Total Duration: 41m 6s
  - Jobs:
    - `call-template / build-graalvm / Build GraalVM` (6m 56s, `success`)
    - `call-template / Native Tests` (34m 7s, `success`)
      - `Run nativeTest in Micronaut launch project with '--future-defaults=all'`: `success` (3m 38s)
      - `Run nativeTest in micronaut-core with '--future-defaults=all'`: `success` (30m 1s)
- **Outcome**: `success` (100% passed - All native image builds and JUnit test suites passed with `--future-defaults=all`).

## 5. Security & Hygiene Assessment
- **Permissions**: Fully governed by `micronaut-template.yml` which defines `permissions: contents: read`.
- **Secrets Management**: No repository secrets required or exposed.
- **Action Pinning**: Pinned action SHAs in invoked templates satisfy Macaron supply chain requirements.

## 6. Maintenance & Troubleshooting Guide
- **Upstream Syncing**: Safe to merge upstream updates; inputs remain backward and forward compatible.
- **Troubleshooting**: If future default options flag syntax changes in new GraalVM releases, adjust `NATIVE_IMAGE_OPTIONS` in this wrapper file or in `workflow_call` defaults.
