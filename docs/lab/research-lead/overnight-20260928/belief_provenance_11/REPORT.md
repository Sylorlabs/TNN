# REPORT: BP-11 (cross-belief interaction beyond shared-fact scoping)

Worker: BELIEF-PROVENANCE-11 subagent, 2026-10-03. Non-ledger
task (claim minting paused); nothing minted.
Branch: lane-bp11-20261003 (forked from tnn-native-lab tip
4aa6b2680); lands on tnn-native-lab by fast-forward.
Local only, never pushed.
Lane: docs/lab/research-lead/overnight-20260928/belief_provenance_11/
Verdict: **BP-11-PASS** (3 preconditions, all 12 kill
bars, K-DET 3/3 byte-identical, K-HYG clean). Method:
frozen prereg (committed as e83e6ff98 before any
implementation), BP-10's belief machinery reused
verbatim, zero new learner machinery, three world arms,
in-driver bars. First implementation run went 15/15:
no amendment round was needed. PREREG Section 5b is
empty.

## 0. What was built

`bp11_learner.zag` is BP-10's `bp10_learner.zag` copied
verbatim (SHA-256
2de20f5a0ff87bc45140a161548b613b008e9c2adabf4da3fdda6d6d46040c5e
on both files): the learner-owned u8 belief table,
R1-R7, eff(), b_retire, bp2_bar_after. No redesign.

`bp11_driver.zag` is the whole lane: three world arms
(PROP/ROUTE/NULL), bp11_absorb (the BP-10 absorb renamed,
identical body), the tally helpers bp11_ck/bp11_bar,
bp11_selfcnt, bp11_liclive (thin wrapper over frozen
bp2_lic_live), world builders, in-driver bars. The
forgery actions (link_edge writes of type-7/type-3
edges) and the driver-written type-14 edges in PROP are
adversary/test-setup actions in the driver, NOT
belief-layer changes: the threat model is an adversary
with the same write access as the world harness, and
the type-14 edges are test setup for the frozen R6
rule exactly as in BP-9 CHAIN. The direct driver calls
to frozen learner functions (bp2_disconfirm,
bp2_confirm, bp2_retire, bp2_form, bp2_propagate,
bp2_kill_one_prov, bp2_relicense, bp2_select, bp2_eff,
bp2_lic_live) are disclosed test actions invoking
frozen operators; they add no rules.

`bp11_full.zag` = `xf_block.zag` (patched block, verbatim,
SHA-256 172a2e7dbbaa4e60d662331965887327350068e0c13f25e438260ad08313c12a
re-verified before and after the build) +
`bp11_learner.zag` + `bp11_driver.zag` (3233 lines).
One `main`. Pinned znc by absolute path, build exit 0
-> bp11_bin (400718 bytes); the A0102 warnings are the
benign ignored-return-value pattern pervasive in the
frozen block itself (same as BP-4 through BP-10).

## 1. Kill-bar results

Preconditions (3/3 PASS): PC-PROP-FORM (z1/m1/m2/m3
sup 100; m1/m2/m3 conf 1, ext 1, formed 1; hasb all
1), PC-ROUTE-FORM (mA/mB/mC sup 100, conf 1, ext 1,
formed 1), PC-NULL-FORM (mD/mE/mF/mG sup 100, conf 1,
ext 1, formed 1).

PROP (R6 coupling with no shared fact and no shared
(s,r)), all PASS:
- K-PROP-COUPLE: 3x R3 on m2 (40/0/3), propagate z1:
  rp==40, sup[z1]==40, conf[z1]==1, disc[z1]==0,
  rev[z1]==0, no k3. A belief's support moves another
  belief's record with no shared fact between them:
  the type-14 structural edge is a genuine
  cross-belief interaction channel beyond BP-9's
  shared-fact scoping.
- K-PROP-ASYM: after the propagation, m1 still
  100/1/0/0 and m2 still 40/0/3/0. Propagation writes
  the composite only; targets are untouched. The
  coupling is asymmetric: target->composite, never
  back.
- K-PROP-SCOPE: 2x R2 on the unlinked m3 (140/3),
  re-propagate z1: rp==40, sup[z1]==40,
  sup[m3]==140. m3's support change does not reach
  z1, and z1's propagation does not touch m3. The
  propagation blast radius is exactly the type-14
  adjacency: radius 1, no further.
- K-PROP-NOBACK: propagate(m1) returns 255, m1 still
  100/1/0/0. m1 has no type-14 out-edges, so nothing
  is read and nothing written. The z1->m1 edge
  couples z1 to m1, never m1 to z1: direction is
  fixed by edge direction, and the 40 sitting on z1
  does not flow back.
- K-PROP-TRACK: 3x R2 on m2 (100/3/0), propagate
  z1: rp==100, sup[z1]==100. The composite tracks
  the min live target in both directions, and only
  its targets.

