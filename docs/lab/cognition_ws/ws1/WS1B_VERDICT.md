# WS1-B VERDICT — forced-conscious vs mixed vs autopilot (2026-09-24)

**Question (Micah):** allow BOTH (conscious + autopilot) or FORCE EVERYTHING conscious?
**Answer: CONDITIONAL — allow both, but routed by evidence-trust profile, not by modality. Neither "force everything" nor the naive mixed router survives the data.**

## The head-to-head (48 cells, pure Zag, 3 reruns each, G1 0/16, G2 0/16, G3 0/10 — all byte-identical)

| Battery (n) | AUTOPILOT acc | FORCED acc | Winner | Autopilot ops | Forced ops |
|---|---|---|---|---|---|
| admit (248) | 1.000 | 1.000 | TIE | 19.5 | 589.9 (30×) |
| revoke (113) | 1.000 | 1.000 | TIE | 11.2 | 245.2 (22×) |
| logic (264) | 1.000 | 1.000 | TIE | 4.3 | 46.2 (11×) |
| trap (127) | 1.000 | 1.000 | TIE | 7.3 | 69.6 (10×) |
| cost (125) | 1.000 | 1.000 | TIE | 7.5 | 84.2 (11×) |
| rtd1 adversarial (14) | **0.643** (9/14) | 0.286 (4/14) | **AUTOPILOT** | 6.9 | 59.1 (9×) |
| refusal (60) | 0.733 | **1.000** | **FORCED** | 3.4 | 80.7 (24×) |
| perception ambiguous, bill (14) | 0.429 (6/14) | **0.857** (12/14) | **FORCED** | — | 1.2–8.3× marginal |

Stress leg (trap × 10 passes): both regimes FLAT — no compounding bill (ops slope 0.00%/pass; ledger +0.06–0.09%/pass).
Memory: not a differentiator (39–40 vs 42–47 MB per 1000 decisions; the 20 MiB fixed + 18 KB/item arenas dominate). **The consciousness bill is compute, not memory.**

## Why "force everything" is ruled out
On the adversarial red-team battery, forced-conscious scored 4/14 vs autopilot's 9/14 — and was **confidently wrong (conf=1000) on all 10 misses**, while autopilot's 5 misses were tentative (conf ≤500). The sequential-elimination machinery is steerable: crafted attacks get trusted (poison), the verdict gets bait-flipped, strong evidence gets refuted at full confidence. Batch autopilot is an unsteerable majority vote. **This is a direct violation of the H5 never-worse law** ("more depth must never make it worse") — it holds on honest evidence and breaks on adversarial evidence. Depth1_discipline lineage agrees: plain depth-2 0.571, disciplined-E 0.429, tocap 0.286 here — the more aggressive the elimination policy, the worse under poison.

## Why the naive mixed router loses too
MIXED as defined (perception→autopilot, deliberation→conscious) gets the worst of both discriminating batteries: 6/14 on perception (like autopilot) and 4/14 on rtd1 (like forced). Modality is the wrong routing variable.

## The conditional rule (what the data supports)
Route by **evidence-trust profile**, not by modality:

1. **Policy/safety judgments (refusal-class) → conscious.** +26.7pp accuracy; false-refusals 0.400 → 0.000. This is where consciousness pays most.
2. **Honest-but-ambiguous evidence (perception trap-classes: omission/inattention/ambiguity/illusion) → conscious, interrupt-gated** (the F2 pattern: deliberate only when triggers fire, 1.2–8.3× marginal ops). +42.9pp.
3. **Clean, unambiguous structured decisions → autopilot.** Accuracy ties everywhere; autopilot is 10–30× cheaper per correct decision.
4. **Adversarially-suspect evidence → autopilot batch; never sequential elimination.** +35.7pp and no confident-wrong. Conscious deliberation is the attack surface here, not the defense.

Caveats: the router's honest-ambiguous vs adversarial-suspect discriminator is itself untested and needs its own preregistered trial (a cheap deterministic pre-screen, e.g. max-attack-weight/margin ratio, is the candidate). KB-control numbers pending WS1-A's re-verification — if they replicate (deliberation cheaper AND 320/0/0 vs 128/128/64), add rule 5: **KB writes → forced-conscious**. The bill's caveat stands: items_v2 has no genuinely-ambiguous-evidence family, so autopilot's ceiling there is still untested.

## Cost per correct decision (ops/correct, pooled)
Tied batteries: autopilot 4.3–19.5 vs forced 46.2–589.9. rtd1: autopilot 10.7 vs forced 207.0 (autopilot wins accuracy AND cost). refusal: autopilot 4.6 vs forced 80.7 (autopilot 17.5× cheaper per correct — but only forced is correct).

## Reproducibility
Frozen prereg commit `5e24c6e2`; frozen binaries (SHAs in RUNLOG); 48-cell manifest with per-file SHA256 in `runs/manifest.json`; analyzer `analyze_ws1b.py`; full tables in `WS1B_ANALYSIS.txt`. Zero RNG in any decision path; wall-clock reported for context only. Raw 35 MB run outputs kept in workspace (not committed); manifest SHAs + byte-identical reruns make any rerun verifiable.
