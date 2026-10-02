# CUTOUT DEBATE — record and preregistered tests (2026-09-22)

Micah's binding ruling: "imagination doesn't cut out like that... cutouts
don't happen in my imagination." The crews' "content by design" defense of
B-β's tag-halt (~13 s) and B-γ's event-grain phrase boundaries is REJECTED.
Continuity is now a standing requirement: imagined scenes flow continuously
— events have connective tissue, never hard stops at phrase boundaries.

Debate participants: sol (via UnoRouter, opening position) + two native
critic voices. grok-4.7 was requested by Micah but is STILL DELISTED from
UnoRouter as of 2026-09-22 12:19 PDT (only grok-4.6 listed); per standing
honesty rules grok-4.6 was NOT substituted silently. The debate ran with sol
+ natives.

## Position 1 — sol: missing connective scene state

The cutouts are caused by an **event-only representation of imagination**.
Both forks place salient events but do not represent the continuously
changing scene between them. When one event phrase ends and the next has not
begun, the assembler emits its default state: silence.

B-β's tag-halt is the same flaw at the semantic level: the score treats
"halt" as a structural command meaning "stop all audio," but a tag-game
imagination would not become an empty waveform for half a second —
movement, breath, distant play, playground air, and shifting attention
continue. B-γ's 2 ms glue fades prevent clicks but cannot invent connective
activity. This is not primarily a mixing problem; it is a missing model of
**between-event continuity**.

The fix is compositional: make the scene's ongoing state primary; laughs,
shouts, and footsteps enter and leave that state. Every phrase boundary
resolves into a successor state (chase → dispersed movement → breath and
distant play; tag moment → change of pursuit direction). A deliberate pause
may exist only as a **continuous low-activity state**, never a global halt.
The grammar must require each transition to specify what persists, what
decays, what changes location, and what new activity emerges. "No event
scheduled" must never mean "the imagined world disappears."

Discriminating test (sol): controlled A/B with identical captured events,
timings, and score landmarks — (1) current event-only version, (2) version
with explicit bridge states at every phrase boundary (13 s tag transition,
26 s chase-to-settle), containing evolving air, residual movement, spatial
repositioning, decaying activity, no new salient events; loudness
normalization and crossfade settings fixed. If Micah still hears cutouts in
the bridge-state version, the hypothesis is wrong. If they disappear, the
compositional grammar — not fade duration — was the governing failure.

## Position 2 — native critic #1: the paste-seam / missing-world hypothesis

The cutouts are a missing-representation problem: the score grammar has
verbs (laugh, shout, chase) but no noun — no representation of the world
those events happen *in*. You cannot crossfade into a world that was never
scored.

The score says "laugh train here, chase there, tag at 13 s" but nothing
about the air between — its vocabulary is events only. At every phrase
boundary the mixer honestly renders: event A decays, nothing is scored,
event B hasn't started. B-β's tag at 13 s is the smoking gun: the score
*explicitly stopped the feet* when the tag landed. An architecture with a
concept of "the playground keeps existing" could not produce that output.

Two details make the seam audible: (a) each captured event smuggles in its
own captured room — pasting events pastes incompatible atmospheres; even a
perfect crossfade blends two wrong rooms, not one right one; (b) the 2 ms
glue fades fix the sample level and guarantee the phrase level — no fade
length changes what was never scored.

The fix: invert the architecture — **score the world first**, as a
continuous 0–30 s world bed with scored evolution (wind shifts, distant
voices swelling, crowd density changing), authored as first-class content;
events are placed INTO the already-continuous world. What the fix is *not*:
longer crossfades, better ducking, reverb tails, or any processing trick —
DSP smears what's there; it cannot invent the sound of feet never captured
and never scored.

