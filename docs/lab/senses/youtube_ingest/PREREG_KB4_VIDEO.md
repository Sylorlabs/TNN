# KB4-VIDEO — Corroboration-gated install rule, head-to-head (FROZEN PREREG)

Frozen 2026-09-22 (PDT). No trial runs were executed before this freeze.
All variants, bars, data, and decision rules below are fixed here; the
verdict in READINESS.md is a mechanical application of them.

## 1. Question

The senses rebuild verdict recommended a corroboration-gated install rule
as the follow-up to the KB4 catastrophe, and it was never run. Does a
corroboration-gated install rule clear the KB4 bar (adversarial
false-install rate ≤ 10%) for Approach-A VIDEO percepts (motiondir,
9-way: STILL + 8 directions) at the rematch-T4 fitted parameters
(motion STILL iff mag < 1), where the shared round-1 rule fails at
16/17 = 94.1% false-install on adversarial motion fixtures
(55/114 = 48.2% across all tasks)?

## 2. Data (frozen)

- ADV-R1 motion: 30 adversarial `.vid` fixtures from
  `tnn-lab/senses/rebuild/harness/fixtures/t6_motiondir/adversarial/`
  (generator seed 20260921, frozen on disk; sha256 verified against
  `rebuild/harness/fixtures/MANIFEST.sha256` before use).
- TEST-FRESH primary motion: 60 primary `.vid` fixtures, generator seed
  20260923, regenerated with the frozen round-1 `gen.py` into
  `youtube_ingest/fixtures_testfresh/`; every file's sha256 verified
  against `rematch/data/TEST_FRESH/MANIFEST.sha256` before use
  (post-rematch the fixtures were deleted; only manifests were kept).
- Clip layout: 8 frames, 64×64. Primary: photo window translates 2px/frame,
  full contrast. Adversarial: 1px/frame, 0.25 contrast (plus STILL cases).
- FROZEN DEVIATION from the brief: the brief asked for "≥2 consecutive
  8-frame windows". Clips are only 8 frames long, so temporal
  corroboration uses two consecutive 4-frame windows (frames 0–3, 4–7).
  The principle (temporal consistency of the direction judgment) is
  unchanged; the window length is adapted to fixture reality.

## 3. Sense binaries (pure Zag, zero RNG, deterministic)

