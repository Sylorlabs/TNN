# PREREG: SUM-DETECTOR-FIX (type-honest count/sum detectors)

Frozen 2026-10-03, before any implementation. Worker:
SUM-DETECTOR-FIX. Branch: tnn-native-lab, local only, never
pushed. Lane:
docs/lab/research-lead/overnight-20260928/sum_detector_fix/
(files sdf_*). Non-ledger task (claim minting paused).

## Objective

SUM-ADDRESSABILITY Section 3 (reasoned from frozen source):
sums are *misaddressable*, not just unaddressable.
`xs5_has_inc` returns 1 on ANY tag-103 cell, and a sum graph is
a pure INC chain, so a live sum MAP passes `xs5_find_countmap`,
`xhier_agg_ok`, the `xs5_agg_exec` capability gate, gets
LINK14-attached as a composite's count MAP, is overcounted by
the driver census, and feeds `xs5_agg_rel` a relation read off
its licensing facts. Once the sum gate opens (tag-8 node
live), a sum MAP can shadow a genuine count MAP by
lowest-id-wins. This persists after XHIER-COUNTMAP-FIX. Latent
correctness issue, independent of COUNTMAP-2.

This experiment implements SUM-1 item 1 ONLY (the type-honest
detector fix) as standalone correctness hardening, and proves:
(a) sum MAPs no longer shadow count MAPs in the singleton
lookup (discrimination battery D1, fixed vs control binary);
(b) every frozen verdict is preserved verbatim with the new
detectors in place (regression batteries R1/R2/R3, byte-
identical stdout against the frozen run records).

## The patch (applied to lane copies; frozen originals never modified)

Two structural detectors, same single-path walk discipline as
`xs5_has_inc` (GUARD via field 12, else SEQ edge, 64-step
bound). Placed immediately after `xs5_has_inc`:

```zag
// 1 if the graph rooted at root is a count graph: the detector
// walk meets at least one GUARD (102) cell AND at least one INC
// (103) cell. Same single-path walk discipline as xs5_has_inc.
fn xs5_graph_is_count(W:[]u8,root:i32)i32 {
  let cur:i32=root; let steps:i32=0;
  let g:i32=0; let ic:i32=0;
  while(cur>=0 && steps<64){
    let tag:i32=ng(W,cur,0);
    if(tag==102){g=1;}
    if(tag==103){ic=1;}
    if(tag==102){cur=ng(W,cur,12);}
    else {cur=seq_nx(W,cur);}
    steps=steps+1;
  }
  if(g==1 && ic==1){return 1;}
  return 0;
}

// 1 if the graph rooted at root is a sum graph: at least one
// cell and every walked cell is INC (103). Sum graphs are pure
// SEQ chains of INC cells, so the walk covers them in order.
// (The 64-step bound truncates only very long sums; any count
// graph shows its guard at the root, so the bound cannot
// confuse the two assembler shapes.)
fn xs5_graph_is_sum(W:[]u8,root:i32)i32 {
  let cur:i32=root; let steps:i32=0; let n:i32=0;
  while(cur>=0 && steps<64){
    let tag:i32=ng(W,cur,0);
    if(tag!=103){return 0;}
    n=n+1;
    cur=seq_nx(W,cur);
    steps=steps+1;
  }
  if(n>=1){return 1;}
  return 0;
}
```

Two call-site swaps, the only other block changes:

- `xs5_find_countmap`: `xs5_has_inc(W,ng(W,m,20))==1` becomes
  `xs5_graph_is_count(W,ng(W,m,20))==1`. The singleton stays a
  singleton (COUNTMAP-2 on hold); it becomes type-honest.
- `xhier_agg_ok`: `xs5_has_inc(W,ng(W,t,20))!=1` becomes
  `xs5_graph_is_count(W,ng(W,t,20))!=1`.

`xs5_has_inc` itself is kept byte-identical as the raw
"contains an INC cell" predicate; after the patch NO lookup
path references it (verified by grep in K7). `xs5_agg_rel` is
unchanged (it reads whatever the singleton names; the fix
makes the singleton name only count MAPs).

Driver census swaps (driver copies only):
- `cm1_scan_countmaps` (R1 driver): `xs5_has_inc` becomes
  `xs5_graph_is_count`.
- `xf_scan_countmaps` and `xf_max_countmap` (R3 driver): same
  swap.

## Why the regression bars should hold (reasoned, tested by R1/R2/R3)

