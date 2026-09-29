# H-FDCR-UNIFIED4 RED TEAM RESULT: SURVIVES (all attacks failed)

**Date:** 2026-09-29
**Researcher:** H-FDCR-UNIFIED4 Red Team (independent subagent)
**Target:** H-FDCR-UNIFIED4 SURVIVES (32/32). Repairs under attack:
  R1 NOADD vote table (32 entries; MATCH-NOADD subjects vote via
  con_vote_concept; con_find_member_str keeps member-only
  semantics) and R2 post-extension concept merge
  (con_merge_check / con_merge_into: member move with 8-cap,
  overflow to NOADD with WARN, noadd_remap, 20-slot intent
  remap, deactivation, CONCEPT-MERGE emit).
**Verdict:** SURVIVES this red team. Every frozen kill criterion
  failed to trigger. One disclosed residual (NOADD exhaustion)
  is confirmed with a new concrete pivotal demonstration;
  per the frozen verdict rule this is a BOUNDARY, not a kill.

## Lineage

- Prereg `PREREG_FDCR_UNIFIED4_ADV.md` committed alone as
  `98c6dfc6e` BEFORE any attack fixture, harness line, build,
  or run.
- Attack harness `fdcr_unified4_adv.zag` = lines 1-1891 of the
  committed `unified_fdcr4.zag` (everything before `fn main`)
  copied byte-verbatim (cmp-verified: MECH-HEAD-IDENTICAL),
  plus a new `main()` containing only the frozen attack
  worlds. No mechanism line was modified.
- Raw evidence `FDCR_UNIFIED4_ADV_RAW.txt` md5
  `289a4df284a8270d4f3b89b5eea5e0a2`, program output only
  (direct binary run, no znc wrapper lines). 3/3 runs
  byte-identical (cmp).
- One post-run correction: a wrong counterfactual direction in
  a T2b comment/emit string was fixed (see T2b below). The
  in-harness assertion (`train_con==-1`) was correct as
  written and unchanged; only the explanatory text was
  corrected. The fix is disclosed here, not hidden.

## Method

Each attack world starts from a fresh workspace
(`z_alloc(65536)`, `set32 ST_STR`, `intent_init`, `con_init`).
Attacks call `handle_concept_learn` and
`handle_proc_learn_unified` directly and assert on
`con_count`, `con_find_member_str`, `con_vote_concept`,
`noadd_find`, raw NOADD memory (base 2412, 32x8 bytes), and
intent records at `intent_proc_base(W,slot)+8`. Merge-count
and WARN-count assertions were verified externally with grep
on the raw output. Pure Zag throughout: fixtures, harness,
builds, runs, greps, md5, cmp. Zero Python at any stage.

## X-FU4-1: merge chains and merge-then-extend cycles

Kill criterion: two ACTIVE concepts with set-identical feature
sets after any sequence, or con_count differing across batch
orders on the identical total fact set, or any fixture
subject lost (votes -1 / not a member while its feature set
matches an active concept). NOT MET.

- **T1a (three-concept chain) PASS.** C0={is_a=pet}(sa),
  C1={is_a=pet,color=orange}(sb),
  C2={is_a=pet,color=orange,size=big}(sc). Extending sa with
  color=orange merged C1 into C0; extending sa with size=big
  merged C2 into C0. End state: con_count=1; sa, sb, sc all
  members of concept 0; exactly 2 CONCEPT-MERGE lines
  (`1 into 0`, `2 into 0`); procedure `sa>as;sb>bs;sc>cs`
  learned train_con=0. The chained merge (merge, then extend
  the survivor, then merge again) resolved fully.
- **T1b order-1 (new subject first) PASS.** Batch
  `T nu | is_a | pet;T nu | color | orange;T olda | color | orange`
  with olda in C0={is_a=pet}: con_form created C1 for nu,
  then olda's extension grew C0 into set-identity and merged
  C1 into C0. con_count=1, olda and nu in concept 0,
  train_con=0 for `olda>adlo;nu>un`.
- **T1b order-2 (extension first) PASS.** Batch
  `T olda | color | orange;T nu | is_a | pet;T nu | color | orange`:
  olda's extension grew C0 first (merge_check found no match
  yet), then nu's con_form matched the grown C0 and joined as
  member. con_count=1, same concept, train_con=0. Both batch
  orders converge; no merge line was needed in order-2 and
  none fired.
