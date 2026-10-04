# Q4 Adversary Consolidation

## Verdict: Q4-ADV-CONSOLIDATED

This document consolidates all adversary defeats of the Q4 discovery
mechanism across independent preregistered waves. It identifies the
systematic weakness shared by the failures.

## Adversary record

### 1. F-RECFOLD v1 pilot (3868e3852)

- Verdict: BUILD-FAIL pilot.
- Governance: K4-VIOLATED (Python-authored patch). Exploratory only.
- Results: I1 40-46/64, I2 63/64 on all 3 seeds (constant-0),
  I3 32-40/64. B1 fails on all instances.

### 2. F-RECFOLD clean rerun (5a21bb2b3)

- Verdict: FREC-CLEAN-VOID (K3 literal violation in pre-prereg).
- Results: exploratory, same pattern as v1.

### 3. F-RECFOLD zero-Python rerun (1c52f7dad)

- Verdict: FREC-ZERO-FAIL. Governance-clean.
- K1 (zero Python from task start): PASS.
- K2 (15/15 evaluations): PASS.
- K3 (3/3 byte-identical): PASS.
- Cross-worker reproduction: byte-identical to the VOID wave output.
- Results: I1 40-46/64 (0/5), I2 63/64 on all 5 seeds via 0-op
  constant-0 (0/5), I3 32-40/64 (0/5).
- B1 FAIL on all 3 instances. B2 PASS. B3 PARTIAL. B4 N/A.

### 4. R1 multi-seed robustness (e40cb1b51)

- Verdict: R1-FAIL. F-R1 fired.
- Prereg: bea779792 (frozen before implementation).
- Results: 0/5 seeds meet the bar.
  - Coverage: 8/8 on all 5 seeds (P-RAND succeeds).
  - Evidence fit: 24-31/32, never 32/32.
  - True accuracy: 48-56/64, never 64/64.
  - Tax-off ties on 3/5 seeds (beam defect signal per prereg).

### 5. R3 reuse beyond perfect terminal (023b4f84a)

- Verdict: R3-FAIL (Arm 1 PASS, Arm 2 FAIL).
- Arm 1: reuse robust to padded (non-minimal) component. PASS.
- Arm 2: reuse 24 IVs, 53/64 true (bar 64/64). FAIL.
- Failure localization: beam locks from round 6 onto a 3-op
  expression containing D that fits evidence (up to 29/32) but
  generalizes to 53/64. The true 4-op E was never generated in 25
  beam extensions.

### 6. R4 disagreement policy (8b0ede871)

- Verdict: R4-FAIL. F-R4 fired.
- P-DIS total coverage 92 vs P-RAND 95.
- Mean margin -0.25 vs frozen dual bar (+0.75).
- P-DIS wins 0/12 paired seeds.
- P-DIS retired; the active-intervention component is decorative.

## Systematic weakness

Four independent preregistered failures (R1, R3, F-RECFOLD zero,
R4) converge on one component: the beam/search.

### W1: Simplicity-tax trap

The 200/opc simplicity tax helped Phase 1 find the minimal D. In
R3 Arm 2 it works against the true form: the 3-op overfitter scores
~9400 at full evidence fit (10000 - 600) versus 9200 for the true
4-op E (10000 - 800). The greedy top-32 beam locks onto the simpler
wrong expression early; subsequent generations build combinations
of overfitters instead of the clean compositional chain. The true
form is never expressed. This is a real mechanism limitation, not
a component or target defect.

### W2: Constant-prediction ceiling

In F-RECFOLD I2, the mechanism deterministically selects 0-op
constant-0 (63/64 correct, since the truth table has 1/64 ones) on
all 5 seeds across two independent workers. It never discovers the
5-AND nested chain. The 63/64 consistency across seeds and workers
shows a systematic deterministic trap, not seed luck: the scoring
landscape has a constant-prediction attractor the search cannot
escape.

### W3: Evidence-fit failure at full coverage

In R1, P-RAND reaches 8/8 coverage on all 5 seeds, yet the beam
never fits the observed evidence (24-31/32, never 32/32) and never
reaches 64/64 true accuracy (48-56/64). Full coverage did not make
the problem beam-solvable. The failure is in search, not just
generalization. Combined with W1, the picture is a search that
cannot navigate expression space to the true form even when the
evidence is fully covered.

### W4: Tax-off ties

Three of five R1 seeds show preregistered tax-off ties: the beam
retains multiple expressions with equal evidence-fit but different
generalization. Per the frozen prereg, a tie indicates a harness
or beam defect. This is a beam defect signal consistent with W3:
the scoring cannot discriminate the true form from competitors at
equal fit.

### Convergent diagnosis

The Q4 beam's greedy filtering plus strong simplicity bias creates
traps where simpler evidence-fitting expressions permanently block
true forms. The mechanism cannot escape local optima in expression
space:

- When a constant predictor scores high (I2), it is selected
  deterministically and the nested structure is never found.
- When a 3-op overfitter outscores the true 4-op form (R3 Arm 2),
  the beam locks on and builds overfitter combinations.
- When full evidence is covered (R1), the beam still cannot fit it
  or generalize from it, with ties signaling scoring blindness.

The same simplicity bias that found the minimal D in Phase 1 now
systematically defeats compositional and nested discovery. This is
the localized weakness the revival closure (563a1b354) identified.

## Standing

- Q4 remains bounded L2. Revival is closed (R1, R3, R4 fail;
  conjunction broken).
- These adversary defeats are governance-clean data points for the
  Q4 line under the promotion pipeline.
- No L3 or Criterion 0 claim is made or implied here.
- The defined next target is a beam/search mechanism that fits
  evidence at full coverage, escapes simplicity-tax traps, and
  resolves ties honestly.

## Kill bars

- K1 (consolidation complete): PASS. All six adversary waves
  recorded with commits, verdicts, and measurements.
- K2 (weakness identified): PASS. W1-W4 documented with the
  measurements that establish each.
- K3 (no overclaim): PASS. Bounded L2 standing restated; no L3,
  no Criterion 0, no revival claim.
