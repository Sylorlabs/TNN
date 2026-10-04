# RED-TEAM REVIEW: wave-20261001-1421pdt

Reviewer: independent red-team subagent. Safebin toolchain guard PASS
(python3 absent; pure shell text analysis; see NAMECHECK.md Step 0).
No commits, pushes, checkouts, or branch changes; all files uncommitted.
No em-dash or en-dash bytes in lane files (byte-checked).

## Target 1: DDES V2 BUILD-PASS, probe-menu equivalence attack

Claim under attack: RESULT_DDES_FOLLOWUP_V2.md verdict BUILD-PASS
(all nine frozen kill bars pass; bounded L2 ceiling stated; no L3
claimed).

### Independent re-verification (my own scans, not the builder's)

- Phase-2 trace (after SCAFFOLD-DISCONNECT in run1.txt): contains only
  WORLD G, RECORD-LOAD, REPLAN [S,W,OY], EXEC, PRED-RECORD, SURVIVE/ELIM,
  CONVERGE-OK, SCAFFOLD-CALLS 0. Zero TARGET, FLAG, derivation PLAN, or
  derivation PRED markers (mechanical grep; the only PLAN/PRED
  substrings are the deliberately distinct REPLAN and PRED-RECORD).
- apply_persisted call-site audit: zero calls to compute_arrivals,
  compute_frontier, synthesize_plan, predict, ddes_world. The single
  raw substring hit is the code comment "Eliminated using persisted
  predictions only" (line 476), not a call. Confirmed false positive.
- load_world_G appears only at its definition (line 398) and in main's
  phase-2 loop (line 589). ddes_world is invoked only for worlds F and
  A. Derivation never sees G.
- Phase-A trace matches every K-G2 frozen line exactly (World F both
  configs: TARGET V*=2 t*=0 schema=1, FLAG TSTAR-ZERO-BOUNDARY floor=1,
  PLAN [S,W,OY], PRED h0=1 h1=0, correct SURVIVE/ELIM, CONVERGE-OK;
  World A both configs: TARGET V*=2 t*=1 schema=1, no FLAG,
  PRED h0=0 h1=1; SCHEMA-RECORD line exact).
- Determinism: run1.txt, run2.txt, run3.txt all sha256
  b8bc5fa9cd2feec8c239baad42eba88438c9dea4341b226189bcc81cca6fcde3
  (matches the claimed hash). RECORD-LOAD fields byte-identical to the
  SCHEMA-RECORD field string (3 occurrences total: 1 write, 2 loads).

### Probe-menu enumeration (the attack)

The sealed phase-2 outputs on World G are a deterministic function of
the 6-field record R = (schema, V*, t*, tstar_zero, pred_h0, pred_h1)
plus the truth config, rendered through the fixed reconstruction
template in apply_persisted. Domain sizes: schema in {0,1}, V* in
{0,1,2} (obs = 4 - V*), t* clamped by eff_waits to at least 1 wait
with the plan buffer capping distinguishable lengths, tstar_zero /
pred_h0 / pred_h1 each binary. The full menu of distinguishable
phase-2 behaviors is at most a few thousand record tuples, each
mapping to one fixed trace template.

Stronger: the record is not extracted from the derivation at runtime.
In main(), the six fields are written as source constants
(learner_state offsets 0/4/8/12/16/20 set to 1/2/0/1/1/0), gated only
on the single bit f_ok (both World F configs converged). The phase-2
runtime therefore has exactly two variants: skip (f_ok=0) or replay
the constant tuple C=(1,2,0,1,1,0). A menu of size 2 reproduces the
sealed phase-2 outputs exactly.

Further: the sealed world G is discriminating-signature-identical to
World F by prereg design (design decision 3), so phase 2 performs
zero new discrimination; the record's validity on G is inherited
from F, not tested. And the derivation-to-record binding is enforced
only by offline reviewer K-G2 trace checks, not by the binary: the
f_ok gate requires CONVERGE-OK (exactly one survivor), which does not
require the correct survivor, so a derivation that converged with
different values would still trigger the constant write; only the
reviewer's exact-line checks bind them.

