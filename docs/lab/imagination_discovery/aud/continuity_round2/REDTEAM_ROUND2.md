# RED TEAM — Continuity Round 2 (2026-09-22)

Adversarial audit of the six round-2 continuity hypotheses. Method: pure-Zag
measurement (`work/redscan.zag`), zero RNG, byte-identical reruns. No ear keys
opened; all package criticism is structural (brief vs frozen prereg). Head at
audit start: `070c94cb46084c204433bf1d6d3567b4ebf574b3`.

For each hypothesis this report separates three things that round 2 blurred
together: (a) the **prereg-letter verdict** (what the frozen Boolean rule
fires), (b) the **scientific verdict** (what the mechanism deserves), and
(c) **incidental defects** found along the way.

## Audit instrument

`work/redscan.zag` — pure-Zag WAV scanner, three modes:

- `dip <wav>`: full-file 10 ms RMS scan; 5th-percentile floor (numpy-compatible
  linear interpolation); longest sub-floor runs; A-NATIVE diagnostics
  (peak, DC, zero-crossing rate, clip count).
- `jf <wav> <filter> <joint_csv_ms> [refmicro]`: per-joint min 10 ms RMS in
  ±150 ms; scene-relative 5th-percentile floor (excluding ±250 ms of joints);
  ratios vs scene floor and vs an optional absolute reference. Filters:
  0=full-band, 1=RBJ 200–800 Hz bandpass, 2=RBJ 0–1 kHz lowpass.
- `xc <wavA> <wavB> <t0ms> <t1ms>`: windowed Pearson correlation + RMS.

Verification against numpy on `renders/g1/g1_oceanwf_r1.wav`: peak
`0.679595947…` exact, zero-crossing rate `4511.133/s` exact, 5th percentile
`40228` vs numpy `40228.83` (exact after truncation). Two consecutive runs
diff-clean (deterministic, zero RNG). One real bug caught and fixed during
verification: the Newton `fsqrt` used 6 iterations from a start of 1.0,
leaving ~1.2% error for small x — now 12 iterations. This file is the only
new measurement code; no v3 clips, sealed packages, or A-NATIVE state touched.

---

## sol-H1 — 10 ms natural-envelope dips — REFINED

**Numbers reproduced.** Normal median dip rates within-phrase 15.00/min vs
boundary 10.25 vs overlap 9.47; boundary > within in 7/20 seeds (one-sided
sign p = 0.9423); overlap > within 8/20 (p = 0.8684). Maximum reported run
990 ms; bed-only itself runs to 520 ms.

**The prereg-letter SURVIVES is real.** The kill rule fires KILLED only if
rates are not elevated AND no dip anywhere lasts >10 ms below floor. The OR
clause (any dip >10 ms → SURVIVES) triggers on the 990 ms runs. Letter-correct.

