# PREREG_DIAG: MA4c diagnostic -- learner-observed cross-error statistics

## 0. Standing (exploratory, preregistered)

MA4b's headline: the current-band tripwire (ADVKILL2) sees the E795
kill, but the proxy itself (RDDM=10, researcher-supplied mean-distance
threshold) still destroys the B4 model. MA4c tests whether the
learner can determine redundancy itself. This prereg covers the
DIAGNOSTIC stage only: measure the learner-observable cross-error
statistics at the two W triggers on the frozen MA4b trajectory, then
decide whether the design is sound. The frozen experiment (exact rule,
frozen bars) gets its own prereg (PREREG.md) after this stage.

Nothing here weakens any frozen bar: the diagnostic changes no
decision, and its soundness gate is stated before measurement.

## 1. Design under test

New learner state `xerr[16]` (arena 3683244, 64 bytes): for each
ordered cell pair (j,i), entry (j*4+i) holds the cumulative
prediction error of cell j on episodes won by cell i. Update rule:
every episode, after winner w is determined, for all j in 0..3:
xerr[j*4+w] += err_j, where err_j is the per-episode prediction
error already computed for scoring (revealed values only). Zeroing
rule: on reseed of cell v, zero row v and column v (7 entries):
the destroyed model's evidence no longer describes the new model,
mirroring the wblkc zeroing discipline from MA4b.

Candidate proxy rule (form frozen; K adopted from this stage):
cell i is redundant given protected cell j iff prot(i)=1 and
xerr[j][i] <= K * wpsm[i]. wpsm[i] is i's own cumulative winner
error (already learner state). Both sides are learner-measured
error tallies in the learner's own units; K is dimensionless
(takeover cost relative to current cost), not a domain
value-distance. The old RDDM=10 proxy is untouched in this stage.

## 2. Diagnostic implementation (write-only)

`ma4c_diag.zag` = `ma4b.zag` plus:
- xerr accumulation in the episode loop of run_multi (all conds),
  from the terr per-cell errors; no feedback into cell state,
  scores, winners, or trigger decisions.
- xerr row/column zeroing in the reseed block (all conds),
  identical to the future learner-state discipline.
- At each trigger evaluation (all conds, before any reseed), one
  DIAG audit entry buffered to diaglog (arena 3683312, 96 entries
  x 384 bytes) and printed after all existing output as DIAG
  lines: episode, cond, victim v, vkind, then per candidate vi:
  prot(vi), wpart(vi), wpsm(vi), then per anchor j: mdist(vi,j),
  xerr[j][vi], oldbit (prot(j) and mdist<=10), bit2 (prot(j) and
  xerr<=2*wpsm), bit3 (prot(j) and xerr<=3*wpsm).
- Banner string "MA4cD" to distinguish from MA4b output.

Predicted: every non-DIAG, non-banner output line byte-identical
to MA4b's run1.txt (verified by cmp after filtering); 3/3 runs
byte-identical (sha256 recorded). The learner trajectory is
provably unchanged: the only new arena writes are xerr/diaglog,
never read by any decision.

## 3. Soundness gate (exploratory adoption criteria, frozen here)

From the DIAG lines at the W triggers, compute for the genuine
pair (E735: victim cell 2, anchor cell 3) and the adversarial
pair (E795: victim cell 2, anchor cell 3) the ratio
xerr[j][i] / wpsm[i]. The design is SOUND iff:
- (a) the genuine-pair ratio < K and the adversarial-pair ratio
      > K for K=2 or K=3 (candidate Ks measured, not fitted
      beyond this binary choice);
- (b) each side has at least 15% relative margin from the K
      boundary (genuine <= 0.85*K, adversarial >= 1.15*K);
- (c) under the adopted K, the per-candidate audit at E735 still
      selects victim 2 via the redundancy path (trajectory
      preserved through E735), and at E795 no candidate is
      flagged redundant for the adversarial pair;
- (d) the adopted K is the smaller of {2,3} satisfying (a)-(c).

If no K in {2,3} satisfies (a)-(c), the design is UNSOUND: MA4c
stops and reports the measured numbers as a negative result; no
frozen implementation follows. The K choice stays exploratory
(one W6 stream, one seed set) and is disclosed as such.

## 4. Artifacts planned (diagnostic stage)

- `ma4c_diag.zag`, `ma4c_diag_bin`
- `diag1.txt`, `diag2.txt`, `diag3.txt` (3/3 byte-identical)
- This prereg and NAMECHECK.md Step 0..1 (this commit)

## 5. Commit order

This prereg commit (PREREG_DIAG.md + NAMECHECK.md only) strictly
predates the diagnostic implementation commit.
