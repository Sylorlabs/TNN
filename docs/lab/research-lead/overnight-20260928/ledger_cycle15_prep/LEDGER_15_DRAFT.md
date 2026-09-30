# Ledger Cycle 15: Draft Claim List

Date: 2026-09-30. Prepared from completed work since C142 (commit aada2ada7).
Draft only. The canonical ledger is NOT modified by this file.

Ledger baseline: 142 claims. This cycle proposes C143 through C152
(10 new claims). Ledger would go 142 -> 152.

---

## Ready now (10 claims)

### C143. TNN-1 F-INT4 disposition (EXPLORATORY)

- Commit: 86518edc4 (local only). Disposition only; no implementation.
- Source material: integration prereg F-INT4/K5 (7fc7148ac), TNN-1
  build t_xcap test (0323b97d5, tnn1.zag lines 1024-1046), TNN-1 red
  team Vector 1 (cbde38737). All read in full; build inspected
  read-only.
- What the prereg requires: F-INT4 (falsifier) demands a
  cross-capability test with four linked properties: (1) plan
  constructed for a query miss (COMP-1 path), (2) promoted as a MAP
  node (CAM-1 path), (3) later selected by ACT as an action guide
  through the same edges, (4) contradiction against the MAP node
  demoting both its query standing and its action candidacy. K5
  (positive bar) requires "a query-miss plan becomes an action guide
  through shared edges, and contradiction demotes both candidacies."
- What the test does: t_xcap has two disconnected parts. Part 1 runs
  ev_query and verifies the plan path, but discards the real MAP node
  (mp_run does not return its id). Part 2 creates a SYNTHETIC guide
  node via alloc_node ("simulating a MAP that guides action"),
  contradicts it, and verifies both map_standing and bid demote. The
  test never calls ev_act. It never shows the query's MAP being
  selected as an action guide.
- The exact gap: what the test proves is metric co-location
  (map_standing and bid computed over shared edge state on one
  node), not plan-to-guide conversion.
- Can the binary support a stronger test? Level 1 (supported):
  replace the synthetic node with the real MAP node from ev_query
  (scan for newest T_MAP node, contradict it, verify both metrics
  demote); no binary modification needed. Level 2 (not supported):
  full "plan becomes guide" conversion. promote_map never links the
  MAP node to POLICY_ROOT; pol_set is called only in test
  scaffolding, never by system functions. No MAP-to-guide
  registration mechanism exists anywhere in TNN-1.
- Bar assessment: F-INT4 (falsifier) does NOT trigger (mechanisms
  genuinely interact through shared state; not a trench coat). K5
  partially satisfied (the "contradiction demotes both candidacies"
  half holds; the "plan becomes guide" half is not demonstrated).
- Recommendation: narrow the claim to "contradiction demotes both
  query standing and action bid through shared edges on a MAP node"
  (honestly supported, still a meaningful cross-capability
  property). Mark the "plan becomes guide" half as not demonstrated.
  If full conversion is wanted, it is a capability addition needing
  a fresh prereg under the One-System Rule, not a test tweak.
- Governance: analysis only; zero Python; paper zero-diff; no
  sealed FW1-FW9; TNN-1 unmodified.

**Status: EXPLORATORY** (disposition and recommendation; no
implementation; no SURVIVES or L3 implication).

### C144. EXECUTE boundary evidence package (EXPLORATORY)

- Commit: 55a7356f2 (local only). Analysis only; no implementation.
- Purpose: state what Micah approved vs what was added, who relies
  on it, and the options, for his ruling on the EXECUTE placement.
- What Micah explicitly approved (0525377f3, FROZEN ARCHITECTURE
  RULING): the ISA class "APPLY/EXECUTE" as domain-neutral machinery,
  alongside ALLOC, READ, WRITE, LINK, COPY, COMPARE/EQ, ADD, BRANCH,
  generic state/register operations. Frozen rule: "No core operation
  may encode a target-domain regularity detector." What the ruling
  does NOT specify: the primitive's exact signature, internal
  dispatch table, frame model, step budget, or strike-down of
  overlapping operations.
