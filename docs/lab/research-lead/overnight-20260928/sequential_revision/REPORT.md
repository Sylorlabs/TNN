# REPORT: Sequential Rule Revision

Date: 2026-10-02. Worker: Sequential Revision Worker.
Verdict: **SEQUENTIAL-REVISION-COMPLETE**.

## What was tested

Whether a learner that has already revised a rule once can revise AGAIN
when the world changes further, and whether the second revision
preserves the first revision's knowledge. This is the open question left
by RULE-REVISION-COMPLETE (single revision ALWAYS(NODE) ->
IF(in<33,NODE,NUM)).

Design (pure Zag, standalone program, frozen in PREREG.md commit
8d54c2d7e before any implementation existed):

- The learner holds its rule as a threshold TREE in its own state
  (node pool; leaf or split nodes), not as a flat form. Prediction is
  always through the tree predicate rule_pred; no lookup list exists.
- Phase 1 (W1, kind law: NODE iff x<34 else NUM): TEACH induces
  ALWAYS(NODE); a verification failure on input 33 drives revision 1
  to IF(in<33,NODE,NUM) via the generic blame walk, a generic
  boundary-localization operator (downward active inquiry from the
  counterexample input, every probe outcome joining the observation
  log), and a generic re-split operator (smallest mispredicted input
  in the log; only the responsible leaf is converted to a split).
- The world then changes (W2: a new STR kind band for x>=67;
  D_true(v)=v+1 never changes). The learner is not told. A new
  verification failure on input 70 (its rule predicts NUM, the world
  now says STR) drives revision 2 through the SAME three generic
  operators, yielding IF(in<33,NODE,IF(in<66,NUM,STR)).

## Kill-bar results

- K-SR-1 (first revision works): PASS. REVISE-1 produced exactly
  IF(in<33,NODE,NUM) with TREE-DUMP nodes=3
  [0:split T=33 L=1 R=2][1:leaf NODE][2:leaf NUM] and RULE-FIT 4/4.
  RETEST-1, REGRESS-1, and GENERALIZE-1 (unprobed inputs 40, 60) all
  MATCH.
- K-SR-2 (second revision works after the world change): PASS. The
  change was detected purely experientially (Z3 gate=0 REJECT on
  input 70, want NUM, final-kind STR). REVISE-2 produced exactly
  IF(in<33,NODE,IF(in<66,NUM,STR)) with RULE-FIT 10/10. RETEST-2
  (66, 70 -> STR) and GENERALIZE-2 (50 -> NUM, 80 -> STR, both
  unprobed) all MATCH.
- K-SR-3 (first revision's knowledge preserved or properly
  superseded; no forgetting): PASS. White-box: TREE-DUMP node
  descriptors [0:split T=33 L=1 R=2] and [1:leaf NODE] appear verbatim
  in both dumps, and PRESERVE-CHECK (driver comparison of node 0/1
  cells snapshotted after REVISE-1 vs after REVISE-2) reads
  root-split-intact=yes left-leaf-intact=yes. Behavioral: REGRESS-2
  shows all revision-1-era cases still MATCH (31, 32 -> NODE;
  33, 40 -> NUM). Proper supersession: node 2 converted from leaf NUM
  to split T=66 with left leaf NUM (old knowledge for [33,66)
  retained in node 3) and right leaf STR (node 4).
- K-SR-4 (learner-driven revision; no researcher constants): PASS.
  learner_refute, boundary_search, and learner_refine contain none of
  the literals 31,32,33,34,40,50,60,66,67,70,80 (sed-scoped grep 0,0,0).
  Node-cell writes (nset) total 11 = 1 definition + 2 inside
  rule_induce + 8 inside learner_refine; zero in the driver. The
  driver calls learner_refute(L,E), boundary_search(L,E),
  learner_refine(L): no values passed. grep -ci 'expected' = 0 over
  both sources. Zero probe lines (OBS, REFUTE link, SEARCH trail)
  mention 40, 60, 50, or 80. The learner never writes world state
  (0 set32(E) inside the three operators; the only E writes are the
  world_init init and the world_downstream gate latch).
- K-SR-5 (determinism): PASS. 3/3 runs byte-identical
  (sha256 025f3b6a78a8cca7652d4016ed57c47081a4a86a62d270dc30cc2ce872022921,
  cmp pairwise identical).

Frozen predictions: 12/12 matched (P1..P12).

## The key mechanism result

The second revision did not rebuild the rule from the observation log.
It re-split exactly one node (node 2, the leaf responsible for the
smallest mispredicted input 66) and left nodes 0 and 1 untouched. The
boundary value 66 was discovered by the learner's own downward search
(5 probes: 69,68,67,66 STR then 65 NUM), never supplied. Structural
locality of revision is what preserves earlier knowledge: only the
wrongly-predicting leaf is rewritten.

## Build notes

- First build's transcript rendered nested leaves as ALWAYS(kind),
  e.g. IF(in<33,ALWAYS(NODE),ALWAYS(NUM)), which mismatched the frozen
  notation. Fixed as a display-only change: the recursive renderer now
  prints bare kinds for nested leaves (root leaf still ALWAYS(kind)),
  matching the prereg exactly. No logic change; no prediction text
  besides rendering was altered.
- The `as *i32` grep hit was a code comment only; reworded. Zero
  occurrences in code.
- Gate E writes: 2 sites, world_init (init to 0) and world_downstream
  (the consequence latch). The prereg's K-SR-4 bars the learner from
  writing world state, which holds (0 writes in learner operators).

## Artifacts

- sr_mech.zag (sha256 5efaed047bd7a1a0a9f42372e63c140ba66ea4bd1d4fd39a45de4d8b70b397aa)
- sr_main.zag (sha256 46d6c2aa1aae4399cf66edfa42856c29c7c8dd51f2a02b3318942505d6586e32)
- sr_full.zag (assembled; sha256 065dd7ed83ddd5d70f88cc9d9a4229a1d2fd2a9120fdeb1f195ea7bfd286e57f)
- sr_bin (sha256 22229d61bfc343545346e6a23954f9ad6bc30203b8d1f4caae949447a56deeb0)
- compile.txt, run1.txt, run2.txt, run3.txt, sha256sums.txt, build.sh
- 40 transcript lines, 15 MATCH lines, 0 MISMATCH lines.

## Architecture accounting

Pure Zag, safebin PATH, no Python at any point (guard re-verified in
build.sh). Zero modes, zero bridges, zero handlers, zero new opcodes
(grep 0/0). Single preallocated output buffer with one raw syscall
write; u8-backed little-endian state cells; recursion verified working
before use. The observation log, node pool, blame walk, boundary
search, and re-split operator are learner-state machinery, not modes:
no task-label dispatch anywhere.

## Boundaries (from prereg, unchanged)

Rule class (binary threshold tree over input order) is
researcher-supplied machinery; content is learner-discovered: not L3.
boundary_search assumes the new regime is at/above the counterexample
input with the old regime directly below (floor 0, cap 64). Single
component D; blame walk stops at link 0 in both traces. The world
change is researcher-imposed but never announced to the learner.
Goal/evaluation inputs are lab task setup. Toy scale; mechanism
demonstration, not a generality or SURVIVES claim.

## Commits (explicit pathspecs, local only, never pushed)

- 8d54c2d7e: PREREG.md alone (frozen before implementation).
- Implementation commit: NAMECHECK.md, REPORT.md, sr_mech.zag,
  sr_main.zag, sr_full.zag, build.sh, sr_bin, compile.txt,
  run1/2/3.txt, sha256sums.txt.
