# XP-COUNTMAP-1 REPORT: Two-Relation Negative (2026-10-03)

## Verdict: XP-COUNTMAP-1-PASS

All 8 frozen checks PASS (A.0-A.2 phase-A gates, K1.0-K4.0).
3/3 runs byte-identical
(sha256 b9771cb64178a21e7d197515fabec61e60ce8ef3ec8092d2e7e2e648298068b6).
Zero source changes to the frozen operators. Opaque identifiers only.
Non-ledger task (claim minting paused).

## What was tested

COUNTMAP-SINGLETON reasoned from code (never executed) that the
composition layer can address exactly one count MAP per world
(Fact A), that the trial layer can nevertheless form more
(Fact B), and that pipeline order starves alternative formation
for already-covered counting while leaving formation reachable
when composition fails (Fact C). This experiment executes that
claim as a frozen negative: a world with TWO live count MAPs in
which the composition layer still behaves as if only the first
existed.

World (one workspace, 3 full queries + 2 direct compose calls):
- Phase A replicates the XP-DAGFAN-4 xd4_train shape verbatim.
  TRAIN-X: (11,81,12..14), query (11,91,14) -> 14 (trial chain
  path). TRAIN-Y: (50,82,51..53), query (50,92,3) -> 3 (trial
  count path mints MAP_Y, count MAP over rel 82). 30 distractors
  on rels 60-69.
- Phase B teaches (110,85,111), (111,85,112), (112,85,113),
  (113,85,114), then: B1 direct xs5_compose(110,117,4) -> -2;
  B2 ev_query_xs5(110,117,4) -> 4; B3 direct
  xs5_compose(110,117,4) -> -2.

Structure (node ids from run): MAP_Y = 84 (rel 82, phase A);
MAP_V2 = second count MAP (rel 85, phase B, higher id).

## Kill-bar disposal

- A.0/A.1/A.2 (phase-A gates): xs5_find_countmap -> 84 (>= 0);
  xs5_agg_rel -> 82; exhaustive INC-ok scan finds exactly 1
  count MAP pre-B. PASS. The singleton formed exactly as in
  XP-DAGFAN-4.
- K1 (TWO COUNT MAPS): after phase B the exhaustive scan (the
  frozen xs5_find_countmap predicate applied to every live
  tag-20 MAP) finds exactly 2; the higher-id one's first type-1
  provenance edge points to a rel-85 fact. PASS. The trial layer
  minted a genuine second count structure over a different
  relation, not a duplicate, and minted exactly one.
- K2 (SINGLETON LOOKUP): xs5_find_countmap still returns 84
  (MAP_Y), not MAP_V2. PASS. Lowest live id wins; the second
  count MAP is invisible to the lookup.
- K3 (SINGLE AGG REL): xs5_agg_rel still returns 82 after
  phase B. PASS. The first-learned aggregation relation is not
  displaced by the second count MAP.
- K4 (FORMATION/ADDRESSABILITY SPLIT): B1 -2, B2 4, B3 -2.
  PASS. The phase-B trace shows rebind tried=1 rejected=1,
  then "XS5-COMPOSE fail", then the answer 4, with zero
  "XS5-COMPOSE ok" and zero "XS5-TRY" anywhere in the run:
  composition was tried first and failed, the trial layer
  answered. Composition cannot address the 85-count before
  MAP_V2 exists (B1) or after (B3); the trial layer forms it
  and answers through it (B2). Demonstrated, not asserted.
- K5 (DETERMINISM): 3/3 byte-identical whole-output runs;
  sha256 b9771cb64178a21e7d197515fabec61e60ce8ef3ec8092d2e7e2e648298068b6.
  PASS.
- K6 (HYGIENE): pure Zag; safebin PATH from the first command;
  `which python` / `which python3` return nothing; zero em/en
  dash bytes in lane docs (byte-verified); opaque identifiers
  only; frozen block reused verbatim (SHA256
  56b2e678d42103d7fb9bf75e8c99289a1698844891a654e215bc025915231004
  re-verified pre/post); driver-only new code under the cm1_
  prefix; 0 new node types, 0 new edge types, 0 new opcodes,
  0 new operators, 0 modes, bridges, handlers; Zag pitfalls
  honored. PASS.

## Interpretation

Facts A-C are now frozen experimental results, not code reading.
The base trial machinery (`t2_asm_count`, `t2_try_verify`,
`promote_graph`) generalizes to N count structures without
modification; the composition layer (`xs5_find_countmap` with
no relation parameter, `xs5_agg_rel` derived from the
first-found MAP) addresses exactly one. Any future design that
needs two aggregation relations must replace the global lookup
with a parameterized one; formation and execution already
generalize. Per the singleton recommendation, the lookup itself
was NOT changed here: no current lane needs two aggregation
relations, and the DAGFAN kill bars that assume the singleton
remain valid for their worlds. XP-COUNTMAP-2 (indexed lookup
alternative) stays held until a lane genuinely needs it.

Honest bounds: single two-relation world; one second relation
(85); the 85-count was answered through the trial layer, not
through any composition path; no L2 adaptation of count
structure was attempted (Fact D stands untested, as before).

## Artifacts

- Prereg: PREREG.md (commit 668de47de, committed alone
  pre-implementation); NAMECHECK.md (Step 0 toolchain guard)
- Build: countmap1_block.zag (SHA 56b2e678..., verbatim),
  countmap1_driver.zag (cm1_ prefix), countmap1_full.zag,
  countmap1_bin, countmap1_compile.txt
- Runs: countmap1_run1/2/3.txt (byte-identical,
  sha256 b9771cb6...)
- Toolchain: safebin PATH, pinned
  src/tools/toolchain/znc_linux_x86_64_abed8aa1, pure Zag

## Notes for the parent

- No ledger entry: non-ledger task, nothing minted.
- lane-xdagfan2-20261003 not modified, not merged; read-only
  git show only.
- Commits local on tnn-native-lab only, explicit pathspecs,
  never pushed.
- The A1 amendment's "cannot form" phrasing (XP-DAGFAN-4) is
  superseded by this result: a second count MAP CAN form via
  the trial path whenever a count verifies against expected;
  it cannot be ADDRESSED via the composition layer. The
  formation/addressability split is now the banked statement.
