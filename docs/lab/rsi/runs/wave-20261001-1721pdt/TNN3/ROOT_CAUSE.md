# ROOT CAUSE ANALYSIS: Sealed Adversarial Battery on TNN-2 (wave-20261001-1421pdt)

Lane: TNN3, wave-20261001-1721pdt. Analysis only; nothing built.
Battery record: `docs/lab/rsi/runs/wave-20261001-1421pdt/sealed_adv/RESULT_SEALED_ADV_BATTERY.md`
Frozen prereg SHA-256: `b5d54f4d92585840febf58e875a8e6aff0e23a0c88b795faa5bed002c6de8590`
Frozen target: tnn2.zag `a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd`
(1591 lines), freeze_shim2_bin `9217054c5af6dec057c4530c4de3ba246f521acc6df741d1989a4504acc72954`.
Verdict: M1 FAILS (K-S5, K-S6, K-S7), M2 FAILS (K-S8, K-S9, K-S10),
M3 FAILS (K-S11, K-S12, K-S13). Process bars all PASS.
Retention K-S14: 12/12 collateral probes correct. Memory persisted;
the mechanisms did not generalize.

## 1. Per-mechanism single architectural cause

### M1 (runtime executable-graph construction): construction enumerates researcher-authored assembler schemas over observed data paths; no learner-owned procedure representation exists distinct from demonstration facts.

Evidence from the frozen source (`t2_trial`, lines 586-666): the miss
policy tries, in a researcher-fixed order, exactly four schema
families: k-hop chains (`t2_asm_chain`), subset sums (`t2_asm_sum`),
counts (`t2_asm_count`), and single-hop fallback. Each schema compiles
a BFS path (`t2_gather`) over the observed fact graph into
guard-then-set cells with stamped literal values. `promote_graph`
then keys the result to the instance: MAP field8=subject,
field4=relation. The learner's writable surface is which path got
stamped and which literals got embedded. The learner cannot author a
new schema, cannot sequence two schemas, cannot invert a schema, and
cannot name a step shared across schemas, because schemas live in
researcher code and the freeze forbids touching them.

- M1-W1 (0/8 composition, 0/4 decoy): composition of P-then-Q is not a
  schema in the menu. Novel subjects have no facts, so path
  enumeration finds nothing, and bootstrap fails because no probe
  relation is invariant. The decoy probes return memorized swapped
  values because the only structures that exist are stamped
  per-instance facts.
- M1-W2 (0/4 backward): every schema follows fact direction
  (guards test slot0 against observed values, sets write observed
  successors). No schema inverts; inversion is not a property the
  learner can derive from a stamped chain.
- M1-W3 (0/3 shared-step): steps are bare literals embedded in
  per-path cells. Two graphs cannot share a step because there is no
  step object, only stamped values. The diamond topology is
  unrepresentable.

One cause explains all three: the "constructor" is a path-finder with
a fixed schema menu, not a procedure synthesizer. Nothing the learner
does can put a new entry in the menu.

### M2 (learner-originated uncertainty guiding action): the uncertainty-to-action pathway is a researcher-fixed mapping (constant action, context-membership selection) with no content encoding and no lifecycle; the learner creates guide nodes but can say nothing through them and cannot retire them.

Evidence from the frozen source: `miss_inquire` (lines 795-812)
writes the guide with `write_node(W,g,30,-999,0,0)`: action field20=30
is a hardcoded constant, relation field24=-999. `ev_act` (lines
859-900) selects among POLICY_ROOT-linked guides whose subject sits
in the 4-deep context ring, picks max `bid()`, and returns the
guide's field20. The UNCERTAINTY node (tag 30) records (s,r) but no
code path reads its content to shape the action. No code path anywhere
supersedes a guide or UNCERT node on resolution: `is_superseded`
checks CON self-edges, and guides never receive one. The L6
(resolution) link is absent by construction, not by oversight of a
parameter.

- M2-W1 (0/8 to informant A, 0/4 hidden): the action alphabet the
  learner can emit is {30, 0}. Informant selection requires emitting
  1/2/3 discriminatingly, which is outside the alphabet. No
  informativeness is computed anywhere; `bid()` counts edge types,
  not information value.
- M2-W2 (stale 30 after resolution): the OBSERVE that resolves the
  uncertainty teaches a fact but touches no guide. The guide persists
  and re-fires when the subject re-enters context.
- M2-W3 (30, 30, 30): the action carries zero bits about the
  uncertainty's content because the content field was never wired to
  the action field.

One cause explains all three: the pathway is signaling without
content or lifecycle. The learner's experience creates nodes; the
researcher's code decides what they mean, and it decided "always 30".

### M3 (counterexample-driven revision): revision is a single researcher-authored patch schema (literal swap on a DEP edge to the contradicted fact node, re-execute, revert on failure) with no evidence model and no law representation; experience can trigger the schema but cannot modulate, generalize, or recover from it.

