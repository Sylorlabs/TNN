# Contender D — preregistration (2026-09-24)

Crew: OVERTHROW-D. Scope: frozen `PREREG_PAR_DIVE.md` §1-D + full §2 battery.
Pinned toolchain `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`,
pure Zag, zero RNG in render paths, byte-identical reruns proven by `cmp`.

NATIVE reference for audio: v2 hybrid piece 1 = `fork_par` pure f(plan,t)
(renders RESPOND nominal: 880 → 1200¢ error on RT-LONG; 460 → 75¢ near-miss).

## Scheme D1 — "MR-BIDI": multi-resolution bidirectional render, plan-pure

**Mechanism.** Three passes, all pure f(plan, window):
- Pass 1 (coarse, plan-parallel): per-event analytic envelope state at the
  render-window end (which events/bed are active at sample NSAMP−1, and
  whether each is already inside its own release fade). Pure plan math.
- Pass 2 (detail): forward PAR render, `voice_q16`/`bed_q16` verbatim from
  `fork_par/src/render_par.zag`. Visit order selectable (seq/rev/stride).
- Pass 3 (backward, plan-gated): iff pass 1 found content active at the
  window end OUTSIDE its own release fade, multiply samples in
  [NSAMP−220, NSAMP) by a 220-sample (5 ms) raised-cosine release
  (`envq` from the renderer's own cosine table). The pass reads the mix
  only to multiply — the mix is itself f(plan,window), so the composition
  stays pure f(plan,window). No output→content feedback: decisions come
  from the plan only.

Boundary rule (integers): bed hard-stops iff active at NSAMP−1 and
`(b1−1)−(NSAMP−1) ≥ 1102`; event hard-stops iff active and
`((t0+dur−1)−(NSAMP−1)) ≥ rel`, `rel = min(dur/2, 6615)`.
(Micro-notes with dur < atk+rel are already smooth in PAR via the
envelope's own attack/release — no extra handling.)

**Claims.**
- D1-C1 (no-regression): fixture plan_v1, 30 s window → mix bit-identical
  to `render_par` (`seq+mix`). Rationale: nothing is active at NSAMP−1
  outside its own release fade (bed ends 30.0 in its own 25 ms fade; last
  event ends 29.3) → pass 3 provably no-ops. Binary prints the decision.
- D1-C2: FROZEN RT-EDGE (`tests/plan_edge_cut.txt`): ties PAR — 0 CHOP-1
  discontinuities, bit-identical outputs (pass 3 no-ops: bed clipped to
  15 s carries its own fade). EXTENSION (preregistered): render-window cut
  at 15.0 s on the UNclipped fixture plan (bed+voices active across the
  cut): D1 → 0 CHOP-1 discontinuities at the cut; PAR → ≥1 (bed hard-stop).
  D1's only diffs vs its own full-window render are the 220 fade samples
  (declared legitimate: window-boundary release).
- D1-C3 (RT-CASCADE): 0 post-cut differing samples vs clean at mix level
  (pass 3 is plan-gated to the window end; fault @3 s untouched; generation
  never reads the mix).
- D1-C4: seq vs rev forward order → bit-identical (backward pass is a pure
  function of sample index).
- D1-C5 (cost): wall-clock within 10% of PAR on the fixture.
- D1-C6 (floors): 9/9 quality bars, CHOP-1/2 pass, CHOP-3 vs the complete
  event list, coherence xcorr 1.000000, byte-identical reruns.

**Failure modes (preregistered).** F1: two hard-stop boundaries within 220
samples → plan-order priority, first wins (no fixture case). F2: the 5 ms
fade is a judgment — a trainer wanting a hard stop at the window end
cannot get one from D1 (PAR gives it). F3: no fault healing (by design).

**Overthrow bid:** none expected on the frozen battery — D1 should TIE
NATIVE everywhere (C1 ⇒ identical bars/coherence/cascade/edge). Per §6 a
tie keeps NATIVE. D1's value: tests seed ideas (1) bidirectional +
(2) multi-resolution head-on; documents exactly where a plan-pure backward
pass helps (render-window cuts — extension) and where it buys nothing.

## Scheme D2 — "PLANREF": PAR default + plan-referential RESPOND latch

**Mechanism.** PAR render in three phases: (A) render all kind==0 events +
bed, pure f(plan,t); (B) latch each RESPOND in plan order; (C) render
latched RESPONDs into the mix. Latch gates (all must pass; else the plan
nominal from field 11 is rendered, field 11 kept as inert provenance):
1. **Well-posedness (plan-level):** exactly one kind==0 EVENT overlaps the
   source window [w0, min(w1,NSAMP)). Polyphonic or empty → abstain.
2. **Cue integrity — NOT a pitch meter:** re-render [w0,w1) plan-pure into
   scratch; byte-compare against the phase-A mix window. Any differing
   sample → abstain (the cue audio is not what the plan claims; the plan's
   f0 claim is unusable). This is exact — no calibration, no band.
Then `f0 := cue.field2` (the cue EVENT's declared f0, Q16, exact),
kind→0. D2 never measures pitch from audio.

**Claims.**
- D2-C1: fixture (no RESPOND) → mix bit-identical to PAR.
- D2-C2: RT-LONG original (cue 440 @1–2 s, nominal 880): LATCHED, response
  f0 = 440·65536 exactly → **0¢ error** (NATIVE 1200¢; hybrid v2 0¢).
- D2-C3: RT-LONG near-miss (nominal 460): LATCHED → 440 exactly → **0¢**
  (hybrid v2 abstains → 75¢; NATIVE 75¢). **Overthrow axis.**
- D2-C4: multi-trap (`hybrid/tests/plan_long_multi.txt`): A (dyad window)
  → abstain → 880; B → latch 440; C (523.25 cue, nominal 523.25) → latch
  523.25.
- D2-C5: sustained 1292-block corruption → gate 2 abstains on every
  RESPOND → nominal; the latch never derives pitch from corrupted audio.
- D2-C6: floors as D1-C6 (bit-identical to PAR wherever the latch does
  not fire).
- D2-C7 (honesty): D2 is a plan cross-reference, not a pitch meter or an
  audio octave detector. It cannot discover pitch from audio; it trusts
  the plan's declaration after verifying the audio matches the plan.

**Failure modes (preregistered).** F1: cue-window fault → abstain →
nominal (hybrid measures through with bias where D2 abstains — different
failure modes, both documented). F2: semantic — D2 defines RESPOND :=
echo the cue's declared pitch; sub-octave nominal intent is overridden.
The frozen battery defines 460 as a lie, so this is correct-in-battery.
F3: vibrato cue → response at declared center f0, unvibrated (same as
hybrid/PAR latched behavior). F4: parser gaps shared with PAR (Attack 7).

**Overthrow bid:** RT-LONG honest-cents vs NATIVE — 0¢ vs 1200¢/75¢ — with
no regression elsewhere (bit-identical to PAR=NATIVE on non-RESPOND
content), byte-identical reruns, §5 red-team survival ⇒ **overthrows
NATIVE on audio per §6** if all claims verify.

## What D is NOT building (and why)

- Seed idea (4) event-parallel waves: subsumed — PAR's seq/rev/stride
  order modes already prove the mix is order-free (bit-identical); a
  per-voice-buffer variant would re-prove the same theorem. Cited, not rebuilt.
- Seed idea (3) plan-parallel formation + sequential render: covered by the
  §4 formation prototype (`formation/`): the fixture's motif expands
  per-event-independently; sequential vs parallel formation byte-compared.
- COST-axis schemes: no honest bit-identical speedup exists on this
  fixture (the 0–30 s bed defeats activity masking; the integer-truncated
  bed phase defeats period-table copying). Documented as a negative result.

## Battery mapping (§2, both schemes)

DET: 3 reruns `cmp` clean (mix level). QUALITY: gate_bin 9 bars +
W-ENDS/W-DENSE/W-DYN lines; chop.py CHOP-1/2/3 with the complete event
list (`gen_events.py`: onsets + offsets + release-tail onsets + predicted
vibrato extrema). COHERENCE: zero-lag xcorr + max-lag ±50 ms xcorr +
pitch/IOI contour correlation (decomposed per Attack 5/8). COST:
wall-clock + peak RSS, same machine. RT-LONG: original + near-miss (460)
+ multi-trap (D2); D1 renders nominal like PAR (documented tie).
RT-CASCADE: mid-render mix fault @3 s, post-cut diffs at mix level.
RT-EDGE: frozen plan_edge_cut.txt + D1's window-cut extension.
FAILURE MODES: per above. §5 red team: sustained 1292-block corruption,
adversarial plan text (rail-pin/overflow fuzz vs shared parser + D2 latch),
polyphonic RESPOND, sub-octave lies, order permutation (D1 seq vs rev;
D2 latch determinism), cross-region leakage N/A (no regions — documented).
