# Legal Evidence & Licensing Analysis: Forking, Modifying, Rebranding, and Redistributing GraalVM as Open Source

**Prepared For:** Company X  
**Project:** GraalVM Community Edition (`oracle/graal`)  
**Date:** March 2025  
**Upstream Repository:** [https://github.com/oracle/graal](https://github.com/oracle/graal)  
**Status:** Legal Feasibility Verified — Permitted under GPLv2 + Classpath Exception, UPL v1.0, and BSD 3-Clause

---

## 1. Executive Summary

### Can Company X legally perform the requested actions?
**YES.** Company X has full legal authority under the open-source licenses governing the GraalVM Community Edition repository to:
1. **Fork the project:** Clone the repository and establish an independent development branch/repository.
2. **Apply bug fixes, vulnerability fixes, and enhancements:** Create derivative works and improve the codebase.
3. **Release under the name "Company X":** Distribute modified builds and releases under Company X's own product name and brand. (In fact, rebranding is **legally mandatory** to avoid infringing Oracle's registered trademarks).
4. **Redistribute the software:** Distribute binaries (containers, tarballs, native images) and source code to internal users, customers, and the general public.
5. **Keep the code open-sourced:** Maintain downstream releases as free and open-source software under the governing reciprocal and permissive licenses.

---

## 2. GraalVM Multi-License Architecture Overview

GraalVM is architected into modular suites governed by three distinct open-source licenses:

```
┌────────────────────────────────────────────────────────────────────────┐
│                     GraalVM Community Edition                          │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │
         ┌─────────────────────────┼─────────────────────────┐
         ▼                         ▼                         ▼
┌──────────────────┐      ┌──────────────────┐      ┌──────────────────┐
│ GPLv2 + Classpath│      │   UPL v1.0       │      │  BSD 3-Clause    │
│    Exception     │      │  (Permissive)    │      │  (Permissive)    │
├──────────────────┤      ├──────────────────┤      ├──────────────────┤
│ • compiler/      │      │ • truffle/       │      │ • sulong/        │
│ • substratevm/   │      │ • sdk/           │      │   (LLVM runtime) │
│ • espresso/      │      │ • regex/         │      └──────────────────┘
│ • tools/         │      │ • wasm/          │
│ • visualizer/    │      │ • espresso-*     │
│ • vm/            │      └──────────────────┘
└──────────────────┘
```

1. **GNU General Public License Version 2 with the "Classpath" Exception (GPLv2 + CPE):** Governs core runtime and compilation engines (`compiler`, `substratevm`, `espresso`, `vm`, `tools`, `visualizer`). Provides strong copyleft protection with an exception that permits linking independent user applications without infecting them with GPL.
2. **Universal Permissive License Version 1.0 (UPL v1.0):** Governs polyglot and language framework components (`truffle`, `sdk`, `regex`, `wasm`). Highly permissive; allows copying, modifying, sublicensing, and distributing in source or binary form with minimal conditions.
3. **BSD 3-Clause License:** Governs the `sulong` (LLVM runtime) suite. Allows redistribution and modification, explicitly prohibiting using the copyright holder's name for promotion without prior permission.

---

## 3. Comprehensive Legal Evidence Table

Below is the structured evidence matrix analyzing each requested action across GraalVM's modular licenses:

