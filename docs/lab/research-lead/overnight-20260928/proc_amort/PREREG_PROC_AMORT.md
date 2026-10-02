# PREREG_PROC_AMORT.md -- Learned-Procedure Amortization Test (C2)

Frozen: 2026-09-30. Committed alone before any implementation or
measurement. Any implementation commit must strictly follow this commit.

## 1. Claim under test

Directive priority B: learned-procedure amortization. Once TNN learns a
procedure, how cheaply can it be executed, and does the executed form
compare honestly against a conventional compiled implementation of the
same computation?

This is a MACHINE-NATIVE claim (execution efficiency of a learned
artifact), NOT an L3 representational-invention claim. The procedure
itself was learned by the Q4-reuse worker; this test only measures
execution forms of that fixed learned function.

## 2. Learned procedure (fixed, from prior committed work)

D1 = majority(X1, X2, X3) = (X1 AND X2) OR (X2 AND X3) OR (X1 AND X3).

Source: Q4-reuse BUILD-PASS (commit b719bb54b), Phase 1 kept node 1079:
5 operator nodes, 64/64 true accuracy, 3/3 byte-identical. The tree
structure reproduced here is exactly that sum-of-products:

- t0 = X1, t1 = X2, t2 = X3 (terminals)
- n3 = AND(t0, t1)
- n4 = AND(t1, t2)
- n5 = AND(t0, t2)
- n6 = OR(n3, n4)
- n7 = OR(n6, n5)   (root)

Input space: X1..X6 bits packed as x in 0..63 (only bits 0..2 used).
D1 depends only on bits 0,1,2. Full truth table over all 64 x values is
the correctness oracle; every execution arm must agree on all 64.

## 3. Execution arms (all compute D1 over N evaluations)

N = 67,108,864 evaluations (2^26; exactly 2^20 full cycles of the
64-combo space). Input for evaluation i: x = i & 63. A 64-bit checksum
acc = acc * 31 + out is accumulated to prevent dead-code elimination;
the final checksum is printed and must be identical across arms and runs.

- E1 TREE-INTERP (Zag): generic recursive tree interpreter over the
  8-node table. evaluate(n, x): dispatch on op code, recurse to children,
  no memoization (shared subterm t1 is re-evaluated; documented naive
  path). This is the "execute the learned structure as-is" form.
- E2 SIG-LOOKUP (Zag): the actual Q4 execution path, verbatim logic from
  q4_reuse.zag node_pred: the learner's precomputed truth signature
  (two bitmasks slo/shi over the 64 combos): out = (slo >> x) & 1.
  The signature is the learner's own amortized artifact (memoized at
  learning time).
- E3 COMPILED-DIRECT (Zag): the learned tree lowered by the worker to a
  direct expression: out = ((x1&x2)|(x2&x3)|(x1&x3)). This is what
  "compiling the learned procedure" buys. The lowering is
  worker-performed (honestly disclosed); the measurement is of the
  compiled form, not of an automatic compiler.
- B1 C-BASELINE (C, gcc -O2): straightforward C loop computing the same
  direct expression, same input cycling, same checksum accumulation into
  a global sink, printed at the end. No SIMD, no tricks.

## 4. Metrics (frozen)

Per arm, per run: wall time in ms (now_ms deltas, verbatim copy of the
mnstress1.zag implementation), checksum (hex), peak RSS kB (verbatim
copy of the mnstress1.zag peak_rss reading /proc/self/status VmHWM;
applies to Zag arms and the C binary alike).

3 runs per arm. Report median wall time. Derived: evals/sec per arm;
speedup of E2 and E3 vs E1 (the within-TNN amortization factor);
speedup/slowdown of best Zag arm vs B1 (the TNN-vs-conventional gap).

## 5. Kill bars

- K1: D1 selected and its 8-node structure reproduced exactly as in
  section 2; all four arms implemented (E1/E2/E3 in one Zag program,
  B1 as C source).
- K2: performance measured: N = 2^26 evaluations per arm, 3 runs each,
  checksums identical across all arms and runs, timings recorded.
- K3: baseline comparison reported honestly: E3 vs B1 gap stated with
  numbers; interpretation of whether any TNN-specific execution
  advantage exists, or parity, or deficit.
- K4: pure Zag plus C plus bash driver only; zero Python invocations;
  zero em/en-dash bytes in committed docs; 3/3 byte-identical Zag
  stdout (checksums and structure, timings excluded from the byte
  comparison).

## 6. Pre-stated expectations (not kill bars)

E1 is expected slowest (dispatch + recursion per node). E2 is expected
fastest per evaluation (a few integer ops; it is a lookup table, the
learner's own amortization). E3 and B1 are expected near parity (both
compile to a handful of ALU ops); any large gap either way is a finding,
not a failure. The sig-lookup form is input-space-bounded (2^k memory);
the compiled form generalizes. This asymmetry is part of the honest
interpretation, whichever arm wins.

## 7. Falsifiers

- F1: checksums differ across arms (wrong implementation; void, fix).
- F2: E3 or E2 slower than E1 (amortization buys nothing; report as
  negative result).
- F3: best Zag arm slower than B1 by more than 2x (conventional
  advantage; report honestly, no tuning of the C baseline upward or
  the Zag arms downward after seeing numbers).

No bar may be altered after results. Timing methodology is frozen here.
