# REPORT: LCONT-1 -- Learned Contracts from Failure

Verdict: **LCONT-1-BUILD-PASS** (K0..K6 all pass).
Date: 2026-10-03. Worker: LEARNED-CONTRACTS (subagent).
Lane: `docs/lab/research-lead/overnight-20260928/learned_contracts/`.
Prereg: PREREG.md (frozen kill bars K0..K6), committed alone as
6b82590dd before any implementation existed. Implementation:
src/lcont.zag (pure Zag, pinned znc via safebin). Binary:
bin/lcont. Runs: runs/lcont-run{1,2,3}.txt, sha256
45bfba7a30a0c3d9f9a64cefd4c52267d402e186e8179ee20c10b656f7c6220f,
3/3 byte-identical.

## What was tested

Whether a learner can acquire its own type system from experience.
The learner composes structures (opaque ids 0..5) into two-step
pipelines F(G(x)) against goals (x, y*). Contracts are (in-kind,
out-kind) per structure; kind 0 means universal/unknown. Selection is
contract-gated plus evidence-max, committed with no search. The four
stages ran in two worlds (world B permutes behaviors across ids by
pi = [4,5,0,1,2,3], undisclosed to the learner).

## Results by kill bar

- K0 (genuine insufficiency) PASS both worlds: at stage B the outer
  candidate set after contract filtering was all 6 structures
  (cand=6; the coarse contract filtered nothing), and the selected
  outer (world A id 1, world B id 3) never produces y*=0 on any probe.
  The selector did the reasonable thing (trust evidence from stage A);
  the coarse contract gave it no other information channel.
- K1 (failure) PASS both worlds: stage B goal (7,0) executed
  DBL(DBL(7)) = 28, not 0. FAIL as predicted, deterministically from
  the evidence landscape, not from tie-break luck (the chosen outer
  had strictly maximal evidence).
- K2 (refinement) PASS both worlds: REFINE split kind 0 into exactly
  6 kinds (kinds=6), one per behaviorally distinct signature; the two
  structures whose probe outputs lie in {0,1} hold kinds disjoint
  from the other four (sep=1). Every kind boundary corresponds to an
  observed signature disagreement; the trace prints all six
  signatures and assignments.
- K3 (permutation control) PASS: the six-signature multiset in world B
  equals world A's (sigmultiset=1), while the {0,1}-output id set
  differs ({0,1} vs {4,5}, idsetdiff=1). The kind partition tracks
  observed behavior across the permutation, not ids.
- K4 (post-refinement success) PASS both worlds, 3/3, with the
  stage-B SELECT code path unchanged: (7,0) retry OK, (2,0) OK,
  (4,18) OK (no regression on the old family). The only thing that
  changed between stage B and stage D is the contracts, so the
  refined contract is load-bearing for the success.
- K5 (determinism) PASS: 3/3 byte-identical runs (sha256 above).
- K6 (no researcher leakage) PASS: grep audit shows PREREG.md
  contains no mapping from structure ids to refined kind ids (only
  kind 0, the preregistered coarse start state, is named); learner
  code uses ids only, with no INT/BOOL/PLAN/CAUSAL/LANGUAGE/AUDIO or
  family labels; the prereg commit (6b82590dd) contains exactly
  PREREG.md + NAMECHECK.md and strictly precedes implementation.

## The refinement, white-box

Stage B failure (world A): outer id 1 on inner value v=14 produced
28, needed 0. REFINE replayed all six kind-0 structures on v=14 and
compared full signatures (8 probes + replay). All six signatures
were pairwise distinct, so kind 0 split into six fresh opaque kinds
(k=1..6 in member order). In world B the same procedure, on permuted
ids, produced the same six signatures grouped identically. The
grouping was computed from the learner's own probe executions; the
researcher supplied the partition procedure but no outcome.

## Why the refinement counts as learner-driven

Three independent legs: (1) the prereg specified the procedure, not
the outcome, audited by grep; (2) the permutation control shows the
outcome follows behavior across ids; (3) the trace exposes every
boundary as an observed disagreement. A hardcoded-by-id alternative
is ruled out by (1) and (2) jointly.

## Honest scope and limits

- Claim level is L2 structural learning, not L3: the refinement
  procedure is researcher-supplied generic machinery; what the
  learner determined is which kinds exist and which structures share
  them.
- The refined partition here is maximally fine (singletons). The
  experiment shows behavioral grounding of kinds, not that coarser
  useful groupings emerge; coarser emergence would need a merging
  pressure, which is future work.
- One failure plus probes sufficed because structures are
  deterministic and probes are cheap. Noisy or stochastic behavior
  would need an evidence-accumulating variant.
- in-kind stayed universal (0) throughout; only out-kind refined.
  Input-side contract learning is not tested here.

## Commits

- 6b82590dd: prereg alone (PREREG.md + NAMECHECK.md).
- This report commits src/lcont.zag, bin/lcont,
  runs/lcont-run{1,2,3}.txt, REPORT.md with explicit pathspecs.
  Local only, never pushed.
