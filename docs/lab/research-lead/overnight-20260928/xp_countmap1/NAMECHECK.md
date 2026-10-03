# NAMECHECK: XP-COUNTMAP-1

Worker: XP-COUNTMAP-1. Lane: xp_countmap1/ (files countmap1_*).
Branch: tnn-native-lab, local only, never pushed.
Task: two-relation frozen negative. Trial mints a second count
MAP over rel 85; the composition layer still ignores it. Banks
COUNTMAP-SINGLETON Facts A-C as a kill-barred result. Non-ledger
task (claim minting paused).

## Step 0: toolchain guard (mandatory startup, recorded before any work)

- Exported PATH="$HOME/safebin" as the first command of the session.
- Verified: `which python3` returns NOTHING.
- Verified: `which python` returns NOTHING.
- Pinned compiler for all builds:
  ~/workspace/tnn-rsi-gpi3/src/tools/toolchain/znc_linux_x86_64_abed8aa1
  (absolute path; verified present).
- Pure Zag for all scientific computation. Shell only for:
  znc invocation, binary execution, git ops, file movement,
  sha256sum/cmp/grep checks.
- If a forbidden executable is invoked at any point, this
  wave is automatically PROCESS-FAIL. None invoked so far.

## Survey (pre-prereg, read-only)

- Read countmap_singleton/REPORT.md in full: Facts A-D, the
  formation/addressability split, the Section 7 prereg sketches
  for COUNTMAP-1 (two-relation negative, banks Facts A-C) and
  COUNTMAP-2 (indexed lookup, held until a lane needs it).
- Read the XP-DAGFAN-4 artifacts on lane-xdagfan2-20261003 via
  read-only git show (branch not modified, not merged):
  xdagfan4_REPORT.md (PASS 22/22, 3/3 byte-identical), xdagfan4_PREREG.md
  (xd4_train shape, K1-K10), xdagfan4_driver.zag (xd4_ helpers,
  emit/e64 output patterns), xdagfan4_NAMECHECK.md (Step 0, Zag
  pitfalls).
- Read the frozen block source (xdagfan4_block.zag, 2648 lines):
  xs5_find_countmap (:2134), xs5_agg_rel (:2147), xs5_agg_exec
  (:2177), xs5_try_nav_agg (:2190), xs5_compose (:2208),
  t2_trial count path (:635-647), promote_graph (:533),
  cc_relseq (:1702), t2_try_verify (:497), ev_query_xs5 (:2423),
  mp_run (:668).
- Re-verified the frozen build block SHA256
  56b2e678d42103d7fb9bf75e8c99289a1698844891a654e215bc025915231004
  (matches the XP-DAGFAN-4 prereg record).
- Confirmed no identifier collisions: query rel 117 and nav/count
  rel 85 and node ranges 110-114 are unused by XDAGFAN-1
  (91,92,93,94,95,96,97,98), XP-DAGFAN-2/3, and XP-DAGFAN-4
  (110-113, 114, 115, 116, 120-121, 213-216, 221-224 are taken
  there, but those worlds are not loaded here; this lane runs a
  fresh workspace, so only the phase-A replication ranges
  11-14, 50-53, 5000-5029 matter, and 110-114 is fresh).
- Did not modify lane-xdagfan2-20261003, xdagfan/, xdagfan2/,
  xdagfan3/, or CLAIM_LEDGER.md.

## Design decisions (frozen in countmap1_PREREG.md)

- One workspace, 3 full queries plus 2 direct xs5_compose calls
  (within the demonstrated safe range).
- Phase A replicates the XP-DAGFAN-4 xd4_train shape verbatim:
  TRAIN-X (11,81,12..14; query (11,91,14)->14), TRAIN-Y
  (50,82,51..53; query (50,92,3)->3, forms MAP_Y), 30
  distractors on rels 60-69.
- Phase B teaches a 4-link 85-chain at fresh subject 110, then:
  B1 direct xs5_compose(110,117,4) -> -2 (pre-formation);
  B2 ev_query_xs5(110,117,4) -> 4 (trial mints MAP_V2);
  B3 direct xs5_compose(110,117,4) -> -2 (post-formation,
  still ignored).
- K1-K4 structural/answer assertions; K5 determinism 3/3
  byte-identical; K6 hygiene (pure Zag, safebin, no em/en
  dashes, opaque identifiers, frozen block verbatim).
- Zag pitfalls honored: no as-*i32 slice construction in
  functions; emit/e64 only for output (block-proven patterns);
  no []f64/[]i64 len reliance; shallow if/while nesting via
  hoisted helpers; never !(A && B) in while conditions;
  no []u8 as *u8 cast.
