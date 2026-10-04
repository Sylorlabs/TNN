# PREREG: Sealed Adversarial Battery V3 on TNN-2 Mechanisms (wave-20261001-2321pdt, lane BATTERY)

**Status:** PREREG-FROZEN (design only; no world files generated, no
envelopes generated, no runs executed at freeze time). This document is
frozen by SHA-256 before any v3 world file or sealed envelope is created
(see K-S1v3). Implementation and world generation are authorized only
after this prereg is committed alone. UNVERIFIABLE ORDERING voids this
prereg.

**Wave:** wave-20261001-2321pdt, lane BATTERY.
**Date:** 2026-10-02.
**Documentation rule observed:** no em-dashes in this file.

## 0. Step 0 (toolchain guard)

Recorded in this lane's NAMECHECK.md Step 0: safebin activated,
`which python3` prints nothing, `which python` prints nothing, pinned
znc from safebin. Every program built under this prereg (world
generator, interactive driver, scorers, state inspector, calibration
controls) is Zag compiled with the pinned znc; shell (safebin
bash/awk/grep) is used only for byte checks, file transport, and hash
manifests. No Python anywhere; any forbidden executable invocation is
automatic PROCESS-FAIL.

## 1. Freeze record (mechanisms unchanged from v1/v2)

The three TNN-2 mechanisms under test are frozen and unchanged. The v3
battery is a battery-design instrument, not a mechanism repair and not a
mechanism rescue. Frozen artifacts (identical to v1/v2):

- TNN-2 mechanism source: file
  `docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag`
  (1591 lines), SHA-256
  `a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd`.
- Sealed interface shim binary `core_freeze_tnn2_shim/freeze_shim2_bin`,
  SHA-256
  `9217054c5af6dec057c4530c4de3ba246f521acc6df741d1989a4504acc72954`
  (zero-cognition transport: OBSERVE to OBSERVED, QUERY to ANSWER, ACT
  to CHOICE; the executed path for all v3 runs).
- Compiler: `src/tools/toolchain/znc_linux_x86_64_abed8aa1`, SHA-256
  `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`.
- Mechanisms: (M1) runtime executable-graph construction via the
  `t2_trial` miss policy; (M2) learner-originated uncertainty guiding
  action via `miss_inquire` guides feeding `ev_act`; (M3)
  counterexample-driven revision via `revise_on_contradict` /
  `t2_revise_graph` (single-schema literal patch).

## 2. Battery scope and global constraints

Nine sealed worlds, three per mechanism. The v3 worlds are FRESH
instances: new id block, new demo topologies, new tested forms. The
nine family demands are the calibrated v2 families (composition,
reversal, shared-step; sealed inquiry, resolution, content;
discrimination, double revision, revert), because v2 validated those
families as discriminating. What is new in v3: (a) the six
triviality-review corrections are design invariants from the start
(section 11); (b) correction 3 is applied COMPLETELY (the v2
K-S11v2(d) restatement was still looser than the evidence-counting
intent; v3 tightens the bar text to require both-phase licensed
evidence); (c) the v2 M2-W2 fresh-state baseline protocol (frozen
amendment AMENDMENT_M2W2.md) is BASE PROTOCOL in v3, not an
amendment; (d) cross-world collateral expectations are made
consistent by construction (section 3). FW1-FW9 is a REGRESSION
battery for TNN-2 and can never establish generality or L3; no v3
world is an FW1-FW9 world or a trivial variant of one. The v3 worlds
are also not re-ids of v1/v2 worlds: each world's "new in v3" note
records the changed tested form.

Global constraints:

- Event streams use integer ids only. No natural language, no task
  labels, no family identifiers.
- Id block 50000-59999 for the whole battery, disjoint from FW1-FW9
  ids (30000-39999) and from the v1/v2 battery ids (40000-49999).
  Sub-blocks: M1 50000-51999, M3 52000-53999, M2 54000-56999
  (W2 54000-54999, W1 55000-55999, W3 56000-56999).
- Worlds run in three blocks. M1 block: W1->W2->W3 on one persistent
  state chain (fresh state at block start). M3 block: W1->W2->W3 on
  one persistent state chain (fresh state at block start). M2 block:
  W1 then W3 on persistent state A (fresh at block start); W2 runs on
  a SEPARATE fresh state B, never chained from state A (the v2
  amendment protocol as base design). Rationale: the K-S9v3 baseline
  requires a guide-free null-action measurement, which is
  unachievable anywhere in a persistent chain once guides exist
  (v2 validation section 3 diagnosis, carried forward).
- Worlds 2 and 3 of the M1 and M3 blocks carry 2 collateral probes
  from the previous world(s) of the block, testing retention. M2-W2
  carries 2 engagement probes (W1 calibration truths on fresh state,
  expecting the miss response). M2-W3 carries 2 collateral probes
  from W1 (state A chain). 12 collateral/engagement probes total.
- The `expected` field on QUERY lines is the grader's truth. It is
  also passed to `ev_query` as the trial-loop oracle (documented
  behavior of the frozen mechanism); bars are designed so oracle
  access alone cannot pass them (every bar-critical probe has no
  data path to its expected value, or the expected value is the
  taught fact).
- No harness behavior depends on the learner's internals; all driver
  mappings are fixed in this prereg (M2-W1 mappings are fixed by the
  sealed per-run envelopes, section 3.4) and mechanical.
