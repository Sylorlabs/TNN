# PREREG: XHIER-COUNTMAP-FIX (use the composite's own count MAP address)

Frozen 2026-10-03, v2 (amends v1, committed 16048790e).
Worker: XHIER-COUNTMAP-FIX. Branch: tnn-native-lab, local only,
never pushed. Lane:
docs/lab/research-lead/overnight-20260928/xhier_countmap_fix/
(files xf_*). Non-ledger task (claim minting paused).

## Amendment note (v1 -> v2): why the construction changed

v1 built and ran after the v1 prereg commit. The patch itself
(xhier_mapz_rel + xhier_exec, in xf_block.zag) behaved as
predicted on the v1 pilot run (K1-EXEC 3 via the composite's own
rel 85 while the singleton named rel 82: the fix path works).
But the v1 *world construction* is unimplementable, for a
reason found in frozen source during v1 implementation:

`alloc_node` (block :87) scans node ids 2..1023 and reuses the
FIRST slot with live flag 0. Tombstoning MAP_Y therefore does
not suspend it: it frees slot 84 for recycling, and the next
allocation takes it. v1's "restore MAP_Y" step
(`ns(W,my,36,1)`) could not resurrect the MAP; worse, restoring
the tag (`ns(W,my,0,20)`) retagged whatever unrelated node had
recycled the slot (a Phase-C fact node), corrupting the world
(the v1 pilot showed S-SINGLETON stuck at 194 and a spurious
NOREL at K1 from the corruption). Tombstone-then-restore is not
a suspend/resume in this architecture; it is destroy-then-
clobber. The v1 pilot outputs are discarded as results; they
serve only as the empirical trigger for this amendment.

v2 keeps the frozen patch byte-identical and rebuilds the test
world so no step depends on resurrecting a tombstoned node:

- A third count MAP (MAP_V3, rel 87) is formed via the proven
  trial path, so the divergence no longer needs MAP_Y to come
  back.
- MAP_Z2's link to the non-singleton count MAP is built with
  frozen ops only (`promote_graph` + `link_edge`, the exact
  shape `xs5_try_nav_agg` produces), instead of relying on
  compose-time singleton capture across a tombstone.
- MAP_Y is tombstoned once, late, with no restore: the task's
  literal scenario. Slot recycling after the tombstone is
  harmless because no later step allocates before the final
  xhier_exec calls... (verified below: the only allocs after
  the tombstone are none; K3a/K3b tombstone further nodes,
  also with no later allocs).

Kill-bar semantics are unchanged (K1 discriminates fixed vs
control on the divergence world; K2 guards the happy path; K3
tests the loud fences; K4 determinism; K5 hygiene). Predicted
values change: K1 is now 4 (fixed) vs 3 (control).

## Objective

COUNTMAP-ADDRESSABILITY Section 5(a) reported a latent
correctness issue, reasoned from source, never executed:
`xhier_exec` resolves each MAP_Z's own type-14 count MAP address
(`a = xhier_mapz_agg(W,z)`), uses it only as an existence gate
(`if(a<0){return -2;}`), then executes the global singleton
anyway (`xs5_agg_exec(W,e,xs5_agg_rel(W))`). If the composite's
own count MAP ever names a different relation than the ambient
singleton (e.g. MAP_Y tombstoned while other count MAPs stay
live), every MAP_Z silently aggregates over the wrong relation
while its own LINK14 edges name the right one. The parent
recommendation: fix or fence this when MAP_Z work next runs; a
correctness fix independent of COUNTMAP-2.

This experiment implements the fix, fenced where the address is
unusable, and proves it against a control binary running the
frozen block verbatim on the same world.

## The fix (honest decision: fix on the happy path, fence on breakage)

Fence-only (refuse whenever the composite's count MAP disagrees
with the singleton) was rejected: it would make `xhier_exec`
return -2 in exactly the worlds where the composite's own
provenance is informative and correct, converting a correctable
divergence into a refusal. The composite was verified at compose
time against its own count MAP; executing with its own relation
preserves the verified semantics.

Patch (applied to a lane copy of the frozen block; the frozen
original is never modified; UNCHANGED between v1 and v2):

1. New helper `xhier_mapz_rel(W,m)`, placed after
   `xhier_mapz_agg`: the exact `xs5_agg_rel` read shape
   (scan edges 0..4095 for `(m -1-> f)`, first live tag-1
   target, return its rel field 24), parameterized by the MAP
   id instead of calling `xs5_find_countmap`. Returns -1 when
   unreadable.
