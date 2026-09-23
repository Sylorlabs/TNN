# VERDICT.md — morphology crew

## Kill-bar scorecard

| Bar | Requirement | Result |
|---|---|---|
| KB-M1 (reproduction) | mirror reproduces the exact miss via the documented stage | **PASS** — `mirror.py` reproduces `Andy Weir wrote The Martian.` with stage-pinned scores (2/12 vs 0/12) |
| KB-M2 (morphology battery) | ≥95% of scored probes post-fix | **PASS** — 13/13 = 100% (S02–S14) |
| KB-M3 (no regressions) | full battery ≥369/370 AND WE-09 turn 1 passes | **PASS** — **370/370**, WE-09 turn 1 passes, zero regressions |
| KB-M4 (determinism) | 5/5 byte-identical | **PASS** — digest `35aaae8a…99834474b` ×5 |
| KB-M5 (symmetry) | repair identical at index and query time | **PASS** — single code path in `proc_token`; compose branch reuses frozen relation primitives |

## Full dialogue battery, post-fix (5 runs)

| Section | Score |
|---|---|
| FOLLOWUP | 45/45 |
| CORRECTION | 45/45 |
| REFERENT | 60/60 |
| WEIRD | **30/30** (was 29/30) |
| WEIRD_CLEAN | 30/30 |
| TOPIC | 60/60 |
| CONTRADICT | 72/72 |
| COMPOSE | 28/28 |
| **Total** | **370/370 = 100%** |

WE-09 turn 1 now answers `Andy Weir was born in 1972.` (was the battery's
only miss).

## Honest notes

1. **The verdict's root cause was incomplete.** "The keyword core cannot
   bridge birth year → born" was true but insufficient: the bridge alone
   leaves the WROTE fact winning 2/12 vs 1/12 (and would tie-break to the
   wrong person). WE-09 was a morphology gap stacked on a composition
   gap. Both are now fixed; the finding is documented in REPRO.md.
2. **The write family was tried and reverted.** Bridging wrote/written/
   writing caused 37 regressions by collapsing the KB's active/passive
   distinction. The table ships without it; C04 documents the boundary.
3. **Derivational and synonym gaps remain** (high/tall, penned/wrote):
   characterized, out of scope, consistent with the independent-battery
   finding on synonym swaps.
4. One analyzer warning class pre-existed; the build is clean of errors.

## Artifacts

- `PREREG.md` (frozen), `REPRO.md`, `FIX.md`, `MORPH_BATTERY.md`,
  `morph_battery.txt`, `mirror.py`, `table_check.log`
- `full_1..5.log` — 370/370 ×5, digest `35aaae8a…`
- `pre_morph.log` / `post_morph.log` — morphology battery before/after
- Patched source: `~/workspace/tnn-lab/dialogue/dialogue.zag`
- Addendum appended to `docs/lab/dialogue/VERDICT.md` (repo)
