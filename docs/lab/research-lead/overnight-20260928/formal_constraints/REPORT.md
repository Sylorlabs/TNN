# REPORT: Learner-Built Constraint Channel (formal_constraints)

## Question

From C264: a learned grammar constrains composition through a generic
clause registry, but the clause ABI was researcher-defined and the
compilation from induced grammar G to clauses was researcher-written.
The open question: can the LEARNER build the constraint channel
itself from experience, or is the ABI plus faithful compilation
always researcher-defined?

## Design (as preregistered, frozen)

- World W16: true divisor D0=16, literals {1,3,5,7}. A 2-word
  sentence is well-formed iff each word decodes as (w/16, w%16) with
  components in [1,7].
- Teaching: 12 labeled judgments (6 accept, 6 reject) as learner-state
  facts. The learner never sees D0, never induces a grammar, never
  computes a gcd.
- Learner induction: generic Occam separation. Feature library
  (domain-neutral): identity, div-by-k, mod-by-k for
  k in {2,4,8,16,32} (11 features). Accept range [mn,mx] per
  (field, feature); search clause sets by increasing cardinality,
  lexicographic order; first set rejecting every length-2 reject is
  written via reg_write into the learner registry.
- Composer: C264's grammar-blind composer verbatim (78 candidates per
  trial over codec hypotheses h in {8,16,32}; blind rule minimize
  (nf,f0,f1,f2)). Six fixed trial pools, no RNG.
- Arms: N = no channel (judgments inert); R = researcher-compiled
  faithful clauses (control); L = learner-built channel.
- Fidelity probes: 78 candidates x 6 trials = 468 per arm,
  reg_check vs independent direct grammar check.

## Frozen predictions vs observed

| Item | Frozen prediction | Observed | Match |
|---|---|---|---|
| Induced channel | exactly nfields=2, one clause (field=0, mod, k=32, lo=17, hi=23) | FC-CLAUSE-L: field=0 xform=2 k=32 lo=17 hi=23 | yes |
| Arm N well-formed | 0/6 | 0/6 | yes |
| Arm R well-formed | 6/6 | 6/6 | yes |
| fidelity_R | 468/468 | 468/468 | yes |
| Arm L well-formed | 6/6 | 6/6 | yes |
| fidelity_L | < 468/468 (forecast 448/468) | 448/468 | yes, exact |

3/3 runs byte-identical (sha256
496b61cce575e22656eab108a2b837ceb15be13e3b58670d1a4c6dbd40699f10).

## Kill bars

- K1 (3/3 byte-identical): PASS.
- K2 (Arm N = 0/6, judgments inert without a channel): PASS.
- K3 (Arm R = 6/6 AND fidelity_R = 468/468): PASS.
- K4 (fidelity_L < 468/468): PASS (448/468).
- K5 (Arm L = 6/6): PASS.
- K6 (no-wire audit, zero domain-vocabulary matches in induction): PASS.
- K7 (toolchain guard, pure Zag, no forbidden executable): PASS.

## Wiring-dependence analysis (the critical test)

The task's critical test: remove the researcher's wiring; does the
constraint still apply?

The experiment decomposes "wiring" into three distinct pieces, and
the answer differs per piece:

1. The registry ABI (field/xform/k/lo/hi, reg_write, reg_check):
   RESEARCHER-DEFINED. It is generic machinery reused from C264.
   The learner did not invent it.

2. The composer's reg_check call site (the bridge from generation
   into the registry): RESEARCHER-WRITTEN. Arm N proves the
   consequence of removing it: with the call site gone, the 12
   judgments sit inert in learner state and the composer picks the
   1-word h=8 candidate every trial (0/6). The learner did NOT wire
   its knowledge into the generation path. Remove the researcher's
   wiring and generation becomes unconstrained. This is a clean
   negative result on the strongest reading of the question.

3. The channel CONTENT (which clauses, which ranges):
   LEARNER-BUILT. No researcher compilation step: from the 12
   judgments alone, generic Occam separation wrote exactly one
   clause (field=0, mod-32, [17,23]) into the learner registry.
   K6 confirms the induction used no domain vocabulary. Once that
   content is in the registry and the (researcher-written) composer
   consults it, generation is constrained: Arm L picks the identical
   well-formed sentences as Arm R on all six trials (6/6), with the
   exact same picks (19,87), (17,119), (19,87), (85,85), (19,87),
   (19,87).

So the honest verdict is split: the learner CAN construct the
constraint CONTENT from experience without a researcher compilation
step, but it CANNOT wire that content into generation by itself; the
channel, the ABI, and the composer's consultation of it remain
researcher machinery.

The second honest boundary: the learned content is a SHORTCUT, not
the grammar. fidelity_L = 448/468, exactly the hand-derived
forecast. The 20 disagreements are the predicted ones (h=32 2-word
candidates whose words decode validly under D=16 but whose
field0%32 falls outside [17,23]). Finite judgments underdetermine the
constraint: many clause sets separate the teaching distribution, and
generic minimal-cardinality search picks mod-32, which tracks the
judgments without implementing the decode structure (16a mod 32 = 16
for odd a). Faithful compilation (div/mod by the true D) still
requires researcher knowledge of that structure. The shortcut is
task-adequate for this composer and pool (6/6, identical picks to
the faithful channel), but it is not the grammar.

## What this does NOT claim

- Not a claim that the learner invented the constraint channel: the
  ABI and the composer's reg_check call are researcher-defined.
- Not a claim of faithful grammar learning: fidelity_L < 1.
- Not a claim about all learners: the Occam/minimal-separation bias
  is researcher-chosen; this characterizes one generic learner.
- One world, six trials. No broad generality. The second domain
  application of the registry is deferred, not claimed.

## Verdict

FORMAL-CONSTRAINTS-COMPLETE, with the wiring-dependence analysis:
channel content can be learner-built from judgments and is
task-adequate (Arm L 6/6, picks identical to Arm R), but is
unfaithful to the grammar (fidelity_L = 448/468, exactly the
forecast shortcut); the channel itself (ABI plus the composer's
consultation of it) remains researcher-defined, and removing it
leaves generation unconstrained (Arm N 0/6). Faithful constraint
compilation still requires researcher knowledge of the decode
structure.

## Process notes

- Stale-binary incident: the fc_bin present at session start had
  been compiled before the final source edit and produced different
  output (Arm L found=0). It was never committed or reported. The
  binary was rebuilt from the frozen source; all results here come
  from the rebuilt binary.
- No em/en dashes in deliverables. Pure Zag, zero Python.
  Commits local only, nothing pushed.
