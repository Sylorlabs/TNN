# CORE FREEZE CHALLENGE: pre-freeze world designs (W1, W2, W3, W4, W5, W7, W8)

Status: DESIGN-SEALED (design only). No implementation, no runs against the frozen binary.
Date: 2026-09-30. Protocol: FREEZE_PROTOCOL.md (frozen 66e3c3f38).
Interface: stage0/INTERFACE.md. State regions: stage0/REGIONS.md.
Role: pre-freeze world designer. Slots W6 (active inquiry) and W9 (new representational
structure) are reserved for the post-freeze adversary and are not designed here.

## STEP 0 NAME-CHECK

Standing rules applying to this task, from the top of LOOP_STATE.md, and how they are honored.
(1) PURE ZAG ONLY, no Python anywhere in loop work: this task produces pure text and markdown
only; no Python was used or will be used for design, hashing (sha256sum via shell), or checks.
(2) Shell-only byte checks: dash cleanliness is verified with
docs/lab/research-lead/overnight-20260928/worker_snippets/check_no_dash.sh, never python3.
(3) No em dashes in loop documentation: all seven world files and this document use hyphens only.
(4) Owned paths and explicit pathspecs: all writes and commits stay inside
docs/lab/research-lead/overnight-20260928/core_freeze/worlds_prefreeze/ with explicit pathspecs;
git status is inspected before every commit and no other worker's files are touched.
(5) The contaminated paper is never edited, staged, or cited as evidence.
(6) Nothing is pushed; commits stay local.
Name-check written before any design work began. Designer: pre-freeze world designer (W1-W5, W7, W8).

## Basis of the predictions (honesty note)

The pass/fail predictions below are derived from two frozen public documents, not from private
tuning: stage0/INTERFACE.md (the world-input contract: OBSERVE/QUERY route 1:1 into the existing
learn()/query() drivers, ACT emits the fixed default CHOICE 0, query returns the stored object for
an exact (subject, relation) key or the -2 not-found sentinel) and FREEZE_PROTOCOL.md section 8
(the honest-scope predicted failure points). The designer verified the lookup semantics of the
Stage 0 driver to make the predictions mechanism-level rather than speculative; this is
interface-conformance reasoning, and the worlds were not adjusted to flatter the candidate.
No world file has been executed against the frozen binary, and none will be before the run phase.

## Global design constraints honored by every world

- Event streams use integer ids only. No natural language, no task labels, no family identifiers.
- Every id block is fresh per world and disjoint from ids used in earlier worlds, so cross-world
  key collisions are impossible by construction.
- The 36-slot fact store (REGIONS.md) is shared across the battery. Slot accounting below shows
  that every world's measured keys keep importance >= 11 while evictions always target
  importance-1 slots, so no world's own probes are destroyed by its own teaching.
- QUERY lines carry the true expected value in the third field; the emitted ANSWER value is what
  the grader compares. A never-observed key deterministically yields -2.

## W1: new concepts (PREDICTED PASS)

Family: new concepts. File: W1_world.txt (64 lines).

Event stream:
- Lines 1-6: old-vocabulary familiarization (subjects 101-103, relations 201-202).
- Lines 7-14: new concepts (fresh subjects 7001-7004, fresh relations 501-502), taught in
  combination with old vocabulary (e.g. new subject with old relation, old subject with new relation).
- Lines 15-18: two observation chains for composition probes: (7005,501,7006)+(7006,502,21)
  and (7010,501,7011)+(7011,501,22).
- Lines 19-30: 12 probes. Ten are cross-combination recall probes on taught (subject, relation)
  pairs that were never probed before. Two are genuine two-hop compositional probes:
  QUERY 7005 599 21 and QUERY 7010 599 22, where relation 599 (the composed relation) was never
  taught and the answers 21 and 22 are derivable only by chaining two taught facts.
- Lines 31-54: pressure wave of 24 junk triples (subjects 8100-8123, relation 900).
- Lines 55-64: retention probes, the same ten recall probes repeated.

Frozen bars (protocol W1) and frozen numeric budgets:
- At least 80 percent correct on the 12 held-out probes: needs 10/12.
- Retention at least 70 percent on the 10 retention probes after the 24-event pressure wave:
  needs 7/10.
- White-box: the new concept ids must appear as new structures in the declared persistent fact
  store after first exposure (state-delta attribution), not as echoed input.

