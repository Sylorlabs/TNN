# CONTINUITY ROUND 2 — frozen preregistration

Frozen 2026-09-22 (native test coordinator). Micah's order: "do more test
based off what SOL and grok recommend to hypothesize."
Source hypotheses: `HYPOTHESES.md` (verbatim record, elicited 2026-09-22;
grok-4.6 named as grok-4.6 — grok-4.7 still delisted, no substitution).
Disagreement/overlap map in HYPOTHESES.md: no direct contradictions; all six
run (test-both law).

Committed alone BEFORE any test execution. A hypothesis the test kills stays
killed. Verdict language for this round:

- **KILLED** — the measurements refute the hypothesis (no defect found).
  The fork is not recomposed; no v4 clip.
- **SURVIVES** — the measurements confirm the defect the hypothesis claims.
  The implicated fork is recomposed world-first and a v4 kids clip is
  produced (a fork that survives all tests unchanged is NOT re-rendered).
- **INDETERMINATE** — numbers fall between the preregistered bands; reported
  honestly, no v4, flagged for the red team.
- **DEFERRED** — cannot be run faithfully with available material; reason
  recorded, never faked.
- **PENDING-EAR** — machine-measurable parts executed; the Micah-listening
  criterion cannot be run by the coordinator; blinded clips prepared with a
  sealed key and an exact brief for the parent.

Standing constraints (all tests): pure Zag renders, zero RNG (splitmix/h32
hashes only), 3/3 byte-identical reruns, A-NATIVE re-verified on any new
deliverable clip. Every sound from captured field recordings only —
synthesis is banned. New recordings cannot be captured on the VM.

## Shared infrastructure

- `work/r2g/r2g.zag` — copy of `b_gamma/gamma.zag` (frozen v3 source
  untouched) plus: chunked mix arena (30 s chunks; required because a 300 s
  i64 arena exceeds the znc 2^25-byte single-slice limit), global seed offset
  `GSS` added inside `h32`/`h01` (`pack_load` uses neither — verified), bridge
  mode flag (standard / extended-window control / event-only ablation),
  placement logging `(dst_sample, nsamp, grain_id)` in `place()`, new scores
  `score_ocean_wf` (world-first ocean), `score_long180` (G2), `score_h3`
  (H3 scene generator). Regression gate: `GSS=0` default render of `kids`
  must reproduce the frozen v3 SHA
  `18cb055571a8a595fa8f080adbf613188407a3c4f2815dd2e1ce41befc54eb8f`
  bit-identically, or no R2 result is trusted.
- `work/r2b/` — copy of `b_beta` assemble chain (`assemble.zag`,
  `mech_kids.zag`, `mech_kethra.zag`, `mech_ocean.zag`, `catalog_kids.bin`;
  `work/wav/` symlinked to the frozen sources) plus: `K_SEED` const → global
  `GSEED` (argv-settable), `GPERM` flag (per-event deterministic ±40 ms onset
  permutation injected at the single `ev_place` choke point; bed placements
  `target==2500` are NOT permuted), `GCOND` flag (foreground phases skipped —
  continuous-bed control), placement log path via argv. Regression gate:
  `GSEED=20260922,GPERM=0,GCOND=0` must reproduce the frozen B-β v3 SHA
  (recorded at build time; byte-identical 3/3) or no R2 result is trusted.
- Analysis: deterministic Python/numpy scripts in `work/` (measurement only;
  renders stay pure Zag). Band-limiting via FFT brickwall; STFT via numpy.
- Controls named below are rendered, not assumed.

Deviations from the models' proposals are marked **[DEV]** with reasons.
Operationalizations of ambiguous protocol language are marked **[OP]**.

---

## sol-H1 — 10 ms natural envelope dips under sparse/dense event conditions

**Claim (defect):** 10 ms dips inside captured laughs are harmless in isolation
but become perceptual cutouts when event envelopes dip simultaneously
(synchronized dips at boundaries/overlaps) or when a phrase has no
independent world bed (sparse exposure).

**Testbed:** B-β v3 kids scene (the artifact the hypothesis is about).
**[DEV]** sol proposed a 60 s scene family; the B-β v3 score is a fixed 30 s
narrative and doubling it would author a new scene rather than test the
artifact. The dip-synchronization mechanism is local; the test runs on the
30 s scene with rates normalized per minute (1800 ten-ms windows per render
× 60 renders).

