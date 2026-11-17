# Workflow Fix & Audit Documentation: `macaron-check-github-actions.yml`

## 1. Workflow Overview & Triggers
- **Workflow Name**: Check GitHub Actions with Macaron
- **File Path**: `.github/workflows/macaron-check-github-actions.yml`
- **Original Purpose**: Performs supply-chain security analysis of GitHub Actions workflows in the repository using Oracle Macaron (`oracle/macaron@4ddb55e3c9ef2c77b548be55c557078c4476fd9c` / `v0.24.0`). It verifies compliance against the `check-github-actions` policy and generates Verification Summary Attestation (VSA) and policy reports.
- **Triggers**:
  - `pull_request` (paths: `['.github/workflows/**']`)
  - `workflow_dispatch`
- **Job Dependency Graph**: Single independent job `analyze` running on `ubuntu-latest`.

## 2. Root Cause Analysis in Fork
When executed in the fork environment, the workflow failed during the `Enforce VSA generation` step with exit code 1:
```
Policy verification failed. VSA was not generated at output/vsa.intoto.jsonl.
Check Workflow summary and uploaded reports: https://github.com/...#macaron-analysis-summary
If the action failed but no findings are reported, check your configuration and make sure policy_purl is valid.
```
**Root Causes**:
1. **Hardcoded Upstream Package URL (`policy_purl`)**: The workflow specified `policy_purl: pkg:github.com/oracle/graal@.*`. In a fork, Macaron inspects and indexes the local cloned repository as `pkg:github.com/<owner>/<repo>` (`pkg:github.com/sajuptpm/graal`). Because the policy verification filter looked specifically for components matching `pkg:github.com/oracle/graal`, it found 0 components matching the filter, causing policy evaluation to fail and preventing VSA generation.
2. **Third-Party Action Pinning Policy (`github_actions_vulns`)**: Macaron's `check-github-actions` policy requires third-party GitHub Actions to be pinned to immutable 40-character commit SHAs. In `codespell.yml`, actions were referenced using mutable version tags (`actions/checkout@v7` and `codespell-project/actions-codespell@v2.2`). This triggered `mcn_githubactions_vulnerabilities_1` failure. Once dynamic repository PURL was configured and `codespell.yml` was pinned to immutable SHAs, Macaron verified 100% compliance.

## 3. Detailed Code Changes & Rationale

### Changes in `.github/workflows/macaron-check-github-actions.yml`
Replaced the hardcoded upstream repository purl with `${{ github.repository }}` so that Macaron evaluates the target package under the active fork's identity:
```yaml
# Before
      - name: Run Macaron action
        uses: oracle/macaron@4ddb55e3c9ef2c77b548be55c557078c4476fd9c # v0.24.0
        with:
          repo_path: ./
          policy_file: check-github-actions
          policy_purl: pkg:github.com/oracle/graal@.*
          reports_retention_days: 90

# After
      - name: Run Macaron action
        uses: oracle/macaron@4ddb55e3c9ef2c77b548be55c557078c4476fd9c # v0.24.0
        with:
          repo_path: ./
          policy_file: check-github-actions
          policy_purl: pkg:github.com/${{ github.repository }}@.*
          reports_retention_days: 90
```

## 4. Alternate Jobs & Feature Flags (If Applicable)
Not applicable. The original job executed natively and cleanly on standard GitHub-hosted runners (`ubuntu-latest`) without requiring bypasses or alternate jobs.

## 5. Secrets & Variables Created/Required
| Name | Type | Purpose | How Generated / Format | Exact gh CLI Command Used to Set |
|---|---|---|---|---|
| *None* | N/A | No repository secrets or variables required (uses default `GITHUB_TOKEN`) | N/A | N/A |

## 6. Verification Proof
- **GitHub Actions Run ID**: `44107653290`
- **Run URL**: https://github.com/sajuptpm/graal/actions/runs/44107653290
- **Duration**: 1m 8s
- **Commit / Ref**: `1de46160587` (`workflow-fix/audit-all-workflows`)
- **Artifacts Produced**: `macaron-reports` (includes `policy_report.json`, HTML reports, and database)
- **Job Status**:

| Job Name | Job ID | Status | Conclusion | Note |
|---|---|---|---|---|
| analyze | `134124294852` | completed | success | Macaron supply chain security policy verification passed and VSA generated |
