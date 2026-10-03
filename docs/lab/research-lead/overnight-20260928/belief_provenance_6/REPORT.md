# REPORT: BP-6 (belief-layer open dynamics, continued)

Worker: BELIEF-PROVENANCE-6 subagent, 2026-10-03. Non-ledger
task (claim minting paused); nothing minted.
Branch: tnn-native-lab, local only, never pushed.
Lane: docs/lab/research-lead/overnight-20260928/belief_provenance_6/
Verdict: **BP-6-PASS** (all 5 preconditions, all 30 kill
bars, K-DET 3/3 byte-identical, K-HYG clean). Method: frozen
prereg (committed as eae389521 before any implementation),
BP-5's belief machinery reused verbatim plus zero new
learner functions, five world arms, in-driver bars.

## 0. What was built

`bp6_learner.zag` is BP-5's `bp5_learner.zag` copied
verbatim (SHA-256
2de20f5a0ff87bc45140a161548b613b008e9c2adabf4da3fdda6d6d46040c5e
on both files, `cmp` clean): the learner-owned u8 belief
table, R1-R7, eff(), b_retire, bp2_bar_after, the lg()
baseline. No redesign; the task's "build on BP-5" is
literal.

`bp6_driver.zag` is the whole lane: `bp6_absorb` (the BP-5
emergent-evidence absorption, renamed), the three
driver-side experimental combiner variants
`bp6_cmax`/`bp6_cavg`/`bp6_cwavg` (same traversal as
bp2_propagate, aggregation only; NOT belief-layer
changes), five world arms (BA/COMB/EV/CY5/NST), the
commitment bookkeeping for the bar loop, in-driver bars.

`bp6_full.zag` = `xf_block.zag` (patched block, verbatim,
SHA-256 172a2e7dbbaa4e60d662331965887327350068e0c13f25e438260ad08313c12a
re-verified before and after the build) + `bp6_learner.zag`
+ `bp6_driver.zag`. One `main`. Pinned znc by absolute path,
build exit 0 -> bp6_bin (412799 bytes); the A0102 warnings
are the benign ignored-return-value pattern pervasive in
the frozen block itself (same as BP-4/BP-5).

## 1. Kill-bar results

Preconditions (5/5 PASS): PC-BA-FORM (mA formed,
ext=self=2; mB=60), PC-COMB-FORM (t1 120/conf 3, t2
60/disc 2, w 70), PC-EV-FORM (m1 formed, ext=self=1;
m2=80), PC-CY5-FORM (all five 100), PC-NST-FORM (all
four 100).

BA (bar-adjustment trajectories), all PASS:
- K-BA-U1..U5: bp2_bar_after unit values 51/51/50/10/11:
  false positive raises, near-bar true positive holds,
  far-above-bar true positive lowers, floor at MIN_BAR,
  raise still works at the floor.
- K-BA-T1: R7({mA,mB},50)=mA; contradicting observe on
  fa2 -> block wrote 1 type-3 -> R3(mA): sup 80, disc=1;
  bar 50->51.
- K-BA-T2: R7({mA,mB},51)=mA; matching observe on fa1 ->
  1 type-7 -> R2(mA): sup 90; eff 80 < 102 -> bar stays
  51.
- K-BA-T3: two boost confirms -> sup 110;
  R7({mA,mB},51)=mA; matching observe -> R2: sup 120;
  eff-at-commit 110 >= 102 -> bar 51->50.
- K-BA-EXCL: R7({mC},51)=-3 while R7({mC},50)=mC
  (mC sup 50 via R5). The raised bar excludes a
  candidate the old bar admitted: the bar has teeth.

COMB (combiner alternatives), all PASS:
- K-COMB-MIN/MAX/AVG/WAVG: 60/120/90/94 on targets
  (120,60), exactly hand-derived (wavg: weights
  4,3 from conf+disc+1; 660/7=94).
- K-COMB-NOINV: min is the unique combiner with result
  <= every target's support (60<=60); max (120), avg
  (90), wavg (94) all exceed the weaker target's 60.
