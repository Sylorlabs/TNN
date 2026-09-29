# PREREG H-FDCR-UNIFIED5 RED TEAM FROZEN

**Date:** 2026-09-29
**Researcher:** H-FDCR-UNIFIED5 Red Team (independent subagent)
**Target:** H-FDCR-UNIFIED5 SURVIVES (40/40). Commits: prereg `1813a6547`,
  result `e28a9c430`. Mechanism: `unified_fdcr5.zag` (worktree verified
  byte-identical to HEAD).
**Status:** FROZEN. No attack code written before this prereg commits.
**Toolchain:** znc 2026.07.0-dev (edition 2026). Pure Zag. No Python anywhere.
**Assumption:** the H-FDCR-UNIFIED5 repair claim is false. Attack it.

## Target claims under test

- R1: vote-exhaustion is surfaced at the procedure layer. `noadd_drop_record`
  tracks every refused vote (total counter at 2668, 64-entry name list at
  2672). `handle_proc_learn_unified` emits
  `ULEARN: NOTE N train input(s) lost concept votes (NOADD table full); train_con computed without them`
  iff at least one training input has `con_vote_concept<0` AND
  `noadd_vote_lost==1`. A subject that never voted returns
  `noadd_vote_lost==0` and must NOT trigger the NOTE.
- R2: `con_merge_into` Step 4 clears the absorbed concept
  (`active=0`, `nmem=0`, `nfeat=0`). Claimed safe: every reader gates on
  `active==1`; the create path resets on slot reuse.
- R3: merge overflow into a full NOADD table is tracked (F-T2).
- K-FU5-4: Parts A-E byte-identical to FDCR_UNIFIED4; mechanism diff
  purely additive.

## Method

Adversary harness `fu5_adv.zag`: lines 1-1973 of the committed
`unified_fdcr5.zag` copied verbatim (the full mechanism region;
`fn main` starts at line 1974), cmp-verified byte-identical, with `main`
replaced by attack drivers. No mechanism edits. Each empirical attack runs
3x; all runs must be byte-identical or the attack is void.

## X-FU5-1: NOTE spoof / suppression

Question: can the NOTE fire when no vote was lost (spoof), or fail to fire
when a training input genuinely lost its vote (suppression, within the
disclosed 64-event design envelope)?

World A (fresh workspace per the frozen pattern: z_alloc 65536,
ST_STR=STR0, intent_init, con_init):
- `handle_concept_learn`: 16 facts `T s1 | is_a | pet` .. `T s16 | is_a | pet`
- `handle_concept_learn`: 16 facts `T s17 | is_a | pet` .. `T s32 | is_a | pet`
- `handle_concept_learn`: 9 facts `T s33 | is_a | pet` .. `T s41 | is_a | pet`
Hand-derived state (matches frozen F-T1): C0 = {s1..s8}, members 8;
NOADD table = 32 entries (s9..s40 voting concept 0); s41 refused
(drop event 1); `noadd_drop_total==1`; drop list = [s41].

Test A1 (spurious NOTE, all inputs voting):
- `handle_proc_learn_unified(W, "s1>1s;s2>2s")`.
- Hand-derived: s1 votes 0, s2 votes 0. Voter: vc=0 cnt=2, best_cnt=2,
  nseg=2, 2*2>2 so train_con=0. NOTE loop: both inputs have vote>=0,
  nlost=0, no NOTE.
- EXPECT: train_con==0 AND zero `ULEARN: NOTE ` lines for this learn.

Test A2 (never-voted vs lost):
- `handle_proc_learn_unified(W, "s1>1s;ghost>tsohg")` ("ghost" never taught).
- Hand-derived: s1 votes 0; ghost: not a member, not in NOADD table,
  vote=-1; `noadd_vote_lost("ghost")==0`. Voter: vc=0 cnt=1, 1*2>2 false,
  train_con=-1. NOTE loop: ghost has vote<0 but lost=0, nlost=0, no NOTE.
- EXPECT: train_con==-1 AND zero `ULEARN: NOTE ` lines. The -1 must read
  as "no concept applied" with NO NOTE, because no vote was lost.

