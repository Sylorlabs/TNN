# Blame Assignment Analysis

**Status:** ANALYSIS-COMPLETE (read-only white-box, frozen TNN-2 build `f4de7ff46`).
**Verdict:** BLAME-ASSIGNMENT-COMPLETE.
**Question:** When a composed plan or revised structure fails, how does the
learner know WHICH part is wrong? Open question 4 from plan constructor
analysis `61402fd25`. This is the credit-assignment problem for structural
revision.

All line references are to `tnn2_build/tnn2.zag` (1591 lines) unless noted.

---

## 1. Current blame assignment in frozen TNN-2

### 1.1 The blame path, end to end

A contradiction enters through `ev_observe` (line 840). When the observed
value `o` differs from the activated fact's stored value, the fact node is
marked contradicted (type-3 self-edge) and `revise_on_contradict(W,n,o)`
is called with the contradicted FACT node `n` (line 845).

`revise_on_contradict` (line 685) performs blame target selection:

1. For every live MAP node `m` (tag 20), scan all edges for a type-1
   (provenance/DEP) edge from `m` to the contradicted fact node.
2. Every MAP with such an edge is blamed. `t2_revise_graph` is called
   on each one.

Blame then narrows within the MAP. `t2_revise_graph` (line 706):

1. Find the stale SETREG: scan edges for type-1 edges into the
   contradicted fact; the source cell `c` of such an edge, if it is a
   live tag-101 (SETREG) cell, is declared the stale step.
2. Find the guard `g`: the live tag-102 (BRANCHEQ) cell whose field 12
   points at the stale cell.
3. If either lookup fails (`stale<0` or `g<0`), return 0. Silent no-op.
4. Otherwise: tombstone the stale cell, insert a corrected SETREG
   holding the observed value, rewire the guard and SEQ chain,
   re-execute the whole graph.

### 1.2 Blame granularity

Two levels, both coarse:

- **Across structures: whole-MAP broadcast.** Every MAP with a
  provenance edge to the contradicted fact is revised. There is no
  ranking, no selection among multiple blamed MAPs, no check that a
  given MAP actually produced the wrong answer. If three MAPs license
  the same fact, all three get the same surgical repair applied.
- **Within a MAP: single stale cell.** The repair targets exactly one
  SETREG cell, the one with direct provenance to the contradicted
  fact. The rest of the graph is assumed innocent by construction.
  The single-schema operator cannot express "the guard is wrong" or
  "two steps are jointly wrong."

So the effective blame resolution is: broadcast at the structure
level, single-cell at the interior level. There is no middle
resolution (sub-graph, fragment, plan segment).

### 1.3 What happens when blame is wrong

There is no re-blame mechanism. The failure modes:

- **Stale cell not found** (`stale<0`): silent return 0. The
  contradiction is still taught as a fact by `ev_observe`, but the
  MAP is never revised and never superseded. The stale MAP persists
  and will produce the wrong answer again on the next query via the
  MAP path. Nothing records that blame failed.
- **Guard not found** (`g<0`): same silent no-op.
- **Wrong cell blamed**: the repair replaces an innocent SETREG with
  the observed value. Re-execution then either fails verification
  (in-place version reverts; the corruption bug `8b58c4104` lived
  here) or, worse, succeeds by accident and teaches a wrong answer.
  Nothing detects that the true culprit was elsewhere.
- **Broadcast over-blame**: innocent MAPs sharing the fact get
  surgically altered. Each such revision is a structural mutation of
  a working procedure, with no record that the blame was speculative.
- **No escalation**: if contradictions keep arriving for the same
  (s,r) after a revision, the same blame logic fires again on the
  same target. There is no "blame a different part this time" and no
  "blame the blame procedure." The system cannot learn that its
  blame assignments are systematically wrong.

In short: blame is a fixed researcher-authored lookup, not a
decision. It has no uncertainty, no alternatives, no memory, and no
correction path.

### 1.4 What blame reads

The entire blame procedure reads exactly three things:

1. Type-1 (provenance/DEP) edges: which MAP licensed which fact,
   which cell was built from which fact.
2. Node tags and liveness flags: is this cell a live SETREG (101),
   a live guard (102), a live MAP (20).
3. Field values: guard field 12 (which cell the guard sets),
   MAP field 20 (root), MAP field 28 (answer).

It reads no learner-state policy, no history of past blame outcomes,
no execution traces, no confidence values. The D4 finding from the
criterion mechanism analysis applies: the acceptance of the repair
("re-execution produced a non-error value") is a source literal,
and the selection of the blame target is a source-fixed graph walk.

### 1.5 Copy-and-commit variant (unfrozen, `880c87c4c`)

The revision substrate changed the blame dispatch key from
exact-fact-node to (s,r): it finds MAPs with DEP edges to any fact
sharing the contradicted fact's (s,r). This fixes the one-shot
limit (second contradiction after fact-lineage fork still reaches
the MAP). It does not change the blame character: still broadcast
across all matching MAPs, still single stale cell within, still no
re-blame, still no uncertainty. The (s,r) widening arguably makes
over-blame more likely (more facts match, more MAPs blamed), trading
missed blame for speculative blame. That tradeoff is unmeasured.