- What the placement recommendation adds (1fc77503b, status:
  "analysis only; recommendation to Micah for approval before any
  core change. No implementation in this commit."): ONE primitive
  EXECUTE(root, frame) -> value | FAIL; closed 4-op ISA
  {MOVE, BRANCHEQ, INC, DEC}; execution context {current, frame,
  steps}; frozen learner-visible BUDGET; frame indirection replacing
  HOLE; amendments A-C.
- The governance breach (documented with evidence): the CLA-2
  builder's NAMECHECK.md line 6 records "EXECUTE placement
  amendments A-C (1fc77503b, APPROVED)". This is false. The builder
  treated commit ancestry (git merge-base --is-ancestor) as approval.
  CLA-2's own prereg (24351fd31) specified six primitives with "No
  execution primitive." The integration prereg (7fc7148ac) was
  honest: "The prereg does not canonize the placement."
- Reliance map (source-verified): rely on the placement: CLA-2
  (cites Amendment A in comments), TNN-1 (ports it, tags 101-104,
  budget 1000). Cite but do not implement: COMP-1 (one comment). Do
  NOT rely: DEVINT-CLA2 (0 matches), MUL-1 (bespoke 7-op
  interpreter, not the 4-op ISA), inquiry both builds (0 matches).
  Correction: earlier claims that "MUL and inquiry rely on this
  arrangement" are incorrect.
- Deltas: one real spec deviation. BUDGET is a code literal 1000 in
  TNN-1, not learner-visible per the placement spec (the placement's
  own F-F covers this). TNN-1's source comment correctly lists 7
  names; the six-name slip was in prose, not source.
- TNN-1 red team never audited the placement: zero mentions of
  EXECUTE in its report; criteria F-A through F-J untested.
- Recommendation: approve the placement as implemented, with (1)
  the governance breach recorded in the ledger (ancestry is not
  approval), and (2) a placement red team against F-A through F-J
  required before SURVIVES consideration or the freeze rerun.
  Justification: the regress argument is unrefuted, the table
  satisfies the frozen rule, and rejection would void CLA-2/TNN-1
  for a boundary with no better alternative on offer.
- Governance: analysis only; zero Python; paper zero-diff; no
  sealed FW1-FW9.

**Status: EXPLORATORY** (evidence and recommendation for Micah's
ruling; the ruling itself is pending and is not claimed here).

### C145. TNN-1 cognition-line remeasurement (EXPLORATORY)

- Commit: 6c40f4238 (local only). Measurement per
  MEASUREMENT_PROCEDURE.md applied to tnn1.zag @ 0323b97d5.
- Headline: 1088 total source lines, 153 functions, 54
  comment-only lines. Cognition source lines: 641 across 53
  functions. Semantic cases: 0. Modes: 0. Bridges: 0. Handlers: 0.
- Category breakdown: INFRA 23 lines / 6 functions; ACCESSOR 55 /
  55; COGNITION generic substrate (workspace primitives + EXECUTE
  ISA) 99 / 10; COGNITION retention/eviction 102 / 10; COGNITION
  teach/query/act path 144 / 9; COGNITION plan synthesis/
  composition 284 / 23; COGNITION init 12 / 1; DRIVER (35 tests +
  runner + main) 331 / 39.
- Key comparisons: frozen core 586 cognition lines -> TNN-1 641
  (+9.4% for the unified workspace, ACT path, COMP-1, CAM-1, DEVINT
  driver). Separate implementations summed to 1255 -> TNN-1's 641
  is a 49% reduction via one shared substrate.
- R_test on cognition-line basis: 5.46 per 100 lines (35 tests /
  641 lines).
- Resolves compression tracker open items 6-8 (formal
  classification per MEASUREMENT_PROCEDURE.md).
- Process disclosure: this wave is PROCESS-FAIL per the Worker
  Toolchain Guard (11th Python incident overall). The worker invoked
  python3 once for arithmetic sums during classification. All sums
  were re-verified via awk-only computation (which the measurement
  procedure explicitly authorizes), and the committed numbers
  reflect the clean verification. The incident is fully disclosed
  in the wave NAMECHECK.md. The parent should decide whether the
  awk-verified measurement stands or requires a fully clean re-do.
- Governance: paper zero-diff; TNN-1 source unmodified; no sealed
  FW1-FW9.

**Status: EXPLORATORY** (measurement result; the 641-line figure is
awk-verified, but the wave carries PROCESS-FAIL on process grounds;
a clean re-do may be ordered before the figure is adopted).

### C146. MUL Rung B preregistration (PREREG-FROZEN)

- Commit: 5924bbdae (local only). Design only; no implementation.
- Parent: PREREG_MUL1.md @ 222899314. Rung A build: fbf14f73a.
  Rung A red team: 44f22979b (6/6 ATTACK-PASS).
- Rung A baseline (adopted): learner promoted 4-cell PROC
  [ACCUM_RX STEP_C TEST_CY GOTO(0)] after 4,297 rejected
  candidates, computing X*Y by repeated core-ADD. 8/8 held-out
  probes plus scaling (13,17)->221. Ablation destroys
  multiplication; core ADD survives. Transfer passes. Lookup
  control 0/8. 3/3 byte-identical. Red-team boundary: negative Y
  would not terminate (out of Rung A scope).
- The standing question for Rung B: Rung A showed one-level
  construction from a basis including core ADD. Rung B tests TWO
  levels: first ADD itself from {MOVE, BRANCHEQ, INC, DEC} (no core
  ADD in the search/execution path; K3 requires structural proof of
  exclusion), then MUL on top of the learner-built ADD via a generic
  CALL (procedure-invocation) move that is domain-neutral. The
  learner discovers the argument wiring and the decision to
  delegate. No existing mechanism performs learner-level procedure
  composition (a constructed procedure calling another constructed
  procedure).
- Predictions P-MULB1..6: ADD promotion (7/8 probes + scaling
  (47,53)->100), ADD structural checklist, MUL promotion with CALL
  cell targeting the learner-ADD root, two-level ablation (ablate
  ADD -> both fail; ablate MUL only -> ADD intact), transfer with
  nested MUL->ADD EXECUTE trace, lookup controls beaten by >=5.
- Falsifiers F-MULB1..5: core-ADD smuggling (kills the two-level
  claim), template contamination, flat re-derivation (no CALL;
  downgrades to one-level), memorization, oracle search.
- Negative-Y boundary now in scope for revision: initial
  construction stays non-negative (Rung A parity); Phase 5 revision
  probes ((5,0), (0,7), (3,-4), (-2,-5), >=3/4 after the learner's
  own revision) test criterion 12, with DEC making sign-handling
  genuinely reachable.
- Kill bars K1-K4: K1 ordering (this prereg strictly precedes any
  implementation); K2 honest recording; K3 purity (forbidden ops +
  core-ADD exclusion scan); K4 EXECUTE-boundary inheritance (nested
  invocation relies on the arrangement pending Micah's ruling;
  re-freeze by amendment if the ruling changes it).
- Controls: C1 Rung A comparison (identical probes; architectural
  not behavioral difference), C2 lookup baselines, C3 single-level
  diagnostic arm (tests whether the ADD-first curriculum is
  load-bearing), C4 no-construction control.
- Lane: construct-and-apply frontier; Micah's ISA boundary ruling
  consequence (2) (do not add MUL; test whether the learner can
  construct it).
- Freeze note: the document asserts "this prereg is frozen alone;
  no Rung B implementation may reference it until reviewed (K1)."
  An independent freeze verification is in flight; if it finds the
  prereg incomplete, this claim will be amended.
- Governance: design only; zero Python; paper zero-diff; no sealed
  FW1-FW9 (FW3 is the sealed multiplication world; this experiment
  uses fresh exemplars only).

**Status: PREREG-FROZEN** (design frozen; no implementation exists;
K1 ordering holds for any future implementation).

### C147. TNN-1 independent reproduction (EXPLORATORY)

- Commit: f51a3df0e (local only). Independent rebuild from
  committed source.
- Method: extracted tnn1.zag from build commit 0323b97d5 via
  git show; verified byte-identical to working-tree copy (cmp
  PASS, 1088 lines). Built with pinned znc_linux_x86_64_abed8aa1.
  Build exit 0 (A0102 analyzer warnings only, non-blocking). Ran
  the rebuilt binary 3 times.
- Results: rebuilt tnn1_repro_bin is byte-identical to the
  committed tnn1_bin (169082 bytes, cmp PASS). Same source + same
  pinned compiler = same binary. Test battery: 35 PASS, 0 FAIL on
  all three runs (TOTAL 35/35). Determinism: SHA-256
  78847448a6afa384b6c9387d11d80ea849135f4c402196a3e03034b254cd8164
  on all three runs, matching the value reported by the
  independent red team (cbde38737, Vector 5).
- Conclusion: REPRO-PASS. The builder's claims (35/35,
  byte-identical binary, deterministic output) all hold when
  rebuilt from committed source by a different worker. No
  discrepancies found.
