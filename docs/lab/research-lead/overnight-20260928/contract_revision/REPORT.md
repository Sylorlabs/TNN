# REPORT: contract_revision (verification failure drives learner-owned contract revision)

Worker: Contract Revision Worker.
Date: 2026-10-02. Prereg: PREREG.md, frozen alone in commit 26966e353
(commit-order self-check: prereg commit is an ancestor of the
implementation commit and contains exactly one file).
Implementation: pure Zag, safebin PATH, no Python (guard verified at
worker start and re-verified in build.sh: python3/python absent at build
time).

## Verdict

**CONTRACT-REVISION-COMPLETE.** All six frozen kill bars hold. No
SURVIVES claim is made; this is a mechanism demonstration, not a
generality proof.

## What was built

A standalone pure-Zag program (`cr_mech.zag` mechanism + `cr_main.zag`
driver, assembled to `cr_full.zag`, compiled to `cr_bin`) in which a
verification failure drives learner-owned revision of the blamed
component's contract:

- TEACH: the learner probes components C (chain-follow) and D (v+1) on
  frozen observations (31->32, 32->33 each), applies the H1 kind probe
  (1=NODE iff the value appears as a fact subject, else 2=NUM) over the
  frozen world facts (31,91,32),(32,91,33),(33,91,34), accumulates
  per-observation kind sums via h1_observe, and finalizes with the H1
  majority rule (n>=2, sum*2>=n*3 -> kind 2). Learned: C=1->1, D=1->1,
  both with empty exception lists. D's probes never cover 33, so D's
  contract is honestly overgeneralized (true kind(D(33))=kind(34)=NUM).
- Z2: goal input=33, want NODE. Learner commits to DD, genuinely
  predicting NODE from its (wrong) D contract (status PENDING, logged
  before execution). World executes (actual 35, instrumentation only),
  downstream rejects (35 is NUM), gate=0. Learner updates conf(DD)
  0->-1 from the gate alone. This is the verification failure.
- REFUTE: the driver invokes learner_refute on the failed (DD, 33).
  The learner walks the chain from the known input value. Link 0 = D on
  33: contract predicts NODE (generic rule, exceptions empty); the
  learner probes D on 33 through the fixed component interface, observes
  out=34, applies its own kind probe -> NUM; NUM != NODE -> the
  counterexample (comp=D, in=33, pred=NODE, actual=NUM) is recorded in
  the learner's ce cells and the walk stops at the first mismatch.
  Blamed: D.
- REVISE: the driver invokes learner_revise (unconditional; no-ops with
  no counterexample). It reads the ce cells and appends (33 -> NUM) to
  D's exception list. D's contract in learner state changes from
  NODE->NODE exc=[] to NODE->NODE exc=[33->NUM]. The function contains
  no D-specific, 33-specific, or NUM-specific constants; the driver
  passes it no values.
- RETEST: learner predicts D(33) with the revised contract -> exception
  hit -> NUM; world truth kind(D(33))=kind(34)=NUM. MATCH.
- REGRESS: learner predicts D(31) -> NODE, D(32) -> NODE (exceptions do
  not cover them; the general rule is untouched). Both match world
  truth.
