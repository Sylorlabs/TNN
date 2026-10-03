# REPORT: SUM-DETECTOR-FIX (type-honest count/sum detectors)

Date: 2026-10-03. Worker: SUM-DETECTOR-FIX. Non-ledger task
(claim minting paused). Branch: tnn-native-lab, local only,
never pushed. Lane:
docs/lab/research-lead/overnight-20260928/sum_detector_fix/
(files sdf_*). Verdict: **SUM-DETECTOR-FIX-PASS** (K1-K7 all
pass).

## What was built

SUM-1 item 1 from the SUM-ADDRESSABILITY report, implemented
as standalone correctness hardening: the has-INC predicate is
replaced at every lookup/census use by two structural
detectors derived from the graph itself.

- `xs5_graph_is_count`: the detector walk meets at least one
  GUARD (102) cell AND at least one INC (103) cell.
- `xs5_graph_is_sum`: at least one cell and every walked cell
  is INC (103).
- Both use the exact single-path walk discipline of the old
  `xs5_has_inc` (GUARD via field 12, else SEQ edge, 64-step
  bound), so the change is a stricter classification on the
  same walk, not a new traversal.
- Call sites swapped: `xs5_find_countmap`,
  `xhier_agg_ok`, and the driver censuses
  (`cm1_scan_countmaps`, `xf_scan_countmaps`,
  `xf_max_countmap`).
- `xs5_has_inc` kept byte-identical as the raw cell
  predicate; no lookup path references it after the patch
  (verified by grep). `xs5_agg_rel` byte-identical; the
  singleton stays lowest-id-wins and query-blind
  (COUNTMAP-2 on hold). SUM-1 items 2-7 not implemented
  (on hold).

Two patched blocks (frozen originals never modified):
- `sdf_base_block.zag` = countmap1_block.zag
  (SHA 56b2e678d42103d7fb9bf75e8c99289a1698844891a654e215bc025915231004,
  re-verified pre/post) + detector patch. Diff against frozen:
  ONLY the two added detector fns, two doc-comment lines on
  `xs5_has_inc`, and the two call-site swaps.
- `sdf_xf_block.zag` = xf_block.zag (the frozen
  XHIER-COUNTMAP-FIX block) + the identical detector patch.

## Battery D1: the shadow is gone (discrimination)

World: tag-8 gate opened (t_p2 shape), sum MAP formed first
by the real trial sum phase (query (110,41,60) -> 60; sum MAP
id 67, sixty INC cells), then a count MAP formed by the trial
count phase (query (50,92,3) -> 3; count MAP id 163). The sum
phase declines the count query (only subset total 51, not 3);
`xs5_compose` cannot interfere (no nav MAP exists, both legs
fail on both binaries). World construction is byte-identical
on both binaries through D1-IDS (ids 67/163): the patch
changes no allocation.

| probe | fixed (patched) | control (frozen verbatim) | frozen prediction |
|---|---|---|---|
| PC0 world built | PASS | PASS | sq 60, cq 3, sum 67 < count 163 |
| PC1 driver walks classify | PASS (0,1,1,0) | PASS (0,1,1,0) | sum: not-count/is-sum; count: is-count/not-sum |
| K1 D1-FIND | 163 (the count MAP) | 67 (the sum MAP) | fixed count_id, control sum_id |
| K2 D1-AGGOK | sum 0, count 1 | sum 1, count 1 | fixed 0/1, control 1/1 |
| K3 D1-AGGREL | 82 | 31 | fixed 82, control != 82 (predicted 31) |

K1 PASS: the control binary demonstrates the exact shadowing
SUM-ADDRESSABILITY reasoned about (lowest-id-wins returns the
sum MAP); the fixed binary skips it and returns the genuine
count MAP. K2 PASS: the sum MAP no longer passes the
aggregation capability gate. K3 PASS: `xs5_agg_rel` reads 82
(the count MAP's relation) on fixed, versus 31 (the sum MAP's
first licensing fact relation) on control. The control legs
behaved exactly as reasoned, so the discrimination claim is
not void.

## Batteries R1/R2/R3: frozen verdicts preserved verbatim

- K4 (R1, XP-COUNTMAP-1): 3/3 runs of the patched-base +
  patched-census battery byte-identical (cmp) to the frozen
  countmap1_run1.txt. 8/8 PASS preserved verbatim, including
  K2.0 (lookup returns MAP_Y) and K3.0 (agg rel still 82).
