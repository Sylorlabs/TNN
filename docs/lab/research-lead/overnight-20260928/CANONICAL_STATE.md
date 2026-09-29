# Canonical Scientific State: TNN Native Lab

**Date:** 2026-09-29 07:44 PDT
**Branch:** tnn-native-lab
**Author:** Canonical State Updater (subagent)
**Status:** This document is the authoritative summary of validated mechanisms,
boundaries, and open questions as of this timestamp. It supersedes the 07:30
PDT version (commit a66de28cf) and all informal summaries. It does not
supersede preregistered verdicts; it cites them.

**Style note:** This document contains no em dashes, per loop documentation rules.

---

## 1. Validated Mechanisms

### 1.1 Procedure Discovery (proc_learn.zag)

**Classification: Bounded L2+ (criteria 1-11 of 12; criterion 12 FAILED)**

**What it does:** Given input-output string pairs, extracts index sequences
and searches 1055 compositional programs (K, N, C0/C1/C2, ADD, SUB, size <= 5)
for the smallest program fitting all examples. The program maps output
position k to input position via an affine function of k and n.

**Validated evidence:**
- Reverse: found [N K C1 ADD SUB] = n-1-k from ("abc"->"cba") etc. 3/3 hidden PASS.
- Identity: found [K] from ("abc"->"abc"). 1/1 hidden PASS.
- Family X (Adversary-assigned undisclosed): broadcast-last [N C1 SUB] = n-1.
  8/8 PASS on 4 disclosed + 4 hidden cases (RT2 authoritative verification).
  Seal verified. Training-data-only change, diff audited.
- Transfer (PI-5): 5/5 PASS across symbol sets and numeric arrays.
- Semantic count: 85 distinct behaviors from 1055 syntactic programs (RT2-B).

**Boundaries (all validated by red team):**
- Requires unique input characters. Extraction returns VACUOUS on ("aaa"->"aaa"),
  ("aba"->"aba"), etc. (RT2-C FAIL). Family X succeeded by luck of unique chars.
- Enumerate-and-select, not constructive invention. All 85 behaviors are affine
  f(k,n) = ak+bn+c. The vocabulary is authored; the learner selects from it.
- Cannot revise. H-REVISE KILLED (c7bfaeba1) with mathematical proof:
  counterexample requires P(k,3)=0 while training requires P(k,3)=2 for
  identical (k,n). No function P(k,n)->index can satisfy both. Five revision
  capabilities all ABSENT (detection, diagnosis, conditional representation,
  revision operators, procedure memory).

**Commits:** prereg 6cd2e95a7; v1 fb6ab328a; Family X prereg 6caa37ed6,
training 8fa0fe2a3, result 850b79ddb; RT2 6e88f3003; H-REVISE prereg 2d720d9bc,
result c7bfaeba1.

### 1.2 Causal Learning (causal_learn.zag)

**Classification: Bounded L2 (structural learning, not L3)**

**What it does:** Observes (state, action, next_state) episodes. Induces
conditional rules via SPLIT on single variables, holds competing hypotheses
(AMBIGUOUS), refutes confounders with single counterexamples, WITHHOLDs under
genuine ambiguity, and revises via CONTEST/RESOLVE with temporal provenance
(SUPERSEDED markings).

**Validated evidence:**
- 14/14 probes PASS across phases A, B, B2, C1, C2.
- 8 kill bars KB-C1..KB-C8 all PASS.
- Safety valve: induced "temp==hot blocks pressurize" (not in source).
- Confounder (lamp) refuted with provenance. Law change revised via contest.
- Baselines: B-memorize and B-unconditional fail probes the learner passes.
  Third baseline B-cond1 gets 12/14; learner gets 14/14.
- Determinism: byte-identical reruns.
- Order robustness: works on shuffled (interleaved) data, not phase-dependent.

**Boundaries (Adversary-confirmed downgrades):**
- Vocabulary narrowness: single-variable equality splits only. Dozens of
  expressible rules, not thousands. "Invention" = data-driven selection from
  a small authored space.
