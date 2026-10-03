# DESIGN.md: Difference-Driven Experiment Synthesis (DDES)

## Successor to H-CAUSALEXP-CONSTRUCT

Design only. No implementation. Committed before any builder work begins.

### 1. What died and why

H-CAUSALEXP-CONSTRUCT (BUILD-PASS 7/7, result `48f2adc15`) was killed as an
L3 construction claim by two independent adversaries:

- A2 (`ae9121f47`): an independent pure-Zag reimplementation written from the
  prereg spec alone produced byte-identical outputs. The learner is a pure
  deterministic function of (hypothesis pair, fixed 1364-sequence enumeration,
  researcher lexicographic order, researcher first-disagreement criterion,
  researcher MAXD=5).
- A1 (`cad84f070`): AX-CX1 (a pure-enumeration program reproduces the raw
  ordinals 3 and 15 exactly; lazy generation by counting IS enumeration);
  AX-CX2 (sealed World C requires depth 6, MAXD=5 is hardcoded, so the
  "unbounded in length" claim is false); AX-CX3 (the disagreement predicate
  only FILTERS the pre-enumerated stream; no algorithm step inspects
  hypothesis structure to propose candidates).
- Baseline (`48e24c825`, BASELINE-LOSES): the filter is genuinely useful
  (17x-85x fewer real-world actions than greedy, 4/4 novel-world
  generalization vs 0/2 for memorization), but usefulness is not construction.
- Ablation (`48cf64979`): the filter is load-bearing for correctness (0/4
  converge without it); simulation is load-bearing for efficiency (35x-254x);
  the depth bound is load-bearing for correctness (exactly 2/4 converge at
  MAXD=3).
- Transfer (`486136c15`, TRANSFER-PARTIAL): the filter principle transfers
  across primitive vocabularies, rule semantics, and domains, but not to
  compositional reuse. The architecture is one-level enumerate-and-filter,
  not a hierarchical builder.

Precise failure: the learner never inspects hypothesis structure to propose
candidates. The generation order is fixed before any hypothesis is consulted.
The disagreement test is a filter applied to a researcher-enumerated stream.

A1's guidance for the successor: "The next causal frontier needs
hypothesis-GUIDED generation, not hypothesis-FILTERED enumeration."

### 2. DDES architecture

Name: Difference-Driven Experiment Synthesis.

Core idea: derive the experiment from the symbolic difference between the
hypotheses. No candidate action sequences are ever generated and tested. The
plan is computed from structure, then executed exactly once.

#### 2.1 Hypothesis access (data, generic)

Hypotheses remain delay-rule sets as data: (src, dst, delay) triples, exactly
as in H-CAUSALEXP-CONSTRUCT. The learner accesses them only through generic
routines over the rule list (edge enumeration). There is no per-hypothesis
branch anywhere in the analysis or synthesis path.

#### 2.2 Difference analysis (the guided core)

Given two hypotheses h0, h1 and an intervention schema. Phase 1 schemas:
"set X:=1 at t0" and the null schema "no intervention".

1. Build the rule graph for each hypothesis: nodes are variables, edges
   src->dst weighted by delay.
2. Compute earliest arrival times: for each variable V, the earliest tick at
   which V becomes 1 under the intervention. This is a shortest-path
   computation (delays are non-negative; rules latch, so every variable's
   trajectory is a monotone step function fully determined by its arrival
   time). No action sequences are simulated.
3. The predicted observation at (V, t) is 1 iff earliest_arrival(V) <= t,
   else 0.
4. The disagreement frontier: the set of (V, t) where the two hypotheses
   predict different values. Because predictions are step functions,
   hypotheses disagree on V iff arrival0(V) != arrival1(V), and the earliest
   disagreeing t is min(arrival0(V), arrival1(V)). Computed analytically.
   There is no scan over t and no bound on t.
5. Select the target: the earliest (V*, t*) in the frontier across variables
   and schemas. Ties broken by a fixed generic rule (lowest variable id),
   documented and tested, not load-bearing.

If the frontier is empty under both schemas, report NO-DISCRIMINATING-PLAN
and perform zero real executions. There is no fallback to enumeration.

#### 2.3 Guided synthesis (incremental construction)

