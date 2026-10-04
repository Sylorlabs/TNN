# PREREG H-FDCR-UNIFIED4 FROZEN

**Date:** 2026-09-29
**Researcher:** H-FDCR-UNIFIED4 Repair Researcher (independent subagent)
**Target:** H-FDCR-UNIFIED3 DOWNGRADED (red team: FDCR_UNIFIED3_ADV_RESULT.md,
  X-FU3-1 and X-FU3-2 kill criteria met)
**Status:** FROZEN. Implementation must strictly follow this prereg.
**Toolchain:** znc 2026.07.0-dev (edition 2026). Pure Zag. No Python anywhere.

## Hypothesis

The two H-FDCR-UNIFIED3 red-team downgrades can be repaired at the
mechanism level without breaking the frozen K-FU3-1..K-FU3-6 bars:

- X-FU3-1 (extension-path order fragility): repair with a
  post-extension concept-merge check. After the extension branch
  grows a concept's feature set, test set-identity against all other
  active concepts and merge on match, so the identical total fact
  set yields one concept in both batch orders.
- X-FU3-2 (member-cap vote splitting): repair with a vote-counting
  policy. MATCH-NOADD subjects (feature set known, excluded only by
  the 8-member cap) are recorded in a NOADD vote table and count as
  concept votes at the procedure layer, so the 16-subject fixture
  learns train_con=0 instead of failing -1 silently.

## Repairs (frozen)

Implementation file: `unified_fdcr4.zag` = `unified_fdcr3.zag`
copied verbatim (cmp-verified), then the changes below only.
`unified_fdcr3.zag` is NOT modified.

### R1: NOADD vote table (X-FU3-2)

Memory: NOADD_BASE()=2412 (first free address after the concept
store, which ends at 2412; WORK=4096 is untouched). 32 entries of
8 bytes (subject string offset, concept index) = 256 bytes, ending
at 2668. A -1 subject offset marks a free entry.

New functions (frozen contracts):

- `noadd_init(W)`: set all 32 subject offsets to -1. Called from
  `con_init` (which runs once per workspace).
- `noadd_record(W, mem_off, c)`: if a NOADD entry already holds a
  subject content-equal to the string at mem_off, update its
  concept to c and return. Else append (mem_off, c) to the first
  free entry. If the table is full, emit
  `ULEARN concept: WARN NOADD vote table full; subject will not vote`
  and return without recording. Never records a subject that is
  already a concept member (defensive check via
  con_find_member_str; emits nothing, returns).
- `noadd_find(W, s)`: return the concept index for the NOADD entry
  whose subject is content-equal to s, or -1.
- `noadd_remap(W, c2, ci)`: set every NOADD entry with concept
  c2 to ci (used by the merge in R2).
- `con_vote_concept(W, s)`: return con_find_member_str(W, s) if
  >= 0, else noadd_find(W, s). This is the ONLY function used for
  procedure-layer voting. `con_find_member_str` keeps its exact
  member-only semantics everywhere else (no false membership is
  ever asserted; queries via intent_winner still use
  con_find_member_str).

Call sites (frozen):

- In `con_form`, on the -2 MATCH-NOADD path: call
  `noadd_record(W, mem_off, c)` immediately before the existing
  WARN emit. Nothing else in `con_form` changes.
- In `handle_proc_learn_unified`, the majority voter: replace
  BOTH `con_find_member_str` calls (the per-input vc lookup and
  the inner counting comparison) with `con_vote_concept`. The
  strict-majority rule `best_cnt*2>nseg`, the first-seen tie
  break, and all intent-record calls are unchanged.

### R2: post-extension concept merge (X-FU3-1)

New functions (frozen contracts):

- `con_merge_check(W, ci)`: after the extension branch grows
  concept ci, scan every other active concept c2. If
  con_nfeat(W,c2)==con_nfeat(W,ci) and every feature of c2 is
  content-found in ci's feature list (set-identity, same shape as
  the R1 check in con_form), call con_merge_into(W, ci, c2).
  Multiple matches merge in index order.
- `con_merge_into(W, ci, c2)`:
  1. Move each member offset of c2 into ci if not already
     present and nm<8; on overflow call noadd_record(W, mo, ci)
     for the excess member and count it. After the loop emit
     `ULEARN concept: WARN merge member overflow on concept N; M
     members kept as votes only` if M>0.
  2. Call noadd_remap(W, c2, ci).
  3. Remap intent concept records: for all 20 slots (16 proc +
     4 bridge at IBASE, concept at offset+8), if the slot is used
     (offset+0 >= 0) and concept==c2, set concept=ci.
  4. con_set_active(W, c2, 0).
  5. Emit `ULEARN concept: CONCEPT-MERGE c2 into ci`.
  The absorbed concept's identity is preserved as the survivor
  index ci; no evidence is silently dropped.

