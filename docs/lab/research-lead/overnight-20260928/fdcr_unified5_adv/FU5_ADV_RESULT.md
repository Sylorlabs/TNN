# H-FDCR-UNIFIED5 RED TEAM RESULT

**Date:** 2026-09-29
**Researcher:** H-FDCR-UNIFIED5 Red Team (independent subagent)
**Target:** H-FDCR-UNIFIED5 SURVIVES (40/40). Prereg `1813a6547`, result `e28a9c430`.
**Verdict:** H-FDCR-UNIFIED5 SURVIVES this red team. Three attacks fail;
  one succeeds as a CONFIRMED DISCLOSED BOUNDARY with a disclosure
  refinement (no kill, no downgrade).

## Method

- Adversary prereg `PREREG_FU5_ADV.md` committed alone as `1af59a8ae`
  before any adversary build or run. No amendments.
- Adversary harness `fu5_adv.zag`: lines 1-1971 of the committed
  `unified_fdcr5.zag` (full mechanism region; `fn main` starts at line
  1974) copied verbatim, cmp-verified byte-identical, with `main`
  replaced by attack drivers. No mechanism edits.
- All 3 adversary runs byte-identical (program output only, znc `--run`
  wrapper line stripped; md5 `175317d89192b183d55ab8cdc2d06e61`).
  All 3 regression rebuilds byte-identical.
- Pure Zag throughout (fixtures, harness, builds, runs, greps, md5, cmp).
  No Python at any stage.

## X-FU5-1: NOTE spoof / suppression — FAILS, defense holds

World A (F-T1 setup: 41 subjects; C0 = 8 members; NOADD = 32 entries;
s41 dropped; `noadd_drop_total==1`, `noadd_vote_lost("s41")==1`,
`noadd_vote_lost("s1")==0`; sanity line 124 of raw).

- A1 (`s1>1s;s2>2s`, all inputs voting): train_con=0 PASS; zero
  `ULEARN: NOTE ` lines in the section. No spurious NOTE.
- A2 (`s1>1s;ghost>tsohg`, "ghost" never taught): train_con=-1 PASS;
  zero NOTE lines. The never-voted subject correctly does NOT trigger
  the NOTE; the -1 reads as "no concept applied" with no NOTE, which is
  the designed distinction (`noadd_vote_lost("ghost")==0`).
- A3 (`s1>1s;s41>14s`, positive control): exactly one NOTE line:
  `ULEARN: NOTE 1 train input(s) lost concept votes (NOADD table full); train_con computed without them`.

The NOTE fires iff a training input genuinely lost its vote, within the
design envelope. No spoof, no suppression found.

## X-FU5-2: drop-list exhaustion — SUCCEEDS AS DISCLOSED BOUNDARY

World B (40 subjects then d1..d70): `noadd_drop_total==70`;
`noadd_vote_lost("d1")==1`, `("d64")==1`, `("d65")==0`, `("d70")==0`
(raw line 540). The 64-entry name list holds d1..d64; d65..d70 are
counted but unnamed.

- B1 (`s1>1s;d70>07d`): train_con=-1 PASS; ZERO NOTE lines. The pivotal
  -1 outcome carries no vote-exhaustion signal: d70's vote was genuinely
  lost (table full, never recorded) but d70 is beyond the 64th drop
  event, so `noadd_vote_lost==0` and nlost=0. This is the X-FU4-2
  failure mode returning silently past 64 events.
- B2 (`s1>1s;d1>1d`, positive control): exactly one NOTE line with
  "1 train input(s)". Within-64 drops are surfaced correctly.

This confirms the residual already disclosed in
FDCR_UNIFIED5_RESULT.md ("Honest residuals"): past 64 drops,
`noadd_vote_lost` can return 0 for a genuinely lost vote and nlost can
undercount to zero. CONFIRMED BOUNDARY. No verdict change: the limit is
in the frozen prereg (`NOADD_DROP_MAX()=64`, "best-effort naming") and
the result doc's honest residuals.

**Disclosure refinement (new):** World C shows the bound is 64 drop
EVENTS, not "64 distinct subjects" as the residual states. Teaching
`T rep | is_a | pet` in 70 separate batches (cross-batch, no intern
dedup, each misses the full NOADD table) produced 70 drop events;
`noadd_drop_total==71` after `T v | is_a | pet`; `noadd_vote_lost("rep")==1`,
`noadd_vote_lost("v")==0` (raw line 1022). Only 2 distinct subjects
exhausted the 64 name slots, because `noadd_drop_record` appends with no
dedup. Procedure `s1>1s;v>v`: train_con=-1, NO NOTE. The disclosed
"64 distinct subjects" framing understates how easily the list fills;
the accurate bound is 64 drop events. This refines the disclosure; it
does not break R1 within its design envelope.