- Z4: new problem, goal input=33, want NODE. Selection with the revised
  contracts: DD is now inadmissible (first-link prediction for 33 is
  NUM via the exception, breaking the seam against sig_in(D)=NODE);
  CC remains admissible (C's contract unchanged). Choice: CC, no
  execution. The revision changed what the learner considers for
  input 33.
- Z5: goal input=31, want NODE. Driver directs commit to DD; revised
  contract predicts NODE (31 has no exception). World executes (actual
  33), downstream accepts, gate=1. Update: conf(DD) -1->0. The
  revision did not break the previously working composition.

## Kill-bar evidence (mechanical)

- K-CR-1 (D initially overgeneralized from limited probes): run1.txt
  lines 4-9 show OBS lines on probes (31,32) only for both components
  and TEACH lines `C sig=NODE->NODE exc=[]`, `D sig=NODE->NODE exc=[]`.
  The source implements probe_kind (cr_mech.zag: 1=NODE iff fact
  subject, else 2=NUM), h1_observe, and h1_finalize (majority rule
  n>=2, sum*2>=n*3 -> kind 2; cr_mech.zag lines 166-182). Zero hardcoded
  signature writes: the only signature-cell writes are the two
  `ls(L,base+4,si)` / `ls(L,base+5,so)` sites at cr_mech.zag lines 173
  and 179, both inside h1_finalize. The frozen world makes the
  overgeneralization factual: kind(D(33))=kind(34)=NUM while the
  contract predicts NODE.
- K-CR-2 (verification failure provides a counterexample): run1.txt
  line 14 reads `Z2 CONSEQUENCE gate=0 downstream=REJECT`; lines 16-18
  read `REFUTE chain=DD input=33 (learner-initiated probes)`,
  `REFUTE link=0 comp=D in=33 pred=NODE probed-out=34 probed-kind=NUM
  MISMATCH`, `REFUTE COUNTEREXAMPLE comp=D in=33 pred=NODE
  actual=NUM`. The COUNTEREXAMPLE line renders the ce cells (18..21),
  which hold (1,33,1,2). learner_refute (cr_mech.zag lines 262-291)
  loops over chain links via comp_first/comp_second, stops at the first
  mismatch, and contains no 33/34 literals (build.sh sed-scoped check
  returns 0); its outcome is determined by the world probe, not by
  researcher constants. No link=1 line is emitted: the walk stopped at
  the mismatch, exactly as preregistered.
- K-CR-3 (learner revises using the counterexample): run1.txt lines
  19-20 read `REVISE before D sig=NODE->NODE exc=[]` and `REVISE after
  D sig=NODE->NODE exc=[33->NUM]`, rendering D's exception cells in
  learner state before and after the single learner_revise call. The
  only exception-cell writes in the program are the three `ls(L,xb...)`
  sites at cr_mech.zag lines 307-309, all inside learner_revise
  (build.sh grep check). learner_revise (cr_mech.zag lines 299-316)
  reads comp/input/kind solely from the ce cells and contains no 33/34
  literals (build.sh sed-scoped check returns 0); the driver passes it
  no arguments carrying values.
- K-CR-4 (revised contract correct on the previously-failed input):
  run1.txt line 21 reads `RETEST D(33) pred=NUM world-kind=NUM MATCH`,
  where world-kind is the fixed probe_kind law applied to the world's
  D(33)=34, not a stored answer. `grep -ci expected` over both sources
  returns 0.
- K-CR-5 (no catastrophic forgetting): run1.txt lines 22-23 read
  `REGRESS D(31) pred=NODE world-kind=NODE MATCH` and `REGRESS D(32)
  pred=NODE world-kind=NODE MATCH`; lines 28-31 show Z5 committing DD
  on 31 with predicted=NODE, actual=33, gate=1 ACCEPT, conf(DD) -1->0.
  The exception list is value-keyed, so the general rule is untouched
  for unrefuted inputs.
- K-CR-6 (determinism): 3/3 runs byte-identical. sha256 of run1.txt,
  run2.txt, run3.txt:
  3fb5c30379994cab20e7c83d833ac4e0903599596c9bae22c2f6832ffc4886b5
  (all three equal; cmp confirms pairwise).

## Predictions vs results

Prereg predictions: P1 TEACH D sig=NODE->NODE exc=[] from probes 31,32
only (got exactly); P2 Z2 gate=0, conf(DD) 0->-1 (got exactly); P3
REFUTE ce comp=D in=33 pred=NODE actual=NUM, walk stops at link 0 (got
exactly, no link=1 line); P4 REVISE D exc [] -> [33->NUM], C exc stays
[] (got exactly); P5 RETEST MATCH, REGRESS 2/2 MATCH (got exactly); P6
Z4 DD inadmissible / CC admissible / choice CC with no execution, Z5 DD
on 31 gate=1 conf -1->0 (got exactly); P7 3/3 byte-identical (got 3/3).
7/7 predictions matched.

## Architecture accounting

- cr_mech.zag: 334 total lines, 240 code lines. Of those: ~100 output
  helpers + state-cell accessors (infrastructure), ~140 cognition
  lines (facts, kind probe, components, H1 observe/finalize, contract
  application, commit, world law, update, refute, revise, select).
- cr_main.zag: 185 total lines, 155 code lines, all harness (phase
  sequencing, transcript emission).
- Zero new modes, zero bridges, zero handlers, zero new opcodes, zero
  new MAP/edge types (standalone program; no substrate types used).
  Zero occurrences of "mode", "bridge", "handler" in either source
  (grep count 0). Zero `as *i32` slice constructions (grep count 0).
- The refutation probe is a learner-initiated experiment through the
  fixed component interface (the same lawful interface H1 teaching
  uses), not a mode. learner_update still reads only the gate; the
  commit path never receives actual output values.

## Red-team self-review

1. "The exception list is researcher-designed machinery; the learner is
  not really revising." The machinery/content distinction is the same
  as H1's: the researcher supplies the generic operation (finalize /
  exception-append); the learner supplies the content. Evidence the
  content is learner-discovered: learner_refute and learner_revise
  contain no D/33/34/NUM literals; the driver passes no values to
  either; the counterexample cells are the only input to the revision;
  the walk could have blamed the second link or found no mismatch, and
  the world determined which. The researcher could not have produced
  (33 -> NUM) without the learner's probing.
