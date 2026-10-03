# RESULT: L3C v3 Alternative-Cover Dispatch (L3C-V3-PASS, with one disclosed prereg miss)

Date: 2026-09-30. Prereg: PREREG_L3C_V3.md (frozen, committed alone as
3124d2e9a, strictly before any implementation). Implementation:
l3c_v3.zag, built from the frozen v2 mechanism (20705ab5a, lines 1-771)
plus the cover-search machinery. Pure Zag, zero Python. Determinism 3/3
byte-identical (run1/run2/run3 sha256 30d7c0fd...; mode-0 ablation
cbb2a358...).

## Verdict

L3C-V3-PASS. The v2 disjunction blind spot is closed without any dedicated
OR case: F2 builds a correct two-edge cover dispatch with 4/4 truth eval.
One prereg analysis miss is disclosed below (P4); the mechanism behaved
correctly in every family and the miss was in the frozen prediction, not
the implementation.

## Results vs frozen predictions

- P1 F2 (sig 702): PASS exactly. Trace: HONEST_FAIL, HONEST_FAIL,
  BUILT_COVER sig=702 ncover=2. built_delta=1, unresolved_delta=2,
  truth_eval=4/4. Structure: rule(702) is DISP with exactly 2 labeled
  edges, atoms (1,0,1) and (2,0,9), both targeting TERM(0), and 1 default
  edge targeting TERM(2). All structure checks pass. The blind spot is
  closed: F2 no longer HONEST_FAILs, with no OR semantic case anywhere.
- P2 MEM (sig 704): PASS exactly. 3 HONEST_FAILs, built_delta=0,
  rule(704) still TERM(2). The per-element EVID_MIN=2 bar blocked every
  singleton memorization atom. No spurious cover built.
- P3 AMB (sig 705): PASS exactly. HONEST_FAIL, HONEST_FAIL,
  AMBIGUOUS_COVER sig=705 k=2. built_delta=0, ambig_delta=1, rule(705)
  still TERM(2) with ambig field = 2. Symmetric evidence honestly
  withheld, not composed by fiat.
- P4 MIN (sig 706): PREREG ANALYSIS MISS, disclosed. Predicted
  HONEST_FAIL x2 then BUILT_COVER ncover=1. Observed: BUILT sig=706
  natoms=1 at clash_n=2 via the DIRECT path, 0 unresolved, truth_eval=4/4,
  all structure checks pass (rep natoms=1, atom (1,0,1), 1 labeled edge).
  Cause: the prereg analysis forgot that disc2 runs before disc_cover,
  and (f1==1) satisfies the all-instances criterion for both contradiction
  rows, so the direct path fires first, exactly as v2 would. The mechanism
  did the correct thing; the prediction was wrong. Architectural
  consequence: size-1 covers are subsumed by the direct path, so
  disc_cover minimality only ever discriminates among multi-atom covers.
  A genuine minimality-vs-memorization cover-path test (corroborated
  singleton atom losing to a smaller cover) remains untested and is left
  for a follow-up builder under a fresh prereg. The bar was not moved:
  the miss is recorded as a miss.
- P5 F1 (sig 701): PASS exactly. built_delta=3, eval 4/4, D1-D2-D3 chain
  with atoms (1,0,1), (3,0,9), (2,0,2), all DISP. Cover fallback never
  fired.
- P6 F3 (sig 703): PASS exactly. built_delta=2, eval 5/5, D1 default edge
  repointed to DISP with labeled atom (3,0,9). Cover fallback never fired.
- P7: PASS. 3/3 byte-identical; zero Python; dash-clean; contaminated
  paper untouched.

## Kill bars

K1: PASS. Prereg commit 3124d2e9a strictly precedes the implementation
commit (sequential commits on the same branch; merge-base verified
below). Implementation and results committed only under
docs/lab/research-lead/overnight-20260928/l3c_v3/ with explicit
pathspecs.
K2: PASS with the disclosed P4 analysis miss. P1 built correctly with 4/4
truth eval (F2 no longer HONEST_FAILs); P2 produced no spurious cover;
P3 withheld with exactly k=2; P5/P6 regression exact. P4 built the
predicted structure (natoms=1, atom (1,0,1)) with 4/4 truth eval via the
direct path; the trace-name/unresolved-count prediction was wrong and is
recorded as a prereg miss, not a mechanism failure.
K3: PASS. Interpreter diff EMPTY: featv, pred_match, select_edge, interp,
trace_last_edge, path_uses are byte-identical to the committed v2 source
(20705ab5a). Zero new semantic cases, modes, bridges, task-specific
handlers, interpreter ops, node kinds, or edge kinds. Pure Zag.
Dash-clean. Contaminated paper untouched.

## Architecture delta (ONE-SYSTEM RULE record)

- Cognition source lines added (mechanism): +269, 1 line modified
  (variable rename in the intended try_refine tail), 0 removed.
- New hardcoded semantic cases: 0.
- New modes: 0.
- New bridges: 0.
- New task-specific handlers: 0.
- New interpreter ops / node kinds / edge kinds: 0.
- Interpreter delta: 0 lines (verified byte-identical).
- The new machinery is the general learning operation of cover-set
  composition (disc_cover + build_cover), reusing the interpreter's
  existing union semantics. Not disjunction-specific: the same operation
  unions conjunctions, inequalities, or any future atom type.
- Learner-state structures created at runtime: F2 multi-edge dispatch
  node (1 DISP, 2 labeled edges to shared TERM(0), 1 default to TERM(2));
  MIN direct-path dispatch. COVER/CAND buffers are search workspace, not
  persistent cognitive structure.
- Standing-question answer: the existing architecture could not learn
  this behavior because the search criterion demanded one all-satisfying
  atom and the builder emitted one labeled edge per node. The missing
  piece was the general operation of cover-set composition, now supplied
  without any new semantic case.

## Ceiling and open items

Bounded L2, as before. Cover-search combinatorics: exhaustive subset
enumeration is capped at 12 candidates and cn at 30 (disclosed bounds);
a scaled-up learner needs a greedy bound with a disclosed approximation
gap. Ambiguity explosion: cover sets multiply faster than single
separators, so AMBIGUOUS_COVER withholds more often; that is the honest
outcome but it bounds the capability. 2-conjunctions remain
direct-path-only (frozen bound). The minimality-vs-memorization
cover-path test is untested (see P4). Recommended next: independent red
team attacking sparse-history worlds against the EVID_MIN/minimality
bars, then integration pressure toward the one continuing learner.
