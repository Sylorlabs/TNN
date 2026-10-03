# PREREG: PATTERN-EPISTEMIC-STATE (frozen)

**Lane:** docs/lab/research-lead/overnight-20260928/pattern_epistemic_state/
**Date:** 2026-10-03
**Status:** Non-ledger task (claim minting paused). Documentation only.
Local commits only, never pushed.
**Style:** hyphens only, no em/en dashes.

## 1. Question

BELIEF-SUF-COMPRESSION (verdict NON-DUP, 2026-10-03) named an honest
partial overlap P1: "shared design pattern (epistemic state distinct
from structural existence) worth naming once." This lane documents
that pattern precisely, proposes a name, and surveys other mechanisms
for further instances. This is pattern-naming and shared vocabulary,
not implementation. No mechanism code is modified.

## 2. Frozen instance criteria

A mechanism M counts as an INSTANCE of the pattern iff all of
C1-C5 hold. Classification is per mechanism, evidenced by citations
to frozen lane documents and exact record fields.

- C1 (identifiable structure S): M keeps, in learner state, a
  structure S the learner constructed or holds (node, graph,
  procedure body, clause set, contract). Structural existence is
  checkable independently of any grading: S occupies learner state
  and an existence predicate answers yes.
- C2 (separate epistemic record E): M keeps, in learner state, a
  record E (scalar, counter, set, flag, bitmask) that is ABOUT S's
  standing: whether S's claim holds, whether S's content is
  determined, whether S applies in a context, whether S is trusted.
  E is written and read by a causal path distinct from S's
  construction: different write sites, different update rules,
  different evidence inputs.
- C3 (learner-ownership): both S and E live in learner state, not in
  transient locals of researcher-authored policy arms. E persists
  across the decisions it informs.
- C4 (demonstrable divergence): there is a reachable world/history
  in which S exists while E withholds endorsement (the canonical
  divergence), or S is degraded/retired while its bytes persist,
  AND the mechanism's observable behavior (selection, prediction,
  use, probing) differs from what S-alone would dictate: E gates,
  blocks, redirects, or escalates.
- C5 (non-triviality): E is not a deterministic recomputation of
  S's current structural fields at read time. E accumulates
  evidence that S's bytes alone do not carry (runs, falsification
  events, disconfirmations, provenance liveness, consequence
  history).

Exclusions (any one disqualifies):

- X1: transient per-query checks with no persistent record
  (a check computed and discarded within one decision).
- X2: researcher-set control flags never written by the learner
  (driver-set masks, arm selectors).
- X3: graded state about the WORLD regime rather than about a
  learner structure (regime estimators, cost accounting); the
  pattern is about the learner's epistemic stance toward its OWN
  structures.
- X4: scalar summaries are NOT excluded by being scalar; what
  matters is C2-C5. But a summary that loses the property being
  graded in a way that breaks the gate (popcount where the
  per-element partition is load-bearing) is noted as a weakened
  instance, not a full one.

## 3. Frozen survey list

Each is classified INSTANCE / NON-INSTANCE / BORDERLINE with
field-level citations and the divergence scenario (or the reason
for exclusion):

1. Belief layer (belief_provenance/DESIGN.md, sections 2-6).
2. SUF resolution records (l3_suf_intermediate/L3_SUF_DESIGN.md).
3. Unified contract module C424 (contract_unify/PREREG.md,
   composition_synthesis/COMPOSITION_SYNTHESIS.md,
   compression_audit/COMPRESSION_AUDIT_MECHANISMS.md).
4. COGOPS learner applicability record
   (cognitive_ops_learner/PREREG.md, REPORT.md).
5. FC clause registry alone, before the contract module
   (formal_constraints/REPORT.md, fc_main.zag).
6. SPEC policy lanes (spec_driftrate_sweep/, spec_l_discipline/,
   spec_lazy_default/ and siblings: EWMA estimator, flip/commit
   rules, lazy wrapper).
7. L2 adaptive-reuse operators (l2_adaptive_reuse/REPORT.md,
   l2_*_xdomain lanes).

No other mechanism may be added to the survey after this commit
without a dated amendment committed before use.

## 4. Deliverables (frozen)

- PATTERN.md: the precise pattern statement (S, E, the separation,
  the divergence), the two canonical instances with concrete
  field-level examples, why conflation fails (citing the
  compression analysis T-A/T-B cross-failures), the survey table
  with classifications and citations, and the proposed name with
  rationale.
- Name proposal: exactly one primary name plus at most two
  considered-and-rejected alternatives with reasons. The name must
  be mechanism-neutral (not "belief-like", not "SUF-like").

## 5. Constraints

- Documentation only. Zero mechanism code modified; verify with
  git status before each commit (only lane files may change).
- No new binaries, no builds, no runs. Evidence is documentary:
  citations to frozen lane artifacts.
- Prereg commit-order self-check: this PREREG.md is committed
  ALONE before any analysis artifact exists. PATTERN.md may be
  written only after the prereg commit hash is recorded.
- Non-ledger task: nothing minted.
- Commits local with explicit pathspecs; never push.