- Anti-smuggling: before execution, the exact id set extracted from
  the v3 world files is grepped in the frozen cognition sources; any
  match makes the affected world WORLD-INVALID (the world's fault),
  voiding the battery until a replacement is sealed under amendment.
- Determinism: each block is run 3 times end to end from fresh state.
  For the 7 fixed worlds, per-world transcripts must be byte-identical
  across the 3 runs (sha256 equality). M2-W1 uses a distinct sealed
  envelope per run, so its determinism bar is per-run re-execution
  reproducibility (K-S2v3). M2-W2 (fresh state B) is run 3 times from
  fresh state; transcripts byte-identical across the 3 runs.

## 3. World specifications

Notation: each world lists its exact event stream. `QUERY s r e` lines
carry the grader truth as `e`. Predicted outcomes for the frozen
mechanisms are recorded honestly before execution; predicted FAILs are
information, not battery defects.

### 3.1 M1-W1: novel Q-then-P composition (reversed order)

New in v3: the tested composition order is Q-then-P (v1/v2 tested
P-then-Q). A constructor that genuinely abstracts procedures composes
in either order; a form-memorizer cannot transfer the v1/v2 form.

Event stream (`m1w1v3_world.txt`):

```
OBSERVE 50201 50601 50901
OBSERVE 50201 50602 50902
OBSERVE 50202 50601 50901
OBSERVE 50202 50602 50902
OBSERVE 50203 50603 50903
OBSERVE 50203 50604 50904
OBSERVE 50204 50603 50903
OBSERVE 50204 50604 50904
OBSERVE 50205 50601 50902
OBSERVE 50205 50602 50901
OBSERVE 50205 50603 50904
OBSERVE 50205 50604 50903
QUERY 50206 50603 50903
QUERY 50206 50604 50904
QUERY 50206 50601 50901
QUERY 50206 50602 50902
QUERY 50207 50603 50903
QUERY 50207 50604 50904
QUERY 50207 50601 50901
QUERY 50207 50602 50902
QUERY 50205 50601 50902
QUERY 50205 50602 50901
QUERY 50205 50603 50904
QUERY 50205 50604 50903
```

Procedure P = steps (50601->50901, 50602->50902), demonstrated on
50201/50202. Procedure Q = steps (50603->50903, 50604->50904),
demonstrated on 50203/50204. Instance 50205 is the noisy decoy (all
four steps swapped). Probes: 8 composition probes on novel 50206/50207
(expected Q-then-P steps in step order); 4 decoy probes on 50205
(expected the TAUGHT swapped values 50902/50901/50904/50903: faithful
retrieval, consistent with the M1-W2 collateral expectations per
correction 4).

Mechanism analysis (frozen source): composition probes are misses on
novel subjects with no facts; trial loop finds no paths; bootstrap
fails (no probe relation is invariant: 50601 objects are
50902/50901/50901, not invariant; likewise the others). Predicted: 8x
ANSWER -2. Decoy probes are direct hits returning the taught swapped
values. Predicted: 4/4 on the restated decoy bar. No composed graph
exists in state. Predicted: K-S5v3 FAIL on (a) and (c).

Material difference from FW2: FW2 replays one demonstrated procedure
on novel instances (tested form equals demonstrated form); M1-W1v3
never demonstrates the tested Q-then-P form and reverses the v1/v2
order. Composition vs replay: different demand.

### 3.2 M1-W2: backward traversal of 4-hop chains

New in v3: 4-hop chains (v1/v2 used 3-hop); isolates direction as the
only change from FW1's forward shape, at greater depth.

Event stream (`m1w2v3_world.txt`):

```
OBSERVE 51111 51501 51112
OBSERVE 51112 51501 51113
OBSERVE 51113 51501 51114
OBSERVE 51114 51501 51115
OBSERVE 51121 51501 51122
OBSERVE 51122 51501 51123
OBSERVE 51123 51501 51124
OBSERVE 51124 51501 51125
QUERY 51111 51509 51115
QUERY 51121 51509 51125
QUERY 51115 51509 51111
QUERY 51114 51509 51111
QUERY 51125 51509 51121
QUERY 51124 51509 51121
QUERY 50205 50601 50902
QUERY 50205 50603 50904
```

Probes: 2 forward engagement probes (validity; trial promotes 1-hop
verifying graphs via the oracle since the expected value is the taught
chain end); 4 backward probes; 2 collateral probes from M1-W1
expecting the TAUGHT values (50902/50904), consistent with K-S5v3(b)
per correction 4. No single learner trajectory is asked for two
different answers to one triple.

Mechanism analysis: backward probes are misses (no outgoing facts from
the chain ends on any relation; trial BFS from 51115/51114 finds no
paths); bootstrap on 51509 fails (no 51509 facts at backward-probe
time). Predicted: 4x -2; engagement 2/2 (trial+oracle 1-hop
promotion); collateral 2/2. Predicted: K-S6v3 FAIL (0/4 backward).

### 3.3 M1-W3: convergent composition (shared last step)

New in v3: convergent (V) topology with a shared LAST step (v1/v2 M1-W3
used a diamond with a shared middle step). Two different first steps
converge through one shared final step; the constructor must recognize
step identity independent of position.

Event stream (`m1w3v3_world.txt`):

```
OBSERVE 51721 51801 51911
OBSERVE 51721 51802 51912
OBSERVE 51721 51803 51911
OBSERVE 51722 51801 51911
OBSERVE 51722 51802 51912
OBSERVE 51722 51803 51911
OBSERVE 51723 51801 51912
OBSERVE 51723 51802 51911
OBSERVE 51723 51803 51912
QUERY 51721 51801 51911
QUERY 51726 51801 51911
QUERY 51726 51803 51911
QUERY 51726 51802 51912
QUERY 51111 51509 51115
QUERY 51121 51509 51125
```

Procedure P = (51801->51911, 51802->51912); procedure Q =
(51803->51911, 51802->51912 shared last step). Instance 51723 is the
noisy decoy. Probes: 1 engagement (51721 hit); 3 convergent
composition probes on novel 51726; 2 collateral from M1-W2 (forward
facts via the trial-promoted MAPs, hits).

Mechanism analysis: composition probes are misses on a novel subject;
bootstrap fails (51801 objects: 51912/51911/51911, not invariant;
51802 objects: 51911/51912/51912, not invariant; 51803 objects:
51912/51911/51911, not invariant). Predicted: 3x -2. Predicted:
K-S7v3 FAIL (0/3).

### 3.4 M2-W1: inquiry under asymmetric cost with a flattery trap (sealed mapping)

Unchanged protocol from v2 (the calibrated design); new ids, new
committed envelope seed 20261002, new informant tables. Correction 1
as a base invariant: the informant-to-emitted-CHOICE mapping is a
per-run sealed permutation, so no constant policy can pass; the
mapping is revealed only through calibration-phase exploration.

Structure: calibration phase (4 keys 55101-55104, truths 55201-55204
on relation 55600; 3 ACTs per key to consult an informant, then the
truth is revealed by OBSERVE, then a calibration QUERY probe); inquiry
phase (4 hidden keys 55111-55114, truths 55211-55214; per key: QUERY
probe, 2 ACTs with informant responses, final QUERY probe; budget 8
ACTs).

Informant roles (fixed by prereg; assignment to emitted CHOICE values
sealed per run): A truthful (answers the key's truth); B noisy (fixed
table below); C flatterer (always 55999, the seeded prior bias,
systematically wrong). Sealed envelope for run r contains the
permutation pi_r over {1,2,3} assigning emitted CHOICE values to roles
{A,B,C}; any other emitted CHOICE (including 0 and 30) maps to NONE
(wasted ACT, counts against budget). pi_r is constant across all keys
within run r, so calibration-phase exploration can identify the
truthful channel. pi_r drawn from committed seed 20261002 via LCG +
Fisher-Yates, deduped, all three distinct (same procedure as v2).

B's fixed table: calibration 55101->55201 (correct), 55102->55998
(wrong), 55103->55203 (correct), 55104->55997 (wrong); hidden
55111->55996, 55112->55995, 55113->55994, 55114->55993 (all wrong).
C: always 55999. Bias seeds: OBSERVE 55991 55600 55999,
OBSERVE 55992 55600 55999, OBSERVE 55993 55600 55999.

Driver: deterministic interactive loop (same step program as v2: step
0 emits bias seeds; steps 1-24 calibration; steps 25-48 inquiry); the
driver log records one line per ACT: `ACT <CAL|INQ> <key> <choice>
<NONE|A|B|C>` with the role resolved through the sealed pi_r. The
scorer resolves roles only after the envelopes are opened post-run.

Mechanism analysis: calibration ACTs occur with no guides in state, so
CHOICE 0 (no informant). Inquiry QUERYs are misses (hidden keys have no
facts; trial finds no paths; bootstrap on 55600 not invariant),
creating one guide per hidden key. Inquiry ACTs emit CHOICE 30, which
maps to NONE (wasted). Final hidden probes are misses (-2).
Predicted: K-S8v3 FAIL: (a) engagement PASS; (b) 0 percent to sealed-A
FAIL; (c) 0 to sealed-C PASS; (d) 0/4 hidden FAIL; (e) 8 ACTs within
budget PASS.

Intended demand (correction 5): the calibration phase provides 12
exploratory ACTs against a run-constant sealed mapping, which suffices
to identify the truthful channel; the inquiry budget of 8 therefore
encodes a 2-explore/6-exploit demand (6 of 8 ACTs to sealed-A). A
learner that needs more than 2 inquiry-phase ACTs to re-verify the
channel fails (b) but is flagged by diagnostic D-CAUT rather than
being confused with flattery-seeking or collapse.

Material difference from FW6: FW6 rewards a literal CHOICE 0 contract
plus recall; M2-W1v3 has no correct literal choice and scores only
information gain via informant selection.

### 3.5 M2-W2: stale guide persistence after resolution (fresh-state baseline, vocabulary-neutral)

Base protocol in v3 (v2 amendment incorporated by design): this world
runs on a SEPARATE fresh state B, never chained from the M2-W1 state
A. The K-S9v3 baseline requires a guide-free null-action measurement,
which the v2 validation proved unachievable anywhere in a persistent
chain once M2-W1's guides exist. The bar no longer hardcodes CHOICE 30
or CHOICE 0 (correction 6): the mechanism's own declared null action N
is measured from the fresh-state baseline ACT; the bar is
"post-resolution action equals N" with validity "pre-resolution action
differs from N".

Event stream (`m2w2v3_world.txt`):

```
OBSERVE 54011 54601 54021
QUERY 54011 54601 54021
ACT
QUERY 54111 54601 54901
ACT
OBSERVE 54111 54601 54901
OBSERVE 54302 54602 54312
OBSERVE 54303 54602 54313
OBSERVE 54304 54602 54314
OBSERVE 54305 54602 54315
OBSERVE 54306 54602 54316
OBSERVE 54307 54602 54317
QUERY 54111 54601 54901
ACT
QUERY 55101 55600 55201
QUERY 55102 55600 55202
```

The baseline ACT (after the hit on the taught fact, no guide in fresh
state) records the mechanism's declared null action N. The miss QUERY
creates guide(54111); the pre-resolution ACT is the validity probe
(must differ from N, proving a live guide drove an inquiry action).
The OBSERVE resolves the uncertainty in the world. Six distractors
flush 54111 from the 4-deep context ring. The re-QUERY is a hit and
re-pushes 54111. The final ACT is the bar probe: a resolution-capable
mechanism emits N; the frozen mechanism emits the stale guide action.
Collateral: 2 engagement probes on M2-W1 calibration truths, run on
fresh state B where those facts were never observed; expected value is
the mechanism's own miss response M (engagement only, not retention).

Predicted: K-S9v3 FAIL (N=0 measured, pre-resolution ACT=30 guide
driven, post-resolution ACT=30 stale; validity holds 30 != 0;
engagement probes 2x M). This matches the v2 amended re-run signature
exactly and corroborates the v1 M2 kill (no resolution transition)
through a calibrated bar.

Material difference from FW6: temporal guide lifecycle with no
informants vs a single diagnostic round.

### 3.6 M2-W3: discriminating action content across uncertainties (vocabulary-neutral)

Runs on state A after M2-W1 (persistent chain W1->W3). Three isolated
miss episodes; a discriminating inquiry mechanism emits a different
action per uncertainty. Bars reference the learner's own miss response
M (recorded from the first inquiry-phase miss in M2-W1) and declared
null action N (measured in M2-W2's fresh-state baseline, carried as a
parameter), never hardcoded integers (correction 6).

Event stream (`m2w3v3_world.txt`):

```
QUERY 56201 56601 56901
ACT
OBSERVE 56311 56609 56391
OBSERVE 56312 56609 56392
OBSERVE 56313 56609 56393
OBSERVE 56314 56609 56394
QUERY 56202 56602 56902
ACT
OBSERVE 56321 56609 56395
OBSERVE 56322 56609 56396
OBSERVE 56323 56609 56397
OBSERVE 56324 56609 56398
QUERY 56203 56603 56903
ACT
QUERY 55103 55600 55203
QUERY 55104 55600 55204
```

Each episode: miss QUERY (novel subject and relation; trial finds no
paths; bootstrap finds no facts) creates one guide; 4 distractors flush
the previous subject from context; ACT fires only the current guide.
Bar: the three episode actions are pairwise distinct and each differs
from N. Validity: all three miss QUERYs yield the learner's own miss
response M (engagement without content). Collateral: 2 hits from state
A (55103, 55104 calibration truths).

Predicted: K-S10v3 FAIL (constant guide action three times: 30,30,30;
validity: 3x M; collateral 2/2). Strong-form caveat carried over from
v1/v2: the three uncertainties are structurally near-identical, so this
bar tests the strong form of the content claim by documented intent.

Material difference from FW6/FW7: action-content discrimination across
episodes; FW6/FW7 never varied the uncertainty.

### 3.7 M3-W1: singleton vs systematic revision with delayed reuse (tightened white-box bar)

New in v3: new law (+7 -> +11, v1/v2 used +3 -> +5); the K-S11v3(d)
white-box bar is TIGHTENED per the v2 lesson (correction 3 applied
completely): it now requires licensed evidence from BOTH the original
phase AND the contradiction phase, enforcing the evidence-counting
intent that the v2 text left unenforced.

Event stream (`m3w1v3_world.txt`):

```
OBSERVE 52911 52950 52921
OBSERVE 52912 52950 52922
OBSERVE 52913 52950 52923
OBSERVE 52914 52950 52924
OBSERVE 52915 52950 52925
OBSERVE 52916 52950 52926
OBSERVE 52201 52600 52208
OBSERVE 52202 52600 52209
OBSERVE 52203 52600 52210
OBSERVE 52204 52600 52211
OBSERVE 52205 52600 52212
OBSERVE 52206 52600 52213
OBSERVE 52207 52600 52214
OBSERVE 52208 52600 52215
QUERY 52201 52601 52208
QUERY 52202 52601 52209
QUERY 52203 52601 52210
QUERY 52204 52601 52211
OBSERVE 52201 52600 52221
OBSERVE 52202 52600 52213
OBSERVE 52203 52600 52214
OBSERVE 52204 52600 52215
OBSERVE 52821 52850 52831
OBSERVE 52822 52850 52832
OBSERVE 52823 52850 52833
OBSERVE 52824 52850 52834
OBSERVE 52825 52850 52835
OBSERVE 52826 52850 52836
OBSERVE 52827 52850 52837
OBSERVE 52828 52850 52838
OBSERVE 52829 52850 52839
OBSERVE 52830 52850 52840
OBSERVE 52831 52850 52841
OBSERVE 52832 52850 52842
QUERY 52201 52601 52208
QUERY 52202 52601 52213
QUERY 52203 52601 52214
QUERY 52204 52601 52215
QUERY 52205 52601 52216
QUERY 52206 52601 52217
QUERY 52911 52950 52921
QUERY 52912 52950 52922
QUERY 52913 52950 52923
QUERY 52914 52950 52924
QUERY 52915 52950 52925
QUERY 52916 52950 52926
```

Phase 0: 6 interference facts. Phase 1: law L (+7) on 52201-52208.
Phase 1b: 4 promotion QUERYs on the novel relation 52601 (trial
promotes 1-hop verifying graphs via the oracle since each expected
value is the taught fact). Phase 2a: singleton noise on 52201 (+20,
never corrected). Phase 2b: systematic shift on 52202-52204 (+11,
never contradicted). Phase 3: 12 distractors. Probes: P1 singleton
(52201, expect 52208 = original law; a counting reviser rejects the
uncorrected singleton); P2-P4 systematic (expect +11:
52213/52214/52215); P5-P6 generalization on unseen 52205/52206
(expect +11: 52216/52217; requires the revision to generalize beyond
contradicted instances); P7-P12 interference.

Mechanism analysis: each contradiction triggers the single-schema
patch (last-write-wins). P1: patched to 52221, probe returns 52221
(FAIL: singleton incorporated). P2-P4: patched to +11 (PASS). P5-P6:
misses with no data path to +11 (ANSWER -2; FAIL: no generalization).
Interference: hits (PASS).

Predicted: K-S11v3 FAIL: (a) 3/3 PASS; (b) singleton FAIL; (c) 0/2
FAIL; (d) FAIL (no both-phase evidence-counted structure under the
tightened text); (e) 6/6 PASS. Strong-demand note carried over from
v1/v2: (c) requires law-level revision, so a competent per-instance
evidence-weighted reviser would fail it; this is deliberate and
documented so no future reader mistakes (c) for a test of revision in
general.

Material difference from FW5: FW5's bar REQUIRES last-write-wins
incorporation under eviction pressure; M3-W1v3's bar PUNISHES it
(singleton must be rejected) and adds generalization. Opposite demands
on the same operator: different properties probed, legitimate
adversarial design.

### 3.8 M3-W2: revision of a revision (recency-proof)

Calibrated v2 design carried forward with new ids (correction 2 as a
base invariant): distractor OBSERVEs on unrelated ids intervene between
the final contradiction and the bar probe, so the expected value
differs from the most recent observation; a global recency-echo policy
answers a distractor object and fails.

Event stream (`m3w2v3_world.txt`):

```
OBSERVE 53201 53601 53202
OBSERVE 53202 53602 53203
QUERY 53201 53609 53203
QUERY 53201 53609 53203
OBSERVE 53202 53602 53209
QUERY 53201 53609 53209
OBSERVE 53202 53602 53219
OBSERVE 53651 53660 53671
OBSERVE 53652 53660 53672
OBSERVE 53653 53660 53673
OBSERVE 53654 53660 53674
OBSERVE 53655 53660 53675
OBSERVE 53656 53660 53676
QUERY 53201 53609 53219
QUERY 52202 52601 52213
QUERY 52201 52601 52208
```

The promotion QUERY builds the 2-hop chain (trial promotes via the
oracle); contradiction 1 (53209) revises; contradiction 2 (53219) is
the bar event; 6 distractor OBSERVEs on unrelated ids follow; the bar
probe expects 53219 (latest evidence for the key, not the most recent
observation in the stream). Collateral: M3-W1 systematic (52213, hit
via patch) and singleton (52208 original law; the frozen mechanism
returns the incorporated noise 52221, recorded as a retention
deficit per the v2 observation).

Predicted: K-S12v3 FAIL (the frozen mechanism's silent no-op leaves
the stale 53209; validity probes 53203 and 53209 correct; collateral
1/2: systematic hit, singleton miss).

Separation note (carried over): K-S12v3 distinguishes global-recency
parroting from per-key revision. It does not by itself convict
per-key last-write-wins (a per-key latest responder passes this bar);
that operator is convicted by M3-W1's singleton and generalization
probes. The two worlds divide the labor by design.

Material difference: M3-W1 tests one revision per instance plus
generalization; M3-W2 tests sequential revisions of the same link.
FW5 tested single contradictions under eviction; double revision is a
different demand.

### 3.9 M3-W3: reverted revision blocks relearning (recency-proof)

Calibrated v2 design carried forward with new ids (correction 2 as a
base invariant): distractor OBSERVEs on unrelated ids intervene between
the final new-link teaches and the bar probe.

Event stream (`m3w3v3_world.txt`):

```
OBSERVE 53801 53901 53802
OBSERVE 53802 53902 53803
QUERY 53801 53909 53803
QUERY 53801 53909 53803
OBSERVE 53801 53901 53811
OBSERVE 53811 53902 53813
OBSERVE 53951 53960 53971
OBSERVE 53952 53960 53972
OBSERVE 53953 53960 53973
OBSERVE 53954 53960 53974
OBSERVE 53955 53960 53975
OBSERVE 53956 53960 53976
QUERY 53801 53909 53813
QUERY 53201 53609 53209
QUERY 52203 52601 52214
```

The promotion QUERY builds the 2-hop chain for (53801,53909). The
contradiction on the FIRST link (53811) breaks re-execution, so a
general reviser must unpromote and re-derive; the world then supplies
the new second link (53811->53813), making the current structure
53801->53811->53813. Six distractor OBSERVEs on unrelated ids follow.
The bar probe expects 53813. Collateral: W2 post-first-revision
(53209, hit via the surviving first revision) and W1 systematic
(52214, hit via patch).

Predicted: K-S13v3 FAIL (the frozen mechanism's revert leaves the
stale taught fact; probe returns 53803, not 53813; validity probes
correct; collateral 2/2).

Material difference: M3-W2 tests silent no-op on second revision;
M3-W3 tests a revision that actively fails (revert) and then vetoes
recovery. FW4/FW5 never produced a reverted revision.

## 4. Frozen kill bars K-S1v3 through K-S15v3

All bars are PASS/FAIL only; no partial credit. Process-bar failures
void the battery (re-seal and re-run); they are never scored as
mechanism verdicts.

- K-S1v3 (prereg ordering). PASS iff the SHA-256 of this file recorded
  by the committer was computed before any v3 world file or sealed
  envelope was created (filesystem mtime order) and the file is
  unmodified thereafter (hash re-verified after the battery).
  UNVERIFIABLE ORDERING voids this prereg.
- K-S2v3 (determinism). PASS iff, for each of the 3 blocks, the 3
  end-to-end runs from fresh state reproduce byte-identical
  per-world transcripts: for the 7 fixed worlds, sha256 equality of
  the transcript files across runs; for M2-W1, whose sealed envelope
  differs per run, immediate re-execution of run r with envelope_r
  reproduces the run-r transcript byte-identically; for M2-W2 (fresh
  state B), 3 fresh-state runs produce byte-identical transcripts.
- K-S3v3 (frozen binary). PASS iff `freeze_shim2_bin` hashes to
  `9217054c5af6dec057c4530c4de3ba246f521acc6df741d1989a4504acc72954`
  before each block run and after the battery, `tnn2.zag` still hashes
  to `a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd`,
  and `git status` shows zero modifications under the frozen
  cognition paths.
- K-S4v3 (seal integrity). PASS iff all world files, templates, truth
  files, and sealed envelopes match the manifest hashes recorded at
  generation, and grep of the exact v3 world id set over the frozen
  cognition sources finds zero matches.
- K-S5v3 (M1-W1 construction). PASS iff (a) at least 7 of the 8
  Q-then-P composition probes are correct; (b) all 4 decoy probes
  return the taught values (50902, 50901, 50904, 50903); (c) the state
  inspector reports a persistent structure whose licensed evidence
  includes at least one P-demo observation (from the 50201/50202
  block) and at least one Q-demo observation (from the 50203/50204
  block). Representation-neutral: no MAP, DEP, or SETREG vocabulary
  appears in this bar. All three required.
- K-S6v3 (M1-W2 reversal). PASS iff at least 3 of the 4 backward probes
  are correct. Validity: both forward engagement probes correct, else
  WORLD-INVALID.
- K-S7v3 (M1-W3 convergent step). PASS iff at least 2 of the 3
  convergent-composition probes are correct. Validity: engagement probe
  correct, else WORLD-INVALID.
- K-S8v3 (M2-W1 calibration, sealed mapping). PASS iff (a) the
  engagement check passes (at least one INQ ACT after a miss on a
  hidden key); (b) at least 6 of the 8 inquiry-phase ACTs route to the
  sealed truthful informant A (the 2-explore/6-exploit intended demand,
  section 3.4); (c) at most 1 inquiry-phase ACT routes to the sealed
  flattery informant C; (d) at least 3 of the 4 final hidden probes are
  correct; (e) inquiry-phase ACTs do not exceed the budget of 8. All
  five required. Roles are resolved through the opened envelopes after
  the runs; no hardcoded CHOICE integers appear in this bar.
- K-S9v3 (M2-W2 resolution, vocabulary-neutral, fresh-state baseline).
  PASS iff the post-resolution ACT equals the mechanism's declared null
  action N, where N is the action emitted by the baseline ACT in the
  fresh-state (state B) M2-W2 run, which occurs after a hit with no
  guide in state. Validity: the pre-resolution ACT differs from N, else
  WORLD-INVALID (an unengaged world is not a pass). Additionally, if the
  baseline ACT does not occur guide-free (verified by construction:
  fresh state B, baseline before the first miss), the run is
  WORLD-INVALID.
- K-S10v3 (M2-W3 content, vocabulary-neutral). PASS iff the three
  episode actions are pairwise distinct and each differs from the
  declared null action N (measured in M2-W2's fresh-state baseline,
  carried as a parameter). Validity: all three miss QUERYs yield the
  learner's own miss response M (recorded from the first inquiry-phase
  miss in M2-W1), else WORLD-INVALID.
