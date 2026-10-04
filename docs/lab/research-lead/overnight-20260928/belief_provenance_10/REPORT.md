# REPORT: BP-10 (belief revision under contradiction)

Worker: BELIEF-PROVENANCE-10 subagent, 2026-10-03. Non-ledger
task (claim minting paused); nothing minted.
Branch: lane-bp10-20261003 (forked from tnn-native-lab tip
ec3d8561c); lands on tnn-native-lab by fast-forward.
Local only, never pushed.
Lane: docs/lab/research-lead/overnight-20260928/belief_provenance_10/
Verdict: **BP-10-PASS** (4 preconditions, all 15 kill
bars, K-DET 3/3 byte-identical, K-HYG clean). Method:
frozen prereg (committed as 3d3c450ca before any
implementation), BP-9's belief machinery reused
verbatim, zero new learner machinery, four world arms,
in-driver bars. First implementation run went 19/19:
no amendment round was needed. One mechanistic
refinement was recorded in PREREG Section 5b (no bar
or number changed).

## 0. What was built

`bp10_learner.zag` is BP-9's `bp9_learner.zag` copied
verbatim (SHA-256
2de20f5a0ff87bc45140a161548b613b008e9c2adabf4da3fdda6d6d46040c5e
on both files): the learner-owned u8 belief table,
R1-R7, eff(), b_retire, bp2_bar_after. No redesign.

`bp10_driver.zag` is the whole lane: four world arms
(CON/REC/REV/AMB), bp10_absorb (the BP-9 absorb renamed,
identical body), the tally helpers bp10_ck/bp10_bar,
bp10_selfcnt, world builders, in-driver bars. The
forgery actions (link_edge writes of type-7/type-3
edges) are adversary actions in the driver, NOT
belief-layer changes: the threat model is an adversary
with the same write access as the world harness. The
direct driver calls to frozen learner functions
(bp2_disconfirm, bp2_confirm, bp2_revise, bp2_retire,
bp2_form) are disclosed test actions invoking frozen
operators; they add no rules.

`bp10_full.zag` = `xf_block.zag` (patched block, verbatim,
SHA-256 172a2e7dbbaa4e60d662331965887327350068e0c13f25e438260ad08313c12a
re-verified before and after the build) +
`bp10_learner.zag` + `bp10_driver.zag`. One `main`.
Pinned znc by absolute path, build exit 0 -> bp10_bin
(417194 bytes); the A0102 warnings (322) are the benign
ignored-return-value pattern pervasive in the frozen
block itself (same as BP-4 through BP-9).

## 1. Kill-bar results

Preconditions (4/4 PASS): PC-CON-FORM (mA1..mA4 sup
100, conf 1, ext 1, formed 1), PC-REC-FORM (mB1/mB2/mB5
ext 1; mB3/mB4 ext 2, formed 2), PC-REV-FORM
(mC1..mC3 ext 1; mC4 ext 2, formed 2), PC-AMB-FORM
(zD1/zD2 sup 100, conf 1).

CON (what contradiction does), all PASS:
- K-CON-GENUINE: one genuine type-3 -> n3==1, sup 80,
  disc 1, conf 0. The belief-layer contradiction
  operation is one R3: support -20, disc +1, conf
  zeroed. Nothing structural happens.
- K-CON-FORGEIDENT: one forged type-3 -> n3==1, sup
  80, disc 1, conf 0, record byte-equal to the genuine
  case on (sup,conf,disc,rev). The record cannot
  distinguish forged from genuine contradiction.
- K-CON-NORETIRE: five forged R3s -> sup 0, disc 5,
  conf 0, hasb==1, no kind-3 edge. Contradiction,
  even driven to zero support, NEVER retires the
  belief: no rule maps contradiction to retirement
  (retire is called only by R4, R6, or explicitly).
  The belief sits at support 0 still fully "live".
- K-CON-SAT: three forged type-3s, one absorb ->
  n3==3 but sup 80, disc 1, conf 0. One R3 per
  absorb: the contradict-side twin of BP-8 K-MCH-SAT.
  The record hides the true forged multiplicity.

REC (recovery: genuine vs forged), all PASS:
- K-REC-GENBLOCKED: genuine contradict (80/0/1),
  then a genuine match attempt on the same fact:
  absorb sees n7==0 and n3==0, record unchanged
  (80/0/1). The block routes the post-contradict
  observation to the highest-bid node (here the
  internal promote_graph node, via the match path,
  ret 1; in the no-promote probe it took the
  contradict path on the newest node, ret 0). Either
  way the ORIGINAL fact is frozen: genuine same-fact
  recovery through the block is impossible.
  (Mechanistic refinement vs the prereg gloss
  recorded in PREREG 5b; every barred number held.)
