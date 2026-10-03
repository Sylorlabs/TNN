# PREREG_BATTERY_E10: Fresh Sealed Adversarial Battery on TNN-2's Three New Mechanisms (wave-20261002-0521pdt)

**Status:** PREREG-FROZEN (design only; no world files generated, no runs
executed, no implementation built at freeze time). This document is frozen
by SHA-256 before any battery artifact exists (see T-K1). The freeze commit
contains this file and NAMECHECK.md only; no .zag, .sh, .txt, or binary.

**Wave:** wave-20261002-0521pdt, lane BATTERY-E9.
**Date:** 2026-10-02.
**Battery name:** E10 (tenth sealed battery generation; second built under
the six triviality-review corrections).

## 0. Why E10 and not a re-run of E9

Battery E9 was completed by the wave-20261002-0221pdt lane BATTERY:
prereg frozen alone in commit 495d30fce, nine worlds run 3x
byte-identical, verdicts M1/M2/M3 MECHANISM-WEAK, red-team ruled
CALIBRATED, all committed. Re-running E9's identical worlds would not
be a fresh battery. E10 is nine NEW sealed worlds on the same three
mechanisms, materially different from FW1-FW9, the 1421pdt battery, and
E9. It applies all six triviality-review corrections (CORRECTIONS.md)
plus the lessons E9 queued: (i) the orphan-poisoning follow-up family
(revision correctness in the presence of rejected trial candidates,
adversarial to the revision lookup itself) is E10-M3-W1; (ii) E-K15 is
rewritten in retrieval-based form as T-K15; (iii) a pre-freeze barspec
index audit is recorded in section 7.5 (the m2e3.barspec typo lesson).

## 1. Step 0 (toolchain guard)

Recorded in NAMECHECK.md Step 0: safebin activated,
`which python3` prints nothing, pinned znc from safebin. All programs in
this battery are Zag compiled with the pinned znc. Shell (safebin
bash/awk/grep) is used only for byte checks, file transport, hash
manifests, and the deterministic interactive driver loop; all scoring,
world-generation logic, and state inspection is pure Zag.

## 2. Freeze record (read-only for this battery)

TNN-2 mechanism source (frozen):

- File: `docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag`
- SHA-256: `a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd`
  (re-verified by this worker before writing this prereg; matches the
  wave-20261001-1421pdt freeze record and the E9 freeze record)

Sealed interface shim (frozen, zero-cognition transport):

- File: `docs/lab/research-lead/overnight-20260928/core_freeze_tnn2_shim/freeze_shim2.zag`
- Binary `core_freeze_tnn2_shim/freeze_shim2_bin`
  SHA-256: `9217054c5af6dec057c4530c4de3ba246f521acc6df741d1989a4504acc72954`
  (re-verified; matches)
- Invocation: `freeze_shim2_bin <world.txt> <state.bin>`
- Protocol: `OBSERVE s r o` -> `OBSERVED s r o`; `QUERY s r expected` ->
  `ANSWER s r v` (ev_query with flags=0: exact hit, else trial loop,
  else bootstrap, else miss); `ACT` -> `CHOICE v`. Miss sentinel -2
  passes through unchanged. State file is exactly 110656 bytes and
  persists across invocations.

Compiler: `src/tools/toolchain/znc_linux_x86_64_abed8aa1`
SHA-256: `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`
(re-verified; matches the sealed freeze evaluation record).

The three mechanisms under test (all inside the frozen tnn2.zag;
behavior re-verified by source reading before this prereg was written):

- (M1) runtime executable-graph construction: `t2_trial` miss policy.
  Proposes k=2..4 chains over BFS data paths (forward links only, max
  4 hops), then subset-sum graphs over the subject's 1-hop values
  (total <= 900), then per-relation count graphs, then 1-hop chains;
  verifies each against the QUERY's expected value (oracle) and
  promotes the first verifier. Rejected candidates leave orphan cells
  with DEP edges to their licensing facts (never freed). Fallback:
  invariant bootstrap (the 6 most recent facts on the relation share
  one object and count >= 3, where the threshold node starts at 3 and
  is never mutated). The trial never consults promoted MAPs; each
  probe is solved from its own data, except exact-hit teaches.
- (M2) learner-originated uncertainty guiding action: `miss_inquire`
  (UNCERTAINTY node plus POLICY_ROOT-linked guide) feeding `ev_act`.
  Frozen behavior, verified in source: ACT scans POLICY_ROOT-linked
  guides, keeps live non-superseded guides whose subject sits in the
  4-deep context ring, selects max directional bid (ties: earliest
  edge), and returns the guide's action value, which
  `write_node(W,g,30,-999,0,0)` fixes at 30 for every guide. Guides
  are never superseded or retired. Each ACT adds a USE (type-6)
  self-loop to the selected guide, raising its future bid
  (stickiness).
- (M3) counterexample-driven revision: `revise_on_contradict` /
  `t2_revise_graph` (single-schema literal patch with re-execution
  check; revert on failure). The stale-cell lookup is GLOBAL: it
  takes the LAST type-101 cell (highest edge index) with a DEP edge
  to the contradicted fact, which may be a rejected trial candidate's
  orphan rather than the live graph's cell (E9 finding). On success
  the old promoted fact is CONed and the corrected answer taught;
  on revert nothing is taught and the MAP is untouched.

## 3. The six corrections and how E10 implements each

Corrections 1-6 verbatim in CORRECTIONS.md. E10 implementation:

1. Sealed informant to CHOICE mapping. E10-M2-W1 seals PI over
   {1,2,3}->{A,B,C} via the post-freeze derivation (section 8.2);
   W2 seals a 1-bit PI over {1,2}->{A,B}; W3 seals two 1-bit PIs
   (one per episode). No fixed mapping appears in this prereg.
   Constant policies are defeated by the distinctness sub-bars, which
   hold for every PI (case analysis in sections 6.4, 6.5, 6.6).
2. Distractor OBSERVEs before every M3 bar probe. EVERY M3 bar probe
   in E10 is preceded by 4 distractor OBSERVEs on unrelated ids.
   Each world spec carries an executed D1 (recency-echo) degenerate
   walk that must FAIL or INVALID the bar.
3. Zero white-box bars. Every E10 bar is transcript-only
   (ANSWER/CHOICE values vs expected). The state inspector runs as a
   diagnostic only, never as a bar condition. No bar names MAP, DEP,
   SETREG, or any internal representation.
4. Cross-world consistency. Collateral probes always expect
   originally-taught values; no contradicted triple is ever re-probed
   in a later world of the block; within each world one learner
   trajectory faces one consistent truth per triple.
5. Explore budget documented. W1: 5 calibration keys, each revealing
   (informant answer, truth); A identifiable within 3 explorations;
   the 5/6 hidden bar allows 1 deviation (documented as the intended
   explore-then-exploit demand). W2: hidden budget 6 ACTs for 4 keys
   (inquire-then-stop, 2 spare for re-verification). W3: 4
   calibration keys (2 per episode) before the 4 hidden keys.
