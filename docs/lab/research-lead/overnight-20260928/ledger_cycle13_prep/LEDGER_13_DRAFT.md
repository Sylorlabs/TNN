# Ledger Cycle 13: Draft Claim List

Date: 2026-09-30. Prepared from completed work since C124 (commit b81ca69ed).
Draft only. The canonical ledger is NOT modified by this file.

Ledger baseline: 124 claims. This cycle proposes C125 through C133
(9 new claims). Ledger would go 124 -> 133.

---

## Ready now (9 claims)

### C125. INTEGRATION-PREREG-FROZEN (PREREG-FROZEN)

- Commit: 7fc7148ac (local only).
- Content: the frozen one-system TNN-1 specification,
  PREREG_INTEGRATION.md (480 lines), design only, no implementation.
- Key frozen elements: unified workspace in CLA-2 format (40-byte nodes,
  16-byte edges, 1024 nodes / 4096 edges); port list (CLA-2 workspace
  machinery, 7 core primitives, POLICY_ROOT/MISS_POLICY, COMP-1 plan
  construction with accessor renaming only, CAM-1 verify/promote/contradict,
  ACT 5-step protocol with directional bid); delete list (CAM-1 eval_body
  menu buried not ported, dead code, duplicate spellings); kill bars
  K1-K5 including the hard 1200-line ceiling (F-INT1); falsification
  F-INT1 through F-INT6 (including F-INT4, the trench-coat test:
  a query-miss plan must become an action guide through shared edges);
  predictions P-INT1 through P-INT7 including the DEVINT-CLA2 11-stage
  curriculum re-run on the integrated workspace.
- Governance: Step 0 guard recorded, zero Python; dash-clean; paper
  zero-diff; no sealed FW1-FW9 accessed; Micah's pending EXECUTE ruling
  (1fc77503b) noted as inherited, not canonized.

**Status: PREREG-FROZEN.**

### C126. INQUIRY-PREREG-FROZEN (PREREG-FROZEN)

- Commit: 04ac028fb (local only).
- Content: the frozen learner-driven inquiry experiment,
  PREREG_INQUIRY.md (422 lines), design only, no implementation.
- Key frozen elements: Piece A (uncertainty reification: 12 ignorance
  admissions -> exactly 12 UNCERTAINTY nodes with ref0 = key context and
  complete learner-side creation trace; ablation A1); Piece B (guide
  construction: 12 ACTION-GUIDEs within 10 events each, anchored at the
  uncertainty node, selecting CHOICE 30 INQUIRE never 31, after a 20-event
  experience window W1; ablation A2); four phases (reification, construction,
  W6-class attribution with swap-test bar 10/12 and binomial tail 0.019,
  novel-domain transfer with conflicting-evidence -3 admissions); kill bars
  K-INQ1 through K-INQ4 (including a 300-cognition-line bound on both
  pieces combined and zero new semantic cases/modes/bridges/handlers);
  falsification F-INQ1 through F-INQ5; controls C1-C3.
- Both pieces constrained to learner-side workspace processes composed
  only of frozen ISA primitives, no core source changes authorized.
- Governance: Step 0 guard recorded, zero Python; dash-clean; paper
  zero-diff; no sealed FW1-FW9 accessed.

**Status: PREREG-FROZEN.**

### C127. TNN-1 one-system integration built (BUILD-PASS)

- Commit: 0323b97d5 (local only).
- Source: tnn1.zag, 1088 source lines (1090 reported incl. header),
  under the frozen 1200-line F-INT1 ceiling. Binary built with pinned
  znc abed8aa1, not committed.
- Implementation: unified CLA-2-format workspace; 7 core primitives
  (ALLOC, WRITE, LINK, ACTIVATE, DECAY, EXECUTE with closed 4-op ISA:
  MOVE, BRANCHEQ, INC, DEC); 13 edge types (CLA-2's 12 + E_CORROB for
  post-promotion corroboration); 3-step eviction with directional bid;
  COMP-1 plan construction (3 frozen templates, post-hoc expected-only
  verification, e-ruling preserved); CAM-1 verify/promote/contradict
  only (eval_body 4-way menu deleted per red team); unified query path
  (exact-key hit -> plan construction -> P-INV bootstrap -> HISTORY/regret
  -> -2); ACT 5-step read path with directional signed bid.
