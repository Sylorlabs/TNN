# Learner-Internal Verification: Problem-Space Analysis

**Status:** Analysis only. Read-only white-box of frozen TNN-2
(`tnn2_build/tnn2.zag`, 1591 lines, build `f4de7ff46`). No implementation
designed or proposed beyond naming the mechanism space. No source modified.

**Purpose:** Connect three findings into one problem statement.
- D4 (criterion mechanism `8a2ff4b77`): D1 trial acceptance reads
  harness-supplied `expected`; D4 revision acceptance uses the source
  literal "successful re-execution."
- G5 (plan constructor `61402fd25`): no learner-internal verification
  criterion exists. "Verification is learner-internal (harness acceptance
  keeps the decision source-side)" is required for SUF.
- H2 void (`72173fe11`): the worlds' direct facts short-circuit the trial,
  so verification never runs. But even when it runs, it verifies against
  `expected`, a researcher-supplied answer.

**Question:** What would it mean for TNN to verify a candidate structure
without the environment handing it the answer, and what is the minimal
machinery that could do it?

---

## 1. Inventory: every verification/acceptance check in TNN-2

Five checks were found by read-only inspection. For each: what is compared
against what, where "correct" comes from, and whether anything
learner-internal participates.

### V1. Trial candidate verification: `t2_try_verify` (line 497)

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

- Compared: the candidate's executed value `v` against `expected`
  (unmasked) or against the sentinels -2/-999999 (masked).
- Source of "correct": the `expected` parameter, passed down the call
  chain `ev_query` (line 813) -> `mp_run` (line 668) -> `t2_trial`
  (line 586) -> `t2_try_verify`. In every production and evaluation
  caller, `expected` originates outside the learner: the test harness,
  the evaluator driver, or the frozen self-tests (lines 1112-1266).
- Masked branch: "correct" is reduced to "executes without error." Any
  value that runs is accepted. The first candidate to execute in the
  fixed researcher search order wins.
- Learner-internal content: zero. The executed value `v` is computed,
  not judged; the judgment inputs (`expected`, `masked`) are both
  supplied by the caller.
- Note the comment at line 584: "E-ruling: expected is post-hoc feedback
  only." The integration scout (`INTEGRATION_SCOUT.md`) records the
  E-ruling's live-mode consequence: "in live mode it [expected] is absent
  and selection falls back to first non-sentinel." That fallback IS the
  masked branch. So the architecture's own answer to "what verifies in
  live operation" is: nothing beyond successful execution, first in
  researcher-fixed order.

**Classification: HARNESS-SUPPLIED** (unmasked) / **SOURCE LITERAL**
(masked). This is D1 in the criterion inventory.

### V2. Revision acceptance: `t2_revise_graph` (line 706)

```zag
  let out:i32=t2_exec(W,root,s);
  if(out==-999999){
    ...revert...
    return 0;
  }
  ...
  ev_teach_in(W,s,r,out);
  ns(W,m,28,out);
  return 1;
```

- Compared: the repaired graph's re-executed output `out` against the
  failure sentinel -999999.
- Source of "correct": the source literal "successful re-execution."
  Acceptance = the repair runs. That is the entire criterion.
- What is NOT checked: `out == new_o`, where `new_o` is the
  contradicting observation that triggered the revision
  (`revise_on_contradict`, line 685, receives `new_o` and passes it to
  `t2_revise_graph`). The repair procedure surgically inserts a literal
  for `new_o` (`t2_lit(W,new_o)`, line ~725), so the re-execution will
  normally produce a value derived from `new_o`; but the acceptance
  check never confirms this. The judgment that the repair is CORRECT is
  embedded in the researcher's surgical procedure (insert the observed
  value at the stale step), not in any check the learner performs
  afterward. A repair that runs but computes something unrelated to the
  observation would still be accepted, provided it does not crash.
- Learner-internal content: zero. The trigger (`new_o` mismatching the
  stored fact) is genuine experience, but the acceptance rule is a source
  literal applied to a computed value.

**Classification: SOURCE LITERAL.** This is D4 in the criterion
inventory.

### V3. P-INV bootstrap consensus: `bootstrap_miss` (line ~766)

- Compared: up to 6 recent fact values sharing relation `r`. Accepted
  only if all are identical (`inv==1`) and count >= `k`.