In every frozen regression world the sum gate never opens (no
tag-8 node is taught in any of the three drivers; verified by
grep), so no sum MAP is live. On every graph the old predicate
matched in those worlds, the count detector also matches:
count graphs always carry a guard at the root and INC cells on
the walk (t2_asm_count); chain graphs carry no INC cells (old
0, new 0); MAP_Zs carry root -1 (old 0, new 0). The detectors
allocate nothing, so node ids and every emitted value are
unchanged. Predicted: byte-identical stdout.

## Battery D1: the shadowing world (discrimination)

One shared driver (sdf_driver_d1.zag, sdf_ prefix, frozen names
only besides its own helpers) runs on two binaries: the
patched base block (fixed) and the frozen base block verbatim
(control).

World construction, all frozen ops:
1. Sum gate: `alloc_node`, `ns(W,cn,0,8)`,
   `write_node(W,cn,1,0,0,0)` (the t_p2 shape, verbatim).
2. Teach (110,31,10), (110,32,20), (110,33,30);
   `ev_query_xs5(W,110,41,60,0)`: chain phase finds no
   multi-hop path; sum phase tries the full subset first
   (total 60 == expected) and promotes the sum MAP (60 INC
   cells). Stash sum_id = live tag-20 MAP with field8==110
   (exactly one).
3. Teach (50,82,51), (51,82,52), (52,82,53);
   `ev_query_xs5(W,50,92,3,0)`: chain phase finds no path;
   sum phase gathers only (50,82,51) (subject filter), total
   51 != 3, declined; count phase verifies 3==3 and promotes
   the count MAP. Stash count_id = live tag-20 MAP with
   field8==50 (exactly one). Allocation order gives
   sum_id < count_id (asserted as a precondition).
   `xs5_compose` cannot interfere: no nav MAP exists, so both
   legs fail on both binaries (the (AGG,NAV) leg's
   `xs5_agg_exec` finds no 31-chain at 50 on control and
   r_agg=-1 on fixed).

Probes (binary-independent preconditions, PASS/FAIL in-driver):
- PC0: sq==60, cq==3, sum_id>=0, count_id>=0,
  sum_id != count_id, sum_id < count_id.
- PC1 (driver-side walk reimplementation, sdf_ prefix, calls
  only frozen ops): is_count(sum_root)==0,
  is_sum(sum_root)==1, is_count(count_root)==1,
  is_sum(count_root)==0. Independent cross-check of the
  detector logic on both binaries.

Probes (binary-dependent, raw values emitted, verified in
shell per binary):
- D1-FIND: `xs5_find_countmap(W)`.
- D1-AGGOK: `xhier_agg_ok(W,sum_id)`, `xhier_agg_ok(W,count_id)`.
- D1-AGGREL: `xs5_agg_rel(W)`.

## Batteries R1/R2/R3: frozen-verdict preservation

- R1: sdf_base_block.zag (frozen base + detector patch) with
  the R1 driver (cm1 driver, census predicate swapped).
  Predicted stdout byte-identical to the frozen
  xp_countmap1/countmap1_run1.txt (XP-COUNTMAP-1 PASS 8/8).
- R2: sdf_base_block.zag with xdagfan4_driver.zag extracted
  verbatim from lane-xdagfan2-20261003. Predicted stdout
  byte-identical to the frozen xdagfan4_run1.txt
  (XP-DAGFAN-4 PASS 22/22, 3/3 byte-identical).
- R3: sdf_xf_block.zag (frozen xf block + detector patch) with
  the R3 driver (xf driver, census predicates swapped).
  Predicted stdout byte-identical to the frozen
  xhier_countmap_fix/xf_run1.txt (XHIER-COUNTMAP-FIX-PASS:
  K1-EXEC 4, K2 happy path, K3a/K3b loud fences).

Builds (cat block + driver; pinned znc):
- sdf_r1: sdf_base_block.zag + sdf_driver_r1.zag
- sdf_r2: sdf_base_block.zag + xdagfan4_driver.zag
- sdf_r3: sdf_xf_block.zag + sdf_driver_r3.zag
- sdf_d1_fixed: sdf_base_block.zag + sdf_driver_d1.zag
- sdf_d1_control: countmap1_block.zag verbatim + sdf_driver_d1.zag

## Frozen predictions

- PC0: sq==60; cq==3; exactly one live tag-20 MAP with
  field8==110 (sum_id); exactly one with field8==50
  (count_id); sum_id < count_id.
- PC1: driver walks classify both graphs as predicted on both
  binaries.
- K1 (D1-FIND): fixed binary returns count_id; control binary
  returns sum_id (the shadowing the fix removes). K1 fails if
  fixed returns sum_id, or if control does NOT return sum_id
  (then the old code never demonstrated the shadow and the
  discrimination claim is void).
