# Story — authority recommendation

**Recommended rule:** *The plan is the sole authority over every rendered
byte. Rendered output may be READ — by deliberation or by a stateless
exception detector — but it never conditions the renderer. Exceptions heal
by plan-pure re-render (contractive, Lipschitz 0); plan amendments enter
only as discrete, deliberated plan events. The renderer has no eyes.*

In hybrid-spec language: story keeps Piece 1 (plan-pure path) as the entire
generative story, adopts Piece 2 (exception detect-and-reassert) for
write-channel and rendering faults, and has **no native Piece-3 analog** —
there is no hidden variable in text rendering for a sensor to discover
(PATH_MECHANICS.md). External edits are plan events (H3), authorized by
deliberation, never by the renderer.

The reasoning below argues both sides first. The steelman for generative
feedback is given real force — then answered.

---

## Steelman: "Story SHOULD let output feed the renderer" (the opposition)

**O1 — Local cohesion needs eyes.** Beats are rendered independently; the
DEL templates are stitched, not woven. A human writer re-reads the last
paragraph before writing the next — that re-reading is output feedback,
and it is load-bearing for flow. A renderer forbidden from reading its own
output will produce seams: "The detective polished the key." followed by
"The thunderstorm struck without warning." with no connective tissue. If
beat 2 could *see* beat 1's rendered sentences, it could choose the
"returned, worse than before" variant (rc==3 branch in `r_climax`,
story_render.zag:88) when — and only when — the event was actually rendered
as striking, rather than deciding from the class table alone.

**O2 — The plan is incomplete by design.** The beat sheet assigns *words* to
beats; it does not specify sentences, emphasis, or which decorative details
landed. `detail()` improvises ("The accordion hung in the air") from class
+ parity — pure decoration with no plan content. Since the renderer already
improvises beyond the plan, forbidding it from *seeing* its improvisations
is arbitrary: the improvisation exists, eyes would just make it coherent.

**O3 — Humans revise while writing; TNN should too.** The hybrid already
concedes this for audio (the RESPOND latch re-enters as plan input). A
storyteller who notices mid-telling that the audience is lost re-plans
*from the telling so far*. Banning the renderer from the output stream
bans the mechanism by which real-time narrative repair happens.

**O4 — Detection without feedback is toothless.** H2 (thread audit) admits
that some faults are visible *only* in the rendered text. If the auditor
can read the text and find the dropped thread, why shouldn't the renderer
itself notice "the key never got clutched" and fix the next beat
accordingly? Routing everything through deliberation + re-render is slow
and theatrical when the renderer is right there.

**O5 — The no-feedback rule proves too much.** Dialogue (`dialogue.zag`)
is also template slot-fill and nobody proposes giving its templates eyes —
but dialogue *answers questions*, and a follow-up question's meaning
depends on the previous *rendered answer*. If output can never condition
generation, multi-turn dialogue is impossible. Story in a conversational
setting (interactive fiction) inherits the same need.

## Answer to the steelman

**A1 (cohesion):** The seams are real, but eyes don't fix them — *planning*
does. If beat 2 needs to know whether beat 1 rendered the event as
"struck," the correct move is to put that fact in the plan (a beat-1
annotation: `rendered_as=STRUCK`), not to have beat 2 parse beat 1's
English. Parsing rendered text to recover a fact the planner already knew
is information-theoretically backwards — and fragile: the parser can
misread, the plan cannot misremember. Cohesion variants belong in the beat
sheet as annotations; the renderer then stays plan-pure and the cohesion
is *stronger* (deterministic, auditable) than any eyes-based heuristic.

**A2 (incomplete plan):** Conceded that `detail()` improvises — but the
improvisation is *decoration by design*, and decoration must never become
load-bearing. The moment beat 2 conditions on a decorative sentence, the
decoration has been promoted to plot — silently, unaudited, unplanned.
O2's argument proves the opposite of what it intends: because the renderer
improvises, its improvisations must be *quarantined* from future beats,
not consulted. If an improvisation is good enough to steer the story, it
was good enough to plan — move it into the beat sheet (a DEL annotation),
where deliberation can vet it. (This is also the answer to the audio
analog: the hybrid lets the sensor discover *octave errors*, a physical
fact; it never lets the renderer improvise timbre from its own output.)

**A3 (human revision):** Humans revise by *re-planning*, not by letting the
hand keep writing while the eyes steer. The writer who notices the audience
is lost *stops, re-plans, and retells* — the retelling is plan-pure under
the new plan. That is exactly the H2/H3 shape: detection reads output,
deliberation amends the plan, rendering re-runs plan-pure. O3 conflates
"the system re-reads output" (allowed, (D)-side) with "the renderer
conditions on output" (banned, (G)-side). The hybrid's RESPOND latch is the
proof that the distinction is workable: it re-enters as *plan input*,
never as renderer state.