- K-REC-FORGED: genuine contradict (80/0/1), then a
  FORGED type-7 written directly on the burned fact:
  n7==1, sup 90, conf 1, disc 0. The forged edge
  bypasses block routing; the layer applies R2
  without question. On a burned fact the ONLY
  same-fact recovery path is forged.
- K-REC-IDENT-C / K-REC-IDENT-R: genuine-contradict
  belief (mB3) and forged-contradict belief (mB4),
  each recovered by one genuine match on a fresh
  licensed fact: post-contradict records identical
  (80/0/1 both), post-recovery records identical
  (90/1/0 both). Through a full contradict-recover
  cycle the learner cannot distinguish genuine from
  forged contradiction, even in recovery.
- K-REC-FORGEBURN: two forged type-3s (one R3 by
  saturation: 80/0/1), then a genuine match attempt:
  ret==1 BUT absorb sees n7==0, n3==0, record stays
  80/0/1. The forged type-3s drop the fact's bid by
  2 (bid subtracts evcount(type-3)); the block routes
  the genuine match to the internal node. Forged
  type-3s burn the fact's routing exactly like
  genuine ones: the BLOCK is provenance-blind too.

REV (revision operation vs retire+create), all PASS:
- K-REV-OP: contradict (80/0/1), then driver-invoked
  bp2_revise: sup 40, rev 1, conf 0, disc 0, no
  kind-3 edge, hasb intact. The R5 operator works as
  specified: halves support, increments b_rev,
  preserves belief identity.
- K-RETREFORM: contradict, retire reason 2, reform:
  sup 100, conf 1, disc 0, rev 0, reason-2 edge
  persists. Retire+reform resets the table but the
  retire record survives the reform.
- K-REV-DISTINCT: the two end states differ on every
  diagnostic field (40/rev=1/no-k3 vs
  100/rev=0/k3r2). The record CAN distinguish a
  revision from retire+reform: if a revision rule
  existed, its trace would be visible. It is not.
- K-REV-UNREACH: after a full evidence cycle (form,
  R2, R3, retire, reform) with no driver-called
  revise, b_rev==0. Source audit (grep over frozen
  learner, block, and BP-9 driver) finds ZERO callers
  of bp2_revise. The revision operator is dead
  machinery: no revision RULE exists in the frozen
  layer.
- K-RET-NOGATE: contradict (80/0/1), retire reason 2
  (sup 0, k3r2), then a genuine match on the fresh
  fact: sup 10, conf 1, disc 0, k3r2 STILL 1.
  bp2_confirm checks no retirement state: retirement
  does not gate evidence absorption. A retired
  belief keeps revising while its retire record
  persists. Retire is record-keeping, not a learning
  gate.

AMB (revision-history erasure), PASS:
- K-REV-AMBIG: R3,R2,R3,R2 vs R2,R3,R3,R2 give the
  identical record (sup 80, conf 1, disc 0, rev 0).
  R2 zeroes disc, R3 zeroes conf, so only the net
  support change and the trailing run survive. The
  provenance record erases WHEN the contradiction
  happened: "contradicted early then recovered" is
  record-identical to "confirmed, contradicted twice,
  then recovered".

K-DET: 3/3 runs byte-identical, SHA-256
5c682624b9e8cca5cdd7bd70cea666a8241f3a4b17e0938bd2abd565cc018419.
K-HYG: pure Zag under safebin (`which python3` /
`which python` empty at build and run); zero em/en
dash bytes in all authored lane files and run
outputs (the 161 matches in bp10_compile.txt are the
znc compiler's own warning prose, "ignored return
value of `link_edge` - result is discarded", not
authored text); 0 new edge types (only type-7/type-3
writes, both pre-existing); 0 new node types (tags
1/3/20 pre-existing); 0 modes, 0 bridges, 0 handlers,
0 semantic cases; block SHA-256 unchanged;
bp10_learner.zag byte-identical to bp9_learner.zag;
opaque identifiers. F-VOID not triggered.
BP10-SUMMARY 19/19 in-driver; 21/21 with K-DET/K-HYG.

## 2. What this means: revision vs retirement, honestly

The frozen layer has FOUR things that could be called
"revision", and the experiment separates them:

1. **R2/R3 adjustment is the ONLY evidence-driven
   revision.** Contradiction = one R3: support -20,
   disc +1, conf zeroed. Nothing structural happens:
   no new belief, no retirement, no trace beyond the
   counters. Recovery = R2, which zeroes disc,
   erasing the contradiction history (K-REV-AMBIG).
2. **R5 (bp2_revise) is a revision OPERATOR with no
   revision RULE.** It works when invoked (K-REV-OP)
   and its record is distinguishable from
   retire+reform (K-REV-DISTINCT), but zero frozen
   code paths call it (K-REV-UNREACH, S1). It is dead
   machinery.