- Source of "correct": agreement across the learner's own stored
  observations, plus the threshold `k` from the tag-903 node.
- Learner-internal content: partial. The agreement computation runs over
  learner-state facts (observations the learner recorded). This is the
  closest TNN-2 comes to a learner-internal verification: the standard
  is "my own observations agree," not "the harness says." But: (a) the
  threshold `k` is a theater node (D7: created with default 3, no
  production write path ever updates it); (b) the "all agree" rule is a
  source-fixed unanimity requirement; (c) the agreed value is taught as a
  fact for a (s,r) the learner never observed, which is induction by
  fiat, not verified inference.
- Failure mode already visible: unanimous-but-wrong observations pass.
  There is no dissent handling, no weighting by premise standing.

**Classification: MIXED** (learner-state observations under
researcher-fixed rule and theater threshold).

### V4. Observation confirmation: `ev_observe` (line ~838)

```zag
  if(n>=0){
    if(ng(W,n,28)==o){
      link_edge(W,n,7,n,0); ... return 1;   // confirmation
    }
    link_edge(W,n,3,n,0);
    revise_on_contradict(W,n,o);             // contradiction
    ...
    return 0;
  }
```

- Compared: the activated fact's stored value against the incoming
  observation `o`.
- Source of "correct": the observation `o`, which is environment-
  supplied. But `o` is EXPERIENCE, not an oracle: it is the world
  presenting a fact, the same channel through which all of the learner's
  knowledge arrives. The learner is not being handed the answer to a
  question it asked; it is being told what is.
- This is the legitimate prediction-error signal in TNN-2. It is the
  only check where mismatch drives a learner-state change
  (contradiction edge, revision trigger) rather than just a reject
  counter.
- It is not, however, a VERIFICATION check in the relevant sense: it
  fires on observations, not on candidate structures before commitment.
  It can falsify a promoted MAP after the fact; it cannot prevent a bad
  promotion.

**Classification: EXPERIENCE-DRIVEN** (genuine signal, wrong temporal
position for pre-commit verification).

### V5. Activation retrieval: `activate` (line 140)

- Compared: query (s,r) against stored fact keys; highest `bid` wins.
- Not verification in any meaningful sense: it is retrieval with a
  fixed scoring formula. Included because it is the gate that
  short-circuited H2 (see section 6): when it succeeds, V1 never runs.

### Summary table

| ID | Check | Compared | "Correct" from | Learner-internal? |
|----|-------|----------|----------------|-------------------|
| V1 | `t2_try_verify` | v vs expected / vs sentinels | Harness param / source literal | No |
| V2 | `t2_revise_graph` | out vs -999999 | Source literal | No |
| V3 | `bootstrap_miss` | fact values vs each other, count vs k | Learner observations + theater k | Partial (rule fixed) |
| V4 | `ev_observe` | stored vs observation o | Experience (post-hoc) | Signal yes, pre-commit no |
| V5 | `activate` | (s,r) vs fact keys | Retrieval, not verification | n/a |

**Bottom line:** TNN-2 has no check in which the standard of correctness
for a candidate structure is computed from the learner's own state. V1
outsources judgment to the harness. V2 reduces judgment to "runs." V3
gestures at self-agreement but under a fixed rule and a theater
threshold. V4 supplies genuine prediction error but only after
commitment.

---

## 2. Definition: what learner-internal verification means

### 2.1 The oracle/observation distinction

The H2 key question asks whether TNN can judge structures "when the
environment does not provide the expected answer." Precision matters
here, because the environment DOES legitimately provide something:
observations. The distinction:

- **Oracle (`expected` in V1):** the answer to the very question being
  asked, supplied before the learner commits to an answer. Accepting on
  oracle-match means the learner never judges; it pattern-matches its
  output against a supplied key. In live operation this channel does not
  exist (E-ruling), which is why the masked branch matters.
- **Observation (`o` in V4):** a fact the world presents through the
  normal experience channel. The learner may have a prior prediction
  that the observation confirms or contradicts. Observations are the
  legitimate fuel of learner-internal verification; the oracle is its
  replacement.

