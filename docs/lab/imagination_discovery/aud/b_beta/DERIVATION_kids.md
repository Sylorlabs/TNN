# DERIVATION — "tag at dusk" (B-β kids benchmark)

Piece: `bbeta_kids_tag.wav` — 30 s, 44.1 kHz mono 16-bit.
Mechanism: `mech_kids.zag` (fresh, written for this brief; did not exist before it).
Seed: 20260922. Render SHA-256 (3/3 byte-identical): `a5e44d0a98704d50b19bdc142914a1de6ddefe1a3c5bfb0efb4c08dd8f1974a0`

## 1. The imagined scene (the commitments)

A game of **tag at dusk on a playground**, three children, five phases.
This is the world the mechanisms are derived from — not a design checklist:

- **PIP** (catalog voice 0 — the `kid_laugh` 4-year-old, bright, breathy):
  the youngest, the one who gets caught. Laughs first when tagged because
  being caught *is* the joke to a four-year-old.
- **WREN** (catalog voice 1): the fastest, the tagger. Her "TAG!" is short
  and sharp — she is already running past.
- **ASH** (catalog voice 3): the loudest, the commentator. Shouts the
  play-by-play, laughs hardest, runs out of breath first.

Phases and their causal logic:

| Phase | Time | What happens | Why |
|---|---|---|---|
| P0 taunt | 0–5 s | Sparse calls across the playground | The game hasn't started; children are arriving, calling out |
| P1 chase | 5–13 s | Running steps (260–404 ms cadence), shouts, short laughs | Feet must precede the tag — cause before effect |
| P2 TAG | 13–15 s | Steps stop dead; WREN's "TAG!"; PIP's gasp | The touch lands; everything halts for half a second |
| P3 tumble | 15–26 s | Contagion laugh chain, voices tumbling into each other, shrinking latencies, draining breath | Laughter is socially contagious; each burst leaves less air |
| P4 settle | 26–30 s | Breathy giggles, slow steps walking away, one distant call | The game dissolves; someone goes home |

A continuous **bed of real playground air** (quiet segments from the
Berlin and playground recordings, alternating sources) runs underneath:
a real scene is never digital silence between events. The first render
without it failed A-NATIVE's floor-spectrum gate — correctly, because
digital silence is not a natural acoustic floor.

## 2. What the study taught (the (b) component)

From `catalog_kids.bin` (85 records: 73 event + 12 bed):

- The `kid_laugh` file holds ~11 laugh events from one bright young voice
  plus 2 real shouts; deterministic spectral clustering of the two group
  recordings separates into stable voice groups (voices 1/2 and 3/4).
- Real footstep sequences (`forest_track4`) run at 260–400 ms IOI when
  running — this set the P1 cadence band, measured not assumed.
- **Honesty boundary:** clustering suggests distinct voice groups; it does
  not prove speaker identity. PIP is *assigned* to voice 0 (the file is
  documented as one 4-year-old); WREN/ASH are stable clusters treated as
  characters. The docs never claim verified identity beyond the file's own
  documentation.

## 3. Mechanisms derived (the (c) component)

Each exists because the scene demands it; none is a generic sequencer part:

1. **Contagion clock** — each laugh's end schedules the next voice's laugh
   with latency `lat = 110 − hysteria·12 − peak/600` (min 0), and the next
   laugh starts up to 120 ms *before* the previous ends. Louder laughs and
   rising hysteria shorten the gap: this is a model of *being unable not to
   laugh*, not a rhythm generator.
2. **Breath ledger** — per-child 3000 ms budget, recovery at ¼ real time.
   As budget drains, only shorter laughs are eligible (2600 → 1000 → 500 ms
   caps). The first calibration (5000 ms, full recovery) never engaged —
   caught by the S5 gate, recalibrated until the arc was structural.
3. **Tag-game phase graph** — steps are forbidden after 13.0 s; the shout
   must land 13.0–13.5 s; the gasp follows; only then does contagion start.
   Cause precedes effect, enforced by construction.
4. **Voice rotation with veto memory** — PIP→ASH→WREN rotation, no event
   repeated within 2 picks, no laugh repeated within the chain. Prevents
   the "same sample again" falseness.
5. **Deterministic choice** — every pick is `h32(20260922, counter) mod
   pool`, vetoes walk the pool. Zero RNG; the piece is byte-identical
   across renders by construction.

## 4. What was rejected (and why)

- **A copied 30-second ambience bed.** The first design had no bed at all
  (digital silence); the fix was *alternating short captured segments from
  2+ source regions*, never one unmodified passage — the no-copy audit
  (worst 2 s NCC 0.387 < 0.75) confirms.
- **Synthetic envelopes/fades.** Only 3 ms seam fades at cut points
  (click prevention) and constant per-placement gain. No ADSR, no swells.
- **Pitch/time modification.** Rejected outright — it would make the
  sources say something they never said.
- **Granular microslicing.** Every placed unit is a complete captured
  event (hundreds of ms); nothing is built from <50 ms grains.
- **The tag shout from ASH's pool.** ASH has zero shout events in the
  catalog; the mechanism was changed to use WREN's real shout rather than
  relabel a laugh. The catalog is not re-tagged to suit the drama.
- **Breath ledger v1** (5000 ms / full recovery): never engaged, caught by
  the S5 gate, recalibrated to 3000 ms / ¼ recovery until the arc was real.

## 5. Anti-rename audit (this is not a synth in disguise)

| Prohibited mechanism | Present? | Evidence |
|---|---|---|
| Oscillator / periodic generator | No | `grep` for osc/sine/tri/saw in `*.zag`: no hits in production path |
| Resonator / filter | No | No feedback delay networks, no biquads, no convolution |
| Synthetic noise / hiss bed | No | Bed is captured air; A-NATIVE exposed-hiss gate: CLEAN (0.000) |
| Chirp / boom / designed drum | No | Steps are captured footstep events, unmodified |
| Additive resynthesis | No | No partials, no spectral processing of any kind |
| Granular synthesis | No | Smallest unit is a complete captured event; no grains |
| Pitch/time modification | No | Events play at captured rate, captured pitch |
| `synth.zag` import | No | `assemble.zag` imports only `mech_*.zag`; verified by inspection |

The only arithmetic on samples: constant Q16 gain, 3 ms seam fades,
addition into the mix bus, DC removal + normalization in the writer.
All are *opinionless* (gain staging), not *opinionated* (a resonator wants
to ring; a gain does not).

## 6. Lineage

`work/place_kids.log` (regenerate: `./assemble kids <out> log`) lists all
88 placements as `dst_ms src_id src_start_ms src_end_ms voice target rev`.
Every span verified inside its source's duration (`social_check.py`
lineage gate). Source IDs → files: see SOURCES.md.
