# REPORT.md -- Clean Scaling Rerun (Micah Priority 6)

Worker: Clean Scaling Rerun Worker. Date: 2026-10-01. Pure Zag,
zero Python invocations. Reproduction of commit 11adcb0ea.

## What this is

The scaling-cont wave (11adcb0ea) carried one accidental
`python3 -c "print('skip')"` during debug assembly (output to
/dev/null, computed nothing). Per the standing rule that wave is
PROCESS-FAIL for canonical promotion; its measurements are preserved
as exploratory. This wave is a clean safebin reproduction:
every source file was regenerated or verified byte-identical, the
binary recompiled from the pinned znc, and the experiment rerun 3/3
with ZERO Python invocations. This wave is PROCESS-PASS.

## Reproduction chain (all verified byte-identical)

1. Expanded workspace base regenerated from
   rebinding_hardening/hard_base.zag with the same sed expansion
   (1024->8192 nodes, 4096->16384 edges). cmp-verified identical to
   the prior wave's pre-fix backup.
2. The 11-line 1000->10000 frame-slot threshold fix reapplied via
   line-addressed sed. cmp-verified identical to the prior wave's
   fixed base; diff vs pre-fix backup shows exactly 22 changed
   lines (11x2).
3. sc_patch.zag and sc_driver.zag copied from scaling_cont;
   sha256-verified identical.
4. sc_full.zag reassembled with the same sed/cat build steps;
   cmp-verified byte-identical (2158 lines).
5. Compiled with the pinned znc
   (src/tools/toolchain/znc_linux_x86_64_abed8aa1), exit=0.
6. 3/3 runs: sha256
   eee373a21053b2a3a0005be8c1c83ed923f51b22c528b36cd9425d3052146d9d
   for run1, run2, run3; byte-identical to each other AND to the
   prior wave's run hash. cmp-verified against scaling_cont/run1.txt.

## Results (clean, matching the exploratory measurements exactly)

### 1. Scale law: 100 / 500 / 1000 MAPs

| MAPs | mode | scan visits | tried | ok |
|------|------|-------------|-------|----|
| 100  | linear | 699  | 1 | 1 |
| 100  | indexed | 5   | 1 | 1 |
| 500  | linear | 3464 | 1 | 1 |
| 500  | indexed | 5   | 1 | 1 |
| 1000 | linear | 6964 | 1 | 1 |
| 1000 | indexed | 5   | 1 | 1 |

Reduction: 140x at 100 MAPs (699/5), 693x at 500 (3464/5),
1393x at 1000 (6964/5). Confirmed clean.

### 2. Emergent ordering (MTF)

| mode | Q0 | Q1 | Q2 | QSTALE |
|------|----|----|----|--------|
| 0 linear, oldest-first | 25 | 43 | 43 | 50 |
| 1 indexed, id-order, no MTF | 25 | 43 | 43 | 50 |
| 3 indexed + MTF emergent | 49 | 1 | 1 | 2 |

MTF 49->1 confirmed on clean runs: 49 verifies on Q0 collapse to
1 on Q1/Q2. Stale recovery in 2 verifies (vs 50 for a full
rescan). All ok=1; verification arbitrates.

### 3. FACT subject index

| op | linear visits | indexed visits | reduction |
|----|---------------|----------------|-----------|
| t2_gather (4 paths) | 32760 | 167 | 196x |
| 50 x t2_lu_first | 24800 | 1092 | 22.7x |

196x gather reduction confirmed clean. Same paths returned
(np=4 both modes; 50/50 lookups hit).

## Verdict

SCALING-CLEAN-COMPLETE. All five scaling-cont claims reproduced
in pure Zag with zero Python: 140x / 693x / 1393x scan reduction
at 100/500/1000 MAPs, MTF 49->1 with 2-verify stale recovery,
196x FACT gather reduction. 3/3 byte-identical runs matching the
prior wave's hash exactly. The exploratory measurements from
11adcb0ea are now canonically reproduced. PROCESS-PASS.

## Files

- NAMECHECK.md, REPORT.md
- sc_base_expanded.zag, sc_patch.zag, sc_driver.zag, sc_full.zag
- sc_bin (compiled binary), compile_err.txt
- run1.txt, run2.txt, run3.txt (byte-identical)