Learner-internal verification therefore means: the learner judges a
candidate structure against a standard C, where C is computed from the
learner's own state and experience, and the environment supplies at most
observations (which the learner may or may not have predicted), never
the criterion itself at decision time.

### 2.2 Formal shape

For a verification check to count as learner-internal, four elements
must exist (this mirrors the K-H3 write-path audit Micah required,
because the underlying demand is identical):

1. **Criterion fields in learner state.** At least one persistent field
   whose value is neither a source literal nor a verbatim copy of an
   observation. It must be addressable by both a read path and a write
   path.
2. **Production read path.** A function on the verification path (V1's
   successor, or a new gate) that loads the field and branches on it
   during the sealed evaluation. Dead code does not count (cf. D6's
   `mp_get`, never called in production).
3. **Production write path.** A function reachable during ordinary
   operation that stores a new value into the field, with the write
   visibly firing in transcripts. A value never rewritten is theater
   (cf. D7's tag-903 k).
4. **Triggering experience.** The write path fires in response to
   prediction error or outcome feedback the learner detects itself:
   contradiction on a promoted fact (V4's mismatch branch), a verified
   candidate later proven wrong, an executed MAP whose answer disagrees
   with a later observation. Not researcher setup, not harness pokes,
   not initialization.

Plus the two K-H2-3 clauses that make it testable:

5. **Separable ablation.** Zeroing or randomizing the criterion value
   alone, holding all experience fixed, flips at least one
   accept/reject decision. This is what distinguishes a criterion from
   raw experience tallies: D5's `bid` fails it because there is no
   parameter separable from the event counts.
6. **Experience-driven change.** The committed log shows the criterion
   changing after prediction error, not at init.

### 2.3 What it is NOT

- It is not the masked branch ("accept anything that runs"). That is
  the absence of verification wearing the uniform of a decision rule.
- It is not V3's unanimity rule with a theater threshold. A fixed rule
  over learner-state data is researcher judgment applied to learner
  data, not learner judgment.
- It is not tuning source literals between evaluations. That is the
  researcher judging, with extra steps.
- It is not "the learner verifies against its own MAPs" if those MAPs
  were themselves promoted by oracle-match. The regress must bottom out
  in experience (observations), not in oracle-laundered structures.

---

## 3. Candidate mechanisms

Eight candidates, ordered roughly from weakest to strongest. For each:
the mechanism sketch (analysis, not design), what experience grounds it,
and the failure modes: how the learner could fool itself. The failure
modes are the point; a candidate whose self-deception modes are not
understood is not a candidate.

### C1. Execution success (status quo, masked branch)

Accept iff the candidate executes without error (v not in {-2,
-999999}). Grounding: none beyond the ISA's determinism. This is what
TNN-2 does today in live mode.

- Failure modes: accepts every well-formed graph regardless of what it
  computes. In H2A both the wrong 2-hop chain and the true 3-hop chain
  execute; the fixed search order picks the wrong one. Self-deception
  is total: the learner cannot distinguish a lucky guess from a sound
  inference. This is the null criterion; it is included as the baseline
  every other candidate must beat.

### C2. Re-execution consistency (determinism check)

Accept iff the candidate executes to the SAME answer across multiple
fresh frames (or repeated runs). Stronger than C1: it rejects
nondeterministic or frame-sensitive graphs.

- Grounding: the learner's own executor, run repeatedly.
- Failure modes: the 4-op ISA is deterministic by construction, so this
  is nearly vacuous for TNN-2's graph type; a deterministically wrong
  graph passes. It checks the machinery, not the content. Self-deception
  mode: the learner "verifies" by re-running the same mistake and
  taking the repetition as confirmation. Two runs of one error are not
  two independent witnesses.

### C3. Cross-path agreement (consilience)

Accept iff two or more independently constructed candidates agree on the
answer. E.g., a chain-built graph and a sum-built graph producing the
same value, or the same answer reached from different premise subsets.
The learner's generative diversity becomes its own check.

- Grounding: the learner's own constructions; no oracle needed.
- Failure modes: (a) CORRELATED PREMISES: the "independent" paths are
  built from the same fact base; if a shared premise is wrong, all paths
  agree on the wrong answer, and agreement now certifies error.
  (b) SPARSITY: in sparse domains only one path may be constructible;
  the criterion then rejects everything, including truths (excessive
  conservatism). (c) COLLUSION BY CONSTRUCTION: if the assemblers share
  a systematic bias (e.g., all prefer short chains), agreement reflects
  the bias, not the world. (d) The agreement threshold itself (how many
  paths, how much overlap counts as "independent") needs a criterion,
  which is the regress one level up.
- Self-deception mode: the learner mistakes the coherence of its own
  biases for evidence about the world.

### C4. Provenance strength (evidential support)

Accept iff the candidate's licensing facts (the DEP-edge premises) have
sufficient standing: high confirmation counts, low contradiction counts,
recent successful use. This is D5's `bid` promoted from a selection
score to a verification gate, with learnable weights (criterion-
mechanism Gap 2).

- Grounding: the learner's recorded experience with the premises (V4's
  confirmation/contradiction edges).
- Failure modes: (a) SELF-CONFIRMATION LOOP: the learner confirms its
  own promoted outputs (every MAP execution that isn't contradicted
  accrues standing); standing then measures un-contradictedness, not
  truth. A false MAP in a domain with no disconfirming observations
  accrues standing indefinitely. (b) PAST-PERFORMANCE TRANSFER: standing
  reflects the premises' history, but the candidate's novel composition
  step is unverified; well-supported premises can license a bad glue
  step. (c) COLD START: novel premises have no standing; the criterion
  rejects genuine discovery built from new observations.
- Self-deception mode: the learner builds an edifice of mutually
  supporting falsehoods, each verified by the standing of the others.

### C5. Structural contract satisfaction

Accept iff the candidate satisfies structural contracts: output slots of
step N match input slots of step N+1, no dangling references, guard
coverage on branches, frame-slot discipline. (Plan-constructor G5's
"type/contract check" option; requires G2 contract metadata.)

- Grounding: the candidate's own structure, checked against contract
  rules.
- Failure modes: contracts check FORM, not content. A well-formed graph
  can compute the wrong answer; H2A's wrong 2-hop chain is perfectly
  well-formed. Worse: WHO WRITES THE CONTRACTS? If researcher-written,
  this is researcher judgment in a new costume (the criterion-mechanism
  doc's warning about "researcher judgment wearing a learner-state
  costume" applies). If learner-written, the contracts themselves need
  verification, which is the regress again.
- Self-deception mode: the learner verifies syntax and mistakes it for
  semantics.

### C6. Simplicity preference (Occam gate)

Among executing candidates, accept the one with the shortest
description (fewest cells, fewest steps). The learner computes
description length itself; no oracle needed.

- Grounding: the candidate structures themselves.
- Failure modes: (a) SIMPLICITY IS NOT TRUTH, and H2A is designed to
  punish exactly this: the wrong 2-hop chain is simpler than the true
  3-hop chain. A simplicity criterion does not merely fail the trap; it
  actively prefers the trap's wrong answer. (b) The simplicity ordering
  over structures is a researcher-chosen bias (why count cells rather
  than edges?) unless the learner can revise it from experience, which
  needs its own write path and criterion. (c) Adversarial worlds can
  always make the truth complex.
- Self-deception mode: the learner mistakes its own aesthetic bias for
  a law of the world. This candidate is included as a warning: it is
  the most tempting and the most dangerous.

### C7. Knowledge-base coherence (non-contradiction)

Accept iff the candidate's answer does not contradict already-promoted
MAPs and facts. The learner's existing knowledge is the standard.

- Grounding: the learner's own promoted knowledge.
- Failure modes: (a) COHERENCE WITH ERROR: the knowledge base may be
  wrong; the criterion then rejects truths that would correct it. This
  is conservatism as a design principle: genuinely novel discoveries
  contradict old beliefs by definition. (b) The criterion cannot
  distinguish "contradicts because the candidate is wrong" from
  "contradicts because the old belief was wrong"; that distinction IS
  the verification problem, restated. (c) In the H2B lie trap, the lie
  is designed to be consistent with the taught facts; coherence passes
  it.
- Self-deception mode: the learner achieves perfect consistency by
  never learning anything new. Coherence is necessary for rationality
  but insufficient for verification; it is a veto, not a license.

### C8. Withhold-on-uncertainty (meta-criterion)

Rather than verifying the candidate, the learner verifies its own
epistemic state: if uncertainty is high (multiple competing candidates
with similar support, low premise standing, high recent contradiction
rate in the domain), WITHHOLD commitment: do not promote, record the
uncertainty, optionally inquire. This is the H2A trap's actual demand:
the honest answer under the withhold trap may be "insufficient evidence
to commit" rather than "pick the true chain."

- Grounding: the learner's own decision-state statistics (candidate
  count, support spread, domain contradiction rate).
- Failure modes: (a) THE UNCERTAINTY MEASURE NEEDS A CRITERION: what
  counts as "too uncertain" is a threshold requiring its own write path
  (regress, but at the meta level). (b) LEARNED HELPLESSNESS: excessive
  withholding means the learner never commits and therefore never gets
  the prediction-error feedback (V4) that would improve it; caution
  starves learning. (c) The withhold decision itself can be wrong in
  both directions (withholding a verifiable truth; committing under
  unrecognized uncertainty), and detecting THOSE errors needs a further
  check.
- Self-deception mode: the learner mistakes timidity for wisdom, or
  uses uncertainty as an excuse to avoid ever being wrong on the record.
- Note: this is the only candidate that directly answers H2's
  accept/reject/WITHHOLD framing. The other seven are accept/reject
  criteria; this one adds the third option the key question names.

### 3.1 Cross-cutting observations

- No candidate is self-sufficient. C3 (agreement) fails on correlated
  premises; C4 (provenance) fails on self-confirmation; C7 (coherence)
  fails on novel truth. The failure modes are DIFFERENT, which is the
  important property: a conjunction of partially-independent weak
  criteria can outperform any single one, provided their failures do not
  correlate. Correlated failure (all candidates sharing one bad premise)
  defeats every conjunction too; that case is handled only by V4-style
  post-hoc observation, i.e., by being wrong and surviving it.
- Every candidate except C1/C2 needs at least one learner-state
  parameter (threshold, weights, uncertainty measure) with a write path.
  The write path is where Micah's theater rule bites: a parameter that
  is set once and never updated by prediction error is not a
  learner-internal criterion, it is a source literal with extra steps.
- The deepest issue is temporal: pre-commit verification (judging before
  promoting) and post-hoc correction (V4 contradiction leading to
  revision) are complements, not substitutes. TNN-2 has only the latter
  (and only via researcher-fixed revision surgery). A learner that
  cannot verify before committing must be able to survive being wrong;
  a learner that cannot revise after committing must verify perfectly.
  TNN-2 currently does neither well: V1's masked branch commits blindly
  and V2's revision accepts on "runs."

---

## 4. Gap analysis: minimal machinery

Building on the criterion-mechanism doc's Gaps 1-4 (which cover the
broader accept/reject machinery), this section isolates the
VERIFICATION-specific delta: what must exist for V1's successor to judge
without `expected`.

