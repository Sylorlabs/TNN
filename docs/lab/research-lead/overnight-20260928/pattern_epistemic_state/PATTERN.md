# PATTERN: Epistemic-Structural Separation (ESS)

**Worker:** PATTERN-EPISTEMIC-STATE subagent, 2026-10-03.
**Lane:** docs/lab/research-lead/overnight-20260928/pattern_epistemic_state/
**Status:** Non-ledger task (claim minting paused). Documentation only.
No mechanism code modified.
**Prereg:** frozen alone at commit b16effd25 (PREREG.md + NAMECHECK.md);
this file written after.
**Style:** hyphens only, no em/en dashes.

## 0. Name

**Epistemic-Structural Separation (ESS).** The pattern: a learner
structure's EXISTENCE in learner state and the learner's EPISTEMIC
STANDING toward that structure are two different records, written by
different causal paths, and they can diverge.

Rejected alternatives:

- "Endorsement-Existence Split": alliterative, but "endorsement"
  biases toward the belief-layer flavor (claims about the world)
  and misdescribes SUF's second-order grading (determination of
  the learner's own form). Fails the prereg's mechanism-neutrality
  requirement.
- "Belief-Structure Duality": centers "belief", which the
  compression analysis keeps as one mechanism's proper name; using
  it for the pattern reintroduces the subsumption-by-redefinition
  the NON-DUP verdict rejects ("belief" stretched to mean "any
  learner-owned record" made the merge vacuous). "Duality" also
  wrongly suggests symmetry; the relation is asymmetric (E is
  about S).

## 1. The pattern, precisely

For a mechanism M, ESS holds when M maintains, in learner state:

- **S, the structure.** A node, graph, procedure body, clause set,
  or contract the learner constructed or holds. S's existence is
  checkable independently of any grading: S occupies learner
  state, and an existence predicate answers yes.
- **E, the epistemic record.** A record (scalar, counter, set,
  flag, bitmask) that is ABOUT S's standing: whether S's claim
  holds, whether S's content is determined, whether S applies in
  a context, whether S is trusted. E is written by a causal path
  distinct from S's construction: different write sites,
  different update rules, different evidence inputs. E
  accumulates evidence S's bytes alone do not carry (runs,
  falsification events, disconfirmations, provenance liveness,
  consequence history).

And the two can DIVERGE: S exists while E withholds endorsement
(the canonical divergence), or S's bytes persist while E records
retirement, and M's observable behavior (selection, prediction,
use, probing) differs from what S-alone would dictate. E gates,
blocks, redirects, or escalates.

What ESS is not: a transient per-query check with no persistent
record; a researcher-set control flag never written by the
learner; graded state about the world regime rather than about
a learner structure; a deterministic recomputation of S's fields
at read time.

Note the order distinction the compression analysis draws
(ANALYSIS.md section 5): beliefs are FIRST-order epistemics
(endorsement of claims about the world); SUF records are
SECOND-order epistemics (the learner's graded state about its
own representation). Both are ESS instances. Granularity and
order differ; the pattern is the same.

## 2. Canonical instance 1: the belief layer

Source: belief_provenance/DESIGN.md sections 2-6; verified against
in the compression model (ANALYSIS.md sections 2-3).

- S: claim-bearing nodes. B-FACT (tag-1 fact nodes: "(s, r, v)
  holds"), B-STRUCT (tag-20 MAPs: "count MAP over (s, r) yields
  v"), B-COMP (MAP_Z composites), B-META (meta-rows: "provenance
  profile X beat profile Y"). The node exists; its claim is read
  from its fields.
- E: the belief record per node id. b_sup/b_conf scalars with
  update rules R1-R7: R2 adds INC_HI/INC_LO saturating at 255
  (corroboration runs), R3 subtracts DEC floored at 0 (TEST
  disconfirmation), R4 scales with licensing liveness (type-1
  provenance), R5 halves on revision, R6 takes the min over
  type-14 successors (network propagation with fixpoint
  dynamics), R7 selects argmax eff among candidates and abstains
  (-3) below a learner-adjusted bar.
- The separation is the design's central move (DESIGN.md section
  2): "today 'structure is live' and 'learner endorses its
  claim' are the same bit. They must become two different facts,
  because provenance can die while the structure lives (K3a) and
  structures can be reformed while old evidence is stale."
- Canonical divergence (compression T-B, K3a/S1 world): all
  type-1 licensing facts of a composite are tombstoned. The
  composite's bytes persist, but b_sup degrades to 0 and the
  structure is retired; R7 abstains. The structure exists; the
  endorsement is withdrawn. S-alone would keep predicting.

## 3. Canonical instance 2: SUF resolution records

Source: l3_suf_intermediate/L3_SUF_DESIGN.md; red-team report;
verified against in the compression model (ANALYSIS.md
sections 2-3).

