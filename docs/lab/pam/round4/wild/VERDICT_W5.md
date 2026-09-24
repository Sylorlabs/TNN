# VERDICT W5 — PAM-as-memory (third generation)

Evidence commit: `075eac896816aad04b6ba2e2c3f7c0e7ae42fc88`
(prereg `wild/prereg/PREREG_W5.md` + `wild/prereg/PREREG_AMEND1.md`, frozen;
comparator bar frozen at `(705, 3588, 0, 0)`.)

## Observed numbers (instrument + independent mirror agree exactly)

- Phase A: rows=2241, hits=2035, misses=206, store=206, maxprobe=22
- Hit-mismatches (stored decision != recompute): **27 / 2035 hits (1.33%)**
- Phase B: 2 distinct W signatures poisoned to (ADMIT, 9); **2 ELIM**
  (both old_strength=9); post-reject **12/12**
- Phase C: 1 signature re-poisoned to (ADMIT, 255); **1 ELIM**
  (old_strength=255); post-reject **1/1**
- Instruments: kb_w5_m=1, kb_w5_e=0, kb_w5_k1=0
- Battery: 2x byte-identical,
  SHA-256 `0e630c0cd85cb53883e2fae1aeee5a577215d89af3b3e30326522110fcd1a4ee`
- D-W5-1 hit rate: 2035/2241 = 90.81%
- Correct admits from memory: 892/910 = 98.02% (>=95% bar met)

## Two prereg miscounts found (documented, mechanism honored)

1. "Distinct signatures over the tape are < 1000": true count is **206**
   (an early mirror said 207 due to a P-row field-mapping slip; corrected).
2. "Poison the 12 W signatures ... 12 ELIM log lines": the frozen
   quantization `(conf//50, mrgF//500, strong, agree)` yields only **2
   distinct W signatures** — `(15,3,1,1)` and `(16,4,1,1)`. The battery was
   run per the frozen *mechanism* (every poisoned entry eliminated):
   2 poison -> 2 ELIM -> 12/12 W rows post-reject. The "12 ELIM lines"
   prediction was an arithmetic miscount in the prereg, not a mechanism
   deviation; KB-W5-E's intent (elimination unconditional on strength) is
   fully satisfied.

## Bar evaluation

- F1 (memory == recompute on 100% of rows): **FALSIFIED** — 27 mismatches.
- KB-W5-M: **FIRED** (any hit-mismatch -> KILL). Root cause, confirmed by two
  independent implementations (Zag instrument + Python mirror agree on all
  27): the frozen quantization buckets **straddle the frozen bar's decision
  boundary** — conf bucket 14 = [700,750) contains the 705 threshold; mrgF
  bucket 7 = [3500,4000) contains the 3588 threshold. One memory per
  signature cannot serve trials on opposite sides of the bar. This is a
  **design flaw, not an implementation defect** (the prereg's "a mismatch is
  an implementation defect" is itself wrong).
  - 14 cases: sig (14,7,1,1), memory REJECT vs recompute ADMIT (missed admits)
  - 11 cases: sigs (14,14,*,1), conf straddling 705 both directions
  - 2 cases: B rows (diagnostic only)
  - Consequence: 1 genuine memory-induced wrong admit in Phase A —
    P-row (704,6603): memory ADMIT, bar REJECT. (The other 2 Phase-A
    wrong-set admits, (718,6600) x2, agree with the bar — the M1 bar itself
    admits that row; the pair still fails via its partner.)
- KB-W5-E: pass (every elimination unconditional on strength, incl. 255).
- K1 (scoped by prereg to post-elimination answers): PASS — 12/12 W
  re-queries REJECT, Phase C 1/1 REJECT; no poisoned entry survived.
- K2: PASS (2x byte-identical). K3: 98.02% >= 95% on the number, but the
  "no wrong admits" clause is violated by the (704,6603) case above.
- F2 (elimination beats promotion): intent VERIFIED — 2/2 at strength 9,
  1/1 at strength 255, zero survivors.

## Status: KILL (KB-W5-M)

The design as frozen cannot meet its own fidelity bar: no faithful
implementation of the frozen quantization + frozen bar can achieve F1's
100%, because the buckets straddle the bar. The elimination machinery
itself works exactly as designed. Redesign direction: the quantization
must respect the bar boundary (bar-aligned buckets), or the bar must be
expressed in quantized units — either way the identity function and the
decision boundary must be co-designed, not frozen independently.

## Numeric-cap classification (standing law: no arbitrary hard limits)

- Store capacity 4096 (existence of a bound): LOAD-BEARING as mechanism
  (open addressing needs a bound); the VALUE 4096 is ARBITRARY calibration
  (206 used) -> FLAGGED for removal (growable structure).
- Strength cap 255: ARBITRARY (u8 convenience) -> FLAGGED for removal.
- Quantization widths 50/500: the EXISTENCE of a signature quantization is
  load-bearing (it is the design's identity function), but the specific
  widths are ARBITRARY — and worse, misaligned with the bar, which is the
  kill cause -> FLAGGED; widths must be derived from the bar, not constants.
