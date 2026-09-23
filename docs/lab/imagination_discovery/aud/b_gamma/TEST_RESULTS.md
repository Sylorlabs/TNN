# TEST_RESULTS.md — B-γ fork results

**Fork:** B-γ (the monster fork), position (b) study-then-invent, event-assembler.
**Ears:** Micah's (final oracle) + 5 fresh native critics (Test 1) — arranged by the parent.
**Status legend:** ⏳ not yet run · ✅ pass · ❌ fail · 🟡 partial/honest-smaller-claim

## K0 — determinism gate (must pass before anything ships)

| Subject | SHA-256 | 3/3 byte-identical |
|---|---|---|
| kids | `655978ec978a6ae5fd792f3c442b48bba601df307a067ecf0a21144c68464b95` | ✅ |
| planet | `71c5c7b0bcbe7b63cb03baa3336f3ae04bf79e97203b29031a43b768b5c50feb` | ✅ |
| ocean | `e8db1a18f47f1df21e0f63c8fa22a3914c14eb85201ebc94732423d5364278bb` | ✅ |
| monster | `6b0c9c576a0fa504490e79c2a6d36f73d8750917129d19a2d2d7775b2d844a9c` | ✅ |

Rendered by `gamma_bin` (pure Zag, zero RNG) from `study_out/gamma.grpk`
(1278 grains, 12 licensed sources). Rerun: `python3 render_verify.py`.

## K1 — the kids-playing-and-laughter bake-off (benchmark / TEST 1)

**Brief given to judges:** 30 seconds, children playing and laughing:
≥3 distinct child voices, overlapping play, running feet, one laugh tumbling
into another.

**Blind set:** three 30 s clips, hidden deterministic order (sorted by
sha256 of bytes — documented in `blind/ORDER_SEALED.md`):

| judge_A.wav | `blind/clip_synth.wav` | control (i): synth.zag paradigm's best attempt at the same brief |
| judge_B.wav | `blind/clip_real.wav` | control (ii): real playground recording (calibration only) |
| judge_C.wav | `blind/clip_method.wav` (= `render/b_gamma_kids.wav`) | B-γ method |

**Kill bars (from AUDIO_DEBATE.md):**
- Any one "sounds like a synth" from Micah → B-γ's kids claim dies.
- No-copy audit must clear (audit.py, bar 0.80).

| Check | Result |
|---|---|
| no-copy audit (max 2 s window xcorr vs any study source) | ✅ CLEAR — 57 windows, 0 trips, worst 0.361 (bar 0.80), 2026-09-22 |
| A-NATIVE (native_check.py) | ✅ PASS (see table below) |
| ≥3 distinct child voices (audit + critics) | ⏳ critics pending |
| overlapping play / running feet / tumbling laughs (critics) | ⏳ critics pending |
| 5 fresh native critics: method vs control | ⏳ parent to dispatch (brief: `blind/JUDGE_BRIEF.md`) |
| Micah's verdict | ⏳ |

**Control history (honest):** the synth control initially shipped with a
numerical bug — `tsin_small`'s 4-term Taylor series diverges for the
harmonic arguments (ph·2/3/4 up to 25 rad), producing million-scale samples
whose peak-normalization crushed the whole clip to near-silence (5 s digital
black tail, A-NATIVE FAIL). Fixed 2026-09-22: phase wrapped to [−π,π] inside
`tsin_small`, score extended to fill 30 s. Rebuilt control passes A-NATIVE
(peak 0.679, hiss CLEAN, clicks 0.39 < 1.20) — which is exactly why Micah's
ears, not the bar, decide the synth-smell question. Final blind mapping:
judge_A = synth control, judge_B = real playground, judge_C = B-γ method
(deterministic sha256 order, `blind/ORDER_SEALED.md`).

**Outcome:** ⏳

## v2 — natural-ending re-render (kids, 2026-09-22)

Micah's ear verdict on v1 (`render/b_gamma_kids.wav`): "meh, same issue as
2nd" + shared defect "cut off weirdly" at the end. Fix dispatched: natural
ending only; no recomposition of the cutouts (see cutout diagnosis below).

**What changed** (one compositional edit in `score_kids`, `gamma.zag`): the
wash-ambience scatter bound moved 30.0 → 26.0 s (`wash_end` variable).
Scatter's t-sequence is t1-independent (deterministic h32), so every
placement before 26.0 s is unchanged; only the final wash grain (was: placed
28.702 s, 3.0 s long → hard-clipped by the 30.0 s file boundary, since
`place()` stops at `nsamp` with no fade — the measured cause of the weird
cutoff) is gone. The last wash grain is now at 25.70 s and its FULL natural
3.0 s decay completes at 28.70 s. No synthetic fades added; the only
envelopes are the grammar's own 88-sample edge glue (unchanged) and the
renderer's standard mastering (unchanged). Grain vocabulary, T1–T8, and all
content before ~28 s identical by construction. v1 file kept intact.

