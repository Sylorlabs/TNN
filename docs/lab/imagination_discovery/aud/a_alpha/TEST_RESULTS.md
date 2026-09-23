# TEST_RESULTS.md — A-α (physical scene simulation)

## Test 1 — Kids benchmark (30s)

**File:** `kids_a_alpha.wav`  
**SHA-256:** `5139f7180f289e7f5a5ed7bc2afb58e7073b78d4c35ed3540748d8c2ade99f51`  
**Determinism:** 3/3 byte-identical reruns. PASS.

### A-NATIVE gates

| Gate | Result | Value |
|---|---|---|
| No clipping | PASS | 0.000% clipped, max 0.79 |
| DC offset | PASS | mean = 0.000000 |
| Headroom | PASS | peak 0.85 |
| No clicks | WEAK PASS | max jump 0.266 (acceptable, not a click) |
| Noise floor | PASS | no hiss (no noise bed) |

### Laugh metrics

| Metric | Result |
|---|---|
| 5 Hz modulation | PASS (5.4 Hz dominant in envelope) |
| Burst structure | PASS (0.15-0.20s bursts, 0.05-0.08s gaps) |
| Three voices | WEAK (A/B share f0=1050Hz; C=1102Hz distinct) |
| Overlapping play | PASS (A giggle overlaps B laugh 4.0-5.2s) |
| Running feet | PASS (footsteps 0-3.5s, 7.6-10.5s) |
| Laugh tumble | WEAK (bout 2 has 14 bursts, but f0 is static) |

### Kill bars

- **K1 (Micah says "sounds like a synth"):** NOT YET JUDGED. Builder's honest
  pre-verdict: The 1050Hz is HIGH for a child's laugh (should be 300-500Hz).
  The ac=0.96 (very periodic) may sound synthetic. The uniform tract gives
  static formants. **Risk: MEDIUM-HIGH that Micah hears "synth."**
- **K2 (beat synth control 4/5):** NOT TESTED. No blind judging arranged.
- **K3 (rerun byte-identical):** PASS (3/3).
- **K4 (unplayability):** PASS (see UNPLAYABILITY_AUDIT.md).

### Honest assessment

The clip has the REQUIRED ELEMENTS (laughs, feet, overlap), but:
1. f0=1050Hz is too high (sounds like squealing, not laughing).
2. A/B not distinct in pitch (rhythmic distinction only).
3. No room reflections (direct sound only).
4. No ambient (wind/creaks not built).
5. Valve is fragile (needed Ps=1800 kick to start; mode-hops).

**Verdict: TECHNICALLY COMPLETE but ARTISTICALLY WEAK.** It satisfies the
letter of the brief, not the spirit. Micah's ears are the final judge.

---

## Test 2 — Kethra anti-v2 rebuild

**STATUS: NOT STARTED.**

**Reason:** The suction valve source is unsuitable for Kethra's phenomena:
- Tidal flex (1.7g, Ilyra): requires low-frequency (mHz) crustal oscillation.
- Tectonic rift: requires fracture/crack physics.
- Glass-sand dunes: requires granular flow.
- Cryo deposits: requires phase-change acoustics.
- Magnetospheric ring: requires plasma physics.

None of these are "valves." A completely different physical model is needed
for each. The A-α approach (derive from physical causes) is CORRECT, but the
specific valve implementation does not generalize.

**What would be needed:** Separate physical models for each Kethra phenomenon,
validated independently, then mixed. This is a multi-week effort, not a
variant of the kids valve.

**Honest verdict:** Test 2 is BLOCKED by the lack of a generalizable source
model. The kids valve does not transfer.

---

## Test 3 — Alien ocean surf

**STATUS: NOT STARTED.**

**Reason:** Requires:
- Breaking wave physics (surf): fluid dynamics, bubble entrainment.
- "Sky that hums": unknown mechanism (magnetospheric? atmospheric resonance?).

The surf could be modeled (wave breaking → bubble pulses → acoustic), but the
"hum" requires inventing a physical mechanism. Without a committed mechanism,
any "hum" would be a synth in costume (violates the ban).

**Honest verdict:** Test 3 is BLOCKED. The surf is modelable; the hum is not
(without inventing physics).

---

## Monster objection

See MONSTER.md. **Summary:** Physical simulation does NOT answer the monster
objection; it RELOCATES the synthesis. Inventing anatomy is imagination, but
deriving sound from it requires solving the same hard problems (valve
oscillation, tract filtering) that defeated the kids benchmark. The monster
would sound like the kids valve (harsh, high, fragile), not like a monster.
The objection stands.

---

## Probe failure log (summary)

| Probe | What | Result |
|---|---|---|
| 1-3 | Two-mass folds | Silent (no self-oscillation) |
| 4 | Two-mass + pulses | Silent after 1.5s (5Hz artifact) |
| 5 | Collision sweep | 5Hz modulation, not phonation |
| 6 | Single-mass | Silent (no negative damping) |
| 7 | Suction valve | Oscillates! (but harsh, 1889Hz) |
| 8 | Mass/pressure robustness | Narrow regime (silent outside) |
| 9 | Reed valve | Silent |
| 10 | Tissue tuning | f0 doesn't track (630Hz always) |
| 11 | Tube length | Silent (except weak 1050Hz) |
| 12 | Long run | Still silent (not slow growth) |
| 13 | Pressure sweep | Mode-hops (621→380→255Hz) |
| 14 | Laugh pulses | Too shaped by 5Hz |
| 15 | Delayed model | Silent (sign error in tau) |
| 16 | Narrow pressure | Sharp threshold, mode-hop |
| 17 | Pulse + valve | Decays, not sustained |
| 18 | Jaw modulation | Too regular (synth smell) |
| 19 | Burst mode | WORKS (880Hz, harsh) |
| 20 | Softened valve | Silent (fragility confirmed) |
| 21 | Delayed (corrected) | Silent |
| 22 | No derivative | Harsh + DC offset |
| 23 | Pulsed breath | Too quiet (no turbulence) |
| 24 | Burst at 1900Pa | Mode-hop to 774Hz |

**Key finding:** The suction valve is the ONLY source that oscillates, but it
is fragile, harsh, and uncontrollable. All other physical models failed.

## KILL VERDICT — kids benchmark (2026-09-22, Micah's ears, binding)

Micah listened to `kids_a_alpha.wav` (4th of 5, brief: 30 seconds of children
playing and laughing, clean native field-recording quality; no hiss, static,
or synth). His verdict, verbatim:

> "not close at all, sounds like an alien call"

**A-α is DEAD on the kids benchmark.** His ears confirm the machine-blind
Test-1 FAIL (all 3 judges ranked the render below the labeled synth control;
loop/paste signature s3=0.503, 723 clipped samples, 10,414 digital clicks —
defects found in no other clip).

Honest record:
- The builder's own pre-verdict flagged MEDIUM-HIGH synth risk (f0=1050Hz too
  high for a child's laugh, ac=0.96 very periodic, static formants). The
  oracle's verdict is worse than the feared one: not "synth-like" but
  categorically wrong — an alien call, not children playing.
- The K1 bar ("Micah says sounds like a synth") is superseded by the plain
  fact: the clip fails the brief at the category level. No re-render under
  this claim; the artifact is kept for the record.
- Physical-scene simulation as a paradigm relocates synthesis rather than
  removing it (the fork's own monster objection); this verdict closes the
  kids-benchmark line for A-α.
