# REPORT: FORMAL KNOWLEDGE CONSTRAINING BEHAVIOR (formal_knowledge)

Worker: FORMAL-KNOWLEDGE. Date: 2026-10-03. Non-ledger task (claim
minting paused). Branch: tnn-native-lab. Commits local only, never
pushed. Lane:
docs/lab/research-lead/overnight-20260928/formal_knowledge/

## 1. Question

Micah's overnight priority #6, from the constitution section 7 (TRUE
UNDERSTANDING MUST HAVE CONSEQUENCES): "If TNN genuinely understands
a formal system, that understanding should constrain behavior...
certain classes of error should disappear when the relevant formal
knowledge is complete and actively used. Design experiments around
this."

Current state: knowledge is STORED (MAPs, beliefs with provenance,
contracts, judgments) but does not CONSTRAIN. The concrete question:
what mechanism makes a learned formal fact render an error
IMPOSSIBLE rather than merely unlikely? Example from the task: if
the learner knows "key X is unique", then "insert duplicate X"
should be impossible, not just avoided.

## 2. Survey: what formal knowledge exists today (tested, from lanes)

- **contract_unify** (verdict CONTRACT-UNIFICATION-SUBSUMES): a
  learned contract is (consumes, produces, constraint-clauses,
  confidence); one module provides induct, check, grow, invalidate,
  revise. `check` serves as both admission (grammar composer) and
  commitment (drift loop). Constraint content is learner-built from
  judgments via minimal-commitment Occam search over a fixed
  11-feature library. But the CALL SITE is harness/researcher
  written; nothing forces the learner to consult it.
- **formal_constraints** (verdict FORMAL-CONSTRAINTS-COMPLETE): the
  wiring-dependence analysis is the critical result. Learner-built
  channel CONTENT constrains generation (Arm L 6/6) but the ABI and
  the composer's consultation of it are researcher-defined, and Arm N
  proves the consequence of removing the wiring: the 12 judgments
  sit inert and generation is unconstrained (0/6). Knowledge without
  a channel does nothing.
- **belief_provenance_2** (verdict BP-2-PASS): beliefs carry
  (support, confidence, disconfirmation, revision, provenance)
  and R7 selection can abstain (-3). This is still ADVISORY:
  a belief guides selection; it cannot block an action.
- **mint_guard** (design only): a pre-commit gate that would have
  blocked all 9 historical ledger wipes plus the empty commit
  (retrospective test: every incident BLOCKED, positive controls
  PASS). This is the closest existing instance of the target
  pattern: formal knowledge (append-only invariant, entry shape,
  TIP chain) making an error class impossible. Its disclosed
  limitation: it is governance (a script workers are told to run),
  not mechanism; a worker can bypass it.
- **domain_blindness** (verdict PASS blind): the rename-and-compare
  battery proving a mechanism's decisions are invariant to human
  identifiers. The procedure ports directly to constraint testing.

Summary of the gap: every existing lane stores formal knowledge and
consults it optionally. None makes violation structurally
impossible. mint_guard shows the pattern works but lives outside
the learner's execution path.

## 3. Definitions

**Formal knowledge** (for this design): a constraint record in
learner state with EXACT satisfaction conditions, as opposed to a
belief with a confidence number. A belief says "MAP_Z2 is probably
the right composite". A constraint says "no second entry with key 5
can exist in store S". The difference is verifiability: given a
proposed state change, constraint satisfaction is decidable by a
fixed structural procedure with no judgment call.

A constraint record is (kind, scope, params, provenance, status):

- kind: one of a SMALL FIXED vocabulary of STRUCTURAL predicates:
  UNIQUENESS (at most one entry per key in a store), BOUND (field
  value within [lo,hi] under a feature xform), ACYCLIC (no directed
  cycle in an edge store), CARDINALITY (entry count within [lo,hi]),
  ORDER (rank(a) < rank(b) for linked pairs). These are about
  structure (equality, order, reachability, count), never about
  content. This is what keeps them domain-blind: renaming every
  domain identifier changes nothing about whether two keys are
  equal or whether a cycle closed.