ROUTE (block bid-routing theft: shared (s,r), no
shared fact node), all PASS:
- K-ROUTE-THEFT: fB's bid inflated to 4 (licensing
  type-1 + 3 forged type-7s) vs fA's 1; a genuine
  ev_observe(921,91,10) matching mA's fact value
  returns 0, writes its type-3 on fB, and fA sees
  zero new type-7/type-3 edges: mA's absorb fires
  no rule, mA stays 100/1/0; mB's absorb sees the
  one new type-3: one R3, 110->90, disc 1, conf 0.
  mB's bid dominance converts mA's confirming
  evidence into mB's disconfirmation, with no
  shared fact between the beliefs. The forged
  type-7s (adversary action on mB's fact) redirect
  mA's genuine evidence: forgery on one belief's
  fact reaches across to another belief's evidence
  stream.
- K-ROUTE-CONTROL: separate world, mA2 alone:
  ev_observe(921,91,10) returns 1, one type-7 on
  fA2, mA2 -> 110/2/0. Without mB's bid dominance
  the observation reaches mA's fact. The theft is
  caused by mB's presence, not by the observation.
- K-ROUTE-BOUND: in the same world after the theft,
  ev_observe(941,91,10) returns 1, mC -> 110/2/0,
  mA still 100, mB still 90. The disjoint-(s,r)
  belief is routing-isolated: bid dominance over
  (921,91) does not leak into (941,91). The routing
  channel is (s,r)-scoped.

NULL (no fourth channel: disjoint facts, no type-14
path, disjoint (s,r)), all PASS:
- K-NULL-CONFIRM: 3 forged type-3s on mE's fact + 1
  forged type-7 on mD's fact; mD's absorb sees
  n7==1 -> 110/2/0, mE's absorb sees n3==3 ->
  one R3 -> 80/0/1. Each absorb counts only its
  own fact's self-edges; mE's contradicts do not
  leak into mD's counts.
- K-NULL-RETIRE: retire mE (reason 2, sup 0);
  genuine ev_observe(951,91,10) returns 1, one
  type-7 on fD, mD -> 120/3/0; select([mD,mE],50)
  -> mD. Retirement of mE gates nothing for mD:
  mD keeps absorbing genuine evidence and wins
  selection on eff (120 vs 0).
- K-NULL-PROVKILL: bp2_kill_one_prov(mE) kills fE
  (returns fE); mD's live licensing stays 1,
  b_ext[mD]==1, sup[mD]==120; relicense retires mE
  on reason 2. Provenance death is per-belief: mE's
  fact death does not touch mD's licensing counts
  or support.
- K-NULL-SELECT: select([mF,mG],50) -> -3 on the
  100/100 tie; one R2 on mG (120/2/0) flips the
  outcome to mG while mF stays 100/1/0 and
  eff(mF)==100. Selection couples outcomes at the
  call site; records stay independent.

K-DET: 3/3 runs byte-identical, SHA-256
bf1a0bfadbd5f9ab622c5fa43b83eaa08c3ea2ab9e8d1a725edaf443f81dd020.
K-HYG: pure Zag under safebin (`which python3` /
`which python` empty at build and run); zero
em/en dash bytes in authored lane files and run
outputs (the 161 matches in bp11_compile.txt are the
znc compiler's own warning prose, "ignored return
value of `link_edge` - result is discarded", not
authored text); 0 new edge types (1/3/7/14 all
pre-existing; kind-3 self-edges pre-exist via
bp2_retire); 0 new node types (tags 1/3/20
pre-existing); 0 modes, 0 bridges, 0 handlers,
0 semantic cases; block SHA-256 unchanged;
bp11_learner.zag byte-identical to bp10_learner.zag;
opaque identifiers. F-VOID not triggered.
BP11-SUMMARY 15/15 in-driver; 17/17 with K-DET/K-HYG.

## 2. What this means: the scope of cross-belief interaction

H-BP11 is confirmed as stated: cross-belief
interaction in the frozen layer plus the frozen
block is exactly scoped to three channels, and no
fourth channel appeared in any arm.

1. **Shared-fact evidence edges** (BP-9): evidence
   non-rivalrous across beliefs sharing a fact;
   forged-edge blast radius 2.
2. **Type-14 structural edges via R6** (this lane,
   PROP): directed, edge-scoped, asymmetric
   (target->composite only), blast radius exactly
   the type-14 adjacency, tracks the min live
   target both ways. Two beliefs sharing no fact
   and no (s,r) still interact through this
   channel, but only along written edges and only
   downstream.
3. **Shared-(s,r) bid routing at the block** (this
   lane, ROUTE): beliefs sharing no fact node but
   sharing the (s,r) namespace interact through
   activate-by-bid. The measured effect is strong:
   the higher-bid belief not only starves the
   lower-bid belief's fact of observations, it
   converts the lower-bid belief's confirming
   evidence into its own disconfirmation. And the
   adversary angle is new: forged type-7s on one
   belief's fact inflate its bid and thereby
   redirect ANOTHER belief's genuine evidence
   stream. The channel is (s,r)-scoped: disjoint
   (s,r) beliefs in the same world are isolated.

Everything else tested is null (NULL arm): absorb
counts only the named fact's self-edges, so forged
contradicts on one belief's fact never leak into
another's counts; retirement is per-belief and
gates nothing for others; provenance death
(kill_one_prov + relicense) is per-belief;
eff() is a pure function of one belief's own
fields, so selection is the only cross-belief
coupling in R7 and it lives at the call site, not
in the records.

Two honest boundaries on the claim. First, the
ROUTE channel is a block behavior (activate-by-bid),
not a belief-layer rule: the belief layer itself
has no cross-belief term outside R6. The layer is
provably interaction-free beyond shared facts and
type-14 edges; the block adds the (s,r) routing
channel on top. Second, "no fourth channel" is
measured over the exercised operations
(R2/R3/retire/relicense/kill_one_prov/propagate/
select/absorb/ev_observe), not proved over all
possible block paths; eviction-pressure coupling
(global arena contention) was explicitly out of
scope for this lane.

## 3. One-system accounting

New learner machinery this lane: ZERO functions.
bp11_absorb is the BP-10 absorb renamed (identical
body); bp11_ck/bp11_bar/bp11_selfcnt/bp11_liclive
are driver-side test-harness code. The forgery
actions and the PROP type-14 edges are
adversary/test-setup actions in the driver,
explicitly not belief-layer changes. Direct driver
calls to frozen learner functions are disclosed test
actions invoking frozen operators. 0 new edge types,
0 new node types, 0 modes, 0 bridges, 0 handlers,
0 semantic cases. Beliefs remain learner-state
records, not a subsystem.

## 4. What was tested vs what was reasoned

Tested (frozen, this lane, PASS): propagate z1 over
type-14 targets m1(100)/m2(40) -> 40 with targets
untouched; unlinked m3 raised to 140, re-propagate
-> 40, m3 keeps 140; propagate(m1) -> 255, m1
untouched; m2 raised to 100, propagate -> 100;
genuine observation matching mA's fact routed to
the higher-bid fB (ret 0), fA zero new edges, mA
unchanged 100/1/0, mB 90/0/1; control world without
mB: ret 1, mA2 110/2/0; disjoint-(s,r) mC in the
theft world: ret 1, 110/2/0, mA/mB untouched;
forged 3x type-3 on mE's fact + 1x type-7 on mD's
fact absorbed independently (110/2/0 and 80/0/1);
retired mE does not gate mD's genuine match
(120/3/0) or selection (mD wins); killing mE's
fact leaves mD's licensing (live 1, b_ext 1, sup
120) intact; select([mF,mG]) -3 on tie, mG after
one R2, mF record and eff unchanged.

