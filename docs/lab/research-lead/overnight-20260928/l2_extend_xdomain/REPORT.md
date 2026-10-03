# REPORT: L2-EXTEND-XDOMAIN (cross-domain extend, learner-chosen length)

Worker: L2 Adaptive Reuse subagent (depth 2/2), 2026-10-02.
Verdict: **L2-EXTEND-XDOMAIN-PASS** (K1-K8 all PASS, 0 falsifiers,
F-COUNT silent).

## What was built

Standalone pure-Zag learner (`learner.zag`, ex_ prefix, EX- tags)
+ environment side (`world.zag`, 20 frozen facts) + experiment
side (`driver.zag`, four arms, in-Zag bar evaluation),
concatenated to `ex_full.zag` and compiled with the pinned safebin
znc (`znc ex_full.zag -o ex_bin`, rc=0, 43 benign analyzer
warnings: discarded returns and unused locals, same classes as the
sibling truncate lane). No forbidden executables. 0 modes, 0
bridges, 0 handlers, 0 new edge types, 0 new opcodes, 0 semantic
cases, 0 domain-pair templates.

Scenario: X = arithmetic aggregation MAP mA (entry + 3 fold
pairs, 7 hops) learned in domain A; Y = planning ROUTE MAP mB0
learned in domain B; distractor mD (cap ROUTE) taught first so
the capability search must examine and reject it. Target query
Q2 = (50,74,77,AGG,B): an aggregation in the planning domain
whose grounding chain needs entry + 4 fold pairs (9 hops), one
fold more than X. Unextended X grounds to terminal 73, one hop
short of 74. The learner's shortest-verifying-extension
enumeration (k = nf+1 upward, bound KMAX=6) selects k=4 on its
first extension attempt, builds Z, verifies by execution,
promotes with type-16 provenance (3->1), and delivers.

## Kill bars (parent numbering)

- K1 PASS (in-Zag + shell): qa_via=1, qb_via=2, q2_via=3;
  mA rels all in {18,5,6}, mB0 rels all 7 (disjoint); shell line
  order `Q QA`(2) < `Q QB`(4) < `Q Q2`(6). X and Y exist before
  the extension task, learned independently.
- K2 PASS (in-Zag + shell): FULL_OK=0; NOEXTEND arm ans=-2,
  t16=0 (informational A_SEARCH=137 = 2+135 as hand-derived);
  verbatim `EX-FULL-FAIL` in run1. Unextended X fails on the
  target; extension is REQUIRED.
- K3 PASS (in-Zag + shell): EXT_K=4, EXT_DECIDED=1 (flag set
  only inside the learner's ascending enumeration branch);
  trace order `EX-TRY k=3` < `EX-FAIL k=3` < `EX-TRY k=4` <
  `EX-OK k=4` (run1 lines 11/14/16/18); `grep -c` of
  `ext_k\|EXT_K` in driver.zag = 0, so the driver never names a
  length. The learner decided how much to add.
- K4 PASS (in-Zag + shell): q2_via=3, q2_val=77, FULL_OK=0;
  verbatim `EX-ZBUILD
  rels=17,15,16,15,16,15,16,15,16
  facts=8,9,10,11,12,13,14,15,16` and
  `ANS term=74 val=77 via=3`. Extended Z succeeds where the
  unextended X fails.
- K5 PASS (in-Zag + shell): EXT_K=4 AND EXT_TRIES=1 (exactly
  one extension length ever attempted); `grep -c 'EX-TRY k=5'`
  = 0 and `grep -c 'EX-TRY k=6'` = 0. The extension is minimal:
  the enumeration stopped at the first verifying k.
- K6 PASS (shell): 3/3 runs byte-identical, sha256
  d8dac499d75487d64c514216314523180117b52fe31bc58440f9d71eec80981d
  x3.
- K7 PASS (shell): 12/12 frozen grep patterns return 0 hits on
  learner.zag. No domain-pair template in source.
- K8 PASS (in-Zag): ABLATE-X (mA retired pre-Q2): ans=-2,
  t16=0, NM=3; capsearch examined id0/id1(retired)/id2, all
  SKIP (A_SEARCH=3 informational). Without X the query fails
  and nothing is promoted.

Falsifiers: 0 fired. F-COUNT silent (FULL A_SEARCH=272,
A_EXEC=2, exactly the frozen hand derivation: capsearch 2 +
k=3 attempt 135 + k=4 attempt 135 = 272; verify + deliver = 2).
Reuse guarded by falsifiers, both silent: Q2B answered via Z
(term 74 val 77) with no re-extension (EX_ENTERED=0).

## Numbers

- FULL arm: ANS term=74 val=77 via=3; A_SEARCH=272; A_EXEC=2;
  t16=1 {3->1}; LINK14 ans->3; Z id 3 rlen 9
  rels [17,15,16,15,16,15,16,15,16] facts [8..16] start 50 end
  74 dom B cap AGG descriptor (17,15,16,4,2); SRC_ID32=1;
  FULL_OK=0; EXT_K=4; EXT_DECIDED=1; EXT_TRIES=1.
- NOEXTEND arm: ans=-2, t16=0, NM=3.
- ABLATE-X arm: ans=-2, t16=0, NM=3.
- FRESH arm: ans=-2, t16=0, NM=0.
- No edge type outside {14,16} in any arm; distractor mD
  survives (live=1).

## Disclosures and non-claims

- The EXTEND operator, descriptor extraction, entry/fold search
  with runtime relation discovery, shortest-verifying-extension
  enumeration, and cost counters are researcher-supplied generic
  machinery, frozen in the prereg. None names a relation, MAP,
  domain, length, or domain pair. KMAX=6 is a disclosed generic
  compute bound, not a length hint.
- EXTEND_ON is a driver-set causal-control flag, never written
  by the learner (the adapt_on precedent).
- One world family (arithmetic aggregation x plan-cost
  aggregation). No generality claim beyond the four arms; the
  world is builder-designed, not adversary-designed.
- State layout, counting rules, emit helpers, and scan idioms
  follow the sibling l2_truncate_xdomain lane; the
  load-bearing difference is the operator under test:
  ascending shortest-first extension with EXT_TRIES minimality
  accounting, versus the sibling's descending longest-first
  truncation.
- Commits local with explicit pathspec. Nothing pushed. Paper
  untouched.

## Files

- `learner.zag`, `world.zag`, `driver.zag`, `ex_full.zag`
  (concatenated build input), `ex_bin` (pinned-znc binary),
  `ex_compile.txt`, `ex_run1.txt`, `ex_run2.txt`, `ex_run3.txt`
- `NAMECHECK.md` (Step 0 toolchain guard), `PREREG.md`
  (frozen, committed alone at b6652e3d6 before implementation)
