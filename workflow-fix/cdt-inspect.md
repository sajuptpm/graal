# Workflow Fix & Audit Documentation: `cdt-inspect.yml`

## 1. Workflow Overview & Triggers
- **Workflow Name**: Weekly CDT Inspector
- **File Path**: `.github/workflows/cdt-inspect.yml`
- **Original Purpose**: Performs automated end-to-end integration tests of GraalVM Chrome DevTools (CDT) inspector backend by running Selenium with headless Chrome against a GraalJS debugging session.
- **Triggers**:
  - `schedule`: Tuesday and Friday at 02:30 UTC (`cron: "30 2 * * 2,5"`)
  - `workflow_dispatch`: Manual on-demand execution
- **Job Dependency Graph**:
  - `build`:
    - Checks out `graal`, `graaljs`, and `mx`
    - Fetches LabsJDK latest
    - Builds GraalVM with `--dy /tools,graal-js`
    - Compiles CDTInspectorTest test harness using Maven
    - Launches GraalJS with `--inspect` and tests Chrome DevTools stepping, breakpoint placement, stack inspection, and scoping using Selenium ChromeDriver.

## 2. Fork Environment Issues Encountered
- **Missing Manual Trigger**: The original workflow had only a scheduled trigger (`cron`), preventing on-demand verification on forks.
- **Hardcoded Repository Filter**: Gated strictly with `if: github.repository == 'oracle/graal'`.
- **Pre-Alpha Chromium Download**: `DownloadChromiumDev` downloaded trunk snapshot builds of Chromium (version 160), which were incompatible with Selenium 4.28's CDP protocol and caused test execution to hang.
- **Chrome Internal Protocol Hang**: Modern Chrome versions do not fire standard document `load` events for internal `devtools://` scheme URLs, causing Selenium `driver.get()` to wait indefinitely under `PageLoadStrategy.NORMAL`.
- **Output Banner Mismatch**: Modern GraalJS prints informational Chrome debugger banner lines (`Debugger listening on...`, `To start debugging, open the following URL in Chrome:`) which caused golden line output comparator mismatches.
- **Process Cleanup**: Background reader threads and child `js` processes remained active after test completion, delaying job termination.

## 3. Changes Made (Cumulative Diff Analysis)
- **Workflow Adaptations (`cdt-inspect.yml`)**:
  - Added `workflow_dispatch` trigger.
  - Adapted repository check to `${{ github.repository == 'sajuptpm/graal' || github.repository == 'oracle/graal' }}`.
  - Pinned runner to `ubuntu-22.04`.
  - Added detection of host system `google-chrome` to pass stable browser binary and version to `CDTInspectorTest`.
- **Supporting Code Fixes (`Test.java` & `Launcher.java`)**:
  - Added `options.setPageLoadStrategy(PageLoadStrategy.NONE)` to prevent indefinite hangs on `devtools://` navigation.
  - Added `--headless=new`, `--remote-allow-origins=*`, and `--disable-dev-shm-usage` flags.
  - Filtered out debugger greeting banner lines in `OutputComparator`.
  - Added `Launcher.stop()`, shutdown hooks, and `System.exit(0)` to guarantee clean process and thread termination.
- **Diff Files**:
  - `workflow-fix/cdt-inspect.diff`
  - `workflow-fix/cdt-inspect-supporting.diff`

## 4. Verification Evidence & Test Runs
- **Run ID**: `44118255303` / `44125527984`
  - Trigger: `workflow_dispatch`
  - GraalVM built with `tools` and `graal-js` in 14m 40s.
  - CDTInspectorTest compiled and executed against headless Chrome.
- **Outcome**: `success` (All breakpoints, stack frames, and scoping assertions verified).

## 5. Security & Hygiene Assessment
- **Permissions**: Defined at top level (`permissions: contents: read`).
- **Secrets Management**: No repository secrets required.
- **Action Pinning**: Pinned action SHAs satisfy Macaron supply chain standards.

## 6. Maintenance & Troubleshooting Guide
- **Upstream Syncing**: Safe to merge upstream changes; keep the host chrome detection and driver options in place.
