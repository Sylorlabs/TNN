# RESULT_WALLREMOVE: CTSVR Implementation

Date: 2026-09-30. Prereg a28ab9873 (committed alone before implementation).
Design: 5daf15951 (DESIGN-COMPLETE). Verdict: BUILD-PASS. All four kill
bars pass.

## Commits (local, tnn-native-lab, owned path only)

- Prereg: a28ab9873 (frozen before any implementation file existed)
- Implementation + result: this commit (wallremove.zag,
  RESULT_WALLREMOVE.md, 3 raw logs, build/run stderr logs)
- Order verified: prereg strictly precedes implementation
  (git merge-base --is-ancestor on a28ab9873).

## What was built

Single-file pure-Zag program (wallremove.zag), adapted from
goalrevise.zag (cb2a6fdbc): the sealed world, layouts, env flag,
information barrier, goals, and action budget are unchanged. CTSVR
additions per the design:

- gen (i32, init 0), wgen[225] (u8 per-cell generation tag),
  transferred flag (0 in Env A, 1 in Env B/C); wgen saved/restored
  with the post-A map.
- T1: on a bump during the normal sweep while transferred==1,
  gen += 1 and the env-change line is logged; the bumped cell is
  marked wall with wgen = gen.
- Re-verify phase: while any stale cell exists (map==2, wgen<gen),
  BFS want==3 targets the nearest stale cell and may route through
  stale cells; probes log PROBE lines; bump==0 marks free (wall
  removed); bump==1 re-tags wgen=gen (wall confirmed) and replans.
- D1 (prereg-disclosed): bumps during re-verify on non-probe cells
  are tagged current-generation discoveries without refiring T1.
- D3 (prereg-disclosed): unreachable stale cells are tagged
  current-gen with a "stale unreachable" line (never triggered in
  the frozen test).

## Results (3/3 byte-identical, md5 64d285b023ef2660213b66a4243d6fc0,
exit 0, zero stderr)

Env A: GOAL_REACHED in 174 actions, 2 bumps (at (5,11) and (10,3)),
2 replans. Replicates cb2a6fdbc exactly. Both walls tagged wgen=0.

Env B (pristine control): GOAL_REACHED in 186 actions, 0 bumps,
probes=0, rv_actions=0, gen=0. CTSVR fully inert; replicates the
published transfer result.

Env C (changed layout): GOAL_REACHED in 234 actions, 2 bumps,
probes=4, rv_actions=46, gen=2.

Trace:

1. Action 179: sweep steps S from (14,8) toward (14,7); BUMP=1.
   T1 fires (transferred==1): gen=1, "REVISE C env-change suspected
   gen=1". (14,7) marked wall, wgen=1.
2. Re-verify (gen=1): stale set = {(5,11), (10,3)} (the only two
   walls in the transferred map, both wgen=0).
   - PROBE (10,3): bump=0. "REVISE C wall removed 10,3". map=1.
   - Routing to (5,11) passes (10,4): bump=1 on an unknown cell.
     D1 discovery: (10,4) marked wall, wgen=1, "reverify discovery",
     no T1 refire.
   - PROBE (5,11): bump=0. "REVISE C wall removed 5,11". map=1.
3. Stale set empty; normal sweep resumes. The sweep probes toward an
   unswept region and bumps (5,10) (unknown cell, real wall in
   Env 1). This is a normal-sweep bump while transferred==1, so T1
   fires per the prereg: gen=2, "REVISE C env-change suspected
   gen=2". (5,10) marked wall, wgen=2.
4. Re-verify (gen=2): stale set = {(14,7) wgen 1, (10,4) wgen 1}.
   - PROBE (10,4): bump=1. "REVISE C wall confirmed 10,4".
     wgen=2.
   - Routing passes (10,7): bump=1 on unknown cell. D1 discovery:
     (10,7) marked wall, wgen=2.
   - PROBE (14,7): bump=1. "REVISE C wall confirmed 14,7".
     wgen=2.
5. Stale set empty; sweep resumes; GOAL_REACHED at action 234.

Post-run MAPDUMP: c147=2 (14,7 wall, confirmed), c511=1 ((5,11)
free, revised), c103=1 ((10,3) free, revised). Step-on counts in
Env C: on511=2, on103=2.

## Kill bars

- K1 PASS: source audit confirms T1 (bump while transferred==1 in
  the sweep), gen/wgen state with save/restore, want==3 targeting
  and stale traversal in BFS, probe removed/confirmed semantics, and
  D1-D5 implemented as preregistered. The information barrier is
  unchanged from cb2a6fdbc (wall literals only in w_iswall; env flag
  read only by w_step and measurement-only w_true_dist).
- K2 PASS: MAPDUMP c511=1 and c103=1; on511=2 and on103=2 (>=1);
  "REVISE C wall removed 10,3" and "REVISE C wall removed 5,11"
  both present in the log.
- K3 PASS: F1 (no cell probed twice in one generation; shell audit
  of PROBE lines finds 0 duplicates), F2 (0 probes in Env B),
  F3 (c511=c103=1, not wall), F4 (rv_actions=46 <= 47, the frozen
  25 percent of the 189-action control), F5 (A=174, B=186).
- K4 PASS: 3/3 runs byte-identical (md5
  64d285b023ef2660213b66a4243d6fc0); pure Zag at every stage (znc,
  shell, grep, git only; zero Python invocations; the only
  "python" strings in the wave are "No Python" declarations);
  zero stderr; zero em/en-dash bytes in wave documentation
  (shell byte-checked).

## Answers to the pre-registered questions

- Revision: YES for removed walls. (5,11) and (10,3) were both
  probed, returned bump=0, and were marked free. The removal
  asymmetry is closed for walls the learner visits.
- Detection: YES, via T1. Both gen=1 (the (14,7) bump) and gen=2
  (the (5,10) bump) fired on first contact with no oracle signal.
- Recovery: YES. Goal reached in Env C; total 234 actions vs the
  189-action no-revision baseline, the delta attributable to the
  two T1 episodes and re-verify detours.
- Cost: re-verify consumed 46 actions, inside the frozen F4 bound
  (47). The bound held despite an unanticipated second T1 episode.

## Honest scope and deviations from the walkthrough

- The prereg walkthrough predicted a clean single-T1 re-verify. What
  actually happened is messier and more informative: re-verify
  routing through unknown cells discovered real walls ((10,4),
  (10,7)), and a normal-sweep bump ((5,10)) fired a second T1 that
  made already-handled walls ((14,7), (10,4)) stale again, costing
  two confirmatory re-probes. All of this is within the frozen
  falsifiers, and F4 still held (46/47), but the margin is thin.
  A future revision could narrow T1 to bumps that contradict
  learned (not unknown) cells; that would be a design change, not
  an implementation fix, and is not made here.
- Bounded L1/L2: the trigger and probe policy are
  researcher-authored control flow. This measures the CTSVR
  mechanism; it does not invent representations.
- Lazy resolution and no-drift handling are inherited from the
  design and remain limitations: unvisited stale walls stay stale,
  and gradual change with no contradiction fires no T1.
- The "stale unreachable" fallback (D3) was implemented but never
  triggered; it is untested code.

## Files

- wallremove.zag (implementation)
- WALLREMOVE_RAW_1.txt, WALLREMOVE_RAW_2.txt, WALLREMOVE_RAW_3.txt
  (byte-identical)
- PREREG_WALLREMOVE.md
- build.err, run1.err, run2.err, run3.err (all empty)

Builder label: BUILD-PASS.
