# VERDICT — Arm F-S (Markov-surprise cuts), Track A closeout

**Date:** 2026-09-21
**Arm:** F-S — Markov-surprise cuts (CUT family)
**Adjudicated by:** verdict gap-fill crew (Track A closeout)
**Verdict: PROVISIONAL** — kill (iii) blocked on D's verdict (see below)

## Frozen kill criterion (verbatim, §3 of `units/PREREG_FREEZE.md`, extracted programmatically)

> Any one: (i) Shakespeare boundary F1-agreement with C-W within ±0.05 AND M3 ≤ C-W's — rediscovers whitespace at 67MB cost; (ii) code cut count > 5× C-W's (cut storm); (iii) loses to D on M3 both corpora.

**Correction to the prior draft:** `docs/VERDICT.md` evaluated kill (i)
as "F1-agreement within ±0.05 AND reuse ≤ C-W's". The frozen text's second
condition is **M3 ≤ C-W's**, not reuse. The conclusion is unchanged (the
first condition fails, so the AND fails), but the record is corrected.
The same draft's "SURVIVES" headline is superseded: kill (iii) is
unresolved, so PROVISIONAL is the honest verdict.

## Kill-criterion evaluation

### Kill (i) — Shakespeare F1-agreement with C-W within ±0.05 AND M3 ≤ C-W's

- F-S prose: 210 committed cuts (211 chunks). C-W prose: 1,926,955 cuts.
  Maximum possible F1 (every F-S cut coinciding with a C-W cut):
  precision 1.0, recall 210/1,926,955 ≈ 0.000109 →
  F1 ≈ 0.000218. Actual agreement is ≤ this bound.
- 0.000218 is **not** within ±0.05 of perfect agreement (1.0).
- First condition FALSE → the AND fails → **kill (i) does NOT fire**
  (the M3 ≤ C-W's condition is moot).

The segmentations are fundamentally different: F-S's recurrence gate is
extremely conservative (prose: 93,439 fired → 210 committed, 0.22%; code:
146,239 fired → 17,155 committed, 11.7%), producing few very large chunks
(mean ~25KB on prose); C-W produces 1.9M word-like tokens.

### Kill (ii) — code cut count > 5× C-W's (cut storm)

- F-S code: 17,155 committed cuts. C-W code: 2,446,767 cuts.
  5 × 2,446,767 = 12,233,835. 17,155 > 12,233,835? **FALSE.**
- **Kill (ii) does NOT fire.** F-S cuts far less than C-W, not more.

### Kill (iii) — loses to D on M3 both corpora

- D's results are not available (`units/arms/D/cl/` is empty; no official
  D scorecard located). **UNRESOLVED — blocked on D's verdict.**

## Evidence trail (complete 1x battery)

- Battery: full M1–M9 at 1x, every mode run twice, stdout byte-identical
  (diff-verified); M8 artifacts (ledger.bin, chain files, hashes, alloc
  trace) byte-identical across runs and perturbations.
- M1 recall/boundary 100.0/100.0 both corpora (211 / 17,156 units);
  M2 ETC=1 all; M3 survival 100.0 / fresh 100.0 / weaken 50 / freeze 0;
  M4 100/100 both corpora; M6 transfer tax 0.0; M8 clean/frag/aslr/
  starve/freelist all 100.
- Scorecard (metrics-v1): `docs/scorecard_r1_1x.json`.
- Spec/build: `docs/ARM_SPEC.md` (AMB-FS-007 resolved: recurrence-gate
  reading "span since previous fired cut"), `docs/BUILD_LOG.md`
  (7-config CONF_BAR/W/MIN_GAP sweep per the test-both rule).
- Raw logs: `work/` (m2/m3/m4 run pairs, `battery/`, `fs_test/`).

## Ambiguities (carried)

CONF_BAR=16, W=8, MIN_GAP=32 remain provisional (sweep-tested, not
frozen); M7 edit/schedule provisional; M5/M8 provisional semantics per
ARM_SPEC.md §7.

## Diagnostic note

The extremely low commit rate (especially prose 0.22%) means F-S may not
be competitive as a tokenizer replacement — few, very large chunks. The
section-champion evaluation (frozen §7) will determine F-S's standing vs
other CUT-family arms; that is a ranking question, not a kill question.

**Result: F-S PROVISIONAL — kills (i) and (ii) do not fire; kill (iii)
blocked on D's M3 evidence.**