- K-S11v3 (M3-W1 discrimination, tightened white-box bar). PASS iff
  (a) at least 2 of the 3 systematic probes are correct; (b) the
  singleton probe is correct (52208, original law); (c) at least 1 of
  the 2 generalization probes is correct; (d) the inspector reports a
  persistent structure whose current answer for the revised relation
  is a post-contradiction value (52213, 52214, or 52215) AND whose
  licensed evidence includes at least one original-phase observation
  (from the 52201-52208 +7 teaches) AND at least one systematic
  contradiction-phase observation (from the 52202-52204 +11 teaches:
  (52202,52600,52213), (52203,52600,52214), (52204,52600,52215)).
  Representation-neutral: no SETREG or MAP vocabulary appears in this
  bar. This tightening (both-phase evidence) enforces the
  evidence-counting intent that the v2 text left unenforced. (e) all 6
  interference probes are correct. All five required.
- K-S12v3 (M3-W2 double revision, recency-proof). PASS iff the
  post-second-contradiction probe returns 53219, with at least one
  distractor OBSERVE on an unrelated id intervening between the final
  contradiction OBSERVE and the bar probe (satisfied by construction;
  verified by the scorer). Validity: the promotion probe (53203) and
  the post-first-revision probe (53209) are correct, else
  WORLD-INVALID.
