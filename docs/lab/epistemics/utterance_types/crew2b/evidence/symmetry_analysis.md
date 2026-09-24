# Evidence: firing-pattern symmetry (critical pair)

Instrumented build `h7_dbg.zag` (scratch only): prints every marker firing and
the scored item it attaches to. `dbg2.txt` additionally dumps all live markers
at end (`MARK|concept|field|status|support|bytes`).

## All 33 hypothetical live markers are provisional, support 1

```
$ grep "^MARK|2|" dbg2.txt | awk -F'|' '{print $4"/"$5}' | sort | uniq -c
     33 1/1
```

Same for joke (52 markers) and every other concept: **no support/conflict
asymmetry exists anywhere.** (The learner returns early on correct predictions
without reinforcing matching markers, so support never exceeds 1. Repairing
this would act symmetrically — see IMPOSSIBILITY_PROOF.md §4.)

## The 7 hypothetical SINC-LK misses: lone content-marker fires

| Item | n | f0 (content) | f1 (frame) | Marker |
|------|---|--------------|------------|--------|
| si3_12 "What time do we leave?" | 1 | 1 | 0 | `do we` (hyp) |
| si3_13 "I wonder if the mail came." | 1 | 1 | 0 | `if the` (hyp) |
| si3_14 "Ask if the shop is open." | 1 | 1 | 0 | `if the` (hyp) |
| si3_15 "It is as if winter came early." | 1 | 1 | 0 | `it is` (joke) |
| si3_16 "See if the door is locked." | 1 | 1 | 0 | `if the` (hyp) |
| si3_18 "Check if the oven is off." | 1 | 1 | 0 | `if the` (hyp) |
| si3_20 "We will see if they reply." | 1 | 1 | 0 | `if the` (hyp) |

All have CTX `says evenly` / `says plainly` (assertoric frame, no learned
frame markers fire).

## The joke-deadpan items that must stay WITHHOLD: identical pattern

| Item | n | f0 | f1 | Marker |
|------|---|---|----|--------|
| no2_05 "Why did my bed become magical? ..." | 1 | 1 | 0 | `why did` (joke) |
| (+ 14 more deadpan no2 items, same shape) | | | | |

## Hypothetical's live marker inventory (concept 2, 33 total)

Content (27): `do we`, `do we move`, `fails this`, `fails this season`,
`floods, where`, `floods, where do`, `harvest fails`, `harvest fails this`,
`if the`, `if the harvest`, `move the`, `move the market`, `river floods`,
`river floods, where`, `suppose that`, `suppose that the`, `that the river`,
`the harvest`, `the harvest fails`, `the river floods`, `this season`,
`we move`, `we move the`, `what if`, `what if the`, `where do`, `where do we`

Frame (6): `aloud`, `musing`, `musing quietly`, `quietly`, `thinking`,
`thinking aloud`

Note: the sincere lookalikes fire **only** the semantically bleached markers
(`if the`, `do we`) — never the suppositional anchors (`suppose that`,
`what if`) — but the anchors' absence is not observable *as* absence by a
generic rule without conditioning on marker identity.

## Sentence-count check (structural feature)

- sinc3-LK (all 10): exactly 1 sentence each
- tr3 genuine hypothetical (all 20): exactly 1 sentence each
- no2 joke: mixed (13×2, 4×1, 2×4, 1×5 sentences)

No utterance-structural feature separates sincere lookalikes from genuine
hypotheticals.
