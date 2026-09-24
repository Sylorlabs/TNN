# WS1-B RUNLOG — forced-conscious vs mixed vs autopilot head-to-head

## 2026-09-24 ~08:20 PDT — setup
- Read prior work: consciousness_cost/ (COST_NOTES.md, analysis.txt full matrix), deliberation_depth/ (depth1_discipline VERDICT.md), BILL.md + 4 frozen preregs (commit e7d1b361).
- WS1-A interim notes: none yet (ws1/ empty at start). Wrote shared/WS1_COORDINATION.md with assumptions + request; WS1-B does NOT rerun the KB-control anomaly leg.
- Wrote PREREG_WS1B.md (frozen regime definitions, 69-cell matrix, gates G1/G2/G3, bars ACC/OPS/LED/MEM/CPA/NW/ST-FLAT, frozen decision rule).
- Verified frozen binaries (SHA256 before runs):
  - cost_harness: 01c562be2c194da93008110421bd5988499c196ee42434bc3a854a12cf556137  MATCH
  - fastref:     5398177a68175011722c5b8b3475bd735a119df69c60e464ee9addbbcd3c2098  MATCH
  - lht_cost:    161d652a8ee4e4109bfe7e1458a049912036114cb1a256dbba0808d41897e39  MATCH
- Determinism: zero RNG in harness decision paths (harness_cost/DETERMINISM.md); ops are the bill metric, wall-clock context only.

## Commits
- (pending) prereg + coordination note → tnn-native-lab
