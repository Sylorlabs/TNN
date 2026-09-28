# PAR Characterization — forensics report (prereg §3 + §0 re-verification)

Date: 2026-09-24. Scope: frozen `PREREG_PAR_DIVE.md` §3 (forensics extension)
plus independent re-verification of §0. Micah's directive: dig super deep into
PAR; test everything, forks, red teams; see if anything overthrows native
stateful-sequential generation.

**Bottom line up front:** on every §3 axis measured, nothing overthrew PAR's
core claims. Two genuine findings against PAR: (1) the stateful AR servo is
strictly better at self-limiting dense polyphonic sums (PAR clips, AR halves
RMS and darkens — a real tradeoff, not a bug); (2) a semantic fork on what
"repeat" means — PAR's event-relative phase replays motifs bit-exactly at any
plan-time distance, while a global-oscillator native (f3_synth bin semantics)
phase-shifts repeats unless gap×frequency is commensurate. No tuning drift
exists in either renderer after 285 s (±0.001 cents). §6 overthrow bars were
NOT fully evaluated (§2 quality bars, COST, RT-LONG, §4, most of §5 remain),
so **no overthrow is claimed**.

## 0. Re-verification of settled forensics (§0)

**CHOP-3, independently re-done.** I wrote a fresh event-list generator
(`work/gen_events.py`) including note onsets, note offsets, release onsets,
vibrato extrema, and bed edges. It produced **296 timestamps, not the 321
recorded in the prereg** — discrepancy disclosed, not hidden. (Likely cause:
my generator counts vibrato extrema per note differently, e.g. 5.5 Hz ×
0.35 s ≈ 2 extrema/note vs the audit's 3, and/or bed-edge deduplication.
The prereg's 321 was not reproduced; the audit's list was not re-derived
here.) Reran `aud_v10/chop.py` on `bytegen/fork_par/src/par_seq1.wav` with
the 296-timestamp list: **CHOP-1: 0 hard discontinuities (PASS); CHOP-2: no
≥150 ms silent gaps (PASS); CHOP-3: 29 spikes, 0 unexplained.** The
substantive §0 conclusion is confirmed despite the count discrepancy.

**Standalone motif vs full plan, independently re-done.** Motif-only plan
(`work/plan_motif_only.txt`) vs full `plan_v1.txt`, rendered with `render_par`
(`seq+mix`): mix-level signed i32 in [2.0, 5.3) s — **0 / 145,530 samples
differ**. Full-plan rerender `cmp` clean. §0(b) confirmed exactly.

## 1. Method

