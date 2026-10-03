# REPORT: BP-9 (provenance chain integrity under adversarial corruption)

Worker: BELIEF-PROVENANCE-9 subagent, 2026-10-03. Non-ledger
task (claim minting paused); nothing minted.
Branch: tnn-native-lab, local only, never pushed.
Lane: docs/lab/research-lead/overnight-20260928/belief_provenance_9/
Verdict: **BP-9-PASS** (2 preconditions, all 15 kill
bars, K-DET 3/3 byte-identical, K-HYG clean). Method:
frozen prereg (committed as 0742f9cea before any
implementation), BP-8's belief machinery reused
verbatim, zero new learner machinery, two world arms,
in-driver bars. First implementation run went 17/17:
no amendment round was needed.

## 0. What was built

`bp9_learner.zag` is BP-8's `bp8_learner.zag` copied
verbatim (SHA-256
2de20f5a0ff87bc45140a161548b613b008e9c2adabf4da3fdda6d6d46040c5e
on both files, `cmp` clean): the learner-owned u8 belief
table, R1-R7, eff(), b_retire, bp2_bar_after. No redesign.

`bp9_driver.zag` is the whole lane: two world arms
(FORGE/CHAIN), bp9_absorb (the BP-8 absorb renamed,
identical body), the tally helpers bp9_ck/bp9_bar,
bp9_selfcnt, bp9_allsup, bp9_liclive (thin wrapper
over frozen bp2_lic_live), world builders, in-driver
bars. The forgery actions (link_edge writes of
type-7/type-3/kind-3 edges, direct bt[] writes) are
adversary actions in the driver, NOT belief-layer
changes: the threat model is an adversary with the
same write access as the world harness.

`bp9_full.zag` = `xf_block.zag` (patched block, verbatim,
SHA-256 172a2e7dbbaa4e60d662331965887327350068e0c13f25e438260ad08313c12a
re-verified before and after the build) + `bp9_learner.zag`
+ `bp9_driver.zag`. One `main`. Pinned znc by absolute path,
build exit 0 -> bp9_bin (383428 bytes); the A0102 warnings
(322) are the benign ignored-return-value pattern
pervasive in the frozen block itself (same as BP-4
through BP-8).

## 1. Kill-bar results

Preconditions (2/2 PASS): PC-FORGE-FORM (all six
beliefs sup 100, conf 1, ext 1, formed 1),
PC-CHAIN-FORM (z1/z2 sup 100; mE sup 100, ext 1,
formed 1).

FORGE (adversarial edge forgery), all PASS:
- K-FORGE-MATCH: forged type-7 on mA's fact:
  n7==1, sup 110, conf 2. Record-identical to a
  genuine single match: the forgery is
  undetectable from the record.
- K-FORGE-DISC: forged type-3 on mB's fact:
  n3==1, sup 80, disc 1, conf 0.
  Record-identical to a genuine block-mediated
  contradict from formation.
- K-FORGE-ORD: genuine contradict absorbed
  (80/0/1), then a FORGED type-7 on the same
  contradicted fact: n7==1, sup 90, conf 1,
  disc 0. The block drops genuine post-contradict
  matches (BP-7 probe, BP-8 K-MCH-ORD n7==0);
  the forged edge bypasses the one-shot
  protection. The 90/1/0 record is unreachable
  by genuine ev_observe paths (match-then-
  contradict gives 90/0/1; contradict-then-match
  is dropped), so the forged edge is the unique
  producer of this record state among the tested
  shapes.
- K-FORGE-SAT: three forged type-7s: n7==3 but
  sup 110, conf 2. Per-channel single-application
  saturation caps per-absorb forgery impact at
  one R2, exactly as with genuine multiplicity
  (BP-8 K-MCH-SAT): the record hides the true
  forged multiplicity.
- K-FORGE-REPLAY: absorb re-run with stale
  watermarks: n7==3 again, sup 120, conf 3. No
  replay protection exists; record integrity
  depends on caller-held watermarks. (Disclosed:
  bp9_absorb is driver-side harness code, not
  belief-layer machinery; the bar maps where
  replay protection does NOT live.)
- K-FORGE-SHARED: genuine match on the shared
  fact fS, absorbed by mP and mQ independently:
  sup 110 both. Evidence is non-rivalrous: no
  cross-belief watermark consumption; each
  belief's provenance scoping is intact.
- K-FORGE-BLAST: ONE forged type-7 on fS,
  absorbed by both: sup 120 both. Blast radius
  2 from a single forged edge: the shared-fact
  scoping that is correct for genuine evidence
  amplifies forged evidence.

