# Canonical Scientific State: TNN Native Lab

**Date:** 2026-09-29 07:30 PDT
**Branch:** tnn-native-lab
**Author:** Research Synthesizer (subagent)
**Status:** This document is the authoritative summary of validated mechanisms,
boundaries, and open questions as of this timestamp. It supersedes informal
summaries. It does not supersede preregistered verdicts; it cites them.

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
  not infer task type.
- Simplified causal store (no split/merge/contest machinery).
- Revision bridge was scaffolding only (logged failures, did not invoke
  causal machinery). Now superseded by functional Bridge v1 (see 1.5).
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

**Boundaries (Adversary-confirmed, 3 downgrades):**
1. Bar confound: K5-v2/K2-v2/K4-v2 probes query TAUGHT facts. Step-0 direct
   lookup (bug fix #3, added without prereg amendment) answers them without
   touching concepts. Only mini_world's 3 "sib"-marked probes genuinely test
   inference (3/3 PASS). Adequacy rests on white-box structure + 3 probes.
2. MERGE incomplete: identical-intent concepts under different parents not
   unified (C2/C65, C3/C66 in F-A2).
3. Spurious SPLITs: reason=2 children with no contradiction (C7/C8 in F-A2;
   C3-C6 in K5).
- COMPOSE operator: defined in prereg, NOT implemented.
- Governance: implementation+fixtures+results landed in ONE commit (17d5de9f7);
  results report claim of separate commits is FALSE (Adversary finding).

**Commits:** prereg 6db93a784; adversary prereg e300bd9cb; adversary report
9d03a1afb. (Note: implementation commit 17d5de9f7 message says "Bridge prereg
FROZEN" but contains FDCR files; hygiene violation documented.)

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

**Boundaries:**
- Binary conditions only: one position, one value, two procedures.
- Condition language: (input[pos] == val) only. No ranges, conjunctions.
- No recursive bridging: subset discovery failure returns -1.
- B-A6b BUG (Adversary-confirmed): slot exhaustion. 15 distractor values
  consume proc slots on failed splits; 16th task bricks the bridge (returns
  -1 on a learnable task). Repair required before integration: dry-run
  discovery without storing.
- B-A6a: slot waste scales linearly with distractor count (9 slots for 2
  needed in test).
- Partially satisfies L3 criterion 12 (revision via conditional split).
  Does not satisfy general revision (merge, deprecate with provenance).

**Commits:** prereg 17d5de9f7; result 06f5e2b5a; adversary prereg 5a7d52195;
adversary report af5869602.

---

## 2. What Is NOT Validated

1. **No L3 representational invention.** SEM-L3 falsified (flat Jaccard
   clustering; K5/K2/K4 all FAIL). FDCR achieves adequacy, not invention.
   The nine-criterion L3 assessment has not been attempted for any mechanism.

2. **No procedure revision in the core mechanism.** H-REVISE KILLED with
   proof. The Bridge provides binary-conditional revision externally, but
   the procedure learner itself cannot revise.

3. **No content-aware procedures.** All discovered programs are index maps
   P(k,n)->index. Content-conditional procedures are inexpressible in the
   program language (this is the H-REVISE impossibility result).

4. **No learned task routing.** Integration v1 uses explicit P/C/Q prefixes.
   The continuing learner does not infer task type from input structure.

5. **No cross-mechanism synergy.** Integration proves coexistence (disjoint
   state). No evidence that procedure and causal mechanisms benefit each other.

6. **No compositional procedures.** Bridge handles binary splits; 3-way and
   conjunctions fail honestly. FDCR COMPOSE unimplemented. No mechanism
   composes learned structures into larger ones.

7. **No active experiment invention.** The fourth frontier (TNN invents
   discriminating experiments) has not been attempted.

8. **No memory strategy invention.** The fifth frontier (learner-controlled
   memory policy) has not been attempted.

9. **Push to GitHub.** Blocked by token security boundary. 250+ commits local.
   Bundle preserved at ~/workspace/tnn-native-lab-20260929.bundle (24M,
   verified). API connector works; git cannot access the token.

---

## 3. L-Level Summary Table

| Mechanism | Level | Basis |
|-----------|-------|-------|
| SEM (Jaccard) | L2 | Flat clustering; hierarchy/split/overlap FAIL |
| Procedure discovery | Bounded L2+ | 11/12 criteria; discovery via search; no revision |
| Causal learning | Bounded L2 | 14/14 probes; narrow authored vocabulary |
| Integration v1 | Bounded L2 | Coexistence; explicit routing; no synergy |
| FDCR | L2 (adequacy) | Hierarchy/split/overlap form; bars confounded |
| Revision bridge | Bounded L2+ | Binary-conditional revision; 1 known bug |

No mechanism has achieved L3. The strongest result is procedure discovery
with 11/12 criteria (criterion 12 definitively failed by proof).

---

## 4. Three Highest-Value Next Architectural Questions

### Q1: Can search-based discovery reach content-conditional programs?

**Why it matters (information gain: HIGH):**
The H-REVISE impossibility proof shows P(k,n)->index cannot express
conditionals. The Bridge works around this externally. But the core question
is whether the discovery mechanism itself can learn programs that inspect
content. If yes, the procedure frontier advances fundamentally. If no, we
have mapped a hard boundary of the enumerate-and-select paradigm.

**L3 relevance: HIGH.** Content access moves representational power from
the researcher (who currently supplies the index-only language) to the
learner (which would discover content-dependent structure).

**Integration leverage: HIGH.** Content-conditional procedures would subsume
the Bridge's external IF/ELSE, unifying procedure learning and revision in
one mechanism. This also unlocks the causal-procedure interface (causal
conditions selecting procedures based on world state, not just input bytes).

**Concrete approach:**
1. Preregister H-CONTENT: extend program signature to P(k, n, input) with
   content primitives (e.g., AT(i) returns input byte at position i; EQ
   compares). Keep the search generic (no hardcoded conditionals).
2. Freeze kill bars: must discover broadcast-last AND the "xab"->"xxx"
   conditional WITHOUT the Bridge; must not regress on Family X; must
   handle ambiguous inputs (RT2-C) or fail honestly.
3. Implement, execute, red-team. The key falsifier: does the enlarged
   search space still find programs, or does it explode intractably?
   (1055 programs worked; content primitives may push it to millions.)

### Q2: Can FDCR concepts compose into genuinely new representations?

**Why it matters (information gain: HIGH):**
FDCR passes adequacy bars (with downgrades) but COMPOSE is unimplemented
and no L3 criteria have been tested. The critical distinction is adequacy
(can form required structures) vs invention (creates structures the
researcher did not enumerate, then reuses them). Currently FDCR's operators
(FORM/MERGE/SPLIT) produce structures within the preregistered test shapes.
A composition test would determine if the representation can grow.

**L3 relevance: VERY HIGH.** This is the most direct test of L3
representational invention remaining. If FDCR can compose two concepts into
a third that solves a novel probe, that is evidence for criterion 7
(unseen-case benefit) and 8 (transfer/reuse).

**Integration leverage: MEDIUM.** Compositional concepts would provide the
representational substrate for richer causal conditions (beyond
single-variable equality) and procedure preconditions.

**Concrete approach:**
1. Preregister H-COMPOSE: implement the COMPOSE operator (union-intent
   concept from two existing concepts). Freeze bars: given concept A
   {flies, feathers} and concept B {swims, waterproof}, the learner must
   form C {flies, feathers, swims, waterproof} ONLY when evidence supports
   it (e.g., a duck entity taught with all four), NOT spontaneously.
2. Kill bars: no spurious compositions (precision); required compositions
   form (recall); composed concept answers probes neither parent could
   answer alone (utility); ablation (removing COMPOSE) destroys the
   capability (causality).
3. Red-team specifically for: combinatorial explosion, meaningless
   compositions, and whether the composition is "invention" or just
   set-union the researcher could have hardcoded.

### Q3: Can the continuing learner infer task type without explicit routing?

**Why it matters (information gain: HIGH):**
Integration v1's P/C/Q prefixes are human-supplied task labels. The
directive requires "no task label supplied to cognition." A learner that
cannot distinguish "learn a transformation" from "learn a causal rule"
from input structure alone is not a continuing learner; it is a
multi-tool with a human operator. Removing the router tests whether the
mechanisms can self-organize.

**L3 relevance: MEDIUM.** Task inference is meta-cognitive rather than
representational. But it is a prerequisite for any L3 claim about a
continuing learner (as opposed to isolated mechanisms).

**Integration leverage: VERY HIGH.** This unlocks the full continuing-life
gauntlet (stages A-J in the directive). Every subsequent integration
experiment depends on unmarked task boundaries.

**Concrete approach:**
1. Preregister H-ROUTE: remove P/C/Q prefixes. The learner sees raw
   lines: either ("abc"->"cba") pairs or (state, action, next_state)
   triples. It must route to the correct store.
2. Freeze kill bars: 5/5 integration tasks must still pass without
   prefixes; a novel ambiguous input (could be either type) must
   WITHHOLD or request clarification, not misroute confidently;
   routing decision must be inspectable (white-box trace).
3. The honest failure mode: if the input formats are trivially
   distinguishable (arrows vs tuples), the test is weak. Strengthen by
   using a unified encoding where both task types look similar, forcing
   the learner to discover the distinguishing structure.
4. Red-team for: router hardcoding the unified encoding, silent
   misrouting, and whether "inference" is just format detection.

---

## 5. Provenance and Governance Notes

- All mechanisms implemented in pure Zag. No Python in loop research
  (one disclosed K12 fixture-generation violation, remediated with shell).
- Prereg commit ordering verified by Scientific-Governance Auditor
  (AUDIT PASS with corrections; commits 09a788213, b94d5b4be).
- Claim corrections applied: "L3 validated (7/9)", "first credible L3",
  and "CORE L3 MECHANISM VALIDATED" annotated as RETRACTED/SUPERSEDED.
- 97 em dashes scrubbed for style compliance.
- Family pre-naming conflict (REVERSE in design doc) flagged and resolved:
  reverse results are mechanism validation; Family X (Adversary-assigned)
  provides the true invention test.
- Push blocked; all commits local. Bundle preserved.

---

## 6. Open Questions (Beyond the Top 3)

- Active experiment invention (fourth frontier): not attempted.
- Memory strategy invention (fifth frontier): not attempted.
- B-A6b slot-exhaustion repair: required before Bridge integration.
- FDCR MERGE incompleteness and spurious SPLITs: repair or scope.
- FDCR bar redesign: held-out inference probes to replace confounded bars.
- Causal vocabulary enrichment: conjunctions, inequalities (beyond nesting).
- Procedure extraction robustness: ambiguous inputs (RT2-C).
- Cross-mechanism synergy: beyond coexistence.
- Synthetic language: the eventual GPT-3 milestone path.

---

*End of canonical state. Next update when new verdicts land.*
