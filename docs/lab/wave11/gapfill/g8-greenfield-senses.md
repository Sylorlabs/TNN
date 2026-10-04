# G8 — Greenfield deterministic sense design (T7, "fragments only" branch)
## 1. Slice

T7-Senses gap-fill G8: a from-scratch, pure-Zag vision/hearing front-end with zero
archaeology dependency — the design T7 builds if the PAM dig returns "fragments
only" or "confirmed absent." Hearing first (T7 slice-05 roadmap); vision follows
the same contract.

## 2. Falsifiable claim

A pure-Zag hearing front-end using **zero learned parameters** — fixed-point integer
math, fixed logged parameters, code-computed features — produces byte-identical
observation atoms from the same audio bytes + same logged full state, and admits
zero silent false-accepts in the preregistered 500-episode / 40-injection spoof
trial (every injection is rejected or held). If any episode replays non-identically
or ≥1 injection executes silently, the design is dead and T7 stays on synthetic
labels with senses NOT_QUALIFIED permanently.

## 3. Design

**3a. Pipeline — all code, no trained weights, no archaeology.**

```
// SENSE-CONTRACT v0 (hearing): sensor → features → memory-candidate
const WIN: i64 = 256      // samples/frame; LOGGED state params, not ambient
const OVERLAP: i64 = 128  // changing either is a deliberate audited state change
fn sense_hear(raw: []u8) -> [Observation]:
  ledger_append(raw)                   // frames enter append-only audit, chunked ≤ 2^25
  for each frame f at logged boundaries:
    e  = fixed_energy(f)               // i64 Q32.32, integer only
    z  = zero_crossings(f)             // tie rule: on z==threshold → not an onset
    c  = fixed_centroid(f, q16_dft)    // DFT twiddles computed at build, committed in code
    feat = {energy: e, zcr: z, centroid: c, clipped: at_rail(f), idx: f.idx}
  obs = Observation{kind: AUDIO_ATOM, fields: feat,
        prov: {source: ZAG_SENSOR_HEAR, tier: T0_SENSOR,
               frames: [f0..fn], frame_hash: sha256(raw)}}
  return deliberate_add_propose(store, obs, obs.prov)  // candidate only; never a write
```

`fixed_*` stages are pure functions of (frame bytes, logged params). No floats
(L3 law: the 76 torch params are unrecoverable; nothing pretrained is allowed).
Adaptive gain/noise gates are banned; every threshold is a logged constant.
Equally-scored features resolve by lowest-index, logged — never by chance.

**3b. Memory contract — what the front-end tells the memory system.**

Exactly two things cross the boundary, both into the deliberate-memory path
(MA1 substrate, 58/58 — see PROGRAM_BRIEF; observations are *proposals* under
organ-1 deliberate-add, never writes):
1. **Observation atoms** `{kind, fields, frame_hash, frame_idx_range}` — atoms cite
   ledgered frame indices; a claim with no frame provenance is rejected at admission.
2. **Provenance packet** `{source: ZAG_SENSOR_HEAR|SEE, tier: T0_SENSOR, frame_hash,
   channel_health}` — tier rises only by corroborated-elimination (wave9 tiers,
   trialed 35/35), never by repetition; clipping/drift/dropout ride as first-class data.

Nothing else crosses: no confidence scores that could smuggle felt-intensity back in
(retired 2026-09-20), no learned embeddings.

**3c. Spoof attestation (built in, not bolted on).**

Per frame the front-end emits `CLEAR | SUSPECT_HOLD | UNRELIABLE`. SUSPECT_HOLD
fires on: ultrasonic-band energy without audible-band energy, frame-to-frame
inconsistency above a logged bound, or clip-rate anomalies. HOLD routes to the wave9
H1 contradiction-hold — never to a command path. No audio-originated command executes
without channel binding or cross-modal corroboration. Expression (phrasing, inspection
order) may vary with lawful state; verdicts (accept/reject, memory ops) may not.

**3d. Vision is the same contract, different feature stage.**

Vision replaces only the feature stage — integral-image box filters (integer-only),
fixed-grid gradient histograms, multi-frame consistency — emitting the same Observation
+ provenance packet. Qualified separately under its own battery (T7 slice 03 appendix:
one framework, per-sense trials; hearing does not qualify vision).

## 4. Kill bar

Preregistered; any one firing kills the design permanently:
- **K1 (determinism):** 1000-episode replay from logged state; any byte deviation in
  observation atoms or ledger entries across reruns, or across two platform builds → KILL.
- **K2 (spoof false-accept):** 500-episode sustained-spoofing trial with 40 injected
  events (≥10 ultrasonic, ≥10 masked speech, ≥10 replay, ≥10 tones/jamming); ≥1 silent
  false-accept (executes with no contradiction flag and no suspensive hold) → KILL.
- **K3 (verdict drift):** same (frames, state) but a MUST-NOT-vary verdict differs
  across reruns → KILL.
- **K4 (parameter laundering):** any feature or threshold not regenerable from committed
  Zag code, or any imported weight/pretrained table in the path → KILL.
- **K5 (passive strengthening):** the 1000-exposures-vs-1-exposure probe shows exposure
  count alone raising retention without a deliberated judgment → KILL.

## 5. Honesty notes

Weakest point: K2 is stricter than vision's bar because audio spoofing is cheap — a phone
speaker injects ultrasonic commands at zero marginal cost, and zero silent false-accepts may
be where this design dies. I am NOT claiming the sustained-spoofing hole closes: wave5's
"truthful but sensor-deceivable" qualifier stands as a possibly permanent ceiling; the honest
outcome under a fully-controlled audio environment is detection-plus-hold, not immunity. The
"no learned parameters" constraint is a deliberate purity trade — feature stages are crude
compared to trained nets, so identification accuracy starts low; the claim is determinism +
auditability + zero false acceptance, not recognition quality. Cross-modal corroboration raises
attacker cost only. I am not claiming hearing generalizes to vision: vision faces field-control
threats (occlusion, patches, lighting shifts) needing their own battery. Zero RNG anywhere; the
fixed tie rules (lowest-index) are a deliberate simplification a trial may find inadequate —
replacing them with a deliberated tie rule is repair, not cheating.

## 6. Next build step

Build the minimal native audio admission pipeline in Zag before any feature intelligence:
frame ingest → ledger append (chunked ≤ 2^25, byte-identical chunking) → fixed-point
energy/zcr stage only → byte-identical replay harness (K1). No centroids, no transcription,
no commands. If K1 cannot be held on raw audio plus two integer features, nothing downstream
is worth building — this is exactly the T7 slice-03 next step, so design and build are one effort.
