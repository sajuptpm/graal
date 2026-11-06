# GraalVM Infrastructure & Tool Estimate (Sheet1 Analysis Report)

## Executive Summary

This report documents the deep workflow analysis, categorization, mandatory/optional classification, and cost estimation populated into **`Sheet1`** of **`infra_tool_estimate.xlsx`** for the **`graal`** component.

The estimation adheres strictly to the upstream workflows before user-level code changes and aligns with the costing and infrastructure assumptions defined in **`Sheet2`** and **`Sheet3`** of the workbook.

---

## 1. Governance & Classification Rules for Sheet1

### Component Column
- Set to **`graal`** across all rows.

### Categories Column
The workflows are classified using the required taxonomy:
- **`Build`**: Monorepo compilation, bootstrap JDK provisioning, and Native Image tool generation (`build-graalvm.yml`).
- **`Package`**: Bundling GraalVM binaries, local Maven caches, and tarball artifacts for transit (`build-graalvm.yml`).
- **`Test`**: Gating suites, multi-suite unit tests, microservices integration (Quarkus, Micronaut, Spring), reachability metadata validation, and debug/layer verification (`main.yml`, `reachability-metadata-template.yml`, `quarkus-template.yml`, `micronaut-template.yml`, `spring-template.yml`, `cdt-inspect.yml`, `ni-layers.yml`).
- **`Release Doc`**: Compilation and publishing of public Javadocs and SDK guides (`publish-javadoc.jsonnet`).
- **`Release`**: Final packaging and distribution of official GraalVM Community Edition JDKs, launchers, and Maven bundles across architectures (`ce-release-artifacts.json` / `vm.jsonnet`).
- **`Internal to Vendor`**: Proprietary Oracle Labs multi-tier CI clusters (`tier1`–`tier4`), internal Nexus repository proxies, and hardware benchmarking infrastructure (`ci.jsonnet`).
- **`Utility`**: Repository automation bots, spelling linters, and supply chain security policy verifiers (`macaron-check-github-actions.yml`, `codespell.yml`, `dependabot.yml`).

### Mandatory Column (`Yes` / `No`)
Evaluates whether the pipeline is required for an **independent open-source fork maintenance and release model**:
- **`Yes` (Mandatory)**: 
  - `build-graalvm.yml`: Required to build GraalVM and Native Image binaries from source.
  - `main.yml`: Core gate validating that compiler, JVMCI, substratevm, and Windows launcher changes do not regress.
  - `reachability-metadata-template.yml` (critical subset): Essential for verifying Native Image compatibility with core ecosystem libraries.
  - `quarkus-template.yml`: Flagship framework integration gate; critical for release qualification.
  - `micronaut-template.yml`: Flagship framework integration gate; critical for release qualification.
  - `spring-template.yml`: Enterprise framework integration gate (Spring Petclinic AOT).
  - `publish-javadoc.jsonnet`: API documentation publishing.
  - `ce-release-artifacts.json`: Distribution pipeline for community releases.
- **`No` (Optional / Non-Mandatory)**:
  - Future defaults workflows (`*-future-defaults.yml`): Test experimental flags (`--future-defaults=all`), non-essential for a stable community release.
  - Layered workflows (`*-layered*.yml`, `ni-layers.yml`): Specialized Native Image layered cache tests.
  - `cdt-inspect.yml`: Chrome DevTools protocol test specific to GraalJS.
  - `macaron-check-github-actions.yml`: Oracle-specific supply-chain governance analyzer.
  - `codespell.yml`: Typo linter; helpful for hygiene but non-blocking for binary releases.
  - `dependabot.yml`: Automated dependency PR bot; optional for a maintained customer fork.
  - `ci.jsonnet`: Oracle's proprietary internal CI; inaccessible to forks and replaced by GitHub Actions.

---

## 2. Infrastructure Cost Basis and Yearly Cost Mapping

Data for the **`Cost basis`** and **`Yearly Cost`** columns are drawn directly from **`Sheet2`** and **`Sheet3`**:
1. **GitHub Larger Runners (`ubuntu-8core-32gb`)**:
   - **Cost Basis:** `Current Linux 8-core rate: $0.022/minute [docs.github.com]; Sheet3 Row 12`
   - **Yearly Cost:** **`$100`** *(Sheet3 Row 12 / Row 44: Based on testing 15 release-critical coordinates × ~30 min each × 4 release qualifications/year plus rerun contingency)*.
