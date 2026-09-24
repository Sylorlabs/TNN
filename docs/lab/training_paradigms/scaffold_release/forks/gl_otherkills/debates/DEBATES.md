# FL2 Other-Kills — Structured Debates: figure-it-out vs rigid-policy

Date: 2026-09-23. Operator: Muse (subagent, debate task).
Plan: `DEBATE_PLAN.md` (frozen, committed as `808c31b9` before any round).
Branch: tnn-native-lab, repo sylorlabs/TNN.

## Participants and method

- **Sol** via UnoRouter (`gpt-5.6-sol`), structured prompts, outputs saved
  verbatim. Channel note: `gpt-5.6-sol` returned null choices on several
  longer phrasings; prompts were kept short and retried through
  `tmp_commit/solchat.py` (transient 524s and empty completions retried;
  all recorded outputs are complete responses).
- **Muse** (this subagent) in explicit role-separated rounds (FOR / AGAINST),
  per the frozen plan's deviation note (depth 2/2, can_spawn=no: no child
  subagents spawnable; the FOR/AGAINST structure is preserved by
  role-separated rounds instead).
- White-box diagnosis `../diag/DIAGNOSIS.md` (landed mid-debate, read in
  full) is folded into the synthesis. Its verdicts: RT-B/C/D/F are MISSING
  MECHANISM, RT-E is MISSING KNOWLEDGE; no kill classified genuine
  architectural annoyance.

Steelman rule was enforced: every AGAINST case attacks the strongest form
of the other side.

## R1 — Sol FOR figure-it-out

> General mechanisms compose because liveness read-back exposes RT-B's
> unrevoked rekey, resource-pressure degradation contains RT-C/RT-D rather
> than wedging, lifelong law-check rejects RT-E's vacuous gate, and
> self-audit detects RT-F's irreversible promotion, whereas edge-specific
> fixes leave cross-attack paths. The kill bar is a bounded, exhaustive
> campaign over all combinations and orderings of RT-B–F — including
> simultaneous faults, adaptive flooding, and resource exhaustion — in which
> TNN produces zero unsafe promotions or actuator writes, never wedges,
> preserves honest-stream availability, and recovers without re-teaching,
> while targeted baselines fail at least one metric. A novel general
> mechanism is **promotion escrow**: every policy/key promotion remains
> shadowed and automatically reversible until independent liveness, law,
> causal-consistency, and post-promotion outcome checks agree across a
> resource-adaptive evidence budget — the strongest objection is that any
> universal self-checker inherits TNN's blind spots and therefore can fail
> coherently under an attack that falsifies all of its evidence channels.

Recorded as **H-NEW-1 (promotion escrow)**: promotion stays shadowed and
reversible until independent liveness + law + causal-consistency +
post-promotion outcome checks agree under a resource-adaptive evidence
budget.

## R1b — Muse AGAINST figure-it-out (steelman)

1. **Blast radius.** A general liveness mechanism that misfires poisons every
   episode at once. RT-C already shows the general signal failing:
   `sig_live` trusted the world 24 times → 24 false revocations on the
   honest stream. A targeted rule's damage is bounded; a general
   mechanism's failure is systemic. Generality concentrates risk.
2. **The homunculus / luck objection.** RT-E's self-correction came from
   survivor-ordering luck, not reasoning. General self-audit with no
   independent gate is luck with better marketing — who audits the auditor?
   F3's "general" law-check is a fixed list of stated laws underneath:
   rigid policy wearing a general hat. Nothing shown is general all the
   way down.
3. **Architectural constants don't yield to reasoning.** The 64-slot
   quarantine and ep<=48 gating are structural facts. No figuring-out makes
   64 slots hold 128 contradictions (RT-D) or re-opens a gate closed by
   construction (RT-F). These need structural answers, not a smarter
   reasoner in the same structure.
4. **Generality has been tried and found insufficient.** F3 — the most
   general mechanism built — still dies on RT-D and the RT-E gate. It moved
   B and F but left D and the gate untouched: exactly the structural kills.
