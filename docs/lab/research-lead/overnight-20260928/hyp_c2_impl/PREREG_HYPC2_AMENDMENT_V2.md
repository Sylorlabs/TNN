# AMENDMENT: Hypothesis C2 Preregistration to Battery v2 Tasks

Date: 2026-09-30.
Status: FROZEN PREREGISTRATION AMENDMENT. v2 implementation not yet started.
Authority: Transparently amends `hyp_c2_impl/PREREG_HYPC2.md` (01336fe83) per
Battery v2 redesign `battery_redesign/BATTERY_REDESIGN.md` (611e8fa1f).
This amendment strictly precedes any v2 implementation or evaluation commit.

## 1. Reason for amendment

Battery v2 redesign (611e8fa1f) found that v1 T1/T4/T5 are COMPROMISED as
conditional discriminators. Hypothesis D exhibited a 7-op straight-line
program for |x| using MOD (`e2ee0964e`), confirming that the full GENEXEC2
op alphabet "secretly expresses abs without comparison". The v2 redesign
mandates GENEXEC2-P (polynomial VM) for T1/T4/T5.

Per v2 sec 3.8 transition plan item 3: "C2 (implementing against v1 tasks):
its prereg MUST be transparently amended to v2 tasks before any v2
evaluation run. Amendment precedes runs; no v1-targeted C2 evaluation
counts toward v2."

v1 C2 measurements: T0 SOLVE, T1 SOLVE (via MOD trick), T2 SOLVE, T3 BUDGET,
T4 BUDGET, T5 BUDGET (run1.txt/run2.txt/run3.txt, 3/3 byte-identical).
Per v2 sec 3.8: v1-T1/T4/T5 interpretations as conditional discriminators
are SUPERSEDED. v1-T0/T2/T3 interpretations stand.

## 2. v2 task specifications for C2

| Task | Target | Train | Held-out | VM | v2-SOLVE |
|------|--------|-------|----------|----|----------|
| T0 | 2x+1 | x 0..8 (9) | x -8..-1, 9..16 (16) | full GENEXEC2 | train exact + ops <= 40 |
| T1 | abs(x) | x -8..8 (17) | x -12..12 excl -8..8 (8) | GENEXEC2-P | train exact + ops <= 40 |
| T2 | x mod 3 | x 0..16 (17) | x 17..33 (17) | full GENEXEC2 | train exact + ops <= 40 |
| T3 | 1 if (a+b) even else 0 | a,b 0..4 (25) | a,b 0..7 excl square (39) | full GENEXEC2 | train exact + ops <= 40 |
| T4 | \|\|x\|-2\| | x -6..6 (13) | x -10..10 excl -6..6 (8) | GENEXEC2-P | train exact + ops <= 40 |
| T5 | \|x\|+\|x-2\| | x -4..8 (13) | x -8..12 excl -4..8 (8) | GENEXEC2-P | train exact + ops <= 40 |

GENEXEC2-P (v2 sec 3.1): full GENEXEC2 minus {DIV, MOD, LT, EQ, GT}.
Kept: PUSH(c) c in -9..9, IN0, IN1, ADD, SUB, MUL, NEG, DUP, DROP, SWAP,
OVER, JZ(k), JNZ(k), JMP(k), CALL(f), RET. Frozen 8d5f58b89 semantics.

v2-SOLVE (v2 sec 3.5): exact integer equality on ALL train episodes AND
total program ops (main + all called fragment bodies) <= 40.

## 3. C2 mechanism amendments for v2

### 3.1 Repair op alphabet (P-VM tasks)

For T1/T4/T5 (GENEXEC2-P), the repair lookahead alphabet is restricted to
P-VM-valid ops. The 34-symbol v1 alphabet:
  IN0, IN1, PUSH -9..9, ADD, SUB, MUL, DIV, MOD, NEG, DUP, DROP, SWAP,
  OVER, LT, EQ, GT
becomes the 29-symbol P-VM alphabet:
  IN0, IN1, PUSH -9..9, ADD, SUB, MUL, NEG, DUP, DROP, SWAP, OVER
(DIV, MOD, LT, EQ, GT removed).

For T0/T2/T3 (full VM), the 34-symbol alphabet is unchanged.

Rationale: region bodies are the solution semantics (v2 sec 3.3) and must
be P-VM-valid on P-VM tasks (F-SMUG). The repair operator constructs
region bodies.

### 3.2 Split probe policy (unchanged, clarified)

