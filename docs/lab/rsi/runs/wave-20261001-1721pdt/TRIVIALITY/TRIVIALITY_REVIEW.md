# TRIVIALITY REVIEW: Post-Freeze Sealed Adversarial Battery on TNN-2

Wave: wave-20261001-1721pdt, lane TRIVIALITY.
Date: 2026-10-01.
Reviewer role: attack the battery itself, not the mechanisms.
Documentation rule observed: no em-dashes in this file.

## 1. Scope and method

The sealed battery (executed wave-20261001-1421pdt, lane sealed_adv)
killed all three TNN-2 mechanisms: M1 no procedure abstraction,
M2 constant inquiry action 30, M3 last-write-wins patching. This review
asks whether the battery deserved to kill them: were the nine worlds
calibrated to discriminate mechanism competence from degeneracy, or
were they too easy, too hard, or miscalibrated in a way that voids
the evidential value of the kills.

Method: document review of the frozen prereg, the sealed world files,
the transcripts, and the result record, plus independent re-verification
of every identity and integrity claim I rely on (hashes, manifest,
determinism, binary identity, white-box state). No new experiments were
needed; all verification programs used were the battery's own frozen
Zag artifacts. Pure-Zag and toolchain-guard rules were observed
(see NAMECHECK.md Step 0).

## 2. Record located and independently verified

- Prereg: `docs/lab/rsi/runs/wave-20261001-1421pdt/sealed_adv/SEALED_BATTERY_PREREG.md`.
  I recomputed its SHA-256: `b5d54f4d92585840febf58e875a8e6aff0e23a0c88b795faa5bed002c6de8590`,
  matching the hash recorded in RESULT_SEALED_ADV_BATTERY.md. Filesystem
  mtimes confirm ordering: prereg 21:41 UTC, world files first created
  21:42:55 UTC. The prereg is unmodified since freeze.
- Worlds: `m1w1_world.txt` through `m3w3_world.txt`, plus
  `m2w1_template.txt` / `m2w1_truths.txt`. I ran `sha256sum -c` against
  `WORLD_MANIFEST.sha256`: all 10 files OK. I diffed `m1w1_world.txt`
  line by line against prereg section 3.1: exact match. The M2-W1 grown
  world file matches the prereg's interactive protocol (bias seeds,
  calibration ACT/truth/probe per key, inquiry probe/2 ACTs/probe per
  hidden key).
- Transcripts: 3 runs per block. I spot-checked sha256 equality across
  runs for `m1_run*_w1.txt` (all `c4a517b1...`) and `m3_run*_w2.txt`
  (all `b9a490e4...`): byte-identical, confirming K-S2.
- Frozen binary identity (re-verified by me, not taken on trust):
  `tnn2_build/tnn2.zag` hashes to `a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd`,
  `core_freeze_tnn2_shim/freeze_shim2_bin` hashes to
  `9217054c5af6dec057c4530c4de3ba246f521acc6df741d1989a4504acc72954`,
  both exactly as preregistered. `git status` on both cognition paths
  is clean. The K-S4 grep hit (`41024`) is confirmed benign: it is
  `fn eoff(e:i32) { return 41024+e*16; }` in the frozen source (present
  identically in both `tnn2.zag` and `freeze_shim2.zag`), a pre-freeze
  edge-block byte-offset constant used only in address arithmetic,
  never as a world id. No world id token (40000-49999) appears in
  cognition source.
- White-box failure evidence (re-verified by me): I ran the battery's
  own `inspect_state_bin` against `m3_state_run1.bin`. Output shows
  `MAP s=42101 r=42501 ans=42110 LITS 42110` (singleton noise
  incorporated), `MAP s=42102..42104` with x+5 literals (systematic
  incorporated), `MAP s=43101 r=43509 ans=43109 LITS 43102 43109`
  (second contradiction silently no-oped; first revision's literal
  persists), `MAP s=43701 r=43809 ans=43703 LITS 43703` (revert left
  the stale taught fact), and `UNCERT` nodes on 42105/42106 (no
  generalization). This matches the result record exactly and is
  learner-state evidence from the verified frozen binary, not a
  harness artifact: the shim is zero-cognition transport
  (OBSERVE to OBSERVED, QUERY to ANSWER, ACT to CHOICE), and the
  transcripts show the mechanical mapping with all behavioral
  signatures (8x ANSWER -2 with decoy memorization; constant
  CHOICE 30; literal patching) originating learner-side.
