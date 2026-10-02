# PREREG_BATTERY_E9: Fresh Sealed Adversarial Battery on TNN-2's Three New Mechanisms (wave-20261002-0221pdt)

**Status:** PREREG-FROZEN (design only; no world files generated, no runs
executed, no implementation built at freeze time). This document is frozen
by SHA-256 before any battery artifact exists (see E-K1). The freeze commit
contains this file and NAMECHECK.md only; no .zag, .sh, .txt, or binary.

**Wave:** wave-20261002-0221pdt, lane BATTERY.
**Date:** 2026-10-02.
**Battery name:** E9 (ninth sealed battery generation; first built under the
six triviality-review corrections).

## 0. Step 0 (toolchain guard)

Recorded in NAMECHECK.md Step 0: safebin activated,
`which python3` prints nothing, pinned znc from safebin. All programs in
this battery are Zag compiled with the pinned znc. Shell (safebin
bash/awk/grep) is used only for byte checks, file transport, hash
manifests, and the deterministic interactive driver loop; all scoring,
world-generation logic, and state inspection is pure Zag.

## 1. Freeze record (read-only for this battery)

TNN-2 mechanism source (frozen):

- File: `docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag`
- SHA-256: `a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd`
  (re-verified by this worker before writing this prereg; matches the
  wave-20261001-1421pdt freeze record)

Sealed interface shim (frozen, zero-cognition transport):

- File: `docs/lab/research-lead/overnight-20260928/core_freeze_tnn2_shim/freeze_shim2.zag`
- Binary `core_freeze_tnn2_shim/freeze_shim2_bin`
  SHA-256: `9217054c5af6dec057c4530c4de3ba246f521acc6df741d1989a4504acc72954`
  (re-verified; matches)
- Invocation: `freeze_shim2_bin <world.txt> <state.bin>`
- Protocol: `OBSERVE s r o` -> `OBSERVED s r o`; `QUERY s r expected` ->
  `ANSWER s r v` (ev_query with flags=0: full trial loop, then bootstrap);
  `ACT` -> `CHOICE v`. Miss sentinel -2 passes through unchanged.
  State file is exactly 110656 bytes and persists across invocations.

Compiler: `src/tools/toolchain/znc_linux_x86_64_abed8aa1`
SHA-256: `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`
(re-verified; matches the sealed freeze evaluation record).

The three mechanisms under test (all inside the frozen tnn2.zag):

- (M1) runtime executable-graph construction: `t2_trial` miss policy
  (propose/execute/verify/promote over the 4-op ISA MOVE/BRANCHEQ/INC/DEC).
  On a miss it gathers BFS data paths (up to 4 hops), assembles chain,
  sum, and count graphs, verifies each against the QUERY's expected
  value (oracle), and promotes the first verifier. Fallback: invariant
  relation bootstrap (needs 3+ recent facts on the relation with
  identical object). Known strengths: forward replay of demonstrated
  linear procedures on novel instances (FW2), forward multi-hop
  composition (FW1). Known gaps (old battery): novel composition,
  backward traversal, shared-step composition.
- (M2) learner-originated uncertainty guiding action: `miss_inquire`
  (UNCERTAINTY node plus POLICY_ROOT-linked guide) feeding `ev_act`.
  Frozen behavior: ACT emits the guide's action value (30) iff some
  live guide's subject sits in the 4-deep context ring, else 0. Guides
  are never superseded or retired. Known strengths: guide-presence
  gating (0 vs 30) works; FW6 literal-choice contract passed. Known
  gaps (old battery): no informant discrimination, no guide retirement,
  constant action content.
- (M3) counterexample-driven revision: `revise_on_contradict` /
  `t2_revise_graph` (single-schema literal patch with re-execution
  check; revert on failure). Known strengths: first contradiction of a
  terminal chain link revises correctly. Known gaps (old battery):
  last-write-wins with no evidence counting, silent no-op on second
  contradiction of the same link (stale DEP lookup), revert vetoes
  relearning.

## 2. The six triviality-review corrections and how E9 implements each

From `docs/lab/rsi/runs/wave-20261001-1721pdt/TRIVIALITY/TRIVIALITY_REVIEW.md`
section 6. Each correction is cited and its E9 implementation is given.
None of these is a mechanism repair.

**Correction 1 (M2-W1 informant mapping): seal the informant to CHOICE
mapping.** E9 implementation: M2-E1 maps CHOICE 1/2/3 to informants
{A,B,C} via a sealed permutation PI. PI is NOT in this prereg. After
this prereg freezes, PI = PERM_TABLE[first_byte(sha256(this file)) mod 6],
computed once, recorded in WORLD_MANIFEST.sha256, and used identically
for all 3 runs (per-run PI would break the E-K2 byte-identity bar, so E9
uses one sealed PI for the battery; the anti-constant protection comes
from sub-bar (f), which defeats every constant policy for every PI, see
section 5.4). PERM_TABLE (CHOICE -> informant), public:
0: 1->A 2->B 3->C | 1: 1->A 2->C 3->B | 2: 1->B 2->A 3->C |
3: 1->B 2->C 3->A | 4: 1->C 2->A 3->B | 5: 1->C 2->B 3->A.

**Correction 2 (M3-W2/W3 recency confound): distractor OBSERVEs between
the final contradiction and the bar probe.** E9 implementation: EVERY
M3 bar probe is preceded by 4 distractor OBSERVEs on unrelated ids, so
the expected value differs from the most recent observation. The D1
(recency-echo) degenerate walk in each world spec verifies the bar
fails for a parrot. M3-E1 additionally places 2 distractors between its
correct-back OBSERVE and its P2 probe.

**Correction 3 (white-box coupling): restate or demote.** E9
implementation: E9 has ZERO white-box bars. Every bar is transcript-only
(black-box). The state inspector runs as a diagnostic in the results,
never as a bar condition. No bar names MAP, DEP, SETREG, or any
internal representation.

