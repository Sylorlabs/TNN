# SENSES-REMATCH VERDICT

Frozen prereg: `PREREG_AMENDMENT.md` (commit `e819852b487b021451567f9ed60ef2ebd0c1e098`).
Fitting grids/tie-breaks: `CALIBRATION.md` (committed before any fitting).
All decisions below are mechanical applications of the preregistered kill bars.
No rescue language is offered; the verdict is delivered as computed.

## Headline

**B STAYS DEAD.**

At T* = T4 (highest completed budget ≥ T3): B_mean − A_mean = **−27.1pp**
(B = 56.6%, A = 83.8%). KB6 requires (B−A) ≥ +2pp AND B ≥ 60%.
B fails both prongs. B never crossed A at any budget, never reached 60%
at any budget, and both approaches plateaued at T1.

## Learning curves (TEST-FRESH, fitted judgments)

| budget | A color-disc | A color-const | A shape | A pitch | A timbre | A motion | **A mean** | B color-disc | B color-const | B shape | B pitch | B timbre | B motion | **B mean** |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| T0 (hand) | 48.3 | 92.5 | 100.0 | 83.3 | 75.0 | 33.3 | **72.1** | 41.7 | 57.5 | 36.7 | 85.0 | 75.0 | 16.7 | **52.1** |
| T1 | 76.7 | 92.5 | 100.0 | 100.0 | 100.0 | 33.3 | **83.8** | 55.0 | 67.5 | 36.7 | 85.0 | 75.0 | 16.7 | **56.0** |
| T2 | 76.7 | 92.5 | 100.0 | 100.0 | 100.0 | 33.3 | **83.8** | 55.0 | 67.5 | 36.7 | 85.0 | 75.0 | 18.3 | **56.2** |
| T3 | 76.7 | 92.5 | 100.0 | 100.0 | 100.0 | 33.3 | **83.8** | 55.0 | 67.5 | 38.9 | 85.0 | 75.0 | 18.3 | **56.6** |
| T4 | 76.7 | 92.5 | 100.0 | 100.0 | 100.0 | 33.3 | **83.8** | 55.0 | 67.5 | 38.9 | 85.0 | 75.0 | 18.3 | **56.6** |

(values in %; T0 = hand-tuned thresholds, no fitting)

Budget sizes (fixtures per task): T0 n/a · T1 = round-1 size (740 total) ·
T2 = 10× (3,700) · T3 = 50× (18,500) · T4 = 100× (37,000).
Budgets are cumulative by construction (same TRAIN seed 20260922, per-index
deterministic; T2 ⊇ T1, T3 ⊇ T2, T4 ⊇ T3).
TEST-FRESH: 740 fixtures, fresh seed 20260923, never seen in training.

## Fitted parameters per budget

| budget | A colordisc t | A colorconst t | A motion t | A pitch t | A timbre (b1,b2,b3) | B colordisc k | B colorconst k | B motion t | B pitch k | B shape (m,prio) | B timbre (tc,tb,tf) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| T0 hand | 40 | 150 | 3 | 20000 | (1075,1400,3000) | 1 | 1 | 200 | 0 | (0,0) | (1150,60,1780) |
| T1 | 10 | 150 | 1 | 5000 | (1075,1400,2600) | 0 | 0 | 200 | 0 | (2,0) | (1150,60,1780) |
| T2 | 10 | 150 | 1 | 5000 | (1075,1400,2600) | 0 | 0 | 100 | 0 | (2,1) | (1150,60,1780) |
| T3 | 10 | 175 | 1 | 5000 | (1075,1400,2600) | 0 | 0 | 100 | 0 | (2,1) | (1150,60,1780) |
| T4 | 10 | 175 | 1 | 5000 | (1075,1400,2600) | 0 | 0 | 100 | 0 | (2,1) | (1150,60,1780) |

(A shapetrans is not fitted — nearest prototype, frozen. Deterministic
coordinate sweep with hand-value tie-break anchor, per CALIBRATION.md.)

## KB1 — viability (mean ≥ 60% on TEST-FRESH)