- The 0821 AB1-AB3 prereg exists at the cited path and its AB1
  (novel two-procedure composition) and AB2 (flattery-trap inquiry)
  match the adoption claim; the two executor amendments are frozen
  in the 1421 prereg before any world file existed.

Process integrity verdict: the seal, the freeze, the determinism,
and the binary identity all check out independently. Whatever is
wrong with this battery is in its design, not its execution.

## 3. Per-world calibration analysis

For each world I ask three questions. (i) Would a trivial degenerate
policy pass? (ii) Would a competent-but-imperfect mechanism
necessarily fail? (iii) Do the bars engage the claimed competence,
or are they coupled to the frozen implementation's internals?

### M1-W1: novel P-then-Q composition

Bar K-S5 is conjunctive: (a) 7/8 composition probes, (b) 4/4 decoy
probes return the consistent majority structure, (c) white-box MAP
with DEP-licensed facts from both demo blocks.

- (a) is well calibrated. Composing two demonstrated procedures into
  a never-demonstrated P-then-Q form is a fair operationalization of
  "runtime executable-graph construction". A memorizer or
  path-follower scores 0; a genuine constructor scores 8/8; 7/8
  allows one slip.
- (b) is miscalibrated. It demands the consistent majority
  (40801/40802/40803/40804) on the noisy instance 40105 rather than
  the taught swapped values. A mechanism that abstracts P and Q
  correctly but reports observations faithfully would return the
  taught swaps and FAIL (b). The bar encodes a designer preference
  (abstraction over faithful retrieval) that is not entailed by
  procedure competence. Worse, it contradicts this battery's own
  M1-W2 collateral probes: the identical triple (40105,40501)
  expects 40801 in W1 and 40802 (the taught swap) in W2, with
  persistent state carried across the two worlds. No single learner
  trajectory can satisfy both bars: a learner that passed K-S5(b)
  would fail W2's collateral, and vice versa. The frozen mechanism
  happened to memorize the swap, so it passed W2 collateral while
  failing W1 decoys, but the design defect is real and would punish
  a competent learner either way.
- (c) is implementation-coupled. It demands a MAP node with
  DEP-licensed facts from both demo blocks: the frozen mechanism's
  specific internal representation. A competent constructor with a
  different internal representation (no MAP/DEP vocabulary) would
  necessarily fail (c), so K-S5 as a conjunctive bar is unpassable
  except by the frozen implementation family.

World verdict: MISCALIBRATED. The mechanism's actual failure (0/8
on (a), confirmed in transcript `m1_run1_w1.txt`: 8x ANSWER -2) is
genuine and sufficient to kill M1 on this world, but bars (b) and
(c) are defective and must not be reused as designed.

### M1-W2: backward traversal of demonstrated chains

Bar K-S6: 3/4 backward probes correct; validity requires 2/2
forward engagement probes.

- A degenerate always -2 policy fails (validity would also fail).
  A forward-only path-follower passes validity and fails the bar,
  which is exactly the discrimination intended: the world isolates
  direction as the single change from FW1's forward 3-hop shape.
- A competent constructor with invertible procedures passes 4/4;
  3/4 allows one slip. No degenerate policy passes. The bootstrap
  analysis (only 2 facts on 41409 at backward-probe time, below k=3,
  not invariant) closes the invariant-relation loophole honestly.
- One could argue a forward-only constructor is still "a
  constructor", making invertibility a stronger demand than the
  mechanism's name implies. But the prereg documents this as the
  adversarial intent against path-following, and direction
  independence is a reasonable reading of generic graph
  construction. Not unfair.

