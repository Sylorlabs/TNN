# REPORT.md -- IVWC-PERBUCKET: per-bucket bars and bar margin for the hybrid

## Verdict: BUILD-FAIL (K5, K6, K9, K10, K11 fail; K1, K2, K3, K4, K7, K8 pass)

Neither rescue works, for two different reasons. The **bar margin**
(strict inequality, C > T_hyb) behaves exactly as predicted: it
flips precisely the two bar-boundary errors to the true labels and
nothing else, landing 10/12 on both regimes -- parity with the
per-regime winners (OF in-distribution, X3 under law change), but
no strict dominance. The **per-bucket bars** are a catastrophic
failure: 4/12 @wp15 and 3/12 @wp45, worse than the original hybrid
and worse than chance on the law-change regime. The mechanism is
crisp and algebraic: a per-bucket bar exactly cancels the
bias correction it was meant to refine -- C - T_b = P -
mean_sealed(P) within bucket b -- so the consequence-training
content is erased from the verdict and the rule degenerates to
within-bucket relative ranking of internal predictions, with
self-passing bars on thin buckets. The margin result confirms
the hybrid report's boundary-pattern diagnosis; the per-bucket
result shows the global bar was load-bearing, not an arbitrary
choice.

## What was built

`src/ivwc_perbucket.zag` (pure Zag, single file, pinned znc),
`bin/ivwc_perbucket` (frozen binary). World/belief/composer/
stepper/verifier/seeds copied verbatim from IVWC-HYBRID; sealed
(bucket, eff) pairs bit-identical (K3/K4 anchors confirm). New
machinery, all in MAIN, all learner-computed from sealed
predictions + learned biases (no world data, no researcher-set
constant):

- Per-bucket bars: T_b = mean sealed C over sealed cases in
  bucket b (empty bucket -> global T_hyb fallback, reported if
  triggered; never triggered -- every bucket had >= 1 sealed
  case on all three shifts). PB verdict: C >= T_b.
- Bar margin: MG verdict C > T_hyb (strict), same bar as the
  original hybrid.
- Shuffled-bias ablations of both: MGsh (C_sh > T_shyb), PBsh
  (C_sh >= T^sh_b), same rotate-by-7 consequence shuffle.
- In-program arms on one shared label ge = (eff >= T_pred):
  OF, X3, HYB (original, re-anchored), MG, PB, MGsh, PBsh.

Build: `znc src/ivwc_perbucket.zag -o bin/ivwc_perbucket` via the
safebin pinned znc (byte-identical to the hybrid wave's
compiler). Analyzer: one informational zagd-unavailable notice
only. No post-prereg probe of any kind; the hybrid's committed
per-case run outputs were not read.

## Kill-bar results

- K1 (commit before signal / diet): PASS. K1T/K1P STRUCT-PASS
  (wc unchanged across train COMMIT and train PREFF); K1S
  STRUCT-PASS at sh=0/1/2. A1: train COMMIT (636) / PREFF (651)
  precede train CONSEQ world_execute (670); sealed COMMIT
  (793/795) precedes SCORING world_execute (913). A2: 0. A3: 0.
  A4: 0. A6: `world_execute(` x3 (def + 2 call sites);
  WC-FINAL=60 (24 train + 36 sealed). A7: 0.
- K2 (determinism): PASS. 3/3 byte-identical, sha256
  f0acfc84b5466ee5e68eb7345d26b604af2151fdcb313fd50e976467cf50e72b.
- K3 (replication anchor, wp=15): PASS. acc_of=10, acc_x3=9 --
  exact match to published numbers.
- K4 (replication anchor, wp=45): PASS. acc_of=8, acc_x3=10 --
  exact match under law change.
- K5 (per-bucket best-of-both, wp=15): FAIL. acc_pb=4 <
  acc_of=10 and < acc_x3=9.
- K6 (per-bucket best-of-both, wp=45): FAIL. acc_pb=3 <
  acc_of=8 and < acc_x3=10.
