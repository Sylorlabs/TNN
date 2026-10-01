# TNN-3 Prerequisites Checklist

Date: 2026-10-01 UTC. Analyst task: define what must be true before
TNN-3 can be preregistered. This is a prerequisites checklist, NOT a
TNN-3 design. No design is proposed here.

Verdict: **TNN3-PREREQUISITES-MAPPED**

## 0. How to read this document

Each prerequisite carries a status:

- COMPLETE: finished and committed.
- LANDED-DRAFT: substantive work exists on disk but is uncommitted.
- IN-PROGRESS: a worker is running or work is partial.
- NOT-STARTED: no evidence of any work.

Nothing in this document authorizes, sketches, or constrains a TNN-3
design. The design-adjacent content in the synthesis report
(`42b4dfa91`) is cited as an input to prerequisite tracking, not
adopted here.

## 1. Prerequisite checklist

### A. Root-cause analysis (Micah's directive item 1)

Status: COMPLETE.

- TNN-1 root cause: `ed38121d4` (5 failure clusters reduced to 3
  shared architectural gaps).
- TNN-2 red team synthesis: `42b4dfa91` (REDTEAM-SYNTHESIS-COMPLETE).
  All three ATTACK-SUCCESS results (construction `340e94e3e`,
  inquiry `4e329c772`, revision `687ba0219`) reduce to one shared
  architectural pattern named "enumerated-schema / filled-slot":
  in each mechanism the researcher authored the schema (the space of
  possible structures and the procedure that fills it) and the
  learner fills runtime-chosen slots (literals, cell indices, miss
  content) inside that schema. The learner chose operands, never
  topology. Each mechanism is genuine at slot filling and
  persistence; none lets the learner choose the schema.
- Revision generalization analysis: `edbb0e9b5`
  (REVISION-GENERALIZATION-ANALYSIS-COMPLETE). Extends the revision
  root cause: five structurally different repair topologies the
  current operator cannot express, a learner-state availability
  audit (blame over guards/INC/DEC unavailable; retained licensing
  facts present but unused; no repair history; no ranking
  criterion), and attribution of the K-T2-6 kill-bar loophole (an
  existence-only bar admits a single-schema satisfier).

### B. Architecture accounting (Micah's directive item 2)

Status: COMPLETE (analysis); NEEDS-MEASUREMENT experiments pending
(follow-up, not a prereg blocker).

- Compression analysis: `b2a6ae82c`
  (COMPRESSION-ANALYSIS-COMPLETE). TNN-2 is 1591 lines (+263 vs the
  TNN-1 base). ~103 lines are dead in the cognition path and
  removable with zero capability loss (test-gated sum branch:
  t2_asm_sum, t2_gather_sum, comb_present, popcnt, subset loop;
  test-only t2_sig, exec_val, map_standing, contradict_map; ET_REG
  tag). ~32 more pending a bootstrap_miss disable experiment; ~32
  via unification. The 1200-line ceiling remains ~290 lines away
  after trimming; closing it needs architectural deletion, not
  trimming. Key architectural findings: 3 fixed assemblers replaced
  3 fixed templates; revision repair is fully researcher-authored;
  inquiry guide content is constant; the sum assembler never runs
  in production (test-gated on a type-8 node no cognition path
  creates), which constrains interpretation of any FW3 result.
- Governance audit `622363372` corroborates the accounting:
  function count base 169 to TNN-2 168 (net deletion), node types
  unchanged, zero new modes/bridges/handlers/semantic cases, ISA
  frozen and byte-identical.

### C. At least three structurally different hypotheses for the major bottleneck (Micah's directive item 3)

Status: COMPLETE (committed in synthesis `42b4dfa91`, section 5).

- H1, the grammar hypothesis: every mechanism's output space is
  enumerated in source; the learner selects and parameterizes
  within the set. Discrimination: freeze an open compositional
  constructor alone and re-run the three red team probe suites.
- H2, the oracle hypothesis: verification, not generation, is the
  bottleneck. Construction matches an environment-supplied
  expected; revision copies the observed literal. Nothing must be
  discovered. Discrimination: masked verification probes with the
  grammar fixed.
- H3, the procedure-ownership hypothesis: the mechanisms'
  operating procedures are source code, not learner state. C0-A
  fails in all three for the same reason. Testable prediction: no
  production path can revise a mechanism's policy from experience.
  The synthesis recommends running H3's check first (pure
  production-path analysis, no new worlds), then H2's probes,
  then considering H1's widening, because widening the space
  before fixing the oracle yields a larger finite menu under the
  same generous acceptance test.

### D. Explicit argument for why a change fixes multiple failures (Micah's directive item 4)

