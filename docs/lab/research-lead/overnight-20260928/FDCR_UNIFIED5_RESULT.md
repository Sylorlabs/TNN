# H-FDCR-UNIFIED5 RESULT: SURVIVES (40/40)

**Date:** 2026-09-29
**Researcher:** H-FDCR-UNIFIED5 Frontier Researcher (independent subagent)
**Target:** H-FDCR-UNIFIED4 SURVIVES (32/32); red-team SURVIVES with
  one confirmed BOUNDARY (FDCR_UNIFIED4_ADV_RESULT.md, X-FU4-2):
  NOADD exhaustion loses a vote loudly (one WARN) and the lost
  vote demonstrably flipped a procedure outcome (train_con -1 vs
  0), with only the earlier WARN as signal.
**Verdict:** SURVIVES. All five frozen kill bars PASS (40/40 named
  checks). Classification: bounded L2 integration repair. No L3 claimed.

## Lineage

- Prereg `PREREG_FDCR_UNIFIED5.md` committed alone as `1813a6547`
  BEFORE any implementation edit, build, or run.
- `unified_fdcr5.zag` = `unified_fdcr4.zag` copied verbatim
  (cmp-verified) plus exactly the frozen R1-R3 changes.
  `unified_fdcr4.zag` untouched.
- Prereg is a verified strict ancestor of the result commit
  (merge-base --is-ancestor).
- One test-code fix during execution (no prereg change): F-T1's
  procedure learn lands on a bridge rule (the mixed
  reversal/identity pairs defeat direct discovery), so the
  train_con read was extended to the bridge intent record,
  exactly as E-T3 already does. The mechanism, fixtures, bars,
  and the NOTE behavior are unchanged; the fix is disclosed
  here, not hidden.

## Repairs implemented (exactly per frozen prereg)

**R1: vote-exhaustion drop tracking + procedure-layer NOTE.**
NOADD_DROP_COUNT=2668 (one i32: total subjects refused vote
recording on a full table); NOADD_DROP_BASE=2672, 64 entries of
4 bytes (subject string offsets), ending at 2928; WORK=4096
untouched. `noadd_drop_init` runs from `noadd_init`;
`noadd_record`'s table-full path calls `noadd_drop_record`
before the existing WARN. `noadd_vote_lost` distinguishes
"vote lost to exhaustion" (1) from "never voted" (0).
`handle_proc_learn_unified` counts training inputs with
con_vote_concept<0 AND noadd_vote_lost==1 and, when nonzero,
emits `ULEARN: NOTE N train input(s) lost concept votes (NOADD
table full); train_con computed without them`. The NOTE fires
on direct, bridge, and fail paths alike.

**R2: absorbed-concept hygiene.** `con_merge_into` Step 4 now
clears the absorbed concept's member and feature lists
(con_set_nmem 0, con_set_nfeat 0) on deactivation. All readers
gate on active==1; the create path resets on reuse. No output
change.

**R3: PART F tests** (F-T1..F-T4) appended after PART E; the
H-FDCR-UNIFIED4 banner lines are preserved so Parts A-E stay
byte-comparable.

## Frozen kill-bar evidence

Raw: `FDCR_UNIFIED5_RAW.txt` (md5
`2f9515e842719da18b5a3255d1681004`), program output only
(direct binary run, no znc wrapper lines).

- **K-FU5-1 PASS:** F-T1 (exact red-team T2a+T2b world):
  con_count=2, train_con=-1 (bridge rule record),
  con_vote_concept("s1")==0, con_vote_concept("s41")==-1,
  noadd_vote_lost("s41")==1, noadd_vote_lost("s1")==0,
  noadd_vote_lost("zz")==0, noadd_drop_total()==1. Exactly one
  `WARN NOADD vote table full` line for this world, and the
  NOTE line `ULEARN: NOTE 1 train input(s) lost concept votes
  (NOADD table full); train_con computed without them` at raw
  line 560. The -1 no longer reads as "no concept applied".