- scope: an opaque structure id (which store / edge set / field).
- params: opaque field ids, feature xforms (identity/div/mod, the
  contract_unify library), ranges. No domain vocabulary.
- provenance: evidence counters (supporting judgments, consecutive
  disconfirmations, revision history). Same shape as BP-2 belief
  records; constraints are beliefs promoted to binding status by
  evidence, not a separate ontological kind.
- status: ACTIVE, RETIRED, or PENDING-REVISION.

**Three enforcement strengths** (this is the core taxonomy):

1. REPRESENTATIONAL: the invariant is encoded in the data
   structure itself. Illegal states are UNREPRESENTABLE. No check
   runs; there is nothing to bypass. Example: a key-addressed
   store where insert(k,v) IS write-to-slot(k); "a second entry
   with key k" has no encoding, so "insert duplicate k" is
   impossible the way "a second 5 in the set {5}" is impossible.
2. ADMISSIONAL: a gate sits inline on the action path. Every
   mutation op passes the registry check; a failing check returns
   a refusal sentinel instead of mutating. Bypass requires
   rewriting the action path, which is itself a gated mutation
   (see section 5).
3. ADVISORY: knowledge consulted at the actor's discretion. This
   is the current state of all lanes, and formal_constraints Arm N
   proved it is inert without wiring. The baseline to beat.

## 4. Mechanism design: BINDING CONSTRAINTS

### 4.1 The channel argument (why "impossible" is achievable)

Impossibility is always relative to an action channel. The design
commits the learner to a SINGLE action channel: a learner-owned,
persistent procedural structure G (the action root), executed via
the protected EXECUTE(root, frame) primitive. All of the learner's
state-mutating effects flow through EXECUTE(G, frame).

Within that channel:

- Representational constraints make violation UNENCODABLE: the op
  the adversary wants ("create a second entry with key k") has no
  realization in the structure. This is not a refusal; the request
  is well-formed and executes, and what it denotes (set the value
  at key k) is not a violation.
- Admissional constraints make violation UNEXECUTABLE: the gate is
  inline in G before the mutation op. There is no second route
  from intent to mutation inside the channel.

The honest boundary: this is impossibility WITHIN THE COMMITTED
CHANNEL, not metaphysical impossibility. A learner that abandons G
abandons its only coherent procedure for acting; G is not a
suggestion box, it is the learner's action procedure. The
alternative (a gate inside the protected ISA's LINK/WRITE so that
no learner code path can avoid it) would give absolute
impossibility but moves the wiring into the protected core, which
requires Micah's protected-core boundary decision (escalation
boundary). Flagged in section 9, not decided here.

### 4.2 Learner-built vs researcher-defined (the wiring map)

formal_constraints proved the content/channel split. The same split
applies here, deliberately:

- Researcher/protected (generic machinery, like the ISA):
  EXECUTE itself; the five structural predicate kinds; the
  revision protocol skeleton (disconfirmation counting, latch
  threshold as a parameter); the feature xform library.
- Learner-owned (intelligence, in what it builds): WHICH
  constraints exist; their params (induced from judgments by the
  contract_unify induct machinery); WHICH representation a store
  uses (list vs keyed vs rank-ordered); the action root G itself,
  including where gates sit; all provenance.

The learner therefore builds the channel that formal_constraints
showed it could not build before: not by being handed a composer
call site, but because its action root IS the call site. G is a
learner-created persistent procedural structure (the L3 target
class), and the gates are part of its body.

### 4.3 Induction path (concrete, reuses frozen machinery)

1. contract_unify's induct produces clause params from labeled
   judgments (accepts/rejects as experience). This already exists
   and is frozen-tested.
2. NEW (designed, not built): representation selection. When
   disconfirmations are attributed to duplicate-key failures (the
   invalidate machinery attributes a failed judgment to the
   responsible clause/store), and the failure mode is
   "duplicate entry committed", the learner migrates the store
   representation list -> keyed. The migration is itself a gated
   action requiring the disconfirmation evidence that motivated
   it. This is the learner promoting a repeatedly-violated
   advisory belief ("keys should be unique", learned from
   failures) into a representational constraint.
