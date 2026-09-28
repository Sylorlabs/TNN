# VISION READINESS — KB4 gate test on video percepts (motiondir)

Date 2026-09-22. Frozen prereg: `PREREG_KB4_VIDEO.md` (this dir).
Verdict below is a mechanical application of its §8 bars.

## Verdict: GATED

Vision is **not ready for blind installs**, but there **is** an honest
gate. The method-agreement gate (G-METH) and the full gate (G-ALL) install
**zero** false adversarial percepts on the frozen probe — but they
withhold 91–94% of the stream, so ingestion would install almost
nothing. Per the frozen bars this is GATED, not READY and not NOT READY.

## Headline numbers (layered: gate + shared round-1 memory rule)

90-fixture stream = 30 ADV-R1 adversarial + 60 TEST-FRESH primary motion
clips, rel-sorted (adversarial first), rematch-T4 fitted rule
(STILL iff mag < 1, else octant).

| variant | installs | withholds | withhold % | adv false / adv installs | adv false-install % |
|---|---|---|---|---|---|
| BASELINE (shared rule) | 17 | 73 | 81.1% | 7 / 8 | **87.5%** |
| G-TEMP (2× 4-frame windows agree) | 16 | 74 | 82.2% | 7 / 11 | 63.6% |
| G-SPAT (L/R crops agree) | 8 | 82 | 91.1% | 2 / 4 | 50.0% |
| G-METH (centroid vs block-match agree) | 5 | 85 | 94.4% | 0 / 3 | **0.0%** |
| G-ALL (temporal ∧ spatial ∧ method) | 8 | 82 | 91.1% | 0 / 4 | **0.0%** |

Pure-gate numbers (corroboration only, no memory rule):

| variant | pure installs | pure adv false / installs | pure primary correct |
|---|---|---|---|
| G-TEMP | 46 | 11 / 19 (57.9%) | 16 / 27 (59.3%) |
| G-SPAT | 43 | 8 / 15 (53.3%) | 12 / 28 (42.9%) |
| G-METH | 29 | 0 / 9 (0.0%) | 20 / 20 (100%) |
| G-ALL | 15 | 0 / 6 (0.0%) | 9 / 9 (100%) |