- **K-FU5-2 PASS:** F-T2 (merge overflow into a full table):
  after `T s1 | color | orange` merged C1 into C0
  (`CONCEPT-MERGE 1 into 0`), con_count==1,
  noadd_drop_total()==9 (s41 + 8 merge-overflow members),
  noadd_vote_lost("m1")==1, con_vote_concept("m1")==-1,
  con_vote_concept("s1")==0, procedure `m1>1m;s1>1s`
  train_con==-1 with the NOTE at raw line 722. Nine
  `WARN NOADD vote table full` lines in this world; no stale
  references (full 32-entry NOADD scan: zero entries point at
  the absorbed concept, verified by the same remap code path
  the X-FU4-3 audit covered).
- **K-FU5-3 PASS:** F-T3 (exact E-T1 world): con_count==1, cat
  and dog in concept 0, train_con==0, and the absorbed
  concept 1 has con_active==0, con_nmem==0, con_nfeat==0.
- **K-FU5-4 PASS:** F-T4: all five E-T1..E-T5 criteria hold
  verbatim on fresh worlds (F-T4a..F-T4e PASS). External diff:
  FU5 raw lines 1-431 are byte-identical to the committed
  FDCR_UNIFIED4_RAW.txt lines 1-431; line 432 onward is the
  PART F block (FU4's own 32/32 tally occupied its lines
  432-433). Zero NOTE lines fire in Parts A-E, as designed:
  no FU4 fixture ever fills the NOADD table.
- **K-FU5-5 PASS:** 3 consecutive full runs byte-identical
  (cmp); md5 `2f9515e842719da18b5a3255d1681004` x3.

Final tally: **40/40. H-FDCR-UNIFIED SURVIVES.**

## Honest residuals (disclosed, not repaired)

- The caps themselves are unchanged: 16 facts/batch, 8
  features per subject accumulation, 8 features/concept, 8
  members/concept, 32 NOADD vote entries, 64 drop-list name
  slots. The drop TOTAL counter is unbounded and
  authoritative; the 64-entry name list is best-effort. If more
  than 64 distinct subjects are dropped, noadd_vote_lost can
  return 0 for a genuinely lost vote (the NOTE count still
  uses the authoritative per-input check against the recorded
  names, so nlost itself could undercount past 64 distinct
  drops; the total counter does not).
- A dropped subject that later becomes a real member votes
  normally; its stale drop-list entry is then unreachable
  because noadd_vote_lost is only consulted when
  con_vote_concept<0.
- The NOTE is a diagnostic, not enlarged capacity. A
  procedure whose decisive votes were lost still learns
  train_con=-1; the NOTE only makes the reason explicit.
- First-seen tie break in the voter is unchanged (disclosed).

## Governance disclosures

1. Prereg committed alone before any implementation; ordering
   verified by merge-base --is-ancestor.
2. Pure Zag throughout: fixtures, harness, builds, runs,
   greps, md5, cmp. Zero Python at any stage.
3. No binaries committed (builds in /tmp/fu5 only).
4. Only the four owned files staged/committed
   (PREREG_FDCR_UNIFIED5.md, unified_fdcr5.zag,
   FDCR_UNIFIED5_RAW.txt, FDCR_UNIFIED5_RESULT.md). No other
   worker's files touched. Pathspec-restricted staging used
   throughout.
5. No em dashes in loop documentation.
6. Mechanism diff vs unified_fdcr4.zag is purely additive:
   zero non-comment lines removed (verified by diff).
7. `unified_fdcr4.zag` and all prior evidence files untouched.
8. The F-T1 bridge-record read fix is test code only; the
   frozen mechanism, fixtures, and kill bars are unchanged.

## Suggested follow-ups for parent

1. Independent red team on H-FDCR-UNIFIED5 (natural attacks:
   X-FU5-1 NOTE spoofing: can any path make the NOTE fire
   when no vote was actually lost, or suppress it when one
   was; X-FU5-2 drop-list exhaustion past 64 distinct drops;
   X-FU5-3 merge chains with the clearing: does any path read
   the cleared lists).
2. The research paper's H-FDCR-UNIFIED4 section needs this
   H-FDCR-UNIFIED5 result entry.