- K1: the build's prereg (7fc7148ac) strictly precedes the build
  (0323b97d5), which strictly precedes this reproduction. Ordering
  satisfied by ancestry.
- Governance: zero Python; TNN-1 source unmodified (read-only);
  build artifacts in /tmp, not committed; paper zero-diff; no
  sealed FW1-FW9.

**Status: EXPLORATORY** (independent verification; step 4 of the
11-stage promotion pipeline; no new build).

### C148. DEVINT-CLA2 unimplemented-elements triage (EXPLORATORY)

- Commit: 2ed45875d (local only). Read-only source audit; no code
  written or executed.
- Inputs: DEVINT-CLA2 prereg (f24063bcb), red team (a5ccb100d),
  implementation (35f9500b2), report correction (a003bd19b).
- Call-site verification (all six confirmed against source):
  m2_check (line 663) defined, never called; split_group (line
  587) defined, never called; s6_train_out (line 717) defined,
  never called; s6_train_in (line 710) called once (line 967) but
  only to feed episodes for substring stats, never to derive the
  pairing; learn_procedure (line 481) called once (line 968) with
  explicit harness arguments (W,gbik,gzol,ggup,gtav,ev) derived by
  byte-matching in stage_s6.
- The six elements assessed (specified vs built, importance,
  difficulty):
  - E1, M2 bid-vs-survival metric: never computed; claim retracted
    by a003bd19b. Importance HIGH (F4 falsifier; honesty test for
    evidence-driven retention). Difficulty MODERATE for
    measurement, with LARGE follow-on risk (honest M2 may fail and
    trigger retention hardening).
  - E2, S10 post-eviction accuracy: 10 held-out episodes never
    measured; stage_s10 checks eviction count + GROUP survival only.
    Importance MODERATE-HIGH. Difficulty LOW-MODERATE.
  - E3, S6 examples-to-criterion + M1 synergy: never recorded; M1
    entirely unimplemented. Importance HIGH. Blocked on E6.
    Difficulty MODERATE once E6 exists.
  - E4, S9 SPLIT: split_group defined, never called. Importance
    MODERATE-HIGH (M3 dead without it). Blocked on E5. Difficulty
    MODERATE (wiring, once E5 lands).
  - E5, S7 boundary-violation representation: harness-local counter
    only (nviol); no SURPRISE edge or workspace structure.
    Importance MODERATE-HIGH (prerequisite for E4). Difficulty
    LOW-MODERATE (SURPRISE edge type already in frozen vocabulary).
  - E6, S6 pairing induction: the pairing is supplied by the
    harness, not induced from training examples; 5/5 held-out check
    tests storage/retrieval. Importance HIGHEST (the red team's
    strongest finding; the learning-vs-storage distinction).
    Difficulty HIGH (genuine induction through the learner's
    vocabulary).
