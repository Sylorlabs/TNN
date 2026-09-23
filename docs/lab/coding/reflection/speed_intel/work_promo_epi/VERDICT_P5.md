# P5 Verification — Epistemic 2x confirmed as mainline default (2026-09-22)

Promotion prereg: `coding/reflection/speed_intel/PROMOTION_PREREG.md` (frozen, commit f5154e8c).
Pinned znc: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
Source: `prose-learning/epistemic_wave/speechact_exp/delib_sa.zag` (UNTOUCHED).

## (a) Confirmed default invocation

The source header (`delib_sa.zag` line 9) is the committed canonical invocation:

> `// Usage: delib_sa_bin <workdir> <arm: 1|2> <items-file>`

Arm is an explicit required argument; there is no built-in default, but the
committed corpus treats arm=2 (full pipeline: world-knowledge checks + all 6
speech-act matchers, knowledge compiled in) as the standard path:

- `speed_intel/PREREG.md` §3d: the epistemic slice is built "on `delib_sa`, arm=2".
- The frozen arm-2 scored evidence in
  `speechact_exp/scored_evidence/arm2_{b12_false,b12_true,c70}_rep1.txt`
  is the supported-hypothesis arm of RESULTS.md / SPEECH_ACT_HEADLINE.md.
- Arm 1 is an ablation of the SAME mechanism (no speech-act matchers);
  nowhere is arm=1 presented as a default.

CONCLUSION: arm=2 is already the effective 2x default. **No code change needed**
(exactly as the prereg expected). 4x/8x reconsideration+verification do not exist
in `delib_sa.zag` (Arm 1 found them inert: 0 recon, 0 flips) — nothing to gate off.

## (b) 3-rerun verification score table (mainline delib_sa, arm=2)

Frozen target from RESULTS_SI.md: total 59/94, false 12/12, true 12/12,
families joke 5, sarcasm 3, hypothetical 5, analogy 3, counterfactual 9,
poetry 5, implicature 5 (/10 each).

| rep | total | false/12 | true/12 | joke | sarc | hyp | anal | cf | poet | impl |
|-----|-------|----------|---------|------|------|-----|------|----|------|------|
| 1 | 59/94 | 12 | 12 | 5 | 3 | 5 | 3 | 9 | 5 | 5 |
| 2 | 59/94 | 12 | 12 | 5 | 3 | 5 | 3 | 9 | 5 | 5 |
| 3 | 59/94 | 12 | 12 | 5 | 3 | 5 | 3 | 9 | 5 | 5 |

All three reps match the frozen 59/94 AND every per-family cell.

## (c) Byte-identical?

YES.
- Raw stdout SHAs identical across reps:
  - b12_false: `be4d1fb6e94b18373cd8010f4e189708d6a8d2127072461d5412351ec8a07612`
  - b12_true:  `d5243eeaa3b8b436a374a68d4a3606edc06f20e9f349c76f4dd89287b994069e`
  - c70:       `181032b1d4bfdc4b9cedbb66a6edb87286cda168b3b46b525aa4d522c6f63fc4`
- Canonical verdict digest (timing-free): `7c9810f064dbf07399815d21aabb27ea58091e38da8414c0dd682e18784fe14a` ×3.
- The run1 outputs are additionally byte-identical (diff -q) to the committed
  frozen arm-2 evidence in `speechact_exp/scored_evidence/`, and the SHAs match
  the digest prefixes recorded in `speechact_exp/RESULTS.md` lines 117–122
  (be4d1fb6…, d5243eea…, 181032b1…).

## (d) Wall-clock (per item-file, ms; `wallclock.txt`)

rep1: b12_false 23, b12_true 26, c70 34 (total ~83ms)
rep2: b12_false 9,  b12_true 42, c70 110 (total ~161ms)
rep3: b12_false 102, b12_true 62, c70 145 (total ~309ms)

End-to-end per full 94-item rerun: 83–309ms (varies with machine load;
the deliberation itself is sub-second — effectively free vs the ZnC coding loop).

## (e) Code change needed? NO.

`delib_sa.zag` already implements arm=2 = full pipeline = the frozen 2x knee.
4x/8x mechanisms live only in Arm 1's `delib_si.zag` and were proven inert.

## (f) Deviations from prereg

None. Invocation replicated Arm 1 exactly (`<workdir> 2 <items-file>` per file);
item-file hashes match the frozen copies (1fcaf170…, f6099234…, 9a1b4f5e…).
Zero RNG; pure Zag deliberation; Python glue only (scorer). Nothing committed.

Artifacts here: `delib_sa_promo` (fresh build, local only — NOT committed),
`epi/` (item copies), `run1/2/3/*.out`, `wallclock.txt`,
`score_promo_epi.py`, `scores_promo_epi.json`.