**The mechanism is contradicted.** The claimed synchronization/exposure
mechanism predicts *elevated* boundary/overlap rates. Both directions went
the wrong way, strongly (p ≈ 0.94/0.87 against the prediction). Long
threshold crossings occur broadly across window classes and in bed-only
material, so they do not isolate the proposed mechanism. What survives is a
nonspecific threshold-crossing fact ("some seeds have sub-floor runs up to
990 ms"), not the hypothesized defect.

**Ear-package deviations (structural, keys sealed):** the frozen prereg froze
*one* k=0 normal-vs-control A/B ("can you reliably tell which is which — does
one cut out where the other flows?"). The package delivers *three* pairs
(k18, k13, k11) of full-mix-vs-bed-only, which makes content identity obvious
and confounds the continuity judgment. The brief's claim that dips were
"concentrated in dense-overlap and sparse-gap regions" contradicts the machine
result (boundary/overlap rates were *not* elevated). This package is not a
clean test of the mechanism; Micah's ear verdict on it will adjudicate
audibility of the variant-seed dips, not the frozen question.

**Verdict: REFINED** — defect exists by the meter, mechanism unproven, ear
test deviates from prereg. Whether the 100–990 ms runs are audible cutouts is
genuinely for Micah's ears.

---

## sol-H2 — bridge_world seams — OVERTURNED → KILLED (machine)

**Numbers reproduced** (299/300 matches):

| measure | bridge median | ordinary median | one-sided p |
|---|---:|---:|---:|
| envelope slope | 0.0912 | 0.0967 | 0.9831 |
| spectral flux | 13.57 | 14.82 | 1.0000 |
| spectral distance | 8.68 | 9.33 | 0.9995 |
| modulation change | 0.8737 | 0.7513 | 0.4042 |

Three of four measures run *strongly opposite* the seam hypothesis (p ≈ 1.0
against). The sole measure in the predicted direction (modulation change)
is noise (p = 0.40). The round-2 "SURVIVES" rests entirely on treating one
nonsignificant median as confirmation. **That is not defensible: OVERTURNED →
KILLED (machine).** No seam discontinuity is detectable at bridge entry/exit
by any of the four preregistered measures; three measures actively favor
the null.

**Ear-package selection claim fails audit.** The brief says the three pairs
were "selected for largest machine-measured seam signature," but no retained
selection script or score supports this. Reconstructing a composite seam
signature (z-score sum of the three always-defined preregistered measures,
higher = more seam-like) over all 300 edges: the chosen edges (s5@14.4,
s30@24.8, s2@26.8) rank **258, 252, and 194 of ~300** — among the *least*
seam-like edges. The retained `h2_ear_candidates.json` triples are
(scene, bridge edge, matched ordinary *timestamp*), not scores. The "largest"
claim is at best unverifiable, at worst false. (Additionally: prereg froze
six standard scenes with open timestamp localization against true edge
times; the package is three selected A/B pairs — a different test.)

---

## sol-H3 — uniform world bed — OVERTURNED → VOID for the stated hypothesis

**The machine comparison cannot test the stated hypothesis.** The claim is
about bed *material* (uniform/frozen captured material). The test compares
bed *arrangement* (standard vs disjoint/nonadjacent placement) — and the
crew's own analysis script notes the corpus holds only **19 wash + 21 wind
grains**, so the mandated disjoint/nonadjacent control reuses 95–100% of the
same source grains. The mandated control was physically impossible. The
"no Holm-significant arrangement effect" result is therefore a comparison of
near-identical material, and it cannot validate or kill the material claim.
**The stated hypothesis is VOID/DEFERRED (machine)** — untested as stated,
not confirmed, not killed.

**The script's SURVIVES default is unpreregistered.** The prereg fires
SURVIVES only on a significant pooled measure; none was significant. The
correct machine verdict under the frozen rule is INDETERMINATE, not SURVIVES.

**The floor shortfall is real but was mis-anchored.** Re-measured
scene-relative (the prereg's actual bar: ≥3× the *scene's own* within-phrase
floor, full-band, 10 ms RMS): across all 12 standard scenes the bridge-joint
floors run **0.91–4.67×** their own scene floors; 12/12 scenes have ≥1 joint
below the 3× bar; only **1 of 60** joints dips below the scene's own
5th-percentile floor. The crew's reported 0.35–1.57× compared against the
*kids* scene median — a foreign reference that overstated the depth. The
defect survives re-anchoring (the 3× bar still fails) but is much shallower
than reported.

**Ear package cannot adjudicate H3.** Prereg: three standard-vs-control pairs,
one per class. Actual: two A/B/X trials of familiar-vs-novel *grammar*, both
built on the same bed construction; X merely repeats A or B. It tests grammar
discriminability, not bed material or arrangement. Structurally invalid for H3.

---

## grok46-G1 — ocean distributional shift — REFINED (letter-SURVIVES stands, corrected)

**Two measurement errors confirmed and corrected:**

1. **Wrong locations.** `analyze_gx.py` measured t = 0.0/2.4/10.8/26.8 — copied
   from kids bridge times. `score_ocean_wf` actually inserts bridges at
   0.0–2.2, 4.6–6.6, 11.6–13.6, 18.6–20.6, 25.6–27.6 (exits 2.2/6.6/13.6/
   20.6/27.6; per the score's own comment, midpoints 1.1/5.6/12.6/19.6/26.6).
   The reported minimum (0.12×) was measured at **t = 0.0 — the scene onset**,
   not a bridge exit.
2. **Band-mismatched reference.** The prereg's reference (0.0435, 0.0401 →
   median 0.0418) is a **full-band** number from the round-1 red team
   (reproduced exactly: 43474/40086 micro). G1's measurement is 200–800 Hz
   **band-limited**. Band-limited RMS ≤ full-band RMS, so every reported ratio
   was biased down. Band-limited kids pivots: 9038/14745 micro.

**Corrected results (band-limited, band-consistent kids-median reference
20408):** ocean bridge midpoints 0.83/1.21/1.50/2.16/0.97 → min **0.83**;
actual exits 1.84/1.07/1.16/1.26/0.71 → min **0.71**; entries (non-onset)
1.07/1.30/1.04/0.84. All below 2.4 → **the letter-SURVIVES stands**; the
0.12 was an artifact of the double error.

**But the mechanism is not demonstrated.** Scene-relative, ocean bridge
windows sit at 0.93–2.43× the ocean scene's own floor (midpoints),
0.80–2.06× (exits) — no localized seam dips; the "defect" is a scene-level
band-energy difference (the ocean recording is quieter than kids in
200–800 Hz). Worse: the kids scene's own bridge midpoints measure
0.93/0.64/0.20/0.49/0.18× the prereg reference — the reference scene fails
its own bar at 3 of 5 midpoints. The reference was unrepresentative.

**Verdict: REFINED** — SURVIVES is letter-correct but the margin collapsed
(0.12 → 0.71–0.84), and what survives is "ocean is quieter than kids in
200–800 Hz," not bridge-exit seams under distributional shift.

---

## grok46-G2 — long-form drift — REFINED (letter-SURVIVES stands, reinterpreted)

**Crew numbers reproduced exactly** (1 ms envelope, ±250 ms, 0–1 kHz; control
floor 0.001728): boundary ratios 1.38/2.15/1.19/2.18/4.27/2.33/1.99. The
1.19 at 60 s is real → **letter-SURVIVES stands**.

**It is a control-level artifact, not a local dip.** Scene-relative (10 ms
RMS, ±150 ms, 0–1 kHz, vs the scene's own floor): 1.23/0.93/1.40/1.28/1.75/
1.00/2.14. No boundary sits below the scene's own floor; the 60 s minimum is
1.40× scene-relative. The sub-2.7× reading comes entirely from comparing
against the foreign B-α control's level.

**The drift mechanism is contradicted.** The hypothesis claims accumulated
drift over 180 s. Scene-relative ratios across time show no monotonic
decline (1.23 → 0.93 → 1.40 → 1.28 → 1.75 → 1.00 → 2.14; maximum at 120 s).
There is no drift signature.

**Verdict: REFINED** — keep "a single sub-2.7× ratio vs the B-α control at
60 s" as the letter-finding; the accumulated-drift mechanism is killed; what
remains is a level difference against a foreign reference, not a continuity
defect in the long scene.

---

## grok46-G3 — isolated event clusters — OVERTURNED → KILLED (machine, decisive test)

The frozen INDETERMINATE was prereg-faithful (median r = 0.303; both floors
far above control; neither bar fires). But the test was poorly targeted:
full-vs-ablation waveform correlation mostly proves that replacing content
changes waveform identity, not whether bridge clusters are isolated or
perceptually seamed.

**Decisive test designed and executed (density stress):** if bridge interiors
mask/fail under density exceeding the original test set, their 10 ms floors
should underperform density-matched non-bridge windows. Testbed: the four
H3 dense standard scenes (4–8 simultaneous streams). Bridge-interior floors
vs the five highest-density non-joint 1.6 s windows per scene (density ≥
bridge density, ≥5 s from any joint), all scene-relative:

| scene | bridge med | control med | diff |
|---|---|---:|---:|
| c1_i0 | 1.52 | 1.61 | −0.09 |
| c1_i1 | 1.49 | 1.26 | +0.23 |
| c1_i2 | 1.19 | 1.63 | −0.44 |
| c1_i3 | 1.56 | 1.92 | −0.36 |

Wilcoxon (bridge < control), n = 4: W = 2.0, **p = 0.19** — mixed signs, not
significant. Bridge interiors hold the same floors as equally dense ordinary
texture. Absolute levels (1.0–2.5× scene floor) are a property of dense
scenes everywhere, not of bridges.

**Verdict: OVERTURNED → KILLED (machine)** under the decisive bars. The
density-stress masking-failure mechanism is not observed. (Caveat: n = 4
scenes limits power, but the direction is mixed, not consistently negative.)

---

## Flagship cutout scan — CONFIRMED clean (no missed cutouts)

Full-file 10 ms RMS dip scans of both frozen v3 flagships:

- **B-β v3** (`bbeta_kids_v3.wav`): longest sub-floor run 590 ms at 28.71 s —
  the scored natural ending (score: "the last event decays by ~28.35 s and the
  quietest air owns the tail"; v1 bed picks replicated exactly, no
  processing). Next longest: 180 ms at 9.17 s; everything else ≤60 ms.
- **B-γ v3** (`b_gamma_kids_v3.wav`, SHA `18cb0555…` matches frozen): longest
  run 1300 ms at 28.70 s — the preserved v2 natural ending (quiet from
  28.7 s per the frozen score). Everything else ≤20 ms. Remarkably clean.

A-NATIVE on both: peak 0.708/0.671, DC 0/30 µ, zero-crossing 2178/2808 /s,
zero clipped samples. The round-2 machine tests missed no cutout in the
flagships; the only long runs are authorized scored content. (The H1
100–990 ms runs live in variant seeds k18/k13/k11, not the flagship —
audibility is Micah's call via the ear package.)

---

## Processing vs imagination (both forks)

Concrete seam/mastering operations present in source, not imagined world
structure: B-γ `place()` applies short smoothstep edge envelopes to every
grain; B-β `place()` applies 3 ms linear edge fades; writers do DC removal +
global peak normalization; the B-β writer comment also names 30 ms file-edge
fades. Any floor improvement or transition smoothness attributable to
overlap, fades, normalization, or source reuse must not be presented as
imagination. (The B-β v3 tail is scored content, verified above — not a
long processing fade.)

---

## Ear packages — structural validity (keys sealed throughout)

| pkg | prereg froze | package delivers | status |
|---|---|---|---|
| H1 | 1 pair, k=0, normal-vs-control | 3 pairs, k18/k13/k11, full-mix-vs-bed-only; brief misstates machine finding | deviates |
| H2 | 6 scenes, open timestamp localization vs true edges | 3 selected A/B pairs; "largest seam signature" claim unaudited (chosen edges rank 194–258/300 by composite) | deviates |
| H3 | 3 standard-vs-control pairs, one per class | 2 familiar-vs-novel A/B/X trials, same bed construction | invalid for H3 |

No ear verdicts are overturned or confirmed here — Micah's ears outrank the
meter, and the packages await his listening. But H1's and H2's packages do
not test their frozen questions, and H3's cannot adjudicate H3 at all; any
ear verdicts from them should be labeled accordingly.

---

## Bottom line

| hypothesis | prereg letter | scientific verdict |
|---|---|---|
| sol-H1 | SURVIVES (real) | **REFINED** — mechanism contradicted; meter-defect only |
| sol-H2 | SURVIVES (claimed) | **OVERTURNED → KILLED (machine)** — 3/4 measures oppose |
| sol-H3 | SURVIVES (unpreregistered default) | **OVERTURNED → VOID** for stated hypothesis; floor defect retained, re-anchored |
| grok46-G1 | SURVIVES (real) | **REFINED** — margin 0.12 → 0.71–0.84; scene-level, not seams |
| grok46-G2 | SURVIVES (real) | **REFINED** — control artifact; drift mechanism contradicted |
| grok46-G3 | INDETERMINATE (faithful) | **OVERTURNED → KILLED (machine)** by decisive density test |

Of the four "SURVIVES" verdicts: H1's and G1's and G2's are real by the
prereg letter but each shrinks on re-measurement (mechanism contradicted in
all three); H2's is scientifically indefensible; H3's was never prereg-
supported. No surviving v3 cutout was missed by round 2 — the flagships'
only long sub-floor runs are authorized scored endings.