- K2 (D1-AGGOK): fixed: sum 0, count 1; control: sum 1,
  count 1.
- K3 (D1-AGGREL): fixed == 82; control != 82 (predicted 31:
  the sum MAP's first type-1 licensing fact carries rel 31).
  K3 fails if fixed != 82 or control == 82.
- K4 (R1): 3/3 runs of sdf_r1 byte-identical (cmp) to the
  frozen countmap1_run1.txt.
- K5 (R2): 3/3 runs of sdf_r2 byte-identical (cmp) to the
  frozen xdagfan4_run1.txt.
- K6 (R3): 3/3 runs of sdf_r3 byte-identical (cmp) to the
  frozen xf_run1.txt.
- K7 (hygiene): pure Zag; safebin PATH from the first command
  (Step 0 in NAMECHECK.md); zero em/en dash bytes in lane docs
  (byte-verified); opaque identifiers only; frozen blocks
  reused verbatim for controls (SHA256 re-verified pre/post);
  diff of each patched block against its frozen source shows
  ONLY the two added detector fns and the two call-site swaps;
  `xs5_has_inc` byte-identical and referenced by no lookup
  path (grep); `xs5_find_countmap` still lowest-id-wins and
  `xs5_agg_rel` byte-identical (singleton lookup NOT changed);
  driver-only new code under sdf_ plus the two census
  predicate swaps; 0 new node types, 0 new edge types, 0 new
  opcodes, 0 modes, bridges, handlers, semantic cases; no
  `!(A && B)` in any while condition (grep); Zag pitfalls
  honored (NAMECHECK.md); commits local only, never pushed,
  explicit pathspecs.

Verdict SUM-DETECTOR-FIX-PASS iff K1 through K7 all pass.
VOID is terminal.

## What this does NOT claim

- This is not COUNTMAP-2: the lookup stays a lowest-id-wins
  singleton, still query-blind. It is now type-honest.
- This is not SUM-1 items 2-7: no sum lookup, no sum
  executor, no composition legs, no formation changes. Items
  2-7 stay on hold.
- The D1 world is surgical scaffolding for the detector
  branches (a sum MAP formed by the real trial sum phase via
  the t_p2 shape, then a count MAP via the frozen XP-
  COUNTMAP-1 shape), not a claimed natural composition
  event.
- The 64-step walk bound is documented on the sum detector;
  it cannot confuse the two frozen assembler shapes (every
  count graph shows its guard at the root).

## Implementation plan (after prereg commit)

1. Re-verify frozen SHAs. Extract xdagfan4_driver.zag
   verbatim via read-only git show.
2. Build sdf_base_block.zag and sdf_xf_block.zag by patching
   lane copies; diff each against its frozen source.
3. Write the three drivers (R1 census swap, R3 census swaps,
   D1 new).
4. Compile all five binaries with the pinned znc under
   safebin; run R1/R2/R3 fixed 3x each (cmp against frozen
   run records); run D1 fixed 1x and control 1x; shell-verify
   every kill bar.
5. Write REPORT.md. Commit with explicit pathspecs (lane
   directory only; never the ledger; never push).

## Constraints

Frozen read-only (never modified). Pure Zag (safebin PATH from
the first command, no python; Step 0 in NAMECHECK.md). Zero
em/en dashes. Commits local only, never pushed, explicit
pathspecs, no reset, no amend of shared history. The
singleton lookup is not changed beyond the detector swap;
COUNTMAP-2 stays on hold. SUM-1 items 2-7 stay on hold. Do not
modify CLAIM_LEDGER.md. Zag pitfalls honored.

## Battery well-formedness (disclosed pre-freeze work)

No implementation, driver code, or patched block was written
before this freeze. Pre-freeze work was limited to reading:
the SUM-ADDRESSABILITY REPORT.md, the COUNTMAP-ADDRESSABILITY
REPORT.md, the xp_countmap1 lane (PREREG, NAMECHECK, driver,
REPORT), the xhier_countmap_fix lane (PREREG, xf_block.zag
diff, xf_driver.zag), the frozen block source at the cited
line refs, and the XP-DAGFAN-4 artifacts via read-only git
show. The D1 value predictions (sq==60 from the t_p2 shape,
cq==3 from the XP-COUNTMAP-1 shape, control aggrel 31 from
the promote_graph type-1 edge order) are derived from frozen
operator semantics, not from any pilot run. The frozen bars
were not adjusted to fit any outcome: the control-binary legs
(K1 sum_id, K2 sum 1, K3 != 82) exist precisely to void the
discrimination claim if the old code does not misaddress as
reasoned.
