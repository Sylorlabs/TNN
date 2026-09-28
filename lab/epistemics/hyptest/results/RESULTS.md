# Hyptest sealed battery — coordinator results (2026-09-27)

Binary: clean-room rebuild of amended source (Crew M2 "are"-fallback),
delib=1 SHA `8becb3831f99f1183d51f9ba83aba2aebdb3acc213d489934c7750e3b0296b8a`
(independently reproduced; matches M2's build).
delib=0 SHA `43bfa928302120cf29956f3c02b887d108ad15631f2f479a637214bad58a384d`.

Runs: `run/s1` (reference), `run/s2`, `run/s3` (env -i), `run/s4`
(MALLOC_PERTURB_=165) — all four byte-identical (`diff -r` clean).
Scorer: `run/score_sealed.py` → **60/60 PASS** (output above, frozen in
`run/score_s1.txt`).

## Per-case verdicts

| case | domain | hypotheses | predictions | audit order | result | gold |
|------|--------|-----------|-------------|-------------|--------|------|
| seal01 | food serving/fat→calories | 2 | many-caloried vs few-caloried | 33 < 35 | h0 refuted+abandoned, h1 supported | B wins ✅ |
| seal02 | aircraft wingspan/weight→speed | 2 | fast vs slow | 33 < 35 | h0 refuted+abandoned, h1 supported | B wins ✅ |
| seal03 | planet distance/diameter→year | 2 | long-yeared vs short-yeared | 33 < 35 | h0 supported, h1 refuted+abandoned | A wins ✅ |
| seal04 | moon distance/size→period | 2 | slow vs fast | 33 < 35 | h0 supported, h1 refuted+abandoned | A wins ✅ |
| sealB1 | latitude/altitude→temperature | 2 | cold vs hot | 33 < 35 | withhold, none abandoned | WITHHOLD ✅ |
| sealB2 | food serving/fat→calories | 2 | many-caloried vs few-caloried | 33 < 35 | withhold, none abandoned | WITHHOLD ✅ |

## K-bar scoreboard

| bar | requirement | result |
|-----|-------------|--------|
| K1 | 2 hypotheses on 6/6 sealed | 6/6 ✅ |
| K2 | discriminating predictions + test choice | 6/6 distinct ✅ |
| K3 | predictions audit-precede observation | 6/6 (33 < 35) ✅ |
| K4 | correct winner on 4/4 discriminating | 4/4 ✅ |
| K5 | withhold on 2/2 boundary | 2/2 ✅ |
| K6a | deliberation-disabled → 0 hypotheses | 6/6 ✅ (separate run, `run/z0`) |
| K6b | content-swap control | red team (Crew R) |
| K6c | narrator-only stub fails | red team (Crew R) |
| K7 | standalone rebuild, no relay | ✅ clean-room rebuild, SHA reproduced |
| K8 | determinism (2×, env -i, perturb) | ✅ 4/4 byte-identical |
| K9 | zero internally confident-wrong | 4/4 ✅ |
| K10 | citation precision/recall ≥ 0.75 | recall 6/6 × 12 hypotheses; 0 extra cites ✅ |

K6b/K6c verdicts pending Crew R (dispatched 2026-09-27).
