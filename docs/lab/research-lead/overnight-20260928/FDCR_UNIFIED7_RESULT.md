# H-FDCR-UNIFIED7 RESULT: SURVIVES (47/47)

**Date:** 2026-09-29
**Researcher:** H-FDCR-UNIFIED7 Frontier Researcher (independent subagent)
**Target:** H-FDCR-UNIFIED6 SURVIVES (42/42). Prereg `814724be5`,
  result `0480f10a6`. Red team SURVIVES (4 attacks fail; confirmed
  boundaries B-FU6-1 through B-FU6-4).
**Verdict:** SURVIVES. All seven frozen kill bars PASS (47/47 named
  checks: 41 preserved + 1 superseded + 5 new), deterministic 3/3.
  Classification: bounded L2 integration repair (honest signaling).
  No L3 claimed.

## Lineage

- Prereg `PREREG_FDCR_UNIFIED7.md` committed alone as `855322a77`
  BEFORE any implementation edit, build, or run.
- AMENDMENT 1 committed alone as `42cbe6396` BEFORE the test-code
  change and the re-run. The amendment is transparent and post-first-
  run: the first run exposed a prereg inconsistency (see below). No
  threshold was weakened; the mechanism was untouched by the
  amendment.
- `unified_fdcr7.zag` = `unified_fdcr6.zag` copied verbatim
  (cmp-verified) plus exactly the frozen R1-R4 changes and the
  Amendment 1 test-code update. `unified_fdcr6.zag` untouched.
- Prereg is a verified strict ancestor of the result commit
  (merge-base --is-ancestor; verified at commit time).
- Pure Zag throughout: fixtures, implementation, builds, runs, greps,
  md5, cmp, diff, git show. Zero Python at any stage.
- No binaries committed (builds in /tmp/fu7 only).
- Only owned files staged/committed (pathspec-restricted).
- No em dashes in loop documentation.

## Repairs implemented (exactly per frozen prereg)

**R1: Distinct-subject overflow (closes B-FU6-1).**
New memory: NOADD_DROP_OVN=2932 (64 entries of 4-byte subject string
offsets; ends 3188); NOADD_DROP_OVERFLOW2=3188 (one i32: drop events
beyond both name lists, where distinctness is unknowable). The
2932..4089 region was verified free (no literals in range; WORK=4096).
`noadd_drop_init` zeroes the overflow-name list and OVERFLOW2.
`noadd_drop_record`: main-list dedup and append unchanged. On
main-list-full with a new distinct subject: dedup against the
overflow-name list by content; if found, return (already counted as a
distinct overflow). Else if a free overflow slot exists: append there
and increment NOADD_DROP_OVERFLOW. Else: increment
NOADD_DROP_OVERFLOW2 (event count, honestly labeled).
`noadd_vote_lost` scans BOTH name lists: a subject named in either is
a definitely-known lost vote. Definite knowledge extends from 64 to
128 distinct subjects. New accessor `noadd_drop_overflow2(W)`.
NOADD_DROP_OVERFLOW now genuinely counts distinct subjects dropped
beyond the 64-name capacity, matching its frozen comment. The FU6
doc/code semantic mismatch (B-FU6-1) is closed at the mechanism level,
not just relabeled.

**R2: Both NOTEs in the mixed case (closes B-FU6-2).**
In `handle_proc_learn_unified`, the definite/uncertainty if/else
became two independent ifs: the definite NOTE fires when nlost>0
(wording unchanged); the uncertainty NOTE fires when nnovote>0 AND
(overflow>0 OR overflow2>0).
Uncertainty NOTE wording:
`ULEARN: NOTE vote status uncertain for some train input(s) (NOADD
drop name capacity exceeded; T total drops, O distinct subject(s)
beyond name capacity[; E further drop events beyond overflow naming
capacity]); train_con may exclude lost votes`
(the bracketed clause appears only when E>0).

**R3: Drop-clear on membership (closes B-FU6-3).**
New fn `noadd_drop_clear(W, mem_off)`: content-based clear of the
subject's entry in BOTH name lists (slot set to -1). Lifetime
counters are unchanged. Called at the three member-adding sites:
`con_form` match branch, `con_form` new-concept branch, and
`con_merge_into` member move. Safety: members always have
con_vote_concept>=0, so the NOTE counters never consult the drop list
for them; clearing cannot change any NOTE or vote outcome.

**R4: PART H tests** (H-T1..H-T5) appended after PART G, with two
test-only world-builder helpers (`fu7_g2_world`, `fu7_pet40_world`).
PART G and earlier tests untouched except the Amendment 1 G-T2
update.