6. Vocabulary decoupling. W1 opens with a VOCAB phase on fresh state
   measuring NULL_ACT (ACT with no live guides) and INQ_ACT (ACT
   after a forced miss, subject ring-resident). W2/W3 re-verify both
   vocabularies in situ (4-flush then ACT must equal NULL_ACT; forced
   miss then ACT must equal INQ_ACT; mismatch aborts the world as
   WORLD-INVALID). No bar names 0, 30, or any fixed CHOICE integer.

## 4. Battery scope and global constraints

Nine sealed worlds, three per mechanism. No world is a FW1-FW9 world
or a trivial variant of one; each world's "material difference" note
explains the separation from FW, from the 1421pdt battery, and from E9.

Global constraints:

- Event streams use integer ids only. No natural language, no task
  labels, no family identifiers.
- Id block 60000-69999 for the whole battery, disjoint from FW1-FW9
  (30000-39999), the 1421pdt battery (40000-49999), and E9
  (50000-59999), and disjoint across worlds except intentional
  within-block collateral probes.
- Sub-blocks: M1 60000-61999 (W1 60000-60999, W2 61000-61999 shares
  609xx distractors; exact ranges per world below); M2 62000-64999
  (W1 62000-62999, W2 63000-63999, W3 64000-64999); M3 65000-67999
  (W1 65000-65999, W2 66000-66999, W3 67000-67999).
- Worlds run in three blocks (M1: W1->W2->W3; M2: W1->W2->W3;
  M3: W1->W2->W3) with persistent learner state carried across worlds
  within a block (same state.bin chain). Each block starts from fresh
  state.
- The `expected` field on QUERY lines is the grader's truth and is
  passed to `ev_query` as the trial-loop oracle (documented frozen
  behavior). Bars are oracle-proofed: every bar-critical probe has no
  data path from the probed subject to its expected value (verified in
  each world spec by a mechanism walk grounded in the source reading
  of section 2), or the expected value is the taught fact, or the
  expected value is -2 (which never verifies: try_verify requires
  expected != -2). The oracle lets the trial loop verify; it cannot
  invent a path that does not exist, and bootstrap ignores it.
- No harness behavior depends on learner internals; all driver mappings
  are fixed in this prereg (plus sealed PIs) and mechanical.
