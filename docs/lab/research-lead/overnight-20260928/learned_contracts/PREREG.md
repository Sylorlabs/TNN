# PREREG: LCONT-1 -- Learned Contracts from Failure

Status: PREREG-FROZEN. No implementation exists at this commit.
Scope: `docs/lab/research-lead/overnight-20260928/learned_contracts/` only.
New files: PREREG.md (this file), NAMECHECK.md, src/lcont.zag,
bin/lcont, runs/lcont-run{1,2,3}.txt, REPORT.md.
Worker: LEARNED-CONTRACTS (subagent, 2026-10-03).
Parent mandate: implement Micah's LEARNED CONTRACTS directive. Types
themselves must be learned from experience. No researcher ontology of
INT/BOOL/PLAN/CAUSAL/LANGUAGE/AUDIO. Push experiments where initially
insufficient contracts are refined by failure and consequence.

## 1. What is being tested

Whether a learner can acquire its own type system from experience:
start with contracts too coarse to distinguish behaviorally different
structures, fail at composition because of that coarseness, use the
failure as evidence to refine the contracts into behaviorally distinct
kinds, and then succeed at composition with the identical selection
rule. The four required stages:

- Stage A (prior experience): the learner explores six structures and
  solves three composition goals by search, building evidence. All
  contracts stay coarse: every structure has out-kind 0 ("value") and
  in-kind 0. The coarse contract is adequate here because every
  structure used so far behaves alike in the roles tried.
- Stage B (coarse failure): a novel goal from a behaviorally different
  family arrives. The learner selects by contract plus evidence, with
  no search, and commits. The coarse contract filters nothing, the
  evidence (all from the old family) points at the wrong structure, and
  the composition FAILS.
- Stage C (refinement): the learner runs a generic partition-refinement
  procedure over its own probe table and the failure log. Kind 0 splits
  into behaviorally distinct kinds. The grouping is computed from
  observed behavior, not supplied by the researcher.
- Stage D (post-refinement success): the same selection rule, unchanged,
  now succeeds on the retried failing goal, on a second novel-family
  goal, and on a held-out old-family goal (no regression).

The claim sought is L2 structural learning: the learner constructs a
new organization of its knowledge (a kind partition) from generic
machinery plus its own experience. The L3 bar is explicitly not
claimed. The interesting content is that the refined kinds are
determined by the learner's observations, verified by the permutation
control (section 7) and the prereg audit (K6).

## 2. Opacity boundary

Everything the learner touches is opaque identifiers. Structures are
ids 0..5. Kinds are ids 0..6 (0 means universal/unknown, see section
5). The learner never sees arithmetic definitions, semantic labels, or
family names. The arithmetic table in section 3 specifies the WORLD,
not the learner's ontology; it exists so the experiment is
reproducible, exactly as a physics defines the apparatus. The
researcher-authored code is partitioned into WORLD functions (the
structure behaviors, called only when the learner executes a structure
or probes it) and LEARNER functions (contracts, selection, refinement,
which never inspect world internals). Section 8 states the function
boundary.

## 3. World design

Two worlds. World B is world A with structure behaviors permuted across
ids by pi = [4,5,0,1,2,3] (world B id i behaves as world A id pi[i]).
The learner is never told pi.

World A behaviors (x integer):
- id 0: x -> x + 1
- id 1: x -> 2 * x
- id 2: x -> x + 10
- id 3: x -> 3 * x
- id 4: x -> x mod 2 (0 or 1)
- id 5: x -> 1 if x >= 5 else 0

World B behaviors:
- id 0: x -> x mod 2
- id 1: x -> 1 if x >= 5 else 0
- id 2: x -> x + 1
- id 3: x -> 2 * x
- id 4: x -> x + 10
- id 5: x -> 3 * x

Behavioral ground truth (researcher-visible only): in each world,
exactly two structures ever produce outputs outside {0,1} on no probe;
precisely, two structures have all probe outputs in {0,1} and four
have probe outputs exceeding 1. Which ids these are differs by world
(A: {4,5}; B: {0,1}).

Probes: the learner may execute any structure on the fixed probe set
P = {1,2,3,4,5,6,7,8} and records the outputs. This is the learner's
own exploration data.

Goals (given to the learner as (x, y*) pairs; success is executing a
pair (F,G) with F(G(x)) == y*):
- Stage A: (2,14), (3,12), (5,30). Solved by search.
- Stage B: (7,0). Selected by contract, committed, no search.
- Stage D: (7,0) retry, (2,0), (4,18). Selected by contract, committed.