- S: elements of the learner's own constructed form (query
  elements: pairs/triples of an intermediate the learner built).
  The element exists in the form.
- E: the per-element resolution record. States RESOLVED(v),
  UNRESOLVED, FALSIFIED-ALL. The state IS a surviving-value set
  (bitmask), shrunk by falsification; l_surviving is a pure
  function of commutative-OR-accumulated consequence-log flags.
  No runs, no saturation, no propagation. UNRESOLVED is
  explicitly represented: there is no code path from UNRESOLVED
  to a predicted value (fabrication impossible by construction),
  UNRESOLVED elements are probe targets, and form-scale
  FALSIFIED-ALL escalates (try ARITY-LIFT/GUARD/UNION/PROJECT in
  fixed order, adopt the first consistent composition) rather
  than terminating.
- Canonical divergence (compression T-A, RK-B world): the learner
  induces a form; evidentially unseen elements are tie-break
  filled. The form exists, but the record marks those elements
  UNRESOLVED and the mechanism ABSTAINs. The structure exists;
  the determination is withheld. S-alone (the filled form) would
  commit confidently-wrong (the belief layer in fact does:
  b_sup=130, R7 SELECT=1 on the same world).

Note the cross-divergence, which is why neither mechanism
subsumes the other: belief-E can distrust what SUF-E trusts
(T-B), and SUF-E can distrust what belief-E trusts (T-A). Two
different separations, both ESS.

## 4. Why it matters: what goes wrong if you conflate them

Conflation = treating "exists in learner state" as "trustworthy"
(a single bit doing both jobs). Five failure modes, each
demonstrated:

1. **Fabrication (T-A).** If existence implies trust, a form with
   tie-break-filled interior elements commits confidently-wrong
   (RK-B: 0/6). The SUF record exists precisely to block this:
   UNRESOLVED is an explicitly represented state with no path to
   a predicted value.
2. **Zombie use (T-B).** If determination implies endorsement, a
   structure whose licensing has died keeps predicting (the K3a
   failure: dead composite used silently, wrong-relation). The
   belief record exists to withdraw endorsement while the bytes
   persist.