---

## 2. The composed-structure blame problem

### 2.1 The question

Suppose a plan is composed of fragments A+B+C (composition memory
direction, `19fa59b6f`) or of sub-MAPs sequenced by a future
constructor. The composed plan executes and produces a wrong answer,
or a contradiction arrives for a fact the plan licensed. Which
fragment is at fault?

Current TNN-2 cannot even represent this question, because:

- Fragments do not exist as separate nodes (composition memory is a
  design, not an implementation).
- MAPs are never embedded in new candidates (plan constructor G3).
- A composed plan would be a single graph; the blame walk would find
  the one SETREG with provenance to the contradicted fact and repair
  it, regardless of which fragment contributed it.

### 2.2 What information correct blame needs

At minimum, four kinds:

1. **Execution trace with intermediate values.** Which step produced
   which intermediate value during the failing run. Without this,
   blame must guess from structure alone. TNN-2's `t2_exec` does not
   persist intermediate register values; the trace exists transiently
   in the frame and is discarded. Re-execution reproduces the trace
   but does not record it.
2. **Fragment identity in the composed graph.** A mapping from each
   plan step back to the fragment (or sub-MAP) that contributed it.
   Provenance edges currently map step to licensing FACT, not step
   to source fragment. Under composition, the licensing fact of a
   fragment-internal step may be unrelated to the fragment's role in
   the plan.
3. **Dependency structure between fragments.** Which fragment's
   output fed which downstream fragment's input. SEQ edges give
   execution order but not data dependency (a MOVE of an unrelated
   register is SEQ-adjacent but not data-dependent). Blaming the
   SEQ-predecessor of the failing step is a heuristic, not an
   analysis.
4. **Counterfactual evaluation.** "Would the plan have succeeded if
   fragment B were replaced by alternative B'?" This requires
   re-running the composed plan with a substituted fragment and a
   learner-internal success criterion (verification gap G5). TNN-2
   has the re-execution machinery (`t2_exec` on a modified copy is
   exactly what copy-and-commit does) but no substitution operator
   and no criterion beyond harness `expected`.

### 2.3 Failure modes of naive blame

For a composed plan A+B+C that fails:

- **Blame-all (broadcast).** Repair or supersede every fragment.
  Destroys working fragments alongside the broken one. Under
  copy-and-commit this is safe (no corruption) but wasteful, and
  repeated broadcast blame will eventually erode the whole fragment
  store. This is the current MAP-level behavior generalized.
- **Blame-first / blame-last (order bias).** Blame the first or last
  fragment by SEQ position. No principled basis. For a wrong
  intermediate value produced mid-plan, the last fragment is
  innocent (it computed correctly from bad input) and the first may
  be innocent (it produced the right output for its own contract).
- **Blame-none (silent no-op).** The current failure mode when the
  stale-cell lookup fails. The contradiction is taught as a fact,
  the composed plan persists, and the next query re-executes the
  same wrong plan. The system oscillates between fact answers and
  plan answers without converging.
- **Blame-wrong (misattribution).** Repair the innocent fragment.
  The guilty fragment persists, so contradictions recur. Worse: the
  repaired innocent fragment may now be wrong in contexts where it
  was previously right, spreading the fault. With no re-blame
  mechanism, the system cannot recover from its own misattribution.
  This is the most dangerous mode because it is self-concealing:
  each repair "succeeds" (verification passes on the copy) while the
  underlying fault remains.

The blame-wrong mode deserves emphasis: copy-and-commit's
verification step checks that the repaired copy executes without
error and (in the current operator) that the output changed. It
does not check that the repaired part was the part at fault. A
verification that cannot distinguish correct blame from incorrect
blame is not a blame check at all; it is a well-formedness check.

### 2.4 What TNN-2 has vs. what blame needs

| Needed | TNN-2 status |
|---|---|
| Intermediate values at failure | Absent (frame discarded) |
| Step-to-fragment mapping | Absent (no fragments; provenance maps step to fact) |
| Data-dependency between steps | Absent (SEQ order only) |
| Counterfactual substitution | Absent (no substitution operator) |
| Learner-internal success criterion | Absent (G5; harness `expected`) |
| Blame uncertainty / alternatives | Absent (single fixed walk) |
| Blame outcome memory | Absent (no record of past blame) |
| Re-blame / escalation | Absent |

The only row TNN-2 partially satisfies is re-execution: `t2_exec`
can re-run a modified graph, which is the engine counterfactuals
would need. Everything the counterfactual would be evaluated
against, and everything that would select the counterfactual, is
missing.

---

## 3. Gap analysis: machinery for precise blame

Precise blame assignment would require, at minimum:

1. **Checkpointed execution traces.** Persist per-step intermediate
   values (or their hashes) for at least the most recent executions
   of each MAP. This is the evidence blame reasons over. Cost: node
   budget pressure (cf. budget-pressure experiment); traces need
   their own retention policy or they become another fossil source.
2. **Fragment provenance.** When a plan is composed from fragments,
   each step carries an edge to its source fragment node. This is
   bookkeeping over existing edge types, not a new graph type
   (One-System Rule compliant), but it requires fragments to be
   nodes, which they currently are not.
