# Ledger Cycle 14: Draft Claim List

Date: 2026-09-30. Prepared from completed work since C133 (commit d5e3222b6).
Draft only. The canonical ledger is NOT modified by this file.

Ledger baseline: 133 claims. This cycle proposes C134 through C142
(9 new claims). Ledger would go 133 -> 142.

---

## Ready now (9 claims)

### C134. Inquiry clean re-freeze (BUILD-PASS)

- Commit: 18ed3331c (local only).
- Content: the INQUIRY-1 experiment re-implemented from scratch
  (inquiry_refreeze/inquire.zag, 935 lines, pure Zag, pinned znc
  abed8aa1) after the prior wave (396ecafa4, C129) was ruled
  PROCESS-FAIL for a self-disclosed python3 invocation.
- Result: all frozen bars pass. P-INQ1 (12 queries -> exactly 12
  UNCERTAINTY nodes, ref0 = key, marker 2, trace 161); A1 (reify
  disabled -> 0 nodes); W1 + P-INQ2 (8-key experience window, then 12
  fresh keys -> 12 guides, all CHOICE 30, within 10 events); A2
  (construct disabled -> 0 guides, 0 emissions); P-INQ3 (>=10/12
  attribution); P-INQ3b (first inquiry strictly after first
  admission, no pre-play); P-INQ4 (>=16/20 follow-ups return
  observations); P-INQ5a/b/c (novel conflict-type transfer: 8
  UNCERTAINTY nodes marker 3, 8 guides selecting CHOICE 30,
  >=12/16 resolutions); C1/C2/C3 (scaffolding passes, null policy
  silent, alternating guides fail bars, non-vacuous).
- Kill bars: K-INQ1 PASS (prereg 04ac028fb verified ancestor before
  implementation and at commit time). K-INQ2 PASS, triple-verified:
  (1) source inspection (zero modes/bridges/handlers/semantic cases,
  zero branches on domain/relation/task/type/content); (2)
  creation-trace audit (all nodes carry 161/162 + DEPENDS edges);
  (3) e-ruling (construction receives only node addresses).
  Cognition lines: 149 (under the 300 budget). K-INQ3 PASS (3/3 runs
  byte-identical, sha256
  42a8d060e7a363093438aaae69bb36d1ff5bb9124b6dc07cd405a30aa43f598a).
  K-INQ4 PASS (zero Python via restricted PATH where python3 was
  absent; paper zero-diff; no FW1-FW9 access).
- Falsifiers F-INQ1 through F-INQ5: none triggered.
- Governance: Step 0 guard recorded with restricted safebin PATH;
  zero forbidden invocations; no em dashes; paper zero-diff; sealed
  FW1-FW9 never touched.

**Status: BUILD-PASS** (builder verdict only; the 11-stage promotion
pipeline has not run). This supersedes the C129 PROCESS-FAIL wave:
the bars C129 recorded are now reproduced in a clean wave and carry
adopted-result standing. No L3 or SURVIVES claim.

### C135. TNN-1 red team audit (ADVERSARY-QUALIFIED)