Status: COMPLETE (committed in synthesis `42b4dfa91`, section 3).

- The synthesis states the shared-cause argument: the shared cause
  is that form lives in source. A single substrate that constructs
  form from learner state, shared by construction, revision, and
  inquiry, moves form into learner state once and widens all
  three mechanisms simultaneously. It is also a deletion story:
  three fixed assemblers, constant guide literals, and the
  single-schema repair procedure collapse into uses of one
  mechanism. Capability up, researcher-authored machinery down.
- The synthesis also records the mandatory caveats: the substrate
  alone does not supply inquiry's missing informativeness
  criterion (banked as an open design question), and the revision
  acceptance criterion must not be "reproduces the observed
  literal" or the substrate rediscovers literal-storing patches.
- This document does not evaluate or adopt that argument as a
  TNN-3 proposal. It records that the required argument exists,
  is committed, and is available as an input to the TNN-3 cycle.

### E. TNN-2 freeze evaluation committed with all kill bars closed

Status: IN-PROGRESS (LANDED-DRAFT, uncommitted).

- The evaluator's draft report exists at
  `core_freeze_tnn2_eval/FREEZE_REPORT.md` (untracked). Draft
  contents: FW battery complete, FW SCORE 5/9 (passes FW1, FW2,
  FW4, FW5 per the table). Old-world regression battery pending.
  K-FZ2-4 determinism pending. Post-eval hash re-verification
  pending. Per-cluster fix analysis pending W results.
- The draft is internally inconsistent and must be reconciled
  before commit: the verdict line says FREEZE-EVAL-COMPLETE and
  the score line says 5/9, but only 4 passes are listed in the
  table (FW1, FW2, FW4, FW5), and K-FZ2-4 is marked PENDING in the
  same document. The 5th pass, if any, is not identified in the
  draft. The FW6 note records that the responder withheld reveal
  and that post-diagnostic ACT was CHOICE 30 rather than the
  contract's literal CHOICE 0; how the frozen interpretation
  rules score that arm must be stated explicitly, not left
  ambiguous.
- FW3 FAIL (0/10, all -2) in the draft is consistent with the
  compression finding that the sum assembler never runs in
  production. FW7 FAIL (all 24 ACTs CHOICE 0) and FW9 FAIL
  (B1 3/30, B2 7/30) stand as drafted.
- This prerequisite is a hard gate: TNN-3 preregistration must
  cite a committed, internally consistent freeze evaluation as
  its baseline. A prereg written against a draft is not frozen
  against a baseline.

### F. Post-freeze adversarial battery (GW worlds) sealed, run, committed

Status: NOT-STARTED.

- No commits, no directories, no design documents for the TNN-2
  post-freeze adversarial battery were found. The lane has not
  begun.
- This is the single largest missing prerequisite. Per the
  overnight directive, the fresh post-freeze battery is the
  important generality test, because FW1-FW9 are now a
  regression/targeted-repair battery for TNN-2: TNN-2 was
  designed after observing TNN-1's failures, and the red teams
  show its mechanisms cover exactly the researcher-enumerated
  envelope. Even a 9/9 on FW1-FW9 would not establish generality
  or L3.
- The red team reports are effectively a specification for the
  battery: construction section 7 (open topologies, world
  feedback verification, learner-managed bounds), inquiry's
  derived-need and resolution requirements, revision section 7
  (multi-member repair space, structurally different repairs,
  derived corrected content, sealed-world repairs the researcher
  did not pre-shape). The adversary must see the public
  architecture claim but not hidden builder fixtures, and must
  not design trivial surface variants of FW1-FW9.
- Minimum bar for this prerequisite: the battery is designed by
  an independent adversary, sealed before TNN-2 exposure, run
  against the frozen TNN-2 binary, and its results are committed
  with per-world scores.

### G. Alternative-explanation attack

Status: COMPLETE.

- `ccee9e5e6` (ALTERNATIVE-EXPLANATION-ATTACK-COMPLETE): simplest
  accounts stated for all three mechanisms (construction as
  parameterized retrieval from a fixed template library keyed by
  the environment-supplied answer; inquiry as a sticky miss flag
  with constant output action; revision as a researcher patch
  script with runtime operands), unified hypothesis (form from
  researcher, content from learner; learner degrees of freedom
  are indices and literals), and per-mechanism plus unified
  falsification criteria.

### H. Transfer/reuse analysis

Status: IN-PROGRESS (working files on disk, uncommitted).

- `tnn2_transfer/` contains working artifacts (NAMECHECK.md,
  build logs, probe outputs, transfer driver, binary) but is
  untracked and uncommitted. Results are not yet available.