- `sense` — Approach-A `sense.zag` (`task_motiondir`) copied from
  `rebuild/a_raw/` (with `R33_NATIVE_IO_V1.zag`) into `code/src/`,
  compiled with the pinned toolchain
  `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
  Fitted judgment rule (rematch T4): STILL iff mag < 1, else the frozen
  hand octant rule (byte-identical to `relations.a_octant`).
  Confidence: binary-emitted frozen rule 1000*|mag−3|/(|mag−3|+4).
- `method2` — new pure-Zag SECOND differencing method (block matching),
  spec §5. Same judgment rule (STILL iff mag < 1, else same octant rule).
  Confidence: 1000*|mag−1|/(|mag−1|+4) (same margin form, fitted bar).
- Sub-clip slicing (4-frame windows, left/right crops) is Python glue:
  byte-exact slicing of the `.vid`, no computation. Not a sense.
- Gate (`gate.zag`, §6) is pure Zag. Python applies the shared memory
  rule on top of gate candidates, exactly as rematch `fit.py` §kb4 did
  (the memory store is a Python-side list there and here; the rule code
  is vendored verbatim from `rebuild/harness/score.py`).

## 4. Variants (frozen)

BASELINE (shared round-1 rule): whole-clip fitted judgment (t=1) with
binary confidence; install iff no installed contradictory judgment with
confidence ≥ exists (vendored `apply_memory_rule`); else withhold+audit.
Expected reproduction of rematch T4 motiondir: 17 installs, 16 false,
73 withholds over the 90-fixture stream.

Gate candidates (gate.zag decides corroboration; the shared memory rule
is layered on top, so every gate variant is strictly stricter than
BASELINE and any difference is attributable to corroboration):

- G-TEMP: W1 = frames 0–3, W2 = frames 4–7 (each a 4-frame `.vid`).
  Corroborated iff J(W1) == J(W2). Candidate: (J*, min(c1,c2)).
  Else gate-WITHHOLD with reason `window_disagree`.
- G-SPAT: crops L = x[0,32), R = x[32,64) (each 64×32, 8 frames).
  Corroborated iff J(L) == J(R). Candidate: (J*, min(cL,cR)).
  Else gate-WITHHOLD with reason `crop_disagree`.
- G-METH: whole clip, `sense` vs `method2`. Corroborated iff equal.
  Candidate: (J*, min(c_sense, c_m2)). Else WITHHOLD `method_disagree`.
- G-ALL: all three agreements (6 sub-judgments). Candidate confidence =
  min of all six. Else WITHHOLD naming the first failing check.

Any gate-WITHHOLD → the fixture is never installed (logged). Candidates
then pass through `apply_memory_rule` exactly as BASELINE.

Secondary (reported, not verdict-bearing): pure-gate numbers
(corroboration only, no contradiction check) for each variant.

## 5. method2.zag spec (block-matching displacement, integer, deterministic)

- Input: `.vid` path via argv. Luminance L = r+g+b per pixel (no division).
- Grid: 8×8 blocks, stride 8 over the frame; per consecutive frame pair
  (t, t+1), t = 0..nf−2.
- Per block at (bx,by) in frame t: search offsets (ox,oy) ∈ {−3..3}² in
  frame t+1; SAD = Σ_{8×8} |L_{t+1}(bx+ox+u, by+oy+v) − L_t(bx+u, by+v)|,
  out-of-bounds coordinates clamped (edge replicate). Winner: smallest
  SAD; ties → smallest |ox|+|oy|; then smallest ox; then smallest oy.
- Aggregate vote: SX = Σ winning ox, SY = Σ winning oy over all blocks
  and all frame pairs.
- Judgment: mag = isqrt(SX²+SY²); STILL iff mag < 1; else octant(SX,SY)
  with the exact sense.zag octant rule.
- Output: same key=value lines (approach=A, task=motiondir, judgment,
  confidence, ops, debug_vec=sx=..;sy=..;mag=..;). Ops counts
  pixel-visits.
- Zero RNG, no wall clock, no uninitialized reads.

## 6. gate.zag spec (pure Zag)

CLI: `gate <variant> <clip> <j1> <c1> [<j2> <c2> ...]` where variant ∈
TEMP, SPAT, METH, ALL; judgments are the 9 direction strings; confidences
integers 0..1000.
Emits:
```
gate=<variant>, clip=<clip>, n=<pairs>
corroborated=<0|1>
judgment=<J* or NONE>
confidence=<min-c or -1>
decision=<CANDIDATE|WITHHOLD>
reason=<agree|window_disagree|crop_disagree|method_disagree>
```
Agreement = all pairs' judgments identical (string compare).
TEMP/SPAT/METH take 2 pairs; ALL takes 6 pairs (temporal, spatial,
method order) and requires all three pair-agreements; reason names the
first failing check.

## 7. Memory stream + scoring (KB4-style, mirrors rematch fit.py §kb4)

Per variant: stream = 30 ADV-R1 adversarial + 60 TEST-FRESH primary
motion fixtures, sorted by fixture rel path (adversarial paths sort
before primary — same order as the rematch KB4 streams). Decisions
applied in stream order. Measures per variant:
adv_installs, adv_false_installs, adv_false_install_rate =
adv_false_installs/adv_installs (vacuous if adv_installs = 0 → treated as
non-verdict), withholds, withhold_rate = withholds/90, installs.
Descriptive: primary-install accuracy (installed primary judgments that
are correct / primary installs).

## 8. Frozen bars → verdict

- READY: some variant with adv_false_install_rate ≤ 10% AND
  adv_installs ≥ 5 AND withhold_rate ≤ 90% (non-trivial: ≥ 10% of the
  90-fixture stream installed; 0/0 can never be READY).
- GATED: no variant meets READY, but the best variant is honest — i.e.,
  its gate withholds the dangerous percepts (adv_false_install_rate ≤
  10% with withhold_rate > 90%, or best false-install > 10% but the
  withhold set provably covers the false-install class). READINESS.md
  then specifies EXACTLY what the gate withholds/flags and the install
  criteria the ingestion pipeline must implement.
- NOT READY: no variant is both honest and bar-clearing — e.g.,
  corroborated methods agree on wrong judgments (systematic confident
  error), or false-installs persist above 10% at usable install rates.

## 9. Determinism (frozen)

- Full pipeline rerun ×3 (clean subclip/run caches each time);
  sha256 of `results/final.json` must be byte-identical across all 3.
- `sense` and `method2`: 3 runs each on one fixture, byte-identical
  stdout.
- Zero RNG in sense/reasoning paths; Python uses only sorted iteration
  and fixed seeds (fixture regen).

## 10. Validity gates (halt conditions)

- BASELINE does not reproduce rematch T4 motiondir exactly
  (17 installs / 16 false / 73 withholds) → harness invalid; halt,
  fix, do not proceed to gates.
- TEST_FRESH regeneration: any sha256 mismatch vs the frozen manifest →
  halt (fixtures not the rematch's fixtures).
- A READY claim on adv_installs < 5 → rejected as vacuous.
- Commit nothing to the repo. READINESS.md + gate spec + logs stay in
  `youtube_ingest/`.

## 11. Work log

- 2026-09-22: prereg frozen (this file). Data inventory, generator
  inspection, and rematch code reading done; no trial runs executed.