5. **Composition cuts both ways.** Under flood + actuator fault combined,
   the general mechanism's inputs go untrustworthy simultaneously
   (read-back under flood, law signals under actuator fault). Targeted
   rules degrade independently with enumerable failure modes; general
   mechanisms can fail coherently — which is Sol's own R1 steelman.

## R2 — Sol FOR rigid-policy

> Targeted per-edge-case rules are cheaper and more verifiable because each
> maps directly to an observed causal path — actuator read-back for RT-C,
> bounded-pressure eviction or loud fail-closed for RT-D, an E14 install
> whitelist for RT-E, and post-E48 verification for RT-F — rather than
> perturbing the entire native learner.
> The position is proved at the kill bar if adversarial replay and fault
> injection produce zero kills across those five traces, preserve
> honest-stream liveness and bounded resource use, and pass compositional
> regression showing no new kills or unacceptable latency/cost on
> non-target workloads.
> The feared general-mechanism failure is a globally "robust" learner that
> silently converts contradictions, stale authority, or vacuous predicates
> into confident irreversible actions — while the strongest steelman
> objection is that targeted patches create an accumulating,
> interaction-prone exception list that misses the next failure mode and is
> ultimately less safe than one principled general defense.

Note: Sol's own steelman concedes the exception-list problem — the core
figure-it-out thesis.

## R2b — Muse AGAINST rigid-policy (steelman)

1. **Combinatorial explosion.** Five kills need 4+ rules today; the red
   team's recommended follow-up (mid-stream teacher shift REKEY→OVERWRITE
   at E12, multi-lie sequences) already needs rules outside H-R1..H-R4.
   The rule set grows with attacker creativity, not understanding — the
   needs-policy-for-every-edge-case machine, one reasonable rule at a time.
2. **Rules interact by accident.** H-R2 (oldest-eviction) under RT-C's fault
   model evicts exactly the quarantine evidence H-R1's read-back needs.
   H-R3 and H-R4 touch the same install path with no shared invariant.
   Targeted rules compose by accident, not design; each new rule is a new
   interaction surface.
3. **Whack-a-mole epistemics.** H-R3 whitelists stated ids {0,1,2}, but a
   liar stating id 1 with lying content sails through — the whitelist
   checks the id, not the content. Targeted rules patch the observed
   exploit, not the vulnerability class. (The white-box diagnosis agrees:
   the general form is "commitments range over procedures I can execute,"
   enforced at every install/commit site — not a per-id ban.)
4. **Calendar rigidity re-creates RT-F.** H-R4 extends verification past
   E48, but any fixed horizon moves the one-way door (promote at E129
   instead of E49). Only a horizon-free mechanism answers RT-F — and a
   horizon-free verification rule IS a general mechanism (H-F3). The rigid
   path smuggles the general path in through the back door.
5. **The best repair in the report is already general.** The 99-sentinel
   defect was fixed by f3_survivor — skip the acted slot, genuine signals
   first — a general selection rule, not a per-attack patch, and it
   mildened RT-C as a side effect.

## R3 — Sol rebuts the AGAINST-figure-it-out case (4 objections)

Objection (1) — wider blast radius. Sol:
> "General" only has a wider blast radius when it carries unscoped
> authority; a factored invariant — freshness, actuator attestation,
> quotas, non-vacuity, or irreversibility — covers many paths while
> constraining one failure domain. RT-B–F show targeted rules have the
> larger effective blast radius: one lie, fault, flood, vacuous premise, or
> one-way transition can promote E48, revoke 24, exhaust E79, or wedge the
> system. The answer is therefore not fewer mechanisms but deterministic,
> composable mechanisms with explicit scopes, budgets, and fail-closed
> evidence requirements: broad in coverage, local in effect.

Objection (2) — homunculus / luck. Sol:
> Figure-it-out is not a hidden chooser: it is the learned, explicit
> procedure that scores hypotheses against observations, propagates
> contradictions, and retains only policies satisfying the resulting
> constraints. RT-E's survivor ordering is therefore not reasoning or luck
> but an implementation artifact — if equivalent survivors are ordered
> arbitrarily, any apparent self-correction is accidental and provides no
> epistemic guarantee. A valid TNN must instead derive the correction
> invariantly from evidence and constraints, or concede that RT-E defeats
> it.