World verdict: CALIBRATED.

### M1-W3: composition over a shared step (diamond)

Bar K-S7: 2/3 shared-composition probes; validity requires the
engagement probe.

- Clean discrimination: a memorizer fails (novel subject 41606,
  no facts, bootstrap not invariant), a step-identity-aware
  constructor passes, 2/3 allows one slip. The diamond topology
  is genuinely different from FW2's linear replay and from M1-W1's
  disjoint composition. No degenerate policy passes; no competent
  constructor is excluded.

World verdict: CALIBRATED.

### M2-W1: inquiry under asymmetric cost with flattery trap

Bar K-S8: (a) engagement, (b) at least 70 percent of 8 inquiry
ACTs target informant A (CHOICE 1), (c) at most 1 ACT targets
informant C (CHOICE 3), (d) at least 3/4 final hidden probes
correct, (e) budget of 8 respected.

- Critical finding: a trivial degenerate policy, always emit
  CHOICE 1, PASSES K-S8 outright. Walk: calibration ACTs consult
  A (truthful); inquiry ACTs (8x CHOICE 1) consult A on every key;
  A's answers teach the truths, so all 4 final probes are hits.
  (a) engagement passes (ACTs follow -2 probes); (b) 8/8 to A;
  (c) 0 to C; (d) 4/4; (e) 8 within budget. The world's fixed,
  prereg-documented mapping (CHOICE 1 to A, always) means the bar
  cannot distinguish "uncertainty-guided informant selection" from
  "hardcoded choose-1". The flattery trap, the asymmetric cost,
  and the calibration phase are all defeated by a one-line
  constant policy.
- On difficulty: the 70 percent bar leaves only 2 exploratory
  ACTs for identifying A among three informants, since the
  calibration phase structurally cannot support identification
  (no misses occur there: truths are taught before probes, so no
  guides exist and calibration ACTs are CHOICE 0 by the
  mechanism's own logic). A competent explorer can still pass
  with a 2-explore/6-exploit split given the deterministic
  informant mapping, so the bar is tight but not impossible.
  However, tightness is moot given the degenerate pass above.
- The driver log confirms the frozen mechanism's actual behavior
  (4x CHOICE 0 in calibration, 8x CHOICE 30 mapped to NONE in
  inquiry, 0/4 hidden probes), which is a genuine mechanism
  failure. But the world does not test what it claims to test.

World verdict: MISCALIBRATED (degenerate-passable). The M2 kill
on this world is evidentially weak: the world cannot tell the
frozen mechanism's failure apart from a competent mechanism, nor
a competent mechanism apart from always-1.

### M2-W2: stale guide persistence after resolution

Bar K-S9: post-resolution ACT emits CHOICE 0; validity requires
the pre-resolution ACT to emit CHOICE 30.

- The transcript shows the exact predicted signature: pre
  CHOICE 30, post CHOICE 30, collateral 2/2. A resolution-capable
  mechanism emitting the mechanism's own no-guide vocabulary (0,
  established in M2-W1 calibration) passes; always-0 fails
  validity (WORLD-INVALID, not a pass); always-30 fails the bar.
  The distractor flush plus re-QUERY design cleanly isolates guide
  lifecycle from retrieval. No degenerate policy passes.
- Caveat: the validity gate (pre-resolution ACT must be 30) is
  coupled to the frozen mechanism's signature. A different
  competent mechanism with its own inquiry vocabulary would be
  ruled WORLD-INVALID rather than scored. Acceptable for a sealed
  test of the frozen target; limits reuse.

World verdict: CALIBRATED (for the frozen target).

### M2-W3: discriminating action content across uncertainties

Bar K-S10: the three episode CHOICEs pairwise distinct; validity
requires 3x ANSWER -2.

- The transcript shows 30, 30, 30 with 3x -2 validity met: the
  exact hardcoded-constant signature. The distractor flush
  between episodes isolates the content question (each ACT fires
  only the current guide). A content-bearing action policy passes;
  the constant policy fails. No trivial degenerate policy passes
  (a fixed rotating sequence would, but that is not a plausible
  degenerate policy for this mechanism class, and random emission
  is outside the threat model).