**Correction 4 (cross-world inconsistency): consistent expectations.**
E9 implementation: (a) collateral probes always expect originally-taught
values; (b) no contradicted triple is ever re-probed in a later world
of the block; (c) within M3-E1, the noise and correct-back phases keep
P1/P2 expectations identical (55103), so one learner trajectory faces
one consistent truth per triple.

**Correction 5 (K-S8(b) tightness): document the explore budget.** E9
implementation: M2-E1's calibration phase CAN support informant
identification (each informant answer is followed by the truth OBSERVE;
6 keys suffice to identify A with 2-3 explorations). The 6/8 hidden-phase
bar therefore encodes explore-then-exploit as the INTENDED demand, with
2 deviations allowed for cautious re-verification. Sub-bar (f) requires
at least 2 distinct CHOICEs across the 6 calibration ACTs.

**Correction 6 (vocabulary decoupling): no hardcoded action integers.**
E9 implementation: M2-E1 opens with a VOCAB phase on fresh state: ACT
with no guides records NULL_ACT; a forced miss followed by ACT records
INQ_ACT. All M2 bars reference NULL_ACT/INQ_ACT, never 0/30. M2-E2/E3
re-measure both vocabularies in situ (validity control ACT and
post-resolution ACT). The driver maps CHOICE to informants via sealed
PI, not via a prereg-fixed 1->A table.

## 3. Battery scope and global constraints

