# B-β test results

## Benchmark: kids playing and laughter — `bbeta_kids_tag.wav`

Render: `./assemble kids bbeta_kids_tag.wav` (seed 20260922).
SHA-256 `a5e44d0a98704d50b19bdc142914a1de6ddefe1a3c5bfb0efb4c08dd8f1974a0`
— **3/3 byte-identical** across independent renders.
(2026-09-22: re-rendered after RNG remediation in `mine_bed.py`; the
bed records are now fully deterministic. This changed the render hash.)

### Preregistered gates (defined before listening; deviation noted below)

| Gate | Bar | Result |
|---|---|---|
| Format | 30 s, 44.1 kHz, mono, 16-bit | PASS (30.000 s exactly) |
| ≥3 child voices | 3 distinct | PASS (PIP/WREN/ASH + background) |
| Overlapping play | voices overlap | PASS (25-laugh chain, 24 overlaps) |
| Running feet | footstep sequence | PASS (23 steps, 260–404 ms cadence) |
| Laugh tumbling into next | onset before prev end | PASS (24/25 chain links) |
| No-copy audit | worst 2 s NCC < 0.75 | PASS (0.182) |
| A-NATIVE | 6 sub-checks | 5/6 PASS — floor-spectrum sub-check FAILS (see note) |
| Social falseness S1–S5 | 8 checks | PASS (contagion shrinks −88→−104 ms, multi-voice, cadence, tag causality, breath arc 615→452 ms) |
| Lineage | every span in-source | PASS (88/88 placements) |
| Anti-rename | no synth mechanisms | PASS (grep audit, §5 of DERIVATION_kids.md) |
| Determinism | byte-identical 3/3 | PASS |

### A-NATIVE floor-spectrum note (one sub-check fails; documented, not tuned)

5/6 sub-checks pass (ZCR 0.0516, exposed hiss 0.001 CLEAN, crest 8.0,
DC −0.000031, headroom 3.0 dB, clicks within nature). The floor-spectrum
sub-check fails: the quietest 1 s (second 10) measures 11.4/11.4/−1.9 dB
(flat) instead of a natural fall.

Evidence this is measurement contamination, not a bad floor:
- Every bed segment in isolation shows strong natural fall (b1−b2 4–15 dB).
- The bed as placed in the mix measures 4.8/1.6/−28.3 dB (natural fall).
- Second 10 contains a real laugh tail (265 ms) + 4 footsteps; the events
  dominate the second's spectrum. The pre-remediation render passed the
  same check only because its quietest second (12) happened to contain
  steps but no laugh — selection luck, not a quality difference.
- The piece was NOT retuned to pass; retuning air to satisfy a
  quietest-second heuristic would be Goodhart. The blind test (with real
  playground calibration) is the arbiter of whether the quiet moments
  sound natural.

### Honest pre-verdict (before blind judging)

- The piece implements the brief's letter: 30 s, ≥3 voices, running feet,
  laughs tumbling into each other, all from captured sources, no synth.
- Known risks for Micah's ears: (1) the three "characters" are cluster
  assignments, not verified individuals — a listener may hear 2 or 4
  children rather than exactly 3; (2) the tag-game narrative is carried by
  timing, not words — no judge will hear "tag" literally, only the
  chase-stop-gasp-contagion shape; (3) the quietest moments may still read
  emptier than a real recording.
- No claim is made about winning the blind bake-off.

### Protocol deviation (disclosed)

The no-copy bar (0.75), the social S1–S5 checks, and the A-NATIVE bar were
defined **after the first render**, not before it as originally instructed.
They were frozen before all subsequent revisions and the final render
passes them, but they are not genuine pre-render preregistration. The
blind judging (designed before any listening) is the untainted check.

### Blind bake-off — PACKAGE READY, judging pending

`blind/`: A/B/C = {B-β piece, same-brief synth control, real-playground
calibration}, deterministic shuffle (seed 20260922), key sealed in
`blind/KEY.sealed.txt`, brief in `blind/BRIEF.txt`. All three 30.000 s.
Builder-knowledge caveat: the mapping was generated in this session, so
the builder (this agent) must be excluded from judging.

