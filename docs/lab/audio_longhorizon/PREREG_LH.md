# PREREG_LH — Long-Horizon Real-Audio Trial Program (FROZEN 2026-09-25 PDT)

Micah's order, 2026-09-25: the audio principles investigation FALSIFIED the
"shitty open-loop generator" hypothesis on all three prongs (P-PASS, C-PASS,
L-PASS — synthesis commit `4467173e8502`, `docs/lab/audio_principles/` on
`tnn-native-lab`). Two independent input organs now exist
(`~/workspace/audio_principles/crew_p/organ.zag`, frozen spec
`crew_p/FROZEN_ORGAN.md`; `~/workspace/audio_principles/crew_l/src/main_organ.zag`).
The open frontiers: real-clip perception 0.783 bit-agreement vs 0.90 target;
organs are standalone binaries, not wired into deliberation; the frozen
autocorr F0 cannot resolve below ~125 Hz. His order: **"the frontier is any
real audio — wire the organs for long horizon real audio, see what happens."**

This prereg governs the entire long-horizon real-audio program. It is written
BEFORE any trial runs. It decides nothing about Round 3B; the four structural
calls remain Micah's word, informed — never decided — by this program.

## 0. Status and standing law

- FROZEN 2026-09-25 PDT per the Phase-A1 task. Amendments need Micah's word.
- Standing law applies throughout: pure Zag, zero RNG in any decision path,
  byte-identical reruns (3 consecutive runs, SHA match, else the run is VOID),
  analyzer-first (agents describe measurements, never how anything "sounds"),
  no Python in the decision path, real mechanisms not stubs, no arbitrary hard
  limits (the znc 2^25-bytes-per-slice ceiling is load-bearing and is worked
  around by chunked framing, never presented as a design cap).
- The standing expectation is NO degradation over long horizons (no-scale-rot
  is law, 2026-09-24/25). If agreement drops with horizon, that is a DEFECT:
  diagnose knowledge-first, then prove the machinery ceiling white-box.
- All commits on `tnn-native-lab`, NEVER `main`.

## 1. The integration contract (what "wired" means)

The live deliberation loop is three pure-Zag stages per episode:

1. **Ingest**: WAV bytes → input organ binary → descriptor vector on stdout
   (native strings/ints; the frozen organ vocabulary: `f0_mhz`, `voiced`,
   `env`, `rms`, `zcr`, `b0r`–`b3r`, `onsets`; crew-P dispatch ids).
2. **Deliberation**: descriptor vector + task intent (native string, frozen
   intent vocabulary) → TNN's own deliberation machinery, which reasons OVER
   the descriptors in the course of its deliberation and journals the
   reasoning natively (which descriptors were consulted, what was inferred,
   what action was chosen and why). The journal is the auditable "reasons"
   step. Python may read the journal afterwards; it never writes it.
3. **Action**: action descriptor (native string) → render machinery (pure
   Zag) → output WAV.

Python's role is the blind harness (prepares intents, holds answer keys,
scores outputs) and offline analyzer of committed artifacts — examiner, never
examinee. **Boundary rule**: only WAV bytes + intent/question descriptor
cross into the deliberation binary. Any measured value or feature sidecar
crossing the boundary = BOUNDARY-BREACH, run void.

Operational verdicts on the wiring claim
("the organ is successfully wired into live deliberation"):

- **WIRING-WORKS**: §8 ablation bars met (ablation changes the action
  distribution significantly AND directionally), 3× byte-identical,
  no Python in the per-episode path, boundary audit clean.
- **WIRING-DEGRADES**: wiring works, but the §2 long-horizon bars decline
  with horizon — recorded as a defect, diagnosed knowledge-first.
- **WIRING-FAILS**: any §8 kill bar trips, or all three §2 batteries fail.

## 2. Long-horizon bars (preregistered before any trial runs)

### 2.0 Horizon ladder

A deliberation session = one full loop episode (ingest → deliberate →
act). The loop's own state may persist across sessions (that is the point:
the loop must not degrade as its own state accumulates). Contamination guard:
the loop must not LEARN from the corpus — descriptors are sense data, not
training data; if any consolidation machinery ingests loop episodes, corpus
clip identities are excluded, else the run is VOID.

| Checkpoint | Clips | Sessions | Role |
|---|---|---|---|
| H0 | 40 | 1 | ANCHOR: the P-R4 40-clip real set, re-run through the WIRED loop |
| H10 | 400 | 10 | 10× horizon |
| H100 | 4000 | 100 | 100× horizon (or one continuous 100-session-equivalent run) |

**Anchor rule**: H0 must reproduce the standalone organ's P-R4 number,
0.783, within ±0.05. If not → WIRING-ANCHOR-FAIL: stop, diagnose; no horizon
claims may be made until the anchor holds (a wiring that changes perception
is itself a finding, not a baseline).

### 2a. Perception agreement over time

Metric (inherited from P-R4): per clip, the organ's 3 bits
(frac_static ≥ 0.15, HNR in [0.7,12], prosody in [0.003,0.25]) vs the frozen
analyzer's labels; agreement = mean bit-agreement over clips. Measured at
H0, H10, H100 on disjoint sealed corpus splits.

