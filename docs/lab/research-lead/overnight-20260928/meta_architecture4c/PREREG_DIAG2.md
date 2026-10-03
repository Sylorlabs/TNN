# PREREG_DIAG2: MA4c diagnostic stage 2 -- revised cross-error proxy

## 0. Standing (exploratory, preregistered)

Diagnostic stage 1 (PREREG_DIAG.md) measured the totals-form
cross-error ratios: 2.90 (E735 genuine) vs 3.42 (E795 adversarial),
and exposed two flaws in the totals form: (1) vacuous fire when
xerr[j][i]=0 from a post-wins anchor reseed, with an additional
apples-to-oranges case (E795 VI1/J2) where totals fire but the
means ratio is 12.7; (2) reverse absorption, where the young B4
model would absorb the old R model at E795 (ratio 2.12). This
prereg covers the REVISED design's diagnostic measurement. The
frozen experiment gets its own prereg (PREREG.md) after this stage.

## 1. Revised design under test

New learner state: `xerr[16]` (as stage 1) plus `xcnt[16]` (arena
3683308, 64 bytes): for each ordered pair (j,i), the number of
episodes won by cell i witnessed by cell j's current incarnation
(i.e. the number of i-wins contributing to xerr[j][i]). Update:
every episode, for all j: xerr[j*4+w] += err_j and xcnt[j*4+w] += 1.
Zeroing: on reseed of v, zero rows v and columns v of both tables.

Revised proxy rule `redun2(G,cb,i)` (form frozen; K adopted here):
cell i is redundant given protected cell j (j != i) iff ALL of:
- (G) minimum shared evidence: xcnt[j][i] >= 5. The 5 is PACT, the
  architecture's own frozen minimum-evidence standard for shown
  success, not a new domain quantity. Blocks vacuous comparisons
  (xerr=0 from no shared experience) and thin-evidence judgments.
- (A) absorption flows toward greater evidence: wpart[j] >= wpart[i].
  A younger model may not absorb an older model's role; the anchor's
  model must rest on at least as much winner evidence as the
  victim's. No constant. Blocks reverse absorption (E795 VI3/J2).
- (R) takeover cost within Kx: xerr[j][i]*wpart[i] <= K*wpsm[i]*xcnt[j][i],
  the integer-exact means comparison
  (xerr[j][i]/xcnt[j][i] <= K * wpsm[i]/wpart[i]): the anchor's mean
  error on the shared wins is within Kx of the victim's mean error
  on its own wins. K is dimensionless (takeover cost vs current
  cost), not a domain value-distance.

All quantities are learner-measured from revealed values; no mean
distance, no RDDM, no block labels reach the rule.

## 2. Diagnostic stage 2 implementation (write-only)

`ma4c_diag2.zag` = `ma4c_diag.zag` plus:
- xcnt[16] accumulation alongside xerr; row/column zeroing on reseed
  for both tables (identical to the future learner-state discipline).
- DIAG2 audit entries replacing the DIAG ones: per trigger, per
  candidate vi (prot, wpart, wpsm), per anchor j: mdist, xerr, xcnt,
  wpart_j, oldbit (prot(j) and mdist<=10), bit R2/R3 = prot(j) and
  (G) and (A) and (R) with K=2/3. No decision reads the new state.
- Banner "MA4cD2".

Predicted: every non-DIAG2, non-banner line byte-identical to MA4b's
run1.txt (cmp after filtering); 3/3 runs byte-identical (sha256
recorded).

## 3. Soundness gate (frozen here)

From the DIAG2 lines, the revised design is SOUND iff:
- (a) at E735, the revised rule with K=3 fires for victim cell 2
      (via anchor cell 3), and the redundancy-path victim selection
      still picks cell 2 (trajectory preserved through E735);
- (b) at E795, the revised rule with K=3 is silent for cell 2
      (adversarial pair), silent for cell 3 (age blocks reverse
      absorption), and silent for all other candidates (guard blocks
      vacuous fires), so no redundancy-path reseed occurs;
- (c) the old proxy's per-candidate bits still fire at E795 for the
      (2,3) pair (the kill pattern is still presented; the shadow in
      the frozen stage will rely on this).

K=3 is adopted iff (a)-(c) hold; K=2 is expected to fail (a) given
stage-1's 2.90. The E735 margin ((3-ratio)/3) is reported exactly;
a margin below 15% is a disclosed limitation (exploratory,
one-stream K choice needing multi-stream validation), not a silent
pass. If no K in {2,3} satisfies (a)-(c), the design is UNSOUND and
MA4c reports the negative result with no frozen implementation.

## 4. Artifacts planned (diagnostic stage 2)

- `ma4c_diag2.zag`, `ma4c_diag2_bin`, `d2_1.txt`, `d2_2.txt`, `d2_3.txt`
- This prereg (this commit)

## 5. Commit order

This prereg commit (PREREG_DIAG2.md only, plus the stage-1
implementation files whose prereg is already frozen in 984e4d29)
strictly predates the stage-2 implementation commit. Concretely:
commit A now = stage-1 implementation (ma4c_diag.zag, bin, diag
runs) + NAMECHECK.md (incident + stage-1 record) + PREREG_DIAG2.md;
commit B later = stage-2 implementation only.
