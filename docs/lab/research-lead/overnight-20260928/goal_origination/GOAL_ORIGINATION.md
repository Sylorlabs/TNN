# Goal Origination Analysis

**Status:** ANALYSIS ONLY. DRAFT-NOT-FROZEN. No implementation designed or proposed in detail.
**Scope:** Open question 1 from plan constructor analysis `61402fd25`, section 5:
"Goal origination: where does the first goal come from?"
**Frozen source:** `tnn2_build/tnn2.zag` (1591 lines), read-only. Never modified.

---

## 1. Current goal-lessness (white-box characterization)

### 1.1 All activity originates outside the learner

TNN-2 exposes four event handlers. Every one is invoked by the harness; none
is invoked from within cognition code:

| Handler | Args | Internal callers (lines 1-918) |
|---|---|---|
| `ev_teach(W,s,r,o)` | (s,r,o) supplied | 0 |
| `ev_query(W,s,r,expected,flags)` | (s,r,expected) supplied | 0 |
| `ev_observe(W,s,r,o)` | (s,r,o) supplied | 0 |
| `ev_act(W)` | none | 0 |

Verified by grep over the cognition region: the only mentions of these names
inside lines 1-918 are their definitions and code comments. All call sites
(lines 991-1460) are test functions. `main()` runs only the test battery
(`run_all`).

Between events, the workspace is completely passive. `decay(W)` is called
only from the four handlers (lines 298, 814, 837, 860). There is no event
loop, no background processing, no spontaneous activity, no idle consolidation.
The learner does not "do" anything unless the harness calls it.

### 1.2 No goal representation exists in production

Tag-2 nodes (`T_GROUP`) are the notional "goal" type. In the cognition region,
exactly one tag-2 node is ever created: line 803 in `miss_inquire`, the
POLICY_ROOT lazy-init (`ns(W,pr,0,2); ns(W,pr,4,-5)`). That is an anchor
node, not a goal. Every other tag-2 creation (lines 951, 995, 1036, 1048,
1062, 1067, 1371) is test code or the regression helper `r_mk_goal`.

Confirmed: plan constructor G1. Queries are (s, r) keys; `expected` comes
from the harness. There is no persistent, learner-writable goal slot.

### 1.3 `ev_act` is reactive, not self-directed

`ev_act` takes no query arguments, which makes it look like the self-directed
endpoint. It is not:

- It is invoked by the harness ("act now"), never by the learner.
- It selects among already-existing guides by `bid` magnitude with context
  matching. It does not decide *when* to act or *what* to pursue.