CHAIN (record completeness and tamper-evidence),
all PASS:
- K-CHAIN-WEAK: 3x R3 on z2 (sup 40, disc 3),
  propagate z1: sup[z1]==40 with disc[z1]==0,
  conf[z1]==1, rev[z1]==0, no k3 self-edge.
  Propagation changes support with no counter
  movement and no reason edge: z1's record
  cannot attribute the 40 to z2's
  disconfirmations. The provenance chain loses
  the link at the propagation step.
- K-CHAIN-RAISE: 2x R2 on z2 (sup 80), propagate
  z1: sup[z1]==80, conf[z1]==1, disc[z1]==0.
  The snap-up is likewise invisible to the
  record: z1 rose 40->80 with no confirm
  recorded on z1.
- K-CHAIN-FORGEREASON: forged kind-3 self-edge
  with novel reason code 9 on z2:
  bp2_has_k3r(z2,9)==1. The forged reason record
  is queryable exactly like a genuine retire
  record; the layer performs no verification of
  reason edges.
- K-CHAIN-DOUBLEK3: genuine bp2_retire(z2,2)
  after the forgery: has_k3r(z2,2)==1 AND
  has_k3r(z2,9)==1, sup[z2]==0. bp2_retire does
  not check for existing k3 edges, so the
  forged reason-9 record coexists with the
  genuine reason-2 record: the provenance record
  is now ambiguous (two retirements, one
  forged) and the layer has no mechanism to
  resolve which is genuine.
- K-CHAIN-TAMPER: retire z1 (reason 2), then
  direct table write bt[z1*8]=100:
  bp2_eff(z1)==100. b_ext=b_self=0 so eff
  returns support directly; nothing
  cross-checks the table against the edge
  record. The tampered value is accepted
  without question.
- K-CHAIN-RESURRECT: bp2_select over [z1] with
  bar 50 returns z1 while bp2_has_k3r(z1,2)==1.
  hasb is not cleared by retire, eff 100 >= 50,
  no tie: the layer selects a genuinely retired
  belief on corrupted state. The edge record
  (retired, reason 2) and the table (support
  100) contradict each other and the layer
  follows the table.
- K-CHAIN-STALE: bp2_kill_one_prov(mE) kills
  fE: b_ext[mE]==1 while live licensing==0.
  The table's licensing counts go stale after
  fact death; only an explicit relicense
  repairs them.
- K-CHAIN-R4: bp2_relicense(mE): formed=1,
  live=0 -> retire reason 2, sup 0,
  has_k3r(mE,2)==1. The dormant R4 detection
  measured in BP-6 still fires when triggered.
  This bar uses current frozen semantics only
  and presupposes no #16 outcome.

K-DET: 3/3 runs byte-identical, SHA-256
55de4ccfa05f33d22e477d670a67abdbb8b33560f8523a9f7b9e6f41d1125a18.
K-HYG: pure Zag under safebin (`which python3` /
`which python` empty at build and run); zero
em/en dash bytes in all authored files and run
outputs; 0 new edge types (1/3/7/14 all
pre-existing in the block; kind-3 self-edges
pre-exist via bp2_retire); 0 new node types
(tags 1/3/20 pre-existing); 0 modes, 0 bridges,
0 handlers, 0 semantic cases; block SHA-256
unchanged; bp9_learner.zag byte-identical to
bp8_learner.zag; opaque identifiers. BP9-SUMMARY
17/17 in-driver; 19/19 with K-DET/K-HYG.

## 2. What this means

The provenance record is trust-on-write at every
level. Evidence edges (type-7/type-3), reason
edges (kind-3 self-edges), and the learner-owned
table (bt[]) are all writable by anyone with the
harness's write access, and nothing in the frozen
layer verifies, cross-checks, or authenticates
any of them. The record's integrity holds only
against the world through the ev_observe path:
genuine block-mediated evidence produces exactly
the records the layer was designed around, but
the record cannot tell genuine from forged
(MATCH, DISC), the block's own one-shot
protection is bypassable at the edge layer (ORD),
reason codes are forgeable and ambiguous
(FORGEREASON, DOUBLEK3), the table is mutable
with no integrity check (TAMPER, RESURRECT), and
licensing counts go stale silently (STALE).