- Tests: 35/35 pass. P-INT1 (CLA-2 suite 15/15), P-INT2 (ACT directional
  bid 6/6), P-INT3 (COMP-1 10/10), P-INT4 (CAM-1 ported P6/P7 2/2),
  P-INT5 (DEVINT-CLA2 compact 11-stage curriculum 1/1), F-INT4
  (cross-capability XCAP 1/1: query plan -> MAP -> ACT guide ->
  contradiction demotes both standing and bid).
- Determinism: 3 consecutive runs byte-identical (P-INT6).
- K1: prereg 7fc7148ac verified ancestor of 0323b97d5. K2: zero new
  ops/cases/modes/bridges/handlers; exactly 3 templates; line ceiling
  holds. K3: pure Zag; Step 0 guard recorded.
- The DEVINT-CLA2 re-run uses a compact curriculum hitting the same
  frozen stage numbers rather than a line-for-line port (the 1251-line
  standalone cannot fit within the 1200-line total).
- Governance: no em dashes; paper zero-diff; sealed FW1-FW9 never touched.

**Status: BUILD-PASS** (builder verdict only; the 11-stage promotion
pipeline has not run). No L3 or SURVIVES claim.

### C128. MUL-1 Rung A: learner constructs multiplication (BUILD-PASS)

- Commit: fbf14f73a (local only).
- Source: mul1.zag (pure Zag, pinned znc abed8aa1, zero warnings).
  Per frozen MUL prereg 222899314, ISA ruling 0525377f3.
- Result: the learner constructed MUL via trial-based composition from
  the domain-neutral vocabulary. After 4,297 incorrect candidates, it
  promoted a 4-cell PROC [ACCUM_RX STEP_C TEST_CY GOTO(0)]: a genuine
  loop (R += X; C += 1 until C == Y). More efficient than the prereg's
  6-cell sketch: the learner discovered zero-initialized slots make
  INITs unnecessary. Six learner-made structural decisions documented.
  No new arithmetic op; no MUL, SUB, or loop primitive in source.
- Tests: P-MUL1 8/8 held-out probes + scaling (13,17)->221 PASS;
  P-MUL2 Tier 2 structural (back-edge, accumulation cell, data-dependent
  termination) PASS; P-MUL3 ablation destroys multiplication (8/8 fail)
  while ADD and unrelated facts intact PASS; P-MUL4 transfer on different
  surface encoding (named attributes width=6/height=7 -> area 42 via MUL
  EXECUTE) PASS; P-MUL5 lookup control 0/8 (ceiling 2), margin 8 PASS.
- Oracle audit: correct not first (trial 4298), 72 genuine rejections
  (minimum 3), shuffled rerun re-promotes a 12/12 program (order not
  load-bearing). PASS.
- Determinism: 3 runs byte-identical (sha256 72a54993...).
- One real bug fixed during development (wset pay-field offset collided
  with the valid flag); workspace execution verified correct after.
- K1: prereg 222899314 verified ancestor of fbf14f73a. K3/K4 scans
  clean. Rung B deferred per prereg sequencing.
- Governance: restricted safebin PATH, python3 ABSENT, zero forbidden
  invocations; no em dashes; paper zero-diff; FW1-FW9 never touched.

**Status: BUILD-PASS** (builder verdict only; the 11-stage promotion
pipeline has not run). No L3 or SURVIVES claim.

### C129. Inquiry build wave process-fail (PROCESS-FAIL)

- Commit: 396ecafa4 (local only).
- Content: the INQUIRY-1 implementation (inquiry.zag, 936 lines)
  completed all frozen bars: P-INQ1 (12 admissions -> 12 nodes, ref0=key,
  trace complete), A1, W1+P-INQ2 (12 guides, all CHOICE 30, within 10
  events), A2, P-INQ3 (>=10/12 genuine/decoy), P-INQ3b, P-INQ4 (>=16/20),
  P-INQ5a/b/c (novel conflict-type transfer, zero researcher mapping),
  controls C1/C2/C3 as expected; K-INQ1 through K-INQ3 pass; 115
  cognition lines under the 300 budget; 3/3 byte-identical.
- Process incident: the builder self-disclosed invoking `python3` once
  to text-patch a /tmp scratch copy (inserting diagnostic prints). The
  copy was deleted without execution. No Python touched research
  computation, scoring, or results; inquiry.zag was written via file
  tools and all results come from the pure-Zag binary.
- Per the Worker Toolchain Guard, any forbidden-executable invocation
  makes the wave PROCESS-FAIL. The scientific result is uncontaminated
  but must be cleanly re-frozen before any claim can rest on it. A
  clean re-freeze worker is in flight.
