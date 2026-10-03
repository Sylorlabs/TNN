# REPORT: rule_revision (counterexample refines an overgeneralized RULE)

Worker: Rule Revision Worker.
Date: 2026-10-02. Prereg: PREREG.md, frozen alone in commit 57a04ac34
(commit-order self-check: prereg commit is an ancestor of the
implementation commit and contains exactly one file).
Implementation: pure Zag, safebin PATH, no Python (guard verified at
worker start and re-verified in build.sh: python3/python absent at build
time).

## Verdict

**RULE-REVISION-COMPLETE.** All six frozen kill bars hold. No SURVIVES
claim is made; this is a mechanism demonstration, not a generality proof.

## What was built

A standalone pure-Zag program (`rr_mech.zag` mechanism + `rr_main.zag`
driver, assembled to `rr_full.zag`, compiled to `rr_bin`) in which a
verification failure drives learner-owned revision of the blamed
component's RULE (not a value-keyed exception; the program contains zero
exception machinery):

- TEACH: the learner probes components C (chain-follow) and D (v+1) on
  frozen observations (31->32, 32->33 each), appends each probe outcome
  to the component's observation log in learner state, runs the real H1
  signature machinery (kind probe + majority finalize), and runs the
  generic rule_induce over the observation log: all observed output kinds
  agree (NODE), so both components induce the CONSTANT rule ALWAYS(NODE).
  D's probes never cover 33, so D's rule is honestly overgeneralized
  (true kind(D(33))=kind(34)=NUM).
- Z2: goal input=33, want NODE. Learner commits to DD, genuinely
  predicting NODE from its (wrong) constant rule (status PENDING, logged
  before execution). World executes (actual 35, instrumentation only),
  downstream rejects (35 is NUM), gate=0. Learner updates conf(DD)
  0->-1 from the gate alone. This is the verification failure.
- REFUTE: the driver invokes learner_refute on the failed (DD, 33).
  The learner walks the chain from the known input value. Link 0 = D on
  33: the rule predicts NODE; the learner probes D on 33 through the
  fixed component interface, observes out=34, applies its own kind probe
  -> NUM, and appends (33,NUM) to D's observation log; NUM != NODE ->
  the counterexample (comp=D, in=33, pred=NODE, actual=NUM) is recorded
  in the learner's ce cells and the walk stops at the first mismatch.
  The transcript states the RULE was refuted. Blamed: D.
- REVISE: the driver invokes learner_refine (unconditional; no-ops with
  no counterexample). It reads the ce cells and D's observation log
  [(31,NODE),(32,NODE),(33,NUM)], finds the smallest logged input the
  current rule mispredicts (33), keeps the old rule's prediction there
  (NODE) as the below kind, takes the observed kind there (NUM) as the
  at-and-above kind, and writes the THRESHOLD rule IF(in<33,NODE,NUM).
  The function contains no D-specific, 33/34/30-specific, or
  kind-specific constants; the driver passes it no values. The refined
  rule fits the learner's own observation log 3/3.
- RETEST: learner predicts D(33) with the refined rule -> 33 is not <
  33 -> NUM; world truth kind(D(33))=kind(34)=NUM. MATCH.
- REGRESS: learner predicts D(31) -> 31 < 33 -> NODE, D(32) -> 32 < 33
  -> NODE (the below-threshold region keeps the old kind). Both match
  world truth.
- GENERALIZE: the learner predicts D(34) and D(30), inputs it never
  probed (build.sh verifies zero OBS lines mention 34 or 30). 34 is not
  < 33 -> NUM; world truth kind(D(34))=kind(35)=NUM. MATCH. 30 < 33 ->
  NODE; world truth kind(D(30))=kind(31)=NODE. MATCH. A value-keyed
  exception for 33 could not have produced either prediction; the rule
  predicate answers inputs absent from the observation log.
- Z4: new problem, goal input=33, want NODE. Selection with the refined
  rules: DD is now inadmissible (rule prediction for D(33) is NUM,
  breaking the seam against sig_in(D)=NODE); CC remains admissible (C's
  rule unchanged). Choice: CC, no execution. The refinement changed what
  the learner considers for input 33.
- Z5: goal input=31, want NODE. Driver directs commit to DD; refined
  rule predicts NODE (31 < 33). World executes (actual 33), downstream
  accepts, gate=1. Update: conf(DD) -1->0. The refinement did not break
  the previously working composition.

## Kill-bar evidence (mechanical)

- K-RR-1 (D's contract is an overgeneralized RULE, not a missing
  exception): run1.txt line 8 reads
  `TEACH D rule=ALWAYS(NODE) sig=NODE->NODE obs=2` with OBS lines on
  probes (31,32) only. The source implements probe_kind (rr_mech.zag
  lines 148-156), h1_observe/h1_finalize (lines 194-218), obs_append
  (lines 180-190), and the generic rule_induce (lines 227-249:
  majority of observed output kinds, tie to first observed kind).
  Prediction goes through rule_pred (lines 251-258), a predicate over
  input values; there is no lookup list anywhere. build.sh reports
  `exception_machinery_occurrences=0` over both sources. The frozen
  world makes the overgeneralization factual: kind(D(33))=kind(34)=NUM
  while the constant rule predicts NODE for every input.
