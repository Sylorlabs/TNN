# REPORT: L2-COMBINED (multi-adaptation composition in one pipeline)

Worker: L2-Combined Worker (subagent, 2026-10-02).
Branch: tnn-native-lab. Local only, never pushed.

## Verdict

**L2-COMBINED-PASS.** K1 through K12 all pass (K1/K2/K5/K8 under
transparent pre-verdict PREREG_AMENDMENT1, which corrected the
hand-derived node ids for killed-fact slot reuse; no bar weakened).
One learner fires TWO different L2 adaptation operators in a single
query pipeline, the later operating on the earlier's output: a chain
MAP that is BOTH stale in the middle (dead licensing fact 3) AND too
short for the span (term 104 < goal 107) is repaired by SUBSTITUTE
then iterative EXTEND, with full provenance, and the composite is
reused as one unit on a second query.

## What was built

`l2c_patch.zag` (combined learner patch) on frozen
cc_base/un_patch/adapt_patch/extn_patch (sha256-verified verbatim
copies), plus `l2c_driver.zag` (world + six arms). The pipeline
`l2c_query`: learner-owned select (exact terminal wins, else
longest) -> stale-check -> SUBSTITUTE (C298 semantics: split at dead
hop, node-id order live-piece search, assemble, execution-verify,
type-16 promote) -> span-check -> EXTEND-ITER from the substitute's
output MAP (C301 `extn_step` reused verbatim, TERM/NOFRONTIER/
EXECFAIL/BUDGET stops) -> full-chain verify -> provenance
(LINK14 to segments, type-15 co-use on consecutive delivery pairs)
-> answer. Order is learner-discovered: staleness is checked before
span because span reasoning on a stale MAP is untrustworthy.

## Per-arm results (3/3 runs byte-identical, exit 0)

| arm | ans | sub | ext | stop | final | allocs | verdict |
|-----|-----|-----|-----|------|-------|--------|---------|
| FULL | 107 | 1 | 3 | 0 | 132 | 132 | PASS |
| REUSE q1/q2 | 107/107 | 1/0 | 3/0 | 0/3 | 132/132 | 132 | PASS |
| EXTONLY | -2 | 0 | 0 | 3 | -1 | 126 | PASS |
| SUBONLY | -3 | 1 | 0 | 3 | 54 | 54 | PASS |
| EXACT | -2 | 0 | 0 | 3 | -1 | 126 | PASS |
| FRESH | -2 | 0 | 0 | 3 | -1 | 99 | PASS |

Run sha256 (all three):
`ebd37eae9e4e02e9df304c51ae2caee9307bac5f67ce70bdcf8f52e47327c88f`
pairwise cmp clean.

## Kill bars

- K1 (FULL exact): PASS. ans=107, sub=1, ext=3, stop=0 TERM,
  final=132; relseq(132)=[1,1,1,1,1,1,1]; type-16 hops 4
  (132->102->76->54->23); ultimate native ancestor 23.
- K2 (provenance exact): PASS. t16=5 with pairs
  {(54,23),(54,37),(76,54),(102,76),(132,102)};
  t14=3, all from 132, dsts {23,37,54};
  t15=5 with pairs {(23,37),(37,54),(54,76),(76,102),(102,132)};
  zero other 14/15/16 edges.
- K3 (white-box trace): PASS. All 16 frozen lines of PREREG
  section 4 (as corrected by the amendment) present verbatim in
  order in run1.txt (mechanical check: 16/16 in order); SUB-*
  lines precede EXTN-* lines, so the learner-discovered order
  (substitute before extend) is white-box. Each firing names the
  op, its trigger (dead fact 3; span shortfall 104 vs 107), and
  the MAP ids. (The prereg text says "17 lines"; the section
  actually lists 16, all present; count typo only.)
- K4 (EXTONLY ablation): PASS. ans=-2; t16=t14=t15=0; trace shows
  SUB-STALE m=23 hop=1 fact=3, then L2C-SPAN EXTEND, then
  EXTN-REFUSE-STALE m=23: the extend operator's own
  full-satisfiability precondition refuses the stale MAP, and the
  generic trial cannot span 7 links (4-link cap). Extend-alone
  fails; the wrong order (extend without substitute) fails at the
  operator precondition, proving substitute must fire first.
- K5 (SUBONLY ablation): PASS. ans=-3; substitute fired and
  promoted m2=54 (t16=2: 54->23, 54->37; ng(54,28)=104);
  t14=t15=0 (no provenance on episode failure); trace shows
  L2C-SPAN term=104 goal=107 SHORTFALL. Substitute-alone fails.
- K6 (EXACT control): PASS. ans=-2; t16=t14=t15=0; SUB-STALE
  fires, MAP unusable, trial fails. Exact reuse fails.
- K7 (FRESH control): PASS. ans=-2; t16=0; L2C-NOSEL, trial
  fails (no 7-link path within the 4-link gather cap; count 7,
  sum 102, and 1-link candidates all reject 107). The learned
  structure was load-bearing.
- K8 (REUSE): PASS. q1 ans=107; q2 ans=107 via m=132
  (exact-terminal select), sub=0, ext=0; after q2 t16=5, t14=3,
  t15=5, mapcount=7, all unchanged; q2 trace has zero SUB-/EXTN-
  lines:
  L2C-QUERY / L2C-SEL m=132 plen=7 term=107 /
  L2C-SPAN term=107 goal=107 OK / L2C-VERIFY term=107 OK /
  L2C-ANS via=132 val=107.
  The multi-adapted composite persists as one unit.
- K9 (determinism): PASS. 3/3 byte-identical, sha256 above,
  exit 0 on all runs.
