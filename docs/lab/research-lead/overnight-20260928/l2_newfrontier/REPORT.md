# REPORT: L2-COMBINE-XDOMAIN (cross-domain combine, learner-chosen binding)

Worker: L2-NEWFRONTIER subagent (depth 2/2), 2026-10-02.
Verdict: **L2-COMBINE-XDOMAIN-PASS** (K1-K8 all PASS, 0 falsifiers,
F-COUNT silent).

## What was built

Standalone pure-Zag learner (`learner.zag`, cb_ prefix, CB- tags)
+ environment side (`world.zag`, 18 frozen facts) + experiment
side (`driver.zag`, five arms, in-Zag bar evaluation),
concatenated to `cb_full.zag` and compiled with the pinned safebin
znc (`znc cb_full.zag -o cb_bin`, rc=0, 43 benign analyzer
warnings: discarded returns and unused locals, same classes as the
sibling extend lane). No forbidden executables. 0 modes, 0
bridges, 0 handlers, 0 new edge types, 0 new opcodes, 0 semantic
cases, 0 domain-pair templates.

Scenario: X = arithmetic aggregation MAP mA (entry + 3 fold
pairs, 7 hops) learned in domain A; Y = planning ROUTE MAP mB0
learned in domain B; distractor mD (cap ROUTE, rel pattern [6])
taught first. Target query Q2 = (90,86,42,AGG,B): an aggregation
in the planning domain whose grounding chain is a ROUTE segment
(90->91->92) followed by a FOLD segment (92->86, entry + 3 fold
pairs, VAL 42). Neither X alone (no rel-18 fact from 90) nor Y
alone (reaches 92, not 86) grounds it. The learner's fixed
(partner-source, binding) enumeration tries (mD,b=1) FAIL,
(mD,b=2) FAIL, (mB0,b=1) FAIL, then (mB0,b=2) VERIFY-OK: the
partner-head rel-[7,7] walk reaches 92 and the AGG-tail
(entry + 3 folds, rels discovered at runtime as 17/15/16)
reaches 86 with VAL 42. Z is built as head facts+rels followed
by tail facts+rels, verified by execution, promoted with
type-16 provenance to BOTH sources (3->1, 3->2), and delivered.

## Kill bars (parent numbering)

- K1 PASS (in-Zag + shell): qa_via=1, qb_via=2, q2_via=3;
  mA rels all in {18,5,6}, mB0 rels all 7 (disjoint); shell line
  order `Q QA`(2) < `Q QB`(4) < `Q Q2`(6). X and Y exist before
  the combination task, learned independently.
- K2 PASS (in-Zag + shell): PIPE_HIT=0; NOCOMBINE arm ans=-2,
  t16=0 (informational A_SEARCH=5 = 2+3 as hand-derived);
  verbatim `CB-PIPELINE-FAIL` in run1 (5 occurrences, one per
  arm). No single structure solves Q2; combination is REQUIRED.
