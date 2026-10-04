# REPORT.md -- Multi-Op Process Selection (Priority F)

## 1. Verdict

**PROCESS-MULTIOP-COMPLETE.**

Frozen kill bars (PREREG.md v1, thresholds unchanged through all
amendments v2-v7):

- **T1 (clean compositional discovery): 1.** The first all-greedy
  [1,3,2] subsequence in CHAIN3 worlds occurred at episode 55 with
  pre-episode comp_sum(1,3) = 0/5 and comp_sum(3,2) = 0/1. Neither
  inner 2-op link had ever been rewarded. The triple was assembled
  from component applicability and systematic rotation, not from
  pair memorization.
- **T2 (adoption and reuse): 1.** Late episodes 400-499: CHAIN3
  27/27 solved, 27/27 by the [1,3,2] triple.
- **T3 (body parameter revision): 1.** p4 = 4 at end, rev_n = 1
  (single revision, no overshoot), late EST 53/53 solved.

All three runs byte-identical (sha256
6881da8ed332d8faec3c675cd4850ab734555236e54681453ca993340b62ed05).

## 2. What was tested

Two research questions, two arms sharing ALL learner machinery:

**Q1 (Arm A):** Can the learner discover a 3-operation sequence
FOLLOW -> SHIFT -> COMPLETE (op ids [1,3,2]) in a novel CHAIN3 world
when the inner 2-op links (1,3) and (3,2) were never directly
rewarded? This tests compositional generalization, not pair
memorization. The components are trained separately: FOLLOW in F2
worlds (FOLLOW -> COMPLETE), SHIFT in T2 worlds (SHIFT -> GATHER),
GATHER/COMPLETE in F worlds. CHAIN3 worlds require all three in
sequence. The learner must compose them.

**Q2 (Arm B):** Can the learner revise an op's INTERNAL body
parameter (not just select/reject the op) based on consequences?
ADJUST has a learner-owned immediate parameter p4 in its byte-array
body, gated behind a T-edge check. In EST worlds the true answer is
V+4 (the constant 4 lives only in the environment). The learner must
revise p4 from 0 to 4 via the signed error on wrong answers.

## 3. Learner design (all generic, no semantic cases)

Ops are learner-owned byte arrays executed by an 8-instruction
interpreter (MATCH_X edge check, MOVE_X, ANSWER, ADD_P, END, FAIL,
JMP, PARAM). The interpreter never branches on op id. Selection is an
epsilon-greedy bandit over op indices scoring applicability(op,ctx)
+ composition(prev,op) with uniform 500 optimism for unseen pairs.
Credit is generic: fail -> 0, wrong answer -> -1, non-terminal +1 iff
the episode solved. Composition links are written only when the
previous op was effective. Retirement removes persistently harmful
ops. Body parameters revise by the full signed error on wrong
answers (at most one revision per op per episode).

No OP_ mode constants, no hardcoded 3-sequences in learner code
([1,3,2] appears only in measurement), 0 modes/bridges/handlers.

## 4. Version history (honest)

Seven versions, each prereg-amended and re-frozen BEFORE code
changes, each run 3/3 byte-identical. Kill-bar thresholds never
changed. What each version taught:

**v1** (single-phase, limit 4, greedy-only unit-step revision):
T1=0, T2=1, T3=0. DISCOVERY ep=26 but clean=0: exploration-assisted
triples rewarded the inner links first (pre13=2/4). T3=0: after
ADJUST's first -1, its applicability (-1000) sat below the fail-0
competitors, so greedy never retried it and exploration could not
revise a parameter it never selected. Lesson: revision needs the op
to be selectable after miscalibration.

**v2** (two-phase Arm A: Phase 1 F/F2/T2 only, Phase 2 adds CHAIN3;
T-gated ADJUST + full-error revision on any wrong answer): T1=0,
T2=1, T3=1. DISCOVERY ep=277, clean=0, pre13=1/7, pre32=3/4. The
4-step limit allowed solved [1,3,X,2] episodes to reward (1,3). T3=1
(p4=4, late 53/53). Lesson: the step limit must equal the triple
length, or longer paths contaminate the link measurement.

