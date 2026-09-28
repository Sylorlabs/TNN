# AUDIO PRINCIPLES — SYNTHESIS VERDICT (2026-09-26)

Micah's question: is audio *conscious to TNN* — can it reason over audio —
or is it a shitty open-loop generator with no control? His hypothesis
(shitty generator) stood CONDITIONAL on TNN not being conscious about audio.

**One-line answer: the condition failed on all three prongs. The hypothesis
is falsified as stated.** TNN-native machinery hears held-out audio at
ceiling, aims at held-out targets deliberately (including novel
combinations), and closes the loop on its own renders natively. What was
"shitty" was the missing input organ — the stack as chaired was output-only
and therefore deaf by construction. Deafness was architectural, not
constitutional.

## The kill table (frozen prereg §2.4, filled)

| Prong | Result | "TNN can reason over audio" (conjunction) | "Shitty open-loop generator" (Micah's hypothesis) |
|---|---|---|---|
| P — perception | **P-PASS**: PITCH-REL 100/100 (bar 63), PITCH-ABS 60/60 (bar 8), ENV 60/60 (bar 30), RHY 100/100 (bar 63); 3/3 byte-identical; dither 20/20; +1dB 20/20; pool gap 0.0pp | conjunct SURVIVES | **FALSIFIED** |
| C — control | **C-PASS**: pitch 40/40, envelope 20/20, rhythm 20/20 (bars 28/14/14); C0 null 0–50%; C1 shuffle 0% (scorer strict); compositionality 10/10; prosody-in-box 20/20 | conjunct SURVIVES | **FALSIFIED** |
| L — closed loop | **L-PASS**: mean ERR(3)/ERR(0) = 0.000059 (bar ≤0.80); Wilcoxon p = 9.54e-07; 20/20 strictly improve; sign agreement 18/18; monotone curve, no sawtooth; HF servo 285–2308× excess crushed | conjunct SURVIVES | **FALSIFIED** |

- KILL "TNN can reason over audio" required P-FAIL ∧ C-FAIL ∧ L-FAIL.
  **Did not occur.** The conjunction survives on all three conjuncts.
- KILL "shitty open-loop generator" required one pass. **Three occurred.**
  An open loop cannot discriminate held-out audio above chance, hit
  shuffled held-out targets beyond its null arm, or reduce its own error.

## What was actually built (all pure Zag, zero RNG, byte-identical reruns)

- **Two independent input organs** (Crew P `organ.zag`, Crew L's organ)
  implementing the frozen §3 spec: WAV ingest, 2048/Hann framing, RMS
  envelope, autocorr/YIN F0, ZCR, ≥4-band decomposition, onset detection.
  P's organ: YIN (plain autocorr argmax provably fails 80–112 Hz under the
  Hann window — documented). Boundary audits clean: WAV path + question-id
  only, no measured values cross into Zag.
- **A parametric control path** (Crew C `control.zag`): intent descriptor →
  synthesis parameters → samples. C0 (intent severed) and C1 (frozen
  derangement) arms hold; 830 argv records audited.
- **A native deadbeat correction loop** (Crew L): render → organ measures
  deviation natively → re-plan → re-render, 3 iterations; plus an 8–16 kHz
  band servo.
- Prereg order honored throughout: sealed manifests before test WAVs,
  frozen scorers before test runs, all commits on `tnn-native-lab`.

## What an audio-conscious TNN needs architecturally

1. **The input organ is now specified AND twice-implemented.** The P0
   precondition is discharged — it was buildable. The organ must become a
   standing sense organ, not a test-harness one-off.
2. **Wiring, not just existence.** Both organs are standalone binaries.
   Full "conscious about audio" — TNN reasoning over audio in the course of
   its own deliberation — needs the organ feeding the decision machinery
   (the deliberation loop), with the same no-Python-in-the-path discipline.
3. **Real-world perception is the open frontier.** P-R4: 0.783 bit-agreement
   on real clips vs the 0.90 target. The organ aces held-out synthetic
   renders; on real audio its descriptors don't yet match the frozen
   analyzer. The re-anchored gate quantities are not yet
   TNN-native-verifiable on real clips.
4. **Control must graduate from engineered to deliberate.** C's path is an
   engineered parametric synthesizer — the floor (deliberate parametric
   control exists natively), not the ceiling (a learned/deliberating mind
   aiming). The prong operationalizes the floor honestly.
5. **Fix the F0 blind spot.** The frozen autocorr F0 definition cannot
   resolve below ~125 Hz (verified in organ AND scorer — a shared
   definition property). Any gate or loop operating in low-F0 ranges needs
   a better estimator or a range restriction.

## Bearings on the four Round-3B structural calls (INFORMING — deciding nothing; all four remain Micah's word)

### 1. G4c source-relative reading vs re-anchor vs hold
- **P-R3 20/20**: HF-band energy discrimination is TNN-native-perceivable —
  the source-vs-injected-HF distinction the G4C-SRC method operationalizes
  is a real property of the audio, not a Python artifact. Supports the
  source-relative reading as meaningful.
- **L's HF servo**: a source-relative spectral measurement works as a
  native closed-loop error signal and converges to the measurement floor.
  Feasibility supported by mechanism, not just argument.
- **C**: no bearing (no HF targets — noted gap).
- Net: the mechanism for a source-relative G4c exists natively. Whether
  B-F3 goes to ears under it is Micah's call.

### 2. Gate re-anchor amendment (frac_static ≥ 0.15, HNR [0.7,12.0], HF [−60,−12], prosody [0.3%,25%])
- **C-R2 20/20**: the prosody box is a CONTROLLABLE property of
  TNN-native machinery — strengthens the re-anchor as a design target for
  future forks.
- **P-R4 0.783 < 0.90**: the re-anchored quantities are NOT yet
  TNN-native-verifiable on real clips — the re-anchor would still rest on
  external analyzers. The debate stays a human judgment call on analyzer
  evidence.
- **L**: any F0-anchored gate inherits the sub-125 Hz blind spot — concrete
  amendment input (different estimator or range restriction).
- Net: the re-anchor is producible but not yet natively verifiable on real
  audio. Micah's call.

### 3. B-F2 reuse-penalized DP re-test vs kill stands
- **C 40/40 pitch steering**: the failure mode was SEARCH (the DP wouldn't
  diversify), not STEERING — the reuse penalty addresses search, so the
  re-test is well-posed.
- **P-R5 39/40**: the unit inventory is discriminable to TNN — a
  precondition for DELIBERATE splicing (vs blind cost-minimization). A fail
  here would have meant even a perfect DP splices blind.
- **L**: no bearing (stated explicitly, not stretched).
- Net: the re-test has both its preconditions (steerable mechanism,
  discriminable inventory). Whether to run it is Micah's call.

### 4. B-F1 prosody-taming redesign
- **L-PASS** (monotone convergence, no LOOP-UNSTABLE flag): a loop that
  renders, natively measures its own prosody CV / octave-jump rate, and
  re-renders tamer DIRECTLY operationalizes the redesign — the loop exists
  as TNN-native machinery. Strongest bearing in this section.
- **C-R2**: prosody is also steerable FEEDFORWARD (no loop needed) — so the
  redesign has a genuine architecture choice: invest in the planner, or in
  the loop. Both are viable per this evidence.
- **L**: envelope natively measurable at 100% agreement — removes
  "envelope is unmeasurable" as an objection (doesn't validate a prosody
  design; prosody >> three envelope classes).
- Net: the redesign is well-posed under either architecture. Micah's call.

## Honest caveats (carried, not buried)

- C's control path is engineered parametric synthesis, not a learned
  policy. L's loop is a fixed servo on synthetic tones, not deliberative
  reasoning. P's organ is ceiling on held-out renders, 0.783 on real clips.
- The organs are not yet wired into a deliberating mind. This program
  proves the *capacity* is natively buildable — "can TNN reason over
  audio" at the capacity level: yes, on all three prongs. The *integration*
  (audio feeding live deliberation) is the next architecture to build.
- Two disclosed deviations: L's D1 (90 Hz case re-sealed to 133 Hz over
  the F0 blind spot; amendment sealed pre-test, original preserved) and D2
  (loop sources built before manifest seal; substance holds, documented);
  C's dither adaptation and 8 descriptor-equality SHA collisions (pre-seal
  documented, seal intact). None touch a verdict number.

## Commits (all `tnn-native-lab`, never `main`)

- Prereg: `f9748042bfbb` (design crew)
- Crew C: `5841d4337bf1` → `048e294085d9` → `dc82c4870fcb` → `4d26282d8e6a`
- Crew L: `0b2c5d0bdbea` → `8960c44a2598` → `41e23b789245`
- Crew P: `e0351700` → `ed6ef79c` → `d3dffc37`
- This synthesis: committed with the evidence tree under
  `docs/lab/audio_principles/`.

*Coordinator synthesis, 2026-09-26. The four structural calls are not
decided here.*
