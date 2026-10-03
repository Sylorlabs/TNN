# NAMECHECK: SUM-DETECTOR-FIX

Worker: SUM-DETECTOR-FIX. Non-ledger task (claim minting paused).
Branch: tnn-native-lab, local only, never pushed. Lane:
docs/lab/research-lead/overnight-20260928/sum_detector_fix/
(files sdf_*).

## Step 0: toolchain guard (recorded before any build)

- Ran the lane setup under safebin: `export PATH="$HOME/safebin"`.
- `which python3` returns nothing; `which python` returns nothing.
- `which znc` resolves to /home/hatch/safebin/znc (the pinned
  toolchain). Safebin holds 36 allowed tools; no interpreter.
- All research logic (block patch, drivers, verification) is pure
  Zag compiled with the pinned znc. Shell is used only to invoke
  znc, run binaries, and do byte comparisons (cmp, sha256sum).
- If any forbidden executable is invoked, the wave is PROCESS-FAIL.

## Frozen sources (read-only, never modified)

- xp_countmap1/countmap1_block.zag: 2648 lines, SHA256
  56b2e678d42103d7fb9bf75e8c99289a1698844891a654e215bc025915231004
  (re-verified by sha256sum before freezing; matches the
  XP-DAGFAN-4 prereg record and the COUNTMAP-ADDRESSABILITY /
  SUM-ADDRESSABILITY citations).
- xhier_countmap_fix/xf_block.zag: the same block plus the frozen
  XHIER-COUNTMAP-FIX patch (xhier_mapz_rel + xhier_exec loud
  fences); diff against countmap1_block.zag re-verified at 33
  lines, touching only the xhier_exec region.
- xhier_countmap_fix/xf_block_control.zag: byte-identical copy of
  countmap1_block.zag (control for the xf battery).
- xp_countmap1/countmap1_driver.zag (XP-COUNTMAP-1 driver),
  xhier_countmap_fix/xf_driver.zag (xf battery driver),
  lane-xdagfan2-20261003:docs/lab/research-lead/overnight-20260928/xdagfan2/xdagfan4_driver.zag
  (XP-DAGFAN-4 driver, read via read-only git show, branch not
  modified).

## Key frozen semantics (line refs to countmap1_block.zag)

- xs5_has_inc (:2121): single-path walk (GUARD via field 12, else
  SEQ edge, 64-step bound); returns 1 on ANY tag-103 INC cell.
  Kept byte-identical as the raw cell predicate; NO lookup path
  uses it after the patch.
- xs5_find_countmap (:2134): lowest live id wins. Patched to use
  the count detector. COUNTMAP-2 stays on hold: still a
  singleton, still query-blind.
- xhier_agg_ok (:2494): patched to use the count detector.
- t2_asm_count (:379): guard/set/inc per link + MOVE epilogue;
  every count graph contains 102 and 103 cells on the detector
  walk path.
- t2_asm_sum (:398): pure INC chain, length = total (1..900); no
  guards. Every sum graph fails the count detector and passes
  the sum detector.
- t2_asm_chain (:363): guard/set cells only, no INC; fails both
  old and new count predicates.
- t2_trial (:586): phase order chains, then sums (gated on
  comb_present, a live tag-8 node), then counts. A sum MAP that
  forms before a count MAP gets the lower id and shadows it
  under the old predicate.
- promote_graph (:533) with root -1 (MAP_Z): old and new
  detectors both return 0 (walk never starts).
- Tag-8 node construction (t_p2, :1080): alloc_node, ns tag 8.
  Reused verbatim as the sum-gate opener in the D1 world.

## Zag pitfalls honored

- No `as *i32` + slice construction; no `_zag_print` for dynamic
  content (emit/e64 only, driver-side as in frozen lanes).
- New detector fns keep if-nesting at 2 or fewer; call results
  (ng, seq_nx) read into locals before conditions; no
  `!(A && B)` in any while condition (checked by grep).
- New block names use the block's xs5_ prefix convention; new
  driver names use the sdf_ prefix; no frozen name is redefined.

## Scope discipline

- SUM-1 item 1 ONLY: the type-honest detector fix. SUM-1 items
  2-7 stay on hold. The singleton lookup is NOT changed
  (COUNTMAP-2 stays on hold). No new node types, edge types,
  opcodes, modes, bridges, handlers, or semantic cases.
- Zero em/en dashes in lane docs (byte-verified before commit).
- Opaque identifiers only (relation numbers, node ids).
- Commits local only, never pushed, explicit pathspecs, no
  reset.