- It cannot initiate a query, a teach, or an inquiry cycle. It returns a
  single integer (the winning guide's action field).

Selection among options is not origination of purpose. `ev_act` is a
harness-polled multiplexer, not an agent.

### 1.4 The miss path is reactive

`miss_inquire` is called only from `ev_query`'s terminal miss branch
(line 833), after activate, trial, and bootstrap all fail. It never fires
except in reaction to a harness query. It creates an UNCERTAINTY node and a
guide, but per the theater audit (`e0423538a`, T5) and the ignorance-dedup
analysis (`8510e327b`), the uncertainty node has no production read path:
`ev_act` never consults it, `bid` does not count it, nothing retires it.
Ablating all T30 nodes changes zero production behavior.

**Summary of section 1:** TNN-2 is a purely reactive system. Every goal-like
thing (the query to answer, the moment to act, the uncertainty to record) is
supplied or triggered by the harness. The learner originates nothing.

---

## 2. The goal origination problem

### 2.1 What is a goal in TNN terms?

A goal, minimally, is a persistent learner-state structure that:

1. **Represents** a target: a question to resolve, a structure to build, a
   skill to practice, a prediction to test. (Representation, cf. G1.)
2. **Persists** across events until satisfied or abandoned. (Not transient
   trial cells.)
3. **Directs** behavior: it changes what the learner does next, not merely
   what it stores. (Causal efficacy, the anti-theater clause.)
4. **Terminates**: there is a recognizable satisfaction condition and an
   abandonment condition. (Otherwise it is a leak, not a goal.)

Note the ordering: (3) is what separates a goal from a write-only record.
A goal structure with no read path into behavior is theater by Micah's rule,
exactly the T5 failure mode.

### 2.2 Candidate origination sources

Following the plan constructor's three options, expanded to five:

**O1. Adopted from the query stream.** Repeated or important harness queries
become implicit goals ("I am frequently asked about (s, r); I should master
it"). The goal set is harness-determined; the learner only prioritizes.

**O2. Generated from uncertainty.** A miss creates an uncertainty record;
the record becomes a goal ("resolve this ignorance"). This was the *intent*
of Change 2 ("the miss-to-act loop is closed in learner state").

**O3. Generated from prediction error.** A contradiction creates a goal
("repair this structure" / "understand why this failed"). Currently
contradictions trigger reactive revision, not goal formation.

**O4. Generated from intrinsic drive.** Curiosity, boredom, practice drive:
goals with no external trigger ("rehearse this MAP", "probe this boundary").
No machinery exists; this is the most speculative source.

**O5. Proposed by a higher-level driver.** A meta-harness or curriculum
assigns goals. This is O1 with the researcher moved up one level.

### 2.3 What distinguishes a learner-owned goal from a harness-supplied task?

Three tests, in increasing strength:

- **T-a (weak):** the goal's *content* is not literally the harness's
  arguments. (O1 passes if the learner generalizes queries into practice
  targets; fails if it just queues (s,r) pairs.)
- **T-b (medium):** the goal's *existence* is not caused by a harness event
  in the same tick. The learner forms goals between events, from accumulated
  state. (Requires breaking pure reactivity; nothing in TNN-2 passes.)
- **T-c (strong):** the goal's *pursuit* changes the learner's behavior in a
  way ablation removes. The anti-theater clause: delete the goal structure,
  and the learner must behave differently. (Requires the read path; cf. the
  SUF 4-condition test.)

O5 fails T-a by construction (it is a harness task with extra steps).
O1 passes T-a only with generalization. O2/O3 can pass T-a and T-b if the
uncertainty/error record is genuinely transformed into a directive rather
than logged. O4 is the only source that passes T-b without qualification.

### 2.4 SUF implications per source

- **O1 (adopted):** weakest SUF position. The goal *set* is
  harness-enumerated; the learner selects and prioritizes. This is menu
  selection over researcher-supplied items, the H3-lite boundary. Cannot
  exceed SUF-FAIL for the goal set itself, though prioritization could be
  learner-owned.
- **O2 (uncertainty):** medium. The uncertainty arises from the learner's
  own experience (its ignorance, not the harness's agenda). But the
  transformation "ignorance record -> goal" must itself be learner-driven,
  not a source-fixed rule like "every miss becomes a goal," which would be
  another enumerated mapping. Currently blocked twice: uncertainty has no
  read path (theater), and goal formation does not exist.
- **O3 (prediction error):** medium, same structure as O2. The error is
  learner-experienced; the goal-formation rule must not be source-fixed.
- **O4 (intrinsic):** strongest in principle, emptiest in practice. An
  intrinsic drive is a researcher-authored objective function unless the
  drive itself is learner-shaped by experience. "Curiosity" as a fixed
  formula is a semantic case smuggled into the core.
- **O5 (driver):** homunculus. Moves the researcher, does not remove them.

---

## 3. Gap analysis: machinery required

Ranked by dependency (each presupposes the previous):

**R1. Goal representation.** A persistent learner-state slot for goals
(plan constructor G1). Must be writable by learner experience, not just
harness. Without this, there is nothing to originate *into*.

**R2. Self-invocation (the deepest gap).** Even with R1, TNN-2 cannot act on
a goal between harness events: there is no mechanism for the learner to
initiate a query, a teach, or an inquiry cycle on its own behalf. All
behavior is event-handler-shaped. A goal without an action loop is a
write-only record (theater). This is not a missing feature; it is the
reactive architecture itself. Any goal system presupposes either a
learner-driven scheduler or a harness that polls learner state for pending
intentions (which is O5, the homunculus).

**R3. Origination rule.** What creates a goal, from which trigger, under
which conditions. Must satisfy T-a at minimum. A source-fixed "every X
becomes a goal" is enumeration, not origination.

**R4. Goal scheduler.** With multiple goals: which first, and when to
switch. Currently vacuous (no goals). Interacts with the fixed trial order
(H3-lite Node 1 direction) and with retention (goals compete for the node
budget).

**R5. Goal-behavior coupling (the read path).** The goal must change what
the learner does: which uncertainties to pursue, which structures to
rehearse, which queries to self-initiate (given R2). This is the anti-theater
clause, T-c. The ignorance-dedup 4-element mechanism (keyed lookup, read
path, retirement, experience-varying content) is the template for what a
non-theatrical coupling looks like.

**R6. Goal lifecycle.** Satisfaction detection ("this goal is met") and
abandonment ("this goal is not worth pursuing"). Without abandonment, goals
accumulate like the unreclaimed trial garbage (69 cells in the white-box
inventory) and become a leak. Abandonment is itself a decision requiring a
criterion (cf. K-H2-3, the decline-signal analysis).

### The R2 problem, stated plainly

R2 deserves emphasis because it is architectural, not incremental. TNN-2's
execution model is: harness calls handler, handler runs, handler returns.
There is no "learner tick." Proposals like "the learner checks its goals
when idle" have no idle to check in: between handler calls, zero cognition
executes. Closing this gap means either:

- (a) adding a learner-invoked scheduling entry point (new machinery,
  protected-core-adjacent, needs Micah-level scrutiny under the ISA ruling);
  or
- (b) the harness polls a learner-state "intention" structure (O5 in
  disguise; the goal's pursuit is still harness-driven); or
- (c) goals are pursued *within* handler calls (the learner uses
  harness-triggered events as opportunities to advance its own goals, e.g.,
  a query event also triggers one goal-directed rehearsal step).

Option (c) is the only one compatible with the reactive architecture, and it
is worth naming precisely: **opportunistic goal pursuit**. The learner does
not self-initiate, but it diverts a fraction of harness-given computation
toward its own goals. This is weaker than true self-direction (T-b fails:
pursuit is still event-caused) but it is not theater (T-c can pass: ablate
the goal, the diversion stops). Whether (c) counts as "origination" is a
judgment call this analysis does not make.

---

## 4. Inquiry: proto-goal system or reactive pipeline?

The file header claims Change 2 closes "the miss-to-act loop in learner
state": miss -> UNCERTAINTY node -> guide -> POLICY_ROOT -> `ev_act`
selection. This was *designed* as a proto-goal system: ignorance becomes an
object, the object gets a guide, the guide gets selected, selection drives
action.

Against the section 2.1 definition, it fails at every clause that matters:

1. **Representation:** the UNCERTAINTY node records (s, r) and a constant.
   It does not represent a target state or a resolution criterion.
2. **Persistence:** nodes persist, but nothing retires them when the
   uncertainty is resolved (no retirement path; ignorance-dedup finding).
3. **Direction:** nothing reads them. `ev_act` selects by context match and
   `bid`, never consulting uncertainty keys. The "loop" is open: the write
   path exists, the read path does not.
4. **Termination:** no satisfaction or abandonment. Duplicate nodes
   accumulate per identical miss (state-dynamics finding).

Additionally, the "act" in the loop is harness-triggered (`ev_act` has no
internal callers), so even a closed loop would be harness-paced.

**Verdict on inquiry:** it is a reactive logging pipeline, not a
proto-goal system. The *intent* was goal-like (O2: uncertainty -> goal),
which makes its current state informative: it shows exactly where the
O2 path breaks (the read path, R5) and what the missing machinery is
(the ignorance-dedup 4-element mechanism). The inquiry work is not wasted;
it built the write half of a goal system. But a write half is not a loop.

Note the implication for H2: K-H2-3 asks whether TNN can accept, reject, or
withhold using a learner-internal criterion. Goal pursuit is the positive
dual of withholding (pursue vs. decline). The same missing machinery (a
criterion with a read path into behavior) blocks both. The decline-signal
analysis and this analysis converge on R5/R6.

---

## 5. Relation to the lifetime protocol

Micah's lifetime requirement (2026-10-01 clarification): one learner,
A -> B -> C -> D -> A', no reset, no task labels, no recompilation, with
spontaneous cross-domain connections as a feature.

A purely reactive learner can satisfy the *letter* (state persists, no
reset) while showing no *directed* growth: it accumulates whatever the
stream happens to teach. The north star ("intelligence grows because its
internal world becomes richer and more interconnected") does not strictly
require goals; richer interconnection can emerge from reactive learning.
But two lifetime measures presuppose something goal-like:

- **Spontaneous cross-domain connections:** "spontaneous" means
  not-harness-caused. In a purely reactive architecture, every connection
  is caused by a harness event in the same tick. True spontaneity needs R2.
- **Improvement in learning itself (K-LT-5):** deliberate practice
  (rehearsing weak structures, probing boundaries) is the most direct
  mechanism for learning-to-learn, and it is goal-shaped.

The honest position: goals are not proven necessary for the lifetime
vision, but the two most ambitious lifetime measures are hard to state
without them. This analysis does not resolve whether (c) opportunistic
pursuit suffices; that is an empirical question for a future build.

---

## 6. Standing architectural metric (this analysis)

| Metric | Value |
|---|---|
| RESEARCHER-OWNED STRUCTURAL DECISIONS | 0 (analysis only) |
| LEARNER-OWNED STRUCTURAL DECISIONS | 0 |
| SOURCE-ENUMERABLE FORMS | n/a (analysis) |
| SUF DECISIONS | 0 |
| LEARNER-INTERNAL CRITERIA | 0 |
| REUSE EVENTS | 0 |
| REVISION EVENTS | 0 |
| COGNITION LINES | 0 added |
| MODES | 0 |
| BRIDGES | 0 |
| HANDLERS | 0 |
| SEMANTIC CASES | 0 |

## 7. Explicit non-claims

- This analysis does not design a goal system and does not claim goals are
  necessary for the lifetime vision (section 5 states the honest position).
- No SUF, L3, or C0 claim is made or implied. O1 cannot exceed SUF-FAIL for
  the goal set; O2/O3/O4 are unblocked in principle but blocked in practice
  by R1-R6.
- The (c) opportunistic-pursuit option is named, not endorsed.
- DRAFT-NOT-FROZEN.

---

**Verdict: GOAL-ORIGINATION-COMPLETE.**