Hand verification of the stage-A search (fixed order F=0..5, G=0..5,
first success commits) is in section 6.

## 4. What counts as "insufficient" and what counts as "refined"

Insufficient contract (preregistered definition): at stage B, the
contract system provides zero bits of selection information, i.e. the
outer candidate set after contract filtering equals all six
structures, and the selected outer is behaviorally incapable of the
goal (its probe outputs never contain y*). Formally: |candidates| = 6
AND y* not in probe outputs of the chosen outer. This is genuine
insufficiency, not a strawman: the evidence-max rule the learner uses
is the reasonable policy of trusting past success, and under the
coarse contract it has no other information channel.

Refined contract (preregistered definition): after REFINE, the out-kind
partition satisfies (a) at least two distinct kinds exist; (b) every
kind boundary corresponds to an observed behavioral disagreement (two
structures share a kind only if their full behavioral signatures
agree); (c) no boundary was specified by the researcher (K6 audit).
The predicted refined partition is stated behaviorally in section 6:
one kind per behaviorally distinct signature (six signatures, six
kinds), with the two {0,1}-output structures in kinds disjoint from
the other four.

Learner-driven verification (three legs):
1. Prereg audit (K6): this file specifies the refinement PROCEDURE
   but not its outcome; it contains no mapping from structure ids to
   refined kinds.
2. Permutation control (K3): world B reruns everything with behaviors
   permuted across ids. The refined partition must track behavior, not
   ids: the {0,1}-output ids are {0,1} in B versus {4,5} in A, and the
   signature multiset must be identical across worlds.
3. White-box trace: the run prints the failure evidence, every
   structure's behavioral signature, and the resulting kind per
   structure, so each boundary is checkable against observed data.

## 5. Learner machinery (generic; fixed before any goal is seen)

Contract state per structure s: outK[s] (init 0), inK[s] (init 0,
stays 0: kind 0 on the input side means universal, matches any
producer kind). Evidence: succO[s], succI[s] (init 0), incremented on
stage-A search successes.

SELECT-OUTER(y*): compute needMask = { outK[s] : s produced y* on some
probe }. Candidates = { s : outK[s] == 0 or outK[s] in needMask }.
(Kind 0 is universal: it matches any need, and any specific kind
satisfies a universal need.) If candidates is empty, selection fails.
Else pick max succO[s], ties to lowest id. This is the entire
selection rule, identical in stages B and D.

SELECT-INNER(F): candidates = all s (inK[F] == 0 is universal). Pick
max succI[s], ties to lowest id.

REFINE (on failed episode (x, y*, F, G)):
1. K = outK[F]; members M = { s : outK[s] == K }.
2. v = G(x), the actual inner value from the failed episode.
3. sig[s] = ( s(1), s(2), ..., s(8), s(v) ) for s in M, from the
   learner's own executions (probes plus the episode replay).
4. Partition M by exact signature equality; each block receives one
   fresh opaque kind id; outK[s] is updated. inK is untouched.
This is generic partition refinement in the Myhill-Nerode spirit:
distinguish kinds exactly where observed behavior disagrees. The
researcher supplies the procedure; the data (signatures) and hence
the grouping come from the learner's experience.

## 6. Hand-verified predictions

Stage A search, world A (F outer 0..5, G inner 0..5, first success):
- (2,14): F=0 fails all G (4,5,13,7,1,1); F=1 fails (6,8,24,12,0,0);
  F=2,G=0 gives 13, G=1 gives ADD10(DBL(2)) = ADD10(4) = 14. Commit
  (F=2,G=1).
- (3,12): F=0 fails (5,7,14,10,2,1); F=1,G=0 gives DBL(4) = 8, G=1
  gives DBL(DBL(3)) = DBL(6) = 12. Commit (F=1,G=1).
- (5,30): F=0 fails (7,11,16,16,2,2); F=1,G=0 gives 12, G=1 gives 20,
  G=2 gives DBL(ADD10(5)) = DBL(15) = 30. Commit (F=1,G=2).
Evidence: succO = [0,2,1,0,0,0], succI = [0,2,1,0,0,0].

Stage B, world A, goal (7,0): needMask = {0} (all outK 0); candidates
all six; max succO is id 1; SELECT-INNER gives id 1 (max succI).
Execute DBL(DBL(7)) = DBL(14) = 28, which is not 0. FAIL. The coarse
contract filtered nothing (|candidates| = 6) and the chosen outer's
probe outputs {2,4,...,16} never contain 0.