Split probes remain [IN0/IN1, PUSH k, LT/GT/EQ], k in -4..4, and run on the
full GENEXEC2 per v2 sec 3.3: "Split probes are meta-level partition
classifiers and run on the full GENEXEC2. Region bodies, the main program,
and every CALLed fragment on a P-VM task must be GENEXEC2-P-valid; this is
audited (F-SMUG). A probe may not leak ablated ops into solution semantics:
the region bodies are the solution."

The probe dispatch (INx, PUSH k, CMP, JZ) is harness-level tooling. The
region bodies constructed by repair are the solution and are P-VM-valid
per 3.1. F-SMUG audits region bodies and straight-line prefixes, not the
probe dispatch sequence.

### 3.3 Unchanged C2 machinery

Lookahead L=3, net-progress criterion, chronological backtracking BMAX=6,
split-from-best_P, frozen probe family order, counterexample ordering,
single program (no population), determinism. All per PREREG_HYPC2.md.

## 4. v2 predictions (from v2 matrix sec 4, frozen)

- T0 (full): SOLVE. v1 measurement stands (SOLVE, 5 ops). No re-run.
- T1 (P): SOLVE via splits. Trace: split on sign-separating probe, each
  branch repaired to linear piece; final 2 regions, 0 CALLs, ops <= 40.
  The MOD trick is unavailable; straight-line P-VM cannot express abs
  (v2 sec 3.2 Lemma 2).
- T2 (full): SOLVE. v1 measurement stands (SOLVE, 3 ops). No re-run.
- T3 (full): SOLVE (v2 matrix). Note: v1 C2 measurement was BUDGET/FAIL
  (1M evals exceeded). v2 task is identical to v1 (full VM). The v2
  prediction stands as the target; the v1 FAIL is the current measurement.
  A v2 re-run is authorized to test whether the op cap or implementation
  changes affect the outcome, but the v1 FAIL is not retracted.
- T4 (P): SOLVE via nested splits, 0 CALLs. Trace: at least 2 nested SPLIT
  events; final 0 CALLs. KEY DISCRIMINATOR vs B preserved.
- T5 (P): SOLVE via splits tracking 0/2 kink structure, 0 CALLs.

## 5. Kill bars (v2)

- K1: Prereg amendment frozen (this document) before any v2 code change.
- K2: C2 implemented against v2 (P-VM repair alphabet for T1/T4/T5).
- K3: T1/T4/T5 tested on v2 per battery protocol (frozen episodes,
  budget 1M evals or 300s per task, 3/3 byte-identical). T0/T2 v1
  measurements stand; T3 v1 measurement stands with v2 prediction noted.
- K4: Pure Zag, zero Python, zero em/en-dash bytes, 3/3 deterministic.
- K5: F-SMUG audit PASS on all P-VM task programs (no DIV/MOD/LT/EQ/GT
  in region bodies or straight-line prefixes).
- K6: v2-SOLVE op cap (<= 40) verified on all SOLVE claims.

## 6. Falsifiers (v2; frozen)

Carried over from PREREG_HYPC2.md, with v2 scope:
- C2-F1: C2 fails T0. (v1: NOT FIRED.)
- C2-F2: C2's T4 trace shows fragment CALLs instead of nested splits, or
  T4 program contains CALLs. Mechanism falsified.
- C2-F3: split count on any task reaches the episode count.
- C2-F4: T0 requires more than BMAX=6 backtracks. (v1: NOT FIRED, 1 used.)
- C2-F5: any task exceeds 1,000,000 evaluations. (v1: FIRED on T3/T4/T5;
  v2 re-evaluates on P-VM tasks.)

New from v2 (apply to C2):
- F-TRICK: C2 exhibits a jump-free GENEXEC2-P program achieving v2-SOLVE
  on T1/T4/T5 with ops <= 40 via a non-split (straight-line) mechanism.
  Then the sec-3.2 separation assumption is violated for that task: VOID
  pending re-investigation. (This would be a discovery, not a C2 success.)
- F-SMUG: a P-VM task's region bodies or straight-line prefixes contain
  DIV, MOD, LT, EQ, or GT. Result VOID.
- F-MEM: a claimed SOLVE exceeds 40 ops. Not SOLVE.

## 7. Determinism

Frozen seed: 0xC2C2C2 (unchanged). 3 runs byte-identical.

## 8. Governance

Pure Zag only. No Python anywhere. No em dashes (byte-verified). Commits
local, owned path `docs/lab/research-lead/overnight-20260928/hyp_c2_impl/`
only. This amendment is committed alone before any v2 code change.
v1 measurements are preserved (not retracted); v1-T1/T4/T5 conditional
interpretations are SUPERSEDED per v2 sec 3.8.
