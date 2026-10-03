# BUILD NOTES — decline-investigation Zag engine variants (2026-09-22)

Five variants of `delib_vol.zag`, built as surgical copy-modify diffs. All five
compile and are deterministic (byte-identical reruns). Four pass the b12_true
control leg at 12/12; **delib_f3_bin BREAKS it (4/12)** — reported, not tuned.

## Toolchain / compile commands

Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
Build cwd: `~/workspace/tnn-lab/prose-learning/epistemic_wave/speechact_exp`
(`@import("../src/...")` resolves relative to cwd — builds must run from this dir.)

Baseline sanity build first (unmodified `delib_vol.zag` → `/tmp`, warnings only):
```
znc_linux_x86_64_abed8aa1 delib_vol.zag -o /tmp/delib_vol_baseline_bin
```
Then one command per variant (exact):
```
znc_linux_x86_64_abed8aa1 delib_cnt.zag -o delib_cnt_bin
znc_linux_x86_64_abed8aa1 delib_b2.zag  -o delib_b2_bin
znc_linux_x86_64_abed8aa1 delib_b3.zag  -o delib_b3_bin
znc_linux_x86_64_abed8aa1 delib_f2.zag  -o delib_f2_bin
znc_linux_x86_64_abed8aa1 delib_f3.zag  -o delib_f3_bin
```
All five wrote native binaries with only analyzer warnings (same warning classes
the original emits: A0101/A0102/A0107/L0012). No build errors, no debugging
needed — the copy-modify approach kept every znc workaround intact.

Note: a `delib_vol_bin` (96469 bytes, 18:11) exists in this directory but was
NOT built by this task (baseline was built to /tmp); left untouched. Binaries
here are per-task deliverables and are NOT committed (per AGENTS.md, build
binaries stay out of the repo).

## What changed per variant

| Variant | Hypothesis | Change (all else identical: examples, order, world knowledge, CLI) |
|---|---|---|
| `delib_cnt.zag` → `delib_cnt_bin` | H-D1 | `concept_match`: decision replaced. Count matched features with `disc ≥ 750`; WITHHOLD iff count ≥ 3. The `prev` term and the `score` accumulator were removed entirely — no prevalence term anywhere in the decision. |
| `delib_b2.zag` → `delib_b2_bin` | H-D3 B2 | Score-only ablation: `if(score>=500)` — the `bestd>=750` gate dropped. Weight math unchanged. |
| `delib_b3.zag` → `delib_b3_bin` | H-D3 B3 | Disc-only ablation: `if(bestd>=750)` — the `score>=500` gate dropped. Weight math unchanged. |
| `delib_f2.zag` → `delib_f2_bin` | H-D4 F2 | `xfeat` gains five closed-class frame feature TYPES (counts still learned from examples): (a) `subjp_i/you/he/she/it/they/we/other` from the first word; (b) `stdur` on has/have/had been, " still ", " again ", since, out of, empty; (c) `negfr` on n't, " not ", " no ", never, nothing, nobody; (d) `yp` on " you ", " your", "yours", or utterance starting with "you "/"are you"; (e) `itloc` on utterance starting with "it is "/"it's "/"it 's ". All existing features kept; decision rule unchanged (500/750). |
| `delib_f3.zag` → `delib_f3_bin` | H-D4 F3 | All of F2, PLUS: for every adjacent bigram `w1_w2`, also add `w1_C` when w2 is a content word (len ≥ 3 AND not in {i,you,he,she,it,they,we,is,are,was,were,be,been,am,this,that}), via an `f3_content` helper, with within-utterance dedup matching the existing bigram pattern. Decision rule unchanged (500/750). |

## Smoke-test results (rung 2, mode=all)

| Binary | c70 output | b12_true output | Determinism (2 runs, cmp) |
|---|---|---|---|
| `delib_cnt_bin` | SUMMARY n=70 endorse=53 withhold=17 | SUMMARY n=12 endorse=12 withhold=0 | IDENTICAL |
| `delib_b2_bin` | SUMMARY n=70 endorse=17 withhold=53 | SUMMARY n=12 endorse=12 withhold=0 | IDENTICAL |
| `delib_b3_bin` | SUMMARY n=70 endorse=17 withhold=53 | SUMMARY n=12 endorse=12 withhold=0 | IDENTICAL |
| `delib_f2_bin` | SUMMARY n=70 endorse=16 withhold=54 | SUMMARY n=12 endorse=12 withhold=0 | IDENTICAL |
| `delib_f3_bin` | SUMMARY n=70 endorse=12 withhold=58 | SUMMARY n=12 endorse=4 withhold=8 ⚠️ | IDENTICAL (3rd run also identical) |

All outputs are well-formed `ID|ENDORSE/WITHHOLD` lines + `SUMMARY`.

## ⚠️ BROKEN VARIANT: delib_f3_bin

`delib_f3_bin` withholds 8 of 12 b12_true items (BC05–BC12) at rung 2 — it does
NOT hold the true leg and must not be used as a clean H-D4 cell without a
prereg amendment. Per the task instructions this is reported as-is, NOT fixed
by tuning.

Mechanism note (no test items were used in design; this is post-hoc
description, not a fix): the withheld items are exactly the ones shaped
"The <frame> of <X> is <N>" with a content-word X (BC05–BC12), vs the endorsed
BC01–BC04 whose X is a single letter. F2 endorses all 12, and F3 at rung 0
(no learned profiles) also endorses 12/12 — so the break is a learned-profile
× slot-feature interaction, not a front-end bug. The distinguishing new
feature is `of_C` (bigram `of_<contentword>` with the content slot abstracted).
The spec's content-word definition (length ≥ 3 AND not in the exclusion list)
admits "the" (len 3, not excluded), so generic `of_the`/`of_<content>` frames
in some concept's rung-2 examples concentrate `of_C` with disc ≥ 750
(df_c dominant over the other six concepts' 2-example profiles) and a single
such feature already clears the score bar (w = prev·disc/1000 ≥ 750).
Consequence for the wave: the F3 spec as written leaks ultra-generic slot
features; any fix (e.g. extending the exclusion list) would be a design change
needing the wave coordinator's word — NOT applied here.