Call site (frozen): at the end of the `existing>=0` extension
branch in `handle_concept_learn`, after the existing
ndropped_ext WARN block, call `con_merge_check(W, ci)`. The
con_form (new-concept) path needs no merge call: con_form
already checks all active concepts before creating.

### R3: PART E tests in main()

Append PART E after PART D. New worlds each start from a fresh
workspace (set32 ST_STR, intent_init, con_init). E-T1..E-T5 use
the exact red-team fixture strings.

- E-T1 (K-FU4-1 attack order): the exact X-FU3-1A fixture
  (batch1 `T cat | is_a | pet;T cat | color | orange`, batch2
  `T dog | color | orange;T dog | is_a | pet;T dog | size | big`,
  batch3 `T cat | size | big`). PASS requires con_count=1,
  cat and dog in the same concept, AND procedure
  `cat>tac;dog>god` yields train_con=0.
- E-T2 (K-FU4-1 control order): the exact X-FU3-1B fixture.
  PASS requires con_count=1 and train_con=0 (unchanged from
  H-FDCR-UNIFIED3 behavior).
- E-T3 (K-FU4-2): the exact X-FU3-2 fixture (16 subjects
  qaa..qap, one `is_a=pet` fact each; 16-pair reversal
  `qaa>aaq;...;qap>paq`). PASS requires con_count=1,
  train_con=0 (was -1), the `WARN member cap 8` lines still
  present in raw output, con_find_member_str("qap")==-1 (still
  not a member), and con_vote_concept("qap")==0 (votes).
- E-T4 (K-FU4-5 merge bookkeeping): batch1
  `T cat | is_a | pet;T cat | color | orange` (C0, 2 feats);
  batch2 eight subjects d0..d7 each
  `is_a=pet;color=orange;size=big` (C1, 3 feats, 8 members);
  batch3 `T d8 | is_a | pet;T d8 | color | orange;T d8 | size |
  big` (d8 MATCH-NOADD, NOADD d8->C1); train
  `d0>0d` and record its train_con (must be 1, d0 votes C1);
  batch4 `T cat | size | big` (extension grows C0 to 3 feats,
  merge fires). PASS requires: con_count=1; a
  `CONCEPT-MERGE 1 into 0` line in raw output; cat and d0 both
  members of concept 0; the pre-merge intent record remapped
  (train_con now reads 0); noadd_find("d8")==0 (remapped);
  con_find_member_str("d7")==-1 (overflow, not a member);
  con_vote_concept("d7")==0 (overflow still votes); and a
  `WARN merge member overflow` line in raw output.
- E-T5 (K-FU4-3 regression): re-run the D-T1..D-T4 PASS
  criteria verbatim on fresh worlds (they must hold), AND
  Parts A-D raw output must be byte-identical to the committed
  FDCR_UNIFIED3_RAW.txt except for the appended PART E block.
  Any other byte difference is a FAIL.

### R4: documentation

The result doc lists: the NOADD table (32 entries, vote-only,
never membership), the merge rule (post-extension, set-identity,
member preservation with overflow-to-votes, intent remap), and
the unchanged caps (16 facts/batch, 8 features/accumulation,
8 features/concept, 8 members/concept).

## Kill bars (frozen)

- **K-FU4-1 (extension-path order fragility closed):** E-T1 and
  E-T2 PASS: con_count=1 in BOTH batch orders on the identical
  total fact set, cat/dog same concept, train_con=0 both.
- **K-FU4-2 (member-cap vote splitting closed):** E-T3 PASS:
  16 identical-feature subjects, train_con=0 (was -1); WARN
  member cap lines still present; qap not a member but votes.
- **K-FU4-3 (regression):** E-T5 PASS: D-T1..D-T4 criteria
  hold; Parts A-D byte-identical to FDCR_UNIFIED3_RAW.txt
  except the appended PART E block.
- **K-FU4-4 (determinism):** 3 consecutive full runs
  byte-identical (cmp).
- **K-FU4-5 (merge bookkeeping):** E-T4 PASS per the frozen
  assertions above.

## Classification target

Bounded L2 integration repair. No L3 claimed. The caps remain;
NOADD subjects vote but are never members; merges preserve all
evidence (members, votes, intent records) with loud warnings on
overflow.

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
