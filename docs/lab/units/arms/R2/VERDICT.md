# R2 — Compounding-Elimination Cuts | CUT — Verdict

**Arm:** R2 (family CUT). **Round:** r1, **scale:** 1x.
**Mechanism:** Candidate boundaries proposed cheaply (every 64B boundary, zero
lookup), eliminated by compounding evidence (8B-pair FNV-1a recurrence check,
online left-to-right running counts; accept iff count≥1).
**Kill (frozen):** (a) M1 verified-boundary recall on held-out probes does not
beat arm R by ≥3 points; OR (b) proposals-per-accepted-cut does not fall over
the corpus.

## Evidence basis (all fresh, this crew)

- Binary rebuilt by this crew from `cl/arm.zag` with the frozen toolchain
  (`znc_linux_x86_64_abed8aa1`); compiles clean, warnings only.
- Full 1× battery rerun FRESH by this crew into `work/battery_r2/` (inherited
  partial outputs discarded as evidence): **18/18 legs passed** — every leg
  ran twice, `rc1=0 rc2=0`, stdout byte-IDENTICAL, `fatal=0` on all 17
  metric legs.
- **M8 gate PASS:** 5 perturbations (clean/frag/aslr/starve/freelist) × 2
  reruns, all rc=0; `store_hashes.txt`, `store_chain.txt`, `ledger.bin`,
  `ledger_chain.txt`, `alloc_trace.txt` byte-identical across all ten runs.
- Zero RNG in any decision path (source-audited: no rand/getrandom/clock use;
  starve-leg runs under a shim that breaks entropy/clock and still passes).
- Scorecard: `work/battery_r2/scorecard_r2_1x.json` (assembled by
  `work/scorecard_assemble_r2.py`).

## Metric results

| Metric | Result |
|---|---|
| M1 | prose: recall 100.0, boundary 100.0, 11,871 units; code: recall 100.0, boundary 100.0, 53,105 units; ID probe PASS; A15 swap 63/63 ok |
| M2 | ETC=1 everywhere (t1/t2 prose+code, t3); ep0 recall 0.0 → final 100.0/100.0, uncensored |
| M9 | fast-then-flat, takeoff ep 1 |
| M3 | survival 100.0, fresh recall 100.0, 7,050 mgmt entries, weaken 50/50 handled → freeze CLEAR |
| M4 | prose+code: boundary rev 100.0, content rev 100.0, 1 episode, kill-substitution false |
| M5 | 0.844 mem/src-byte (bar 1.5× PASS); audit 2.43 entries/KB (bar 10/KB PASS) |
| M6 | p2c + c2p: recall/boundary/revision 100.0, tax 0.0; memorizer validity gate PASS (drop 54.8 ≥ 15 pts) |
| M7 (ID arm) | hit 100.0 (bar 90 PASS), **reuse 1.36 (bar 1.5 FAIL)**, dedup 99.6 (bar 0.4 PASS) — PROVISIONAL-PENDING-FREEZE (A7 C′ edit, A8 lookup schedule) |
| M8 | M8GATE PASS |

## Kill-bar adjudication

**Disjunct (b) — proposals-per-accepted-cut must fall over the corpus:**
falls on BOTH corpora, computed from raw per-decile pairs (TAG,R2_CURVE):
- prose: early-3 mean 12.577 → late-3 mean 5.350 (per-decile ratios:
  20.37, 11.51, 9.75, 7.79, 7.27, 6.34, 5.61, 5.31, 5.33, 5.41 — monotone
  decline to the asymptote).
- code: early-3 mean 3.869 → late-3 mean 2.338 (per-decile ratios:
  5.10, 3.83, 3.15, 2.91, 2.73, 2.42, 2.56, 2.41, 2.32, 2.29).
**Verdict: disjunct (b) does NOT fire — the core claim holds.**

**Disjunct (a) — M1 verified-boundary recall vs arm R (≥3 pt margin):**
R2 M1 boundary recall = 100.0 on both corpora (A15 swap probe 63/63).
Arm R has committed **no** scorecard and **no** VERDICT — checked
`units/arms/R/` locally (no scorecard/VERDICT files; only ARM_SPEC.md,
cl/, substrate/, work/) and branch `tnn-native-lab` head `aa992bb5`
(zero paths under any `arms/R/`). R's numbers do not exist to compare
against; none are invented here.
**Verdict: PROVISIONAL-PENDING-R.** (Mechanically: R2 sits at the ceiling,
so the kill fires unless R's boundary recall ≤ 97.0; the R2/Z1 merge
decision A-37 defaults to both tested, so R2 is adjudicated on its own
merits once R's number lands.)

## Provisional cells and ambiguities (logged, not reinterpreted)

- **A15 (M1 ID-swap probe): PROVISIONAL-PENDING-FREEZE.** Implemented
  literally per ARM_SPEC §3; result 63/63 ok labeled provisional.
- **A7/A8 (M7): PROVISIONAL-PENDING-FREEZE.** M7 reuse bar FAILS (1.36 vs
  1.5) — reported as-is. Non-binding for the kill but a real miss: the
  compounding-elimination mechanism's chunk identity is too aggressive for
  the reuse bar on this schedule. Not patched, not hidden.
- Cut-statistics operationalization (late-3 < early-3 from raw decile pairs)
  is the disclosed arm-build interpretation from ARM_SPEC §2.1 (chosen
  post-smoke for the original 64B version, pre-1×-battery for the hybrid;
  raw pairs preserved so any aggregation can be re-checked).
- M8 freelist perturbation is the documented no-op (slot placement is a pure
  function of unit ID); per-proposal/per-elimination ledger entries are the
  documented M5 deviation (10 per-decile op=41 aggregates instead).

## Bottom line

**R2: CORE CLAIM HOLDS (disjunct b does not fire). HEAD-TO-HEAD vs R:
PROVISIONAL-PENDING-R.** R2's M1 verified-boundary recall is at ceiling
(100.0, both corpora, swap 63/63); the arm dies by disjunct (a) iff arm R's
committed boundary recall is ≥ 97.0. M7 reuse misses its bar (1.36 < 1.5) —
honest miss, non-binding. All 18 legs + M8 gate passed with byte-identical
double runs, zero randomness.