Discriminating test (critic #1): 2×2, same event list, positions, timeline —
world bed absent/present × 2 ms/500 ms fades (R1=status quo, R2=long fades
only, R3=world bed only, R4=both). Metric: boundary penalty
P = median(D_boundaries) − median(D_controls), D = max envelope drop vs
local median in ±250 ms windows. Prediction: P large for R1 *and* R2 (a
long crossfade cannot fill a gap — at a true gap there is no second thing
to blend into); P ≈ 0 for R3/R4. Kill criterion: if R2 drives P to zero
while R3 does not, the hypothesis is dead — it's a fade-engineering
problem, not a missing-world problem. Second kill: if R1 shows P ≈ 0 on
the machine while Micah still hears cutouts, the measurement frame is wrong.

## Position 3 — native critic #2: the grammar-halt hypothesis

The cutouts are not paste seams — measurements killed that view (no digital
dropouts, no hard onsets, no gate dips; boundaries are soft-shouldered).
What we have is a **deliberate compositional command for nothing to
happen**, executed faithfully. B-β's DERIVATION_kids.md phase table: P2 TAG
— "Steps stop dead; WREN's 'TAG!'; PIP's gasp — the touch lands; **everything
halts for half a second**." The grammar treats SILENCE AS AN EVENT: a node
whose content is "nothing happens" occupying a half-second slot.

The mechanism is a category error between narrative punctuation and acoustic
reality. In the story the tag landing is punctuation; the composer wrote the
punctuation *as* the acoustic event. In a real playground the tag landing
does not stop the world — the tagged child gasps *and laughs*, the tagger
runs past, others keep breathing, feet shuffle, the air continues. The
phase grammar's event vocabulary lacked a "keep the world alive" primitive —
its only way to say "the action pauses" was to say "the acoustics stop."
B-γ's dips are the same disease in milder form: phrases as separate
movements with rest bars between them — but imagination doesn't rest between
phrases.

The fix is a grammar fix, not a seam fix: (1) **delete "silence" from the
event vocabulary** — no phase/node/transition may score "nothing happens";
a tag landing becomes a **pivot** (shout lands, gasp-laugh pivots
immediately, breath bed swells, footstep pattern *changes cadence* — the
world re-organizes, never vanishes); (2) **overlap, don't abut** — the next
phase's world-content starts before the previous phase's foreground ends
(the contagion clock already does this *inside* P3; the phase graph needs it
*across* phases).

Discriminating test H-KILL-1 (critic #2): three 30 s variants of B-β's
frozen scene, identical placements except the 12.8–13.6 s tag boundary —
A: halt-scored (current grammar); B: pivot-scored (same TAG! and gasp, but
world continues under them — footstep pattern pivots cadence, breath bed
swells, one laugh overlaps the shout ~100 ms); C: sham control (halt-scored
like A + 200 ms bed crossfade at the boundary — the seam camp's best
proposal, no grammar change). Blind to Micah, order-randomized: "children
playing tag at dusk; the tag lands around 13 s — does the scene cut out
anywhere?" Kill: if B flows while A and C still cut out, grammar-halt
survives and the seam view dies. Critic #2's hypothesis dies if B still
cuts out with the world provably alive under it, or if C passes while B
fails (then it's acoustic edges, not causal commands).

## Killed hypotheses

1. **"It's a digital artifact"** — killed by measurement before the debate:
   0 digital dropouts, 0 hard onsets, 0 gate-like slams at 10/50 ms
   resolution across all three crews. The cutouts are compositional.
2. **"Content by design" (the crews' defense)** — killed by Micah's ruling,
   not by argument. The tag-halt and phrase-boundary dips are deliberate
   score content AND they violate the continuity law. Deliberate does not
   mean acceptable.
3. **"Longer crossfades fix it"** — the sham control (critic #1's R2,
   critic #2's variant C) is preregistered to kill this: processing smears
   what exists; it cannot invent the world between events.

## Surviving convergent mechanism

All three voices agree the defect is compositional, not processing. The
convergent mechanism: **an event-only score grammar with no continuous
world representation, which commands silence-as-an-event at boundaries.**
The fix all three imply: **world-first composition** — a continuously
scored world (bed with scored evolution) that never empties; no silence
nodes anywhere; every boundary a pivot/bridge with overlapping successor
content. The three proposals differ only in emphasis (bridge states at
boundaries / continuous world bed / halt→pivot rewrite) and the fix
implements all three.

## Preregistered tests (frozen before results)

Machine metric: boundary penalty P at flagged boundaries vs within-phrase
controls (envelope depth in dB + max slope + minimum floor in ±250 ms
windows; `/tmp/continuity.py`). Baseline on v2 clips (2026-09-22):

| Clip | Boundary | depth_dB | floor (min RMS) |
|---|---|---|---|
| B-β v2 | 13.2 s tag | −4.6 | 0.0094 |
| B-β v2 | 26.2 s P3→P4 | −12.2 | 0.0090 |
| B-γ v2 | 9.35 s phrase | −21.8 | 0.0083 |
| B-γ v2 | 18.75 s phrase | −7.0 | 0.0111 |
| B-α v2 (control) | 13.2 s | −4.3 | 0.0596 |

B-α — the fork Micah called "most realistic" — keeps a 6× higher floor at
the same timestamp: its continuous bed is the positive control.

- **T-CONT-1 (world-bed factor):** fixed B-β/B-γ vs v2 — P must drop and
  boundary floors must rise toward the bed's natural floor at every flagged
  boundary. Bar: floor ≥ 3× the v2 floor at each flagged boundary.
- **T-CONT-2 (sham control):** a long-crossfade-only variant must NOT meet
  T-CONT-1's bar — pre-kills the "just crossfading" objection.
- **T-CONT-3 (halt→pivot):** the 12.8–13.6 s tag region re-measured; the
  half-second commanded halt must be gone (no ≥300 ms window below the bed
  floor that isn't also present in a within-phrase control).
- **T-CONT-4 (oracle):** v3 kids clips to Micah's ears with the standard
  brief. His verdict is binding over all machine results.

## Fix scope (authorized)

- B-β `mech_kids.zag` `score_kids`: P2 tag landing rewritten as a pivot
  (shout lands → gasp-laugh overlaps ~100 ms → footstep cadence pivots
  rather than stopping → breath bed swells through); P3→P4 transition
  bridged with contagion-style overlap across the phase boundary; bed
  verified continuous and evolving at all boundaries.
- B-γ `gamma.zag` `score_kids`: phrase boundaries (9.35 s, 18.75 s, and any
  other flagged) given scored successor/bridge content; no silence nodes.
- B-α: check only — its continuous bed is the positive control; re-render
  only if a cutout signature is found.
- Invariants: pure Zag, zero RNG, 3/3 byte-identical reruns, A-NATIVE
  re-verified, v2 natural endings preserved, v1/v2 clips untouched.
- v3 clips: `b_beta/bbeta_kids_v3.wav`, `b_gamma/render/b_gamma_kids_v3.wav`.
