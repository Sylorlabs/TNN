# Learning-to-Learn Gap Analysis for TNN

Date: 2026-10-01. Status: analysis only. No implementation designed.

## 1. Operational Definition

### What learning-to-learn means for TNN

Learning-to-learn is present when **experience with task A measurably reduces
the cost of learning task B**, where the cost reduction is causally traced to
learner-state changes from A (not to B being intrinsically easier).

### Observables (in priority order)

1. **Reduced examples-to-criterion.** The primary metric. If task family A
   takes E(A) examples to reach criterion and a later same-form family B
   takes E(B) < E(A), with a difficulty control showing B is not
   intrinsically easier, the learner has learned to learn. This is exactly
   the K-LT-5 bar: R = E_life(A)/E_life(A') > 1.15 with E_iso(A) ==
   E_iso(A') as the difficulty control.

2. **Faster trial convergence.** Fewer assembler families attempted before a
   successful verification on the second uncertainty of the same type.
   Measurable in transcripts: count of t2_try_verify calls per miss.

3. **Cheaper repeated ignorance.** The second miss on an identical (s,r) key
   costs less than the first. Currently both cost exactly +14 nodes / +6
   edges (state dynamics, phases B and G). Any reduction is learning.

4. **Better inquiry on second similar uncertainty.** Fewer miss-observe-act
   cycles to resolve the second uncertainty of a type seen before.

### Minimal measurable unit

One (task family A, task family B) pair with:
- Same structural form (e.g., both offset-finding, both 2-hop chains)
- Different surface parameters (different offset values, different literals)
- Difficulty control: B solved fresh (no retained state) takes the same
  examples as A solved fresh
- Causal ablation: removing the specific retained state from A returns B
  to A-speed

The L2L2 experiment is the reference implementation of this unit: Family A
(offset 3) took 13 examples; Family B (offset 7) with retained state took
10; Family B fresh took 13; ablation (form_known forced 0) returned B to 13.
Transfer of 3 examples, causally traced to retained `form_known` state.

### What does NOT count

- Solving B faster because B is easier (fails the difficulty control)
- Researcher changing source between A and B (that is researcher learning)
- Memorizing A's answers and regurgitating them on B (that is storage, L0)
- Trying fewer families because the researcher removed families (envelope change)

## 2. Inventory: What in TNN-2 Could Vary with Experience

### Currently fixed (source literals or straight-line code)

From read-only inspection of frozen `tnn2.zag`:

| Parameter | Location | Current value | Effect on learning speed |
|---|---|---|---|
| Trial search order | `t2_trial` lines 586-660 | chains k=2,3,4, then sums, then counts, then single hops | Fixed order means the learner tries doomed families first every time |
| Guide default action | `miss_inquire` line 810 | action 30 (`write_node(W,g,30,-999,0,0)`) | Every guide proposes the same action regardless of history |
| Guide default content | `miss_inquire` line 810 | content -999 | Every guide carries the same placeholder |
| Repair topology | `t2_revise_graph` | literal-patch only | Only one repair shape ever attempted |
| Uncertainty dedup | absent | N/A | Every miss creates a new UNCERTAINTY node even for identical keys |
| Trial budget per family | `t2_trial` loop bounds | exhaustive | All families tried to exhaustion; no early stopping |
| Event log capacity | `log_ev` | 128 slots, write-stops | Learning history beyond 128 events is unavailable |
| POLICY_ROOT | created once | never touched | The policy substrate exists but is inert |
| Trial statistics | header field 16 | written, never read | The learner records trial outcomes but never uses them |

### Currently varying (but not affecting learning speed)

From the state dynamics profile (`ee238d8d4`):

- FACT nodes accumulate linearly (+1 per teach, constant cost)
- UNCERTAINTY nodes accumulate (+1 per miss, including duplicates)
- Trial graphs accumulate as inert fossils (never revised, reused, or freed)
- MAP answer fields revise surgically (one narrow path)
- E9 recency window saturates (researcher-designed bound, not learning)
- Per-experience costs are exactly constant across 260 experiences

The state changes continuously but nothing in the state changes **how**
future experiences are processed. This is the precise meaning of "stability
without plasticity in the learning process itself."

### Parameters that, if learner-owned, would change learning efficiency

1. **Trial search order.** If the learner promotes families that verified
   successfully and demotes families that exhausted without success, the
   second miss of the same type tries fewer families. Direct effect on
   observable 2 (faster trial convergence).

2. **Uncertainty dedup key.** If the learner checks for an existing
   UNCERTAINTY node on (s,r) before creating a new one, the second
   identical miss costs near zero instead of +14/+6. Direct effect on
   observable 3 (cheaper repeated ignorance). This is the highest-impact
   single change because the cost is currently paid in full every time.

3. **Guide default action.** If the learner shifts the default action
   toward actions that historically resolved uncertainties, inquiry
   cycles may resolve faster. Weak effect: the action is currently
   constant and the environment may not differentiate actions.

4. **Repair topology preference.** If the learner prefers topologies
   that verified successfully, the second contradiction of the same
   fault type is repaired faster. Effect conditional on encountering
   repeated fault types.

5. **Trial budget allocation.** If the learner stops trying a family
   after k consecutive failures within a single miss (rather than
   exhausting all candidates), per-miss cost drops. This is a
   within-episode speedup, distinct from cross-episode learning.

6. **Retention priority.** Under memory pressure (not yet exercised;
   the 1024-node budget was never approached in the dynamics run),
   which structures survive eviction determines what is available
   for future reuse. Currently no learned eviction policy exists.

## 3. Gap Analysis: Missing Machinery, Ranked by Expected Impact

### Rank 1: Uncertainty dedup (remembering one's own ignorance)

**Gap:** No check for existing UNCERTAINTY on (s,r) before creating a new
one. Phase G of the dynamics run created 6 more UNCERTAINTY nodes for keys
that already had them from phase B.

**Why highest impact:** The +14/+6 per-miss cost is the largest
per-experience cost in the system, and it is paid in full on every
identical miss. Dedup converts the second identical miss from full cost
to near zero. No other single change removes this much wasted work.

**What it requires:** A lookup by (s,r) key over live UNCERTAINTY nodes
before allocation in `miss_inquire`, plus a policy for when to refresh
versus reuse an existing uncertainty (stale uncertainties after
contradictions need handling).

**Relation to L2L:** This is the most elementary form of learning to
learn: the learner's ignorance state affects the cost of future
ignorance. Without it, the learner cannot even avoid repeating its own
most expensive operation.

### Rank 2: Trial order policy (H3-lite Node 1)

**Gap:** Fixed search order in `t2_trial`. The learner tries chain k=2
before chain k=4 before sums before counts, always, regardless of which
families have ever succeeded.

**Why high impact:** Every miss pays the cost of trying doomed families
first. In a world where answers are always counts, the learner tries
chains (k=2,3,4) and sums before reaching counts, on every single miss,
forever.

**What it requires:** A learner-state ordering over the six families, a
production read path in the trial loop, and a production write path from
verify success/failure. This is exactly H3-lite Node 1.

**Honest bound:** The policy space is 6! = 720 orders over 6 fixed
families. The maximum speedup is bounded by the cost of the skipped
families. This is learning to select, not learning to invent.

### Rank 3: Cross-task policy generalization

**Gap:** Even if trial order were learned per relation, there is no
mechanism to transfer "counts work well" from relation R1 to relation
R2. Policies are per-decision-point, not generalized.

**Why it matters:** The K-LT-5 bar is about task family B benefiting
from task family A. If the trial-order policy is stored per (s,r) or
per relation, B starts from scratch. True learning-to-learn requires
the policy to generalize across surface differences.

**What it requires:** A policy representation indexed by structural
features of the uncertainty (not by literal subject/relation), plus a
similarity judgment the learner itself computes. This is beyond H3-lite,
which stores one global order, not a conditional policy.

**Note:** H3-lite Node 1 as drafted uses a single global order. That
order helps if the world is globally biased (all answers are counts)
but does not transfer selectively. A global order is the coarsest
form of policy learning.

### Rank 4: Repair topology policy (H3-lite Node 3)

**Gap:** Only literal-patch repair exists. When it fails, the learner
has no alternative.

**Why medium impact:** Contradictions are rarer than misses in the
observed lifetimes. The speedup applies only when contradictions
recur with the same fault type.

**What it requires:** Multiple researcher-written topologies plus a
preference policy. This is H3-lite Node 3. The six topologies remain
researcher-enumerated; the learner selects among them.

### Rank  5: Guide template policy (H3-lite Node 2)

**Gap:** Fixed default action 30 and content -999.

**Why lower impact:** The draft itself states the known limit: this
makes the default revisable but does not make guides discriminating.
A revisable constant is still a constant until experience changes it,
and the sealed worlds may not supply differential action feedback.

**What it requires:** H3-lite Node 2. The informativeness criterion
(which guide content actually helps) is explicitly out of scope.

### Rank 6: Trial budget adaptation (within-episode)

**Gap:** No early stopping. Every family is tried to exhaustion.

**Why listed:** This is a real efficiency gap, but it is
within-episode optimization, not cross-episode learning. It makes
each miss cheaper but does not make the second miss cheaper than
the first because of experience.

### Rank 7: Retention/eviction learning

**Gap:** No learned importance for eviction decisions. The 1024-node
budget was never approached in testing, so this is currently
unexercised.

**Why lowest (for now):** It matters only under sustained memory
pressure, which the current experiments do not create. It becomes
high priority in a true lifetime protocol.

### What is NOT missing (already present but inert)

- **Trial statistics** are recorded (header field 16) but never read.
  The data for a trial-order policy already exists; only the read
  path and write path are missing.
- **POLICY_ROOT** exists as a node but is never touched. The
  substrate for policy storage is present; the policies are absent.
- **The event log** records 128 events but write-stops. Extending
  or compressing it is infrastructure, not learning.

## 4. H3-lite and Learning-to-Learn: Honest Assessment

### What H3-lite does address

H3-lite's three policy nodes are genuine learning-to-learn mechanisms
in the bounded sense:

- **Node 1 (trial order)** directly targets observable 2 (faster trial
  convergence). If the sealed world systematically rewards counts over
  chains, the order flips and subsequent misses try fewer doomed
  families. This is experience reducing future learning cost, the
  operational definition from section 1.

- **Node 3 (repair topology)** targets faster revision on repeated
  fault types. Narrower applicability, but the same causal shape:
  experience changes a decision criterion, future episodes cost less.

- **Node 2 (guide template)** targets observable 4 (better inquiry)
  only weakly. The draft is honest about this limit.

If all three nodes pass K-H3 with the write paths firing on sealed
transcripts, H3-lite will have demonstrated **policy revisability**:
the learner's decision criteria change with experience in ways that
reduce future costs. That is a real, bounded form of learning to
learn.

### What H3-lite does NOT address

1. **Uncertainty dedup (Rank 1).** None of the three nodes touches
   the duplicate-ignorance cost. The +14/+6 per identical miss
   persists under H3-lite. The highest-impact gap is unaddressed.

2. **Cross-task generalization (Rank 3).** Node 1 learns one global
   order. It does not learn "for relation type X prefer counts"
   as a conditional policy transferable to new relations. The
   K-LT-5 bar in its strong form (B benefits from A across surface
   differences) needs conditional policies, not a single global
   ordering.

3. **Invention of new learning strategies.** All three nodes select
   among researcher-enumerated alternatives (6 orders, 1 action
   default, 6 topologies). The learner never invents a seventh
   family, a new inquiry strategy, or a new repair shape. This is
   the SUF boundary, and the draft correctly disclaims it.

4. **Learning efficiency as an explicit objective.** The nodes
   optimize implicit proxies (verify success, resolution counts).
   Nothing in H3-lite measures "examples to criterion" and
   optimizes it directly. The K-LT-5 bar is the diagnostic readout,
   not a training signal.

### The K-LT-5 prediction

The lifetime protocol predicts K-LT-5 FAILs for frozen TNN-2 and
passes "only if policy learning exists and works." H3-lite is the
candidate policy learning. Honest calibration of that prediction:

- **Weak K-LT-5** (same relation, biased world): Node 1 should pass.
  If every miss in the lifetime rewards counts, the global order
  flips to counts-first and E(B) < E(A). The 1.15 ratio is
  achievable when the skipped families are expensive.

- **Strong K-LT-5** (different relation, same structural type):
  Node 1 as drafted should fail, because the global order carries
  no conditional structure. If A teaches "counts for R1" and B
  tests "counts for R2," a global order helps only if the world
  is globally counts-biased, which is a world property, not
  transfer.

- **The dedup gap** means even weak K-LT-5 may underperform: the
  per-miss floor stays high because identical misses still cost
  full price.

### Bottom line on H3-lite

H3-lite addresses learning-to-learn at the **policy selection**
level, which is the correct first step and the right diagnostic
before expanding the protected core. It does not address
learning-to-learn at the **ignorance management** level (dedup),
the **generalization** level (conditional policies), or the
**invention** level (new strategies). Those are the gaps the
H3-lite results should be read against: if K-H3 passes but K-LT-5
(in strong form) still fails, the residual is dedup plus
generalization, not policy revisability.

## 5. Requirements Summary (Not a Design)

For TNN to "improve how it learns" in the full sense Micah named,
the following are required, in dependency order:

1. **Ignorance memory.** The learner must not pay full price for
   identical ignorance twice. (Rank 1 gap.)

2. **Policy revisability.** Decision criteria in learner state with
   exercised production write paths. (H3-lite; Rank 2, 4, 5 gaps.)

3. **Conditional policies.** Policies indexed by structural features
   of the situation, not global defaults. Required for cross-task
   transfer. (Rank 3 gap.)

4. **Learning-efficiency measurement.** The learner (or at minimum
   the evaluator) must measure examples-to-criterion as the
   objective, with difficulty controls. K-LT-5 is the bar; nothing
   in TNN-2 currently optimizes it.

5. **Strategy invention.** New trial families, new inquiry moves,
   new repair shapes created by the learner. This is the SUF
   boundary and is correctly deferred past H3-lite.

Each requirement is independently testable. Requirement 1 can be
tested without requirement 2. Requirement 2 (H3-lite) can be tested
without requirement 3. The program should not conflate passing
requirement 2 with achieving requirement 5.

## Standing Architectural Metric (This Analysis)

- RESEARCHER-OWNED STRUCTURAL DECISIONS: 0 (analysis only)
- LEARNER-OWNED STRUCTURAL DECISIONS: 0 (no mechanism built)
- SOURCE-ENUMERABLE FORMS: N/A (no forms produced)
- SUF DECISIONS: 0
- LEARNER-INTERNAL CRITERIA: 0 exercised
- REUSE EVENTS: 0
- REVISION EVENTS: 0
- COGNITION LINES: 0 added
- MODES: 0, BRIDGES: 0, HANDLERS: 0, SEMANTIC CASES: 0

## References (Read-Only)

- State dynamics: `state_dynamics/STATE_DYNAMICS.md` (commit `ee238d8d4`)
- L2L2 result: `learntolearn2/L2L2_RESULT.md` (operational reference)
- K-LT-5: `lifetime_protocol/LIFETIME_PROTOCOL_DRAFT.md` sections 11-12
- H3-lite draft: `h3lite_prereg/H3LITE_PREREG_DRAFT.md` (DRAFT-NOT-FROZEN)
- Frozen source: `tnn2_build/tnn2.zag` (`t2_trial`, `miss_inquire`)

No sealed contents inspected. No implementation designed. Paper untouched.
