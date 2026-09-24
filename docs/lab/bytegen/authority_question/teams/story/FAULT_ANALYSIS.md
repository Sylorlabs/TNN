# Story — fault/exception analysis

The load-bearing distinction for everything below:

- **(D) Deliberation-layer reading**: the planner (or a repair/verifier)
  reads rendered output bytes *as data* — to detect faults, audit thread
  continuity, or judge quality — and then acts **on the plan** (amend,
  re-plan, re-render plan-pure). Output is evidence, never instruction.
- **(G) Generative feedback**: the *renderer* reads already-rendered bytes
  to compute the *next* beat — beat n is a function of (plan, rendered
  bytes 0..n−1). Output becomes an input to generation.

(D) and (G) have opposite authority implications. (D) preserves plan
authority (the audio hybrid's Piece 3 RESPOND latch "re-enters as plan
input" is (D)-shaped). (G) hands authority to output (the audio v1 servo,
deleted for cause, was (G)-shaped).

The native story generator does **neither**: the renderer reads only the
plan, and the planner reads only plan tables. The analysis below asks what
each would do *to* story.

## Where output feedback would genuinely HELP

All three live on the (D) side. None requires (G).

### H1 — Write-channel corruption (the exact analog of audio Piece 2)

**Fault**: the render is plan-pure but the *bytes* get corrupted downstream
— a buffer overwrite, a truncated `st[8192]` story buffer (a long set could
overflow 8192 bytes and silently truncate RESOLUTION), a bit-flip in the
stdout channel.

**Help**: after rendering, scan the story text for plan-derived expectations
— every word assigned in `beat` tables must appear in its beat's text
(the Plan-Reconstruction Fidelity check); story must end with the resolution
template's closing line. On mismatch, **re-render the beat plan-pure**
(overwrite). Correction map `C(x) = render_beat(plan)` is constant in `x` —
Lipschitz 0, idempotent, one-step convergence, exactly the hybrid Piece 2
contract. A false positive is a no-op (re-rendering clean bytes yields
identical bytes).

**Authority accounting**: the *detection* reads output, but the authority is
the plan's: correction bytes ∈ {plan-pure}. This is exception-path authority
— the narrowest kind the hybrid grants. ✓ allowed under the hybrid rule.

### H2 — Dropped thread anchor (renderer/planner fault)

**Fault**: a genuine bug in role selection drops a thread anchor — e.g.,
`r_climax` picks R = the first class-3/4/0 word, but a class-table error
assigns O = R's word too, or `detail()`'s decorative sentence accidentally
consumes the word the thread needed. Concretely: SETUP treasures "the key"
(T), but CLIMAX's O-scan finds no class-2 word ≠ R (plan assigned all
THINGs elsewhere), so O = −1 and the climax degrades to "stood alone" — the
object thread silently dies mid-story. Or worse: the scan picks a *decorative*
word and the thread visibly misroutes.