- **DEGRADED**: agreement(H_n) < agreement(H0) − 0.03 at two consecutive
  checkpoints → defect. Diagnosis order, knowledge-first: (1) corpus/label
  noise — which clip classes dropped? (2) organ computation — which
  descriptor bit, which signal property? (3) wiring/deliberation — is the
  loop misusing descriptors? Only after (1)–(3) are exhausted may a
  machinery ceiling be claimed, and then only white-box (named mechanism).
- **ROT-FAIL** (the standing expectation violated): agreement(H_n) < 0.70
  at any checkpoint, or monotone decline H0 → H10 → H100. The program
  records ROT-FAIL; the no-degradation law is not relaxed by this prereg.

### 2b. Control stability on REAL targets

Targets are REAL reference clips (sealed, held-out): TNN hears the reference
through the organ, then renders to match its measured descriptors.
Hit criterion per axis (frozen scorer, scorer sanity floor ≥ 95% agreement
to manifest labels on real material, else the battery is VOID):

| Axis | n targets (per checkpoint) | Hit criterion | Bar |
|---|---|---|---|
| Pitch | 40, refs spanning ≥125–1200 Hz | \|F0_meas − F0_ref\| / F0_ref ≤ 5% | ≥ 28 hits (70%) |
| Envelope | 40 (flat/rise/decay per manifest) | scorer 3-class == ref class | ≥ 28 hits (70%) |
| Prosody | 40 | scorer prosody CV within ref ±25% rel | ≥ 28 hits (70%) |

Null arms (same targets, same scorer), inherited from the principles prereg:
**RC0** (intent severed → default render) must be significantly below wired
(one-sided p < 0.01 per axis); **RC1** (frozen derangement of targets)
≤ 25% per axis, else the SCORER is lenient and the battery is VOID.

- **STABLE**: all axes ≥ 70% at H1 (40-target real set), AND hit rate at
  H10/H100 ≥ H1 − 0.05 per axis (no drift beyond 5pp).
- **DRIFT-FAIL**: any axis drops > 5pp from H1 at a later checkpoint →
  defect, same knowledge-first diagnosis order as §2a.

### 2c. Closed-loop correction on REAL material

20 held-out real reference clips (sealed). Per case, all TNN-native:
iteration 0 = open-loop render to the reference's descriptors; TNN receives
render0 back THROUGH THE INPUT ORGAN, measures deviation natively, re-plans,
re-renders; up to 3 correction iterations. Scorer measures ERR(k) =
|F0_meas − F0_ref|/F0_ref + 0.5·[env class wrong] + 0.5·[prosody CV outside
±25%]; the F0 term applies only to references ≥ 125 Hz (§5).

**CONVERGE-PASS** (all required, inherited from L-PASS):
(a) mean ERR(3)/ERR(0) ≤ 0.80; (b) Wilcoxon signed-rank ERR(3) < ERR(0),
alpha = 0.01; (c) ≥ 16/20 cases strictly improve; every iteration-3 render
differs from iteration-0 by SHA (no resubmission); sign agreement ≥ 80% on
cases with |deviation| > 1% (corrections DIRECTIONAL, not lucky).

**Instability flags** (preregistered, not advisory):
- A case with ERR(k+1) > ERR(k) + 0.01 for any k is flagged LOOP-UNSTABLE.
- A case with two consecutive direction reversals (improve→regress→improve
  or regress→improve→regress) is a SAWTOOTH = FAIL for that case.
- ≥ 5/20 cases flagged unstable → the battery FAILS.

## 3. Real-audio corpus

Minimum 400 clips, sealed before trials (§8):

| Class | Minimum | Content rule |
|---|---|---|
| Field recordings | 100 | Non-speech environmental (indoor/outdoor, ≥3 noise regimes) |
| Speech | 150 | ≥ 30 distinct speakers, conversational (not read lists) |
| Child-vowel-class | 50 | kidc.wav-class: child speech vowel takes |
| Real prosody | 100 | Expressive speech with manifest prosody labels |

Diversity requirements: no single donor/source > 25% of any class; every
clip carries a frozen manifest label (class + per-question ground truth);
the frozen scorer must clear the ≥ 95% sanity floor per question on the
corpus, else those questions are void. **Synthetic renders are calibration
ONLY** (harness sanity checks, gain-change dithers) — never headline
evidence.

**Corpus-sealing protocol**: SHA-256 per clip + corpus-level manifest
(path, sha, class, labels-hash), committed to `tnn-native-lab` BEFORE any
trial binary opens a trial WAV. Trial RUNLOGs record the corpus manifest
commit hash. Clips added after seal = new corpus version, new manifest, and
a note in the verdict (never silent).

## 4. F0 blind-spot kill bars

Measured fact (principles synthesis): the frozen autocorr/YIN F0 definition
cannot resolve below ~125 Hz on real material (verified in organ AND
scorer — a shared definition property), despite the nominal 80–1200 Hz
spec. Attacked two ways, in parallel; first to meet its bar is adopted, the
other recorded defeated-but-documented:

