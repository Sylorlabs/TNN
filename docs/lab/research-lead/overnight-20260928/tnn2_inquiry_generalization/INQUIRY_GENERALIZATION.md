# TNN-2 Inquiry Generalization Analysis

Status: ANALYSIS ONLY. Not a patch. Not TNN-3. No source was modified.
Purpose: input to TNN-3 root-cause clustering, per the standing rule that
failures are clustered by shared architectural cause, never patched per
world.

## 0. What the red team established

Commit `4e329c772` (INQUIRY-ATTACK-SUCCESS) verified the six-link causal
chain for TNN-2's inquiry mechanism (`miss_inquire`, `tnn2.zag` lines
795-812, frozen at `f4de7ff46`):

- L1 miss to inquire trigger: PASS, learner-originated.
- L2 uncertainty creation: PASS, learner-originated (T_UNCERT node with
  miss-specific slots).
- L3 discriminating need: HARDCODED. Guide slots are researcher constants:
  action 30, content -999 (`tnn2.zag` lines 805-808). The learner never
  computes what evidence would discriminate.
- L4 guide to POLICY_ROOT: PASS, learner-originated.
- L5 ACT selection: real machinery, trivially satisfied (one guide).
- L6 evidence updates behavior: ABSENT. No uncertainty resolution, no
  guide supersession anywhere in production code. Stale guides persist
  forever and stay ACT-eligible.

This document asks what genuine discriminating inquiry would require
architecturally, and how much of it fits inside the frozen ISA and the
existing learner-state machinery.

## 1. What a derived question representation would look like

### 1.1 The operational definition

A derived question is not a flag that says "I do not know." It is a
structure that encodes three things:

1. A set of competing hypotheses H = {h1..hn}, each with a distinct
   predicted consequence.
2. A set of candidate probes A = {a1..am} (observations the learner can
   actually make through its action interface).
3. A selection of the probe that maximally splits H: the probe whose
   possible outcomes eliminate the most hypotheses, or split them most
   evenly.

Nothing in the current mechanism represents any of the three. The guide
is a constant pointer; there is no H, no A, and no split computation.

### 1.2 Where the representation would live

The existing machinery already has the right shape for two of the three
pieces, unused:

- **Candidate probes as competing guides.** `ev_act` (lines 859-911) is a
  max-scan over POLICY_ROOT-linked candidates filtered by context match
  and gated by `is_superseded`. It already selects among competing
  guides; today it never sees more than one. A derived-question design
  generates several differentiated guide nodes per uncertainty and lets
  the existing selector choose. No new selection machinery is needed,
  only differentiated candidates and a better score than raw `bid`.
- **Hypotheses as persisted trial structures.** The trial loop already
  computes predicted answers for candidate graphs (`t2_try_verify` runs
  each candidate and records tried/rejected counts). What it does not do
  is persist the candidates. The predictions evaporate; only aggregate
  counts survive in header field 16. A hypothesis set is therefore
  available in principle at zero new representational cost: persist each
  tried candidate's root id, predicted value, and licensing facts, linked
  to the new UNCERTAINTY node.

- **The split computation** is the genuinely new algorithm (see 1.4 and
  section 5).

### 1.3 A concrete slot-level sketch (within existing node types)

Guide nodes today: type 1, slot4 = miss subject s (context key), slot20
= 30 (action), slot24 = -999 (dead payload, read by nothing). Free slots
on a guide: 8, 12, 16, 28, 32. Free slots on an uncertainty node: 8, 12,
16. Uncertainty node today: type 30, slot4 = -4 (excluded from ACT
context matching), slots 20/24 = (s, r) miss key, slot28 = 2, slot32 = 0.

A derived question could be represented without any new node or edge
type:

- One guide per candidate probe. slot20 = inquiry action kind (derived,
  not constant, if the world offers more than one inquiry action;
  constant 30 is legitimate only when the action set is a singleton).
- slot24 (currently dead) = the probe parameter: the sub-query target,
  e.g. the (s2, r2) whose answer would discriminate. This gives the dead
  payload its first consumer.
- slot28 = informativeness score: the number of persisted hypotheses this
  probe splits (computed at construction, see 1.4).
- Edges from each guide to the hypotheses it discriminates (existing
  ET_DEP or ET_REF), so the provenance of the score is inspectable in
  learner state rather than hidden in a scalar.