Nine sealed worlds, three per mechanism. FW1-FW9 is a REGRESSION /
TARGETED-REPAIR battery for TNN-2 and can never establish generality or
L3; no world here is a FW1-FW9 world or a trivial variant of one (each
world's "material difference" note explains the separation). Worlds are
also materially different from the wave-20261001-1421pdt sealed battery
(worlds W1/W2/W3 of that battery are cited per world as the nearest
neighbor and the structural difference is stated).

Global constraints:

- Event streams use integer ids only. No natural language, no task
  labels, no family identifiers.
- Id block 50000-59999 for the whole battery, disjoint from FW1-FW9
  (30000-39999) and from the 1421pdt battery (40000-49999), and disjoint
  across worlds except intentional within-block collateral probes.
- Sub-blocks: M1 50000-51999 (E1 50000-50699, E2 50700-51399,
  E3 51400-51999); M2 52000-54999 (E1 52000-53999, E2 54000-54499,
  E3 54500-54999); M3 55000-57999 (E1 55000-55999, E2 56000-56999,
  E3 57000-57999).
- Worlds run in three blocks (M1: E1->E2->E3; M2: E1->E2->E3;
  M3: E1->E2->E3) with persistent learner state carried across worlds
  within a block (same state.bin chain). Each block starts from fresh
  state. Worlds E2 and E3 of each block carry 2 collateral probes from
  earlier worlds of the block (taught values only, per correction 4).
- The `expected` field on QUERY lines is the grader's truth and is
  passed to `ev_query` as the trial-loop oracle (documented frozen
  behavior). Bars are oracle-proofed: every bar-critical probe has no
  data path from the probed subject to its expected value (verified in
  each world spec by a mechanism walk), or the expected value is the
  taught fact. The oracle lets the trial loop verify; it cannot invent
  a path that does not exist.
- No harness behavior depends on learner internals; all driver mappings
  are fixed in this prereg (plus sealed PI) and mechanical.
- Anti-smuggling: before execution, the frozen cognition source is
  grepped for id tokens in 50000-59999; any match makes the affected
  world WORLD-INVALID (the world's fault), voiding the battery until a
  replacement is sealed under amendment.
- Determinism: each block is run 3 times end to end from fresh state;
  per-world transcripts (and for M2-E1 the driver logs) must be
  byte-identical across the 3 runs (sha256 equality).
- Degenerate calibration: for every mechanism bar, section 5 gives a
  degenerate walk (D0 always -2/0, D1 recency-echo/constant-30,
  D2 last-write-wins/0, plus always-NULL/always-INQ for M2 and
  always-c/rotate for M2-E1) showing the trivial contestant does NOT
  pass. The walks are executed, not just asserted: `degen.zag`
  generates degenerate transcripts for the 8 static worlds and the
  scorer evaluates the bars on them.

## 4. Adversarial coverage requirement

At least one world per mechanism is adversarial to that mechanism's
KNOWN STRENGTH (not just its known gaps):

- M1: E1 embeds the demonstrated strength (forward 2-hop replay, which
  FW1/FW2 proved) as in-world engagement probes, then demands a runtime
  branch on a per-subject discriminator: the strength fires and is
  insufficient. E3 takes FW1's exact demand (forward chains) to depth 5,
  one past the 4-hop gather ceiling.
- M2: E2 attacks the working 0/30 presence gate itself: a live guide
  exists in learner state but its subject has left the 4-deep context
  ring, so the gate silences genuine uncertainty. E3 attacks inquiry
  thrift: the USE edge records the prior inquiry in learner state, but
  the frozen ACT re-fires identically.
- M3: E1 attacks the working first-revision path: the operator revises
  eagerly on a SINGLE uncorrected observation (noise), where a counting
  reviser would wait. E2 attacks revision completeness: a downstream
  MAP keeps licensing a superseded fact after the upstream revision.

## 5. World specifications

Notation: exact event streams. `QUERY s r e` carries grader truth `e`.
Predicted outcomes are recorded honestly before execution; predicted
FAILs are information, not battery defects. Each world lists: adversarial
intent, material difference, mechanism walk (why the frozen mechanism
behaves as predicted, including oracle-proofing), degenerate walks, and
the bar.

### 5.1 M1-E1: runtime branch on a per-subject discriminator (branch family)

Adversarial intent: the frozen trial loop replays linear chains but
cannot condition on runtime data. Two procedures P and Q are
demonstrated; a discriminator fact on each subject selects which
applies. Probes on novel subjects require choosing the branch. The
4-op ISA contains BRANCHEQ, so a genuine constructor could build the
conditional; the frozen trial loop cannot.

Material difference: FW2 replayed ONE demonstrated procedure (tested
form = demonstrated form). The 1421pdt M1-W1 composed two procedures
SEQUENTIALLY (P-then-Q); E1 SELECTS between two procedures by a runtime
discriminator (branch topology, not sequential composition). Nearest
neighbor is M1-W1; the difference is selection vs sequencing.

Event stream (`m1e1_world.txt`):

```
OBSERVE 50101 50500 50501
OBSERVE 50101 50510 50801
OBSERVE 50801 50511 50802
OBSERVE 50102 50500 50501
OBSERVE 50102 50510 50801
OBSERVE 50801 50511 50802
OBSERVE 50103 50500 50502
OBSERVE 50103 50520 50811
OBSERVE 50811 50521 50812
OBSERVE 50104 50500 50502
OBSERVE 50104 50520 50811
OBSERVE 50811 50521 50812
OBSERVE 50105 50500 50501
OBSERVE 50106 50500 50501
OBSERVE 50107 50500 50502
OBSERVE 50108 50500 50502
QUERY 50101 50509 50802
QUERY 50103 50509 50812
OBSERVE 50901 50900 50911
OBSERVE 50902 50900 50912
OBSERVE 50903 50900 50913
OBSERVE 50904 50900 50914
QUERY 50105 50509 50802
QUERY 50106 50509 50802
QUERY 50107 50509 50812
QUERY 50108 50509 50812
```

P = 2-hop chain on (50510,50511), demonstrated on type-A subjects
50101/50102 (discriminator 50501). Q = 2-hop chain on (50520,50521),
demonstrated on type-B subjects 50103/50104 (discriminator 50502).
Probe relation 50509 is novel. Engagement probes (idx0,1) run the
demonstrated forward composition (the known strength). Branch probes
(idx2-5) on novel subjects 50105-50108 require the P/Q choice.

Mechanism walk (frozen): engagement idx0: BFS from 50101 finds path
[50101,50801,50802] (len 3); k=2 chain verifies against oracle 50802;
promotes MAP; ANSWER 50802. idx1 likewise 50812. Branch probes: novel
subject 50105 has one fact (50105,50500,50501); BFS yields only
[50105,50501]; no path computes 50802 (1-hop gives 50501; count gives 1;
sum declined above 900); bootstrap on 50509 sees 2 facts with distinct
objects (below k=3 and not invariant). Miss -> ANSWER -2, guide created.
Oracle-proof: the expected value is unreachable from the subject's data;
the oracle cannot help. Predicted: idx0,1 PASS; idx2-5 ANSWER -2.

Degenerate walks: D0 (always -2, ACT 0): engagement idx0,1 get -2, so
HIT fails -> WORLD-INVALID (not a pass). D1 (recency-echo, ACT 30):
at idx0 the most recent OBSERVE is (50108,50500,50502) -> answers 50502,
wrong -> WORLD-INVALID. D2 (last-write per (s,r)): no (50101,50509)
OBSERVE exists -> -2 -> WORLD-INVALID. No degenerate passes E-K5.

### 5.2 M1-E2: cross-subject value join (join family)

Adversarial intent: the trial loop's entire search space is followable
data paths (BFS from the subject). The tested form (find the subject
sharing this subject's key value, return that subject's payload) is
provably not a data path: it requires a reverse value lookup the BFS
cannot express. A decoy followable 2-hop path is included so the
strength visibly fires (TRIAL tried/rejected counts) and still fails.

Material difference: 1421pdt M1-W1/W2/W3 and E1/E3 are all
intra-subject path problems (compose, reverse, share, branch, extend).
E2 is inter-subject: the answer lives on ANOTHER subject reachable only
by value equality, not by links. No FW world did joins.

Event stream (`m1e2_world.txt`):

```
OBSERVE 50201 50610 50651
OBSERVE 50201 50611 50652
OBSERVE 50202 50610 50651
OBSERVE 50202 50611 50654
OBSERVE 50203 50610 50661
OBSERVE 50203 50611 50662
OBSERVE 50204 50610 50661
OBSERVE 50204 50611 50664
OBSERVE 50205 50610 50671
OBSERVE 50205 50611 50672
OBSERVE 50206 50610 50671
OBSERVE 50206 50611 50674
OBSERVE 50207 50610 50681
OBSERVE 50207 50611 50682
OBSERVE 50208 50610 50681
OBSERVE 50208 50611 50684
OBSERVE 50201 50612 50655
OBSERVE 50655 50613 50656
QUERY 50201 50611 50652
QUERY 50203 50611 50662
OBSERVE 50911 50900 50921
OBSERVE 50912 50900 50922
OBSERVE 50913 50900 50923
OBSERVE 50914 50900 50924
QUERY 50201 50619 50654
QUERY 50203 50619 50664
QUERY 50205 50619 50674
QUERY 50207 50619 50684
QUERY 50101 50510 50801
QUERY 50103 50520 50811
```

Pairs share a key (50610 value); the probe (50619) on the first subject
of each pair expects the SECOND subject's payload. Decoy: followable
path 50201->50655->50656 (wrong value). Engagement (idx0,1) are direct
hits (intra-subject retrieval works). Collateral (idx6,7) from M1-E1
are taught-value hits.

Mechanism walk: engagement idx0,1 exact hits. Join probes: BFS from
50201 gives [50201,50651],[50201,50652],[50201,50655,50656]; the 2-hop
decoy verifies against oracle 50654 and is rejected (50656); 1-hop and
count candidates miss; sum declined; bootstrap on 50619 has no facts.
Miss -> -2. The TRIAL header tried/rejected counters will show the
decoy was genuinely tried: the strength fired and misfired. Predicted:
idx0,1 PASS; idx2-5 -2; idx6,7 PASS.

Degenerate walks: D0: engagement fails -> WORLD-INVALID. D1: at idx0
most recent OBSERVE is the decoy (50655,50613,50656) -> 50656, wrong ->
WORLD-INVALID. D2: no (50201,50611) OBSERVE... wait, (50201,50611,50652)
IS an OBSERVE (line 2), so D2 answers 50652 correctly on idx0; idx1:
(50203,50611,50662) observed -> 50662 correct; then bar probes: no
(50201,50619) OBSERVE -> -2 -> NEED fails (0/4). So D2 reaches scoring
and FAILS E-K6. No degenerate passes.

### 5.3 M1-E3: depth extrapolation to 5 hops (depth family)

Adversarial intent: FW1 proved forward 3-hop composition; the gather
BFS caps at 4 hops (paths of at most 5 nodes). E3 demonstrates 1-hop
and 2-hop chains, then probes 5-hop chains: the identical forward shape
at one depth beyond capacity. A constructor that learned "follow the
relation" iterates; the frozen trial loop cannot.

Material difference: FW1 tested 3-hop (passed). 1421pdt M1-W2 isolated
DIRECTION (backward) on the same 3-hop shape; E3 isolates DEPTH
(forward, 5-hop). Nearest neighbor is FW1 itself; the single changed
parameter is depth 3 -> 5.

Event stream (`m1e3_world.txt`):

```
OBSERVE 50301 51401 51451
OBSERVE 50302 51401 51452
OBSERVE 51452 51401 51453
OBSERVE 50303 51401 51461
OBSERVE 51461 51401 51462
OBSERVE 51462 51401 51463
OBSERVE 51463 51401 51464
OBSERVE 51464 51401 51465
OBSERVE 50304 51401 51471
OBSERVE 51471 51401 51472
OBSERVE 51472 51401 51473
OBSERVE 51473 51401 51474
OBSERVE 51474 51401 51475
OBSERVE 50305 51401 51481
OBSERVE 51481 51401 51482
OBSERVE 51482 51401 51483
OBSERVE 51483 51401 51484
OBSERVE 51484 51401 51485
QUERY 50301 51409 51451
QUERY 50302 51409 51453
OBSERVE 51901 51900 51911
OBSERVE 51902 51900 51912
OBSERVE 51903 51900 51913
OBSERVE 51904 51900 51914
QUERY 50303 51409 51465
QUERY 50304 51409 51475
QUERY 50305 51409 51485
QUERY 50201 50611 50652
QUERY 50203 50611 50662
```

Mechanism walk: engagement idx0 (1-hop: [50301,51451] -> 51451) and
idx1 (2-hop: [50302,51452,51453] -> 51453) promote and PASS. Bar probes:
longest gathered path has 5 nodes (4 hops), so the best chain candidate
yields 51464, not 51465; count yields 5; sum declined; bootstrap on
51409 sees 2 taught facts with distinct objects. Miss -> -2. Predicted:
idx0,1 PASS; idx2-4 -2; idx5,6 PASS.

Degenerate walks: D0: engagement fails -> WORLD-INVALID. D1: at idx0
most recent OBSERVE is (51484,51401,51485) -> 51485 wrong ->
WORLD-INVALID. D2: no (50301,51409) OBSERVE -> -2 -> WORLD-INVALID.
No degenerate passes E-K7.

### 5.4 M2-E1: informant selection under sealed permutation (selection family)

Adversarial intent: remove every fixed mapping the old battery leaked.
Informants A (truthful), B (noisy, fixed wrong table), C (flatterer:
always the seeded bias 52999, systematically wrong). CHOICE 1/2/3 maps
to informants via sealed PI (section 2, correction 1). The calibration
phase CAN support identification (each informant answer is followed by
the truth OBSERVE; 6 keys), so explore-then-exploit is the intended
demand (correction 5). The flattery trap is adversarial against
prior-agreement seeking rather than uncertainty reduction.

Material difference: 1421pdt M2-W1 had a FIXED prereg-documented mapping
(degenerate-passable by always-1) and a calibration phase that could not
support identification. E1 seals the mapping and makes calibration
informative. No FW world did informant selection.

Structure: VOCAB phase, bias seeds, calibration phase (6 keys; per key:
ACT, optional informant OBSERVE, truth OBSERVE, calibration QUERY),
hidden phase (4 keys; per key: miss QUERY probe, 2 ACTs with informant
responses, final QUERY probe; budget 8 ACTs). Interactive driver grows
the world from the template; driver log records
`ACT <CAL|INQ> <key> <choice> <NONE|A|B|C>`.

Template (`m2e1_template.txt`):

```
ACT
QUERY 52901 52900 52911
ACT
OBSERVE 52991 52990 52991
OBSERVE 52992 52990 52992
OBSERVE 52993 52990 52993
OBSERVE 52994 52990 52994
OBSERVE 52091 52500 52999
OBSERVE 52092 52500 52999
OBSERVE 52093 52500 52999
```

VOCAB: CHOICE#1 with no guides records NULL_ACT (frozen: 0, POLICY_ROOT
unset). QUERY (52901,52900,52911) is a true miss (no facts on 52901 or
rel 52900) -> guide created. CHOICE#2 records INQ_ACT (frozen: 30,
subject in ring). 4 flush OBSERVEs retire the vocab subject from the
ring (the guide persists; it never interferes because its subject never
re-enters the ring).