3. ACYCLIC for composition edges: the composition edge store is
   rank-ordered from the start (topological ranks assigned at
   link time); a link that would close a cycle has no valid rank
   and cannot be encoded. This directly serves overnight
   priority #1 (general DAG/fan-out/fan-in composition): with
   ACYCLIC representational, the composer can attempt fan-out and
   diamond assemblies freely because the dangerous error class
   (cycle creation) is impossible, not merely discouraged.

### 4.4 Revision protocol (binding but not dogma)

The drift lanes (contract_unify Arm D/C) proved constraints go
stale. A binding constraint that cannot be revised is dogma, not
knowledge. The protocol:

- Every ACTIVE constraint carries a disconfirmation counter
  (invalidate: judgment vs consequence mismatch bumps it).
- 2 consecutive disconfirmations retire the clause (U6-style, as
  in contract_unify); 3 consecutive latch a revision request.
- Removing or weakening a binding constraint, or migrating a
  store AWAY from a constraining representation, is a mutation
  that must flow through G's meta-gate, which requires the
  latched revision request. Without evidence the removal op is
  refused (prototype META: remove_noevidence=0). With evidence
  it proceeds (remove_withevidence=1) and re-induction runs.

So the learner cannot silently drop a constraint to make an
action convenient, but it is never permanently bound to a false
one. This is the difference from mint_guard's governance: the
gate is IN the execution path, not beside it.

## 5. Domain-blindness

Constraints are expressed only over opaque integer ids,
structural predicates (equality, order, reachability, count),
and feature xforms. The rename-and-compare battery from
domain_blindness ports directly: mechanically permute every
identifier in the world, the stores, and the constraint records;
the refusal pattern and final state must be byte-identical after
inverse mapping. Additionally a no-wire audit: grep the
constraint induction and gate source for domain vocabulary must
return empty (the formal_constraints K6 pattern). The five
predicate kinds are structural, not semantic: UNIQUENESS does
not know what a key MEANS, ACYCLIC does not know what an edge
MEANS. If Micah judges any predicate kind to smuggle domain
semantics, that kind is cut; the design does not depend on any
single one.

## 6. Prototype (TESTED)

fk_main.zag implements the mechanism pattern on the canonical
example: 200 adversarial insert attempts, keys cycling through
1..7 (coprime step, so 193 of 200 attempts are duplicates),
distinct values. Three arms plus the revision protocol.

Results (3/3 runs byte-identical, sha256
d6e33c374490cd24ccdb177d9b6c242e0c23786d952a0f0e493fa1db21155761,
stderr empty):

- FK-ARM LIST entries=200 dupkeys=193. No formal knowledge:
  the error class is fully possible. Baseline.
- FK-ARM REP entries=7 dupkeys=0 updates=193.
  Representational UNIQUENESS: the 193 duplicate attempts
  executed as updates; a second entry with the same key was
  never committed because it has no encoding. Zero is
  structural, not behavioral.
- FK-ARM GATE entries=7 dupkeys=0 refusals=193. Admissional
  UNIQUENESS: the gate refused all 193 duplicate ops before
  mutation.
- FK-META latch=1 remove_noevidence=0 remove_withevidence=1.
  Constraint removal without disconfirmation evidence is
  refused; with a latched revision request (3 consecutive
  disconfirmations) it is allowed.

Hand derivation matched exactly (LIST 200/193, REP 7/0/193,
GATE 7/0/193, META 0/1), so the binary's stdout bytes were
verified before trusting them, per the toolchain rule.

What the prototype does NOT test (reasoned, not tested): the
induction of the constraint from judgments, the list->keyed
migration step, multi-predicate interaction, and any claim of
generality. It is an existence proof of the mechanism pattern,
nothing more.

## 7. Falsifiable predictions