**A4 (toothless detection):** Speed is not authority. Letting the renderer
"notice and fix" the next beat is precisely C1's telephone game with a
helpful face: the fix is conditioned on rendered bytes, so the "fixed"
beat is a function of possibly-corrupt input, and the story's suffix is no
longer plan-pure — which destroys the Piece-2 healing guarantee (C2: the
past becomes unhealable). The deliberation round-trip is the *price* of
keeping every byte plan-accountable. For a fault path that fires rarely
(write-channel corruption, dropped anchors), the price is negligible; for a
path that fires every beat, the "fix" isn't a fault path at all — it's
(G), and it's banned for cause.

**A5 (dialogue):** The follow-up question is *new input*, not *output
feedback*. In the hybrid's terms it is a plan-level event (like RESPOND):
the new utterance enters deliberation, deliberation amends the plan
(conversation state), and the response renders plan-pure. Nothing in the
recommended rule forbids the *system* from reading its own prior output —
the dialogue manager may re-read the rendered answer as data (to resolve
anaphora, say). What is forbidden is the *renderer* conditioning the next
response's bytes on the previous response's bytes *as a generative
mechanism*. Interactive fiction works fine under the rule: user input and
even self-review are (D)-side; only the byte generator is (G)-banned. The
distinction is architectural (which component reads output), not
prohibitive.

## Why story gets no Piece-3 analog (and why that's principled, not a gap)

Audio's Piece 3 exists for one reason: the plan cannot compute what the
synth actually rendered (the K_PLAN calibration gap — §5 of the hybrid
spec). The sensor reads a physical fact unavailable to the plan. Story has
no such gap: the renderer is a pure function, so the plan *can* compute
every byte it will render — the plan is complete with respect to its own
output. There is no sub-octave-scale hidden variable for a story sensor to
honestly discover. Granting story a Piece-3-style "output sensing" event
would therefore be C3: theater at best, fabrication at worst. The honest
story analog of "the plan was wrong about reality" is not a sensor — it's
an *outside edit* (H3) or a *fault* (H1/H2), both handled without giving
the renderer eyes.

## The recommended rule, stated tightly

1. **Generative authority**: the beat sheet (`beat`/`beat_n`/`seq_*` +
   class tables + tv + P/L) is the sole authority over every rendered byte.
   The renderer is a pure function of the plan. No carried output state,
   no output-conditioned branching — mirroring the native design, which
   already has this shape.
2. **Exception authority (Piece-2-shaped)**: a stateless detector may read
   rendered beats and compare against plan-derived expectations (anchor
   presence per beat, closing-line presence). On fault it re-renders the
   affected beat(s) plan-pure. Correction bytes ∈ {plan-pure}; constant
   map, Lipschitz 0, idempotent. False positives are no-ops.
3. **Plan-event authority (latch-shaped, deliberation-gated)**: thread
   audits (H2) and external edits (H3) may amend the plan — but only
   through deliberation, as discrete plan events, with the amendment
   recorded (extend `seq_r` with new rule codes, e.g. r=4 AUDIT_REPAIR,
   r=5 EXTERNAL_EDIT). The renderer never sees the event; it sees the new
   plan. Re-render is plan-pure.
4. **What is banned**: any (G)-shaped mechanism — beat n as a function of
   rendered bytes 0..n−1, output-conditioned template choice, cohesion
   heuristics over rendered text, sensor→plan writes from the renderer's
   own output. Cohesion improvements must be planned (beat annotations),
   never sensed.
5. **Determinism**: zero RNG; byte-identical reruns (SHA-256 over the story
   bytes); pure Zag. The `tv` variant and word sets are plan inputs, so
   determinism is per (plan) — same plan, same bytes, always.

## Residual honest limits (carried over from the hybrid's §8 style)

- The exception detector can only catch faults visible against
  plan-derived expectations: a dropped anchor (word missing from its
  beat's text), a truncated story, a corrupted byte run. A *semantically*
  wrong-but-present word (wrong word, right shape) is invisible — same as
  audio's sub-floor corruptions.
- The thread audit (H2) judges thread continuity from text; it cannot judge
  *quality* (is the story good?) — that remains a deliberation/oracle job,
  out of scope for bytegen authority.
- Interactive latency: the H3 plan-event round trip (edit → deliberate →
  amend → re-render) is heavier than streaming the edit into the renderer.
  That cost is the price of plan accountability; for a storyteller it is
  measured in milliseconds against a deliberation step that already exists.