- K7 (margin best-of-both, wp=15): PASS. acc_mg=10 >= acc_of=10
  and >= acc_x3=9. Matches the in-distribution winner.
- K8 (margin best-of-both, wp=45): PASS. acc_mg=10 >= acc_of=8
  and >= acc_x3=10. Matches the law-change winner.
- K9 (strict dominance): FAIL. Neither variant strictly beats
  the per-regime winners: MG ties both (10 = 10 on each home
  regime); PB is far below.
- K10 (consequence-content ablation, wp=15): FAIL.
  acc_mgsh=4 < acc_mg=10 (strict drop holds for the margin
  variant), but acc_pbsh=4 = acc_pb=4 -- no drop for the
  per-bucket variant. The conjunction fails. As the mechanism
  section shows, this is not a measurement fluke: the
  per-bucket rule algebraically erases the bias content, so
  shuffling it cannot change the verdicts.
- K11 (non-degenerate, wp=15): FAIL. acc_mg=10 > maj=7 holds,
  but acc_pb=4 < maj=7.

Scoreboard (MG vs PB vs OF vs X3 vs HYB): wp=15: 10 vs 4 vs 10
vs 9 vs 9; wp=30: 8 vs 6 vs 8 vs 9 vs 8 (finding); wp=45: 10 vs
3 vs 8 vs 10 vs 9. The margin variant ties the best pure
approach on every regime; the per-bucket variant is worst on
every regime.

## Mechanism detail (white box)

### The margin variant: exactly the two boundary flips

wp=15 (tpred=28, thyb=21): MG errors {s=0, s=3} -- bit-identical
to OF's error set. The s=10 tie (adj=21, not > 21) flips to FAIL,
matching its true label (eff=25 < 28). No correctly-verdict'd
case sat exactly on the bar, so strict inequality changed
nothing else: verified per-case, MG's verdicts differ from HYB's
only at s=10.

wp=45 (tpred=21, thyb=17): MG errors {s=0, s=4} -- bit-identical
to X3's error set. The s=5 tie (adj=17, not > 17) flips to FAIL,
matching its true label. Again the only HYB/MG verdict
difference is the boundary case.

The margin result is therefore a clean confirmation of the
hybrid report's boundary-pattern diagnosis: both hybrid-specific
errors were bar artifacts, and the minimal honest margin
removes exactly those. What remains is structural, not a bar
artifact: s=0 (confident internal optimism, adj=25@15 / 46@45 --
the internal model is sure and wrong), s=3@15 (phantom items,
adj=46 -- invisible to bucket-level training), s=4@45 (confident
optimism, adj=46). No bar placement fixes score errors; the
strict-dominance ceiling is set by the scores, not the bars.

### The per-bucket variant: the bar cancels the bias

For a sealed case in bucket b, the PB verdict compares
C - T_b = (P - bias_b) - mean_sealed(P - bias_b).
The trained bias_b is constant within the bucket, so it
subtracts out exactly: C - T_b = P - mean_sealed(P).
The verdict no longer depends on the consequence-trained bias
at all -- it is purely "is this case's internal prediction above
its bucket's sealed mean prediction." The per-bucket bar was
meant to refine the bias correction; instead it annihilates it.
Every trained quantity (biases 0/4/15/16) is erased from the
verdict by construction. This is why the ablation cannot hurt
it (PBsh == PB: shuffling a term the rule already cancels) and
why K10's failure is mechanism, not noise.

The per-case damage, wp=15 (bucket bars: b0 Tb=0 cnt=2, b1 Tb=30
cnt=6, b2 Tb=25 cnt=1, b3 Tb=14 cnt=3):

- Bucket 1 (Tb=30): the six sealed cases carry optimistic
  beliefs, so the bucket bar sits at 30 -- above the four
  genuine positives (s=2,4,7,9: adj=29, eff=33, ge=1), all
  flipped to FAIL (29 < 30). The phantom s=3 (adj=46) stays
  PASS. The boundary case s=10 (adj=21) flips to FAIL, but at
  the cost of four good verdicts.
