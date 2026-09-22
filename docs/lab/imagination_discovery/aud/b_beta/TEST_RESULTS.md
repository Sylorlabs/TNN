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