- P1 (representational impossibility): sealed adversarial world,
  10,000 insert attempts with 50 percent adversarial duplicates
  against a keyed store with ACTIVE UNIQUENESS: committed
  duplicate entries = 0 exactly. Control (list store): > 0.
  Prototype result at 200 attempts (0 vs 193) is the small-scale
  instance.
- P2 (admissional impossibility): same workload against the
  action-root gate: 0 committed, refusals = number of duplicate
  attempts. A gate-free variant of the same root: > 0 committed.
  This is the wiring-dependence test (mirrors FC K2/K5): it must
  show the constraint, not the world, does the work.
- P3 (revision binding): attempts to remove the ACTIVE
  constraint with 0 disconfirmations are refused (0/ N
  succeed); after 3 consecutive disconfirmations the removal
  succeeds and re-induction runs. Prototype META (0 vs 1) is
  the small-scale instance.
- P4 (stale-constraint recovery): world law changes so that
  UNIQUENESS becomes wrong (multiset semantics needed).
  Disconfirmations accumulate; the clause retires at 2
  consecutive; revision re-inducts; post-drift score recovers
  to at least 9/12 within contract_unify's budget. If the
  learner instead stays bound to the false constraint, P4
  fails and the design is refuted (dogma risk made testable).
- P5 (domain blindness): mechanical identifier permutation over
  world, stores, and constraint records; refusal pattern and
  final state byte-identical after inverse mapping; no-wire
  audit (domain vocabulary grep) empty.
- P6 (ACYCLIC for DAG composition): on the composition edge
  store, adversarial compose attempts that would close a cycle:
  0 cycles ever committed across the battery; acyclic
  diamond/fan-out/fan-in attempts proceed normally. Failure
  mode that refutes: any committed cycle, or any refused
  acyclic assembly.
- P7 (BOUND): with BOUND constraints induced from range
  judgments, out-of-range writes = 0 across a sealed
  adversarial battery; control without the constraint: > 0.

## 8. What this does NOT claim

- Not a full implementation: induction of representations,
  the migration step, and multi-predicate stores are designed
  but unbuilt.
- Not a generality claim: one predicate (UNIQUENESS), one
  adversary, 200 attempts in the prototype.
- Not absolute impossibility: section 4.1's channel-relative
  boundary is load-bearing. The protected-core gate variant
  that would give absolute impossibility is flagged for
  Micah's boundary decision, not taken.
- Not a claim that the learner can currently perform the
  migration step: that is the next experiment (P4's setup),
  not an established result.
- The five predicate kinds are proposed generic machinery;
  they are not frozen and any one can be cut on Micah's
  ruling without collapsing the design.

## 9. Dependencies and governance questions for Micah

1. EXECUTE(root, frame) placement is pending his ruling. The
   admissional layer anchors on EXECUTE as the single action
   channel. If he rules EXECUTE out of the protected core, the
   action-root channel needs a different anchor and section 4
   must be redesigned.
2. Protected-core gate option: putting the gate inside
   LINK/WRITE would make violation absolutely impossible for
   all learner code paths, but it moves wiring into the
   protected core. This is his boundary decision; the design
   here deliberately does not take it.
3. The structural predicate vocabulary
   (UNIQUENESS/BOUND/ACYCLIC/CARDINALITY/ORDER) is proposed as
   generic machinery comparable to the ISA. If he judges any
   kind to be domain semantics in disguise, name it and it is
   cut.

## 10. Follow-ups (not claimed, not started)

- Build the induction-to-representation migration (P4 setup):
  the experiment where duplicate-failure disconfirmations
  cause the learner to migrate list -> keyed on its own.
- Port P6 to the composition lanes once the DAG composition
  work produces an edge store to constrain.
- Run the P5 rename battery against the prototype as the
  first domain-blindness check on a constraint mechanism.

## Files

formal_knowledge/: NAMECHECK.md (this file's toolchain record),
REPORT.md (this file), fk_main.zag (prototype source),
fk_bin (pinned znc 2026.07.0-dev build), fk_compile.txt,
fk_run1/2/3.txt (byte-identical, sha256 d6e33c37...155761),
fk_run1/2/3.err (empty).