- **Path (i) — better estimator. "FIXED"** iff, on real low-F0 material
  (55–125 Hz, voiced per the frozen analyzer): resolution floor ≤ 65 Hz;
  |f0_meas − f0_ref|/f0_ref ≤ 5% on ≥ 90% of voiced frames; per-band error
  bounds reported (55–80, 80–100, 100–125 Hz); 3× byte-identical
  determinism retained; NO regression — the P-R4 anchor re-run within
  ±0.01 of the frozen baseline.
- **Path (ii) — explicit range restriction. "SCOPING WORKS"** iff: the organ
  contract is amended to state the measured 125 Hz effective floor; on a
  probe battery of ≥ 50 sub-125 Hz real clips, ≥ 95% are reported unvoiced
  or f0 = 0, and 0% are confidently-wrong (voiced = 1 with f0 in
  [80,1200] Hz). Any confident-wrong = SCOPING-FAIL.
- If NEITHER meets its bar → **F0-BLINDSPOT-OPEN**: no F0-anchored gate or
  loop may claim validity below 125 Hz, recorded as a standing restriction.

## 5. Real-clip gap closure: 0.783 → 0.90

Candidate mechanisms (preregistered; each tested head-to-head against the
frozen baseline organ on the sealed corpus, held-out split, frozen scorer,
3× byte-identical):

- **M1 descriptor enrichment**: ≥ 2 new native descriptors (e.g. spectral
  centroid/rolloff from the existing DFT bands; promote the native HNR
  approximation to first-class).
- **M2 longer temporal context**: utterance-level aggregation over the
  2048/Hann frames (vs frame-thirds statistics).
- **M3 better F0**: feeds the prosody bit; gated on §4 path (i).
- **M4 band-decomposition retune**: band edges or a natively computed
  8–16 kHz band.

Verdict ladder:

- **CLOSED**: agreement ≥ 0.90 on the full sealed corpus with the frozen
  scorer, byte-identical 3×, no per-class regression > 2pp vs baseline.
  (Bearing: the re-anchored gate quantities become TNN-native-verifiable
  on real clips — Round-3B call 2 stays Micah's call.)
- **NARROWED**: agreement in [0.85, 0.90).
- **STRUCTURAL CEILING**: agreement < 0.85 after ≥ 2 candidates each
  deliver ≤ +2pp, AND the white-box mechanism is NAMED: which organ
  computation, which signal property of real audio, with a measured causal
  chain (e.g. "reverberant field recordings: frame-RMS thirds lose the
  4 dB rise threshold because the reverb tail fills decays — rise-recall
  0.41 on corpus class F vs 0.93 synthetic"). A story is not a mechanism.

## 6. "See what happens" reporting discipline

Trials report what the machinery ACTUALLY does — including failures,
anomalies, and surprises. Burying is a verdict-voiding offense. Every trial
RUNLOG carries an ANOMALIES section in this format:

```
ANOM-ID: LH-A-###
DATE: <PDT date>
HORIZON: <H0|H10|H100|which checkpoint>
OBSERVED: <measured — exact command, artifact SHAs, numbers>
EXPECTED: <which prereg line, and what it predicted>
CANDIDATES (knowledge-first order): <corpus/label → organ computation → wiring → deliberation>
DISPOSITION: <DIAGNOSED|OPEN|PROMOTED-TO-INVESTIGATION|VOID-RERUN>
```

A run with zero anomalies states explicitly: "zero anomalies observed at
<H>" — absence of evidence is recorded, never assumed.

## 7. Kill bars for the wiring itself

- **K-W1 ABLATION-DEAD**: organ descriptors replaced by a frozen constant
  vector, everything else identical. If the action distribution is
  statistically indistinguishable from wired runs (p ≥ 0.01) → the wiring
  claim is KILLED (deliberation is not consulting the organ).
- **K-W2 ABLATION-DIRECTIONAL**: given a significant ablation difference,
  wired-vs-ablated action changes must track the organ descriptors: sign
  agreement ≥ 70% on cases where the two differ — else WIRING-DECORRELATED,
  claim killed.
- **K-W3 PYTHON-IN-PATH**: any Python process in the per-episode
  descriptor → deliberation → action path → immediate WIRING-FAIL; repair
  needs an amendment.
- **K-W4 NONDETERMINISM**: 3 consecutive full-loop runs byte-identical on
  descriptor stream + action artifacts (SHA); any divergence → WIRING-FAIL
  until root-caused and re-proven.
- **K-W5 BOUNDARY**: anything other than WAV bytes + intent/question
  descriptor crossing into deliberation → BOUNDARY-BREACH, run void.

## 8. Prereg order

1. This prereg frozen on `tnn-native-lab` (this commit).
2. Corpus SHA-256 manifests sealed and committed BEFORE any trial WAV is
   touched by any trial binary.
3. Scorers frozen and committed before runs begin.
4. Every headline number requires 3 consecutive byte-identical runs (SHA
   match); otherwise VOID.
5. Amendments need Micah's word. All commits on `tnn-native-lab`, never
   `main`.

---
*Phase-A1 prereg author, 2026-09-25 PDT. Governs the long-horizon real-audio
program until amended by Micah.*
