# PREREG H-FDCR-UNIFIED5 FROZEN

**Date:** 2026-09-29
**Researcher:** H-FDCR-UNIFIED5 Frontier Researcher (independent subagent)
**Target:** H-FDCR-UNIFIED4 SURVIVES (32/32); red team SURVIVES all
  attacks with one confirmed BOUNDARY (FDCR_UNIFIED4_ADV_RESULT.md,
  X-FU4-2): NOADD table exhaustion at 32 entries loses a vote
  loudly (one WARN) and the lost vote demonstrably flipped a
  procedure outcome (train_con -1 vs 0), with only the earlier
  WARN as signal. Residual observations: (2) the absorbed
  concept's stale member/feature lists are not cleared on merge
  (verified safe by code reading, invisible while inactive);
  (3) the combined stress case (merge overflow into an already
  full NOADD table) was not run.
**Status:** FROZEN. Implementation must strictly follow this prereg.
**Toolchain:** znc 2026.07.0-dev (edition 2026). Pure Zag. No Python anywhere.

## Hypothesis

The X-FU4-2 boundary can be closed at the mechanism level: the
procedure layer can explicitly surface vote-exhaustion, so a
train_con computed without lost votes no longer reads as "no
concept applied". Residual (2) can be removed by clearing the
absorbed concept on merge. Residual (3) becomes a frozen test.
None of this changes any frozen K-FU4 behavior: in all FU4
fixtures the NOADD table never fills (max 8 NOADD entries in
E-T3), so no new output lines fire there, and clearing an
inactive concept's lists is output-invisible.

## Repairs (frozen)

Implementation file: `unified_fdcr5.zag` = `unified_fdcr4.zag`
copied verbatim (cmp-verified), then the changes below only.
`unified_fdcr4.zag` is NOT modified.

### R1: vote-exhaustion drop tracking + procedure-layer NOTE

Memory (all below WORK=4096, which is untouched):
- NOADD_DROP_COUNT()=2668: one i32, total number of subjects
  whose NOADD vote recording was refused because the table was
  full. The NOADD table ends at 2412+32*8=2668, so this is the
  first free address.
- NOADD_DROP_BASE()=2672: 64 entries of 4 bytes (subject string
  offsets of dropped subjects), ending at 2928.
- NOADD_DROP_MAX()=64.

New functions (frozen contracts):

- `noadd_drop_init(W)`: set32(W, NOADD_DROP_COUNT(), 0); set all
  64 list entries to -1. Called from `noadd_init` (which is
  called once per workspace from `con_init`).
- `noadd_drop_record(W, mem_off)`: increment the total counter;
  if a list entry holds -1, store mem_off in the first such
  entry. The total counter is authoritative; the list is
  best-effort naming for up to 64 dropped subjects.
- `noadd_drop_total(W)`: return the total counter.
- `noadd_vote_lost(W, s)`: return 1 if s is content-equal to
  any recorded drop-list subject offset, else 0. This
  distinguishes "vote lost to exhaustion" from "never voted":
  a subject whose feature set matched no concept returns
  con_vote_concept=-1 and noadd_vote_lost=0.

Call sites (frozen):

- In `noadd_record`, on the table-full path: call
  `noadd_drop_record(W, mem_off)` immediately BEFORE the
  existing `WARN NOADD vote table full` emit. Nothing else in
  `noadd_record` changes. This covers both the con_form
  MATCH-NOADD path and the con_merge_into overflow path, since
  both funnel through `noadd_record`.
- In `handle_proc_learn_unified`, immediately after
  `if(best_cnt*2>nseg){train_con=best_con;}`: count nlost =
  number of training inputs vi with vil>0 where
  con_vote_concept(W,vstr)<0 AND noadd_vote_lost(W,vstr)==1.
  If nlost>0, emit exactly:
  `ULEARN: NOTE <nlost> train input(s) lost concept votes (NOADD table full); train_con computed without them`
  followed by newline. The emit fires regardless of the rc
  branch (direct, bridge, or fail), because the vote loss is a
  property of the training inputs, not of the learned program.

### R2: absorbed-concept hygiene on merge

In `con_merge_into` Step 4, after `con_set_active(W,c2,0);`
add `con_set_nmem(W,c2,0);` and `con_set_nfeat(W,c2,0);`.
Rationale: the absorbed concept's stale member/feature lists
become invisible garbage; clearing them removes the hazard
class entirely. Safe: every reader gates on
con_active(W,c)==1 (verified in the X-FU4-4 source audit);
the create path already resets nfeat, features, mem[0], nmem
on slot reuse. No output change.

### R3: PART F tests in main()

Append PART F after PART E. New worlds each start from a fresh
workspace (set32 ST_STR, intent_init, con_init). Banner lines:
`\n=== PART F: H-FDCR-UNIFIED5 (vote-exhaustion signal, merge hygiene) ===\n`
and
`=== H-FDCR-UNIFIED5 repairs: NOADD drop tracking, procedure NOTE, absorbed-concept clearing ===\n`.

