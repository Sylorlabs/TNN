# RESULT: Hypothesis C2 on Battery v2 (Counterexample-Driven Growth with Non-Myopic Repair)

Date: 2026-09-30.
Battery v2 redesign: 611e8fa1f. C2 v2 amendment: 9bc64e4cf.
Implementation: hyp_c2_impl/hyp_c2.zag (pure Zag, no Python).
Runs: run_v2_1.txt, run_v2_2.txt, run_v2_3.txt (3/3 byte-identical).

## Verdict: C2-F5 FIRES. Hypothesis falsified as a bounded discovery mechanism.

C2 exceeds the 1,000,000 evaluation budget on T1, T3, T4, and T5.
Per v2 amendment sec 6: "C2-F5: any task exceeds 1,000,000 evaluations.
C2 is not a bounded discovery mechanism."

## Results (3/3 byte-identical)

| Task | VM | Predicted | Observed | Train | Evals | Repairs | Backtracks | Splits | Ops | F-SMUG |
|------|----|-----------|----------|-------|-------|---------|------------|--------|-----|--------|
| T0 2x+1 | full | SOLVE | SOLVE | 9/9 | 229287 | 3 | 1 | 0 | 5 | 1 |
| T1 abs | P | SOLVE | BUDGET | - | 1000012 | 10 | 7 | 1 | - | 1 |
| T2 mod3 | full | SOLVE | SOLVE | 17/17 | 105230 | 1 | 0 | 0 | 3 | 1 |
| T3 parity | full | SOLVE | BUDGET | - | 1000020 | 4 | 3 | 0 | - | 1 |
| T4 nabs | P | SOLVE | BUDGET | - | 1000001 | 14 | 9 | 2 | - | 1 |
| T5 fcomp | P | SOLVE | BUDGET | - | 1000009 | 15 | 12 | 1 | - | 1 |

v2-SOLVE requires train exact + ops <= 40. BUDGET tasks did not achieve
train exact within 1M evals.

## Mechanism analysis

### T0 (full VM): SOLVE, prediction CONFIRMED.

Trace (matches design walkthrough e658766bd sec 5):
  REPAIR [PUSH 1] c0=0 c1=1
  BACKTRACK [PUSH 1] (constant trap retracted)
  REPAIR [IN0 PUSH 1] c0=0 c1=1
  REPAIR [IN0 ADD ADD] c0=1 c1=9
  SOLVE 9/9 train, 16/16 held-out.

The valley is crossed by the combination the design required: lookahead
finds the multi-op fix, backtracking retracts the constant trap, and the
net-progress criterion guides the trajectory. C2-F1 does NOT fire. C2-F4
does NOT fire (1 backtrack <= 6).

### T1 (P-VM): BUDGET, prediction NOT CONFIRMED.

The MOD trick is unavailable (F-SMUG audit passes; repair alphabet
restricted to 29 P-VM symbols). C2 tries 7 negation variants ([IN0 NEG],
[IN0 IN0 NEG], [IN0 PUSH -1 MUL], etc.), each achieving 9/17 (the
non-negative x values). After 6 backtracks exhaust BMAX, it splits on
[IN0 PUSH -4 LT] (nleft=4, nright=13).

Critical: the probe is NOT sign-separating. The frozen probe order
(k=-4..4) selects [IN0 PUSH -4 LT] before [IN0 PUSH 0 LT]. The v2
mandatory trace event requires "split event on a sign-separating probe"
(v2 sec 3.6); this is not observed.

The left branch (x=-8..-5) solves via [IN0 NEG] (4/4), but the right
branch (x=-4..8, mixed signs) stagnates and the budget exhausts.

With a sign-separating probe ([IN0 PUSH 0 LT]), C2 would solve T1 in 2
repairs: [IN0 NEG] on negatives (8/8), [IN0] on non-negatives (9/9).
The failure is in probe selection order, not the repair mechanism.

### T2 (full VM): SOLVE, prediction CONFIRMED.

Single REPAIR [IN0 PUSH 3 MOD], zero backtracks, 17/17 train, 17/17
held-out. Matches design walkthrough sec 6.

### T3 (full VM): BUDGET, prediction NOT CONFIRMED.

v1 measurement stands (BUDGET/FAIL). v2 task is identical (full VM).
C2 selects [IN0 IN1 EQ] (17/25, a local optimum correlating a==b with
(a+b) even) and cannot escape via backtracking. The true solution path
([IN0 IN1 ADD] -> [PUSH 2 MOD] -> [PUSH 1 SWAP SUB]) requires intermediate
steps with LOWER pass count than the starting point (12 -> ~0 -> ~0 -> 25),
which the net-progress criterion (strictly increase) forbids. This is a
fundamental limitation: C2 cannot tolerate stepping stones that do not
immediately improve the objective.

