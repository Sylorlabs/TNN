# PREREG H-FDCR-UNIFIED4 RED TEAM FROZEN

**Date:** 2026-09-29
**Researcher:** H-FDCR-UNIFIED4 Red Team (independent subagent)
**Target:** H-FDCR-UNIFIED4 SURVIVES (32/32). Repairs: R1 NOADD vote
  table (32 entries, MATCH-NOADD subjects vote via
  con_vote_concept), R2 post-extension concept merge
  (con_merge_check / con_merge_into, member move with 8-cap,
  overflow to NOADD, NOADD remap, intent-record remap over all 20
  slots, deactivation, CONCEPT-MERGE emit).
**Status:** FROZEN. Attacks execute exactly as specified below.
**Toolchain:** znc 2026.07.0-dev (edition 2026). Pure Zag.
  No Python anywhere: fixtures, harness, builds, runs, greps,
  md5, cmp.

## Hypothesis under attack

The H-FDCR-UNIFIED4 repair claim: both X-FU3-1 (extension-path
order fragility) and X-FU3-2 (member-cap vote splitting) are
closed at the mechanism level, with no silent evidence loss and
no regressions. I assume this claim is false and attack it.

## Attack harness

`fdcr_unified4_adv.zag` = lines 1-1891 of the committed
`unified_fdcr4.zag` (everything before `fn main`, i.e. the full
mechanism) copied byte-verbatim (cmp-verified), plus a new
`main()` containing only the attack worlds below. Each world
starts from a fresh workspace (`z_alloc(65536)`, `set32 ST_STR`,
`intent_init`, `con_init`). No mechanism line is modified.

## Attacks (frozen)

### X-FU4-1: merge chains and merge-then-extend cycles

- **T1a (three-concept chain).** Fresh world. Batch1:
  `T sa | is_a | pet` (C0={is_a=pet}). Batch2:
  `T sb | is_a | pet;T sb | color | orange` (C1, 2 feats).
  Batch3: `T sc | is_a | pet;T sc | color | orange;T sc | size | big`
  (C2, 3 feats). Batch4: `T sa | color | orange` (extend C0,
  expect CONCEPT-MERGE of C1 into C0). Batch5:
  `T sa | size | big` (extend C0, expect CONCEPT-MERGE of C2
  into C0). Assertions: con_count==1; con_find_member_str of
  "sa","sb","sc" all == 0; exactly 2 CONCEPT-MERGE lines in raw
  output; procedure `sa>as;sb>bs;sc>cs` learns train_con=0.
- **T1b (same-batch order, both orders).** Fresh world per
  order. Setup batch: `T olda | is_a | pet` (C0).
  Order-1 batch: `T nu | is_a | pet;T nu | color | orange;T olda | color | orange`
  (new subject first: con_form creates, then extension merges).
  Order-2 batch: `T olda | color | orange;T nu | is_a | pet;T nu | color | orange`
  (extension first, then con_form matches). Assertions (both
  orders): con_count==1; "nu" and "olda" in the same concept;
  procedure `olda>adlo;nu>un` learns train_con=0.
- **T1c (two extensions in one batch converge).** Fresh world.
  Setup batch1: `T s1 | is_a | pet` (A={is_a=pet}, member s1).
  Setup batch2: `T s2 | kind | animal` (B={kind=animal},
  member s2). Two distinct 1-feat concepts.
  Attack batch: `T s1 | kind | animal;T s2 | is_a | pet`.
  s1 extends A to {is_a=pet,kind=animal}; merge_check finds
  no match (B has 1 feat). s2 extends B to
  {kind=animal,is_a=pet}; merge_check: A matches by
  set-identity -> merge A into B (ci=B, the extended one).
  Assertions: con_count==1; s1 and s2 in the same concept;
  procedure `s1>1s;s2>2s` learns train_con=0; exactly one
  CONCEPT-MERGE line.
- **Kill criterion X-FU4-1:** after any attack sequence, two
  ACTIVE concepts hold set-identical feature sets (the X-FU3-1
  class recurs), OR con_count differs between the two batch
  orders on the identical total fact set, OR any fixture
  subject votes -1 / is not a member while its feature set
  matches an active concept (evidence lost).

### X-FU4-2: NOADD table exhaustion at 32 entries

- **T2a (fill and overflow).** Fresh world. 41 subjects
  w01..w41, one fact each `T wNN | is_a | pet`, fed as three
  concept-learn batches (16/16/9; 16 facts/batch cap).
  Assertions: con_count==1; con_nmem==8;
  con_vote_concept("w01")==0 (member);
  con_vote_concept("w32")==0 (NOADD vote);
  con_vote_concept("w41")==-1 (vote lost);
  raw output contains exactly one
  `WARN NOADD vote table full` line.
- **T2b (pivotal flip).** Same world as T2a plus a second
  concept: batch `T s2 | color | orange` (C1, member s2).
  Procedure `w01>10w;s2>2s;w41>14w` (all reversals; direct
  discovery). Vote math: w01 votes 0, s2 votes 1, w41 lost
  (-1). best_cnt=1 for both 0 and 1; 1*2=2 > 3 false, so
  train_con==-1. Counterfactual recorded in prereg: had w41's
  vote counted (concept 1), best_cnt=2, 2*2=4 > 3 true,
  train_con==1. Assertion: train_con==-1 AND the WARN fired
  (loud). This attack distinguishes KILL from BOUNDARY:
  missing/misleading WARN = KILL-class; WARN present with the
  flip = confirmed disclosed residual = BOUNDARY.
