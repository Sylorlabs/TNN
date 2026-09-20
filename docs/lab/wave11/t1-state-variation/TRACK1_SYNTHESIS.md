# TRACK 1 SYNTHESIS — State-dependent deterministic variation (Arm C)
Date: 2026-09-20. Coordinator: wave11 mega-swarm. Investigators: 25/25 complete.
Source files: `findings/01-*.md` … `findings/25-*.md` (each: falsifiable claim + kill bar + honesty notes).

## Track verdict: GO as a design program
All 25 slices returned buildable, falsifiable designs. No slice found the concept impossible.
The 25 designs cohere into one architecture (no contradictions found between slices):

```
enumerated state (16) ──evolution law (18)──▶ state @ episode E
        │                                            │
        ▼                                            ▼
projections: P(M) (01), salience (02),          firewalls (12/13/14/20):
budget (03), load (04)                          verdict → sealed record;
        │                                       memory/refusal/ledger paths
        ▼                                       can never read variation
variation functions (05/06/07/08)               state; two coincident
composed lexicographically (23),                barriers (phase seam +
calibrated (21)                                 import-graph boundary)
        │
        ▼
expression (MAY vary) ──logged──▶ ledger (15): VARIATION_CHOICE entries,
   phrasing/path/order/depth                      variant_id + selector_hash;
                                                  phrasing excluded

Auditors around everything: no-RNG gate (09), replay protocol (17),
adaptivity metric (10), arbitrariness detector (11), null baseline (24),
corrupted-state degradation (22), human-variation mapping (19),
trial kill bars (25).
```

## Consolidated prereg-style bars for the Arm C build trial
- **K1 replay:** any byte mismatch replaying input + logged full state → concept dead, no repair.
- **K2 ledger/integrity:** any ledger-byte or integrity-disagreement across expression variants → dead.
- **K3 verdict:** any verdict divergence across variants of identical (input, state) → dead.
- **K4 memory decisions:** any memory-op divergence under expression-state perturbation → dead.
- **K5 arbitrariness:** arbitrariness detector fires → one dated repair, then concept dead.
- **K6 adaptivity/degeneracy:** adaptivity below bar (direction rate <0.60, NMI < max(0.30, 5×null), fails on
  held-out states) or degenerate variation → one repair, then dead.
- **K7 head-to-head:** fenced RNG Arm B beats Arm C honestly at 1x and 10x → retire C, report B's win as-is.
- **K8 cost:** latency >1.50× null median, >500 new Zag lines, or audit >1.10× null bytes/episode → implementation dead.
- **K9 regression:** any regression on committed evidence (RC3 corpus, wave5/6 traps) → implementation dead.
- Supporting numeric bars: adaptivity direction rate ≥0.60 (99.5% CI >0.50, ≥400 pairs); arbitrariness
  predictor must beat best-constant by ≥10pp at p<0.01 on ≥2/3 inputs; variation diversity D strictly
  between 0.15 and 0.6·D_cross with Spearman ρ ≥ 0.4 vs state distance; salience weights in [16,1000]
  from logical clocks only; load L integer-only with monotone 4-tier mapping and refusal floor;
  no-RNG audit must catch 20/20 planted entropy sources with 0 false positives.

## Falsifiable claims (track-level, from the slices)
1. Output = f(input, full logged state) with zero RNG can produce ≥3 distinct lawful expression
   variants per verdict class while verdicts, memory decisions, refusals, and ledger stay
   byte-identical (01/05/12/13/14/15).
2. Every legitimate variation is attributable to a logged state difference; any unattributable
   variation proves a missing state variable via differential replay, discoverable at p≥0.01
   within 460 episode pairs (16/17/18).
3. The no-RNG auditor provably gates the variation path: any audit-passing build cannot emit
   RNG-influenced variation (09).
4. Variation is adaptive (tracks state, extrapolates to novel states — 10) and not arbitrary
   (11), calibrated between cosmetic jitter and RNG-equivalence (21), beating the null baseline
   (24) at bounded cost.
5. Corrupted or adversarial state degrades to deterministic NULL variation; the worst case an
   attacker buys is boring phrasing (22).

## Honest tensions (do not hide these)
- **Ledger tension (24):** Micah's byte-identical-ledger bar sits in real tension with any
  state-dependent deliberation path that audits itself. Held as written; flagged for Micah.
- **Unmapped human variation (19):** mood/affect, paraphrase-without-cause, stranger-audience
  shifts, and production noise do not map to the four state variables. The "humans vary via
  state" premise is an engineering idealization, not a fact.
- **Arbitrary constants (04/21/23):** load weights, calibration bands, and composition priority
  are judgment calls — benchmark per no-free-lunch, do not harden prematurely.
- **Scope bounds (06):** path-inventory confluence proven only for |H| ≤ 6; large deliberation
  excluded from variation for now.
- **Detector blind spots (11):** lawful-but-exotic mappings can false-positive; deterministic
  unlogged constants escape Gate 0 — enumeration completeness is load-bearing.

## What to build next (ordered)
1. The no-RNG auditor + versioned attestation (09) — the gate everything else passes through.
2. The state schema + replay protocol + evolution law (16/17/18) — the foundation.
3. The sealed verdict record + the two coincident firewalls (12/20) + ledger canonicalization (15).
4. One variation function (phrasing, 05) with the adaptivity/arbitrariness harnesses (10/11)
   and the null baseline (24).
5. The full Arm C trial vs null vs fenced Arm B under K1–K9 (25), at 1x then 10x.

**Amendments used:** none (Track 1 uses zero RNG). **Reverts available:** n/a — design phase, nothing built.