2. **Standard GitHub-hosted Linux Runners (`ubuntu-22.04` / `ubuntu-latest`)**:
   - **Cost Basis:** `Standard public-repository runners are free. Chargeable Linux 2-core rate is $0.006/minute only where free public use does not apply. [docs.github.com]; Sheet2 Row 8`
   - **Yearly Cost:** **`$0`**
3. **Standard GitHub-hosted Windows Runners (`windows-2022`)**:
   - **Cost Basis:** `Standard public-repository runners are free; chargeable Windows 2-core rate is $0.010/minute. [docs.github.com]; Sheet2 Row 9`
   - **Yearly Cost:** **`$0`**
4. **GitHub Actions Artifact Storage & Cache (`actions/upload-artifact`, `actions/cache`)**:
   - **Cost Basis:** `Free within public repository limits ($0.008/GB/day beyond quota) / Free up to 10 GB per repository [docs.github.com]; Sheet2 Row 3/5`
   - **Yearly Cost:** **`$0`**
5. **Container & Package Registries (`GHCR`, `Maven Central`, `Docker Hub`)**:
   - **Cost Basis:** `Public GitHub Container Registry (GHCR) storage and bandwidth are free [docs.github.com]; Sheet2 Row 5`
   - **Yearly Cost:** **`$0`**
6. **Oracle Internal CI Infrastructure (`ci.jsonnet`)**:
   - **Cost Basis:** `Proprietary and externally inaccessible (No external price) [Sheet3 Row 70/120]`
   - **Yearly Cost:** **`$0`** *(Proprietary; outside the fork baseline)*.

---

## 3. Complete Sheet1 Data Content (52 Rows Populated)