`ev_act`'s max-scan then compares informativeness (alone or combined
with `bid`) instead of `bid` alone. The comparison loop already exists;
only the compared quantity changes.

### 1.4 How the learner computes the split, using only the frozen ISA

The frozen ISA (MOVE/BEQ/INC/DEC over register frames, one `execute()`)
is not the constraint here. The split computation is ordinary Zag code
over learner state, using only existing accessors:

1. Persist trial candidates: for each candidate the trial loop already
   executed, record (root, predicted value v_i, licensing facts). This
   is bookkeeping at the existing `t2_try_verify` call sites.
2. For chain candidates, the predicted values are already computed. Two
   candidates with different predicted values disagree; the first link
   position where their value paths diverge identifies a discriminating
   sub-query (s2, r2): asking about that link decides between them.
3. For each candidate probe, count how many hypothesis pairs it splits.
   This is a scan over persisted hypotheses with equality comparisons,
   the same algorithmic shape as `activate`'s scan or `ev_act`'s
   max-scan. No new opcode, no new executor, no new mode.
4. Counterfactual execution, if needed for non-chain candidates, is
   already supported: `t2_exec(W, root, s0)` executes any graph on a
   fresh frame seeded with a hypothetical subject. The executor does not
   care whether the frame seed came from the world or from the learner's
   imagination. That is the honest counterfactual primitive, and it
   already exists.

The subtle point: the split computation as sketched is a
researcher-authored algorithm. It uses only frozen machinery, so it
violates no ISA freeze and triggers no falsifier, but it does not earn
L3 credit either. The L3 version would require the learner to construct
the divergence-finding procedure itself as an executable graph. The
trial loop constructs answer-graphs; nothing constructs
scorer-graphs. That gap is named explicitly in section 5.

### 1.5 What this fixes relative to the red-team attacks

- Ambiguous evidence (two warranted uncertainties): each uncertainty gets
  its own differentiated guide set; selection is by derived
  informativeness, not incidental `bid` ties.
- Locally attractive wrong questions: a probe that merely confirms the
  current best hypothesis splits zero hypothesis pairs and scores zero.
  Expected-split scoring is exactly the antidote to confirmation-shaped
  local attractiveness named in the adversarial battery brief.
- Misleading evidence: handled by the resolution transition (section 2),
  not by the question representation.

## 2. What a resolution transition on learning would require

### 2.1 The missing transition, precisely

Today `ev_observe` (lines 836-857) teaches the new fact and, on
contradiction, revises MAPs. It never consults T_UNCERT nodes. The
uncertainty created at miss time is write-only: created, linked,
selected from, never resolved. Two consequences the red team
demonstrated: resolved uncertainties stay ACT-eligible, and the `bid`
mechanism makes repeatedly selected guides progressively harder to
dislodge (each selection adds a type-6 self-edge via line 897, raising
`evcount` and therefore `bid`: rich-get-richer lock-in on a stale
guide).

### 2.2 The sketch, using only existing machinery

The supersession convention already exists and is already honored by
both selection paths: `is_superseded` (line 132) returns true when a
type-3 (ET_CON) self-edge exists on a node, and both `activate` and
`ev_act` filter superseded nodes out. Production code already creates
type-3 self-edges in exactly two places: `ev_observe`'s contradiction
branch (line 844, on the contradicted fact) and `t2_revise_graph`
(line 744, on the superseded answer fact). The resolution transition
is therefore a third call site of an existing convention, not new
machinery:

1. In `ev_observe`, after the fact (s, r, o) is learned (both the
   confirm branch and the miss-teach tail), scan T_UNCERT nodes whose
   slots 20/24 match (s, r).
2. For each match, create the type-3 self-edge on the uncertainty node.
   It immediately becomes invisible to any future scan that honors
   `is_superseded`.
3. Find its guides by scanning edges of type 1 (ET_DEP) whose target is
   the uncertainty node and whose source is a type-1 node with the
   inquiry signature; create type-3 self-edges on those guides. They
   drop out of `ev_act`'s candidate set through the existing gate.
4. Optionally link the new fact to the uncertainty with ET_CFM (7,
   corroboration): the resolution and its evidence stay inspectable in
   learner state, which is what makes the transition white-box rather
   than silent deletion.

