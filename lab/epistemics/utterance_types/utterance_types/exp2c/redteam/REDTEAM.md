# REDTEAM.md — H7 exp2c independent red-team

Date: 2026-09-27. Red-team agent: independent subagent of the exp2c coordinator.
Scope: attack the verdict that a 48-episode sincere-calibration corpus moves
hypothetical SINC lookalikes from 3/10 to 9/10 (A+B) and 10/10 (A+B+C under
design β) at zero price.

Method: primary evidence only. `REPORT.md` was not trusted; every number below
was recomputed from the committed raw run outputs, or produced by an
independently rebuilt binary from the committed v3 source. Source commits were
verified as ancestors of `origin/tnn-native-lab` on 2026-09-27
(prereg `48328416`, v2 source `1d52fa9f`, v3 `3f692d84`, report `1890519a`).

Independent rebuild: `h7_exp2c.zag` (v3, from `3f692d84`) + the 39 pristine
input files re-assembled with the pinned toolchain
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`. Build warnings
only (implicit-int + unused-symbol, same class as the original build log).

Verdict scale per attack: **KILL** (claim false) / **WEAKEN** (claim overstated
or under-evidenced; numbers stand but interpretation/grade drops) /
**HOLDS** (attack fails; claim survives).

## Summary table

| # | Attack | Verdict |
|---|---|---|
| A1 | Independent score recomputation (all 13 legs × all bars) | **HOLDS** (1 bar-neutral transcription error) |
| A2 | Teaching-to-the-test / semantic near-duplicates | **WEAKEN** |
| A3 | α/β mechanism (white-box) | **HOLDS** |
| A4 | Probe-blindness of the D/E legs | **WEAKEN** (summary wording, not data) |
| A5 | Reproducibility: rebuild + rerun + determinism + Stage-0 gate | **HOLDS** |
| A6 | HARD0 hardcode re-audit on v3 source | **HOLDS** (footnote: 4 new hits of adjudicated shape) |
| A7 | Protocol deviations (D1–D6) | **WEAKEN** (D1, D6; D2–D5 adequate) |

Headline adjudication:

- **"3/10 → 9/10 (A+B) at zero price": STANDS as a measured effect.**
  All 2c bars pass in ab-a/ab-b/ab-a-rev; independently recomputed;
  byte-identical rerun from my own build; per-probe isolation shows 6 genuine
  causal fixes + 1 identified residual; mechanism white-box verified.
- **"3/10 → 10/10 (A+B+C under β) at zero price": the measured datum stands,
  the preregistered claim does not.** abc-b's numbers are real (10/10 LK, all
  2c bars pass — recomputed and rerun). But: (i) abc-b is Stage-1/pilot-grade
  (predictions post-hoc); (ii) the prereg-compliant volume leg vol2-b reaches
  LK 10/10 only at the price of SINC-DP 8/10 on types 3 and 5 — "zero price"
  does not replicate under the prereg-compliant protocol; (iii) the 10th
  point is carried by cc40, a near-template copy of probe si3_15.

---

## A1. Independent score recomputation — HOLDS

Recomputed every `2C_CURVE`, `H7_CHECK`, `2c_sinc_dp_N`/`2c_sinc_lk_N` check
bit, `n_2c_fail`, frozen failure count, leakage, paraphrase leakage,
suppression, NEST, FHYP, phase-3 facts, and cross-type interference from the
13 committed `runs/*.txt` files with an independent parser
(`~/workspace/redteam_exp2c/recompute.py`).

- All headline experimental rows match the claimed scores exactly.
- All 2c check bits agree with the recomputed ≥9 threshold.
- Auxiliary bars pass in every committed leg: leakage 0/0, paraphrase
  leakage 0/0, suppression 5/5, NEST 20/20, FHYP 20/20, phase-3 20/20,
  cross-type interference checks pass.
- All 13 committed SHA-manifest entries verified against the files.

**One factual error found (bar-neutral):** `bartable.md` claims base type-5
SINC-DP = 9. The raw committed `base_rep1.txt` says
`2C_CURVE|5|TR|20|PA|20|NO|20|DP|10|LK|9` and the check bit
`H7_CHECK,2c_sinc_dp_5,1,1` (PASS). Base type-5 DP is **10**, not 9. No bar
changes (both ≥9); `n_2c_fail=1` still correct.

## A2. Teaching-to-the-test / semantic near-duplicates — WEAKEN

The 16-byte anti-confound rule holds syntactically (independently re-verified:
688 forbidden utterances, 18,331 distinct 16-grams, zero violations in any
2c corpus file; positive control confirmed the checker is live). **But the
rule is miscalibrated to the learner.** The learner is an n-gram marker
machine; the rule blocks 16-byte string identity but not n-gram identity —
and the corpus shares the probes' n-gram frames:

- cc01 "Ask if the corner shop is open." vs probe si3_14 "Ask if the shop is
  open." — Jaccard 0.86; shares 3-grams `ask if the`, `shop is open`.
- cc05 "See if the side door is bolted." vs si3_16 "See if the door is
  locked." — Jaccard 0.62; shares `see if the`.
- cc02 "Check if the rear entrance is bolted." vs si3_18 "Check if the oven
  is off." — shares `check if the`.
- Six probe 3-grams appear verbatim in the corpus: `ask if the`,
  `see if the`, `check if the`, `tell me if`, `shop is open`, `do we leave`.
- Sharpest case: cc40 "It is as if the whole town paused." vs probe si3_15
  "It is as if winter came early." — a near-template copy (shared 4-gram
  `it is as if`, under the 16-byte tripwire).

Per-probe isolation (my own experiment: variant roots with 10 copies of one
probe, base vs ab-a, rebuilt binary) confirms the scores are REAL, not
arithmetic artifacts:

| probe | base LK | ab-a LK | reading |
|---|---|---|---|
| si3_11 "Call me if you need help." | 10/10 | 10/10 | already passing |
| si3_12 "What time do we leave?" | 0/10 | 10/10 | **fixed** (`do we` revoked) |
| si3_13 "I wonder if the mail came." | 0/10 | 10/10 | **fixed** |
| si3_14 "Ask if the shop is open." | 0/10 | 10/10 | **fixed** |
| si3_15 "It is as if winter came early." | 0/10 | 0/10 | residual failure |
| si3_16 "See if the door is locked." | 0/10 | 10/10 | **fixed** |
| si3_17 "I doubt if he will come." | 10/10 | 10/10 | already passing |
| si3_18 "Check if the oven is off." | 0/10 | 10/10 | **fixed** |
| si3_19 "Tell me if it rains." | 10/10 | 10/10 | already passing |
| si3_20 "We will see if they reply." | 0/10 | 10/10 | **fixed** |

So 9/10 = 3 already-passing + 6 genuine causal fixes + 1 residual. The
residual si3_15 is a **joke**-marker collision (`it is` live on the joke
concept in base and ab-a), outside A/B's coverage — and it is exactly what
family C fixes (see A3). The mechanism is genuine marker-collision repair.

The WEAKEN is on the *interpretation*, not the numbers: the corpus was
authored to mirror the probe templates, so the experiment demonstrates
targeted marker-family calibration, not broad sincere-calibration
generalization. The 16-byte verifier gives false comfort against the wrong
threat model (verbatim memorization vs n-gram markers). A same-family
ablation (rewrite A/B frames, keep bigrams) was not run.

Novel-frame probe test (16-byte-novel "if the"/"do we" frames the corpus
never used — "Determine if the vault is sealed.", "Ascertain if the ledger
is balanced.", "Establish if the signal is strong.", "Do we trust the
morning forecast?", "Do we replace the worn cables?", "Confirm if the
cellar door is barred."): **6/6 go from base 0/10 to ab-a 10/10.** The fix
operates at the bigram-marker level, not the taught-template level — the
corpus's template-mirroring is not load-bearing for the effect. (A second
novel set using "whether"/"that" frames failed its own 16-byte novelty
check against the frozen curriculum and was discarded.)

Refined verdict: the scores are real and causal; the mechanism transfers to
untaught frames *within the same marker families* (`if the`, `do we`,
`it is`). What the experiment cannot claim is generalization *beyond* the
taught marker families. "Teaching to the test" is too strong; the accurate
description is targeted marker-family calibration with demonstrated
within-family transfer. The 16-byte rule still guards the wrong threat
model (string identity vs n-gram markers), and a same-family frame-rewrite
ablation was not run.

## A3. α/β mechanism — HOLDS

White-box evidence from the committed MDUMP lines supports the REPORT's
mechanism, and extends it:

- Design β (`design==1`) appends every E item to the endorse pool before
  delivery; the final `calibrate()` revokes any live marker matching the
  expanded pool. Verified in `run_2c` source. α does not append. The β
  effect is architectural, not luck.
- abc-a (α, single-block C): joke CTX markers `evenly`/`says evenly` live
  (PROVISIONAL); the W-items' installs survive → catastrophe is genuine in
  the raw curves and MDUMP.
- abc-b (β): `evenly`/`says evenly` REVOKED; 8 calibrate revocations.
- **New finding (not in REPORT): the 9/10 → 10/10 step is one marker.**
  si3_15 fails as a *joke* collision: joke `it is` is live in base and
  ab-a, REVOKED in abc-b and vol2-b. Family-C E-items (all 8 start "It
  is…", cc40 "It is as if the whole town paused.") revoke it. The 10th
  point is mechanistically identified.
- vol2-a self-corrects under α (interleaving: original-48 E-items revoke
  before the new W-items install) — the REPORT's explanation is consistent
  with the MDUMP (`evenly`, `plainly`, `says evenly`, `says plainly`
  revoked in vol2-a).

## A4. Probe-blindness of the D/E legs — WEAKEN (wording, not data)

Verified: the frozen `sinc*.txt` probe files contain **zero** occurrences of
"what if" and **zero** of "where do". The D/E corpus teaches exactly those
families, so `2c_sinc_lk_3` staying 3/10 in de-a/de-b is uninformative about
D/E efficacy — the REPORT discloses this ("probe-blind, not mechanism
failure").

Two refinements from my own MDUMP audit:
- The mechanism DID engage: `what if` and `where do` (bare bigrams) go
  PROVISIONAL → REVOKED in de-a/de-b; longer n-grams (`what if the`,
  `where do we`) survive. So "no effect" would be the wrong reading; the
  probes simply cannot see the effect.
- The REPORT §1 summary line "Clean generalization" overclaims. The honest
  line is: "no collateral damage; generalization unmeasured with current
  probes." The body text is accurate; the summary is not.

## A5. Reproducibility — HOLDS

- Rebuilt v3 from the committed source (`3f692d84`) with the pinned
  toolchain: success (warnings only).
- **All 13 legs byte-identical** to the committed rep1 outputs from my own
  build (base, ab-a, ab-b, ab-a-rev, abc-a, abc-b, vol-a, vol-b, vol2-a,
  vol2-b, de-a, de-b).
- **Stage-0 gate independently verified:** empty mode from my build emits
  SHA `71731400c1758f883c8057ad3dca044f34491c9a7861e6f53c1c5815b8f75407`
  — the frozen SHA. The v3 `if(mode.len>0)` gate works as specified.
- Determinism: all 3 reps byte-identical within every leg (SHA manifest).
- Frozen baseline SHA independently confirmed in the origin branch.

## A6. HARD0 re-audit — HOLDS (footnote)

- Zero type-name strings in `h7_exp2c.zag` code (one inherited comment
  mention of "hypotheticals" in the FHYP battery note).
- The 5 frozen `fname("tr"/"pa"/"no"/"sinc",…)` file-loading hits are
  inherited unchanged (same lines, shifted by the insertion).
- **Footnote the REPORT omits:** the new 2c re-scoring block adds 4 more
  hits of the same shape (`fname("tr"/"pa"/"no"/"sinc",t3,…)` at the 2c
  scoring site). Same adjudication applies (probe-file loading with `t3`
  as an opaque loop index; no value-branching on the type index anywhere
  in the new code — verified by inspection of `learn_sincere`, `run_2c`,
  dispatch, and scoring).
- Dispatch branches only on mode strings ("ab-a", …) and design 0/1;
  `ti` arrives as an opaque concept index from the item files. No type
  constants in control flow.

## A7. Protocol deviations

**D1 — Stage-1 runs preceded the prediction lock and source commit: WEAKEN
(on confirmatory grade, not on measurements).** The measurements stand as
observed data (they reproduce byte-identically). But the 9/10 (A+B) and
10/10 (abc-b) effects are pilot-grade for prediction purposes: the formal
`PREDICTIONS_LOCKED.md` records Stage-1 as OBSERVED post-hoc. Note the
prereg §5.4 *did* contain detailed Stage-1 predictions (L1 → 9–10/10 etc.);
the crew's conservative downgrade is disclosed and defensible given the
source wasn't committed. **Reporting gap:** the prereg §5.4 L3 prediction
(abc-α → `sinc_lk_3` 10/10) was falsified by the catastrophe (0/10) and is
never scored in REPORT §5. The catastrophe was a surprise; the α/β story,
though white-box verified, is post-hoc.

**D2 — volume legs used 96-all-new instead of 48+48: corrected adequately.**
vol-a/vol-b are retained as labeled supplementary legs; the prereg-compliant
vol2-a/vol2-b were predicted a priori in a dated addendum and run. Trust
vol2 for the prereg volume question.

**D3 — Stage-0 gate fixed in v3: corrected and independently verified**
(A5: empty mode reproduces the frozen SHA from my own build).

**D4 — baseline rebuild timing before prereg: minor.** The baseline
reproduces public frozen evidence; independently re-verifiable (done in A5).

**D5 — post-state 2c scoring: adequate.** The prereg §5.5 specifies
final-state `2C_CURVE`; the base 2c-control leg (not the historical inline
curve) is the comparison, and it reproduces the frozen 3/10.

**D6 — vol2 does not satisfy all bars: WEAKEN on "zero price".** vol2-b
reaches LK 10/10 but SINC-DP drops to 8/10 on types 3 and 5. The only leg
showing 10/10 *at zero price* is abc-b — which is pilot-grade (D1).
Additionally, REPORT §5's "ceiling" row is mis-scored: it claims the prereg
§6.2 ceiling ("no better than L1–L4") was "FALSIFIED positively" by vol2-b's
10/10, but L4 (abc-b) already hit 10/10 — vol2-b *equals* the best Stage-1
result; it does not exceed it. (The addendum's "L1–L4 hit 9/10" misstates
L4's 10/10.)

## What survives

1. The 3/10 → 9/10 (A+B) effect is real, causal, and mechanistically
   identified (revocation of the promiscuous `if the` / `do we` markers;
   6/7 failing probes fixed per-probe; zero collateral damage on any bar).
2. The α/β mechanism is architecturally real (pool-append → final-calibrate
   revocation), white-box confirmed, and it explains both the abc-a
   catastrophe and the abc-b/vol2-b recoveries.
3. The 9/10 → 10/10 step is exactly one marker: family-C E-items revoke the
   joke `it is` collision on si3_15.
4. Reproducibility is total: independent rebuild → all 13 legs
   byte-identical; Stage-0 gate → frozen SHA.

## What does not survive

1. **"3/10 → 10/10 at zero price" as a preregistered claim.** The datum
   (abc-b) is real; the claim-grade is not. The prereg-compliant volume
   leg buys its 10/10 LK with DP 8/10 on types 3 and 5.
2. **Broad-generalization language.** The corpus mirrors the probe
   templates (up to Jaccard 0.86; cc40 ≈ template-copy of si3_15); the
   16-byte rule guards the wrong threat model for an n-gram learner. What
   was shown is targeted marker-family calibration with demonstrated
   within-family transfer (6/6 novel frames fixed) — not generalization
   beyond the taught marker families.
3. **"Clean generalization" for D/E.** The probes are blind to D/E; the
   correct statement is "no collateral damage; generalization unmeasured."
4. **REPORT §5's ceiling row.** vol2-b's 10/10 equals, not exceeds, L4.

## Recommended follow-ups

- Same-family ablation (preregistered): rewrite A/B frames keeping
  `if`/`do we` bigrams, rerun ab-a; does 9/10 persist?
- Preregistered novel-probe battery (predictions locked before running).
- Score the prereg §5.4 L3/L4 predictions explicitly (L3 falsified by the
  catastrophe; L4's 10/10 was a genuine a priori hit worth recording).
- Fix the documentation errors: bartable.md base t5 DP (9→10); addendum
  "L1–L4 hit 9/10" (L4 hit 10/10); REPORT §5 ceiling row (vol2-b equals,
  not exceeds, L4).
- Amend the prereg's D/E prediction as untestable-with-current-probes
  rather than falsified.

## Artifacts (red-team scratch, not committed)

- `~/workspace/redteam_exp2c/recompute.py` — independent score recomputation
- `~/workspace/redteam_exp2c/overlap_check.py` — 16-byte contamination checker
- `~/workspace/redteam_exp2c/mdump.py` — MDUMP marker-state differ
- `~/workspace/redteam_exp2c/probe_test.py` — per-probe isolation + novel probes
- `~/workspace/redteam_exp2c/similarity.py` — corpus/probe similarity quantification
- `~/workspace/redteam_exp2c/evidence/` — pristine extraction from origin
  (sources, corpora, runs, manifests, prereg, predictions, bartable)
- `~/workspace/redteam_exp2c/build/h7_exp2c_bin_rt` — independent rebuild
  (binary; do not commit)
- `~/workspace/redteam_exp2c/root/` — pristine input root (39 files)
