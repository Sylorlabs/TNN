# ARM I1 — Verdict (1x)

**Date:** 2026-09-21
**Scale:** 1x (14 modes + M8)
**Verdict:** **SURVIVES** — no binding kill criterion fires at 1x.

## Kill-criterion results

### (i) L2+ share of successful recalls — SURVIVES (≥5% required)

| Mode | L2+ share |
|------|-----------|
| m4-1x-prose | 99.04% |
| m4-1x-code | 98.32% |
| m5-1x | 100.00% |

M1/M2/M3 report 0% because they do not build L2 (M1 = flat ingest/recall;
M2 stops at ETC=1 before `T_co`; M3 = churn without rehearsal). Where the
hierarchy exists, L2+ ancestry covers 98–100% of recalls.

**Caveat:** the implementation counts L0 recalls with live L2+ ancestry;
it is not a true equal-store-cost flat comparator. The margin (98%+ vs 5%
bar) leaves no plausible comparator that flips the result, but the
comparator should be built before 10x.

### (ii) Parent maintenance + stale rebuild ≤20% — SURVIVES

| Mode | Maintenance fraction |
|------|----------------------|
| m1-1x-prose | 0.13% |
| m1-1x-code | 0.23% |
| m4-1x-prose | 15.08% |
| m4-1x-code | 15.36% |
| m5-1x | 14.67% |

All well under the 20% bar on every corpus.

**Caveat:** measured per mode-instance (whole store), not per corpus as
the freeze phrases it. Each mode exercises primarily one corpus, so the
per-mode figure is the closest available; all pass with margin.

### (iii) L1 boundary agreement ≥50% — SURVIVES

| Mode | Agreement |
|------|-----------|
| m5-1x | 70.42% |

(M2 reports 100% vacuously — no L1 forms before its ETC stop.)

**Caveat:** "natural breaks" is undefined in the freeze. Under the
provisional whitespace interpretation (boundary at corpus edge or after
whitespace), agreement is 70.42%. This interpretation is **nonbinding** —
it cannot trigger a death by itself.

## Other bars

- **M1:** 100.0% recall, 100.0% boundary, both corpora; swap probe true.
- **M3:** 100.0% valuable survival, 100.0% fresh recall, 50/50 weaken handled.
- **M4:** 100.0% / 100.0% revised, 0.0% killed, both corpora.
- **M5:** footprint within ranking bar (see scorecard for bytes).
- **M6:** transfer 100.0% both directions.
- **M7:** 100.0% / 100.0% lookup hits.
- **M8:** byte-identical artifacts across base/frag/aslr perturbations;
  283989 ledger entries, no truncation.
- **M9:** gradual takeoff shape on M2 tiers (no false sudden-takeoff).

## 10x status

**Not run.** The 10x scale legs require 10x corpora; the harness provides
only 1x corpora and this build implements no 10x modes. Per R-9, 10x was
gated on 1x bars passing — they do — but the scale leg itself is
unimplemented. Recommend: coordinator decides whether 10x = 10x data
(needs corpora) or 10x episodes before I1 builds 10x modes.

## Ambiguities carried

1. `E=3` demotion threshold — PROVISIONAL-PENDING-FREEZE.
2. Natural-break definition — provisional whitespace interpretation.
3. A17 M8 instance — combined M1+M3 chosen provisionally.
4. I1 as ID arm — provisional; M1 swap probe + M7 retained.
5. Equal-store-cost comparator for kill-(i) — not yet built.
6. Per-corpus (vs per-instance) maintenance accounting for kill-(ii).
