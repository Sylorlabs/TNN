# UNIVERSAL_VS_PERPATH — the video team's argued position

## Position: the *principle* is universal; the *pieces* are per-path.

One law, instantiated per path — not one mechanism copied across paths, and
not a free-for-all where each path reinvents authority from scratch.

### The universal principle (applies to every generation path)

> **The plan keeps the last word. Output feedback earns authority only (a)
> on the exception path, as plan-pure re-render of faulted units, or (b)
> for discrete plan-level events provably uncomputable plan-side — bounded,
> quantized on commit, re-derivable, revocable. Continuous feedback loops
> are denied by default.**

Video's evidence supports every clause of this as a *universal* statement:

- **Plan-last-word:** video never violated it natively — the survey found
  zero output→input loops in any native path, and video is the closest to
  the PAR extreme (`frame = F(plan, f)`, PATH_MECHANICS.md). A principle
  that video already satisfies without being told is a good candidate for
  a law.
- **Exception path as re-render:** the contractivity argument (constant
  correction map, Lipschitz 0, idempotent, one-step) is pure mathematics —
  it holds for audio blocks, video frames, image layers, text spans alike.
  Nothing about it is audio-specific. Healing-the-past by re-assertion vs
  distorting-the-future by forward correction is a causal argument, not a
  domain argument.
- **Continuous loops denied by default:** audio proved the failure modes
  (involution servo, frozen targets, 1.0→0.74 tax, Attack 11 incoherence).
  Video adds an independent proof from the other direction: here the tax
  would be *created* from nothing (native recurrence already 1.0), which
  shows the denial doesn't depend on audio's particular carried-state
  mechanics.

### Why the pieces must be per-path (video's three exhibits)

**Exhibit 1: piece 3 exists in audio and must not exist in video.**
Audio's RESPOND octave latch answers a real, battery-demonstrated need
(RT-LONG: the plan's pitch label was wrong by an octave; only rendered
bytes carried the correction). Video has no such need — the RESPOND-analog
search came back empty (FAULT_ANALYSIS.md), and the one property that made
audio's latch necessary (hidden state making plan-side computation
impossible) is absent: every "measure the frame" value in video is
plan-computable without rendering. A universal *mechanism* would either
force a latch onto video (inventing authority for a need that doesn't
exist — the exact "when in doubt, test" violation) or strip it from audio
(destroying a proven capability). Per-path pieces; universal principle.

**Exhibit 2: the detection predicates are per-path by necessity.**
Audio's fault predicate is block RMS vs `K_PLAN · plan_rms(block)` with a
`[0.35×, 2.5×]` band and a peak edge (HYBRID_SPEC §2, §5). Video's must be
per-frame tile luminance vs the material model, file-size exactness, and
the pairwise V-TEMP motion band — different units (frames vs blocks),
different statistics (spatial tiles vs temporal RMS), different floors
(±2 LSB dither vs 64-sample zeroing). The *form* — plan-derived targets,
wide bands, disclosed floors — is universal; the *content* is per-path.
Copying audio's predicate onto video would be as wrong as copying video's
onto audio.

**Exhibit 3: the coherence question is answered differently per path because
coherence comes from different places.** This is the deep per-path fact the
swarm should carry back:

| Path | Where temporal coherence comes from | What feedback threatens |
|---|---|---|
| Audio (stateful-sequential) | Partly carried state (phase continuity across blocks) + plan | Corrupts the state the coherence lives in (1.0→0.74 measured) |
| Video (PAR frames) | Entirely the plan (advected coordinates, keyframe interpolation) | Creates state where none existed; tax from 1.0 *created*, not increased |
| Image (canvas painting) | Layer order + compositing (survey: `d_blend` reads the pixel — bounded) | Would convert ordered painting into history-dependent painting |
| Text/dialogue (template) | The plan directly (slot-fill, no generative loop) | Nothing to threaten — and nothing to gain |

The authority rule for a path should be derived from *where that path's
coherence lives*. Where coherence is plan-sourced (video, text), feedback
has no foothold and the rule is nearly "plan absolute + re-render
exceptions." Where coherence is partly state-sourced (audio), feedback has
a narrow, proven foothold (the latch) that must be fenced with quantization
and gates. A universal mechanism can't see this difference; a universal
principle with per-path pieces can.

### What "universal" must not mean (two failure modes to avoid)

1. **Universal must not mean "audio's three pieces everywhere."** That
   imports piece 3 into paths with no demonstrated need — precisely the
   foot-in-the-door the video recommendation denies. If the swarm converges
   on "universal," it must be the principle above, not the parts list.
2. **Universal must not mean "per-path teams may each re-derive whether
   feedback is allowed at all."** The default-deny on continuous loops and
   the exception-path-only grant should not be re-litigated per path; they
   are settled by the audio battery and confirmed by video's independent
   analysis. Per-path work is: predicates, floors, and whether a
   piece-3-class need exists (with the three gates from
   AUTHORITY_RECOMMENDATION.md as the admission test).

### The test that would change this position

If another path's team finds a *native* output→input dependency that is
load-bearing for quality — not a constructed prototype, not a hypothetical —
and shows the universal principle can't express it, then the principle needs
revision, not just a new piece. Video looked hard for such a dependency and
found none; the position stands or falls with the other teams' findings.

### One-line version for Micah

**Same law everywhere — plan keeps the last word, feedback only heals faults
or latches what the plan can't compute — but each path gets its own pieces:
video needs two (render + re-render), audio needs three (render + re-render
+ the octave latch), because video's frames are already pure functions of
the plan and audio's aren't.**