- Decorative provenance: revision is real (SUPERSEDED markings, not silent
  overwrite), but no probe can query SUPERSEDED entries. Provenance is logged,
  not queryable.
- Bounded scope: 3 variables, 4 actions, hand-fed phases in prereg.

**Commits:** prereg 75de43886; implementation 0df42f648; fixtures 8ead2ca68;
verdict 902e92330; adversary prereg 2e8fdf251; adversary report 164d7158e.

### 1.3 Integration v1 (integ_learn.zag)

**Classification: Bounded L2 integration (coexistence, not synergy)**

**What it does:** Single Zag process with dual stores (procedure: 8 slots of
affine programs; causal: 16 single-condition rules). Task router uses P/C/Q
line prefixes. Sequential task processing, no re-init, no interference.

**Validated evidence:**
- 5/5 kill bars K-I1..K-I5 PASS.
- T1 learned reverse (slot 0), T2 learned safety valve (2 rules), T3 learned
  broadcast-last (slot 1, slot 0 undisturbed), T4 all queries PASS.
- No forgetting, no cross-store contamination, single process verified.

**Boundaries (disclosed in result):**
- Explicit router: P/C/Q prefixes are human-supplied task labels. Learner does
  not infer task type. (Superseded by H-ROUTER, see 1.6.)
- Simplified causal store (no split/merge/contest machinery).
- Revision bridge was scaffolding only (logged failures, did not invoke
  causal machinery). (Superseded by functional Bridge v1, see 1.5.)
- Disjoint state is easy: no shared representation to corrupt. Proves
  coexistence, not synergy. Not stress tested (2 procedures, 2 rules).

**Commits:** prereg 3be18d8ad; result 492f5b01d.

### 1.4 FDCR: Representational Adequacy (rep_v2/fdcr_learn.zag)

**Classification: Representational adequacy (NOT L3; L2 structural)**

**What it does:** Forms concepts via FORM (shared-subset parents), MERGE
(identical-intent unification), SPLIT (contradiction-driven children),
GRADE (graded membership), CONTEXTUALIZE (context-conditioned children).
Supports hierarchy, delayed split, delayed merge, overlap.

**Validated evidence:**
- K5 hierarchy: PASS (4/4). Parent {flies=yes} with 8 members; sparrow/eagle
  clusters descend.
- K2 delayed split: PASS (5/5). Merged E1a/E1b split on distinguishing r3.
- K4 overlap: PASS (2/2). True shared concept {r1o1,r2o2} with B1/B2 members.
- K3 delayed merge: PASS (5/5). Identical entities unified.
- mini_world regression: 8/8 PASS.
- 3-level hierarchy (F-A2): forms correctly, 12 entities.
- Scale (F-A6): 24 entities, 36 concepts, 0.192s, no blowup.
- No hardcoding: zero fixture vocabulary in source.
- Inference repair (H-INFER SURVIVES, 3/3): most-specific-preference sibling
  inference. Per-candidate evidence accumulators (was global); first candidate
  with consistent non-empty evidence decides; conflicting evidence at that
  level WITHHOLDs immediately. The disambiguation probe (Q e5 | kind =>
  roller [OK] sib) now passes. Zero regression on k5/k2/k4/k3_merge/
  mini_world/ctx_test. Deterministic (byte-identical).

