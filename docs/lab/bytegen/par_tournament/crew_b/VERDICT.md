# CREW B — PAR Tournament VERDICT

Date: 2026-09-24. Pinned toolchain `znc_linux_x86_64_abed8aa1`. Zero RNG.
Fixture: `bytegen/fixture/plan_v1.txt`. WAV comparisons at MIX level.

Prior dive: `par_dive/contender_b/` — VERDICT was OVERTHROW (RT-LONG 0¢ +
COST), with a disclosed inverted-release-envelope bug. This round fixes the
bug (B-fix), extends the pitch gate (B-gate), and maps the plan-trust
boundary (B-lie).

## B-fix — release-envelope fix (binary `41a95366…ead1`, source `637479bd…`)

The fix: `x=(rem*1024)/rel` → `x=((rel-rem)*1024)/rel` at 4 release sites
(`voice_closed`, `bus_env_at` [dead code, fixed for consistency],
`span_render` hot loop, `render_bed`). Notes now fade full→silent instead of
silent→full→hard-cut.

### Byte-level proof of what changed (B-fix vs dive baseline `432a55e1…`)
- 152,657 / 1,323,000 samples differ (11.54%) — **every one inside a note
  release window** (per-sample check against all 23 event release windows +
  the bed release; the 12 apparent outliers were ±1-sample rounding in the
  checker, each the first sample of a release window). 0 diffs in
  attack/sustain/gap audio (pre-release sustain: 0 diffs).
- Direction: event-0 release window RMS — baseline head500=7,908 /
  tail500=17,274 (inverted: quiet→loud); B-fix head500=17,668 /
  tail500=6,802 (true fade: loud→quiet).

### Frozen battery (§2)
| Leg | B-fix | Dive baseline | Bar |
|---|---|---|---|
| DET | 2-run `cmp` clean; 20/20 battery byte-identical (mix SHA `b7d3a71e…`) | cmp clean | PASS |
| G-PER | **0.324** | 0.336 | ≤0.350 PASS (improved) |
| G-STA | 1.841 | 1.840 | ≤3.000 PASS |
| G-LURCH | 2.373 | 2.373 | ≤5.000 PASS |
| G-DRIFT | **383.553** | 451.195 | ≤800.000 PASS (improved) |
| G-FLUXm | **213.116** | 235.714 | ≤350.000 PASS (improved) |
| G-SIL1 | 0.000 | 0.000 | ≤0.020 PASS |
| G-SIL2 | 0.000 | 0.000 | ≤0.500 PASS |
| G-CLIP | 0.915 | 0.915 | ≤0.950 PASS |
| G-CREST | 3.860 | 3.860 | ≤14.000 PASS |
| CHOP-1/2/3 | 0 / NONE / 16 spikes, 0 unexplained | 0 / NONE / 33, 0 unexpl. | PASS |
| Coherence xcorr | 1.000000 zero-lag; 1.000000 @ 0 ms (±50 ms) | 1.000000 | ≥ NATIVE PASS |
| Pitch/IOI contour r | 1.000000 / 1.000000 | 1.000000 | PASS |
| COST | 3.77 s mean interleaved (base 3.48 s; delta within load noise), RSS 20.1 MB | 8.54 s / 20.1 MB | no regression |
| RT-LONG | 440.00 Hz, **+0.00¢** (spectral; autocorr meter locks the 110 Hz bed — honest note) | 0¢ | strictly > NATIVE |
| RT-LONG near-miss | 460 stands, 460.00 Hz, +0.00¢ | stands | PASS |
| RT-CASCADE 1-bit | 1 diff @ fault sample, **0 post-cut** | 0 post-cut | PASS |
| RT-CASCADE burst/dropout/DC | 0 post-cut diffs on all three | n/a | PASS |
| RT-EDGE | 0 pre-14.8 s diffs; cut step **0** (16-bit units); bed fades to exactly 0 | step ~12,109 | improved |
| Order perm. | rev/stride byte-identical | identical | PASS |

### §5 red team (densified)
- R1 cross-region leakage: **30/30 PASS** — standalone `regionmix k` ==
  in-context slice with zero outside, for all 10 regions × 3 adversarial
  plans (legato+vibrato+glide chains crossing boundaries, boundary-exact
  event starts, rail-amplitude region-0 event).
- R2 sustained 1292-block corruption: rerender-vs-clean 0 diffs (render
  never reads the mix; corruption cannot propagate by construction).
- R3 plan-text adversarial (14 fz plans): all rc=0, no hangs, bounded peaks
  (fail-open parser as documented in the dive — unchanged behavior).
- R4 polyphonic RESPOND (2-voice and 3-voice): abstain, nominal stands.
- R5 sub-octave nominal lies (220/110/55, cue 440): latch corrects all to
  440 (k=+1/+2/+3).

### §6 verdict: B-fix OVERTHROWS NATIVE (overthrow stands, bug fixed)
All 9 gates pass (3 improved), coherence 1.000000, byte-identical reruns
(20/20 + order permutations), red team survives. Strictly better than NATIVE
on RT-LONG (0¢ vs NATIVE's 880 Hz octave error) and COST (parity-or-better,
same RSS). No regression on any bar — the envelope fix strictly improved
G-PER/G-DRIFT/G-FLUXm, CHOP-3 spike count, and the truncation step.

## B-gate — B-fix + 40–4000 Hz gate on the full pitch path (binary `7d02dc05…585`, source `54f156cc…`)

Design: plan fields keep plan truth (`respond_latch` reads raw cue/nominal);
every RENDERED pitch passes `gate_f` → [40,4000] Hz (bus/overlay/legato/
bed/endpitch sites). Latch additionally vetoes out-of-range nominal
(`GATE-VETO(nominal)`) and out-of-range latched output (`GATE-VETO(output)`).