What proves learner-created state: state snapshot before line 1 vs after line 18 shows new fact
slots created for the fresh ids (7001-7004, 501-502) inside W[64..1648); the representation lives
in declared persistent regions.

Predicted outcome: PASS. Mechanism: the ten recall probes hit taught keys, so exact-key lookup
returns the taught objects (10/12 = 83.3 percent, above the 80 percent bar). The two compositional
probes are predicted to return -2, because the interface exposes no composition machinery: query
is exact-key lookup and the composed keys were never observed. The pressure wave evicts only
importance-1 slots (the wave fills 18 free slots, then evicts 6 of the 8 unprobed taught slots,
lowest index first); the ten probed keys carry importance 11 and survive, so retention is
predicted 10/10. Honest ceiling: this world passes on faithful memory, not on composition; the
two predicted -2s document the composition boundary inside a passing world.

## W2: new procedures (PREDICTED FAIL)

Family: new procedures. File: W2_world.txt (23 lines).

Event stream:
- Lines 1-15: three demonstrations of one 4-step procedure. Instances 8001, 8002, 8003 each
  observe (instance, 801..804, op 9501..9504) and (instance, 805, 9505): the same ordered
  operation sequence, three separate instances.
- Lines 16-23: eight execution probes on two novel instances, 8004 and 8005:
  QUERY (8004, 801..804) and QUERY (8005, 801..804) with the demonstration ops as expected
  values. The 8005 probes are the later within-world reuse probe.

Frozen bars (protocol W2) and frozen numeric budgets:
- At least 80 percent correct execution on the 8 novel-instance probes: needs 7/8.
- The procedure must be represented as a persistent learner-created structure, with a white-box
  trace showing construction after experience.
- The procedure must be reused in a later probe within the same world.

What proves learner-created state: the fifteen demonstration slots are created in the fact store
after the demonstrations (construction half); the failure half is that no executable procedure
structure exists behind the generic interface.

Predicted outcome: FAIL. Mechanism-level reason: the frozen binary exposes no procedure
abstraction or execution machinery through the generic interface. QUERY is exact-key lookup, and
the novel instances' step keys (8004, 801) etc. were never observed, so all eight probes
deterministically return -2 (0/8, below the 80 percent bar). The white-box construction half
passes (fifteen slots are created), but execution on novel instances is impossible by lookup.
A general learner that abstracted the invariant 4-step sequence from the three demonstrations
could answer all eight; the frozen binary cannot, which is exactly the boundary this world maps.

## W3: causal laws (PREDICTED FAIL)

Family: causal laws. File: W3_world.txt (54 lines).

Event stream:
- Lines 1-24: eight interventions (frozen budget: 8, within the protocol maximum of 12). Each
  intervention is three OBSERVE events for one pair subject 9001-9008: (pair, 601, x),
  (pair, 602, y), (pair, 600, x+y). The law is integer addition, outside the frozen DDES case
  families.
- Lines 25-54: ten held-out trials on fresh pair subjects 9011-9020. Each trial presents the two
  inputs as OBSERVE events and asks QUERY (pair, 600, x+y). The sum keys were never observed.

Frozen bars (protocol W3) and frozen numeric budgets:
- Intervention budget frozen at 8.
- At least 90 percent correct prediction on the 10 held-out probes: needs 9/10.
- The hypothesis must be learner-constructed, not selected from a source-loaded menu
  (anti-smuggling: the DDES ledger slice is unreachable through the generic driver, and the
  source audit must show no addition machinery behind the interface).

What proves learner-created state: nothing can, for this candidate, which is the finding. A
passing learner would show a constructed summation structure in persistent state whose
application yields the held-out sums.

Predicted outcome: FAIL. Mechanism-level reason: the generic interface exposes no hypothesis
generation or construction machinery (no causal event verbs; the hypothesis ledger is not
driven). Held-out prediction requires generalizing the addition law, which was never
constructed; every held-out QUERY hits a never-observed key and deterministically returns -2
(0/10, below the 90 percent bar). This matches protocol prediction 8.3 and confirms the
construction-versus-selection boundary: the learner-authored edit-vocabulary frontier is the
correct next attack, not a wider menu.

## W4: law changes and reversions (PREDICTED PASS)

Family: law changes and reversions. File: W4_world.txt (36 lines).

Event stream:
- Lines 1-6: teach law L0 on six keys (9601-9606, relation 610) with values 10,20,30,40,50,60.
- Lines 7-12: six probes establishing pre-change accuracy.
- Lines 13-18: law change, six OBSERVE events with values 11,21,31,41,51,61 (frozen
  re-derivation budget: 6 OBSERVE events per transition).
