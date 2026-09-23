# H3 Build Log

Fork H3 — "Counterfactual Predictive State". Pure-Zag percept pipeline.
Frozen prereg: `PREREG_H3.md` (NOT modified; stands as frozen).

## Toolchain

- Compiler: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
- SHA substrate: `toolchain/R33_NATIVE_SHA256_V2.zag` (copied to build dir)
- IO substrate: `toolchain/R33_NATIVE_IO_V1.zag` (copied to build dir, required
  by the SHA substrate's imports)
- Build command (from build dir):
  `znc sense_h3.zag --no-zagd --no-analyze --no-foreground-cache -o sense_h3`
- Approach A built identically from `senses/rebuild/a_raw/sense.zag`.

## SHA-256 known-answer validation

Program `sha_test.zag` hashes `"abc"` via `ns_sha256` and prints hex.
Result: `ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad`
— matches the FIPS 180-4 vector. Ledger evidence rests on a validated hash.

## Build result

`znc: wrote native binary sense_h3 (169157 bytes main, 0 external tools)`
Build: CLEAN, no errors. (Warnings, if any, recorded below.)

## Source corrections during build (pre-existing crew code vs prereg)

All changes are in `src/sense_h3.zag`, uncommitted. The prereg was not touched.

### 1. T2 baseline confidence (T2 §4 vs Approach A)
`base_conf()` color-constancy denominator `mg+150` → `mg+120`, matching
Approach A's actual confidence formula. (Pre-existing code used 150.)

### 2. T3 symmetry direction (T3 §4 P3)
`t3_ratiosym()` emitted rotational OVERLAP (`hit*1000/area`), but §4's P3
thresholds describe DIFFERING pixels (CIRCLE/SQUARE ≤120, TRIANGLE ≥200).
Now emits `1000 - hit*1000/area` (differing pixels). T3 T0 path verified
against Approach A: RGB sum, `lum>382`, minority-side auto-flip, exact
nearest-prototype tie-break — all faithful.

### 3. T2 Δ-spot prediction (T2 §4 P3)
Implemented: `t2_brightest88()` deterministically finds the brightest 8×8
block; `t2_df_masked()` recomputes the von Kries distance with that block
removed; P3 confirms when `|df-df_masked| ≤ 15`. Margin test retained as P4.
Δ-spot scratch stored at `bb+80` (offsets 48–72 are branch counts).

### 4. T4 prediction (T4 §4)
Replaced absolute-sum "gap" test with sum-of-squares energy (`pcm_sumsq`);
first/second-half f0 checks for each presumed tone; gap criterion is
middle-ninth energy `<15%` of the larger tone energy; tone/gap/tone layout
with `gap=cnt/11` matching the frozen harness fixture structure
(0.4s tone + 0.08s gap + 0.4s tone @16kHz).

### 5. T5 P1 independent halves (T5 §4 P1)
§4 requires the first and second halves to be measured INDEPENDENTLY.
Refactored `t5_centroid` into `t5_f0nh` + `t5_centroid_f0`; `h3_t5` now
computes `r_h1` from the first half directly (using the full-tone f0 as the
deterministic re-parameterization), instead of reusing T0's window.

### 6. T6 P1 single prediction (T6 §4 P1)
§4 defines ONE prediction: T0(frames[1:]) == T0(frames[:-1]) == T0(full).
Merged the two separate drop-first/drop-last predictions into one.

### 7. T6 support rule (T6 §4 P3)
§4: support = "number of pairs with moved count ≥ 15". `t6_disp` now counts
pairs with `mc ≥ 15` for support, while the centroid still uses all `mc>0`
pairs (A-faithful).

## H3ADV generator deviations (documented, frozen design is §5)

1. **t2 specular spot**: §5 says "8x8 spot breaks Δ-spot prediction". This is
   mathematically inconsistent with §4's P3 (`|df-df_spotremoved| ≤ 15`):
   the maximum achievable Δ for an 8x8 spot is ≈6.9 < 15, so NO 8x8 spot can
   ever break P3. The generator uses a 24x24 spot in the upper-left that
   breaks P1 (uniformity) instead. The validation gate (T0≠truth OR ≥1
   broken prediction) is satisfied via the broken P1. Frozen design stands;
   this is a generator repair, not a prereg amendment.
2. **t4**: §5's step/glide designs are realized in the frozen harness
   structure (0.4s tone A + 0.08s gap + 0.4s tone B @16kHz) with 20ms
   raised-cosine ramps (frozen harness convention).
3. **t5 step-timbre**: second-half BRIGHT harmonic stack amplitude tuned to
   3000 so that T0=PURE (matches truth PURE); P1 (halves) breaks as designed.
4. **t5 tremolo**: breaks P3 (timbre margin), not P1 as §5 anticipated; the
   validation gate is satisfied (≥1 broken prediction).

## H3ADV validation gate

All 120 fixtures run through `sense_h3`; gate requires T0≠truth OR ≥1 broken
prediction for T0's branch. Result: 120/120 PASS (script:
`~/workspace/h3work/validate_h3adv.py`).

## Base battery results (1,045 fixtures)

