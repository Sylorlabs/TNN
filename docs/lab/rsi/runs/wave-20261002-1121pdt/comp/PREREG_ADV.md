# PREREG_ADV: adversarial testing of the unified `satisfy` composition operation

Wave: wave-20261002-1121pdt. Lane: COMP. Branch: lane-comp-20261002-1121pdt.
Frozen: 2026-10-02 (this commit contains ONLY this file).
Status: FROZEN. Implementation must follow this spec exactly. Any design
change requires transparent amendment and re-freeze, never silent edit.

## 0. Question

The 0521pdt COMP verdict kept `satisfy` (patch_d.zag) as the single
composition operation: BUILD-PASS, 12/12, KB6 PARTIAL on the trial-path
confound, no L3 claims. This wave attacks `satisfy` adversarially:

(a) ADV-A breaker families: adversarial problem families designed to
    break composition through the single operation, including cases
    where trial-path reuse would silently leak the answer.
(b) A trial-path-free evaluation battery: sealed worlds where no
    trial/answer path from training can reach the eval goal.
(c) One post-freeze adversary family (PF-1, diamond DAG topology),
    designed AFTER this freeze, with materially different structure
    from the sealed eval. Its design is recorded in a separate
    commit after the freeze point; it is scored separately.

The mechanism under test is FROZEN (0521pdt patch_d.zag, SHA recorded
in KB2). This wave builds no new mechanism and changes no mechanism
code. A BUILD-PASS here faces the probe-menu/source-audit adversarial
check (KB5) before any promotion.

## 1. Mechanism under test (frozen, source-audited 2026-10-02)

`satisfy` = recursive goal-part satisfaction (patch_d.zag, 350 lines,
299 code lines, 7 fns). Pipeline: activate -> satisfy -> trial ->
bootstrap. No compose stage, no compose flag, no rebind stage.

- d_satisfy (supervised, expected >= 0): k0 from 4 down to 1
  (longest-applicable-prefix first), MAP id order, t2_gather grounding
  order; first terminal == expected wins; full backtracking across
  MAPs, prefix lengths, groundings; depth bound 8 (learner policy
  header, default 8); visited-value cycle guard. Emits SAT-SEGS on
  successful assemble+promote (LINK14 provenance to used MAPs).
- d_fixpoint (unsupervised, expected < 0): GREEDY, no backtracking.
  Longest applicable prefix wins; ties by lowest MAP id, then gather
  order; commits to the first novel terminal; stops at fixpoint or
  12 iterations. Emits SAT-FIX on promote.
- Shared substrate trial path (t2_trial, runs only if satisfy fails):
  assembles taught fact paths of k = 2..4 edges, verifies vs expected;
  plus sum/count fallbacks (t2_asm_sum over single-fact values from s,
  t2_asm_count over same-rel chains). Trial promotion adds NO type-14
  edges; satisfy promotion always adds LINK14 edges to used MAPs.
- t2_gather: BFS from s, cap 96 paths, max 4 edges, fact-id order,
  within-path cycle guard.

Known properties exploited by the breakers: greedy unsupervised has
no backtracking (B3U, PF-1c); supervised selection among multiple
valid compositions is entirely expected-driven (PM-1); t2_gather
truncates at 96 paths (noted as a bound, not directly attacked).

## 2. Sealed battery (frozen worlds; driver implements exactly these)

Notation: q(s,r,exp) = ev_query. Training protocol (all tests): ev_teach
component facts; query each component on a novel relation (71, 72, ...)
which promotes one MAP per component via trial; 30 gap-noise facts
(5000+i, 60+(i%10), 6000+i) unless noted; teach goal facts; query goal
on novel relation 70. Fresh workspace per test (and per PM-1 leg).
The driver never names which MAPs to use. PASS/FAIL is mechanical.

### 2.1 Trial-path-free battery