- K5 (R2, XP-DAGFAN-4): 3/3 runs of the patched-base +
  verbatim xdagfan4 driver byte-identical to the frozen
  xdagfan4_run1.txt. 22/22 PASS preserved verbatim.
- K6 (R3, XHIER-COUNTMAP-FIX): 3/3 runs of the patched xf
  block + patched xf driver byte-identical to the frozen
  xf_run1.txt. K1-EXEC 4, K3A-EXEC -2 (XHIER-EXEC-NOREL),
  K3B-EXEC -2 (XHIER-EXEC-NOAGG), 15/15 preserved verbatim.

The byte identity is the empirical proof of the prereg's
reasoned claim: in sum-free worlds every graph the old
predicate matched still matches the count detector (count
graphs carry guard+INC on the walk; chain graphs and MAP_Zs
match neither before nor after), and the detectors allocate
nothing.

## Kill-bar disposition

- K1 D1 discrimination: PASS (fixed 163, control 67).
- K2 agg gate type-honesty: PASS (fixed 0/1, control 1/1).
- K3 provenance relation: PASS (fixed 82, control 31).
- K4 XP-COUNTMAP-1 verbatim: PASS (3/3 byte-identical).
- K5 XP-DAGFAN-4 verbatim: PASS (3/3 byte-identical).
- K6 XHIER-COUNTMAP-FIX verbatim: PASS (3/3 byte-identical).
- K7 hygiene: PASS. Pure Zag; safebin PATH from the first
  command (Step 0 in NAMECHECK.md; `which python3`/`which
  python` resolve nothing); zero em/en dash bytes in lane
  docs (byte-verified); opaque identifiers only; frozen
  blocks reused verbatim for controls (SHA re-verified
  pre/post); patched-block diffs show only the intended
  changes; `xs5_has_inc` body byte-identical and unreferenced
  by any lookup path; `xs5_agg_rel` byte-identical;
  `xs5_find_countmap` still lowest-id-wins; driver-only new
  code under sdf_ plus the census predicate swaps; 0 new node
  types, edge types, opcodes, modes, bridges, handlers,
  semantic cases; no `!(A && B)` in any while condition
  (grep); Zag pitfalls honored.

Verdict: SUM-DETECTOR-FIX-PASS. VOID was not triggered.

## Run record

- sdf_r1_bin: 3 runs, sha256 of run1
  b9771cb64178a21e7d197515fabec61e60ce8ef3ec8092d2e7e2e648298068b6
- sdf_r2_bin: 3 runs, sha256 of run1
  90f26b33e999ca237b92802fbd386e633c9fa66d5cdc9d91438123e6c0f69cbd
- sdf_r3_bin: 3 runs, sha256 of run1
  9cfc0bd3da2d86992eb0ca6da81bbebba576275bb11731163cdb4b91bafb9f02
- sdf_d1_fixed_bin: 1 run, sha256 of run1
  8b31c29f3b15f5a6da87bd835e52fe3bf351264b0ab3c9b6868803456c4
- sdf_d1_control_bin: 1 run, sha256
  3d96a29ba95d9a4140d4194fad139374917dbd81aadd9589bf6b6868803456c4
- All five binaries compiled with the pinned znc under
  safebin, exit 0, analyzer warnings only (the same 171
  A0102-class warnings the frozen lanes carry).

## What this does NOT claim

- Not COUNTMAP-2: the lookup is still a lowest-id-wins
  singleton, still query-blind. It is now type-honest: it can
  only ever name a count graph.
- Not SUM-1 items 2-7: no sum lookup, no sum executor, no
  composition legs, no formation changes. Sums remain
  unaddressable; they are no longer misaddressable.
- The D1 world is surgical scaffolding for the detector
  branches, not a claimed natural composition event. The sum
  MAP was formed by the real trial sum phase (not hand-built
  cells), which is what makes the shadowing test honest.
- The 64-step walk bound is documented on the sum detector;
  it cannot confuse the two frozen assembler shapes.

## Notes for the parent

- No ledger entry: non-ledger task, nothing minted.
- The detector fix is now proven as standalone hardening on
  both the base block and the xf block. The next lane that
  touches the xs5/xhier patches can carry
  `xs5_graph_is_count` / `xs5_graph_is_sum` forward; the
  regression batteries here (R1/R2/R3 drivers and frozen run
  records) are reusable verbatim for that.
- A duplicate `operand_namespace_fix/` lane was noted in the
  standing context as needing deduplication; unrelated to
  this lane, flagged only because lane hygiene was in scope.
- Style: no em/en dashes in this file (hyphens only),
  opaque identifiers throughout.
