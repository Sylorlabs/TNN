# DDES Integration Result

Date: 2026-09-30. Pure Zag. Prereg frozen in commit c3fecd3c8 BEFORE any
implementation file existed.

## Verdict: DDES-INTEGRATION-PASS

The continuing learner's causal path now routes AMBIGUOUS entries through
DDES construction instead of withholding only. The integrated learner
constructs exactly one discriminating intervention, executes it exactly
once, and resolves the entry from the real outcome. All three kill bars
pass.

## What was built

File `ddes_integ.zag` (pure Zag, zero Python). One continuing process
holds a persistent causal ledger across sequential experiences
(e0, e1, e2). Each entry carries two competing hypothesis rule graphs.
Both consistent with passive evidence plus a disagreement frontier ->
AMBIGUOUS. Hypotheses identical -> ACTIVE.

- Mode 0 (BASE, un-integrated learner): AMBIGUOUS entries stay ambiguous;
  queries emit WITHHOLD (ambiguous).
- Mode 1 (INTEG, integrated learner): an AMBIGUOUS entry at feed time
  triggers the DDES derivation path copied verbatim from the frozen
  sources (compute_arrivals, compute_frontier from ddes.zag at
  56db8d606; eff_waits, synthesize_plan_gen, predict_gen, world_step_gen
  from ddes_gen.zag at 843c45fee): two-schema arrival analysis, earliest
  frontier (V*, t*), exactly one synthesized plan, exactly one real
  execution against the sealed true world, elimination from the outcome,
  exactly one survivor required, entry set ACTIVE with the winner.

## Frozen ambiguity case (test a and b)

Entry e2: h0 = [(X->Y,1)], h1 = [(X->Y,2)], passive (Y,2) = 1 (both
consistent), sealed true world = h1.

(a) Un-integrated learner (MODE=BASE):
```
FEED e2 nh=2 passive=(1,2)=1
ENTRY e2 AMBIGUOUS cands=2
Q e2 (1,1) -> WITHHOLD (ambiguous)
```
The base learner withholds. SUMMARY mode=BASE ok=4/4 resolved=0.

(b) Integrated learner (MODE=INTEG):
```
ENTRY e2 AMBIGUOUS cands=2
INTEG e2 TARGET V*=1 t*=1 schema=1
INTEG e2 PLAN [S,W,O(1)] built=1
INTEG e2 EXEC real=0
INTEG e2 PRED h0=1 h1=0
INTEG e2 ELIM h0
INTEG e2 SURVIVE h1
INTEG e2 RESOLVED winner=h1
Q e2 (1,1) -> 0
Q e2 (1,2) -> 1
```
SUMMARY mode=INTEG ok=6/6 resolved=1. Every frozen prereg expectation
holds: target, plan, real outcome, predictions, elimination, winner,
post queries.

## Genuinely discriminating (test d)

The two hypotheses' analytic predictions at the derived frontier are
shown side by side: PRED h0=1 h1=0. The single real execution returns
real=0, matching exactly one hypothesis (h1); the other is eliminated.
No enumeration occurred (built=1, one plan assembled from (V*, t*,
schema)); no length bound exists in the derivation path.

## No regression (test c)

The 7 P1/P2 output lines (e0/e1 FEED, ENTRY, Q lines) are byte-identical
between the MODE=BASE and MODE=INTEG sections. Verified by shell diff on
the extracted sections: diff exit 0, empty output, recorded in
NOREGRESS_DIFF.txt.

## Determinism

3/3 runs byte-identical, md5 cc62047dc6b2161558a9e4517658de0a. Exit 0,
zero stderr on all runs (RUN1/2/3.txt, RUN1/2/3.err).

## Kill bar verdicts

- K1 (prereg precedence): PASS. Prereg commit c3fecd3c8 strictly
  precedes the implementation commit; verified with
  git merge-base --is-ancestor.
- K2 (resolution plus no regression): PASS. (a) base withholds on the
  frozen ambiguity query; (b) integrated constructs exactly one plan,
  executes exactly once, eliminates exactly one hypothesis, resolves
  winner=h1, both post queries correct; (c) P1/P2 lines byte-identical
  between modes (shell diff clean).
- K3 (purity and determinism): PASS. Pure Zag, zero Python at every step
  (implementation, build, runs, checks); 3/3 byte-identical; zero
  em/en dash bytes per shell-only check_no_dash.sh; exit 0, zero stderr.

## Classification

Bounded L2 integration. NOT L3. Researcher still owns: hypothesis
format, the frozen case set, the derivation algorithm, action
vocabulary. The learner authors: the intervention decision on ambiguity,
the observed variable, plan length, the full sequence, and the
resolution from the real outcome. This closes the arena audit gap
"genuine causal inference (DDES not integrated)" at the mechanism level;
arena re-entry is a separate measurement.
