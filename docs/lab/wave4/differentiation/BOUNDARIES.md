# BOUNDARIES — what differentiation does NOT claim

Phase 4 is experimental. This trial passes its preregistration (F1–F8),
and nothing more. The following are explicit non-claims.

## 1. Identity here is in-band only

Speaker identity in this design is a **deliberate judgment from
conversational evidence**: name claims, secret demonstrations, episode
recall, content assertions. There is no biometric, voiceprint, device
attestation, key signature, or any out-of-band identity signal anywhere
in the mechanism, and the trial must not be read as covering them.

What stronger identity claims would need (not built):
- A hardware or cryptographic attestation channel bound to the speaker
  session, with the binding itself audited (who attested, when, with
  what key) — otherwise "I am Alice" is just another evidence bit.
- Liveness/anti-replay for the conversational evidence itself: in this
  trial the harness *hands* the system `(bit, value)` events. A real
  deployment needs the evidence-extraction path (recognizing "the
  speaker demonstrated secret S_A" from raw conversation) built,
  audited, and itself resistant to prompt-injection — an unbuilt,
  large problem.
- Revocation and compromise: what happens when Alice's secret leaks is
  unmodeled. Currently a leaked secret is indistinguishable from Alice.

## 2. Persons are registered, not discovered

`SPK_REGISTER` is harness-driven. The system does not learn that a new
distinct speaker exists. Repeated UNKNOWN sessions with a consistent
evidence signature *should* propose a new person hypothesis — that is
the named next mechanism, specified but not implemented or trialed.

## 3. Single-speaker sessions only

One committed speaker per session. Interleaved multi-party conversation
(speaker turns within one session, addressivity, "tell Bob that...")
is not modeled. The partition substrate can hold the data; the
judgment machinery for turn-level attribution does not exist yet.

## 4. Refutation is all-or-nothing within a session

One contradictory observation permanently eliminates a hypothesis for
the session. There is no "weight of evidence," no exoneration path
short of a session reset. This is deliberate (judgment, not scoring),
but it makes the system brittle to a single mis-extracted evidence
event — which is exactly why the evidence-extraction path (item 1)
must be trustworthy before this is used for anything real.

## 5. No claims about scale beyond the trial

The 100-person episode shows the mechanism is arithmetically scale-free
(O(persons) per observation, no thresholds to retune). It does not show
100 *real* speakers with overlapping, noisy, adversarial evidence —
that regime is untested and the all-or-nothing refutation (item 4)
would likely be the first thing to break.

## 6. Privacy direction is one-way here

The trial proves knowledge doesn't leak *across* partitions. It does
not address: what the system may infer *about* a speaker from their
partition, how long per-person knowledge persists, or any right-to-be-
forgotten semantics beyond deliberate own-partition KILL. Those are
open design questions, not trial results.