**Conditions** (20 deterministic seeds `GSEED = 20260922 + k·7919`, k=0..19):
- (a) normal: `GPERM=0, GCOND=0`
- (b) permuted: `GPERM=1` — every foreground event onset shifted by a
  deterministic per-placement offset uniform in [−40,+40] ms
  (`(h32(7000,GPERMCTR)%81)−40`); downstream chaining uses shifted times
- (c) continuous-bed control: `GCOND=1` — bed-first air scored as usual, all
  foreground phases skipped

**Measurement** (per render): 1 ms rectified envelope; per 10 ms window record
`min1` = minimum 1 ms energy and `rms10` = 10 ms RMS. Window classes from the
deterministic placement log:
- boundary: window center within ±250 ms of a phase boundary
  (5.0 / 13.0 / 15.0 / 26.0 s — B-β P0..P3 joints)
- overlap: ≥2 foreground events simultaneously active (log spans), not a
  boundary window
- within-phrase: all other windows
Floor reference `F` = 5th percentile of `rms10` over within-phrase windows
(per render). A window is a **dip** if `min1 < F`. Dip rate per class per
minute; dip duration = run length of consecutive dip windows × 10 ms.

**Prediction:** synchronized/exposed dips in (a) and (b) — boundary and
overlap dip rates above within-phrase rates; reduced in (c).

**Kill criterion (machine):** across the 20 seeds, median boundary dip rate ≤
median within-phrase dip rate AND median overlap dip rate ≤ median
within-phrase dip rate (paired sign test, α=0.05, preregistered direction),
AND no dip anywhere in (a)/(b) lasts >10 ms below F. If all hold → **KILLED**.
If boundary/overlap rates are significantly higher in the predicted direction
OR any dip exceeds 10 ms below F → **SURVIVES** (defect confirmed → recompose
B-β world-first, v4 kids clip).

**Kill criterion (ear):** Micah blinded A/B — normal (a) vs continuous-bed
control (c), seed k=0, order randomized, sealed key. Brief: "Two renders of
children playing at dusk. In a blinded A/B, can you reliably tell which is
which — does one cut out where the other flows?" → **PENDING-EAR** (clips +
key prepared by coordinator; parent runs the session).

---

## sol-H2 — bridge_world seams via source/room/texture discontinuity

**Claim (defect):** `bridge_world` removes silence but can insert audible
seams: the joined captured material changes acoustic identity (spectral
balance, room, texture statistics) at bridge entry/exit even when amplitude
is continuous.

**Testbed:** B-γ kids score (5 scored bridges at salts 51/54/57/60/63;
**[OP]** grok's G3 says "four" — the frozen v3 score has five; all five are
tested). 30 deterministic scenes: `GSS = 1..30` (fresh deterministic
variants of the kids grammar, 5 bridges each → 300 bridge edges).

**Conditions per scene:**
- standard: `bridge_world` as frozen
- control: same captured bridge material scored from `t0−2 s` through
  `t1+2 s` with the bridge's gain trajectory held constant (per-placement
  gain factor fixed at 1.0, no insertion/removal at the nominal edges), same
  salts → same grains, same intra-window positions

**Measurement** (per bridge edge, 10 per scene; identical nominal edge times
measured in both conditions): 1 ms amplitude slope = max |d(env₁ms)/dt| in
±50 ms; 10 ms spectral-flux peaks = max frame-to-frame L2 distance of
log-magnitude STFT (46 ms window, 10 ms hop) in ±200 ms; 50 ms log-spectrum
distance = L2 distance between mean log-magnitude spectra of the 50 ms
flanks; modulation-rate change = |Δ| of 2–20 Hz modulation-spectrum centroid
of the 1 s flanks. **[OP]** "stereo/ambisonic image change" is N/A — all
renders are mono by design; documented, not faked.
Matched ordinary transitions: from the placement log, event onsets NOT at
bridge edges, matched 1:1 to bridge edges by local 500 ms RMS (±1 dB bin);
300 bridge-edge vs 300 ordinary-transition samples per measure.

**Prediction:** bridge-edge outliers and detectable seam locations in the
standard condition; control edges clean.

**Kill criterion (machine):** per preregistered measure, one-sided
Mann-Whitney U (bridge > ordinary), α=0.05. Kill requires NO measure
significant AND median(bridge) ≤ median(ordinary) on all four measures →
**KILLED**. Any measure significant in the predicted direction →
**SURVIVES** (defect confirmed → recompose B-γ bridges, v4 kids clip).

**Kill criterion (ear):** Micah blinded seam localization — 6 standard scenes
(seeds), brief: "Mark any moment that sounds like a splice/edit, with a
timestamp." Sealed key = true bridge edge times. Chance = edges/total
duration. → **PENDING-EAR**.