- Prerequisite graph: E5 -> E4; E6 -> E3; E1 independent as
  measurement (may trigger retention hardening); E2 independent.
- Priority ranking: 1. E6 pairing induction, 2. E1 M2 metric,
  3. E5 violation representation, 4. E4 SPLIT,
  5. E3 examples-to-criterion/M1, 6. E2 post-eviction accuracy.
- Recommendation: implement E6 first. It is the learning-vs-storage
  distinction on which the developmental claim stands or falls, the
  red team's strongest finding, the unlock for E3/M1, and a direct
  test of the prereg's own S6 localization row. Scoping: derive the
  pairing from the S6 training examples through the learner's
  segment/GROUP vocabulary (positional correspondence or
  co-occurrence), recorded as SUPPORTS edges from training examples
  per the section 4 mapping, without reading the frozen hidden
  pairing. E1 and E2 are parallelizable alongside E6; E5 precedes E4
  in a later wave; E3 follows E6.
- Governance notes: BUILD-PASS stands (B1-B5 unaffected); these are
  prereg-specified elements, not kill-bar failures. Any next-wave
  implementation needs its own frozen prereg amendment before
  implementation (commit-order rule). One-System Rule applies: no
  new modes, bridges, handlers, or semantic cases; E6 must work
  through the existing executable-graph form and edge vocabulary,
  or its failure is the finding.
