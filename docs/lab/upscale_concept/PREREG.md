# PREREG — Upscale concept probe → teach → re-probe (AS-RUN)

**Frozen:** 2026-09-26. **Task:** determine whether TNN *holds* the upscale concept
C1–C4 behaviorally (not recited), via probe → teach → re-probe.
**Branch:** `tnn-native-lab` only. Pure Zag, zero RNG, byte-identical reruns.

## The concept

- **F1 (C1):** 2x means 4x the pixels — output dims exactly (2w, 2h).
- **F2 (C2a):** same content, same alignment — the alignment peak is at (0,0); no shifting.
- **F3 (C2b):** no new objects — after best-offset alignment, mean abs residual ≤ 2.0 levels.
- **F4 (C3/C4):** new detail only from knowledge, never invented; no pixel depends on an
  invented term — HF ratio HF(U)/HF(L) ≤ T (T taught; exploratory T0 = 2.0 for probe-before).

C4's full pixel-value line test (pixel == f(measured terms) exactly) is enforced on TNN's
own future constructions; the probe verifies its detectable consequences (M2b+M3).
This limitation is recorded, not hidden.

## Measurements (all computed by `uprobe_bin`; integer math, ×1000 fixed point)

- **M1:** dims(U) == (2w, 2h) → 1/0.
- **M2a:** D = 2×2 box-downscale(U) → w×h; SAD(D shifted by (dx,dy), L) over
  dx,dy ∈ {−2..+2}; report argmin offset (px,py) and uniqueness.
  (0,0) must be the strictly unique best.
- **M2b:** R = mean abs diff between D (at found peak) and L, in levels×1000.
- **M3:** HF = mean |adjacent diff| (right+down neighbors, luma) in levels×1000;
  Q = HF(U)×1000 / HF(L).

**Symmetry fix (exploratory finding, applied before teach):** the first synthetic
fixtures had exact translational symmetries (checkerboard periods + hash grain
conspired to SAD-tie at multiple offsets), making M2a ambiguous. Fix: every
synthetic image carries a gentle non-periodic gradient (+x//2) that breaks all
shifts in the search range. This is a fixture-design correction, not a bar change.

## Bars

- **Probe-before (exploratory, non-binding):** F1: M1==1. F2: (px,py)==(0,0) unique.
  F3: R ≤ 2000. F4: Q ≤ 2000. Purpose: baseline discriminability only.
  Bars shipped in `prereg_bars/exploratory_bars.bin` (on,on,on,on / 2000 / 2000).
- **Teach (binding commit gates, unanimous over the 4 teaching pairs):**
  F1: all pairs exact 2x → commit (exact). F2: all pairs peak (0,0) unique → commit.
  F3: all pairs R ≤ 2000 → commit bar 2000 (white-box: 2×2 box-average rounding bound).
  F4: all pairs Q ≤ 4000 (sanity ceiling) → commit bar T = 2 × max_pair_Q (measured,
  2x headroom over the worst true-detail case). Any pair failing a feature → REVERT it.
- **Probe-after (binding):** bars from the committed concept knowmap, on held-out cases
  (different images AND different violator parameters).

## Fixtures (sealed + SHA-256 manifest)

- `fixtures/teach/pair{0..3}/`: 32×32 low + 64×64 high true pairs
  (checker, circles, stripes+grain, blocks).
- `fixtures/probe_before/case{0..3}/`: teach images; violator set A, per-case:
  shifts (2,0)/(0,2)/(−2,0)/(0,−2) px; squares 12/12/16/10 px; invent amp 60,
  zero-mean per 2×2 block (targets F4 only).
- `fixtures/probe_after/case{0..3}/`: HELD-OUT (2 new synthetics + 1 hash-grain +
  1 real 64×64 crop of stage/gt_512x184.bmp); violator set B, per-case:
  shifts (0,2)/(2,0)/(0,−2)/(−2,0) px; squares 12/16/12/10 px; invent amp 50,
  zero-mean per 2×2 block.
- Each case: `low.ppm, correct.ppm, v_shift.ppm, v_invent.ppm, v_object.ppm,
  v_dims.ppm` (v_dims = 60×64 crop).

## HELD criterion and gate

Per feature: HELD iff the correct candidate is ACCEPTed and every violator REJECTed
on every held-out case. **Concept HELD iff every committed feature is HELD on all
held-out cases. Gate PASSES iff concept HELD.** A reverted feature cannot be tested
→ gate fails for the full concept; partial-held is reported honestly, never rounded up.

## Anti-leading

Candidates are anonymous files; the binary applies committed bars only. Teaching
input is image pairs — no crew-authored concept text; TNN demonstrates, not recites.
Violator amplitudes were set to be unambiguous instances of each violation; all bars
were taught from true-pair measurements only (causal order documented in RUNLOG.md).

## Trace types (documented in every trace)

- `[MEASURED]` — numbers computed live by the binary.
- `[RULE]` — predicate-guarded fixed wording with live numbers.
- `[DELIB]` — the commit/revert and accept/reject *selections*: computed from
  measurements (the selection is generated; the sentence template is fixed).
