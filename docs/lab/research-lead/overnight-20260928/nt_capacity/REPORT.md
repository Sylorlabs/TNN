# REPORT: NT-CAPACITY (NT2)

## Verdict

**FAIL** per the frozen verdict mapping (PREREG Section 8, as amended by
A1). K1, K3, K5 hold; K2 and K4 fail. This is the preregistered
directional prediction: the selective-retention principle does NOT
survive capacity pressure under NT1's generic eviction rule.

## Frozen results (3/3 byte-identical)

- Run digest: `3d33f8333e31e91a6fb8188a5d442da13896fdc4d6eb18624472ca73bcd32644`
- Binary digest: `9f9aab1b053a35634b9bc7af65a4021e93b1d7b8e0064b7ee599ba8b1bc15a28`
- Source digest: `aac50efbd6eae5aeaeca83cb37001e290b8d0b4de49c8ab2b4c682a4fb72fdbb`

```
NT2 ML1 CTRLA ttc=2 acc=24 nevict=0
NT2 ML1 CTRLB ttc=2 pc=1 acc=24 nevict=0
NT2 ML1 SEQ ttcA=2 accA=24 accB=18 nevict=41 nentries=30
NT2 ML1 RETEST c_vb=0 nc=6 u=12 forget=6
NT2 ML1 EVHIST 100=6 101=5 102=5 103=5 104=5 105=5 134=1 135=1 136=1 137=1 138=1 139=5
NT2 ML0 ABL ttcA=2 accB=24 nevict=0 nalias=12 nentries=24
NT2 ML0 RETEST c_vb=6 nc=6 u=0 forget=12
NT2 K1=1 K2=0 K3=1 K4=0 K5=1
NT2 VERDICT=FAIL
```

Every frozen numeric prediction matched exactly (Section 6), except the
K5 nalias literal, which is the subject of the transparent amendment A1
below. In particular the full 12-bin eviction histogram matched the
hand-derived prediction bin-for-bin.

## Kill-bar evaluation

- K1 (learning intact under capacity): PASS. Both families learnable in
  isolation at CAP=30 (TTC 2/2), SEQ phase A clean (TTC 2, 24/24).
  Capacity itself does not break learning; no VOID.
- K2 (eviction minimal, no churn): FAIL. nevict_seq = 41, not the forced
  minimum 6. Eviction churns at +7 per pass from pass 2 onward instead
  of settling.
- K3 (uncontested retention survives): PASS. NC_OK = 6/6, U_OK = 12/12.
  Keys B never contradicts are fully retained under pressure.
- K4 (revision survives pressure): FAIL. C_VB = 0/6, FORGET = 6. The six
  contradicted keys never complete revision; all six are absent at
  retest.
- K5 (discriminative validity): PASS (as amended). ML0 shows the pure
  alias signature (u_abl = 0/12, nevict_abl = 0, nalias_abl = 12),
  sharply distinct from ML1's eviction signature (nevict 41 vs 0,
  u 12/12 vs 0/12, c_vb 0/6 vs 6/6). The apparatus distinguishes the two
  fragility modes.

## What this establishes

1. **Eviction preempts revision.** This is the mechanism, traced through
   the frozen rules and confirmed bin-for-bin by the histogram. A
   contradicted C key accumulates ref, depressing its net evidence to 1
   (sup=2, ref=1) -- tying it for globally-lowest with just-inserted
   novel keys (sup=1, ref=0, net=1). The generic tie-break (lowest slot
   index) then evicts the actively-revising C keys to make room for
   novel keys; within each pass, each new novel key evicts the one
   inserted just before it. Evicted C keys are re-inserted FRESH
   (sup=1, ref=0) on the next pass, so ref never exceeds sup: revision
   can never complete. The churn is a stable cycle, not a transient.
2. **The evicted set is exactly the working set of ongoing learning.**
   Histogram: keys 100..105 (revising) evicted 5-6x each; keys 134..139
   (incoming novel) evicted 1-5x each; keys 106..123 (agreed or
   untouched) evicted 0x. Eviction cannibalizes the entries current
   experience is about, while the untouched U keys (net=2, never
   reinforced during B) are never eviction candidates. Under the
   generic lowest-net rule, contradiction is punished more than staleness.
3. **The failure is complementary to ML0's, not a blur.** ML0 (no
   eviction possible, aliasing instead) revises contested keys normally
   (c_vb=6/6) but destroys aliased uncontested keys (u=0/12). ML1
   retains uncontested keys (u=12/12) but cannot revise contested ones
   (c_vb=0/6). Two addressing/eviction regimes, two clean complementary
   fragility signatures, one apparatus detecting both.
