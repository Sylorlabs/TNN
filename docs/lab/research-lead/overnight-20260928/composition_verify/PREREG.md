# PREREG: composition internal verification (composition_verify lane)

Worker: Composition Internal Verification Worker.
Frozen: 2026-10-02 (this commit contains ONLY this file).
Status: FROZEN. Implementation must follow this spec exactly. Any design
change requires transparent amendment and re-freeze, never silent edit.

## 0. Question

Owner priority 2026-10-02 (#5): reduce composition's dependence on harness
expected answers. Current composition work verifies Z against harness
EXPECTED values. Required instead: learner commitment -> later world
consequence -> learner-owned evaluation. The learner should prefer a
composition because its contracts predict success, not because the harness
says EXPECTED=37.

This experiment implements the verification loop as a standalone pure-Zag
mechanism: commit to a composition with a predicted outcome, observe a
world consequence in a downstream task, update composition confidence from
the consequence alone, and later prefer the composition with higher earned
confidence. An ablation arm with no consequence history must not show the
preference, proving the preference is learned.

## 1. Design (frozen)

Standalone mechanism, NOT built on the TNN substrate. Rationale, recorded
before results: the claim under test is the verification loop itself, and
a minimal white-box implementation makes the learner/world information
boundary structurally auditable (separate state slices, tiny functions).
Integration with the TNN substrate is future work, not claimed here.

### 1.1 Components (fixed behavior, learner's world model)

- X(v) = v + 10. True behavior: preserves parity.
- Y(v) = v * 2.  True behavior: output always even.
- D(v) = v + 1.  True behavior: flips parity.

Component ids: X=0, Y=1, D=2. Compositions: XD id 0, XY id 1.

### 1.2 Contract induction (learner operation, general rule)

The learner induces a parity contract per component from exactly 2 fixed
probe executions. Contract codes: 0=ALWAYS_EVEN, 1=ALWAYS_ODD,
2=PRESERVE, 3=FLIP, -1=UNKNOWN.

Induction rule (identical for every component, frozen): let (p1,q1) and
(p2,q2) be (input parity, output parity) of the two probes. If q1==q2,
contract = ALWAYS_q1. Else if q1==p1 and q2==p2, contract = PRESERVE.
Else if q1!=p1 and q2!=p2, contract = FLIP. Else UNKNOWN.

Frozen probes (documented before results; this is the experimental setup,
not a result):
- X probes: 100 -> 110 (E->E), 101 -> 111 (O->O). Induces PRESERVE.
  Correct.
- Y probes: 100 -> 200 (E->E), 101 -> 202 (O->E). Induces ALWAYS_EVEN.
  Correct.
- D probes: 101 -> 102 (O->E), 103 -> 104 (O->E). Induces ALWAYS_EVEN.
  OVERGENERALIZED: D's true behavior is FLIP, but the learner's
  experience of D covers odd inputs only, on which FLIP looks like
  ALWAYS_EVEN. This honest overgeneralization is the setup the
  verification loop must catch at the composition level.

Composed contract: chain the two component contracts. apply(c, p):
ALWAYS_EVEN->0, ALWAYS_ODD->1, PRESERVE->p, FLIP->1-p, UNKNOWN->-1.
compose_contract(first, second, p) = apply(c_second, apply(c_first, p)).
If the result is -1 the learner does not commit (no prediction possible;
does not occur in this battery).

For input parity E: (X,Y) predicts apply(CY, apply(CX, E)) = EVEN.
(X,D) predicts apply(CD, apply(CX, E)) = EVEN. The learner genuinely
predicts downstream success for BOTH compositions; the contracts give it
no reason to prefer either. Any later preference must come from
consequences.

### 1.3 World (environment; fixed law, no per-query expected values)

The world holds a downstream machine M with one fixed law: M accepts a
value iff the value is even. world_execute runs a composition on an input
(actual value computed). world_downstream latches GATE=1 (accept) or
GATE=0 (reject) in world state. The gate is the ONLY consequence signal
the learner may read. The harness supplies no expected answer for any
query; the string "expected" does not occur in the source.

### 1.4 Learner state and world state (separate slices)

- L (learner state, i32 cells): [0]=conf_XD, [1]=conf_XY,
  [2]=commit_comp, [3]=commit_pred, [4]=commit_input,
  [5]=commit_status (0=none, 1=PENDING, 2=RESOLVED),
  [6]=contract_X, [7]=contract_Y, [8]=contract_D.
- E (world state, i32 cells): [0]=gate, [1]=accepts, [2]=rejects.

Information boundary (frozen, auditable): learner_commit takes (L, comp,
input). learner_update takes (L, E, comp) and reads ONLY world_gate(E);
it never receives an actual output value. learner_select takes (L) and
reads ONLY conf_XD, conf_XY. The driver holds actual values in locals
for white-box instrumentation logging only; no learner function is ever
passed an actual value.

### 1.5 Phases (frozen order and inputs)

- IND: run the frozen probes, induce and store the three contracts,
  log probes and induced contracts.
- Z1: learner_commit(L, XY, input=100): predicted=EVEN, status=PENDING,
  logged before execution. Driver executes XY on 100 (instrumentation
  logs actual=220; not a learner input). world_downstream(220): 220 is
  even, ACCEPT, gate=1. learner_update(L, E, XY): gate=1, conf_XY 0->1.
- Z2: learner_commit(L, XD, input=100): predicted=EVEN, status=PENDING.
  Driver executes XD on 100 (instrumentation logs actual=111).
  world_downstream(111): 111 is odd, REJECT, gate=0. learner_update(L,
  E, XD): gate=0, conf_XD 0->-1.
- Z3 (new problem): input=200, same downstream law. learner_select(L):
  argmax conf; tie broken by lowest composition id (XD=0). Logs both
  confidences, the choice, and the rule. Main arm: conf_XY=1 >
  conf_XD=-1, choice=XY. Driver executes the choice (instrumentation
  logs actual=420, ACCEPT) and learner_update raises conf_XY 1->2.
- ABL (ablation arm): fresh zeroed learner state; NO induction phase,
  NO Z1/Z2 consequence phases. learner_select(L) on the same new
  problem (input=200): conf_XD=0, conf_XY=0, tie -> lowest id -> XD.
  Logs confidences, choice=XD, rule=tie->lowest-id. No execution, no
  update in this arm.

Selection rule detail (frozen): the SAME single learner_select function
is called by both arms; the only input that differs between arms is the
ledger content. The neutral tie-break (lowest id) is documented here
before results; the main arm's choice (XY, id 1) goes AGAINST the
tie-break default, showing learned confidence overriding the default.

## 2. Frozen kill bars

- K-IV-1 (commit before any answer): in the run transcript, each COMMIT
  line has a smaller line number than its phase's EXEC and CONSEQUENCE
  lines; the commitment slot shows status=PENDING at commit time; code
  order is learner_commit before world_execute in Z1 and Z2; and
  `grep -ci expected` over the lane's .zag sources returns 0 (no
  expected-answer variable exists anywhere in the program).