- K1: prereg 04ac028fb verified ancestor of 396ecafa4.

**Status: PROCESS-FAIL** (documentation of the wave; the bars it
measured are recorded here for the re-freeze to reproduce, not as
adopted results).

### C130. DEVINT-CLA2 red team audit (ADVERSARY-QUALIFIED)

- Commit: a5ccb100d (local only). Read-only attack; target unmodified.
- Per-vector verdicts:
  - Vector 1 (unseen domain transfer): ATTACK-SUCCESS. form_groups
    replays the frozen harness corpus instead of operating on the
    learner's accumulated experience; feed_episode/segment_episode
    hardcode length-3 substrings. A novel domain fails at the
    mechanism level, not just the stage checks.
  - Vector 2 (long interference, 10x): ATTACK-SUCCESS. Evidence-cascade
    failure: 200 distractors + 60 evictions killed all 3 rules because
    unprotected bid-0 evidence nodes evict first, collapsing rule bids,
    and the positional tie-break (lowest node id) finishes them. M2
    (m2_check) is defined but never called, so the BUILD_REPORT's
    "M2 holds" claim is unmeasured. Prereg S10's post-eviction accuracy
    was not implemented.
  - Vector 3 (stage-label leakage, B3): ATTACK-PASS with caveat.
    feed_episode takes only episode bytes; no stage/task/mode params.
    The leakage present is domain-answer leakage, not stage-label.
  - Vector 4 (GROUP protection under pressure): ATTACK-SUCCESS
    (conditional). The learner-authored PROTECT anchor (bid 0) is
    evicted on the first eviction; protection works only because the
    anchor is hardcoded node 2 and evict_one hard-skips nodes 0-2.
    Rule payload support counters never decrement when evidence edges
    are evicted (payload=5, edges=0).
  - Vector 5 (contradiction handling): ATTACK-SUCCESS (partial). S7
    boundary violations are a harness-local counter only; split_group
    is defined but never called (SPLIT never attempted); retention is
    blind to demotion (demoted rule with bid 4 survived 55 evictions).
    What holds: CONTRADICTS edges, demotion, retrievable history.
  - K1/K2/K3: K1 PASS (f24063bcb ancestor of 35f9500b2); K2 qualified
    PASS (zero modes/bridges/handlers; qualifications: form_groups
    coupling, S6 pairing harness-supplied, positional tie-break);
    K3 PASS (pure Zag).
- Strongest single finding: S6 "procedure learning" does not learn
  from examples. s6_train_out is never called; learn_procedure takes
  the pairing as explicit harness arguments derived by byte-matching.
  The 5/5 check verifies storage/retrieval of a harness-supplied
  pairing, not induction.
- Bottom line: frozen B1-B5 literally hold, so C119 BUILD-PASS stands.
  But six prereg-specified elements were not implemented as specified
  (M2, post-eviction accuracy, examples-to-criterion, SPLIT, violation
  representation, pairing induction), and the retention mechanism has
  three genuine fragilities (evidence cascade, anchor dependence,
  demotion-blindness). The BUILD_REPORT's M2/F4 claims need correction
  before any SURVIVES consideration.

**Status: ADVERSARY-QUALIFIED** (4 attack vectors succeed; the build's
frozen bars hold but its broader claims do not).

### C131. C1 harness resume bug fixed (REMEDIATION-COMPLETE)

- Commit: fac9875b0 (local only).
- The fix: refreeze_drive.sh now does `rm -rf "$d"` before
  `mkdir -p "$d"` in run_one(), matching the pattern already correct
  in drive_remaining.sh. The Zag driver never clears state/ itself;
  without this, resume after interruption re-ingests all turns on
  stale state, doubling every weight.
- Verification (test_harness_fix.sh): baseline fresh dir 63/63 with
  32 facts; OLD behavior (resume without clearing) 58/63 with 62
  facts (bug reproduced, facts exactly doubled); NEW behavior (resume
  with fix) 63/63 with 32 facts, identical to fresh run.
- Harness-only fix. No contestant binary changes, no driver Zag source
  changes. drive_all.sh has the same latent issue (no skip logic,
  assumes fresh tree); flagged for hardening or fresh-run-only
  documentation.
- Governance: zero Python invocations; paper zero-diff; no sealed
  FW1-FW9 accessed.

**Status: REMEDIATION-COMPLETE.** C115's investigation is now closed
with a verified fix.

### C132. Architecture compression tracker established (EXPLORATORY)