- K-S13v3 (M3-W3 revert, recency-proof). PASS iff the post-revert
  probe returns 53813, with at least one distractor OBSERVE on an
  unrelated id intervening between the final new-link teach and the
  bar probe. Validity: the promotion/engagement probes return 53803,
  else WORLD-INVALID.
- K-S14v3 (retention). PASS iff at least 75 percent of all collateral
  and engagement probes across the battery (12 total) return their
  prereg-expected values. Prereg expectations: M1-W2v3 2/2 taught
  hits; M1-W3v3 2/2 MAP hits; M2-W2v3 2/2 miss-response engagement;
  M2-W3v3 2/2 calibration-truth hits; M3-W2v3 systematic hit +
  singleton original-law (predicted: systematic hit, singleton
  returns incorporated noise 52221, per the v2 observation);
  M3-W3v3 2/2 hits. Predicted total: 11/12 (91.7 percent).
- K-S15v3 (no-leak audit). PASS iff the scorer reports zero correct
  ANSWERs on novel-key probes whose value coincides with a taught
  triple from a different v3 world, and the K-S4v3 id-set grep is
  clean.

### 4.1 Predicted bar outcomes for the frozen mechanisms (recorded before execution)

K-S1v3, K-S2v3, K-S3v3, K-S4v3, K-S14v3, K-S15v3: predicted PASS
(process bars). K-S5v3: predicted FAIL (0/8 composition; decoy (b)
predicted 4/4 PASS under the faithful-retrieval expectation; (c)
FAIL). K-S6v3: predicted FAIL (0/4 backward). K-S7v3: predicted FAIL
(0/3). K-S8v3: predicted FAIL ((b) 0 percent to sealed-A, (d) 0/4
hidden). K-S9v3: predicted FAIL (N=0, pre=30, post=30 stale).
K-S10v3: predicted FAIL (constant action three times). K-S11v3:
predicted FAIL ((b) singleton incorporated, (c) 0/2 generalization;
(a), (e) predicted PASS; (d) FAIL under the tightened text).
K-S12v3: predicted FAIL (stale 53209, not 53219). K-S13v3: predicted
FAIL (stale 53803, not 53813).

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

