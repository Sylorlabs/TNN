# NAMECHECK: XHIER-COUNTMAP-FIX

Worker: XHIER-COUNTMAP-FIX. Lane: xhier_countmap_fix/ (files xf_*).
Branch: tnn-native-lab, local only, never pushed.
Task: fix/fence the COUNTMAP-ADDRESSABILITY Section 5(a) latent
issue: `xhier_exec` resolves each MAP_Z's own type-14 count MAP
address, uses it only as an existence gate, then executes the
global singleton anyway. Non-ledger task (claim minting paused).

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

- Read countmap_addressability/REPORT.md in full: the
  formation/addressability split, the Section 5(a) latent issue
  (`xhier_exec` discards the MAP_Z's own count MAP address;
  recommendation to fix or fence when MAP_Z work next runs,
  independent of COUNTMAP-2), and the constraint that the
  singleton lookup is NOT changed.
- Read the frozen block source (xp_countmap1/countmap1_block.zag,
  2648 lines, SHA256
  56b2e678d42103d7fb9bf75e8c99289a1698844891a654e215bc025915231004):
  xhier_exec (:2546), xhier_mapz_agg (:2532), xhier_mapz_nav
  (:2519), xs5_find_countmap (:2134), xs5_agg_rel (:2147),
  xs5_agg_exec (:2177), xs5_try_nav_agg (:2190), xs5_compose
  (:2208), xs5_select (:2391), promote_graph (:533),
  t2_try_verify (:497), t2_revise_graph tombstone pattern
  (:731: ns(W,stale,0,0); ns(W,stale,36,0)).
- Read xp_countmap1/PREREG.md, NAMECHECK.md, driver, and REPORT.md
  for the proven phase shapes (phase A forms MAP_Y over rel 82;
  phase B forms MAP_V2 over rel 85 via trial) and the lane
  conventions (prereg-before-implementation, 3/3 byte-identical,
  explicit pathspecs, no em/en dashes, opaque identifiers).
- Confirmed the latent issue in source: xhier_exec computes
  `a=xhier_mapz_agg(W,z)`, gates `if(a<0){return -2;}`, then
  calls `xs5_agg_exec(W,e,xs5_agg_rel(W))` with the world-global
  singleton relation. The resolved address `a` never reaches
  execution.
- Confirmed callers: xs5_find_countmap is called from
  xs5_agg_rel, xs5_agg_exec (gate), xs5_try_nav_agg (compose-time
  link), and xhier_exec (:2553, the site being fixed).
  xs5_agg_rel is called from xs5_compose, xs5_select, and
  xhier_exec (:2553, the site being fixed). No other xhier_exec
  callers besides xhier_try_pair (only reachable via
  ev_query_xhier, which this driver never calls).

## Design decisions (frozen in xf_PREREG.md)

- FIX on the happy path, FENCE (loud -2) on unusable-address
  paths. Rationale: the composite's own type-14 count MAP is the
  address formation recorded; its provenance relation is
  learner-state data already present. Using it preserves the
  verified compose-time semantics. A fence (refuse on divergence)
  would reject composites whose provenance is informative and
  correct, which is strictly less capable. The old behavior is
  silent-wrong; the fix makes it right; the fence makes the
  genuinely broken cases loud.
- New helper `xhier_mapz_rel(W,m)`: the xs5_agg_rel read shape
  parameterized by MAP id instead of the global singleton.
- Patched `xhier_exec`: relation comes from `xhier_mapz_rel(W,a)`;
  emits XHIER-EXEC-NOAGG on a<0 and XHIER-EXEC-NOREL on r<0,
  both returning -2 (the codebase's failure protocol, made loud).
- Untouched: xs5_find_countmap and xs5_agg_rel stay
  byte-identical in the patched block (verified by diff); all
  their other call sites unchanged. COUNTMAP-2 stays on hold:
  this adds no parameterized world-global lookup, only a
  per-composite provenance read.
- Two binaries from one driver: xf_fixed (patched block) and
  xf_control (frozen block verbatim, SHA re-verified). The
  control binary proves K1 discriminates (old code silently
  returns the wrong-relation count on the same world).
- Divergence construction: tombstone MAP_Y (canonical ns 0/36
  pattern) so MAP_V2 becomes the singleton at compose time;
  compose MAP_Z2 via the normal xs5_compose path (links MAP_V2
  honestly); restore MAP_Y so the singleton flips back to rel 82
  while MAP_Z2's own count MAP still names rel 85.
- Zag pitfalls honored: no as-*i32 slice construction in
  functions; emit/e64 only for output (block-proven patterns);
  no []f64/[]i64 len reliance; shallow if/while nesting; never
  !(A && B) in while conditions; no []u8 as *u8 cast.
