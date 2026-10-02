# PREREG: Sealed Adversarial Battery V2 on TNN-2 Mechanisms (wave-20261001-2021pdt, lane BATTERY)

**Status:** PREREG-FROZEN (design only; no world files generated, no envelopes
generated, no runs executed at freeze time). This document is frozen by SHA-256
before any v2 world file or sealed envelope is created (see K-S1v2). No commits
are made by this worker (standing task instruction); the coordinator commits
this prereg alone. Implementation and world generation are authorized only
after that commit. UNVERIFIABLE ORDERING voids this prereg.

**Wave:** wave-20261001-2021pdt, lane BATTERY (sealed adversarial battery
redesign).
**Date:** 2026-10-01.
**Documentation rule observed:** no em-dashes in this file.

## 0. Step 0 (toolchain guard)

Recorded in this lane's NAMECHECK.md Step 0: safebin activated,
`which python3` prints nothing, pinned znc from safebin. This task is
WRITING ONLY. Every program built under this prereg (world generator,
interactive driver, scorers, state inspector, calibration controls) is
Zag compiled with the pinned znc; shell (safebin bash/awk/grep) is used
only for byte checks, file transport, and hash manifests. No Python
anywhere; any forbidden executable invocation is automatic PROCESS-FAIL.

## 1. Freeze record (mechanisms unchanged from v1)

The three TNN-2 mechanisms under test are frozen and unchanged. The v2
battery is a battery-design validation instrument, not a mechanism
repair and not a mechanism rescue. Frozen artifacts (identical to the
v1 battery):

- TNN-2 mechanism source: commit `f4de7ff46`, file
  `docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag`
  (1591 lines), SHA-256
  `a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd`.
- Sealed interface shim binary `core_freeze_tnn2_shim/freeze_shim2_bin`,
  SHA-256
  `9217054c5af6dec057c4530c4de3ba246f521acc6df741d1989a4504acc72954`
  (zero-cognition transport: OBSERVE to OBSERVED, QUERY to ANSWER, ACT
  to CHOICE; the executed path for all v2 runs).
- Compiler: `src/tools/toolchain/znc_linux_x86_64_abed8aa1`, SHA-256
  `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`.
- Mechanisms: (M1) runtime executable-graph construction via the
  `t2_trial` miss policy; (M2) learner-originated uncertainty guiding
  action via `miss_inquire` guides feeding `ev_act`; (M3)
  counterexample-driven revision via `revise_on_contradict` /
  `t2_revise_graph` (single-schema literal patch).

## 2. Battery scope and global constraints

Nine sealed worlds, three per mechanism, same families as v1 (the
calibrated worlds stay close to v1; the miscalibrated worlds are
redesigned per the six corrections in section 9). FW1-FW9 is a
REGRESSION battery for TNN-2 and can never establish generality or L3;
no v2 world is an FW1-FW9 world or a trivial variant of one (each
world's "material difference" note explains the separation, carried
over from v1 where unchanged).

Global constraints:

- Event streams use integer ids only. No natural language, no task
  labels, no family identifiers.
- Id block 40000-49999 for the whole battery, disjoint from FW1-FW9
  ids (30000-39999). Sub-blocks: M1 40000-41999, M3 42000-43999, M2
  44000-46999 (W2 44000-44999, W1 45000-45999, W3 46000-46999). v2
  world ids are chosen disjoint from the v1 world id sets to prevent
  cross-battery identity confusion; numeric reuse of an id across
  batteries in a different role is harmless because every block starts
  from fresh state and K-S15v2 audits smuggling within the v2 battery
  only.
- Worlds run in three blocks (M1: W1->W2->W3; M2: W1->W2->W3;
  M3: W1->W2->W3) with persistent learner state carried across worlds
  within a block (same state.bin chain). Each block starts from fresh
  state. Worlds 2 and 3 of each block carry 2 collateral probes from
  the previous world(s) of the block, testing retention.
- The `expected` field on QUERY lines is the grader's truth. It is also
  passed to `ev_query` as the trial-loop oracle (documented behavior of
  the frozen mechanism); bars are designed so oracle access alone cannot
  pass them (every bar-critical probe has no data path to its expected
  value, or the expected value is the taught fact).
- No harness behavior depends on the learner's internals; all driver
  mappings are fixed in this prereg (M2-W1 mappings are fixed by the
  sealed per-run envelopes, section 6) and mechanical.