- K-COMB-SELDISC: R7({z,w},50) on the same structure:
  min selects w (60<70); max/avg/wavg select z
  (120/90/94>70). The combiner flips selection.

EV (eviction interaction), all PASS:
- K-EV-VICTIM: the block's own evict_node, with all
  other live nodes type-9 protected, returned m1; m1
  dead (36=0), m2 live.
- K-EV-TOMB: rec_evict pushed a live tag-3 tombstone
  (node 10) onto the hg(12) chain.
- K-EV-PERSIST: hasb[m1]==1, b_sup[m1]==100. H-persist
  holds; H-tombstone fails. The belief layer does not
  notice the eviction.
- K-EV-STALE: R7({m1,m2},50)==m1. The dead MAP is still
  selected: stale selection, the gap, measured.
- K-EV-LGSEL: bp2_lgsel({m1,m2})==m2. The liveness
  baseline skips the dead node: discriminating pair
  with STALE, showing R7 lacks a liveness gate.
- K-EV-R4: bp2_relicense on the evicted MAP: licensing
  edges died with the node, live=0, formed=2 ->
  b_sup=0 with a kind-3 reason-2 self-edge. The layer
  owns dormant detection machinery; nothing triggers
  it.

CY5 (5-cycle), all PASS:
- K-CY5-WEAK: z3=40 after 3x R3.
- K-CY5-1HOP: R6(z2)=40; z1,z5,z4 stay 100 (no
  cascade on a 5-cycle either).
- K-CY5-FULL: per-hop R6 around z1,z5,z4,z3: all 40.
- K-CY5-FIX: re-application: all still 40 (fixpoint,
  idempotent, no oscillation at 5 nodes).
- K-CY5-RAISE: 2x R2(z5) -> 80, R6(z4)=80. The R6
  snap-up (BP-5 C2) generalizes to the 5-cycle.

NST (nested cycles), all PASS:
- K-NST-1HOP: R6(zB)=min(100,60)=60 on the nested
  node; zA,zC untouched.
- K-NST-CONV: R6(zA),R6(zC),R6(zD): all 60. The
  triangle and the nested 2-cycle converge to the
  shared min.
- K-NST-Z0B: 3x R3(zD) -> 0; R6(zB)=0 with reason-2
  retirement.
- K-NST-ZALL: R6(zA),R6(zC),R6(zD): all 0, reason-2
  edges on zA,zC,zD. 0 absorbs the nested component.

K-DET: 3/3 runs byte-identical, SHA-256
71acb6ed896f967bf2c0ac17903851d2af9d0cdc9d04d80d4958873419b8f179.
K-HYG: pure Zag under safebin (`which python3`/`which
python` empty at build and run); zero em/en dash bytes
in all authored files and run outputs (the only dash
bytes in the lane are znc's own A0102 warning text
inside the machine-generated bp6_compile.txt,
disclosed); 0 new edge types (1/3/7/9/14 all
pre-existing in the block: 7 block-written evidence,
9 block-native protection, 14 propagation); 0 new node
types (tags 1/3/20 pre-existing); 0 modes, 0 bridges,
0 handlers; xf_block.zag hash unchanged;
bp6_learner.zag byte-identical to bp5_learner.zag;
opaque identifiers. BP6-SUMMARY 35/35 in-driver; 37/37
with K-DET/K-HYG.

## 2. What this means

The bar is learnable. bp2_bar_after sat dormant since
BP-2; closed through R7 commitments and emergent world
outcomes it produces exactly the policy its comment
promises: raise after false positives, lower after easy
true positives, floor at 10, and the moving bar changes
real selection outcomes (K-BA-EXCL). No new machinery
was needed: the rule was already in the belief layer.

