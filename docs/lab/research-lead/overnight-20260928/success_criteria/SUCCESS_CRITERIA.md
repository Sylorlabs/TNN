# Success Criteria Analysis: What "Success" Means for Each H3-lite Node

## 1. Purpose

Each H3-lite policy node learns from experience: a write path fires on
some "success" (or failure) event and updates the policy. If the success
criterion is wrong, the node learns the wrong lesson, and a "pass" on the
discrimination test means the learner adapted to a corrupted signal.
This analysis extracts each node's success criterion from the frozen
prereg (`9084a7760`, read-only), traces what the criterion actually
measures against the confirmed verification findings, and defines what
correct success would require.

Central frame (from `7eab34ff2`, section 2.6): consequence re-entry
amplifies whatever the criterion measures, correct or not. Garbage in,
garbage re-entered.

## 2. Node 1: Trial search order policy

### 2.1 Prereg success criterion (quoted from frozen prereg, section 3)

Production write path: "in `t2_try_verify`, on verification success for
family F at position p > 0, swap F one step earlier (Hebbian promotion).
On trial exhausting all families without success, increment field 32;
when field 32 exceeds 8 (researcher-chosen threshold, documented),
demote the first-choice family one step and reset field 32."

So the success event for family F is: `t2_try_verify` returns success
(not -2) for a candidate graph built by family F.

### 2.2 What `t2_try_verify` actually measures

From the verification criterion analysis (`c2a48bee6`, V1, frozen
`tnn2.zag` line 497):

```zag
fn t2_try_verify(W,s0,root,expected,masked,st)i32 {
  if(root<0){return -2;}
  set32(st,0,get32(st,0)+1);
  let v:i32=t2_exec(W,root,s0);
  if(masked==1){
    if(v!=-2 && v!=-999999){return v;}
  } else {
    if(expected!=-2 && v==expected){return v;}
  }
  set32(st,4,get32(st,4)+1);
  return -2;
}
```

Two regimes:

(a) **Masked mode** (`masked==1`): success = "executes without error."
Any value that runs is accepted. The first candidate to execute in the
policy order wins. There is zero correctness content.

(b) **Unmasked mode**: success = "executed value equals harness-supplied
`expected`." This is a correctness check, but the oracle is the test
harness (or evaluator driver), supplied by the caller. Zero
learner-internal content.

### 2.3 Consequences for Node 1 learning

**Masked/live mode: the success signal is vacuous.** Node 1's Hebbian
promotion rewards families that produce runnable graphs, not families
that produce correct answers. In a world where the wrong family always
runs (for example, chains that execute but compute wrong values, the
H2A lie pattern), Node 1 promotes the wrong family. The node learns
"what runs first," not "what works." This is the Node-1 analogue of the
V2 hole: the criterion cannot distinguish correct from wrong-but-running,
so the policy adapts to executability.

