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

---

# WS1-A RUNLOG — KB-control anomaly: deliberate vs autopilot cost (Micah's "consciousness bill" leg)

## 2026-09-24 ~08:10 PDT — prereg frozen before any new run
- Wrote and committed `docs/lab/cognition_ws/ws1/PREREG_WS1A.md` BEFORE any fresh run: commit `403906826516f3c76c0a26ff1b60e94a094370d9` (tnn-native-lab).
- Frozen battery: 18 cells (cap 32/128/512 × adv 0/15/35% × rep 1/3) × 3 arms (deliberate-trained, deliberate-untrained, silent autopilot) × 3 reruns = 162 executions.
- Fresh deterministic generator (seed S=7, new truth functions, A/B/C/D phases); primary metric W = find_steps + scan_steps + mutops (+ suppressions). Wall-clock secondary (VM noise).
- Confirm bar: median W(auto)/W(trained) >= 1.5 overall; >= 2.0 in >=75% of adversarial/large cells; accuracy gate trained vs auto <= 0.05; byte-identical reruns; >=70% of gap mechanically assigned to scans/overwrite churn.

## 2026-09-24 ~15:20 PDT — sources built, battery launched
- New sources in `src/`: w1a_gen.zag (fresh generator), w1a_time.zag (CLOCK_MONOTONIC ns), w1a_memory_core.zag (MA copy, MA_CAP=512, MA_AUDIT_CAP=16384, only size consts changed), w1a_common.zag (shared harness + W1C counters), w1a_arm1.zag (trained policy verbatim + counters), w1a_arm3.zag (naive policy verbatim + counters), w1a_psm.zag (psm mode=0 verbatim + c_age/c_find/c_scan/c_overwrite/c_evict counters), w1a_auto.zag (autopilot driver + probe).
- Build: pinned znc `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`, `--no-zagd --no-analyze --no-foreground-cache`. Three binaries in `build/` (scratch, never committed).

## 2026-09-24 ~16:00 PDT — battery complete, VERDICT: CONFIRMED
- 162/162 runs rc=0. Rerun byte-identity: 54/54 cell-arms identical modulo wall_ns measurement lines (wall is VM-noisy by design); in-driver digest match=1 on all 162.
- Median W(auto)/W(trained) = 2.73 (18/18 cells >= 2.0; range 2.48–2.97). Adversarial+large subregime: 8/8 >= 2.0 (median 2.67). Accuracy: trained and auto both 1.0000 on all 18 cells (0 gate failures). Scans assign 103.4% of the aggregate W gap (overwrite=0, evict=0 on all cells — last-wins/eviction never fired; gap is scan-driven, not churn-driven).
- W/ep: trained 9.5–178.4, auto 27.3–459.7 across regimes. Memory: trained/naive 667,648 B fixed arenas; auto 66,752–84,992 B fixed (~8–10x smaller, 2.5–3x costlier work). Zero per-episode allocation all arms.
- Naive (untrained): collateral true-kills 0 benign → 681 on cap512a35r3 (phenomenon replicates; exact 28 was generator-specific). Naive slightly cheaper on raw W (0.91–1.00x trained) — savings paid in collateral damage. Training is load-bearing.
- Conditions map: no flip anywhere tested; ratio narrows slightly with adversarial pressure (2.88→2.58 at cap512) but never approaches 1.0.
- Honesty notes: (1) cost advantage only on this battery — no accuracy gap demonstrated; (2) W ratios are conservative lower bounds (auto's counted steps cost more wall/step); (3) wall-clock too noisy for precise mapping.
- Verdict doc: WS1A_VERDICT.md. Evidence commit: (pending — this commit).