Frozen bar check (READY needs ≤10% AND adv_installs ≥ 5 AND withhold ≤ 90%):
no variant qualifies. G-METH/G-ALL clear 10% on the rate but fail the
non-triviality guards (adv_installs 3/4 < 5; withhold 94.4%/91.1% > 90%).
Prereg §8 GATED clause ("adv_false_install_rate ≤ 10% with withhold_rate
> 90%") matches G-METH and G-ALL exactly → **GATED**.

## Baseline reproduction (prereg §10 validity gate: PASS)

- Overall A/T4 KB4 recomputed from the surviving raw inputs
  (`runs_TEST_FRESH.jsonl` + `runs_ADV_R1.jsonl`): **55/114 = 48.2%** —
  matches the rematch verdict exactly.
- Motiondir stream: **17 installs / 16 total false / 73 withholds** —
  matches the verdict's per-task stream exactly.
- Correction to the task brief: the "~48%" is the ALL-TASK rate. The
  video-only adversarial false-install rate is **87.5% (7/8)** — worse.
  (The brief's phrasing conflated the two; both numbers above are the
  reproducible ones.)
- TEST-FRESH t6 primary fixtures were regenerated from seed 20260923
  with the frozen round-1 generator: 60/60 sha256-verified against
  `rematch/data/TEST_FRESH/MANIFEST.sha256`.

## What the experiment found (mechanism, not just numbers)

1. **The KB4 failure for video is stable blindness.** Adversarial clips
   (1px/frame, 0.25 contrast) produce zero suprathreshold difference
   pixels → centroid displacement mag=0 → STILL, wrong, conf 428.
   The blindness is IDENTICAL in every 4-frame window and every spatial
   crop — so G-TEMP and G-SPAT agree with the error (pure adv false
   57.9% / 53.3%). Self-corroboration cannot catch a stable failure mode.
2. **Method disagreement is the only informative signal.** The
   block-matcher (local 8×8 correlation, ±3px search) sees the 1px/frame
   motion the centroid method is blind to (e.g. adv p010: centroid N
   wrong, block-match E right, sx=448 = all 448 blocks voting +1x).
   When the two independent methods agree, the judgment was correct
   **29/29 times** on this probe (20/20 primary + 0/9 adv false for
   G-METH pure).
3. **The gate is honest but nearly silent.** G-ALL installs 8/90, all
   correct (all STILL in this probe); G-METH installs 5/90, all correct
   (incl. 3 real motions: SW, NW, SE). Everything uncertain withholds.

## Determinism (prereg §9: PASS)

- Full pipeline (windowize → sense/method2/gate → scoring) rerun ×3
  from wiped caches: `results/final.json` sha256 identical all 3 runs:
  `0885fe959279ce7f9bbf1e18879c65418f62d64b803a1f02699ccdedbe5464fb`
  (`logs/digest_run{1,2,3}.txt`, `results/final_run{1,2,3}.json`).
- `sense`, `method2`, `gate`: 3 runs each on one fixture, byte-identical.
- Zero RNG in sense/reasoning; Python glue deterministic (sorted orders).

## Gate spec for the ingestion pipeline (implement exactly this)

Per 8-frame window of ingested video:

1. Compute two independent percepts (pure Zag, zero RNG):
   - P1 = centroid-track (`sense motiondir`): difference-mask
     (|ΔRGB| summed > 90) centroid displacement, first→last mask.
   - P2 = block-match (`method2`): 8×8 blocks, stride 8, ±3px SAD
     search on luminance (r+g+b), edge-clamped; aggregate vote (SX,SY).
   - Judgment each: STILL iff mag < 1, else the sense.zag octant rule
     (N = up, y grows downward; E/W if |dx| ≥ 2|dy|, etc.).
2. Corroboration checks (`gate.zag`, pure Zag):
   - TEMP: J(frames 0–3) == J(frames 4–7), else WITHHOLD `temp_disagree`.
   - SPAT: J(left half x∈[0,32)) == J(right half x∈[32,64)),
     else WITHHOLD `spat_disagree`.
   - METH: J(P1) == J(P2), else WITHHOLD `meth_disagree`.
   - (ALL additionally requires all six sub-judgments identical;
     cross-pair mismatch → `cross_disagree`.)
3. INSTALL only if all three checks pass (G-ALL). Candidate judgment =
   the agreed direction; candidate confidence = min of the six
   sub-confidences. Then the shared memory rule: install iff no
   installed contradictory judgment with confidence ≥ exists;
   else WITHHOLD + audit entry (same `apply_memory_rule` as round 1).
4. Anything failing step 2 or 3: WITHHOLD + flag with the reason.
   Nothing withheld enters memory. Log every percept (installed /
   gate-withheld / memory-withheld) with window id, judgments,
   confidences, reason.

Install criteria summary for the pipeline: **unanimous agreement of two
4-frame windows, two spatial crops, and two independent methods, then
the contradiction check.** Expected install rate on adversarial-style
content: <10%; on clean content: unknown (probe had only 4 clean STILLs
install under G-ALL) — the ingestion run must report it.

## Honest caveats

- Small denominators: G-METH pure adv is 0/9 — the 95% rule-of-three
  upper bound is ~33%, so "≤10%" is a point estimate on this probe, not
  a confident bound. The held-out YT1 probe (PREREG_YT_INGEST.md) is the
  real test; any YT1 violation halts the run and quarantines installs.
- The probe is synthetic (procedural low-contrast translation).
  Real YouTube footage has camera shake, cuts, compression — all
  untested. The gate's withhold rate there could approach 100%.
- Frozen deviation from the brief: clips are 8 frames, so temporal
  corroboration used 4-frame windows, not 8-frame (documented in
  PREREG_KB4_VIDEO.md §2).
- G-TEMP/G-SPAT are documented failures — do not use them as gates.
  Their withholds are indiscriminate (temp_disagree fired 44/90).

## Recommended follow-ups (not decided here)

- Test whether TNN can select the corroboration strength itself
  (analog of the chunking-trial open question), rather than the imposed
  unanimity rule.
- A cheaper method-2 (fewer blocks) — current ops 2.8M px-visits/clip
  vs 29k for centroid (~100×).
- YT1 held-out probe during ingestion before any install.

## Artifacts (all in `youtube_ingest/`, nothing committed)

- `PREREG_KB4_VIDEO.md` — frozen prereg
- `READINESS.md` — this file
- `code/src/sense.zag`, `method2.zag`, `gate.zag` (+ built binaries
  `sense`, `method2`, `gate`; `R33_NATIVE_IO_V1.zag`)
- `code/scripts/regen_testfresh_t6.py`, `windowize.py`,
  `baseline_kb4.py`, `score_gates.py`
- `results/final.json` (+ `final_run{1,2,3}.json`), `results/baseline_kb4.json`
- `logs/digest_run{1,2,3}.txt`, `logs/run2.log`, `logs/run3.log`
- `fixtures_testfresh/` (60 verified fixtures), `subclips/`, `runs/`
  (90 per-fixture percept+gate records)