Control definitions (v3 ids; same policies as v2):

- M1-W1: D = per-key latest-observation responder (memorizer; novel
  subjects yield the miss response). C = symbolic composer: extracts
  the per-relation mapping from the demo OBSERVEs and emits Q-then-P
  in step order on novel subjects. The C control also emits a
  synthetic structure report satisfying K-S5v3(c) (evidence from both
  demo blocks).
- M1-W2: D = forward-only responder (answers forward probes from
  taught facts; backward probes yield the miss response). C =
  bidirectional responder (builds a reverse index; answers backward
  probes).
- M1-W3: D = per-key latest-observation responder. C = convergent-step
  composer (recognizes the shared last step; composes on the novel
  subject).
- M2-W1: D suite = three constant policies (always emit 1, always emit
  2, always emit 3). Gate: per run, at least 2 of the 3 must FAIL
  K-S8v3 (exactly the constant aligned with the sealed truthful
  channel may pass). C = calibrate-then-exploit: emits 1, 2, 3 across
  the 12 calibration ACTs, identifies the emitted value whose
  informant responses always match the revealed truths, and exploits
  that channel for all 8 inquiry ACTs. Must PASS K-S8v3 on all 3 runs.
- M2-W2: D1 = constant-action policy (one fixed action every ACT);
  D2 = stale-action policy (repeats the pre-resolution action after
  resolution). Neither may pass K-S9v3 (run on the fresh-state
  configuration). C = miss/hit responder (emits a guide action on
  miss, the measured null action on hit). Must PASS.
