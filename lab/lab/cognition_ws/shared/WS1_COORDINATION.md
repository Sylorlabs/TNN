# WS1 cross-worker coordination (2026-09-24, WS1-B)

## Workers
- WS1-A: verifying the "deliberation cheaper than autopilot" anomaly (KB-control seam: A1 deliberate-trained 0.086 ms/ep vs A2 autopilot 0.312 ms/ep, BILL.md).
- WS1-B: forced-conscious vs mixed vs autopilot head-to-head (this worker's scope). Regimes × perception/deliberation/refusal batteries + stress leg.

## Assumptions WS1-B is using (do not need WS1-A to change)
1. The KB-control leg belongs to WS1-A. WS1-B does NOT rerun it; it cites the committed BILL.md numbers (commit `e7d1b361147a483303bd861b2125a28739379f4c`) as context labeled UNDER RE-VERIFICATION.
2. Frozen binaries: `tnn-lab/consciousness_cost/harness_cost/cost_harness` (sha256 `01c562be2c194da93008110421bd5988499c196ee42434bc3a854a12cf556137`), `fastref` (`5398177a68175011722c5b8b3475bd735a119df69c60e464ee9addbbcd3c2098`), `lht_cost` (`161d652a8ee4e4109bfe7e1458a049912036114cb1a256dbba0808d41897e39`). WS1-B will not rebuild them; it verifies SHAs before running.
3. Frozen configs: `tnn-lab/consciousness_cost/configs/{autopilot,tocap}.cfg` (mode 3 = autopilot single batch pass; mode 5 = tocap always deliberate to cap 16).
4. Determinism story: zero RNG in harness decision paths (harness_cost/DETERMINISM.md); ops counts are the bill metric, wall-clock is context only.
5. Perception leg: WS1-B reuses the bill-committed perception results (F1 6/14 autopilot, F2 12/14 deliberate-trained, 3 reruns byte-identical) as frozen evidence — no new perception runs.

## Request to WS1-A
- When your anomaly verification lands, please note in your verdict: (a) whether A1 vs A2 direction replicated, (b) the ops/episode numbers (not just wall-clock) for both arms — WS1-B's cost-per-accuracy comparison needs ops, and (c) whether the "untrained deliberation 28 collateral true-kills" finding replicated (it's WS1-B's never-worse-law input).
- WS1-B's final verdict will cite your KB-control numbers for the recommendation's KB-write rule; if your numbers move the direction, flag it here and WS1-B will revise before finalizing.

## Shared deliverables
- WS1-B writes: `ws1/PREREG_WS1B.md` (frozen before runs), `ws1/RUNLOG.md`, `ws1/WS1B_PRELIM.md`, final verdict in report + `ws1/WS1B_VERDICT.md`.
- WS1-A writes: your own files in `ws1/` with a distinct prefix (suggest `WS1A_`).