### What is NOT needed

- No new node types, no new opcodes, no new modes/bridges/handlers
  (Alternative C holds: structural mutation opcodes stay deferred).
- No H1 widening: more assemblers change the candidate space, not who
  judges. The verification gap is orthogonal to the construction gap.
- No second graph type (Alternative D stays rejected).

### What IS needed (three components, all required)

**Component A: a correctness-substitute computation.** Something the
learner computes from its own state that stands in for `expected`.
This is NEW COMPUTATION, not a parameter tweak: TNN-2 has no function
that takes a candidate and returns a learner-grounded quality judgment.
The candidates in section 3 are the menu (agreement count, provenance
score, coherence check, uncertainty measure). Minimality note: exactly
one substitute is needed to start; the analysis in 3.1 argues for
eventual conjunction, but the minimal delta is one working substitute
with an exercised write path, not five.

**Component B: a threshold/decision field with read AND write paths.**
The substitute computation produces a score; the decision needs a
cutoff (or weight vector) in learner state, read by the verification
gate on the production path, and rewritten by a write path reachable
from prediction-error sites (V4's contradiction branch in `ev_observe`,
or a "promoted candidate later contradicted" detector). The write path
must be EXERCISED in transcripts: the evaluation must show the field
changing after the learner is wrong. This is the K-H3 audit standard
applied to verification, and it is where D6/D7 failed as theater.