**Builds:** pure Zag, pinned compiler
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`, zero RNG.
All renders proven byte-identical across reruns by `cmp`.

**Forensics renderer** (`src/render_fn.zag`, ported from
`bytegen/fork_par/src/render_par.zag`, validated below):
- `par` — pure `f(plan,t)`: per-event phase is a closed form of
  **event-relative** time `tr = t − t0`: `ph = floor(f0q·tr/SR)·65536`.
  **Correction to my own early assumption:** par's phase is NOT absolute
  time; it resets per event. Repetition-exactness comes from event-relative
  formulation, not absolute time.
- `nat` — carried integer phase, f3_synth pattern: per-event phase
  accumulator `ph += inc` with `inc = floor(f0q·65536/SR)` (truncated once);
  bed phase carried globally from t=0 (gap-walked across chunks).
- `natg` — **global** carried phase (true f3_synth bin semantics): each
  frequency's oscillator runs from t=0 whether or not its event is active;
  carried recurrence telescopes exactly to `ph(t) = (t·inc) mod 2^32`
  (implemented directly; modular telescoping is exact). Vibrato LFO stays
  event-local in all modes; glide unsupported in `natg` (test plans use
  glide=0).
- Fault hooks: `burst` (1024 zeroed samples @3 s), `dc` (+6553 ≈ +0.1 FS
  from 3 s to end), `pstate` (flip bit 20 of the carried phase accumulator
  @3 s; no-op under `par` by construction — control).
- `DUR_S`-driven length, chunked output below the 2²⁵ slice cap.

**Hybrid** (`bytegen/hybrid/src/render_hyb.zag`, v2 three-piece) built with
the pinned compiler; a test-only copy (`src/render_hyb_t.zag`) adds one
fault mode `dcmix` (DC +0.1 FS from 3 s to end, mix-output path). No
production paths touched; clean `seqmix` output verified `cmp`-identical
between the two binaries.

**Port validation:** `render_fn … par clean` on `plan_v1.txt` is
**byte-identical** to `render_par … seq+mix`. Reruns `cmp` clean at 30 s
and 300 s.

**Method note (bug caught):** the first `render_fn` build passed a `[]u8`
where the plan parser took `*i64` for the duration out-param; the write went
nowhere and all renders silently used the 30 s default. Fixed (slice +
`put64`); 300 s renders redone. All 30 s results predate the fix and are
unaffected (default was 30 s).

**Analysis:** `work/ana.py` — mix diffs, zero-lag/max-lag normalized xcorr,
autocorrelation pitch with parabolic interpolation (validated: +0.001 cents
on pure 440 Hz sine, +0.016 on 6-harmonic stack; vibrato-phase dependent, so
only early-vs-late *differences* are reported as drift), ZCR, RMS.

## 2. Determinism record

| check | result |
|---|---|
| `render_fn par` vs `render_par seq+mix` (plan_v1) | byte-identical |
| `render_fn par` rerun, 30 s | `cmp` clean |
| `render_fn par` rerun, 300 s drift plan | `cmp` clean |
| `render_hyb seqmix` vs `render_par seq+mix` | byte-identical (per v2 spec) |
| `render_hyb_t seqmix` vs `render_hyb seqmix` | `cmp` clean (no behavior change) |
| plan with 23 EVENT lines randomly shuffled → `par` | bit-identical to canonical order (§5 permutation probe) |

## 3. Polyphony (chord_N, N = 1/2/4/8/16; whole-tone stack from 220 Hz, 2.0–5.0 s)

Steady region [2.1, 4.9) s. `corr_k` = normalized correlation of voice k's
solo render with the mix.

| N | mix ZCR | top voice 2f/SR | voice corr (min–max) | 1/√N |
|---|---|---|---|---|
| 1 | 0.01717 | 0.00998 | 1.0000 | 1.0000 |
| 2 | 0.02110 | 0.01120 | 0.7071 | 0.7071 |
| 4 | 0.02411 | 0.01411 | 0.4988–0.5003 | 0.5000 |
| 8 | 0.03160 | 0.02240 | 0.3183–0.4648 | 0.3536 |
| 16 | 0.05928 | 0.05644 | 0.2821–0.3723 | 0.2500 |

Notes: ZCR of the sum tracks the **highest** voice (≈ 2f/SR of 1244.51 Hz),
not any lower voice's pitch — ZCR-of-sum is not any one voice's pitch for
N≥2. Voice correlation follows 1/√N while voices are incoherent; the spread
at N=8/16 is harmonic overlap (voices 6 apart are an octave: 220·2^(12/12)),
i.e. real acoustic masking structure, rendered deterministically.
`par` vs `nat` on chord_16: 87,404/1,323,000 differ (6.6%), max|d| = 903
(0.0138 FS) — same quantization-structure difference as §6, inaudible.

**AR on chord_16** (stateful reference, FR=1024 servo): agc driven to its
0.5 floor, bright to −3, vibmul up to 1.5 during the chord. AR mix RMS 0.539
FS vs PAR 0.897 FS; AR ZCR 0.04321 vs PAR 0.05928 (darkened: fewer harmonics
→ fewer crossings); AR vs PAR max|d| = 97,266 (1.48 FS). PAR peaks: 0.66×
i16FS (N=1), 1.32× (N=2), 2.44× (N=4), 3.99× (N=8), **6.39× (N=16)** — the
plan-exact linear sum clips at any i16 output stage from N=2 up. AR's servo
halves RMS and darkens timbre to self-limit. **Genuine AR win on dense sums,
genuine tradeoff:** PAR preserves the plan bit-exactly and clips downstream;
AR never promised plan-exactness and buys headroom with gain/timbre
deviation. Neither is "wrong"; they optimize different things.

## 4. Long-horizon drift (300 s plan, motif at 10 s and 290.0 s, identical params)

| check | par | nat (per-event carried) | natg (global carried) |
|---|---|---|---|
| motif recurrence, 280 s apart (149,940-sample windows) | **0 differ, xcorr 1.000000** | 147,795 differ (LSB-level), xcorr 0.999999 | 149,331 differ, **xcorr 0.513** |
| note-1 pitch Δ (early vs late) | 441.1293 → 441.1293 Hz (Δ 0.000 c) | 441.1291 → 441.1323 Hz (Δ ≈ +0.01 c, estimator/vibrato-phase noise) | — |
| bed tuning @15 s → @285 s | 109.99994 Hz (−0.0010 c) both | 109.99994 → 110.00000 Hz (−0.0009 → +0.0000 c) | — |
| par-vs-X max\|d\| @10 s → @290 s | — | 289 → 360 (0.0044 → 0.0055 FS) | 59,277 both (≈0.90 FS, constant phase offset, not growth) |

**No tuning drift exists in any renderer** (bed ±0.001 cents after 285 s;
motif pitch Δ ≈ 0). The differences are all *phase interpretation*:

- `par` and `nat` are both **event-relative** (par: closed form in
  `t−t0`; nat: accumulator reset per event). Identical event params ⇒
  structurally identical voices; they differ only by the one-time `inc`
  truncation (≤0.0055 FS, bounded, non-growing).
- `natg` (global bin oscillator) does NOT repeat the motif after 280 s:
  each voice is phase-shifted by `frac(f·280)` cycles. 440 Hz realigns
  (123,200 cycles, integer); 369.99 Hz is 0.2 cycles off.

**Minimal probe** (369.99 Hz, two events 10 s apart = 3699.9 cycles,
non-commensurate gap): par **0/15,435 differ, xcorr 1.000000**; nat 0/15,435,
xcorr 1.000000; natg 15,399/15,435 differ, **xcorr 0.4956**. PAR's
event-relative phase makes "repeat the motif" mean *identical bytes at any
plan-time distance for any frequency* — a structural property, not a
tuning accident. The global-oscillator native answers a different question
("the oscillators never stopped"), and its answer is also self-consistent.
**Semantic fork, not a bug on either side** — but it is the precise boundary
of PAR's repetition claim: it holds because phase is event-relative.

## 5. Fault behavior

Fixture: plan_v1 (30 s). `cut` = 3 s.

| fault | par | nat | hybrid v2 |
|---|---|---|---|
| burst: 1024 samples zeroed @3 s | 1,023 diffs (one zeroed sample was already 0), **0 outside footprint** | 1,024 diffs, **0 outside** | **0 diffs** — piece 2 detected 1 fault, healed 1 (exact) |
| DC +0.1 FS (6553) from 3 s → end | residual after DC removal: **0** | residual **0** | residual **0**, but **0 faults detected** — sustained sub-threshold shift is a **documented blind spot** (block RMS barely moves; the 1292-block recovery story does not cover it) |
| `pstate`: phase-accumulator bit-20 flip @3 s | **0 diffs** (no state to corrupt; control clean) | 5,889 diffs, **confined to 3.0026–3.1499 s** (target event 2.8–3.15 s — genuine cascade *within* the voice lifetime, dies at event end) | n/a |
| plan-level dropout: EVENT 12.5 removed | 100,935 diffs, **0 outside [12.5, 14.8)** | 100,934 diffs, **0 outside** | 100,935 diffs, **0 outside** |

**AR (stateful reference) on plan-level dropout:** 101,046 diffs, 0 outside
[12.5, 14.8) — *but* the servo trace shows it is not indifferent: agc/bright/
vibmul swing hard during the span (e.g. frame 600: agc 111,695 vs 62,632,
bright +3 vs −1) and differ for **2 frames past the span end** (frames 637,
638; memoryless proportional servo ⇒ recovery ≈ 2 frames ≈ 46 ms). Output
was unaffected here only because the post-span gap is bed-only and the bed
path bypasses the servo. **Propagation proven** with a probe voice inserted
at 14.82 s (inside frame 638): AR diffs extend to **15.020 s** (+0.22 s past
the removed event's span end); par's stop exactly at 14.800 s. So: output
faults don't propagate in any renderer; *state* faults propagate in `nat`
(within voice lifetime) and in AR's servo (until the memoryless loop
re-converges); PAR has no state to corrupt.

## 6. Truncation probe (RT-EDGE flavor)

Plan truncated @15 s (events with onset ≥15 s removed; 11/23 kept).
par: 481,918 diffs, span **16.000–29.300 s** — exactly the removed events'
active regions, 0 diffs before 16.0 s. nat: 481,911, same span. Legitimate
diffs only; no edge artifacts at the cut in either renderer.

## 7. Per-path wins / breaks / ties

| path | verdict | evidence |
|---|---|---|
| **audio** | PAR WINS on determinism, recurrence, fault containment, exact repetition; TIES tuning (nobody drifts); AR wins dense-sum self-limiting | §§2–6 above |
| **video** (`imagination_discovery/vid/ocean.zag`) | PAR HOLDS for the present renderer | `o_emit_frame(f,…)` computes each frame from the frame index and static deterministic scene functions; no prior-frame buffer is read. "Advection" is analytically encoded from `f`, not simulated carried fluid state. A genuinely history-dependent simulation would need carried state or an equivalent closed form. |
| **dialogue** (`dialogue.zag::do_compose`) | PAR BREAKS at plan formation, HOLDS at realization | `do_compose` is deterministic from explicit inputs, but the surrounding pipeline carries salience, previous-query state, topic stack, user-claim history, contradictions, corrections, ellipsis resolution. Response bytes can be parallel after a response plan exists; conversational plan formation cannot generally be independent per turn/token. |
| **image** (`imagination/design/render.zag`) | PAR HOLDS across images; HOLDS per-pixel only after z-order is explicit; current raster keeps local sequential state | Each screen starts from fresh buffers (no cross-image temporal state). Final pixels *could* be evaluated independently from an explicit ordered primitive stack, but the current implementation uses sequential draw order for overlaps/compositing — draw-order semantics remain local carried state. |

**Hybrid v2 verdict:** clean output byte-identical to PAR (spec holds);
heals large detectable output corruption exactly (burst: 1 detected /
1 healed / 0 residual); **does not detect** sustained +0.1 FS DC shift
(0 faults over 1292 blocks). The "stateful healing without stateful risk"
story is real for abrupt faults and has a known hole for slow ones.

## 8. Limitations (what this report does NOT cover)

- §2 frozen battery: the 9 V10 quality bars, COST (wall/RSS), RT-LONG
  (RESPOND cents), and full CHOP with the audit's 321 list were not run.
- §4 plan-formation parallelism prototype: not built.
- §5 red team: only the permutation probe, truncation probe, and the fault
  models above were run. Sustained 1292-block corruption vs each contender,
  rail-pin plan-text attacks, sub-octave lies, vibrato/glide-vs-ZCR, and
  contender D schemes were not attempted.
- `nat`/`natg` model the surveyed native *patterns* (per-event accumulator;
  per-bin global oscillator); they are not the full `f3_synth` cell pipeline.
- Event-count discrepancy: my independent CHOP-3 list has 296 timestamps vs
  the prereg's 321 — substantive conclusion confirmed, count not reproduced.

## 9. Deliverables

- This report: `bytegen/par_dive/PAR_CHARACTERIZATION.md`
- Sources: `bytegen/par_dive/src/render_fn.zag` (par/nat/natg + fault hooks),
  `bytegen/par_dive/src/render_hyb_t.zag` (test-only `dcmix` mode)
- Plans: `work/plan_drift.txt`, `work/plan_chord{1,2,4,8,16}.txt`,
  `work/plan_solo*`, `work/plan_motif_only.txt`, `work/plan_dropout.txt`,
  `work/plan_shuffled.txt`, `work/plan_trunc15.txt`, `work/gen_events.py`,
  `work/events_complete.txt`, `work/ana.py`
- Excerpts: `work/excerpt_par_2to12s.wav`, `work/excerpt_nat_2to12s.wav`
  (10 s, 2–12 s of plan_v1; 3,801/441,000 samples clip at i16 identically —
  known renderer behavior, not a finding)
- Small text logs: `work/hyb_dropout.log`, `work/hyb_dc.log`

Committed per workspace rules: report + pure-Zag sources + small plans +
compact text logs only. No binaries, no WAV/mix bulk, no `.zagd`, no
`.zag-cache`. `TMPDIR=~/workspace/tmp_commit`, lab-relative paths.