- Caveat: the bar tests the strong form of the claim. The three
  uncertainties are structurally near-identical (differing only
  in subject/relation ids), so a competent mechanism with a
  generic type-level inquiry action ("I have an unresolved guide")
  would fail while a subject-encoding one passes. The prereg
  documents this as the intent (the L3 link is the constant under
  test), so the strength is deliberate, not accidental.

World verdict: CALIBRATED, with the strong-form caveat noted.

### M3-W1: singleton vs systematic revision with delayed reuse

Bar K-S11 is conjunctive: (a) 2/3 systematic, (b) singleton probe
returns the original law 42104, (c) 1/2 generalization probes,
(d) white-box MAP with a SETREG literal, (e) 6/6 interference.

- The black-box bars are the best-designed in the battery. (b)
  defeats last-write-wins and any recency heuristic (the most
  recent observation for 42101 is the uncorrected singleton
  42110, which fails). (c) defeats per-instance patching (unseen
  subjects 42105/42106 have no data path to x+5). A degenerate
  always-last-write policy passes (a), (d), (e) but is killed by
  (b) and (c): the world discriminates exactly as intended.
- (c) is a strong demand: it requires law-level revision, so a
  competent per-instance evidence-weighted reviser would fail it.
  The prereg documents this as deliberate (EXECUTOR-AMENDMENT-2
  added the generalization probes to separate law revisers from
  per-instance patchers). Strong but honest; recorded here so a
  future reader does not mistake (c) for a test of revision in
  general.
- (d) is implementation-coupled: it demands a SETREG literal in
  the live MAP graph, i.e., the frozen mechanism's internal
  representation. A competent reviser with different internals
  necessarily fails the conjunctive bar.
- The transcript confirms the genuine mechanism failure:
  singleton incorporated (42110), systematic incorporated
  (42107/42108/42109), 2x -2 on generalization, 6/6
  interference; my independent inspector run confirms the
  white-box state.

World verdict: CALIBRATED on the black-box bars, which drive the
verdict; sub-bar (d) is implementation-coupled and should be
demoted to a diagnostic in future batteries.

### M3-W2: revision of a revision

Bar K-S12: post-second-contradiction probe returns 43119;
validity requires the promotion (43103) and post-first-revision
(43109) probes correct.

- Critical finding: a trivial degenerate policy, recency-echo
  ("answer the object of the most recent OBSERVE event"), PASSES
  K-S12. Stream walk: after OBSERVE 43102 43502 43103, both
  promotion probes see most-recent 43103 (expected 43103, pass);
  after OBSERVE 43102 43502 43109, the probe sees 43109
  (expected 43109, pass); after OBSERVE 43102 43502 43119, the
  bar probe sees 43119 (expected 43119, PASS). No OBSERVE
  intervenes between the second contradiction and the bar probe,
  so the expected value is identical to the most recent
  observation. The world therefore cannot distinguish "revises
  to the latest evidence" from "parrots the latest observation":
  it provides zero evidence that any revision occurred. The
  frozen mechanism failed only because of its specific
  silent-no-op bug (confirmed: MAP ans=43109, LITS 43102 43109),
  not because the world tests revision.
- Contrast M3-W1, whose singleton and generalization probes do
  defeat recency-echo. Within the M3 block, W1 is the calibrated
  discriminator; W2 is not.

World verdict: MISCALIBRATED (degenerate-passable).

### M3-W3: reverted revision blocks relearning

Bar K-S13: post-revert probe returns 43713; validity requires the
promotion probes to return 43703.

- Same defect as M3-W2. Stream walk: promotion probes follow
  OBSERVE 43702 43802 43703 (most-recent 43703, expected 43703,
  pass); the bar probe follows OBSERVE 43711 43802 43713
  (most-recent 43713, expected 43713, PASS under recency-echo).
  Again the expected value equals the most recent observation,
  so a parrot passes and the world tests only the frozen
  mechanism's specific revert-veto bug, not revision competence.