| Component | Pipeline | Description | Category | Mandatory | Infra | Cost basis | Yearly Cost |
|---|---|---|---|---|---|---|---|
| graal | build-graalvm.yml | Reusable workflow to build GraalVM and Native Image from source and package runtime archives | Build | Yes | Standard GitHub Linux runners (ubuntu-22.04) | Standard public-repository runners are free. Chargeable Linux 2-core rate is $0.006/minute only where free public use does not apply. [docs.github.com] | $0 |
| graal | build-graalvm.yml | Reusable workflow to build GraalVM and Native Image from source and package runtime archives | Package | Yes | GitHub Actions Artifact Storage (actions/upload-artifact for graalvm.tgz) | Free within public repository limits ($0.008/GB/day beyond quota) [docs.github.com] | $0 |
| graal | build-graalvm.yml | Reusable workflow to build GraalVM and Native Image from source and package runtime archives | Build | Yes | Oracle Labs JDK distribution / JVMCI bootstrap JDK (labsjdk-ce-latest) | Official public JDK sources and GitHub Releases are sufficient / Upstream hosting cost only [Sheet3 Row 74/122] | $0 |
| graal | build-graalvm.yml | Reusable workflow to build GraalVM and Native Image from source and package runtime archives | Build | Yes | mx build toolchain, Python 3.8 and GCC | Open-source licensing; runner compute is free for public repositories. [Sheet2 Row 14] | $0 |
| graal | main.yml | Primary continuous integration gate validating compiler, substratevm, truffle, sulong, and espresso suites on Linux and Windows | Test | Yes | Standard GitHub Linux runners (ubuntu-22.04 / ubuntu-latest) | Standard public-repository runners are free. Chargeable Linux 2-core rate is $0.006/minute only where free public use does not apply. [docs.github.com] | $0 |
| graal | main.yml | Primary continuous integration gate validating compiler, substratevm, truffle, sulong, and espresso suites on Linux and Windows | Test | Yes | Standard GitHub Windows runners (windows-2022) | Standard public-repository runners are free; chargeable Windows 2-core rate is $0.010/minute. [docs.github.com] | $0 |
| graal | main.yml | Primary continuous integration gate validating compiler, substratevm, truffle, sulong, and espresso suites on Linux and Windows | Test | Yes | GitHub Modern Kernel Linux runners (ubuntu-24.04) | Standard public-repository runners are free. Chargeable Linux 2-core rate is $0.006/minute only where free public use does not apply. [docs.github.com] | $0 |
| graal | main.yml | Primary continuous integration gate validating compiler, substratevm, truffle, sulong, and espresso suites on Linux and Windows | Test | Yes | Microsoft Visual Studio 2022 Enterprise (MSVC toolchain) | Preinstalled on GitHub Windows virtual environments; free on public runners | $0 |
| graal | main.yml | Primary continuous integration gate validating compiler, substratevm, truffle, sulong, and espresso suites on Linux and Windows | Test | Yes | Oracle Labs JDK distribution (mx fetch-jdk) | Official public JDK sources and GitHub Releases are sufficient / Upstream hosting cost only [Sheet3 Row 74/122] | $0 |
| graal | main.yml | Primary continuous integration gate validating compiler, substratevm, truffle, sulong, and espresso suites on Linux and Windows | Test | Yes | Eclipse SDK download archive (archive.eclipse.org) for JDT formatting | Free public open-source archive | $0 |
| graal | main.yml | Primary continuous integration gate validating compiler, substratevm, truffle, sulong, and espresso suites on Linux and Windows | Test | Yes | Python and pip packages (ninja_syntax, black, pylint) | Open-source licensing; runner compute is free for public repositories. [Sheet2 Row 14] | $0 |
| graal | reachability-metadata-template.yml | Reusable matrix test pipeline validating Native Image reachability metadata across third-party Java library coordinates | Test | Yes | GitHub 8-core runner (ubuntu-8core-32gb) for -H:Preserve=all high-memory analysis | Current Linux 8-core rate: $0.022/minute [docs.github.com]; Sheet3 Row 12 | $100 |
| graal | reachability-metadata-template.yml | Reusable matrix test pipeline validating Native Image reachability metadata across third-party Java library coordinates | Test | Yes | Standard GitHub Linux runners (ubuntu-latest) | Standard public-repository runners are free. Chargeable Linux 2-core rate is $0.006/minute only where free public use does not apply. [docs.github.com] | $0 |
| graal | reachability-metadata-template.yml | Reusable matrix test pipeline validating Native Image reachability metadata across third-party Java library coordinates | Test | Yes | GitHub Actions Artifact Storage (actions/download-artifact & upload-artifact) | Free within public repository limits ($0.008/GB/day beyond quota) [docs.github.com] | $0 |
| graal | reachability-metadata-template.yml | Reusable matrix test pipeline validating Native Image reachability metadata across third-party Java library coordinates | Test | Yes | Docker Hub / GHCR Container Engine (pullAllowedDockerImages) | Public GitHub Container Registry (GHCR) storage and bandwidth are free [docs.github.com]; Sheet2 Row 5 | $0 |
| graal | reachability-metadata-future-defaults.yml | Weekly and dispatch tests of reachability metadata against future experimental Native Image default flags (--future-defaults=all) | Test | No | Standard GitHub Linux runners (ubuntu-latest) | Standard public-repository runners are free. Chargeable Linux 2-core rate is $0.006/minute only where free public use does not apply. [docs.github.com] | $0 |
| graal | reachability-metadata-dedicated-layer.yml | Weekly tests of reachability metadata using dedicated Native Image layers | Test | No | Standard GitHub Linux runners (ubuntu-latest) | Standard public-repository runners are free. Chargeable Linux 2-core rate is $0.006/minute only where free public use does not apply. [docs.github.com] | $0 |
| graal | reachability-metadata-layered.yml | Weekly tests of reachability metadata using shared base layers | Test | No | Standard GitHub Linux runners (ubuntu-latest) | Standard public-repository runners are free. Chargeable Linux 2-core rate is $0.006/minute only where free public use does not apply. [docs.github.com] | $0 |
| graal | reachability-metadata-layered.yml | Weekly tests of reachability metadata using shared base layers | Test | No | GitHub Actions Artifact Storage (actions/upload-artifact for reachability-metadata-base-layer) | Free within public repository limits ($0.008/GB/day beyond quota) [docs.github.com] | $0 |
| graal | reachability-metadata-layered-future-defaults.yml | Tests of reachability metadata with layered Native Image and future default options | Test | No | Standard GitHub Linux runners (ubuntu-latest) | Standard public-repository runners are free. Chargeable Linux 2-core rate is $0.006/minute only where free public use does not apply. [docs.github.com] | $0 |
| graal | ni-layers.yml | Weekly Native Image layer building tests across a matrix of popular Maven library coordinates | Test | No | Standard GitHub Linux runners (ubuntu-latest) | Standard public-repository runners are free. Chargeable Linux 2-core rate is $0.006/minute only where free public use does not apply. [docs.github.com] | $0 |
| graal | ni-layers.yml | Weekly Native Image layer building tests across a matrix of popular Maven library coordinates | Test | No | GitHub Actions Artifact Storage (actions/download-artifact) | Free within public repository limits ($0.008/GB/day beyond quota) [docs.github.com] | $0 |
| graal | quarkus-template.yml | Downstream integration pipeline building Quarkus and running parallel category native image tests | Test | Yes | Standard GitHub Linux runners (ubuntu-22.04 / ubuntu-latest, 8-parallel matrix) | Standard public-repository runners are free. Chargeable Linux 2-core rate is $0.006/minute only where free public use does not apply. [docs.github.com] | $0 |
| graal | quarkus-template.yml | Downstream integration pipeline building Quarkus and running parallel category native image tests | Test | Yes | GitHub Actions Cache (actions/cache for ~/.m2/repository) | Free up to 10 GB per repository; automated LRU eviction [docs.github.com] | $0 |
| graal | quarkus-template.yml | Downstream integration pipeline building Quarkus and running parallel category native image tests | Test | Yes | GitHub Actions Artifact Storage (actions/upload-artifact for maven-repo.tgz and reports) | Free within public repository limits ($0.008/GB/day beyond quota) [docs.github.com] | $0 |
| graal | quarkus-template.yml | Downstream integration pipeline building Quarkus and running parallel category native image tests | Test | Yes | Maven Central (repo1.maven.org) and GitHub REST API | Free public package registries and GitHub API endpoints | $0 |
| graal | quarkus-future-defaults.yml | Tests Quarkus native integration against upcoming experimental Native Image default flags | Test | No | Standard GitHub Linux runners (ubuntu-latest) | Standard public-repository runners are free. Chargeable Linux 2-core rate is $0.006/minute only where free public use does not apply. [docs.github.com] | $0 |
| graal | micronaut-template.yml | Builds and tests Micronaut starter application and micronaut-core with Native Image | Test | Yes | Standard GitHub Linux runners (ubuntu-22.04) | Standard public-repository runners are free. Chargeable Linux 2-core rate is $0.006/minute only where free public use does not apply. [docs.github.com] | $0 |
| graal | micronaut-template.yml | Builds and tests Micronaut starter application and micronaut-core with Native Image | Test | Yes | Micronaut Launch REST API (launch.micronaut.io) | Free public cloud REST API service [launch.micronaut.io] | $0 |
| graal | micronaut-template.yml | Builds and tests Micronaut starter application and micronaut-core with Native Image | Test | Yes | GitHub Actions Artifact Storage (actions/download-artifact) | Free within public repository limits ($0.008/GB/day beyond quota) [docs.github.com] | $0 |
| graal | micronaut-future-defaults.yml | Tests Micronaut native compilation against future experimental Native Image default options | Test | No | Standard GitHub Linux runners (ubuntu-22.04) | Standard public-repository runners are free. Chargeable Linux 2-core rate is $0.006/minute only where free public use does not apply. [docs.github.com] | $0 |
| graal | spring-template.yml | Builds and executes native image tests for the Spring Petclinic application | Test | Yes | Standard GitHub Linux runners (ubuntu-22.04) | Standard public-repository runners are free. Chargeable Linux 2-core rate is $0.006/minute only where free public use does not apply. [docs.github.com] | $0 |
| graal | spring-template.yml | Builds and executes native image tests for the Spring Petclinic application | Test | Yes | GitHub Actions Artifact Storage (actions/download-artifact) | Free within public repository limits ($0.008/GB/day beyond quota) [docs.github.com] | $0 |
| graal | spring-template.yml | Builds and executes native image tests for the Spring Petclinic application | Test | Yes | Maven Central / Gradle Plugin Portal | Free public open-source dependency registries | $0 |
| graal | spring-future-defaults.yml | Tests Spring Petclinic native compilation with future experimental Native Image flags | Test | No | Standard GitHub Linux runners (ubuntu-22.04) | Standard public-repository runners are free. Chargeable Linux 2-core rate is $0.006/minute only where free public use does not apply. [docs.github.com] | $0 |
| graal | cdt-inspect.yml | Integration test of Chrome DevTools (CDT) Inspector backend with GraalJS | Test | No | Standard GitHub Linux runners (ubuntu-latest) | Standard public-repository runners are free. Chargeable Linux 2-core rate is $0.006/minute only where free public use does not apply. [docs.github.com] | $0 |
| graal | cdt-inspect.yml | Integration test of Chrome DevTools (CDT) Inspector backend with GraalJS | Test | No | Oracle Labs JDK distribution (mx fetch-jdk) | Official public JDK sources and GitHub Releases are sufficient / Upstream hosting cost only [Sheet3 Row 74/122] | $0 |
| graal | cdt-inspect.yml | Integration test of Chrome DevTools (CDT) Inspector backend with GraalJS | Test | No | Apache Maven toolchain | Open-source licensing; runner compute is free for public repositories. [Sheet2 Row 14] | $0 |
| graal | macaron-check-github-actions.yml | Supply chain security analysis of GitHub Actions workflows using Oracle Macaron analyzer | Utility | No | Standard GitHub Linux runners (ubuntu-latest) | Standard public-repository runners are free. Chargeable Linux 2-core rate is $0.006/minute only where free public use does not apply. [docs.github.com] | $0 |
| graal | macaron-check-github-actions.yml | Supply chain security analysis of GitHub Actions workflows using Oracle Macaron analyzer | Utility | No | Oracle Macaron container analyzer (oracle/macaron@v0.24.0) | Macaron, CodeQL, actionlint and StepSecurity community capabilities are available at $0 for public repositories [Sheet3 Row 75] | $0 |
| graal | codespell.yml | Automated spelling linting across codebase and documentation files | Utility | No | Standard GitHub Linux runners (ubuntu-latest) | Standard public-repository runners are free. Chargeable Linux 2-core rate is $0.006/minute only where free public use does not apply. [docs.github.com] | $0 |
| graal | codespell.yml | Automated spelling linting across codebase and documentation files | Utility | No | Codespell Action (codespell-project/actions-codespell@v2.2) | Open-source action running on free standard public runners | $0 |
| graal | dependabot.yml | Automated dependency scanning and security update PR creation for GitHub Actions, Maven, Gradle, and Bundler | Utility | No | GitHub Dependabot bot service (dependabot[bot]) | Free native GitHub automation [Sheet2 Row 13] | $0 |
| graal | publish-javadoc.jsonnet | Generates Javadoc across sdk, truffle, tools, and compiler suites and publishes to documentation repository | Release Doc | Yes | Standard GitHub Linux runners (ubuntu-latest / Linux x64 compute) | Standard public-repository runners are free. Chargeable Linux 2-core rate is $0.006/minute only where free public use does not apply. [docs.github.com] | $0 |
| graal | publish-javadoc.jsonnet | Generates Javadoc across sdk, truffle, tools, and compiler suites and publishes to documentation repository | Release Doc | Yes | GitHub Pages / Git repository hosting for docs (graalvm-website.git) | Public GitHub repository and GitHub Pages hosting are free [docs.github.com] | $0 |
| graal | publish-javadoc.jsonnet | Generates Javadoc across sdk, truffle, tools, and compiler suites and publishes to documentation repository | Release Doc | Yes | mx javadoc and Java compiler toolchain | Open-source licensing; runner compute is free for public repositories. [Sheet2 Row 14] | $0 |
| graal | ce-release-artifacts.json | Packages and publishes GraalVM Community Edition JDKs, Native Image standalone binaries, and Maven resource bundles | Release | Yes | GitHub Releases / Public Asset CDN (gh release upload) | GitHub Releases can distribute public artifacts; storage and bandwidth are free [Sheet2 Row 3, Sheet3 Row 62] | $0 |
| graal | ce-release-artifacts.json | Packages and publishes GraalVM Community Edition JDKs, Native Image standalone binaries, and Maven resource bundles | Release | Yes | Multi-architecture build compute (Linux x64, Linux ARM64, Darwin AArch64, Windows x64) | Standard public runners free; ARM64 via QEMU or OCI Always-Free ARM64 VM [Sheet3 Row 70/120] | $0 |
| graal | ce-release-artifacts.json | Packages and publishes GraalVM Community Edition JDKs, Native Image standalone binaries, and Maven resource bundles | Release | Yes | GitHub Container Registry (GHCR) for container images | Public GitHub packages are free; GitHub currently states Container Registry storage and bandwidth are free [Sheet2 Row 5] | $0 |
| graal | ci.jsonnet | Oracle Labs proprietary multi-tier gating and benchmarking cluster across bare-metal OL7-9, Darwin ARM64, and Windows Server | Internal to Vendor | No | Oracle Labs internal dedicated bare-metal & VM cluster (tier1-tier4) | Proprietary and externally inaccessible (No external price) [Sheet3 Row 70/120] | $0 |
| graal | ci.jsonnet | Oracle Labs proprietary multi-tier gating and benchmarking cluster across bare-metal OL7-9, Darwin ARM64, and Windows Server | Internal to Vendor | No | Internal Oracle Nexus repository (nexus_base_url) | Internal enterprise registry infrastructure; no customer-service list price [Sheet2 Row 4, Sheet3 Row 74] | $0 |
| graal | ci.jsonnet | Oracle Labs proprietary multi-tier gating and benchmarking cluster across bare-metal OL7-9, Darwin ARM64, and Windows Server | Internal to Vendor | No | Internal benchmarking infrastructure (ol8_bench_image, benchmarking_config_repo) | Proprietary Oracle Labs internal service [Sheet3 Row 70] | $0 |