## Amendment 1 (transparent, post-first-run)

First run: 46/47, deterministic 3/3 (md5
`425f693a28398b4f19faf65b9d96e417` x3, exit 1), preserved as
`FDCR_UNIFIED7_RAW_PRE_AMEND.txt`. The single failure was G-T2's
legacy condition `noadd_vote_lost("d70")==0` (observed 1; all other
G-T2 conditions passed: total=70, overflow=6, train_con=-1,
d70vote=-1).

Root cause: prereg inconsistency, not mechanism failure. Frozen R1
specifies "`noadd_vote_lost` scans BOTH name lists", and frozen
K-FU7-2 requires `noadd_vote_lost("d70")==1`; both entail that d70
(overflow-named) is definitely-known. K-FU7-6's claim "G-T2 PASS
unchanged" was therefore unsatisfiable as written: the frozen R1 and
K-FU7-2 jointly contradicted it, and the execution exposed the
contradiction. The mechanism behaved exactly as R1 specifies (pre-
amend raw line 1832: the G-T2 procedure fired the definite NOTE for
d70, not the uncertainty NOTE).

Disposition: G-T2's `d70lost==0` condition is SUPERSEDED by R1.
G-T2's surviving intent (d70's genuine vote loss is signaled, not
silent; train_con==-1) is preserved and strengthened: under R1 the
signal is the definite NOTE rather than the uncertainty NOTE
(K-FU7-2 verifies the definite NOTE fires). No threshold was
weakened: the new expectation (d70 definitely-known) is strictly more
informative than the old one (d70 unknown). The amendment changed
test code only; the mechanism was untouched. K-FU7-6 was corrected
to: 41/42 preserved checks PASS unchanged, G-T2's d70lost condition
superseded per R1, 5 new checks PASS: 47/47.

## Frozen kill-bar evidence

Raw: `FDCR_UNIFIED7_RAW.txt` (md5
`a28b0dca016472b1daad625e0b3d56b4` x3), program output only (direct
binary run).

- **K-FU7-1 PASS** (raw line 2249): H-T1 (G-T2 world + two extra
  `T d65 | is_a | pet`): noadd_drop_total()==72,
  noadd_drop_overflow()==6 (unchanged by the re-drops; d65 already
  overflow-named), noadd_drop_overflow2()==0. Overflow is genuinely
  per-distinct-subject. (Under FU6: overflow==8.)
- **K-FU7-2 PASS** (raw line 2654): H-T2 (procedure `s1>1s;d70>07d`
  on the G-T2 world): train_con==-1 AND noadd_vote_lost("d70")==1.
  Raw line 2652 shows the definite NOTE firing:
  `ULEARN: NOTE 1 train input(s) lost concept votes (NOADD table
  full; 70 total drops); train_con computed without them`.
  d70's loss is now definitely-known; the uncertainty NOTE does not
  fire (nnovote==0). (Under FU6: uncertainty NOTE.)
- **K-FU7-3 PASS** (raw line 3060): H-T3 (procedure
  `s1>1s;d1>1d;ghost>tsohg`): definite conditions
  (vote_lost("d1")==1, d1 has no vote) and uncertainty conditions
  (ghost has no vote, ghost not lost, overflow>0) co-occur. Raw
  lines 3058-3059 show BOTH NOTEs firing consecutively:
  `ULEARN: NOTE 1 train input(s) lost concept votes (NOADD table
  full; 70 total drops); train_con computed without them` then
  `ULEARN: NOTE vote status uncertain for some train input(s)
  (NOADD drop name capacity exceeded; 70 total drops, 6 distinct
  subject(s) beyond name capacity); train_con may exclude lost
  votes`. (Under FU6: only the definite NOTE.)
- **K-FU7-4 PASS** (raw line 3447): H-T4 (40 pet + `T x | is_a |
  pet` then `T x | is_a | animal` then 64 distinct `T n1..n64 |
  is_a | pet`): noadd_vote_lost("x")==0 (stale entry cleared on
  membership), con_vote_concept("x")>=0, noadd_drop_overflow()==0,
  noadd_drop_total()==65. All 64 new distinct drops were named; x's
  freed slot was reused. (Under FU6: overflow==1 from x's stale
  slot.)
- **K-FU7-5 PASS** (raw line 4095): H-T5 (40 pet + d1..d130, 130
  distinct drops): noadd_drop_total()==130,
  noadd_drop_overflow()==64, noadd_drop_overflow2()==2. Raw line
  4096 shows the uncertainty NOTE carrying both tiers honestly:
  `ULEARN: NOTE vote status uncertain for some train input(s)
  (NOADD drop name capacity exceeded; 130 total drops, 64 distinct
  subject(s) beyond name capacity; 2 further drop events beyond
  overflow naming capacity); train_con may exclude lost votes`.