Min is the conservative combiner, now with evidence.
On one fixed structure the four combiners give four
different values (60/120/90/94) and two different
selection outcomes. The no-invention criterion
discriminates them cleanly: only min never assigns the
composite support exceeding a component's support
without new evidence. Since R2/R3 are the belief
layer's only evidence-driven support moves, a combiner
is not evidence, so max/avg/wavg manufacture support
the learner never earned. Min stays the frozen R6
combiner; the comparison is the evidence for keeping
it. The disjunctive (OR-composite) reading, where max
would be principled, stays open: the layer does not
represent AND vs OR.

Eviction is currently invisible to the belief layer,
and that is now measured rather than assumed. The
record persists (H-persist), R7 has no liveness gate
so it stale-selects the dead MAP while the baseline
skips it, and R4 already implements the detection that
would retire it (reason 2, provenance-death) if
anything called it. This is the same pattern as
bp2_bar_after in BP-2: the machinery exists, the
trigger does not. Whether eviction should tombstone
(I1-style), retire via R4, or persist deliberately is
a design decision for the parent, with the
measurements above as the evidence base.

Cycles generalize. The BP-5 2-cycle result (monotone
convergence to the min, fixpoint, no oscillation,
0-absorption with retirement, R6 snap-up) holds at 5
nodes and under nesting (triangle + nested 2-cycle):
per-hop R6 never cascades, re-application is
idempotent, 0 absorbs the whole strongly-connected
component. The open question from BP-5 ("does the min
behavior generalize beyond the 2-cycle") is answered
yes for the tested shapes.

## 3. One-system accounting

New learner machinery this lane: ZERO functions. The
bar loop triggers existing dormant code; the combiner
variants are driver-side experimental code explicitly
not adopted into the belief layer; eviction and cycles
use frozen R1-R7 and block ops. 0 new edge types, 0 new
node types, 0 modes, 0 bridges, 0 handlers, 0 semantic
cases. Beliefs remain learner-state records, not a
subsystem.

## 4. What was tested vs what was reasoned

Tested (frozen, this lane, PASS): the full
bp2_bar_after policy (5 unit branches) plus a
three-step closed-loop trajectory with exact bar
values (50->51->51->50) and exact support values
(100->80->90->110->120), all outcomes from
block-written evidence edges; four combiner values
(60/120/90/94) with the no-invention discriminator
and selection flips; eviction victim determinism via
block-native protection, record persistence, the
R7-stale vs baseline-skip pair, R4 retirement on the
evicted node; 5-cycle per-hop convergence (40), no
cascade, fixpoint idempotence, snap-up (80); nested
cycle convergence (60) and 0-absorption with
retirements.

Reasoned: that no-invention is the right criterion for
choosing the combiner (it follows from the belief
layer's evidential semantics, but the disjunctive
reading is unrepresented); that eviction should get a
learner-owned trigger (persist vs tombstone vs R4
retire is a design choice, measured but not decided
here); that cycle convergence generalizes beyond the
tested shapes (monotonicity of min argues it does).

## 5. Open questions (not claimed)

A learner-owned eviction-sync trigger (which of
persist/tombstone/R4-retire the architecture should
adopt); the disjunctive combiner reading; d_self
dynamics; per-belief bars; multi-channel absorption;
cycles larger than 5 or with heterogeneous edge
structure; whether the bar policy's constants (INC 1,
floor 10, 2x threshold) are the right meta-parameters.

## 6. Notes for the parent

- No ledger entry: non-ledger task, nothing minted.
- No push: commits local on tnn-native-lab only,
  explicit pathspecs. This report is committed with the
  lane's implementation artifacts.
- DESIGN.md is untouched; this lane tests it and does
  not reinterpret it. BP-2/BP-3/BP-4/BP-5 REPORT.md
  files are untouched. The 7 sealed predictions stay
  sealed; this lane adds open-dynamics evidence only.
- Suggested next from the remaining open list:
  eviction-sync design decision (needs a parent-level
  ruling: persist vs tombstone vs R4-retire, since it
  changes belief lifecycle semantics); combiner
  constants are frozen (min stays); bar-policy
  meta-parameter sensitivity; d_self dynamics;
  per-belief bars.
- Style: no em/en dashes in authored files (hyphens
  only), opaque identifiers throughout.