- Commit: cbde38737 (local only). Read-only attack; target unmodified.
- Target: tnn1.zag @ 0323b97d5 (1088 lines, 153 functions).
- Per-vector verdicts (5 ATTACK-PASS, 1 qualified ATTACK-SUCCESS):
  - Vector 1 (integration genuineness): ATTACK-SUCCESS (qualified).
    The workspace IS genuinely shared: ev_query, ev_teach, ev_act,
    plan construction, promote_map, contradict_map all operate on
    the same W:[]u8. Not three systems in a trench coat at the
    state level. BUT the XCAP test (t_xcap, F-INT4) does not prove
    the prereg's strongest claim. It never calls ev_act and never
    shows the query's MAP becoming an action guide. It creates a
    SYNTHETIC guide node, contradicts it, and verifies both
    map_standing and bid demote. That verifies metric co-location
    on one node, not plan-to-guide conversion. The builder's own
    report acknowledges the synthetic node. Recommendation:
    strengthen F-INT4 or narrow its claim.
  - Vector 2 (line-count honesty): ATTACK-PASS (with note). 1088
    lines, 153 functions. One dead function (verify_plan, 11
    lines, logic inlined in mp_run). Fundamentally honest.
  - Vector 3 (template smuggling): ATTACK-PASS. Exactly 3 base
    templates (plan_c2, plan_g, plan_it). TM_COMP=4 is the
    prereg-authorized TM_COMPOSED marker, not a fourth template.
    No semantic cases.
  - Vector 4 (menu resurrection): ATTACK-PASS. No eval_body, no
    LITERAL/COPY_A/DBL_A/ADD_AB. Dispatch branches on ISA opcodes
    (READ/MOVE/BEQ/INC/EMIT/APPLY), not domain templates. Generic
    execution machinery, prereg-authorized.
  - Vector 5 (determinism): ATTACK-PASS. 3 runs byte-identical
    (sha256 78847448a6...).
  - Vector 6 (cross-suite interference): ATTACK-PASS. 35 tests,
    each with fresh z_alloc(110656) workspace. No shared state;
    order-dependence structurally impossible.
- Kill bars: K2 PASS (zero modes/bridges/handlers, 1088 < 1200).
  F-INT3 PASS. F-INT4 QUALIFIED (see vector 1).
- Governance: zero Python; target unmodified; sealed FW1-FW9 never
  accessed; paper zero-diff; no em dashes.

**Status: ADVERSARY-QUALIFIED** (the integration is structurally
real, but F-INT4 as frozen does not discriminate plan-to-guide flow
from metric co-location; the XCAP claim needs strengthening or
narrowing before SURVIVES consideration).

### C136. MUL-1 Rung A red team audit (ADVERSARY-CLEARED, proposed)

- Commit: 44f22979b (local only). Read-only attack; target unmodified.
- Target: mul1.zag @ fbf14f73a.
- All 6 attack vectors: ATTACK-PASS (no successful attacks).
  - Vector 1 (lookup smuggling): PASS. run_prog and ws_exec are
    genuine interpreters with no lookup tables. The only product
    data is ex_p (12 training labels, the intended supervised
    signal) and pr_p (probe labels, scoring only). Data-flow audit
    confirms the search never sees probe answers.
  - Vector 2 (oracle leakage): PASS. Trial enumeration is a
    standard length-first lexicographic odometer. Verified
    arithmetically: trial 4298 = cell codes [2,4,5,7] at the
    3209th position of L=4 (2*11^3+4*11^2+5*11+7=3208,
    0-indexed). The shuffled rerun promotes the identical program,
    confirming order is not load-bearing. 72 genuine rejections
    confirm a discriminating search.
  - Vector 3 (scaling): PASS. The promoted program is a genuine
    loop (R+=X; C+=1 until C==Y) that computes X*Y for all
    non-negative inputs by construction. Binary verifies
    (13,17)->221 via the workspace graph. One documented boundary:
    negative Y would not terminate; out of prereg scope (Phase 5
    revision probes deferred).
  - Vector 4 (structural honesty): PASS. check_tier2 operates on
    the actual workspace graph: back-edge with earlier target,
    accumulation cell in loop body, data-dependent termination
    test all verified present. 8/8 probe agreement between
    search-time and post-promotion execution confirms faithful
    materialization.
  - Vector 5 (ablation): PASS. Ablation invalidates PROC nodes;
    ws_exec returns unknown. ADD survives because it is a core ISA
    primitive, not workspace state. This is the honest claim.
  - Vector 6 (determinism): PASS. 3 independent runs
    byte-identical; sha256 matches BUILD_REPORT exactly.
- Governance: zero Python; dash-clean; paper zero-diff; no sealed
  FW files; read-only attack.