- The transcript confirms the genuine bug signature (probe
  returns 43703; MAP ans=43703, LITS 43703 unchanged), but the
  bar cannot tell that bug from competence-in-general.

World verdict: MISCALIBRATED (degenerate-passable).

## 4. Cross-cutting checks

### (a) Material difference from FW1-FW9

Verified against `freeze_worlds_v2/WORLD_DESIGN.md`. All nine
worlds are materially different from FW1-FW9, and id blocks are
disjoint (40000-49999 vs 30000-39999; I grepped all world files:
zero 3xxxx ids). The separations:

- M1-W1 vs FW2: FW2 replays one demonstrated 5-step procedure on
  novel instances (tested form equals demonstrated form); M1-W1
  never demonstrates the tested P-then-Q form. Composition vs
  replay: different demand.
- M1-W2 vs FW1: FW1 tested forward 3-hop composition; M1-W2
  isolates direction (backward probes on the same shape).
- M1-W3 vs FW2: diamond topology with a shared step vs linear
  5-step replay.
- M2-W1 vs FW6: FW6 rewards a literal CHOICE 0 contract plus
  recall; M2-W1 has no correct literal choice and scores only
  information gain via informant selection. (That M2-W1 is
  degenerate-passable is a separate defect; it is not an FW6
  variant.)
- M2-W2 vs FW6: temporal guide lifecycle with no informants vs a
  single diagnostic round.
- M2-W3 vs FW6/FW7: action-content discrimination across
  episodes; FW6/FW7 never varied the uncertainty.
- M3-W1 vs FW5: FW5's bar REQUIRES last-write-wins incorporation
  (B1: 3/3 return the corrected 999) under eviction pressure;
  M3-W1's bar PUNISHES it (singleton must be rejected) and adds
  generalization. Opposite demands on the same operator: the
  worlds probe different properties, and the tension is
  legitimate adversarial design, not duplication.
- M3-W2 vs FW5: sequential double revision of one link vs single
  contradictions.
- M3-W3 vs FW4/FW5: a failed revision that vetoes relearning vs
  retention under pressure.

The "no trivial FW1-FW9 variants" order was honored.

### (b) Mechanism vs harness artifact

The failure evidence is about the mechanisms, not the harness:

- Binary identity independently re-verified (hashes match the
  prereg exactly; git clean on cognition paths).
- The shim is zero-cognition transport; transcripts show the
  mechanical OBSERVE/QUERY/ACT mapping, with every behavioral
  signature originating learner-side.
- White-box state independently reproduced by me with the
  battery's own inspector on the final state bins; the MAP
  answers, SETREG literals, and UNCERT nodes match the result
  record exactly.
- Determinism independently spot-checked (byte-identical
  transcripts across all 3 runs for sampled worlds).

The kills are real kills of the frozen mechanisms. What is in
question is only whether the worlds were fair tests, not whether
the runs happened as recorded.

## 5. Verdicts

Per-world:

- M1-W1: MISCALIBRATED. Bar (a) is calibrated and the 0/8
  failure is genuine, but bars (b) and (c) are defective:
  (b) penalizes faithful retrieval and contradicts M1-W2's own
  collateral expectations for the identical triple; (c) is
  coupled to the frozen MAP/DEP internals.
- M1-W2: CALIBRATED.
- M1-W3: CALIBRATED.
- M2-W1: MISCALIBRATED. Degenerate always-CHOICE-1 passes K-S8;
  the world cannot discriminate uncertainty-guided inquiry from
  a hardcoded constant.
- M2-W2: CALIBRATED (for the frozen target; validity gate is
  implementation-coupled, noted as a reuse limit).
- M2-W3: CALIBRATED (tests the strong form of the claim by
  documented intent).
- M3-W1: CALIBRATED on the black-box bars (the singleton and
  generalization probes genuinely defeat recency and
  per-instance patching); white-box sub-bar (d) is
  implementation-coupled and should be a diagnostic.
