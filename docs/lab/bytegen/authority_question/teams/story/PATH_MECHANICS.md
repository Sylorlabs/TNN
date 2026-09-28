# Story path — native mechanics

Source: `~/workspace/tnn-lab/GOALB_STORY/src/` (pure Zag, deterministic, zero RNG —
"Story bytes go only to stdout (the constructed channel); no belief writes."
— `story.zag:3-4`).

## The two halves

Story generation is split into **planning** and **rendering**, and the split
is temporal as well as logical: the plan is fully computed *before* a single
byte is rendered.

### 1. Planning (`story.zag`) — the "plan" is the beat sheet

Two planners produce the same plan data structure, an explicit **beat sheet**:

- `plan_pos` (`story.zag`, "positional"): divides the word set into 4 beats
  by position alone (`base=nw/4`, `rem=nw%4`; words dealt round-robin into
  beats 0..3). No semantics.
- `plan_del` (`story.zag`, "deliberative"): assigns each word to a beat by
  **semantic class** via `first_match` with predicates:
  - beat 0 SETUP: PERSON (protagonist, r=0 CLASS_SLOT; fallback r=1
    FALLBACK_ORDER if no PERSON), then PLACE, then THING
  - beat 1 COMPLICATION: EVENT, then THING|PERSON
  - beat 2 CLIMAX: EVENT|ABSTRACT|PERSON, then THING
  - beat 3 RESOLUTION: ABSTRACT; all leftovers spill here
- Then a **verification + bounded repair** pass (max 2 passes): if any beat is
  empty, steal the last-assigned word of the fullest beat and move it there,
  logged as rule r=2 REPAIR_SPILL. The planner *re-reads its own plan state*
  (beat tables) to check and fix — note: it reads plan tables, never rendered
  output bytes.

The plan is stored in three tables plus an audit log:

| Table | Layout | Content |
|---|---|---|
| `beat` | 4 beats × 12 word-index slots (`beat[(b*12+k)*4]`) | which word goes in which beat |
| `beat_n` | 4 counts (`beat_n[b*4]`) | words per beat |
| `seq_w / seq_b / seq_r` | per assignment (≤24 incl. repairs) | word index, beat, rule used (audit trail) |

The plan is printed verbatim as the `### PLAN` section (`story_main.zag`,
plan print loop): `SETUP: detective(PERSON,CLASS_SLOT) lighthouse(PLACE,...)`.
Every word's beat assignment and the rule that put it there is inspectable.

### 2. Rendering (`story_render.zag`) — template slot-fill, plan-pure per beat

Five beat renderers, each a **pure function of (beat tables, class tables,
template variant tv, plus P/L)**:

| Fn | Line | Beat | What it does |
|---|---|---|---|
| `ww_emit` | 19–21 | — | emits one word's bytes by index (slot fill) |
| `detail` | 4–19 | filler | decorative sentence from word class + parity `dk%2` |
| `r_setup` | 23 | 0 SETUP | protagonist P + setting L sentences; treasured object T (first class-2 word ≠ P,L) |
| `r_compl` | 55 | 1 COMPLICATION | event E (first class-3) "struck without warning"; victim V (first class-2 or 0 ≠ E) |
| `r_climax` | 88 | 2 CLIMAX | R (first class-3/4/0) returned/demanded/arrived; O (first class-2 ≠ R) clutched/faced |
| `r_resol` | 143 | 3 RESOLUTION | H (first class-4) "found/discovered"; protagonist P at setting L |
| `r_posbeat` | 176 | POS 0–3 | positional variant: anchor word + positional templates, no thread threading |

Sentence templates are fixed strings; the *only* choices are which word fills
which slot and the `tv` variant (template variant 0/1, derived from the set
number — plan metadata, not output). Role words (E, V, R, O, H, T) are picked
by **scanning the plan's beat tables for class matches**, not by reading
rendered text.

`story_main.zag` main: P (first PERSON in beat 0, else beat0[0]) and L (first
PLACE in beat 0, else −1) are resolved **once from the plan** and threaded
through all four renderers. Rendering then proceeds beat 0→3 via an
append-only cursor `spos`.