- Recommended input to TNN-3, not a hard blocker: Micah's
  explicit pre-TNN-3 list (root-cause, accounting, hypotheses,
  multi-failure argument) does not name transfer, and the
  promotion pipeline treats transfer as a mechanism-level step.
  Its results strengthen the "explicit argument" but do not
  gate preregistration.

### I. Claim ledger current through the TNN-2 cycle

Status: PARTIAL.

- Ledger C143-C149 committed (`503a3bedc`), with C149 carrying
  an explicit follow-up requirement for the freeze evaluation.
- Committed since but not yet ledgered: the three red team
  verdicts, compression analysis, governance audit, synthesis,
  revision generalization, alternative-explanation attack, and
  frontier backlog. The freeze evaluation commit, when it lands,
  will close C149's follow-up.
- The ledger must be updated through cycle closure before
  TNN-3 preregistration, so the prereg cites a current claim
  record.

### J. Governance: no blockers, audit caveat closed

Status: PASS with one open caveat (see Q6 below).

## 2. What is still missing before TNN-3 can be preregistered

In priority order:

1. **Post-freeze adversarial battery (F): NOT-STARTED.** Design,
   seal, run, commit. This is the critical missing generality
   evidence.
2. **Freeze evaluation commit (E): IN-PROGRESS.** Finish the W
   battery, close K-FZ2-4 (3/3 byte-identical determinism),
   re-verify all four hashes post-eval, complete the per-cluster
   fix analysis, reconcile the draft's internal inconsistency
   (5/9 claim vs 4 listed passes; COMPLETE verdict vs PENDING
   bars), then commit.
3. **Ledger update (I): PARTIAL.** Append claims for all analyses
   since C149 and close C149's freeze-eval follow-up when (2)
   lands.
4. **H3 policy-revisability check and H2 masked probes (C
   follow-up): NOT-STARTED.** The synthesis recommends this
   experimental order before any TNN-3 design: H3 first (cheap,
   pure production-path analysis), then H2 (masked verification
   probes), then H1 widening only after the oracle question is
   settled. At minimum the H3 analysis should be run so the
   TNN-3 prereg can state which hypothesis binds first.
5. **Transfer results (H): IN-PROGRESS.** Finish and commit;
   informative for the prereg's reuse claims.
6. **Compression NEEDS-MEASUREMENT experiments (B follow-up):
   NOT-STARTED.** The bootstrap_miss disable experiment and the
   sum-branch deletion experiment are one to two runs each and
   would sharpen the architecture accounting, but they are not
   prereg blockers.

## 3. How the freeze evaluation results affect TNN-3 prerequisites

- The freeze measures capability; the red teams measure mechanism
  generality. Both can be true at once, and no freeze outcome
  invalidates the red teams and no red team outcome invalidates
  the freeze (synthesis section 4). The draft 5/9 (if confirmed)
  is a legitimate capability improvement over TNN-1's 4/9 on a
  battery sealed before TNN-2 existed, but it must be reported
  with the red-team bound: capability improved within the
  researcher-enumerated envelope; the envelope is unchanged in
  kind. It does not establish generality or L3.
- The per-cluster fix analysis (pending W results) feeds the
  TNN-3 "explicit argument" directly: it will show which of the
  three mechanisms actually moved capability on which clusters.
  That analysis is required input, not optional context.
- Watch condition from the frozen freeze prereg: a TNN-2 FW score
  at or below 4/9, or regressions on FW1/FW2/FW4/FW5, falsifies
  the frozen root-cause prediction and requires re-clustering.
  The draft shows FW1/FW2/FW4/FW5 holding and 5/9 above the bar,
  but the W battery is pending; if W1/W2/W4/W5 regress, the
  re-clustering requirement triggers before TNN-3 preregistration.

## 4. How the post-freeze adversary results affect TNN-3

- They are the generality evidence the FW battery cannot supply.
  TNN-3's preregistration must be written against them: its kill
  bars for generality properties must require demonstrations on
  fresh sealed worlds, not on FW1-FW9.
- The results discriminate the hypotheses in practice. If TNN-2
  fails fresh worlds requiring non-enumerated structures,
  non-single-schema repairs, or state-varying informative
  actions, the failures must be clustered by shared architectural
  cause (per the no-treadmill rule) and those clusters become the
  TNN-3 problem statement. If, contrary to the source audits,
  TNN-2 passes such worlds, the red-team findings require
  re-examination before any TNN-3 design proceeds.
- Without this battery, TNN-3 preregistration would be written
  with FW-only evidence, which is now by ruling a regression
  battery. That would repeat the exact failure mode the
  directive forbids: designing to a known battery while calling
  it generality.

