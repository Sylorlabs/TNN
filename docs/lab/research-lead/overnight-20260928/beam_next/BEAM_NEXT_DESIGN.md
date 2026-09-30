# Beam Next Design: G0 diagnostic, then conditional G1/G2/G3

Date: 2026-09-30. Worker: Beam Next-Design Architect.
Status: DESIGN ONLY. Not a preregistration. A future builder must write its
own preregistration (prereg-first rule) before implementing anything here.
No implementation exists at this commit. No .zag written or modified. No
binaries built. No runs executed. Zero Python at every stage.

## 0. Lineage and coordination

- Frozen beam (`q4_r3/q4_r3.zag`, commit `023b4f84a`): R3-FAIL. Arm 2
  (compositional target E = (D AND Y4) OR ((NOT D) AND Y5)) reaches 53/64
  at 24 IVs, never 64/64. HAS_D=1, so this is not re-derivation.
- Design 1 (niching + tax annealing + diverse IV, commit `27a8fd108`):
  BEAM-FAIL (commit `845d01bc`), F-DIVERSE-FAIL fired. Arm 2 reaches
  50/64 at 24 IVs, slightly worse than control. Arm 1 does not regress.
- U1-U7 unified (commit `1f303396b`): in flight under `beam_unified/`
  with a frozen prereg. This design does NOT redirect that builder and
  does not touch `beam_unified/` or `beam_impl/`. Its result is the
  governing data point for the unified direction.
- "The failing niched beam" in this document means: Design-1's beam now;
  the unified beam if it fails F-DIVERSE-FAIL. The G0 diagnostic is
  defined generically against whichever niched beam last failed, so this
  design does not go stale when the unified result lands.

## 1. What the post-mortem established (commit 47d5c0137)

Four causes, in causal order:

- Cause 1 (primary): the generation gap. Niching is retention machinery;
  diverse IV is selection machinery; neither creates E. The true 4-op E
  was never discovered in 24 IVs despite niching active in 72 of 76
  extends. The design fixed everything downstream of the bottleneck and
  nothing at the bottleneck.
- Cause 2 (mechanism hypothesis, testable): the species-merge rule kills
  novelty. With 72/76 extends at the 8-species cap, "merge the two
  smallest species by member count" ran constantly and preferentially
  destroys nascent singleton species: exactly the novel structural forms
  niching was meant to protect, before they establish a foothold.
- Cause 3: the IV policy cannot target what is absent from its hypothesis
  set. Disagreement among wrong hypotheses does not concentrate on the
  overfitter's failure modes, so Fold 2 (no refuting evidence) was not
  actually fixed either.
- Cause 4: the tax ceiling held by design. At the final tax the
  overfitter at full fit still outscores E at full fit, so escape
  requires refuting evidence, which per Cause 3 never arrived.

Net: the binding constraint is generation, not retention or selection.
The post-mortem's standing recommendation: G0 diagnostic first (highest
information); do not build fixes before G0 data exists; do not build a
third retention/selection variant without new diagnostic information.

## 2. The generation loop, grounded in frozen code

From `q4_r3.zag` `beam_extend` (line 382):

- Candidates emitted per round: beam members carried forward, plus NOT
  of each member (op 2, unary), plus all pairwise AND (op 0), OR (op 1),
  XOR (op 3) combinations of beam members. Dedup via sigtab and the
  round-local `seen` set. All candidates scored on the current evidence.
  Frozen retention: top 32 by (score desc, opc asc, node id asc).
- E = OR(AND(D,Y4), AND(NOT(D),Y5)) is a two-round composition: the
  generator must propose AND(D,Y4) and AND(NOT(D),Y5) in some round,
  both must co-survive retention, and a later round must OR-combine
  them. The generator CAN propose E in principle; the question is
  whether it ever does and what happens next.
- Query signature Q (harness-side only, never in learner code): the
  species signature the true target would occupy under the U2
  definition (tree depth, sorted operator multiset). For E: depth 3
  (OR -> AND -> NOT -> D is 3 edges), operator count vector
  [n_AND=2, n_OR=1, n_NOT=1, n_XOR=0]. Q is computed once from the
  known target in the analysis step. The instrumented learner logs
  signatures generically; only the shell post-processing knows Q.

## 3. G0: instrumented diagnostic (unconditional, run first)

### 3.1 The question

On R3 Arm 2 with the same seed and sealed harness as the failing run,
are Q-signature candidates:

