# ROUTER2_ADV_RESULT: Adversary Report Against H-ROUTER2

**Target:** H-ROUTER2 SURVIVES (commit `313b840ed`)
**Adversary prereg:** `PREREG_ROUTER2_ADV.md` (commit `48ed09d9c`), frozen
before execution. No amendments.
**Date:** 2026-09-29
**Verdict: H-ROUTER2 DOWNGRADED.** Two of four attacks met kill criteria.
X-R4 (source audit) and X-R2 (boundary collisions) passed; X-R1 (curriculum
gaming) and X-R3 (threshold divergence) killed the broad claim.

## Attack results

### X-R1: Curriculum gaming -- KILL CRITERION MET (DOWNGRADE)

A variant curriculum marked all str>str multi-segment items (s0=1, s1 in
{2,3,4}) as CAUS_LEARN instead of PROC_LEARN, keeping everything else
identical and consistent. The learner:

- Accepted all 18 gamed episodes without any diagnostic, flag, or abstention.
- Induced s0=1 -> CAUS_LEARN rules via the same SPLIT machinery.
- Routed a novel str>str input (`zz>yy;xx>ww`) to CAUS_LEARN, faithful to
  the wrong marks and wrong per ground truth.
- Emitted nothing distinguishing this run from the honest run.

The routing "knowledge" is fully determined by researcher-supplied marks.
What the learner contributes is a white-box reformatting of supervised
decisions, not policy content. The H-ROUTER2 claim "the ROUTING POLICY
itself moved from researcher to learner" is false at the content level;
what moved is the representation (induced entries vs authored if-statements).

Raw: `ROUTER2_ADV_XR1_RAW.txt`

### X-R2: Feature-extractor boundary collisions -- PASS (claim survives)

Five boundary strings tested against the honest curriculum:

- `ab>ba>cd` (double `>`): feat=(3,1,0) -> WITHHOLD. Documented mixed class.
- `a1>b2` (alphanumeric): feat=(1,1,0) -> WITHHOLD. Consistent with
  curriculum single-pair withhold.
- `AB>BA;CD>DC` (uppercase): feat=(1,2,0) -> PROC_LEARN. Correct; uppercase
  is non-numeric per the documented extractor.
- `ab>ba;` (trailing separator): feat=(3,2,0) -> WITHHOLD. Empty segment
  triggers mixed class; honest.
- `a>b ` (trailing space): feat=(1,1,0) -> WITHHOLD. Consistent.

No boundary string produced undocumented features with confident misrouting.
The extractors behave as documented; the learner withholds where it should.

Raw: `ROUTER2_ADV_XR2_RAW.txt`

### X-R3: Threshold divergence from H-ROUTER -- KILL CRITERION MET (DOWNGRADE)

The H-ROUTER2 hypothesis states the induced predicates match "the authored
H-ROUTER decisions." H-ROUTER's authored predicate (`route_learn.zag` line
593) is `if(nseg>=2 && all_pair_str==1)` -- a threshold. H-ROUTER2 induces
per-value equality rules (s1=2, s1=3, s1=4 -> PROC_LEARN) and withholds
outside the curriculum range.

Six probes, all DIVERGE:

| input | nseg | H-ROUTER (authored) | H-ROUTER2 (induced) |
|---|---|---|---|
| `a>b;c>d;e>f;g>h;i>j` | 5 | PROC_LEARN | WITHHOLD |
| 6-seg str>str | 6 | PROC_LEARN | WITHHOLD |
| 7-seg str>str | 7 | PROC_LEARN | WITHHOLD |
| 8-seg str>str | 8 | PROC_LEARN | WITHHOLD |
| 9-seg str>str | 9 | PROC_LEARN | WITHHOLD |
| 5-seg iii>ii | 5 | CAUS_LEARN | WITHHOLD |

6/6 divergence. The hypothesis sentence is FALSE on this principled input
class. K-R2C required WITHHOLD on `(1,5,0)`, which means the prereg
redefined success away from H-ROUTER agreement -- the "match" was
stipulated, not achieved. The induced policy is a per-value approximation
that withholds outside the curriculum range; it does not recover the
threshold.

Raw: `ROUTER2_ADV_XR3_RAW.txt`

### X-R4: Source audit for hardcoded rules -- PASS (claim survives)

- Task-code literals (10-14) appear only in `TC_*()` definitions, display
  name mapping, bounds validation, and test expectations via `TC_*()` calls.
- No feature-to-task mapping exists outside the generic `predict()` path.
- `learned_route()` computes features, calls `predict()` on the SPLIT-induced
  hypothesis store, and returns the result. No conditional branches on
  feature values toward task codes.
- The 11 induced rules genuinely come from SPLIT machinery, not hardcoding.

## Revised classification

H-ROUTER2 SURVIVES in narrowed form:

**What stands:** Routing predicates are induced as white-box hypothesis
entries via the causal SPLIT machinery (X-R4). The induction is
deterministic, inspectable, and handles documented feature boundaries
honestly (X-R2). Within the curriculum feature range, 16/16 routing matches.

**What falls:**
1. (X-R1) The policy CONTENT is researcher-supplied via marks. The learner
   is a faithful supervised compiler of mark-to-rule mappings, not a
   discoverer of routing policy. "Learned routing" means "induced
   representation of taught decisions."
2. (X-R3) The induced policy does NOT match H-ROUTER's authored decisions
   outside the curriculum range. The threshold (`nseg>=2`) is not recovered;
   the learner withholds where H-ROUTER routes. The hypothesis claim of
   matching is false for nseg>=5.

**New classification:** Bounded L2 supervised rule induction (narrowed).
The learner compiles consistently-marked curricula into inspectable
equality-based routing entries via generic SPLIT machinery. It does not
invent routing policy content (marks supply it) and does not generalize
thresholds beyond the curriculum (equality vocabulary limitation, now with
a demonstrated divergence rather than just a predicted boundary).

## Governance notes

- Adversary used Python once for a single text replacement in a harness
  file (not in the experimental pipeline, not in verification). Disclosed
  per the pure-Zag rule; no experimental result depends on it.
- Attack harnesses were built by copying `router2_learn.zag` verbatim and
  replacing only `main()`; the causal machinery under test was unmodified.
- `router2_learn.zag` itself was not modified by the adversary.
- Binaries were not committed (per existing convention).

## Commits

- Prereg: `48ed09d9c` (frozen before execution)
- This report + raw evidence: (this commit)