3. **Retirement is never triggered by contradiction**
   (K-CON-NORETIRE) **and does not gate learning**
   (K-RET-NOGATE). It is an explicit record-keeping
   act: write the reason edge, zero support. A
   retired belief keeps absorbing evidence.
4. **Retire+reform is the only "start over"**, and it
   does not erase the retire record (K-RETREFORM).

So the honest answer to "revision mechanism or just
retirement": NEITHER, as mechanisms. The layer has
adjustment (the sole evidence-driven update),
retirement (an explicit, non-gating, never
contradiction-triggered act), and a dead revision
operator. There is no contradiction-triggered
revision rule and no contradiction-triggered
retirement. "Belief revision under contradiction"
in the current frozen design is exactly one R3
decrement, and the provenance record of the revision
is lossy by construction.

On genuine vs forged: the belief layer cannot
distinguish them at any point, including through
recovery (K-CON-FORGEIDENT, K-REC-IDENT-C/R). The
block cannot either: its bid penalty counts forged
type-3s exactly like genuine ones (K-REC-FORGEBURN).
The one asymmetry found is structural, not
provenance-based: on a burned fact, genuine evidence
is routed away by the block while forged edges are
written directly, so the only same-fact recovery
path is forged (K-REC-GENBLOCKED vs K-REC-FORGED).
The layer applies that forged recovery as a routine
R2.

## 3. One-system accounting

New learner machinery this lane: ZERO functions.
bp10_absorb is the BP-9 absorb renamed (identical
body); bp10_ck/bp10_bar/bp10_selfcnt are driver-side
test-harness code. The forgery actions are adversary
actions in the driver, explicitly not belief-layer
changes. Direct driver calls to frozen learner
functions are disclosed test actions invoking frozen
operators. 0 new edge types, 0 new node types, 0
modes, 0 bridges, 0 handlers, 0 semantic cases.
Beliefs remain learner-state records, not a
subsystem.

## 4. What was tested vs what was reasoned

Tested (frozen, this lane, PASS): genuine contradict
-> 80/0/1 (n3==1); forged contradict ->
record-identical 80/0/1; five contradicts -> 0/0/5
with hasb intact and no retire edge; three forged
type-3s + one absorb -> one R3 (80/0/1, n3==3);
genuine match attempt on burned fact -> zero new
edges, record frozen at 80/0/1; forged match on
burned fact -> 90/1/0; genuine vs forged
contradict+recover cycles -> identical records at
both checkpoints (80/0/1, 90/1/0); forged type-3s
burn block routing (ret 1, zero new edges on the
fact); driver-invoked bp2_revise -> 40/rev=1/no-k3;
retire+reform -> 100/1/0/rev=0/k3r2 persists; full
evidence cycle with no revise call -> b_rev==0;
retired belief + genuine match -> 10/1/0 with k3r2
intact; R3,R2,R3,R2 vs R2,R3,R3,R2 -> identical
80/1/0/0.

Reasoned: that no revision rule exists (follows from
the zero-caller source audit plus the b_rev==0
measurement, not from the measurement alone); that
"revision under contradiction" is exactly R3 (follows
from the absence of any other contradiction-triggered
path in the frozen code, now measured at the record
level); that the block's routing provenance-blindness
follows from the bid formula (read from source,
measured at P-BP10g); that a record-only auditor
cannot recover contradiction timing (follows from
the measured record equivalence, not from a built
auditor).

## 5. Open questions (not claimed)

Whether a revision RULE should exist (R5 is dead
machinery; wiring it to a trigger would be new
learner machinery, a design decision in the same
class as #16/#17/#18, NOT presupposed here);
whether retirement SHOULD gate learning or be
triggered by contradiction (measured: neither);
whether the block's bid penalty should be
provenance-sensitive (measured provenance-blind);
whether R6 should write revision traces (same
design-decision status as BP-9's propagation
finding). The remaining untested task option is
option 3: cross-belief interaction beyond the
shared-fact scoping measured in BP-9.

## 6. Notes for the parent

- No ledger entry: non-ledger task, nothing minted.
- No push: commits local on lane-bp10-20261003, to be
  fast-forwarded onto tnn-native-lab (additive-only,
  explicit pathspecs). This report is committed with
  the lane's implementation artifacts.
- DESIGN.md is untouched; this lane tests it and
  does not reinterpret it. BP-2 through BP-9
  REPORT.md files are untouched. The 7 sealed
  predictions stay sealed.
- No amendment round: the first implementation run
  went 19/19 against the frozen prereg, so PREREG
  Section 5b holds only the R1 mechanistic
  refinement (no bar or number changed).
- Suggested nexts: the remaining open task option
  (cross-belief interaction beyond shared-fact
  scoping); whether R5 should ever be wired to a
  rule (design decision, offered not presupposed);
  the block bid-penalty provenance-blindness as a
  possible follow-up surface.
- Style: no em/en dashes in authored files
  (hyphens only), opaque identifiers throughout.