| budget | A | B |
|---|---|---|
| T0 | 72.1% ALIVE | 52.1% **KILLED** |
| T1 | 83.8% ALIVE | 56.0% **KILLED** |
| T2 | 83.8% ALIVE | 56.2% **KILLED** |
| T3 | 83.8% ALIVE | 56.6% **KILLED** |
| T4 | 83.8% ALIVE | 56.6% **KILLED** |

B never reaches the 60% viability bar at any budget, including 100× training.

## KB2 — head-to-head (higher mean wins; tie iff |Δ| < 2pp AND ops < 2×)

| budget | B−A (pp) | winner |
|---|---|---|
| T0 | −20.0 | A |
| T1 | −27.8 | A |
| T2 | −27.5 | A |
| T3 | −27.1 | A |
| T4 | −27.1 | A |

No ties. A wins every budget by 20–28pp.
Compute (TEST-FRESH binary ops): A = 413,890,710 · B = 171,235,328 · ratio 2.42×.

## KB3 — winner fragility (TEST-FRESH → ADV-R1 drop > 25pp ⇒ fragile)

Winner is A at every budget. Drop: T0 20.4pp · T1–T4 18.7pp.
**Not fragile** at any budget (all < 25pp).

Adversarial accuracy (ADV-R1, fitted): A 51.7%→65.0% · B 45.7%→44.7%.

## KB4 — adversarial false-install rate ≤ 10% (shared round-1 memory rule)

| budget | A rate | B rate |
|---|---|---|
| T0 | 59.0% (79/134) **FAIL** | 55.0% (72/131) **FAIL** |
| T1 | 48.2% (55/114) **FAIL** | 54.5% (72/132) **FAIL** |
| T2 | 48.2% (55/114) **FAIL** | 54.5% (72/132) **FAIL** |
| T3 | 48.2% (55/114) **FAIL** | 55.8% (67/120) **FAIL** |
| T4 | 48.2% (55/114) **FAIL** | 55.8% (67/120) **FAIL** |

Both approaches fail KB4 at every budget. Under the shared memory rule,
roughly half of all installed adversarial judgments are false — for the
winner (A) as well as for B. Training does not repair this: A's rate drops
from 59% to 48% at T1 and then freezes; B's never drops below 54%.

## KB5 — 3 reruns of the full fitted pipeline byte-identical

**PASS.** Three fresh reruns (binary re-evaluation of TEST-FRESH + ADV-R1
from deleted caches, then deterministic sweep) produced identical result
digests: `100b19f438b378297d96bf7082061597771464b6595a7d009017dc870bfd968e`
× 3. (`kb5_digests.txt`)

## KB6 — crossover at T* (B−A ≥ +2pp AND B ≥ 60%)

T* = T4 (highest completed budget ≥ T3).
B − A = **−27.1pp**. B mean = 56.6% (< 60%).

**Decision: B STAYS DEAD.**

B never crossed A at any budget (crossing set: empty). The gap widened
against B with the first 10× of training (T0 −20.0pp → T1 −27.8pp) and
then froze. 100× training bought B +4.5pp total (52.1% → 56.6%) while A
gained +11.7pp by T1 (72.1% → 83.8%) and then plateaued.

(B2 vocabulary growth is out of scope for this rematch.)

## Robustness at scale (descriptive, no kill bar)

D = TEST-FRESH mean − ADV-R1 mean, in pp:

| budget | D_A | D_B | D_A − D_B |
|---|---|---|---|
| T0 | 20.4 | 6.3 | +14.0 |
| T1 | 18.7 | 9.4 | +9.3 |
| T2 | 18.7 | 9.7 | +9.0 |
| T3 | 18.7 | 11.9 | +6.8 |
| T4 | 18.7 | 11.9 | +6.8 |

"B's robustness advantage grows" is SUPPORTED iff at T*: D_B < D_A AND
(D_A−D_B)(T*) > (D_A−D_B)(T0). At T4: D_B (11.9) < D_A (18.7) holds, but
the gap **shrank** (14.0 → 6.8). **NOT SUPPORTED.**

Note: B's smaller D is an artifact of its lower ceiling — B degrades less
in absolute pp because it starts lower, and its adversarial accuracy
actually fell slightly with training (45.7% → 44.7%).

## Plateau report

Earliest budget after which every subsequent step is < 1pp:

