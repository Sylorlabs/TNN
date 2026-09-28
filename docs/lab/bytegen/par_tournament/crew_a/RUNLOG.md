# CREW A — PAR tournament RUNLOG

**Contender:** A — pure-PAR end to end (plan formation AND render both
parallel; every sample f(plan,t), zero carried state).
**Crew scope:** A + A-forks through the full frozen battery (§2).
**Date:** 2026-09-24 | **Toolchain:** `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` (pinned)
**Laws:** pure Zag, zero RNG in decision/render paths, byte-identical reruns proven by `cmp`/SHA-256,
WAV comparisons at MIX level (house rule: global mastering shifts samples).

## 0. Inherited evidence (par_dive, 2026-09-24 — re-verified below, not blindly cited)

`../par_dive/contender_a/evidence/`: COST.md, FAILURE_MODES.md, FORMATION.md,
PER_PATH_NOTES.md, RT_CASCADE.md, VERDICT_AUDIO.md.
Dive headline: PARTIAL WIN — RT-LONG 440.00 Hz +0.00¢ vs native +53.27¢;
RT-CASCADE 0 vs 5791 post-fault diffs; coherence 1.000000 vs 0.736557; 9/9
gates; 5-min drift byte-identical. **Verdict: NO OVERTHROW** (COST regression
−46% single-threaded blocks §6's "no regression elsewhere").

## 1. Battery plan (§2 frozen, fixture `bytegen/fixture/plan_v1.txt`, 30 s / 44.1 kHz / mono)

Rebuild `render_a.zag` + `form_par.zag` from par_dive sources into this
crew's `src/` (self-contained tournament record), re-run fresh:
- DET: two renders, `cmp` clean @ mix level.
- QUALITY: 9 V10 bars via audio-line consistency gate
  (`imagination_discovery/aud/b_alpha/consistency_gate/src/gate_bin`,
  `gate <clip.wav>`) on an i16 WAV written from the s32 mix dump
  (clip behavior documented, not hidden) + CHOP-1/2/3 with the COMPLETE
  event list (onsets+offsets+release tails+predicted vibrato extrema).
- COHERENCE: motif recurrence zero-lag normalized xcorr (motif 2.0–5.4 s vs
  24.0–27.4 s) + max-lag ±50 ms + pitch/IOI contour correlation (decomposed).
- COST: wall-clock + peak RSS, same machine, 6 interleaved runs vs native
  (`bytegen/fork_ar/src/render_ar.zag`, rebuilt pinned).
- RT-LONG: cue 440 Hz @ t=1 s, RESPOND @ t=28 s nominal 880 Hz; cents error
  of response (honest: octave detector vs pitch meter). Near-miss: nominal 460.
- RT-CASCADE: single-bit fault in mix @ t=3 s; differing post-cut samples vs
  clean @ mix level. Extended with burst, dropout, DC-shift (forensics §3).
- RT-EDGE: plan truncated @ 15 s; discontinuities at cut + legitimate vs
  illegitimate diffs vs full plan.
- FAILURE MODES: documented — where it breaks that others don't.
- §5 red team (A): parallel-order permutation (evperm — must be
  bit-identical), sustained 1292-block corruption, plan-text adversarial
  inputs, sub-octave nominal lies, vibrato/glide cues vs ZCR sensor.

## 2. Fork claims (PREREGISTERED — each tested below, claim stated before build)

### A-fmt — plan-formation parallelism (Micah: "left to right but it first plans parallelly")
CLAIM: plan events can be formed in parallel shards and assembled into a
byte-identical plan (formation is order-free); formation-only speedup ≈
linear in shard count S (dive proto: 4.44× @ S=8, 8.65× @ S=64 on the toy
theme); end-to-end win is bounded by the formation fraction of total time
(formation ≈ 0.03 s of a 6.4 s render ⇒ E2E ≈ 1.00× at 30 s — the parallelism
dividend is real for formation scaling, not for the 30 s render). Test: form
a scaled-up theme (thousands of events) sequentially vs parallel shards,
`cmp` byte-for-byte, measure min-of-N CPU times, report formation-only and
E2E speedups. PASS bars: byte-identical plans in all orders; speedup_form ≥
0.7×S at S=8 (measured, unloaded); E2E reported honestly.

### A-long — long-horizon drift (≥5 min)
CLAIM: pure f(plan,t) shows ZERO phase/tuning drift at ≥5 min (extending the
dive's 300 s result to 600 s): motif recurrence 590 s apart byte-identical,
bed tuning Δ ≤ 0.001 cents, because phase is a closed form of event-relative
time. Native per-event-carried shows bounded LSB-level (≤0.006 FS) drift;
native global-oscillator shows phase-shift semantics on repeats (xcorr
≈0.5), not tuning drift. PASS bars: par motif @t vs @t+590 s — 0 samples
differ, xcorr 1.000000; pitch Δ 0.000 cents. FAIL if any par sample differs.

### A-poly — polyphony battery
CLAIM (from dive §3, to quantify + document as A's failure mode): on dense
N-voice chords (N=2/4/8/16/32, whole-tone stack from 220 Hz) PAR's
plan-exact linear sum clips at the i16 output stage from N=2 up (peak
≈ N/√? measured: 0.66×/1.32×/2.44×/3.99×/6.39× i16FS at N=1/2/4/8/16 —
superlinear because the stack is coherent-ish), ZCR-of-sum tracks the
highest voice (not a pitch), voice-vs-mix correlation follows 1/√N (real
masking structure, deterministic); AR's servo self-limits (RMS halved,
darkened) at the cost of plan-deviation. Genuine tradeoff, neither side
"wrong". PASS bars: measurements reproduce dive figures within tolerance;
clip fractions at i16 stage documented per N; no crashes/hangs on N=32.

## 3. Excerpt policy

Excerpts rendered for the record into `par_tournament/crew_a/excerpts/`
labeled WITHHELD-NOT-FOR-REVIEW. NEVER presented to Micah — his judgment
queue (child-voice motif clips) comes first; these stay banked until he
judges those.

## 4. Commit rule

Commit to branch `tnn-native-lab` via:
`TMPDIR=~/workspace/tmp_commit ~/workspace/commit_racefree.py tnn-native-lab
<msgfile under ~/workspace/tmp_commit> <tnn-lab-relative paths>`.
Never commit binaries/.zagd/.zag-cache. Verify with
`~/workspace/skills/github/bin/gh-api GET /repos/sylorlabs/TNN/branches/tnn-native-lab`
plus a read-back.

---
(run entries follow)

## 5. Base battery results (fresh builds, pinned toolchain, 2026-09-24)

Binaries: `src/render_a` (from par_dive contender_a/src/render_a.zag),
`src/form_par`, `src/render_nat` (from bytegen/fork_ar/src/render_ar.zag,
the servo-AR native baseline). All pure Zag, zero RNG.

| Bar | Contender A | Native (AR) | Verdict |
|---|---|---|---|
| DET (2 renders, cmp @ mix) | byte-identical, SHA a30c6577e265152d... | byte-identical | TIE |
| QUALITY 9 V10 bars | 9/9 PASS (G-PER 0.340, G-STA 1.826, G-LURCH 2.362, G-DRIFT 480.284, G-FLUXm 241.824, G-SIL1 0, G-SIL2 0, G-CLIP 0.849, G-CREST 3.863 — exact dive values reproduced) | 9/9 PASS (dive) | TIE |
| CHOP-1/2/3 (296-ts complete list) | 0 hard disc / no ≥150 ms gaps / 29 spikes, 0 unexplained | — | PASS |
| COHERENCE xcorr zero-lag (2.0–5.4 vs 24.0–27.4 s) | 1.000000, byte-identical windows | 0.736557 (dive) | A WINS |
| COHERENCE max-lag ±50 ms | 1.000000 @ lag 0 | 0.736557 (dive) | A WINS |
| COHERENCE pitch contour | 1.000000 (per-note pitches identical; note 7's estimator locks to 110 Hz bed in BOTH motifs — symmetric, not a finding) | 0.999630 (dive) | A WINS |
| COHERENCE IOI contour | constant 0.400 s by plan; correlation degenerate (constant sequences) — tie by construction | 1.0 (dive) | TIE |
| COST wall (6 interleaved, quiet) | median 6.75 s | median 4.29 s (1.57×) | NATIVE WINS |
| COST cpu (8 interleaved, wait4, contention-free) | median 0.92 s (tight 0.90–0.93) | median 0.80 s (tight 0.79–0.81) → 1.15× | NATIVE WINS |
| COST peak RSS | 15.3 MB | 15.4 MB | TIE |
| RT-LONG (cue 440, nominal 880) | formation → 440; render 440.00 Hz, +0.01¢ (bed-subtraction, exact for A) | ZCR-measures own cue → 454.00 Hz (+54.23¢); renders 454.38 Hz (+55.69¢) | A WINS |
| RT-LONG near-miss (nominal 460) | 440.00 Hz, −0.00¢ | — | A ignores nominal |
| RT-CASCADE single-bit @3 s | pre 0, win 1/1, post **0**/1,190,699 | pre 0, win 1/1, post **5,854**/1,190,699 (dive: 5,791 — same phenomenon, current-build number) | A WINS |
| RT-CASCADE burst/dropout/DC @10 s | post **0** all (dropout win 44,098/44,100 — 2 clean-zero samples) | — | A: zero cascade |
| RT-EDGE trunc @15 s | DUR-15 vs full[0,15): **0**/661,500 diffs; DUR-30-trunc vs full: 481,918 diffs ALL in [16.0,29.3) (removed events' spans — reproduces characterization's 481,918 exactly); 0 illegitimate at cut | — | PASS |
| §5 evperm | bit-identical to seq+mix | — | PASS |
| §5 1292-block sustained corruption | 1,323,000/1,323,000 samples corrupted over 1024 blocks; re-render byte-identical | — | PASS (recovery) |
| §5 adversarial plan text (9 cases) | no crash/hang, rc=0 all | — | PASS (permissive-degrade, documented) |
| §5 sub-octave/vibrato/glide cues | all resolve 440 Hz | — | PASS |

RT-EDGE note: the dive's VERDICT_AUDIO cited "4,397 diffs in [14.9,15.0)" on the
DUR-15 comparison; the current build gives 0 on the identical comparison and
481,918 (characterization's exact number) on the DUR-30 comparison. The 4,397
figure did not reproduce — possibly their truncated plan differed in an
unrecorded way. Both of my comparisons show legitimate-only diffs; the bar passes.

COST note: the fair number is CPU time (wait4, contention-free): A 1.15×
native. Wall ratios (1.46–1.57×) inflate under VM contention. Either way native
wins COST single-threaded; the architectural price (per-sample integer-division
phase recompute vs carried add) is confirmed, smaller than the dive's wall
number suggested.

## 6. Fork builds (claims preregistered in §2 above)

### A-fmt — RESULTS (2026-09-24)
- Identity: `form_pfmt seq` == `form_par` on theme_v1 (byte-identical);
  bigtheme (4,000 directives, 571 RESPONDs) seq == S=8 assembled, SHA
  `31ceb5f91289f66a6eb0e5e8aa55d88441274d0794a6b393b9f4150df714386b`;
  also exact at S=1, S=2, S=64, theme_v1 S=4. PASS (identity bar).
- Speed: seq formation CPU min-of-5 0.174 s; one S=8 shard 0.098 s;
  8 shards concurrent wall 1.612 s on loaded 2-CPU VM (≈0.07× sequential
  in one batch; every shard reparses the whole theme, pass-2 assembles
  serially — replicated-parse serial fraction dominates at this theme size).
  **FAIL on the preregistered speedup_form ≥ 0.7×S bar.** No measured
  formation speedup in this implementation/environment; E2E impact nil
  (rendering dominates).
- Verdict: mechanism PROVEN (deterministic sharding/assembly, exact at all
  S), speedup NOT demonstrated. A determinism result, not a performance
  result. The dive prototype's projected 1.67–8.65× numbers do not transfer
  to this implementation — not claimed here.

### A-long — RESULTS (2026-09-24)
- 600 s render: 26,460,000 samples, 105,840,000-byte MIX; two rerenders
  byte-identical, SHA-256 both
  `dc5be1ca16ad223a8dac1ac7f087f56feafe45ff0f91650d8e43fba6446b7a1e`
  (files deleted after hashing — size).
- Motif @5 s vs @590 s: byte-identical windows, zero-lag xcorr
  1.0000000000. Bed FFT (Hann, zero-padded): 20–30 s 110.00018 Hz
  (+1.65 ppm); 560–570 s 110.00018 Hz (+1.65 ppm) — no tuning drift.
- `nat` (carried accumulators, no servo): early/late motif xcorr 0.999945,
  windows not byte-identical (bounded one-time inc-truncation noise).
- Verdict: PASS (exceeds the preregistered ≥5 min bar at 600 s).

### A-poly — RESULTS (2026-09-24)
Raw MIX, chord region 2–5 s, i16FS=32768:
| N | A peak | A clipfrac | A RMS | A ZCR | nat peak | nat clipfrac | nat RMS | nat ZCR |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0.664 | 0.0000 | 0.3454 | 716 Hz | — | — | — | — |
| 2 | 1.325 | 0.0370 | 0.4880 | 930 Hz | — | — | — | — |
| 4 | 2.442 | 0.1536 | 0.6901 | 1,064 Hz | — | — | — | — |
| 8 | 3.991 | 0.3567 | 1.0822 | 1,394 Hz | — | — | — | — |
| 16 | 6.394 | 0.5627 | 1.7741 | 2,606 Hz | 4.476 | 0.3539 | 1.0780 | 1,908 Hz |
| 32 | 10.309 | 0.7066 | 2.7246 | 8,960 Hz | 5.764 | 0.5331 | 1.5822 | 7,590 Hz |
- A clips at the i16 stage from N=2 up; no output-adaptive behavior.
- Native servo-AR self-limits: RMS ≈ halved, timbre darkened, AGC at 0.5
  floor — but max|par−nat| = 4.793 FS at N=32 (4.79 full-scales of
  plan-deviation). `render_fn nat` (no servo) matches A to 0.0138 FS: the
  self-limiting is the servo's, not carried accumulators'.
- Linearity: Σ(32 solos) == chord mix exactly (max|d| = 0).
- Masking: voice↔sum correlation mean 0.2465 vs 1/√32 = 0.1768 (coherent
  above incoherent baseline — harmonic overlap in the whole-tone stack).
- ZCR-of-sum tracks the highest voice (not a pitch).
- Mitigation: gain-staged N=32 (amp 88 = 500/√32): peak 1.814 i16FS,
  clipfrac 0.0365, RMS 0.4794, rerun byte-identical — clipping is manageable
  at plan level, but the renderer does not adapt.
- Note: `render_nat` mix-output mode is `seqmix`; `seq+mix` silently writes
  16-bit WAV (caught during this fork — all native numbers above use
  `seqmix`).
- Verdict: CONFIRMED REGRESSION vs native on dense sums (tradeoff, not a
  bar failure — preregistered as the failure-mode fork).