- Governance: zero Python; paper zero-diff; no sealed FW1-FW9;
  target implementation untouched.

**Status: EXPLORATORY** (triage and recommendation; no
implementation).

### C149. ACT coverage assessment (EXPLORATORY)

- Commit: 4b36f0c1e (local only). Read-only analysis.
- What the prereg required: integration prereg (7fc7148ac), P-INT2:
  "the integrated binary passes ACT's 24/24 tests (P-ACT1 planning,
  P-ACT2 inquiry, P-ACT3 null policy, P-ACT4 ablation, P-ACT5
  generality, P-ACT6 memory prerequisite), all in one process, with
  the directional bid. No test changes from the aligned ACT." K4
  references P-INT2 as (24/24). The prereg's own words forbid test
  changes.
- What the standalone suite contains: act_build/act.zag (614
  lines). 24 lines containing "PASS": 23 individual ptest checks
  plus the ALL-PASS banner. 16 unique checks (P-ACT5 re-runs P-ACT1
  and P-ACT2 through the same handler).
- What TNN-1 carries: 6 single-check tests (t_a1..t_a6).
- Coverage map: 3 of 16 fully covered (null-root->0, uncert->20,
  no-guides->0), 1 partial (t_a6 covers P-ACT6B's
  evidenced-retention without any capacity pressure), 1 weak
  (P-ACT5 generality implied but never asserted), 11 not covered.
- The missing ones that matter:
  - P-ACT1 (state-varying emission + D1 derivation): the planning
    claim. TNN-1 tests bid competition (t_a1) but never emits
    different actions per state. The "constant-0 baseline scores
    0/4" discrimination is untested.
  - P-ACT2 decoy->21 / other->0: the no-bleed claim. t_a2 checks
    only the positive case; a sloppy matcher would pass.
  - P-ACT4 no-goal->0 / fact-alive: the no-hallucination and
    recall-intact claims. Neither tested.
  - P-ACT6A (unevidenced evicted under pressure): the retention
    claim's negative half. Untested. Note the standalone used a
    stand-in eviction; a ported P-ACT6A would exercise TNN-1's real
    3-step directional eviction, making the port strictly more
    informative than the original.
