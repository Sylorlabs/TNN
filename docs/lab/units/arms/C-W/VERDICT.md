# C-W — Verdict (r1, 1x)

## Verdict

**VERDICT: PASS** (1x)

No binding kill criterion fired; no disqualifying event occurred. Every leg
ran twice with byte-identical stdout (rc=0); the M8 gate additionally
requires byte-identical artifacts across 5 perturbations × 2 reruns.

## Binding criteria checked

- Frozen cross-arm criterion ("a smart arm beats C-W ≥2x on M3 and M2 at
  equal M1 both corpora → C-W retires; [REV] if no smart arm beats C-W on
  Shakespeare by end of 10x, every smart arm is killed"): **cannot be settled
  by this crew alone** — no cross-arm evidence is in scope. Referred to the
  Track A coordinator.
- M3 freeze tripwire: `CLEAR` (not fired).
- M4 kill-substitution: `false` (not fired).
- M2 censor: none (`m2_censored: false`, ETC=1 on all tiers).

## Bars (prereg)

| metric | value | bar | status |
|---|---|---|---|
| M1 prose recall / boundary | 100.0 / 100.0 | — | pass |
| M1 code recall / boundary | 100.0 / 100.0 | — | pass |
| M2 ETC (t1-prose, t1-code, t2-prose, t2-code, t3) | 1 / 1 / 1 / 1 / 1 | — | pass |
| M2 final recall / boundary (all tiers) | 100.0 / 100.0 | — | pass |
| M3 survival | 100.0 | ≥ 90.0 | pass |
| M3 fresh recall | 100.0 | ≥ 80.0 | pass |
| M3 mgmt entries | 8050 | ≥ 700 | pass |
| M3 freeze | CLEAR | — | pass |
| M4 rev boundary / content (prose, code) | 100.0 / 100.0 | — | pass |
| M4 kill rate | 0.0 | — | pass |
| M5 units/KB | ~363.9 | ≥ 3.0 | pass |
| M5 memory / source byte | 16.481 | ≤ 1.5 (proposed) | **MISS** (see note) |
| M5 audit entries/KB | 364.1 | ≤ 10 (proposed) | **MISS** (see note) |
| M6 transfer (p2c, c2p): rec/bnd/rev | 100.0 / 100.0 / 100.0 | — | pass |
| M6 transfer tax | 0.0 | — | pass |
| M7 | non-ID (`m7_reread_bytes` = 14070, independently verified) | — | pass |
| M8 gate | **PASS** — `M8GATE COMPLETE rc=0`; 5 perturbations × 2 reruns, all byte-identical | byte-identical ×10 | pass |

**M5 efficiency notes:** both M5 bars (≤1.5x memory, ≤10 audit/KB) are
*proposed* bars per METRICS.md ("Micah signs the exact numbers") — they are
not binding kill criteria, and C-W is a control arm whose frozen
retirement criterion is exclusively the ≥2x-beaten-by-a-smart-arm rule.
The misses are priced information about the per-chunk `ADD_UNIT` design
(AMBIGUITIES-CW.md A1): 1,927,956 entries / 5,295 KB ≈ 364/KB; the bulk-
`SCAN_COMMIT` alternative would score ~0 but make C-W non-comparable with
the B-64 control (which also misses its audit bar at 16.2/KB). This is
priced information about the confound, not a defect.

## 10x status

**10x: NOT ATTEMPTED — structural blocker (proven, not guessed).**

The r10 corpora are exact 10× tilings (verified: r10 prose = 54,227,210 bytes
= 10 × 5,422,721, byte-identical tiling). Chunk counts scale linearly, so the
10x ledger demand is:

| mode | 10x ledger entries needed | cap |
|---|---|---|
| M1 prose | 19,269,560 | 8,000,000 |
| M1 code | 24,467,680 | 8,000,000 |
| M8 | 43,749,290 | 8,000,000 |

The ledger cap is 16 shards × 500,000 entries = 8,000,000 (512 MB), a hard
`LEDGER-BOUND` trip in code. Every one of these modes would trip it. Raising
the cap to ~96 shards (3 GB heap) is a redesign of the arm's 10x resource
profile, not a build note — referred to the Track A coordinator. Note the
frozen [REV] criterion ("if no smart arm beats C-W on Shakespeare by end of
10x, every smart arm is killed") needs C-W 10x numbers; this blocker applies
to that comparison and must be resolved at program level.

**Second 10x blocker — 24-bit chunk-index field.** Chunk IDs are
`(corpus << 24) | chunk_index`; the index field holds at most 16,777,216
values. Tenfold prose needs 19,269,560 chunk indices and tenfold code needs
24,467,680 — both overflow the field. Widening the ID layout changes the
arm's on-disk identity scheme and is a redesign, not a build note — referred
to the Track A coordinator alongside the ledger cap.

## Evidence

- `scorecard_r1_1x.json` (top-level `arm` corrected to `"cw"`; see A6)
- `logs/` — per-leg STATUS.txt, fragment.jsonl, stdout excerpts, M8 GATE.txt
- `BUILD_LOG.md`, `ARM_SPEC.md`, `AMBIGUITIES-CW.md`
- Implementation: `units/arms/C-W/cl/arm.zag`,
  `units/arms/C-W/substrate/R33_NATIVE_IO_V1.zag`,
  `units/arms/C-W/substrate/R33_NATIVE_SHA256_V2.zag`

Binaries (`cw_bin`, `mem_bin`), `.zagd.semantic-ready`, `.zag-cache/`,
corpora, and M8 `ledger.bin` files are excluded from the repo by rule.