**Status: ADVERSARY-CLEARED (proposed).** No ledger precedent exists
for a red team with zero successful attacks; the 8 existing
ADVERSARY-QUALIFIED claims all carry qualifications, and the 6
ADVERSARY-BREAKS claims record breaks. This draft proposes the new
status to distinguish a clean adversarial audit from a qualified
one. If the ledger prefers, ADVERSARY-QUALIFIED with the note
"no qualifications" is the conservative fallback. The C128
BUILD-PASS stands unqualified by adversarial review.

### C137. COMP-1 red team audit (ADVERSARY-QUALIFIED)

- Commit: 7ffc2dae4 (local only). Read-only attack; target unmodified.
- Target: comp1.zag @ 170e39424.
- Per-vector verdicts (4 ATTACK-PASS, 1 process-level
  ATTACK-SUCCESS):
  - Vector 1 (template enumeration): ATTACK-PASS. Exactly three
    template constructors (plan_chain2, plan_gather, plan_iterate).
    plan_new is called with tm=4 only from the two composition
    functions. The tm=4 (COMPOSED) marker is written but never
    dispatched on; no if(tm==4) branch exists. All T_PLAN nodes go
    through plan_new; the executor handles exactly six step kinds
    with no hidden seventh.
  - Vector 2 (three-hop genuineness): ATTACK-PASS.
    plan_extend_read and plan_compose_c2 genuinely operate on plan
    structure: they walk the SEQ chain, clone steps with operands,
    compute the extension point from the input plan via
    chain_outslot, and draw appended relations from
    subject-incident relations of the executed intermediate.
    Different input plans produce structurally different composed
    plans. Real composition, not a fixed fourth template.
  - Vector 3 (expected-value leakage, e-ruling): ATTACK-PASS.
    Structural, not just test-observed: mp_build and
    mp_build_compose take no expected parameter; expected appears
    only in mp_run's post-construction selection loop; the masked
    bit is never consulted during construction; the query node
    holding expected is never passed to either constructor. No
    code path exists for expected to reach construction.
  - Vector 4 (bootstrap budget): ATTACK-SUCCESS (process-level).
    The fenced section holds exactly 157 code lines vs the prereg
    bound of 150. The prereg uses the word "bound" three times and
    states "growth past the bound without a fresh prereg fails
    review"; K1 references "the One-System accounting bound." No
    fresh prereg was written. The BUILD_REPORT's "variance on a
    projection" framing understates the prereg's own language.
    Materiality is low (7 lines, 4.7%, zero capability impact),
    but the deviation is real. Recommendation: a prereg amendment
    documenting the 157-line actual before any SURVIVES
    consideration.
  - Vector 5 (determinism): ATTACK-PASS. Three independent runs of
    comp1_bin: 10/10 each, byte-identical via cmp.
- K1/K2/K3 spot-check: all PASS (ancestor verified, zero
  handlers/cases/modes/bridges, pure Zag).
- Governance: Step 0 guard recorded; zero Python; paper zero-diff;
  no sealed FW1-FW9 accessed.

**Status: ADVERSARY-QUALIFIED** (all scientific claims under attack
hold; the single finding is process-level: the 7-line bound
overage needs a prereg amendment before SURVIVES consideration).

### C138. Python incident audit 2 (EXPLORATORY)

- Commit: 4a97c985c (local only).
- Scope: all 16 commits on tnn-native-lab since guard audit
  e0a842962 (C123). Method: shell and git only. Zero Python
  invocations during the audit itself.
- Findings: 1 new Python incident (the 9th overall). 15 commits
  clean. Incident 9 is the inquiry build (396ecafa4): the worker
  invoked python3 once to text-patch a /tmp scratch copy
  (diagnostic prints); the copy was deleted without execution.
  Zero scientific impact: no Python in research computation,
  scoring, or results. Self-disclosed in BUILD_REPORT.md
  "Toolchain Incident" section. Adjudicated PROCESS-FAIL per the
  Worker Toolchain Guard. The clean re-freeze (C134) now stands
  in its place.
- Record inconsistency flagged: the inquiry NAMECHECK.md Step 0
  claims "Zero invocations during this wave," contradicting the
  BUILD_REPORT disclosure. Same error class as composition scout
  incident 5 (C98/C133). Should be corrected.