From the target (V*, t*), build the plan incrementally:

1. Start with the empty plan.
2. If the winning schema is set-X, append S. Justification: the analysis
   shows the frontier is empty or later without the initial condition.
3. While the plan's current time is less than t*, append W. Justification:
   each wait advances toward the computed target time. The count is derived
   from t*, not bounded by any constant.
4. Append observe(V*). Justification: V* is the variable where the frontier
   says the predictions differ.
5. The plan is complete. Exactly one plan is ever assembled.

Every append is a construction step whose choice is a function of
(hypotheses, target, partial plan). The plan length is determined by t*,
which is determined by the world's delays. There is no MAXD.

#### 2.4 Execution and elimination (unchanged)

Execute the single synthesized plan once against the sealed true world: zero
search in the real world. Observe, then eliminate hypotheses whose analytic
prediction mismatches the observation. The predictor used for elimination is
the same analytic predictor used in synthesis.

### 3. Worked derivations

World A: H0 = (X,Z,2),(Z,Y,0); H1 = (X,Y,1).
- Arrivals under set-X at t0: H0 gives Z@t0+2, Y@t0+2. H1 gives Y@t0+1.
- Frontier: Y differs on [t0+1, t0+2). Target: (Y, t0+1).
- Plan: [S, W, OY]. The old learner found this same plan by checking 3
  candidates. DDES derives it with 0 candidates considered.

World B: H0 = (X,Z,3),(Z,Y,0); H1 = (X,Y,2).
- H0: Z@t0+3, Y@t0+3. H1: Y@t0+2. Target: (Y, t0+2).
- Plan: [S, W, W, OY].