**Unmasked mode: the success signal is supervised, not autonomous.**
When `expected` is present, promotion tracks the oracle. Node 1 then
implements supervised order learning: the harness tells it which family
was right, and it reorders. That is a real causal improvement in
revisability (the prereg's claim), but it is not the learner determining
for itself what works. Any Node-1 "pass" in unmasked mode must be read
as harness-guided, not learner-internal.

**Demotion reachability.** The demotion path requires field 32 to exceed
8, i.e., nine consecutive total trial failures (no family produced even
a runnable graph, in masked mode; no family matched expected, in
unmasked). Trial families are built to virtually always emit something
runnable, so in masked mode the demotion counter may in practice never
fire. The prereg's discrimination test ("chains-before-counts
systematically picks the wrong family first... order flips to
counts-first within the demotion threshold") assumes demotion is the
mechanism of the flip. But if chains always run (just wrongly), every
trial "succeeds" at position 0 for chains, field 32 never increments,
and the order never changes. The predicted flip may depend on the
Hebbian promotion of counts (on the occasions counts verify at p > 0)
rather than on demotion. Whether the test as designed can produce the
predicted outcome depends on masked/unmasked mode details the prereg
leaves to the adversary.

### 2.4 Node-1 hole summary

Yes, there is a Node-1 analogue of the V2 hole. In masked mode the
success criterion is "runs," so Node 1 learns executability order. In
unmasked mode the criterion is the oracle, so Node 1 learns
harness-approved order. Neither is "the family whose structures the
learner itself judges correct," because no such judgment exists
(verification Component A gap, `c2a48bee6` section 7).

## 3. Node 2: Guide template policy

### 3.1 Prereg success criterion (quoted from frozen prereg, section 3)

Production write path: "new `resolve_uncertainty`, called from
`ev_observe`: when an observation matches an open uncertainty (s,r),
supersede the uncertainty and its guide via the existing type-3
self-edge convention, increment field 28, record the resolving action
in history. If the most recent three resolutions all followed action A
where A differs from the current default, set field 20 = A
(majority-of-three rule, researcher-authored heuristic operating on
learner-state history)."

So the success event for action A is: an observation matched an open
uncertainty (s,r), and the guide attached to that uncertainty carried
action A.

### 3.2 What the success event actually measures

Three problems:

**Correlation, not causation.** The observation arrives from the world
(or the harness) on its own schedule. The guide's action did not cause
the observation; at most, the action was pending when the observation
arrived. Node 2 attributes spontaneous resolutions to whatever action
happened to be the default. If uncertainties are always resolved by
harness teaching regardless of action, Node 2 "learns" that the default
action resolves uncertainties. The criterion measures co-occurrence,
not causal efficacy.

**Bootstrapping.** The guide's action is copied from the template
default at creation time (frozen `miss_inquire`, line 795: the guide
node is written with literal action 30; under H3-lite this literal
becomes a read of the policy default). Therefore every guide created
under a stable default carries that default's action, and every
resolution records that same action. For the majority-of-three rule to
fire, the last three resolutions must have "followed action A" with A
different from the current default. From a stable default, the
recorded actions are always the default itself, so the rule's
triggering condition appears unreachable without some other mechanism
first changing guide actions. On the prereg's literal text, the write
path that changes the default can only fire after the default has
already changed. This needs scrutiny before the discrimination test is
built: the adversary's Phase 1/Phase 2 design assumes the default can
shift, but the mechanism as specified may not permit the first shift.

**Teach/observe conflation.** Per `8744796fb`, `ev_observe` funnels both
environmental observations and harness teaching through `ev_teach_in`
into indistinguishable tag-1 FACTs. A "resolution" may be the harness
supplying the answer, not the environment responding to inquiry. Node 2
would then learn action preferences from the harness's teaching
schedule, a supervised signal misread as autonomous inquiry learning.

### 3.3 Node-2 hole summary

The Node-2 success criterion is the weakest of the three. It is
correlational (action did not cause resolution), possibly unreachable
(bootstrapping), and confounded (harness teaching counts as
observation). A Node-2 "pass" (default action shifts) would need to
survive three challenges: show the rule could fire at all, show the
resolutions were not harness-supplied, and show the action played a
causal role. The prereg's own "known limit" (section 3, Node 2) states
that revisable guide content does not make guides discriminating; this
analysis adds that the revision signal itself may not be sound.

## 4. Node 3: Repair dispatcher policy

### 4.1 Prereg success criterion (quoted from frozen prereg, section 3)

Production write path: "on verification success for topology T,
increment T's counter. If T differs from the current preference and T's
counter exceeds the preference's counter by margin 2 (researcher
heuristic), set field 20 = T. On total failure (all tried, all
reverted): no counter changes."

So the success event for topology T is: `t2_revise_graph` accepts a
repair performed by topology T, i.e., the V2 criterion.

### 4.2 The V2 hole interaction (CONFIRMED)

