# PREREG — W7 LAUNDERING-HUNTER PAM (wild track, WILD-B)

**Date:** 2026-09-24. **Crew:** WILD-B. **Status:** FROZEN — committed before
any W7 fixture, build, or run. Parent: `pam/round4/prereg/PREREG_ROUND4.md`
(§4 seed design W7). Shared tape: `wild/tape/TAPE.md` (frozen).

## 1. Falsifiable claim

W7 is a dedicated provenance-laundering detector, SEPARATE from the admission
path. Given the H6 finding (GEN→EXT relabeling defeats label-trust), W7 uses
only content/behavioral signals — never the claimed label. Claims:

- **F1:** on the frozen laundering fixture set (200 entries: 100 laundered
  GEN→EXT + 100 genuine EXT), W7 flags ≥95% of laundered entries (TPR ≥ 95%)
  with ≤5% false flags on genuine externals (FPR ≤ 5%).
- **F2 (label-blindness):** the instrument never reads the claimed label —
  enforced by FILE SEPARATION: it reads only the signals file (which contains
  no label column); the truth file is joined by the scorer. A source audit
  (grep) confirms no label/truth field is referenced.
- **F3 (hygiene):** byte-identical reruns (≥2×), O(1) work per entry,
  terminates.

## 2. Frozen fixture design (`gen_launder.py`, committed after this prereg)

Deterministic (zero RNG). 200 entries, ids 0..199:
- ids 0..99: LAUNDERED — true origin GEN, claimed label EXT.
- ids 100..199: GENUINE — true origin EXT, claimed label EXT.

Per-entry signals (all 0..1000 unless noted), constructed by counter-indexed
deterministic formulas (documented in the generator; no RNG):
- `sig_c`: content similarity to the frozen GEN reference profile.
  Laundered: 550 + (id*37 mod 401) → 550..950 (GEN-authored content keeps
  GEN markers even when relabeled). Genuine: 50 + (id*53 mod 601) → 50..650.
  (Deliberate overlap band 550..650 — the detector must earn its keep.)
- `sig_b`: behavioral anomaly (bulk arrival, zero edit history, no
  first-seen history). Laundered: 700 + (id*29 mod 251) → 700..950.
  Genuine: 50 + (id*41 mod 401) → 50..450.
- `sig_a`: external attestation count (0..4). Laundered: 0 (stolen content
  gets no real attestation). Genuine: 1 + (id mod 3) → 1..3.

Two files (frozen):
- `launder_signals.txt`: `id|sig_c|sig_b|sig_a` — THE ONLY FILE THE
  INSTRUMENT READS. No label columns exist in it.
- `launder_truth.txt`: `id|true_origin|claimed_label` — scorer only.

This extends the shared attack tape via `wild/tape/TAPE_W7_ADDENDUM.md`
(committed with the fixtures, before the W7 build).

## 3. Frozen mechanism (instrument: pure-Zag `w7_hunter.zag`)

Suspicion score (frozen weights, integer arithmetic):
`suspicion = (sig_c*3 + sig_b*2 + (1000 − min(sig_a,4)*250)) / 6`
Verdict: FLAG iff suspicion ≥ 600 (frozen threshold), else CLEAR.
Per-entry O(1); no state across entries (the hunter is stateless — each
entry judged on its own signals).

Design rationale for the frozen constants (recorded, not tuned): the three
signal terms are scaled to 0..1000 each; weights 3/2/1 reflect the design
prior that content markers are the strongest laundering evidence,
behavioral second, attestation absence third. Threshold 600 sits above the
genuine population's typical score (~290) and below the laundered
population's typical score (~840). Whether the overlap band defeats it is
exactly what the battery measures.

Predicted: laundered min (550,700,0) → 675 ≥ 600 ✓; genuine max corner
(650,450,1) → 600 → false flag (boundary). Expected FPR small; measured.

## 4. Kill bars (program §4 K1–K5 verbatim + W7 additions, add-only)

- **K1:** the laundering fixture set IS W7's wrong set analog: any laundered
  entry CLEARED beyond the FPR/TPR bars is counted in KB-W7-D below. (K1's
  frozen wrong set (TMB-5/CC1) is a different attack class; W7 does not
  process it — recorded, not evaded: W7 is a separate detector, and its K1
  analog is defined here.)
- **KB-W7-D (added):** TPR < 95% (<95/100 laundered flagged) → KILL.
  FPR > 5% (>5/100 genuine flagged) → KILL.
- **KB-W7-L (added):** source audit finds the instrument reading
  `launder_truth.txt`, or referencing any label/origin field, or the signals
  file containing a label column → KILL (label-trust smuggled in).
- **K2:** the two battery runs' stdout differ by even one byte → KILL.
- **K3:** not applicable as a throughput bar (W7 is a detector, not an
  admission gate) — reported instead: TPR/FPR are the judgment metrics.
  Recorded explicitly so the verdict is not accused of dropping K3.
- **K4:** per-entry work superlinear in fixture size → KILL (stateless O(1)
  by construction; asserted via entry count vs cycle proxy).
- **K5:** non-termination on any fixture → KILL.

## 5. Diagnostics (reported, never kill — frozen list)

- **D-W7-1:** full score histogram (laundered vs genuine) — shows the
  separation and the overlap band.
- **D-W7-2:** per-signal ablation: TPR/FPR using each signal alone
  (computed by the scorer, not the instrument) — which signal carries the
  detection.
- **D-W7-3:** the exact ids of missed laundered entries and falsely flagged
  genuine entries.

## 6. Battery

Instrument: pure-Zag `w7_hunter.zag`. CLI: `w7_hunter <signals_file>`.
Emits `id|FLAG|CLEAR|suspicion` per entry + summary. Runs: 2×;
sha256(stdout) must match. Scorer: `score_w7.py` joins truth, computes
TPR/FPR, runs the KB-W7-L source audit, D-W7-1..3.

## 7. Open question from the debate — DECIDED HERE

"Whether W10's forger library and W7's laundering detector should share
transforms." DECISION: NO sharing. W7's signal construction
(`gen_launder.py`) and W10's forger transform library are independently
defined and independently implemented (Python fixture generator vs Zag
in-instrument transforms, different field semantics). Rationale: shared code
is shared fate (debate §notes); W10's forger must be fixed BEFORE seeing
W7's signals or the duel is tuned to the detector. Recorded here so the
non-sharing is deliberate, not an oversight.

## 8. Hands-off / laws compliance

- No M1 thresholds involved; nothing recalibrated.
- Fable's 4 kill-bar repairs: not applied. 3 HELD items: not run.
- Zero RNG; no wall-clock; deterministic given (signals, weights).
- []u8 arenas + LE accessors; no `as []i32/u32/u16` indexed casts.

## 9. Standing-law cap note (for verdict-time classification)

Frozen numeric caps: suspicion threshold 600, weights 3/2/1. Classified at
verdict time per the 2026-09-24 standing law. (Design note: A threshold is
load-bearing for any detector — the decision must come from somewhere; the
VALUE 600 is calibration to the signal gap, flaggable.)