World C (A2's sealed killer): H5 = (X,Z,5),(Z,Y,0); H6 = (X,Y,4).
- H5: Y@t0+5. H6: Y@t0+4. Target: (Y, t0+4).
- Plan: [S, W, W, W, W, OY] (length 6). No bound is consulted, because no
  bound exists.

World D (Z-only hypotheses, cf. transfer test): the hypotheses differ only
on Z timing.
- Frontier selects (Z, t*). The plan ends with OZ, not OY. The observed
  variable is chosen by the analysis, never hardcoded.

### 4. Why this is not a disguised menu

Point-by-point against the kills:

- vs AX-CX1 (finite researcher-enumerated family): there is no family. No
  routine generates sequences. The plan is derived by analysis; the specific
  plan did not exist anywhere (not in source, not in a list) before
  derivation. A pure-enumeration program cannot reproduce DDES outputs
  without reimplementing the analysis, in which case it IS the analysis.
- vs AX-CX2 (depth bound load-bearing): there is no depth constant. World C
  (length 6) and any deeper sealed world work by construction, because plan
  length is computed from delays.
- vs AX-CX3 (filter never guides): there is no filter. Nothing is generated
  and then tested. Hypothesis structure (the rule graph, the delays)
  determines every construction choice: which variable (frontier), how many
  waits (target time), whether to intervene at all (schema comparison).
- vs the template objection ("[S, W x t, O V]" with V and t as filled
  parameters): the linear shape is constrained by the world's action API
  (set, wait, observe are the only actions that exist), not by a researcher
  template. Within that API, every degree of freedom (intervene or not,
  which variable, how long) is derived from hypothesis structure. Phase 2
  (section 8) removes even the linear shape.

Anticipated A2 counter: "the (variable, time) frontier is the real menu."
Response: the frontier is not enumerated; it is computed analytically
(shortest-path arrival times, disagreement by inequality of arrival times).
The output is the argmin of a computed function, not the first match in a
list. There is no list.

### 5. Residual researcher authority (honest)

DDES does not claim L3. The researcher still owns:

1. The primitive action vocabulary (S, W, OY, OZ): it is the world's API.
   The learner cannot invent new actions.
2. The hypothesis representation (delay rules as data): the format is
   researcher-designed. The analysis is generic over it, but the format
   itself is given.
3. The difference-analysis algorithm (shortest path, frontier computation):
   researcher-written generic machinery. The learner does not invent the
   method of analysis.
4. The intervention schemas considered (set-X, null): a small fixed set.
   Phase 2 expands this.

What the learner authors (derived per world, on no list): whether to
intervene, which variable to observe, the exact plan length, the full action
sequence. The specific experiment did not exist before the learner derived
it.

Classification target: strong L2 (guided generation), a strict improvement
over filtered enumeration. L3 would require the learner to invent its own
hypothesis representations or its own analysis methods (section 6).

### 6. What would make this L3

Recorded as the bar for the successor's successor; DDES Phase 1 does none of
these:

- The learner invents a new hypothesis representation (not delay rules)
  when delay rules fail, and constructs analysis machinery for it.
- The learner extends its own action vocabulary (e.g., invents a reusable
  "wait until" composite) and reuses the invention.
- The learner revises the difference-analysis method itself after a
  predictive failure.

### 7. Prereg-ready kill bars

The builder prereg must freeze every bar below before implementation.
BUILD-PASS requires all of them. Amend transparently and re-freeze if any
bar is broken; never alter a bar after seeing results.

Validity bars:

- V-NX1: Worlds A and B converge correctly (4/4 configs), exactly 1 real
  execution per config.
- V-NX2: 3/3 byte-identical runs, exit 0, zero stderr.
- V-NX3: pure Zag, zero Python, zero em-dash bytes.

Kill bars:

- K-NX1 (no enumeration, static): source audit. The committed source must
  contain no routine that generates all sequences of length <= D over the
  primitive set, and no numeric constant that bounds plan length. Method:
  reviewer reads the full synthesis path. Any sequence-generating loop or
  length constant kills the bar.
- K-NX2 (no enumeration, behavioral): instrument the learner to count
  candidate complete plans assembled and compared before selection. On
  Worlds A and B the count must be <= 8. (Guided synthesis assembles
  approximately 1.) Kill: count >= 100.
- K-NX3 (sealed depth): after freeze, the adversary supplies a world
  requiring L actions with L >= 8, where L exceeds every length constant in
  source (there must be none). The learner must converge with exactly 1
  real execution. Kill: NO-DISCRIMINATING-PLAN, or more than 1 execution.
- K-NX4 (structure sensitivity): two sealed worlds differing only in rule
  delays. Without any source change, the learner must produce
  correspondingly different plans matching the analytically computed
  targets. Kill: identical plans for both worlds, or a plan that does not
  match its computed target.
- K-NX5 (variable choice): a sealed world whose hypotheses differ only on
  Z timing. The learner must emit a plan observing Z and converge. Kill:
  an OY-only plan, or failure to converge.
- K-NX6 (C0-A source audit): no branch on specific delay values, variable
  ids, or world ids anywhere in the analysis/synthesis path. Kill: any
  delay==2-style dedicated case.
- K-NX7 (one-shot derivation): on at least one sealed world, the learner
  emits the discriminating plan having assembled <= 3 candidate plans
  (per the K-NX2 instrumentation). This is the positive evidence of
  guidance as opposed to search.
- K-NX8 (empty-frontier honesty): a sealed world on which both hypotheses
  agree everywhere under both schemas. The learner must report
  NO-DISCRIMINATING-PLAN and perform 0 real executions. Kill: any real
  execution, or a fabricated plan.

### 8. Phase 2 sketch (compositional generation)

Phase 1 derives linear plans. Phase 2 extends the schemas and the synthesis:

- Richer schemas: multiple sets (set X, wait, set X again), mid-plan
  observation.
- The frontier analysis generalizes to partial plans: earliest arrivals
  under the plan so far; the learner extends the plan at the point of
  maximal expected frontier growth.
- Draft kill bar for Phase 2: a sealed world on which no linear plan
  discriminates but a two-set plan does; the learner finds it with no
  enumeration (K-NX2-style count <= 8).

Phase 2 is not part of the Phase 1 builder prereg. It is recorded here so
the Phase 1 design does not foreclose it.

### 9. Key insight

The failure of H-CAUSALEXP-CONSTRUCT was not that its filter was useless:
the filter saved 17x-85x real-world actions and generalized 4/4 to novel
hypothesis pairs. The failure was architectural: the learner chose among
options instead of deriving the answer. DDES moves the intelligence from
selection to derivation. The experiment is computed from the symbolic
difference between the hypotheses, so there is nothing to enumerate, no
bound to hit, and no menu to disguise.