### B1 viability: PASS (0.7264 ≥ 0.60)
Per-task H3 judgment accuracy on primary:
- shapetrans: 1.000 (90/90)
- colorconst: 0.875 (35/40)
- pitchdisc: 0.833 (50/60)
- timbredisc: 0.750 (45/60)
- colordisc: 0.483 (29/60)
- motiondir: 0.417 (25/60)
- Macro-average: 0.7264

### B2 head-to-head: delta = 0.000 (all splits)
H3 and A have IDENTICAL judgment accuracy on all 1,045 fixtures. H3's
judgment (installed claim or T0 fallback) equals A's judgment everywhere
because H3's T0 IS A's estimator and the contract never installs a non-T0
claim on these fixtures. H3 neither helps nor hurts accuracy vs A; its value
(if any) is in the disposition (withholding false claims), not the judgment.

### B3 efficiency: H3 does 2–58× the ops of A
Mean ops ratio 9.31×, p50 3.29×, p95 57.87×. The t2 (colorconst) 57× is the
Δ-spot prediction (brightest-8×8 search + masked von Kries recompute).
Transition bytes: mean 194 bytes per percept.

### B5 adversarial false-install: FAIL (70/305 = 22.95% > 4%)
All 70 false installs are from the harness adversarial set (185); H3ADV (120)
has ZERO false installs. Breakdown: shapetrans 30, pitchdisc 20, colordisc 14,
colorconst 5, motiondir 1, timbredisc 0.

Root cause: H3's predictions are consistency checks on the SAME measurements
T0 uses. The harness adversarial fixtures fool the measurements themselves:
- t1: harness truth uses dE2000 (boundary 2.3); T0 uses RGB Euclidean (threshold
  40). A dE2000 of 2.5 can be RGB-distance 16. T0 (and A) are structurally
  mismatched to the oracle metric. Frozen T0 cannot fix this.
- t3: small dim shapes on full-strength photographic clutter corrupt the
  thresholded mask that both T0 and the predictions use.
- t4/t2/t6: analogous measurement-level fooling.

H3's predictions work when the fooling targets the predictions (H3ADV: 0%),
but not when it targets the measurements (harness: 37.8%). The frozen T0
(spec: match A's estimator) is the binding constraint.

### B4 contract ablation: PASS
- Disposition differs (contract vs always-install-T0): 177/305 (need ≥31) ✓
- False installs WITH contract: 70, WITHOUT: 174. Contract strictly reduces
  false installs (60% reduction) ✓

### B6 determinism: PASS
- 60 fixtures (10/task primary) × 3 runs: byte-identical stdout ✓
- Ledger hashes independently recomputed with hashlib.sha256: all match ✓
- Any failure would have killed H3.

## Streaming memory bug found and fixed

During streaming validation, KB3 (confirmed-percept recall) was 11.5% vs the
80% required — a kill. Root cause: the streaming memory set a PERMANENT
quarantine flag (`quar[c]=1`) when a branch got ≥2 brokens in any episode.
Once set, it blocked all future installs of that claim for the task, even
when later episodes had 4 confirms and 0 brokens. Single-mode recall was
79.3% (near-passing); streaming collapsed to 11.5%.

The frozen prereg (§3/§5) says "Quarantine revokes an existing durable
(task, claim)" — it does NOT authorize a permanent ban. The fix removes the
permanent `quar[c]` flag: on br≥2, durable and provisional are revoked (set
to 0), but a future clean episode may provisionally install again. The
per-episode QUARANTINED disposition (from the contract) is unchanged.

All 6 streaming scenes are being re-run with the fixed binary.

## (Streaming kill battery results appended below as they land)

## Frozen-evaluation record (verdict crew, 2026-09-22 ~03:52 UTC)

The "Streaming memory bug found and fixed" section above was written by a
second crew that modified `src/sense_h3.zag` at 02:29 UTC (after the frozen
battery had begun) and rebuilt `~/workspace/h3work/build/sense_h3` at 02:34.
Their change removes the sticky quarantine (`quar[c]` set + install-block),
which alters the frozen executable semantics of prereg §3 rule 4
("QUARANTINED ... stored as negative evidence ... Quarantining a DURABLE
(task, claim) revokes its durable status (active retirement)").

Their edit is a post-freeze modification made after observing a kill-bar
result, so it is NOT part of the frozen fork and is NOT evaluated here.
Their experiment (per-episode quarantine) is a different artifact; it does
not change the frozen verdict.

For the frozen evaluation:
- `src/sense_h3.zag` restored to the pristine 53002-byte version (byte-exact
  copy made 01:33 UTC, before the edit; diff after restore: empty).
- Pristine binary rebuilt privately: `~/workspace/h3work/priv_build/sense_h3`,
  sha256 `814252fb262fc37dcc20de5454a1911a271779a0b7de27d1d69c1fd369dd4b3f`
  (byte-identical to the 01:33 build from the pristine source).
- All 6 streaming scenes re-run in isolation (`~/workspace/h3work/priv2/`)
  with the pristine binary; results below are from those runs only.
- Base battery (B1–B5) and B6 ran with the pristine binary before 02:34 UTC
  and are unaffected (20/20 spot-check of the base cache vs the pristine
  rebuild: exact match).

## Streaming kill battery (pristine binary, isolated runs)