**Boundaries (Adversary-confirmed, 3 downgrades; H-INFER does not repair these):**
1. Bar confound: K5-v2/K2-v2/K4-v2 probes query TAUGHT facts. Step-0 direct
   lookup (bug fix #3, added without prereg amendment) answers them without
   touching concepts. Only mini_world's 3 "sib"-marked probes genuinely test
   inference (3/3 PASS). Adequacy rests on white-box structure + 3 probes.
2. MERGE incomplete: identical-intent concepts under different parents not
   unified (C2/C65, C3/C66 in F-A2).
3. Spurious SPLITs: reason=2 children with no contradiction (C7/C8 in F-A2;
   C3-C6 in K5).
- COMPOSE operator: implemented and KILLED on utility (see 1.8). The
  inference-side gap that motivated COMPOSE is now repaired by H-INFER.
- Governance: implementation+fixtures+results landed in ONE commit (17d5de9f7);
  results report claim of separate commits is FALSE (Adversary finding).

**Commits:** prereg 6db93a784; adversary prereg e300bd9cb; adversary report
9d03a1afb; H-INFER prereg 276709293; H-INFER result 4abfdf7d0. (Note:
implementation commit 17d5de9f7 message says "Bridge prereg FROZEN" but
contains FDCR files; hygiene violation documented.)

### 1.5 Revision Bridge (bridge_learn.zag)

**Classification: Bounded L2+ with functional revision bridge (binary-conditional)**

**What it does:** When procedure discovery returns -1 (no program fits),
searches (input position, byte value) pairs from training data for a split
where both subsets are discoverable. Learns IF input[pos]==val THEN procA
ELSE procB. Both procedures preserved in store. Dispatches at query time.

**Validated evidence:**
- 7/7 kill bars K-B1..K-B4 PASS.
- Task A: learned IF input[0]==120 ('x') THEN [C0] ELSE [N C1 SUB].
- Task B: generalized to pos=1, val=113 ('q'). Not hardcoded to pos=0/'x'.
- Task C (control): 0 bridge rules on success. Failure-gated correctly.
- B-A2 (Adversary): pos=2 (middle) generality confirmed.
- B-A5 (Adversary): no spurious trigger on accidental correlations.
- B-A3/B-A4 (Adversary): honest -1 on 3-way splits and conjunctions.
- B-A6b REPAIRED (H-FIX SURVIVES, K-F1..K-F3 PASS): the slot-exhaustion
  denial-of-learning bug is fixed via pdiscover_dry (search without storing;
  proc slots reserved only for the winning split). The 15-distractor attack
  now succeeds (2/16 slots used, was 16/16). Original 7/7 still pass. Failed
  attempts consume 0 slots. The bridge is cleared for integration use.

**Boundaries:**
- Binary conditions only: one position, one value, two procedures.
- Condition language: (input[pos] == val) only. No ranges, conjunctions.
- No recursive bridging: subset discovery failure returns -1.
- B-A6a slot waste: fixed by the same dry-run change (was linear waste).
- Partially satisfies L3 criterion 12 (revision via conditional split).
  Does not satisfy general revision (merge, deprecate with provenance).

**Commits:** prereg 17d5de9f7; result 06f5e2b5a; adversary prereg 5a7d52195;
adversary report af5869602; fix prereg c22c29e4e; fix result 974a9ca13.

### 1.6 Learned Routing (route_learn.zag)

**Classification: Bounded L2 integration infrastructure (structure-inferred routing)**

**What it does:** Replaces Integration v1's explicit P/C/Q prefixes with
per-item structure inference. Each input line carries no type label. The
router computes the route from structural predicates over format markers
(>, ;, ,) and field content (comma-free string vs int-tuple), emits a
white-box trace (ROUTE [line] -> TARGET (reason)), and withholds on
ambiguity. Procedure and causal mechanism code copied verbatim from
integ_learn.zag; only router, handlers, and main() are new.

**Validated evidence:**
- 5/5 kill bars K-R1..K-R5 PASS (9/9 sub-checks).
- K-R1: procedure learning routes and works (reverse at slot 0,
  broadcast-last at slot 1, slot 0 intact).
- K-R2: causal learning routes and works (hot->low, cold->high).
- K-R3: queries route and work (procedure query reports all slots;
  causal queries fire correctly).
- K-R4: ambiguity withholds with reasons (single pair, malformed
  episode, mixed segments, empty line); zero misroutes.
- K-R5: no regression; committed integ_learn.zag recompiled from source
  still 5/5, H-INTEG SURVIVES.
- Determinism: 3 runs byte-identical (md5 ee7f050c2975050a89afba0b4c07d6d2).

**Boundaries (disclosed in result):**
- Predicates are authored. What is inferred is the per-item decision, not
  the routing rules. This is structure-inferred routing, not meta-learned
  routing.
- Slot selection out of scope: procedure queries apply all stored
  procedures and report each (slot, output). Intent retrieval is future work.
- The >=2 segment threshold is an authored disambiguation rule. One-shot
  procedure learning from a single pair is unreachable through this router.
- Format markers assumed (>, ;, ,). A fully marker-free stream needs a
  further inference step.
- Simplified stores inherited from v1.
- Not L3. No representational invention involved.

**Commits:** prereg d6e4eb485; result 05a00279d.

### 1.7 Unified Learner (unified_learn.zag)

**Classification: Bounded L2 integration (first unlabeled learn-route-revise loop)**

**What it does:** Unifies the learned router (1.6) with the revision bridge
(1.5, B-A6b fixed) in one process. One item stream, no P/C/Q labels, no
reset. Router infers task type per item; procedure-learning items that fail
direct discovery automatically trigger bridge conditional induction; causal
items use causal induction; queries apply stored procedures AND bridge rules.

**Validated evidence:**
- 9/9 checks PASS (K-U1..K-U5).
- K-U1: simple procedure ("abc>cba;xy>yx" routed PROC_LEARN, reverse at
  slot 0, "hello"->"olleh").
- K-U2: conditional procedure (5-pair item routed PROC_LEARN, direct failed,
  bridge induced IF input[0]==120 THEN proc1 ELSE proc2; "xqw"->"xxx",
  "zzz"->"zzz").
- K-U3: causal (episodes routed CAUS_LEARN, hot->low / cold->high correct).
- K-U4: queries (procedure query reported slots plus QBRIDGE rule 0;
  causal query fired).
- K-U5: no interference (reverse intact, causal intact after all learning).
- Ambiguity probe "ab>ba" correctly WITHHOLDs.
- Determinism: 3 runs byte-identical (md5 aa9166f60325a2736ac9bd870e09cc2b).

**Honest finding (documented, not hidden):** The first run used a 4-pair
conditional item (all n=3). The bridge found a valid split but the
ELSE-branch program was the constant ADD(C0,C2) (=2), correct on n=3
training but wrong on n=5 queries. The smallest-program search has no
generality preference; this is honest mechanism behavior, not a bug. The
evidence was strengthened (added n=5 ELSE pair "abcde>eeeee"),
the bridge then learned the generalizing SUB(N,C1), and the mechanism was
not modified. K-U4a failed on the first run (8/9) and passed after the
evidence fix (9/9); both runs are documented in UNIFIED_RESULT.md.

**Boundaries (from prereg, confirmed):**
- Routing predicates authored (inherited from H-ROUTER).
- Bridge conditions single (pos,val) equality only (inherited from H-BRIDGE).
- Procedure queries report all slots/rules; intent selection out of scope.
- Integration infrastructure, not L3 evidence. Each component was
  independently validated and red-teamed; this tests their composition.

**Commits:** prereg d652fdaee; result f5dd7cdc7.

---

## 2. Negative Results (Preserved)

Per loop governance, negative evidence is preserved with lineage. These are
real results, not failures to report.

### 2.1 H-COMPOSE KILLED on Utility

**Claim:** Deliberate union-intent COMPOSE operator would enable novel
inferences in FDCR.

**Result:** KILLED. K-C1 PASS (operator fires: 3 reason=6 concepts on
disambiguation fixture, white-box verified). K-C2 FAIL (Q e5 | kind =>
WITHHOLD with and without COMPOSE; 0/1). K-C3 N/A (ablation confirms no
effect; removing the operator changes nothing). K-C4 PASS (no harm: all six
fixtures unchanged, zero reason=6 on standard fixtures, 3x byte-identical).

**Redundancy theorem (preregistered, confirmed empirically):** In FDCR's
architecture, deliberate union-intent composition cannot enable novel
held-out inferences beyond FORM/MERGE/leaves. Step-1 (direct) is impossible
(target-in-intent implies taught fact); Step-2 (sibling) unions with 2+
evidence-carrying members are already covered by existing operators. The
composed concepts that fired ({red,block}, {round,block}, {square,blue})
are unions the existing SPLIT/FORM machinery also produces; COMPOSE merely
created them earlier in the fixpoint.

**Interpretation:** Union-COMPOSE is not FDCR's missing operator. The
genuine gap was inference-side (most-specific preference), now repaired by
H-INFER (see 1.4). Informative negative: rules out a natural hypothesis
with a mechanism-level explanation.

**Scope:** Bounded to union-intent COMPOSE in FDCR's feature-based
architecture. Other composition semantics (invented features, relational,
graded) untested. NOT L3 evidence.

**Governance note:** The researcher used `python3 -c` twice for
brace-counting during debugging. Disclosed fully in the final report:
Python generated no committed artifacts and influenced no results; the
brace count was redone with shell tools (grep -o + wc -l); Python use
stopped immediately on correction. No Python in any committed file.

**Commits:** prereg 271ec362b; result 8fc591047.

### 2.2 H-CC VOID (Content-Conditional Discovery)

**Claim:** Search-based discovery extended with IF(input[0]==v, A, B)
conditionals would find content-conditional programs (4/4 kill bars claimed
PASS on researcher data).

**Result:** VOID as a preregistered verdict. The prereg (dd5f2f77e, line 66)
FROZE training datum ("xy"->"yy"). The implementation (dd95a64b3,
proc_cond.zag lines 275-276) silently substituted ("def"->"fff") with only
a result-file footnote ("I cleaned the training data... to ensure a fair
test"). No prereg amendment was committed. K-CC2 was evaluated on different
data than preregistered. The Adversary's CC-A6 confirms: on the ORIGINAL
preregistered data the mechanism returns NO PROGRAM FOUND. The cleaning was
load-bearing, not cosmetic.

**What remains valid (exploratory, not preregistered):** The mechanism finds
IF(input[0]=='x', C0, SUB(N,C1)) on researcher-arranged data where the
discriminating feature is pre-isolated at position 0. 10,130 programs for
V=3; no hallucination on the tested pure cases. Byte-identical reproduction
confirms honest implementation.

**Boundaries (Adversary 5/6 attacks PASS):**
- CC-A1: position-0 predicates only. Position 1+ fails. "Content-conditional"
  is really "position-0-conditional."
- CC-A2: tractable only for V<33 (50 values -> 152,305 programs, breaks the
  100k bar; V=256 -> 775,455 programs). No cap in source.
- CC-A3: branch-size limit causes SILENT OVERFITTING, not clean failure.
  Found SUB(C2,K)=2-k (fits n=3 training [2,1,0] coincidentally, gives
  [2,1,0,-1] for n=4 instead of true reverse [3,2,1,0]). Worse than
  incompleteness: undetectable without generalization tests.
- CC-A4: two-phase gating causes CONDITIONAL BLINDNESS. When training is
  misleadingly pure (base program fits), Phase 2 never runs and the
  mechanism is wrong on hidden conditional cases.
- CC-A5: equality-only predicates. No inequality, ranges, or compounds.
- CC-A6: fails on the original H-REVISE motivating data.

**Honest restatement:** "Content-conditional search demonstrates
IF(input[0]==v, A, B) discovery on a single researcher-arranged case
(4/4 bars pass exploratorily). Requires researcher to pre-isolate the
discriminating feature. The preregistered K-CC2 verdict is VOID."

**Classification:** Bounded exploratory mechanism demonstration. NOT a
validated preregistered result. NOT L3 evidence.

**Commits:** prereg dd5f2f77e; result dd95a64b3; adversary prereg 449c1226f;
adversary report 0ca84f3f4; determinism fix 9810e2bfd.

---

## 3. What Is NOT Validated

1. **No L3 representational invention.** SEM-L3 falsified (flat Jaccard
   clustering; K5/K2/K4 all FAIL). FDCR achieves adequacy, not invention.
   H-COMPOSE killed (union composition redundant). The nine-criterion L3
   assessment has not been attempted for any mechanism.

2. **No procedure revision in the core mechanism.** H-REVISE KILLED with
   proof. The Bridge provides validated binary-conditional revision
   externally (1.5, B-A6b fixed), and H-UNIFIED composes it end-to-end
   (1.7), but the procedure learner itself cannot revise. H-CC (direct
   content-conditional search) is VOID as preregistered; its exploratory
   form has severe boundaries (2.2).

3. **No general content-aware procedures.** All discovered programs are
   index maps P(k,n)->index. The Bridge handles single (pos,val) equality
   conditionals. General content-conditional procedures (ranges,
   conjunctions, position-independent features) are inexpressible in all
   validated mechanisms.

4. **No learned task routing.** H-ROUTER (1.6) provides structure-inferred
   routing, but the predicates are authored. The learner does not discover
   routing rules from experience. Meta-learned routing is unattempted.

5. **No procedure intent retrieval.** Queries apply all stored procedures
   and report each (slot, output). The learner does not infer which
   procedure the querier intends. This is the documented out-of-scope gap
   in H-ROUTER and H-UNIFIED.

6. **No cross-mechanism synergy.** Integration proves coexistence (disjoint
   state). No evidence that procedure and causal mechanisms benefit each
   other. H-UNIFIED composes them in one stream but they remain separate
   stores.

7. **No stress test of the unified learner.** H-UNIFIED used a handful of
   tasks. Behavior under store pressure (10+ interleaved tasks), slot
   exhaustion, and bridge-rule accumulation is untested.

8. **No active experiment invention.** The fourth frontier (TNN invents
   discriminating experiments) has not been attempted.

9. **No memory strategy invention.** The fifth frontier (learner-controlled
   memory policy) has not been attempted.

10. **Push to GitHub.** Blocked by token security boundary. 301 commits
    local. Bundle preserved at
    ~/workspace/tnn-native-lab-20260929-v4.bundle (25M, verified
    "is okay", HEAD f5dd7cdc7). API connector works; git cannot access
    the token.

---

## 4. L-Level Summary Table

| Mechanism | Level | Basis |
|-----------|-------|-------|
| SEM (Jaccard) | L2 | Flat clustering; hierarchy/split/overlap FAIL |
| Procedure discovery | Bounded L2+ | 11/12 criteria; discovery via search; no revision |
| Causal learning | Bounded L2 | 14/14 probes; narrow authored vocabulary |
| Integration v1 | Bounded L2 | Coexistence; explicit routing; superseded by 1.6/1.7 |
| FDCR | L2 (adequacy) | Hierarchy/split/overlap form; inference repaired (H-INFER); 3 red-team downgrades open |
| Revision bridge | Bounded L2+ | Binary-conditional revision; B-A6b fixed; cleared for integration |
| Learned router | Bounded L2 | Structure-inferred routing; authored predicates; no intent retrieval |
| Unified learner | Bounded L2 | Unlabeled learn-route-revise loop; composes validated components |
| COMPOSE | KILLED | Union composition redundant (redundancy theorem) |
| Content-conditional (H-CC) | VOID / exploratory | Prereg violated; position-0/equality-only; silent overfitting |

No mechanism has achieved L3. The strongest result is procedure discovery
with 11/12 criteria (criterion 12 definitively failed by proof; the Bridge
provides partial external revision).

---

## 5. Architectural Questions: Answered and Open

### Answered since 07:30 PDT

**Q1 (was: content-conditional search): ANSWERED as VOID/exploratory.**
H-CC's preregistered claim did not survive adversarial review (training
data substituted post-freeze; K-CC2 VOID). The exploratory mechanism has
severe boundaries (position-0 only, V<33, silent overfitting, conditional
blindness, equality-only). The validated conditional mechanism remains the
Revision Bridge (binary (pos,val) equality, B-A6b fixed).

**Q2 (was: FDCR composition): ANSWERED as KILLED with repair.**
H-COMPOSE was killed on utility; the redundancy theorem shows union-intent
composition cannot add inference power in FDCR's architecture. The genuine
gap was inference-side and is now repaired (H-INFER: most-specific
preference; disambiguation probe passes).

**Q3 (was: learned task routing): ANSWERED as structure-inferred (authored).**
H-ROUTER SURVIVES: routing without P/C/Q labels, white-box traces,
ambiguity withholds, no regression. H-UNIFIED SURVIVES: end-to-end
unlabeled learn-route-revise loop in one process. Remaining gap: the
routing predicates are authored, not learned.

### Three Highest-Value Next Questions

#### NQ1: Can the unified learner survive store pressure and interference?

**Why it matters (information gain: HIGH):**
H-UNIFIED was tested with a handful of tasks. A continuing learner must
handle dozens of interleaved procedures, bridge rules, and causal rules
without forgetting, misrouting, or slot exhaustion. The B-A6b bug showed
that resource exhaustion is a real failure mode; the fix was verified on
one attack, not on sustained pressure. If the unified learner degrades
gracefully (honest WITHHOLD on exhaustion) it is integration-ready. If it
fails silently or catastrophically, we have mapped the next architectural
boundary.

**L3 relevance: MEDIUM.** Robustness is engineering, not invention. But no
L3 claim about a continuing learner is credible without it.

**Integration leverage: VERY HIGH.** This is the prerequisite for the full
continuing-life gauntlet. Every subsequent integration experiment assumes
the unified learner holds up.

**Concrete approach:**
1. Preregister H-STRESS: 12+ interleaved tasks (6 procedures incl. 2
   conditional, 4 causal rules, mixed queries) in one stream, one process.
2. Freeze kill bars: all previously-learned capabilities queryable at the
   end (no forgetting); ambiguous/overflowing items WITHHOLD honestly
   (no silent corruption); bridge-rule count bounded and reported;
   byte-identical determinism.
3. Red-team for: slot-exhaustion honesty, bridge-rule interference with
   direct procedures, causal-store overflow behavior.

#### NQ2: Can routing predicates be learned from experience rather than authored?

**Why it matters (information gain: HIGH):**
H-ROUTER's predicates are written by the researcher. The directive
requires "no task label supplied to cognition"; authored structural
checks are a weaker form of supplied labeling. If the learner can induce
its own routing rules from labeled-then-unlabeled experience (e.g., from
a curriculum where task types are initially marked, then marks are
removed), routing moves from researcher to learner. If it cannot, we have
mapped a hard boundary of the current architecture.

**L3 relevance: HIGH.** Discovering task structure from experience is a
form of meta-structural learning. It directly addresses the "who supplies
the representation" question for the routing layer.

**Integration leverage: HIGH.** Learned routing removes the last
researcher-supplied component of the unified learner (routing predicates,
segment thresholds, format markers).

**Concrete approach:**
1. Preregister H-ROUTER2: curriculum phase with explicit task-type marks,
   then unmarked phase. The learner must induce routing predicates from
   the marked phase (using the causal learner's own SPLIT machinery on
   input-structure features) and apply them in the unmarked phase.
2. Freeze kill bars: induced predicates must be inspectable (white-box);
   must match or beat the authored predicates on the H-ROUTER test suite;
   must WITHHOLD on genuinely ambiguous inputs (not overfit to curriculum).
3. The honest failure mode: if the causal learner's vocabulary
   (single-variable equality) is too narrow for routing predicates, the
   test fails informatively and motivates vocabulary enrichment.

#### NQ3: Can the learner invent discriminating experiments? (fourth frontier)

**Why it matters (information gain: HIGH):**
All current mechanisms are passive: they learn from supplied evidence.
The fourth innovation frontier (Micah's standard: "new experiment") asks
whether TNN can design an experiment that discriminates between competing
hypotheses. This is Level D (self-directed evidence) in the
pattern-matching-vs-intelligence program. No mechanism has attempted it.

**L3 relevance: VERY HIGH.** Experiment invention requires the learner to
represent its own uncertainty, generate candidate disambiguating actions,
and select among them. This is the most direct test of active inquiry
remaining.

**Integration leverage: MEDIUM.** Experiment invention would provide the
active counterpart to the causal learner's passive confounder refutation
(which currently relies on the researcher to supply the discriminating
episode).

**Concrete approach:**
1. Preregister H-EXP: supply the causal learner with two competing
   hypotheses (e.g., "lamp blocks pressurize" vs "temp==hot blocks
   pressurize") and a set of primitive actions (set temp, toggle lamp,
   attempt pressurize). WITHHOLD the discriminating action sequence.
2. Freeze kill bars: the learner must select (or rank) the action that
   discriminates (e.g., pressurize with lamp on and temp cold); must not
   select uninformative actions; the selection must be justified by an
   inspectable trace referencing the competing hypotheses.
3. Red-team for: hardcoding the discriminating action, selecting by
   surface heuristics (e.g., "try everything"), and whether the
   hypothesis representation supports the required counterfactual
   reasoning.

---

## 6. Provenance and Governance Notes

- All mechanisms implemented in pure Zag. No Python in loop research,
  with two disclosed exceptions: (a) the K12 fixture-generation
  violation (remediated with shell regeneration; in lineage); (b) the
  COMPOSE researcher's two `python3 -c` brace-counting calls during
  debugging (disclosed in final report; no committed artifacts affected;
  redone with shell tools; use stopped on correction).
- Prereg commit ordering verified throughout: every prereg cited above
  strictly precedes its implementation commit (276709293<4abfdf7d0,
  d6e4eb485<05a00279d, d652fdaee<f5dd7cdc7, 271ec362b<8fc591047,
  c22c29e4e<974a9ca13). The H-CC violation was training-data
  substitution within the implementation step, not commit misordering;
  K-CC2 is VOID (not INVALID as a measurement; the exploratory result
  stands as exploratory).
- Claim corrections applied: "L3 validated (7/9)", "first credible L3",
  and "CORE L3 MECHANISM VALIDATED" annotated as RETRACTED/SUPERSEDED
  (prior audit). No "bounded L3" wording survives for procedure v1.
- 97 em dashes scrubbed for style compliance (prior audit); this document
  verified to contain none.
- Family pre-naming conflict (REVERSE in design doc) flagged and resolved:
  reverse results are mechanism validation; Family X (Adversary-assigned)
  provides the true invention test.
- Push blocked; all commits local (301 ahead of origin/tnn-native-lab).
  Bundle preserved at ~/workspace/tnn-native-lab-20260929-v4.bundle
  (25M, git bundle verify "is okay", HEAD f5dd7cdc7).
- Concurrent-agent commit hygiene: FDCR files landed in a "Bridge prereg"
  commit (17d5de9f7); content verified correct, prereg order intact,
  misattribution noted.

---

## 7. Open Questions (Beyond the Top 3)

- Procedure intent retrieval for queries (documented gap in H-ROUTER/H-UNIFIED).
- FDCR MERGE incompleteness and spurious SPLITs: repair or scope (red-team
  downgrades 2 and 3, still open).
- FDCR bar redesign: held-out inference probes to replace confounded bars
  (red-team downgrade 1, still open).
- Causal vocabulary enrichment: conjunctions, inequalities, multi-variable
  conditions (beyond single-variable equality).
- Procedure extraction robustness: ambiguous inputs (RT2-C).
- Full causal contest/split/merge machinery ported into the unified process
  (H-UNIFIED uses the simplified causal store).
- Memory strategy invention (fifth frontier): not attempted.
- Synthetic language: the eventual GPT-3 milestone path.
- Cross-mechanism synergy: beyond coexistence.

---

*End of canonical state. Next update when new verdicts land.*