- **A: T1** (steps: +11.7, 0.0, 0.0, 0.0 pp)
- **B: T1** (steps: +3.9, +0.3, +0.4, 0.0 pp)

Both approaches plateau at T1 (10× round-1 data). T2–T4 (up to 100×)
changed neither approach's mean by more than 0.4pp. The learning curves
are flat after the first order of magnitude — for the winner and the loser.

## Per-task notes

- **motiondir** is catastrophic for both: A 33.3% (unfitted octant rule
  keeps hand behavior; fitted STILL gate t=1 cannot save it), B 16.7%→18.3%.
  The fitted families cannot express the task.
- **shapetrans**: A 100% at all budgets (frozen nearest-prototype). B's
  vote family tops out at 38.9% — qualitative shape votes lose to raw
  prototype matching and fitting cannot close it.
- **timbredisc**: A 75.0%→100% (b3: 3000→2600). B frozen at 75.0%
  across all budgets (fitted thresholds identical to hand:
  (1150,60,1780) — the sweep never moved).
- **pitchdisc**: A 83.3%→100% (t: 20000→5000). B stuck at 85.0% (k=0).
- **colordisc/colorconst**: A 76.7%/92.5%; B 55.0%/67.5%. B's k=1→0 move
  helped at T1 (+13.3pp/+10pp) but stalled there.

## Caveats

1. **Premature T1 start (documented 2026-09-22):** a T1 generation run was
   accidentally launched after CALIBRATION.md was authored but before it
   was committed and before validation finished. Only fixture-count log
   lines were observed (no fitted values); the directory and run cache
   were deleted and T1 was regenerated after the calibration commit with
   seed 20260922. The reported T1 numbers come from the regenerated data.
2. **Environment instability:** the lab VM rebooted 4 times during the run
   (2026-09-22 ~03:12, ~05:22, ~06:52 UTC, plus one service restart).
   Generation was made resumable (per-index deterministic) and the run
   cache writes incrementally in 2000-record chunks; all completed datasets
   were re-verified by manifest after each incident. No fixture or cache
   content was lost; at most one partial chunk per incident was recomputed.
3. **B motion fitting rule ≠ round-1 binary rule:** the frozen fitting
   family ("STILL iff mcount < t", anchored at 200) is not the binary's
   original centroid-displacement STILL rule (hand-rule agreement on
   fixtures: 141/150). Reported B motion numbers are under the fitted
   family, as the amendment specifies.
4. **T2 colordisc class balance:** the frozen generator's absolute-index
   behavior yields SAME=20/DIFFERENT=580 at T2. This was not rebalanced;
   it is the generator's specified behavior.
5. **KB4 confidence:** the shared memory rule ran on binary-emitted
   confidences (frozen confidence rules); only judgments were fitted,
   per the amendment's "fitted judgment streams".
6. **ADV-R1 A shapetrans:** one known binary task failure
   (`p042.img`) counts as incorrect (denominator preserved).
7. **T4 feasibility:** T4 completed within the 24-hour rule (measured T3
   timing projected it feasible; actual T4 generation + runs ≈ 4.5h).

## Artifacts

- `results_main.json` — full per-budget results (params, TEST-FRESH,
  TEST-R1, ADV-R1, memory, ops). sha256 in `results_main.sha256`.
- `verdict_summary_main.json` — machine-readable kill-bar decisions.
- `learning_curves.csv` — plot data for the curves above.
- `kb5_digests.txt` — KB5 rerun digests (PASS).
- `data/*/MANIFEST.sha256`, `data/*/counts.json` — training/TEST-FRESH
  manifests.
- `runs_*.jsonl` — binary judgment caches (TRAIN_T1..T4, TEST_FRESH,
  TEST_R1, ADV_R1).
- `pipeline.log` — generation/run log with incident markers.

## Commits (branch `tnn-native-lab`)

- `e819852b487b021451567f9ed60ef2ebd0c1e098` — frozen amendment (alone, first)
- `2c7a894b629f1f54a0c9a1c9d546f2a480af4996` — calibration, instrumented B,
  validation/relation harness
- `f34a167292a28814363044e3d615d5943cef097d` — KB4 stream-order fix, KB5 script
- (this commit) — resumable pipeline, fit/analyze/kb5, results, verdict