**Verification:**

| Check | Result |
|---|---|
| 3/3 byte-identical renders | ✅ `1842356072a9f19bbdd830517ab9d6c5df140cf6596cbc7f60d03db2e788d71f` |
| A-NATIVE (same gates as v1) | ✅ PASS — peak 0.673, DC 0.000073, ZCR 0.0593, natural fall (20.8/6.9/1.7 dB), hiss 0.000 CLEAN, clicks 0.34 < 1.20 |
| 30.00 s mono 44.1 kHz PCM16 | ✅ |
| no-copy audit (audit.py, bar 0.80) | ✅ CLEAR — 57 windows, 0 trips, worst 0.361 |

**Tail-envelope evidence** (max |sample| per 100 ms, last 2 s):
- v1: `[…,1479,1870,1745,1766,1348,906,647,432,141,62]` — compressed
  1479→62 taper in the last 600 ms: the clipped grain choking at the boundary.
- v2: `[…,2855,1688,335,335,335,335,335,320,282,229,167,106,52,14]` —
  genuine decay: last grain energy ends 28.7027 s; 28.7–29.2 s is the file's
  natural floor (flat digital 335 = the mastering's DC-removal residue,
  inaudible DC); 29.2–30.0 s is the renderer's standard 0.8 s end-fade
  resolving it to 0. Final 100 ms max = 14 (≤ 1000) ✅. Last nonzero sample
  at 29.975 s; file ends at 30.0 s from the quiet floor.

**Pre-28 s unchanged (honest accounting):** the integer mix is bit-identical
to v1 for the first 28.70 s (deterministic placements + integer adds; the
reverted source reproduces v1's SHA `655978ec…` exactly, proving pipeline
determinism). The final WAV differs from v1 by ±1 LSB on ~2% of pre-28.7 s
samples: `write_wav` does full-file DC removal + peak normalization, so
removing the clipped tail grain shifts the file-wide DC by ~0.02 LSB and
~2% of samples round differently at truncation. Inherent to the mastering
chain, inaudible, A-NATIVE unaffected. Peak unchanged (22040 @ 6.422 s both).

**Cutout diagnosis (independent 10/50 ms envelope pass, my own):** AGREE
with the dispatched diagnosis. 0 flanked digital dropouts at both
resolutions; 0 hard onsets; 0 gate-like slams to zero. Three soft-shouldered
dips flagged (0.77 s, 9.35 s, 18.75 s) are 150–300 ms wide with minima
~1000–1900 and soft edges — phrase boundaries of the event-grain grammar
(e.g. 9.35 s: laugh trains decayed, next chase not yet started), i.e.
compositional content, not a digital artifact. Per the fix-only-artifacts
rule, the grammar was not changed.

## v3 — continuity fix (kids, 2026-09-22)

Micah's binding continuity law ("imagination doesn't cut out") + his ear
verdict on v1 ("meh, same issue as 2nd"): the three soft-shouldered dips
(0.77 s, 9.35 s, 18.75 s) are phrase boundaries of the event-grain grammar
where the score scheduled "end of behavior, next not yet started." The
"content by design" defense is REJECTED per the frozen cutout debate
(`imagination_discovery/aud/CUTOUT_DEBATE.md`). Fix implements the debate's
surviving convergent mechanism: **world-first composition** — a continuously
scored world, no silence nodes, every boundary a pivot/bridge with
overlapping successor content.

