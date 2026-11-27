# Windows Development Setup Guide for GraalVM

**Repository**: `sajuptpm/graal` (forked from `oracle/graal`)  
**Operating System**: Windows 11 / Windows 10 (x64)  
**Date**: November 27, 2026  

---

## 1. Overview

This document provides a comprehensive, step-by-step guide for developers setting up a Windows laptop to **fork, clone, bug fix, build, test, and debug** the GraalVM codebase (including the Graal compiler, SubstrateVM / Native Image, Truffle, and language runtimes).

---

## 2. Essential Toolchain & Software Matrix

| Category | Tool / Software | Minimum Required Version | Purpose in GraalVM Development | Download / Installation Source |
|:---|:---|:---|:---|:---|
| **Version Control** | **Git for Windows** | 2.40+ (64-bit) | Cloning repository, branch management, cherry-picking, patch generation | [git-scm.com](https://git-scm.com/download/win) or `winget install Git.Git` |
| **GitHub CLI** | **`gh`** | 2.30+ (64-bit) | Managing repository fork, viewing GitHub Actions workflow runs, downloading CI logs | [cli.github.com](https://cli.github.com/) or `winget install GitHub.cli` |
| **Build Orchestrator** | **`mx`** | Master branch | Oracle GraalVM's dedicated build system, suite dependency manager, and test runner | Clone from [github.com/graalvm/mx](https://github.com/graalvm/mx) |
| **Scripting Runtime** | **Python** | 3.8 to 3.13 (64-bit) | Executes `mx` and supporting Python build scripts | [python.org](https://www.python.org/) or `winget install Python.Python.3.13` |
| **Bootstrap Java** | **JDK 21+ / LabsJDK** | JDK 21+ (or LabsJDK via `mx fetch-jdk`) | Bootstrap JVM required to compile GraalVM compiler and runtime classes | Oracle JDK / OpenJDK 21+ or `mx fetch-jdk` |
| **C/C++ Compiler** | **Visual Studio 2022** *(or Build Tools)* | **17.6.0+** *(17.13+ recommended)* | Microsoft Visual C++ (MSVC) compiler required by SubstrateVM to produce native `.exe` / `.dll` | [visualstudio.microsoft.com](https://visualstudio.microsoft.com/downloads/) |
| **Windows Platform SDK** | **Windows 11 SDK** | 10.0.22000+ (or Win 10 SDK 10.0.19041+) | Windows C runtime headers, kernel libraries, and debug symbols | Included with Visual Studio C++ workload |
| **IDE** | **IntelliJ IDEA** *(or VS Code)* | 2024.1+ | Source code editing, navigation, and attaching remote Java debuggers (`mx ideinit`) | [jetbrains.com/idea](https://www.jetbrains.com/idea/) |

---

## 3. Windows Operating System Configuration (Mandatory)

Windows enforces a default 260-character path limit (`MAX_PATH`) and restricts symlink creation by default. GraalVM's deep package hierarchy and build artifacts will fail without these adjustments:

### 3.1. Enable Git Long Paths
Open PowerShell and configure Git globally:
```powershell
git config --system core.longpaths true
```

### 3.2. Enable Windows OS Long Paths
Open PowerShell as **Administrator** and run:
```powershell
New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" `
  -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force
```

### 3.3. Enable Developer Mode (for Unprivileged Symlinks)
1. Open Windows **Settings** (`Win + I`).
2. Navigate to **System** -> **For developers**.
3. Toggle **Developer Mode** to **On**.
4. Configure Git to support symlinks:
   ```powershell
   git config --system core.symlinks true
   ```

---

## 4. Step-by-Step Installation & Setup

### Step 1: Install Visual Studio 2022 & C++ Build Tools
SubstrateVM (Native Image) depends on the Microsoft Visual C++ toolchain:
1. Run the following command in PowerShell to install the C++ build tools automatically via `winget`:
   ```powershell
   winget install Microsoft.VisualStudio.2022.BuildTools --override "--passive --wait --add Microsoft.VisualStudio.Workload.VCTools;includeRecommended"
   ```
2. Alternatively, download the installer manually and select:
   * Workload: **Desktop development with C++**
   * Individual Components:
     * **MSVC v143 - VS 2022 C++ x64/x86 build tools (Latest)**
     * **Windows 11 SDK** (or Windows 10 SDK 10.0.19041+)
     * **C++ CMake tools for Windows**

### Step 2: Install Python (64-bit)
1. Install Python 3.11+ using `winget`:
   ```powershell
   winget install Python.Python.3.13
   ```
2. Verify Python is available in your PATH:
   ```powershell
   python --version
   ```

### Step 3: Install `mx` (GraalVM's Build System)
GraalVM does not use traditional Maven or Gradle commands for its internal suites (`compiler`, `substratevm`, `vm`). Instead, it uses Oracle's `mx` tool:
1. Clone the `mx` repository into your development directory:
   ```powershell
   cd e:\projects
   git clone https://github.com/graalvm/mx.git
   ```
2. Add `mx` to your user `PATH` environment variable:
   ```powershell
   [Environment]::SetEnvironmentVariable("Path", $env:Path + ";e:\projects\mx", "User")
   ```
3. Restart your terminal and verify:
   ```powershell
   mx --version
   ```

### Step 4: Configure Bootstrap JDK (LabsJDK)
GraalVM builds on top of an existing JVM. The easiest and most reliable method is to let `mx` fetch the exact compatible JDK:
```powershell
cd e:\projects\graal
mx fetch-jdk
```
Take the path output by `mx fetch-jdk` and configure `JAVA_HOME`:
```powershell
[Environment]::SetEnvironmentVariable("JAVA_HOME", "<path_to_fetched_jdk>", "User")
```

---

## 5. Recommended Directory Structure

GraalVM suites and tools require sibling directory arrangements:
```text
e:\projects\
  ├── mx\                             <-- GraalVM build toolchain
  ├── graal\                          <-- Forked GraalVM repository
  │    ├── compiler\                  <-- Graal JIT/AOT compiler suite
  │    ├── substratevm\               <-- Native Image / SubstrateVM suite
  │    ├── truffle\                   <-- Truffle language implementation framework
  │    ├── sdk\                       <-- GraalVM SDK APIs
  │    ├── vm\                        <-- Distribution builder suite
  │    └── docs\                      <-- Documentation source files
  └── graalvm-reachability-metadata\  <-- (Optional) Upstream reachability metadata TCK
```

---

## 6. End-to-End Developer Workflow

### 6.1. Forking and Cloning the Repository
```powershell
# 1. Authenticate with GitHub CLI
gh auth login

# 2. Fork oracle/graal to your personal account
gh repo fork oracle/graal --clone=false

# 3. Clone your personal fork
git clone https://github.com/sajuptpm/graal.git e:\projects\graal
cd e:\projects\graal

# 4. Add upstream remote to track Oracle releases
git remote add upstream https://github.com/oracle/graal.git
```

### 6.2. Building GraalVM Suites Locally
Always execute `mx` commands from the relevant suite folder inside a terminal with MSVC environment variables loaded (**x64 Native Tools Command Prompt for VS 2022** or PowerShell with environment configured):

```powershell
# Build SubstrateVM (Native Image)
cd e:\projects\graal\substratevm
mx build --build-logs=silent

# Build full GraalVM distribution
cd e:\projects\graal\vm
mx build --build-logs=silent
```

### 6.3. Running Tests
```powershell
# Run compiler unit tests
cd e:\projects\graal\compiler
mx unittest

# Run SubstrateVM / Native Image unit tests
cd e:\projects\graal\substratevm
mx unittest
```

### 6.4. Code Quality & Checkstyle (Pre-Commit Checks)
GraalVM enforces strict formatting and checkstyle rules:
```powershell
mx checkstyle
```

### 6.5. IDE Integration (IntelliJ IDEA)
To generate IDE project configurations, compiler annotation processors, and debug targets:
```powershell
cd e:\projects\graal\substratevm
mx ideinit
```
1. Open IntelliJ IDEA and open `e:\projects\graal\substratevm` (or `e:\projects\graal\compiler`).
2. `mx ideinit` automatically configures:
   * Project SDK and library dependencies.
   * Debug run configuration: `substratevm-localhost-8000`.
3. To debug a native image build in IntelliJ:
   ```powershell
   mx native-image --debug-attach HelloWorld
   ```
   Attach IntelliJ to port `8000` to step through the Native Image ahead-of-time analysis.
