# H-FDCR-UNIFIED6 RED TEAM REPORT: SURVIVES (4 attacks fail)

**Date:** 2026-09-29
**Adversary:** H-FDCR-UNIFIED6 Independent Red Team (subagent)
**Target:** H-FDCR-UNIFIED6 SURVIVES (42/42). Prereg `814724be5`,
  result `0480f10a6` (per FU6 result doc; verified below).
**Stance:** Assumed the FU6 claim false. Attacked the R1 dedup and R2
  uncertainty-NOTE repairs.
**Verdict:** H-FDCR-UNIFIED6 SURVIVES this red team. All four
  preregistered attacks fail. Two new confirmed boundaries recorded
  (neither changes the verdict).

## Lineage and governance

- Prereg `PREREG_FU6_ADV.md` committed alone as `22268fc34` BEFORE any
  attack code was written, any build, or any run. No amendments.
- Harness = lines 1-2018 of the committed `unified_fdcr6.zag` blob
  (everything before `fn main`, verified clean cut at the
  `// ============ MAIN` comment boundary), byte-identical via
  construction from `git show HEAD:...`, plus an attack-only `main()`
  and two small helpers (`drop_name_count`, `new_world`,
  `fill_pet40`). Zero mechanism edits. The harness main is committed
  as `FU6_ADV_HARNESS_MAIN.zag` in this directory.
- Pure Zag throughout: fixtures, harness, builds, runs, greps, md5,
  cmp, diff, git show. Zero Python at any stage.
- Each attack run 3x; all three runs byte-identical via cmp
  (deterministic 3/3).
- Raw evidence: `FU6_ADV_RAW.txt` (940 lines, program output only,
  direct binary run), md5 `7c5fc95cac535500f25264055c1afcba` x3.
- Binaries built in /tmp/fu6adv only; never committed.
- Only `docs/lab/research-lead/overnight-20260928/fdcr_unified6_adv/`
  paths staged. No other worker's files touched. No broad git add.
- No em dashes in this documentation.
- One fixture correction, disclosed below (X-FU6-1 step 5). The
  prereg's kill criteria were not weakened: the corrected fixture
  tests the same dedup property through the actually-reachable path.

## Frozen mechanism under test (code reading, before any attack run)

- `noadd_drop_record` (lines 1472-1500 of `unified_fdcr6.zag`):
  increments NOADD_DROP_COUNT on every call; dedups the 64-entry name
  list by subject CONTENT via `streq` on `con_str_at` reads; appends to
  a free slot if the subject is new; increments NOADD_DROP_OVERFLOW
  only when the list is full AND the subject is new and distinct.
  Drop-list entries are never cleared (writes only in `noadd_drop_init`
  and `noadd_drop_record`, verified by grep).
- `handle_proc_learn_unified` NOTE logic (lines ~1690-1722): counts
  `nlost` (inputs with `con_vote_concept<0` AND `noadd_vote_lost==1`)
  and `nnovote` (inputs with `con_vote_concept<0` AND
  `noadd_vote_lost==0`). If `nlost>0`: definite NOTE carrying the
  lifetime drop total. Else if `nnovote>0 && overflow>0`: uncertainty
  NOTE. Else: silence.
