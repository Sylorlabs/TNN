# Attack A5 Report: Delayed Transfer under Heavy Interference

Worker: DEVINT1 adversary, Worker C (attacks A5 + A6).
Date: 2026-09-30.
Target: DEVINT1, builder commit `476c24b3d`, prereg `4b50ff7d4`.
Frozen criteria: `PREREG_ADVERSARY.md` (commit `60701a55f`).
Toolchain: `znc 2026.07.0-dev (edition 2026)` (frozen path
`tnn-forkbattery-1121pdt/local-tnn-native-lab/znc`), `--no-analyze`
(analyzer lints only, no code change).

## Verdict: ATTACK-FAILS

Reuse survives 12x interference. Recognition 17/17 (>= 15/17) and
procedure reuse 3/3, frozen criteria for ATTACK-FAILS met exactly.

## Construction

`adv_delay.zag` = builder machinery (lines 1..825) byte-verbatim, S1..S9
main body (builder lines 829..1017) byte-verbatim, attack prelude
(`novel_morph` / `inter_ep`, new code), then 240 interference episodes,
then the S11 reuse battery (builder lines 1037..1057) byte-verbatim.
Verbatim claims checked with `diff` pre-commit. The builder S10 flood is
replaced by the interference section; everything else intact.

Interference design (per frozen prereg): 240 episodes = 12x the builder's
20, fed with `process_ep(W,s,9,1)` + `count_split_cands` (same feed
semantics as builder S10: mirror=1, policy 0 live / policy 1 SNAP twin).
Each episode is 3 novel 3-char morphemes (9 chars), indices
`(i*5)%12`, `(i*7+1)%12`, `(i*11+2)%12`, fully deterministic.

Disjoint inventory (12 morphemes): wex qiv vum jad (builder S10 flood
vocab, per prereg example) plus cfh nrs ysf hnc rfy shc fnr yhs (letters
{c,f,h,n,r,s,y}, zero shared characters with any builder string).
Zero overlap with bik/gup/zol/tav/bi/k verified: no morpheme equals any
of them, and none of the letters b,i,k,g,u,p,z,o,l,t,a,v appears, so no
cross-boundary window can form a target morpheme either. No
1-substitution neighbor of any true morpheme.

## Runs

3 runs, exit 0 each, zero stderr bytes, `cmp` byte-identical 3/3.
md5 `838ac398fa0975dd381762d4ce48693b`. Raw: `A5_RAW.txt`.

## Results (identical all 3 runs)

- S1..S9 section byte-identical to builder baseline:
  `STATE-CONT 9 8 17 65 888166382`, S6 treat=4 ctrl=5, held-out 5/5 both.
- `A5-INTERFERE 240 episodes, disjoint inventory` / `A5-INTERFERE-DONE`.
- `STATE-CONT 10 24 20 846 840445444` (concept table saturated at 24).
- `S11-RECOG 17/17`.
- `S11-PROC-REUSE 3/3`.
- `S3METRIC-REFINE treat=0 ctrl=0` (builder baseline: treat=1).
- `STATE-CONT 11 24 20 863 370038195`.
- `A5-SUMMARY recog=17/17 proc=3/3`.

## Grading against frozen criteria

- ATTACK-SUCCEEDS required recognition < 12/17 or procedure reuse < 2/3.
  Not met: 17/17 and 3/3.
- ATTACK-FAILS requires recognition >= 15/17 AND procedure reuse = 3/3.
  Met exactly. **ATTACK-FAILS.**

## Observations (not criteria)

- The concept table filled to capacity (24) under interference, yet the
  four true concepts were retained and segmentation still recovered all
  17 true morphemes in the S11 battery. The pairing table (S6) is
  untouched by interference episodes, so procedure reuse is structurally
  insulated in this design.
- The S3METRIC-REFINE treat count dropped 1 -> 0 under interference: the
  S9-installed split candidates (halves of violated concepts) never
  reached count 2 in the disjoint episodes, so `split_eval` retired
  nothing. This is the one S11-adjacent metric that did move, but it is
  outside the frozen A5 criteria and is reported here only as an
  observation.

## Purity

Pure Zag. Analysis via bash, znc, grep, cmp, md5sum only. No Python.
No em dashes in this document (byte-verified pre-commit).