- K-RR-2 (verification failure refutes the rule): run1.txt line 14
  reads `Z2 CONSEQUENCE gate=0 downstream=REJECT`, preceding the REFUTE
  lines 16-19: `REFUTE link=0 comp=D in=33 rule-pred=NODE probed-out=34
  probed-kind=NUM MISMATCH`, `REFUTE COUNTEREXAMPLE comp=D in=33
  pred=NODE actual=NUM`, and `REFUTE RULE-REFUTED D rule=ALWAYS(NODE)
  wrong on probed input 33`. The ce cells (18..21) hold (1,33,1,2).
  learner_refute (rr_mech.zag lines 319-354) loops over chain links via
  comp_first/comp_second, stops at the first mismatch, appends each
  probe outcome to the observation log, and contains no 33/34/30
  literals (build.sh sed-scoped check returns 0); its outcome is
  determined by the world probe, not by researcher constants. No link=1
  line is emitted: the walk stopped at the mismatch, exactly as
  preregistered.
- K-RR-3 (learner induces a REFINED RULE, not an exception): run1.txt
  lines 20-21 read `REVISE before D rule=ALWAYS(NODE)
  obs-log=[(31,NODE),(32,NODE),(33,NUM)]` and `REVISE after D
  rule=IF(in<33,NODE,NUM) fit=3/3 (refined rule vs learner obs log)`,
  rendering D's rule cells and observation log in learner state before
  and after the single learner_refine call. The only rule-cell writes
  in the program are the six `ls(L,rb...)` sites: two at rr_mech.zag
  lines 243-244 (inside the generic rule_induce) and four at lines
  377-380 (inside the generic learner_refine); build.sh verifies the
  6/2/4 split. learner_refine (lines 356-387) reads the blamed
  component from the ce cells and every value from the observation log;
  it contains no 33/34/30 literals and no D-specific constants
  (build.sh sed-scoped check returns 0); the driver passes it no
  arguments. The revision content (T=33, NODE below, NUM at/above)
  originates in the learner-recorded observation log. RULE-FIT 3/3
  shows the refined rule fits the learner's own recorded experience.
- K-RR-4 (refined rule generalizes to new inputs): run1.txt lines 24-25
  read `GENERALIZE D(34) rule-pred=NUM world-kind=NUM MATCH (input 34
  never probed: no OBS line above)` and `GENERALIZE D(30) rule-pred=NODE
  world-kind=NODE MATCH (input 30 never probed: no OBS line above)`,
  where world-kind is the fixed probe_kind law applied to the world's
  true D(34)=35 and D(30)=31, not a stored answer. `grep -ci expected`
  over both sources returns 0. build.sh verifies zero OBS lines mention
  34 or 30 (`grep -c 'OBS D in=34\|OBS D in=30'` returns 0), so these
  inputs are genuinely unseen: the learner's observation log holds only
  (31,32,33). A value-keyed entry for 33 could not have answered 34 or
  30; the threshold predicate did.
- K-RR-5 (no forgetting of previously-correct cases): run1.txt lines
  22-23 read `REGRESS D(31) rule-pred=NODE world-kind=NODE MATCH` and
  `REGRESS D(32) rule-pred=NODE world-kind=NODE MATCH`; lines 29-33 show
  Z5 committing DD on 31 with predicted=NODE, actual=33, gate=1 ACCEPT,
  conf(DD) -1->0. The threshold keeps the below-33 region on the old
  kind, so the previously-correct region is preserved by construction.
- K-RR-6 (determinism): 3/3 runs byte-identical. sha256 of run1.txt,
  run2.txt, run3.txt:
  fa93199d9c7737cef608f97cdd057c9b7859889d7f9da4f1ead4aecc99aeb93b
  (all three equal; cmp confirms pairwise). All three runs exit 0.

## Predictions vs results

Prereg predictions: P1 TEACH D rule=ALWAYS(NODE) from probes 31,32 only
(got exactly); P2 Z2 gate=0, conf(DD) 0->-1 (got exactly); P3 REFUTE ce
comp=D in=33 pred=NODE actual=NUM, RULE-REFUTED line, walk stops at link
0 (got exactly, no link=1 line); P4 REVISE ALWAYS(NODE) ->
IF(in<33,NODE,NUM), fit=3/3, C rule unchanged (got exactly); P5 RETEST
MATCH, REGRESS 2/2 MATCH (got exactly); P6 GENERALIZE 34->NUM MATCH and
30->NODE MATCH with zero OBS lines for either (got exactly); P7 Z4 DD
inadmissible / CC admissible / choice CC with no execution, Z5 DD on 31
gate=1 conf -1->0 (got exactly); P8 3/3 byte-identical (got 3/3). 8/8
predictions matched.

## Architecture accounting