- K-IV-2 (world consequence): the gate cell E[0] is written ONLY by
  world_downstream (verified by grep: exactly one writer); the
  transcript CONSEQUENCE lines read gate=1 after Z1 (actual 220, even)
  and gate=0 after Z2 (actual 111, odd), consistent with the fixed world
  law accept-iff-even.
- K-IV-3 (update from consequence): the transcript UPDATE lines read
  conf_XY 0->1 and conf_XD 0->-1; learner_update's only world read is
  world_gate(E) (the function body is quoted in REPORT.md; it takes no
  actual value and references no expected value).
- K-IV-4 (prefer by earned confidence): the Z3 SELECT line reads
  conf_XY=1, conf_XD=-1, choice=XY, rule=argmax-conf.
- K-IV-5 (ablation control): the ABL SELECT line reads conf_XD=0,
  conf_XY=0, choice=XD (not XY); exactly one learner_select definition
  exists in the source (verified by grep), called by both arms.
- K-IV-6 (determinism): the binary is run 3 times; stdout is
  byte-identical across the 3 runs (sha256 equal). Any mismatch voids
  the run.

Verdict COMPOSITION-VERIFY-COMPLETE iff K-IV-1 through K-IV-6 all hold.
Otherwise BUILD-FAIL, naming the failed bar. No SURVIVES claim is made;
this is a mechanism demonstration, not a generality proof.

## 3. Predictions (not kill bars; calibration only)

Main arm Z3 choice = XY. Ablation choice = XD. All transcripts
byte-identical across runs. Induced contracts: X=PRESERVE, Y=ALWAYS_EVEN,
D=ALWAYS_EVEN (overgeneralized). Gate sequence: 1, 0, 1.

## 4. Implementation constraints (frozen)

- Pure Zag only. Safebin PATH (`export PATH="$HOME/safebin"`). No
  Python, no other interpreters. Forbidden executable invocation =
  automatic PROCESS-FAIL with immediate disclosure.
- Zero modes, zero bridges, zero handlers, zero new opcodes. The world
  is a set of functions, not a mode. The ablation arm is a driver-level
  entry point calling the same selection function, not a mode.
- Toolchain lessons: u8-backed cells with get32/set32 (no `as *i32` +
  slice construction in functions); single preallocated output buffer
  with cursor-returning emit helpers and one `_zag_raw_syscall` write
  (no `_zag_print` for dynamic content); verify stdout bytes.
- Lane writes only under
  docs/lab/research-lead/overnight-20260928/composition_verify/.
- Commits: this prereg ALONE first; implementation second (explicit
  pathspec, never `git add -A`, never push). Local only.
- Bug fixes allowed only if they do not change this design or these
  bars; any design change = transparent amendment + re-freeze.
- Loop docs: hyphens only (no em/en dashes); check_no_dash.sh before
  each commit.
- Frozen read-only: no other repo files are touched. Paper untouched.

## 5. Deliverables

NAMECHECK.md (Step 0 done), this PREREG.md (frozen alone),
implementation (iv_mech.zag, iv_main.zag, build.sh), binary (iv_bin),
run outputs (run1.txt, run2.txt, run3.txt, sha256sums.txt), REPORT.md
(kill-bar verdicts with evidence, architecture accounting, red-team
self-review, boundaries and non-claims).