2. "The refutation probe lets the learner observe actual values,
  violating the no-actuals principle." The no-actuals constraint
  governed the commit/update path (no answer keys in verification).
  Refutation probes are active inquiry through the same lawful
  interface as H1 teaching probes, which also observe (in, out) pairs.
  The transcript labels probe outcomes as learner-observed experiment
  results, distinct from driver instrumentation, and learner_update
  still reads only the gate.
3. "The driver decides to call refute/revise after the failure, so the
  revision is researcher-sequenced." Phase sequencing is harness, the
  same standing as the driver calling learner_update after a
  consequence in verify_h1. What the driver passes back (composition
  id, input value) is exactly what the learner committed to; every
  revision decision (which component, which input, which kind) is
  computed by learner functions from learner state.
4. "Value-keyed exceptions do not generalize; this is not real
  revision." Accepted as a boundary, not a flaw in the claim: the bars
  test revision by counterexample, not rule induction. The exception is
  the minimal contract change that fixes the misprediction while
  leaving the general rule intact (K-CR-5), which is precisely what a
  counterexample warrants.
5. "C is equally overgeneralized but never revised; the experiment is
  selective." Accepted as a boundary, documented in the prereg: C
  revision is a follow-up, not part of these bars. Z4 performs no
  execution, so no claim about C is made.
6. "Toy scale; ~140 cognition lines prove nothing about TNN."
  Accepted: mechanism demonstration with frozen bars, explicitly not
  substrate integration and not a generality claim.

## Boundaries and non-claims

- The blame walk stops at the first mismatching link; deeper
  multi-link fault localization is not claimed.
- The exception list is value-keyed with capacity 4; the learner does
  not induce a general rule from the counterexample. The claim is
  revision by counterexample, not rule induction.
- The refutation probe lets the learner observe intermediate values as
  experiment outcomes; the commit/update path still never receives
  actuals. The distinction is labeled in the transcript.
- No claim is made about transfer, scaling, or subsumption of other
  mechanisms. The verdict is CONTRACT-REVISION-COMPLETE (mechanism built
  and bars met), never SURVIVES.

## Deliverables (this lane dir)

- NAMECHECK.md (Step 0 toolchain guard + steps)
- PREREG.md (frozen alone, commit 26966e353)
- cr_mech.zag, cr_main.zag (sources), cr_full.zag (assembled,
  sha256 beac899a137981b951393e162d05791b4d8c4bf95ce27ab04e24f0ea03792834),
  build.sh (guard + checks + build + 3x run)
- cr_bin (compiled binary, sha256
  bdfde9649cef0af41f503fd17338704536e45f3407450fbc99fbbcb4b37fc919),
  compile.txt
- run1.txt, run2.txt, run3.txt, sha256sums.txt
- REPORT.md (this file)

All commits local only, explicit pathspecs, nothing pushed.