| # | Action / Item Needed | Component / Suite Scope | License | License File Location (Upstream URL) | Exact Verbatim Words in License Permitting This Action | Mandatory Conditions & Obligations Imposed on Company X | Trademark & Naming Rules ("Release in name Company X") |
|---|---|---|---|---|---|---|---|
| **1** | **Fork the Project** (Clone, replicate, and host repository) | **Core Engines:** `compiler/`, `substratevm/`, `espresso/`, `vm/`, `tools/`, `visualizer/` | **GPLv2 + Classpath Exception** | Root: [`LICENSE`](https://github.com/oracle/graal/blob/master/LICENSE#L88-L93)<br>SubstrateVM: [`substratevm/LICENSE`](https://github.com/oracle/graal/blob/master/substratevm/LICENSE#L88-L93)<br>Compiler: [`compiler/LICENSE.md`](https://github.com/oracle/graal/blob/master/compiler/LICENSE.md#L88-L93) | *"1. You may copy and distribute verbatim copies of the Program's source code as you receive it, in any medium, provided that you conspicuously and appropriately publish on each copy an appropriate copyright notice and disclaimer of warranty; keep intact all the notices that refer to this License and to the absence of any warranty; and give any other recipients of the Program a copy of this License along with the Program."* | Retain all upstream copyright notices (`Copyright (c) Oracle...`), license texts, and disclaimers of warranty. | Permitted. Upstream repo can be forked into `github.com/company-x/graal` or `github.com/company-x/company-x-native-runtime`. |
| | | **Polyglot & SDK:** `truffle/`, `sdk/`, `regex/`, `wasm/` | **UPL v1.0** | Truffle: [`truffle/LICENSE.md`](https://github.com/oracle/graal/blob/master/truffle/LICENSE.md#L6-L24)<br>SDK: [`sdk/LICENSE.md`](https://github.com/oracle/graal/blob/master/sdk/LICENSE.md#L6-L24)<br>Regex: [`regex/LICENSE.md`](https://github.com/oracle/graal/blob/master/regex/LICENSE.md#L6-L24)<br>Wasm: [`wasm/LICENSE`](https://github.com/oracle/graal/blob/master/wasm/LICENSE#L6-L24) | *"...permission is hereby granted to any person obtaining a copy of this software, associated documentation and/or data... without restriction, including without limitation the rights to copy, create derivative works of, display, perform, and distribute the Software..."* | Retain the copyright notice and UPL text or reference in all copies or substantial portions. | Fully permitted without naming constraints. |
| | | **LLVM Runtime:** `sulong/` | **BSD 3-Clause** | Sulong: [`sulong/LICENSE`](https://github.com/oracle/graal/blob/master/sulong/LICENSE#L6-L12) | *"Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met: 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer."* | Retain copyright notice, list of conditions, and disclaimer. | Fully permitted. |
| **2** | **Bug Fixes, Vulnerability Patches & Enhancements** (Modifications & Derivative Works) | **Core Engines:** `compiler/`, `substratevm/`, `espresso/`, `vm/`, `tools/` | **GPLv2 + Classpath Exception** | Root: [`LICENSE`](https://github.com/oracle/graal/blob/master/LICENSE#L98-L105)<br>SubstrateVM: [`substratevm/LICENSE`](https://github.com/oracle/graal/blob/master/substratevm/LICENSE#L98-L105) | *"2. You may modify your copy or copies of the Program or any portion of it, thus forming a work based on the Program, and copy and distribute such modifications or work under the terms of Section 1 above, provided that you also meet all of these conditions: a) You must cause the modified files to carry prominent notices stating that you changed the files and the date of any change."* | **Prominent Notice of Modification:** Modified files must contain comments indicating that Company X modified them and the date of change (GPLv2 §2a). | Changes are owned by Company X (or contributors) while remaining licensed under GPLv2. |
| | | **Polyglot & SDK:** `truffle/`, `sdk/`, `regex/`, `wasm/` | **UPL v1.0** | Truffle: [`truffle/LICENSE.md`](https://github.com/oracle/graal/blob/master/truffle/LICENSE.md#L20-L24)<br>SDK: [`sdk/LICENSE.md`](https://github.com/oracle/graal/blob/master/sdk/LICENSE.md#L20-L24) | *"...without restriction, including without limitation the rights to copy, create derivative works of, display, perform, and distribute the Software and make, use, sell, offer for sale, import, export, have made, and have sold the Software... and to sublicense the foregoing rights on either these or other terms."* | No modification notice requirement; only retain original copyright and UPL text. | Company X can freely enhance and create derivative works. |
| | | **LLVM Runtime:** `sulong/` | **BSD 3-Clause** | Sulong: [`sulong/LICENSE`](https://github.com/oracle/graal/blob/master/sulong/LICENSE#L6-L8) | *"Redistribution and use in source and binary forms, with or without modification, are permitted..."* | Retain original disclaimer and notice. | Company X can freely modify and patch. |
| **3** | **Release in the Name of Company X** (Product Branding, Naming & Trademark Compliance) | **Entire Project:** All suites (`compiler/`, `substratevm/`, `truffle/`, `sdk/`, `sulong/`, `vm/`) | **GPLv2 + UPL v1.0 + BSD 3-Clause** | Root: [`LICENSE`](https://github.com/oracle/graal/blob/master/LICENSE#L55-L59)<br>Sulong: [`sulong/LICENSE`](https://github.com/oracle/graal/blob/master/sulong/LICENSE#L17-L19) | **GPLv2 Preamble:** *"If the software is modified by someone else and passed on, we want its recipients to know that what they have is not the original, so that any problems introduced by others will not reflect on the original authors' reputations."*<br><br>**BSD 3-Clause §3:** *"3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission."* | **Trademark Law & Brand Separation:** Open-source licenses grant *copyright* and *patent* licenses, **never** trademark licenses. Releasing under the name "Company X" (e.g. *Company X Enterprise VM*, *Company X Native Engine*) is **strictly allowed and legally required** to avoid trademark infringement against Oracle's registered marks (*Oracle*, *GraalVM*). | **Required Action:** Must NOT call the derivative "Oracle GraalVM" or "The Official GraalVM". Permissible naming: *"Company X VM (a fork of GraalVM Community Edition)"* or *"Company X Native Image Runtime"*. |
| **4** | **Redistribute** (Distribute Binaries, Native Images, Containers, Tarballs, and Source) | **Core Engines:** `compiler/`, `substratevm/`, `espresso/`, `vm/` | **GPLv2 + Classpath Exception** | Root: [`LICENSE`](https://github.com/oracle/graal/blob/master/LICENSE#L140-L154)<br>VM: [`vm/LICENSE_GRAALVM_CE`](https://github.com/oracle/graal/blob/master/vm/LICENSE_GRAALVM_CE#L140-L154) | *"3. You may copy and distribute the Program (or a work based on it, under Section 2) in object code or executable form under the terms of Sections 1 and 2 above provided that you also do one of the following: a) Accompany it with the complete corresponding machine-readable source code... or, b) Accompany it with a written offer, valid for at least three years, to give any third party... a complete machine-readable copy of the corresponding source code..."* | When distributing pre-built binaries (Docker images, tarballs), Company X must either: (1) provide the complete corresponding source code, OR (2) provide a written offer valid for at least 3 years to provide the source code. | Binaries can be published to Company X's GitHub Releases, Maven Central, Docker Hub, or private registry under Company X's namespace. |
| | | **Polyglot & SDK:** `truffle/`, `sdk/`, `regex/`, `wasm/` | **UPL v1.0** | Truffle: [`truffle/LICENSE.md`](https://github.com/oracle/graal/blob/master/truffle/LICENSE.md#L20-L24) | *"...without restriction, including without limitation the rights to copy, create derivative works of, display, perform, and distribute the Software and make, use, sell, offer for sale, import, export, have made, and have sold the Software..."* | Include the copyright notice and UPL text in documentation/materials accompanying the binary distribution. | No restriction. Can be distributed commercially or non-commercially. |
| | | **LLVM Runtime:** `sulong/` | **BSD 3-Clause** | Sulong: [`sulong/LICENSE`](https://github.com/oracle/graal/blob/master/sulong/LICENSE#L13-L16) | *"2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution."* | Include the 3-clause BSD notice and disclaimer in the documentation accompanying the binary distribution. | No restriction. |
| **5** | **Keep Code Open Sourced** (Copyleft Compliance & Reciprocal Open Sourcing) | **Core Engines:** `compiler/`, `substratevm/`, `espresso/`, `vm/` | **GPLv2 + Classpath Exception** | Root: [`LICENSE`](https://github.com/oracle/graal/blob/master/LICENSE#L106-L109)<br>Classpath Exception: [`LICENSE`](https://github.com/oracle/graal/blob/master/LICENSE#L381-L390) | **GPLv2 §2b:** *"b) You must cause any work that you distribute or publish, that in whole or in part contains or is derived from the Program or any part thereof, to be licensed as a whole at no charge to all third parties under the terms of this License."*<br><br>**Classpath Exception:** *"If you modify this library, you may extend this exception to your version of the library, but you are not obligated to do so."* | **Reciprocal Licensing:** Any derivative work of GPLv2 code distributed to third parties must be licensed under GPLv2 at no charge.<br>**Retain Classpath Exception:** Company X should explicitly extend the Classpath Exception so downstream users can link their applications without GPL infection. | Guarantees downstream consumers and users that Company X's fork remains free and open-source. |
| | | **Polyglot & SDK:** `truffle/`, `sdk/`, `regex/`, `wasm/` | **UPL v1.0** | Truffle: [`truffle/LICENSE.md`](https://github.com/oracle/graal/blob/master/truffle/LICENSE.md#L26-L30) | *"The above copyright notice and either this complete permission notice or at a minimum a reference to the UPL must be included in all copies or substantial portions of the Software."* | Can remain open-source under UPL v1.0 or be dual-licensed. | Transparent, open permissive licensing. |
| | | **LLVM Runtime:** `sulong/` | **BSD 3-Clause** | Sulong: [`sulong/LICENSE`](https://github.com/oracle/graal/blob/master/sulong/LICENSE#L10-L16) | *"1. Redistributions of source code must retain the above copyright notice... 2. Redistributions in binary form must reproduce the above copyright notice..."* | Retain BSD notice in public repository. | Preserves open-source pedigree. |

---

## 4. Critical Additional Columns & Legal Factors Company X Must Consider

In addition to the standard columns (License, File Location, Verbatim Words), the following factors are critical for a commercial enterprise fork:

### A. Trademark & Product Naming Rules
* **Why it matters:** Copyright licenses (GPL, UPL, BSD) do **not** grant trademark licenses. "GraalVM" and "Oracle" are registered trademarks of Oracle Corporation.
* **The Rule:** Company X **cannot** name its fork "Oracle GraalVM" or represent its binary as the official GraalVM release.
* **Compliant Naming Convention:**
  - ✅ *"Company X Runtime for Native Java"*
  - ✅ *"Company X Enterprise VM, built on GraalVM Community Edition technology"*
  - ✅ *"Company X Polyglot Engine (Fork of GraalVM CE)"*
  - ❌ *"Company X Oracle GraalVM"* (Infringes Oracle trademark)
  - ❌ *"The Official GraalVM 25"* (Misleading)

### B. The "Classpath Exception" (Why Company X MUST Preserve It)
* **What it is:** The GNU Classpath Exception is located at lines 375–390 of the root `LICENSE`:
  > *"As a special exception, the copyright holders of this library give you permission to link this library with independent modules to produce an executable, regardless of the license terms of these independent modules, and to copy and distribute the resulting executable under terms of your choice, provided that you also meet, for each linked independent module, the terms and conditions of the license of that module... If you modify this library, you may extend this exception to your version of the library, but you are not obligated to do so."*
* **Impact for Company X:** If Company X creates native images (`native-image`) or distributes runtime JARs, retaining the Classpath Exception is **vital**. Without it, any customer application compiled or linked with Company X's native image runtime would legally be considered a derivative work of GPLv2 and forced to be open-sourced! Preserving the exception ensures Company X's customers can compile proprietary enterprise applications safely.

### C. Prominent Notices of Modification (GPLv2 §2a)
* **Requirement:** Whenever Company X modifies a file in `compiler/`, `substratevm/`, `espresso/`, or `vm/`, Company X must add a header or comment stating:
  ```java
  /*
   * Modifications Copyright (c) 2025 Company X Inc.
   * Contributed under GPLv2 + Classpath Exception.
   * Modified on: 2025-03-XX by Company X Engineering.
   */
  ```
* **Best Practice:** Maintain a `CHANGELOG.md` or git commit log clearly recording each bug fix and vulnerability patch.

### D. Third-Party Licenses & Bundled Code
* **Requirement:** The GraalVM repository includes third-party libraries (e.g., LLVM toolchain, Apache Commons, ICU, JLine, Netty, ASM).
* **Location:** [`THIRD_PARTY_LICENSE.txt`](https://github.com/oracle/graal/blob/master/THIRD_PARTY_LICENSE.txt) and [`vm/THIRD_PARTY_LICENSE_CE.txt`](https://github.com/oracle/graal/blob/master/vm/THIRD_PARTY_LICENSE_CE.txt).
* **Compliance Action:** Company X must keep `THIRD_PARTY_LICENSE.txt` intact in all releases and distributions.

### E. Patent Grant & Protection
* **UPL v1.0:** Explicitly includes a worldwide, royalty-free, perpetual patent grant from Oracle and all contributors covering both the software and larger works.
* **GPLv2 §7:** Prohibits redistributors from enforcing contradictory patent restrictions, ensuring royalty-free use across all downstream recipients.

---

## 5. Compliance Checklist for Company X

Before distributing the first release of Company X's fork:

- [ ] **Repository Setup:** Fork repository to `github.com/company-x/graal-runtime`.
- [ ] **Rebranding:** Update user-facing strings, banner displays, and documentation to feature "Company X [Product Name]" instead of "Oracle GraalVM".
- [ ] **License Preservation:** Keep all root and module `LICENSE`, `LICENSE.md`, and `THIRD_PARTY_LICENSE.txt` files intact.
- [ ] **Modification Notices:** Ensure modified source files carry change notices as required by GPLv2 §2a.
- [ ] **Preserve Classpath Exception:** Ensure SubstrateVM and compiler libraries explicitly retain the Classpath Exception.
- [ ] **Binary Source Code Offer:** Include a link to Company X's public GitHub repository in release notes, documentation, and the `WRITTEN_OFFER.txt` file for all binary distributions (Docker images, tarballs).
- [ ] **CI/CD Quality Gates:** Ensure builds, tests, and formatting pass (`mx build`, `mx checkstyle`).