**Component C: a triggering experience taxonomy.** The write path needs
defined triggers, i.e., the learner must be able to detect, without an
oracle, the events that should move the criterion. The available
detectors in TNN-2: (i) V4 contradiction (observation mismatches
promoted fact): the strongest, already exists; (ii) MAP-execution
surprise: an executed MAP's answer disagrees with a later observation
for the same (s,r): partially exists via the shadow-fact mechanism the
reuse experiment removed, needs re-thinking on the MAP-first path;
(iii) cross-candidate conflict: two promoted structures disagree, and a
later observation adjudicates: does not exist, needs the disagreement
to be recorded rather than resolved by bid-order.

### Why Component A is the hard one

Components B and C are bookkeeping: fields, paths, triggers. Component A
is the intellectual content: WHAT does the learner check? Each section-3
candidate has known self-deception modes, which means Component A cannot
be "pick the obvious substitute" but must be "pick a substitute whose
failure modes are detectable by Components B and C." Concretely: if the
substitute is cross-path agreement (C3), then the write path (B) must be
able to DOWN-WEIGHT agreement evidence when agreement-certified
candidates are later contradicted (C-trigger i). The criterion must be
revisable not just in its threshold but in its trust of its own
evidence. This is the point at which "learner-internal verification"
stops being a threshold and starts being a small learning system of its
own, which is why Micah's invention requirements list it alongside SUF
rather than beneath it.

