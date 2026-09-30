# PROC_AMORT_RESULT.md -- Learned-Procedure Amortization Test

Date: 2026-09-30. Author: Procedure Amortization Worker.
Prereg: bb5491c00 (committed alone before implementation).
Implementation: amort.zag (pure Zag), amort.c (C baseline), run_amort.sh
(bash driver). Toolchain: znc 2026.07.0-dev, gcc 13.3.0 -O2.

## Verdict: AMORT-TESTED

All four kill bars pass. No falsifier fires. The finding is a bounded
engineering result: amortization is real and large within TNN, the
learner's own signature artifact is the fastest TNN execution form, and
conventional compiled C beats the best TNN form by 1.8x (near parity,
no TNN-specific execution advantage).

## Kill bar results

### K1 procedure selected, all arms implemented: PASS

D1 = majority(X1,X2,X3) = (X1&X2)|(X2&X3)|(X1&X3), the kept 5-op tree
from Q4-reuse BUILD-PASS (b719bb54b), reproduced as the 8-node table in
amort.zag exactly per prereg section 2. Correctness gate: all 64 input
combos agree across E1/E2/E3 (gate=0), signature e8e8e8e8e8e8e8e8
matches the hand-derived majority truth table.

Arms:
- E1 TREE-INTERP: generic recursive interpreter over the node table,
  no memoization (shared subterm X2 re-evaluated).
- E2 SIG-LOOKUP: learner's precomputed truth signature,
  out = (slo >> x) & 1 (verbatim node_pred logic from q4_reuse.zag).
- E3 COMPILED-DIRECT: worker-lowered direct expression
  ((x1&x2)|(x2&x3)|(x1&x3)).
- B1 C-BASELINE: straightforward gcc -O2 C, same input cycling
  (x = i & 63), same checksum recurrence, no SIMD, no tricks.

### K2 performance measured: PASS

N = 67,108,864 evaluations per arm (2^26; 2^20 full cycles of the
64-combo space). 3 runs per arm. Checksums identical across all arms
and all runs: 4223e82e31000000 (Zag i64 wraparound verified identical
to C uint64_t wraparound in a pre-test probe).

Wall times in ms (3 runs; median):

| arm | run1 | run2 | run3 | median | evals/sec |
|-----|------|------|------|--------|-----------|
| E1 TREE-INTERP (Zag) | 37551 | 34992 | 30495 | 34992 | 1.92M |
| E2 SIG-LOOKUP (Zag) | 1073 | 878 | 705 | 878 | 76.4M |
| E3 COMPILED-DIRECT (Zag) | 2867 | 3279 | 2163 | 2867 | 23.4M |
| B1 C-BASELINE (gcc -O2) | 489 | 246 | 491 | 489 | 137.3M |

Derived speedups (medians):
- E2 vs E1: 39.9x (the learner's own amortized form vs naive tree interp)
- E3 vs E1: 12.2x (compiled direct vs naive tree interp)
- E2 vs E3: 3.3x (signature lookup beats the lowered expression in Zag)
- Best Zag (E2) vs B1: 0.56x (C is 1.8x faster)
- E3 vs B1: 0.17x (C is 5.9x faster on the identical expression)

Peak RSS (VmHWM kB; process-wide high-water mark, cumulative across
arms within one process, so per-arm deltas reflect allocator behavior,
not arm-specific needs): Zag process 4152..12356 across arms
(single-digit MB throughout); C binary 1424..1448.

### K3 baseline comparison, honest interpretation: PASS

1. Amortization within TNN is real and large. The same learned function
   executes 12x to 40x faster once it leaves naive tree-interpretation
   form. Learning pays once; execution is cheap thereafter.
2. The learner's own artifact wins inside TNN. E2 (the precomputed
   truth signature, a byproduct of the learner's own scoring machinery)
   is 3.3x faster than the worker-lowered direct expression and is the
   fastest TNN execution form measured. Machine-native observation: the
   Q4 signature mechanism is effectively a compilation to a lookup
   table, and that compilation is essentially free because the
   signature already exists as a learning byproduct.
3. No TNN-specific execution advantage over conventional code. gcc -O2
   C beats the best Zag form by 1.8x, and beats the identical direct
   expression in Zag by 5.9x (a znc codegen gap, honestly noted, not a
   TNN architectural finding). Compilation is compilation: TNN's edge,
   if any, is in learning the procedure, not in executing it faster
   than conventional compiled code.
4. Scope bound on the signature form: the bitmask amortization costs
   2^k entries and does not scale to large input spaces; the compiled
   direct form is the scalable amortization. For this 6-bit task the
   table wins; the ranking would invert where tables do not fit.

### K4 purity and determinism: PASS

- Zero Python invocations at every stage (implementation, build via
  znc/gcc, execution, analysis via bash/sed/md5sum/grep).
- Zero em/en-dash bytes in all committed docs (byte-grep verified).
- 3/3 byte-identical Zag stdout after normalizing ms/rss fields
  (md5 9f3d7ecf149bec692466518d60ccbc8e x3); 3/3 byte-identical C
  stdout normalized (md5 28592704baa2595ddea079f86c3997fc x3).
- Zero stderr bytes on all runs (empty .err files).

## Falsification criteria

- F1 (checksums differ): does NOT fire. All arms, all runs:
  4223e82e31000000.
- F2 (E2 or E3 slower than E1): does NOT fire. 39.9x and 12.2x faster.
- F3 (best Zag slower than B1 by more than 2x): does NOT fire.
  878 vs 489 ms = 1.80x, under the 2x bar.

## Honest scope

One learned procedure (5-op boolean majority, 6-bit input space), one
task shape (bulk re-evaluation). The E3 lowering was worker-performed,
not automatic compilation by the learner; the measurement is of the
compiled form's execution, not of an auto-compiler. The znc-vs-gcc gap
(5.9x on identical expressions) is a toolchain codegen difference. No
claim is made about TNN executing learned procedures faster than
conventional systems; the measured result is near-parity with a
conventional lead. The machine-native content of this result is points
1, 2, and 4 of K3: the learner's scoring byproduct is its fastest
execution form, amortization factors are large, and the table-vs-code
tradeoff is explicit.

## Files

- PREREG_PROC_AMORT.md: frozen prereg (bb5491c00)
- amort.zag: three-arm measurement program (pure Zag)
- amort.c: conventional baseline (C, gcc -O2)
- run_amort.sh: bash build-and-measure driver
- AMORT_RAW_1/2/3.txt: Zag raw outputs; AMORT_RAW_1/2/3.err: empty
- AMORT_C_RAW_1/2/3.txt: C raw outputs; AMORT_C_RAW_1/2/3.err: empty
- AMORT_NORM_1/2/3.txt, AMORT_C_NORM_1/2/3.txt: timing-normalized copies
- build_zag.err, build_c.err: build logs
- amort_bin, amort_c: compiled binaries (untracked, not committed)
