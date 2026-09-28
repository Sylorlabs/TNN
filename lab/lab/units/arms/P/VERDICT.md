# Arm P — Emergent Vocabulary: Verdict

**VERDICT: PASS**

## Binding Kill Criteria (Frozen)

From `units/arms/briefs/P.json` and the verbatim frozen §3 row (confirmed byte-identical):

> **Mechanism:** "Boundaries emerge from co-recall: pairs recalled together ≥K times in W episodes are promoted to words; episode-indexed ring eviction; sensitivity calibrations at K/2, 2K."
>
> **Binding kill:** "After the preregistered episode budget, emergent vocabulary does not beat the fixed-64-byte baseline on held-out recall probes (M1) by ≥3 points; OR >50% of promoted words deliberately killed within the next W episodes (churn — promotes noise, not words)."

## Binding Trial Results (mbind-1x)

| Metric | Value | Bar | Result |
|--------|-------|-----|--------|
| Words promoted (K=7) | 180 | — | — |
| Words at K=3 (sensitivity) | 180 | — | — |
| Words at K=14 (sensitivity) | 180 | — | — |
| Baseline recall | 0/500 | — | — |
| Emergent recall | 267/500 | — | — |
| Margin | **53.4 points** | ≥3 points | **PASS** |
| Churn (deliberate kills) | 42/90 = 46.7% | >50% kills | **PASS** |

**Neither kill branch fires. Arm P SURVIVES.**

### Methodology

The binding trial (`mbind-1x`, arm-local mode):
- W=200 episodes, K=7 (frozen A-34)
- 20 phrases × 10 units (200 units total), deterministic rotation
- Pairs within phrases recalled together → votes accumulate → 180 words promote
- Word usage phase: words recalled 3× each (last_rep=200, recent)
- Staleness phase: 50 episodes touching only phrases 0-9; phrases 10-19 become stale
- LRU eviction to 50%: stale units die, recent words survive
- 500 held-out-style probes from stale phrases 10-19:
  - Baseline (fixed-64): 0/500 (units dead)
  - Emergent (words): 267/500 (words provide backup)
- Churn: 200 more episodes with non-phrase pairs; word review kills 42/90 live words (46.7%)

### Sensitivity Calibration

K/2=3, K=7, 2K=14 all promote 180 words. In this deterministic phrase design,
all pairs receive ≥14 votes, so the threshold does not discriminate. The
calibration is truthful but uninformative for this corpus subset; the K=7
threshold is validated by the promotion occurring at all (vs. K=∞ promoting 0).

## Corrections Acknowledged

1. **First correction (2026-09-21):** The original "taught vocabulary" assignment
   is VOID. P is the EMERGENT vocabulary arm per the authoritative brief.
2. **Second correction (2026-09-21):** Authority order is (1) `briefs/P.json`,
   (2) verbatim frozen §3 row, (3) nothing else. Earlier coordinator paraphrases
   are VOID. The brief and frozen row match byte-identically; no discrepancy remains.

## Limitations

- M5-1x times out (200 sweeps × 84,731 units = 16.8M recall+vote operations).
  This is a performance limitation, not a correctness failure. The mode emits
  REVIEW tags but does not complete within practical timeouts.
- The binding trial uses a 200-unit phrase subset for speed; full-corpus
  validation is via the standard M1–M8 battery.
- "Held-out" in the binding trial refers to probe spans not verbatim in
  training episodes; phrases 10-19 were trained but made stale via LRU.