### Relation to the criterion-mechanism gaps

- Gap 2 (parameterize `bid`) is the minimal path to Component B for a
  C4-style (provenance) substitute: the weights become the criterion
  fields, contradiction becomes the write trigger.
- Gap 3 (learner-held acceptance threshold in `t2_try_verify`) is
  Components A+B together for the unmasked-to-masked transition: it
  names the missing substitute explicitly ("a correctness-substitute
  computation") and is the largest single delta.
- Gap 4 (withhold gate) is the C8 direction: it needs an uncertainty
  measure (Component A at the meta level) plus its own threshold (B).
- H3-lite as drafted touches NONE of these: its three policy nodes move
  search order, guide defaults, and repair dispatch into learner state,
  which is genuine revisability of procedure, but no node is an
  accept/reject/withhold criterion. The criterion-mechanism doc states
  this explicitly; it is repeated here because conflating "revisable
  procedure" with "learner-internal verification" is the most likely
  category error in reading H3-lite results.

---

## 5. The H2 void, layer by layer

The void report establishes two independent layers. They must not be
conflated, because fixing one without the other still yields no
measurement.

### Layer 1: the trial never runs (world-design defect)

The H2 trap worlds teach direct facts for the query (s,r) (e.g., H2A:
(50001,50051,50002) and (50001,50051,50011); query is (50001,50051)).
`ev_query` calls `activate` first; on hit it returns the highest-bid
fact immediately (line 813-817). `mp_run` -> `t2_trial` ->
`t2_try_verify` is reached only on total miss. Result: on all H2 worlds
the masked/unmasked/lie manipulations, which target `t2_try_verify`,
have no effect; zero MAPs promoted; even the paired controls fail
(returning direct facts, not true answers).

Fix (world redesign, no source change): remove direct facts for the
query (s,r) so `activate` misses and the trial runs. The trap must force
multi-hop inference, not direct lookup. This is the void report's
recommendation 2, and it is correct as far as it goes.

### Layer 2: even when the trial runs, masked verification is vacuous
(criterion defect)

Suppose Layer 1 is fixed and the trial runs on H2A masked. The
candidates: the wrong 2-hop chain (50001->50002->50003, answer 50003...
per the world spec, the 2-hop reading) and the true 3-hop chain. BOTH
execute successfully. V1's masked branch accepts the FIRST candidate
with a clean execution value in the fixed researcher search order
(chains k=2 before k=3). The predicted outcome, recorded in the frozen
H2 prereg section 12, is K-H2-1 FAIL: the masked branch accepts the
wrong chain because "runs" does not discriminate true from false.

This is the deeper point of the void: Layer 1's fix makes the trial
RUN, but nothing in TNN-2 makes the trial JUDGE. The void report's
recommendation 4 ("test the trial path directly via mp_run with
synthetic workspaces") would measure the masked branch in isolation and
would measure exactly this: accept-first-that-runs.

### What should verification check against when there is no `expected`?

This is the question Layer 2 forces. The honest answers, given
sections 3-4:

1. **Against nothing currently available.** That is the finding, not a
   shrug: TNN-2's masked branch has no correctness-substitute (Component
   A), so a redesigned H2 measures the null criterion. The predicted
   K-H2-1 FAIL stands, and its evidentiary value is: the failure is now
   attributable to the criterion (Layer 2), not the world design
   (Layer 1). Attribution is information gain.

2. **Against later observation (two-phase redesign).** The trap worlds
   could be extended so the environment withholds the answer during the
   commit phase but presents a disconfirming observation later (the
   lifetime-stream framing: commit under uncertainty in world A, face
   evidence in world B). Verification is then tested in two parts: (a)
   was the commitment well-calibrated (did it withhold when it should
   have? C8), and (b) did the learner revise on the evidence without
   destroying unrelated structure (V4 -> revision path)? This converts
   H2 from a single-shot trap into a test of the verify-then-revise
   loop, which is the actual cognitive competence at issue.

3. **Against the learner's own uncertainty (withhold as success).**
   For H2A masked, the CORRECT behavior under a learner-internal
   criterion may be withhold, not "pick the 3-hop chain." Nothing in the
   world tells the learner the 2-hop chain is a trap; a learner that
   promotes the 3-hop chain has guessed right, not judged rightly. The
   redesigned bar should credit withhold-on-insufficient-evidence as a
   pass condition alongside correct selection, with the uncertainty
   measure subject to the same write-path audit as any other criterion.
   This is C8, and it is the only candidate that treats the H2 key
   question's third verb (withhold) as first-class.

4. **NOT against simplicity, NOT against the harness.** C6
   (simplicity) actively prefers the trap's wrong answer; any redesign
   that lets the harness leak the answer (e.g., "verification" against
   a hidden expected) reintroduces the oracle and voids the key
   question. The void report's t2_sig calibration failure is a
   cautionary tale here: the signature function is part of the
   measurement apparatus, and when the apparatus contradicts its spec
   (recording literals it must exclude), the evaluation is void rather
   than scored. The same discipline applies to verification redesign:
   if the "learner-internal" check can see the answer, it is not
   learner-internal.

### The t2_sig void as a verification parable

The H2 evaluation went void because the measurement instrument
(`t2_sig`) failed its own calibration: it recorded literals the spec
excluded. There is a structural parallel to the verification problem:
a criterion is a measurement instrument the learner applies to itself,
and TNN-2's instruments are either uncalibrated (masked: no standard)
or calibrated against the wrong thing (unmasked: the oracle). The void
is therefore not just a mishap; it is the verification problem
appearing one level up, in the evaluation apparatus. Any future
verification machinery should be held to the same calibration
discipline the prereg imposed on `t2_sig`: specify the properties first,
verify them before scoring, void on failure.

---

## 6. Connection to Micah's invention requirements and the continuous learner

Micah's entrance criterion for future construction work:

> SUF AND useful behavior AND learner-internal verification AND
> revisability AND cognitive reuse.

Learner-internal verification is listed as a CONJUNCT, not a corollary.
The analysis above shows why: SUF (the form not enumerable from source)
is about WHO DECIDES the structure; verification is about WHO JUDGES
it. A learner could in principle construct source-underdetermined forms
and still verify them against a harness oracle; that would satisfy SUF
and fail verification. Conversely, a learner could verify rigorously
against learner-internal standards while constructing only from fixed
templates; that would satisfy verification and fail SUF. The five
conjuncts are independent gates, and TNN-2 currently fails all five at
the relevant level (0 pure learner-owned structural decisions; 0 SUF
decisions; 0 learner-internal criteria; revision that is unsafe and
researcher-shaped; reuse shadowed by facts).

### The continuous-learner framing

Micah's architecture clarification reframes the target:

> FROZEN RESEARCHER CODE + CONTINUOUSLY CHANGING LEARNER STATE.

For verification, this framing dissolves a false dilemma. The
criterion-mechanism doc's section 5 already notes: "none of the gaps
above require freezing learner state. The criterion fields, once they
exist, are SUPPOSED to change continuously during evaluation." What must
stay frozen is the EXISTENCE AND SEMANTICS of the read and write paths,
not the values they carry. An evaluation that resets learner state
between H2 worlds can still test whether the criterion EXISTS (the
write path fires within each world); a lifetime evaluation across
worlds additionally tests whether the criterion IMPROVES, which is the
stronger claim:

- Does the false-promotion rate decline over the lifetime?
- Does the uncertainty measure calibrate (withhold when it should,
  commit when it should)?
- Does the learner's trust in its own evidence sources (Component A's
  substitute) adjust after the substitutes mislead it?