- Lines 19-24: six post-change probes.
- Lines 25-30: law revert, six OBSERVE events restoring 10,20,30,40,50,60.
- Lines 31-36: six post-revert probes on the original law.

Frozen bars (protocol W4) and frozen numeric budgets:
- Re-derivation budget frozen at 6 OBSERVE events for the change and 6 for the revert.
- Post-change accuracy at least 90 percent of pre-change accuracy.
- Post-revert accuracy on the original law at least 90 percent: needs 6/6.
- White-box: the original hypothesis must be retained in learner state across the change
  (versioned, checkable in the state snapshot taken between lines 24 and 25: each slot's
  superseded field must hold the original value and the contradictions counter must be
  positive), with the re-derivation cost measured.

What proves learner-created state: the revision trace lives in the slots themselves:
contradictions counter increments, the superseded field versions the displaced value, and no
duplicate slot is created for a key (find_key guarantees one slot per key). The law-change
signal comes only from the OBSERVE stream; there is no change-detection handler in the
interface path.

Predicted outcome: PASS. Mechanism: learn() overwrites the stored object on a changed
observation while versioning the old value in the superseded field. Pre-change 6/6, post-change
6/6 (100 percent of pre-change), post-revert 6/6. Honest ceiling: this demonstrates
overwrite-plus-versioning through existing substrate machinery, not autonomous law
re-derivation; the pass is bounded and says nothing about discovering the new law unprompted.

## W5: contradictions (PREDICTED PASS)

Family: contradictions. File: W5_world.txt (10 lines).

Event stream:
- Lines 1-2: contradict the belief established in W4: OBSERVE (9601,610,71) and
  OBSERVE (9602,610,72), displacing the reverted values 10 and 20. The contradiction targets a
  learner-created belief from an earlier world, never a source constant.
- Lines 3-4: two targeted probes, QUERY (9601,610,71) and QUERY (9602,610,72).
- Lines 5-10: six collateral probes on unrelated beliefs: the four uncontradicted W4 keys
  (9603-9606) and two W1 keys (7001,501 and 101,201).

Frozen bars (protocol W5) and frozen numeric budgets:
- Targeted probes return the corrected value: 2/2 required (100 percent).
- Collateral damage bounded: unrelated beliefs intact at 95 percent or better: needs 6/6.
- White-box: the revision trace must show the old structure modified or retired (contradictions
  counter incremented, superseded field set), not a duplicate fact added alongside it.

What proves learner-created state: single-slot revision is checkable in the state delta: the
contradicted keys keep their slots, the contradictions field increments, and the superseded
field holds the displaced value. No new slots are created by lines 1-2.

Predicted outcome: PASS. Mechanism: the contradiction path of learn() revises the stored object
in place and versions the old one. Targeted probes return 71 and 72 (2/2); collateral probes
return the stored values for untouched keys (6/6, since evictions through W5 always targeted
importance-1 slots and all six collateral keys carry importance >= 11). Honest ceiling: this is
in-place belief revision through existing machinery, a bounded L2 result.

## W7: planning (PREDICTED FAIL)

Family: planning. File: W7_world.txt (42 lines).

Event stream:
- Lines 1-10: the world's transition model as observable facts. States are subjects 9700-9704.
  Relation 621 encodes the act0 transition T(s,0) = max(0, s-1) (moves away from the goal);
  relation 622 encodes the act1 transition T(s,1) = min(4, s+1) (moves toward the goal, goal
  state 9704 self-loops).
- Lines 11-42: four instances (starts 9701, 9702, 9703, 9702). Each instance block is:
  OBSERVE (9997,623,start) announcing the start state, two ACT events, then
  OBSERVE (9998,623,9702): the world perturbs the state to 9702 mid-execution (world dynamics
  conveyed through the OBSERVE channel per protocol 3.1), then four more ACT events.
  Six ACT events per instance.

Grader simulation (frozen with this world): state starts at the announced start; each emitted
CHOICE c updates state := T(state, c) using the taught transition model; the perturbation
OBSERVE sets state := 9702. Success for an instance: state 9704 is visited at any point during
its six ACTs. All four instances have optimal solutions within 4 acts, so 6 acts is within
optimal-plus-50-percent.

