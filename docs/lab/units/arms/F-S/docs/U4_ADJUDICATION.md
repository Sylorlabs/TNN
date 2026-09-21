# U4 Adjudication — Arm F-S (Markov-surprise cuts), Track A closeout

**Date:** 2026-09-21 (~11:30 PDT)
**Arm:** F-S — Markov-surprise cuts (CUT family)
**Adjudicated by:** MARATHON CREW U4
**Status: COMPLETE EXCEPT KILL (iii)** — kills (i) and (ii) independently
verified do-not-fire; M8 verified PASS; kill (iii) blocked on D's M3
(T3's pending deliverable). This document supersedes the gap-fill
PROVISIONAL verdict on all points except kill (iii), which is unchanged.

## Frozen kill bars (verbatim, §3 of `units/PREREG_FREEZE.md` line 482, extracted programmatically)

```
$ sed -n '482p' units/PREREG_FREEZE.md
| F-S — Markov-surprise cuts | CUT | Deterministic order-2 byte Markov predictor; cuts at confident-miss positions (predicted≠actual, count≥CONF_BAR), local-maximum within ±W, ≥MIN_GAP apart; chunks = spans between cuts (just code 4); cut must recur (rep≥2) before commit — surprise proposes, it does not mint. | Any one: (i) Shakespeare boundary F1-agreement with C-W within ±0.05 AND M3 ≤ C-W's — rediscovers whitespace at 67MB cost; (ii) code cut count > 5× C-W's (cut storm); (iii) loses to D on M3 both corpora. |
```

Kill criterion column: **"Any one: (i) Shakespeare boundary F1-agreement
with C-W within ±0.05 AND M3 ≤ C-W's — rediscovers whitespace at 67MB cost;
(ii) code cut count > 5× C-W's (cut storm); (iii) loses to D on M3 both
corpora."**

Note: the table header marks these kill criteria "(binding, PROPOSED)";
the Track A closeout treats them as binding per §0 RULE-7 (no Micah
amendment to F-S's bars exists in the frozen text).

## Kill-bar evaluation (independent, from raw evidence)

### Kill (i) — Shakespeare F1-agreement within ±0.05 (of 1.0) AND M3 ≤ C-W's — DOES NOT FIRE

- F-S prose: 210 committed cuts (211 chunks) — `docs/scorecard_r1_1x.json`
  diagnostics `prose_committed: 210`; corroborated by BUILD_LOG ("Prose
  (5,422,721 bytes): 93,439 fired, 210 committed, 211 chunks").
- C-W prose: 1,926,955 cuts (1,926,956 units − 1) — from
  `units/arms/C-W/logs/scorecard_r1_1x.json` `m1.prose.units = 1926956`.
- Maximum possible F1 (every F-S cut coinciding with a C-W cut):
  precision = 210/210 = 1.0; recall = 210/1,926,955 ≈ 0.00010898;
  F1 = 2·1·0.00010898 / 1.00010898 ≈ **0.000218**.
- 0.000218 is not within ±0.05 of 1.0 (requires ≥ 0.95).
- First AND-condition FALSE → the AND fails → **kill (i) does NOT fire**.
- Second condition recorded for the file: F-S M3 survival 100.0, fresh
  recall 100.0; C-W M3 survival 100.0, fresh recall 100.0 → "M3 ≤ C-W's"
  would be TRUE, but it is moot.

### Kill (ii) — code cut count > 5× C-W's (cut storm) — DOES NOT FIRE

- F-S code: 17,155 committed cuts (17,156 chunks) — scorecard diagnostics
  `code_committed: 17155`; corroborated by BUILD_LOG ("Code (9,515,341
  bytes): 146,239 fired, 17,155 committed, 17,156 chunks").
- C-W code: 2,446,767 cuts (2,446,768 units − 1) — C-W scorecard
  `m1.code.units = 2446768`.
- Threshold: 5 × 2,446,767 = 12,233,835. 17,155 > 12,233,835? **FALSE.**
- **Kill (ii) does NOT fire.** F-S cuts ~143× *less* than C-W on code, not more.

### Kill (iii) — loses to D on M3 both corpora — BLOCKED ON D'S M3

- F-S M3 (`m3-1x`, single combined battery: ingest prose+code, 1,000 pinned
  valuable, 3,000 fresh ingests, 3,000 kills, 50 weakens, 4,000 fresh
  ingests): **survival 100.0, fresh_recall 100.0, weaken 50/50, freeze 0**,
  9,050 management entries. Raw log `work/m3_run1.txt` byte-identical to
  `m3_run2.txt` (diff-verified).
- Frozen M3 definition (§5): headline = survival rate of the 1,000-unit
  valuable set (bars ≥ 90%; champion ≥ 95%); freeze flag CLEAR/FROZEN.
- **No official D M3 exists.** D's local verdict (`units/arms/D/VERDICT.md`)
  is DRAFT with M3 pending; D's battery is blocked by 5 conformance
  blockers (CONFORMANCE_BLOCKERS.md). Branch `tnn-native-lab` at HEAD
  `6d109ef5` (2026-09-21 18:03 UTC) contains only
  `docs/lab/units/arms/D/{BUILD_LOG.md, cl/arm.zag}` — no VERDICT.md, no
  scorecard (verified via full branch tree, 44,515 paths).
- **Exact evidence pointer (pending deliverable):** crew **T3 —
  D-FAMILY COMPLETION** (per NIGHT_RUN_2026-09-21.md: "D/D-T/D-R full
  scorecards + M8 + verdicts, kill bars binding"). Expected commit to
  `sylorlabs/TNN` branch `tnn-native-lab` adding
  `docs/lab/units/arms/D/VERDICT.md` + `docs/lab/units/arms/D/scorecard_r1_1x.json`
  with official M3 values.
- **Resolution rule (mechanical, to be applied when T3 lands):** let
  D_prose, D_code = D's M3 survival rates per corpus from T3's committed
  scorecard. Kill (iii) FIRES iff F-S survival (100.0) is strictly below
  D's on BOTH corpora. (F-S's M3 is a single combined battery, so the same
  F-S value compares against both D per-corpus values.) No judgment call —
  run the inequality, document the numbers.

## Full scorecard (1x, from `docs/scorecard_r1_1x.json`, schema metrics-v1)

| Mode | Result |
|---|---|
| M1 prose | 211 units, recall 100.0, boundary 100.0 |
| M1 code | 17,156 units, recall 100.0, boundary 100.0 |
| M2 t1/t2 (prose+code), t3 | ETC=1, 100/100 all |
| M3 | survival 100.0, fresh 100.0, weaken 50/50, freeze 0 |
| M4 prose+code | 100/100 both |
| M5 | PROVISIONAL structural accounting (ledger 11.37MB / 177,585 entries) |
| M6 p2c + c2p | transfer tax 0.0 both directions |
| M7 | lookup 100.0, reuse 2.0, dedup 50.0 (A7/A8 PROVISIONAL) |
| M8 | PASS — see verification below |
| M9 | implicit: mean/range of per-episode M2 content recall = 100.0/100.0 |

Battery status: complete. Every mode run twice; stdout byte-identical
(diff-verified per run pair in `work/`).

## M8 verification (U4, independent)

- Run-log pairs diff-verified byte-identical: clean, frag, aslr, freelist
  (local); starve r2 recovered from the branch blob and verified
  byte-identical to starve r1. **All 5 perturbations × 2 runs: PASS,
  m1p/m1c/m3 all 100.0.**
- `work/m8_artifact_hashes.txt`: ledger.bin, ledger_chain.txt,
  store_chain.txt, store_hashes.txt hashes **identical across all 10 runs**
  (clean/frag/aslr/starve/freelist × r1/r2) — byte-identical artifacts
  under perturbation.
- Caveat: the raw artifact dirs (`clean/r1/` etc.) were not retained
  locally; the hashes file is the surviving artifact evidence (binaries are
  correctly not committed). The hashes corroborate the scorecard's
  "all byte-identical to clean" note.
- **M8: VERIFIED PASS.**

## Ambiguities / provisional items (carried, unchanged)

- CONF_BAR=16, W=8, MIN_GAP=32: sweep-tested (7 configs; CONF_BAR inert,
  W strong: 4→414, 8→155, 16→46 units), not frozen.
- M5, M7-A7/A8, M8-perturbation semantics: provisional per ARM_SPEC §7.
- M9 not a separate scorecard mode (implicit from M2 episodes).

## Verdict

**F-S: PROVISIONAL — complete except kill (iii).** Kills (i) and (ii)
independently verified do-not-fire from the frozen text and raw evidence.
M8 verified PASS. Kill (iii) cannot be evaluated until T3's D-family
deliverable lands (`docs/lab/units/arms/D/VERDICT.md` +
`docs/lab/units/arms/D/scorecard_r1_1x.json` on `tnn-native-lab`); the
mechanical resolution rule above applies with no judgment call. When D's
M3 is committed, any crew re-runs the inequality and upgrades this
document to BINDING.

Diagnostic (unchanged): F-S's recurrence gate is extremely conservative
(prose commit rate 0.22%), producing few very large chunks (mean ~25KB on
prose) vs C-W's 1.9M word-like tokens — a section-champion (§7) ranking
question, not a kill question.

---
Pure Zag; no RNG in decision paths; byte-identical reruns (N=2 per mode,
diff-verified; N=5 not run — prior crew's battery). znc quirks ZNC-002..012
respected (no new builds; verification only). No binaries / `.zagd` /
`.zag-cache` touched.
