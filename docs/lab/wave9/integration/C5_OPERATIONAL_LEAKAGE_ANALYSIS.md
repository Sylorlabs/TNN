# C5 Operational-Leakage Analysis — intact repaired-S10 run

**Question:** does the INTACT repaired-S10 run (main `s0`–`s5` re-run, `c5_arm=0`) exhibit
operational leakage — successful COMPOSE ledger entries whose backing claim (`a1=claim_cid`)
was O2-REFUTED at the compose episode?

## Method note (read first)

The committed raw evidence (`evidence_s10_repair/`) contains **only aggregate telemetry**
(CHECK/DROPS/P1RET/PINFRAC lines) — no per-ledger-entry data. The ledger is in-process;
the frozen binary has no dump mode. I reconstructed the intact ledger with a **scratch
analysis driver** (`/tmp/c5leak/analyze.zag`, not trial code — nothing in `impl/` was
changed) that replays `loop_init(10)` + `loop_run_stage(s,10)` exactly as `mn_stage` does
(incl. `force_abstain=12` for s2). Fidelity check: the replay reproduces the committed
instrument telemetry **exactly** per stage (drops 0,0,0,0,125,87; P1RET
1000,1000,1000,1000,780,823; PINFRAC 0,3,3,3,3,3). Paired determinism is byte-identical,
so this is the same ledger the intact run produced. Verdict-at-compose = latest
`(LG_O2, VERDICT)` entry for the claim **strictly before** the compose entry in ledger
order (verdicts dispatch in loop section 2, after section-1 composes). Episode `d2` is
per-stage; joins are within-stage.

## Results

| Measure | Count | % of 1,024 |
|---|---|---|
| Successful COMPOSE entries (rc=0), intact run (s2–s5, 256/stage; s0/s1: O4 off, 0) | **1,024** | 100% |
| Backing claim REFUTED at compose time | **9** | **0.9%** |
| No backing claim (a1 ≤ 0) — verdict-uncheckable | **6** | 0.6% |
| Backing claim CONFIRMED | 263 | 25.7% |
| Backing claim OPEN | 584 | 57.0% |
| Backing claim SUSPECT / EXONERATED | 162 | 15.8% |

(Context: 7,228 COMPOSE ledger entries total in the intact run; the remaining 6,204
failed inside `o4_compose` — the verification gate doing its job. The leakage question
concerns the 1,024 that passed.)

The 9 REFUTED-backed successes: 3 in DC-2, 3 in DC-3, 3 in DC-4, 0 in DC-5. Detail shows
the natural mechanism — e.g. stage 2: claim 46 SUSPECT at ep 69 → REFUTED, then a
successful compose at ep 70 backed by claim 46 (trace 57); same pattern for claims
81 and 116. A claim on the anchor slot is refuted in episode N (section 2); episodes
N+1 composes still annotate it as backing until a new claim opens there. The compose
path (`c5_arm=0`) never reads the verdict — by design.

**Downstream (Q4):** all 9 REFUTED-backed successful composes were followed by a
successful APPLY in the same episode (matching trace id + episode, APPLY rc=0) —
the composites flowed into live application. **Zero** of the 9 backing claims were ever
used as CONSOLIDATE backing (consolidation only fires on CONFIRMED at dispatch time;
REFUTED is terminal), so the leak did not propagate into O3 in this run.

## Assessment: the leak is OPERATIONALLY REAL (with two qualifiers)

The killed-only arm was **not** an artificial construction: it proved the machinery
admits refuted-backed composes when allowed, and this join proves the intact system
**actually reaches that state in normal operation** — 9 times, across three
developmental stages, each flowing into a successful apply. "Partitions are advisory,
not enforced" is a property of the live system, not just the test harness.

Qualifiers: (1) It is rare — 0.9% of successful composes — because the exposure window
is narrow (refuted claim → replaced on the anchor slot). (2) `claim_cid` is an **audit
annotation**, not an input to `o4_compose`: the composed vector derives from O4's
trace-store selection, which never reads the claim. This join therefore proves
*partition non-enforcement at the seam* (the C5 claim), not that refuted claim
*content* influenced the composed vectors. A content-flow test would need to trace
O4's store lineage, which this analysis did not do.