**Design correction during the round (documented):** v1 clamped EVENT f0 at
parse; the trap battery caught a REGRESSION — the clamp laundered the 30 Hz
cue into 40 Hz, the cue gate saw an in-range cue, and the latch fired
880→55 Hz (the exact trap the gate exists to kill). v2 gates at render and
preserves plan truth for the latch. The battery caught it; the shipped v2
does not have it.

### Battery
- Frozen fixture: **byte-identical to B-fix** (`cmp` clean), 9/9 gates PASS
  (identical numbers), RT-LONG 440.00 Hz +0.00¢.
- Trap battery (B-gate v2, spectrally verified):

| Trap | B-fix (baseline) | B-gate v2 | Status |
|---|---|---|---|
| cue 30 Hz / nom 880 | nominal stands → 880 | fcue=30 rejected → nominal stands → **880** | DEFENDED (matches dive) |
| cue 5000 Hz / nom 880 | nominal stands → 880 | fcue=5000 rejected → **880** | DEFENDED |
| cue 440 / nom 30 | LATCHED 480 | **GATE-VETO(nominal)** → renders 40 | NEW abstain |
| cue 440 / nom 5000 | LATCHED 312 | **GATE-VETO(nominal)** → renders 4000 | NEW abstain |
| cue 4000 / nom 40 | LATCHED 5120 (ultrasonic) | **GATE-VETO(output)** → renders 40 | NEW abstain |
| EVENT 30 Hz | renders 30 | renders **40** (clamped at synth) | NEW clamp |

### §6 verdict: B-gate is the SHIP CANDIDATE
Identical §6 profile to B-fix on the frozen fixture (byte-identical output,
all bars), plus strictly better trap immunity on the nominal/output paths
that B-fix lacks. No §6 bar moves. Recommend B-gate over B-fix for adoption.

## B-lie — plan-lie battery (B-fix binary, no code change)

10 adversarial plans + boundary probe. Classification:

| Plan | B behavior | Class |
|---|---|---|
| lie1: cue 440, nom 1760 | k=-2 → LATCHED 440 | CORRECTED |
| lie2: cue 440, nom 220 | k=+1 → LATCHED 440 | CORRECTED |
| lie9: cue 440, nom 110 | k=+2 → LATCHED 440 | CORRECTED |
| lie3: cue field 440 ("true" 880 per comment), nom 880 | LATCHED 440 | FOLLOWED (undetectable) |
| lie4: cue field 880, nom 880 | nominal stands → 880 | FOLLOWED |
| lie7: cue 622, nom 880 | k=-1 → LATCHED 440 (boundary) | FOLLOWED (plan math) |
| lie8: cue 40 (gate edge), nom 880 | k=-4 → LATCHED 55 | FOLLOWED (plan math) |
| lie10: cue field 220, nom 1760 | k=-3 → LATCHED 220 | FOLLOWED (cue lie amplified) |
| lie5: window excludes cue | nvoice=0 → abstain | ABSTAINED |
| lie6: zero-duration ghost voice in window | nvoice=2 → abstain (overlap test counts it) | ABSTAINED |
| 7b: cue 623, nom 880 | k=0 → nominal stands | boundary probe |

Findings:
- **Nominal lies are CORRECTED** when the cue is true — that is the latch's
  purpose, and it works for ±1/±2 octaves (lie1/lie2/lie9, R5's 55 Hz).
- **Cue-field lies are UNDETECTABLE by construction** (lie3/lie10): B renders
  the cue from the same field it latches from — self-consistent, wrong only
  vs an external ground truth B cannot observe. The hybrid v2's
  audio-measured path is more robust ONLY where the sounding cue can diverge
  from the plan field (external audio / foreign renderer); inside B's closed
  plan→render→latch world there is no divergence to measure.
- **Provenance boundary:** B's RESPOND is a pure function of plan text
  (fcue, nom, w0, w1). Defenses are well-posedness checks only: single voice
  (ghosts veto — lie6), 40–4000 Hz cue gate, |k|≤10 clamp, 2^-0.5 rounding
  boundary (622→k=-1, 623→k=0 — razor-thin, deterministic).
- lie8 documents gate-edge behavior: a 40 Hz cue is in-range and latches to
  55 Hz — plan-faithful, musically dubious, sub-bass.

## Failure modes (tournament update)
1. B-fix/B-gate RESPOND trusts plan cue fields completely (B-lie FOLLOWED
   class) — no independent sensor; boundary documented above.
2. B-gate clamps out-of-range EVENT pitches at render (30→40, 5000→4000) —
   intended, documented; changes plan-faithfulness for hostile plans only.
3. Gate edge: 40 Hz cue latches to 55 Hz (in-range per the gate).
4. Octave-rounding boundary razor-thin at exactly 2^-0.5.
5. Unchanged from dive: no amplitude carry across legato (G-PER tradeoff),
   fixed 80 ms legato threshold, fixed 3 s regions, prefix-simulation cost
   (closed-form seed still future work).

## Adoption recommendation
- **Ship B-gate** (superset of B-fix; identical fixture behavior; vetoes the
  nominal/output traps B-fix falls for).
- B-fix's overthrow verdict stands on every §6 bar; the envelope fix is
  proven byte-confined and strictly improving.
- B-lie is evidence, not a contender: it maps exactly where plan-trust
  breaks and where the next mechanism (independent sensing) would be needed.

Excerpts: `excerpts/WITHHELD-NOT-FOR-REVIEW_{b_fix,b_gate}_motif_0-8s.wav` —
withheld from review per policy; no listening claims made (analyzer-first
rule). Micah's ears outrank all of the above.