2. Patched `xhier_exec`:
   - `a<0` (no live count MAP on the composite's own type-14
     edges: tombstoned or never linked): emit
     `XHIER-EXEC-NOAGG z=<z>`, return -2. Loud fence.
   - relation `r = xhier_mapz_rel(W,a)`; `r<0` (address
     resolved but its relation unreadable): emit
     `XHIER-EXEC-NOREL a=<a>`, return -2. Loud fence.
   - else `xs5_agg_exec(W,e,r)`: the composite's own count
     MAP's relation, not the singleton. The fix.
3. Explicitly NOT changed: `xs5_find_countmap`,
   `xs5_agg_rel` (byte-identical in the patched block,
   verified by diff), and all their other call sites
   (`xs5_compose`, `xs5_select`, `xs5_agg_exec`,
   `xs5_try_nav_agg`). COUNTMAP-2 stays on hold: no
   parameterized world-global lookup is added; this is a
   per-composite provenance read, not indexed addressing.

In single-relation worlds `a` is always the singleton, so
`xhier_mapz_rel(W,a)` equals `xs5_agg_rel(W)` by construction
and no loud path fires: the patched binary must behave
identically to the frozen one (K2).

## Frozen background (read-only, never modified)

- Build block: xp_countmap1/countmap1_block.zag (the
  XP-DAGFAN-4 block), 2648 lines, SHA256
  56b2e678d42103d7fb9bf75e8c99289a1698844891a654e215bc025915231004,
  re-verified by sha256sum before freezing. Copied verbatim to
  the lane as xf_block_control.zag (control binary); copied and
  patched as xf_block.zag (fixed binary). No frozen name is
  redefined by the driver.
- Key frozen semantics (all line refs to the block):
  - `xhier_exec` (:2546): the latent site. Gate on `a`, then
    `xs5_agg_rel(W)`.
  - `xhier_mapz_agg` (:2532): first live count-MAP type-14
    target of z, or -1. Only live MAPs pass
    (`xhier_agg_ok`: live flag 36, tag 20, INC cell).
  - `xs5_find_countmap` (:2134): lowest live id wins. NOT
    changed.
  - `xs5_agg_rel` (:2147): singleton's provenance relation.
    NOT changed.
  - `xs5_try_nav_agg` (:2190): promotes MAP_Z with LINK14 to
    the nav MAP and to the then-current singleton count MAP.
  - `promote_graph` (:533) with root -1: MAP_Z field-20 is -1,
    so MAP_Zs are never nav-ok (`cc_relseq` < 1) and never
    count-ok (`xs5_has_inc(-1)` = 0). The driver uses this
    exact call shape for the surgical MAP_Z2.
  - Tombstone pattern (:731): `ns(W,stale,0,0);
    ns(W,stale,36,0)`. Destructive: `alloc_node` (:87)
    recycles the first live-0 slot, so a tombstoned node
    cannot be restored (v1 lesson).
  - `t2_try_verify` (:497) with masked=1 returns the raw
    count, no expected check: `xs5_agg_exec` returns the
    chain length over the given relation.

## Design (v2)

All identifiers opaque (relation numbers only). One workspace.
Driver prefix xf_. The driver NEVER calls ev_query_xhier
(the only in-block xhier_exec caller besides the driver's own
direct calls), so every xhier_exec under test is a direct,
surgical call. No phase allocates after the MAP_Y tombstone
except K3a/K3b's own tombstones (also allocation-free
afterward); slot recycling is therefore inert.

Phase A, verbatim XP-COUNTMAP-1 phase A (proven shape):
teach (11,81,12), (12,81,13), (13,81,14);
ev_query_xs5(11,91,14) -> 14 (forms the 81 nav MAP);
teach (50,82,51), (51,82,52), (52,82,53);
ev_query_xs5(50,92,3) -> 3 (forms MAP_Y, the 82 count MAP);
30 distractors (5000+i, 60+(i%10), 6000+i).
Stash my = xs5_find_countmap(W) (expect >= 0).

Phase B, verbatim XP-COUNTMAP-1 phase B formation step (proven
shape): teach (110,85,111), (111,85,112), (112,85,113),
(113,85,114); b = ev_query_xs5(110,117,4) -> 4 (trial forms
MAP_V2, the 85 count MAP). Stash mv2 = the live count MAP id
!= my (exhaustive INC-ok scan).

Phase B2, third count MAP (same proven trial shape, fresh
relation): teach (120,87,121), (121,87,122), (122,87,123),
(123,87,124); b2 = ev_query_xs5(120,118,4) -> 4 (trial forms
MAP_V3, the 87 count MAP: rebind cannot answer, xs5_compose
fails, count path verifies 4==4). Stash mv3 = the live count
MAP id distinct from my and mv2.

Phase R, regression (pre-tombstone, singleton = MAP_Y, rel
82): teach (14,82,40), (40,82,41): 2-link 82-count at 14.
c = xs5_compose(W,11,94,2) direct call: nav MAP walks 11->14,
count over 82 at 14 = 2 == expected, promotes MAP_Z1 with
LINK14 to the nav MAP and to MAP_Y (then-singleton).
Stash mz1 = the MAP_Z id (xhier_is_mapz scan; the only one).
vR = xhier_exec(W,mz1,11). Emit XF-PHASER-END marker.