- K10 (0 new machinery): PASS. Frozen copies sha256-identical to
  origins (cc_base dc0e86d4..., un_patch 3e61056a...,
  adapt_patch 867bd6d9..., extn_patch 78821703...); origins
  unmodified. New code issues link_edge only with types 14/15/16
  (3/5/2 calls); 0 new edge types, opcodes, modes, bridges,
  handlers, semantic cases, node tags; no relation/value literals
  in the learner patch (world values live in the driver only);
  grep audit: no `as *i32`, no `while.*!(`, no _MODE/bridge (one
  comment hit is the audit claim itself).
- K11 (commit order): PASS. Prereg commit b512181bf contains only
  PREREG.md and NAMECHECK.md (2 files, verified by git show
  --stat); PREREG_AMENDMENT1.md committed pre-verdict with the
  implementation.
- K12 (no dashes): PASS. check_no_dash.sh clean on all
  deliverables.

No falsifier fired.

## White-box trace: FULL (run 1, identical in runs 2-3)

```
L2C-QUERY s=101 goal=107
L2C-SEL m=23 plen=3 term=104
SUB-STALE m=23 hop=1 fact=3
SUB-CAND id=23 skip=self
SUB-CAND id=28 s=102 e=110 skip=ep
SUB-CAND id=37 s=102 e=103 flive=2 MATCH
SUB-BUILD rels=1,1,1,1 facts=2,5,6,4
SUB-VERIFY term=104
SUB-PROMOTE m2=54
L2C-SPAN term=104 goal=107 EXTEND
EXTN-STEP n=1 parent=54 id=76 plen=5 lic=104,1,105 term=105
EXTN-STEP n=2 parent=76 id=102 plen=6 lic=105,1,106 term=106
EXTN-STEP n=3 parent=102 id=132 plen=7 lic=106,1,107 term=107
EXTN-STOP reason=0 ext=3 ans=107 final=132
L2C-VERIFY term=107 OK
L2C-ANS via=132 val=107
```

Reading: the learner selects native MAP 23, detects its hop-1
licensing fact dead, searches its inventory (self skipped,
distractor 28 rejected on endpoints 102->110 vs 102->103, piece 37
matched with 2/2 facts live), assembles facts [2,5,6,4] into MAP
54 (type-16 to 23 and 37), verifies by execution to 104, sees the
span shortfall (104 vs 107), and extends three times from the new
frontier, each step licensed by a live fact and type-16 linked,
stopping TERM at the goal. Provenance is written only on episode
success.

## Ablation numbers

- Extend-only (EXTONLY): 0 adaptations, ans=-2 after 126 node
  allocations of trial search; the extend operator refuses stale
  input at its precondition.
- Substitute-only (SUBONLY): 1 adaptation, 54 allocations,
  ans=-3; the repaired MAP terminates at 104, 3 links short.
- Exact (EXACT): 0 adaptations, ans=-2.
- Fresh (FRESH): 0 adaptations, ans=-2 after 99 allocations.
- Treatment (FULL): 2 adaptations in sequence, 132 allocations,
  ans=107. Both adaptations were load-bearing: removing either
  fails exactly as derived, and the order substitute-then-extend
  is enforced by the extend precondition (wrong order refused).

## Architecture accounting

- Cognition lines added: 306 (l2c_patch.zag operator section:
  select, stale-check, substitute, extend-from, deliver,
  pipeline; non-comment non-blank) + 25 prior-knowledge scaffold
  (l2c_mk_from_facts) + 26 audit helpers. Driver (197 lines) is
  harness, not cognition.
- 0 new edge types (14/15/16 reused with established semantics),
  0 new opcodes, 0 modes, 0 bridges, 0 handlers, 0 new semantic
  cases, 0 new node tags.
- Capability-source delta: the composition lives in the generic
  pipeline plus learned MAP state; no per-problem researcher
  choice in either firing (candidate order is node-id order,
  triggers are learner-owned checks).

## Build and artifact hashes

- l2c_full.zag:
  eddc6a3f8c3aa889db1baf843d861b50ab330679f827d7a6953e4b2e29a423af
  (cat of cc_base + un_patch + adapt_patch + extn_patch +
  l2c_patch + l2c_driver in build order)
- l2c_bin:
  864e6b087035d50b7c61d016e3c1f8ffde58ac737568dae7789c69ac57fd1438
  (pinned znc src/tools/toolchain/znc_linux_x86_64_abed8aa1,
  compile exit 0; only pre-existing A0102 warnings)
- runs: ebd37eae9e4e02e9df304c51ae2caee9307bac5f67ce70bdcf8f52e47327c88f x3

## Notes and follow-ups (not verdict changes)

- Two implementation bugs were fixed pre-verdict (out-buffer
  4-byte stride offsets; missing EXTN-STEP emits in the extend
  loop); both are researcher-side harness/emit issues, neither
  touches a frozen bar.
- PREREG_AMENDMENT1 corrected the hand-derived node ids: the
  killed fact's node slot is recycled by alloc_node, shifting
  post-kill ids down by one (m2=54 not 55). Pre-verdict,
  transparent, no bar weakened.
- The stale MAP m is intentionally not retired via the live flag
  (that would free its slot for reuse and corrupt provenance);
  it stays live-but-stale and is never reselected (q2 selects the
  exact-terminal composite). Its staleness is asserted white-box,
  not by retirement.
- Open: cross-domain multi-adaptation (e.g. interface-adapt +
  extend across the arithmetic/planning boundary), and
  substitute where the piece needs its own interface adaptation
  (the xdomain_l2_causal open item).
