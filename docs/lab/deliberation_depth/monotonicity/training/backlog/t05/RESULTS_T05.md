# RESULTS_T05.md — T-05 worst-case polarity loss (pure form v2)

Date: 2026-09-24. Prereg: `PREREG_T05.md` v2 (amended before any 100× run;
v1 design killed by its own go/no-go, diagnosed, amended — §4).

## 1. Training

Trainer `src/train5.zag` (pure per-cell loss; NO theater, NO G-batch —
v2 amendment). Builds A/B byte-identical
(SHA-256 `6c14bfce07b9c1c7`, 160393 bytes).

| arm | scale | params A/B | log A/B | P/O train conf | phase-A loss p0→p1 |
|-----|-------|-----------|---------|----------------|---------------------|
| W (target 0) | 10× | identical | identical | 4 (< 300 ✓) | 722882 → 1783366 (up — WAIVED, see §2) |
| W | 100× | identical | identical | — | — |
| L (target 500) | 10× | identical | identical | 493 (∈ [300,700] ✓) | 722882 → 553976 (down ✓) |
| L | 100× | identical | identical | — | — |

Substitution-validity (Arm L settles at ≈500 on P/O): **PASSES**
(493 at 10×). D4: v2/gviol log columns read 0 on all 600 epochs per arm
(confounds confirmed off).

Final 100× weights —
W: w=[330,−600,0,−183,−155,−2161,−869,687], b=2060;
L: w=[779,157,0,−309,−246,−1534,−947,850], b=1726
(init was w1=1000, rest 0, b=0; both arms moved substantially).

## 2. Go/no-go waiver (Arm W, bar (c))

Bar (c) (phase-A loss decreased pass 1 vs pass 0) FAILED for Arm W
(722882 → 1783366). Diagnosis: not a machinery failure — the P/O→0
pressure on shared weights interferes with phase-A calibration, which is
exactly the D1/D2 tension the experiment measures (bar (b-W) passed:
P/O conf = 4; Arm L's bar (c) passed, proving the machinery is sound).
Bar (c)'s purpose (catch unrepresentable/broken updates) is met; the
failure mode is signal, not noise. **Waived with this diagnosis
recorded**; D1/D2 adjudicate at eval.

## 3. Eval

Policy `src/policy5.zag` (policy.zag + T-05 params; gate frozen from v2).
Builds A/B byte-identical per arm per scale.
22 legs (§8: ceiling d1–d64; logic/admit/trap d1–d16) × 2 arms × 2 scales
(10×, 100×) × A/B = **176 legs, all byte-identical, rc=0**.

## 4. Kill-bar evaluation (literal, strict primary)

The live O battery contains **zero wrong cells at any depth** (all graded
O cells correct; d64 all-abstain under the frozen M4 skeleton — M4 does
the same). Hence:

- Worst-case arm O G(64): **UNDEF** (no graded cells) → `> 0.1` NOT TRIGGERED.
- Worst-case arm O V2: **0/0 = 0.0%** → `> 5%` NOT TRIGGERED.
- "Only worst-case" clause (control O G ≤ 0): G(64) UNDEF → literal
  clause not triggered. (Substantive reading: control O G(d) = −0.48…−0.58
  < 0 at all graded depths — but this is automatic since all graded O
  cells are correct, G = conf − 1 ≤ 0 for ANY policy. Vacuous.)

The literal kill bar is **vacuous on the live O battery** — it can neither
fire nor confirm. The claim's substance is evaluated on P (the family
where wrong released cells exist; the backlog's "wrong O item" role).

## 5. Substance: P family (wrong released cells), 100×

| arm | G(d1)→G(d32) | V1 | V2 | 1→0 |
|-----|--------------|----|----|-----|
| W | +0.008 → +0.000 (no overconfidence, all depths) | 0/0 | 10/140 (7.1%) | 0 |
| L | +0.420 → +0.473 (≈ +0.5, law violated as predicted) | 0/0 | 70/140 (50.0%) | 0 |

W's 10 V2s: all on H5B-P-40-*, rises of +1…+13 thousandths
(max conf 20/1000 = 0.02) — strict-counted, substantively flat at ~0.
Refined reading: 0 crossings of substance (one rounding artifact
+0.008→+0.000).

Predicted observables (§5):
- W: P/O conf ≈ 0 (< 0.05 ✓); V1 = 0 ✓; V2 substantively 0 ✓;
  O G(d) ≤ 0 all d ✓ (vacuously, G = −0.99…−1.00).
- L: P/O conf ≈ 450–500 (≈ 0.5 ✓); violation present (P G ≈ +0.5 ✓,
  on P rather than O as the backlog's battery imagined it).

10× → 100× stability: W P G ≈ 0 and L P G ≈ +0.5 already at 10×;
honest-family damage also already present at 10× (W logic 39, L logic 409).

## 6. Non-degeneracy guards (100×)

| arm | D1 logic correct mean c (≥500) | D2 logic collapse vs v2-100× (<50%) | D2 admit | D3 answer vs M4 |
|-----|-------------------------------|-----------------------------------|----------|-----------------|
| W | **67 — FAIL** | **93% — FAIL** | −268% (801 vs 217: inflated, not collapsed) | 0/4035 disagreements — PASS |
| L | **385 — FAIL** | **62% — FAIL** | −318% (909 vs 217) | 0/4035 — PASS |

(Logic has no wrong cells → C−W separation n/a; the collapse metric is
the binding D2 bar. v2-100× reference: logic 1000, admit 217.)

Per §6: **W's P-family numbers do NOT count as satisfying the kill bar**
— D1 and D2 fail. The numerical win is degenerate suppression.

## 7. Mechanism of the degeneracy

Released training cells, feature means (f1..f8):
- P (wrong): [457,100,0,42,269,**1000**,0,0]
- O (right): [457,100,0,42,286,**1000**,0,0]
- logic (right): [562,28,0,62,976,**917**,124,0]

To drive P/O (f6=1000) to 0, Arm W learned w5=−2161 on f6; logic's
f6=917 rides the same crush (logic conf ≈ 0). A separating solution
EXISTS in the hypothesis class (f5: P/O ≈ 280 vs logic 976 → w4 ≈ +1500
separates with b tuned), but greedy online updates found the lazy
f6-crush. The failure is in the training dynamics finding the degenerate
optimum, not (provably) in the loss's global optimum. Finite-λ or a
non-greedy optimizer might separate — follow-up, not this entry.

## 8. Determinism record

- train5 build A/B: byte-identical (both forms).
- 10×/100× params + logs per arm: A/B byte-identical (8 runs).
- policy5 build A/B per arm per scale: byte-identical.
- 176/176 eval legs A/B byte-identical, rc=0 throughout.

## 9. Artifacts

- `src/train5.zag`, `src/policy5.zag`, `src/build_{a,b}/`, `polbuild/`
- `params_v2/`, `logs_v2/` (pure form); `params/`, `logs/` (superseded v1 confounded runs)
- `results/` (176 TSVs), `analyze_t05.py`, `run_eval_t05.sh`