Test A3 (positive control):
- `handle_proc_learn_unified(W, "s1>1s;s41>14s")`.
- Hand-derived: s41 vote=-1, `noadd_vote_lost("s41")==1`, nlost=1.
- EXPECT: exactly one `ULEARN: NOTE 1 train input(s) lost concept votes
  (NOADD table full); train_con computed without them`.

KILL CRITERION: If A1 or A2 emits a NOTE, R1's "NOTE iff vote lost"
contract is broken by SPOOF -> DOWNGRADE. If A3 emits no NOTE, R1 is
broken by SUPPRESSION within the design envelope -> DOWNGRADE.

## X-FU5-2: drop-list exhaustion

Question: past 64 drop events, does the NOTE go completely missing on a
pivotal outcome (the X-FU4-2 failure returning silently)? And is the
disclosed bound really "64 distinct subjects", or 64 drop events?

World B (fresh):
- s1..s16, s17..s32, s33..s40 (40 subjects, 3 batches).
  Hand-derived: C0 = 8 members; NOADD = 32 entries; 0 drops; table full.
- d1..d16, d17..d32, d33..d48, d49..d64 (64 subjects, 4 batches of 16).
  Hand-derived: 64 drop events; `noadd_drop_total==64`; drop list full
  with [d1..d64].
- d65..d70 (6 subjects, 1 batch).
  Hand-derived: 6 more drop events; `noadd_drop_total==70`; d65..d70 NOT
  in the name list (all 64 slots taken).

Test B1 (victim beyond 64):
- `handle_proc_learn_unified(W, "s1>1s;d70>07d")`.
- Hand-derived: s1 votes 0; d70: vote=-1 (not member, not in NOADD),
  `noadd_vote_lost("d70")==0` (beyond 64). Voter: vc=0 cnt=1, 2>2 false,
  train_con=-1. NOTE loop: d70 lost=0, nlost=0, NO NOTE.
- EXPECT: train_con==-1, NO NOTE, `noadd_drop_total==70`,
  `noadd_vote_lost("d70")==0`, `noadd_vote_lost("d1")==1`.
- This is the disclosed residual: the NOTE is completely absent past 64
  events. CONFIRMED BOUNDARY, no verdict change (it is disclosed in
  FDCR_UNIFIED5_RESULT.md "Honest residuals").

Test B2 (positive control within 64):
- `handle_proc_learn_unified(W, "s1>1s;d1>1d")`.
- Hand-derived: d1 vote=-1, lost=1, nlost=1.
- EXPECT: `ULEARN: NOTE 1 train input(s) ...` present.

Test B3 (per-EVENT vs per-distinct; disclosure refinement):
World C (fresh):
- s1..s40 (40 subjects) -> C0: 8 members, NOADD: 32, 0 drops.
- 70x `handle_concept_learn(W, "T rep | is_a | pet")` (one fact per batch;
  within-batch dedup does not apply across batches; `con_intern` has no
  dedup so each teaching is a fresh offset; each misses the NOADD table).
  Hand-derived: 70 drop events; `noadd_drop_total==70`; name list holds
  64 copies of "rep" (full).
- `handle_concept_learn(W, "T v | is_a | pet")`.
  Hand-derived: drop event 71; `noadd_drop_total==71`; "v" NOT in list.
- EXPECT: `noadd_drop_total==71`, `noadd_vote_lost("v")==0`,
  `noadd_vote_lost("rep")==1`.
- Procedure `s1>1s;v>v`: v vote=-1, lost=0 -> NO NOTE, train_con=-1.
- Only 2 distinct subjects ("rep", "v") were involved. If confirmed, the
  disclosure's "64 distinct subjects" framing is inaccurate: the bound is
  64 drop EVENTS (no dedup in `noadd_drop_record`).

KILL CRITERION: B1/B2 confirming the 64-event limit -> CONFIRMED
DISCLOSED BOUNDARY, no verdict change. B3 showing exhaustion with <64
distinct subjects -> DISCLOSURE REFINEMENT (report; not a verdict
change by itself). DOWNGRADE only if a NON-disclosed NOTE failure
appears: NOTE suppressed while total drops <= 64, `noadd_vote_lost`
wrong for a within-64 drop, or nlost undercounted within 64 events.

## X-FU5-3: merge chains with clearing

