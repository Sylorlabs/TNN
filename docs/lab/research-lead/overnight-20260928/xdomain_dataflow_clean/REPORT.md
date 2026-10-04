# REPORT.md -- XDOMAIN-DATAFLOW-CLEAN (H3 clean reproduction)

## Verdict: XDOMAIN-DATAFLOW-CLEAN-COMPLETE

**PROCESS-PASS.** Clean pure-Zag reproduction of the H3 dataflow
experiment. Zero Python invocations. All 8 kill bars PASS. Run outputs
byte-identical to the original wave's measurements.

## Purpose

The original H3 wave (`xdomain_dataflow/`) passed all 8 kill bars
experimentally but was marked PROCESS-FAIL for canonical promotion
because the worker invoked `python3 -c` once during a documentation
check (dash verification, output discarded, no scientific computation).
Per Micah's mandatory toolchain guard, the measurements stood as
exploratory only. This wave reproduces them cleanly under safebin with
an explicit zero-Python attestation (see NAMECHECK.md).

## Method

1. Copied `df_patch.zag`, `df_patch_nodf.zag`, `df_driver.zag` verbatim
   from `xdomain_dataflow/` (sha256-verified byte-identical).
2. Reassembled `df_full.zag` / `df_full_nodf.zag` with the same `cat`
   build steps as the original `build.sh`, using the unchanged
   `composition_C/cc_base.zag`. Assembled inputs sha256-verified
   byte-identical to the originals.
3. Compiled with the pinned `znc_linux_x86_64_abed8aa1` (exit 0, both
   binaries).
4. Ran `df_bin` 3/3 and `df_nodf_bin` 1/1 under the restricted safebin
   PATH.

## Results (3/3 byte-identical)

SHA-256 `391c929274d1d25f0440ef0a4428e6a2c75a1fcf55d9fe5b99892ec27cee677a`
for all three treat runs, matching the original wave's hash exactly.
`cmp`-verified. NO-DF run
`7e57d080b0fc987e8a58b28eaeed98ae13372efd287c5bf3fc3af9560ab22bcf`,
also matching the original.

| Arm | Z ans | Expected | Kill bar |
|-----|-------|----------|----------|
| TREAT | 2 | 2 | K1 PASS |
| Z-REUSE | 3 (via DF-REUSE) | 3 | K8 PASS |
| ABL-X | -2 | -2 | K2 PASS |
| ABL-Y | -2 | -2 | K3 PASS |
| FRESH | -2 | -2 | K4 PASS |
| NO-DF (treat, dataflow off) | -2 | -2 | K5 PASS |

- K6 (determinism): 3/3 byte-identical, `cmp` clean. PASS.
- K7 (no hardcoded literals): grep audit of `df_patch.zag` found zero
  93/91/92/81/82 literals in code. The wiring (proc pairing, mid=34)
  is computed from goal facts at query time. PASS.

Trace (clean run, identical to original):
```
DF-DISCOVER s=31 r=93
DF-STAGE1 proc=0 rel=91 factrel=81
DF-STAGE1 out=34
DF-STAGE2 proc=2 factrel=82
DF-EXEC ans=2
DF-PROMOTE id=271
```

## What this establishes

The H3 dataflow measurements are now canonical. The mechanism (generic
dataflow wiring between heterogeneous learned procedures, discovered
from fact connectivity, no domain-pair template) is confirmed under a
clean toolchain. The PROCESS-FAIL on the original wave is lifted for
these measurements: they were reproduced without any forbidden
executable.

The original wave's honest boundaries still apply (structure-derived
execution, two-stage only, driver-set registry fact_rel, one
cross-domain pair). This reproduction changes the process status, not
the scientific scope.

## Deliverables

All in `docs/lab/research-lead/overnight-20260928/xdomain_dataflow_clean/`:

- NAMECHECK.md (Step 0 guard, zero-Python attestation)
- REPORT.md (this file)
- df_patch.zag, df_patch_nodf.zag, df_driver.zag (verbatim copies)
- df_full.zag, df_full_nodf.zag (assembled inputs)
- df_bin, df_nodf_bin (pinned znc builds)
- df_run1.txt, df_run2.txt, df_run3.txt (3/3 byte-identical)
- df_nodf_run1.txt (NO-DF control)
- df_compile.txt, df_compile_nodf.txt

Pure Zag for all scientific computation. Frozen source read-only.
Paper untouched. Local commit only, nothing pushed. 0 modes, 0 bridges,
0 handlers, 0 new semantic cases.
