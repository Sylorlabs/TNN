# REPORT NW-1 — Noisy-legitimate withhold measurement (advisor proposal #2)

Date: 2026-09-28. Prereg: PREREG_NW1.md (frozen before measurement).
Advisor: z.ai/GLM key still HTTP 403 on both listed models
(glm-5.3-flash, glm-5.3-flash-search), probed 2026-09-28 ~01:10 UTC.
grok-4.7 (highest reasoning, streaming) served as advisor per the brief;
full exchange in zai_advisor_prompt.txt / zai_response.txt.
Implemented advisor proposal #2. Proposal #1 (substrate + lineage
integration) was referred to the free-memory substrate crew as their next
kill bar once the substrate lands — it cannot run before the substrate exists.

## Corpus correction (prereg K2 as written was based on a wrong premise)
The 40 `xp_calib_*` pairs are NOT all byte-identical. They are:
- 20 byte-identical must-admit controls (pitchdisc 001–019, shapetrans 000–018 even), and
- 20 single-byte ±1 tolerance probes (pitchdisc 021–039, shapetrans 020–038 even),
  truth=SAME, "tolerance-boundary probe: single byte … (+1); underlying fact
  effectively unchanged".
The frozen corpus itself encodes the exact-vs-tolerant semantic fork. K2 is
restated: all ids admit 20/20 byte-identical; the 20 probes are reported per
variant (their correct verdict IS the semantic question).

## Results (352 pairs; 3/3 runs byte-identical incl. MALLOC_PERTURB_=165)

Counts are WITHHOLDS. Classes: IDENT (20 byte-identical), PROBE (20 one-byte
±1 probes), ADV (312 adversarial), N1/N2/N3/N4 = in-memory deterministic
noise on all 352 F blobs (1B@L/2; 3B; 8B; 1B@pos3).

| class (n)        | id2 span_seq/8 | id3 span_sum/8 | id4 FNV-1a exact |
|---|---:|---:|---:|
| IDENT (20)       | 0 (admit 20/20) | 0 (admit 20/20) | 0 (admit 20/20) |
| PROBE (20)       | **20** | 6 (admit 14/20) | **20** |
| ADV (312)        | **208** (miss 104) | 0 (miss 312) | **312** |
| N1 (352)         | 352 | 6 | 352 |
| N2 (352)         | 352 | 6 | 352 |
| N3 (352)         | 352 | 352 | 352 |
| N4 (352)         | 61 | 6 | 352 |

id2 ADV misses by family: fshuffle 48/48, pxperm colordisc+colorconst 32/32
(shapetrans 16/16 caught), wsumcol 24/24; audiorev/blkswap/cycshift/sumswap
48/48 each caught.

## White-box findings

**1. The fix1 primary gate (id2) is blind to block permutations of
equal-sum blocks — 104/312 adversarial missed.** Its "provably separates
permutations" argument covers byte-level swaps (delta = (i-j)·(y-x)), not
block moves. For 8 frames of equal byte sum S at 384-byte stride,
span_seq = S·Σ(8+384·pos) + Σ_frames inner(frame): both terms are
permutation-invariant (verified numerically: total diff exactly 0 on
xp_fshuffle_motiondir_000). So all 48 fshuffle pairs collide exactly, and
32/48 pxperm single-frame pairs land in the same /8 bucket. Only id4
(FNV-1a) reaches 312/312.

**2. id2's /8 "tolerance" is vestigial on realistic noise.** It withholds
352/352 N1/N2/N3 and 20/20 frozen probes — identical to exact identity —
because a one-byte change at position ≥7 moves the /8 bucket. Its tolerance
window covers only the first ~7 bytes (N4: 291/352 admitted). It is
near-exact in practice, not a lenient alternative.

**3. Generator mod-8 clustering explains the id3 noise numbers.**
span_sum mod 8 over the 352 F blobs is {0:170, 1:40, 2:106, 3:6, 4:24, 7:6}
— zero mass at 5,6. Hence id3 withholds exactly the 6 blobs at mod 7 on
+1 noise (N1, N4) and the same 6 on +3 noise (N2), not the naive 1/8 and 3/8
rates. No driver bug (verified against independent Python recomputation).

## Kill bars
- K1: id4 withholds 312/312 ADV — HOLD.
- K2 (restated): all ids admit 20/20 IDENT — HOLD. The 20 PROBE items are
  the semantic fork: id2/id4 withhold 20/20, id3 admits 14/20.
- K3: 3 runs byte-identical (2 plain + MALLOC_PERTURB_=165) — HOLD
  (run1/2/3.txt SHA 4fc695f8…; stdout SHA 7b87e88c…).
- K4 prediction audit: id4 all cells exact. Misses with explanations:
  id2 ADV 208 vs predicted 312 (finding 1); id3 N1/N2/N4 admit rates above
  naive prediction (finding 3); id2 N4 61 vs ~44 predicted (non-uniform
  weighted-sum mod-8, within noise of the 5% band at 4.8%).

## What this means for Micah's decision (informs, does not decide)
- The 100% number belongs to id4 alone. id2 (the fix1 "primary") scores
  208/312 on the adversarial expansion — it does not survive its own
  red team.
- There is no lenient option among the tested variants: id2 withholds
  benign one-byte noise exactly like id4. If the semantic choice is
  "tolerate harmless noise", neither id2 nor id4 implements it; that needs
  a different tolerance design (relative/noise-floor-aware), not a ruling
  between these two.
- The 20 frozen tolerance probes give him a concrete anchor: under exact
  identity they are withheld 20/20; under the legacy sum gate 14/20 are
  admitted — at the cost of admitting 312/312 adversarial.

## Files
- nw_measure.zag — driver (pure Zag, zero RNG; committed g1_candidate.zag
  used unmodified)
- run1.txt — per-pair verdicts (canonical; run2/run3 byte-identical)
- stdout1.txt — summary counts
- zai_advisor_prompt.txt, zai_response.txt — advisor exchange (grok-4.7)