The phase-A derivation itself is genuine computation, not menu
selection: Bellman-Ford arrivals, frontier search, and plan synthesis
contain no per-world, per-delay, or per-variable branches and compute
(V*, t*, schema, predictions) from the rule tables. But phase A runs
on prereg-frozen, researcher-designed worlds, not sealed ones.

### Verdict: SURVIVES-ATTACK (with landed findings)

The probe-menu attack lands on the sealed-usability reading: the
phase-2 sealed outputs are fully menu-reproducible (menu of size 2 at
runtime), the sealed world exercises no new discrimination, and the
persisted artifact is a researcher-constant tuple, not a
runtime-extracted product of the derivation. However, this does not
kill the BUILD-PASS verdict as frozen: all nine kill bars are
mechanical and independently re-verified above; the builders disclosed
every one of these limitations themselves (result design decisions
1-3; prereg honest boundaries scoring C0-A through C0-D as FAIL;
explicit bounded-L2 ceiling; no L3 claim). The attack therefore
constrains what BUILD-PASS may be cited for rather than falsifying it.
Binding caveats for any future citation of this BUILD-PASS: (a) the
record is a source constant gated on a binary convergence signal,
with derivation-to-record binding enforced only by offline reviewer
checks; (b) the sealed world is signature-identical to the derivation
world, so no generalization is tested; (c) the phase-2 outputs cannot
distinguish persisted genuine generation from frozen-constant replay.

## Target 2: F1 three-mechanism source audit (tnn2.zag)

Audited: docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag
(1591 lines; sha256 a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd),
the frozen TNN-2 cognition source containing M1 (t2_trial /
constructors / promote_graph), M2 (miss_inquire / ev_act guide path),
M3 (revise_on_contradict / t2_revise_graph). Diffed against the frozen
base tnn1_act.zag: 565 added lines, all three mechanisms plus tests.

- Hardcoded semantic cases (SUB, DIV, PARITY, two-threshold COND or
  equivalents): zero hits.
- Protected-core regularity detectors (FIND_POLYNOMIAL_ORDER,
  DETECT_NEGATION, BUILD_CAUSAL_RULE, LEARN_PROCEDURE, FIND_THRESHOLD,
  MAKE_CONDITIONAL or equivalents): zero hits.