Question: does R2's clearing break slot reuse, post-merge matching, or
voting? Does any path read the cleared lists?

World D (fresh):
- `handle_concept_learn`: 8 facts `T s1 | is_a | pet` .. `T s8 | is_a | pet`.
  Hand-derived: C0 slot 0, {is_a=pet}, 8 members.
- `handle_concept_learn`: 16 facts `T m1 | is_a | pet;T m1 | color | orange`
  .. `T m8 | is_a | pet;T m8 | color | orange`.
  Hand-derived: m1 creates C1 slot 1 {is_a=pet,color=orange}; m2..m8 join.
  NOADD: 0 entries.
- `handle_concept_learn`: `T s1 | color | orange`.
  Hand-derived: s1 in C0, extend C0 to {is_a=pet,color=orange};
  `con_merge_check` finds C1 set-identical -> `con_merge_into(C0, C1)`:
  Step 1: m1..m8 overflow (C0 full) -> 8 NOADD entries for concept 0
  (table had room); WARN merge overflow; Step 4: C1 active=0, nmem=0,
  nfeat=0; CONCEPT-MERGE 1 into 0.
- EXPECT: `con_count==1`; `con_active(1)==0`; `con_nmem(1)==0`;
  `con_nfeat(1)==0`; `con_vote_concept("m1")==0` (NOADD vote);
  `con_find_member_str("m1")==-1`; `noadd_drop_total==0`.

Slot reuse:
- `handle_concept_learn`: `T n1 | size | big`.
  Hand-derived: n1 {size=big} matches nothing; create reuses slot 1
  (first inactive).
- EXPECT: `con_active(1)==1`; `con_nfeat(1)==1`; `con_nmem(1)==1`;
  `con_str_at(con_feat(1,0))` content-equal "size=big" (NOT "is_a=pet"
  or "color=orange": stale-feature check);
  `con_find_member_str("n1")==1`.

Post-reuse behavior:
- `handle_concept_learn`: `T n2 | size | big` -> n2 joins C1'.
- `handle_proc_learn_unified(W, "n1>1n;n2>2n")`.
  Hand-derived: n1 votes 1, n2 votes 1; vc=1 cnt=2; 2*2>2; train_con=1.
- EXPECT: train_con==1 (reused slot votes correctly).
- `handle_concept_learn`: `T z1 | is_a | pet;T z1 | color | orange`.
  Hand-derived: z1 {is_a=pet,color=orange} matches active C0; C0 full;
  MATCH-NOADD -> NOADD entry for concept 0 (table has 8, room).
- EXPECT: `con_vote_concept("z1")==0` (cleared C1 does not interfere
  with `con_form` matching, which requires active==1).

KILL CRITERION: Any stale data observed (old features/members visible on
the cleared or reused slot, a vote resolving to the inactive concept, or
wrong nfeat/nmem) -> DOWNGRADE (R2 clearing unsafe). Broken slot reuse
or post-merge voting -> DOWNGRADE.

## X-FU5-4: regression and additivity

- Rebuild from a pristine `git show HEAD:unified_fdcr5.zag` copy with the
  frozen toolchain; run 3x; outputs must be byte-identical (cmp).
- All 40 named checks must PASS (tally in output).
- Output lines 1-431 must be byte-identical to the committed
  FDCR_UNIFIED5_RAW.txt lines 1-431 (Parts A-E).
- `diff unified_fdcr4.zag unified_fdcr5.zag` must show only additions:
  zero removed or modified non-comment mechanism lines (PART F main code
  is new; R1/R2 are insertions).

KILL CRITERION: Any check fails, Parts A-E differ, outputs not
deterministic, or the diff is not purely additive -> KILL (frozen
K-FU5-4 broken).

## Governance

- This prereg commits alone, before any adversary build or run.
  Strict-ancestor ordering verified via merge-base before the result
  commit lands.
- Pure Zag: fixtures, harness, builds, runs, greps, md5, cmp. No Python.
- Only owned files under `fdcr_unified5_adv/` staged. No other worker's
  files touched. No binaries committed (builds in /tmp only).
- No em dashes in loop documentation.
- On .git/index.lock contention: wait; never remove a live lock.