- Does revision preserve unrelated structure (no catastrophic
  forgetting of good criteria when bad ones are corrected)?

These are lifetime-stream measurements, reported separately from
isolation tests per the evaluation policy. The isolation test asks
"does the machinery exist"; the lifetime test asks "does it learn."
Both are needed; neither substitutes for the other.

### Cross-domain connection as verification fuel

The evaluation policy names cross-domain connection formation as a
FEATURE: "a structure learned for arithmetic recognized as useful for
planning." For verification, cross-domain agreement is potentially the
strongest form of Component A: if a causal abstraction learned in one
domain successfully predicts in another, that is C3 (consilience) with
genuinely independent premises, the case where agreement is hardest to
fake. This is speculative (no such machinery exists), but it locates
where the lifetime stream could supply what isolation tests cannot: a
verification signal whose independence is grounded in domain separation
rather than in construction-path bookkeeping.

---

## 7. Open questions (not conclusions)

1. **Which Component A first?** Section 3 offers eight candidates; 3.1
   argues no single one suffices and their failures must not correlate.
   But the minimal delta is ONE working substitute with an exercised
   write path. The analysis does not pick the winner; that choice needs
   its own preregistered comparison, because each candidate's
   self-deception modes are the actual experimental variable.
2. **Can the write path for a criterion be exercised without an
   oracle anywhere in the loop?** The triggers in 4 (V4 contradiction,
   MAP-execution surprise, cross-candidate conflict adjudicated by
   later observation) are all post-hoc. Pre-commit verification
   calibrated ONLY by post-hoc feedback is a slow loop; whether it
   converges, and how many bad promotions it costs, is unmeasured.
