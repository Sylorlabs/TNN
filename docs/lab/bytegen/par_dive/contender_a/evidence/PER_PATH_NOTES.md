# §3 Per-path notes — where PAR's argument holds (contender A perspective)

These are analytical notes, not tested verdicts (only the audio path was built).
Question per path: does the modality's nature demand carried state, or is pure
`f(plan,t)` natural?

## Audio — TESTED (see VERDICT_AUDIO.md)

**Verdict: partial win.** Samples are conditionally independent given the plan:
every sample is a pure function of (plan, t). PAR gives bit-identical motif
recurrence (xcorr 1.000000 vs native 0.736557), zero fault cascade by
construction, zero long-horizon drift, and order-free plan formation. The price
is ~46% single-threaded wall time (per-sample phase recompute via division vs
carried-phase addition). For robustness-critical audio (fault tolerance,
deterministic replay, auditability), PAR's argument holds strongly. For
raw throughput on one core, native wins.

## Video — NOT BUILT (notes)

Frames are audio samples in 2D+time: pure `f(plan, x, y, t)` is natural for
**procedural/generative** video (every pixel independent given the scene plan).
PAR's argument holds here — same independence structure as audio, same
zero-cascade benefit (a corrupted frame cannot infect the next). Where the
path's nature demands state: **predictive/compressed** video (P-frames,
motion compensation) is inherently stateful — the "plan" would have to carry
the reference frames, at which point PAR degenerates to shipping state as plan
content. Also **adaptive bitrate / feedback** loops need output→input coupling.
Verdict: PAR holds for generative video; loses for predictive/codec video.

## Dialogue — NOT BUILT (notes)

**PAR's argument breaks here; the path demands state.** Dialogue is
inherently sequential and adaptive: utterance N+1 depends on the *content* of
utterance N (anaphora, ellipsis, common-ground tracking, repair). A pure
`f(plan,t)` renderer would need the entire conversation history reified as the
"plan" — but the plan is supposed to precede rendering, while dialogue history
is *produced by* rendering. This is a genuine circularity, not an
implementation gap. Contender B (plan-seeded state at region boundaries) or C
(bounded-feedback AR) are the honest architectures here; pure PAR (A) cannot
express "respond to what was just said" without smuggling state into the plan.
Verdict: state demanded by the path's nature. A loses dialogue.

## Image — NOT BUILT (notes)

**Trivially parallel; PAR's argument holds vacuously.** A static image has no
time dimension: `f(plan, x, y)` over pixels is embarrassingly parallel, and
"sequential vs parallel" is purely an implementation choice with identical
output. There is no carried state to debate (nothing is "carried" across a
single image). The interesting question for images is plan *formation*
(§4): is the scene plan's content order-independent? For compositional scenes
(place tree, then house, then sun), formation is naturally parallel; for
relational constraints (shadow must fall opposite the sun), formation needs
either multi-pass (cf. A's two-pass RESPOND resolution) or joint solving.
Verdict: PAR holds for rendering; formation parallelism depends on constraint
structure (A's two-pass pattern generalizes).

## Summary matrix (per §6: report the matrix, not a single crown)

| Path | A (pure PAR) vs native | Basis |
|---|---|---|
| Audio | **Partial win** (robustness axes won, COST lost) | Tested §2 battery |
| Video (generative) | PAR argument holds (unbuilt) | Analytical |
| Video (predictive) | State demanded (unbuilt) | Analytical |
| Dialogue | **State demanded — A loses** (unbuilt) | Analytical |
| Image (render) | Trivially parallel (unbuilt) | Analytical |
| Image (formation) | Depends on constraints (unbuilt) | Analytical |

Only the audio row is evidence-backed. The rest are honest priors for future
crews, flagged as unbuilt.