- Anti-smuggling: before execution, the frozen cognition source is
  grepped for id tokens in 60000-69999; any match makes the affected
  world WORLD-INVALID (the world's fault), voiding the battery until a
  replacement is sealed under amendment.
- Determinism: each block is run 3 times end to end from fresh state;
  per-world transcripts (and for M2 worlds the grown world file plus
  driver log plus vocab file) must be byte-identical across the 3 runs
  (sha256 equality).
- Degenerate calibration: for every mechanism bar, the world spec
  gives degenerate walks (D0 always -2/0, D1 recency-echo/constant-30,
  D2 last-write-wins/0, plus always-c and rotate for the M2 selection
  worlds) showing the trivial contestant does NOT pass. The walks are
  executed, not just asserted: `degen.zag` generates degenerate
  transcripts for the 6 static worlds and the scorer evaluates the
  bars on them; the M2 policy analyses are verified by case analysis
  over all sealed PIs (recorded in each world spec).

## 5. Adversarial coverage requirement

At least one world per mechanism is adversarial to that mechanism's
KNOWN STRENGTH (not just its known gaps):

- M1: W1 embeds the demonstrated strength (forward 2-hop composition,
  proved by FW1/FW2 and re-proved in-world by the engagement probes)
  then demands NESTING (sum over chain-ends): the strength fires and
  is insufficient.
- M2: W1 is adversarial to the inquiry strength itself: engagement
  sub-bar (a) proves ACTs fire after misses in-world, but the demand
  is that inquiry carry INFORMATION (guide-addressed informant
  selection); constant content cannot.
- M3: W1 attacks the working first-revision path: the revision
  machinery fires and its re-execution check "succeeds", but it
  revises a dead orphan instead of the live graph.

## 6. World specifications

Notation: exact event streams. `QUERY s r e` carries grader truth `e`.
Predicted outcomes are recorded honestly before execution; predicted
FAILs are information, not battery defects. Each world lists:
adversarial intent, material difference, mechanism walk (why the frozen
mechanism behaves as predicted, grounded in the section 2 source
reading, including oracle-proofing), degenerate walks, and the bar.

### 6.1 M1-E10-W1: sum over chain-ends (nesting family)

Adversarial intent: the trial loop composes (chains) and sums, but it
cannot NEST the two: the sum assembler sees only the subject's 1-hop
values, never values at the ends of composed paths. Engagement proves
2-hop composition fires in-world; the bar probes demand
sum-of-chain-ends, which no trial phase expresses.

Material difference: no FW world, no 1421pdt world, and no E9 world
tested nesting. E9-E1/E2/E3 tested branch/join/depth (all flat
topologies). Nearest neighbor is FW1 (forward chains); the difference
is the sum-over-paths demand.

Event stream (`m1w1_world.txt`):

```
OBSERVE 60101 60501 60701
OBSERVE 60701 60502 3
QUERY 60101 60509 3
OBSERVE 60102 60501 60704
OBSERVE 60704 60502 2
QUERY 60102 60509 2
OBSERVE 60105 60501 60701
OBSERVE 60105 60501 60702
OBSERVE 60105 60501 60703
OBSERVE 60701 60502 3
OBSERVE 60702 60502 5
OBSERVE 60703 60502 7
QUERY 60105 60509 15
OBSERVE 60106 60501 60704
OBSERVE 60106 60501 60705
OBSERVE 60704 60502 2
OBSERVE 60705 60502 7
QUERY 60106 60509 9
```

Probe indices: 0:(60101,60509,3) 1:(60102,60509,2) 2:(60105,60509,15)
3:(60106,60509,9). Four QUERYs total.

Mechanism walk (frozen): idx0: k=2 path [60101,60701,3] executes to 3,
verifies against oracle 3, promotes. idx1 likewise (2). idx2: k=2
paths [60105,60701,3]->3, [60105,60702,5]->5, [60105,60703,7]->7, all
reject vs 15; k=3/k=4: no length-4/5 paths (leaf values have no
outgoing facts); sum phase: 1-hop values {60701,60702,60703}, every
subset sum >= 60701 > 900, all declined; count phase: relation 60501
chain is [60105,60701] (first match only), count 1, rejects; 1-hop
phase: 60701/60702/60703 reject; bootstrap on 60509: the two most
recent 60509 facts are the engagement teaches (objects 3 and 2,
distinct) so invariance fails. Miss -> ANSWER -2. idx3 likewise
(values {60704,60705}, leaves 2 and 7, expected 9) -> -2. Predicted:
idx0,1 PASS; idx2,3 -2.

Oracle-proof: no data path from 60105 computes 15 (all path values
are 3/5/7 or fan values; subset sums decline); same for 60106/9.

Degenerate walks: D0: idx0 -2 -> WORLD-INVALID. D1 (recency-echo):
idx0: most recent OBSERVE (60701,60502,3) -> 3 PASS; idx1: 2 PASS;
idx2: most recent (60703,60502,7) -> 7 != 15 FAIL; idx3: most recent
(60705,60502,7) -> 7 != 9 FAIL. NEED 0/2 -> T-K5 FAIL. D2: idx0: no
(60101,60509) OBSERVE -> -2 -> WORLD-INVALID. No degenerate passes.

Bar T-K5: PASS iff HIT 0,1 (engagement) and at least 1 of probes 2,3
correct. Validity: HIT fails -> WORLD-INVALID. Predicted FAIL (0/2).

### 6.2 M1-E10-W2: chained join (join family, depth 2)

Adversarial intent: E9-E2 killed the one-hop value join. W2 chains
TWO value lookups: the subject whose key matches this subject's key,
whose payload matches a third subject's key: return the third
subject's payload. The BFS cannot express even one value to subject
step; two in sequence is a new structure.

Material difference: E9-E2 was a single equi-join. No FW world did
joins. Nearest neighbor is E9-E2; the difference is join depth 1->2
(two value lookups, materially different demand).

Event stream (`m1w2_world.txt`):

```
OBSERVE 60202 60610 60651
OBSERVE 60202 60611 60661
QUERY 60202 60611 60661
OBSERVE 60211 60610 60661
OBSERVE 60211 60611 60671
QUERY 60211 60611 60671
OBSERVE 60201 60610 60651
OBSERVE 60204 60610 60652
OBSERVE 60204 60611 60662
OBSERVE 60212 60610 60662
OBSERVE 60212 60611 60672
OBSERVE 60203 60610 60652
OBSERVE 60911 60900 60921
OBSERVE 60912 60900 60922
QUERY 60201 60619 60671
QUERY 60203 60619 60672
QUERY 60101 60509 3
QUERY 60102 60509 2
```

Probe indices: 0:(60202,60611,60661) 1:(60211,60611,60671)
2:(60201,60619,60671) 3:(60203,60619,60672) 4:(60101,60509,3)
5:(60102,60509,2). Six QUERYs total. Probes 4,5 are collateral from
M1-E10-W1 (taught values, correction 4).

Mechanism walk (frozen): idx0,1 exact hits (direct retrieval works).
idx2: BFS from 60201: paths [60201], [60201,60651]; no fact has
subject 60651, so no longer path. k=2..4: none. Sum: {60651},
declined (>900). Count: relation 60610 chain [60201,60651], count 1,
rejects vs 60671. 1-hop: 60651 rejects. Bootstrap: no 60619 facts
exist. Miss -> -2. idx3 likewise -> -2. idx4,5: exact hits on W1's
promoted facts -> 3, 2. Predicted: idx0,1 PASS; idx2,3 -2; idx4,5
PASS.

Oracle-proof: the only length-2 path is [60201,60651]; no path
reaches 60671 or 60672. The 60911/60912 distractors defeat
recency-echo and touch no data path.

Degenerate walks: D0: idx0 -2 -> WORLD-INVALID. D1: idx0: 60661
PASS; idx1: 60671 PASS; idx2: most recent OBSERVE (60912,60900,60922)
-> 60922 != 60671 FAIL; idx3: 60922 != 60672 FAIL. NEED 0/2 ->
T-K6 FAIL. D2: idx0: (60202,60611) observed -> 60661 PASS; idx1 PASS;
idx2: no (60201,60619) OBSERVE -> -2 -> NEED 0/2 FAIL. No degenerate
passes.

Bar T-K6: PASS iff HIT 0,1 and at least 1 of probes 2,3 correct.
Validity: HIT fails -> WORLD-INVALID. Predicted FAIL (0/2).

### 6.3 M1-E10-W3: bootstrap fabrication (fallback family)

Adversarial intent: the miss policy's fallback (invariant bootstrap)
is a surface heuristic with no grounding: three coincidentally
invariant recent facts on a novel relation make it fabricate an
answer instead of admitting ignorance. Engagement proves the trial
loop works in-world; the bar probe has no data path at all, so the
only honest answer is the miss sentinel.

Material difference: no prior world tested the fallback heuristic.
FW and E9 worlds always gave the trial a data path or a genuine
miss. Nearest neighbor is E9-E3 (also a -2/miss world), but E3's
miss came from a depth cap; here the miss is fabricated away by the
fallback.

Event stream (`m1w3_world.txt`):

```
OBSERVE 60301 60501 60311
OBSERVE 60311 60502 60312
QUERY 60301 60509 60312
OBSERVE 60302 60501 60321
OBSERVE 60321 60502 60322
QUERY 60302 60509 60322
OBSERVE 60311 60519 60399
OBSERVE 60312 60519 60399
OBSERVE 60313 60519 60399
QUERY 60305 60519 -2
QUERY 60101 60509 3
QUERY 60102 60509 2
```

Probe indices: 0:(60301,60509,60312) 1:(60302,60509,60322)
2:(60305,60519,-2) 3:(60101,60509,3) 4:(60102,60509,2). Five QUERYs.
Probes 3,4 are collateral from M1-E10-W1 (taught values).

Mechanism walk (frozen): idx0,1: k=2 chains promote, PASS. idx2:
subject 60305 has no facts: gather yields [60305] only; k=2..4: no
paths; sum: no 1-hop values; count: no relations; 1-hop: none.
Bootstrap on 60519: the 3 most recent 60519 facts are the
distractors, all object 60399, count 3 >= k (k=3, verified constant
in source: the 903 node is only ever read, never mutated). Invariant
holds -> teaches (60305,60519,60399), returns 60399. Predicted
ANSWER 60399, expected -2 -> FAIL. idx3,4: exact hits -> 3, 2.

Oracle-proof: expected -2 never verifies (try_verify requires
expected != -2); bootstrap ignores the oracle. The fabricated 60399
comes from surface coincidence, not from any path.

Degenerate walks: D0: idx0 -2 -> WORLD-INVALID. D1: idx0: 60312
PASS; idx1: 60322 PASS; idx2: most recent OBSERVE
(60313,60519,60399) -> 60399 != -2 FAIL. NEED 0/1 -> T-K7 FAIL. D2:
idx0: no (60301,60509) OBSERVE -> -2 -> WORLD-INVALID. No degenerate
passes.

Bar T-K7: PASS iff HIT 0,1 and probe 2 == -2 (ignorance admitted).
Validity: HIT fails -> WORLD-INVALID. Predicted FAIL (60399).

### 6.4 M2-E10-W1: informant selection v2 (selection family)

Adversarial intent: E9-E1 proved the frozen mechanism cannot direct
inquiry under a sealed mapping. W1 hardens the discriminator: the
liar is PLAUSIBLE (truth+1, varies per key, cannot be memorized) and
the third informant is a CONTRARIAN (returns another key's truth).
The demand is the same family (guide-addressed selection) with a
materially different informant population.

Material difference: E9-E1's informants were truthful / fixed wrong
table / constant flatterer (52999). W1's are truthful / plausible
liar (truth+1) / cross-key contrarian. Calibration is now
miss-first (guide-gated exploration is genuinely informative, unlike
E9-E1's wasted calibration ACTs). No FW world did informant
selection.

Structure (driver-grown from template; driver fixed and deterministic):

Template (`m2w1_template.txt`):

```
ACT
QUERY 62901 62900 62911
ACT
OBSERVE 62991 62990 62991
OBSERVE 62992 62990 62992
OBSERVE 62993 62990 62993
OBSERVE 62994 62990 62994
OBSERVE 62091 62500 62999
OBSERVE 62092 62500 62999
```

VOCAB: ACT#1 with no live guides records NULL_ACT (frozen: 0).
QUERY (62901,62900,62911) is a true miss -> guide created. ACT#2
records INQ_ACT (frozen: 30, subject ring-resident). 4 flush
OBSERVEs retire the vocab subject from the ring. Bias seeds
(62091,62092 -> 62999) are taught values reused as collateral in
W2/W3.

Driver phases (fixed):

- Calibration keys 62101-62105, truths 62201-62205, relation 62500.
  Per key: `QUERY k 62500 truth` (miss probe, unscored; creates the
  guide so the ACT is guide-gated); `ACT` -> C; INF = PI(C) if C in
  {1,2,3} else NONE; log `ACT CAL k C INF`; if INF != NONE:
  `OBSERVE k 62500 ans` with ans = truth (A), truth+1 (B),
  previous-key truth in this phase else 62999 (C); then
  `OBSERVE k 62500 truth`; then `QUERY k 62500 truth` (unscored).
- Hidden keys 62111-62113, truths 62211-62213. Per key:
  `QUERY k 62500 truth` (miss probe); twice: `ACT` -> C; INF as
  above; log `ACT HID k C INF`; if INF != NONE: `OBSERVE k 62500
  ans`; then `QUERY k 62500 truth` (final probe, scored).

Informant personalities: A truthful; B plausible liar (truth+1);
C contrarian (previous key's truth in the phase, 62999 for the first
key of the phase). Sealed PI over {1,2,3}->{A,B,C} from the
post-freeze derivation (section 8.2); the public PERM_TABLE is the
same six permutations E9 used.

Mechanism walk (frozen): VOCAB gives NULL_ACT=0, INQ_ACT=30.
Every ACT (calibration and hidden) fires with the key's guide
ring-resident -> CHOICE 30 -> NONE (30 not in {1,2,3}). No
informant is ever consulted; hidden final probes -> -2. Predicted:
(a) PASS (6 hidden ACTs after miss probes); (b) 0/6 to A FAIL;
(c) 0 to C PASS; (d) 0/3 final probes FAIL; (e) 6/6 budget PASS;
(f) calibration distinct CHOICEs 1 (all 30) FAIL. T-K8 FAIL.

Explore budget (correction 5): 5 calibration keys; each reveals
(informant answer, truth), so A is identifiable within 3
explorations; the 5/6 hidden bar allows 1 deviation. Documented as
the intended explore-then-exploit demand.

Degenerate/policy analysis (verified for every PI by case analysis):
always-c for c in {1,2,3}: sub-bar (f) fails (1 distinct CHOICE) for
EVERY PI -> cannot pass T-K8. rotate-1,2,3 over the 6 hidden ACTs:
A is hit exactly 2/6 times for every PI < 5 -> (b) FAIL. D0
(ACT->0): (a) PASS (ACTs are performed), (b) 0/6 FAIL. D1 (ACT->30):
identical to frozen -> (b) FAIL. A win-stay policy on calibration
feedback is competent behavior, not degenerate. No trivial
contestant passes T-K8.

Bar T-K8: PASS iff (a) at least one hidden key has an ACT after its
miss probe; (b) at least 5 of the 6 hidden ACTs target A
(CHOICE == PI-inverse(A)); (c) at most 1 hidden ACT targets C;
(d) at least 2 of the 3 final hidden probes correct; (e) hidden
ACTs <= 6; (f) at least 2 distinct CHOICE values across the 5
calibration ACTs. All six required. Predicted FAIL.

### 6.5 M2-E10-W2: inquiry budget (stopping family)

Adversarial intent: the frozen gate is all-or-nothing per ACT: while
a live guide's subject is ring-resident it can only re-fire; it
cannot STOP inquiring. W2 makes stopping the scored behavior: each
hidden key offers up to 3 ACT opportunities and the driver stops at
the first NULL_ACT. The budget (6 for 4 keys) demands
inquire-then-stop thrift. E9-E3 demanded suppression of a second
inquiry; W2 demands a stopping DECISION under a budget, which the
mechanism controls (correction 6 is load-bearing: the stop signal
is the mechanism's own measured NULL_ACT).

Material difference: E9's worlds used fixed ACT counts per key. No
prior world let the mechanism control the inquiry count. Nearest
neighbor is E9-E3 (thrift); the difference is mechanism-controlled
stopping vs fixed suppression.

Structure (driver-grown):

Template (`m2w2_template.txt`): 4 flush OBSERVEs, vocab-verify ACT,
forced miss QUERY, vocab-verify ACT:

```
OBSERVE 63991 63990 63991
OBSERVE 63992 63990 63992
OBSERVE 63993 63990 63993
OBSERVE 63994 63990 63994
ACT
QUERY 63901 63900 63911
ACT
```

Vocab-verify (correction 6): the first ACT must equal W1's NULL_ACT
(no live guide subject in the ring after the flushes); the QUERY is
a true miss (guide created); the second ACT must equal W1's INQ_ACT.
Mismatch aborts the world as WORLD-INVALID (driver exits nonzero).

Driver phases (fixed):

- Calibration keys 63101-63103, truths 63201-63203, relation 63500,
  informants {A truthful, B plausible liar (truth+1)}, sealed 1-bit
  PI over {1,2}->{A,B} (section 8.2). Per key: `QUERY k 63500
  truth` (miss probe); up to 2 ACTs, stopping at the first CHOICE
  == NULL_ACT; C = last non-NULL CHOICE or NONE; INF = PI(C);
  log `ACT CAL k C INF`; if INF != NONE: `OBSERVE k 63500 ans`;
  then `OBSERVE k 63500 truth`; then `QUERY k 63500 truth`
  (unscored). Log `KEYDONE k n_acts early` per key.
- Hidden keys 63111-63114, truths 63211-63214. Per key: `QUERY k
  63500 truth` (miss probe); up to 3 ACTs with the same stop rule;
  C = last non-NULL CHOICE or NONE; INF as above; log `ACT HID k C
  INF`; if INF != NONE: `OBSERVE k 63500 ans`; then `QUERY k 63500
  truth` (final probe, scored). Log `KEYDONE` per key.
- Collateral (for T-K14): `QUERY 62091 62500 62999`,
  `QUERY 62092 62500 62999` (W1's bias seeds, taught values);
  driver logs `COLLATERAL s r got exp`.

Mechanism walk (frozen): every ACT fires with the key's guide
ring-resident -> CHOICE 30 != NULL_ACT -> never stops: 3 ACTs per
hidden key = 12 total; C=30 -> NONE; final probes -> -2. Predicted:
(a) PASS; (b) 12 > 6 FAIL; (c) 0/4 FAIL; (d) 0 keys early FAIL;
(e) vocab-verify PASS. T-K9 FAIL.

Budget doc (correction 5): 6 ACTs for 4 keys = inquire once per key
then stop, with 2 spare for cautious re-verification. Documented as
the intended stopping demand.

Policy analysis: always-NULL: (a) fails (no non-NULL ACT) ->
WORLD-INVALID (unengaged, not a pass). always-INQ: 12 ACTs ->
(b) FAIL. rotate-1,2 (never NULL): (b) FAIL. No trivial contestant
passes T-K9.

Bar T-K9: PASS iff (a) at least 1 non-NULL hidden ACT; (b) total
non-NULL hidden ACTs <= 6; (c) at least 3 of the 4 final probes
correct; (d) at least 2 keys stopped early (fewer than 3 ACTs);
(e) vocab-verify passed (else WORLD-INVALID). All required.
Predicted FAIL.

### 6.6 M2-E10-W3: selection under population change (flexibility family)

Adversarial intent: the informant population changes mid-task
(episode A: {A,B}; episode B: {A,C} with a fresh sealed mapping).
A selector that perseverates on the first episode's mapping fails
the second. The frozen mechanism cannot select at all; the demand
is adaptive re-selection, which requires per-episode exploration.

Material difference: E9-E1 had one fixed population and one mapping.
No prior world changed the mapping mid-task. Nearest neighbor is
E9-E1; the difference is the population change and the
re-selection demand.

Structure (driver-grown): template like W2 (flush, vocab-verify ACT,
forced miss, vocab-verify ACT) with 6499x ids.

Driver phases (fixed):

- Calibration keys 64101-64104, truths 64201-64204, relation 64500.
  Keys 64101-64102 are episode A ({A truthful, B plausible liar
  truth+1}, sealed bit_a PI over {1,2}->{A,B}); keys 64103-64104 are
  episode B ({A truthful, C constant 64999}, sealed bit_b PI over
  {1,2}->{A,C}). Per key: `QUERY k 64500 truth` (miss probe);
  `ACT` -> C; INF = episode-PI(C); log `ACT CAL k C INF`; if INF:
  `OBSERVE k 64500 ans`; then `OBSERVE k 64500 truth`; then
  `QUERY k 64500 truth` (unscored).
- Hidden keys 64111-64114, truths 64211-64214: 64111-64112 episode
  A, 64113-64114 episode B. Per key: `QUERY k 64500 truth` (miss
  probe); `ACT` -> C; INF as above; log `ACT HID k C INF`; if INF:
  `OBSERVE k 64500 ans`; then `QUERY k 64500 truth` (final probe,
  scored).
- Collateral: `QUERY 62091 62500 62999`, `QUERY 62092 62500 62999`;
  driver logs COLLATERAL lines.

Mechanism walk (frozen): all ACTs -> 30 -> NONE -> final probes -2.
Predicted: (a) PASS; (b) 0/4 FAIL; (c) 4 <= 4 PASS; (d) calibration
distinct 1 FAIL; (e) vocab-verify PASS. T-K10 FAIL.

Policy analysis over all 4 PI combinations: always-1: correct in
{0,2,4}; the 4/4 case is defeated by (d) (1 distinct CHOICE) ->
FAIL. always-2: symmetric -> FAIL. rotate-1,2 over hidden keys
1,2,1,2: correct = [PI_a(1)=A]+[PI_a(2)=A]+[PI_b(1)=A]+[PI_b(2)=A]
= exactly 2 < 3 -> (b) FAIL for every combination. D0: (a) PASS,
(b) 0/4 FAIL. No trivial contestant passes T-K10.

Bar T-K10: PASS iff (a) at least one hidden key has an ACT after
its miss probe; (b) at least 3 of the 4 final probes correct;
(c) hidden ACTs <= 4; (d) at least 2 distinct CHOICE values across
the 4 calibration ACTs; (e) vocab-verify passed (else
WORLD-INVALID). All required. Predicted FAIL.

### 6.7 M3-E10-W1: orphan poisoning, adversarial (lookup family)

Adversarial intent: the E9 execution discovered that
`t2_revise_graph`'s stale-cell lookup is global: it patches the
LAST type-101 cell with a DEP edge to the contradicted fact, which
can be a rejected trial candidate's orphan. W1 is built to trigger
exactly this: MAP_B's promotion trial rejects a 2-hop candidate
whose orphan cells carry DEP edges to the fact W1 then contradicts.
The revision machinery fires, its re-execution check "succeeds"
(on the untouched live graph), and the live MAP is never revised.
This is adversarial to the WORKING first-revision path: engagement
(MAP_B's promotion, which requires the trial to try and reject the
decoy) proves the machinery is live in-world.

Material difference: this family was queued by E9's SEALED_RESULTS
("revision correctness in the presence of rejected trial
candidates, adversarial to the revision lookup itself") and has
never been tested deliberately. Not in FW, 1421pdt, or E9.

Event stream (`m3w1_world.txt`):

```
OBSERVE 65101 65501 65102
OBSERVE 65102 65502 65103
OBSERVE 65103 65510 65104
QUERY 65101 65509 65103
QUERY 65101 65509 65103
QUERY 65101 65519 65104
OBSERVE 65102 65502 65113
OBSERVE 65801 65800 65811
OBSERVE 65802 65800 65812
OBSERVE 65803 65800 65813
OBSERVE 65804 65800 65814
QUERY 65101 65509 65113
QUERY 65801 65800 65811
QUERY 65802 65800 65812
```

Probe indices: 0:(65101,65509,65103) 1:(65101,65509,65103)
2:(65101,65519,65104) 3:(65101,65509,65113) 4:(65801,65800,65811)
5:(65802,65800,65812). Six QUERYs total.

Mechanism walk (frozen; grounded in the section 2 source reading):
idx0,1: MAP_A's trial accepts k=2 [65101,65102,65103] immediately
(no rejects, no orphans), promotes ans 65103, teaches
(65101,65509,65103). idx2: MAP_B's trial on (65101,65519,65104):
k=2 tries [65101,65102,65103] first (BFS order: the 65501 fact has
the lower node index) -> assembles chain cells with DEP edges to
the link-1/link-2 fact nodes -> executes to 65103, rejects vs
65104; the orphan cells persist. Then [65101,65103,65104] verifies
-> promotes ans 65104. Contradiction OBSERVE (65102,65502,65113):
activate hits the link-2 fact; CON self-loop; revise_on_contradict
finds MAP_A's DEP to the fact; t2_revise_graph's global stale
lookup takes the LAST type-101 cell with a DEP edge to the
contradicted fact node = MAP_B's orphan (its DEP edge has the
higher edge index, created later) -> patches the orphan's guard,
re-executes MAP_A's untouched root -> 65103 (not -999999) ->
"success": CONs the live promoted fact (65101,65509,65103),
re-teaches (65101,65509,65103), MAP_A ans stays 65103. 4
distractors (correction 2). idx3: exact hit on the re-taught
(65101,65509,65103) -> 65103, expected 65113 -> FAIL. idx4,5:
exact hits on distractor teaches -> PASS.

Oracle-proof: idx3 is an exact hit on a stale taught fact; the
trial loop is never reached, so the oracle plays no role. The
expected 65113 is not taught for (65101,65509) anywhere.

Degenerate walks: D0: idx0 -2 -> WORLD-INVALID. D1: idx0: most
recent OBSERVE (65103,65510,65104) -> 65104 != 65103 ->
WORLD-INVALID. D2: idx0: no (65101,65509) OBSERVE -> -2 ->
WORLD-INVALID. No degenerate passes.

Bar T-K11: PASS iff HIT 0,1,2 (validity) and probe 3 == 65113.
Validity: HIT fails -> WORLD-INVALID. Predicted FAIL (65103).

### 6.8 M3-E10-W2: chained propagation (propagation family, depth 2)

Adversarial intent: E9-E2 (amended) killed depth-1 downstream
propagation. W2 chains it: MAP_C is licensed by MAP_B's promoted
fact, which is licensed by MAP_A's promoted fact; contradicting
MAP_A's link must propagate through two levels. The amendment's
link-3 trick is reused deliberately to keep the stale lookup clean,
so the bar tests propagation, not orphan poisoning (that is W1's
job).

Material difference: E9-E2 was single-downstream propagation.
Depth-2 chained propagation is new. Not in FW or 1421pdt.

Event stream (`m3w2_world.txt`):

```
OBSERVE 66101 66501 66102
OBSERVE 66102 66502 66103
OBSERVE 66103 66503 66105
OBSERVE 66105 66510 66104
QUERY 66101 66509 66105
QUERY 66101 66509 66105
QUERY 66101 66519 66104
OBSERVE 66104 66520 66106
QUERY 66101 66529 66106
OBSERVE 66103 66503 66113
QUERY 66101 66509 66113
OBSERVE 66113 66510 66114
OBSERVE 66114 66520 66116
OBSERVE 66801 66800 66811
OBSERVE 66802 66800 66812
OBSERVE 66803 66800 66813
OBSERVE 66804 66800 66814
QUERY 66101 66529 66116
QUERY 66801 66800 66811
QUERY 66802 66800 66812
```

Probe indices: 0:(66101,66509,66105) 1:(66101,66509,66105)
2:(66101,66519,66104) 3:(66101,66529,66106) 4:(66101,66509,66113)
5:(66101,66529,66116) 6:(66801,66800,66811) 7:(66802,66800,66812).
Eight QUERYs total.

Mechanism walk (frozen): idx0,1: MAP_A's trial: k=2
[66101,66102,66103] rejects vs 66105 (orphans with DEP to link-1/2
facts); k=3 [66101,66102,66103,66105] verifies -> promotes ans
66105. idx2: MAP_B's trial: k=2 [66101,66102,66103] rejects;
[66101,66105,66104] verifies -> promotes ans 66104 (k=3 never
runs). idx3: MAP_C's trial: k=2 [66101,66102,66103] rejects,
[66101,66105,66104] rejects vs 66106, [66101,66104,66106] verifies
-> promotes ans 66106. Contradiction (66103,66503,66113): link 3 of
MAP_A. Stale lookup: only MAP_A's live SETREG#3 carries a DEP edge
to the link-3 fact (no rejected candidate ever included link 3,
because k=2 acceptance short-circuits before k=3 runs) -> clean
patch; terminal link; re-execution succeeds -> MAP_A ans 66113,
old promoted fact CONed, (66101,66509,66113) taught. MAP_B and
MAP_C untouched (no DEP to the contradicted fact). New downstream
links taught as plain OBSERVEs: (66113,66510,66114),
(66114,66520,66116). 4 distractors (correction 2). idx4: exact hit
(66101,66509,66113) -> 66113 PASS (validity). idx5: exact hit on
MAP_C's still-live promoted fact (66101,66529,66106) -> 66106,
expected 66116 -> FAIL. idx6,7: hits.

A competent downstream-propagating reviser would re-derive B
(66114) and C (66116) from the new links; the frozen mechanism has
no such machinery.

Oracle-proof: idx5 is an exact hit on the stale fact; the trial
loop is never reached.

Degenerate walks: D0: idx0 -2 -> WORLD-INVALID. D1: idx0: most
recent OBSERVE (66105,66510,66104) -> 66104 != 66105 ->
WORLD-INVALID. D2: idx0: no (66101,66509) OBSERVE -> -2 ->
WORLD-INVALID. No degenerate passes.

Bar T-K12: PASS iff HIT 0,1,2,3,4 (validity) and probe 5 == 66116.
Validity: HIT fails -> WORLD-INVALID. Predicted FAIL (66106).

### 6.9 M3-E10-W3: revision specificity (precision control)

Adversarial intent: none; this is a CONTROL world. E9 showed the
revision operator fires eagerly (W1: singleton noise) and on the
wrong graph (W1 here). W3 maps the precision boundary from the
other side: a contradiction of a NONTERMINAL link must revert
without corrupting the MAP; a contradiction of a fact no graph
licenses must be a complete no-op; an independent MAP must be
unaffected. A competent precise reviser passes; the frozen
mechanism is predicted to pass, which keeps the battery honest
(bars are passable) and documents the revert/no-op behavior.

Material difference: no prior world tested revision specificity or
the no-op case. Nearest neighbor is E9-E3 (nonterminal revert);
the difference is that W3 scores the revert as CORRECT (old answer
retained) and adds the unlicensed-contradiction no-op probe.

Event stream (`m3w3_world.txt`):

```
OBSERVE 67101 67501 67102
OBSERVE 67102 67502 67103
QUERY 67101 67509 67103
QUERY 67101 67509 67103
OBSERVE 67111 67511 67112
OBSERVE 67112 67512 67113
QUERY 67111 67519 67113
QUERY 67111 67519 67113
OBSERVE 67101 67501 67122
OBSERVE 67101 67505 67130
OBSERVE 67101 67505 67131
OBSERVE 67801 67800 67811
OBSERVE 67802 67800 67812
OBSERVE 67803 67800 67813
OBSERVE 67804 67800 67814
QUERY 67111 67519 67113
QUERY 67101 67509 67103
QUERY 67801 67800 67811
QUERY 67802 67800 67812
```

Probe indices: 0:(67101,67509,67103) 1:(67101,67509,67103)
2:(67111,67519,67113) 3:(67111,67519,67113) 4:(67111,67519,67113)
5:(67101,67509,67103) 6:(67801,67800,67811) 7:(67802,67800,67812).
Eight QUERYs total.

Mechanism walk (frozen): idx0,1: MAP_A promotes (ans 67103).
idx2,3: MAP_B promotes (ans 67113; its k=2 trial accepts the only
path immediately, leaving no orphans touching A's facts).
Contradiction (67101,67501,67122): link 1 of MAP_A
(nonterminal). Stale lookup finds MAP_A's live SETREG#1 (no orphan
carries a DEP edge to this fact) -> patch -> re-execution: guard#2
expects 67102, sees 67122 -> -999999 -> REVERT: MAP_A untouched,
nothing taught, nothing CONed. Unlicensed contradiction:
(67101,67505,67130) is a plain teach (novel (s,r)); then
(67101,67505,67131) contradicts it; revise_on_contradict finds no
MAP with a DEP edge to that fact -> complete no-op; the new value
is taught. 4 distractors. idx4: MAP_B unaffected -> exact hit
67113 PASS. idx5: MAP_A retained -> exact hit 67103 PASS.
idx6,7: hits.

Degenerate walks: D0: idx0 -2 -> WORLD-INVALID. D1: idx0: most
recent (67102,67502,67103) -> 67103 PASS; idx1 PASS; idx2: most
recent (67112,67512,67113) -> 67113 PASS; idx3 PASS; idx4: most
recent distractor 67814 != 67113 FAIL; idx5: 67814 != 67103 FAIL.
NEED 0/2 -> T-K13 FAIL. D2: idx0: no (67101,67509) OBSERVE -> -2 ->
WORLD-INVALID. No degenerate passes.

Bar T-K13: PASS iff HIT 0,1,2,3 (validity) and probe 4 == 67113
and probe 5 == 67103. Validity: HIT fails -> WORLD-INVALID.
Predicted PASS.

## 7. Frozen kill bars T-K1 through T-K15

All bars are PASS/FAIL only; no partial credit. Process-bar failures
void the battery (re-seal and re-run); they are never scored as
mechanism verdicts.

- T-K1 (prereg ordering). PASS iff the SHA-256 of this file recorded
  in SEALED_RESULTS.md was computed before any battery artifact
  (world/template/driver/scorer file) was created (filesystem mtime
  order and commit topology) and the file is unmodified thereafter
  (hash re-verified after the battery). The freeze commit contains
  this file and NAMECHECK.md only.
- T-K2 (determinism). PASS iff, for each of the 3 blocks, the 3
  end-to-end runs produce byte-identical per-world transcripts
  (sha256 equality; for M2 worlds the grown world file plus driver
  log plus transcript plus vocab file).
- T-K3 (frozen binary). PASS iff `freeze_shim2_bin` hashes to
  `9217054c5af6dec057c4530c4de3ba246f521acc6df741d1989a4504acc72954`
  before each block run and after the battery, `tnn2.zag` still hashes
  to `a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd`,
  and `git status` shows zero modifications under
  `docs/lab/research-lead/overnight-20260928/tnn2_build/` and
  `.../core_freeze_tnn2_shim/` cognition paths.
- T-K4 (seal integrity). PASS iff all world/template/truth/driver
  files match the manifest hashes recorded at generation, and
  `grep -r` over the frozen cognition sources finds zero tokens in
  60000-69999.
- T-K5 (M1-E10-W1 nesting). PASS iff HIT 0,1 and at least 1 of
  probes 2,3 correct. Validity: HIT fails -> WORLD-INVALID.
- T-K6 (M1-E10-W2 chained join). PASS iff HIT 0,1 and at least 1 of
  probes 2,3 correct. Validity: HIT fails -> WORLD-INVALID.
- T-K7 (M1-E10-W3 bootstrap). PASS iff HIT 0,1 and probe 2 == -2.
  Validity: HIT fails -> WORLD-INVALID.
- T-K8 (M2-E10-W1 selection v2). PASS iff (a) at least one hidden
  key has an ACT after its miss probe; (b) at least 5 of the 6
  hidden ACTs target A; (c) at most 1 hidden ACT targets C;
  (d) at least 2 of the 3 final hidden probes correct; (e) hidden
  ACTs <= 6; (f) at least 2 distinct CHOICE values across the 5
  calibration ACTs. All six required.
- T-K9 (M2-E10-W2 budget). PASS iff (a) at least 1 non-NULL hidden
  ACT; (b) total non-NULL hidden ACTs <= 6; (c) at least 3 of the 4
  final probes correct; (d) at least 2 keys stopped early (fewer than
  3 ACTs); (e) vocab-verify passed, else WORLD-INVALID. All
  required.
- T-K10 (M2-E10-W3 population change). PASS iff (a) at least one
  hidden key has an ACT after its miss probe; (b) at least 3 of the
  4 final probes correct; (c) hidden ACTs <= 4; (d) at least 2
  distinct CHOICE values across the 4 calibration ACTs; (e)
  vocab-verify passed, else WORLD-INVALID. All required.
- T-K11 (M3-E10-W1 orphan poisoning). PASS iff HIT 0,1,2 and probe
  3 == 65113. Validity: HIT fails -> WORLD-INVALID.
- T-K12 (M3-E10-W2 chained propagation). PASS iff HIT 0,1,2,3,4 and
  probe 5 == 66116. Validity: HIT fails -> WORLD-INVALID.
- T-K13 (M3-E10-W3 specificity). PASS iff HIT 0,1,2,3 and probe 4
  == 67113 and probe 5 == 67103. Validity: HIT fails ->
  WORLD-INVALID.
- T-K14 (retention). PASS iff at least 9 of the following 12
  collateral probes return their prereg-expected taught values:
  m1w2 idx4, idx5; m1w3 idx3, idx4; m2w2 collateral 62091/62500 and
  62092/62500; m2w3 collateral 62091/62500 and 62092/62500; m3w1
  idx4, idx5; m3w2 idx6, idx7.
- T-K15 (no-leak audit, retrieval-based). PASS iff (a) the T-K4 grep
  over frozen cognition sources finds zero tokens in 60000-69999;
  (b) the scorer mechanically verifies that no M1 or M3 bar probe's
  (s,r,expected) matches an OBSERVE-taught triple for the same
  (s,r) with the expected object in its world file (a match makes
  the world WORLD-INVALID: the bar would be retrieval-passable);
  the M2 hidden-phase final probes are exempt from (b) because they
  are scored as informant selection via the sealed driver log, and
  that exemption is recorded here; (c) the per-world mechanism
  walks in section 6 document the no-data-path / oracle-proof
  argument for every bar probe.

### Predicted bar outcomes (recorded before execution)

T-K1, T-K2, T-K3, T-K4, T-K14, T-K15: predicted PASS (process bars).
T-K5: predicted FAIL (engagement 2/2 PASS; nesting 0/2).
T-K6: predicted FAIL (engagement 2/2 PASS; chained join 0/2).
T-K7: predicted FAIL (engagement 2/2 PASS; probe2 60399, not -2).
T-K8: predicted FAIL ((a) PASS; (b) 0/6; (c) PASS; (d) 0/3;
(e) PASS; (f) 1 distinct FAIL).
T-K9: predicted FAIL ((a) PASS; (b) 12 > 6; (c) 0/4; (d) 0 keys;
(e) vocab-verify PASS).
T-K10: predicted FAIL ((a) PASS; (b) 0/4; (c) PASS; (d) 1 distinct
FAIL; (e) vocab-verify PASS).
T-K11: predicted FAIL (validity 3/3 PASS; probe3 65103, not 65113).
T-K12: predicted FAIL (validity 5/5 PASS; probe5 66106, not 66116).
T-K13: predicted PASS (validity 4/4; specificity probes correct).

### 7.5 Pre-freeze index audit (the m2e3.barspec typo lesson)

Before freezing, the author counted QUERY lines per world file
specification and verified every probe index named in section 7
against that count: m1w1 4 probes (idx 0-3): T-K5 names 0,1,2,3 OK;
m1w2 6 probes: T-K6 names 0,1,2,3 OK; m1w3 5 probes: T-K7 names
0,1,2 OK; m3w1 6 probes: T-K11 names 0,1,2,3 OK; m3w2 8 probes:
T-K12 names 0-5 OK; m3w3 8 probes: T-K13 names 0-5 OK; T-K14 names
m1w2 4,5 / m1w3 3,4 / m3w1 4,5 / m3w2 6,7, all within range OK. M2
bars reference driver-logged phases, not static probe indices; the
driver asserts phase counts at runtime (fail-closed).

## 8. Execution protocol and tools

### 8.1 Tools (all pure Zag, pinned znc; built AFTER this prereg freezes)

- `e10_score.zag`: adapted from E9's `e9_score.zag` (verbatim logic):
  argv [worldfile, transcript, barspec, nullval, inqval]. Parses
  QUERY (s,r,e) and ANSWER (s,r,v) 1:1 in order; parses CHOICE lines;
  evaluates HIT/NEED/CHOICE directives; prints per-probe lines and
  the bar verdict. Exits nonzero on WORLD-INVALID or bar FAIL.
- `e10_score_m2w1.zag`: argv [transcript, driverlog, truthsfile,
  vocabfile]. Evaluates T-K8 sub-bars (a)-(f) from the driver log
  (ACT lines with informant tags), the transcript (final hidden
  probes vs truths), and the sealed PI. Prints sub-bar results and
  the verdict.
- `e10_score_m2w2.zag`: argv [transcript, driverlog, truthsfile,
  vocabfile, nullval, inqval]. Evaluates T-K9 sub-bars (a)-(e):
  non-NULL ACT counts and early stops from KEYDONE lines, final
  probes vs truths, vocab-verify line check.
- `e10_score_m2w3.zag`: argv [transcript, driverlog, truthsfile,
  vocabfile]. Evaluates T-K10 sub-bars (a)-(e) with per-episode PIs
  applied by the driver (INF tags already episode-correct).
- `degen.zag`: copied from E9 (verbatim logic): argv [worldfile,
  outtranscript, policy]. Generates degenerate transcripts D0/D1/D2
  for the 6 static worlds; each is scored by e10_score.zag against
  the world's barspec; all must FAIL or INVALID, none may PASS.
- `inspect_state.zag`: copied from E9 (diagnostic only): prints
  MAP/UNCERT/GUIDE summaries from a state.bin. Never part of a bar
  (correction 3).
- `e10_m2_driver.sh`: deterministic bash driver (safebin tools only)
  implementing sections 6.4, 6.5, 6.6; sealed PIs embedded at
  generation time from the section 8.2 derivation; writes the grown
  world file, transcript, driver log, truths file, and vocab file.
  Any vocab-verify mismatch aborts with nonzero exit
  (WORLD-INVALID, fail-closed).

### 8.2 Sealed PI derivation (after freeze, before generation)

1. Compute H = sha256sum(PREREG_E10.md).
2. W1: idx = H[0] mod 6; PI = PERM_TABLE[idx] (public table, same
   six permutations E9 used: 0: 1->A 2->B 3->C | 1: 1->A 2->C 3->B |
   2: 1->B 2->A 3->C | 3: 1->B 2->C 3->A | 4: 1->C 2->A 3->B |
   5: 1->C 2->B 3->A).
3. W2: bit = H[1] mod 2; PI = [{1->A,2->B},{1->B,2->A}][bit].
4. W3: bit_a = H[2] mod 2 over [{1->A,2->B},{1->B,2->A}] (episode A);
   bit_b = H[3] mod 2 over [{1->A,2->C},{1->C,2->A}] (episode B).
5. Record H, all PIs, in WORLD_MANIFEST.sha256. The derivation is
   mechanical (shell arithmetic); the selection is sealed because it
   is not in the prereg text.

### 8.3 Block driver (deterministic shell)

Per block run: remove any prior state.bin; for W1..W3 in order run
`freeze_shim2_bin <world> <state.bin>` (exit code 0 required), saving
stdout as the transcript. For M2 worlds the driver grows the world
per sections 6.4-6.6 and saves transcript + driver log + vocab file
+ truths file. After the block, run the inspector on the final
state.bin (diagnostic). Repeat 3 times; compare sha256 across runs
(T-K2).

### 8.4 Anti-smuggling and manifest

At generation: sha256 manifest of all world/template/truth/driver/
barspec/perm/vocab files. Before execution: grep the frozen
cognition sources for 60000-69999 (T-K4). Hash re-verification of
the shim binary before each block run and after the battery (T-K3).

## 9. Verdict rules

- M1 MECHANISM-STRONG iff T-K5 and T-K6 and T-K7 all PASS; else
  M1 MECHANISM-WEAK (kill evidence: the failed sub-bars).
- M2 MECHANISM-STRONG iff T-K8 and T-K9 and T-K10 all PASS; else
  M2 MECHANISM-WEAK.
- M3 MECHANISM-STRONG iff T-K11 and T-K12 and T-K13 all PASS; else
  M3 MECHANISM-WEAK.
- Any process-bar (T-K1..T-K4, T-K14, T-K15) failure VOIDs the
  battery; a void battery is re-sealed and re-run, never interpreted.
- No verdict beyond the mechanism: no generality claim, no L3 claim,
  no cross-battery aggregation. See section 10.

## 10. Criterion 0 status (binding; no L3 claim on any pass)

This battery tests whether frozen, researcher-authored mechanisms
generalize to fresh structures. It does not test representational
invention:

- C0-A (runtime-defined semantics): NOT MET. The exercised semantics
  (trial-loop assemblers, constant guide action, single-schema patch)
  are researcher-authored machinery in the frozen source.
- C0-B (open structural form): NOT MET. Every world's tested form is
  enumerable from its demonstrations before the run.
- C0-C (multiple unforeseen forms, independent post-freeze
  adversary): NOT MET. Nine worlds across nine families, designed
  post-freeze, but the adversary role is played inside the same
  research loop. A second battery by a genuinely separate adversary
  is required before any L3-adjacent claim.
- C0-D (cognitive reuse): NOT MET as a criterion. Collateral probes
  measure retention, which is evidence toward a future C0-D case, but
  a single battery's probes are explicitly insufficient.

Consequence: no score on this battery, however high, may be described
as L3, L3-adjacent, or progress toward L3 without a separate
Criterion 0 case on independent evidence. The strongest honest claim
available is about the generality of M1, M2, M3 as frozen mechanisms.

## 11. What a FAIL means

Per the standing no-patch-treadmill rule, an expected FAIL is evidence
about what the frozen core is missing, not a request for a patch. The
results document clusters failures by shared architectural cause and
proposes general substrate hypotheses; benchmark-specific handlers and
per-world opcodes are rejected in advance.