- [ ] Five fresh native critics (parent to arrange — depth-2 cannot spawn)
- [ ] Micah's verdict (final authority; one "sounds like a synth" kills)

## Test 2: Kethra's planet voice — `bbeta_kethra.wav` — ALL GATES PASS

Render: `./assemble kethra bbeta_kethra.wav` (seed 20260922).
SHA-256 `0b72af1afdc5dd5e76f19826782ee715310e8b72f98054635e60caefd4000f99`
— **3/3 byte-identical**.

| Gate | Bar | Result |
|---|---|---|
| Format | 21 s (matches v2), 44.1 kHz, mono, 16-bit | PASS (21.000 s) |
| No-copy | worst 2 s NCC < 0.75 | PASS (0.632) |
| A-NATIVE | 6 sub-checks | PASS (ZCR 0.062, hiss CLEAN, crest 5.9, headroom 3.0 dB) |
| Lineage | every span in-source | PASS (51/51 placements) |
| Anti-rename | no synth mechanisms | PASS (grep audit; beating is acoustic, rising tones are vocal) |
| Determinism | byte-identical 3/3 | PASS |
| 10-element structure | v2's world, rebuilt | 9/10 — ice cracks OMITTED (no captured crack source; documented in DERIVATION_kethra.md, not faked) |

### Honest pre-verdict

- The nine chorus events are real loon yodels with hash-walk spacing
  (2.0–15.9 s, all gaps distinct); the hum is real beating between
  captured throat drones; moon-breath is real 16 s ocean swells on the
  18 s tidal clock.
- Known risks: (1) a listener may hear "bird/whale" and convict it of
  Earth pastiche — the defense is structural (alien causal grammar), the
  verdict is the judges'; (2) only 4 throat-drone records fed both the
  hum and the groans (vetoed picks, but a small pool).

### Blind A/B vs v2 — PACKAGE READY, judging pending