- M2-W3: D = constant-action policy. C = per-episode distinct actions.
  C must PASS K-S10v3; D must FAIL it.
- M3-W1: D = per-key last-write responder. Must FAIL K-S11v3 (via the
  singleton and generalization probes). C = evidence-counted reviser
  (adopts a change only after at least 2 consistent observations;
  rejects the uncorrected singleton; applies the observed shift law to
  unseen subjects; emits a synthetic structure report satisfying the
  tightened K-S11v3(d): post-contradiction answer with both-phase
  evidence). Must PASS.
- M3-W2: D = global-recency responder (answers the object of the most
  recent OBSERVE in the whole stream). Must FAIL K-S12v3 (answers a
  distractor object). C = per-key latest responder. Must PASS.
  Documented separation: this bar isolates global-recency parroting
  from per-key revision; per-key last-write-wins is convicted by
  M3-W1, not here.
- M3-W3: D = global-recency responder. Must FAIL K-S13v3. C =
  unpromote-and-rederive responder (on contradiction of a link in a
  derived chain, drops the derived fact and re-derives the 2-hop
  structure from current observations). Must PASS.

### 4.3 Diagnostics (informational only; never part of any kill bar)

- D-WB1 (M1-W1): whether a MAP/DEP-structured node with both demo
  blocks exists. Informational.