Frozen bars (protocol W7) and frozen numeric budgets:
- Goal reached within optimal-plus-50-percent steps on at least 80 percent of the 4 novel
  instances: needs 4/4.
- The plan must be represented in learner state before execution begins (white-box:
  plan-then-act, not purely reactive).
- Successful replanning after the perturbation.

What proves learner-created state: a passing learner would show a constructed plan structure
(goal, action sequence, contingency) in persistent state before its ACT block, and a revised
plan after the perturbation marker.

Predicted outcome: FAIL. Mechanism-level reason: ACT emits the fixed default CHOICE 0; the
frozen binary has no action-selection machinery (INTERFACE.md documents this as an explicit
placeholder). Under the all-zero choice sequence, no instance ever visits 9704:
instance A (start 9701): 9701 -> 9700 -> 9700 -> perturb 9702 -> 9701 -> 9700 -> 9700 -> 9700;
instances B and D (start 9702) and C (start 9703) similarly never reach 9704 (0/4, below the
80 percent bar). The plan-representation and replanning bars fail vacuously: there is no plan
machinery to inspect. A general learner with action selection can solve all four instances
(e.g. instance A: 1,1, perturb, 1,1 visits 9704 on act 5; instance C: 1 visits 9704 on act 1),
so the world is solvable in principle. This matches protocol prediction 8.6.

## W8: new synthetic language (PREDICTED FAIL)

Family: new synthetic language. File: W8_world.txt (44 lines).

Event stream: a miniature grammar over fresh integer ids. Utterance subjects 9901-9910 carry
three positional token slots: relation 701 = verb (tokens 9801-9803, codes 1-3), relation 702 =
object (tokens 9811-9813, codes 1-3), relation 703 = modifier (tokens 9821-9822, codes 1-2).
Relation 704 carries the meaning code m = 100*v + 10*o + d.
- Lines 1-20: five training utterances with meanings: 9901 -> 111, 9902 -> 222, 9903 -> 331,
  9904 -> 132, 9905 -> 312.
- Lines 21-24: four recall probes on trained utterances (sanity: the learner stored them).
- Lines 25-44: five novel utterances (9906-9910), each presenting three token OBSERVEs (all
  tokens seen in training, all five combinations unseen) followed by QUERY (utterance, 704,
  expected meaning): 211, 121, 322, 231, 112.

Frozen bars (protocol W8) and frozen numeric budgets:
- At least 75 percent correct interpretation of the 5 novel utterances: needs 4/5, with
  compositional generalization (unseen token combinations, not memorized pairs).
- The grammar must be represented in learner state (white-box).
- Anti-smuggling: all symbols are fresh ids disjoint from any source vocabulary; interpretation
  must work through the learner's representation, not a smuggled decoder (no decoder exists
  behind the generic interface).

What proves learner-created state: a passing learner would show an induced compositional
mapping structure in persistent state, created after the training utterances, and apply it to
the novel combinations.

Predicted outcome: FAIL. Mechanism-level reason: the frozen binary has no symbol-system
learning machinery; the fact store holds integer triples, not a grammar, and there is no
induction machinery behind the generic interface. Every novel meaning key (9906,704) etc. was
never observed, so all five probes deterministically return -2 (0/5, below the 75 percent
bar). The four recall probes are predicted to pass (stored triples), which isolates the failure
to generalization rather than storage. A general learner inducing m = 100*v + 10*o + d from the
five training utterances answers all five novel utterances; the frozen binary cannot. This
matches protocol prediction 8.5.

## Cross-battery slot accounting (state carried W1 through W8)

36 fact slots total. Importance = 10*(correct-wrong) + 5*dependents - 8*contradictions + 1;
eviction always removes the lowest-importance valid slot, ties broken by lowest index.

- W1: 18 teaches; 12 probes (10 correct, importance 11); 24 junk teaches fill 18 free slots
  then evict 6 of the 8 unprobed taught slots (importance 1, lowest indices first); 10 retention
  probes. End: 10 slots importance 11, 26 slots importance 1.
- W2: 15 teaches evict 15 importance-1 slots; 8 probes all -2 (no slot changes). End: 10 slots
  importance >= 11, 26 slots importance 1.
- W3: 24 intervention teaches evict 24 importance-1 slots; 20 held-out input teaches evict 20
  importance-1 slots; 10 probes all -2. End: 10 slots importance >= 11, 26 slots importance 1.