- Bucket 0 (Tb=0): both empty-plan cases (s=1, s=8: adj=0,
  eff=0) PASS on 0 >= 0 -- two FPs from a vacuous bar.
- Bucket 2 (cnt=1, Tb=25): the single case's bar equals its own
  score (s=0: adj=25 >= 25) -- self-PASS on a true FAIL.
  Any singleton bucket self-passes under >= by construction.
- Bucket 3 (Tb=14) is the only bucket that behaves: s=5 PASS
  (28 >= 14, eff=33), s=6/s=11 FAIL (10,6 < 14; eff=20,13).

PB errors @15: {s=0, s=1, s=2, s=3, s=4, s=7, s=8, s=9} -> 4/12.

wp=45 (bars: b0 Tb=0 cnt=7, b1 Tb=62 cnt=3, b2 Tb=10 cnt=1,
b3 Tb=17 cnt=1): bucket 0's vacuous bar passes all seven
empty-plan cases (eff=0, all FP); the singleton buckets self-pass
(s=3: 10 >= 10, eff=0 FP; s=5: 17 >= 17, eff=0 FP). PB errors:
{s=1, s=2, s=3, s=5, s=6, s=7, s=8, s=9, s=10} -> 3/12, below
chance (maj=11/12).

Two compounding defects, both structural: (1) the algebraic
cancellation above -- a per-bucket mean bar on bias-corrected
scores is a within-bucket demeaned prediction, blind to absolute
eff levels; (2) thin-bucket degeneracy -- with 12 sealed cases
over 4 buckets, singleton buckets self-pass and zero-score
buckets pass-all. Defect (1) alone is fatal: even with infinite
sealed cases per bucket, the bias content would still cancel.

## Honest caveats

1. One wall-density law-change axis; item law, belief noise, and
   energy budget fixed (inherited from the hybrid setup).
2. T_pred/T_hyb/T_b/T^sh_b are computed over the sealed batch
   (transductive), but from predictions + learned biases only --
   no world data enters any bar.
3. The 12-case test makes every bar a one-case margin; the MG
   result (10/10) rests on exactly the two predicted boundary
   flips, verified per-case.
4. The consequence-training diet (24 true train outcomes at
   wp=15) is declared in PREREG section 1, not hidden; sealed
   verdicts never observe sealed truth (K1).
5. Mechanism test, not a composition-novelty or L3 claim (per
   PREREG section 3). The composer is fixed; the claims concern
   hybrid-verdict bar variants on the two dissociation regimes.
6. The per-bucket failure does not say "finer bars are always
   bad": it says a bar computed as the within-bucket mean of the
   already-bias-corrected score cancels the correction. A
   per-bucket bar on a different scale (e.g. on raw P with the
   bias kept in the bar, or a bar from a separate calibration
   split) is a different hypothesis, not tested here.

## Reproduction

```
cd docs/lab/research-lead/overnight-20260928/ivwc_perbucket
znc src/ivwc_perbucket.zag -o bin/ivwc_perbucket   # safebin pinned znc
./bin/ivwc_perbucket | sha256sum   # expect f0acfc84b5466ee5e68eb7345d26b604af2151fdcb313fd50e976467cf50e72b
```

Frozen audits (PREREG section 5): A1 ordering 636/651 < 670 and
793/795 < 913; A2 count 0; A3 count 0; A4 count 0; A5 sha256
equality across runs/ivwc_perbucket-run{1,2,3}.txt; A6
`world_execute(` count 3, WC-FINAL=60; A7 count 0.

## Branch note

Work committed on `tnn-native-lab` (the shared checkout this
worker was spawned on). Prereg commit 5f4012189 strictly precedes
the implementation commit. All commits use explicit pathspecs
confined to `ivwc_perbucket/`. Local only, never pushed. Git
writes via /usr/bin/git directly (safebin git symlink is
known-broken for writes).