4. **A stable solution existed and was not found.** CAP=30 admits all 24
   B keys simultaneously, yet the dynamics never converge there: the
   revision rule's evidence reset (sup=1, ref=0 on revise) and the
   ref-accumulation dip keep revising entries at the bottom of the
   eviction ranking. The interaction is structural, not a capacity
   shortage.

## Q1/Q2/Q3 answers (frozen questions)

- Q1 (does selective retention survive eviction?): Partially. Retention
  of the uncontested survives (K3); revision of the contradicted does
  not (K4). The NT1 pattern does not survive intact.
- Q2 (what gets evicted, and is it the right thing?): The revising and
  the incoming -- the entries with the most current-experience
  relevance. By the preregistered definition of correct (minimal,
  revision completes, nothing needlessly forgotten), it is the wrong
  thing: 41 evictions instead of 6, revision preempted, 6 keys forgotten
  that a stable assignment could have kept.
- Q3 (does evidence-revision interact correctly with eviction?): No.
  The two rules are locally consistent but dynamically pathological:
  revision depresses net evidence, and eviction removes low-net entries,
  so eviction systematically removes entries mid-revision.

## Amendment A1 (transparent; committed before implementation)

The as-first-built binary evaluated K5 with the prereg's original
nalias literal (72) and reported K5=0 / VERDICT=INCONCLUSIVE. The 72 was
a hand-trace arithmetic error in the prereg: under the frozen Section 2
rules each B-novel key aliases its ML0 slot exactly once (pass 1); from
pass 2 on the novel key owns the slot, so nt_find hits and the update
path runs. The rule-derivable value is 12, corroborated by NT1's own
ML0 arm (nalias=12 under 4 B passes). The bar's stated intent -- pure
alias signature, distinct from ML1 -- is fully satisfied by the data
(u_abl=0/12, nevict_abl=0, nalias_abl=12 vs ML1's nevict=41).

Per governance (broken prereg -> amend transparently and re-freeze, never
pretend the execution was valid): PREREG.md Section 11 records A1; the
amendment was committed alone (8acb5da) before the implementation
commit; the one-literal source fix was rebuilt and re-run 3/3
byte-identical. The ONLY output lines that changed vs the pre-amendment
build are K5 (0->1) and VERDICT (INCONCLUSIVE->FAIL); every measurement
line is byte-identical. The corrected verdict FAIL is the preregistered
directional prediction. The pre-amendment output is preserved at
/tmp/nt2_run1_preamend.txt for audit.

## Honest boundaries (from PREREG Section 10, unchanged)

- ML1/ML0 are minimal surrogates for the principle under test, not
  TNN's production memory substrate. This FAIL characterizes the NT1
  rule-set under pressure; it does not show TNN-as-built is fragile.
- Families are memorized key-value mappings; no L2/L3 claim. The
  experiment measures retention/revision/eviction dynamics only.
- Single capacity point (CAP=30, 1.2x over capacity); pressure-ratio
  scaling is out of scope.
- Single contradiction magnitude; graded contradiction out of scope.
- The eviction histogram is measurement-only; it influenced no learner
  decision.
- The tie-break (lowest slot index) is part of the tested generic rule,
  not a tuned choice; alternative generic policies (total-evidence,
  recency-weighted, evidence-preserving revision) are preregistered as
  follow-up hypotheses, not implemented here.

## Recommended follow-up (preregistered, PREREG Section 9)

Test whether ANY generic non-protective eviction policy preserves
revision under pressure: (H1) evict by lowest total evidence (sup+ref);
(H2) recency-weighted eviction; (H3) revision preserving accumulated
evidence instead of resetting to sup=1. Each needs its own prereg with
kill bars. Do NOT patch the tie-break or add protection -- the FAIL is
diagnostic.

## Provenance

- Prereg frozen alone: commit `eb74184` (PREREG.md + NAMECHECK.md only),
  strictly before implementation.
- Amendment A1 frozen alone: commit `8acb5da` (PREREG.md only), strictly
  before the implementation commit.
- Implementation + results: this commit. Pure Zag, safebin-only PATH,
  pinned znc 2026.07.0-dev. Zero forbidden-executable invocations.
- Build: `znc nt2_full.zag -o nt2_bin`; 3/3 runs byte-identical (cmp).
- Commits local only, explicit pathspecs, never pushed.