Stage C, world A: v = 14. Signatures (probes 1..8, then s(14)):
- id 0: (2,3,4,5,6,7,8,9,15)
- id 1: (2,4,6,8,10,12,14,16,28)
- id 2: (11,12,13,14,15,16,17,18,24)
- id 3: (3,6,9,12,15,18,21,24,42)
- id 4: (1,0,1,0,1,0,1,0,0)
- id 5: (0,0,0,0,1,1,1,1,1)
All six pairwise distinct. Predicted: six kinds, one per structure;
the two structures with probe outputs in {0,1} (ids 4,5) receive kinds
disjoint from the other four. Stated behaviorally: no id-to-kind
table is given here by design (K6).

Stage D, world A, same SELECT code:
- (7,0): producers of 0 on probes are ids 4,5; candidates {4,5};
  succO tie 0/0, lowest id 4; inner max succI is id 1; execute
  ISODD-behavior(DBL(7)) = (14 mod 2) = 0. SUCCESS.
- (2,0): outer id 4, inner id 1; (4 mod 2) = 0. SUCCESS.
- (4,18): producers of 18 are ids 2 (p=8) and 3 (p=6); succO picks
  id 2; inner id 1; ADD10(DBL(4)) = ADD10(8) = 18. SUCCESS.

World B predictions (same code, permuted behaviors):
- Stage A commits: (F=4,G=3) on (2,14); (F=3,G=3) on (3,12);
  (F=3,G=4) on (5,30). Evidence: succO = [0,0,0,2,1,0],
  succI = [0,0,0,2,1,0].
- Stage B (7,0): outer id 3, inner id 3; DBL(DBL(7)) = 28. FAIL.
- Stage C: six distinct signatures (same multiset as world A; the
  {0,1}-output structures are now ids 0,1); six kinds.
- Stage D: (7,0) -> outer id 0, inner id 3, (14 mod 2) = 0, SUCCESS;
  (2,0) -> outer id 0, inner id 3, SUCCESS; (4,18) -> outer id 4
  (succO 1 beats id 5's 0), inner id 3, ADD10(DBL(4)) = 18, SUCCESS.

## 7. Kill bars

- K0 (genuine insufficiency): at stage B, in both worlds, the outer
  candidate set has size 6 AND the chosen outer's probe outputs do not
  contain y*. Checked in-program.
- K1 (failure): stage B goal (7,0) FAILS in both worlds (executed
  output != 0). Checked in-program.
- K2 (refinement): after REFINE, in both worlds, the number of
  distinct out-kinds is exactly 6; no two structures with different
  signatures share a kind; the ids whose probe outputs are all in
  {0,1} hold kinds disjoint from every other id's kind. Checked
  in-program from the learner's own tables.
- K3 (permutation control): the multiset of the six signatures in
  world B equals that of world A; the {0,1}-output id set differs
  ({0,1} vs {4,5}) while the kind separation tracks it. Checked
  in-program.
- K4 (post-refinement success): stage D goes 3/3 in each world with
  the stage-B SELECT code path unchanged. Checked in-program.
- K5 (determinism): three runs byte-identical (sha256).
- K6 (no researcher leakage): shell grep audit. PREREG.md contains no
  mapping from structure ids to refined kind ids. Learner functions
  never reference world behavior except through exec/probe calls; the
  words for semantic families appear only in this WORLD-spec section,
  never in learner code or learner-visible trace labels.

Verdict rule: BUILD-PASS requires K0..K6 all pass. Any single kill bar
failure is BUILD-FAIL.

## 8. Function boundary (auditable)

WORLD (may encode section-3 arithmetic): world_apply(w, s, x).
LEARNER (values and ids only; never inspects world internals):
learner_probe, learner_search_A, learner_select_outer,
learner_select_inner, learner_refine, plus the bar-check helpers which
read only learner tables. HARNESS: main, which runs the staged
protocol for both worlds and prints the trace. The goal targets y*
are given to the learner as goal specifications (it must observe
consequence against them); they are not hidden world state.

## 9. Honest scope

This tests contract refinement as L2 structural learning: the learner
reorganizes its knowledge (kind partition) using generic machinery and
its own evidence. It does not test L3 invention (the refinement
procedure itself is researcher-supplied generic machinery, in the same
sense as a CPU's compare instruction). What is learner-determined is
which kinds exist and which structures share them. A BUILD-PASS shows
a learner can learn a behaviorally grounded type distinction from a
single failure plus probes, and that the distinction is load-bearing
for composition: identical selection code fails before and succeeds
after.
