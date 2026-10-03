# PREREG: XHIER-COUNTMAP-FIX (use the composite's own count MAP address)

Frozen 2026-10-03. To be committed alone before implementation.
Worker: XHIER-COUNTMAP-FIX. Branch: tnn-native-lab, local only,
never pushed. Lane:
docs/lab/research-lead/overnight-20260928/xhier_countmap_fix/
(files xf_*). Non-ledger task (claim minting paused).

## Objective

COUNTMAP-ADDRESSABILITY Section 5(a) reported a latent
correctness issue, reasoned from source, never executed:
`xhier_exec` resolves each MAP_Z's own type-14 count MAP address
(`a = xhier_mapz_agg(W,z)`), uses it only as an existence gate
(`if(a<0){return -2;}`), then executes the global singleton
anyway (`xs5_agg_exec(W,e,xs5_agg_rel(W))`). If the composite's
own count MAP ever names a different relation than the ambient
singleton (e.g. MAP_Y tombstoned while a second count MAP stays
live, then MAP_Y restored), every MAP_Z silently aggregates over
the wrong relation while its own LINK14 edges name the right
one. The parent recommendation: fix or fence this when MAP_Z
work next runs; a correctness fix independent of COUNTMAP-2.

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
original is never modified):

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
    count-ok (`xs5_has_inc(-1)` = 0).
  - Tombstone pattern (:731): `ns(W,n,0,0); ns(W,n,36,0)`.
    Restore is `ns(W,n,36,1)` (tag field untouched).
  - `t2_try_verify` (:497) with masked=1 returns the raw
    count, no expected check: `xs5_agg_exec` returns the
    chain length over the given relation.

## Design

All identifiers opaque (relation numbers only). One workspace.
Driver prefix xf_. The driver NEVER calls ev_query_xhier
(the only in-block xhier_exec caller besides the driver's own
direct calls), so every xhier_exec under test is a direct,
surgical call.

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

Phase R, regression (pre-surgery, singleton = MAP_Y, rel 82):
teach (14,82,40), (40,82,41): 2-link 82-count at 14.
c = xs5_compose(W,11,94,2) direct call: nav MAP walks 11->14,
count over 82 at 14 = 2 == expected, promotes MAP_Z1 with
LINK14 to the nav MAP and to MAP_Y (then-singleton).
Stash mz1 = the MAP_Z id (xhier_is_mapz scan; the only one).
vR = xhier_exec(W,mz1,11). Emit XF-PHASER-END marker.

Tombstone MAP_Y: ns(W,my,0,0); ns(W,my,36,0). The singleton
becomes MAP_V2 (rel 85).

Phase C, divergence construction: teach (14,85,30),
(30,85,31), (31,85,32): 3-link 85-count at 14. (The 82-count
at 14 from Phase R stays the only 82-chain there: no fork.)
c2 = xs5_compose(W,11,93,3) direct call: nav MAP walks 11->14,
r_agg = 85 (MAP_Y tombstoned), count over 85 at 14 = 3 ==
expected, promotes MAP_Z2 with LINK14 to the nav MAP and to
MAP_V2 (then-singleton, via the normal compose path: honest
provenance, no driver surgery on edges). Stash mz2 = the new
MAP_Z id.

Restore MAP_Y: ns(W,my,36,1). Singleton flips back to MAP_Y
(lowest live id, rel 82). Divergence precondition: MAP_Z2's
own live count MAP is MAP_V2 (provenance rel 85) while the
world singleton names rel 82.

K1, the tombstone test: v = xhier_exec(W,mz2,11) direct call.

K3a, provenance-unreadable fence: tombstone every live tag-1
type-1 provenance target of MAP_V2 (loop until none; count
killed); v = xhier_exec(W,mz2,11).

K3b, tombstoned-address fence: tombstone MAP_V2 itself;
v = xhier_exec(W,mz2,11).

Query budget: 3 full ev_query_xs5 calls (phases A x2, B x1)
plus 2 direct xs5_compose calls plus 4 direct xhier_exec
calls (Phase R x1, K1 x1, K3a x1, K3b x1), within the
demonstrated safe range.

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
- PC-R: xs5_compose(W,11,94,2) promotes MAP_Z1 (exactly one
  MAP_Z exists); vR == 2 on BOTH binaries.
