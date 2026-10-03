# SEALED BATTERY PREREG: Post-Freeze Sealed Adversarial Battery on TNN-2 (wave-20261001-1421pdt)

**Status:** PREREG-FROZEN (design only; no world files generated, no runs executed
at freeze time). This document is frozen by SHA-256 before any world file is
written or any evaluation run starts (see K-S1). No commits are made by this
worker (standing task instruction); freeze ordering is by file hash plus
filesystem timestamps, recorded in RESULT_SEALED_ADV_BATTERY.md.

**Wave:** wave-20261001-1421pdt, lane sealed_adv.
**Date:** 2026-10-01.

## 0. Step 0 (toolchain guard)

Recorded in NAMECHECK.md Step 0: safebin activated, `which python3` prints
nothing, pinned znc from safebin. All programs in this battery are Zag
compiled with the pinned znc. Shell (safebin bash/awk/grep) is used only for
byte checks, file transport, and the deterministic interactive driver loop;
all scoring and state inspection logic is pure Zag.

## 1. Freeze record (no source edits after this point)

TNN-2 mechanism source (frozen, read-only for this battery):

- Commit: `f4de7ff46` ("TNN-2 build: runtime 4-op trial loop, miss-to-act
  inquiry, generic revision")
- File: `docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag`
  (1591 lines)
- SHA-256: `a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd`
- Binary `tnn2_build/tnn2_bin`
  SHA-256: `6044f91f8fe35e307e1d6f73a4ee73bffb930fa0a16a9c899048a086d0d5f77b`

Sealed interface shim (frozen, zero-cognition transport):

- Commit: `23c2c0206` ("CORE-FREEZE-TNN2 driver shim built")
- File: `docs/lab/research-lead/overnight-20260928/core_freeze_tnn2_shim/freeze_shim2.zag`
- SHA-256: `33795c19c9f7ecd8e4c0c9a180293bf577b53ba7aae6f6a5557c972fe372ace8`
- Binary `core_freeze_tnn2_shim/freeze_shim2_bin`
  SHA-256: `9217054c5af6dec057c4530c4de3ba246f521acc6df741d1989a4504acc72954`
- Invocation: `freeze_shim2_bin <world.txt> <state.bin>`
- Protocol: `OBSERVE s r o`, `QUERY s r expected`, `ACT`; outputs
  `OBSERVED s r o`, `ANSWER s r v`, `CHOICE v`. Miss sentinel -2 passes
  through unchanged. State file is exactly 110656 bytes.

Compiler: `src/tools/toolchain/znc_linux_x86_64_abed8aa1`
SHA-256: `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`
(matches the sealed freeze evaluation record).

The three mechanisms under test (all inside the frozen tnn2.zag):

- (M1) runtime executable-graph construction: `t2_trial` miss policy
  (propose/execute/verify/promote over the 4-op ISA MOVE/BRANCHEQ/INC/DEC).
- (M2) learner-originated uncertainty guiding action: `miss_inquire`
  (UNCERTAINTY node plus POLICY_ROOT-linked guide) feeding `ev_act`.
- (M3) counterexample-driven revision: `revise_on_contradict` /
  `t2_revise_graph` (single-schema literal patch with superseded-field
  versioning).

## 2. Battery scope and global constraints

Nine sealed worlds, three per mechanism. FW1-FW9 is a REGRESSION battery
for TNN-2 and can never establish generality or L3; no world here is a
FW1-FW9 world or a trivial variant of one (each world's "material
difference" note explains the separation).

Global constraints:

- Event streams use integer ids only. No natural language, no task labels,
  no family identifiers.
- Id block 40000-49999 for the whole battery, disjoint from FW1-FW9 ids
  (30000-39999) and disjoint across worlds except for intentional
  within-block collateral probes (documented per world).
- Id sub-blocks: M1 block 40000-41999 (W1 40000-40999, W2 41000-41499,
  W3 41500-41999); M3 block 42000-43999 (W1 42000-42999, W2 43000-43499,
  W3 43500-43999); M2 block 44000-46999 (W2 44000-44999, W1 45000-45999,
  W3 46000-46999).
- Worlds run in three blocks (M1: W1->W2->W3; M2: W1->W2->W3;
  M3: W1->W2->W3) with persistent learner state carried across worlds
  within a block (same state.bin chain). Each block starts from fresh
  state. Worlds 2 and 3 of each block carry 2 collateral probes from the
  previous world(s) of the block, testing retention.
- The `expected` field on QUERY lines is the grader's truth. It is also
  passed to `ev_query` as the trial-loop oracle (documented behavior of
  the frozen mechanism); bars are designed so oracle access alone cannot
  pass them (every bar-critical probe has no data path to its expected
  value, or the expected value is the taught fact).
- No harness behavior depends on the learner's internals; all driver
  mappings are fixed in this prereg and mechanical.
- Anti-smuggling: before execution, the frozen cognition source is
  grepped for id tokens in 40000-49999; any match makes the affected
  world WORLD-INVALID (the world's fault), voiding the battery until a
  replacement is sealed under amendment.
- Determinism: each block is run 3 times end to end from fresh state;
  per-world transcripts must be byte-identical across the 3 runs
  (sha256 equality).

### 2.1 Relationship to the wave-20261001-0821pdt AB1-AB3 prereg

The 0821 prereg
(`docs/lab/rsi/runs/wave-20261001-0821pdt/adv_battery/PREREG_TNN2_ADVERSARIAL_BATTERY.md`)
designed AB1/AB2/AB3 post-freeze with adversarial intent but executed
nothing. This battery adopts AB1 as M1-W1, AB2 as M2-W1, AB3's intent as
M3-W1, with two documented executor amendments (below) that preserve the
adversarial intent while fixing mechanism-engagement gaps found during
source review:

- EXECUTOR-AMENDMENT-1 (M1-W1): the noisy exemplar is extended to the Q
  steps (40105 also observes swapped Q ops), adding 2 decoy probes. This
  extends decoy coverage to both procedures and hardens all four probe
  relations against invariant-relation bootstrap.
- EXECUTOR-AMENDMENT-2 (M3-W1): a MAP-promotion phase is added so M3
  actually engages (the 0821 design taught the law only by OBSERVE, which
  creates no MAP and therefore never triggers the revision operator);
  the singleton is never corrected back (the 0821 "corrected back" form
  is passed by last-write-wins and does not discriminate
  evidence-counting from recency); and a law-generalization probe pair
  is added (the 0821 design expected x+5 on unseen subjects, which
  requires revision to generalize beyond contradicted instances).

Both amendments are frozen here, before any world file exists.

## 3. World specifications

Notation: each world lists its exact event stream. `QUERY s r e` lines
carry the grader truth as `e`. Predicted outcomes are recorded honestly
before execution; predicted FAILs are information, not battery defects.

### 3.1 M1-W1: novel composition of two separately demonstrated procedures (AB1 family)

Adversarial intent (post-freeze): the tested form (P-then-Q on novel
instances) is never demonstrated. Only a constructor that abstracts
procedures and composes them at runtime can answer; data-path
construction, memorized-demo replay, and nearest-instance matching all
score zero by construction.

Material difference: FW2 tested replay of one demonstrated 5-step
procedure on novel instances (the tested form was the demonstrated
form). M1-W1 never demonstrates the tested form. FW3 tested induction
of one arithmetic law; M1-W1 tests procedure composition.

Event stream (`m1w1_world.txt`):

```
OBSERVE 40101 40501 40801
OBSERVE 40101 40502 40802
OBSERVE 40102 40501 40801
OBSERVE 40102 40502 40802
OBSERVE 40103 40503 40803
OBSERVE 40103 40504 40804
OBSERVE 40104 40503 40803
OBSERVE 40104 40504 40804
OBSERVE 40105 40501 40802
OBSERVE 40105 40502 40801
OBSERVE 40105 40503 40804
OBSERVE 40105 40504 40803
QUERY 40106 40501 40801
QUERY 40106 40502 40802
QUERY 40106 40503 40803
QUERY 40106 40504 40804
QUERY 40107 40501 40801
QUERY 40107 40502 40802
QUERY 40107 40503 40803
QUERY 40107 40504 40804
QUERY 40105 40501 40801
QUERY 40105 40502 40802
QUERY 40105 40503 40803
QUERY 40105 40504 40804
```

Procedure P = steps (40501->40801, 40502->40802), demonstrated on
40101/40102. Procedure Q = steps (40503->40803, 40504->40804),
demonstrated on 40103/40104. Instance 40105 is the noisy decoy (all four
ops swapped). Probes: 8 composition probes on novel 40106/40107
(expected P-then-Q ops in step order); 4 decoy probes on 40105
(expected the consistent majority structure 40801/40802/40803/40804,
not the memorized swap).

Mechanism analysis (frozen source): composition probes are misses on
novel subjects with no facts, so the trial loop finds no paths;
bootstrap fails (no probe relation is invariant: 40501 has
40802/40801/40801 by recency; 40502, 40503, 40504 likewise mixed).
Predicted: 8x ANSWER -2. Decoy probes are direct hits returning the
taught swapped values (40802/40801/40804/40803), not the consistent
majority. Predicted: 0/4. No MAP is promoted for novel subjects, so no
composed graph exists in state.

Predicted: K-S5 FAIL (0/8 composition, 0/4 decoy, no white-box).

### 3.2 M1-W2: backward traversal of demonstrated chains (reversal family)

Adversarial intent (post-freeze): M1's construction follows observed
data direction only (forward guard->set chains). A general constructor
forms an invertible procedure; this world demonstrates forward chains
and probes the reverse direction, which no assembler supports.

Material difference: FW1 tested forward 3-hop composition (TNN-2 passed
12/12); M1-W2 isolates direction as the only change (same 3-hop shape,
backward probes). Differs from M1-W1 (single-chain reversal vs
two-procedure composition).

Event stream (`m1w2_world.txt`):

```
OBSERVE 41011 41401 41012
OBSERVE 41012 41401 41013
OBSERVE 41013 41401 41014
OBSERVE 41021 41401 41022
OBSERVE 41022 41401 41023
OBSERVE 41023 41401 41024
QUERY 41011 41409 41014
QUERY 41021 41409 41024
QUERY 41014 41409 41011
QUERY 41013 41409 41011
QUERY 41024 41409 41021
QUERY 41023 41409 41021
QUERY 40105 40501 40802
QUERY 40105 40503 40804
```

Probes: 2 forward engagement probes (41011->41014, 41021->41024; the
trial loop builds the 3-hop chain; validity condition); 4 backward
probes (41014->41011, 41013->41011, 41024->41021, 41023->41021);
2 collateral probes from M1-W1 (40105 decoy facts, expected taught
values 40802/40804).

Mechanism analysis: backward probes are misses (subjects 41014/41024
have no outgoing facts; 41013/41023 have only forward facts, and no
path ends at the expected value); bootstrap on 41409 fails (only 2
facts by the time of backward probes, below the k=3 threshold, and not
invariant). Predicted: 4x -2. Forward probes promote MAPs (validity).
Collateral probes are hits.

Predicted: K-S6 FAIL (0/4 backward; engagement 2/2; collateral 2/2).

### 3.3 M1-W3: composition over a shared step (diamond family)

Adversarial intent (post-freeze): construction has no step identity;
steps are bare facts. Two procedures sharing one step (diamond)
require recognizing the shared step to compose correctly; a
fact-memorizer cannot even represent the sharing.

Material difference: M1-W1 composes two disjoint procedures; M1-W3
composes two overlapping procedures with one shared step. FW2 replayed
a single linear procedure; the diamond is a different topology.

Event stream (`m1w3_world.txt`):

```
OBSERVE 41601 41701 41901
OBSERVE 41601 41702 41902
OBSERVE 41601 41703 41903
OBSERVE 41602 41701 41901
OBSERVE 41602 41702 41902
OBSERVE 41602 41703 41903
OBSERVE 41603 41701 41902
OBSERVE 41603 41702 41901
OBSERVE 41603 41703 41902
QUERY 41601 41701 41901
QUERY 41606 41701 41901
QUERY 41606 41702 41902
QUERY 41606 41703 41903
QUERY 41011 41409 41014
QUERY 41021 41409 41024
```

Procedure P = (41701->41901, 41702->41902); procedure Q =
(41702->41902 shared, 41703->41903). Instance 41603 is the noisy decoy
(all swapped). Probes: 1 engagement (41601 hit); 3 shared-composition
probes on novel 41606 (expected 41901/41902/41903); 2 collateral from
M1-W2 (forward MAP facts, hits).

Mechanism analysis: composition probes are misses on a novel subject
with no facts; bootstrap fails (41701: 41902/41901/41901 by recency;
41702: 41901/41902/41902; 41703: 41902/41903/41903; none invariant).
Predicted: 3x -2.

Predicted: K-S7 FAIL (0/3; engagement 1/1; collateral 2/2).

### 3.4 M2-W1: inquiry under asymmetric cost with a flattery trap (AB2 family)

Adversarial intent (post-freeze): removes FW6's literal-choice contract
entirely; only information gain scores. The flattery trap (informant C)
is adversarial against the specific alternative hypothesis that TNN-2's
contingency is prior-agreement seeking rather than uncertainty
reduction. The mechanism cannot compute informativeness (constant guide
action 30), so it cannot discriminate informants.

Material difference: FW6 rewarded one literal choice (CHOICE 0) after a
diagnostic; M2-W1 has no correct literal choice and scores only
information gain. FW7 tested fixed planning to a goal; M2-W1 tests
adaptive information acquisition under cost.

Structure: calibration phase (4 keys 45001-45004, truths 45101-45104;
one ACT per key to consult an informant, then truth revealed by
OBSERVE, then a calibration QUERY probe); inquiry phase (4 hidden keys
45011-45014, truths 45111-45114; per key: QUERY probe, 2 ACTs with
informant responses, final QUERY probe; budget 8 ACTs).

Informant mapping (fixed, mechanical): CHOICE 1 -> informant A
(truthful: answers the key's truth); CHOICE 2 -> informant B (noisy:
fixed table below); CHOICE 3 -> informant C (flatterer: always 45999,
the seeded prior bias, systematically wrong); any other CHOICE
(including the mechanism's 30 and the 0 fallback) -> no informant
consulted (wasted ACT, counts against budget).

B's fixed table: calibration 45001->45101 (correct), 45002->45998
(wrong), 45003->45103 (correct), 45004->45997 (wrong); hidden
45011->45996, 45012->45995, 45013->45994, 45014->45993 (all wrong).
C: always 45999. Bias seeds: OBSERVE 45091 45500 45999,
OBSERVE 45092 45500 45999, OBSERVE 45093 45500 45999 (45999 is the most
frequent object in the static prefix).

Driver: deterministic shell loop (fixed in section 5). The driver log
records one line per ACT: `ACT <CAL|INQ> <key> <choice> <NONE|A|B|C>`.
Note: an informant OBSERVE that disagrees with a later truth OBSERVE
creates a genuine contradiction event (handled by the frozen
contradiction path); this is intended and deterministic.

Mechanism analysis: calibration ACTs occur with no guides in state, so
CHOICE 0 (no informant). Inquiry QUERYs are misses (hidden keys have no
facts; trial finds no paths; bootstrap on 45500: calibration truths
45101-45104 plus bias seeds 45999x3, not invariant), creating one guide
per hidden key. Inquiry ACTs emit CHOICE 30 (guide subject in context),
which maps to no informant (wasted). Final hidden probes are misses
(-2). Engagement check (ACT after ANSWER -2) passes.

Predicted: K-S8 FAIL: (a) engagement PASS; (b) 0 percent to A FAIL;
(c) 0 to C PASS; (d) 0/4 hidden FAIL; (e) 8 ACTs within budget PASS.

### 3.5 M2-W2: stale guide persistence after resolution (resolution family)

Adversarial intent (post-freeze): exploits the missing L6 link (no
uncertainty-resolution transition; guides are never superseded). The
world resolves the uncertainty and then re-presents the subject in
context; a general mechanism stops emitting the inquiry action, while
the frozen mechanism keeps firing the stale guide.

Material difference: M2-W1 tests informant discrimination; M2-W2 tests
guide lifecycle over time with no informants at all. FW6 tested a
single diagnostic round; M2-W2 tests temporal staleness.

Event stream (`m2w2_world.txt`):

```
OBSERVE 44011 44501 44021
QUERY 44101 44501 44901
ACT
OBSERVE 44101 44501 44901
OBSERVE 44102 44502 44202
OBSERVE 44103 44502 44203
OBSERVE 44104 44502 44204
OBSERVE 44105 44502 44205
OBSERVE 44106 44502 44206
OBSERVE 44107 44502 44207
QUERY 44101 44501 44901
ACT
QUERY 45001 45500 45101
QUERY 45002 45500 45102
```

The miss QUERY creates guide(44101); the first ACT must be CHOICE 30
(validity). The OBSERVE resolves the uncertainty in the world (fact
taught). Six distractors flush 44101 from the 4-deep context ring. The
re-QUERY is a hit (44901) and re-pushes 44101 to the ring front. The
final ACT is the bar probe: a resolution-capable mechanism emits 0;
the frozen mechanism emits 30 via the stale guide. Collateral: 2
calibration facts from M2-W1 (hits).

Predicted: K-S9 FAIL (final ACT = 30, not 0; validity ACT = 30;
collateral 2/2).

### 3.6 M2-W3: discriminating action content across uncertainties (content family)

Adversarial intent (post-freeze): exploits the hardcoded L3 link (guide
action is the constant 30 regardless of what is unknown). Three
isolated miss episodes; a discriminating inquiry mechanism emits a
different action per uncertainty, while the frozen mechanism emits 30
three times.

Material difference: M2-W1 tests discrimination via external
informants; M2-W3 tests whether the action itself encodes the
uncertainty, with no informants and no shared context between
episodes. FW6/FW7 never varied the uncertainty across episodes.

Event stream (`m2w3_world.txt`):

```
QUERY 46101 46501 46901
ACT
OBSERVE 46211 46509 46291
OBSERVE 46212 46509 46292
OBSERVE 46213 46509 46293
OBSERVE 46214 46509 46294
QUERY 46102 46502 46902
ACT
OBSERVE 46221 46509 46295
OBSERVE 46222 46509 46296
OBSERVE 46223 46509 46297
OBSERVE 46224 46509 46298
QUERY 46103 46503 46903
ACT
QUERY 44101 44501 44901
QUERY 45003 45500 45103
```

Each episode: miss QUERY (novel subject and relation; trial finds no
paths; bootstrap finds no facts) creates one guide; 4 distractors
flush the previous subject from context; ACT fires only the current
guide. Bar: the three CHOICEs pairwise distinct. Collateral: 44101
(M2-W2) and 45003 (M2-W1) hits.

Predicted: K-S10 FAIL (30, 30, 30; validity: 3x -2 on miss QUERYs;
collateral 2/2).

### 3.7 M3-W1: singleton vs systematic revision with delayed reuse (AB3 family)

Adversarial intent (post-freeze): the revision operator is
last-write-wins literal patching with no evidence counting and no
generalization beyond the contradicted instance. The singleton probe
separates counting revisers from recency revisers; the generalization
probes separate law revisers from per-instance patchers.

Material difference: FW5 tested a sequential dependency chain under
eviction pressure with simple contradiction-overwrite semantics (memory
protection demand); M3-W1 tests evidence discrimination and delayed
reuse (revision-quality demand). FW5 never required rejecting a
counterexample.

Event stream (`m3w1_world.txt`):

```
OBSERVE 42901 42950 42911
OBSERVE 42902 42950 42912
OBSERVE 42903 42950 42913
OBSERVE 42904 42950 42914
OBSERVE 42905 42950 42915
OBSERVE 42906 42950 42916
OBSERVE 42101 42500 42104
OBSERVE 42102 42500 42105
OBSERVE 42103 42500 42106
OBSERVE 42104 42500 42107
OBSERVE 42105 42500 42108
OBSERVE 42106 42500 42109
OBSERVE 42107 42500 42110
OBSERVE 42108 42500 42111
QUERY 42101 42501 42104
QUERY 42102 42501 42105
QUERY 42103 42501 42106
QUERY 42104 42501 42107
OBSERVE 42101 42500 42110
OBSERVE 42102 42500 42107
OBSERVE 42103 42500 42108
OBSERVE 42104 42500 42109
OBSERVE 42801 42850 42811
OBSERVE 42802 42850 42812
OBSERVE 42803 42850 42813
OBSERVE 42804 42850 42814
OBSERVE 42805 42850 42815
OBSERVE 42806 42850 42816
OBSERVE 42807 42850 42817
OBSERVE 42808 42850 42818
OBSERVE 42809 42850 42819
OBSERVE 42810 42850 42820
OBSERVE 42811 42850 42821
OBSERVE 42812 42850 42822
QUERY 42101 42501 42104
QUERY 42102 42501 42107
QUERY 42103 42501 42108
QUERY 42104 42501 42109
QUERY 42105 42501 42110
QUERY 42106 42501 42111
QUERY 42901 42950 42911
QUERY 42902 42950 42912
QUERY 42903 42950 42913
QUERY 42904 42950 42914
QUERY 42905 42950 42915
QUERY 42906 42950 42916
```

Phase 0: 6 interference facts (42900s). Phase 1: law L (x+3) on
42101-42108. Phase 1b (EXECUTOR-AMENDMENT-2): 4 promotion QUERYs on the
novel relation 42501; the trial loop builds 1-hop chains (longer
chains and counts are tried and genuinely rejected first) and promotes
4 MAPs with DEP edges to the respective 42500 facts. Phase 2a:
singleton noise on 42101 (x+9, never corrected). Phase 2b: systematic
shift on 42102-42104 (x+5, never contradicted). Phase 3: 12
distractors. Probes: P1 singleton (42101, expect 42104 = original law;
a counting reviser rejects the uncorrected singleton); P2-P4
systematic (expect x+5); P5-P6 generalization on unseen 42105/42106
(expect x+5; requires the revision to generalize beyond contradicted
instances); P7-P12 interference (expect taught values).

Mechanism analysis: each contradiction triggers the single-schema
patch (last-write-wins). P1: MAP_1 patched to 42110, probe returns
42110 (FAIL: singleton incorporated). P2-P4: patched to x+5, probes
return x+5 (PASS). P5-P6: misses with no data path to x+5 (single-hop
yields x+3, rejected against expected x+5; bootstrap on 42501 not
invariant), ANSWER -2 (FAIL: no generalization). Interference: hits
(PASS).

Predicted: K-S11 FAIL: (a) systematic 3/3 PASS; (b) singleton FAIL;
(c) generalization 0/2 FAIL; (d) white-box PASS (MAP graphs contain
the patched literal SETREGs); (e) interference 6/6 PASS.

### 3.8 M3-W2: revision of a revision (second-contradiction family)

Adversarial intent (post-freeze): the operator's stale-cell lookup
requires a DEP edge to the contradicted fact, but the first revision
links the new cell to the OLD fact node, never to the newly taught
fact. A second contradiction on the same link therefore silently
no-ops. A general reviser tracks the latest evidence.

Material difference: M3-W1 tests one revision per instance plus
generalization; M3-W2 tests sequential revisions of the same link.
FW5 tested single contradictions under eviction; double revision is a
different demand.

Event stream (`m3w2_world.txt`):

```
OBSERVE 43101 43501 43102
OBSERVE 43102 43502 43103
QUERY 43101 43509 43103
QUERY 43101 43509 43103
OBSERVE 43102 43502 43109
QUERY 43101 43509 43109
OBSERVE 43102 43502 43119
QUERY 43101 43509 43119
QUERY 42102 42501 42107
QUERY 42101 42501 42110
```

The promotion QUERY builds a 2-hop chain MAP (DEP to both licensing
facts). Contradiction 1 (43109) revises the second SETREG to the
literal 43109 (re-execution succeeds). Contradiction 2 (43119) finds
no SETREG with a DEP edge to the newly taught fact node, so
`t2_revise_graph` is never called (silent no-op); the MAP keeps
answering 43109. Bar probe expects 43119 (latest evidence).
Collateral: M3-W1 systematic (42107) and singleton-incorporated
(42110) values.

Predicted: K-S12 FAIL (probe returns 43109; validity probes 43103 and
43109 correct; collateral 2/2).

### 3.9 M3-W3: reverted revision blocks relearning (revert family)

Adversarial intent (post-freeze): when the single-schema patch breaks
the graph (guard can no longer fire), the operator reverts and leaves
the stale MAP answer taught as a fact, which short-circuits all future
trial-loop learning on that key. A general reviser would unpromote and
re-derive; the frozen mechanism is stuck.

Material difference: M3-W2 tests silent no-op on second revision;
M3-W3 tests a revision that actively fails (revert) and then vetoes
recovery. FW4/FW5 never produced a reverted revision.

Event stream (`m3w3_world.txt`):

```
OBSERVE 43701 43801 43702
OBSERVE 43702 43802 43703
QUERY 43701 43809 43703
QUERY 43701 43809 43703
OBSERVE 43701 43801 43711
OBSERVE 43711 43802 43713
QUERY 43701 43809 43713
QUERY 43101 43509 43109
QUERY 42103 42501 42108
```

The promotion QUERY builds a 2-hop chain MAP for (43701,43809). The
contradiction on the FIRST link (43711) patches SETREG#1, but
re-execution fails (guard2 tests slot0==43702, now 43711), so the
operator reverts; the MAP and its taught fact (43701,43809,43703)
are unchanged. The world then supplies the new second link
(43711->43713), making the current 2-hop structure 43701->43711->43713.
The bar probe expects 43713, but direct retrieval of the stale taught
fact returns 43703 (the trial loop never runs).

Predicted: K-S13 FAIL (probe returns 43703; validity probes correct;
collateral 2/2).

## 4. Frozen kill bars K-S1 through K-S15

All bars are PASS/FAIL only; no partial credit. Process-bar failures
void the battery (re-seal and re-run); they are never scored as
mechanism verdicts.

- K-S1 (prereg ordering). PASS iff the SHA-256 of this file recorded in
  RESULT_SEALED_ADV_BATTERY.md was computed before any battery world
  file was created (filesystem mtime order) and the file is unmodified
  thereafter (hash re-verified after the battery).
- K-S2 (determinism). PASS iff, for each of the 3 blocks, the 3
  end-to-end runs produce byte-identical per-world transcripts
  (sha256 equality of the 9 transcript files across runs).
- K-S3 (frozen binary). PASS iff `freeze_shim2_bin` hashes to
  `9217054c5af6dec057c4530c4de3ba246f521acc6df741d1989a4504acc72954`
  before each block run and after the battery, `tnn2.zag` still hashes
  to `a29972ca...`, and `git status` shows zero modifications under
  `docs/lab/research-lead/overnight-20260928/tnn2_build/` and
  `.../core_freeze_tnn2_shim/` cognition paths.
- K-S4 (seal integrity). PASS iff all world files match the manifest
  hashes recorded at generation, and `grep -r` over the frozen
  cognition sources finds zero tokens in 40000-49999.
- K-S5 (M1-W1 construction). PASS iff (a) at least 7 of the 8
  composition probes are correct; (b) all 4 decoy probes return the
  consistent majority structure (40801, 40802, 40803, 40804); (c) the
  state inspector reports a MAP whose DEP-licensed facts include both
  P-demo facts (40101/40102 block) and Q-demo facts (40103/40104
  block). All three required.
- K-S6 (M1-W2 reversal). PASS iff at least 3 of the 4 backward probes
  are correct. Validity: both forward engagement probes correct,
  else WORLD-INVALID.
- K-S7 (M1-W3 shared step). PASS iff at least 2 of the 3
  shared-composition probes are correct. Validity: engagement probe
  correct, else WORLD-INVALID.
- K-S8 (M2-W1 calibration). PASS iff (a) the engagement check passes
  (at least one INQ ACT after an ANSWER -2 on a hidden key);
  (b) at least 70 percent of inquiry-phase ACTs target informant A
  (CHOICE 1); (c) at most 1 inquiry-phase ACT targets informant C
  (CHOICE 3); (d) at least 3 of the 4 final hidden probes are correct;
  (e) inquiry-phase ACTs do not exceed the budget of 8. All five
  required.
- K-S9 (M2-W2 resolution). PASS iff the post-resolution ACT (with
  44101 in context) emits CHOICE 0. Validity: the pre-resolution ACT
  emits CHOICE 30, else WORLD-INVALID.
- K-S10 (M2-W3 content). PASS iff the three episode CHOICEs are
  pairwise distinct. Validity: all three miss QUERYs yield ANSWER -2,
  else WORLD-INVALID.
- K-S11 (M3-W1 discrimination). PASS iff (a) at least 2 of the 3
  systematic probes are correct; (b) the singleton probe is correct
  (42104, original law); (c) at least 1 of the 2 generalization probes
  is correct; (d) the inspector reports a MAP on relation 42501 whose
  answer is a post-contradiction value and whose live graph contains a
  SETREG holding that value as a literal; (e) all 6 interference probes
  are correct. All five required.
- K-S12 (M3-W2 double revision). PASS iff the post-second-contradiction
  probe returns 43119. Validity: the promotion probe (43103) and the
  post-first-revision probe (43109) are correct, else WORLD-INVALID.
- K-S13 (M3-W3 revert). PASS iff the post-revert probe returns 43713.
  Validity: the promotion/engagement probes return 43703, else
  WORLD-INVALID.
- K-S14 (retention). PASS iff at least 75 percent of all collateral
  probes across the battery return their prereg-expected values.
- K-S15 (no-leak audit). PASS iff the scorer reports zero correct
  ANSWERs on novel-key probes whose value coincides with a taught
  triple from a different world (cross-world smuggling), and the K-S4
  grep is clean (recorded here separately).

### Predicted bar outcomes (recorded before execution)

K-S1, K-S2, K-S3, K-S4, K-S14, K-S15: predicted PASS (process bars).
K-S5: predicted FAIL (0/8, 0/4, no white-box).
K-S6: predicted FAIL (0/4 backward).
K-S7: predicted FAIL (0/3).
K-S8: predicted FAIL ((b) 0 percent to A, (d) 0/4 hidden).
K-S9: predicted FAIL (stale 30).
K-S10: predicted FAIL (30, 30, 30).
K-S11: predicted FAIL ((b) singleton incorporated, (c) 0/2
generalization; (a), (d), (e) predicted PASS).
K-S12: predicted FAIL (43109, not 43119).
K-S13: predicted FAIL (43703, not 43713).

## 5. Execution protocol and tools

### 5.1 Tools (all pure Zag, pinned znc; built after this prereg freezes)

- `sealed_score.zag`: argv [worldfile, transcript]. Parses QUERY
  (s,r,e) lines from the world file and ANSWER (s,r,v) lines from the
  transcript (1:1 in order); prints per-probe PASS/FAIL and summary
  counts; also lists CHOICE values in order. Used for the 8
  non-interactive worlds.
- `score_m2w1.zag`: argv [transcript, driverlog, truths]. Checks K-S8
  sub-bars: engagement, informant targeting percentages from the
  driver log, final hidden probes (last ANSWER per hidden key) against
  truths, budget.
- `inspect_state.zag`: argv [state.bin]. Prints `TRIAL tried=.. rej=..`
  (header field 16), one `MAP s=.. r=.. ans=.. root=..` line per active
  MAP node plus `LITS ..` (SETREG literal values found by walking SEQ
  edges and guard true-targets from the root), `UNCERT s=.. r=..` per
  active tag-30 node, `GUIDE s=..` per POLICY_ROOT type-10-linked node,
  and `POLICYROOT ..`.

### 5.2 Block driver (deterministic shell)

Per block run: remove any prior state.bin; for W1..W3 in order, run
`freeze_shim2_bin <world> <state.bin>` (exit code must be 0), saving
stdout as the world transcript. For M2-W1, the interactive driver
(section 3.4) grows the world file from the fixed template; the driver
log is saved. After the block, run the inspector on the final
state.bin (once per block run; informational, not part of
determinism). Repeat 3 times; compare transcript sha256 across runs.

### 5.3 Anti-smuggling and manifest

At generation: sha256 manifest of all world/template/truth files.
Before execution: grep the frozen cognition sources for 40000-49999.
Hash re-verification of the shim binary before each block run and
after the battery.

## 6. Verdict rules

- M1 SURVIVES-SEALED iff K-S5 and K-S6 and K-S7 all PASS; else
  M1 FAILS (kill evidence: the failed sub-bars).
- M2 SURVIVES-SEALED iff K-S8 and K-S9 and K-S10 all PASS; else
  M2 FAILS.
- M3 SURVIVES-SEALED iff K-S11 and K-S12 and K-S13 all PASS; else
  M3 FAILS.
- Any process-bar (K-S1..K-S4, K-S14, K-S15) failure VOIDs the battery;
  a void battery is re-sealed and re-run, never interpreted. There is
  no partial-generality verdict.

## 7. Criterion 0 status (binding; no L3 claim on any pass)

This battery tests whether frozen, researcher-authored mechanisms
generalize to fresh structures. It does not test representational
invention:

- C0-A (runtime-defined semantics): NOT MET. The exercised semantics
  (trial-loop assemblers, constant guide action, single-schema patch)
  are researcher-authored machinery in the frozen source. A passing
  probe would still run researcher-defined semantics.
- C0-B (open structural form): NOT MET. Every world's tested form is
  enumerable from its demonstrations before the run (P-then-Q,
  backward chain, shared step, informant choice, x+5 law).
- C0-C (multiple unforeseen forms, independent post-freeze adversary):
  NOT MET. Nine worlds across three families, designed post-freeze,
  but the adversary role is played inside the same research loop (see
  the independence caveat in the 0821 prereg, adopted here). A second
  battery by a genuinely separate adversary is required before any
  L3-adjacent claim.
- C0-D (cognitive reuse): NOT MET as a criterion. M3-W1's delayed
  reuse probes and the within-block collateral probes measure
  reuse-like behavior, which is evidence toward a future C0-D case,
  but a single battery's probes are explicitly insufficient.

Consequence: no score on this battery, however high, may be described
as L3, L3-adjacent, or progress toward L3 without a separate
Criterion 0 case on independent evidence. The strongest honest claim
available is about the generality of M1, M2, M3 as frozen mechanisms.

## 8. What a FAIL means

Per the standing no-patch-treadmill rule, an expected FAIL is evidence
about what the frozen core is missing, not a request for a patch. The
results document clusters failures by shared architectural cause and
proposes general substrate hypotheses; benchmark-specific handlers and
per-world opcodes are rejected in advance.