## X-FU5-3: merge chains with clearing — FAILS, defense holds

World D: C0 (8 members, {is_a=pet}); C1 (8 members,
{is_a=pet,color=orange}); `T s1 | color | orange` triggers
`con_merge_into(C0, C1)`; 8 overflow members recorded as NOADD votes
(table had room); C1 cleared.

- D-merge PASS: `con_count==1`, `con_active(1)==0`, `con_nmem(1)==0`,
  `con_nfeat(1)==0`, `con_vote_concept("m1")==0` (NOADD vote for C0),
  `con_find_member_str("m1")==-1`, `noadd_drop_total==0`.
- D-reuse PASS: `T n1 | size | big` reuses slot 1; `con_active(1)==1`,
  `con_nfeat(1)==1`, `con_nmem(1)==1`, `con_find_member_str("n1")==1`,
  feature 0 content-equal "size=big" (no stale "is_a=pet"/"color=orange").
- D-vote PASS: `n1>1n;n2>2n` gives train_con=1 (reused slot votes correctly).
- D-match PASS: `T z1 | is_a | pet;T z1 | color | orange` gives
  `con_vote_concept("z1")==0` (cleared C1 does not interfere with
  `con_form` matching, which requires `active==1`).

Code reading confirms: Step 1 moves members before Step 4 clears;
`con_find_member`, `con_find_member_str`, `con_merge_check`, and the
cross-batch extension path all gate on `active==1`; the create path
resets `nfeat`/features/`mem[0]`/`nmem` on reuse and all readers are
`nmem`/`nfeat`-bounded, so stale `mem[1..7]` is never read. No stale
data observed anywhere. R2 is safe.

## X-FU5-4: regression and additivity — FAILS, defense holds

Rebuilt from a pristine `git show HEAD:unified_fdcr5.zag` copy:

- 3/3 runs byte-identical (md5 `0718d6cd01ac78bd1df6cd52b90c53bf` after
  stripping the `znc --run` wrapper line; program output only).
- 40 PASS lines, 0 FAIL lines; `=== FDCR-UNIFIED RESULT: 40/40 ===`.
- Output lines 1-431 byte-identical to the committed
  FDCR_UNIFIED5_RAW.txt lines 1-431 (Parts A-E). Full-file diff vs the
  committed raw: only the `znc: program exited 0` trailer line (an
  artifact of `--run`; the builder ran the binary directly).
- Committed FDCR_UNIFIED5_RAW.txt md5 `2f9515e842719da18b5a3255d1681004`
  matches the builder's claimed value.
- `diff unified_fdcr4.zag unified_fdcr5.zag`: 0 removed lines, 317 added
  lines. The mechanism change is PURELY ADDITIVE; zero non-comment lines
  removed or modified. The builder's governance claim holds.

## Causal interpretation

R1 works exactly as specified within its frozen design envelope (64
drop events): the NOTE fires iff a training input's vote was lost to
exhaustion, and never for never-voted subjects. The envelope's edge is
real and now empirically confirmed: past 64 drop events the NOTE can go
completely missing on a pivotal outcome. That edge was disclosed, so it
does not change the verdict; the new information is that the edge is
reached at 64 drop events (not 64 distinct subjects), which is easier to
hit than the disclosure implies. R2's clearing is safe: all readers
gate on active, move precedes clear, and slot reuse is clean. The 40/40
evidence reproduces byte-identically from the committed source.

## Classification

Bounded L2 integration repair, unchanged. Nothing here is L3.

## Commits (branch `tnn-native-lab`, local only)

- `1af59a8ae`: adversary prereg (frozen, pre-execution).
- This result commit: `FU5_ADV_RESULT.md`, `FU5_ADV_RAW.txt`,
  `fu5_adv.zag` under `docs/lab/research-lead/overnight-20260928/fdcr_unified5_adv/`.
  Prereg is a strict ancestor (verified via merge-base --is-ancestor).
  No push attempted.

## Suggested follow-ups for parent

1. The paper's H-FDCR-UNIFIED5 entry should record the red-team
   survival AND the refined 64-drop-EVENT boundary (the current
   "64 distinct subjects" framing is inaccurate).
2. A future H-FDCR-UNIFIED6 could consider drop-list dedup (making the
   bound genuinely per-subject) or including the authoritative drop
   total in the NOTE so undercounting is visible. That is a new
   hypothesis, not a repair of a broken bar.