- New modes/bridges/routers/handlers: zero code hits. The only matches
  are comments documenting absence (line 17: "ISA frozen: no new
  opcodes, modes, bridges, handlers, semantic cases") and removal
  (lines 6, 323-324 documenting exec_plan and fixed-template removal).
- ISA is the frozen 4-op (OP_MOVE=101, OP_BEQ=102, OP_INC=103,
  OP_DEC=104); no MUL, no DIV, no new opcode. Node types are originals
  only (1,2,3,4,20,21,30). exec_plan has zero code references; the
  fixed plan templates and T_PLAN/T_STEP constants are gone.
- False positives adjudicated: (a) miss_inquire's
  write_node(W,g,30,-999,0,0): the 30 is the transcript-protocol
  inquiry act id carried by the learner-constructed guide, not a
  domain semantic case; (b) t2_asm_sum's total<=0||total>900: a
  generic execute-budget guard; (c) the three proposal families
  (chain/count/sum/single-hop) in t2_trial: researcher-authored
  proposal machinery, but trial-verified with genuine rejections
  (F-T2-3), which the protected-core ISA ruling explicitly permits;
  the battery prereg already concedes C0-A NOT MET for proposal
  generators. None are forbidden content.

### Verdict: SURVIVES-ATTACK (audit clean)

No forbidden semantic case, regularity detector, mode, bridge, router,
or handler in the committed mechanism sources. The ISA freeze holds.

## Target 3: architecture accounting spot-check (two HEAD commits)

### 02a338dbf substrate expansion (5 behaviors, one consequence substrate)

- Commit shape: 12 files, all additions (A), 4145 insertions, zero
  modifications to existing files. Frozen base untouched.
- Claimed accounting (DESIGN.md:73, REPORT.md, se_behaviors.zag:5):
  0 modes, 0 bridges, 0 handlers, 0 semantic cases.
- Verified: no architectural mode/bridge/router/handler in the new
  code. ev_query and evict_node are experiment-variant replacements
  (declared: "minus 3 replaced fns"), not additions to the frozen core.
- Declared observations (not hidden, all in code comments or REPORT
  honest limits): (a) config node tag 904 with a researcher-set
  bitmask gating the five behavior reads (se_driver.zag sets
  31/30/29/27/23/15 per battery); this is an ablation control,
  disclosed as "researcher-set per battery, not learned"; it is not a
  cognitive mode in the CAUSAL_MODE sense, but it is a researcher-set
  behavior switch and learner-owned arbitration is explicitly future
  work; (b) the packed life-field "mode" subfield (F1-F7) is
  failure-cause telemetry, not a mode switch; (c) thresholds
  sc_n()=3 (withhold) and se_abandon_n()=6 (abandon) are
  researcher-chosen constants on a consequence counter: generic
  resource-management policy thresholds, not domain semantic cases,
  and the "one field, two thresholds" sharing is the lane's core
  claim; (d) new learner-state data types tag 61 (substrate records,
  reused from fa8405a90) and tag 904 (config node): data record types,
  not modes/handlers. Learner-state structures are documented
  (tag-61 record layout in the se_behaviors.zag header; REPORT
  shared-fields evidence).
- No undeclared mode/bridge/handler found.

### 1963e994d mini-lifetime integration (3-arm persistent comparison)

- Commit shape: 17 files, all additions (A), 5511 insertions, zero
  modifications to existing files.
- REPORT.md carries an explicit architecture accounting section.
  Verified line counts match the added files (substrate 79, rebind 54,
  protection 68, provenance tags ~7, merged ev_query ~52; total ~250).
  No modes/bridges/routers/handlers in the added code;
  phase_a_enabled() is dead code (defined, never called), not a mode.
  No hardcoded semantic cases. Learner-state structures documented
  (MAP graphs, rebind bindings, tag-61 substrate records, PRO edges,
  field-16 source tags on FACTs).
- Minor imprecision (not a violation): the "New node types: 0"
  phrasing is lane-relative. Tag 61 is new relative to the frozen
  TNN-2 base type registry (introduced by the earlier substrate_build
  commit fa8405a90 and reused here); it is a learner-state data record
  type allocated from the existing node storage pool, not a
  mode/bridge/handler, and the parenthetical "use existing storage"
  is accurate about the pool.

### Verdict: SURVIVES-ATTACK (accounting verified as stated)

Both commits' claimed accounting matches the code. No undeclared
mode, bridge, or handler. Observations above are recorded for the
architecture ledger; none contradict the claims.

## Target 4: sealed-battery prereg triviality review

PENDING. At end of review, docs/lab/rsi/runs/wave-20261001-1421pdt/
sealed_adv/ contains only NAMECHECK.md (Steps 0-1 complete; Step 2
mechanism source freeze not yet filled). No prereg has been produced
by the sealed-battery worker, so no adversarial-world triviality
judgment is possible. For the parent's reference: the 0821pdt
adv-battery lane's PREREG_TNN2_ADVERSARIAL_BATTERY.md (a different
lane's prereg, not the sealed_adv worker's output) designs AB1-AB3
with explicit per-world "materially different, not a FW variant"
justifications; triviality review of the sealed_adv worker's own
prereg is deferred until it lands.

## Overall: REDTEAM-COMPLETE

Per-target verdicts: (1) SURVIVES-ATTACK with three binding caveats;
(2) SURVIVES-ATTACK, audit clean; (3) SURVIVES-ATTACK, accounting
verified; (4) PENDING, no prereg produced. No Python used at any
stage; safebin guard recorded in NAMECHECK.md Step 0.

Files left behind (uncommitted, as instructed):
- docs/lab/rsi/runs/wave-20261001-1421pdt/redteam/NAMECHECK.md
- docs/lab/rsi/runs/wave-20261001-1421pdt/redteam/REDTEAM_1421PDT.md
