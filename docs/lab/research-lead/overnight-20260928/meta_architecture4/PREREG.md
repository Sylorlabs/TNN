# PREREG: MA4 -- Adversarial close-regimes red-team of the RDDM=10 redundancy proxy

## 0. Standing

MA3 (C449) demonstrated redundancy-aware victim choice: with K=4
saturated, the architecture reseeded redundant duplicates twice
(REDSEEDW=2, BADRED=0) and never destroyed unique knowledge
(PROTDEST=0). MA3's prereg froze an explicit honest limitation,
named as red-team future work: "Mean distance is a proxy for
shared regime knowledge, not a proof of it. Distinct regimes
closer than RDDM would be conflated." MA3's W5 kept distinct
regimes >= 15 apart while redundant pairs sat at <= 5, so the
proxy was never stressed. MA4 is the adversarial test MA3's
prereg called for: two genuinely distinct regimes with means
within RDDM=10, built so the mean-distance proxy conflates them,
asking whether the architecture then destroys unique demonstrated
knowledge.

The architecture is MA3's UNCHANGED (not a redesign): cell
selection, EMA scoring, absorption, the consec>=3 trigger, the
protection predicate (PACT=5, PERR=10), the redun() predicate
(RDDM=10), and the victim rule (a) unprotected / (b) redundant
lowest-wpart / (c) decline are all frozen as in MA3. Only the W
stream changes (W5 -> W6, adversarial). X/Y/Z replicate MA3
exactly and are expected byte-identical to MA3's outputs.

Nothing in this prereg weakens any frozen bar. All thresholds
below are frozen before implementation.

## 1. Adversarial design (frozen)

W6 (852 episodes, one frozen binary):
- D (e 0..11): MA3's exact Block D (tiled {16..24} with
  40/47/54 outliers at e=3/7/11). Distractor cell, mean ~20.
- R (e 12..671): NEW tile {73..81} (mean 77), independent
  shuffle, 660 episodes. Genuinely distinct regime 1.
- B2 (e 672..731): NEW tile {46..54} (mean 50), independent
  shuffle, 60 episodes.
- B4 (e 732..791): NEW tile {78..86} (mean 82), independent
  shuffle, 60 episodes. Genuinely distinct regime 2.
  |77 - 82| = 5 <= RDDM=10.
- B5 (e 792..851): tile {46..54} (mean 50), independent
  shuffle, 60 episodes (return to the B2 regime).

The two close regimes (R and B4) are genuinely distinct by:
(1) different generative tiles; (2) independent shuffles;
(3) temporal separation by B2 (60 episodes, different regime);
(4) independent demonstration: the R-cell accumulates 200+
winner episodes on R values with mean win-error <= 10, the
B4-cell 50+ winner episodes on B4 values with mean win-error
<= 10, both protected; (5) disjoint demonstrated histories
(no episode belongs to both); (6) no block labels reach the
cells (B6/B7). The proxy sees only |mean_i - mean_j| <= 10
and ignores (1)-(5). Disclosed: the value ranges overlap on
{78,79,80,81}; distinctness is by construction and
demonstration, not by range disjointness. (The parent task's
illustrative 75/82 pair also overlaps; the implemented 77/82,
distance 5, is chosen for robustness to the R-absorber split,
see section 5.)

The adversarial event: at the B5-onset trigger, the
redundancy path fires with victim = the R-regime cell and
anchor = the B4-regime cell, even though no protected cell
shares the victim's regime. The architecture then holds two
50-models and zero models of the {73..81} regime: unique
demonstrated knowledge destroyed because the proxy conflated
it.

## 2. Frozen mechanism (MA3 unchanged) + harness tripwire

Learner (frozen, from revealed values only): prot() as MA2;
redun(i) iff prot(i) and some prot(j), j != i, has
|mean_i - mean_j| <= 10; victim rule (a)/(b)/(c) as MA3;
RDDM=10 joins the researcher-supplied constants (same status
as PACT/PERR).

