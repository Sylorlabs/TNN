# ACT Coverage Assessment: TNN-1's 6-test battery vs the standalone 24/24 suite

Date: 2026-09-30. Worker: ACT Coverage Scout. Read-only analysis.

## 1. What the prereg required

Integration prereg (`7fc7148ac`), P-INT2:

> the integrated binary passes ACT's 24/24 tests (P-ACT1 planning,
> P-ACT2 inquiry, P-ACT3 null policy, P-ACT4 ablation, P-ACT5
> generality, P-ACT6 memory prerequisite), all in one process, with
> the directional bid. No test changes from the aligned ACT.

K4 references P-INT2 as (24/24). The prereg's own words forbid test
changes.

## 2. What the standalone suite actually contains

`act_build/act.zag` (614 lines), run as `./act_bin all`. Output is
24 lines containing "PASS": 23 individual `ptest` checks plus the
`ALL-PASS` banner. The TNN-1 red team and the compression tracker both
use the "24/24" label; the substantive count is 23 distinct checks,
of which 16 are unique (P-ACT5 re-runs P-ACT1 and P-ACT2 through the
same handler).

The 16 unique checks:

| # | Check | What it proves |
|---|-------|----------------|
| 1 | P-ACT3 null-root -> 0 | null POLICY_ROOT yields CHOICE 0 |
| 2 | P-ACT1 s1 -> 10 | planning: state-varying action |
| 3 | P-ACT1 s2 -> 11 | planning: state-varying action |
| 4 | P-ACT1 s3 -> 10 | planning: state-varying action |
| 5 | P-ACT1 3 guides | D1 backward-chain derivation produced all guides |
| 6 | P-ACT2 uncert -> 20 | uncertainty-anchored guide fires the inquiry action |
| 7 | P-ACT2 decoy -> 21 | decoy context fires its own action, no bleed into 20 |
| 8 | P-ACT2 other -> 0 | unrelated context fires nothing |
| 9 | P-ACT4 pre s1 -> 10 | sanity: works before ablation |
| 10 | P-ACT4 no-guides -> 0 | deleting guides degrades to 0 |
| 11 | P-ACT4 no-goal -> 0 | dead policy root: refuse, do not hallucinate |
| 12 | P-ACT4 fact-alive | recall intact after ablation |
| 13 | P-ACT5 one-handler-both-classes | identical act_event serves W6 and W7 classes |
| 14 | P-ACT6A pre s1 -> 10 | sanity: works before pressure |
| 15 | P-ACT6A post -> 0 | unevidenced guides evicted under pressure |
| 16 | P-ACT6B post s1 -> 10 | evidenced guides survive the same pressure |

Note: the standalone P-ACT6 used a test stand-in eviction (lowest
signed bid), not the CLA-2 three-step routine; the RESULTS.md says so
explicitly. TNN-1 has the real 3-step eviction with directional signed
bids, so a ported P-ACT6A would test the real mechanism.

## 3. What TNN-1's battery contains

`tnn1_build/tnn1.zag`, lines 865-912, six tests (t_a1..t_a6), each a
single check, all against `ev_act` on a fresh 110656-byte workspace.
Edge types in TNN-1: ET_DEP=1, ET_SUP=2, ET_CON=3, ET_USE=6, ET_CFM=7,
ET_MEM=10. Bid = count(1)+count(2)+count(6)+count(7) - count(3), plus
ET_MEM-linked node contributions.

| Test | Setup | Check | Standalone analogue |
|------|-------|-------|---------------------|
| t_a1 | two guides under one policy; g1 has one ET_SUP self-edge, g2 has two; ctx 101 | ev_act == 11 (higher-bid guide wins) | none directly; new bid-competition check |
| t_a2 | T_UNCERT node (type 30) linked ET_MEM to guide gd (action 20, payload 202); ctx 202 | ev_act == 20 | P-ACT2 check 6 (uncert -> 20) |
| t_a3 | pol_set(-1) | ev_act == 0 | P-ACT3 check 1 (null-root -> 0) |
| t_a4 | policy root with no guides; ctx 303 | ev_act == 0 | P-ACT4 check 10 (no-guides -> 0) |
| t_a5 | guide with ET_USE self-edge (payload 404, action 30); ctx 404 | ev_act == 30 | none directly; basic evidenced-guide emission |
| t_a6 | 60 facts taught; last 10 given ET_USE+ET_CFM self-edges; all 10 queried | all 10 retrieved | P-ACT6B check 16, weakened (no capacity pressure) |