- M3-W2: MISCALIBRATED. Recency-echo passes K-S12; the bar
  probe's expected value equals the most recent observation, so
  the world supplies no evidence of revision.
- M3-W3: MISCALIBRATED. Same recency-echo defect in K-S13.

Overall battery verdict: MISCALIBRATED.

This is not TRIVIAL: five worlds (M1-W2, M1-W3, M2-W2, M2-W3,
and M3-W1's black-box bars) are genuinely discriminating, the
process integrity is independently confirmed, and the three
mechanism kills stand on real learner-state evidence from the
verified frozen binary. The battery says something true: M1
cannot compose, invert, or share steps; M2 cannot discriminate,
retire, or content-encode inquiry; M3 incorporates noise, stalls
on second contradiction, and vetoes relearning after revert.

But three of nine world bars are degenerate-passable and two
white-box sub-bars are implementation-coupled, so the battery as
a scoring instrument is miscalibrated. In particular: the M2
family verdict rests partly on M2-W1, which cannot distinguish
competence from always-1; and the M3-W2/W3 kills, while true of
the frozen mechanism's specific bugs, were measured by bars a
parrot would pass. A future battery must apply the corrections
below before its scores are trusted as generality evidence.
None of these corrections is a mechanism repair.

## 6. Required battery-design corrections (not mechanism repairs)

1. M2-W1 (informant mapping): seal a per-run (or per-key)
   permutation of the informant to CHOICE mapping, revealed only
   through calibration-phase exploration. A fixed mapping lets
   always-1 pass; a sealed permutation defeats every constant
   policy while remaining fair to a genuinely discriminating
   mechanism. Alternative: score information gain directly and
   require cross-key exploration before exploitation.
2. M3-W2 and M3-W3 (recency confound): insert distractor
   OBSERVEs on unrelated ids between the final contradiction
   (W2) or the new-link teaches (W3) and the bar probe, so the
   expected value differs from the most recent observation. A
   revision bar must require the answer to differ from what a
   no-revision recency heuristic would emit; otherwise the world
   tests nothing.
3. K-S5(c) and K-S11(d) (white-box coupling): restate
   white-box bars in representation-neutral terms (e.g.,
   "a persistent structure whose licensed evidence includes
   both demo blocks") or demote them from the conjunctive bar
   to diagnostics. Bars that name MAP, DEP, or SETREG are
   unpassable by any implementation except the frozen one.
4. M1-W1 decoy vs M1-W2 collateral (cross-world inconsistency):
   make expectations consistent across the persistent state
   chain. Either both expect the taught values (and the decoy
   bar tests something else, e.g., explicit conflict marking),
   or collateral compares against the learner's own W1 answers
   rather than a fixed truth. Two bars must never demand
   different answers to the identical triple from one learner
   trajectory.
5. K-S8(b) tightness (minor): the 70 percent bar leaves exactly
   2 exploratory ACTs, because the calibration phase cannot
   support informant identification (no misses, hence no guides,
   hence CHOICE 0). Either document the 2-explore budget as the
   intended demand or lower the bar to tolerate cautious
   re-verification. Do this together with correction 1.
6. For reuse beyond the frozen target: decouple validity gates
   from the frozen action vocabulary (K-S9's required 30,
   K-S8's CHOICE 1/2/3 mapping). A sealed battery for a future
   mechanism should score vocabulary-neutral behavior
   (e.g., "the post-resolution action differs from the
   pre-resolution inquiry action and matches the mechanism's own
   declared null action") rather than hardcoded integers.

## 7. What the battery got right (for the record)

Prereg discipline (hash before worlds, unmodified after),
byte-identical determinism across 3 runs, seal integrity with a
documented benign grep hit, oracle-proofing analysis, validity
gates that prevent scoring unengaged worlds, within-block
collateral retention design, the M3-W1 singleton/generalization
discrimination (the strongest single world design in the
battery), and the M2-W2/W3 isolation of lifecycle and content.
The execution was clean; the defects are all in bar design.
Future batteries should keep the process machinery and fix the
six items above.