- **Kill criterion X-FU4-2:** the 33rd NOADD subject is
  dropped with NO `WARN NOADD vote table full` line (silent
  loss), OR con_vote_concept("w41")!=-1 (vote silently kept
  despite the WARN), OR the table-full path corrupts an
  unrelated vote.

### X-FU4-3: intent records on the survivor concept during merge

- **T3a (proc records across the merge).** Fresh world.
  Batch1: `T pa | is_a | pet;T pb | is_a | pet`
  (C0={is_a=pet}, members pa,pb).
  Batch2: `T qa | is_a | pet;T qa | color | orange;T qb | is_a | pet;T qb | color | orange`
  (C1={is_a=pet,color=orange}, members qa,qb).
  Learn P1=`qa>aq;qb>bq`: rc1>=0, read concept at
  IBASE()+rc1*12+8, assert ==1.
  Learn P2=`pa>ap;pb>bp`: rc2>=0, concept at
  IBASE()+rc2*12+8, assert ==0.
  Batch3: `T pa | color | orange` (extend C0 -> merge C1
  into C0).
  Assertions: CONCEPT-MERGE 1 into 0 in raw output;
  P1's record concept now ==0 (remapped);
  P2's record concept still ==0 (survivor untouched);
  con_count==1; proc_apply of P1 on "qa" still gives "aq"
  and P2 on "pa" still gives "ap" (procedures intact).
- **T3b (NOADD remap across the merge).** Fresh world.
  Batch1: eight subjects d0..d7, each
  `T dN | is_a | pet;T dN | color | orange;T dN | size | big`
  (C1: 3 feats, 8 members; 16 facts = 2 batches of 8 facts).
  Batch2: `T d8 | is_a | pet;T d8 | color | orange;T d8 | size | big`
  (d8 MATCH-NOADD; assert noadd_find("d8")==1).
  Batch3: `T cat | is_a | pet;T cat | color | orange`
  (C0: 2 feats).
  Batch4: `T cat | size | big` (extend C0 -> merge).
  Assertions: noadd_find("d8")==0 after merge;
  con_vote_concept("d8")==0; no NOADD entry references
  concept 1 (scan all 32: no entry with concept==1).
- **Kill criterion X-FU4-3:** after the merge, any intent
  record (proc slots 0..15 or bridge slots 0..3) still
  references the deactivated concept index, OR any NOADD
  entry still references it, OR a pre-merge procedure no
  longer applies correctly.

### X-FU4-4: regression and source audit

- **T4a (rebuild).** Rebuild the committed
  `unified_fdcr4.zag` unmodified with znc; run; md5 of
  program output must equal
  `0cce903c554697b72e70b21008f6bc42` (the frozen
  FDCR_UNIFIED4_RAW.txt hash).
- **T4b (prior fixtures).** In the attack harness (copied
  mechanism), re-run the exact X-FU3-1A attack order, the
  X-FU3-1B control order, and the exact X-FU3-2 16-subject
  fixture; assert con_count==1 and train_con==0 in all
  three (the H-FDCR-UNIFIED4 headline claims).
- **T4c (source audit).** Verify by reading: (i)
  noadd_record's AMEND1 defensive check is scoped to the
  TARGET concept only; (ii) con_merge_into performs steps
  1-5 in order (member move with 8-cap, overflow to NOADD
  with WARN, noadd_remap, 20-slot intent remap,
  deactivation, CONCEPT-MERGE emit); (iii) the voter in
  handle_proc_learn_unified uses con_vote_concept at BOTH
  call sites and con_find_member_str keeps member-only
  semantics on the intent query path; (iv) no test-answer
  literals in mechanism regions; (v) merge_check is called
  exactly at the end of the extension branch.
- **Kill criterion X-FU4-4:** rebuilt output md5 differs,
  any prior fixture regresses, or any prereg-contract (R1-R4
  of PREREG_FDCR_UNIFIED4.md) deviation is found in source.

## Verdict rule

- Any KILL criterion met -> H-FDCR-UNIFIED4 is DOWNGRADED
  (claim narrowed) or KILLED (mechanism broken), per the
  severity: silent evidence loss or wrong-confident
  procedure learning = DOWNGRADE at minimum; failure of the
  two headline repairs on their own fixtures = KILL.
- X-FU4-2 T2b with WARN present = BOUNDARY (disclosed
  residual confirmed with a concrete pivotal case), not a
  kill.
- All attacks fail -> H-FDCR-UNIFIED4 SURVIVES this red team.

## Governance

- This prereg commit contains ONLY this file, committed
  BEFORE any attack fixture, harness code, build, or run.
- Pure Zag. No Python at any stage.
- Only adversary-owned files staged/committed
  (pathspec-restricted). No other worker's files touched.
  No binaries committed (builds in /tmp only).
- No em dashes in loop documentation.
- On .git/index.lock contention: wait for the live lock to
  clear; never remove it while workers may be active.