Driver (fixed, deterministic; PI embedded at generation):

- Calibration keys 52101-52106, truths 52201-52206. Per key:
  step "ACT" -> C; INF = PI(C) if C in {1,2,3} else NONE;
  log `ACT CAL <k> <C> <INF>`;
  if INF != NONE: step "OBSERVE <k> 52500 <ans>" with ans =
    truth (A), B-table (B), 52999 (C);
  step "OBSERVE <k> 52500 <truth>"; step "QUERY <k> 52500 <truth>".
- Hidden keys 52111-52114, truths 52211-52214. Per key:
  step "QUERY <k> 52500 <truth>" (miss probe);
  twice: step "ACT" -> C; INF as above; log `ACT INQ <k> <C> <INF>`;
    if INF != NONE: step "OBSERVE <k> 52500 <ans>";
  step "QUERY <k> 52500 <truth>" (final probe, scored).

B tables: calibration 52101->52291, 52102->52292, 52103->52293,
52104->52294, 52105->52295, 52106->52296; hidden 52111->52281,
52112->52282, 52113->52283, 52114->52284.

Mechanism walk (frozen): VOCAB gives NULL_ACT=0, INQ_ACT=30.
Calibration ACTs occur with no guides -> CHOICE 0 -> NONE (wasted).
Hidden miss QUERYs: novel keys, no data paths (bootstrap on 52500 sees
many facts with distinct objects, never invariant) -> guides created.
Hidden ACTs -> CHOICE 30 -> NONE (30 not in {1,2,3}). Final probes
-> -2. Predicted: (a) engagement PASS (8 INQ ACTs follow misses);
(b) 0/8 target A FAIL; (c) 0 target C PASS; (d) 0/4 FAIL; (e) 8 ACTs
within budget PASS; (f) calibration CHOICEs all 0 -> 1 distinct FAIL.
E-K8 FAIL.