**What changed** (compositional, `score_kids` only, `gamma.zag`):
- New `bridge_world(h,m,nsamp,t0,t1,wt1,salt)` helper: scores the scene state
  that persists BETWEEN events as first-class captured content — sustained
  world texture (long wash grains overlapping at 0.9 s spacing, gain 0.20),
  breath/air (wind scatter, 0.055), shuffling feet (thump `run_feet` at
  1.2 Hz, gain 0.10), distant play (laugh scatter at 0.9 s spacing, gain
  0.09). All picks deterministic h32; grains placed whole, no pitch/time
  modification; never a crossfade (this is composed content, not a fade —
  the sham control's "just crossfading" objection does not apply).
- Five scored bridges (fresh salts 51..66, so no pre-existing t-sequence is
  disturbed): 0.0–2.4 (scene already alive at sample 0), 8.8–10.8 (the 9.35
  pivot), 14.4–16.4 (post-trip breath — kids catching air), 18.3–21.4 (the
  18.75 pivot through the wind-down), 24.8–26.8 (world settles WITH the
  ending). The final bridge caps long grains at 25.6 s (`wt1`) so the v2
  natural ending is preserved.
- Four `run_feet` trains EXTENDED across boundaries (append-only — the
  `while(t<t1)` loops walk identical prefix steps, so every pre-existing
  placement is bit-identical): running-in 4.5→5.2 (feet carry into the
  chase), chase trains 9.0→10.7 / 9.2→10.9 / 8.5→10.5 (chase feet continue
  UNDER the decaying laugh trains at 9.35 and overlap the next chase),
  breathless chase 20.0→21.2 (slows INTO the walk).
- The trip at 12.2 s (thud 0.62 + squeals + shriek-laughter) is untouched;
  the world continues under it — chase feet (10.0–13.5) keep running; no
  global dip is scored.
- v2 natural ending preserved: wash bed still ends at 26.0 (`wash_end`
  unchanged); last grain energy ends 28.7 s; 28.7–30.0 s is the quiet floor
  resolving through the renderer's standard end-fade.

**Verification:**

| Check | Result |
|---|---|
| 3/3 byte-identical renders | ✅ `18cb055571a8a595fa8f080adbf613188407a3c4f2815dd2e1ce41befc54eb8f` |
| A-NATIVE (same gates as v2) | ✅ PASS — peak 0.671, DC 0.000040, ZCR 0.0641, natural fall (22.1/7.2/3.1 dB), hiss 0.000 CLEAN, clicks 0.34 < 1.20, crest 6.8 |
| 30.00 s mono 44.1 kHz PCM16 | ✅ |
| no-copy audit (audit.py, bar 0.80) | ✅ CLEAR — 57 windows, 0 trips, worst 0.395 |

**Continuity measurements** (`/tmp/continuity.py`, 10 ms RMS frames,
±250 ms window; bar: boundary floor ≥ 3× v2 floor):

| Boundary | v2 floor | v3 floor | ×v2 | v2 depth | v3 depth | Bar (3×) |
|---|---|---|---|---|---|---|
| 0.77 s | 0.0142 | 0.0368 | 2.6× | −15.5 dB | −8.2 dB | n/a (not flagged in prereg) |
| 9.35 s | 0.0083 | 0.0435 | 5.2× | −21.8 dB | −10.1 dB | ✅ (≥0.0249) |
| 18.75 s | 0.0111 | 0.0401 | 3.6× | −7.0 dB | −4.3 dB | ✅ (≥0.0333) |
| control 3 s | 0.0186 | 0.0312 | — | −12.4 dB | −8.8 dB | — |
| control 18 s | 0.0179 | 0.0359 | — | −3.7 dB | −4.9 dB | — |

300 ms-window check (T-CONT-3 style): no ≥300 ms window below 0.020 RMS at
any flagged boundary — min 300 ms averages are 0.0605 (0.77 s), 0.0846
(9.35 s), 0.0555 (18.75 s), all at or above the within-phrase controls
(0.0488–0.0689). The 18.75 boundary floor (0.0401) now sits ABOVE the 18 s
control minimum (0.0359): the boundary is indistinguishable from
within-phrase texture — the world-first ideal.

**Tail-envelope evidence** (max |sample| per 100 ms, last 2 s):
- v3: `[…,3056,2951,3454,2756,3722,2968,1571,455,455,455,455,435,384,311,228,144,71,19]`
  — genuine decay ending 28.7 s, then the quiet floor (455 = the mastering's
  DC-removal residue at the new normalization, inaudible), then the
  renderer's standard 0.8 s end-fade to 19. Same shape as v2; no grain is
  clipped by the file boundary. The `wt1=25.6` cap holds: no bridge grain
  outlives the bed's last wash grain (28.70 s).

**Honest caveats:**
- Pre-existing placements are bit-identical BY CONSTRUCTION (append-only
  t-sequences: extending `t1` cannot change earlier loop iterations; bridge
  salts are fresh; `place()` adds are commutative integer adds), but the WAV
  is NOT prefix-identical to v2: the added bridge content moved the file
  peak (v2: −22040 @ 6.42 s, the tag laugh; v3: 21995 @ 1.52 s, the
  pre-existing running-in transient lifted 2.7% by the opening bridge), so
  peak normalization rescales the whole file ~0.2% and DC removal shifts
  with the new mix mean; the soft-clip stage then redistributes a few LSB
  on loud samples. Same class of mastering caveat as v2, slightly larger
  because the peak moved. Pipeline determinism re-proven: the unmodified v2
  source still reproduces the v2 SHA `18423560…` exactly.
- The 1.52 s transient is the pre-existing running-in stack, not a new
  composed accent — but the opening bridge did make it the file peak. If
  Micah hears the opening as too hot, the fix is to trim the 0.0–2.4
  bridge's laugh-scatter gain, not to touch the grammar.
- Machine bars pass; per the debate prereg (T-CONT-4) Micah's ears are
  binding over all of this. The v3 clip is at
  `render/b_gamma_kids_v3.wav`, awaiting his verdict with the standard
  brief.

## K2 — anti-v2 rebuild (paradigm escape / TEST 2)

**Question:** does B-γ escape the v2 paradigm (oscillator/resonator/noise-bed
synth smell), or is it a synth in costume?

**Evidence:**
- TRANSFORMATION_LOG.md: closed mechanism list, exclusion list, per-piece use.
- Anti-rename audit: each mechanism defended against 1:1 mapping to synth.zag.
- `b_gamma_planet.wav`: the deliberate anti-v2 artifact — built from the
  debate's anti-v2 brief, no synth primitive anywhere in the chain.

**Judge:** Micah's ears + blind critics on planet.wav.

**Outcome:** ⏳

## K3a — alien ocean generalization (TEST 3a)

**Question:** does the studied vocabulary (Earth surf, thunder, ice) stretch
to an alien ocean without collapsing into Earth pastiche?

**Honest risks (pre-registered):** Earth-surf pastiche; reversed-crack tails
reading as synth-reverse cliché.

**Outcome:** ⏳

## K3b — the Raxith (imagination beyond experience / TEST 3b)

**Question:** can position (b) invent a movie-monster-class creature it never
heard — the Raxith, whose voice is controlled micro-fracture (MONSTER.md,
committed before rendering)?

**Honest risks (pre-registered):** ice-cubes-in-a-glass; Hollywood-boom
pastiche on the plate-breaks; "fracture percussion, not a voice."

**Smaller claim (ready if needed):** "real-event fracture percussion with
language-like phrasing" — reported honestly if the creature-voice claim
fails.

**Outcome:** ⏳

## A-NATIVE quality table (native_check.py, 2026-09-22)

| Clip | peak | DC offset | ZCR | noise-floor slope | exposed hiss | clicks | verdict |
|---|---|---|---|---|---|---|---|
| b_gamma_kids | 0.673 | 0.000072 | 0.063 | natural fall (20.8/6.9/1.7 dB) | 0.013 CLEAN | 0.34 < 1.20 | ✅ PASS |
| b_gamma_planet | 0.680 | 0.000036 | 0.076 | natural fall (8.8/−5.5/−8.2 dB) | 0.065 CLEAN | 0.63 < 1.20 | ✅ PASS |
| b_gamma_ocean | 0.679 | −0.000013 | — | natural fall | 0.006 CLEAN | 0.66 < 1.20 | ✅ PASS |
| b_gamma_monster | 0.679 | 0.000002 | — | natural fall | 0.000 CLEAN | 0.78 < 1.20 | ✅ PASS |

(Crest factors 7.8–28.8 — healthy dynamics, not squashed.)

## Grain inventory (from study_summary.json, 2026-09-22)

| Class | Grains | Voices | Notes |
|---|---|---|---|
| laugh | 144 | 0:27, 1:44, 2:73 | the benchmark's core vocabulary |
| squeal | 107 | 0:29, 1:59, 2:19 | youngest-voice events, trip scene |
| shout | 104 | 0:25, 1:30, 2:49 | calls, "you're it" |
| thump | 231 | — | footsteps, impacts |
| swell | 28 | — | lake-swell anchors (ocean) |
| wash | 19 | — | texture grains (ambience, never a bed) |
| creak | 57 | — | wood/swing creaks (seismic groans, Raxith plates) |
| crack | 442 | — | ice micro-fractures (chorus, Raxith syllables) |
| boom | 60 | — | thunder onsets (rift, plate-breaks) |
| rumble | 65 | — | thunder tails (planet hum, sky hum) |
| wind | 21 | — | Mars wind/dust-devil textures |
| **total** | **1278** | | 12 sources, pack 77.8 MB |

12 sources: 3 playground recordings (CC0 / CC BY-SA 4.0 / PD), gravel
footstep (CC BY 4.0), lake surf (CC BY-SA 4.0), 2 wood creaks (PD), swings
(CC BY 4.0), ice crackling + storm thunder + Mars wind + Mars dust devil
(PD, from aud/inspiration). Full table: STUDY_LOG.md.

## Commitments kept / broken

- [x] every transformation auditable against the grain map
- [x] no study material committed (study_src/, study_out/, binaries excluded)
- [x] synth control built and included blind
- [ ] honest verdicts reported per test, smaller claims where earned