## 4. Coverage map

| Standalone check | TNN-1 coverage | Status |
|---|---|---|
| 1. null-root -> 0 | t_a3 | COVERED |
| 2-4. s1->10, s2->11, s3->10 (state-varying emission) | none | NOT COVERED |
| 5. D1 derives 3 guides | none | NOT COVERED |
| 6. uncert -> 20 | t_a2 | COVERED |
| 7. decoy -> 21 | none | NOT COVERED |
| 8. other -> 0 | none | NOT COVERED |
| 9. ablation sanity pre | none (t_a4 is post-only) | NOT COVERED |
| 10. no-guides -> 0 | t_a4 | COVERED |
| 11. no-goal -> 0 (no hallucination) | none | NOT COVERED |
| 12. fact-alive (recall intact) | none | NOT COVERED |
| 13. one-handler-both-classes | implied (t_a1 planning-flavored and t_a2 inquiry-flavored both run through ev_act) but never asserted | WEAK |
| 14-15. P-ACT6A (unevidenced evicted under pressure) | none | NOT COVERED |
| 16. P-ACT6B (evidenced survives) | t_a6, without any pressure | PARTIAL |

Tally: 3 of 16 fully covered, 1 partial, 1 weak, 11 not covered.

t_a1 (bid competition) and t_a5 (evidenced guide fires) are genuine
new checks with no standalone counterpart. They add value but do not
substitute for the missing ones.

## 5. Do the uncovered tests matter?

Yes, for the specific claims TNN-1 inherits from ACT:

- **P-ACT1 (checks 2-5): the planning claim.** The standalone result
  reads "ACT emits 10/11/10 by state. The constant-0 baseline would
  score 0/4 here." TNN-1 tests bid competition between two guides
  (t_a1) but never state-varying emission and never guide derivation.
  The claim that integrated ACT does planning work is untested in
  TNN-1.
- **P-ACT2 decoy/other (checks 7-8): the no-bleed claim.** t_a2
  checks the positive case only. Without the decoy and unrelated
  checks, a sloppy matcher that fires 20 on any live context would
  pass.
- **P-ACT4 no-goal and fact-alive (checks 11-12): the honesty
  claims.** "No hallucination without a live policy root" and
  "recall survives ablation" are the two properties that separate
  structure-driven action from handler magic. Neither is tested in
  TNN-1.
- **P-ACT6A (checks 14-15): the retention claim's negative half.**
  Directional signed bids are supposed to evict the unevidenced.
  t_a6 tests only the positive half (evidenced nodes retrievable,
  with no pressure applied). The eviction direction is untested.

## 6. Recommendation

**Port the full 24/24 into TNN-1, per the prereg's "no test changes"
requirement.** The tests already exist in the aligned ACT; the port
maps the standalone scaffolding (mk_goal, mk_guide, derive_d1,
evict_to_cap) onto TNN-1's conventions and runs them against
`ev_act` in the shared workspace. This is builder work, not scout
work, and it should be preregistered as a remediation wave because
the prereg forbade test changes and the compact battery is a
deviation from P-INT2/K4 as written.

Reasons the full port beats the targeted subset:

1. The prereg is explicit: "No test changes from the aligned ACT"
   and K4 says P-INT2 (24/24). A subset keeps the deviation open.
2. Ported P-ACT6A would exercise TNN-1's real 3-step directional
   eviction, which the standalone could not test (it used a
   stand-in). The port is strictly more informative than the
   original for the retention claim.
3. The marginal cost is low: the scenarios are already designed;
   only the scaffolding mapping is new.

If a full port is deferred, the minimum honest subset is: P-ACT1
checks 2-5 (planning), P-ACT2 checks 7-8 (no-bleed), P-ACT4 checks
11-12 (no-hallucination, recall), P-ACT6A checks 14-15 (eviction
negative half). Without at least these, TNN-1's action-selection
claims rest on 3 of 16 checks and the K4 P-INT2 (24/24) line should
be read as not literally satisfied.

## Verdict: ACT-COVERAGE-ASSESSED.