- Strings are interned append-only (`con_intern`: "Simple linear
  append; no deduplication in v1"); `mem_off` values stored in the
  drop list never dangle or get reused.
- `noadd_drop_record` has exactly one call site: `noadd_record`, in
  the NOADD-table-full branch (line 1564). Overflow can only increment
  on a genuine vote refusal.

## X-FU6-1 (Dedup: drop, re-drop, member-after-drop, re-drop) -- FAILS

Setup (world W1): 40 `T sN | is_a | pet` facts fill the pet concept
(8 members) and the NOADD vote table (32 entries), matching G-T1.

1. `T x | is_a | pet` twice. Result: `noadd_drop_total==2`,
   exactly 1 name slot holds content "x", `noadd_drop_overflow==0`,
   `noadd_vote_lost("x")==1`. Repeated drops of one subject consume
   exactly one name slot. PASS.
2. `T x | is_a | animal`: x becomes member of new concept 1
   (`con_find_member_str("x")==1`). The stale drop-list entry for x
   persists (entries are never cleared).
3. Re-drop of member x. FIXTURE CORRECTION (disclosed): the prereg
   assumed `T x | is_a | pet` would route x through `noadd_record`.
   It does not. `handle_concept_learn` Pass 2 checks
   `con_find_member_str` first; an existing member takes the
   concept-extension path (`subject [x] -> concept 1 (total nfeat=2)`),
   never reaching `con_form`/`noadd_record`. A concept member
   therefore CANNOT be re-dropped through the public learn path. The
   same property holds by construction: `con_form` (the only caller
   path to `noadd_record` besides merge) is only invoked when
   `existing<0`. The re-drop of a member IS reachable through
   merge-overflow (`con_merge_into` calls `noadd_record` for moved
   members when the surviving concept is full), so the dedup was
   tested directly: `noadd_record(W1, con_intern(W1,"x"), pet_concept)`
   with x a member and NOADD full. Result: the WARN fired,
   `noadd_drop_total==3`, exactly 1 name slot holds "x",
   `noadd_drop_overflow==0`, `noadd_vote_lost("x")==1`,
   `con_vote_concept("x")==1`. The dedup correctly identifies the
   member subject as already named. PASS.
4. Procedure `s1>1s` (member input): zero `ULEARN: NOTE` lines between
   the STEP6 banners. The stale drop-list entry for the now-member x
   does not produce a spurious NOTE, because the NOTE counters gate on
   `con_vote_concept<0` before consulting `noadd_vote_lost`. PASS.

No kill criterion (a/b/c/d) fired. X-FU6-1 FAILS. Causal reading:
the dedup is content-based over append-only strings, so it is sound
for every reachable re-drop path (repeated learn drops, direct
re-record, merge-overflow re-record). The learn path additionally
makes member re-drop unreachable, which shrinks the attack surface
rather than widening it.

## X-FU6-2 (Uncertainty NOTE: trigger conditions) -- FAILS

Setup (world W2): 40 pet subjects + d1..d65 (65 distinct drops).

1. After d65: `noadd_drop_total==65`, `noadd_drop_overflow==1`. The
   65th distinct drop increments overflow exactly once. Setup PASS.
2. Two further `T d65 | is_a | pet` drops: `noadd_drop_total==67`,
   `noadd_drop_overflow==3`. CONFIRMED: overflow increments per drop
   EVENT of an unnamed subject while the list is full, not per
   distinct subject. The frozen comment ("distinct subjects dropped
   beyond the 64-name capacity") misdescribes the implementation.
   Recorded as a doc/code semantic mismatch (new boundary B-FU6-1
   below). The NOTE wording ("3 beyond name capacity") remains true
   of events; no false claim is emitted.
3. Procedure `s1>1s;ghost>tsohg` (ghost never taught, features match
   no concept; genuine historical overflow>0): exactly one
   `ULEARN: NOTE vote status uncertain...` line, zero definite
   `lost concept votes` lines. Raw line:
   `ULEARN: NOTE vote status uncertain for some train input(s)
   (NOADD drop name capacity exceeded; 67 total drops, 3 beyond name
   capacity); train_con may exclude lost votes`.
   - No KILL (a): no false definite claim.
   - No KILL (b): no silence; the uncertainty NOTE fires as R2
     specifies.
   - No DOWNGRADE (c): overflow>0 could not be produced without a
     genuine NOADD-table-full refusal. `noadd_drop_record`'s single
     call site (line 1564) sits inside `noadd_record`'s table-full
     branch; attempts to drop without filling NOADD first never
     reach it (the table accepts the vote instead). The uncertainty
     NOTE's precondition is not spoofable.

X-FU6-2 FAILS. Causal reading: the uncertainty NOTE is a deliberately
conservative signal per frozen R2 ("the vote status is uncertain (not
'never voted')"). It fires for genuinely never-voted inputs when
historical overflow exists, which is the documented design tradeoff:
the procedure layer cannot distinguish "matched no concept" from
"matched a concept but the vote was lost beyond name capacity", so it
reports uncertainty rather than asserting "never voted". The signal is
honest because it is labeled uncertain and never claims a definite
loss.

## X-FU6-3 (65th distinct subject: loss must not be silent) -- FAILS

Setup (world W3): 40 pet subjects + d1..d64 (64 distinct drops, all
named): `noadd_drop_overflow==0`. Then `T d65 | is_a | pet` (65th
distinct): `noadd_drop_overflow==1`, `noadd_vote_lost("d65")==0`.

1. Procedure `s1>1s;d65>56d`: exactly one uncertainty NOTE, zero
   definite NOTEs. The 65th subject's genuine vote loss is signaled,
   not silent. No KILL (a), no KILL (b). PASS.
2. Mixed procedure `s1>1s;d1>1d;d65>56d` (d1: named definite loss;
   d65: unnamed uncertain loss): the definite NOTE fires
   (`ULEARN: NOTE 1 train input(s) lost concept votes (NOADD table
   full; 65 total drops); train_con computed without them`), and the
   uncertainty NOTE does NOT fire (if/else structure). d65's
   uncertainty is swallowed when any definite loss exists. The frozen
   code is explicit about the if/else, so this is by design;
   recorded as a minor information-loss boundary (new boundary
   B-FU6-2 below). The definite NOTE's count ("1") is accurate for
   definite losses; it does not claim to enumerate uncertain ones.

X-FU6-3 FAILS on both kill criteria. The 64/65 boundary behaves
exactly as the frozen R1/R2 specify.

## X-FU6-4 (Regression and source audit) -- PASSES (defense holds)

1. Rebuilt `unified_fdcr6.zag` from `git show HEAD:...` (pristine
   blob; cmp-verified identical to the working file). Three runs:
   byte-identical via cmp (deterministic 3/3), md5
   `4a6cb7179a588bd09cecbe4d3bbfffba` x3, cmp-verified byte-identical
   to committed `FDCR_UNIFIED6_RAW.txt`, 0 FAIL lines, final tally
   `42/42`, exit 0.
2. Diff `unified_fdcr5.zag` vs `unified_fdcr6.zag` (135 diff lines):
   the change set is exactly R1 (dedup loop + overflow counter +
   `noadd_drop_overflow` accessor in `noadd_drop_record`), R2
   (`nnovote` counting, definite NOTE carrying the lifetime total,
   uncertainty NOTE branch), and R3 (PART G tests). No other
   mechanism function differs.
3. Grep on the pristine blob: exactly one `noadd_drop_record` call
   site (line 1564, genuine table-full branch); `NOADD_DROP_BASE`
   written only in `noadd_drop_init` and `noadd_drop_record`
   (never cleared).

No kill criterion fired. X-FU6-4 PASSES.

## New confirmed boundaries (do not change the verdict)

- B-FU6-1 (overflow semantics): NOADD_DROP_OVERFLOW counts drop
  EVENTS beyond name capacity, not distinct subjects. Evidence:
  one distinct subject (d65) dropped 3 times yields overflow==3.
  The frozen comment says "distinct subjects dropped beyond the
  64-name capacity"; the implementation increments per event. The
  emitted NOTE ("O beyond name capacity") is true of events, so no
  false claim is made, but the comment and the FU6 result doc's
  gloss should be corrected to event semantics.
- B-FU6-2 (mixed definite+uncertain): when a procedure has both a
  named definite vote loss and an unnamed uncertain one, only the
  definite NOTE fires; the uncertainty is not separately signaled
  (explicit if/else in the frozen code). Minor information loss by
  design.
- B-FU6-3 (stale drop-list entries): a subject that becomes a concept
  member keeps its drop-list name entry forever (entries are never
  cleared), permanently occupying one of the 64 name slots. Harmless
  to correctness (NOTE counters gate on `con_vote_concept<0` first),
  but it reduces effective name capacity by one per such subject.
- B-FU6-4 (conservative uncertainty): any never-voted procedure
  input triggers the uncertainty NOTE whenever historical overflow>0,
  even if this procedure lost no votes. Deliberate per frozen R2;
  the NOTE is labeled uncertain, never definite.

## Classification

H-FDCR-UNIFIED6 remains a bounded L2 integration repair (honest
signaling). No L3 claimed, none observed. The red team found no
silent vote loss, no false definite claim, no spoofable precondition,
no dedup failure, and no regression. The two substantive findings
(B-FU6-1 event-vs-distinct semantics, B-FU6-2 mixed-case information
loss) are disclosed boundaries of the frozen design, not verdict
changers.

## Suggested follow-ups for parent

1. Correct the FU6 result doc and the source comment to describe
   NOADD_DROP_OVERFLOW as counting drop events beyond name capacity
   (B-FU6-1), not distinct subjects.
2. Consider, in a future hypothesis, whether the mixed
   definite+uncertain case (B-FU6-2) should emit both NOTEs. Not
   required for the FU6 claim.
3. The research paper's H-FDCR-UNIFIED6 entry should record this red
   team: SURVIVES, 4 attacks fail, with B-FU6-1 through B-FU6-4 as
   confirmed boundaries.