---

## sol-H3 — uniform world bed feels spatially frozen over long/novel scenes

**Claim (defect):** world-first scoring preserves continuous energy but the
bed's texture/activity changes too little over minutes or under novel
grammars — an audible-but-unevolving imagined world.

**Testbed:** `score_h3` in r2g (chunked mix, 300 s scenes). 12 scenes:
- familiar low-density ×4: kids-at-dusk grammar, 10 consecutive 30 s
  tag-game phrase blocks, fresh salt base per block
- high-overlap ×4: 4–8 simultaneous event streams (wash/wind/laugh/thump/
  shout/creak layers), density cycling 4→8→4 per 30 s
- novel grammars ×4: unseen orderings/tags — (n1) ocean-grammar events under
  kids voices, (n2) monster crack-syllables over kids bed, (n3) reversed
  (`place_rev`) phrases, (n4) brightness-descending cascades with feet
Conditions per scene: standard world-first (continuous bed + bridges at
every 30 s joint) vs control (identical events/timing; bed amplitude floor
preserved but bed grains picked from a disjoint deterministic salt region
`+700000` — different, nonadjacent captured segments; source-id
nonadjacency verified post-hoc via the placement log × `grains.csv`).

**Measurement** (per scene, standard vs control): 1 s and 10 s spectral
novelty = mean L2 distance between consecutive log-magnitude spectra (46 ms
STFT window, 1 s / 10 s hop); repeated-segment distance = for each 2 s
window (1 s step), max normalized cross-correlation against all
non-overlapping 2 s windows ≥30 s away (high = frozen/repetitive);
event-conditioned bed response = Pearson r between per-1 s bed-band
(200–800 Hz) energy and per-1 s foreground event count (from placement log);
boundary floor = min 10 ms RMS in ±250 ms at each 30 s joint, bar ≥3× the
scene's within-phrase 5th-percentile floor (round-1 bar). **[OP]** spatial-
feature change is N/A (mono); documented.

**Prediction:** standard beds show excessive repetition / weak event-
conditioned response vs control despite acceptable floors, especially in
novel scenes.

**Kill criterion (machine):** primary: pooled paired standard-vs-control
comparison across all 12 scenes (Wilcoxon signed-rank, n=12, α=0.05,
preregistered direction: novelty↓, repetition↑, |response|↓ for standard;
Holm-corrected across the four measures). Secondary (descriptive): per-class
medians, to check whether any effect concentrates in the novel class as
predicted. (n=4 per class cannot reach α=0.05 alone, so no per-class
significance claim is made.) Kill requires NO measure significant pooled AND
all standard boundary floors ≥3× → **KILLED**. Any measure significant
pooled in the predicted direction → **SURVIVES** (defect confirmed →
recompose B-γ world bed with evolving state, v4 kids clip).

**Kill criterion (ear):** Micah blinded pairs (standard vs control, one per
class), brief: "Two long scenes. Does either world's background feel frozen
or unchanging while the action continues? Which feels more alive?" →
**PENDING-EAR**.

---

## grok46-G1 — world-bed uniformity under distributional shift

**Claim (defect):** the world-first fix holds only on the kids-at-dusk
distribution; on recordings with fundamentally different spectral/temporal
statistics the bed's uniformity breaks (seam-like floors).

**Testbed:** **[OP]** no new recordings can be captured on the VM; the most
spectrally/temporally different AVAILABLE captured corpus with a world-first
score is B-γ **ocean** (broadband surf/wash + crack transients vs kids'
pitched voices/shouts — named honestly; not forest, which has no catalog or
score). `score_ocean_wf` = the frozen ocean grammar + world-first bridges at
its phrase joints (fresh salts; the frozen `score_ocean` is untouched).
**[DEV]** grok proposed 45 s; the authored ocean grammar is 30 s and
extending it would author a new scene — the distributional-shift mechanism
does not need 45 s. Control: the original-corpus 30 s B-γ kids v3
(`18cb0555…`).

**Measurement:** at every ocean phrase boundary: `floor_new` = min 10 ms RMS
of the 200–800 Hz band-limited envelope (1 ms sampling) in ±150 ms.
`floor_orig` = median of the same quantity at the kids-v3 boundaries
(9.35 s: 0.0435, 18.75 s: 0.0401 → median 0.0418; renders are peak-
normalized so absolute RMS floors are comparable). Ratio = floor_new /
floor_orig per boundary. 3/3 byte-identical renders.

**Prediction:** every boundary ratio ≥ 3.2×.