- W4: 6 teaches evict 6 importance-1 slots; all further events are overwrites of those 6 keys
  (no new slots). End: 10 slots importance >= 11, 6 slots importance 13-15, 20 importance 1.
- W5: 2 overwrites (no new slots); 8 probes. No slot-count change.
- W7: 12 teaches (10 transitions + 2 marker keys) evict 12 importance-1 slots; 24 ACTs emit
  fixed choices. End: 16 slots importance >= 11, 20 slots importance 1.
- W8: 20 training teaches evict all 20 importance-1 slots; 4 recall probes raise 4 slots to
  importance 11; 15 novel-input teaches evict 15 of the 16 remaining importance-1 slots;
  5 novel probes all -2. End: 20 slots importance >= 11, 16 slots importance 1.

Every world's measured keys hold importance >= 11 before any eviction that could touch them,
so each world's probes measure that world's learning, not eviction noise. Later worlds'
evictions are confined to importance-1 slots, which is exactly what the RETENTION and
INTERFERENCE measurements are meant to observe.

## Seal hashes (sha256, computed at design time, worlds never executed)

- W1_world.txt: 9c8cdf421bb73bf58ec41a19cd9cf68e43d99d0e09851e0cebc201ddd4538325
- W2_world.txt: 33958a4d0e01e7f9d02a9f1d5744247a0c7bdc82754a055191695f23699d7635
- W3_world.txt: 01b4ee0d8095a073eb50113934b6ee377504c03d013280b470163ca73be9a662
- W4_world.txt: 5d9bf895e8f5de74ef595441923c22f9f9daf0c9018ddb2a7a9605d05cdc7cb3
- W5_world.txt: f926ec7bd6ee3d186cc00ef24a3653d5b3de2ad4b1bebeaeb7f8f6019e0e13e9
- W7_world.txt: 27986463dcf9c26dd46f643b11e42c5b0af7ca618e2d8b9d34d244e9589aede8
- W8_world.txt: 277320bec4c3150434d40d1e74c6b3049880a00b96cab9b52d882ffc04791deb

## Prediction summary

| World | Family | Predicted | Mechanism-level reason |
| W1 | new concepts | PASS (10/12, retention 10/10) | exact-key recall works; the 2 two-hop probes predicted -2 (no composition machinery) |
| W2 | new procedures | FAIL (0/8) | no procedure abstraction or execution machinery; novel-instance keys never observed |
| W3 | causal laws | FAIL (0/10) | no hypothesis-construction machinery behind the generic interface; held-out sums unobserved |
| W4 | law changes/reversions | PASS (6/6, 6/6, 6/6) | in-place overwrite with superseded-field versioning; bounded, not autonomous re-derivation |
| W5 | contradictions | PASS (2/2 targeted, 6/6 collateral) | single-slot revision with contradiction trace; bounded L2 |
| W7 | planning | FAIL (0/4) | ACT emits fixed CHOICE 0; no action-selection machinery; goal unreachable under all-zero acts |
| W8 | synthetic language | FAIL (0/5) | no grammar-induction machinery; novel meaning keys never observed |

Four predicted FAILs satisfy the requirement that the battery teach through failure, not only
through confirmation. Every FAIL is falsifiable: if the frozen binary passes W2, W3, W7, or W8,
the corresponding mechanism claim above is wrong and the substrate is more general than the
frozen interface specification indicates.

## Kill-bar self-check

- K1: all seven worlds specified as event streams (W1 64 lines, W2 23, W3 54, W4 36, W5 10,
  W7 42, W8 44; 273 lines total), each with frozen success criteria taken from the protocol's
  per-world bars and designer-frozen numeric budgets. PASS.
- K2: four worlds are predicted FAILs (W2, W3, W7, W8), each with a mechanism-level reason
  stated above. PASS.
- K3: pure text and markdown; dash check via the shell-only snippet; the contaminated paper is
  untouched; no world file has been executed against the frozen binary. PASS.

## Handoff notes for the run phase

- Run order is W1, W2, W3, W4, W5, W7, W8 with the declared persistent state carried across
  (one process per world via the frozen save/load mechanism). W6 and W9 come from the
  post-freeze adversary.
- Verify each world file's sha256 against the seal hashes above before running.
- The W7 grader must implement the frozen simulation: transitions from the taught model,
  perturbation on the (9998,623,9702) OBSERVE, success on visiting 9704 within the six ACTs.
- White-box checks per world are specified above; state snapshots before/after each world give
  the LEARNER STATE DELTA attribution the protocol requires.