(a) never proposed by the generator,
(b) proposed but merged away by the species-merge rule, or
(c) proposed but pruned within their species by higher-scoring mates?

The trichotomy maps 1:1 to Causes 1/2/3. Answering it is the highest
information step available.

### 3.2 Instrumentation (logging only; zero decision perturbation)

- Work on an instrumented COPY of the failing niched beam. Frozen
  sources are never edited.
- In the candidate-emission section of the copied `beam_extend`, emit
  to a diagnostic channel (a separate log file, never stdout) the
  species signature of every emitted candidate, computed with the
  same generic tree walk the beam itself uses (depth, sorted operator
  multiset). No target, family, or library knowledge enters this
  logging: it is the beam's own signature function, logged.
- At retention time, emit per species: member count before merging,
  a merged-away flag (1 if this species was absorbed by the merge
  rule), and the count of candidates pruned within the species.
- F-NOPERTURB (frozen): the instrumented run's stdout must be
  byte-identical to the uninstrumented failing run's stdout on the
  same seed. Verify with cmp/md5 BEFORE any log is read. If the
  decision behavior moved, the diagnostic is void.
- Analysis is shell-only (grep, wc, sort, uniq; zero Python): count
  per-round Q matches by joining the candidate-signature log against
  Q = (3, [2,1,1,0]); tabulate the retention fates of Q species.

### 3.3 Decision rule (frozen)

Per run, compute:

- PROPOSED_Q: total Q-signature candidates emitted across all rounds.
- RETAINED_Q: Q candidates surviving retention into the next round.
- MERGED_Q: number of Q species absorbed by the merge rule.
- PRUNED_Q: Q candidates pruned within their species.

Then:

- (a) iff PROPOSED_Q == 0. The generator never proposes E-shaped
  candidates. Cause 1 confirmed in its strongest form.
- (b) dominant iff PROPOSED_Q > 0 and MERGED_Q > 0 and
  RETAINED_Q == 0. Cause 2 confirmed.
- (c) dominant iff PROPOSED_Q > 0 and PRUNED_Q > 0 and
  RETAINED_Q == 0. Cause 3 confirmed (with the retention ranking
  implicated; note U1 Pareto should have prevented (c), so a (c)
  outcome on the unified beam would additionally implicate the U5
  ordering).
- Mixed outcomes: report the raw numbers; the future builder's
  prereg names the dominant branch and gates the fix on it.
- F-G0-INCONCLUSIVE (design-killing, must be reported honestly):
  PROPOSED_Q > 0 and RETAINED_Q > 0 while Arm 2 still fails. Then
  the generation-gap premise is wrong: E-shaped candidates were
  proposed AND survived, and the true E still was not found. The
  problem is scoring or selection among surviving candidates, not
  generation, and sections 4-5 of this document do not apply.

### 3.4 G0 verdict rule

- G0-PASS iff F-NOPERTURB holds, the trichotomy is resolved (or
  F-G0-INCONCLUSIVE fires honestly), runs are 3/3 byte-identical,
  and zero Python was used at every stage.
- G0 is a diagnostic. Its output is data, not a mechanism. No L3
  claim, no Criterion 0 claim, no Q4 revival.

## 4. Conditional branches (gated on G0 data; sketches, not preregs)

### G1: merge-rule fix, gated on branch (b)

The future builder preregisters exactly one of these generic
candidates (variants, not a bundle):

- G1a: never merge a species younger than N rounds, where age is
  tracked generically (rounds since the species signature first
  appeared). N frozen by the builder prereg.
- G1b: merge by lowest best-accuracy instead of fewest members, so
  a novel singleton with decent fit is not the first victim.
- G1c: exempt just-generated singleton species from merging for one
  round, giving novelty one retention cycle to prove itself.

All three are generic search machinery. No target, family, or
library knowledge. F-CASE applies unchanged.

### G2: refutation-seeking IV policy, gated on branch (c), or on (a)+(b)
ruled out with no refuting evidence observed

A complement to (not replacement of) the disagreement IV selector.
For each unused x, compute agree_frac = the fraction of beam members
whose prediction matches the current champion's prediction; select
the x minimizing agree_frac, i.e. maximal beam-internal disagreement
about the champion's own prediction. Alternative operationalization
the builder may prereg: prefer unused x where the champion's
evidence neighborhood is sparsest (fewest evidence points within a
frozen Hamming radius). Both key on the learner's own uncertainty,
never on target identity.