Degenerate walks: always-c for c in {1,2,3}: sub-bar (f) fails (1
distinct CHOICE) for EVERY PI, so always-c cannot pass E-K8
deterministically. rotate-1,2,3: (f) passes but (b) gets at most 3/8
to A -> FAIL. A win-stay policy (repeat the calibration CHOICE whose
informant matched truth) is competent behavior, not degenerate. No
trivial contestant passes E-K8.

### 5.5 M2-E2: silenced inquiry under a live guide (gate-scope family)

Adversarial intent: the frozen ACT gate is context-ring membership, not
uncertainty. A guide exists in persistent learner state (genuine,
unresolved uncertainty), but its subject has been flushed from the
4-deep ring, so the mechanism stays silent. A competent
uncertainty-guided mechanism scans all live guides. The demand is
documented as strong: inquiry must be driven by the EXISTENCE of
unresolved uncertainty in learner state, not by incidental ring
occupancy.

Material difference: 1421pdt M2-W2 tested staleness AFTER resolution
with the subject IN the ring (expected silence). E2 tests the OPPOSITE:
genuine live uncertainty with the subject OUT of the ring (expected
inquiry). Opposite demands on the same gate; the pair brackets it.

Event stream (`m2e2_world.txt`):

```
QUERY 54101 54501 54111
OBSERVE 54201 54200 54211
OBSERVE 54202 54200 54212
OBSERVE 54203 54200 54213
OBSERVE 54204 54200 54214
ACT
QUERY 54102 54501 54112
ACT
OBSERVE 54101 54501 54111
OBSERVE 54205 54200 54215
OBSERVE 54206 54200 54216
OBSERVE 54207 54200 54217
OBSERVE 54208 54200 54218
ACT
QUERY 52091 52500 52999
QUERY 52092 52500 52999
```

QUERY (54101,54501,54111): true miss (fresh ids) -> guide(54101).
4 flush OBSERVEs (fresh subjects, plain teaches, no guides, no
contradictions). ACT#1 (bar (a)): ring holds 54204..54201; no live
guide subject in ring -> CHOICE NULL_ACT. Expected INQ_ACT.
QUERY (54102,54501,54112): miss -> guide(54102). ACT#2 (validity):
54102 in ring -> CHOICE INQ_ACT (re-measured in situ).
OBSERVE (54101,54501,54111): free resolution (exact teach, no
contradiction). 4 flush OBSERVEs. ACT#3 (bar (b)): nothing eligible
-> CHOICE NULL_ACT. Expected NULL_ACT (defeats always-INQ).
Collateral (idx2,3): bias seeds from M2-E1, taught values, hits.

Mechanism walk (frozen): ACT#1 -> 0 (NULL). ACT#2 -> 30 (INQ).
ACT#3 -> 0. Predicted: (a) 0 != INQ FAIL -> E-K9 FAIL; (b) PASS;
validity PASS; collateral PASS.