- Recommendation: port the full 24/24 into TNN-1 per the prereg's
  "no test changes" requirement, as a preregistered remediation
  wave. Minimum honest subset if deferred: P-ACT1 checks 2-5,
  P-ACT2 checks 7-8, P-ACT4 checks 11-12, P-ACT6A checks 14-15. As
  it stands, K4's P-INT2 (24/24) line is not literally satisfied.
- Process disclosure: this wave is PROCESS-FAIL per the Worker
  Toolchain Guard (10th Python incident overall). During final
  verification the worker included `python3 -c "pass"` as a stray
  prefix in a shell command. It executed (zero computation: literal
  pass, no I/O, no output used). The em-dash check was redone with
  shell-only grep, confirming both files clean. Zero impact on
  deliverable content: all analysis was file reads, grep/sed, and
  running the prebuilt act_bin. The incident is disclosed in the
  wave NAMECHECK.md and commit message.
- Governance: paper zero-diff; ACT and TNN-1 unmodified
  (read-only).

**Status: EXPLORATORY** (coverage analysis and recommendation; the
analysis content is untouched by the incident, but the wave carries
PROCESS-FAIL on process grounds).

### C150. COMP-1 prereg amendment (EXPLORATORY)

- Commit: af82536c4 (local only). Dated amendment document; does
  NOT modify the frozen prereg.
- Purpose: document the process deviation in the COMP-1 build
  (170e39424) relative to the frozen prereg (4f6f0c5c8), per red
  team 7ffc2dae4 recommendation.
- The deviation: the frozen prereg specifies "Cognition source
  lines added: projected at most 150", "cognition source lines
  (bound 150)", "Exact count is an implementation measurement;
  growth past the bound without a fresh prereg fails review." K1
  incorporates "the One-System accounting bound" by reference. The
  implementation's fenced bootstrap miss-policy section
  (comp1.zag, lines 459-632) contains 157 non-blank, non-comment
  code lines (independently verified by shell count of the
  committed source; matches the red team measurement). Actual: 157.
  Bound: 150. Overage: 7 lines (4.7%).
- Materiality: zero capability impact (P1-P5 held, K2/K3 hold). The
  red team found the prereg's "bound" language is stronger than the
  builder's "+7 variance on a projection" framing.
- The frozen bound is NOT retroactively altered. This amendment is
  a separate dated document. It must be frozen before any SURVIVES
  consideration of COMP-1.
- Governance: zero Python; paper zero-diff; original prereg
  untouched; no sealed FW1-FW9.

**Status: EXPLORATORY** (governance documentation; the amendment
must be frozen before SURVIVES consideration).

### C151. Inquiry NAMECHECK record correction (REMEDIATION-COMPLETE)

- Commit: 1c84f8116 (local only). Appended correction note (22
  lines); all prior content preserved; no history rewrite.
- What was corrected: the inquiry build NAMECHECK.md (396ecafa4)
  Step 0 claimed "Zero invocations during this wave," contradicting
  the BUILD_REPORT's self-disclosure of one python3 invocation.
  Same error class as composition scout incident 5 (corrected at
  67f92ed4f; the correction follows that pattern).
- The appended note: retracts the false Step 0 statement; records
  the one self-disclosed python3 invocation (text-patch of a /tmp
  scratch copy, deleted without execution; no Python in research
  computation, scoring, or results); aligns with Python audit 2
  incident 9 (4a97c985c) and ledger C129
  (INQUIRY-BUILD-PROCESS-FAIL); states the wave remains
  PROCESS-FAIL per the literal guard; notes the scientific bars
  have no standing until the clean re-freeze (complete at
  18ed3331c, ledger C134).
- Governance: zero Python this wave; paper zero-diff; no sealed
  FW1-FW9; only the two owned paths touched.

**Status: REMEDIATION-COMPLETE** (record inconsistency resolved;
pattern matches C133).

### C152. Ledger cycle 14 append (EXPLORATORY)