- F-T1 (K-FU5-1, vote-exhaustion surfaced): the exact red-team
  T2a+T2b world. 41 subjects s1..s41, one `is_a=pet` fact each,
  in batches of 16/16/9. Then `T zz | color | orange` (C1).
  Then procedure `s1>1s;zz>zz;s41>14s` (all reversals; direct
  discovery). PASS requires, all asserted in code:
  con_count==2; train_con==-1 (read from the intent record);
  con_vote_concept("s1")==0; con_vote_concept("s41")==-1;
  noadd_vote_lost("s41")==1; noadd_vote_lost("s1")==0;
  noadd_drop_total()==1. External grep on raw: exactly one
  `WARN NOADD vote table full; subject will not vote` line and
  the NOTE line
  `ULEARN: NOTE 1 train input(s) lost concept votes (NOADD table full); train_con computed without them`.
- F-T2 (K-FU5-2, merge overflow into a full table): F-T1's
  41-subject world WITHOUT the zz/C1 part (drop total=1 from
  s41). Then 8 subjects m1..m8, each
  `T mN | is_a | pet;T mN | color | orange` (C1, 8 members).
  Then `T s1 | color | orange` (extends C0 to 2 feats; merge
  fires; C1's 8 members overflow the full NOADD table).
  Then procedure `m1>1m;s1>1s`. PASS requires, all asserted
  in code: con_count==1; noadd_drop_total()==9;
  noadd_vote_lost("m1")==1; con_vote_concept("m1")==-1;
  con_vote_concept("s1")==0; train_con==-1. External grep on
  raw: one `CONCEPT-MERGE 1 into 0` line; exactly nine
  `WARN NOADD vote table full; subject will not vote` lines;
  at least one NOTE line naming vote loss.
- F-T3 (K-FU5-3, absorbed-concept hygiene): the exact E-T1
  world (X-FU3-1A attack order). After the merge: PASS
  requires con_count==1; cat and dog in concept 0;
  train_con==0 for `cat>tac;dog>god`; AND con_active(1)==0,
  con_nmem(1)==0, con_nfeat(1)==0 (the absorbed concept's
  lists are cleared). External grep: one
  `CONCEPT-MERGE 1 into 0` line.
- F-T4 (K-FU5-4, regression): re-run the E-T1..E-T5 PASS
  criteria verbatim on fresh worlds (5 named checks). AND
  Parts A-E program output must be byte-identical to the
  committed FDCR_UNIFIED4_RAW.txt except for the appended
  PART F block (verified externally by diff). Rationale: no
  FU4 fixture ever fills the NOADD table (max 8 NOADD entries
  in E-T3), so no NOTE line can fire in Parts A-E; R2's
  clearing touches only inactive concepts and is
  output-invisible.

### R4: documentation

The result doc lists: the drop counter and 64-entry drop list
(addresses 2668..2928), the NOTE contract (fires iff at least
one training input lost its vote to a full table; names the
count, never asserts membership), the absorbed-concept
clearing, and the unchanged caps.

## Kill bars (frozen)

- **K-FU5-1 (vote-exhaustion surfaced):** F-T1 PASS: the
  pivotal -1 outcome now carries an explicit NOTE naming the
  lost vote; noadd_vote_lost distinguishes s41 (lost) from s1
  (voting) and from never-voting subjects.
- **K-FU5-2 (merge overflow into full table):** F-T2 PASS: 8
  merge-overflow members dropped into the full table are all
  tracked (drop total 9), the NOTE fires on the subsequent
  procedure learn, no stale references.
- **K-FU5-3 (absorbed-concept hygiene):** F-T3 PASS: absorbed
  concept deactivated with nmem=0 and nfeat=0; merge behavior
  otherwise unchanged (1 concept, train_con=0).
- **K-FU5-4 (regression):** F-T4 PASS: all 32 FU4 named checks
  hold verbatim; Parts A-E byte-identical to
  FDCR_UNIFIED4_RAW.txt except the appended PART F block.
- **K-FU5-5 (determinism):** 3 consecutive full runs
  byte-identical (cmp).

Final tally target: 40/40 (32 FU4 checks + 8 new: F-T1, F-T2,
F-T3, and the 5 re-run E-T1..E-T5 criteria).

## Classification target

Bounded L2 integration repair. No L3 claimed. The caps remain;
the NOTE is a diagnostic, not an enlarged capacity.

## Governance

- This prereg commit contains ONLY this file. Implementation
  follows in a later commit with a strict-ancestor relationship
  (verified via merge-base --is-ancestor before the result
  commit lands).
- Pure Zag. No Python at any stage: fixtures, harness, builds,
  runs, greps, md5.
- Only owned files staged/committed (pathspec-restricted). No
  other worker's files touched. No binaries committed (builds
  in /tmp only).
- No em dashes in loop documentation.
- On .git/index.lock contention: wait for the live lock to
  clear; never remove it while workers may be active.