Trial-path-free means: no taught fact path of 2..4 edges from the query
subject executes to the expected terminal (t2_trial's chain reach), no
subset-sum of single-fact values from the subject equals expected, and
no same-rel count equals expected. Verified by construction below and
by the mechanism-attributing criteria (SAT-SEGS/SAT-FIX marker presence
plus composite relseq/terminal extracted with the mechanism-neutral
dv_relseq copy). If satisfy fails and trial rescues, the criterion
scores FAIL (no marker or wrong relseq), so a trial leak cannot be
miscounted as a satisfy win.

- TPF-1 LONG-11: X=[1,1] (11-12-13, rel 71), Y=[2,2] (21-22-23, rel 72),
  W=[3,3,3] (31-32-33-34, rel 73). Z (11 edges): 101-1->102-1->103-2->
  104-2->105-3->106-3->107-3->108-1->109-1->110-2->111-2->112.
  q(101,70,112). Trial: 2..4-edge paths from 101 end at 102..105;
  none is 112; sums from {102} are 102; counts are small ints.
  PASS iff ans==112 AND SAT-SEGS present in the log AND the newest
  rel-70 MAP has extracted relseq [1,1,2,2,3,3,3,1,1,2,2] (11 entries)
  AND its terminal value == 112.
- TPF-2 LONG-11-DISTRACT: TPF-1 world plus 40 distractor facts
  (101+(i%8), 1+(i%3), 9100+i), i=0..39, taught AFTER the Z facts
  (D4 pattern). q(101,70,112). Same PASS criterion as TPF-1.
- TPF-3 UNSUP-LONG: TPF-1 world (no distractors). q(101,70,-1).
  PASS iff a rel-70 composite is promoted with extracted relseq
  [1,1,2,2,3,3,3,1,1,2,2] AND terminal == 112 AND SAT-FIX present.
  (No expected answer exists for anything to leak through.)

### 2.2 Adversarial breaker battery

- B1 DEEP-DISTRACT (depth-boundary robustness): X=[1,1] (71),
  Y=[2,2] (72). Distractor taught FIRST: (103,2,904) then
  904-2->906-2->908-2->910-2->912-2->914-2->916-2->918-2->920
  (9 edges, rel 2). Then correct: 101-1->102-1->103,
  (103,2,104), (104,2,105). q(101,70,105). The DFS must walk the
  9-edge distractor branch to depth exhaustion (depth bound 8 hit
  mid-chain), unwind through all k0=1 alternatives, and backtrack
  to the correct grounding. PASS iff ans==105 AND SAT-SEGS present
  AND composite relseq == [1,1,2,2] AND wall time < 120 s.
- B2 CYCLE (visited-guard robustness): X=[1,1] (71), Y=[2,2] (72).
  Facts: 101-1->102-1->103-1->101 (cycle), plus 103-2->104-2->105.
  q(101,70,105). PASS iff ans==105 AND SAT-SEGS present AND
  relseq == [1,1,2,2] AND wall time < 60 s. (A cycle-naive DFS
  would loop forever; the visited guard must terminate it.)
- B3S GREEDY-TRAP-SUPERVISED: X=[1,1,1] (11-12-13-14, rel 71, MAP
  relseq [1,1,1]), Y=[2,2] (21-22-23, rel 72). Distractor taught
  FIRST: (102,1,912), (912,1,913), (913,1,914). Then correct:
  101-1->102-1->103-1->104, (104,2,105), (105,2,106).
  q(101,70,106). The longest-prefix-first ordering tries the
  distractor grounding first at every level; backtracking must
  recover. PASS iff ans==106 AND SAT-SEGS present AND
  relseq == [1,1,1,2,2].
- B3U GREEDY-TRAP-UNSUPERVISED: B3S world. q(101,70,-1). The greedy
  fixpoint commits to the first novel terminal with no backtracking:
  predicted terminal 914 (wrong). PASS iff composite relseq ==
  [1,1,1,2,2] AND terminal == 106. PREDICTED FAIL (breaker wins):
  this test is expected to demonstrate the greedy unsupervised bound,
  not to pass. A PASS falsifies the trap hypothesis (recorded as
  calibration, bars not moved).
- B4 TRIAL-LEAK (attribution negative control): X=[1,1] (71),
  Y=[2,2] (72). Z with an UNCOVERED relation: 101-1->102-1->103-3->
  104-2->105 (rel 3 has no component MAP). q(101,70,105). satisfy
  cannot fire (no MAP covers a rel-3-first path); the shared trial
  path assembles the taught 4-edge path and answers. PASS iff
  ans==105 AND SAT-SEGS ABSENT from the log AND the newest rel-70
  MAP has ZERO type-14 edges (trial promotion adds none; satisfy
  promotion always adds LINK14). A SAT-SEGS marker or a LINK14
  edge here is dishonest attribution and scores FAIL.
- B4U TRIAL-LEAK-UNSUPERVISED (informational, unscored): B4 world.
  q(101,70,-1). The fixpoint is predicted to promote a PARTIAL
  composite (terminal 103). The driver emits T-B4U-ANS, T-B4U-TERM,
  and the composite relseq; RESULT=INFO. Records what unsupervised
  satisfy does when stuck; not a kill bar.
- B5 NO-FACTS (hallucination check): fresh workspace, NOTHING taught.
  q(999,70,105). PASS iff ans==-2 AND no SAT-SEGS/SAT-FIX markers.
- B6 ADVA-REPRISE (0521 ADV-A verbatim rerun on the rebuilt binary):
  X=[1,1] clean; Y=[2,2] clean; distractor (103,2,904) taught FIRST,
  then (904,2,905), then correct 101-1->102-1->103, (103,2,104),
  (104,2,105). q(101,70,105). PASS iff ans==105 AND SAT-SEGS
  present AND relseq == [1,1,2,2]. Provenance check: reproduces the
  0521 sealed result on the rebuilt binary.
- B7 COMB-BLOWUP (computational robustness, the untested
  exhaustive-grounding axis): X=[1,1] (71), Y=[2,2] (72). 40
  distractor chains taught FIRST: chain i (i=0..39): (103,2,C(i,0)),
  (C(i,j),2,C(i,j+1)) for j=0..6, C(i,j)=4000+10*i+j (8 edges each).
  Then correct: 101-1->102-1->103, (103,2,104), (104,2,105).
  q(101,70,105). The DFS must exhaust 40 eight-edge distractor
  subtrees (each walked to depth exhaustion with k0=1 unwind)
  before reaching the correct grounding. PASS iff ans==105 AND
  SAT-SEGS present AND relseq == [1,1,2,2] AND wall time < 300 s.
  A stall is a genuine breaker win (reported as BREAK, the axis
  0521 left untested for A).
- B8 PREFIX-OVERSHOOT (longest-prefix recovery): X=[1,1,1,1]
  (11-12-13-14-15, rel 71, MAP relseq [1,1,1,1]), Y=[2,2] (72).
  Distractor taught FIRST: (103,1,912), (912,1,913), (913,1,914).
  Then correct: 101-1->102-1->103, (103,2,104), (104,2,105).
  q(101,70,105). k0=4 of X matches the distractor path first and
  must be abandoned through k0=3, k0=2 backtracking. PASS iff
  ans==105 AND SAT-SEGS present AND relseq == [1,1,2,2] (proves
  prefix use, not whole-X).

### 2.3 Probe-menu characterization

- PM-1a: X=[1,1] (71), Y=[2,2] (72), Yb=[2,2] (24-25-26, rel 74,
  second MAP with relseq [2,2]). Facts: 101-1->102-1->103,
  (103,2,104),(104,2,105), (103,2,204),(204,2,205). Fresh workspace.
  q(101,70,105). PASS iff ans==105 AND SAT-SEGS present AND
  relseq == [1,1,2,2] AND terminal == 105.
- PM-1b: same world, FRESH workspace. q(101,70,205). PASS iff
  ans==205 AND SAT-SEGS present AND relseq == [1,1,2,2] AND
  terminal == 205.
  Interpretation (either way): two fully MAP-licensed completions
  exist; the expected value selects. A pass on both legs confirms
  expected-driven selection (BOUND on intrinsic preference, not a
  fail). If leg b fails while leg a passes, the first-promoted
  composite shadows alternatives (also a BOUND, reported).

### 2.4 Post-freeze family PF-1 (diamond DAG; designed after freeze)

Designed after this prereg's freeze commit; recorded in a separate
commit that names the freeze point. Materially different structure:
branching/merging DAG, not linear chains.

- PF-1a: A=[1] (11-12, rel 71, MAP relseq [1]), B=[2] (21-22,
  rel 72), C=[3] (31-32, rel 73). Facts: (101,1,102), (101,1,103),
  (102,2,104), (103,2,104), (104,3,105). q(101,70,105). PASS iff
  ans==105 AND SAT-SEGS present AND relseq == [1,2,3].
- PF-1b DIAMOND-TRAP: (101,1,102) taught first but 102's branch is
  dead: (102,2,106); correct: (101,1,103), (103,2,104), (104,3,105).
  q(101,70,105). PASS iff ans==105 AND SAT-SEGS present AND
  relseq == [1,2,3].
- PF-1c (informational, unscored): PF-1b world, q(101,70,-1).
  Greedy fixpoint predicted to commit to the dead branch
  (terminal 106). Driver emits T-PF1C-ANS/TERM; RESULT=INFO.

## 3. Frozen kill bars

- KB1 determinism: bin_adv built 3x from the frozen assembly;
  sha256 equal across builds. The battery run 3x; stdout sha256
  equal across runs. Any mismatch voids the affected results.
- KB2 mechanism freeze: patch_d.zag sha256 ==
  df1d0faa1802a8dc11c1b59f1b8277664308a0f699a3f7f479284a623a80fe82
  (0521 frozen value); full_adv.zag lines 1..2027 (substrate 1..1677
  + patch_d + shim region) byte-identical to 0521 full_d.zag lines
  1..2027 (record sha256); pipeline is activate -> satisfy ->
  trial -> bootstrap (source-verified); zero code occurrences of
  "compose" in patch_d.zag (comments explaining the absence allowed).
- KB3 trial-path-free battery: TPF-1, TPF-2, TPF-3 all PASS per the
  mechanical criteria in 2.1.
- KB4a supervised breakers: B1, B2, B3S, B6, B7, B8 all PASS per
  2.2 (B1 wall < 120 s, B2 wall < 60 s, B7 wall < 300 s, measured
  externally with the shell `time` builtin).
- KB4b attribution honesty: B4 PASS and B5 PASS per 2.2.
- KB4c unsupervised bounds (characterization only, never kill):
  B3U predicted FAIL; a PASS falsifies the greedy-trap hypothesis
  and is recorded as calibration. B4U and PF-1c are informational.
- KB5 probe-menu/source-audit: (a) source audit: no test-specific
  integer literals (101..112, 204..206, 904..920, 4000..4399,
  9100..9139, 70..74, 105, 106, 205) in patch_d.zag outside comments;
  zero "compose" code occurrences (re-grep). (b) PM-1a and PM-1b
  both PASS (expected-driven selection confirmed and bounded).
  KB5a must be clean for any BUILD-PASS; PM-1 outcomes are
  characterization either way.
- KB6 commit-order self-check: over this lane's wave commits, the
  first commit containing PREREG_ADV.md must strictly precede the
  first commit containing driver_adv.zag / full_adv.zag /
  run_adv*.txt. Failure = UNVERIFIABLE ORDERING; no verdict beyond
  BUILD-FAIL.
- KB7 verdict rule: the battery verdict line is BUILD-PASS /
  BUILD-FAIL (build = battery built and run per this prereg).
  Survival verdict SURVIVES-ADV-A iff KB1, KB2, KB3, KB4a, KB4b,
  KB5a hold. If any KB4a breaker FAILS, the verdict is
  BREAK-ON-<axis> (the battery still BUILD-PASS as executed; the
  break is the finding). PF-1a/PF-1b: any FAIL downgrades an
  otherwise clean SURVIVES-ADV-A to SURVIVES-SEALED-ONLY with the
  PF-1 break named.

## 4. Predictions (calibration only; never move bars)

TPF-1 PASS, TPF-2 PASS, TPF-3 PASS, B1 PASS, B2 PASS, B3S PASS,
B3U FAIL (greedy trap wins; terminal 914), B4 PASS, B4U INFO
(partial composite, terminal 103), B5 PASS, B6 PASS, B7 PASS
(< 300 s), B8 PASS, PM-1a PASS, PM-1b PASS, PF-1a PASS, PF-1b PASS,
PF-1c INFO (terminal 106).

## 5. Implementation constraints (frozen)

- Pure Zag only. Safebin PATH. No Python. Forbidden executable =
  automatic PROCESS-FAIL with immediate disclosure.
- Mechanism code reused byte-identical from the 0521 record
  (patch_d.zag SHA in KB2; substrate lines 1..1677 of cmp_full_c
  via 0521 full_d.zag lines 1..2027). No edits to mechanism logic.
- Lane writes only under docs/lab/rsi/runs/wave-20261002-1121pdt/comp/.
  Commits: this prereg ALONE first; implementation second (explicit
  pathspec, never git add -A, never push).
- Driver/shim/asm are harness, not cognition; counted separately.
- Loop docs: hyphens only (no em/en dashes); check_no_dash.sh
  before each doc commit.

## 6. Deliverables

NAMECHECK.md (Step 0 done), this PREREG_ADV.md (frozen alone),
implementation (driver_adv.zag, shim_adv.zag, full_adv.zag, asm_adv.sh,
bin_adv, run_adv1/2/3.txt), SEALED_EVAL_ADV.md (matrix + numbers +
timing), POSTFREEZE_PF1.md (PF-1 design record, post-freeze commit),
REDTEAM_ADV.md (probe-menu/source-audit adversarial pass; is any
ADV-A result explainable by probe-menu equivalence or source audit?),
REPORT.md (lane verdicts, commit ids, kill evidence, queue).
