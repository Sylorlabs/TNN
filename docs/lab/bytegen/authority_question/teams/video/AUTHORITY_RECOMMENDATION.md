# AUTHORITY_RECOMMENDATION — video

## Recommendation: a two-piece rule (pieces 1+2 of the hybrid pattern, no piece 3)

| # | Piece | Default | State | Authority |
|---|---|---|---|---|
| 1 | PAR frame path (always) | **always** | zero cross-frame state | all scene content, timing, color, motion — always |
| 2 | Exception detect-and-reassert (per frame) | idle (fires only on artifact fault) | stateless | re-render the faulted frame plan-pure, nothing else |
| 3 | Output-conditioned scene events | **does not exist** | — | denied unless proven plan-incomputable (see §"The piece-3 rule") |

Piece 1 is the SOLE authority over: what is in the scene, where it is, what
color it is, how it moves, and when. Piece 2 may only replace a frame's bytes
with `F(plan, f)` for that frame. It cannot change scene parameters, invent
content, touch uncorrupted frames, or adjust future frames to "compensate" a
past fault.

This is the audio hybrid v2 pattern (HYBRID_SPEC.md) with piece 3 removed —
not because video is simpler, but because video has no native event class
that needs it (FAULT_ANALYSIS.md, RESPOND-analog check: none found).

## The steelman for output feedback on video (argued honestly, then answered)

