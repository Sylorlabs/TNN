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

## 2026-09-24 ~08:25 PDT — matrix launched
- Prereg committed: `5e24c6e2e654b2529188c1aae4603f3f23906afa` (tnn-native-lab).
- Stress battery generated: batteries/trap_x10.jsonl (1270 lines, 10 passes, content verified: strip _pK restores original 127 lines).
- Smoke test: cost_harness tocap on rt_d1 → rc=0, 14/14 ok. NOTE: RT-POISON-01 already wrong at conf=1000 (confident-wrong) — never-worse watch-list item live.
- run_ws1b.py launched in background (48 cells): D=30, RT=6, RF=6, S=6.

## 2026-09-24 ~08:45 PDT — matrix complete, analysis done
- 48 cells, all rc=0, err=0. Gates: G1 0/16, G2 0/16, G3 0/10. Analyzer bug found and fixed (G1 false alarms — data was fine).
- Headline: FORCED wins refusal (+26.7pp) and perception (+42.9pp, bill); ties 5 deliberation batteries at 10–30× the ops; AUTO wins rtd1 (+35.7pp) — NEVER-WORSE VIOLATION (H5 law), forced confident-wrong (conf=1000) on 10/14.
- Stress: FLAT both regimes (no compounding). Memory: not a differentiator. Bill is compute.
- Recommendation: CONDITIONAL — trust-profile router (4 rules), not modality. Details in WS1B_VERDICT.md.
- Raw runs/ = 35 MB — NOT committed (too large); manifest SHAs + byte-identical reruns preserve verifiability.

## Commits
- 5e24c6e2 prereg + coordination note + RUNLOG (tnn-native-lab)
- (pending) scripts + analysis + prelim + verdict + RUNLOG update

## 2026-09-24 ~08:50 PDT — coordination + close
- WS1-A active in shared workdir (PREREG_WS1A.md frozen 08:10 PDT): KB-control anomaly verification on FRESH batteries (cap x adv x rep, 18 cells), arms D1/D3/A2. No leg overlap with WS1-B. Their D3 arm covers the untrained-deliberation re-verification requested in WS1_COORDINATION.md.
- Final commit: 77eedd0757faf5b31ebbdf7cb0972b0ba88b7ac8 (tnn-native-lab).