Note what is deliberately reused rather than invented: tombstoning
versus supersession is an existing distinction in the codebase
(`t2_revise_graph` tombstones cells with tag 0; `is_superseded` gates
selection). Resolution wants the gate semantics (the node stays as
history, stops participating), so the type-3 self-edge is the right
existing tool.

### 2.3 The contradiction sub-case

If the arriving evidence contradicts what a live guide expected (once
guides carry expectations in free slots, per 1.3), the guide is not
merely stale but misleading. The same type-3 self-edge applies, with an
ET_CON edge from the evidence to the guide recording why. This is the
same pattern as `ev_observe`'s contradiction branch, extended from
facts to guides. The red team's Attack 2 (misleading evidence locks
in) is fixed by the same call site, not by a separate mechanism.

### 2.4 What resolution must not do

It must not delete the uncertainty node or its guides. Deletion
destroys the learning history that transfer and interference analysis
need (did this uncertainty resolve the same way before? does the
learner keep re-asking settled questions under memory pressure?).
Supersession preserves the record while removing eligibility, which is
why the existing convention is preferable to node reuse.

## 3. What information is available at miss_inquire time

The call site is `miss_inquire(W, s, r)` from `ev_query` line 833. Only
three values cross the boundary: the workspace, the miss subject, the
miss relation. Everything else must be recovered from W. What is there:

Available in W at that moment:

- The exact miss key (s, r), already recorded into the uncertainty
  node's slots 20/24.
- All stored facts: `inc_fill` gives the relation inventory of s;
  `t2_gather_sum` gives s's direct values and their licensing facts;
  `t2_rels` gives s's relations. This is the neighborhood the trial
  loop searched.
- MAP nodes (type 20): promoted graphs with provenance DEP edges to
  licensing facts. A miss adjacent to a MAP's licensed region is a
  different epistemic situation from a miss in empty territory; the
  distinction is readable from state.
- The 128-entry event log: recent queries, teaches, and acts with
  timestamps. A learner could read which past uncertainties resolved
  and what resolved them. Nothing reads the log today except tests.
- The 4-deep context ring: what the learner has been attending to.
  Already used as ev_act's relevance filter.
- `bootstrap_miss`'s byproduct (currently discarded): up to 6 recent
  values of relation r across subjects, and whether they agree. Value
  disagreement across subjects is itself a competing-hypotheses signal
  at the value level, available before any graph is built.

Conspicuously NOT available, by construction:

- The trial loop's candidates. `t2_trial` allocates its path buffer on
  the transient stack (`z_alloc`), executes candidates, keeps aggregate
  tried/rejected counts, and returns. By the time `miss_inquire` runs,
  the single most informative artifact of the failed search, which
  hypotheses were tried and what they predicted, has been discarded.
  The miss path is ordered trial, then bootstrap, then inquire, and the
  inquiry step inherits none of the trial's work. This ordering is the
  deepest architectural fact behind L3's hardcoded status: the question
  cannot be derived from hypotheses the learner was not allowed to
  remember.

Any derived-question design must therefore either persist trial
candidates before they evaporate (a bookkeeping change at the existing
`t2_try_verify` call sites) or re-derive candidates at inquire time
from W (a re-search). The first is cheaper and preserves the causal
link between the failed search and the question asked about it.

## 4. Could the trial loop generate candidate questions

Yes, with one criterion transplant. The trial loop's shape,
propose/execute/verify/promote, is already the shape of a question
generator. What changes is only the verifier:

- Today: propose candidate answer-graphs from the existing grammar
  (`t2_gather` paths, `t2_gather_sum` subsets, `t2_rels` counts;
  assembled by `t2_asm_chain`/`t2_asm_sum`/`t2_asm_count`), execute each
  on a fresh frame, verify against `expected`, promote the winner.