- Note on incident 8 (STATUS doc 6e4a9479f): chronologically before
  the guard audit commit (18 seconds earlier) but not in its list
  of 7. The guard audit likely finalized before it was known. This
  audit adopts the parent's numbering (STATUS=8th, inquiry=9th).
- PROCESS-FAIL handling verified: neither the STATUS wave nor the
  inquiry wave's output has been used as input to clean scientific
  claims. The inquiry re-freeze builds from the frozen prereg, not
  the failed implementation.
- Guard effectiveness: self-disclosure 100% (both new incidents
  self-disclosed by workers); Step 0 records 100% compliance (all
  16 commits have NAMECHECK.md); zero scientific contamination
  across all 9 incidents to date. Weakness: restricted PATH
  adoption is weak. Only 1 of 16 workers (MUL builder) used a true
  safebin where python3 was ABSENT. The other 15 claimed "surgical
  PATH removal not possible" and relied on documented non-use. The
  MUL builder proves it IS possible. Recommendation: make safebin
  default for builder workers. The inquiry re-freeze (C134) used
  the safebin technique successfully.
- Governance: zero Python this wave; no em dashes (byte-verified);
  paper zero-diff; explicit pathspecs; read-only audit (no worker
  files modified).

**Status: EXPLORATORY** (governance audit, not a capability claim).
Total incidents to date: 9. All process-level. Zero scientific
contamination.

### C139. DEVINT-CLA2 report corrected (REMEDIATION-COMPLETE)

- Commit: a003bd19b (local only).
- Content: the DEVINT-CLA2 BUILD_REPORT.md is amended with a dated
  (2026-09-30) correction note per red team a5ccb100d (C130)
  recommendation 1. All other BUILD_REPORT content preserved
  untouched. Red team report and implementation not modified.
- Corrections:
  - M2 retracted as measured: m2_check (line 663) is defined but
    never called; the frozen M2 metric was never computed. Correct
    statement: M2 was not measured. GROUPs survived S10 via
    harness-authored PROTECT edges, not bid-driven retention.
  - F4 guard qualified as vacuous: because the bid-vs-survival
    correlation it guards was never computed, the guard is vacuous
    as stated. Also notes the positional tie-break in evict_one
    becomes the decider under bid-collapse, weakening F1 under 10x
    interference.
  - Cites the red team report as the source.
  - States B1-B5 and the 11 stage results are unaffected;
    BUILD-PASS stands; corrections must be addressed before any
    SURVIVES consideration.
- Governance: Step 0 guard recorded; zero Python; no em dashes
  (byte-verified); paper zero-diff; explicit pathspecs; read-only
  on red team report and implementation.

**Status: REMEDIATION-COMPLETE.** Resolves the C130 recommendation
on M2/F4 claims. The C119 BUILD-PASS (C130: stands, B1-B5 literally
hold) is unchanged; only the unmeasured claims are retracted.

### C140. Compression tracker updated with TNN-1 and MUL-1 (EXPLORATORY)

- Commit: 78a556e3a (local only).
- Content: COMPRESSION_TRACKER.md appended with new snapshot rows
  for TNN-1 and MUL-1 (historical rows untouched), trajectory
  reading update, open measurement items extended (items 6-10).