Evidence from the frozen source: `revise_on_contradict` (lines
685-705) scans MAPs for a DEP edge to the contradicted fact node and
calls `t2_revise_graph` (lines 706-752), which finds the stale SETREG
(tag 101) via that DEP edge, tombstones it, inserts a corrected
SETREG holding the new literal, rewires SEQ edges, and re-executes.
On re-execution failure it reverts. The trigger is any contradiction
(no counting: `map_standing`, `contradict_map`, and the `log_ev`
event log exist in the file but are called only from the test
battery, never from the cognition path). The patched unit is one
literal in one per-instance graph. Provenance anchors to the
contradicted fact node, which `ev_observe` immediately supersedes
(CON self-edge) and replaces with a new node.

- M3-W1 singleton (returned 42110, the noise): one uncorrected
  contradiction is treated identically to a systematic shift. There
  is no support comparison because the trigger does not consult
  support.
- M3-W1 generalization (0/2 on unseen subjects): the MAP is keyed
  per instance (field8=subject) and the patch edits one instance's
  literal. There is no law object above instances, so nothing can
  propagate x+5 to 42105/42106.
- M3-W2 (returned 43109, not 43119): the first revision's new SETREG
  links its DEP edge to the now-superseded fact node. The second
  contradiction arrives against the new fact node, the stale-cell
  lookup finds nothing, and the operator silently no-ops.
- M3-W3 (returned 43703, not 43713): the revert path restores the
  old graph and leaves the stale taught answer fact in place.
  `ev_query` checks exact-hit `activate()` before the trial loop,
  so the stale fact short-circuits all relearning on that key.

One cause explains all four observations: patching without an
evidence model. The operator cannot weigh (no counting in the
trigger), cannot lift (no law representation), cannot follow
(provenance points at dead nodes), and cannot recover (revert plus
stale-fact short-circuit vetoes re-derivation).

## 2. Cross-mechanism clustering (no-patch-treadmill)

The nine world-failures cluster into three shared architectural
causes. These are not nine requests for nine patches; each cluster
names one missing substrate property.

### Cluster A: no abstraction tier (instance-keyed learning without abstraction)

Members: M1-W1 (novel P-then-Q composition), M1-W3 (shared-step
diamond), M3-W1 generalization probes (x+5 on unseen subjects).

Shared cause: every learned structure is keyed to the demonstrating
instance. M1's MAPs carry (subject, relation) as identity fields;
M3's MAPs are per-instance literal graphs. There is no procedure
object, no law object, no step object. Anything the sealed world asks
about a novel instance therefore starts from zero: no facts to walk,
no literals to patch, bootstrap inapplicable. M1-W1 and M3-W1
generalization are the same failure wearing different clothes: the
learner learned about 40106's facts and 42101's literals, never about
composing or about x+5.

Fixing one member without the abstraction tier fixes nothing else:
a researcher-authored "compose" schema would pass M1-W1 and still
fail M1-W3 and M3-W1 generalization. The cluster demands a
substrate in which experience can create instance-independent
structure.

### Cluster B: no lifecycle (creation without supersession, unpromotion, or re-derivation)

Members: M2-W2 (stale guide re-fires after resolution), M3-W2
(second contradiction silently no-ops), M3-W3 (reverted revision
vetoes relearning).

Shared cause: the architecture creates persistent structure
(guides, patched SETREGs, taught answer facts, MAPs) but has no
generic machinery that retires, unpromotes, or re-derives it in
response to later experience. Supersession exists as a flag
(`is_superseded` over CON self-edges) and is honored by the
selectors (`ev_act`, `activate`), but nothing in the cognition path
ever sets it on guides or MAPs: `contradict_map` is dead code
outside the test battery. Each member is a different face of
staleness: a guide that outlives its uncertainty, a provenance
pointer that outlives its fact, a taught answer that outlives its
derivation.

Notably, Cluster B spans M2 and M3, which the per-mechanism
clustering keeps separate. One generic lifecycle substrate
(supersede-on-resolution, unpromote-on-contradiction,
re-derive-from-current-facts) addresses all three members at once.

### Cluster C: closed control plane (learner writes data, researcher writes control)

Members: M1-W2 (no inversion schema), M2-W1 (no informant
discrimination), M2-W3 (no action content), M3-W1 singleton probe
(no evidence-weighted trigger).

Shared cause: in each case the missing behavior is a decision, and
every decision lives in researcher code that experience cannot
reach. The assembler menu order, the constant 30, the bid function,
the any-contradiction trigger: none of these read learner state in
a way experience could reshape. The learner's writable surface is
node and edge creation with researcher-fixed semantics; the control
plane interprets that surface through frozen procedures. The sealed
worlds demanded new decisions (invert, select, discriminate,
weigh), and decisions are the one thing the frozen core cannot
learn.

Cluster C is the capability-source-delta argument in miniature:
wherever the demand sat in the control plane, the frozen core was
structurally unable to meet it, no matter how much experience it
received.

## 3. What did NOT fail

K-S14 retention passed 12/12. Facts persist, MAPs persist, collateral
probes hit across worlds within each block. The persistence
substrate (teaching, activation, eviction protection, determinism)
is intact. The failures are generativity failures, not memory
failures: the core remembers what it was told and cannot do anything
it was not told how to do. TNN-3 therefore does not need a new
memory; it needs new things memory can become.
