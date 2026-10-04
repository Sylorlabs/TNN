# NAMECHECK.md -- Composition Comparative Worker

## Step 0: Toolchain Guard
- Date: 2026-10-02
- Safebin: $HOME/safebin activated
- `which python3 python`: (empty, verified below)
- Pinned znc: src/tools/toolchain/znc_linux_x86_64_abed8aa1
- Pure Zag for all research computation

## Guard verification
---
If empty above, guard holds.

## Build Records

### Mechanism C
- Base: composition_C/cc_base.zag (1677 lines)
- Patch: composition_C/cc_patch.zag (unfrozen, this worker read-only)
- Driver: cmp_driver_c.zag (this worker)
- Build: cat cc_base.zag cc_patch.zag cmp_driver_c.zag > cmp_full_c.zag
- Binary: cmp_bin_c (pinned znc_linux_x86_64_abed8aa1)
- Runs: cmp_run_c1/2/3.txt, SHA 4b8f81559b1ae12442c6129a97ba4674e0eaf094a57a52927a8caec1983ca296
- Determinism: 3/3 byte-identical

### Mechanism A
- Base: composition_A/cx_core.zag (1677 lines)
- Patch: composition_A/cx_patch.zag
- Driver: cmp_driver_a.zag (derived from cmp_driver_c.zag)
- Binary: cmp_bin_a
- Runs: cmp_run_a1/2/3.txt, SHA 4e6bc34ec5ba28c8a78f1e1d89f4c5c543dfd9f27b7cf96efb2b8b4eba7ab69d
- Determinism: 3/3 byte-identical

### Mechanism B
- Base: knowledge_composition/kc_core.zag lines 1-1567
- Patch: composition_B/cb_patch.zag
- Driver: cmp_driver_b.zag (with co-use episodes)
- Binary: cmp_bin_b
- Runs: cmp_run_b1/2/3.txt, SHA d562c2d473e22285b8cb2b85281bc50bbb1eb632ca314ad6229061fab8b23bef
- Determinism: 3/3 byte-identical

## Toolchain Guard
- `which python3 python`: empty (verified 2026-10-02)
- Safebin PATH active for all builds and runs
- Pure Zag. Zero em/en dashes in REPORT.md (byte-verified).
