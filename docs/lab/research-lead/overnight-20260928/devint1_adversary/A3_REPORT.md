# A3 Report: synergy reproduction (independent code)

Worker: DEVINT1 Adversary Worker B. Date: 2026-09-30.
Target: DEVINT1 builder commit `476c24b3d`, prereg `4b50ff7d4`.
Frozen criteria: `PREREG_ADVERSARY.md` (commit `60701a55f`), Attack A3.

## Method

`adv_synergy.zag` was written fresh from the frozen functional descriptions in
PREREG_DEVINT1.md (lexicon substring counts 2..4; DP segmentation maximizing
len*ilog(count+1) with longer-segment tie-break; concept table with recurrence
counts; rule table with support/refute states and dual eviction policies;
treatment/control procedure pairing tables; contradiction/inquiry/revision;
split-on-contradiction vs delete-only). Own buffer layout (separate buffers,
not the builder's single W arena), own function decomposition and naming; no
builder code copied. Same frozen episode corpora (S1 x12, S2 x6, S7
contradiction/boundary episodes, S10 flood x20, 10 held-out probe episodes,
S11 x6). Pure Zag, toolchain `znc 2026.07.0-dev`. 3/3 runs byte-identical.

## Results

| sub-claim | builder baseline | independent result | denominator check | frozen verdict |
|---|---|---|---|---|
| (a) proc examples-to-criterion | treat=4 ctrl=5 | treat=4 ctrl=5 | both reached 5/5 criterion (non-degenerate) | REPRODUCED (4<5) |
| (b) post-eviction probe, 10 held-out eps | treat=8/12 ctrl=0/12 | treat=8/12 ctrl=0/12 | 12 and 12 predictions (non-degenerate) | REPRODUCED (8>0) |
| (c) refinement count | treat=1 ctrl=0 | treat=1 ctrl=0 | 4 split candidates evaluated (non-degenerate) | REPRODUCED (1>0) |

Raw output: `A3_RAW.txt` (3 runs, byte-identical).

## Verdict

All three sub-claims reproduce with the same signs under an independent
implementation. Per the frozen criteria, overall **ATTACK-FAILS**: the three
synergy numbers are not artifacts of the builder's implementation choices.
They follow from the functional design (segmentation objective, dual eviction
policies, split-vs-delete refinement) on the frozen corpora.

Standing assumption retained: this says nothing about whether the synergy
would survive different corpora or stronger controls; that is A2/A4/A5
territory. The BUILD-PASS engineering result is not contested by this attack.