The V2 probe (`705833a27`) confirmed: `t2_revise_graph` accepts a repair
iff `out != -999999` (successful re-execution). It never checks
`out == new_o`. Probe 1: a repair computing 999 was accepted when the
contradicting observation was 500; the MAP was retargeted to 999 and a
fact (100,200,999) taught; the observation (500) was silently
discarded.

Applied to Node 3: every wrong-but-running repair increments its
topology's success counter. If a topology systematically produces
wrong-but-running repairs, its counter grows, and once it exceeds the
current preference by the margin of 2, the dispatcher switches
preference to the wrong-repair topology. The learner learns to prefer
the topology that produces wrong answers, because the success criterion
cannot tell them apart. This is the corrupted-consequence warning from
`7eab34ff2` section 2.6 made concrete: garbage in, garbage re-entered.

**One-sided learning.** "On total failure: no counter changes." Failure
is not recorded. Node 3 cannot learn "topology T fails on this kind of
contradiction"; it can only accumulate (possibly corrupted) successes.
Combined with the V2 hole, the counters measure "how often topology T
produced something runnable," not "how often topology T repaired
correctly."

**Exploitability horizon.** The V2 probe's honest-scope note says the
hole is "deficient but not currently exploited" because trial-built
graphs lack value-transforming steps after provenance SETREGs. Node 3's
six topologies go beyond literal-patch (guard-predicate edit, branch
rerouting, multi-step coordinated repair, step-count/type conversion,
step deletion). If any implemented topology emits graphs with
post-provenance value transformation, the hole becomes live inside
Node 3's own learning loop. The composition-memory red team
(spawned in parallel) is checking whether planned graph construction
opens this shape.

### 4.3 Node-3 hole summary

Direct hit. Node 3's success criterion IS the confirmed-broken V2
criterion. A Node-3 "pass" (preference shifts to the succeeding
topology) is uninterpretable until each counted "success" is checked
against `out == new_o`. Without that check, the pass could mean the
learner learned to prefer wrong repairs.

## 5. Cross-node comparison

| Node | Success event | Criterion source | Hole |
|------|---------------|------------------|------|
| 1 (trial order) | `t2_try_verify` ok for family F | V1: masked = runs; unmasked = oracle | Masked: learns executability. Unmasked: learns harness approval. |
| 2 (guide template) | observation matches open (s,r); guide had action A | Correlation; possibly unreachable rule; harness-teach confound | May learn spurious action; may never fire. |
| 3 (repair topology) | `t2_revise_graph` accepts | V2: `out != -999999`, CONFIRMED broken | Learns to prefer wrong-but-running repairs. |

All three success criteria are supplied from outside the learner's own
judgment: Node 1 from execution status or the harness oracle, Node 2
from world/harness event timing, Node 3 from a deficient re-execution
check. None is a learner-internal correctness judgment. This is
consistent with the verification gap analysis: Component A (a
correctness-substitute computation) does not exist, so every
consequence signal available to re-entry machinery is either vacuous,
supervised, correlational, or broken.

## 6. What correct success would require

**Node 1.** A family succeeds if its structures lead to answers the
learner can stand behind. That needs a learner-internal correctness
judgment (verification Component A), which does not exist. A minimal
honest proxy with existing machinery: track which families' promoted
structures survive without contradiction (are not later revised away).
That signal is delayed, noisy, and needs per-family provenance on MAPs
(which does not exist: MAPs record (s,r) provenance, not builder
family), but it is learner-internal and causally downstream of the
family's work. Anything researcher-defined ("prefer families whose
outputs look like X") is one step from a domain detector; treadmill
risk HIGH.

**Node 2.** An action succeeds if performing it causes resolution. That
needs causal attribution of resolutions to actions, which needs (a)
actually trying different actions (currently every guide gets the
default; no variation exists to learn from) and (b) a comparison of
resolution rates with and without the action. Both need the R2
self-invocation / experimentation machinery that does not exist
(`3bf4d7bb4`). Treadmill risk HIGH: any researcher-specified
"good action" for a benchmark world is task-specific by construction.