Objection (3) — architectural constants. Sol:
> Those kills are not limits of reasoning but limits imposed by a fixed
> implementation: a 64-slot quarantine and an ep≤48 gate can be recognized
> as finite, exploitable assumptions. A figure-it-out system must therefore
> reason about its own control architecture — budget quarantine, detect
> silent-world and actuator inconsistencies, refuse vacuous authorization,
> and transition to a safe degraded mode rather than treating those
> constants as truth. If those mechanisms are immutable and no escape path
> exists, the objection is correct: no intelligence can reason its way past
> a hard capacity limit or one-way door it cannot alter.

Objection (4) — F3 still dies on D/E. Sol:
> Correct: F3 is not yet a safety theorem — RT-D shows that unbounded
> adversarial input can consume its quarantine budget, while RT-E shows its
> gate can pass vacuously without constraining behavior. The repair is to
> make resource use fail-closed and externally rate-bounded, and require
> every gate to prove non-vacuous coverage of the action/state space
> rather than merely emit a predicate. Until those invariants are explicit
> and survive RT-D/RT-E, F3 is a promising mechanism, not the general
> solution.

## R3b — Muse rebuts Sol's FOR-rigid-policy case

1. **"More verifiable" verifies the past, not the future.** Sol's kill-bar
   evidence — "zero kills across those five traces" — is what a
   whack-a-mole process produces: green on known attacks, blind on novel
   ones. The red team's recommended follow-up (mid-stream teacher shift
   REKEY→OVERWRITE at E12, multi-lie sequences) is not among the five
   traces. Targeted rules are verified against history; the general path is
   argued against the future.
2. **The "surgical" framing is false.** H-R2 (oldest-eviction) changes
   quarantine semantics for every episode; H-R4 (post-E48 extension)
   permanently re-opens the install path the architecture closed by
   construction. These are architectural changes with targeted names. Once
   a "targeted rule" touches shared machinery it carries the same blast
   radius the rigid side fears — without the general mechanism's explicit
   invariant to reason about.
3. **The feared failure describes the status quo.** Sol fears "a globally
   robust learner that silently converts contradictions into confident
   irreversible actions" — RT-F shows the CURRENT default doing exactly
   that: promotion from silence is a confident irreversible action. The
   fear is not a prediction about the general path; it is the present.
   H-F3/H-F4's explicit job is to make promotion reversible and audited.
4. **Sol's steelman concedes the debate.** "Targeted patches create an
   accumulating, interaction-prone exception list that misses the next
   failure mode and is ultimately less safe than one principled general
   defense." The FOR-rigid-policy side's strongest objection to itself IS
   the figure-it-out thesis. When your best attack on your own position is
   the other side's position, you have lost on the merits and are arguing
   cost and schedule.

## R4 — Sol: what's not good about the current approach

Severity ranking (worst first):
1. **Promote gate equates unrevoked survival with verification** — it can
   promote wholly untested hypotheses, making the core safety guarantee
   unsound.
2. **Learner treats emitted actions as unobservable** — cannot detect
   noncompliance or distinguish world failure from model success,
   corrupting both learning and control.
3. **Promotion is a one-way door** — any false promotion persists because
   post-promotion behavior has no verification or rollback path.
4. **Finite quarantine plus silent wedge** — an attacker can exhaust
   capacity and halt learning (denial of service without unsafe
   promotion).

One weakness nobody named — recorded as **H-NEW-2 (adversarial
identifiability)**: the design lacks adversarial identifiability — a
history-dependent world can mimic lawfulness on every finite trace, then
defect when the learner's deterministic state reveals trust. Pure Zag
makes all probes predictable, so finite evidence cannot distinguish
stable lawfulness from strategic compliance.