- Commit: aada2ada7 (local only). Appended C134-C142 to the
  canonical ledger (133 -> 142 claims).
- The 9 claims: C134 INQUIRY-REFREEZE-BUILD (BUILD-PASS,
  18ed3331c); C135 TNN-1-REDTEAM (ADVERSARY-QUALIFIED, cbde38737);
  C136 MUL-REDTEAM (ADVERSARY-QUALIFIED with no qualifications,
  44f22979b; per parent's governance decision, the conservative
  existing taxonomy was used, no new status invented); C137
  COMP-1-REDTEAM (ADVERSARY-QUALIFIED, 7ffc2dae4); C138
  PYTHON-AUDIT-2 (EXPLORATORY, 4a97c985c); C139
  DEVINT-REPORT-CORRECTED (REMEDIATION-COMPLETE, a003bd19b); C140
  COMPRESSION-UPDATE (EXPLORATORY, 78a556e3a); C141
  FREEZE-RERUN-PLANNED (EXPLORATORY, 4e36f31f2); C142 BUNDLE-V14
  (BACKUP-VERIFIED, 323e3bbb4).
- Ledger state after append: 142 claims. Zero new SURVIVES (34
  total, all bounded L2/L2+). L3 achieved anywhere: still zero.
- Process disclosure: this wave is PROCESS-FAIL on process grounds
  per the literal Worker Toolchain Guard (12th Python incident
  overall). During pre-commit verification, the worker invoked
  `python3 -c` to byte-check the three touched files for em dashes.
  This was a verification convenience, not research computation;
  no Python-derived content is in the committed files. The check
  was immediately re-run with shell-only tools (all three files
  confirmed zero em dashes). The incident is disclosed in
  ledger_cycle14/NAMECHECK.md and the commit message. The ledger
  content itself is verified correct. The parent may accept the
  commit on content grounds or order a clean re-append of the same
  9 claims.
- Governance: paper zero-diff; no sealed FW1-FW9; append only, no
  prior claim body modified.

**Status: EXPLORATORY** (ledger state record; the content is
verified correct, but the wave carries PROCESS-FAIL on process
grounds; a clean re-append may be ordered).

---

## Not ready (no claims assigned this cycle)

All 10 completed results above have draft claims. No in-flight
workers are pending claim assignment at draft time.

---

## Cycle 15 tally when appended

C143-C152 = 10 new claims. Ledger goes 142 -> 152.

- PREREG-FROZEN: 1 (C146, MUL Rung B prereg)
- EXPLORATORY: 8 (C143 F-INT4 disposition, C144 EXECUTE evidence,
  C145 cognition remeasurement, C147 TNN-1 repro, C148 DEVINT
  triage, C149 ACT coverage, C150 COMP-1 amendment, C152 ledger 14
  append)
- REMEDIATION-COMPLETE: 1 (C151 inquiry NAMECHECK correction)

Zero new SURVIVES. L3 achieved anywhere: still zero.
BUILD-PASS total: 15 (unchanged).
PROCESS-FAIL total: 5 (unchanged; the 10th, 11th, and 12th incidents
are disclosed in C149, C145, and C152 claim bodies as wave-level
PROCESS-FAIL designations, but these are analysis/documentation
waves, not build waves, so no new PROCESS-FAIL claims are
proposed; the append worker or Micah should confirm this
treatment).

Note on C145: the 641-line cognition figure is awk-verified, but
the wave carries PROCESS-FAIL (11th incident). The parent should
decide whether the measurement stands or requires a fully clean
re-do before the figure is adopted.

Note on C146: the prereg document asserts frozen status, but an
independent freeze verification is in flight. If it finds the
prereg incomplete, this claim will be amended.

Note on C149 and C152: the analysis/ledger content is verified
correct and untouched by the incidents; the PROCESS-FAIL
designations are on process grounds per the literal guard.

No em dashes were used in this document (verified with the shell-only
byte check before commit).