- D-WB2 (M3-W1): whether a SETREG-literal node exists in the live
  graph. Informational.
- D-CAUT (M2-W1): cautious re-verification signature: (d) at least 3/4
  probes correct AND fewer than 6 inquiry ACTs to sealed-A AND zero
  ACTs to sealed-C AND a majority of the remaining ACTs to sealed-B.
- D-IG (M2-W1): count of inquiry-phase ACTs routed to sealed-A
  (information-gain diagnostic).
- D-CONF (M1-W1): whether composition answers on novel instances
  follow the majority structure despite the noisy decoy
  (informational on the abstraction vs faithful-retrieval tension).

## 5. Execution protocol and tools

### 5.1 Tools (all pure Zag, pinned znc; built after this prereg freezes)

- `v3_worldgen.zag`: generates the 7 fixed world files and the M2-W1
  template from sections 3.1-3.3 and 3.5-3.9; generates the 3 sealed
  envelopes for M2-W1 (per-run permutation pi_r drawn from committed
  seed 20261002; informant tables per section 3.4); writes
  `WORLD_MANIFEST_V3.sha256` covering world files, template, truth
  files, and envelope hashes (envelope contents stay sealed).
- `v3_sealed_score.zag`: argv [worldfile, transcript]. Parses QUERY
  (s,r,e) lines and ANSWER (s,r,v) lines 1:1 in order; prints
  per-probe PASS/FAIL and summary counts; lists CHOICE values in
  order; verifies distractor-intervention requirements for K-S12v3
  and K-S13v3.
- `v3_score_m2w1.zag`: argv [transcript, driverlog, envelope]. Opens
  the envelope after the run; checks K-S8v3 sub-bars with roles
  resolved through pi_r; computes D-CAUT and D-IG.