- PC-T: after tombstoning MAP_Y, xs5_find_countmap(W) == mv2
  and xs5_agg_rel(W) == 85.
- PC-C: xs5_compose(W,11,93,3) promotes MAP_Z2 (exactly two
  MAP_Zs exist); xhier_mapz_agg(W,mz2) == mv2; provenance
  rel of mv2 == 85.
- PC-S: after restoring MAP_Y, xs5_find_countmap(W) == my and
  xs5_agg_rel(W) == 82; xhier_mapz_agg(W,mz2) == mv2 still
  (MAP_V2 live). The divergence is real: composite's own
  address names rel 85, singleton names rel 82.
- K1: fixed-binary K1-EXEC == 3 (count over rel 85, the
  composite's own relation); control-binary K1-EXEC == 2
  (count over rel 82, the singleton's relation: the old code
  silently aggregates over the wrong relation).
- K2: PC-R holds on both binaries (vR == 2 each), AND the
  fixed-run stdout prefix through XF-PHASER-END is
  byte-identical to the control-run prefix (cmp): the patch
  changes nothing on the happy path.
- K3a: fixed K3A-EXEC == -2, killed >= 1, stdout contains
  XHIER-EXEC-NOREL. (Control: -2 is not expected; the old
  code returns 2 here, silently.)
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

- K1 fails if the fix does not take (fixed returns 2 or -2),
  if the divergence was not constructed (preconditions catch
  it), or if the control binary does NOT return 2 (then the
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
  singleton behavior is unchanged (K1's control leg
  re-demonstrates it on a new world).
- This does not change formation, promotion, provenance
  writing, or the trial layer in any way.
- The K3a construction (tombstoning provenance facts) is
  surgical test scaffolding, not a claimed natural event;
  it exercises the fence branch, nothing more.

## Implementation plan (after prereg commit)

1. Copy the verified frozen build block to the lane as
   xf_block_control.zag; re-verify SHA256
   56b2e678d42103d7fb9bf75e8c99289a1698844891a654e215bc025915231004.
2. Copy to xf_block.zag; apply the two-part patch (add
   xhier_mapz_rel after xhier_mapz_agg; replace the
   xhier_exec body); diff against control to prove the only
   differences are the helper and the xhier_exec body.
3. Write xf_driver.zag (xf_ prefix): phase A/B/R/C,
   tombstone/restore surgery, MAP_Z discovery helpers,
   K1/K3 direct xhier_exec calls, precondition tallies.
   Pure Zag. No redefinition of any frozen name. Zag
   pitfalls honored.
4. Build: cat xf_block.zag xf_driver.zag > xf_full.zag;
   cat xf_block_control.zag xf_driver.zag >
   xf_control_full.zag. Compile both with the pinned znc;
   run fixed 3x (byte-identical check); run control 1x;
   shell-verify every kill bar per the predictions above.
5. Write xf_REPORT.md. Commit with explicit pathspecs
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

Before freezing, no driver code was written or prototyped and
no block copy was made. The phase-A and phase-B shapes are the
committed XP-COUNTMAP-1 shapes (executed, PASS); phases R and
C compose new queries from frozen operator semantics
(xs5_try_nav_agg promotion, LINK14 capture of the
then-singleton, t2_chain per-relation walks); the tombstone
pattern is the frozen t2_revise_graph pattern (:731); the
K1/K2/K3 value predictions are derived from frozen operator
semantics (masked t2_try_verify returns raw counts; lowest
live id wins the lookup), not from execution. The frozen bars
were not adjusted to fit any outcome: the control-binary leg
(K1c == 2, K3c) exists precisely to void the discrimination
claim if the old code does not behave as reasoned.
Pre-freeze verification was limited to reading the
COUNTMAP-ADDRESSABILITY REPORT.md, the xp_countmap1 lane
(PREREG, NAMECHECK, driver, REPORT), and the frozen block
source at the line refs above, plus re-verifying the
build-block SHA.
