# H-FDCR-UNIFIED6 RESULT: SURVIVES (42/42)

**Date:** 2026-09-29
**Researcher:** H-FDCR-UNIFIED6 Frontier Researcher (independent subagent)
**Target:** H-FDCR-UNIFIED5 SURVIVES (40/40). Prereg `1813a6547`, result
  `e28a9c430`. Red team SURVIVES (3 fail, 1 succeeds as CONFIRMED
  DISCLOSED BOUNDARY with refinement: the bound is 64 drop EVENTS, not
  64 distinct subjects).
**Verdict:** SURVIVES. All four frozen kill bars PASS (42/42 named
  checks: 40 preserved + 2 new). Classification: bounded L2 integration
  repair (honest signaling). No L3 claimed.

## Lineage

- Prereg `PREREG_FDCR_UNIFIED6.md` committed alone as `814724be5`
  BEFORE any implementation edit, build, or run. No amendments.
- `unified_fdcr6.zag` = `unified_fdcr5.zag` copied verbatim
  (cmp-verified) plus exactly the frozen R1-R3 changes.
  `unified_fdcr5.zag` untouched.
- Prereg is a verified strict ancestor of the result commit
  (merge-base --is-ancestor).
- Pure Zag throughout: fixtures, implementation, builds, runs, greps,
  md5, cmp. Zero Python at any stage.

## Repairs implemented (exactly per frozen prereg)

**R1: Drop-list dedup + overflow counter.**
`noadd_drop_record` now dedups by subject content: if the subject is
already named in the 64-entry list, only the authoritative total
increments; no new name slot is consumed. If the list is full and the
subject is new and distinct, NOADD_DROP_OVERFLOW increments. New memory:
NOADD_DROP_OVERFLOW=2928 (one i32, after the 64-entry name list ending
at 2928). New function `noadd_drop_overflow(W)`. The 64-entry bound is
now genuinely per-subject, not per-drop-event, making the FU5 disclosure
("64 distinct subjects") accurate.

**R2: Honest procedure-layer NOTE.**
In `handle_proc_learn_unified`: nlost counts inputs with
con_vote_concept<0 AND noadd_vote_lost==1 (unchanged semantics);
nnovote counts inputs with con_vote_concept<0 AND noadd_vote_lost==0.
If nlost>0: NOTE now includes the authoritative total:
`ULEARN: NOTE N train input(s) lost concept votes (NOADD table full;
T total drops); train_con computed without them`.
If nlost==0 but nnovote>0 and overflow>0: emit the uncertainty NOTE:
`ULEARN: NOTE vote status uncertain for some train input(s) (NOADD
drop name capacity exceeded; T total drops, O beyond name capacity);
train_con may exclude lost votes`. This closes the X-FU5-2 B1 silence:
the pivotal -1 no longer reads as "no concept applied" without signal.

**R3: PART G tests** (G-T1, G-T2) appended after PART F. The
H-FDCR-UNIFIED5 banner lines are preserved so Parts A-F stay
byte-comparable (Parts A-E have zero NOTE lines; Part F NOTEs use the
new wording, documented as supersession in K-FU6-3).

## Frozen kill-bar evidence

Raw: `FDCR_UNIFIED6_RAW.txt` (md5 `4a6cb7179a588bd09cecbe4d3bbfffba`),
program output only (direct binary run).

- **K-FU6-1 PASS:** G-T1 (X-FU5-2 World C replay: 70 cross-batch
  `T rep | is_a | pet` + `T v | is_a | pet`): noadd_drop_total()==71,
  name list holds exactly 2 distinct entries, noadd_vote_lost("rep")==1,
  noadd_vote_lost("v")==1, noadd_drop_overflow()==0. The bound is
  genuinely per-subject. (Under FU5: vote_lost("v")==0.)
- **K-FU6-2 PASS:** G-T2 (X-FU5-2 World B replay: 40 subjects then
  d1..d70, 70 distinct): noadd_drop_total()==70,
  noadd_drop_overflow()==6 (d65..d70 beyond 64 distinct). Procedure
  `s1>1s;d70>07d`: train_con==-1 AND the uncertainty NOTE fires:
  `ULEARN: NOTE vote status uncertain for some train input(s) (NOADD
  drop name capacity exceeded; 70 total drops, 6 beyond name capacity);
  train_con may exclude lost votes` (raw line 1832). The B1 silence is
  closed. (Under FU5: zero NOTE lines.)
- **K-FU6-3 PASS:** All K-FU5-1..K-FU5-4 preserved with explicit
  supersessions: (a) F-T1 NOTE now reads `... (NOADD table full;
  1 total drops); ...` (raw line 560); (b) F-T2 NOTE now reads
  `... (NOADD table full; 9 total drops); ...` (raw line 722);
  (c) Parts A-E output (lines 1-431) byte-identical to FU5 via cmp;
  (d) Part F non-NOTE lines byte-identical. 40/40 original checks hold
  (with updated NOTE expectations) + G-T1, G-T2.
- **K-FU6-4 PASS:** 3 consecutive full runs byte-identical (cmp);
  md5 `4a6cb7179a588bd09cecbe4d3bbfffba` x3; exit 0; 0 FAIL lines.

Final tally: **42/42. H-FDCR-UNIFIED6 SURVIVES.**

## Honest residuals (disclosed, not repaired)

- The 64-name capacity remains. Dedup makes it genuinely per-subject,
  but the 65th distinct dropped subject is still unnamed; the
  uncertainty NOTE now signals this instead of silence.
- The authoritative total counter is lifetime, not per-procedure. The
  NOTE shows the lifetime total; a large total with nlost==0 and
  overflow==0 means past drops are irrelevant to the current procedure.
- The NOTE is a diagnostic, not enlarged capacity. A procedure whose
  decisive votes were lost still learns train_con=-1; the NOTE only
  makes the reason explicit (or explicitly uncertain).
- First-seen tie break in the voter is unchanged (disclosed in FU5).

## Governance disclosures

1. Prereg committed alone before any implementation; ordering verified
   by merge-base --is-ancestor.
2. Pure Zag throughout. Zero Python at any stage.
3. No binaries committed (builds in /tmp/fu6 only).
4. Only the four owned files staged/committed
   (PREREG_FDCR_UNIFIED6.md, unified_fdcr6.zag,
   FDCR_UNIFIED6_RAW.txt, FDCR_UNIFIED6_RESULT.md). No other worker's
   files touched. Pathspec-restricted staging used throughout.
5. No em dashes in loop documentation.
6. Mechanism diff vs unified_fdcr5.zag: the R1/R2 modifications touch
   exactly the preregistered lines (dedup logic in noadd_drop_record,
   nnovote counting and NOTE wording in handle_proc_learn_unified);
   all other mechanism functions untouched. Disclosed in prereg.
7. `unified_fdcr5.zag` and all prior evidence files untouched.

## Suggested follow-ups for parent

1. Independent red team on H-FDCR-UNIFIED6 (natural attacks: X-FU6-1
   dedup edge cases - subject that becomes a member after being
   drop-listed, then dropped again; X-FU6-2 uncertainty NOTE spoofing -
   can overflow>0 be triggered without genuine vote loss; X-FU6-3
   the 65th distinct subject boundary).
2. The research paper's H-FDCR-UNIFIED5 entry should record the red-team
   survival AND the refined 64-drop-EVENT boundary; the H-FDCR-UNIFIED6
   entry records the dedup repair (now genuinely per-subject) and the
   uncertainty NOTE.