Reasoned: that the three channels exhaust
cross-belief interaction (follows from the NULL
bars passing across the exercised operations, not
from exhaustive proof); that the ROUTE channel is
a block property rather than a belief-layer rule
(follows from the layer's per-belief field writes,
S1/S2, plus the measured routing); that forged
type-7 bid inflation is the adversary's lever on
the routing channel (follows from B-BP11c plus
the measured theft, not from a separate forgery
red team on bids).

## 5. Open questions (not claimed)

Whether the block's bid routing SHOULD be
(s,r)-scoped this way (a higher-bid belief eating
another belief's confirming evidence and turning it
into its own disconfirmation is a real hazard, and
the forged-bid-inflation lever makes it
adversarially reachable); whether R6 propagation
should be visible to the provenance record (BP-9
CHAIN showed it is not; this lane shows the
channel is at least tightly scoped); whether
eviction-pressure coupling exists between beliefs
at arena capacity (not tested here); whether any
belief-layer path outside the exercised set
couples beliefs (not proved). All four are design
questions in the same class as #16/#17/#18, NOT
presupposed here.

## 6. Notes for the parent

- No ledger entry: non-ledger task, nothing minted.
- No push: commits local on lane-bp11-20261003, to be
  fast-forwarded onto tnn-native-lab (additive-only,
  explicit pathspecs). This report is committed with
  the lane's implementation artifacts.
- DESIGN.md is untouched; this lane tests it and
  does not reinterpret it. BP-2 through BP-10
  REPORT.md files are untouched. The 7 sealed
  predictions stay sealed.
- No amendment round: the first implementation run
  went 15/15 against the frozen prereg, so PREREG
  Section 5b is empty.
- Suggested nexts: the block bid-routing hazard
  (genuine evidence converted to another belief's
  disconfirmation; forged bid inflation as the
  adversary lever) as a follow-up surface; whether
  R6 propagation should write a trace (same
  design-decision status as BP-9's propagation
  finding); eviction-pressure coupling at arena
  capacity as the remaining untested interaction
  surface.
- Style: no em/en dashes in authored files
  (hyphens only), opaque identifiers throughout.