3. **Retirement becomes destruction.** Without the separation,
   the only way to stop using a structure is to delete it, which
   destroys what revision and diagnosis need. ESS keeps both:
   belief R5 HALVES on revision rather than deleting; the
   contract module REVISES from post-change data rather than
   discarding; SUF ESCALATES on form falsification rather than
   terminating. Distrust must be reversible by new evidence (R2
   re-accumulates; U6's strike counter resets on confirmation).
4. **Loss of directed action.** E does not only gate; it directs.
   SUF probes target UNRESOLVED elements; U6 retires specific
   stale bits (RETIRE=m,p,k in the learner's own trace). A single
   existence bit cannot carry a probe target or a per-bit
   retirement.
5. **Category destruction.** Folding the record into machinery
   reclassifies a learner invention as machinery and destroys the
   L3 claim under test (ANALYSIS.md section 5): the SUF record's
   FORM (that UNRESOLVED needs explicit representation) is the
   invention being adjudicated. "Just add it to the belief layer"
   is subsumption by redefinition.

## 5. Survey results

Applied the frozen criteria (PREREG.md section 2) to the frozen
survey list (section 3). Citations are to frozen lane artifacts;
no code was read beyond what the lanes' own documents cite.

| # | Mechanism | Verdict | S (structure) | E (epistemic record) | Divergence / exclusion |
|---|---|---|---|---|---|
| 1 | Belief layer | INSTANCE (canonical) | Claim-bearing nodes: B-FACT/B-STRUCT/B-COMP/B-META | b_sup/b_conf per node id; R1-R7 update algebra | K3a world: licensing tombstoned, node persists, b_sup=0, retired, R7 abstains |
| 2 | SUF resolution records | INSTANCE (canonical) | Elements (pairs/triples) of the learner-built form | Per-element surviving-value set; RESOLVED(v)/UNRESOLVED/FALSIFIED-ALL | RK-B world: form exists with filled interior, elements marked UNRESOLVED, ABSTAIN; probes targeted at UNRESOLVED |
| 3 | Unified contract module C424 (GEN+LCONT+FC lineage) | INSTANCE | Contract: consumes (NFIELDS), produces (judgment semantics), constraint-clauses (field, xform, k, lo, hi, active, dc) | Per-clause disconfirmation counter dc; contract-level consecutive-failure run C_FAIL_RUN; ops induct/check/grow/invalidate/revise | Clause structurally present but dc=2 retires it (active=0, U6-style); 3 consecutive verification failures latch CONTRACT_REVISE_REQ and trigger post-change refit. Lineage: GEN kind-set masks (structural admission filter) with success-recording growth (epistemic record of observed kinds); LCONT 3-failure drift latch; U6 per-bit disconfirmation counters retiring stale ledger bits at 2 consecutive disconfirmations (C352). The compression audit's own words: "a contract is a promise acted on with a verifier comparing commitment vs consequence" (promise = S, verifier's accumulated verdict = E). Sources: contract_unify/PREREG.md, contract_unify/REPORT.md, composition_synthesis/COMPOSITION_SYNTHESIS.md, compression_audit/COMPRESSION_AUDIT_MECHANISMS.md |
| 4 | COGOPS learner applicability record | INSTANCE | Procedure bodies as learner-owned structures: vfy_gen (id 0, generic) and vfy_spec (id 1, specialized) | Learned applicability record (coverage index / working set of encountered relations) selecting original vs revised per query context, with fallback to the original when the revised does not cover the query | vfy_spec exists in learner state but the applicability record says "not covered for this context": the structure is present but not endorsed for this use. Selection is a coverage lookup in learner state, not mode dispatch. Sources: cognitive_ops_learner/PREREG.md, REPORT.md |
| 5 | FC clause registry alone (pre-contract-module) | NON-INSTANCE (informative) | Clauses written via reg_write into the learner registry; checked via reg_check | None: formal_constraints/fc_main.zag (547 lines) contains zero counter/disconfirmation fields; clauses are purely structural admission filters | Fails C2/C5. The epistemic layer arrived only when FC's clause ABI was absorbed into the C424 contract module, which added active/dc/C_FAIL_RUN. A registry of constraints is not an ESS instance until something tracks the clauses' standing. This shows the pattern is not automatic. |
| 6 | SPEC policy lanes (spec_driftrate_sweep, spec_l_discipline, spec_lazy_default, siblings) | NON-INSTANCE | (No learner structure is the object of grading) | EWMA drift-density estimates, flip/commit rules, lazy-vs-eager policy arms | Exclusion X3: the graded state is about the WORLD regime (drift/query rates), not about a learner structure's claim. The policy arms are researcher-authored machinery, not learner-owned records. Near-miss noted and rejected: the lazy wrapper's refuse-on-stale-epoch is a transient per-query check (X1), not a persistent record. |
| 7 | L2 adaptive-reuse operators | NON-INSTANCE | Adapted structures produced by COMBINE/SUBSTITUTE/TRUNCATE | None persistent | Exclusion X2: OP_MASK is explicitly "a driver-set causal-control flag... never written by the learner" (l2_adaptive_reuse/REPORT.md). Operator selection is by runtime execution/verification, not by a stored epistemic record. An L2 operator lane COULD grow an ESS record (e.g. per-operator applicability learned from verification history); none surveyed has one. |

Score: 4 instances (2 canonical + contract module + COGOPS
applicability), 3 non-instances (1 informative negative, 2 clean
exclusions). No BORDERLINE classifications were needed; the
criteria discriminated cleanly.

## 6. Usage: the "name once" rule

Per the compression recommendation (ANALYSIS.md section 8), the
point of naming ESS is that future mechanisms reuse the pattern
deliberately instead of rediscovering it. Concretely, a new
mechanism's design should state:

- whether it keeps an ESS record, and if so its exact fields
  (the S and the E, with write sites);
- the divergence scenario it guards (the T-A/T-B analogue: what
  world makes S and E disagree, and what behavior must result);
- which exclusion it does NOT fall into (why its record is not
  transient, researcher-set, regime-about, or a recomputation).

Naming the pattern licenses none of the following: merging two
mechanisms because both are ESS instances (the NON-DUP verdict
stands: shared pattern is not shared decision logic); calling any
graded scalar a belief; treating a clause registry or an operator
menu as epistemically graded without a record.

## 7. Open questions (not claimed)

- Should every learned structure that persists across episodes be
  REQUIRED to carry an ESS record, or are there structure classes
  where existence-may-imply-trust is safe? The survey suggests
  the requirement tracks action risk: structures acted on
  (selected, predicted from, composed) need E; purely passive
  indexes may not.
- The contract module and the belief layer both keep
  disconfirmation-shaped counters (dc vs R3 DEC) with different
  algebras (eliminative retirement vs saturated scalar). Whether
  one update algebra can serve both without losing the
  fabrication-blocking or propagation properties is the P3
  substrate question, still open.
- L2 operators are the conspicuous absence: adaptation without a
  standing record. If an operator lane adds per-operator
  applicability learned from verification history, that record
  would be ESS instance #5 by the frozen criteria.

## 8. Provenance and governance

- Prereg commit: b16effd25 (PREREG.md + NAMECHECK.md alone; no
  analysis artifact existed). This file written after.
- No mechanism code modified. Only lane files created.
- Evidence is documentary: citations to frozen lane artifacts
  listed in section 5. No new binaries, builds, or runs.
- Toolchain: no computational research operation performed; no
  interpreter invoked (NAMECHECK.md Step 0).
- Non-ledger task: nothing minted.
- Commits local with explicit pathspecs; never pushed.
