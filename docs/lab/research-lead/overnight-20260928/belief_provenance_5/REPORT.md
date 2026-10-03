# REPORT: BP-5 (belief-layer open dynamics)

Worker: BELIEF-PROVENANCE-5 subagent, 2026-10-03. Non-ledger
task (claim minting paused); nothing minted.
Branch: tnn-native-lab, local only, never pushed.
Lane: docs/lab/research-lead/overnight-20260928/belief_provenance_5/
Verdict: **BP-5-PASS** (all 4 preconditions, all 27 kill
bars, K-DET 3/3 byte-identical, K-HYG clean). Method: frozen
prereg (committed as bcbc25221 before any implementation),
BP-4's belief machinery reused verbatim plus exactly three
new learner functions (B-FACT/B-META formation, I1
enforcement), six independent worlds, in-driver bars.

## 0. What was built

`bp5_learner.zag` is BP-4's `bp4_learner.zag` copied
verbatim (SHA-256
2de20f5a0ff87bc45140a161548b613b008e9c2adabf4da3fdda6d6d46040c5e
on both files, `cmp` clean): the learner-owned u8 belief
table, R1-R7, eff(), b_retire, the lg() baseline. No
redesign; the task's "build on BP-4" is literal.

`bp5_rules.zag` is the new learner machinery this lane
(exactly three functions, disclosed in PREREG Section 1):
`bp5_form_fact` (B-FACT R1: the fact's own P6 field16 tag
sets the ext/self partition; formed=0 so R4 is a no-op),
`bp5_form_meta` (B-META R1: no type-1 licensing; support
moves only via R2/R3 on policy outcomes),
`bp5_fact_tombstone` (I1 enforcement: tombstone destroys
the fact's belief record; slot recycling gives a fresh
R1).

`bp5_driver.zag` is the battery driver: the BP-4 world
replay (renamed bp5_build), the emergent-evidence
absorption helper `bp5_absorb_fact` (applies R2/R3 iff the
frozen block wrote a new type-7/type-3 self-edge), the
meta-update mapping, the R5 field28-delta trigger, six
world arms, in-driver bars.

`bp5_full.zag` = `xf_block.zag` (patched block, verbatim,
SHA-256 172a2e7dbbaa4e60d662331965887327350068e0c13f25e438260ad08313c12a
re-verified before and after the build) + `bp5_learner.zag`
+ `bp5_rules.zag` + `bp5_driver.zag`. One `main`. Pinned
znc by absolute path, build exit 0 -> bp5_bin (408778
bytes); the A0102 warnings are the benign
ignored-return-value pattern pervasive in the frozen block
itself (same as BP-4).

## 1. Kill-bar results

Preconditions (4/4 PASS): PC-E-R3-FORM (ma formed,
ext=self=1), PC-E-R5-FORM (mb formed, field28=201),
PC-MH-BUILD (replay: mv2=194, mv3=274),
PC-CY-FORM (zA=zB=100).

E-R3 (emergent disconfirmation), all PASS:
- K-E-R3-C7: the block wrote exactly 1 new type-7 edge
  on the observed fact (ret 1). The confirmation
  evidence is block-written, not driver-chosen.
- K-E-R3-CSUP: b_sup[ma]=110, b_conf=2 (R2 routed).
- K-E-R3-D3: the block wrote exactly 1 new type-3 edge
  on the contradicted fact (ret 0).
- K-E-R3-DSUP: b_sup[ma]=90, b_disc=1, b_conf=0 (R3
  routed).
- K-E-R3-NOR5: field28 still 10, b_rev=0. The block
  attempted the revise and reverted (rootless MAP), so
  R5 correctly did not fire. R3-without-R5 isolation.

E-R5 (emergent revision), all PASS:
- K-E-R5-CTL: matching observation leaves field28=201,
  b_rev=0, b_sup=100. No contradiction -> no revision
  -> no R5 (no spurious firing).
- K-E-R5-REV: contradicting observation -> block's
  t2_revise_graph succeeds -> field28=999. The revision
  evidence is a structural delta, not a driver call.
- K-E-R5-TRAJ: b_sup[mb]=50, b_rev=1, b_conf=0,
  b_disc=0 (R5 applied iff the field28 delta held).

B-FACT (fact beliefs), all PASS:
- K-BF-FORM: 100/100/100; (ext,self) = (1,0)/(0,1)/
  (0,0) from field16 tags 2/6/untagged; b_conf=1.
- K-BF-EV: one new type-7 on fc1 -> 110; one new
  type-3 on fc2 -> 80, b_disc=1. Emergent evidence
  routes to fact beliefs.
- K-BF-SEL: R7({fc1,fc2,fc3})=fc1. Fact beliefs are
  selectable.
- K-BF-EFF: eff[fc3]=100 (no-partition branch),
  eff[fc1]=110 (partition branch).
- K-BF-I1DIE: tombstone -> hasb=0, node dead.
- K-BF-I1SEL: R7({fc2,fc3})=fc3 (recordless fact
  skipped).
- K-BF-I1FRESH: recycled slot re-formed -> 100/0/1,
  no inheritance of the old b_disc=1.

B-META (meta-beliefs), all PASS:
- K-BM-FORM: 100/100; 2 type-16 edges each (P5
  convention, winner-first).
- K-BM-EV: one observation (mA's licensing fact
  confirmed) -> mA=110, mr1 (winner confirmed)
  =110/b_conf=2, mr2 (loser confirmed) =80/b_disc=1.
  One event moves rival meta-rows oppositely.
