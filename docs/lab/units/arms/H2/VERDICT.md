# H2 VERDICT — KILLED at 1x (binding kill tripped)

**Arm:** H2 — Budgeted deliberation, CUT family (continuation attempt 2)
**Date:** 2026-09-21
**Battery:** 1x, corpus round `~/workspace/tnn-lab/corpora/r1/`
(prose 5,638,480 B / code 9,515,341 B)
**Evidence:** `evidence/r1/` (second corrected battery, 09:12–09:36 UTC) +
`evidence/r1a/` (first corrected battery, byte-identical stdout on 13/14
modes; M5 difference explained in `evidence/r1/m5-1x-clean-rerun/NOTE.md`)
**Compiler:** `znc_linux_x86_64_abed8aa1` (frozen)

## Verdict

**H2 is KILLED at 1x.** The binding kill tripped mechanically:

> "fallback rate on corpus B > 40% of windows — the budget destroys the
> deliberation."

Measured corpus-B (code) fallback rate: **99.9%** (2,323 / 2,324 windows).
Corpus-A (prose) fallback rate: **100.0%** (1,377 / 1,377 windows).

The reuse-advantage prong passes by a wide margin and does not save the arm:
the kill is an OR — either prong trips it.

**No 10x run.** The protocol gates 10x on every 1x bar passing. The kill
tripped at 1x, so 10x is not run.

## Why it failed (mechanical, not empirical surprise)

Frozen A-19 sets B=8 evaluations/window; the CUT noticer nominates C=16
candidates per window in frozen priority order. With 16 candidates and a
budget of 8, the budget binds in **every** window with ≥9 evaluable
candidates — which on dense corpora is essentially every window. The
fallback is then the fixed-midpoint coarse cut, and the remaining 8
candidates are bulk-refused (exactly 8.0 bulk refusals per fallback window
on both corpora: 11,016/1,377 prose, 18,584/2,323 code).

So the >40% bar is tripped **by construction of the frozen (B=8, C=16)
parameter pair**, not by a surprising property of the deliberation. The
deliberation itself is healthy: recall 100%, boundary 100%, reuse advantage
+80.4/+74.9 points, zero kill-rate, zero tax. The budget is simply set
below the candidate flow the noticer produces. See AMBIGUITIES.md A11.

Any change to B, C, or the kill bar is a prereg change and needs Micah's
re-approval. This verdict applies the frozen rule as written.

## Mode-by-mode results (1x)

| Mode | Result | Key numbers |
|------|--------|-------------|
| M1 prose | pass (metrics) | recall 100.0%, boundary 100.0%, 13,770 units, ID probe 64/64; 1,377 windows, 1,377 fallback (100.0%), 11,016 bulk-refused |
| M1 code | **KILL** | recall 100.0%, boundary 100.0%, 23,236 units, ID probe 64/64; 2,324 windows, 2,323 fallback (**99.9%**), 18,584 bulk-refused |
| M2 T1/T2/T3 | pass | mastery episode 1, final recall/boundary 100% (all) |
| M3 | pass | survival 100%, fresh recall 100%, freeze CLEAR, 1,150 mgmt entries, 50 weakens handled |
| M4 prose/code | pass | revision content/boundary 100%, kill rate 0.0% |
| M5 | pass | 13,770 units; slot table 684,124 B (0.42× source); ledger 1,689,280 B / 26,395 entries (4.7/KB ≤ 10/KB) |
| M6 p2c / c2p | pass | recall/boundary/revision 100%, tax 0.0% both directions |
| M7 | pass (both prongs) | H2 hit rate 100% both corpora; baseline 19.6% prose / 25.1% code; advantage **+80.4 / +74.9** (kill needs < +5); ID-stable companion +84.4 both |
| M8 (5 regimes) | *see M8-REPORT.md* | clean/frag/aslr/starve/freelist-rev |
| M9 T1 | info | fast-then-flat, takeoff ep 1, steepness 100%, late gain 0% |

All modes exited 0.

## Determinism

- 13/14 modes byte-identical stdout across the two corrected 1x batteries.
- M5 differed in one trailing write-status field (`0` vs `-1`): a
  harness working-directory collision (stale `ledger.bin`), not AI
  nondeterminism. Clean rerun byte-identical to battery 1; ledger SHA-256
  `c988bd357c9d7e5a19485c18326003636ca995b05945a4ac4f5ac0cf4460090f`.
  See `evidence/r1/m5-1x-clean-rerun/NOTE.md`. The anomalous record is
  preserved, not overwritten.
- Post-repair smoke: `m1-1x-prose` byte-identical after the t_m8-only
  source repair (BUILD_NOTES.md).

## What this does NOT claim

- The kill is about the **budget parameters**, not the deliberation's
  correctness: every quality metric is at ceiling.
- Boundary fidelity is folded into the recall pass (A3); the ID probe is
  provisional pending the ID-arm freeze (A10).
- The 10x separator-vs-verbatim construction conflict (A5) was not
  resolved and not exercised.
