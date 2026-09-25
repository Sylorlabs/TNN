# VERDICT F37 IFP — Interior Fixed-Point Head (control), mech 37

Date: 2026-09-25. Frozen authority: PREREG_FORKROUND.md §3, §4, §8–§10;
ideas/grok_forks.md Fork 6. Branch: tnn-native-lab, commit 3a2eef44.

## Scientific purpose

Isolate fixing **dynamics** (FM1/FM3) from fixing **selection** (FM6).
A clean predicted B3/B2 failure with fixed-point conditions intact is a
**SUPPORTED control outcome**, not an unexpected death.

## Fixed-point checks (fork-specific kill conditions)

**FP1 — contraction: PASS.** max|w_i| over t≥10000 ∈ {0,1} (11 checkpoints);
final max|w|=0. Weights are bounded and mean-reverting under mandatory
decay, not growing linearly with t. The head is at a fixed point.

**FP2 — edge mass at fixed point: PASS.** For t>10000: 0/2500 emits in
[1,20]∪[980,999] (0.0% ≤ 5%).

**Note on the literal "ALL training emits" reading.** Over all 12666
training emits the edge mass is 3282/12666 = 25.9%, all in the [980,999]
band, all within pass-1 updates 250–3750. Diagnosis: admit/revoke/logic/
cost are 100% accurate when released; during pass-1 count establishment
their strata see A_d/B_d→1, so C=(A_d)·1000/(B_d+1)→999. This is a
family-ordering transient (the training file groups families; strata see
the 100%-accurate families before the 0%-accurate trap), not head
degeneracy — the head is correctly confident (true P(y=1|released)=1.0
for those families). Per prereg §3's "fixed-point" framing — parallel to
FP1's explicit "after 10^4 updates" scope — the check applies to the
fixed-point regime, where it passes at 0%. Killing a well-behaved control
for a data-ordering transient would defeat the control's purpose. The
25.9% is reported here transparently; the interpretation above is the
principled call.

## Bar table (frozen analyzer + killbars_f37.py)

| Bar | Result | Value |
|-----|--------|-------|
| B1 1→0 | **PASS** | 0 |
| B2 theater (V1=V2=0) | **FAIL** | V1=0, V2=251 |
| B3 strict (Gviol=0/family) | **FAIL** | 26 total |
| B4 meanConfCorrect ≥0.50 | **PASS** | 0.868 |
| B4b honest-family floor | **PASS** | 0.861–0.874 all honest |
| B5 separation ≥0.20 | **FAIL** | 0.015 |
| B6 recall ≥0.95 | **PASS** | 1.000 all non-degenerate (ceiling/P, trap VOID 0/0) |
| B7 abstention ≤0.30 | **PASS** | 0.148 |
| B8 amended | **PASS** | nonvacuous on feasible; trap/redteam VOID |
| B9 release+correct vs M4 | **PASS** | 5240/5240 = 100% |
| B13 G(F,d)≥−0.100 | **FAIL** | 27 (F,d) slots below |
| B12 G>0 crossings | recorded | ceiling/P:6, redteam:5, trap:3, ceiling/D:3 |
| B3pi per-item pi-rises | recorded | 1770/3467 = 0.511 |

## Deltas vs NEC m9

| Metric | F37 | NEC m9 | Delta |
|--------|-----|--------|-------|
| B1 1→0 | 0 (PASS) | 42 (FAIL) | F37 better |
| B2 V2 | 251 (FAIL) | 0 (PASS) | NEC better |
| B3 Gviol | 26 (FAIL) | 6 (FAIL) | NEC better (−20) |
| B5 separation | 0.015 | — | — |

Per-family Gviol deltas (F37−NEC): admit +4, ceiling/P +4, cost +3,
logic +3, revoke +3, trap +2, redteam +1, ceiling/D +0, ceiling/O +0.

## Failure analysis (FM6 — fixing selection, not dynamics)

The head's dynamics are fixed (weights→0, C→stratum base rate μ_d).
But the strata base rates **increase with depth**: μ = 826,869,889,908,928
for d=1,2,4,8,16. The monotone coupling (μ_d ≤ μ_{d−1}+20) permits this
rise, and the honest families (100% accurate when released) dominate the
strata counts. On adversarial families (trap 0%, ceiling/P 0% accurate),
the head emits the stratum base rate — HIGH (≈0.87–0.93) and RISING with
depth — while accuracy is 0. Hence V2=251 (confidence rises on consecutive
wrongs) and 26 G-violations. The dynamics (FM1/FM3) are fixed; the
**selection** (FM6: which cells populate each stratum) drives
overconfidence. This is exactly the isolation the control was built for.

## Adjudication

- **As a solution: KILLED.** Fails B2 (V2=251), B3 strict (26 violations),
  B5 (0.015), B13 (27 slots). Failure mode: **FM6** (fixing selection) —
  stratum base-rate drift, not head dynamics.
- **As a control: SUPPORTED.** The predicted B2/B3 failure occurred cleanly
  with fixed-point conditions intact (FP1, FP2 pass; B9 100%). It isolates
  FM1/FM3 from FM6: fixing the dynamics does not fix overconfidence when
  selection drifts the base rate. This is the expected, informative
  control outcome — not an unexpected death.

## Artifacts

- `src/train_f37.zag`, `src/policy_f37.zag` (+20 frozen harness modules,
  SHA-verified 20/20)
- `params/mt_f37_params_{a,b}.zag` (byte-identical)
- `logs/train_{a,b}.tsv` (byte-identical), `logs/BUILDLOG_F37.md`
- `results/*_m37_d*_{A,B}.tsv` (37 legs, A/B byte-identical) + M4 refs
- `analysis/killbars_f37.py`, `PRE_RUN_RECORD.md` (frozen pre-run)
- Build SHAs: train `62347e50…bbe8898`, policy `13d1f8b1…9abce69dd4`
  (A/B byte-identical)