**Node 3.** A topology succeeds if the repaired graph computes the
observed value. The information (`new_o`) is already passed to
`t2_revise_graph`; the check (`out == new_o`) is simply not performed.
This is the most tractable fix of the three and is NOT a treadmill: it
completes the criterion the code already intends. One subtlety from the
V2 probe (Probe 2, count case): a strict `out == new_o` check would
reject a defensible repair (the count genuinely did not change when a
link value changed). The fully correct criterion distinguishes
"repaired graph computes a value consistent with the observation given
the graph's semantics" from "repaired graph computes an unrelated
value." That distinction needs semantic knowledge the current
criterion lacks; treadmill risk LOW for the simple check, MEDIUM for
the semantic version if done via special cases.

## 7. Implications for interpreting H3-lite results

1. **Node 1 pass (order flips):** report the mode. In unmasked mode the
   flip is harness-supervised; in masked mode check whether the
   promoted family produces correct or merely runnable structures. An
   order flip toward a wrong-but-runnable family is a fail of the
   diagnostic's intent, not a pass.
2. **Node 2 pass (default shifts):** first show the majority-of-three
   rule could fire (address the bootstrapping concern), then show the
   resolutions were environmental rather than harness-taught, then
   argue the action played a role beyond co-occurrence.
3. **Node 3 pass (preference shifts):** audit every counted success for
   `out == new_o`. A preference shift built on wrong-but-running
   repairs is corrupted learning and must be reported as such, not as
   revisability working.
4. **F2 falsifiability** (`7eab34ff2` section 4): Node 1 is the
   cleanest test of the consequence re-entry principle, but only if the
   success signal is sound. If Node 1 is implemented with correct
   M2/M3/M4 yet the order does not causally improve, that falsifies the
   principle's necessity claim for this decision. If the order
   "improves" on a vacuous signal, that confirms nothing.

## 8. Standing architectural metric

- RESEARCHER-OWNED STRUCTURAL DECISIONS: 0 added (analysis only).
- LEARNER-OWNED STRUCTURAL DECISIONS: 0.
- SOURCE-ENUMERABLE FORMS: 0.
- SUF DECISIONS: 0.
- LEARNER-INTERNAL CRITERIA: 0 (this analysis finds none of the three
  nodes' success criteria are learner-internal).
- REUSE EVENTS: 0.
- REVISION EVENTS: 0.
- COGNITION LINES: 0.
- MODES: 0. BRIDGES: 0. HANDLERS: 0. SEMANTIC CASES: 0.

## 9. Verdict

**SUCCESS-CRITERIA-COMPLETE.** Findings:

1. Node 3's success criterion is the confirmed-broken V2 criterion.
   Wrong-but-running repairs count as success; Node 3 would learn to
   prefer wrong repairs. Direct hit, empirically confirmed hole.
2. Node 1's success criterion is vacuous in masked mode (learns
   executability order) and supervised in unmasked mode (learns
   harness-approved order). Analogous hole, no learner-internal
   content either way.
3. Node 2's success criterion is correlational, confounded by
   harness teaching, and its majority-of-three update rule appears
   unreachable from a stable default on the prereg's literal text.
   Weakest of the three; needs scrutiny before the discrimination
   test is built.
4. Of the three, only Node 3's correct criterion is tractable without
   new deep machinery (check `out == new_o`, with the Probe-2
   subtlety noted). Nodes 1 and 2 need verification Component A and
   causal experimentation machinery respectively, neither of which
   exists.
5. Interpretation guardrails for H3-lite results are specified in
   section 7. A "pass" on any node that does not survive its guardrail
   is adaptation to a corrupted signal, not evidence for criteria
   ownership.