- Key findings:
  - First genuine compression: ~1555 cognition lines across four
    separate builds -> 1088 total source lines in one TNN-1 binary
    (~30% smaller), passing 35 tests spanning five formerly
    separate capability families plus the XCAP cross-capability
    interaction test.
  - TNN-1: 1088 lines measured (build report states 1090; both
    under the 1200-line F-INT1 ceiling). Test battery: P-INT1
    (CLA-2 15) + P-INT2 (ACT 6 compact) + P-INT3 (COMP-1 10) +
    P-INT4 (CAM-1 P6/P7) + P-INT5 (DEVINT compact) + XCAP = 35/35.
    R_test 3.22/100.
  - Deviation flagged, not hidden: TNN-1 carries a compact 6-test
    ACT battery (A1-A6), not the standalone 24/24 suite the
    integration prereg target row specified. Recorded in the
    tracker notes.
  - MUL-1: 563 lines measured. 5/5 P-MUL. R_test 0.89/100 (not
    comparable to capability batteries; its 5 tests are
    construction tests, noted as such).
  - Cognition-line caveat: the 1555->1088 comparison is
    source-line, not cognition-line. Formal classification per
    MEASUREMENT_PROCEDURE.md is open items 6-8. R_test values use
    total source lines until classified.
  - Inquiry (396ecafa4) recorded as PROCESS-FAIL per the guard,
    with clean re-freeze in progress (now C134). Not counted in
    any ratio.
  - Largest evidence gap unchanged: freeze worlds and sealed
    FW1-FW9 still not run on any builder system including TNN-1.
    Priority 5 (freeze rerun on consolidated core) is the next
    canonical measurement.
- All three result commits verified to exist (0323b97d5, fbf14f73a,
  396ecafa4). Fact verification from build files, not just task text.
- Governance: Step 0 guard recorded; zero Python; no em dashes;
  paper zero-diff; no sealed FW1-FW9 accessed; explicit pathspecs;
  append only.

**Status: EXPLORATORY** (measurement infrastructure, not a
capability claim).

### C141. Core Freeze re-run planned (EXPLORATORY)

- Commit: 4e36f31f2 (local only). No freeze executed.
- Content: FREEZE_RERUN_PLAN.md, the full plan for re-running the
  Core Freeze Challenge on the consolidated TNN-1 core.