The design's T3 prediction (single REPAIR [IN0 PUSH 2 MOD]) was incorrect;
[IN0 PUSH 2 MOD] computes a mod 2, not (a+b) parity.

### T4 (P-VM): BUDGET, prediction NOT CONFIRMED.

14 repairs, 9 backtracks, 2 splits. C2 tries MOD-based repairs (unavailable
on P-VM; alphabet restriction prevents emission, but the search wastes
evals on P-VM-valid variants that don't help). The nested conditional
structure (kinks at -2, 0, 2) is not discovered within budget. C2-F2 does
not fire (no CALLs, but T4 not solved so mechanism not observed).

### T5 (P-VM): BUDGET, prediction NOT CONFIRMED.

15 repairs, 12 backtracks, 1 split. Degenerate splitting tendency observed
(probe [IN0 PUSH -4 EQ] isolates single episode). The 0/2 kink structure
is not discovered within budget.

## Falsifiers

- C2-F1: NOT FIRED (T0 SOLVE).
- C2-F2: NOT FIRED (T4 not solved; 0 CALLs observed, mechanism not tested).
- C2-F3: NOT FIRED (max splits: 2 on T4 < 13 episodes).
- C2-F4: NOT FIRED (T0: 1 backtrack <= 6).
- **C2-F5: FIRES** (T1, T3, T4, T5 exceed 1M evals).
- F-TRICK: NOT FIRED (no straight-line P-VM solve exhibited).
- F-SMUG: NOT FIRED (audit passes on all P-VM tasks; no DIV/MOD emitted).
- F-MEM: NOT FIRED (T0: 5 ops, T2: 3 ops, both <= 40).

## Honest scope

C2's non-myopic repair (lookahead + backtracking + net-progress) solves
T0, which falsified C1. This is genuine progress: the valley-crossing
mechanism works where greedy C1 failed.

However, C2 fails as a general discovery mechanism:
1. The net-progress criterion cannot follow solution paths through
   intermediate count decreases (T3).
2. The probe order (k=-4 first) selects non-sign-separating splits,
   preventing the predicted T1 mechanism (T1).
3. On P-VM tasks, the restricted alphabet removes arithmetic shortcuts
   but C2 lacks the conditional-discovery power to compensate within
   budget (T1/T4/T5).
4. C2-F5 fires on 4/6 tasks; C2 is not a bounded discovery mechanism.

The implementation is faithful to the amended prereg: P-VM repair
alphabet (29 symbols) for T1/T4/T5, full alphabet (34) for T0/T2/T3,
probes on full VM per v2 sec 3.3, F-SMUG audit, v2-SOLVE op cap.

## v1 vs v2

v1 C2 (full VM on all tasks): T0 SOLVE, T1 SOLVE (via MOD trick),
T2 SOLVE, T3 BUDGET, T4 BUDGET, T5 BUDGET.
v2 C2: T0 SOLVE, T1 BUDGET (P-VM, MOD trick removed), T2 SOLVE,
T3 BUDGET (unchanged), T4 BUDGET (P-VM), T5 BUDGET (P-VM).

Per v2 sec 3.8, v1-T1/T4/T5 conditional interpretations are SUPERSEDED.
v1-T0/T2/T3 interpretations stand.

## Kill bars (v2 amendment sec 5)

- K1: PASS. Amendment 9bc64e4cf frozen before v2 code changes.
- K2: PASS. C2 implemented against v2 (P-VM alphabet for T1/T4/T5).
- K3: PASS. T1/T4/T5 tested on v2 (3/3 byte-identical). T0/T2 v1 stand.
- K4: PASS. Pure Zag, zero Python, zero em/en-dash bytes, 3/3 deterministic.
- K5: PASS. F-SMUG audit 1 on all P-VM tasks.
- K6: PASS. Op cap verified (T0: 5, T2: 3, both <= 40).

## Files

- hyp_c2_impl/PREREG_HYPC2.md (v1 prereg, 01336fe83)
- hyp_c2_impl/PREREG_HYPC2_AMENDMENT_V2.md (v2 amendment, 9bc64e4cf)
- hyp_c2_impl/hyp_c2.zag (v2 implementation)
- hyp_c2_impl/HYP_C2_RESULT_V2.md (this file)
- hyp_c2_impl/run_v2_1.txt, run_v2_2.txt, run_v2_3.txt (3/3 byte-identical)
- hyp_c2_impl/run1.txt, run2.txt, run3.txt (v1 runs, superseded for T1/T4/T5)

**Builder label: C2-TESTED (C2-F5 FIRES on v2, hypothesis falsified as bounded discovery)**