`blind_kethra/`: A/B = {v2, B-β rebuild}, deterministic shuffle, key
sealed, brief with kill bars ("sounds like a synth" kills; "Earth
pastiche" majority kills). Builder excluded from judging.

## Test 3: alien ocean surf — `bbeta_ocean.wav` — ALL GATES PASS

Render: `./assemble ocean bbeta_ocean.wav` (seed 20260922).
SHA-256 `904833c220d38eb95270dde2e3d087a3de27dae57e878c3fa9b0138c5f978654`
— **3/3 byte-identical**.

| Gate | Bar | Result |
|---|---|---|
| Format | 30 s, 44.1 kHz, mono, 16-bit | PASS (30.000 s) |
| No-copy | worst 2 s NCC < 0.75 | PASS (0.492) |
| A-NATIVE | 6 sub-checks | PASS (ZCR 0.0516, hiss CLEAN, crest 6.2, headroom 3.0 dB) |
| Lineage | every span in-source | PASS (40/40 placements, 3 reversed) |
| Anti-rename | no synth mechanisms | PASS (reversal is an allowed arrangement op) |
| Determinism | byte-identical 3/3 | PASS |
| Dawn arc | energy/density shift 0→30 s | PASS (rms 2917 → 4698 → 3602 across phases) |
| Sky-conducts-sea | crashes under whale phrases | PASS (5 crashes inside 8–21.5 s sky phase) |

### Honest pre-verdict

- The alien grammar is structural: crashes timed by whale-phrase onsets,
  every 3rd crash reversed, no fixed wave period anywhere.
- Known risks: (1) Earth-pastiche is the kill bar and the materials are
  Earth recordings — if judges hear "beach with whales," it fails;
  (2) the dawn chorus is sparse (2 loon calls) — thin by design, may read
  as empty.

### Blind judging — PENDING

No blind package built for Test 3 yet (no synth-control/ocean-calibration
pair defined). Options for the parent: A/B against an Earth-beach
recording (pastiche test), or a three-way with a same-brief synth ocean.

## Kill-bar status

No kill bar has tripped on any gate. All three pieces await ears.

---

## v2: natural ending — `bbeta_kids_v2.wav` (2026-09-22)

Micah's ear verdict on v1: "more cutouts then a bit realistic and weird" —
plus the shared defect: "they all cut off weirdly" at the end. The v1
render ended mid-sound (last 100 ms max 3789/32768, chopped by the 30 s
file boundary; the writer's 30 ms edge fade cannot hide a chop from that
level). v2 re-renders the kids clip with a natural ending. Same seed
(20260922), same catalog (`catalog_kids.bin`), same phases and tag grammar.

### What changed (compositional, in `mech_kids.zag` `score_kids` only)

1. **P4 settle dissolves by ~28.3 s.** The third giggle (was @28612, ended
   29067) and fourth footstep (was @28710, ended 28910) are still
   *picked* — the deterministic `ctr` sequence is preserved, so every
   later phase's picks are unchanged — but not *placed*. The distant call
   moves 28200 → 28100 ms (same picked event, 246 ms) so its tail fully
   decays by 28.35 s. P4 is now: 2 breathy giggles, 3 slow steps, 1
   distant call — the game dissolves instead of running to the file's edge.
2. **The ending is the quietest captured air.** The bed's deterministic
   picks run unchanged through bedt=27956 (15 segments, identical to v1),
   preserving `ctr` for all later phases. v1's two tail bed segments
   (which summed to the 3789 chop at the 30 s clip) are still picked but
   not placed; instead the file's ending is covered once by the quietest
   bed record (deterministic catalog query: min peak over bed records =
   catalog idx 73, src kids_berlin 89505–91843 ms, peak 476). That record
   is captured air that genuinely resolves to its natural floor (per-100 ms
   max 476 → 14 across its 2338 ms). No fades, no processing, same 300 ms
   overlap, same target peak — choosing, not shaping.

Render: `./assemble_v2 kids bbeta_kids_v2.wav` (seed 20260922; `assemble_v2`
built from the edited `mech_kids.zag`, v1's `assemble` binary untouched).
SHA-256 `882a29bd7d99f982cd2e1c32e2625bc1880344f8b839de14e41049ce049f620a`
— **3/3 byte-identical** across independent renders.

### Gates

| Gate | Bar | Result |
|---|---|---|
| Format | 30 s, 44.1 kHz, mono, 16-bit | PASS (30.000 s exactly, 1323000 frames) |
| Tail decay | genuine decay to quiet floor, final 100 ms ≤ ~1000 | PASS — last-2 s per-100 ms max: [6656, 5238, 3894, 3679, 1236, 1274, 805, 674, 595, 634, 511, 595, 488, 612, 527, 494, 539, 499, 494, 482]; final 100 ms max = 482 |
| Only bed after ~28.35 s | no events past the call's decay | PASS — last placed event (distant call) ends 28346 ms; 28.35–30 s is bed only |
| A-NATIVE | 6 sub-checks, same gates as v1 | 5/6 PASS — identical to v1 (ZCR 0.0508, hiss CLEAN 0.001, crest 8.0, DC −0.000027, headroom 3.0 dB, clicks within nature; floor-spectrum sub-check fails with the same 11.4/11.4/−1.9 signature on second 10 — the documented measurement-contamination note still applies, not retuned) |
| Social falseness S1–S5 | 8 checks | PASS (lineage 85/85, cadence 260–404 ms, tag 13.0–13.5 s, 24 tumble overlaps, contagion −88→−104 ms, multi-voice, breath arc 615→452 ms) |
| No-copy | worst 2 s NCC < 0.75 | PASS (0.179) |
| Determinism | byte-identical 3/3 | PASS |

### Pre-28 s unchanged (verified, with one honest caveat)

Placement-log diff v1→v2: all 15 bed placements before bedt=27956 ms and
all P0–P3 and early-P4 placements are identical; only the tail lines differ
(2 bed segments → 1 quiet-air segment @27956; giggle3/step4 unplaced; call
28200→28100). The picked events are unchanged (same `ctr` sequence).

Caveat: the rendered PCM samples before 28 s differ from v1 by a global
~17 LSB DC offset (inaudible: −66 dBFS, constant). Cause: the writer's
whole-file DC removal sees a different mix mean after the tail change, so
its `(m−mean)` subtraction shifts every sample. The *events* are identical;
the shift is the established writer's correct response to a changed mix,
not a content change. (The bed-air swap itself begins at 27956 ms, 44 ms
before the 28 s mark — inside the "~28 s" tolerance; everything before
27.956 s has identical placements.)

### Cutout diagnosis — CONFIRMED content-by-design (not recomposed)

Micah's "cutouts" were re-measured on v1 at 10 ms / 50 ms resolution:
- 13.0–13.4 s: the TAG shout (peaks ~18578) decays, then the envelope
  drops to ~900–1130 for ~half a second — the deliberate P2 halt ("steps
  stop dead; everything halts" when the tag lands, DERIVATION_kids.md §1).
- 25.8–26.8 s: dips to ~908–1265 around 26.0 s — the P3→P4 transition gap
  before the first settle giggle @26200.
- Zero 10 ms windows below 150/32768 in the full 30 s: **no digital
  dropouts, no gate-like dips, no hard onsets.**

These are the phase grammar's deliberate halts — content by design, the
same mechanism that makes the tag land. Per the task rule (fix only
artifact defects), they were NOT smoothed or recomposed. v2's pre-28 s
events are the same, so the halts are preserved.

### Honest pre-verdict (v2)

- The ending is now a genuine dissolve: last event decays by 28.35 s,
  then ~1.65 s of quiet captured air resolving to its natural floor
  (final 100 ms max 482/32768 — the writer's 30 ms edge fade handles the
  boundary inaudibly from this level).
- Known risks carried over from v1: (1) the three "characters" are cluster
  assignments, not verified individuals; (2) the tag narrative is carried
  by timing, not words; (3) the quietest moments may still read emptier
  than a real recording.
- The v1 file (`bbeta_kids_tag.wav`, SHA
  `a5e44d0a98704d50b19bdc142914a1de6ddefe1a3c5bfb0efb4c08dd8f1974a0`)
  is untouched — the verdict trail stays intact.

## v3: continuity fix (2026-09-22)

**Binding law:** imagination doesn't cut out. The v2 "content by design"
defense of the tag-halt (~13 s) and the P3→P4 transition gap (~26 s) is
rejected per the frozen cutout-debate mechanism: the fix replaces
event-only/silence-node composition with world-first composition — a
continuous evolving bed, the tag boundary as a pivot (not a halt), and
overlapping content across phase boundaries. It is not a crossfade.

**Changed file:** `mech_kids.zag`, function `score_kids` only. Seed
20260922, `catalog_kids.bin`, pure Zag, zero RNG preserved. v1
(`bbeta_kids_tag.wav`) and v2 (`bbeta_kids_v2.wav`) untouched.

**The compositional changes (all inside `score_kids`):**
1. P1's chase steps now continue to the phase boundary (no 400 ms early
   stop — the halt grammar is dead).
2. P2 is a pivot, not a halt: WREN's TAG still lands at 13.100 s; PIP's
   reversed gasp-laugh begins 101 ms into the tag (overlapping, not
   abutting); the feet keep moving in a new slower cadence (380–560 ms
   repositioning steps, mean 410 ms vs P1's 332 ms). A breath-bed
   (reversed laugh at low gain, the children's exertion breath) swells
   under the pivot so the world's air carries through the boundary.
3. P4 is a thinning tumble across the phase boundary, not a restart:
   giggle1 overlaps P3's last laugh by 101 ms, giggle2 overlaps giggle1
   by 100 ms, giggle3 overlaps giggle2; two steps enter overlapping
   (bridge density) then space out as the game dissolves.
4. The v2 natural ending is re-derived, not regressed: fourth step still
   picked-not-placed, distant call still at 28100 ms (ends 28346 ms),
   no events after 28350 ms, final 100 ms max 520/32768.

**Render:** `bbeta_kids_v3.wav` — 30.00 s, 44.1 kHz, mono, 16-bit.
SHA256 `94349376a35bd7dbc5d31ab5173c309243f19293680a91399674de22082baecb`
(byte-identical 3/3 independent renders). Placement log:
`work/place_kids_v3.log` (90 placements, 90/90 lineage-valid).

### Continuity metric (`/tmp/continuity.py`, v3 vs v2)

| Boundary | v2 floor | v3 floor | Ratio | Bar (≥3× v2) | Depth v2→v3 |
|---|---|---:|---:|---|---|
| 13.2 s (tag pivot) | 0.0094 | 0.0250 | 2.66× | 0.0282 — **MISS** | −4.6 dB → **+2.6 dB** |
| 26.2 s (P3→P4 bridge) | 0.0090 | 0.0157 | 1.74× | 0.0270 — **MISS** | −12.2 dB → −8.5 dB |

**Deviation (honest):** the 3× absolute-floor bar is NOT met. What was
fixed structurally: the half-second near-silence at the tag is gone
(the boundary is now 2.6 dB *louder* than its flanks — a pivot, not a
halt), and the 800 ms P3→P4 gap is filled by an explicit overlap chain
(giggle1 25847–26073, giggle2 25973–26257, giggle3 26157–26612, steps
26361/26481 overlapping — every bridge frame carries overlapping event
energy). What remains are 10 ms natural envelope dips of real captured
events (0.0250 at 13.2 s during the gasp's breath pause; 0.0157 at
26.2 s in giggle3's tail) — not commanded silences, mix gaps, or gate
dips. Five compositional iterations confirmed this is the envelope
floor of the deterministic record picks, not a placement gap: adding
further layers to chase the absolute 10 ms minimum would be metric
tuning (Goodhart), not world-building. The companion bar — no ≥300 ms
window below the bed floor at a flagged boundary absent from controls
— **PASSES** (13.2 s: 190 ms; 26.2 s: 10 ms; controls: 50 ms / 0 ms).

### v3 gate table

| Gate | Bar | Result |
|---|---|---|
| Format | 30 s, 44.1 kHz, mono, 16-bit | PASS (30.000 s, 1323000 frames) |
| Determinism | byte-identical 3/3 | PASS |
| Continuity floors | ≥3× v2 (0.0282 / 0.0270) | **MISS** — 2.66× / 1.74× (see deviation above) |
| No ≥300 ms sub-bedfloor run | absent at flagged boundaries | PASS (190 ms / 10 ms) |
| Pivot depth @13.2 s | boundary not quieter than flanks | PASS (+2.6 dB; was −4.6 dB) |
| Tail decay | genuine decay, final 100 ms ≤ ~1000 | PASS (final 100 ms max 520) |
| Only bed after ~28.35 s | no events past call's decay | PASS — last event ends 28346 ms |
| A-NATIVE | 6 sub-checks, same gates as v2 | 5/6 PASS — identical signature to v2 (ZCR 0.0502, hiss CLEAN 0.001, crest 7.9, DC −0.000028, headroom 3.0 dB, clicks within nature; floor-spectrum sub-check fails with the same flat signature — the documented measurement-contamination note still applies, not retuned) |
| Social falseness (v3-adapted S1–S5) | 12 checks | PASS (lineage 90/90, P1 cadence 260–404 ms, tag 13.1 s, gasp/tag overlap 101 ms, pivot cadence 380–560 ms, 23 tumble overlaps, contagion −93→−100 ms, multi-voice, breath arc 723→419 ms, bridge overlap 101 ms, 2 bridge overlaps) |
| No-copy | worst 2 s NCC < 0.75 | PASS (0.212) |

### Honest pre-verdict (v3)

- The world no longer cuts out at the two flagged seams: the tag is a
  pivot the children move through (breath, gasp, and feet overlapping
  the shout), and the tumble thins across the P3→P4 boundary instead of
  stopping and restarting. The bed is continuous throughout.
- The 3× absolute-floor bar is missed (2.66× / 1.74×). If Micah's ears
  still hear a "cutout" at either seam, it will be a natural breath
  pause inside a real laugh, not a composed halt — and that distinction
  is measurable in the placement log.
- Known risks carried over: (1) the three "characters" are cluster
  assignments, not verified individuals; (2) the tag narrative is carried
  by timing, not words; (3) the A-NATIVE floor-spectrum sub-check still
  fails on the documented contaminated heuristic.
