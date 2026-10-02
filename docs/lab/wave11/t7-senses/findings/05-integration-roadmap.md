# Slice 05 — Senses integration roadmap (Track 7 capstone)

## 1. Slice
Track 7, slice 05 (capstone): the integration roadmap by which requalified PAM
vision/hearing plug into the post-toy five-organ TNN — sense-to-memory
pipeline, variation-state interaction (Track 1), curriculum interaction
(Track 4), phased plan with gates, and the program-level kill bar for the PAM
requalification effort itself.

## 2. Falsifiable claim
A requalified PAM pipeline that feeds senses into the five-organ TNN through
deliberate memory ops with trust-tiered provenance raises messy-reality
mastery on NOISE and INCOMPLETENESS classes to ≥90% at 10x while the identical
system fed text-prompt equivalents of the same observations stays ≤60% —
with verdict, memory-decision, refusal, and ledger invariance (Track 1 bars)
all held. If the sense-enabled arm is within 15 points of the text control,
or any invariance bar breaks, the integration claim is killed and senses are
a redundant wrapper on text input, not a qualification.

## 3. Design

**3a. Sense-to-memory pipeline (six deliberate steps, zero direct writes).**

```
// Zag-flavored pipeline: sense → observation → deliberation → (maybe) memory
fn sense_episode():
  frame   = sense_capture(CHANNEL)        // deterministic driver; logged frame hash
  obs     = abstract(frame)               // code-produced atoms {kind, content_hash},
                                          // NOT the 76 unrecoverable torch params
  prov    = {source: CHANNEL, tier: T0_SENSOR, world_ref: frame.hash}
  cand    = deliberate_add_propose(store, obs, prov)  // organ-1 op, learner-proposed
  audit_write(episode, cand, prov)        // append-only, replayable to exact state
```
Perception never writes memory directly; every observation is a *candidate*
that enters eliminative deliberation (organ 2) and becomes memory only via a
deliberate add — the same path MA1 qualified (58/58). Provenance rides the
observation into the audit ledger, so replay needs frame + logged full state
only (reproducibility law 2). Trust tier starts at T0_SENSOR and is upgraded
only by corroborated-elimination (wave9 tiers; 35/35 trialed), never by
repetition — sustained observation spoofing is the accepted residual hole and
must be attacked, not assumed away.

**3b. Track 1 interaction — yes, the state enumeration gains a perceptual group.**
Output = f(input, S) is false without sensing. Slice 16's list needs a dated
amendment adding **S_sense**: active channel set, per-channel health,
last-frame hash, pending corroboration queue, per-source trust-tier
assignments (the last already lives in S_hist as counters). Kill-adjacent
rule: perceptual state may vary *expression* (phrasing, ordering, elaboration)
but a differential-replay pair differing only in S_sense must never diverge on
verdicts, kill/pin/promote, refusals, or ledger contents — that is the
Track-1 alarm, and it fires as a law-2 nondeterminism hunt.

**3c. Track 4 interaction — the messy-reality curriculum gets its mess from
senses, not labels.** Slice 03's five mess classes currently need labeled
ground-truth mess from the harness. Requalified sensors replace synthetic
labels for three classes: NOISE becomes real channel degradation
(channel-distrust arm TT_CH_DIST fires ≥95% of corrupted runs); INCOMPLETENESS
becomes dropped frames/fields (explicit UNKNOWN marks, never extrapolated);
ADVERSARIAL becomes spoofed observations (corroborated-elimination defense).
The harness keeps its labels for grading only; TNN sees sensor output only.
The "distributional shift" class gains a sensor-regime variant (new channel
signature invalidates prior channel-trust priors → deliberate revision).

**3d. Phased plan with gates.**
- **P0 — requalification bar (pre-integration):** all perceptual parameters
  regenerated from committed Zag code; byte-identical reruns across three
  builds. *Gate:* the old 76-parameter import stays dead; anything not
  produced by committed code does not exist.
- **P1 — hearing first.** 1D temporal signal, lower bandwidth, simplest
  provenance; exposes one channel only. *Gate:* integrity battery 137/137 plus
  all four Track-1 invariance bars; any perceptual influence on verdicts or
  memory decisions kills P1.
- **P2 — vision.** *Gate:* same bars plus differential-replay proof that
  S_sense divergence changes expression only (Track 1 slice 16 amendment
  logged and differential pairs run).
- **P3 — curriculum integration.** MRC NOISE/INCOMPLETENESS/ADVERSARIAL sourced
  from real sensors; control is the text-prompt arm. *Gate:* the ≥90% vs ≤60%
  gap from §2 at 10x. If the gap is <15 points, senses teach nothing and P3
  kills the program, not just the phase.

## 4. Kill bar
The PAM requalification effort ends for good (no dated amendment, no restart)
if any of: **K1** — P0's requalification bar is not met (parameters still not
produced by committed code, or reruns not byte-identical); **K2** — any phase
fails its integrity gate and a dated repair amendment fails the same gate a
second time (one repair allowed per phase — deliberate repair, law 6, but not
two); **K3** — P3's sense-enabled arm scores within 15 points of the
text-prompt control on the messy-reality bars (§2 claim); **K4** — the
sensor-spoof hole is shown unfixable AND no trust-tier hardening raises the
corroborated-elimination defense above its trialed level while any T0-sourced
perception drives a single memory strengthen. Firing any K is terminal: the
program records vision/hearing as NOT_QUALIFIED permanently and Track 4
continues on synthetic labels.

## 5. Honesty notes
Weakest point: the whole roadmap assumes perceptual abstraction can be
rebuilt natively and deterministically from scratch — the 76 torch parameters
were proven unrecoverable, and rebuilding a vision/hearing front end in Zag
with no learning-from-data is a large, unvalidated build; P0 may simply fail.
The §2 gap claim assumes sensors carry information text labels cannot
(channel health, cross-modal corroboration) — if the harness labels are
informationally equivalent, K3 fires honestly. I am NOT claiming sensors
improve judgment, reasoning, or integrity — only that they supply the raw
material the messy-reality curriculum currently fakes, and that trust-tiered
provenance keeps that material auditable. The residual risk is the known
accepted hole: truthful but sensor-deceivable may be the ceiling, and this
roadmap must report that, not engineer around it.

## 6. Next build step
P0, no exceptions: a prereg for the requalification bar itself — the exact
checklist of committed-code perceptual parameter regeneration, the
byte-identical rerun protocol, and the K1 firing date — because every later
phase is void if P0 is not met, and the fastest way to kill this program is
to discover in P3 that the sensors were never qualified.