## 5. Minimal set of completed analyses that justifies starting TNN-3 preregistration

All of the following must hold. Each is checkable from the repo.

1. Freeze evaluation committed: FREEZE-EVAL verdict with all
   K-FZ2 bars closed (FW1-FW9 primary, W1-W9 supplementary,
   3/3 byte-identical determinism, pre and post hash
   re-verification, seal integrity, per-cluster fix analysis),
   internally consistent.
2. Post-freeze adversarial battery: independently designed,
   sealed, run against the frozen TNN-2 binary, results
   committed with per-world scores.
3. Root-cause synthesis committed (done: `42b4dfa91`).
4. Architecture accounting committed (done: `b2a6ae82c`).
5. Ledger updated through TNN-2 cycle closure (C149 follow-up
   closed; all analyses since C143 ledgered).
6. H3 policy-revisability analysis run, so the prereg can state
   which of H1/H2/H3 binds first. H2 masked probes strongly
   recommended alongside.
7. Governance clean: no new violations; the `622363372` caveat
   closed by the eval commit; the evaluator's draft inconsistency
   reconciled before commit.
8. The TNN-3 preregistration document itself must fix the K-T2-6
   process weakness identified in `edbb0e9b5` section 5: bars for
   generality properties must require at least two structurally
   different demonstrations, never "in at least one test".

Items 1, 2, 5, and 6 are the work remaining. Items 3 and 4 are
done. Item 7 is a check at prereg time. Item 8 is a property of
the prereg document.

## 6. Governance blockers

No governance blockers. Findings:

- The cycle audit `622363372` is GOVERNANCE-AUDIT-PASS. Its one
  open caveat (evaluation in progress) is exactly prerequisite E
  above; it closes when the eval commits with its K-FZ2 bars
  closed.
- The three red-team ATTACK-SUCCESS verdicts do not trigger any
  governance issue. They are mechanism-generality results, not
  kill-bar violations. They do not retroactively alter TNN-2's
  BUILD-PASS (`f4de7ff46`) or REPRO-PASS (`fdf1fa626`), which
  were correctly scoped to build and reproduction, and no bar
  was weakened after results. The synthesis states this
  explicitly in its section 7, and the governance lane should
  record the same when it ledgers these results.
- The K-T2-6 loophole (an existence-only bar admitted the
  single-schema repair) is a process weakness to fix in the
  TNN-3 prereg, not a retroactive violation. The audit already
  recorded the analogous K-T2-5 wording caveat without finding
  a violation. No bar text was altered after results.
- The compression finding that the sum assembler is dead in
  production is an interpretation caveat for the freeze report
  (section E above), not a governance violation.
- One watch item for the governance lane: the evaluator's draft
  carries a COMPLETE verdict while K-FZ2-4 is PENDING and claims
  5/9 while listing 4 passes. This is an evaluator-report
  quality issue, not yet a violation (the report is uncommitted),
  but the commit must not land in this state. The auditor
  should require reconciliation before accepting the eval
  commit.
- Toolchain: every analysis worker in this prerequisite set
  (red teams, compression, audit, synthesis, revision
  generalization, alternative-explanation, frontier, this
  analyst) records Step 0 safebin activation with no forbidden
  executable reachable. Zero violations found. The contaminated
  paper is untouched; sealed FW assets were never inspected by
  any worker in this set (only the authorized evaluator's draft
  was read).

## 7. Status of the assigned questions

1. Current state of each prerequisite: root-cause COMPLETE
   (`42b4dfa91`, plus `edbb0e9b5`); architecture accounting
   COMPLETE (`b2a6ae82c`); hypotheses COMPLETE (H1/H2/H3 in
   `42b4dfa91` section 5).
2. Still missing: post-freeze adversarial battery (not started),
   freeze evaluation commit (draft on disk, inconsistent, W
   battery and determinism pending), ledger update, H3/H2
   discrimination experiments, transfer results.
3. Freeze results effect: capability evidence only; bounded by
   the red teams; per-cluster fix analysis is required input;
   W regressions would trigger re-clustering before TNN-3.
4. Adversary results effect: the generality evidence; required
   before preregistration; failures must be clustered by shared
   cause; a surprise pass would force re-examination of the
   red teams.
5. Minimal set: the eight items in section 5 above.
6. Governance blockers: none; one open audit caveat; one
   evaluator-draft quality watch item.

## 8. Banked note for the coordinator

The frontier backlog (`65effc909`, 17 ranked research questions)
exists and is committed; it is the refill source for worker
slots and is not itself a TNN-3 prerequisite. The transfer lane
is running; the alternative-explanation lane is complete. No
architectural or governance decision in this document requires
Micah's ruling. Independent lanes continue.