### G3: honest C fallback (generic compositional generation moves),
gated on branch (a)

Permitted now: Design 1's fallback clause allowed explicit
compositional operators once A+B+D honestly failed, and it did
(commit 845d01bc). If the unified beam also fails, the clause is
doubly satisfied.

Candidate generic moves, added to the candidate generator (the
builder preregisters the bounded set):

- Splice: substitute a subexpression of beam member A into a
  terminal position of beam member B. Bounded: only into top-K
  members by accuracy, K frozen by the builder prereg.
- Library-embed: embed any kept-library terminal as an operand
  subexpression of a new binary combination.

F-CASE kill (hard, frozen): any move whose proposal distribution is
shaped by the R3 target (preferring D/Y4/Y5 combinations, depth-3
OR-of-ANDs, or the Q signature) kills the design on the spot. The
moves must be uniformly generic over the beam's own vocabulary.
Compute guard: per-round candidate simulations stay within 10
percent of the frozen baseline (the existing F-BLOAT bound), so
splice is explicitly bounded and cannot buy diversity with an
unbounded simulation budget.

## 5. What not to do

- No third retention/selection variant without G0 data. The Q4 beam
  lineage is now three generations deep (frozen beam -> Design 1 ->
  U1-U7). G0 is a diagnostic, not a repair generation; G1/G2/G3 may
  only be built after G0 data exists, and that data is the new
  information that justifies them. A further blind tweak would
  trigger the architecture-review question ("is the current
  representation itself wrong?") rather than another beam
  adjustment.
- If U1-U7 PASSES F-DIVERSE-FAIL: the R3 generation question is
  closed for this lane. G0 may still run as a positive control
  (expect the trichotomy to resolve with RETAINED_Q > 0). Remaining
  beam work is then R1 evidence-fit (only if F-FIT fired) and the
  W2 constant-prediction ceiling (F-RECFOLD I2, 0-op constant-0 at
  63/64 on all seeds), which this design does not address and which
  needs its own design lane.

## 6. Builder protocol (for the future G0 worker)

1. Write a preregistration adopting section 3 (with kill bars)
   before any implementation. Prereg commit strictly precedes
   implementation (commit-order self-check).
2. Control first: reproduce the failing niched-beam run
   byte-identically on the uninstrumented copy.
3. Instrument the copy; verify F-NOPERTURB by cmp before reading
   any diagnostic log.
4. Shell-only analysis; report PROPOSED_Q, RETAINED_Q, MERGED_Q,
   PRUNED_Q and the resolved branch (or F-G0-INCONCLUSIVE).
5. Pure Zag at every stage, 3/3 byte-identical instrumented runs,
   zero stderr bytes on stdout, zero Python, zero em/en dash bytes
   in loop documentation (verified with
   worker_snippets/check_no_dash.sh).

## 7. Honest scope

Bounded-L2 diagnostic and search design. G0 produces measurements,
not a mechanism. G1-G3 are conditional sketches, not preregs. No
L3, no Criterion 0, no Q4 revival (the revival conjunction remains
dead per 563a1b354). If a conditional branch is later built and
passes, the outcome is bounded-L2 search robustness for one
compositional form.

## Kill bars (this design task)

- K1 (design complete): PASS. G0 fully specified with instrumentation
  points grounded in frozen code (sections 2-3); G1/G2/G3 as
  conditional sketches gated on G0 branches (section 4); frozen
  decision rule including the design-killing F-G0-INCONCLUSIVE
  (3.3); builder protocol (6).
- K2 (addresses failure cause): PASS. The (a)/(b)/(c) trichotomy
  maps 1:1 to Causes 1/2/3 of the post-mortem (47d5c0137); each
  conditional branch targets exactly the cause the data selects;
  F-G0-INCONCLUSIVE honestly kills the premise if the data
  contradicts it.
- K3 (no implementation): PASS. Prose only. No .zag written or
  modified, no binaries, no runs, no instrumentation executed.

## Governance notes

- The Unified Beam Builder (`beam_unified/`) is not redirected and
  none of its files are touched. The Design-1 builder artifacts
  (`beam_impl/`) are untouched. This commit contains only this
  design document.
- The contaminated research paper was not touched.
- Zero Python at every stage of this design task (reading via
  shell/grep/sed, writing via the file tool, dash check via the
  shell-only snippet). No em/en dash bytes in this document
  (verified before commit).

BEAM-NEXT-DESIGN-COMPLETE.