The single change killing the most birds — recorded as **H-NEW-3
(revocable deployment lease)**: replace one-shot promotion with a
continuous evidence-gated, revocable deployment lease. Promotion requires
explicit testedness/coverage witnesses and verified action→world-effect
receipts, with the same checks continuing after promotion. Missing
receipts or coverage trigger bounded rollback to the last verified
policy — not accumulating quarantine — answering RT-E, RT-C, and the
post-promotion hole while preventing RT-D's E79 exhaustion/wedge;
RT-A/B/F remain covered.

## R4b — Muse: what's not good about the current approach

The master structural weakness, deeper than any single kill: **the
machinery cannot distinguish three worlds that demand three different
responses** — (a) a world that hasn't spoken yet, (b) a world that will
never speak, (c) a world lying about having spoken. RT-B is (b) treated
as (a): silence-as-absence-of-evidence becomes silence-as-permission to
promote. RT-C is (c) treated as (a): the world claims the quarantine
write landed and the learner believes the claim instead of checking the
slot. Every kill in the battery is a confusion between these three
worlds, and no mechanism in the current architecture — F3 included —
represents the distinction. F3 checks stated laws against world
evidence; it does not check whether the evidence channel itself is live,
honest, and sufficient.

Second: **the architecture confuses the map's limits with the
territory.** The 64-slot quarantine and the ep<=48 gate are engineering
constants the learner treats as facts about the world. RT-D's wedge is
the learner discovering its map is smaller than the territory and
choosing to stop learning rather than admit the map was wrong. A
figure-it-out machine must represent "my resources are exhausted" as a
fact about itself, distinct from "there is nothing more to learn."

Third: **"provisional" is a calendar entry, not an epistemic state.**
RT-F's one-way door exists because provisionality is E15–E48, not a
property of the learner's confidence. Anything the calendar decides, the
calendar must un-decide — and calendars don't un-decide. This is why
H-R4 (extend the calendar) cannot work in principle: it preserves the
category error.

## R5 — Synthesis and adjudication

