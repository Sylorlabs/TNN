# PROMOTION_VERDICT.md — deliberative magnifying-glass arm D promoted to live text-QA intake

Date: 2026-09-26. Branch: `tnn-native-lab`. Pure Zag, zero RNG.

## What was decided

The fork's deliberative rule-table arm **D is promoted** to TNN's live
text-QA intake path. Fixed arms **C (char), W (word), S (span) are retired
from production** and retained only as negative controls: on the money trap
("what is the 2nd letter of fox" / "the quick brown fox") they answered the
wrong question — C and S said `h` (the 2nd letter of the whole text), W needed
a fallback — that's their fault, they're out.

## Live-path choice

A search of the lab tree found **no other production text-QA chunking intake
path**: the only other "chunk" hits are MDL compression segments
(`units/arms/R/cl/arm.zag` — compression units, not a QA intake) and ledger
framing. The fork's exercised path `run_q -> d_answer` is therefore the
intake entry point. This is documented in `intake.zag`, which copies D's
`classify`, `d_choose`, `d_locate`, `mg_zoom`, and `d_answer` verbatim from
the frozen fork and runs **only arm D** over the original 24 questions.

`controls.zag` contains the fixed C/W/S battery arms only, marked
negative-controls-only and frozen/retired.

## Regression rerun (2026-09-26, after Phase 2 — binaries untouched, sources unchanged)

| run | n | correct | native | fallbacks | ops | zooms | SHA-256 |
|-----|---|---------|--------|-----------|-----|-------|---------|
| promotion run 1 | 24 | 24 | 24 | 0 | 190 | 12 | `25563035cdf8b1d9de0dd571445533edb7a3e1645d5a09ec54e94b4bf044d69e` |
| promotion run 2 | 24 | 24 | 24 | 0 | 190 | 12 | identical |

`# PROMOTION_RESULT PASS`. Both runs rc=0, byte-identical.

Retired controls reproduce the frozen baseline exactly (rc=0, byte-identical
across reruns, SHA-256 `5c9eea118441e93cf28bcadda101734c9fa36813acbabb9ab98a854652b1d23f`):

| arm | correct | native | fallbacks |
|-----|---------|--------|-----------|
| C (char) | 23/24 | 24/24 | 0 |
| W (word) | 24/24 | 6/24 | 18 |
| S (span) | 23/24 | 2/24 | 22 |

## Money-trap trace (q22, promoted path)

```text
Q 22 kind=POSITION q="what is the 2nd letter of fox" t="the quick brown fox" exp="o"
D qid=22 kind=POSITION chunk=WORD>CHAR ...
D zoom qid=22 span=1 parent=0 off=16 len=3 depth=1 why=locate-target-word
D zoom qid=22 span=2 parent=1 off=17 len=1 depth=2 why=index-character-inside-word
```

D locates `fox`, zooms to its second character, answers `o`.

## Pre-existing verdict coverage

No applicable pre-existing chunking/intake verdict exists: the representation
line's `units/arms/R/cl/arm.zag` is MDL compression segmentation, not a
text-QA intake. The fork's original 24-question battery (`VERDICT.md`,
`evidence/RUN_R1.out` / `RUN_R2.out`) is the direct regression, rerun above.

## Files

- `intake.zag` — promoted D-only live path (D's functions verbatim from the fork)
- `controls.zag` — retired C/W/S, negative controls only
- `build_promotion.sh` — build script
- `evidence_promotion/RUN_P1.out`, `RUN_P2.out` — promotion runs (PASS)
- `evidence_promotion/RUN_C1.out`, `RUN_C2.out` — retired-control runs

Build binaries (`intake_bin`, `controls_bin`) and `build_promotion.log` are
local intermediates and are **not** committed.