New HARNESS-SIDE tripwire (write-only, no feedback into cell
state, same status as MA3's snapshots/tripwires): per-cell
per-block winner tallies for W (4 cells x 5 blocks;
blocks 0=D,1=R,2=B2,3=B4,4=B5). At each W redundancy-path
reseed, the harness computes the victim's dominant block
(argmax of its winner tallies, ties -> lower index) and
checks every protected anchor j != victim with
|mean_victim - mean_j| <= 10. ADVKILL increments iff
{victim_dominant, anchor_dominant} == {1, 3}, i.e. the
proxy paired the R regime with the B4 regime. BADRED (MA3's
in-binary predicate tripwire) is kept: it must stay 0,
confirming the implementation matches the (defective)
proxy design rather than misimplementing it.

## 3. Experimental protocol (frozen harness)

X/Y/Z: MA3 exactly (tiles t9={16..24}, t3, t9r={76..84},
t9b={16..24}; seeds 20261020/21/22/23). Expected
byte-identical to MA3's run outputs (verified by cmp).

W6: D identical to X's D (same tiles, same order);
R/B2/B4/B5 use new dedicated tiles (t9w={73..81},
t9wb={46..54}, t9c={78..86}, t9d={46..54}), each shuffled
with the continuing PRNG stream. SEED_W6=20261026 for W
flips (new, frozen). X/Y/Z tiles and seeds untouched, so
their trajectories cannot change.

## 4. Frozen metrics

All MA3 metrics carried over, with W-block targets updated
for W6's tiles: RWB2 = first W-B2 episode k (1..60) with
|MWA-50| <= 1; RWB4 = first W-B4 episode k with
|MWA-82| <= 1; RWB5 = first W-B5 episode k with
|MWA-50| <= 1. (X's RXB2 still targets 20; X/Y/Z unchanged.)
TRIGW/DECLW/REDSEEDW/BADRED/PROTDEST as MA3, plus ADVKILL.
New audit output: per-cell per-block winner tallies (WBLK)
and the dominant-block pair at each R-path reseed.

## 5. Mechanism-derived predictions (frozen)

- T1 (log E14, 0-indexed e=13): U-path, victim=cell3, as
  MA3 (D identical; R-onset trigger logic unchanged).
- During R: the MA3 v14-split dynamics produce two
  R-absorbers at ~ (tile mean - 3) and ~ (tile mean + 1.5),
  i.e. ~74 and ~78.5 for the {73..81} tile (MA3: 76.9/81.5
  from {76..84}); both protected. Both are within RDDM=10
  of the B4-learned mean (~82), so the adversarial call is
  robust to which absorber survives T2'.
- T2' (log E675, 0-indexed e=674, B2 onset): active =
  R-absorber errs >20 three straight; winner = spare cell1
  (mean 40); candidates = {D-cell, other R-absorber}, both
  protected. R-path; victim = the R-absorber candidate
  (genuine duplicate, redundant via the active absorber).
  Reseeds as the 50-model. REDSEEDW=1.
- During B2: the 50-model is protected; spare cell1 wins
  low B2 values and may or may not reach protection.
- T3' (log E735, 0-indexed e=734, B4 onset): active =
  50-cell errs >20 three straight; winner = R-survivor;
  candidates = {D-cell, cell1}. Victim = cell1 via U-path
  (if still unprotected) or R-path (if protected: genuine
  duplicate of the 50-model). Reseeds as the 82-model.
- During B4: the 82-model is protected (WP ~50+).
- T4' (log E795, 0-indexed e=794, B5 onset): active =
  82-cell (lowest score) errs 28..36 three straight on
  {46..54}; winner = 50-cell (err 0..4); candidates =
  {D-cell (mean ~20), R-survivor (mean ~74..78.5)}.
  R-survivor is redundant SOLELY via the 82-cell anchor
  (|~76 - 82| <= 10); D-cell is unique (nearest protected
  mean 50, distance 30). Victim = R-survivor (only
  redundant candidate) -> reseeds as a second 50-model.
  The {73..81} regime loses its only model. ADVKILL=1.
- TRIGW n=4; REDSEEDW in {2,3} (T2'+T4', plus T3' iff
  R-path); DECLW=0; BADRED=0 (predicate implemented
  correctly); PROTDEST=0 (proxy-internal consistency holds;
  the defect is proxy-vs-ground-truth, measured by B10).

## 6. Frozen verdict mapping

- B1 COMMIT-ORDER: PASS iff this prereg commit (PREREG.md +
  NAMECHECK.md Step 0 only) strictly predates every
  implementation commit.
- B2 TOOLCHAIN: PASS iff safebin-only PATH throughout,
  Step 0 recorded, zero forbidden-executable invocations.
- B3 DETERMINISM: PASS iff 3/3 runs byte-identical
  (sha256 recorded).
- B4 NOVELTY: PASS iff (a) 12 Block-D values pairwise
  distinct (X), (b) same-episode flip vectors differ across
  X/Y/Z (as MA3; W tiles intentionally differ, reported
  separately), (c) per-block ones-fractions in bands:
  X/Y/Z as MA3; W: D [2880,5040], R {73..81}
  [554400,712800], B2 {46..54} [28800,43200], B4 {78..86}
  [50400,64800], B5 {46..54} [28800,43200].
- B5a RECOVERY (kill bar): PASS iff 1 <= R_X <= 99.
- B5b BASELINE-REPLICATION: PASS iff R_Z >= 500.
- B5c COST: PASS iff COST_XY < 4690.
- B5d SHIFT-BACK: PASS iff 1 <= R_XB2 <= 30.
- B5e APPARATUS: PASS iff max etc <= 1200 and genfail=0.
- B5f STREAM-VALIDITY: PASS iff PARID=1 over X/Y/Z and
  W-vs-X over the D block (e<12), and XDISJ=1 over X/Y/Z.
  (W's R/B2/B4/B5 tiles are adversarially different by
  design; cross-condition identity there is not claimed.)
- B5g MANIPULATION: PASS iff b5gok=3 (cell 0 of X and of
  W6 both end Block D with sum=180, n=9).
- B6 NO-RESEARCHER-RULE: PASS iff learner fns read only
  revealed values and derived tallies; the per-block
  winner tallies and ADVKILL computation are write-only
  harness hooks with no feedback into cell state (audit
  by grep/diff as MA3).
- B7 OPAQUE-IDS: PASS iff episode labels are E0001.. and
  case-insensitive grep for the frozen 29-word list in
  ma4.zag returns empty.
- B8 NO-UNIQUE-DESTRUCTION: PASS iff PROTDEST=0.
- B9 REDUNDANCY-PATH (kill bar): PASS iff REDSEEDW >= 2
  AND BADRED=0.
- B10 ADVERSARIAL-KILL (PRIMARY, kill bar): PASS iff
  ADVKILL=1, i.e. a redundancy-path reseed paired the
  R regime (dominant block 1) with the B4 regime
  (dominant block 3).

Headline verdict: INFORMATIVE-FAIL (proxy) iff B10 PASS
and B5a PASS and B9 PASS, with B1, B2, B3, B5b, B5c, B5d,
B5e, B5f, B6, B7, B8 all PASS: the RDDM=10 mean-distance
proxy conflated two genuinely distinct regimes and the
architecture destroyed unique demonstrated knowledge
because of it. (Predicted outcome; the red team expects
to break the proxy.)

If B10 FAILS (ADVKILL=0) with the apparatus bars PASS,
the headline is PROXY-SURVIVES: the red team failed to
break the proxy on this design, and the report must
diagnose why (e.g. the adversarial trigger did not
materialize as predicted vs the proxy genuinely
distinguished the regimes). A broken prereg is amended
transparently and re-frozen, never reinterpreted.

## 7. Honest boundaries (frozen)

- What is learned are cell means (L1/L2-ish), as MA1-3.
  Not strategy invention, not L3. RDDM=10 remains a
  researcher-supplied constant; the red team attacks the
  proxy design, not the learner.
- ADVKILL=1 is a proxy-design failure, not an
  implementation bug: BADRED=0 is predicted to hold
  simultaneously, separating "code does what the proxy
  says" from "the proxy says the wrong thing".
- The R/B4 value ranges overlap on {78..81}; regime
  distinctness rests on construction, temporal
  separation, independent demonstration, and disjoint
  histories (section 1), not on range disjointness.
- One W6 scenario, one frozen seed set; X/Y/Z seeds
  reused from MA1-3 for direct comparability.
- The T3' path (U vs R) is trajectory-dependent and is
  logged, not bar-gated; B9 uses >= 2 for this reason.

## 8. Artifacts planned

- `ma4.zag`: frozen implementation (B6/B7 audited).
- `ma4_bin`: frozen compiled binary.
- `run1.txt`, `run2.txt`, `run3.txt`: 3/3 byte-identical
  outputs.
- `REPORT.md`: results and frozen verdict.
- `NAMECHECK.md`: build record (this file's Step 0 +
  build record).