- Commit: f46a89e99 (local only).
- Content: COMPRESSION_TRACKER.md, the living architecture-accounting
  document, plus NAMECHECK.md with the Step 0 guard record.
- Defines Micah's metric: "How much general capability does each
  researcher-authored line buy?" Three ratios: R_test (provisional,
  self-tests / cognition lines), R_world (canonical, freeze-worlds /
  lines), R_fw (future canonical, sealed FW1-FW9 / lines).
- Current snapshot: frozen core (586 lines, 1/9 worlds), contlearn2
  (136), CLA-2 (685, 15/15, 3 structures), CAM-1 (408, 6/6, 1
  structure, bounded L2), ACT (162, 24/24, 2 structures), COMP-1
  (~300 estimated, 10/10, 5+ structures), DEVINT-CLA2 (informational
  row, unmeasured). One-System metrics zero across every row
  (modes/bridges/handlers/semantic cases).
- Arithmetic correction recorded as a dated note, not an edit: the
  4-system total is ~1555 cognition lines (1255 measured + ~300
  estimated for COMP-1), correcting the earlier 2134 figure which had
  used COMP-1's total source lines instead of cognition lines.
- Integration target row (to be filled when TNN-1 lands): ~1100
  projected lines, hard 1200-line ceiling, one binary passing CLA-2
  15 + ACT 24 + COMP-1 10, CAM-1 menu source-scan ban, sealed FW1-FW9
  run, R_fw computation.
- Trajectory reading: lines negative (1555 > 586), One-System metrics
  holding at zero, learner-created structures positive (0 -> 11+).
  Largest evidence gap: cross-comparable capability (no builder system
  yet run on the same worlds).
- Update protocol: append rows after every builder landing, integration
  milestone, or sealed-world run; never edit historical rows.
- Governance: dash-clean; paper zero-diff; sealed FW1-FW9 never
  accessed; one transient .git/index.lock handled per the no-remove
  rule (waited, cleared on its own, retried).

**Status: EXPLORATORY** (measurement infrastructure, not a capability
claim).

### C133. Composition scout record corrected (REMEDIATION-COMPLETE)

- Commit: 67f92ed4f (local only).
- Content: the composition scout NAMECHECK.md is amended with a dated,
  attributed correction note that explicitly retracts the false
  "No Python invoked at any point in this task" statement and records
  the 5th Python process incident consistent with ledger C98 (worker
  ran `python3 -c "pass"` as a stray fragment; no research logic
  depended on it; process failure per the literal rule). Scientific
  content unaffected (pure markdown analysis, scout only). All other
  file content preserved untouched.
- The ledger already recorded this incident correctly at C98, so no
  ledger edit was needed; the correction aligns the two records.
- Resolves guard audit (e0a842962, C123) recommendation 1.
- Governance: zero Python this wave; no em dashes (byte-verified);
  paper zero-diff; explicit pathspecs; ledger untouched per scope.

**Status: REMEDIATION-COMPLETE.**

---

## Not ready (in-flight workers, no claims assigned)

- Inquiry clean re-freeze (descendant of prereg 04ac028fb; zero-Python
  tolerance): claim pending its completion commit.
- TNN-1 red team (integration genuineness, line-count honesty, template
  smuggling, menu resurrection, determinism, cross-suite interference):
  claim pending its completion commit.
- MUL red team (lookup smuggling, oracle leakage, scaling, structural
  honesty, ablation, determinism): claim pending its completion commit.
- Bundle v14 (blockers cleared): claim pending its completion commit.

---

## Cycle 13 tally when appended

C125-C133 = 9 new claims. Ledger goes 124 -> 133.

- PREREG-FROZEN: 2 (C125, C126)
- BUILD-PASS: 2 (C127, C128)
- PROCESS-FAIL: 1 (C129, inquiry wave; documentation of the wave)
- ADVERSARY-QUALIFIED: 1 (C130)
- REMEDIATION-COMPLETE: 2 (C131, C133)
- EXPLORATORY: 1 (C132)

Zero new SURVIVES. L3 achieved anywhere: still zero.
BUILD-PASS total: 14 (was 12, added C127, C128).
PROCESS-FAIL total: 5 (was 4, added C129).

Note on C129: per the guard, the inquiry wave is process-failed. The
bars it measured are recorded here so the in-flight clean re-freeze
can reproduce them; they carry no adopted-result standing until the
re-freeze lands.

No em dashes were used in this document (verified with the shell-only
byte check before commit).