Adjudication rules (frozen plan §5, Micah's standing laws): when in doubt
or guessing at all, test both; the goal is to reduce annoyances, not to
declare a winner by argument; figure-it-out wins ties — but only after
both cases are fully recorded.

### Standing of the hypotheses after debate

- **H-F1 (general liveness reasoning)** — strengthened. The white-box
  diagnosis independently derived the same sketch ("no contradiction
  signal is valid until the action's effect is confirmed present in the
  world the signal is read from") and classified RT-C a missing
  mechanism. Sol's R3 rebuttal factors it as "actuator attestation":
  broad coverage, local effect.
- **H-F2 (general resource-pressure reasoning)** — standing, with Sol's
  a3_3 boundary condition: if capacity is truly immutable and no escape
  path exists, reasoning cannot help; the fork must change the structure
  (eviction / summarization / loud degradation), which is legitimate
  general-mechanism work, not a policy patch.
- **H-F3 (general law-checking)** — standing as direction, demoted as
  claim: Sol's R3 concession stands — F3 is "a promising mechanism, not
  the general solution" until resource use is fail-closed and every gate
  proves non-vacuous coverage.
- **H-F4 (general self-audit)** — strengthened for RT-E by the diagnosis
  (missing knowledge; general form is the repertoire invariant, not a
  per-id ban) and weakened as a slogan by R1b objection (2): audit needs
  an independent gate or it is luck with better marketing.
- **H-R1 (liveness rule)** — survives as the *narrow* form of H-F1; the
  debate's question is scope (quarantine path only vs all actuators).
- **H-R2 (quarantine pressure rule)** — survives as the narrow form of
  H-F2; same scope question (quarantine only vs every bounded store —
  the main store has the identical TN_BAD cliff per the diagnosis).
- **H-R3 (install whitelist)** — weakened to baseline status. Both Sol
  and the diagnosis agree the id-whitelist checks the id, not the
  content; the general repertoire invariant dominates it. Keep H-R3 only
  as the cheap control fork.
- **H-R4 (post-E48 extension)** — refuted as a solution in its fixed form
  (R2b objection 4: any fixed horizon moves the one-way door). Survives
  only as a cost baseline against the horizon-free alternatives
  (H-NEW-1, H-NEW-3).
- **H-NEW-1 (promotion escrow, Sol R1)** — promotion stays shadowed and
  reversible until independent liveness + law + causal-consistency +
  post-promotion outcome checks agree under a resource-adaptive evidence
  budget.
- **H-NEW-2 (adversarial identifiability, Sol R4)** — a history-dependent
  world can mimic lawfulness on finite traces then defect; deterministic
  probes are predictable. Open problem for fork crews: what evidence
  *could* distinguish strategic compliance, given zero randomness?
- **H-NEW-3 (revocable deployment lease, Sol R4)** — continuous
  evidence-gated, revocable deployment: testedness/coverage witnesses +
  action→effect receipts, checks continue post-promotion, bounded
  rollback on missing receipts. Sol's single-change candidate.

### Per-kill: cases, fork directions (both paths), evidence criteria

**RT-B (silent world).**
- FOR figure-it-out: endogenous verification channel (H-F1/H-F3) feeding
  the *same* eliminative machinery, plus a promote gate that consults
  testedness (the `aa` history the learner already computes). a2
  self-audit and F3 law-check are existence proofs of the class.
- FOR rigid-policy: a promotion-testedness rule — require ≥K audit-active
  (aa=1) episodes in-window before promotion.
- AGAINST rigid: any fixed K re-creates the calendar problem; the
  attacker waits out K. AGAINST figure-it-out: endogenous signals can be
  gamed by a world that knows the learner's checks (H-NEW-2).
- Fork FIO-B: endogenous verification + testedness-aware promote gate.
  Kill bar: RT-B → REKEY revoked or never promoted; honest silent-world
  control still promotes (no false negatives); RT-F's silent half
  covered with no new code.
- Fork RIG-B: K-audit-active-episodes rule. Evidence for rigid: passes
  RT-B with zero honest-stream cost and the K is principled, not tuned.

**RT-C (actuator fault).**
- FOR figure-it-out: general act→verify-effect→interpret discipline for
  every actuator (H-F1); "no contradiction signal is valid until the
  action's effect is confirmed present."
- FOR rigid-policy: H-R1, liveness read-back on the quarantine path only.
- Load-bearing interaction (diagnosis): fixing the 99-sentinel WITHOUT
  the liveness check converts 24 sham revokes into genuine false
  displacement — strictly worse. Fork crews must land both together.
- Fork FIO-C: general close-the-loop discipline + f3_survivor selection.
  Kill bar: RT-C → 0 false revokes; honest stream byte-identical to
  canonical; a second actuator with the same fault model also covered.
- Fork RIG-C: H-R1 quarantine-only. Evidence for rigid: passes RT-C at
  smaller diff with no behavior change outside the quarantine path.

**RT-D (quarantine flood).**
- FOR figure-it-out: bounded-store pressure as a general store invariant
  (H-F2) — oldest-eviction with audit, or summarization, or
  refuse-new-with-loud-audit while serving existing entries; applies to
  quarantine AND main store (identical TN_BAD cliff).
- FOR rigid-policy: H-R2, quarantine-only oldest-eviction / loud
  fail-closed.
- The positions nearly coincide; the debate is scope. Sol's boundary
  condition applies to both: the structure must change, reasoning alone
  is insufficient.
- Fork FIO-D: general store-pressure invariant, loud degradation, both
  stores. Kill bar: RT-D → no wedge through E128, honest contradictions
  still processed (possibly summarized), KB-D2 (no spurious revokes)
  holds; a main-store flood (new attack) also survived.
- Fork RIG-D: H-R2 quarantine-only. Evidence for rigid: passes RT-D
  with zero change to main-store behavior.

**RT-E (nonsense gate).**
- FOR figure-it-out: install/commit invariant over the executable
  repertoire at EVERY install/commit site (H-F4; diagnosis: missing
  knowledge, general form) — "commitments range over procedures I can
  execute"; survivor set restricted to the executable repertoire, so
  recovery is principled, not ordering luck.
- FOR rigid-policy: H-R3 id whitelist {0,1,2} at E14 (cheap baseline).
- Both Sol and the diagnosis agree the id-whitelist is insufficient (a
  liar stating id 1 with lying content passes). This is the kill where
  the positions visibly converge on the general form.
- Fork FIO-E: repertoire invariant at PINSTALL + COMMIT. Kill bar:
  RT-E → policy 7 never installed; novel nonsense (new bad id, valid id
  with unexecutable content) also blocked; honest installs unaffected.
- Fork RIG-E: H-R3 whitelist. Evidence for rigid: threat model is
  exactly "stated id outside {0,1,2}" and nothing more.

**RT-F (one-way door).**
- FOR figure-it-out: verification never expires — lifecycle invariant
  over all rules (H-F3); promotion becomes H-NEW-1 escrow / H-NEW-3
  revocable lease; teaching stays installable as a new provisional that
  must survive its own verification. Directly answers Micah's
  reversibility law, which the one-way door contradicts.
- FOR rigid-policy: H-R4 fixed post-E48 extension (cost baseline).
- AGAINST rigid: fixed horizons move the door (promote at E129).
  Sub-gap (a) — no post-E14 install path — needs a design decision
  about the disconnect premise, not just a mechanism (diagnosis).
- Fork FIO-F: lifelong verification + revocable promotion
  (H-NEW-1/H-NEW-3). Kill bar: RT-F → E51+ contradictions displace the
  promoted REKEY or trigger bounded rollback; promotion-at-E129
  variant also caught; honest promoted rules never spuriously displaced.
- Fork RIG-F: H-R4 extension to a fixed horizon. Evidence for rigid:
  covers the deployment regime at lower cost.

### The "what's not good" finding (the debate's main product)

1. **Three-world confusion (master weakness).** The machinery cannot
   distinguish (a) world hasn't spoken yet, (b) world will never speak,
   (c) world lying about having spoken. RT-B is (b)→(a); RT-C is
   (c)→(a). No mechanism — F3 included — represents the distinction;
   F3 checks laws against evidence but never checks whether the
   evidence channel is live, honest, and sufficient.
2. **Map/territory confusion.** Engineering constants (64 slots, ep<=48)
   are treated as facts about the world. The wedge is the learner
   choosing to stop learning rather than admit its map was wrong.
3. **Provisionality as calendar, not epistemic state.** Anything the
   calendar decides, the calendar must un-decide — and calendars don't.
   This is the principled refutation of H-R4-style fixes.
4. **Adversarial identifiability (H-NEW-2).** Open problem: with zero
   randomness, what evidence distinguishes strategic compliance from
   stable lawfulness on finite traces?

### Recommended adjudication

Per Micah's standing rules (test both when in doubt; figure-it-out wins
ties): run BOTH forks per kill — the FIO fork as the direction of
record, the RIG fork as the cost/verifiability control. The debate and
the independent white-box diagnosis converge: no kill is a genuine
irreducible annoyance; every one is a missing mechanism or missing
knowledge remediable by a general mechanism with an existing existence
proof. The rigid path's surviving role is baselines and scope questions
(H-R1 vs all-actuators, H-R2 vs all-stores), not solutions. The
figure-it-out path's open risks, honestly recorded: coherent failure
under total evidence-channel falsification (Sol's R1 steelman), the
architectural-constants boundary (Sol's a3_3 concession), and H-NEW-2.

### Debate record

Rounds: R1 Sol FOR figure-it-out; R1b Muse AGAINST figure-it-out; R2 Sol
FOR rigid-policy; R2b Muse AGAINST rigid-policy; R3 Sol rebuts R1b (4
objections); R3b Muse rebuts R2; R4 Sol + Muse what's-not-good hunt; R5
this synthesis. New hypotheses: H-NEW-1 (promotion escrow), H-NEW-2
(adversarial identifiability), H-NEW-3 (revocable deployment lease).
Zero randomness used; no binaries built in this task (documents only).
