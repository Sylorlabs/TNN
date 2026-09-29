# ROUTER3_RESULT: H-ROUTER3 Threshold Compilation and Mark Provenance

**Verdict: H-ROUTER3 SURVIVES.** All four frozen kill bars pass.
**Frozen prereg:** `PREREG_ROUTER3.md` (commit `fb7ea5d56`), strictly before
implementation. No amendments.
**Date:** 2026-09-29
**Raw evidence:** `ROUTER3_RAW_OUTPUT.txt` (md5
`9c2206c9ba506fe23c2670b0865cebc9`, 3 runs byte-identical)
**Implementation:** `router3_learn.zag` (induction machinery copied from
`router2_learn.zag` untouched; new sections: threshold compilation, compiled
routing table, mark provenance audit; new `main()`). `router2_learn.zag`
not modified.
**Pure Zag. No Python.**

## Kill bar results

**K-R3-1 (gamed curriculum flagged): PASS.** On the X-R1 gamed variant
(s0=1 multi-seg items marked CAUS_LEARN), the run emits
`MARK-MERGER: task CAUS_LEARN spans multiple s0-families` and the
mark-dependence manifest lists the gamed marks (#1..#4 under CAUS_LEARN
rules). Replay is 18/18: the gamed marks are compiled faithfully, not
rejected. On the honest curriculum, no MARK-MERGER fires for any of
{11,12,13,14}. The diagnostic distinguishes the runs.

**K-R3-2 (threshold generalization): PASS 10/10.** nseg=5,6,7,8,9 str>str
inputs all route PROC_LEARN; nseg=5,6,7,8,9 iii>ii inputs all route
CAUS_LEARN. This matches H-ROUTER's authored predicate
(`nseg>=2 && all_pair_str==1` -> PL, `nseg>=2 && all_ep==1` -> CL,
`route_learn.zag`). K-R2C (withhold on nseg=5) is SUPERSEDED by this bar,
as preregistered: the behavior change is intentional and tested.

**K-R3-3 (regression + faithfulness): PASS.** All 16/16 original H-ROUTER2
suite items route identically through the compiled table, and REPLAY is
18/18 on the honest curriculum (every mark reproduced by the compiled
policy).

**K-R3-4 (determinism): PASS.** Three consecutive runs byte-identical
(md5 `9c2206c9ba506fe23c2670b0865cebc9`).

## What was repaired

**X-R3 (threshold divergence):** The post-induction threshold compiler
detected the clean-boundary pattern in both learn families and compiled:
- `[s0=1&s1>=2]->PROC_LEARN` + `[s0=1&s1<2]->WITHHOLD` (from H6,H7,H8,H9)
- `[s0=2&s1>=2]->CAUS_LEARN` + `[s0=2&s1<2]->WITHHOLD` (from H10,H11,H12,H13)
The boundary B=2 is data-determined; the preference for the minimal
consistent threshold over per-value memorization is the disclosed
researcher bias. The 8 consumed equality entries are marked COMPACTED in
the store (white-box audit trail); the compiled table has 7 rules
(4 threshold + 2 query + fallback). The induced policy no longer withholds
on nseg>=5: it routes per the threshold, agreeing with H-ROUTER on all 10
probes.

**X-R1 (curriculum gaming):** Three provenance mechanisms, all white-box:
1. **Mark-dependence manifest:** every compiled rule lists its supporting
   curriculum indices, e.g. `[s0=1&s1>=2]->PROC_LEARN from marks
   {#1,#2,#3,#4}`. Policy content is traceable to researcher marks.
2. **Replay audit:** 18/18 on both honest and gamed runs. The learner is
   a faithful compiler; it does not silently drop marks.
3. **Mark-merger diagnostic:** fires iff a learn/query mark is concluded
   from rules spanning multiple s0-families. Fires for CAUS_LEARN on the
   gamed run (constrained s0 values {1,2} plus unconstrained rules);
   silent on the honest run. This is a structural observation, not a
   correctness judgment the learner cannot make.
Plus the verbatim provenance statement: "POLICY PROVENANCE: every routing
decision is traceable to researcher-supplied marks; the learner contributes
rule structure (SPLIT) and threshold compilation, not policy content."

The induction itself is byte-for-byte the H-ROUTER2 induction (H0..H14,
identical split order and seq numbers), confirming the machinery was
untouched. On the gamed curriculum, no clean threshold exists
(mask patterns differ), so compilation degrades honestly to equality
routing and the merger diagnostic carries the X-R1 signal.

## Honest boundaries

1. The threshold preference is a researcher-supplied inductive bias, not a
   discovery. The data determines B=2; the bias chooses thresholds over
   memorization.
2. Threshold extrapolation to unobserved nseg values (5..9) is tested
   against H-ROUTER, not against ground-truth task outcomes. It is correct
   here; it is still extrapolation.
3. The merger diagnostic detects the structural signature of mark-merging,
   not mark incorrectness. A legitimately merged mark class (researcher
   intent) would fire it too; the diagnostic reports structure, and the
   researcher judges intent.
4. Features remain authored; marks remain supplied. The gamed run proves
   the learner still compiles whatever marks it is given.
5. Threshold compilation is currently scoped to the s1 (nseg) variable in
   s0-families {1,2} with the {W,M} two-task pattern. Generalizing the
   pattern detector is open work.

## Classification

Bounded L2+ structural learning with threshold vocabulary enrichment, over
supervised rule induction. The learner constructed threshold rules from
generic machinery plus a disclosed bias; the exact compiled policy did not
exist in source. NOT L3: features are authored, marks are supplied, the
threshold preference is researcher-chosen, and no new representation was
invented. The X-R1 downgrade's core point stands and is now explicit:
policy content is researcher-supplied; what the learner contributes is
rule structure, threshold compilation, and auditable provenance.

## Lineage

- H-ROUTER (authored predicates, SURVIVES): baseline; threshold probes now
  agree with it on nseg=5..9.
- H-ROUTER2 (DOWNGRADED by red team): induction layer retained verbatim;
  its false "matching authored decisions" claim outside curriculum range
  is repaired by the threshold compiler; its "learner discovers the
  policy" claim is re-scoped to supervised compilation with provenance.
- H-ROUTER3 supersedes H-ROUTER2 as the routing layer for unified-learner
  work.
- K-R2C is SUPERSEDED by K-R3-2 (preregistered behavior change).