- K-BM-SEL: R7({mr1,mr2})=mr1. The evidential policy
  is revisable state that participates in selection.

MH (multi-hop), all PASS:
- K-MH-1HOP: R6(z1)=(60,100,100). A single R6 does
  NOT cascade: z2,z3 untouched.
- K-MH-2HOP: R6(z2)=(60,100). K-MH-3HOP: R6(z3)=60.
  Weakening crosses 3 hops via per-hop application.
- K-MH-MIN: z4 with targets mv2(100),mv3(60) -> 60
  (min combiner over two targets).

CY (cyclic), all PASS:
- K-CY-C1: (80,80) after R6(zA).
- K-CY-C2: zB=80 after R3(zB)->60 then R6(zB). R6
  snaps the node to its targets' min; it can RAISE
  support, not only lower it.
- K-CY-C3: re-application (80,80): fixpoint,
  idempotent, no oscillation.
- K-CY-C4: zB=0 then R6(zA) -> zA=0 with kind-3
  reason-2 edge. 0 absorbs with retirement.
- K-CY-C5: R6(zB) -> zB=0. The whole 2-cycle
  converges to the min.

K-DET: 3/3 runs byte-identical, SHA-256
6793bd2bd5798c1546702bac42efd8d74a974dc00a65a88448e317a29b58af2f.
K-HYG: pure Zag under safebin (`which python3`/`which
python` empty at build and run); zero em/en dash bytes
in all authored files; 0 new edge types (1/3/14 frozen;
16 pre-exists in the block per DESIGN.md P5, used for
meta-rows); 0 new node types (tags 1/3/20
pre-existing); 0 modes, 0 bridges, 0 handlers;
xf_block.zag hash unchanged; bp5_learner.zag
byte-identical to bp4_learner.zag; opaque identifiers.
BP5-SUMMARY 31/31 in-driver; 33/33 with K-DET/K-HYG.

## 2. What this means

R3/R5 now fire on emergent evidence. The harness never
chooses confirm vs disconfirm and never calls R5
directly: block-written type-7/type-3 edges route to
R2/R3, and a block-made field28 delta triggers R5. The
control legs (matching observations) show the triggers
are absent without the world event, so the dynamics are
world-driven, not driver-driven.

B-FACT and B-META are now formed beliefs, not just
design text. Facts carry the P6 partition on their own
tag; meta-rows carry the evidential policy as revisable
state. I1 holds for facts: tombstone destroys the
record and recycling starts fresh.

Propagation dynamics are characterized, answering the
DESIGN.md 10 open question empirically: R6 is a
per-hop, per-node operator (no automatic cascade);
multi-hop weakening works by explicit re-application;
on cycles the min combiner converges monotonically to
the cycle min (fixpoint, no oscillation, cycles not
prevented); R6 sets the node to its targets' min and
can therefore raise as well as lower (K-CY-C2); 0 is
absorbing and retires the component with reason 2.

## 3. One-system accounting

New learner machinery this lane: exactly three
functions, `bp5_form_fact`, `bp5_form_meta`,
`bp5_fact_tombstone` (~40 lines total), all operating
on the existing 8-u8 record schema. Everything else is
BP-4's belief layer verbatim plus test-harness code.
0 new edge types, 0 new node types, 0 modes, 0
bridges, 0 handlers, 0 semantic cases. Beliefs remain
learner-state records, not a subsystem.

## 4. What was tested vs what was reasoned

Tested (frozen, this lane, PASS): emergent R2/R3
routing from block-written evidence edges with exact
b_sup trajectories (110/90); R5 firing iff the block
revised (field28 201->999) with the exact halving
(50) and its absence without contradiction; B-FACT
formation/partition/evidence/selection/eff branches;
B-META formation, opposite updates from one event,
policy selection; 3-hop propagation values
(60/60/60) with the no-cascade discriminator; the
2-cycle fixpoint, the R6 snap-up (60->80), 0-absorption
with retirement; determinism; hygiene.

Reasoned: that the absorb mapping (indep=0 for
same-fact evidence) and the meta-update mapping are
adequate forms (the lane tests that routing happens at
all and is world-gated, not that the form is optimal);
that per-hop R6 application is the right operational
reading of propagation (as opposed to a built-in
fixpoint loop); that the min combiner's cycle behavior
generalizes beyond the 2-cycle (monotonicity of min
argues it does, untested at larger cycles).

## 5. Open questions (not claimed)

Combiner alternatives (min is frozen); bar-adjustment
trajectories; eviction interaction; d_self on
fact/meta beliefs; per-belief bars; larger cycles
(3+, nested); multi-channel absorption in one arm;
whether R6 should be a built-in fixpoint loop rather
than per-node application.

## 6. Notes for the parent

- No ledger entry: non-ledger task, nothing minted.
- No push: commits local on tnn-native-lab only,
  explicit pathspecs. This report is committed with the
  lane's implementation artifacts.
- DESIGN.md is untouched; this lane tests it and does
  not reinterpret it. BP-2/BP-3/BP-4 REPORT.md files are
  untouched. The 7 sealed predictions stay sealed; this
  lane adds open-dynamics evidence only.
- Suggested next from the remaining BP-4 open list:
  bar-adjustment trajectories, combiner alternatives,
  eviction interaction, larger/nested cycles.
- Style: no em/en dashes in authored files (hyphens
  only), opaque identifiers throughout.