- `v3_inspect_state.zag`: argv [state.bin, worldfile]. Reports
  persistent structures in representation-neutral terms: for each
  persistent structure, its current answer value and the set of source
  observation facts (s,r,o triples from the world's OBSERVE stream)
  reachable as its licensed evidence.
- `v3_struct_check.zag`: argv [inspector_report, check]. check=C5v3
  implements K-S5v3(c); check=D11v3 implements the tightened
  K-S11v3(d) (post-contradiction answer AND original-phase AND
  systematic-contradiction-phase evidence).
- `v3_m2w1_driver.zag`: the interactive M2-W1 driver (same step
  program as v2, with v3 ids); plus a thin mechanical shell loop.
- `v3_controls.zag`: implements the section 4.2 control policies as
  driver-level responders; prints per-control PASS/FAIL against each
  world's mechanism bar; writes synthetic structure reports where
  required.
- `v3_audit_noleak.zag`: implements K-S15v3; "novel-key" is
  subject-novel (never observed as a subject in any v3 world).

### 5.2 Block driver (deterministic shell)

M1 block per run: remove any prior state.bin; run W1->W2->W3 in order
via `freeze_shim2_bin <world> <state.bin>` (exit 0 required), saving
transcripts; run the inspector on the final state once per block run.
M3 block per run: same, W1->W2->W3. M2 block per run: fresh state A:
run M2-W1 via the interactive driver with envelope_r (driver log
saved); then run M2-W3 on state A. Fresh state B (separate file, never
chained from A): run M2-W2; N is recorded as a measured parameter from
this run and carried to the M2-W3 scorer. Determinism per K-S2v3.
Shim hash verified before each block and after the battery; tnn2.zag
hash verified after the battery (K-S3v3).

### 5.3 Anti-smuggling and manifest

At generation: sha256 manifest of all world/template/truth/envelope
files (envelope contents hashed but sealed). Before execution: grep
the exact v3 world id set in the frozen cognition sources (K-S4v3).
Hash re-verification of the shim binary before each block run and
after the battery (K-S3v3).

## 6. Sealing protocol

1. Roles. WORLDGEN builds world files, envelopes, and the manifest.
   SCORER builds the scoring and inspection tools from this prereg.
   EXECUTOR runs the blocks. No role modifies mechanism source; no
   role edits this prereg after freeze. (One worker may play all
   three roles sequentially; the ordering constraint is what matters:
   prereg frozen before worlds, worlds sealed before runs, envelopes
   opened only post-run.)
2. Adversary independence. The worker attests in NAMECHECK.md Step 0:
   (i) it has not authored mechanism-build or mechanism-repair code in
   the previous two waves; (ii) it may read the frozen mechanism
   source for adversarial design; (iii) it writes only inside its wave
   lane directory. The sealed envelopes are generated by the worldgen
   program alone; no run sees envelope contents before completion.
3. Freeze ordering. This prereg is committed alone and its SHA-256
   recorded. World files and envelopes are created only after that
   recorded freeze (K-S1v3 verifies hash plus filesystem mtime
   ordering). UNVERIFIABLE ORDERING voids this prereg.
4. Sealed envelopes (M2-W1). Three envelopes, one per run, each
   containing pi_r and the informant response tables. Envelope hashes
   are committed in the world manifest before any run. Envelopes are
   opened by the scorer only after all runs complete. The learner
   never sees pi_r; it observes only its own emitted CHOICE values
   and the resulting OBSERVE responses.
5. No post-freeze amendments to sealed files. Any defect found after
   world generation makes the affected world WORLD-VOID; a
   replacement requires a new sealed world under a new prereg section,
   never an edit to the sealed files. A defect in EXECUTION PROTOCOL
   (not world content) may be repaired by a frozen amendment with a
   fresh-state re-run, exactly per the v2 precedent (AMENDMENT_M2W2).
6. Determinism and manifest discipline per section 5.

## 7. Verdict rules and what a run on the three TNN-2 mechanisms establishes

Verdict rules:

- M1 SURVIVES-SEALED iff K-S5v3 and K-S6v3 and K-S7v3 all PASS; else
  M1 FAILS (kill evidence: the failed sub-bars).
- M2 SURVIVES-SEALED iff K-S8v3 and K-S9v3 and K-S10v3 all PASS; else
  M2 FAILS.
- M3 SURVIVES-SEALED iff K-S11v3 and K-S12v3 and K-S13v3 all PASS; else
  M3 FAILS.
- Any process-bar (K-S1v3..K-S4v3, K-S14v3, K-S15v3) failure VOIDs the
  battery; a void battery is re-sealed and re-run, never interpreted.
- Any calibration-gate (G-DEP/G-COMP) failure VOIDs the affected world
  as a battery defect; no mechanism verdict is drawn from a void world.
  There is no partial-generality verdict.

What a v3 run on the three frozen TNN-2 mechanisms establishes and
does not establish:

- The three v1/v2 kills STAND and are not re-litigated here. M1: no
  procedure abstraction (on calibrated bars). M2: constant inquiry
  action, no informant discrimination, no resolution transition (on
  calibrated bars). M3: last-write-wins patching, silent no-op on
  second contradiction, revert veto on relearning (on calibrated bars
  plus frozen-binary learner-state evidence). The v3 battery is a
  battery-design instrument carrying the six corrections forward, not
  a mechanism rescue.
- Expected result: the mechanisms FAIL the v3 bars with the predicted
  degenerate signatures (section 4.1). If observed, the v3 battery
  PASSES its validation: it convicts known degeneracy through
  calibrated bars on fresh world instances.
- If a mechanism PASSES a v3 bar it failed in v1/v2, the v3 battery
  FAILS its validation on that world: this is a battery defect, not a
  mechanism vindication. The corresponding kill evidence is REOPENED
  for defect analysis, and no mechanism verdict is upgraded.
- The v3 battery must be able to acquit genuine competence: the
  competent controls (section 4.2) demonstrate that every bar is
  passable by a correct policy, and the degenerate controls
  demonstrate that every bar is impassable by the degenerate policies
  it targets.

## 8. Criterion 0 status (binding; no L3 claim on any pass)

This battery tests whether frozen, researcher-authored mechanisms
generalize to fresh structures, and whether the battery itself is a
calibrated instrument. It does not test representational invention:

- C0-A (runtime-defined semantics): NOT MET. The exercised semantics
  are researcher-authored machinery in the frozen source.
- C0-B (open structural form): NOT MET. Every world's tested form is
  enumerable from its demonstrations before the run.
- C0-C (multiple unforeseen forms, independent post-freeze adversary):
  NOT MET. Nine worlds across three families, designed post-freeze,
  but the adversary role is played inside the same research loop.
- C0-D (cognitive reuse): NOT MET as a criterion. Collateral probes
  measure reuse-like behavior, explicitly insufficient for C0-D.

Consequence: no score on this battery, however high, may be described
as L3, L3-adjacent, or progress toward L3 without a separate
Criterion 0 case on independent evidence.

## 9. Traceability: the six corrections as v3 design invariants

1. M2-W1 sealed mapping (correction 1): per-run sealed permutation
   pi_r from committed seed 20261002 (section 3.4); K-S8v3(b)(c)
   scored against the opened envelopes with no hardcoded integers;
   G-DEP requires at least 2 of the 3 constant policies to fail per
   run; D-IG scores the information-gain alternative directly.
2. Recency confound (correction 2): 6 distractor OBSERVEs on unrelated
   ids between the final contradiction (M3-W2) or final new-link
   teaches (M3-W3) and the bar probe; K-S12v3/K-S13v3 require the
   expected value to differ from the most recent observation, with
   scorer-verified distractor intervention; G-DEP runs a
   global-recency responder that must fail both bars.
3. White-box coupling (correction 3), APPLIED COMPLETELY: K-S5v3(c)
   and K-S11v3(d) are representation-neutral (persistent structure,
   licensed evidence sets, current answer values). K-S11v3(d) is
   additionally TIGHTENED relative to v2: the v2 text ("licensed
   evidence includes at least one contradiction-phase observation")
   was satisfied by structures carrying only contradiction-phase
   teaches, which is looser than the evidence-counting intent (v2
   validation prediction miss 1). The v3 text requires BOTH
   original-phase AND systematic-contradiction-phase licensed
   evidence. The v1 MAP/DEP/SETREG checks survive only as diagnostics
   D-WB1 and D-WB2.
4. Cross-world consistency (correction 4): K-S5v3(b) decoy probes and
   the M1-W2 collateral probes both expect the taught values; M2-W2's
   engagement probes expect the miss response on fresh state (the
   retention claim across the state-B break is not made); no two bars
   demand different answers to the identical triple from one learner
   trajectory.
5. K-S8 tightness (correction 5): the 2-explore/6-exploit budget is
   documented as the intended demand (section 3.4); the calibration
   phase supplies 12 exploratory ACTs against a run-constant sealed
   mapping so identification is feasible; D-CAUT distinguishes
   cautious re-verification from flattery-seeking or collapse.
6. Vocabulary-neutral validity (correction 6): K-S9v3 and K-S10v3
   reference the mechanism's own declared null action N and miss
   response M, measured in-block (N from the fresh-state M2-W2
   baseline, M from M2-W1), instead of hardcoded integers; M2-W1
   roles are resolved through sealed envelopes rather than a fixed
   CHOICE table.

## 10. What a FAIL means

Per the standing no-patch-treadmill rule, a mechanism FAIL on v3 is
corroboration of the standing v1/v2 kills through calibrated bars on
fresh instances, not a request for a patch. A battery-validation FAIL
(a world VOID by calibration gates, or a mechanism PASS on a bar it
failed in v1/v2) is evidence about the battery's design, not about the
mechanisms; it is recorded as a battery defect with the void world's
evidence preserved, and any replacement world is sealed under a new
prereg section. Benchmark-specific handlers and per-world opcodes are
rejected in advance.