- Anti-smuggling: before execution, the exact id set extracted from the
  v2 world files is grepped in the frozen cognition sources; any match
  makes the affected world WORLD-INVALID (the world's fault), voiding
  the battery until a replacement is sealed under amendment. (The v1
  review's benign 41024 constant is outside every v2 world id set and
  therefore cannot false-positive this check.)
- Determinism: each block is run 3 times end to end from fresh state.
  For the 8 fixed worlds, per-world transcripts must be byte-identical
  across the 3 runs (sha256 equality). M2-W1 uses a distinct sealed
  envelope per run (correction 1), so its determinism bar is
  per-run re-execution reproducibility (K-S2v2).

## 3. World specifications

Notation: each world lists its exact event stream. `QUERY s r e` lines
carry the grader truth as `e`. Predicted outcomes for the frozen
mechanisms are recorded honestly before execution; predicted FAILs are
information, not battery defects.

### 3.1 M1-W1: novel composition of two separately demonstrated procedures

Adversarial intent: the tested form (P-then-Q on novel instances) is
never demonstrated. Only a constructor that abstracts procedures and
composes them at runtime can answer; data-path construction,
memorized-demo replay, and nearest-instance matching all score zero by
construction. Material difference from FW2/FW3: as v1 (composition vs
replay; procedure composition vs arithmetic induction).

Event stream (`m1w1v2_world.txt`):

```
OBSERVE 40201 40601 40901
OBSERVE 40201 40602 40902
OBSERVE 40202 40601 40901
OBSERVE 40202 40602 40902
OBSERVE 40203 40603 40903
OBSERVE 40203 40604 40904
OBSERVE 40204 40603 40903
OBSERVE 40204 40604 40904
OBSERVE 40205 40601 40902
OBSERVE 40205 40602 40901
OBSERVE 40205 40603 40904
OBSERVE 40205 40604 40903
QUERY 40206 40601 40901
QUERY 40206 40602 40902
QUERY 40206 40603 40903
QUERY 40206 40604 40904
QUERY 40207 40601 40901
QUERY 40207 40602 40902
QUERY 40207 40603 40903
QUERY 40207 40604 40904
QUERY 40205 40601 40902
QUERY 40205 40602 40901
QUERY 40205 40603 40904
QUERY 40205 40604 40903
```

Procedure P = steps (40601->40901, 40602->40902), demonstrated on
40201/40202. Procedure Q = steps (40603->40903, 40604->40904),
demonstrated on 40203/40204. Instance 40205 is the noisy decoy (all
four ops swapped). Probes: 8 composition probes on novel 40206/40207
(expected P-then-Q ops in step order); 4 decoy probes on 40205
(expected the TAUGHT swapped values 40902/40901/40904/40903: faithful
retrieval, consistent with the M1-W2 collateral expectations per
correction 4).

Mechanism analysis (frozen source): composition probes are misses on
novel subjects with no facts; trial loop finds no paths; bootstrap
fails (no probe relation is invariant). Predicted: 8x ANSWER -2.
Decoy probes are direct hits returning the taught swapped values.
Predicted: 4/4 on the restated decoy bar. No composed graph exists in
state. Predicted: K-S5v2 FAIL on (a) and (c).

### 3.2 M1-W2: backward traversal of demonstrated chains

Adversarial intent and material difference: as v1 (isolates direction
as the only change from FW1's forward 3-hop shape).

Event stream (`m1w2v2_world.txt`):

```
OBSERVE 41111 41501 41112
OBSERVE 41112 41501 41113
OBSERVE 41113 41501 41114
OBSERVE 41121 41501 41122
OBSERVE 41122 41501 41123
OBSERVE 41123 41501 41124
QUERY 41111 41509 41114
QUERY 41121 41509 41124
QUERY 41114 41509 41111
QUERY 41113 41509 41111
QUERY 41124 41509 41121
QUERY 41123 41509 41121
QUERY 40205 40601 40902
QUERY 40205 40603 40904
```

Probes: 2 forward engagement probes (validity); 4 backward probes;
2 collateral probes from M1-W1 expecting the TAUGHT values
(40902/40904), consistent with K-S5v2(b) per correction 4. No single
learner trajectory is asked for two different answers to one triple.

Mechanism analysis: backward probes are misses; bootstrap on 41509
fails (only 2 facts by backward-probe time, below k=3, not invariant).
Predicted: 4x -2; engagement 2/2; collateral 2/2. Predicted: K-S6v2
FAIL (0/4 backward).

### 3.3 M1-W3: composition over a shared step (diamond)

Adversarial intent and material difference: as v1 (diamond topology
with a shared step vs M1-W1's disjoint composition and FW2's linear
replay).

Event stream (`m1w3v2_world.txt`):

```
OBSERVE 41721 41801 41911
OBSERVE 41721 41802 41912
OBSERVE 41721 41803 41913
OBSERVE 41722 41801 41911
OBSERVE 41722 41802 41912
OBSERVE 41722 41803 41913
OBSERVE 41723 41801 41912
OBSERVE 41723 41802 41911
OBSERVE 41723 41803 41912
QUERY 41721 41801 41911
QUERY 41726 41801 41911
QUERY 41726 41802 41912
QUERY 41726 41803 41913
QUERY 41111 41509 41114
QUERY 41121 41509 41124
```

Procedure P = (41801->41911, 41802->41912); procedure Q =
(41802->41912 shared, 41803->41913). Instance 41723 is the noisy decoy.
Probes: 1 engagement (41721 hit); 3 shared-composition probes on novel
41726; 2 collateral from M1-W2 (forward facts, hits).

Mechanism analysis: composition probes are misses on a novel subject;
bootstrap fails (41801: 41912/41911/41911 by recency; 41802:
41911/41912/41912; 41803: 41912/41913/41913; none invariant).
Predicted: 3x -2. Predicted: K-S7v2 FAIL (0/3).

### 3.4 M2-W1: inquiry under asymmetric cost with a flattery trap (sealed mapping)

Adversarial intent: removes FW6's literal-choice contract entirely;
only information gain scores. The flattery trap (informant C) is
adversarial against prior-agreement seeking rather than uncertainty
reduction. Correction 1 redesign: the informant-to-emitted-CHOICE
mapping is a per-run sealed permutation, so no constant policy can
pass; the mapping is revealed only through calibration-phase
exploration.

Structure: calibration phase (4 keys 45101-45104, truths 45101-45104
via objects 45201-45204 on relation 45600; 3 ACTs per key to consult an
informant, then the truth is revealed by OBSERVE, then a calibration
QUERY probe); inquiry phase (4 hidden keys 45111-45114, truths
45211-45214; per key: QUERY probe, 2 ACTs with informant responses,
final QUERY probe; budget 8 ACTs).

Informant roles (fixed by prereg; assignment to emitted CHOICE values
sealed per run): A truthful (answers the key's truth); B noisy (fixed
table below); C flatterer (always 45999, the seeded prior bias,
systematically wrong). Sealed envelope for run r contains the
permutation pi_r over {1,2,3} assigning emitted CHOICE values to roles
{A,B,C}; any other emitted CHOICE (including 0 and 30) maps to NONE
(wasted ACT, counts against budget). pi_r is constant across all keys
within run r, so calibration-phase exploration can identify the
truthful channel.

B's fixed table: calibration 45101->45201 (correct), 45102->45998
(wrong), 45103->45203 (correct), 45104->45997 (wrong); hidden
45111->45996, 45112->45995, 45113->45994, 45114->45993 (all wrong).
C: always 45999. Bias seeds: OBSERVE 45991 45600 45999,
OBSERVE 45992 45600 45999, OBSERVE 45993 45600 45999.

Driver: deterministic interactive loop frozen in section 5; the driver
log records one line per ACT: `ACT <CAL|INQ> <key> <choice> <NONE|A|B|C>`
with the role resolved through the sealed pi_r. The scorer resolves
roles only after the envelopes are opened post-run.

Mechanism analysis: calibration ACTs occur with no guides in state, so
CHOICE 0 (no informant). Inquiry QUERYs are misses (hidden keys have no
facts; trial finds no paths; bootstrap on 45600 not invariant),
creating one guide per hidden key. Inquiry ACTs emit CHOICE 30, which
maps to NONE (wasted). Final hidden probes are misses (-2).
Predicted: K-S8v2 FAIL: (a) engagement PASS; (b) 0 percent to sealed-A
FAIL; (c) 0 to sealed-C PASS; (d) 0/4 hidden FAIL; (e) 8 ACTs within
budget PASS.

Intended demand (correction 5): the calibration phase provides 12
exploratory ACTs against a run-constant sealed mapping, which suffices
to identify the truthful channel; the inquiry budget of 8 therefore
encodes a 2-explore/6-exploit demand (6 of 8 ACTs to sealed-A). A
learner that needs more than 2 inquiry-phase ACTs to re-verify the
channel fails (b) but is flagged by diagnostic D-CAUT (section 4.3)
rather than being confused with flattery-seeking or collapse.

### 3.5 M2-W2: stale guide persistence after resolution (vocabulary-neutral)

Adversarial intent: exploits the missing uncertainty-resolution
transition; guides are never superseded. Correction 6 redesign: the
bar no longer hardcodes CHOICE 30 or CHOICE 0. The mechanism's own
declared null action N is measured from a baseline ACT after a hit
with no guide in state; the bar is "post-resolution action equals N"
with validity "pre-resolution action differs from N".

Event stream (`m2w2v2_world.txt`):

```
OBSERVE 44011 44601 44021
QUERY 44011 44601 44021
ACT
QUERY 44111 44601 44901
ACT
OBSERVE 44111 44601 44901
OBSERVE 44302 44602 44312
OBSERVE 44303 44602 44313
OBSERVE 44304 44602 44314
OBSERVE 44305 44602 44315
OBSERVE 44306 44602 44316
OBSERVE 44307 44602 44317
QUERY 44111 44601 44901
ACT
QUERY 45101 45600 45201
QUERY 45102 45600 45202
```

The baseline ACT (after the hit on the taught fact, no guide in state)
records the mechanism's declared null action N. The miss QUERY creates
guide(44111); the pre-resolution ACT is the validity probe (must differ
from N, proving a live guide drove an inquiry action). The OBSERVE
resolves the uncertainty in the world. Six distractors flush 44111 from
the 4-deep context ring. The re-QUERY is a hit and re-pushes 44111.
The final ACT is the bar probe: a resolution-capable mechanism emits
N; the frozen mechanism emits the stale guide action. Collateral: 2
calibration truths from M2-W1 (hits).

Predicted: K-S9v2 FAIL (final ACT = stale guide action, not N;
validity: pre-resolution action differs from N; collateral 2/2).

### 3.6 M2-W3: discriminating action content across uncertainties (vocabulary-neutral)

Adversarial intent: exploits the hardcoded constant guide action. Three
isolated miss episodes; a discriminating inquiry mechanism emits a
different action per uncertainty. Correction 6 redesign: bars reference
the learner's own miss response M and declared null action N (N
carried across the block from M2-W2's baseline; M recorded from the
first inquiry-phase miss in M2-W1), never hardcoded integers.

Event stream (`m2w3v2_world.txt`):

```
QUERY 46201 46601 46901
ACT
OBSERVE 46311 46609 46391
OBSERVE 46312 46609 46392
OBSERVE 46313 46609 46393
OBSERVE 46314 46609 46394
QUERY 46202 46602 46902
ACT
OBSERVE 46321 46609 46395
OBSERVE 46322 46609 46396
OBSERVE 46323 46609 46397
OBSERVE 46324 46609 46398
QUERY 46203 46603 46903
ACT
QUERY 44111 44601 44901
QUERY 45103 45600 45203
```

Each episode: miss QUERY (novel subject and relation; trial finds no
paths; bootstrap finds no facts) creates one guide; 4 distractors flush
the previous subject from context; ACT fires only the current guide.
Bar: the three episode actions are pairwise distinct and each differs
from N. Validity: all three miss QUERYs yield the learner's own miss
response M (engagement without content). Collateral: 44111 (M2-W2) and
45103 (M2-W1) hits.

Predicted: K-S10v2 FAIL (constant guide action three times; validity:
3x M; collateral 2/2). Strong-form caveat carried over from v1: the
three uncertainties are structurally near-identical, so this bar tests
the strong form of the content claim by documented intent.

### 3.7 M3-W1: singleton vs systematic revision with delayed reuse

Adversarial intent: the revision operator is last-write-wins literal
patching with no evidence counting and no generalization beyond the
contradicted instance. The singleton probe separates counting revisers
from recency revisers; the generalization probes separate law revisers
from per-instance patchers. Material difference from FW5: as v1 (FW5's
bar REQUIRES last-write-wins; M3-W1's bar PUNISHES it and adds
generalization; opposite demands on the same operator).

Event stream (`m3w1v2_world.txt`):

```
OBSERVE 42911 42950 42921
OBSERVE 42912 42950 42922
OBSERVE 42913 42950 42923
OBSERVE 42914 42950 42924
OBSERVE 42915 42950 42925
OBSERVE 42916 42950 42926
OBSERVE 42201 42600 42204
OBSERVE 42202 42600 42205
OBSERVE 42203 42600 42206
OBSERVE 42204 42600 42207
OBSERVE 42205 42600 42208
OBSERVE 42206 42600 42209
OBSERVE 42207 42600 42210
OBSERVE 42208 42600 42211
QUERY 42201 42601 42204
QUERY 42202 42601 42205
QUERY 42203 42601 42206
QUERY 42204 42601 42207
OBSERVE 42201 42600 42210
OBSERVE 42202 42600 42207
OBSERVE 42203 42600 42208
OBSERVE 42204 42600 42209
OBSERVE 42821 42850 42831
OBSERVE 42822 42850 42832
OBSERVE 42823 42850 42833
OBSERVE 42824 42850 42834
OBSERVE 42825 42850 42835
OBSERVE 42826 42850 42836
OBSERVE 42827 42850 42837
OBSERVE 42828 42850 42838
OBSERVE 42829 42850 42839
OBSERVE 42830 42850 42840
OBSERVE 42831 42850 42841
OBSERVE 42832 42850 42842
QUERY 42201 42601 42204
QUERY 42202 42601 42207
QUERY 42203 42601 42208
QUERY 42204 42601 42209
QUERY 42205 42601 42210
QUERY 42206 42601 42211
QUERY 42911 42950 42921
QUERY 42912 42950 42922
QUERY 42913 42950 42923
QUERY 42914 42950 42924
QUERY 42915 42950 42925
QUERY 42916 42950 42926
```

Phase 0: 6 interference facts. Phase 1: law L (x+3) on 42201-42208.
Phase 1b: 4 promotion QUERYs on the novel relation 42601. Phase 2a:
singleton noise on 42201 (x+9, never corrected). Phase 2b: systematic
shift on 42202-42204 (x+5, never contradicted). Phase 3: 12
distractors. Probes: P1 singleton (42201, expect 42204 = original law;
a counting reviser rejects the uncorrected singleton); P2-P4
systematic (expect x+5: 42207/42208/42209); P5-P6 generalization on
unseen 42205/42206 (expect x+5: 42210/42211; requires the revision to
generalize beyond contradicted instances); P7-P12 interference.

Mechanism analysis: each contradiction triggers the single-schema
patch (last-write-wins). P1: patched to 42210, probe returns 42210
(FAIL: singleton incorporated). P2-P4: patched to x+5 (PASS).
P5-P6: misses with no data path to x+5 (ANSWER -2; FAIL: no
generalization). Interference: hits (PASS).

Predicted: K-S11v2 FAIL: (a) 3/3 PASS; (b) singleton FAIL; (c) 0/2
FAIL; (d) FAIL (no evidence-counted structure); (e) 6/6 PASS.
Strong-demand note carried over from v1: (c) requires law-level
revision, so a competent per-instance evidence-weighted reviser would
fail it; this is deliberate and documented so no future reader
mistakes (c) for a test of revision in general.

### 3.8 M3-W2: revision of a revision (recency-proof)

Adversarial intent: the operator's stale-cell lookup fails on second
contradiction (silent no-op). Correction 2 redesign: distractor
OBSERVEs on unrelated ids intervene between the final contradiction
and the bar probe, so the expected value differs from the most recent
observation; a global recency-echo policy answers a distractor object
and fails.

Material difference: M3-W1 tests one revision per instance plus
generalization; M3-W2 tests sequential revisions of the same link.
FW5 tested single contradictions under eviction; double revision is a
different demand.

Event stream (`m3w2v2_world.txt`):

```
OBSERVE 43201 43601 43202
OBSERVE 43202 43602 43203
QUERY 43201 43609 43203
QUERY 43201 43609 43203
OBSERVE 43202 43602 43209
QUERY 43201 43609 43209
OBSERVE 43202 43602 43219
OBSERVE 43651 43660 43671
OBSERVE 43652 43660 43672
OBSERVE 43653 43660 43673
OBSERVE 43654 43660 43674
OBSERVE 43655 43660 43675
OBSERVE 43656 43660 43676
QUERY 43201 43609 43219
QUERY 42202 42601 42207
QUERY 42201 42601 42204
```

The promotion QUERY builds the 2-hop chain; contradiction 1 (43209)
revises; contradiction 2 (43219) is the bar event; 6 distractor
OBSERVEs on unrelated ids follow; the bar probe expects 43219 (latest
evidence for the key, not the most recent observation in the stream).
Collateral: M3-W1 systematic (42207) and singleton (42204, original
law) values.

Predicted: K-S12v2 FAIL (the frozen mechanism's silent no-op leaves
the stale 43209; validity probes 43203 and 43209 correct; collateral
2/2).

Separation note: K-S12v2 distinguishes global-recency parroting from
per-key revision. It does not by itself convict per-key
last-write-wins (a per-key latest responder passes this bar); that
operator is convicted by M3-W1's singleton and generalization probes.
The two worlds divide the labor by design.

### 3.9 M3-W3: reverted revision blocks relearning (recency-proof)

Adversarial intent: when the single-schema patch breaks the graph,
the operator reverts and leaves the stale taught fact, short-circuiting
all future trial-loop learning on that key. Correction 2 redesign:
distractor OBSERVEs on unrelated ids intervene between the final
new-link teaches and the bar probe.

Material difference: M3-W2 tests silent no-op on second revision;
M3-W3 tests a revision that actively fails (revert) and then vetoes
recovery. FW4/FW5 never produced a reverted revision.

Event stream (`m3w3v2_world.txt`):

```
OBSERVE 43801 43901 43802
OBSERVE 43802 43902 43803
QUERY 43801 43909 43803
QUERY 43801 43909 43803
OBSERVE 43801 43901 43811
OBSERVE 43811 43902 43813
OBSERVE 43951 43960 43971
OBSERVE 43952 43960 43972
OBSERVE 43953 43960 43973
OBSERVE 43954 43960 43974
OBSERVE 43955 43960 43975
OBSERVE 43956 43960 43976
QUERY 43801 43909 43813
QUERY 43201 43609 43209
QUERY 42203 42601 42208
```

The promotion QUERY builds the 2-hop chain for (43801,43909). The
contradiction on the FIRST link (43811) breaks re-execution, so a
general reviser must unpromote and re-derive; the world then supplies
the new second link (43811->43813), making the current structure
43801->43811->43813. Six distractor OBSERVEs on unrelated ids follow.
The bar probe expects 43813. Collateral: W2 post-first-revision
(43209) and W1 systematic (42208).

Predicted: K-S13v2 FAIL (the frozen mechanism's revert leaves the
stale taught fact; probe returns 43803, not 43813; validity probes
correct; collateral 2/2).

## 4. Frozen kill bars K-S1v2 through K-S15v2

All bars are PASS/FAIL only; no partial credit. Process-bar failures
void the battery (re-seal and re-run); they are never scored as
mechanism verdicts.

- K-S1v2 (prereg ordering). PASS iff the SHA-256 of this file recorded
  by the coordinator was computed before any v2 world file or sealed
  envelope was created (filesystem mtime order) and the file is
  unmodified thereafter (hash re-verified after the battery).
  UNVERIFIABLE ORDERING voids this prereg.
- K-S2v2 (determinism). PASS iff, for each of the 3 blocks, the 3
  end-to-end runs from fresh state reproduce byte-identical
  per-world transcripts: for the 8 fixed worlds, sha256 equality of
  the transcript files across runs; for M2-W1, whose sealed envelope
  differs per run, immediate re-execution of run r with envelope_r
  reproduces the run-r transcript byte-identically.
- K-S3v2 (frozen binary). PASS iff `freeze_shim2_bin` hashes to
  `9217054c5af6dec057c4530c4de3ba246f521acc6df741d1989a4504acc72954`
  before each block run and after the battery, `tnn2.zag` still hashes
  to `a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd`,
  and `git status` shows zero modifications under the frozen
  cognition paths.
- K-S4v2 (seal integrity). PASS iff all world files, templates, truth
  files, and sealed envelopes match the manifest hashes recorded at
  generation, and grep of the exact v2 world id set over the frozen
  cognition sources finds zero matches.
- K-S5v2 (M1-W1 construction). PASS iff (a) at least 7 of the 8
  composition probes are correct; (b) all 4 decoy probes return the
  taught values (40902, 40901, 40904, 40903); (c) the state inspector
  reports a persistent structure whose licensed evidence includes at
  least one P-demo observation (from the 40201/40202 block) and at
  least one Q-demo observation (from the 40203/40204 block).
  Representation-neutral: no MAP, DEP, or SETREG vocabulary appears in
  this bar. All three required.
- K-S6v2 (M1-W2 reversal). PASS iff at least 3 of the 4 backward probes
  are correct. Validity: both forward engagement probes correct, else
  WORLD-INVALID.
- K-S7v2 (M1-W3 shared step). PASS iff at least 2 of the 3
  shared-composition probes are correct. Validity: engagement probe
  correct, else WORLD-INVALID.
- K-S8v2 (M2-W1 calibration, sealed mapping). PASS iff (a) the
  engagement check passes (at least one INQ ACT after a miss on a
  hidden key); (b) at least 6 of the 8 inquiry-phase ACTs route to the
  sealed truthful informant A (the 2-explore/6-exploit intended demand,
  section 3.4); (c) at most 1 inquiry-phase ACT routes to the sealed
  flattery informant C; (d) at least 3 of the 4 final hidden probes are
  correct; (e) inquiry-phase ACTs do not exceed the budget of 8. All
  five required. Roles are resolved through the opened envelopes after
  the runs; no hardcoded CHOICE integers appear in this bar.
- K-S9v2 (M2-W2 resolution, vocabulary-neutral). PASS iff the
  post-resolution ACT equals the mechanism's declared null action N,
  where N is the action emitted by the baseline ACT after a hit with
  no guide in state. Validity: the pre-resolution ACT differs from N,
  else WORLD-INVALID (an unengaged world is not a pass).
- K-S10v2 (M2-W3 content, vocabulary-neutral). PASS iff the three
  episode actions are pairwise distinct and each differs from the
  declared null action N (carried across the block from M2-W2).
  Validity: all three miss QUERYs yield the learner's own miss
  response M (recorded from the first inquiry-phase miss in M2-W1),
  else WORLD-INVALID.
- K-S11v2 (M3-W1 discrimination). PASS iff (a) at least 2 of the 3
  systematic probes are correct; (b) the singleton probe is correct
  (42204, original law); (c) at least 1 of the 2 generalization probes
  is correct; (d) the inspector reports a persistent structure whose
  current answer for the revised relation is a post-contradiction
  value and whose licensed evidence includes at least one
  contradiction-phase observation (the 42207/42208/42209 teaches).
  Representation-neutral: no SETREG or MAP vocabulary appears in this
  bar. (e) all 6 interference probes are correct. All five required.
- K-S12v2 (M3-W2 double revision, recency-proof). PASS iff the
  post-second-contradiction probe returns 43219, with at least one
  distractor OBSERVE on an unrelated id intervening between the final
  contradiction OBSERVE and the bar probe (satisfied by construction;
  verified by the scorer). Validity: the promotion probe (43203) and
  the post-first-revision probe (43209) are correct, else
  WORLD-INVALID.
- K-S13v2 (M3-W3 revert, recency-proof). PASS iff the post-revert
  probe returns 43813, with at least one distractor OBSERVE on an
  unrelated id intervening between the final new-link teach and the
  bar probe. Validity: the promotion/engagement probes return 43803,
  else WORLD-INVALID.
- K-S14v2 (retention). PASS iff at least 75 percent of all collateral
  probes across the battery (12 total) return their prereg-expected
  values.
- K-S15v2 (no-leak audit). PASS iff the scorer reports zero correct
  ANSWERs on novel-key probes whose value coincides with a taught
  triple from a different v2 world, and the K-S4v2 id-set grep is
  clean.

### 4.1 Predicted bar outcomes for the frozen mechanisms (recorded before execution)

K-S1v2, K-S2v2, K-S3v2, K-S4v2, K-S14v2, K-S15v2: predicted PASS
(process bars). K-S5v2: predicted FAIL (0/8 composition; decoy (b)
predicted 4/4 PASS under the restated faithful-retrieval expectation;
(c) FAIL). K-S6v2: predicted FAIL (0/4 backward). K-S7v2: predicted
FAIL (0/3). K-S8v2: predicted FAIL ((b) 0 percent to sealed-A, (d) 0/4
hidden). K-S9v2: predicted FAIL (stale guide action, not N).
K-S10v2: predicted FAIL (constant action three times). K-S11v2:
predicted FAIL ((b) singleton incorporated, (c) 0/2 generalization;
(a), (e) predicted PASS; (d) FAIL). K-S12v2: predicted FAIL (stale
43209, not 43219). K-S13v2: predicted FAIL (stale 43803, not 43813).

### 4.2 Calibration controls (battery-validation gates, not mechanism bars)

For each world, two pure-Zag control policies are frozen with the
battery and run once per world (they are deterministic programs; no
3-run requirement). Controls validate the bars; they make no claim
about any mechanism.

- G-DEP (degenerate gate): every degenerate control must FAIL the
  world's mechanism bar. If a degenerate control passes, the world is
  WORLD-VOID (battery defect): no mechanism verdict is drawn from it.
- G-COMP (competent gate): every competent control must PASS the
  world's mechanism bar. If a competent control fails, the world is
  WORLD-VOID (battery defect): the bar is too hard or miscalibrated.

Control definitions:

- M1-W1: D = per-key latest-observation responder (memorizer; novel
  subjects yield the miss response). C = symbolic composer: extracts
  the per-relation mapping from the demo OBSERVEs and emits P-then-Q
  in step order on novel subjects.
- M1-W2: D = forward-only responder (answers forward probes from
  taught facts; backward probes yield the miss response). C =
  bidirectional responder (builds a reverse index; answers backward
  probes).
- M1-W3: D = per-key latest-observation responder. C = shared-step
  composer (recognizes the shared step; composes on the novel
  subject).
- M2-W1: D suite = three constant policies (always emit 1, always emit
  2, always emit 3). Gate: per run, at least 2 of the 3 must FAIL
  K-S8v2 (exactly the constant aligned with the sealed truthful
  channel may pass). C = calibrate-then-exploit: emits 1, 2, 3 across
  the 12 calibration ACTs, identifies the emitted value whose
  informant responses always match the revealed truths, and exploits
  that channel for all 8 inquiry ACTs. Must PASS K-S8v2 on all 3 runs.
- M2-W2: D1 = constant-action policy (one fixed action every ACT);
  D2 = stale-action policy (repeats the pre-resolution action after
  resolution). Neither may pass K-S9v2. C = miss/hit responder (emits
  a guide action on miss, the baseline null action on hit). Must PASS.
- M2-W3: D = constant-action policy. C = per-episode distinct actions.
  C must PASS K-S10v2; D must FAIL it.
- M3-W1: D = per-key last-write responder. Must FAIL K-S11v2 (via the
  singleton and generalization probes). C = evidence-counted reviser
  (adopts a change only after at least 2 consistent observations;
  rejects the uncorrected singleton; applies the observed shift law to
  unseen subjects). Must PASS.
- M3-W2: D = global-recency responder (answers the object of the most
  recent OBSERVE in the whole stream). Must FAIL K-S12v2 (answers a
  distractor object). C = per-key latest responder. Must PASS.
  Documented separation: this bar isolates global-recency parroting
  from per-key revision; per-key last-write-wins is convicted by
  M3-W1, not here.
- M3-W3: D = global-recency responder. Must FAIL K-S13v2. C =
  unpromote-and-rederive responder (on contradiction of a link in a
  derived chain, drops the derived fact and re-derives the 2-hop
  structure from current observations). Must PASS.

### 4.3 Diagnostics (informational only; never part of any kill bar)

- D-WB1 (M1-W1): the v1 implementation-coupled check restated as a
  diagnostic: whether a MAP/DEP-structured node with both demo blocks
  exists. Informational.
- D-WB2 (M3-W1): the v1 SETREG-literal check as a diagnostic.
  Informational.
- D-CAUT (M2-W1): cautious re-verification signature: (d) at least 3/4
  probes correct AND fewer than 6 inquiry ACTs to sealed-A AND zero
  ACTs to sealed-C AND a majority of the remaining ACTs to sealed-B.
  Distinguishes cautious verification from flattery-seeking or
  collapse when (b) fails.
- D-IG (M2-W1): count of inquiry-phase ACTs routed to sealed-A
  (information-gain diagnostic; the correction-1 alternative scored
  directly).
- D-CONF (M1-W1): whether composition answers on novel instances
  follow the majority structure despite the noisy decoy
  (informational on the abstraction vs faithful-retrieval tension).

## 5. Execution protocol and tools

### 5.1 Tools (all pure Zag, pinned znc; built after this prereg freezes)

- `v2_worldgen.zag`: generates the 8 fixed world files and the M2-W1
  template from sections 3.1-3.3 and 3.5-3.9; generates the 3 sealed
  envelopes for M2-W1 (per-run permutation pi_r drawn from a
  committed seed; informant tables per section 3.4); writes
  `WORLD_MANIFEST_V2.sha256` covering world files, template, truth
  files, and envelope hashes (envelope contents stay sealed).
- `v2_sealed_score.zag`: argv [worldfile, transcript]. Parses QUERY
  (s,r,e) lines and ANSWER (s,r,v) lines 1:1 in order; prints
  per-probe PASS/FAIL and summary counts; lists CHOICE values in
  order; verifies distractor-intervention requirements for K-S12v2
  and K-S13v2.
- `v2_score_m2w1.zag`: argv [transcript, driverlog, envelope]. Opens
  the envelope after the run; checks K-S8v2 sub-bars with roles
  resolved through pi_r; computes D-CAUT and D-IG.
- `v2_inspect_state.zag`: argv [state.bin]. Reports persistent
  structures in representation-neutral terms: for each persistent
  structure, its current answer value and the set of source
  observation facts (s,r,o triples from the world's OBSERVE stream)
  reachable as its licensed evidence. The exact byte format is frozen
  at build time; the semantic requirement (evidence sets, not node
  types) is fixed here.
- `v2_controls.zag`: implements the section 4.2 control policies as
  driver-level responders; prints per-control PASS/FAIL against each
  world's mechanism bar.

### 5.2 Block driver (deterministic shell)

Per block run: remove any prior state.bin; for W1..W3 in order, run
`freeze_shim2_bin <world> <state.bin>` (exit code must be 0), saving
stdout as the world transcript. For M2-W1, the interactive driver
grows the world file from the fixed template using envelope_r for run
r: bias seeds, calibration loop (per key: up to 3 ACTs with informant
routing through pi_r, truth OBSERVE, calibration QUERY probe),
inquiry loop (per hidden key: QUERY probe, 2 ACTs with informant
responses, final QUERY probe); the driver log is saved. After the
block, run the inspector on the final state.bin (once per block run;
informational for the representation-neutral bars, not part of
determinism). Repeat 3 times; apply K-S2v2 (including immediate
re-execution of each M2-W1 run with its envelope to confirm
byte-identical reproduction).

### 5.3 Anti-smuggling and manifest

At generation: sha256 manifest of all world/template/truth/envelope
files (envelope contents hashed but sealed). Before execution: grep
the exact v2 world id set in the frozen cognition sources (K-S4v2).
Hash re-verification of the shim binary before each block run and
after the battery (K-S3v2).

## 6. Sealing protocol

1. Roles. WORLDGEN (independent adversary builder lane) generates
   world files, envelopes, and the manifest. SCORER lane builds the
   scoring and inspection tools from this prereg. EXECUTOR runs the
   blocks. No lane modifies mechanism source; no lane edits this
   prereg after freeze.
2. Adversary independence. The WORLDGEN worker attests in its
   NAMECHECK Step 0: (i) it has not authored mechanism-build or
   mechanism-repair code in the previous two waves; (ii) it may read
   the frozen mechanism source for adversarial design (white-box
   adversarial intent is permitted); (iii) it writes only inside its
   wave lane directory. The sealed envelopes are generated by WORLDGEN
   alone; the SCORER and EXECUTOR lanes never see envelope contents
   before the runs complete.
3. Freeze ordering. The coordinator commits this prereg alone and
   records its SHA-256. World files and envelopes are created only
   after that recorded freeze (K-S1v2 verifies hash plus filesystem
   mtime ordering). UNVERIFIABLE ORDERING voids this prereg.
4. Sealed envelopes (M2-W1). Three envelopes, one per run, each
   containing pi_r and the informant response tables. Envelope hashes
   are committed in the world manifest before any run. Envelopes are
   opened by the scorer only after all runs complete. The learner
   never sees pi_r; it observes only its own emitted CHOICE values
   and the resulting OBSERVE responses.
5. No post-freeze amendments. Any defect found after world generation
   makes the affected world WORLD-VOID; a replacement requires a new
   sealed world under a new prereg section, never an edit to the
   sealed files.
6. Determinism and manifest discipline per section 5.

## 7. Verdict rules and what a re-run on the three TNN-2 mechanisms establishes

Verdict rules:

- M1 SURVIVES-SEALED iff K-S5v2 and K-S6v2 and K-S7v2 all PASS; else
  M1 FAILS (kill evidence: the failed sub-bars).
- M2 SURVIVES-SEALED iff K-S8v2 and K-S9v2 and K-S10v2 all PASS; else
  M2 FAILS.
- M3 SURVIVES-SEALED iff K-S11v2 and K-S12v2 and K-S13v2 all PASS; else
  M3 FAILS.
- Any process-bar (K-S1v2..K-S4v2, K-S14v2, K-S15v2) failure VOIDs the
  battery; a void battery is re-sealed and re-run, never interpreted.
- Any calibration-gate (G-DEP/G-COMP) failure VOIDs the affected world
  as a battery defect; no mechanism verdict is drawn from a void world.
  There is no partial-generality verdict.

What a v2 re-run on the three frozen TNN-2 mechanisms establishes and
does not establish:

- The three v1 kills STAND and are not re-litigated here. M1: no
  procedure abstraction (0/8 composition, 0/4 backward, 0/3 shared,
  on calibrated bars). M2: constant inquiry action, no informant
  discrimination, no resolution transition (on calibrated bars).
  M3: last-write-wins patching, silent no-op on second contradiction,
  revert veto on relearning (on calibrated bars plus re-verified
  frozen-binary learner-state evidence). These rest on the calibrated
  portion of the v1 battery, not on its miscalibrated bars.
- The v2 battery is a battery-design validation instrument, not a
  mechanism rescue. The mechanisms are frozen and unchanged; no v2
  score alters, softens, or reopens the three standing kills on its
  own.
- Expected result, given the kills were on the calibrated portion:
  the mechanisms FAIL the v2 bars with the same degenerate signatures
  (section 4.1). If observed, the v2 battery PASSES its validation:
  it convicts known degeneracy through calibrated bars, and the v1
  kills are corroborated through calibrated bars.
- If a mechanism PASSES a v2 bar it failed in v1, the v2 battery
  FAILS its validation on that world: this is a battery defect, not
  a mechanism vindication. The corresponding v1 kill evidence is
  REOPENED for defect analysis, and no mechanism verdict is upgraded.
- The v2 battery must be able to acquit genuine competence: the
  competent controls (section 4.2) demonstrate that every bar is
  passable by a correct policy, and the degenerate controls
  demonstrate that every bar is impassable by the degenerate policies
  it targets. A future mechanism passing the v2 bars would therefore
  constitute calibrated generality evidence for that mechanism,
  still subject to section 8: no L3 claim follows from any score
  here.

## 8. Criterion 0 status (binding; no L3 claim on any pass)

This battery tests whether frozen, researcher-authored mechanisms
generalize to fresh structures, and whether the battery itself is a
calibrated instrument. It does not test representational invention:

- C0-A (runtime-defined semantics): NOT MET. The exercised semantics
  (trial-loop assemblers, guide actions, single-schema patch) are
  researcher-authored machinery in the frozen source.
- C0-B (open structural form): NOT MET. Every world's tested form is
  enumerable from its demonstrations before the run.
- C0-C (multiple unforeseen forms, independent post-freeze adversary):
  NOT MET. Nine worlds across three families, designed post-freeze,
  but the adversary role is played inside the same research loop. A
  second battery by a genuinely separate adversary is required before
  any L3-adjacent claim.
- C0-D (cognitive reuse): NOT MET as a criterion. Delayed-reuse and
  collateral probes measure reuse-like behavior, which is evidence
  toward a future C0-D case, but a single battery's probes are
  explicitly insufficient.

Consequence: no score on this battery, however high, may be described
as L3, L3-adjacent, or progress toward L3 without a separate
Criterion 0 case on independent evidence. The strongest honest claim
available from a v2 validation PASS is: the v2 battery is a calibrated
instrument that convicts known degeneracy and acquits correct
policies, and the v1 mechanism kills are corroborated through
calibrated bars.

## 9. Traceability: the six corrections as frozen bars

1. M2-W1 sealed mapping (correction 1): per-run sealed permutation
   pi_r over emitted CHOICE values to informant roles (section 3.4);
   K-S8v2(b)(c) scored against the opened envelopes with no hardcoded
   integers; G-DEP requires at least 2 of the 3 constant policies to
   fail per run; D-IG scores the information-gain alternative
   directly.
2. Recency confound (correction 2): 6 distractor OBSERVEs on unrelated
   ids between the final contradiction (M3-W2) or final new-link
   teaches (M3-W3) and the bar probe; K-S12v2/K-S13v2 require the
   expected value to differ from the most recent observation, with
   scorer-verified distractor intervention; G-DEP runs a
   global-recency responder that must fail both bars.
3. White-box coupling (correction 3): K-S5v2(c) and K-S11v2(d)
   restated in representation-neutral terms (persistent structure,
   licensed evidence sets, current answer values); the v1
   MAP/DEP/SETREG checks survive only as diagnostics D-WB1 and D-WB2.
4. Cross-world consistency (correction 4): K-S5v2(b) decoy probes and
   the M1-W2 collateral probes both expect the taught values; no two
   bars demand different answers to the identical triple from one
   learner trajectory.
5. K-S8 tightness (correction 5): the 2-explore/6-exploit budget is
   documented as the intended demand (section 3.4); the calibration
   phase supplies 12 exploratory ACTs against a run-constant sealed
   mapping so identification is feasible; D-CAUT distinguishes
   cautious re-verification from flattery-seeking or collapse.
6. Vocabulary-neutral validity (correction 6): K-S9v2 and K-S10v2
   reference the mechanism's own declared null action N and miss
   response M, measured in-block, instead of hardcoded 30/0; M2-W1
   roles are resolved through sealed envelopes rather than a fixed
   CHOICE table.

## 10. What a FAIL means

Per the standing no-patch-treadmill rule, a mechanism FAIL on v2 is
corroboration of the standing v1 kills through calibrated bars, not a
request for a patch. A battery-validation FAIL (a world VOID by
calibration gates, or a mechanism PASS on a bar it failed in v1) is
evidence about the battery's design, not about the mechanisms; it is
recorded as a battery defect with the void world's evidence preserved,
and any replacement world is sealed under a new prereg section.
Benchmark-specific handlers and per-world opcodes are rejected in
advance.