**Help**: a (D)-layer thread audit reads the rendered text, checks the four
thread continuities (PATH_MECHANICS.md), and on failure **re-plans** —
e.g., move a THING into beat 2 via the existing REPAIR_SPILL mechanism
(`plan_del`'s bounded repair, rule r=2), then re-render plan-pure. This is
"re-reading output to re-plan": output is the *diagnostic*, the plan is the
*patient*, the cure is plan surgery + plan-pure re-render.

**Authority accounting**: is this "feedback authority"? No — the audit never
tells the *renderer* what to do; it tells the *planner* the plan failed its
own invariant, and the planner amends the plan. The renderer still only ever
sees the plan. This is the narrative analog of the RESPOND octave latch:
a discrete, deliberated plan-level event, not a renderer parameter tweak.
✓ allowed under the hybrid rule (with the deliberation-authorization
caveat in the recommendation).

### H3 — External edit adoption (the "interactive story" case)

**Fault** (not really a fault): a trainer or the user edits the rendered
story — "no wait, the detective is afraid of thunderstorms" — or an
upstream system mutates the text between beats in a streaming setting.

**Help**: a (D)-layer event ingests the edit, deliberates it (does it
contradict the beat sheet? does the thread audit still pass?), and if
accepted **amends the plan** (e.g., annotate beat 1's E with an
affects-protagonist flag) and re-renders plan-pure from the amended plan.
The edit is never piped into the renderer's next beat as raw bytes.

**Authority accounting**: the outside edit has *zero* authority until
deliberation accepts it and it becomes plan. This is the story analog of the
hybrid's "octave latch re-enters as plan input" — except note the asymmetry:
in audio the latch fires on *measured evidence from rendered audio*; in story
the rendered text carries no hidden information (PATH_MECHANICS.md), so the
only legitimate external-input events are *explicit edits from outside the
generator*, never "the renderer noticed something in its own output."

## Where output feedback would CORRUPT

All three are (G)-shaped: beat n computed from (plan, rendered 0..n−1).

### C1 — The telephone-game drift (the narrative AR coherence tax)

**Mechanism**: give the renderer "eyes" — e.g., beat 2's role scan prefers
words that *appear near* words already rendered in beat 1 (a "local
cohesion" heuristic), or `detail()` sentences are chosen to echo the
previous beat's rendered nouns.

**Corruption**: each beat now conditions on rendered noise, not on the plan.
SETUP renders "The detective polished the key. The accordion hung in the
air." — the decorative accordion is now in the byte stream. Beat 1's
cohesion heuristic latches onto "accordion" as the salient object; the
complication becomes about the accordion, not the plan's EVENT
(thunderstorm). By RESOLUTION the story is about an accordion and the beat
sheet's thunderstorm/key/detective threads are dead. This is *exactly* the
audio AR result: motif recurrence 0.741083, where 946 blocks of state carry
made the render diverge from the plan. The narrative version: **Thread
Continuity < 1.0, Plan-Reconstruction Fidelity < 1.0**, degrading with story
length because there is no plan-target pulling back — each beat reinterprets
the last, and the reinterpretation error compounds (the v1 servo's
involution 2-cycle has its narrative twin: beat n echoes beat n−1's noise,
beat n+1 echoes beat n's echo — a neutrally stable drift with no fixed
point at the plan).

**Why it happens**: decorative `detail()` sentences are *plan-irrelevant
by design* — they exist to fill space. A renderer that reads rendered text
cannot distinguish thread anchors from decoration, because the distinction
lives in the plan (class + beat assignment), not in the bytes. Output
feedback inverts the information hierarchy: it treats the *least*
informative representation (rendered bytes) as authoritative over the *most*
informative one (the plan).

### C2 — Corruption amplification

**Mechanism**: same (G) renderer as C1, but now an H1-type write-channel
fault corrupts beat 1's bytes (or a single misclassified word plants a wrong
anchor).

**Corruption**: under plan-pure rendering, a corrupted beat is *contained*:
beats 0, 2, 3 are still correct, and Piece-2-style re-render heals beat 1
exactly. Under (G) rendering, beat 2 conditions on the corrupted beat 1 —
the corruption is now *load-bearing input* to future generation. Re-rendering
beat 1 plan-pure no longer heals the story, because beats 2..3 were computed
from the corrupted bytes; healing requires re-rendering the *suffix*, and the
suffix's "correct" values are now undefined (they were functions of
corrupted input — there is no plan-pure value to restore). The hybrid spec
§2 calls this out for audio: "Forward gain correction is causally wrong…
Re-assertion is the only correction that heals the past." The narrative
version: **(G) makes the past unhealable.** Exception-path healing
structurally requires plan-pure suffixes.

### C3 — Theatrical sensing (the "story RESPOND latch" anti-pattern)

**Mechanism**: mandate a universal rule — "every path gets an output-sensing
event latch like audio's RESPOND" — so story gets one too: after beat 1
renders, "measure" something from the rendered bytes (e.g., count anchor
words) and "correct" beat 2's plan nominal.

**Corruption**: in audio the latch is honest work because the ZCR sensor
reads a physical property the plan cannot compute (synth↔model gap); the
spec is cents-honest about it being octave-scale only. In story there is no
gap: the renderer is a pure function, so "measuring" the output can only
return what the plan already says, *unless* the measurement is wrong —
in which case the latch "corrects" the plan toward a sensor hallucination.
A story RESPOND latch either does nothing (honest but pointless) or
fabricates (dishonest). Mandating it universally would be worse than
useless: it creates a write-path from a biased sensor into the plan with no
information to justify it. (This is the concrete case against universal
*mechanisms* in UNIVERSAL_VS_PERPATH.md.)

## The one subtle case: plan_del's verify/repair pass

`plan_del` already does "detect-and-repair" — but it reads *plan tables*,
not output bytes, and it runs *before* rendering. Is the H2 thread audit
(detecting from rendered text) meaningfully different? Yes, in one way:
the plan-table check can catch *assignment* faults (empty beat) but not
*rendering* faults (anchor dropped by a role-scan bug — the plan looks fine,
the text is wrong). The rendered text is the only place a rendering fault
is visible. So H2's output-reading is genuinely necessary for *detection* —
but the repair is still plan surgery, never renderer feedback. Detection
reads output; authority stays with the plan. That is the whole rule in one
sentence.

## Summary table

| Case | Reads output? | Output authority over future bytes? | Verdict |
|---|---|---|---|
| H1 write-channel heal | yes (detect) | no (re-render plan-pure) | HELP — Piece-2-shaped |
| H2 thread audit + re-plan | yes (diagnose) | no (plan amended, re-render plan-pure) | HELP — latch-shaped, needs deliberation auth |
| H3 external edit adoption | yes (ingest) | no until deliberated into plan | HELP — plan-event-shaped |
| C1 telephone drift | yes | yes — beat n = f(plan, rendered 0..n−1) | CORRUPT — narrative AR tax |
| C2 corruption amplification | yes | yes | CORRUPT — makes the past unhealable |
| C3 theatrical story latch | yes | yes (sensor→plan write) | CORRUPT — no information, only bias |
| plan_del verify/repair | no (reads plan tables) | n/a | native, fine, keep |