3. **A blame decision point with learner-state input.** Which
   candidate part to blame must be resolvable by learner history,
   not by a fixed walk. Per the K-H3 six-element audit: the decision
   needs learner-state fields, a production read path on the blame
   path, an exercised production write path (blame outcomes update
   the fields), and sealed behavioral variation (different histories
   blame differently). Without all six, the "blame decision" is
   theater.
4. **Counterfactual re-execution with substitution.** Copy the plan,
   substitute an alternative for the blamed fragment, re-execute,
   compare against a learner-internal criterion. Copy-and-commit
   provides the copy and re-execute; substitution and the criterion
   are missing.
5. **Re-blame on recurrence.** If contradictions recur for the same
   (s,r) after a repair, the next blame must consider a different
   target or a different granularity (escalate from cell to
   fragment, from fragment to composition glue). This requires blame
   outcome memory (which target was blamed last time, did it stop
   the contradictions).

Ranked by expected information per architectural cost, item 1
(checkpointed traces) is the prerequisite: without evidence of what
happened during the failing run, every blame rule is guessing from
structure. Item 3 (learner-state blame decision) is the SUF-relevant
one: it is the only item that moves blame from researcher-owned to
learner-owned. Items 2, 4, 5 presuppose a compositional architecture
that does not yet exist.

Explicitly not claimed: none of this establishes SUF, L3, or correct
blame. This is a requirements analysis, not a design.

---

## 4. Copy-and-commit: help or hindrance for precise blame?

Both, in different respects.

**Helps:**

- **Wrong blame is no longer corrupting.** In the in-place version,
  a misattributed repair tombstoned live cells and the revert path
  could corrupt the graph (bug `8b58c4104`). Copy-and-commit
  converts blame errors from corruption events into wasted work:
  the bad copy is freed, the original untouched. This makes
  experimenting with blame rules safer.
- **Counterfactual-shaped.** Copy, modify, re-execute, commit or
  discard is the skeleton of counterfactual blame evaluation
  (gap item 4). The substrate exists; the substitution operator
  and the criterion do not.
- **Makes blame failures visible.** The supersede-on-failure path
  (`contradict_map` + teach the observation as fact) is an honest
  signal that blame+repair did not work, as opposed to silent
  in-place mutation that might or might not have helped.

**Hinders (or rather, masks):**

- **Fail-safe reduces the pressure to blame correctly.** When wrong
  blame is cheap (discard the copy, supersede the MAP, facts answer),
  there is less architectural pressure to develop precise blame.
  The system can "succeed" behaviorally (queries get answered via
  the fact path) while its blame assignments are systematically
  wrong. This is failure-mode preservation: the behavioral metric
  improves while the cognitive capability (knowing which part is
  wrong) does not.
- **Supersede destroys the evidence.** When a MAP is superseded after
  failed blame, the structure that could have been analyzed for
  correct blame is tombstoned. A blame-learning system would want
  to keep failed structures around as negative examples; the
  current policy deletes them.
- **Verification conflates well-formedness with correct blame**
  (section 2.3). Copy-and-commit's verify step gives a false sense
  of blame validation: "the repair verified" is read as "the blame
  was right," but the check cannot distinguish the two.

Net assessment: copy-and-commit is the right substrate for
revision, and it is compatible with future precise blame, but it
does not advance blame precision by itself and its fail-safety can
mask systematic misattribution. Any blame work built on this
substrate must measure blame correctness directly (did the repair
target the actually-faulty part, as judged by recurrence of
contradictions), not via the verification pass.

---

## 5. Standing architectural metric (this analysis)

| Metric | Value |
|---|---|
| RESEARCHER-OWNED STRUCTURAL DECISIONS | 0 (analysis only) |
| LEARNER-OWNED STRUCTURAL DECISIONS | 0 (analysis only) |
| SOURCE-ENUMERABLE FORMS | n/a |
| SUF DECISIONS | 0 |
| LEARNER-INTERNAL CRITERIA | 0 |
| REUSE EVENTS | 0 |
| REVISION EVENTS | 0 |
| COGNITION LINES | 0 |
| MODES | 0 |
| BRIDGES | 0 |
| HANDLERS | 0 |
| SEMANTIC CASES | 0 |

Current TNN-2 blame characterization (for reference, not claimed
by this analysis but read from frozen source):

- Blame target selection: researcher-owned (fixed graph walk).
- Blame granularity: whole-MAP broadcast + single stale cell.
- Re-blame mechanism: none.
- Blame outcome memory: none.
- Learner-state input to any blame step: zero.

## 6. Explicit non-claims

- This analysis does not design a blame mechanism and does not
  implement one.
- It does not establish that precise blame is achievable within the
  current architecture, only what it would require.
- It does not claim copy-and-commit is sufficient for blame; section
  4 argues it is necessary but not sufficient, and partly masking.
- Predictions about composed-plan blame are extrapolations from the
  current single-MAP behavior, not measurements, because composed
  plans do not yet exist in TNN-2.
- No SUF, L3, C0-D, or capability claims are made or implied.
