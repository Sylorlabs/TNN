# H6R sealed worlds (frozen before the evaluation run)

World parameters are frozen in h6r_checks.zag (committed before the run).
Concrete parameters:

- B1: singleton slot (501,51): teach + 3 confirms + 1 contradict + 2 confirms.
  Systematic slot (502,52): teach + 1 confirm + 1 contradict + 1 contradict.
- B2: slot (503,53): teach + 1 confirm + 5 query hits.
- B3: four worlds, 20 probes each (80 total).
  W1: guides (601,61) vs (602,62), truthful guide taught second, 10 queries.
  W2: one contradict then 4 confirms on (602,62).
  W3: 2 confirms + 3 contradicts on (602,62).
  W4: 3 confirms on (603,63), 2 confirms + 2 contradicts on (604,64).
  Probes: alternating (601,61)/(602,62) and (603,63)/(604,64)/(605,65).
  Ablation: tombstone -44 on all records, require 20/20 treatment/control
  agreement and lbid == bid white-box per probed node.
- B4: three retention worlds (pacemaker design, PREREG Amendment 1).
  R1: nH (701,71) 8 confirms; nF (702,72) 3 confirms + 12 queries; P (901,90).
  R2: nH (703,73) 5 confirms; nF (704,74) 2 confirms + 8 queries; P (902,90).
  R3: nH (705,75) 6 confirms; nF (706,76) 1 confirm + 16 queries; P (903,90).
  Interleave: [2 queries + 1 pacemaker confirm] rounds; lapse: 2x[10 ev_acts
  + 1 pacemaker confirm]; then real evict_node calls.

## Run log hashes (3 byte-identical reruns)

- h6r_run1.log: 01128d9af991d824595d127d963a35e9e283fa8b5bf47725197fd37497021bd7
- h6r_run2.log: 01128d9af991d824595d127d963a35e9e283fa8b5bf47725197fd37497021bd7
- h6r_run3.log: 01128d9af991d824595d127d963a35e9e283fa8b5bf47725197fd37497021bd7

## Results

- H6R-REGRESSION: PASS (46/46 substrate self-tests)
- B1: PASS. B2: PASS.
- B3: accT 50/80, accC 50/80, margin 0 points. Bar >= 15. KILL fires.
- B4: SUBSTRATE-INSUFFICIENT (first real eviction took nH's standing record,
  node 6, not nF; records are unprotected lbid-0 nodes).
- H6R-VERDICT: BUILD-FAIL