- As a question generator: propose candidate probe-graphs from the same
  grammar (a probe is a graph whose execution identifies a
  discriminating observation: the diverging-link sub-query of section
  1.4 is itself a chain prefix), execute each probe counterfactually
  against each persisted hypothesis via the existing `t2_exec` on
  hypothetical frame seeds, verify by discrimination score (how many
  hypothesis pairs the probe's possible outcomes split), promote the
  highest-scoring probe as the guide set.

Three honest caveats:

1. The verifier's `expected` input is the environment's post-hoc
   feedback (the E-ruling preserved in the code comments). A
   discrimination verifier needs no `expected` at all: the criterion is
   internal to the hypothesis set. This is a genuine architectural
   improvement, the question loop is self-supervised in a way the
   answer loop is not.
2. The candidate grammar is the same finite researcher-authored family
   the construction red team attacked (commit `340e94e3e`:
   CONSTRUCTION-ATTACK-SUCCESS, 3 templates, depth bounds, 96-path cap).
   A question generator built on `t2_gather`/`t2_asm_*` inherits exactly
   that finiteness. Derived questions from this loop are honest L2:
   derived from learner state, but drawn from a researcher-enumerated
   family. Open question invention would need the same open-construction
   story the construction lane still lacks. The two lanes share the
   bottleneck.
3. Probes must be executable against the action interface. The current
   ACT to driver contract is a single scalar (`CHOICE <int>`, driver
   line 97-98). A parameterized probe (action kind plus sub-query
   target) does not fit a scalar unless encoded into it or unless the
   question's content lives in learner state with the scalar as a key.
   Widening the channel is a driver interface decision, bankable for
   TNN-3, not a cognition change.

## 5. Within the frozen ISA versus new machinery

### (a) Fits inside the frozen ISA and existing learner-state machinery

All of the following use only the 4-op ISA, the existing node types
(1, 2, 20, 30), the existing edge types (notably 1 DEP, 3 CON, 7 CFM,
10 MEM), the existing executors (`execute`, `t2_exec`), and the
existing conventions (`is_superseded`, free slots, event log, context
ring):

- Persisting trial candidates as hypothesis structures linked to the
  uncertainty node (bookkeeping at existing call sites).
- Deriving probe parameters (diverging-link sub-queries) from persisted
  candidates by scanning value paths already computed during the trial.
- Scoring probes by hypothesis-pair splits with equality comparisons in
  ordinary Zag code.
- Representing each candidate probe as a guide node with derived
  slot20/slot24/slot28 and provenance edges to the hypotheses it
  splits.
- Selecting among competing guides by informativeness in `ev_act`'s
  existing max-scan.
- Resolving uncertainties and superseding guides on later learning via
  type-3 self-edges, discovered through existing edge scans.
- Recording resolution evidence with ET_CFM and misleading-evidence
  cases with ET_CON.

None of this needs a new opcode, a new node type, a new edge type, a
new mode, a bridge, a handler, or a parallel executor. The ISA freeze
is not the binding constraint on genuine inquiry.

### (b) Requires new machinery (honest accounting)

- The divergence-finding and split-scoring algorithm itself. It is new
  cognition source: researcher-authored Zag code in the cognition path.
  It is not an ISA change and it triggers no falsifier, but it must be
  counted in the architecture accounting as researcher-authored
  machinery, and it earns no L3 credit. Criterion C0-A is the tripwire:
  a dedicated pre-written semantic case for "what counts as
  discriminating" would kill an L3 claim; a general split-scoring
  procedure over learner-built hypothesis structures is the honest L2
  version.
- A learner-constructed scorer (the L3 version of the above): nothing in
  TNN-2 constructs scorer-graphs, and the 4-op frame/budget model would
  need scrutiny before hosting learner-built meta-computation. This is
  a research question, not a near-term change.
- The ACT to driver channel, if questions need parameters the world
  must receive. Widening `CHOICE <scalar>` is an interface change
  outside cognition; the driver stays zero-cognition either way.

### Minimal honest package

The smallest change that converts the current miss-flag into genuine
discriminating inquiry, all within (a):

1. Persist trial candidates (roots, predicted values, licensing facts)
   instead of only tried/rejected counts.
2. At `miss_inquire`, derive one guide per discriminating sub-query
   from the persisted candidates, with derived slots and an
   informativeness score.
3. Score competing guides by informativeness in `ev_act`'s existing
   max-scan.
4. On `ev_observe` learning, supersede matching uncertainties and their
   guides via the existing type-3 convention; record evidence links.

Everything else, open question invention, learner-built scorers, wider
action channels, is explicitly beyond this package.

## 6. Why the builder used a constant action

Three causes, in descending order of explanatory weight:

1. **Prereg specification gap (primary).** The frozen kill bars tested
   the structure of the chain, not the information content of the
   question. K-T2-4 required an UNCERTAINTY node, a constructed guide,
   and POLICY_ROOT linkage with no scaffolding. K-T2-5 required
   `ev_act` to return "a non-constant choice derived from
   learner-constructed guides," where "non-constant" was written
   against the TNN-1 failure mode: the hardcoded 0 fallback. The
   builder satisfied the letter exactly: the guides are
   learner-constructed (created on the real miss path from the miss
   key), and the returned 30 is read from the guide's slot20 rather
   than from a code constant at the `ev_act` site, and 30 is not 0.
   The build report (TNN2_BUILD_REPORT.md, Change 2) describes the
   guide as "built on the base's validated t_a2 act pattern," i.e. the
   previously validated inquiry-build piece from commit `18ed3331c`
   was integrated as specified. Nothing in K-T2-1 through K-T2-8
   required the guide's content to vary with the uncertainty or to
   discriminate between hypotheses. The red team attacked the spirit;
   the builder built to the letter. This is a prereg miss, not a
   builder defiance.

2. **Complexity tradeoff (secondary).** Deriving discriminating need
   requires everything in section 5(a): persisting candidates, a
   divergence finder, a scoring rule, a resolution path. That is a
   second mechanism of comparable size to the three changes the
   generation was scoped to (construction, inquiry integration,
   revision). Within one frozen generation, the builder closed the
   loop structurally and left the content constant. Given the kill
   bars as written, that was the rational allocation.

3. **Conceptual gap (tertiary but real).** Nobody had operationalized
   what a "discriminating need" is computed *from*. The prereg, the
   root-cause analysis (commit `ed38121d4`), and the build report all
   describe inquiry as "miss to UNCERTAINTY to guide to act." The
   question the guide is supposed to ask has no named source: the
   trial loop discards its candidates (section 3), so even a builder
   who wanted derived questions would have found no hypothesis set to
   derive them from without redesigning the trial loop's bookkeeping.
   The constant 30 was the minimal honest way to make the ACT path
   live given a scalar action interface and a prereg that did not ask
   for more.

Implication for governance: future inquiry kill bars must assert on
guide content variance (two different uncertainties produce different
guide parameters), on informativeness ordering (the selected probe
splits more hypotheses than the alternatives), and on resolution (a
later observation supersedes the uncertainty and its guides). Bars on
chain structure alone will be satisfied by constants again.

## 7. Clustering note for TNN-3

The inquiry failure shares its architectural cause with the other two
TNN-2 red-team findings:

- Construction (commit `340e94e3e`): the trial loop searches a finite
  researcher-authored family; verdicts (counts) are kept, candidate
  structures are discarded.
- Revision (commit `687ba0219`): a single-schema literal-patch
  procedure; the learner chooses operands while the researcher chose
  the topology.
- Inquiry (commit `4e329c772`): verdicts (miss admitted, guide built,
  action taken) are kept; the structures verdicts were about
  (candidate hypotheses, what would discriminate them, whether the
  question resolved) are never represented.

The shared cause: **TNN-2's learner state records verdicts but not the
structures verdicts were about.** Trial counts without candidates,
guides without questions, revisions without repair alternatives. All
three are generation failures in the sense of the TNN-1 root-cause
finding (commit `ed38121d4`): competent retrieval and standing, no
generation. The TNN-3 direction this points to is not three patches
but one: make the objects of cognition (candidates, questions,
repairs) persistent, inspectable, competing structures in learner
state, with selection and supersession as the general lifecycle. That
is the same "one learner-owned structural workspace" the continuing
learner lane already calls for.

## 8. Explicit non-claims

- Nothing in this analysis was implemented, executed, or measured. It
  proposes no source change.
- The derived-question sketch in sections 1 through 5 is an honest L2
  design: questions derived from learner state by a researcher-authored
  procedure. It does not satisfy C0-A (the discrimination procedure
  would be pre-written), C0-B (questions would come from the existing
  candidate grammar, a finite researcher-enumerated family), or C0-C
  (no fresh adversarial battery has touched it). No L3 is claimed or
  implied.
- A 9/9 FW regression score for TNN-2, if it materializes, would not
  validate this analysis; the FW battery postdates the design it would
  be validating against.
- The minimal package in section 5 is a candidate hypothesis for
  TNN-3 root-cause clustering. It has not been experimentally
  discriminated against the at-least-three alternatives the standing
  rules require before TNN-3.