Three containment properties survive the
adversary, all measured: (1) per-channel
saturation caps per-absorb forgery impact at one
R2/R3 no matter how many edges are forged (SAT);
(2) evidence is non-rivalrous across beliefs
sharing a fact, with no cross-belief watermark
consumption (SHARED): provenance scoping is
intact for genuine evidence, though the same
sharing amplifies a forgery's blast radius
(BLAST); (3) the dormant R4 provenance-death
detection still fires when explicitly triggered
(R4).

Propagation is invisible to the provenance
record. R6 moves support between beliefs without
touching counters or writing reason edges, so a
composite's record systematically
underdetermines its own support value (WEAK,
RAISE). This is incompleteness rather than
corruption, but it has the same consequence for
a white-box auditor: the record cannot explain
the belief's current support. Any future
provenance audit that walks only the record
(table + reason edges + evidence counters) will
misattribute propagated support.

The 90/1/0 signature is a forgery detector for
one shape. Because genuine paths cannot produce
sup 90 with conf 1 and disc 0, an auditor that
knows the frozen rules can flag exactly the
contradict-then-forged-match shape. The layer
itself has no such audit; the detection exists
only as a human-readable consequence of the
frozen R2-then-R3 order, not as machinery.

## 3. One-system accounting

New learner machinery this lane: ZERO functions.
bp9_absorb is the BP-8 absorb renamed (identical
body); bp9_ck/bp9_bar/bp9_selfcnt/bp9_allsup/
bp9_liclive are driver-side test-harness code.
The forgery actions are adversary actions in the
driver, explicitly not belief-layer changes.
0 new edge types, 0 new node types, 0 modes,
0 bridges, 0 handlers, 0 semantic cases. Reason
code 9 is a novel field12 VALUE used only as the
forgery marker (disclosed in PREREG Section 1),
not a new edge type or semantic case: no layer
code branches on it. Beliefs remain
learner-state records, not a subsystem.

## 4. What was tested vs what was reasoned

Tested (frozen, this lane, PASS): forged type-7
absorbs to 110/2 (n7==1); forged type-3 absorbs
to 80/0/1 (n3==1); forged type-7 on a
contradicted fact absorbs to 90/1/0 (n7==1),
bypassing the block's drop rule; three forged
type-7s saturate to one R2 (n7==3, 110/2);
stale-watermark replay re-applies (120/3);
shared-fact genuine match counted by both
beliefs (110/110); one forged shared-fact edge
corrupts both (120/120); propagated weakening
(40) and snap-up (80) leave no trace on the
composite's counters or reason edges; forged
reason-9 edge queryable and coexisting with
genuine reason-2 retire; table tamper to 100
accepted (eff 100) with the retired belief
selected at bar 50 while its reason-2 edge
persists; fact death leaves b_ext stale (1 vs
live 0); explicit relicense retires reason-2.

Reasoned: that the record is trust-on-write at
every level (follows from the absence of any
verification code path in the frozen layer, now
measured at all three levels); that the 90/1/0
shape is forgery-attributable (follows from the
frozen R2/R3 order plus the block's drop rule,
not from an audit mechanism); that propagation
incompleteness would mislead a record-only
auditor (follows from the measured record
states, not from a built auditor).

## 5. Open questions (not claimed)

Whether any tamper-evidence belongs in the
belief layer (measured absent at all three
levels; adding it would be new learner
machinery, a design decision); whether R6
should write provenance traces for propagated
support (measured absent; same design-decision
status); whether watermark discipline should
move into the layer (currently caller-held);
eviction-sync design (still needs the parent
ruling: persist vs tombstone vs R4-retire,
#16); per-belief bar adoption (#17); d_self
recovery (#18). The two untested task options
remain open: belief revision under
contradiction (option 2) and cross-belief
interaction (option 3).

## 6. Notes for the parent

- No ledger entry: non-ledger task, nothing minted.
- No push: commits local on tnn-native-lab only,
  explicit pathspecs. This report is committed with
  the lane's implementation artifacts.
- DESIGN.md is untouched; this lane tests it and
  does not reinterpret it. BP-2 through BP-8
  REPORT.md files are untouched. The 7 sealed
  predictions stay sealed; this lane adds
  adversarial-integrity evidence only.
- No amendment round: the first implementation
  run went 17/17 against the frozen prereg, so
  PREREG.md Section 5b stays empty.
- Suggested nexts from the remaining open list:
  the two untested task options (belief revision
  under contradiction; cross-belief interaction
  beyond the shared-fact scoping measured here);
  whether to adopt per-belief bars (#17); whether
  d_self needs a recovery path (#18);
  eviction-sync design (#16, still needs your
  ruling).
- Style: no em/en dashes in authored files
  (hyphens only), opaque identifiers throughout.
