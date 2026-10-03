# H-FDCR-UNIFIED4 RESULT: SURVIVES (32/32)

**Date:** 2026-09-29
**Researcher:** H-FDCR-UNIFIED4 Repair Researcher (independent subagent)
**Target:** H-FDCR-UNIFIED3 DOWNGRADED (red team:
  FDCR_UNIFIED3_ADV_RESULT.md; X-FU3-1 and X-FU3-2 kill criteria met)
**Verdict:** SURVIVES. All five frozen kill bars PASS (32/32 named
  checks). Classification: bounded L2 integration repair. No L3 claimed.

## Lineage

- Prereg `PREREG_FDCR_UNIFIED4.md` committed alone as `a69dbb78f`
  BEFORE any implementation edit, build, or run.
- Amendment `PREREG_FDCR_UNIFIED4_AMEND1.md` (pre-execution):
  `noadd_record`'s defensive membership check scoped to the TARGET
  concept (an any-concept check would have wrongly rejected
  merge-overflow members still listed in the absorbed concept).
  Authored before any build or run; kill bars and fixtures
  unchanged. Committed before the result.
- `unified_fdcr4.zag` = `unified_fdcr3.zag` copied verbatim
  (cmp-verified) plus exactly the frozen R1-R4 changes.
  `unified_fdcr3.zag` untouched.
- Prereg is a verified strict ancestor of the result commit
  (merge-base --is-ancestor).

## Repairs implemented (exactly per frozen prereg)

**R1: NOADD vote table (X-FU3-2).** 32 entries x 8 bytes at
NOADD_BASE=2412 (first free address after the concept store;
WORK=4096 untouched). `con_form`'s -2 MATCH-NOADD path records
the excluded subject via `noadd_record`. The procedure majority
voter uses `con_vote_concept` (member first, else NOADD vote).
`con_find_member_str` keeps exact member-only semantics; the
intent query path still uses it, so no false membership is ever
asserted. Table-full emits a loud WARN.

**R2: post-extension concept merge (X-FU3-1).** `con_merge_check`
runs at the end of the extension branch: on set-identity with
another active concept, `con_merge_into` moves members (8 cap;
overflow becomes NOADD voters with a loud WARN), remaps NOADD
entries, remaps all 20 intent concept records, deactivates the
absorbed concept, and emits CONCEPT-MERGE. No evidence is
silently dropped.

**R3: PART E tests** (E-T1..E-T5) appended after PART D; the
H-FDCR-UNIFIED3 banner line is preserved so Parts A-D stay
byte-comparable.

## Frozen kill-bar evidence

Raw: `FDCR_UNIFIED4_RAW.txt` (md5 `0cce903c554697b72e70b21008f6bc42`),
program output only (no znc wrapper lines).

- **K-FU4-1 PASS:** E-T1 (exact X-FU3-1A attack order):
  `CONCEPT-MERGE 1 into 0`, con_count=1, cat/dog same concept,
  `cat>tac;dog>god` train_con=0 (was -1). E-T2 (exact X-FU3-1B
  control order): con_count=1, train_con=0, unchanged.
- **K-FU4-2 PASS:** E-T3 (exact X-FU3-2 fixture): con_count=1,
  16-pair reversal train_con=0 (was -1); 8 `WARN member cap 8`
  lines still present; con_find_member_str("qap")==-1 (still not
  a member); con_vote_concept("qap")==0 (votes).
- **K-FU4-3 PASS:** E-T5: D-T1..D-T4 criteria all hold
  in-evidence. External diff: FU4 program output lines for
  Parts A-D are byte-identical to the committed
  FDCR_UNIFIED3_RAW.txt lines 1-208; the only additions are the
  PART E block and the 32/32 tally (was 27/27).
- **K-FU4-4 PASS:** 3 consecutive runs byte-identical (cmp);
  md5 `0cce903c554697b72e70b21008f6bc42` x3. (The `znc --run`
  wrapper appends its own status lines; program output is
  identical.)
- **K-FU4-5 PASS:** E-T4: pre-merge `d0>0d` train_con=1;
  after cat's extension: `CONCEPT-MERGE 1 into 0`,
  con_count=1, cat and d0 members of concept 0, intent record
  remapped 1->0, NOADD d8 remapped 1->0, d7 not a member
  (overflow) but con_vote_concept("d7")==0, and a
  `WARN merge member overflow on concept 0; 1 members kept as
  votes only` line in raw output.

Final tally: **32/32. H-FDCR-UNIFIED SURVIVES.**

## Honest residuals (disclosed, not repaired)

- The caps themselves are unchanged: 16 facts/batch, 8
  features per subject accumulation, 8 features per concept,
  8 members per concept, 32 NOADD vote entries. All are loud
  now; enlargement/eviction policy remains future work.
- NOADD subjects vote but are never members; a query for a
  NOADD subject gets no concept boost (conservative, honest).
- Merge overflow beyond 32 NOADD entries would emit the
  table-full WARN and lose the vote (loud, not silent).
- First-seen tie break in the voter is unchanged (disclosed).

## Governance disclosures

1. Prereg committed alone before any implementation; amendment
   committed before the result; ordering verified by
   merge-base --is-ancestor.
2. Pure Zag throughout: fixtures, harness, builds, runs,
   greps, md5, cmp. Zero Python at any stage.
3. No binaries committed (builds in /tmp/fu4 only).
4. Only the four owned files staged/committed
   (PREREG_FDCR_UNIFIED4.md, PREREG_FDCR_UNIFIED4_AMEND1.md,
   unified_fdcr4.zag, FDCR_UNIFIED4_RAW.txt,
   FDCR_UNIFIED4_RESULT.md). No other worker's files touched.
   Pathspec-restricted staging used throughout.
5. No em dashes in loop documentation.
6. No test-answer literals in mechanism regions (verified by
   grep; only the word "cap" in comments matched loosely).
7. `unified_fdcr3.zag` and all prior evidence files untouched.

## Suggested follow-ups for parent

1. Independent red team on H-FDCR-UNIFIED4 (natural attacks:
   X-FU4-1 three-concept merge chains and merge-then-extend
   cycles; X-FU4-2 NOADD table exhaustion at 32 entries;
   X-FU4-3 merge with intent records on the survivor concept).
2. The research paper's H-FDCR-UNIFIED3 section needs both
   this downgrade entry and the H-FDCR-UNIFIED4 result.
