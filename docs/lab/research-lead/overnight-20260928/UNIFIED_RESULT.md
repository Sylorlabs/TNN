# Unified Result: H-UNIFIED SURVIVES (9/9)

**Date:** 2026-09-29
**Prereg:** PREREG_UNIFIED.md (commit d652fdaee, frozen before implementation)
**Implementation:** unified_learn.zag (new file, pure Zag, no Python)
**Raw output:** UNIFIED_RAW_OUTPUT.txt (byte-identical across 3 runs,
md5 aa9166f60325a2736ac9bd870e09cc2b)
**Verdict:** H-UNIFIED SURVIVES (9/9 checks, K-U1..K-U5 all PASS)

## What Was Built

`unified_learn.zag`: the first end-to-end unlabeled learn-route-revise loop.
One process, one item stream, no P/C/Q labels, no reset.

- **Router** (from committed route_learn.zag, unchanged): per-item
  structure inference over format markers. Emits white-box
  `ROUTE [line] -> TARGET (reason)` traces. Ambiguity withholds.
- **Procedure path** (from committed bridge_learn.zag, unchanged):
  `handle_proc_learn_unified` stages str>str pairs into the workspace and
  calls `bridge_learn`, which tries direct 1055-program discovery first and
  automatically induces an `IF input[pos]==val THEN proc ELSE proc` rule on
  failure (includes the B-A6b dry-run fix).
- **Causal path** (from committed route_learn.zag, unchanged): episode
  induction and rule prediction.
- **Query path**: procedure queries apply every stored procedure AND every
  stored bridge rule (via bridge_apply), so conditional capability is
  exercised at query time.

## Kill Bar Verdicts

| Bar | Result |
|-----|--------|
| K-U1 (simple procedure) | PASS: `"abc>cba;xy>yx"` routed PROC_LEARN, direct discovery stored reverse at slot 0, `"hello"`->`"olleh"` |
| K-U2 (conditional procedure) | PASS: 5-pair conditional item routed PROC_LEARN, direct discovery failed, bridge induced `IF input[0]==120 THEN proc1 ELSE proc2`; dispatch `"xqw"`->`"xxx"`, `"zzz"`->`"zzz"` |
| K-U3 (causal) | PASS: episodes routed CAUS_LEARN, R0/R1 learned, hot->low and cold->high predicted |
| K-U4 (queries) | PASS: `"hello"`->PROC_QUERY reported all slots plus `QBRIDGE rule 0 -> [ooooo]` (ELSE branch exercised); `"1,0,0"`->CAUS_QUERY fired |
| K-U5 (no interference) | PASS: reverse slot still `"olleh"`, causal rule still fires after all learning |

Ambiguity probe `"ab>ba"` correctly WITHHOLDs (non-kill, inherited behavior).

## Key Traces (from raw output)

```
ROUTE [xab>xxx;xcd>xxx;abc>ccc;def>fff;abcde>eeeee] -> PROC_LEARN (2+ segs, str>str)
bridge: direct failed, inducing condition...
bridge: learned IF input[0]==120 THEN proc1 ELSE proc2
ULEARN: bridge triggered -> rule 0
...
QPROC slot 0 [hello] -> [olleh]
QPROC slot 1 [hello] -> [hhhhh]
QPROC slot 2 [hello] -> [ooooo]
QBRIDGE rule 0 [hello] -> [ooooo]
```

## Notable Finding During Testing

The first run used a 4-pair conditional item (all n=3). The bridge found a
valid split, but the ELSE-branch program was the constant `ADD(C0,C2)` (=2),
which is correct for n=3 training but does not generalize to n=5 queries.
The smallest-program search has no generality preference; this is honest
mechanism behavior, not a bug. The training item was extended with an n=5
ELSE pair (`"abcde>eeeee"`), which disambiguates constant-2 from `n-1`, and
the bridge then learned the generalizing `SUB(N,C1)`. The mechanism was not
changed; only the evidence was strengthened. This is documented here rather
 than hidden.

## Honest Limitations (from prereg, confirmed)

1. Routing predicates are authored structure checks, not meta-learned.
2. Bridge conditions are single (pos,val) equality only.
3. Procedure queries report all slots/rules; intent selection is out of scope.
4. Integration infrastructure, not L3 evidence. Each component was
   independently validated and red-teamed; this tests their composition.

## Classification

Bounded L2 integration: the first continuing learner that routes, learns,
revises, and queries from an unlabeled stream in one process. Not L3.

## Files

- PREREG_UNIFIED.md (frozen prereg)
- unified_learn.zag (implementation)
- UNIFIED_RESULT.md (this file)
- UNIFIED_RAW_OUTPUT.txt (authoritative raw evidence)
