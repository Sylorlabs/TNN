# PREREG H-FDCR-UNIFIED7: Distinct Overflow, Both NOTEs, Drop-Clear

**Date:** 2026-09-29
**Researcher:** H-FDCR-UNIFIED7 Frontier Researcher (independent subagent)
**Target:** H-FDCR-UNIFIED6 SURVIVES (42/42). Prereg `814724be5`,
  result `0480f10a6`. Red team SURVIVES (4 attacks fail; confirmed
  boundaries B-FU6-1 through B-FU6-4).
**Hypothesis:** The three repairable confirmed boundaries can be closed
  at the mechanism level: (B-FU6-1) make NOADD_DROP_OVERFLOW genuinely
  per-distinct-subject via a second name list, with an honest event
  tier where distinctness is unknowable; (B-FU6-2) emit both NOTEs in
  the mixed definite+uncertain case instead of swallowing the
  uncertainty signal; (B-FU6-3) clear a subject's drop-list name entry
  when it becomes a concept member, so stale entries stop permanently
  consuming name capacity. B-FU6-4 (conservative uncertainty NOTE) is
  deliberate design and stays unchanged.

## Repairs (frozen)

**R1: Distinct-subject overflow (closes B-FU6-1).**
New memory: NOADD_DROP_OVN=2932 (64 entries of 4-byte subject string
offsets; ends 3188); NOADD_DROP_OVERFLOW2=3188 (one i32: drop events
beyond both name lists, where distinctness is unknowable). The
2932..4089 region is verified free (no literals in range; WORK=4096).
`noadd_drop_init` zeroes the overflow-name list and OVERFLOW2.
`noadd_drop_record`: main-list dedup and append unchanged. On
main-list-full with a new distinct subject: dedup against the
overflow-name list by content; if found, return (already counted as a
distinct overflow). Else if a free overflow slot exists: append there
and increment NOADD_DROP_OVERFLOW. Else: increment
NOADD_DROP_OVERFLOW2 (event count, honestly labeled).
`noadd_vote_lost` scans BOTH name lists: a subject named in either is
a definitely-known lost vote. Definite knowledge extends from 64 to
128 distinct subjects.
New accessor `noadd_drop_overflow2(W)`.
NOADD_DROP_OVERFLOW now genuinely counts distinct subjects dropped
beyond the 64-name capacity, matching its frozen comment.

**R2: Both NOTEs in the mixed case (closes B-FU6-2).**
In `handle_proc_learn_unified`, replace the definite/uncertainty
if/else with two independent ifs: the definite NOTE fires when
nlost>0 (wording unchanged); the uncertainty NOTE fires when
nnovote>0 AND (overflow>0 OR overflow2>0).
Uncertainty NOTE wording:
`ULEARN: NOTE vote status uncertain for some train input(s) (NOADD drop
name capacity exceeded; T total drops, O distinct subject(s) beyond
name capacity[; E further drop events beyond overflow naming
capacity]); train_con may exclude lost votes`
where the bracketed clause appears only when E>0.

**R3: Drop-clear on membership (closes B-FU6-3).**
New fn `noadd_drop_clear(W, mem_off)`: content-based clear of the
subject's entry in BOTH name lists (slot set to -1). Lifetime
counters are unchanged. Called at the three member-adding sites:
`con_form` match branch, `con_form` new-concept branch, and
`con_merge_into` member move.
Safety: members always have con_vote_concept>=0, so the NOTE counters
never consult the drop list for them; clearing cannot change any NOTE
and cannot affect vote outcomes.

**R4: PART H tests** (H-T1..H-T5) appended after PART G. PART G and
earlier tests untouched.

## Frozen kill bars

**K-FU7-1 (distinct overflow, event dedup):** G-T2 world replay
(40 pet subjects, then d1..d70): requires noadd_drop_total()==70,
noadd_drop_overflow()==6, noadd_drop_overflow2()==0. Then two more
`T d65 | is_a | pet`: requires total==72, overflow==6 (unchanged;
d65 already overflow-named), overflow2==0. (Under FU6: overflow==8.)

**K-FU7-2 (overflow-name is definite knowledge):** Procedure
`s1>1s;d70>07d` on the G-T2 world: requires train_con==-1 AND
noadd_vote_lost("d70")==1 (d70 named in the overflow list, so the
definite NOTE is the honest signal; raw output must show the definite
`1 train input(s) lost concept votes` NOTE, not the uncertainty NOTE).
(Under FU6: uncertainty NOTE.)

**K-FU7-3 (both NOTEs):** Procedure `s1>1s;d1>1d;ghost>tsohg` on the
G-T2 world (d1 main-list named; ghost never taught): requires the
definite NOTE conditions (vote_lost("d1")==1) AND the uncertainty
conditions (con_vote_concept("ghost")<0, vote_lost("ghost")==0,
overflow>0) to hold simultaneously, so per R2 both NOTEs must fire;
raw output must contain both the `1 train input(s) lost concept
votes` line and the `vote status uncertain` line. (Under FU6: only
the definite NOTE.)

**K-FU7-4 (stale entry clearing):** 40 pet subjects, then
`T x | is_a | pet` (x dropped): requires noadd_vote_lost("x")==1.
Then `T x | is_a | animal` (x becomes a member): requires
noadd_vote_lost("x")==0 (entry cleared) and con_vote_concept("x")>=0.
Then 64 distinct `T n1..n64 | is_a | pet`: requires all 64 named,
noadd_drop_overflow()==0, noadd_drop_total()==65. (Under FU6:
overflow==1, because x's stale entry consumed a name slot.)

**K-FU7-5 (second tier honesty):** 40 pet subjects, then d1..d130
(130 distinct drops): requires noadd_drop_total()==130,
noadd_drop_overflow()==64, noadd_drop_overflow2()==2. Procedure
`s1>1s;ghost>tsohg`: the uncertainty NOTE must fire; raw output must
contain `64 distinct subject(s) beyond name capacity` and `2 further
drop events beyond overflow naming capacity`.

**K-FU7-6 (preserved/superseded):** K-FU6-1 (G-T1) PASS unchanged:
total==71, vote_lost("rep")==1, vote_lost("v")==1, overflow==0.
Parts A-E output byte-identical to FU6 (verified by cmp on the raw
prefix; R2/R3 emit nothing new there). Part F NOTEs unchanged
(F-T1/F-T2 have overflow==0, so no uncertainty NOTE can fire; definite
wording unchanged). 42/42 preserved checks + 5 new = 47.

**K-FU7-7 (deterministic):** 3 consecutive full runs byte-identical
(cmp), exit 0, 0 FAIL lines.

## Governance

- Prereg committed alone BEFORE any implementation edit, build, or run.
- `unified_fdcr7.zag` = `unified_fdcr6.zag` copied verbatim
  (cmp-verified) plus exactly the frozen R1-R4 changes.
  `unified_fdcr6.zag` untouched.
- Pure Zag throughout: fixtures, implementation, builds, runs, greps,
  md5, cmp. Zero Python at any stage.
- No binaries committed (builds in /tmp/fu7 only).
- Only owned files staged/committed (pathspec-restricted).
- No em dashes in loop documentation.
- Mechanism diff vs unified_fdcr6.zag must touch exactly the
  preregistered lines (new memory constants and comment, init,
  record, vote_lost, clear fn, three call sites, NOTE if/else and
  wording, PART H). All other mechanism functions untouched.

## Classification

Bounded L2 integration repair (honest signaling). Not L3. The
name-list capacities remain (64 + 64); the improvement is that
overflow is now genuinely per-distinct-subject, the mixed case
signals both facts, and stale entries stop consuming capacity.
