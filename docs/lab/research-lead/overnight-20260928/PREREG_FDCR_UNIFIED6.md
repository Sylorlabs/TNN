# PREREG H-FDCR-UNIFIED6: Honest Vote-Exhaustion Envelope

**Date:** 2026-09-29
**Researcher:** H-FDCR-UNIFIED6 Frontier Researcher (independent subagent)
**Target:** H-FDCR-UNIFIED5 SURVIVES (40/40). Prereg `1813a6547`, result `e28a9c430`.
  Red team SURVIVES (3 fail, 1 succeeds as CONFIRMED DISCLOSED BOUNDARY).
**Hypothesis:** The vote-exhaustion signal can be made honest about its
  envelope: (1) dedup the drop list so the bound is genuinely 64 distinct
  subjects (not 64 drop events), and (2) track overflow distinctly so the
  procedure layer can distinguish "vote certainly lost" from "vote status
  uncertain due to tracking exhaustion," closing the B1 silence hole.

## Background

X-FU5-2 confirmed: `noadd_drop_record` appends with no dedup, so the
64-entry name list fills at 64 drop EVENTS, not 64 distinct subjects.
World C: 2 distinct subjects (`rep`, `v`) in 70 batches produced 71 drop
events, exhausting the list; `noadd_vote_lost("v")==0` though v's vote was
genuinely lost. World B B1: d70 (70th distinct subject) beyond capacity;
`noadd_vote_lost("d70")==0`, nlost==0, ZERO NOTE lines on a pivotal
train_con=-1. The vote-loss signal goes completely silent past the
envelope.

The FU5 disclosure claims "64 distinct subjects." Dedup makes this true.
The overflow distinction makes the silence honest.

## Repairs (frozen)

**R1: Drop-list dedup + overflow counter.**
`noadd_drop_record(W, mem_off)`:
- Increment NOADD_DROP_COUNT (authoritative total) always.
- Scan the 64-entry name list for content-equal subject. If found,
  return (dedup: no new slot consumed).
- Else if an empty slot exists, append mem_off there.
- Else (list full, new distinct subject): increment NOADD_DROP_OVERFLOW.

New memory: NOADD_DROP_OVERFLOW (one i32, after NOADD_DROP_COUNT).
New function `noadd_drop_overflow(W)` returns it.
`noadd_drop_init` zeroes both.

**R2: Honest procedure-layer NOTE.**
In `handle_proc_learn_unified`, after computing nlost (unchanged:
inputs with con_vote_concept<0 AND noadd_vote_lost==1):
- If nlost>0: emit `ULEARN: NOTE N train input(s) lost concept votes
  (NOADD table full; T total drops); train_con computed without them`
  where T = noadd_drop_total(W). (Supersedes the FU5 NOTE wording by
  appending the authoritative total; the nlost count semantics are
  unchanged.)
- Else if noadd_drop_overflow(W)>0 AND exists input with
  con_vote_concept(W,lstr)<0: emit `ULEARN: NOTE vote status uncertain
  for some train input(s) (NOADD drop name capacity exceeded; T total
  drops, O beyond name capacity); train_con may exclude lost votes`
  where O = noadd_drop_overflow(W). This closes the B1 silence: the
  -1 no longer reads as "no concept applied" without signal.

**R3: PART G tests** (G-T1..G-T4) appended after PART F. The
H-FDCR-UNIFIED5 banner lines are preserved so Parts A-F stay
byte-comparable (Parts A-E have zero NOTE lines; Part F NOTEs use the
new wording, documented as supersession).

## Frozen kill bars

**K-FU6-1 (dedup: bound genuinely per-subject):** G-T1 replays X-FU5-2
World C: 70 batches of `T rep | is_a | pet` (cross-batch, no intern
dedup) + `T v | is_a | pet`. Requires: noadd_drop_total()==71,
name list holds exactly 2 distinct entries, noadd_vote_lost("rep")==1,
noadd_vote_lost("v")==1, noadd_drop_overflow()==0. (Under FU5:
vote_lost("v")==0.)

**K-FU6-2 (overflow NOTE closes B1 silence):** G-T2 replays X-FU5-2
World B: 40 subjects then d1..d70 (70 distinct). Requires:
noadd_drop_total()==70, noadd_drop_overflow()==6 (d65..d70 beyond 64
distinct). Procedure `s1>1s;d70>07d`: train_con==-1 AND the uncertain-
vote NOTE fires (contains "vote status uncertain" and "70 total drops").
(Under FU5: zero NOTE lines.)

**K-FU6-3 (preserved/superseded):** All K-FU5-1..K-FU5-4 PASS with the
following explicit supersessions: (a) K-FU5-1 F-T1 NOTE wording now
includes "; 1 total drops" (nlost==1, total==1, overflow==0); (b) K-FU5-2
F-T2 NOTE wording now includes "; 9 total drops" (nlost>=1, total==9,
overflow==0); (c) Parts A-E output byte-identical to FU5 (zero NOTEs
there); (d) Part F non-NOTE lines byte-identical. K-FU5-4 regression:
40/40 original checks (with updated NOTE expectations) + G-T1..G-T4.

**K-FU6-4 (deterministic):** 3 consecutive full runs byte-identical
(cmp), exit 0, 0 FAIL lines.

## Governance

- Prereg committed alone BEFORE any implementation edit, build, or run.
- `unified_fdcr6.zag` = `unified_fdcr5.zag` copied verbatim
  (cmp-verified) plus exactly the frozen R1-R3 changes.
  `unified_fdcr5.zag` untouched.
- Pure Zag throughout: fixtures, implementation, builds, runs, greps,
  md5, cmp. Zero Python at any stage.
- No binaries committed (builds in /tmp/fu6 only).
- Only owned files staged/committed (pathspec-restricted).
- No em dashes in loop documentation.
- Mechanism diff vs unified_fdcr5.zag must show zero non-comment lines
  removed (additive + the two small R1/R2 modifications, disclosed).

## Classification

Bounded L2 integration repair (honest signaling). Not L3. The 64-name
capacity remains; the improvement is that the bound is now genuinely
per-subject and the envelope edge is signaled rather than silent.