**Kill criterion:** any single boundary ratio < 2.4× → defect confirmed →
**SURVIVES** (recompose B-γ ocean world-first; v4 ocean kids clip is N/A —
the v4 deliverable stays the kids clip per round scope; the ocean fix is
documented). All boundaries ≥ 3.0× → **KILLED** (refuted). Between 2.4× and
3.0× → **INDETERMINATE**.

---

## grok46-G2 — accumulated scoring drift in multi-minute scenes

**Claim (defect):** deterministic scoring accumulates float/memory-resident
state drift over >30 s intervals, compressing envelopes → sub-3× boundary
floors late in long scenes.

**Testbed:** `score_long180` in r2g (chunked mix): one unbroken 180 s world
pass — continuous world bed 0–180 s, six 30 s kids-grammar phrase groups
with fresh salt bases per group, bridges at every 30 s joint; same grain
pack/classes as the kids-at-dusk test. Three byte-identical renders.
Controls: three 30 s segments extracted from the render — middle (75–105 s),
2/3 mark (120–150 s), end (150–180 s).

**Measurement:** at every phrase boundary (30/60/90/120/150 s) and at
internal pseudo-boundaries every 45 s (45/135 s; 90 s coincides with a real
boundary): `floor_180` = min 1 ms RMS of the 0–1 kHz band envelope in
±250 ms. `floor_balpha` = 5th percentile of 1 ms RMS (0–1 kHz) over the
30 s B-α control `b_alpha/clips/b_alpha_kids_v2.wav`. Ratio per boundary.

**Prediction:** every measured ratio ≥ 3.1×.

**Kill criterion:** any ratio < 2.7× → defect confirmed → **SURVIVES**
(recompose; v4 kids clip). All ratios ≥ 3.0× → **KILLED** (refuted).
Between 2.7× and 3.0× → **INDETERMINATE**.

---

## grok46-G3 — bridge_world authoring seams under density stress

**Claim (defect):** `bridge_world` helpers are composed as isolated event
clusters rather than true world-state continuations (10 ms-scale masking
failures where bridge recordings overlap).

**Testbed:** B-γ kids v3 scene (all five `bridge_world` calls active;
**[OP]** grok wrote "four" — the frozen score has five: 0.0–2.4, 8.8–10.8,
14.4–16.4, 18.3–21.4, 24.8–26.8).
- full: standard world-first render
- ablation: each `bridge_world(t0,t1,…)` replaced by a plain event-only
  block spanning the identical `[t0,t1]` (same byte length): laugh trains +
  `run_feet` with the bridge's salt base — ordinary events, no wash/wind
  world texture
3/3 byte-identical renders each.

**Measurement** (at the exact five bridge transition points = bridge
midpoints; 125 ms windows centered there): `corr` = normalized
cross-correlation (0–1 kHz band, 1 ms resolution) between the FULL and
ABLATION renders' windows; `floor_full[b]`, `floor_abl[b]` = min 10 ms RMS
in ±250 ms at each bridge point, as a ratio vs the B-α control floor
(`b_alpha_kids_v2.wav` 5th-percentile 10 ms RMS, same band).

**[OP]** grok's protocol language is ambiguous about what the correlation
compares; this prereg fixes it: correlation is full-vs-ablation (does the
event-only replacement reproduce the bridge?), floors are per-render vs the
B-α control.

**Verdicts:**
- **SURVIVES** (defect confirmed) if median corr ≥ 0.90 AND all
  floor_abl[b] ≥ 3.0× (ablation matches bridges → bridges are decorative
  isolated clusters), OR any floor_full[b] < 2.5× (bridges fail to hold the
  world — masking failures).
- **KILLED** if median corr < 0.88 AND all floor_full[b] ≥ 3.0× AND any
  floor_abl[b] < 2.5× (bridges do provable unique work).
- Else **INDETERMINATE** (numbers reported, no v4, flagged for red team).

---

## Ear-clip packages (all PENDING-EAR unless machines decide first)

Prepared under `continuity_round2/ear/` with sealed keys (`KEY.sealed.txt`
per package, brief in `BRIEF.txt`): H1 A/B pair, H2 six-scene localization
set, H3 three class pairs. Builder-knowledge caveat: the coordinator built
the keys and must be excluded from judging; only Micah's ears count.

## Commit record

- PREREG_ROUND2.md — this file — committed alone first; head SHA recorded
  in the final report before any test executes.
- Results, fixed sources, and v4 clips (if any) committed after; never
  binaries or `.zagd` files.