- rr_mech.zag: 404 total lines, ~300 code lines. Of those: ~110 output
  helpers + state-cell accessors (infrastructure), ~190 cognition
  lines (facts, kind probe, components, observation log, H1
  observe/finalize, rule induction, rule application, commit, world law,
  update, refute, refine, select).
- rr_main.zag: 241 total lines, ~200 code lines, all harness (phase
  sequencing, transcript emission).
- Zero new modes, zero bridges, zero handlers, zero new opcodes, zero
  new MAP/edge types (standalone program; no substrate types used).
  Zero occurrences of "mode", "bridge", "handler", "exception" in either
  source (grep counts 0; the rule form selector is named rule_form).
  Zero `as *i32` slice constructions (grep count 0).
- The observation log and the refinement operator are learner-state
  machinery, not modes: there is no conditional dispatch on task labels
  anywhere. The refutation probe is a learner-initiated experiment
  through the fixed component interface (the same lawful interface H1
  teaching uses), not a mode. learner_update still reads only the gate;
  the commit path never receives actual output values.

## Red-team self-review

1. "The rule class (CONSTANT / single THRESHOLD on input order) is
  researcher-designed; the learner is not really inducing." The
  machinery/content distinction is the same as H1's: the researcher
  supplies the generic operators (rule_induce, the first-deviation
  split); the learner supplies the content. Evidence the content is
  learner-discovered: learner_refute and learner_refine contain no
  D/33/34/30/NUM literals; the driver passes no values to either; the
  observation log and counterexample cells are the only inputs to the
  refinement; the split point could have been any logged input, and the
  world determined which. The researcher could not have produced
  IF(in<33,NODE,NUM) without the learner's probing. The claim is
  learner-driven rule revision within this class, not open-ended rule
  invention (not L3); the prereg states this boundary explicitly.
2. "The threshold operator bakes in the world's integer-order
  structure, so the generalization is rigged." The operator is a
  decision stump on input order; the world (D is v+1, kind flips at 34)
  has matching structure. The learner exploits it, it does not discover
  the world's law. The honest claim is narrower: the induced rule
  answers unseen inputs correctly on the tested cases, which a
  value-keyed exception provably cannot do. That is exactly the delta
  this lane was asked to demonstrate.
3. "IF(in<33,...) is just a fancy exception for 33 in disguise." It is
  not: the predicate partitions the whole input line, including values
  never observed. The GENERALIZE phase is the discriminator: 34 and 30
  were never probed (zero OBS lines, build.sh verified), yet the rule
  predicts both correctly. A lookup entry for 33 is silent on 34 and 30.
4. "The driver decides to call refute/refine after the failure, so the
  revision is researcher-sequenced." Phase sequencing is harness, the
  same standing as the driver calling learner_update after a
  consequence in the contract_revision lane. What the driver passes back
  (composition id, input value) is exactly what the learner committed
  to; every revision decision (which component, which split point,
  which kinds) is computed by learner functions from learner state.
5. "C is equally overgeneralized but never revised; the experiment is
  selective." Accepted as a boundary, documented in the prereg: C
  revision is a follow-up, not part of these bars. Z4 performs no
  execution, so no claim about C is made. C's rule cells are never
  written after TEACH (the six rule write sites touch only rule_induce
  and the ce-named component in learner_refine).
6. "Toy scale; ~190 cognition lines prove nothing about TNN."
  Accepted: mechanism demonstration with frozen bars, explicitly not
  substrate integration and not a generality claim.

## Boundaries and non-claims

- The rule class (CONSTANT / single THRESHOLD on input order) is
  researcher-supplied machinery; the content (T=33, the two kinds) is
  learner-discovered. Not open-ended rule invention, not L3.
- The refinement operator performs a single split at the first
  deviation; multi-split or multi-predicate refinement is not
  implemented and not claimed.
- The generalization along integer input order works because the frozen
  world has that structure; no claim is made that the learner discovered
  the world's law.
- The blame walk stops at the first mismatching link; deeper
  multi-link fault localization is not claimed.
- The refutation probe lets the learner observe intermediate values as
  experiment outcomes; the commit/update path still never receives
  actuals. The distinction is labeled in the transcript.
- No claim is made about transfer, scaling, or subsumption of other
  mechanisms. The verdict is RULE-REVISION-COMPLETE (mechanism built and
  bars met), never SURVIVES.

## Deliverables (this lane dir)

- NAMECHECK.md (Step 0 toolchain guard + steps)
- PREREG.md (frozen alone, commit 57a04ac34)
- rr_mech.zag, rr_main.zag (sources), rr_full.zag (assembled, sha256
  59e0014158243861015bf5bc7868a62e219a72efba225e33b81bd4ea07b2450b),
  build.sh (guard + checks + build + 3x run)
- rr_bin (compiled binary, sha256
  1cef3b9abd26c69c2e56652fcf41044307cbc537d2584e192888cd3e884b9465),
  compile.txt
- run1.txt, run2.txt, run3.txt, sha256sums.txt
- REPORT.md (this file)

All commits local only, explicit pathspecs, nothing pushed.