Degenerate walks: always-NULL: validity (CHOICE#2 == INQ) fails ->
WORLD-INVALID. always-INQ: (b) expects NULL, gets INQ -> FAIL. D0/D2
(ACT 0): validity fails -> WORLD-INVALID. D1 (ACT 30): (b) fails ->
FAIL; also HIT collateral fails (recency-echo gives distractor) ->
WORLD-INVALID. No degenerate passes E-K9.

### 5.6 M2-E3: duplicate-inquiry suppression (thrift family)

Adversarial intent: the frozen ACT re-fires identically while the guide
is ring-resident, although the learner state records the prior inquiry
(a USE edge is added to the guide on every ACT). A calibrated
uncertainty-guided mechanism suppresses repeat inquiry when no new
information arrived. Documented as strong-but-honest: the demand is
thrift, not retirement (the uncertainty is still live; nothing was
resolved).

Material difference: 1421pdt M2-W2 tested post-RESOLUTION staleness;
E3 tests post-INQUIRY duplication with the uncertainty still live.
1421pdt M2-W3 tested distinct actions across DIFFERENT uncertainties;
E3 tests same-vs-suppressed across REPEATED inquiry on one
uncertainty.

Event stream (`m2e3_world.txt`):

```
QUERY 54601 54651 54661
ACT
ACT
OBSERVE 54701 54700 54711
OBSERVE 54702 54700 54712
OBSERVE 54703 54700 54713
OBSERVE 54704 54700 54714
QUERY 54602 54652 54662
ACT
ACT
QUERY 54201 54200 54211
QUERY 54202 54200 54212
```

Episode 1: QUERY miss -> guide(54601). ACT#1 (validity): 54601 in ring
-> INQ_ACT. ACT#2 (bar): 54601 still in ring (ring is [-3,54601,..])
-> frozen re-fires INQ_ACT; expected NULL_ACT (already inquired, USE
edge on record, no new information). Episode 2 identical on 54602
(ACT#3 validity, ACT#4 bar). Collateral (idx2,3): M2-E2 distractors,
taught values, hits.

Mechanism walk (frozen): CHOICEs 30,30,30,30. Predicted: validity
PASS; bar 0/2 FAIL -> E-K10 FAIL; collateral PASS.

Degenerate walks: always-NULL: validity fails -> WORLD-INVALID.
always-INQ: validity passes, bar (expects NULL) fails -> FAIL.
No degenerate passes E-K10.

### 5.7 M3-E1: singleton noise at the licensing level (evidence-counting family)

Adversarial intent: the revision operator fires on EVERY contradiction
with no evidence counting. A single uncorrected contradictory
observation (noise) against a licensing fact should not move a counting
reviser; the frozen operator revises eagerly. Then the noise is
corrected back; a competent reviser is unaffected, while the frozen
mechanism is stuck (the W2 stale-DEP gap); P2 reuses that demand
honestly as a secondary probe.

Material difference: 1421pdt M3-W1 tested the singleton at the ANSWER
level (probe the contradicted instance). E1 tests it at the LICENSING
level (probe the MAP's composed answer after its evidence was singly
contradicted): the noise is one step removed from the probe. Nearest
neighbor is M3-W1; the difference is licensing-level vs answer-level
noise.

Event stream (`m3e1_world.txt`):

```
OBSERVE 55101 55501 55102
OBSERVE 55102 55502 55103
QUERY 55101 55509 55103
QUERY 55101 55509 55103
OBSERVE 55102 55502 55109
OBSERVE 55801 55800 55811
OBSERVE 55802 55800 55812
OBSERVE 55803 55800 55813
OBSERVE 55804 55800 55814
QUERY 55101 55509 55103
OBSERVE 55102 55502 55103
OBSERVE 55805 55800 55815
OBSERVE 55806 55800 55816
QUERY 55101 55509 55103
```

Promotion probes (idx0,1) build the 2-hop MAP (answer 55103).
Noise: single uncorrected contradiction of link 2 (55109), then 4
distractors (correction 2). P1 (idx2) expects 55103 (noise rejected).
Correct-back: (55102,55502,55103) restores the original; 2 more
distractors; P2 (idx3) expects 55103.

Mechanism walk (frozen): promotion -> MAP ans 55103. Noise triggers
revise_on_contradict: stale SETREG#2 found via DEP to the contradicted
fact; patched to 55109; re-execution succeeds (terminal link); MAP
ans=55109, taught fact (55101,55509,55109). P1 -> 55109, FAIL.
Correct-back contradicts the NEW fact node; the revised SETREG's DEP
points to the OLD fact node -> silent no-op (the W2 gap); MAP stays
55109. P2 -> 55109, FAIL. Predicted: idx0,1 PASS; idx2,3 FAIL.

Degenerate walks: D0: -2 everywhere; NEED fails. D1 (recency-echo):
idx0: most recent OBSERVE is (55102,55502,55103) -> 55103 PASS;
idx1: same -> PASS (validity met); idx2: most recent is distractor
55814 -> FAIL; idx3: most recent is distractor 55816 -> FAIL.
NEED 0/2 -> E-K11 FAIL. D2 (last-write per (s,r)): idx0: no
(55101,55509) OBSERVE -> -2 -> validity fails -> WORLD-INVALID.
No degenerate passes E-K11.

### 5.8 M3-E2: downstream propagation through stacked MAPs (propagation family)

Adversarial intent: revision does not propagate. MAP_B licenses MAP_A's
promoted answer fact; when MAP_A revises (contradiction of its
evidence), MAP_A's promoted fact is superseded and re-taught, but
MAP_B is never revisited: it keeps answering through a superseded
fact. A complete reviser re-derives downstream structures.

Material difference: 1421pdt M3-W1/W2/W3 each revised (or failed to
revise) a SINGLE MAP. E2 stacks two MAPs with a cross-MAP dependence:
the tested property is propagation, which no earlier world exercised.

Event stream (`m3e2_world.txt`):

```
OBSERVE 56101 56501 56102
OBSERVE 56102 56502 56103
OBSERVE 56103 56510 56104
QUERY 56101 56509 56103
QUERY 56101 56509 56103
QUERY 56101 56519 56104
OBSERVE 56102 56502 56113
QUERY 56101 56509 56113
OBSERVE 56113 56510 56114
OBSERVE 56801 56800 56811
OBSERVE 56802 56800 56812
OBSERVE 56803 56800 56813
OBSERVE 56804 56800 56814
QUERY 56101 56519 56114
QUERY 55801 55800 55811
QUERY 55802 55800 55812
```

MAP_A: 2-hop chain 56101->56102->56103, probe rel 56509, ans 56103
(idx0,1 validity). MAP_B: licensed by MAP_A's promoted fact
(56101,56509,56103) and (56103,56510,56104): the trial finds path
[56101,56103,56104] (the [56101,56102,56103] candidate is tried first
and rejected against oracle 56104), promotes MAP_B ans 56104 (idx2
validity). Contradiction of MAP_A's terminal link (56113): MAP_A
revises (terminal link, re-execution succeeds); its promoted fact is
CONed and (56101,56509,56113) taught; MAP_B untouched (no DEP to the
contradicted fact). New downstream link (56113,56510,56114) taught
(plain teach). 4 distractors (correction 2). Bar probe idx4
(56101,56519,56114): MAP_B's promoted fact (56101,56519,56104) is still
active -> exact hit 56104. Expected 56114 (recomputation through the
revised upstream). Collateral idx5,6: M3-E1 distractors, hits.

Mechanism walk (frozen): idx0,1 -> 56103; idx2 -> 56104; idx3 ->
56113; idx4 -> 56104 (stale), FAIL. Predicted E-K12 FAIL.

Degenerate walks: D0: -2; validity fails -> WORLD-INVALID. D1: idx0:
most recent OBSERVE (56103,56510,56104) -> 56104 != 56103 -> validity
fails -> WORLD-INVALID. D2: idx0: no (56101,56509) OBSERVE -> -2 ->
WORLD-INVALID. No degenerate passes E-K12.

### 5.9 M3-E3: success-then-revert across two links (compound-revision family)

Adversarial intent: compound of the W2 (sequential) and W3 (revert)
gaps on DIFFERENT links of one MAP: a terminal-link revision succeeds,
then a nonterminal-link contradiction reverts (the downstream guard
still expects the old intermediate). The bar demands the fully
recomputed answer; the frozen mechanism delivers the partially revised
one.

Material difference: 1421pdt M3-W2 contradicted the SAME link twice;
M3-W3 contradicted the FIRST link once and tested veto-after-revert.
E3 contradicts TWO DIFFERENT links in sequence (terminal then
nonterminal): the structure is success-then-revert, which neither
earlier world built.

Event stream (`m3e3_world.txt`):

```
OBSERVE 57101 57501 57102
OBSERVE 57102 57502 57103
QUERY 57101 57509 57103
QUERY 57101 57509 57103
OBSERVE 57102 57502 57113
QUERY 57101 57509 57113
OBSERVE 57112 57502 57123
OBSERVE 57101 57501 57112
OBSERVE 57801 57800 57811
OBSERVE 57802 57800 57812
OBSERVE 57803 57800 57813
OBSERVE 57804 57800 57814
QUERY 57101 57509 57123
QUERY 56801 56800 56811
QUERY 56802 56800 56812
```

Promotion (idx0,1): 2-hop MAP ans 57103. Terminal contradiction
(57113): revises cleanly (re-execution succeeds); idx2 validity ->
57113. New middle link (57112,57502,57123) taught (plain teach).
Nonterminal contradiction (57101,57501,57112): stale SETREG#1 found,
patched, re-execution fails (guard#2 expects 57102, sees 57112) ->
revert; MAP ans stays 57113. 4 distractors (correction 2). Bar probe
idx3 expects 57123 (full recomputation 57101->57112->57123). Frozen
-> 57113, FAIL. Collateral idx4,5: M3-E2 distractors, hits.

Mechanism walk (frozen): idx0,1 -> 57103; idx2 -> 57113; idx3 ->
57113, FAIL. Predicted E-K13 FAIL.

Degenerate walks: D0: validity fails -> WORLD-INVALID. D1: idx0:
most recent OBSERVE (57102,57502,57103) -> 57103 PASS; idx1: same
PASS; idx2: most recent (57102,57502,57113) -> 57113 PASS; idx3:
most recent distractor 57814 -> FAIL. NEED 0/1 -> E-K13 FAIL. D2:
idx0: no (57101,57509) OBSERVE -> -2 -> WORLD-INVALID. No degenerate
passes E-K13.

## 6. Frozen kill bars E-K1 through E-K15

All bars are PASS/FAIL only; no partial credit. Process-bar failures
void the battery (re-seal and re-run); they are never scored as
mechanism verdicts.

- E-K1 (prereg ordering). PASS iff the SHA-256 of this file recorded in
  SEALED_RESULTS.md was computed before any battery artifact
  (world/template/driver/scorer file) was created (filesystem mtime
  order) and the file is unmodified thereafter (hash re-verified after
  the battery). The freeze commit contains this file and NAMECHECK.md
  only.
- E-K2 (determinism). PASS iff, for each of the 3 blocks, the 3
  end-to-end runs produce byte-identical per-world transcripts
  (sha256 equality; for M2-E1 the grown world file plus driver log).
- E-K3 (frozen binary). PASS iff `freeze_shim2_bin` hashes to
  `9217054c5af6dec057c4530c4de3ba246f521acc6df741d1989a4504acc72954`
  before each block run and after the battery, `tnn2.zag` still hashes
  to `a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd`,
  and `git status` shows zero modifications under
  `docs/lab/research-lead/overnight-20260928/tnn2_build/` and
  `.../core_freeze_tnn2_shim/` cognition paths.
- E-K4 (seal integrity). PASS iff all world/template/truth/driver files
  match the manifest hashes recorded at generation, and `grep -r` over
  the frozen cognition sources finds zero tokens in 50000-59999.
- E-K5 (M1-E1 branch). PASS iff HIT 0,1 (engagement) and at least 3 of
  probes 2-5 correct. Validity: HIT fails -> WORLD-INVALID.
- E-K6 (M1-E2 join). PASS iff HIT 0,1 and at least 3 of probes 2-5
  correct. Validity: HIT fails -> WORLD-INVALID.
- E-K7 (M1-E3 depth). PASS iff HIT 0,1 and at least 2 of probes 2-4
  correct. Validity: HIT fails -> WORLD-INVALID.
- E-K8 (M2-E1 selection). PASS iff (a) at least one hidden key has an
  ACT after its miss probe; (b) at least 6 of the 8 hidden-phase ACTs
  target informant A (CHOICE == PI-inverse(A)); (c) at most 1
  hidden-phase ACT targets informant C; (d) at least 3 of the 4 final
  hidden probes correct; (e) hidden-phase ACTs <= 8; (f) at least 2
  distinct CHOICE values across the 6 calibration ACTs. All six
  required.
- E-K9 (M2-E2 gate scope). PASS iff CHOICE#1 == INQ_ACT (bar a),
  CHOICE#3 == NULL_ACT (bar b), HIT 2,3 (collateral). Validity:
  CHOICE#2 == INQ_ACT, else WORLD-INVALID. All required.
- E-K10 (M2-E3 thrift). PASS iff CHOICE#2 == NULL_ACT and
  CHOICE#4 == NULL_ACT (bar), HIT 4,5 (collateral). Validity:
  CHOICE#1 == INQ_ACT and CHOICE#3 == INQ_ACT, else WORLD-INVALID.
  All required.
- E-K11 (M3-E1 evidence counting). PASS iff HIT 0,1 (validity) and
  probes 2,3 both correct (P1: noise rejected; P2: correct-back
  stable). All required.
- E-K12 (M3-E2 propagation). PASS iff HIT 0,1,2,3 (validity) and probe
  4 correct (downstream recomputed). All required.
- E-K13 (M3-E3 compound revision). PASS iff HIT 0,1,2 (validity) and
  probe 3 correct (fully recomputed). All required.
- E-K14 (retention). PASS iff at least 75 percent of all collateral
  probes across the battery (12 total: M1 4, M2 4, M3 4) return their
  prereg-expected taught values.
- E-K15 (no-leak audit). PASS iff no bar-critical probe's (s,r)
  expected value coincides with an OBSERVE-taught triple for a
  different (s,r) in any world file (checked mechanically by the
  scorer), and the E-K4 grep is clean (recorded here separately).

### Predicted bar outcomes (recorded before execution)

E-K1, E-K2, E-K3, E-K4, E-K14, E-K15: predicted PASS (process bars).
E-K5: predicted FAIL (engagement 2/2 PASS; branch 0/4).
E-K6: predicted FAIL (engagement 2/2 PASS; join 0/4).
E-K7: predicted FAIL (engagement 2/2 PASS; depth 0/3).
E-K8: predicted FAIL ((a) PASS; (b) 0/8; (c) PASS; (d) 0/4; (e) PASS;
(f) FAIL).
E-K9: predicted FAIL (bar (a) 0 vs INQ; (b) PASS; validity PASS;
collateral PASS).
E-K10: predicted FAIL (validity PASS; bar 0/2; collateral PASS).
E-K11: predicted FAIL (validity PASS; P1 55109 not 55103; P2 55109).
E-K12: predicted FAIL (validity PASS; probe4 56104 not 56114).
E-K13: predicted FAIL (validity PASS; probe3 57113 not 57123).

## 7. Execution protocol and tools

### 7.1 Tools (all pure Zag, pinned znc; built AFTER this prereg freezes)

- `e9_score.zag`: argv [worldfile, transcript, barspec]. Parses QUERY
  (s,r,e) lines and ANSWER (s,r,v) lines 1:1 in order; parses CHOICE
  lines in order; evaluates HIT/NEED/CHOICE directives from the
  barspec; prints per-probe lines, CHOICE list, per-directive
  PASS/FAIL/INVALID, and the bar verdict. Exits nonzero on WORLD-INVALID
  or bar FAIL (so the driver can fail closed).
- `e9_score_m2e1.zag`: argv [transcript, driverlog, truthsfile, permfile,
  vocabfile]. Evaluates E-K8 sub-bars (a)-(f) from the driver log
  (ACT lines with informant tags), the transcript (final hidden probes
  vs truths), and the sealed PI. Prints sub-bar results and the verdict.
- `degen.zag`: argv [worldfile, outtranscript, policy]. Generates a
  degenerate transcript: D0 (QUERY->-2, ACT->0), D1 (QUERY->most recent
  OBSERVE object, ACT->30), D2 (QUERY->most recent OBSERVE object for
  the same (s,r) else -2, ACT->0). Used for the calibration check:
  each degenerate transcript is scored by e9_score.zag against the
  world's barspec; all must FAIL or INVALID, none may PASS.
- `inspect_state.zag`: copied from the 1421pdt battery (diagnostic
  only): prints MAP/UNCERT/GUIDE summaries from a state.bin. Never part
  of a bar (correction 3).
- `m2e1_driver.sh`: deterministic bash driver (safebin tools only)
  implementing section 5.4; PI embedded at generation time from the
  sealed derivation; writes the grown world file, transcript, driver
  log, and vocab file.

### 7.2 Sealed PI derivation (after freeze, before generation)

1. Compute H = sha256sum(PREREG_BATTERY_E9.md).
2. Take its first byte B (two hex chars); idx = B mod 6.
3. PI = PERM_TABLE[idx]. Record PI and H in WORLD_MANIFEST.sha256.
The derivation is mechanical (shell arithmetic); the selection is
sealed because it is not in the prereg text.

### 7.3 Block driver (deterministic shell)

Per block run: remove any prior state.bin; for E1..E3 in order run
`freeze_shim2_bin <world> <state.bin>` (exit code 0 required), saving
stdout as the transcript. For M2-E1 the driver grows the world per
section 5.4 and saves transcript + driver log + vocab file. After the
block, run the inspector on the final state.bin (diagnostic). Repeat 3
times; compare sha256 across runs (E-K2).

### 7.4 Anti-smuggling and manifest

At generation: sha256 manifest of all world/template/truth/driver/
barspec/perm files. Before execution: grep the frozen cognition
sources for 50000-59999 (E-K4). Hash re-verification of the shim
binary before each block run and after the battery (E-K3).

## 8. Verdict rules

- M1 MECHANISM-STRONG iff E-K5 and E-K6 and E-K7 all PASS; else
  M1 MECHANISM-WEAK (kill evidence: the failed sub-bars).
- M2 MECHANISM-STRONG iff E-K8 and E-K9 and E-K10 all PASS; else
  M2 MECHANISM-WEAK.
- M3 MECHANISM-STRONG iff E-K11 and E-K12 and E-K13 all PASS; else
  M3 MECHANISM-WEAK.
- Any process-bar (E-K1..E-K4, E-K14, E-K15) failure VOIDs the battery;
  a void battery is re-sealed and re-run, never interpreted.
- No verdict beyond the mechanism: no generality claim, no L3 claim,
  no cross-battery aggregation. See section 9.

## 9. Criterion 0 status (binding; no L3 claim on any pass)

This battery tests whether frozen, researcher-authored mechanisms
generalize to fresh structures. It does not test representational
invention:

- C0-A (runtime-defined semantics): NOT MET. The exercised semantics
  (trial-loop assemblers, constant guide action, single-schema patch)
  are researcher-authored machinery in the frozen source.
- C0-B (open structural form): NOT MET. Every world's tested form is
  enumerable from its demonstrations before the run.
- C0-C (multiple unforeseen forms, independent post-freeze adversary):
  NOT MET. Nine worlds across nine families, designed post-freeze, but
  the adversary role is played inside the same research loop. A second
  battery by a genuinely separate adversary is required before any
  L3-adjacent claim.
- C0-D (cognitive reuse): NOT MET as a criterion. Collateral probes
  measure retention, which is evidence toward a future C0-D case, but
  a single battery's probes are explicitly insufficient.

Consequence: no score on this battery, however high, may be described
as L3, L3-adjacent, or progress toward L3 without a separate
Criterion 0 case on independent evidence. The strongest honest claim
available is about the generality of M1, M2, M3 as frozen mechanisms.

## 10. What a FAIL means

Per the standing no-patch-treadmill rule, an expected FAIL is evidence
about what the frozen core is missing, not a request for a patch. The
results document clusters failures by shared architectural cause and
proposes general substrate hypotheses; benchmark-specific handlers and
per-world opcodes are rejected in advance.
