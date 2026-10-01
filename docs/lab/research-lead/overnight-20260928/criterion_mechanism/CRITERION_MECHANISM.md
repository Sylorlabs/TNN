# Criterion Mechanism Analysis

**Status:** Analysis only. Read-only white-box of frozen TNN-2
(`tnn2_build/tnn2.zag`, 1591 lines). No implementation proposed beyond
what the task asks: the mechanism space and the minimal delta.

**Purpose:** Interpretation framework for H2 / K-H2-3. The H2 key
question: "Can TNN accept/reject/withhold structures using a
learner-internal criterion when the environment does not provide the
expected answer?" K-H2-3 requires (a) a learner-created persistent value
in the causal chain of an accept/reject decision, (b) ablation of that
value alone flipping the decision, (c) an experience log showing the
criterion changing after prediction error.

---

## 1. Inventory: TNN-2 accept/reject machinery

Seven decision points were found by white-box inspection. For each: the
exact location, the inputs the decision reads, and whether any input is
learner-created.

### D1. Trial candidate acceptance: `t2_try_verify` (line 497)

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

Inputs read: the executed value `v` (computed, not stored); `expected`
(environment-supplied oracle, passed down from `ev_query`); `masked`
(flag derived from `ev_query`'s `flags` argument). The stats buffer `st`
records tried/rejected counts into header field 16 (learner state), but
those counts are never read back by any decision. They are write-only
telemetry.

The acceptance rule: in masked mode, any successful execution passes; in
unmasked mode, only exact match with the environment's expected answer
passes. Nothing in this rule is learner-created. The `expected` value is
the environment providing the answer, which is exactly what H2 withholds.

**Classification: RESEARCHER-OWNED.** (DOF map J2, J3 agree.)

### D2. Graph promotion: `promote_graph` (line 533)

Unconditional once `t2_try_verify` returns non-`-2`. Creates the tag-20
MAP node with fixed layout (field4=r, field8=s, field20=graph root,
field24=promotion index, field28=answer), provenance DEP edges to
licensing facts, and the shadow `ev_teach_in(W,s,r,ans)` fact (the fact
that the reuse experiment later deleted on an unfrozen variant). There
is no second gate: verification success implies promotion.

**Classification: RESEARCHER-OWNED.** (DOF map J5, J6, J7 agree.)

### D3. Trial search order and family gating: `t2_trial` (line ~590)

Fixed phase order in source: chains k=2..4, then sums in descending
subset size, then counts, then single hops. The `dc` and `di` flags gate
the chain and count families; they derive from `ev_query`'s `flags`
argument. In production the flags are caller-supplied test parameters,
not learner state. First candidate to verify stops the search.

**Classification: RESEARCHER-OWNED** for the order and gating.
**MIXED** for the stop rule (DOF map K4): the candidate space is
populated from learner-state facts, but the first-to-verify rule under
the fixed order is researcher-fixed.

### D4. Revision acceptance: `t2_revise_graph` (line ~706)

Trigger: `ev_observe` contradicts a fact that licenses a MAP
(`revise_on_contradict`, line 685). The repair is built by
researcher-fixed topology surgery (find the stale SETREG step via
provenance, tombstone it, insert a corrected step, rewire). Acceptance:
`out != -999999` after re-execution, i.e., the repaired graph runs. On
failure the graph is reverted in place (the allocator-alias corruption
bug documented in `8b58c4104` lives here; the copy-and-commit experiment
Micah approved addresses it). On success the new answer is taught and
the MAP's field28 updated.

Inputs read: the contradiction (environment), provenance edges (learner
state), execution result (computed). The acceptance criterion, successful
re-execution, is a source literal.

**Classification: RESEARCHER-OWNED** for the acceptance criterion;
MIXED for the target selection (provenance is learner state, the
surgical procedure is researcher-fixed).

### D5. Guide selection: `ev_act` (line 859), `bid` (line 237)

```zag
fn bid(W,n)i32 {
  let c:i32=evcount(W,n,1)+evcount(W,n,2)+evcount(W,n,6)+evcount(W,n,7)-evcount(W,n,3);
  ...
}
```

`ev_act` selects the context-matching guide with maximal `bid`, ties
broken by edge-id order. The event counts are learner-state-derived:
edge type 1 (DEP/provenance uses), 2 (MAP standing increments), 6
(activation/usage markers), 7 (confirmation markers), minus type 3
(contradictions). So the *magnitudes* come from experience, but the
*formula*, which event types count positively and that contradictions
subtract, is a source literal. No learner-state value anywhere alters
which terms are added or subtracted, or their weights.

**Classification: MIXED.** (DOF map M4 agrees: space from learner state,
rule fixed.) This is the closest TNN-2 comes to a learner-internal
criterion, and it still fails K-H2-3(a): ablating experience changes the
magnitudes, but there is no single learner-created persistent *value*
whose ablation flips a decision while holding all experience fixed,
because the criterion has no parameters, only the fixed formula applied
to raw counts.

### D6. Miss policy dispatch: `mp_run` (line 668)

```zag
fn mp_run(W,s,r,expected,flags)i32 {
  let masked:i32=flags&1; let dc:i32=(flags>>1)&1; let di:i32=(flags>>2)&1;
  return t2_trial(W,s,r,expected,masked,dc,di);
}
```

The MISS_POLICY node (node 1, tag 901, field 20 via `mp_get`/`mp_set`)
exists in learner state but `mp_run` never reads it. `mp_set` has no
production caller (only a test at line 1010/1011). This is the clearest
theater instance in TNN-2: a policy node in learner state with no
production read path and no production write path.

**Classification: RESEARCHER-OWNED** in effect (the node is inert).
Under Micah's theater rule this node must not be cited as a
learner-owned decision.

### D7. P-INV bootstrap threshold: `k_get` / tag-903 node (lines 751-761)

The k threshold (default 3) is stored in a learner-state node (tag 903,
field 20). `k_get` creates it with default 3 if absent. There is no
production write path that ever updates it. A value in learner state
with no exercised write path is theater: it is a source literal (3)
with extra steps.

**Classification: RESEARCHER-OWNED** in effect.

### Withhold path

`ev_query` on total miss calls `miss_inquire` (line 796), which creates
an UNCERTAINTY node (tag 30) and a guide linked to POLICY_ROOT. There is
no withhold *decision*: the system always inquires on miss; it never
evaluates whether inquiry is warranted. Withholding as a criterion-gated
choice does not exist.

---

## 2. Classification summary

| ID | Decision point | Inputs from learner state? | Classification |
|----|---------------|---------------------------|----------------|
| D1 | Trial acceptance (`t2_try_verify`) | No (expected is environmental) | RESEARCHER |
| D2 | Promotion (`promote_graph`) | No (unconditional) | RESEARCHER |
| D3 | Search order / gating (`t2_trial`) | Space only (stop rule) | RESEARCHER / MIXED (stop) |
| D4 | Revision acceptance (`t2_revise_graph`) | Target only (procedure fixed) | RESEARCHER / MIXED (target) |
| D5 | Guide selection (`bid` in `ev_act`) | Event-count magnitudes | MIXED |
| D6 | Miss policy (`mp_run`) | None (node inert) | RESEARCHER (theater node) |
| D7 | P-INV threshold (tag 903) | None (never rewritten) | RESEARCHER (theater node) |

Pure learner-owned accept/reject decisions: **0**. This matches the DOF
map (`d2af26581`): 0 pure learner, 5 mixed, ~240 researcher. The H2
prereg (commit `c15a47d63`, section on predicted outcomes) records the
same expectation: the accept decision reads exactly three inputs (v,
expected, masked flag).

---

## 3. What a learner-internal criterion would look like

Mechanistically, not aspirationally. For K-H2-3's three sub-clauses to
be satisfiable, the following six elements must exist. This mirrors the
K-H3 write-path audit format Micah required for H3-lite, because the
underlying demand is identical: a value in learner state is only a
criterion if it sits in a production causal chain with an exercised
write path.

### (i) Learner-state fields holding the criterion

At least one persistent field whose value is not a source literal and
not a verbatim copy of an observation. Examples of the *shape* (not a
design): a per-family acceptance threshold; a weight vector over the
`bid` event-type terms; a withhold-vs-inquire threshold compared against
an uncertainty magnitude. The field must be addressable by both a read
path and a write path below.

### (ii) Production read path

A function on the accept/reject path that loads the field and branches
on it. Concretely: `t2_try_verify` (or its successor) must consult the
field when deciding accept vs reject, or `ev_act`'s selection must
weight by it, or a withhold gate must compare against it. The read must
be on the path that actually fires during the sealed evaluation, not in
dead code. D6 is the cautionary example: `mp_get` exists, is never
called in production, and therefore reads nothing.

### (iii) Production write path

A function, reachable from `ev_observe`, `ev_query`, or `ev_act` during
ordinary operation, that stores a new value into the field. The write
must be *exercised*: the evaluation transcript must show the write path
firing. D7 is the cautionary example: the tag-903 node is created in
learner state and never rewritten.

### (iv) Triggering experience

The write path must fire in response to a prediction error or an
outcome the learner can detect without the environment handing it the
criterion. Acceptable triggers: a contradiction on a promoted fact
(`ev_observe` with mismatching `o`); a trial candidate that verified
against `expected` but later proved wrong; an executed MAP whose answer
disagrees with a later observation. Unacceptable: the researcher writing
the value during setup, a test harness poking it, or the value being set
once at creation and never touched again.

### (v) Sealed behavioral variation (K-H2-3(b))

Ablating the learner-created value alone, holding all experience fixed,
must flip at least one accept/reject decision. This is the anti-theater
clause. D5 (`bid`) fails it: zeroing all experience changes decisions,
but there is no parameter to ablate independently of the experience
itself. A genuine criterion has parameters separable from the data they
were learned from.

### (vi) Experience-driven change (K-H2-3(c))

The committed experience log must show the criterion's value changing
after a prediction error. Not at initialization, not by test setup, but
in response to the learner being wrong about something.

---

## 4. Gap analysis: minimal architectural delta from TNN-2

Ranked from smallest to largest. None of these is claimed to be
sufficient for H2; the ranking is by how little of TNN-2 must change for
the mechanism space to contain a genuine learner-internal criterion.

### Gap 1: Give the inert nodes their missing paths (smallest delta)

D6 (MISS_POLICY) and D7 (tag-903 k) already have learner-state fields
and, for D6, a getter/setter pair. The delta is: (a) make `mp_run`
actually read `mp_get` and branch on it; (b) add a write path from a
prediction-error site (e.g., repeated trial failure in `t2_trial`, or
contradiction in `ev_observe`) to `mp_set`. This converts theater into
machinery. It does not by itself satisfy K-H2-3, because the *content* of
the policy would still need to be a criterion rather than a flag, but it
is the smallest change that makes the write-path audit non-vacuous.

Estimated surface: one read-path branch, one write-path call site, the
policy value semantics. No new node types, no new opcodes.

### Gap 2: Parameterize `bid` (small delta, targets D5)

Today `bid` is a fixed formula over five event counts. The delta:
store per-term weights in learner state (five fields on the POLICY_ROOT
node or a dedicated criterion node), have `bid` read them, and add a
write path that adjusts weights after prediction errors (contradiction
decrements the weights of the terms that voted for the losing guide;
confirmation increments). Then K-H2-3(b) becomes testable: zero the
learned weights while holding event counts fixed and the decision
flips. This is the natural minimal step from "magnitudes from
experience, formula from researcher" to "magnitudes and formula
parameters from experience."

Estimated surface: weight fields, read in `bid`, one update rule,
triggered from existing contradiction/confirmation sites.

### Gap 3: Learner-held acceptance threshold in `t2_try_verify` (medium delta)

D1's unmasked rule (`v == expected`) outsources judgment to the
environment. A learner-internal replacement needs a *substitute source
of correctness* the learner can compute: e.g., consistency of the
candidate's answer with already-promoted facts, agreement across
independent trial families, or a confidence value accumulated from the
candidate's provenance strength. The delta is larger because TNN-2 has
no such substitute; the DOF map (item 9, line 399) flags exactly this:
"Consult a learner-held acceptance threshold or consistency check in
`t2_try_verify` instead of the external `expected`." In masked mode H2
already removes `expected`, and the current fallback (accept any
successful execution) is too weak to be called a criterion, it accepts
everything that runs.

Estimated surface: a correctness-substitute computation, a threshold
field with read and write paths, and a trigger (e.g., later
contradiction lowers the threshold that admitted the bad candidate).

### Gap 4: Withhold as a criterion-gated choice (larger delta)

TNN-2 has no withhold decision; `miss_inquire` fires unconditionally.
A withhold criterion needs: (a) an uncertainty magnitude the learner
computes (not the UNCERTAINTY node's existence, which is just a tag);
(b) a threshold field; (c) a gate that withholds inquiry (and
promotion) when uncertainty is below threshold, i.e., the learner
judges the candidate not worth committing to. This is new decision
machinery, not a parameterization of existing machinery.

### What does NOT close the gap

- Adding more trial families or assemblers (H1 widening). This changes
  the candidate space, not who judges.
- Storing more values in learner state without read/write paths (more
  theater nodes like D6/D7).
- Tuning source literals (threshold constants, orderings) between
  evaluations. That is researcher judgment wearing a learner-state
  costume.
- The H3-lite policy nodes as currently drafted: they move *search
  order*, *guide defaults*, and *repair dispatch* into learner state,
  which is genuine revisability of procedure, but none of them is an
  accept/reject/withhold *criterion*. H3-lite and the criterion gap are
  adjacent but distinct.

---

## 5. K-H2-3 interpretation guidance

For the running H2 evaluation, this analysis predicts the following
white-box checks, in order:

1. **Enumerate the actual inputs** to every accept/reject/withhold
   decision that fires during H2A/H2B/H2C. The predicted set is
   {executed value, expected-or-absent, masked flag} for D1; {event
   counts} for D5; nothing else. Any input outside this set is a
   discovery and must be documented as such.

2. **Test sub-clause (a)** by searching learner state for a value that
   is both learner-created (not a source literal, not a verbatim
   observation copy) and loaded on the decision path. The known
   candidates (MISS_POLICY field, tag-903 k, `bid` weights) are
   predicted absent or inert per sections 1-2.

3. **Test sub-clause (b)** by ablation: for each candidate value found
   in step 2, zero or randomize it while holding all other state fixed
   and re-run the decision. Predicted result: no flip, because the
   values are either unread (D6), unwritten (D7), or nonexistent as
   parameters (D5).

4. **Test sub-clause (c)** by scanning the experience log for
   criterion-value changes following prediction errors. Predicted
   result: none, because no write path targets a criterion field.

5. **Record the failure mode precisely.** The informative outcome is
   not just "K-H2-3 FAIL" but *which* sub-clause fails and *where* the
   causal chain breaks: no field (fails a), field present but
   causally inert (fails b), or field updated but never by prediction
   error (fails c). Each points at a different gap in section 4.

A final note on the continuous-learner framing: none of the gaps above
require freezing learner state. The criterion fields, once they exist,
are *supposed* to change continuously during evaluation; that is the
FROZEN RESEARCHER CODE plus CONTINUOUSLY CHANGING LEARNER STATE ideal.
What must stay frozen is the *existence and semantics* of the read and
write paths, not the values they carry. An evaluation that resets
learner state between H2 worlds can still test the criterion (the
write path fires within each world); a lifetime evaluation across
worlds additionally tests whether the criterion *improves*, which is
the stronger claim and should be reported separately per the lifetime
protocol.

---

## 6. Standing architectural metric (this analysis)

| Metric | Value |
|---|---|
| RESEARCHER-OWNED STRUCTURAL DECISIONS | 7/7 inventoried (D1-D4, D6, D7 researcher; D5 mixed) |
| LEARNER-OWNED STRUCTURAL DECISIONS | 0 |
| SOURCE-ENUMERABLE FORMS | all accept/reject rules |
| SUF DECISIONS | 0 |
| LEARNER-INTERNAL CRITERIA | 0 (D5 magnitudes only, no parameters) |
| REUSE EVENTS | n/a (analysis) |
| REVISION EVENTS | n/a (analysis) |
| COGNITION LINES | 0 added, 0 modified (read-only) |
| MODES / BRIDGES / HANDLERS / SEMANTIC CASES | 0 / 0 / 0 / 0 |

**Verdict: CRITERION-MECHANISM-COMPLETE.**