- **K-FU7-6 PASS:** 41/42 preserved checks PASS unchanged, G-T2's
  d70lost condition superseded per Amendment 1 (raw line 1834:
  `G-T2 overflow: 70 drops, 6 overflow, train_con=-1, d70
  definitely-known PASS`). Parts A-E output (raw lines 1-431)
  byte-identical to FU6 via cmp. Part F (raw lines 432-955)
  byte-identical to FU6 (F-T1/F-T2 have overflow==0, so no
  uncertainty NOTE can fire; definite wording unchanged). Full-file
  diff FU6 raw vs FU7 raw: exactly the G-T2 NOTE/PASS lines and the
  appended PART H; nothing else differs.
- **K-FU7-7 PASS:** 3 consecutive full runs byte-identical (cmp);
  md5 `a28b0dca016472b1daad625e0b3d56b4` x3; exit 0; 0 FAIL lines.

Final tally: **47/47. H-FDCR-UNIFIED7 SURVIVES.**

## Honest residuals (disclosed, not repaired)

- Name-list capacities remain: 64 main + 64 overflow names. The 129th
  distinct dropped subject is unnamed; its drop is counted as an
  event in NOADD_DROP_OVERFLOW2 and the NOTE labels it honestly
  ("further drop events beyond overflow naming capacity",
  distinctness unknowable). Definite knowledge covers 128 distinct
  subjects; beyond that the signal degrades gracefully to honest
  event counts, never to silence.
- B-FU6-4 (conservative uncertainty) is unchanged by design: any
  never-voted procedure input triggers the uncertainty NOTE whenever
  historical overflow>0, even if the current procedure lost no votes.
  The NOTE is labeled uncertain, never definite.
- The lifetime counters (total drops, overflow) are historical, not
  per-procedure. R3 frees name slots on membership but does not
  rewrite history: a subject whose vote was genuinely lost and later
  becomes a member keeps its contribution to the lifetime totals.
- First-seen tie break in the voter is unchanged (disclosed in FU5).

## Governance disclosures

1. Prereg committed alone as `855322a77` before any implementation;
   ordering verified by merge-base --is-ancestor at commit time.
2. Amendment 1 (`42cbe6396`) was post-first-run and is disclosed in
   full above: it corrected a prereg inconsistency (R1+K-FU7-2 vs
   K-FU7-6), changed test code only, weakened no threshold, and was
   committed alone before the test-code change and re-run. The
   pre-amend 46/47 run is preserved as
   `FDCR_UNIFIED7_RAW_PRE_AMEND.txt`.
3. Pure Zag throughout. Zero Python at any stage (fixtures,
   implementation, builds, runs, greps, md5, cmp, diff).
4. No binaries committed (builds in /tmp/fu7 only).
5. Only owned files staged/committed
   (PREREG_FDCR_UNIFIED7.md, unified_fdcr7.zag,
   FDCR_UNIFIED7_RAW.txt, FDCR_UNIFIED7_PRE_AMEND raw,
   FDCR_UNIFIED7_RESULT.md). No other worker's files touched.
   Pathspec-restricted staging used throughout.
6. No em dashes in loop documentation.
7. Mechanism diff vs unified_fdcr6.zag: hunks touch exactly the
   preregistered lines (new memory constants and layout comment,
   noadd_drop_init, noadd_drop_record, noadd_drop_clear,
   noadd_drop_overflow2 accessor, noadd_vote_lost both-list scan,
   three noadd_drop_clear call sites in con_form/con_merge_into,
   NOTE if/else and wording, PART H tests and helpers, Amendment 1
   G-T2 test update). All other mechanism functions untouched.
8. `unified_fdcr6.zag` and all prior evidence files untouched.

## Suggested follow-ups for parent

1. Independent red team on H-FDCR-UNIFIED7 (natural attacks: X-FU7-1
   overflow-list dedup under merge-overflow re-record paths; X-FU7-2
   R3 clearing vs a subject dropped, membered, then dropped again;
   X-FU7-3 the overflow2 tier boundary at 128/129 distinct subjects;
   X-FU7-4 both-NOTE emission under nlost>0 with overflow2>0 only).
2. The research paper's H-FDCR-UNIFIED7 entry should record: SURVIVES
   47/47, B-FU6-1/B-FU6-2/B-FU6-3 closed at the mechanism level,
   B-FU6-4 retained by design, and Amendment 1 (transparent
   post-first-run prereg correction, 46/47 pre-amend raw preserved).