**v3** (limit 4 -> 3; eps=0 in Phase 2): T1=0, T2=0, T3=1. CHAIN3
0/65 solved. At CHAIN3-E2, COMPLETE (comp(1,2)=664 from F2 pair
history) outscored SHIFT (appl(3,4)=541 + comp(1,3)=0). Greedy stuck
picking the failing COMPLETE. Lesson: two-phase starves SHIFT's
applicability (Phase 1 has no CHAIN3 to train it); the test became
weak-applicability vs strong-habit, which is not the intended
compositional question.

**v4** (Phase 1 -> F35/F2-25/T2-40 to strengthen SHIFT): T1=0,
T2=0, T3=1. appl(3,4)=571 still lost to comp(1,2)=627. Lesson:
exploration zeros dilute applicability faster than extra T2 share
builds it.

**v5** (Phase 1 -> F20/F2-20/T2-60): T1=0, T2=0, T3=1.
appl(3,4)=591 vs comp(1,2)=607. Still loses. Lesson: the two-phase
design cannot fairly train the component it needs; CHAIN3 itself
must train SHIFT's applicability (as v2's single-phase did,
reaching 946).

**v6** (single-phase, eps=0 globally, limit 3): T1=1, T2=1, T3=0.
DISCOVERY ep=55, clean=1, pre13=0/5, pre32=0/1. Late 27/27. But
T3=0: with eps=0 the deterministic tie-break picked ADJUST 3 times
in one episode; full-error revision applied the stale error 3
times, overshooting p4 0 -> 12; then ADJUST locked out (-1000 below
fail-0), EST 0/241. Lesson: (a) at most one parameter revision per
op per episode (error signal is stale after the first); (b) Arm B
needs exploration to recover a miscalibrated op.

**v7** (one-revision-per-op-per-episode; Arm A eps=0, Arm B normal
eps schedule): **T1=1, T2=1, T3=1. PROCESS-MULTIOP-COMPLETE.**

The v6 design (single-phase + eps=0 + 3-step limit) gives a
STRUCTURAL clean-discovery guarantee: with eps=0 every triple is
all-greedy by construction, and with a 3-step limit the inner links
can be rewarded ONLY by the triple itself, so the first triple
necessarily satisfies T1's clean condition. Discovery still
requires genuine composition (component applicability + systematic
rotation at the novel E4 context under optimism).

## 5. v7 detailed results (3/3 byte-identical)

**Arm A (composition):**

- DISCOVERY ep=55 clean=1 pre13=0/5 pre32=0/1. The first [1,3,2]
  triple: FOLLOW picked at CHAIN3-Q (applicability from F2),
  SHIFT picked at E2 (appl(3,4)=962 + comp(1,3)=0 = 962, vs
  COMPLETE appl(2,4)=0 + comp(1,2)=0 = 0; SHIFT wins decisively),
  COMPLETE picked at E4 (systematic least-tried rotation at the
  novel context under 500 optimism; first correct answer gives
  +1 to appl(2,9) and to comp(3,2)).
- CHAIN3 all=146 ok=129 tri=129. Late (400-499): 27/27 solved,
  27/27 by the triple. T1=1, T2=1.
- Final tables: comp(1,3)=528, comp(3,2)=992 (the links, learned
  FROM the triple, as they should be); appl(3,4)=962.

**Arm B (revision):**

- PARAM p4=4 rev_n=1 rev_eps=3. Single revision at episode 3
  (0 + 4 = 4, full signed error, no overshoot). EST all=241
  ok=234, late 53/53. T3=1.
- Final appl(4,9)=991 (ADJUST strongly applicable at EST after
  revision).