- **T1c (two extensions in one batch) PASS.** A={is_a=pet}(s1),
  B={kind=animal}(s2). Batch
  `T s1 | kind | animal;T s2 | is_a | pet`: s1 extended A to
  2 feats (no match yet), s2 extended B to the identical set,
  merge_check fired and merged A into B (ci=B, the extended
  concept; `CONCEPT-MERGE 0 into 1`). con_count=1, s1 and s2
  in concept 1, procedure `s1>1s;s2>2s` learned.

Total CONCEPT-MERGE lines in raw: 7, at exactly the expected
sites (2 in T1a, 1 in T1b-order1, 0 in T1b-order2, 1 in T1c,
1 in T3a, 1 in T3b, 1 in T4b-1A). No duplicate active
concepts with identical feature sets survived any sequence.

## X-FU4-2: NOADD table exhaustion at 32 entries

Kill criterion: the 33rd NOADD subject dropped with NO
`WARN NOADD vote table full` line (silent loss), or its vote
silently kept despite the WARN, or an unrelated vote
corrupted. NOT MET. Boundary rule per frozen prereg: WARN
present with a demonstrated flip = confirmed disclosed
residual = BOUNDARY.

- **T2a (fill and overflow) PASS.** 41 subjects s1..s41, one
  `is_a=pet` fact each, in batches of 16/16/9. End state:
  con_count=1, con_nmem(0)=8, con_vote_concept("s1")=0
  (member), con_vote_concept("s32")=0 (NOADD vote),
  con_vote_concept("s41")=-1 (vote lost). Exactly one
  `WARN NOADD vote table full` line in raw output. The loss
  is loud, not silent, exactly as the builder disclosed.
