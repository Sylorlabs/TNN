# EVIDENCE — C7 Direction 3+1 Head-On Test (2026-09-20)

**Prereg:** `PREREG_2026-09-20-C7-DIRECTION-3PLUS1.md` (frozen BEFORE
implementation; not in effect — tap required).
**Method:** same episodes, both metrics, one binary per arm; independent
Python checker re-derives every verdict from raw logs.
**Determinism:** paired reruns byte-identical 6/6 both arms; rebuilds
byte-identical; zero RNG (static scan).

## The two runs

| | Run A (baseline) | Run B (redesign) |
|---|---|---|
| sources | pristine `wave9/integration/impl` | `wave12/integration-c7/impl` (§3) |
| binary SHA-256 | `e673bae2…cf0` — **byte-identical to the committed S10 trial binary** | `15f1fa35…` (new instrument) |
| C7_TELEMETRY | `…cap4,914,cap5,897` = committed evidence, byte-equal | `…cap4,914,cap5,897` = committed evidence, byte-equal |
| CHECK,c7_withdrawal | 1,0 (§5 FAIL reproduced) | 0,0 |

Run A proves the harness reproduces the committed S10 exactly on this
machine. Run B's byte-identical legacy telemetry proves the redesign is
instrument-only: the mechanism behaved identically.

## Head-on numbers (Run B, re-derived from C7_COMP components)

Intact arms:
- DC-4: cok 256, ccon 2, mhyp 639, opened 17 → cap_old 914, **cap_new 897**
- DC-5: cok 256, ccon 2, mhyp 639, opened 0 → cap_old 897, **cap_new 897**
- K1: cap_new = cap_old − opened exactly, per stage (914−17=897; 897−0=897).
  **The double-count is eliminated: each hypothesis counted exactly once.**

2×2 ablation (metric × bar), all four cells as preregistered:

| metric | bar | reading | verdict |
|---|---|---|---|
| old (double-count) | `==` | 914→897 | FIRED (§5 FAIL reproduced) |
| old (double-count) | `>=` | 914→897 | FIRED (direction 1 alone insufficient) |
| new (single-count) | `==` | 897→897 | ALIVE (direction 3 alone unblocks here) |
| new (single-count) | `>=` | 897→897 | **ALIVE — the redesign** |

The ablation isolates exactly which direction does the work: direction 1
earns no credit it did not earn (it still fires under the buggy metric);
direction 3 does the unblocking on this ledger; direction 1 is the
principled test formulation (non-inferiority) plus the dualism tripwire.

Legacy record: `C7_LEGACY_VERDICT,1` — the §5 FAIL is preserved as labeled
telemetry in the redesigned run. Nothing retro-edited.

## Positive control (K3) — convicts under BOTH metrics

- New metric: `C7_POSCTRL,cap4d,897,cap5d,641` → 641 < 897 → **convicts**.
- Legacy metric: `C7_POSCTRL_LEGACY,cap4d,914,cap5d,641` → convicts.
- Decomposition: composites_ok 256→0; hypotheses 639=639. The in-binary dep4
  arm keeps the default gate's 17 forced hypotheses (counted once inside
  mhyp under the new metric); the collapse is purely composites — the
  instrument discriminates teacher-dependence through the composites
  channel, exactly as designed. (The gate-less "zero forced" reading in the
  rescore docs was the calibration variant with the gate excised; the
  in-binary control never excised it.)

## Regression battery (K2) — no other control weakened

Run B vs Run A: all 12 stage logs byte-identical; pbite + cbite logs
byte-identical; controls CHECK-name sets identical; every controls CHECK
value identical **except** `c7_withdrawal` 1→0 (the predicted flip).
C1–C4, C6 ALIVE; §4 C5 bar holds (killed-only 0); all 17 bites pass;
P1–P10, gates G0–G5, L5 static all hold. The controls.log diff is exactly
the predicted delta: added C7_COMP/C7_NEW/C7_LEGACY_VERDICT/C7_POSCTRL*
lines, the now-executing positive control, `c7_withdrawal` 1→0.

## Kill-bar tally

- K1 double-count eliminated — PASS (914−17=897, 897−0=897, exact)
- K2 no regression — PASS (only predicted C7 delta)
- K3 positive control convicts — PASS (897→641 new; 914→641 legacy)
- K4 C7 unblocks — PASS (897→897, cap5 ≥ cap4)
- K5 determinism + behavior-neutrality — PASS (6/6 identical both runs;
  rebuilds byte-identical; Run A binary = committed binary; legacy
  telemetry byte-equal to committed evidence)
- K6 zero RNG + G0b — PASS

Independent checker: `impl/check_c7_3plus1.py` → **CHECKER VERDICT: PASS**
(full report: `evidence_3plus1/checker_report.txt`).

## Honest caveats (carried, not buried)

1. On THIS ledger direction 3 alone (with the old `==` bar) also unblocks.
   Direction 1's contribution is principled (non-inferiority is the correct
   formulation of "survives withdrawal") and protective (it resolves the
   `cap5 > cap4` case the old text left undefined, via the dualism tripwire).
2. Direction 3 relies on single-counting within a binding budget. If a future
   mechanism×curriculum interaction makes forced hypotheses ADDITIVE (a stage
   inflated without 1:1 displacement), the within-run comparison breaks again —
   forward falsifier F2, escalate to Direction 2 (budget separation).
3. The ~17-proactive crowding-out per firing stage (real gate cost) remains
   telemetry, not a bar input — correct scoping for C7's question
   (teacher-dependence), per the prereg.
4. The redesign takes effect ONLY on Micah's tap (PREREG §7). The §5 FAIL
   stands as the C5-redesign S10's verdict under the preregistered metric.
   S100 stays gated until: tap + K1–K6 pass (done) + record preserved (done).

---
*Raw logs: `evidence_3plus1/runA/`, `evidence_3plus1/runB/`. Reproduce:
`impl/run_3plus1.sh <src> <out>` then `impl/check_c7_3plus1.py <runA> <runB>`.*
