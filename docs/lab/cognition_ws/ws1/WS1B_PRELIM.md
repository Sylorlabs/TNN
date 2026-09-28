# WS1-B interim notes (2026-09-24)

Legs complete: D (5 batteries × 2 configs × 3), RT (rt_d1 × 2 × 3), RF (refusal × 2 × 3), S (trap×10 × 2 × 3) = 48 cells, all rc=0.
Perception leg: frozen bill evidence (F1 6/14, F2 12/14), no new runs.

## Gates
G1 0/16 (byte-identical res+ledger across 3 reruns), G2 0/16 (ops/rounds/ev/correct identical), G3 0/10 (matches bill anchors).
Note: first analyzer pass reported G1 15/16 — analyzer bug (mixed res-SHA and led-SHA into one set); data was fine, analyzer fixed, re-verified.

## Headline numbers (AUTO vs FORCED=tocap, pooled 3 runs)

| Battery | n | AUTO acc | FORCED acc | ACC bar | AUTO ops | FORCED ops |
|---|---|---|---|---|---|---|
| admit | 248 | 1.000 | 1.000 | TIE | 19.5 | 589.9 (30.3×) |
| revoke | 113 | 1.000 | 1.000 | TIE | 11.2 | 245.2 (21.8×) |
| logic | 264 | 1.000 | 1.000 | TIE | 4.3 | 46.2 (10.8×) |
| trap | 127 | 1.000 | 1.000 | TIE | 7.3 | 69.6 (9.6×) |
| cost | 125 | 1.000 | 1.000 | TIE | 7.5 | 84.2 (11.3×) |
| rtd1 | 14 | 0.643 | 0.286 | **AUTO WINS** | 6.9 | 59.1 (8.6×) |
| refusal | 60 | 0.733 | 1.000 | **FORCED WINS** | 3.4 | 80.7 (23.7×) |
| perception (bill) | 14 | 0.429 | 0.857 | **FORCED WINS** | — (1.2–8.3× marginal) |

## Never-worse watch: VIOLATION on rtd1
FORCED 4/14 vs AUTO 9/14 (Δ −35.7pp, band 7.14pp). Item detail:
- FORCED wrong on all 10 adversarial items, at conf=1000 (confident-wrong): POISON×3, BAIT×3, DOUBLE×2, STRONG×2. Only the 4 CLEAN right.
- AUTO wrong on 5/14 (POISON×3, DOUBLE×2) but at conf 300–500 — tentative, never confident-wrong.
Mechanism: tocap's falsification-first sequential elimination is steerable by crafted evidence (trusts poison attacks, gets bait-flipped); batch autopilot is an unsteerable majority vote. Depth1_discipline lineage agrees: plain depth-2 scored 0.571 here, disciplined-E 0.429, tocap 0.286 — the more aggressive the elimination policy, the worse under poison. The H5 never-worse law ("more depth must never make it worse") FAILS on adversarial evidence; holds on honest evidence.

## Stress leg
10 passes over trap, both regimes FLAT: ops slope 0.00%/pass both; ledger +0.06%/pass (auto), +0.09%/pass (tocap). No compounding bill.

## Memory
Per-1000-decision pressure: 20 MiB fixed dominates; AUTO 39–40 MB vs FORCED 42–47 MB (<17% apart). The consciousness bill is compute (ops), not memory.

## Cost per correct decision (ops/correct)
- Tied batteries: AUTO 4.3–19.5 vs FORCED 46.2–589.9 (10.8–30.3×).
- rtd1: AUTO 10.7 vs FORCED 207.0 (19.3×) — autopilot wins accuracy AND cost.
- refusal: AUTO 4.6 vs FORCED 80.7 — autopilot 17.5× cheaper per correct, but only forced is correct (0.733 vs 1.000).

## Working recommendation (→ verdict)
Neither FORCED (ruled out by rtd1 NW violation) nor MIXED-as-defined (modality router: loses perception like autopilot AND rtd1 like forced — worst of both) wins. Answer is CONDITIONAL with a trust-profile router: policy/safety judgments → conscious; honest-but-ambiguous evidence → conscious (interrupt-gated); clean structured decisions → autopilot; adversarially-suspect evidence → autopilot batch (never sequential elimination). Router's ambiguity-vs-adversarial discriminator is itself untested — needs its own preregistered trial. KB-control leg pending WS1-A (if replicated: KB writes → forced-conscious, cheaper AND better).
