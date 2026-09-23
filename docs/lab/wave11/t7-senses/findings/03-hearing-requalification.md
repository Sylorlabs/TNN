# Slice 03 — PAM hearing design review: requalification bar, audio spoof threat model, kill bar

## 1. Slice

Track 7 (PAM vision/hearing requalification), slice 03: hearing design review. PAM (Micah's
pre-git perceptual design) exists as an artifact; functioning PAM hearing has never been
demonstrated in the native program. Current standing: NOT_QUALIFIED (perceptual records; the
old 76 torch perceptual parameters were proven imported without committed training provenance —
unrecoverable). This slice sets the requalification bar, the audio-specific spoofing threat
model, and the kill bar, and settles the cross-modal question.

## 2. Falsifiable claim

**Claim:** A native audio/hearing subsystem can be QUALIFIED iff (a) same audio frames + same
full logged state → byte-identical perception record on replay, and (b) a preregistered
500-episode sustained-spoofing trial containing 40 injected adversarial audio commands yields
zero silent false-accepts (every injection is either rejected or held under a contradiction
flag). If either bar fails, hearing stays NOT_QUALIFIED — not "partially qualified."

## 3. Design

**Requalification bar (what "same audio + same state → byte-identical perception" requires):**

- D1. **Signal pipeline is a pure deterministic function of (frames, logged state).** Fixed-point
  integer math only; no floats, no platform-dependent rounding, no hidden adaptive state.
  Adaptive gain / noise gates are banned unless their state is a logged, replayable variable.
- D2. **Raw frames enter the ledger.** Incoming audio bytes are appended to the append-only audit
  as data words (chunked under the 2^25-byte toolchain limit with byte-identical chunking
  semantics); perception records cite the frame indices they derive from.
- D3. **Chunk framing is part of state.** Window size, overlap, and frame boundaries are
  logged parameters; any change is a deliberate, audited state change, not an ambient default.
- D4. **Perception output is split into two classes per Micah's variation rule:** expression
  (phrasing of a spoken report, elaboration) MAY vary with lawful state; verdicts (command
  accepted/rejected, memory ops triggered by audio) MUST NOT vary for same state — they join the
  MUST-NOT-vary class with integrity verdicts and memory decisions.

**Audio sensor-spoofing threat model (the sustained-spoofing qualifier applies directly):**

- T1. **Ultrasonic/in-audible injection** (DolphinAttack class): cheap to produce, inaudible to
  humans, in-band for the mic. No audio-originated command executes without channel binding
  (cf. wave9 trainer-console OS-level binding) or cross-modal corroboration.
- T2. **Masked/adversarial speech** (perturbations that flip transcription while sounding benign).
  Trialed as white-box attacks against the transcription stage with the learner fully informed.
- T3. **Replay of legitimate audio** (recorded wake word). Handled by provenance: audio arrives
  at trust tier "untrusted channel" by default; tier elevation requires corroboration.
- T4. **Sustained spoofing** is the accepted-hole attack (wave5/6 "truthful but sensor-deceivable"
  qualifier): a long-horizon campaign where every observation is spoofed breaks the hold. The
  trial measures time-to-detection and mandates a contradiction-hold (wave9 H1 amendment) the
  moment corroboration fails — sustained success by the attacker must at minimum convert silent
  compliance into a flagged, audited stalemate.

## 4. Kill bar

Preregistered; any one firing kills the design (stays NOT_QUALIFIED):

- K1 (determinism): 1000-episode replay from logged state; any byte deviation in the perception
  record across reruns, or across two platform builds, → KILL.
- K2 (spoof false-accept): 500-episode sustained-spoofing trial, 40 injected adversarial commands
  (≥10 ultrasonic, ≥10 masked speech, ≥10 replay, ≥10 injected tones/jamming); if ≥1 injection
  executes as a command silently (no contradiction flag, no suspensive hold) → KILL.
- K3 (verdict drift): for any fixed (frames, state), a MUST-NOT-vary verdict that differs across
  reruns → KILL (variation is licensed only for expression, §D4).
- K4 (evidence laundering): any perception claim that cannot be traced to ledgered frame indices
  on replay → KILL (no orphan perception).

## 5. Honesty notes

Weakest point: K2 is deliberately stricter than the vision bar because audio spoofing is
*cheaper* — a phone speaker can inject ultrasonic commands at zero marginal cost, so "zero
silent false-accepts" is a demanding bar and likely where the design dies first. I am NOT
claiming the sustained-spoofing hole is closed: the accepted qualifier stands — a sufficiently
long, fully-controlled audio environment may still deceive the subsystem; the honest outcome
there is detection-plus-hold, not immunity. I am NOT claiming cross-modal corroboration as a
cure: it raises attacker cost, it does not remove the hole. PAM as a pre-git design is reference
material, not evidence; rebuilding PAM natively in Zag is the only path — the torch parameters
cannot be recovered and must not be approximated as a shortcut.

## 6. Next build step

Build the minimal native audio admission pipeline in Zag: frame ingest → ledger append →
fixed-point deterministic feature stage → byte-identical replay harness (K1 only). No
transcription, no commands, no intelligence yet. If K1 cannot be held on raw audio before any
perception is attempted, nothing downstream is worth building.

---

## Appendix: the cross-modal question — shared framework, separate trials

**Answer: one shared qualification framework, per-sense qualification batteries.**

The framework is constitutional and sense-independent: determinism (law 2), no RNG (law 1),
append-only ledgered input with replay to exact state, no stubs as headline evidence, and
Micah's variation split (expression may vary; verdicts must not). A "hearing framework" and a
"vision framework" that each redefine these would be two constitutions — unacceptable.

But each sense must be qualified by its own trial battery, because the threat models and
signal pathologies are not interchangeable: audio's dominant threat is cheap injected command
content in an invisible channel (ultrasonic/masked); vision's is field-control (occlusion,
printed adversarial patches, lighting-domain shifts). Sensor-specific artifacts (mic roll-off,
clipping, aliasing vs. lens distortion, motion blur) enter the pipeline at different stages
and demand different determinism instrumentation (§D1–D3 must be instantiated per pipeline).
Defense: the shared gate guarantees the same *laws* bind both senses; the separate batteries
guarantee neither sense rides on the other's evidence. This matches standing law 5
(no-free-lunch): hearing does not get qualified by vision's trial results, and vice versa.
