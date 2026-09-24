# VERDICT_T05.md — T-05 worst-case polarity loss: FALSIFIED

Date: 2026-09-24. Entry: T-05 (grok H-17), HYPOTHESIS_BACKLOG_TRAINING.md §T-05.
Prereg: `PREREG_T05.md` v2 (frozen; v1 killed by its own go/no-go, amended,
re-run). Results: `RESULTS_T05.md`.

## Verdict: FALSIFIED

The claim — "only a worst-case loss over polarity pairs matches the
law's universal quantifier" — fails on its sufficiency direction. The
worst-case arm (Arm W, target 0 on released P/O cells) does drive
P-family overconfidence to G ≈ +0.008 → +0.000, but **degenerately**:
logic correct-cell mean confidence collapses 1000 → 67 (D1 FAIL),
93% collapse vs v2-100× (D2 FAIL). Per prereg §6 the numbers do not count
as satisfying the kill bar. The loss buys mirror-family compliance by
crushing the shared feature direction (w5 = −2161 on f6=1000 for P/O
drags logic's f6=917 with it) — the exact degenerate-suppression pattern
the H-0 re-verification flagged (conf→0 + collapse, here without even
needing abstention volume since D3 holds: answer channel frozen,
0/4035 disagreements vs M4).

The necessity direction is confirmed: the mean control (Arm L, target 500)
settles at P/O conf ≈ 493 and shows the predicted violation —
P G ≈ +0.42 → +0.47 with 50% V2 (70/140). Log loss cannot express
"never", as claimed. But since the worst-case loss does not
non-degenerately match the law either, the "only X matches" claim is
false as stated.

## Kill-bar accounting (honest)

- Literal bar ("Worst-case arm leaves O G(64) > 0.1 or O V2 > 5% →
  KILLED"): **NOT TRIGGERED — vacuous**. The live O battery contains zero
  wrong cells at any depth (all graded O cells correct; d64 all-abstain
  under the frozen skeleton, M4 identical), so O G(64) is undefined and
  O V2 is 0/0. The bar can neither fire nor confirm on this battery.
- "Only worst-case" clause (control reaches O G ≤ 0 → clause KILLED):
  literally vacuous on O (G = conf − 1 ≤ 0 automatic for any policy);
  substantively the control does NOT reach compliance where violations
  are possible (P G ≈ +0.5) → the clause's intent SURVIVES.
- The falsification therefore comes via prereg §6 guard-gating, not via
  the bar firing. No post-hoc bar movement was performed; the vacuity is
  documented, not repaired.

## Strict vs refined L-OVERCONF

- Strict: W P shows 10 V2 violations (7.1%) — all rises ≤ 13 thousandths
  (max conf 0.02), substantively flat at zero; V1 = 0. L P: 70 V2 (50%),
  massive. O: 0/0 both arms.
- Refined (zero-crossings): W P 1 rounding artifact (+0.008 → +0.000);
  W O 0; L as strict. The verdict is identical under both readings —
  it turns on D1/D2, not on V-counts.

## What this means

1. v2's mean-vs-maximum diagnosis STANDS and is sharpened: the mean
   aggregation violates exactly as predicted (G ≈ +0.5), but the
   worst-case aggregation is not sufficient — with this linear head and
   greedy online optimizer, training finds the degenerate crush even
   though a separating solution exists in the hypothesis class
   (f5: P/O ≈ 280 vs logic 976 admits w4 ≈ +1500 separation).
2. The binding constraint appears to be the OPTIMIZER, not the loss
   geometry: finite-λ worst-case, a non-greedy optimizer, or a head that
   can gate on the separating feature might succeed. That is a new
   follow-up (optimizer/curriculum direction — feeds T-04/T-09), not a
   rescue of this entry.
3. For Micah's hypothesis (depth-overconfidence is trainable away):
   this is one clean negative data point — the "right" loss, trained
   100× deterministically, still failed non-degenerately. It does not
   kill the hypothesis (other losses/optimizers untested), but it kills
   the specific "worst-case loss suffices" mechanism.

## Dependencies

- T-05 does not kill or rescue other backlog entries by its prereg.
- Informs T-04/T-09 (optimizer/curriculum): the degenerate-crush
  dynamics found here are the obstacle any training intervention must
  avoid; the f5 separation signal is the positive lead.

## Reproducibility

Pure Zag, zero RNG throughout. train5 build A/B byte-identical
(`6c14bfce07b9c1c7`); 8/8 training runs A/B byte-identical;
policy5 builds A/B byte-identical; 176/176 eval legs A/B byte-identical.
Artifacts: `src/`, `params_v2/`, `logs_v2/`, `results/`,
`analyze_t05.py`, `run_eval_t05.sh`, `RESULTS_T05.md`, this file.
Superseded v1 (confounded) runs retained in `params/`, `logs/`.