- **T2b (pivotal flip) PASS with a correction.** Same world
  plus `T zz | color | orange` (C1={color=orange}, member zz).
  Procedure `s1>1s;zz>zz;s41>14s` (all reversals; direct
  discovery): s1 votes 0, zz votes 1, s41 lost (-1).
  Vote math: best_cnt=1 for concepts 0 and 1; 1*2=2 > 3 is
  false, so train_con=-1 (observed and asserted).
  Counterfactual: had s41's vote been recorded, s41 matches
  C0 ({is_a=pet}) and would vote concept 0, giving 2v1 and
  train_con=0. So the single lost vote flipped the procedure
  outcome from 0 to -1, with the WARN as the only signal.
  CORRECTION OWNED: the frozen prereg (and the first harness
  run's info line) stated the counterfactual as concept 1 /
  train_con=1. That was my error: s41's feature set is
  {is_a=pet}, identical to C0, so it would vote concept 0,
  not concept 1. The true counterfactual is train_con=0.
  The flip remains pivotal (-1 vs 0) and the in-harness
  assertion (train_con==-1) was correct as written. The
  explanatory text was fixed post-run and the harness
  rebuilt and rerun 3/3 deterministic; this correction is
  disclosed rather than silently edited.

Interpretation: the builder's disclosure ("loud, not silent")
is accurate at the concept layer, but the downstream effect
is stronger than "lose the vote": a single exhausted vote can
flip a procedure's train_con (-1 vs 0 here) while the only
evidence is a WARN line emitted pages earlier at concept-learn
time. This stays a BOUNDARY under the frozen rule because the
WARN did fire exactly once and the mechanism never asserts a
false membership. Recommended follow-up (not a kill): make
the procedure layer surface vote-exhaustion explicitly, e.g.
a train-time note when any input's vote was lost to a full
table, so the -1 does not read as "no concept applied".

## X-FU4-3: intent records on the survivor concept during merge

Kill criterion: any intent record (proc slots 0..15, bridge
slots 0..3) still referencing the deactivated concept after
merge, or any NOADD entry still referencing it, or a
pre-merge procedure failing to apply post-merge. NOT MET.

- **T3a (proc records across merge) PASS.** C0={is_a=pet}
  (pa,pb); C1={is_a=pet,color=orange} (qa,qb). P1=`qa>aq;qb>bq`
  recorded concept 1 (asserted pre-merge); P2=`pa>ap;pb>bp`
  recorded concept 0 (asserted pre-merge). After
  `T pa | color | orange` extended C0 and merged C1 into C0:
  con_count=1; P1's record remapped 1->0; P2's record still
  0 (survivor untouched); proc_apply(P1,"qa")="aq" and
  proc_apply(P2,"pa")="ap" still correct. The remap did not
  disturb records already on the survivor.
- **T3b (NOADD remap across merge) PASS.** C0: 3 feats, 8
  members d0..d7; d8 MATCH-NOADD (noadd_find("d8")=0 asserted
  pre-merge). C1={is_a=pet,color=orange} (cat); extending cat
  with size=big merged C0 into C1 (`CONCEPT-MERGE 0 into 1`).
  Post-merge: con_count=1; noadd_find("d8")=1 (remapped);
  con_vote_concept("d8")=1; d7 (merge overflow: C1 held cat
  plus d0..d6 at the 8-cap) is not a member
  (con_find_member_str=-1) but votes
  (con_vote_concept=1), with one `WARN merge member overflow`
  line in raw; a full scan of all 32 NOADD entries found zero
  entries still referencing concept 0. No stale references
  anywhere.

## X-FU4-4: regression and source audit

Kill criterion: rebuilt output md5 differs, any prior fixture
regresses, or any frozen prereg-contract deviation in source.
NOT MET.

- **T4a (rebuild) PASS.** The committed `unified_fdcr4.zag`
  rebuilt unmodified; program output md5
  `0cce903c554697b72e70b21008f6bc42`, byte-identical to the
  frozen FDCR_UNIFIED4_RAW.txt.
- **T4b (prior fixtures) PASS.** Exact X-FU3-1A attack order,
  X-FU3-1B control order, and exact X-FU3-2 16-subject fixture
  re-run through the copied mechanism: con_count=1 and
  train_con=0 in all three.
- **T4c (source audit) PASS on all five sub-checks:**
  (i) noadd_record's AMEND1 defensive check
  (`con_find_member_str(W,s0)==c`, line 1458) is scoped to
  the TARGET concept only; (ii) con_merge_into performs
  steps 1-5 in frozen order (member move with 8-cap,
  overflow to NOADD with WARN, noadd_remap, 20-slot intent
  remap, deactivation, CONCEPT-MERGE emit); (iii) the
  procedure voter uses con_vote_concept at BOTH call sites
  (lines 1575, 1584) while the intent query path
  (intent_winner, line 946; intent_trace_emit, line 1032)
  still uses con_find_member_str with member-only semantics;
  (iv) no test-answer literals in mechanism lines 1-1891
  (grep for s41/w41/d8/olda/"zz" returned nothing);
  (v) con_merge_check is called exactly once, at the end of
  the extension branch (line 1821).

## Residual observations (not kills)

1. The first-seen tie-break in the voter (`cnt>best_cnt`) is
   unreachable for train_con: a tie at best_cnt implies
   best_cnt*2 <= nseg, so the strict-majority gate already
   failed. The disclosed tie-break never decides. Cosmetic.
2. con_merge_into does not clear the absorbed concept's stale
   member/feature lists; they are invisible while inactive and
   overwritten on slot reuse (create path resets nfeat,
   features, mem[0], nmem). Verified safe by code reading;
   no test constructed a leak.
3. The combined stress case (NOADD table already full when a
   merge overflows members into it) was not run; the code
   path emits the same table-full WARN and drops the vote.
   Suggested follow-up, within the disclosed boundary.

## Governance disclosures

1. Prereg committed alone before any attack code, build, or
   run (98c6dfc6e).
2. Pure Zag throughout. Zero Python at any stage.
3. Only three adversary-owned files staged/committed
   (PREREG_FDCR_UNIFIED4_ADV.md already committed;
   fdcr_unified4_adv.zag, FDCR_UNIFIED4_ADV_RAW.txt,
   FDCR_UNIFIED4_ADV_RESULT.md in this commit).
   Pathspec-restricted staging. No other worker's files
   touched. No binaries committed (builds in /tmp/fu4adv).
4. No em dashes in loop documentation.
5. The T2b counterfactual correction is disclosed above; the
   in-harness assertion was correct as written and is
   unchanged in meaning.
6. The harness's mechanism section is cmp-verified identical
   to committed unified_fdcr4.zag lines 1-1891.

## Verdict

**H-FDCR-UNIFIED4 SURVIVES this red team.** 11/11 attack
checks passed; 3/3 deterministic; rebuild byte-identical;
source audit clean. The merge cannot be broken by
three-concept chains, same-batch order swaps, or dual
extensions; the NOADD table fails loudly at exactly 32
entries; intent and NOADD bookkeeping survive merges with no
stale references; all prior fixtures hold. The one new
finding is a confirmed boundary: NOADD exhaustion loses a
vote loudly and that lost vote demonstrably flipped a
procedure outcome (train_con -1 vs 0), with only the earlier
WARN as signal. Recommend the procedure layer surface
vote-exhaustion explicitly in future work.