**The case for a video piece 3 goes like this.** Audio earned its RESPOND
latch because sometimes the plan is genuinely wrong about the world — a cue
mislabeled by an octave — and only the rendered bytes carry the correction.
Video will face its own version: a scene event the plan can't fully specify
up front. "The breaker fires when the vortex's rendered crest first crosses
the rock line." "The bird banks toward the brightest cloud." These are
natural, expressive authoring constructs, and forbidding them makes the video
path less capable than the audio path. Moreover, detection *already* concedes
that reading output bytes is sometimes necessary (piece 2); once you're
reading bytes, using them for content — not just fault detection — is a
small step, and it would let scenes be *reactive* instead of merely
*played back*. A bounded latch (fire once, commit a quantized value, never
the raw measurement — exactly audio's octave rule) would carry the same
safety properties audio proved.

**Why it loses.** Four independent reasons, any one sufficient:

1. **No native need exists.** The steelman is hypothetical: no native video
   mechanism does this, and every candidate examined (foam advection, vortex
   migration, keyframe timing, A/V interleave) turned out plan-pure on
   inspection. Audio's piece 3 was built to answer a *measured* attack
   (RT-LONG: wrong nominal pitch, proven on the battery). Video's piece 3
   would be built to answer an imagined one. Per Micah's standing rule —
   tests decide, and "when in doubt, test both" — the burden is on the
   feedback side to produce a failing case first. Until a battery
   demonstrates a scene the plan cannot author but a latch can, piece 3 stays
   denied.
2. **It's computable plan-side anyway.** This is the deep one, and it's
   specific to video's mechanics. In audio, the RESPOND latch measures
   *rendered audio* because the plan's pitch label was wrong — the error is
   in the plan's description of the world, and the bytes are the evidence.
   In video, "the brightest pixel of frame 29" or "when the crest crosses
   the rock line" are pure functions of the plan: the renderer is
   deterministic and stateless across frames, so you can compute the answer
   from the plan without rendering a single byte. The steelman's "reactive
   scene" is achievable with zero output feedback — it just requires the
   plan language to expose derived queries ("`crest_crossing_frame(vortex,
   rockline)`"), which is a plan-language feature, not an authority feature.
   Output feedback is irreplaceable only when the forward map has hidden
   state (audio's carried phase) or the measurement is of the physical world
   beyond the buffer. Video file generation has neither.
3. **The cascade asymmetry.** Granting piece 3 converts the path from PAR to
   AR *by construction*: frame `f+1`'s plan becomes a function of frame `f`'s
   bytes. Audio measured the price of that conversion (RT-CASCADE: 5,791
   derailed samples from one fault; coherence 1.0→0.74). In video the price
   is worse, because the blast radius is the *scene*: one corrupted frame
   permanently diverts all subsequent frames, and healing means re-deriving
   the tail, not re-rendering one file. Piece 2's healing guarantee ("exact,
   one frame, idempotent") depends on frames being independent; piece 3
   destroys the independence piece 2 relies on. The two cannot coexist
   safely — this is audio's Attack 11 ("one loop incoherent") restated for
   video: the exception path and the reactive path want contradictory
   things from the frame sequence.
4. **A bounded latch is still a foot in the door for a servo.** Audio's v1
   history is the cautionary tale: a "bounded" per-block servo turned out to
   be an involution with rail pins constructible from plan text
   (HYBRID_SPEC §6). A video latch that "fires once and commits a quantized
   value" is safe *per event*, but the event class itself — predicates over
   rendered bytes that rewrite the plan — is the mechanism by which a future
   continuous loop would be built. Deny the class until the need is proven.

## The steelman for pure plan-absolute with NO exception path (argued, then answered)

**The case goes like this.** If the renderer is deterministic and every frame
is `F(plan, f)`, then any fault is either in the plan (VF-6, which re-render
can't fix) or in the artifact (VF-1–VF-4, which are someone else's problem —
the disk, the encoder, the transport). The generator's job ends at emitting
correct bytes; policing storage is scope creep, and the detection predicates
need plan-derived targets (per-frame tile statistics) that are real
engineering work for a fault class the lab has never actually observed in
video. Ship correct bytes; let the verifier (`verify_vid.py`, SHA256SUMS
manifests) catch the rest. Simpler rule, smaller surface.

**Why it loses.** The verifier comparison concedes the point: `SHA256SUMS`
already exists because the lab *does* police artifacts — the exception path
just moves that policing to where it can act. Three concrete reasons:

1. **Faults VF-1–VF-4 are real and cheap to heal.** A 48-frame ocean run
   costs ~2 minutes (VID-README); re-rendering one detected-bad frame costs
   ~2.5 s and is byte-exact. Refusing to heal means shipping a corrupted
   frame to Micah's eyes — and his senses outrank every metric, so a
   single black frame in a blind judging round is a program-level failure,
   not a storage footnote.
2. **False positives are no-ops, so the bar for adding detection is low.**
   Re-rendering a clean frame yields byte-identical bytes (recurrence 1.0).
   The exception path cannot corrupt anything it misfires on — unlike a
   servo, whose false positives distort. The only cost is compute.
3. **The boundary is clean.** Piece 2 heals artifact faults and provably
   cannot touch plan faults (C4): if the bytes match the wrong plan, every
   plan-derived predicate passes and nothing fires. There is no slippery
   slope from "re-render frame 12" to "rewrite the scene" — the correction
   map is constant in its input (Lipschitz 0), so it *cannot* express
   anything but the plan.

## The piece-3 rule (for future video work)

If a future video mechanism proposes an output-conditioned scene event, it
must clear all three gates before it earns any authority:

1. **Plan-incomputability proof.** Show the measured value cannot be derived
   from the plan without the rendered bytes — i.e., name the hidden state or
   extra-buffer measurement that makes plan-side computation impossible.
   ("The plan could compute it but it's inconvenient" fails this gate.)
2. **Battery demonstration.** A fault/need battery, preregistered, showing a
   scene the plan-only path provably cannot author and the latch provably
   can — video's equivalent of RT-LONG.
3. **Non-interference proof.** Show the latch preserves piece 2's healing
   guarantee: a corrupted frame must still heal by single-frame re-render,
   which means the latch's committed values must be re-derivable plan-pure
   (audio's answer: commit `f_nom · 2^k`, a pure function of plan nominal +
   quantized evidence — the video analog would need the same property).

Until then: **no feedback, plan absolute, exceptions re-rendered.**

## What "bounded, revocable" means for video specifically

Audio's authority rule says feedback is "bounded, revocable." For video:

- **Bounded:** piece 2's correction bytes ∈ {plan-pure bytes of the faulted
  frame}; at most the faulted frames are rewritten; no parameter, no future
  frame, no scene constant is touched. Detection predicates are
  plan-derived (per-frame expected statistics from the scene model), never
  frozen literals.
- **Revocable:** there is nothing to revoke — piece 2 is stateless and
  idempotent. A bad detection self-corrects to a no-op. This is stronger
  than audio's v1 revoke windows (deleted with the servo) and matches v2's
  §7: no revocation mechanism is needed because there is no authority to
  take back.
- **The one revocation that matters** is at the rule level: if piece-3 gates
  are ever cleared, the grant must be per-event-class, quantize-on-commit,
  and re-derivable plan-pure — revocable by deleting the event class, with
  the sequence falling back to plan-pure frames byte-identically.