- K3 PASS (in-Zag + shell): AGG_SRC=1, ROUTE_SRC=2, BINDING=2,
  BIND_TRIES=4, BIND_DECIDED=1 (flag set only inside the
  learner's verifying-enumeration branch); trace order
  `CB-SRC-ROUTE id=0`(15) < `CB-BIND b=1 FAIL`(17) <
  `CB-BIND b=2 FAIL`(18) < `CB-SRC-ROUTE id=2`(19) <
  `CB-BIND b=1 FAIL`(21) < `CB-BIND b=2 OK`(24); `grep -c` of
  `AGG_SRC\|ROUTE_SRC\|BINDING\|BIND_DECIDED\|BIND_TRIES` in
  driver.zag = 0, so the driver never names a source or a
  binding. The learner decided the source pair and the binding
  by execution verification.
- K4 PASS (in-Zag + shell): q2_via=3, q2_val=42, PIPE_HIT=0;
  verbatim `CB-ZBUILD
  rels=7,7,17,15,16,15,16,15,16
  facts=8,9,10,11,12,13,14,15,16` and
  `ANS term=86 val=42 via=3`. Combined Z succeeds where each
  source alone fails.
- K5 PASS (in-Zag): ABLATE-A (mA retired pre-Q2): ans=-2,
  t16=0, NM=3 (no AGG source; CB-NO-SRC); ABLATE-B (mB0 retired
  pre-Q2): ans=-2, t16=0, NM=3 (partner=[mD] only: both
  bindings fail verification; informational A_SEARCH=71 =
  2+3+48+18 as hand-derived). Both sources are necessary: the
  distractor mD cannot substitute for mB0.
- K6 PASS (shell): 3/3 runs byte-identical, sha256
  a19c97d0964b04700cfd2b96b45ecb8e1989309321a54fe773e55abcc4f6a144
  x3.
- K7 PASS (shell): 11/11 frozen grep patterns return 0 hits on
  learner.zag. No domain-pair template in source.
- K8 PASS (in-Zag): t16=2, e_has(3,1,16)=1, e_has(3,2,16)=1.
  Z carries dual derived-from provenance: the white-box proof
  that TWO old structures were combined.

Falsifiers: 0 fired. F-COUNT silent (FULL A_SEARCH=254,
A_EXEC=2, exactly the frozen hand derivation: AGG search 2 +
partner collection 3 + (48+18+48+135) enumeration = 254;
verify + deliver = 2). Reuse guarded by falsifiers, all
silent: Q2B answered via Z (term 86 val 42) with no
re-combination (CB_ENTERED=0).

## Numbers

- FULL arm: ANS term=86 val=42 via=3; A_SEARCH=254; A_EXEC=2;
  t16=2 {3->1, 3->2}; LINK14 ans->3; Z id 3 rlen 9
  rels [7,7,17,15,16,15,16,15,16] facts [8..16] start 90 end
  86 dom B cap AGG descriptor (0,0,0,0,2); AGG_SRC=1;
  ROUTE_SRC=2; BINDING=2; BIND_DECIDED=1; BIND_TRIES=4;
  PIPE_HIT=0.
- NOCOMBINE arm: ans=-2, t16=0, NM=3.
- ABLATE-A arm: ans=-2, t16=0, NM=3.
- ABLATE-B arm: ans=-2, t16=0, NM=3.
- FRESH arm: ans=-2, t16=0, NM=0.
- No edge type outside {14,16} in any arm; distractor mD
  survives (live=1).

## Disclosures and non-claims

- The COMBINE operator, descriptor extraction, entry/fold
  search with runtime relation discovery, strict
  partner-segment walk, first-verifying-combination
  enumeration, and cost counters are researcher-supplied
  generic machinery, frozen in the prereg. None names a
  relation, MAP, domain, source pair, binding, or domain pair.
  The partner capability is the first distinct live non-query
  cap met in MAP-id order (no capability literal in the
  learner). The enumeration order (query-capability-led
  binding first, partner sources in id order) is fixed generic
  policy; which combination verifies is decided at runtime by
  execution, as the ABLATE-B arm demonstrates (same order,
  nothing verifies).
- COMBINE_ON is a driver-set causal-control flag, never written
  by the learner (the adapt_on precedent).
- One world family (arithmetic aggregation x plan-route +
  plan-cost aggregation). No generality claim beyond the five
  arms; the world is builder-designed, not adversary-designed.
- This wave does not integrate a composition engine into the
  protected core or any continuing learner; like the L2 matrix
  waves it tests a learner-mechanism claim in a standalone
  harness. Whether one general composition operation subsumes
  the H1/H2/A/B/C mechanisms remains an open comparative
  question, not decided here.
- State layout, counting rules, emit helpers, and scan idioms
  follow the sibling l2_extend_xdomain lane; the load-bearing
  difference is the operator under test: combining two
  structures with a learner-chosen (partner-source, binding)
  pair and dual type-16 provenance, versus the sibling's
  single-structure extension.
- Commits local with explicit pathspec. Nothing pushed. Paper
  untouched.

## Files

- `learner.zag`, `world.zag`, `driver.zag`, `cb_full.zag`
  (concatenated build input), `cb_bin` (pinned-znc binary),
  `cb_compile.txt`, `cb_run1.txt`, `cb_run2.txt`, `cb_run3.txt`
- `NAMECHECK.md` (Step 0 toolchain guard), `PREREG.md`
  (frozen, committed alone at 28c5aa169 before implementation)
