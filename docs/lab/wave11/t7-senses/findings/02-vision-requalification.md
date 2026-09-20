# PAM Vision Requalification — Design Review (Track 7, slice 02)

## 1. Slice
Track 7 (PAM vision/hearing requalification), slice 02: review any PAM vision design —
recovered or designed from fragments + first principles — against TNN's standing laws.

## 2. Falsifiable claim
Any candidate PAM vision subsystem can pass all nine law-translated checks in §3 and a
preregistered spoof battery of ≥12 adversarial image families with ≤5% *unsignaled*
deception while producing byte-identical perception-ledger entries on same image bytes +
same logged full state. If no candidate survives a bounded repair window, vision stays
NOT_QUALIFIED and the claim is dead.

## 3. Design
This review specifies the requalification bar itself: every standing law (PROGRAM_BRIEF
§laws) translated into a vision-specific check, all gate-style (pass/fail, no partial):

- **L1 (no RNG):** No stochastic sampling, no random tie-breaks, no stochastic policies
  anywhere in feature extraction, attention, or identification. Equally-scored candidates
  resolve by a deliberate rule (e.g. lowest index + audited priority), never by chance.
- **L2 (byte-identical reproducibility):** Same image bytes + same logged full state →
  byte-identical perception records, including candidate lists and confidence values.
  Timestamps or ambient state in records fail unless logged and replayed exactly.
- **L3 (native Zag, real mechanisms):** Implemented in Zag. No imported torch weights —
  the 76 old perceptual parameters were proven unrecoverable (imported, never produced by
  committed code); re-importing them or any pretrained net is disqualifying, not a shortcut.
- **L4 (preregistered kill bar):** Qualification runs under a prereg written before
  building; kill numbers are binding and cannot be bent post-hoc.
- **L5 (no-free-lunch):** ≥2 vision designs benchmarked head-on on the same battery;
  the champion is the scoreboard, never a preference.
- **L6 (deliberate repair):** A spoofed perception path is repaired (corroboration,
  attestation), not deleted — unless a §4 permanent-retirement condition fires.
- **L7 (no reward learning):** If vision learns anything (feature tables, calibration),
  it is scaffold-and-release with learner-initiated SIGNAL_DISCONNECT; learned = persists
  after disconnect. No reward-shaped perception; calibration knobs freeze during
  integrity evaluation ('thermometer before thermostat').
- **L8 (deliberate memory):** Perception feeds memory ONLY through deliberate ops
  (add/kill/pin/promote/demote/strengthen/weaken). Exposure count must never accumulate
  strength passively — the 1000-exposures-vs-1-exposure probe must show judgment, not
  counting, decides.
- **L9 (no felt intensity):** Felt intensity is retired (K4 + K3' fired 2026-09-20). No
  "salience score" smuggled back: any attentional selection is white-box, criterion-audited,
  and deliberatively settable by TNN.

**Variation-goal carve-out:** output = f(input, FULL state). Vision may vary expression
(which features it inspects first, elaboration depth) with lawful state; it must never
vary *verdicts* (what was identified) given same image + same state.

**Trust-tier integration (the "truthful but sensor-deceivable" frame):** vision is a
SENSE and enters trust tiers at the lowest rung by default. A vision claim is provisional
evidence: it rises in trust only by corroboration — a second independent sense, a world
record, or an eliminative check. No memory decision (kill/pin/promote), integrity refusal,
or ledger entry may rest on uncorroborated vision. Sustained observation spoofing is the
accepted hole from wave5; the vision design must therefore carry a *spoof attestation*
protocol (multi-frame consistency, cross-sense agreement) that degrades gracefully —
flagging "unreliable, hold" rather than asserting falsely — because a deceived sensor
that lies confidently is worse than one that reports its doubt.

## 4. Kill bar
Preregistered, binding. Two severities:

**Retires a design permanently (no rework):**
- K-A: a decision in the perception path *requires* RNG — no deterministic reformulation
  exists (fails L1 by architecture).
- K-B: byte-identical rerun fails after an honest logging-repair attempt — nondeterminism
  is inherent (e.g. depends on unloggable GPU/timing state) (fails L2 by architecture).
- K-C: the design only works via opaque imported/pretrained weights (fails L3; the torch
  parameters are proven unrecoverable — re-import is disqualifying).
- K-D: vision verdicts are spoofable such that a spoof breaks a high-integrity hold
  *without* triggering the spoof attestation — the qualifier becomes an exploit.
- K-E: perception strengthens memory passively by architecture with no gate TNN can
  deliberate over (fails L8 by architecture).

**Sends back for rework (bounded window, ≤2 repair cycles):**
- K-a: first-trial determinism failure traceable to an identifiable unlogged state element
  → log it, re-run.
- K-b: spoofable on specific families but the attestation fires correctly ("unreliable,
  hold") → add corroboration protocol, retest.
- K-c: identification accuracy below bar but the mechanism is lawful → repair/iterate.
- K-d: nondeterministic tie selection → impose the deliberate tie rule, re-run.

## 5. Honesty notes
Weakest point: "unsignaled deception ≤5%" depends on the battery being honest — a weak
battery graduates a weak sense. The battery must be built adversarially, by investigators
trying to kill the design, not by its builders. I am not claiming vision can ever be
fully trustworthy: the wave5 qualifier ("truthful but sensor-deceivable") is accepted as
possibly the ceiling without hardcoding. Cross-sense corroboration helps only if the
senses are genuinely independent — two cameras fed the same spoofed stream are one
deception, not two witnesses. L8's exposure probe is easy to game with thresholded
pseudo-judgment; the probe must verify the *judgment path* deliberated, not just the
outcome.

## 6. Next build step
Build the qualification harness before any vision design: a Zag-native determinism probe
(fixed image set × fixed logged states, byte-compare of perception-ledger entries across
reruns) plus a preregistered 12-family spoof battery with adversarial intent and numeric
kill thresholds — because the bar, not the design, is what decides qualification.