Phase C, divergence construction (frozen ops only, no
tombstone yet): teach (14,87,60), (60,87,61), (61,87,62),
(62,87,63): 4-link 87-count at 14; teach (14,85,30),
(30,85,31), (31,85,32): 3-link 85-count at 14. (The 82-count
at 14 from Phase R stays the only 82-chain there: no fork.)
mz2 = promote_graph(W,-1,11,93,4,emptyfacts,0) direct call
(the exact MAP_Z call shape); link_edge(W,mz2,14,navX,0)
where navX = xhier_mapz_nav(W,mz1); link_edge(W,mz2,14,mv3,0).
MAP_Z2's provenance names MAP_V3 honestly: this is the world
state the latent issue is about (a composite addressing a
non-singleton count MAP), constructed with the same ops the
composition layer itself uses.

Tombstone MAP_Y (the task's scenario): ns(W,my,0,0);
ns(W,my,36,0). No restore: the slot recycles, which is fine
because nothing after this point needs MAP_Y. The singleton
becomes MAP_V2 (rel 85). Divergence: MAP_Z2's own live count
MAP is MAP_V3 (provenance rel 87) while the world singleton
names rel 85.

K1, the tombstone test: v = xhier_exec(W,mz2,11) direct call.

K3a, provenance-unreadable fence: tombstone every live tag-1
type-1 provenance target of MAP_V3 (loop until none; count
killed); v = xhier_exec(W,mz2,11).

K3b, tombstoned-address fence: tombstone MAP_V3 itself;
v = xhier_exec(W,mz2,11).

Query budget: 4 full ev_query_xs5 calls (phases A x2, B x1,
B2 x1) plus 1 direct xs5_compose call plus 1 direct
promote_graph/link pair plus 4 direct xhier_exec calls
(Phase R x1, K1 x1, K3a x1, K3b x1), within the demonstrated
safe range.

Two binaries, one driver:
- xf_fixed: cat xf_block.zag (patched) xf_driver.zag.
- xf_control: cat xf_block_control.zag (frozen verbatim)
  xf_driver.zag.
The driver is identical; only the block differs. The control
binary is the honest baseline: it shows what the old code does
on the divergence world.

## Frozen predictions

- PC-A: my >= 0 and xs5_agg_rel(W) == 82 after phase A.
- PC-B: exactly 2 live INC-ok count MAPs after phase B; the
  higher-id one's provenance rel == 85; b == 4.
- PC-B2: exactly 3 live INC-ok count MAPs after phase B2; the
  newest one's provenance rel == 87; b2 == 4.
- PC-R: xs5_compose(W,11,94,2) promotes MAP_Z1 (exactly one
  MAP_Z exists); vR == 2 on BOTH binaries.
- PC-C: promote/link yields mz2 with xhier_is_mapz(W,mz2)==1;
  xhier_mapz_agg(W,mz2) == mv3; provenance rel of mv3 == 87;
  exactly two MAP_Zs exist.
- PC-T: after tombstoning MAP_Y, xs5_find_countmap(W) == mv2
  and xs5_agg_rel(W) == 85 (MAP_Y's slot is gone; the next
  lowest live count MAP wins).
- K1: fixed-binary K1-EXEC == 4 (count over rel 87, the
  composite's own relation); control-binary K1-EXEC == 3
  (count over rel 85, the singleton's relation: the old code
  silently aggregates over the wrong relation while MAP_Y is
  tombstoned).
- K2: PC-R holds on both binaries (vR == 2 each), AND the
  fixed-run stdout prefix through XF-PHASER-END is
  byte-identical to the control-run prefix (cmp): the patch
  changes nothing on the happy path.
- K3a: fixed K3A-EXEC == -2, killed >= 1, stdout contains
  XHIER-EXEC-NOREL. (Control: the old code returns 3 here,
  silently.)
- K3b: fixed K3B-EXEC == -2, stdout contains
  XHIER-EXEC-NOAGG. (Control: -2 via the silent gate.)
- K3c: control stdout contains neither XHIER-EXEC-NOREL nor
  XHIER-EXEC-NOAGG (loudness is new behavior).
- K4: 3/3 byte-identical whole-output runs of xf_fixed;
  sha256 recorded.
- K5: pure Zag; safebin PATH from the first command; zero
  em/en dash bytes in lane docs (byte-verified); opaque
  identifiers only; frozen block reused verbatim for control
  (SHA re-verified pre/post); diff of xf_block.zag against
  xf_block_control.zag shows ONLY the added xhier_mapz_rel
  helper and the xhier_exec body (xs5_find_countmap and
  xs5_agg_rel byte-identical: singleton lookup untouched);
  driver-only new code under the xf_ prefix plus the two
  loud-fail emits inside xhier_exec; 0 new node types, 0 new
  edge types, 0 new opcodes, 0 new operators, 0 modes,
  bridges, handlers; Zag pitfalls honored (see NAMECHECK.md).

## Kill-bar discrimination (why each bar can fail)

- K1 fails if the fix does not take (fixed returns 3 or -2),
  if the divergence was not constructed (preconditions catch
  it), or if the control binary does NOT return 3 (then the
  test never demonstrated the old silent-wrong behavior, and
  the discrimination claim is void).
- K2 fails if the patch alters happy-path behavior: any
  vR != 2, or any stdout prefix byte difference (a stray
  emit, a changed value, a reordered allocation).
- K3a fails if the NOREL fence does not fire (wrong return
  or missing trace), or if fewer than 1 provenance fact was
  killed (fence untested).
- K3b fails if the NOAGG fence does not fire loudly on a
  tombstoned linked count MAP.
- K3c fails if the control binary emits either loud line
  (would mean the loudness predates the fix).
- K4/K5 are process bars: any nondeterminism, toolchain
  lapse, singleton-lookup diff, or dash byte voids the result.

Verdict XHIER-COUNTMAP-FIX-PASS iff K1, K2, K3 (a+b+c), K4,
K5 all pass. VOID is terminal.

## What this does NOT claim

- This is not COUNTMAP-2. No parameterized world-global
  lookup is added; count MAPs are not addressable by relation
  through composition after this fix. The xs5_compose
  singleton behavior is unchanged.
- This does not change formation, promotion, provenance
  writing, or the trial layer in any way.
- The Phase-C manual promotion is surgical world
  construction with frozen ops, not a claimed natural event;
  it builds the composite-provenance-diverges-from-singleton
  state the latent issue is about. The K3a construction
  (tombstoning provenance facts) is likewise scaffolding for
  the fence branch, nothing more.

## Implementation plan (after prereg commit)

1. The frozen block copies stand (xf_block_control.zag SHA
   56b2e678d42103d7fb9bf75e8c99289a1698844891a654e215bc025915231004
   re-verified; xf_block.zag carries the unchanged v1 patch,
   diff re-verified).
2. Rewrite xf_driver.zag (xf_ prefix) to the v2 world plan:
   phases A/B/B2/R/C, MAP_Y tombstone with no restore, manual
   MAP_Z2 promotion + linking, K1/K3 direct xhier_exec calls,
   precondition tallies. Pure Zag. No redefinition of any
   frozen name. Zag pitfalls honored.
3. Build: cat xf_block.zag xf_driver.zag > xf_full.zag;
   cat xf_block_control.zag xf_driver.zag >
   xf_control_full.zag. Compile both with the pinned znc;
   run fixed 3x (byte-identical check); run control 1x;
   shell-verify every kill bar per the predictions above.
4. Write xf_REPORT.md. Commit with explicit pathspecs
   (lane directory only; never the ledger; never push).

## Constraints

Frozen read-only (the 2648-line build block; the
xp_countmap1 lane is not modified). Pure Zag (safebin PATH
from the first command, no python; Step 0 recorded in
NAMECHECK.md). Zero em/en dashes. Commits local only, never
pushed, explicit pathspecs, no reset, no amend of shared
history. The singleton lookup (xs5_find_countmap,
xs5_agg_rel) is not changed; COUNTMAP-2 stays on hold. Do not
modify CLAIM_LEDGER.md. Zag pitfalls honored.

## Battery well-formedness (disclosed pre-freeze work)

v1 was implemented and run once after the v1 prereg commit;
its patch (unchanged in v2) behaved as predicted on the fix
path, but its tombstone-then-restore world construction
proved unimplementable (slot recycling, see the amendment
note); the v1 pilot outputs are discarded as results. The v2
world plan is new: phases B2 and C and the K1/K3 value
predictions (4/3) are derived from frozen operator semantics
(masked t2_try_verify returns raw chain counts; lowest live
id wins the lookup; promote_graph + link_edge produce the
documented MAP_Z shape), not from the v1 pilot's outputs.
No driver code for the v2 plan was written or prototyped
before this freeze. The frozen bars were not adjusted to fit
any outcome: the control-binary legs (K1 == 3, K3a == 3
silent, K3c) exist precisely to void the discrimination claim
if the old code does not behave as reasoned. Pre-freeze
verification was limited to reading the
COUNTMAP-ADDRESSABILITY REPORT.md, the xp_countmap1 lane
(PREREG, NAMECHECK, driver, REPORT), and the frozen block
source at the line refs above, plus re-verifying the
build-block SHA.