## Carried state across beats — inventory

| State | Type | Verdict |
|---|---|---|
| `spos` (append cursor) | append-only | **bookkeeping**, not generative: removing it changes nothing about any later computation (the survey's exact exclusion) |
| P / L (protagonist / setting) | plan-derived, computed once | **plan state**, not output state: derived from beat tables, never from rendered bytes |
| `dk` (detail alternation) | per-beat local | resets per beat |
| `assigned[12]` bitmap | plan-construction scratch | lives only in `plan_del`, gone before rendering |

**Net: zero generative output→input feedback natively.** No beat reads any
other beat's rendered bytes. The whole story is `story = F(plan)` with each
beat independently computable from the plan — this path is the native
**closest analog of the audio PAR path** (`s[t] = F(plan, t)`), and the survey
classifies it "OTHER (template slot-fill)", not stateful-sequential, because
there isn't even carried DSP state.

## The coherence question: is there a long-range coherence property feedback could degrade?

**Yes, and it is plan-threaded, not feedback-maintained.** The DEL variant
carries four long-range threads across beats:

1. **Protagonist thread**: P established in SETUP, referenced in CLIMAX
   ("The detective held the key tight") and RESOLUTION ("the detective found
   peace").
2. **Setting thread**: L established in SETUP ("lived near the lighthouse"),
   referenced in RESOLUTION ("found peace at the lighthouse").
3. **Object thread**: T treasured in SETUP ("polished the key"), O clutched
   in CLIMAX ("clutching the key") — same-class continuity.
4. **Event arc**: E strikes in COMPLICATION ("the thunderstorm struck without
   warning"), R "returned, worse than before" in CLIMAX.

All four are guaranteed **by plan structure**: P/L are threaded explicitly
from the plan; T/O/R/H/E/V are class-matched from the plan's own beat
tables. The renderer never consults prior rendered text to maintain them —
which is why feedback cannot *maintain* them (there is nothing to maintain
that the plan doesn't already guarantee) but a feedback-based renderer
* could* degrade them (see FAULT_ANALYSIS.md): if beat 2 conditioned on
rendered beat 1 instead of the plan, it could latch onto a decorative
`detail()` word ("the accordion hung in the air") as the thread anchor and
misroute the object thread — the narrative analog of AR's coherence tax.

The POS variant is the control case: no thread constraints at all (anchor
word per beat only). It shows what "no long-range coherence" looks like
natively — and it still renders plan-pure.

### Measurable analog of motif recurrence (xcorr)

Audio's motif-recurrence metric (PAR 1.000000 vs AR 0.741083) measures
whether re-extracting the motif from the render matches the plan. Story's
analog is **plan-reconstruction fidelity**: from the rendered story text
alone, extract which set-words appear in which beat's text, and compare with
the plan's `beat` tables. Plan-pure rendering scores 1.0 by construction:
every assigned word appears in its beat's text; the renderer never moves a
word across beats. (Full metric proposal in BATTERY_PREREG_DRAFT.md: Anchor
Recall, Thread Continuity, Plan-Reconstruction Fidelity.)

## Bottom line for the authority question

- The "plan" = the beat sheet (`beat`/`beat_n`/`seq_*`), fully frozen before
  rendering begins.
- Rendering is plan-pure per beat; there is no native output feedback, and —
  crucially — **the rendered text contains strictly less information than the
  plan**: every byte is a deterministic function of (beat tables, classes,
  tv, P/L). There is no synth↔model gap as in audio (where K_PLAN had to be
  calibrated because the plan can't compute exact waveforms). The story
  renderer adds zero information the plan didn't already have.
- Consequence: unlike audio's RESPOND latch (which exists because the plan
  is *incomplete* about what actually rendered — octave-scale pitch), story
  has **no native information need that output could fill**. The only thing
  output can tell you is (a) the write channel was corrupted, or (b) an
  outside party changed the text — both are *exception* facts, not
  generative inputs.