- Key findings:
  - TNN-1 is ready to freeze, with qualifications: 1088 lines,
    35/35 tests, BUILD-PASS (C127). But the TNN-1 red team was
    still in flight at plan time (now C135, qualified on XCAP).
  - Critical gap: TNN-1 has no world-driver interface. The
    original freeze used a purpose-built world_learn.zag with the
    stage0/INTERFACE.md event protocol. TNN-1's tnn1.zag is a
    test-suite binary with no world-file input path. "Without
    source edits" cannot mean running it as-is against FW worlds.
    Either a zero-cognition driver shim is added (with frozen
    attestation and red-team review), or TNN-1 is declared
    not-freezable in current form.
  - Architectural deltas that matter: C75 eviction pathology
    (original 36-slot store with lowest-index tie-break dominated
    5 worlds; TNN-1 has 1024 nodes, 3-step eviction with
    directional signed bids; FW4/FW5 are the direct test);
    composition/procedures (original had none, W2 0/8; TNN-1 ports
    COMP-1's 3 templates + EXECUTE; FW2 and FW1 are the tests);
    action selection (original had fixed CHOICE 0, W7 0/4; TNN-1
    has ACT 5-step with directional bid; FW6/FW7 are the tests);
    contradiction (TNN-1 ports CAM-1 verify/contradict with
    E_CORROB edges; W5's failure was cascade, so the fix depends
    on the eviction fix holding).
  - Recommended scope: freeze TNN-1 alone (Option A), not
    TNN-1+inquiry. Inquiry is now clean (C134) but was in
    re-freeze at plan time; waiting would have delayed priority 5
    indefinitely. FW1-FW9 primary battery; W1-W9 re-run only as
    supplementary (original worlds are unsealed, so not
    adversarial).
  - Scoring is not "beat 1/9": the re-run measures (a) FW4/FW5 vs
    W4/W5 (C75 fix validation), (b) any construction/action world
    flipping FAIL to PASS, (c) FW1 non-regression, (d) zero
    capability source delta throughout.
- Five governance flags for Micah (presented, awaiting rulings):
  1. Driver-shim question (architectural): approve building a
     zero-cognition driver shim, or declare TNN-1 not-freezable
     as-is.
  2. New preregistration required (procedural): a re-run on a
     different artifact with different worlds needs its own frozen
     prereg. Not optional.
  3. EXECUTE boundary (inherited): TNN-1 uses the 4-op ISA whose
     exact placement (1fc77503b, amendments A-C) is still pending
     Micah's ruling. The freeze inherits this ambiguity.
  4. Inquiry scope (architectural): confirm Option A (freeze TNN-1
     without inquiry) or direct waiting for inquiry integration.
  5. W1-W9 re-run (methodological): recommend FW-first; W re-run
     supplementary only.
- Critical path: TNN-1 red team (done, C135) -> governance rulings
  (flags 1-4, pending) -> new prereg -> driver shim -> freeze
  record -> FW battery -> pure-Zag rescore -> ledger + compression
  tracker update.
- Governance: Step 0 guard recorded; zero Python; dash-clean;
  paper zero-diff; sealed FW1-FW9 files never accessed (only the
  design document at 200387b42 was read); explicit pathspecs; no
  freeze executed.

**Status: EXPLORATORY** (planning document, not an execution).
Priority 5 remains blocked on Micah's rulings for flags 1-4.

### C142. Bundle v14: verified backup (BACKUP-VERIFIED)

- Commit: 323e3bbb4 (local only, metadata commit).
- Bundle: ~/workspace/tnn-native-lab-20260930-v14.bundle
  - Size: 2.0G
  - SHA-256:
    06b43ac8db876447237da11e3e33d5f44e50e7d5277429deccf9396d89759481
  - HEAD captured: d5e3222b608c358b92332f0cad4020d00be71741
  - Refs: 69, commits on HEAD: 3279
  - git bundle verify: complete history confirmed
  - Supersedes v13
- Major work captured since v13: TNN-1 integration build + red
  team, MUL-1 build + red team, inquiry prereg + build
  (PROCESS-FAIL) + clean re-freeze, DEVINT-CLA2 red team, COMP-1
  red team, ACT bid alignment, C1 harness fix, guard audits,
  record correction, compression tracker, ledger cycles 12 and 13
  (133 claims).
- Process notes: working tree verified clean before each bundle
  creation. Bundle was recreated twice because concurrent workers
  landed new commits mid-task (Python incident audit 2, inquiry
  clean re-freeze, TNN-1/MUL red teams, ledger cycle 13). Final
  bundle HEAD matches repo HEAD at creation time (verified via
  list-heads comparison).
- Governance: zero Python this wave; paper zero-diff.

**Status: BACKUP-VERIFIED.** Supersedes v13 (C117).

---

## Not ready (no claims assigned this cycle)

All 9 completed results above have draft claims. No in-flight
workers are pending claim assignment at draft time.

---

## Cycle 14 tally when appended

C134-C142 = 9 new claims. Ledger goes 133 -> 142.

- BUILD-PASS: 1 (C134, inquiry clean re-freeze)
- ADVERSARY-QUALIFIED: 2 (C135 TNN-1 red team, C137 COMP-1 red team)
- ADVERSARY-CLEARED (proposed): 1 (C136 MUL red team)
- EXPLORATORY: 3 (C138 Python audit 2, C140 compression update,
  C141 freeze rerun plan)
- REMEDIATION-COMPLETE: 1 (C139 DEVINT report correction)
- BACKUP-VERIFIED: 1 (C142 bundle v14)

Zero new SURVIVES. L3 achieved anywhere: still zero.
BUILD-PASS total: 15 (was 14, added C134).
PROCESS-FAIL total: 5 (unchanged; C129 stands as the record of the
failed wave, C134 is the clean replacement).

Note on C129/C134: the inquiry wave's PROCESS-FAIL (C129) is not
erased. The ledger records both the failed wave and its clean
replacement, so the process record is complete.

Note on C136: the ADVERSARY-CLEARED status is proposed (no ledger
precedent for a red team with zero successful attacks). The
conservative fallback is ADVERSARY-QUALIFIED with the note "no
qualifications." The append worker or Micah should confirm the
status before appending.

No em dashes were used in this document (verified with the shell-only
byte check before commit).