**Determinism:** three runs, sha256 identical
(6881da8ed332d8faec3c675cd4850ab734555236e54681453ca993340b62ed05).
Fixed LCG seeds, fixed tie-breaks, no wall-clock or ASLR dependence
in output bytes.

## 6. Interpretation

**What T1 establishes:** The learner produced a 3-op chain whose
middle links were never rewarded before the chain itself. The
mechanism is fully white-box: FOLLOW selected by applicability
learned in F2; SHIFT selected by applicability learned in T2
(appl(3,4)=962) beating COMPLETE's pair-history score (0 at that
point, since F2's (1,2) link does not transfer to E2's context);
COMPLETE selected by optimistic rotation at the novel E4 context.
No component of the learner "knew" the triple. This is
compositional generalization by the preregistered definition.

**What T2 establishes:** Once discovered, the triple is adopted
(27/27 late) and the composition links are written (comp(3,2)=992).
The learner reuses the discovered structure.

**What T3 establishes:** The learner revised an op's internal body
parameter (p4: 0 -> 4) from the signed error of a wrong answer,
rewriting the op's byte-array body. This is parameter revision
INSIDE a selected structure, not selection among structures. The
T-gate isolates the parameter: it is only ever explanatory where
the op answers wrongly.

**Limitations and what this does NOT show:**

- The worlds are researcher-designed with clean component
  structure. The learner did not invent FOLLOW/SHIFT/COMPLETE or
  their bodies; it composed researcher-provided ops. This is L2
  structural learning (new relationships from generic mechanisms),
  not L3 representational invention.
- T1's clean condition was achieved via a structural guarantee
  (eps=0 + 3-step limit), which removes exploration noise but also
  removes a realistic discovery pressure. v1/v2 showed that with
  exploration, assisted triples contaminate the link histories;
  the strict "never rewarded" bar is fragile under exploration.
  The compositional ABILITY (produce the triple from components)
  is robust; the strict measurement condition is not.
- Arm B's revision is a single scalar parameter with a linear
  error signal. It does not show revision of control flow,
  instruction choice, or multi-parameter bodies.
- Scale: 4-5 ops, 16 contexts, 500 episodes. No evidence yet at
  larger scales or with interfering tasks.

## 7. Files and reproducibility

All in docs/lab/research-lead/overnight-20260928/process_multop/:

- PREREG.md (frozen v1 at 2dfecede8, amended v2-v7, each committed
  alone before code changes; kill-bar thresholds unchanged).
- multop.zag (pure Zag, ~1100 lines; builds with the pinned znc).
- multop_bin_v1..v7 (binaries) and run1_vN.txt/run2_vN.txt/
  run3_vN.txt (3/3 outputs per version).
- multop_bin, run1.txt/run2.txt/run3.txt (current = v7).
- NAMECHECK.md (this file), REPORT.md.

Reproduce: build with
`~/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1
multop.zag -o multop_bin`, run three times, compare sha256 against
6881da8ed332d8faec3c675cd4850ab734555236e54681453ca993340b62ed05.

## 8. Architecture accounting

- New cognition lines: ~1100 (multop.zag, standalone experiment).
- New hardcoded semantic cases: 0.
- Modes / bridges / handlers: 0 / 0 / 0.
- Learner-state structures: 5 op byte-array bodies (8-instruction
  interpreter), appl 5x16, comp 5x5, tot/retired, param cells,
  consequence ring buffer, discovery recorder.
- Capability-source delta: the triple [1,3,2] and p4=4 exist only
  in learner state, never in source. Source holds only generic
  machinery (interpreter, bandit, credit, revision rule).

## 9. Recommendation

Promote as BUILD-PASS with the limitations in section 6. The
compositional-discovery mechanism (applicability + optimistic
rotation at novel contexts) and the body-parameter revision rule
(one-per-episode full-error) are candidates for the continuing
learner. Next: scale to more ops/contexts, add interfering tasks,
test revision of multi-parameter bodies, and run an adversarial
red team on the T1 measurement (does the structural guarantee
hide a failure mode?).
