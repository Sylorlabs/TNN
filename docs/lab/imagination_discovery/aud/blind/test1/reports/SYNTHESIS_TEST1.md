# BLIND TEST-1 — cross-fork synthesis (machine-signal judging)

Five forks, 15 valid native-critic ballots (3 fresh judges per fork, all
signal-only, no builders, no judge served on more than one package). Every
fork's judges agreed with each other 100% on labels and ranking.

## Judge × label matrix

S = syntheticity index (higher = more machine-like). Confidence per frozen
rules. Key = post-ballot byte-verified ground truth (never opened by
judges).

| fork | judge | clip→label (S) | confidence | vs key |
|---|---|---|---|---|
| B-β | 1 | A→fork (0.382), B→real (0.342), C→synth (0.509) | LOW ×3 | key sealed — unopened in judging context |
| B-β | 2 | A→fork (0.382), B→real (0.342), C→synth (0.509) | LOW ×3 | sealed |
| B-β | 3 | A→fork (0.382), B→real (0.342), C→synth (0.509) | LOW ×3 | sealed |
| B-γ | 1 | A→real (0.337), B→synth (0.509), C→fork (0.413) | LOW ×3 | key sealed — unopened in judging context |
| B-γ | 2 | A→real (0.337), B→synth (0.509), C→fork (0.413) | LOW ×3 | sealed |
| B-γ | 3 | A→real (0.337), B→synth (0.509), C→fork (0.413) | LOW ×3 | sealed |
| B-α | 1 | 1→synth (0.470), 2→fork (0.393), 3→real (0.351) | LOW ×3 | 1=synth ✓; 2,3 swapped (2=real, 3=fork) |
| B-α | 2 | 1→synth (0.470), 2→fork (0.393), 3→real (0.351) | LOW ×3 | same swap |
| B-α | 3 | 1→synth (0.470), 2→fork (0.393), 3→real (0.351) | LOW ×3 | same swap |
| D-α | 1 | 1→fork (0.370), 2→real (0.286), 3→synth (0.506) | MED/LOW | full rotation (1=synth, 2=fork, 3=real) |
| D-α | 2 | 1→fork (0.370), 2→real (0.286), 3→synth (0.506) | MED/LOW | full rotation |
| D-α | 3 | 1→fork (0.370), 2→real (0.286), 3→synth (0.506) | MED/LOW | full rotation |
| A-α | 1 | 1→real (0.352), 2→fork (0.371); calib_real>1>calib_synth>2 | MEDIUM | both correct |
| A-α | 2 | 1→real (0.352), 2→fork (0.371); calib_real>1>calib_synth>2 | MEDIUM | both correct |
| A-α | 3 | 1→real (0.352), 2→fork (0.371); calib_real>1>calib_synth>2 | MEDIUM | both correct |

## Majority verdicts (preregistered rules, PREREG_TEST1.md)

Fail bar: fork render labeled "synth control" by ≥2/3 judges (A-α:
majority ranks fork render below the labeled synth control).

| fork | fork render labeled "synth control" | majority verdict |
|---|---|---|
| B-β | 0/3 (3/3 "fork render") | **PASS** — unanimous, LOW confidence |
| B-γ | 0/3 (3/3 "fork render") | **PASS** — unanimous, LOW confidence |
| B-α | 0/3 (3/3 "real recording") | **PASS** — unanimous, LOW confidence; the render outscored the genuine playground on S (0.351 vs 0.393) |
| D-α | 0/3 (3/3 "real recording") | **PASS (hollow)** — unanimous, but all three judges labeled the *genuine playground* "synth control" (its stationary background wash, s2=0.44, reads as synthetic); the real-vs-synth discrimination inverted on this content |
| A-α | n/a (forced-choice + ranking rule) | **FAIL** — 3/3 judges ranked the fork render below the labeled synth control (least-real of four), MEDIUM confidence |

Evidence summary:
- B-β/B-γ: the synth controls separate cleanly (stationary bed s2≈0.46,
  static formants s5≈0.40–0.59, ~3 transients/30 s); fork-vs-real gaps are
  narrow (<0.10), hence LOW confidence everywhere.
- B-α: judges unanimously mistook the fork render for the real recording —
  its S is the lowest in the set and the genuine playground's steady wash
  (s2=0.19) reads as mildly stationary beside it.
- D-α: the genuine w1 30–60 s segment's steady background wash defeats the
  fingerprints — a metric-calibration failure, disclosed, not a package
  labeling error (byte-verified).
- A-α: the fork render carries a loop/paste signature (s3=0.503: half of
  all distant 1-s chunk pairs >0.999-identical — verbatim self-repetition no
  voice does) plus assembly scars: 723 hard-clipped samples and 10,414
  digital clicks in 30 s, found in no other clip. Forced choices unanimous
  and correct against the key.

## Provenance: the v1 source failure and recovery (Amendment A1)

After v1 package assembly, verification showed `b_alpha/study/s1_playground_berlin.wav`
and `b_beta/sources/kids_berlin.wav` were stationary noise, not playground
audio (crest ≈3.0, centroid ≈11.8 kHz, ZCR ≈0.48, uncorrelated stereo). All
nine v1 B-α/D-α/A-α ballots were VOIDED (reports renamed `*_v1_VOID.md`,
keys preserved as `keys/*_key_v1_VOID.json`). Nine fresh v2 packages were
built with independently verified genuine sources (crest 5.9–7.8, centroid
1.6–2.2 kHz) and judged by nine fresh critics. The 15 ballots above are all
v2 (B-β and B-γ's packages never used the bad file as a judged clip —
their `real_calib_30s.wav` was independently verified genuine).

Related caveat: B-β's study log says its render used `kids_berlin.wav` for
distant background voices — that file was noise. This does not touch the
sealed B-β blind package, but it must be disclosed when interpreting B-β's
method.

Methodological disclosure: the first prereg draft defined s3 as maximum
chunk similarity; a pre-package sanity check showed it saturated at 1.0 on
known real and synth clips alike. Before any package assembly or judge
dispatch, s3 was corrected to the fraction of distant 1-s chunk pairs with
cosine similarity >0.999, and the prereg text updated. The report's first
draft did not stay byte-frozen — this correction is disclosed here.

## Standing

Machine-blind Test 1 is complete: 4 of 5 forks pass the machine track
(B-β, B-γ, B-α clean; D-α hollow), A-α fails it. Confidence is LOW-to-
MEDIUM throughout — the machine track separates obvious synth beds but its
fork-vs-real discrimination is close, and two packages exposed real-segment
stationarity that the fingerprints misread. **Micah's ears remain the final
oracle regardless of every machine verdict above** — one "sounds like a
synth" from him kills a fork's claim, and he may acquit where the machine
convicts.