3. **Is withhold (C8) a separate bar or part of every bar?** H2's key
   question names accept/reject/withhold as three options, but K-H2-1/2
   are framed as accept/reject. If withhold-on-uncertainty is the
   honest answer to the trap, the bars need a withhold-credit condition
   with its own calibration discipline.
4. **Does V3's consensus idea generalize?** `bootstrap_miss` is the
   only learner-data-driven check in TNN-2, and it is crude (unanimity
   + theater threshold). Whether "agreement across my own observations"
   can be developed into a real Component A, or whether it is a dead
   end (unanimity is too strong, any quorum is arbitrary), is open.
5. **The regress terminus.** Every candidate's grounding eventually
   bottoms out in V4-style observation. Is observation-backed
   post-hoc correction plus pre-commit weak criteria (the
   verify-then-revise loop) SUFFICIENT for the invention conjunct, or
   does "learner-internal verification" demand a pre-commit standard
   with no oracle anywhere upstream? The requirement as stated does not
   resolve this; the lifetime measurements in section 6 are the
   empirical way to find out.

---

## 8. Standing architectural metric (this analysis)

| Metric | Value |
|---|---|
| RESEARCHER-OWNED STRUCTURAL DECISIONS | 5/5 inventoried checks (V1, V2 researcher; V3 mixed; V4 experience-driven post-hoc; V5 retrieval) |
| LEARNER-OWNED STRUCTURAL DECISIONS | 0 |
| SOURCE-ENUMERABLE FORMS | all verification rules |
| SUF DECISIONS | 0 |
| LEARNER-INTERNAL CRITERIA | 0 (V3 partial: learner data under fixed rule + theater threshold) |
| REUSE EVENTS | n/a (analysis) |
| REVISION EVENTS | n/a (analysis) |
| COGNITION LINES | 0 added, 0 modified (read-only) |
| MODES / BRIDGES / HANDLERS / SEMANTIC CASES | 0 / 0 / 0 / 0 |

**Verdict: VERIFICATION-CRITERION-COMPLETE.**
