# PREREG_A: refusal-branch exercise, learner-state-caused vs hardcoded refusal (frozen)

Status: PREREG-FROZEN (design only; no implementation in this commit).
Wave: wave-20261002-1121pdt. Lane: CONTLEARN (queue item 9, exercise a).
Date: 2026-10-02. Implementation authorized only after this prereg is
committed alone.

Note: this document uses hyphens only; no em or en dashes appear.

## 0. Commit order (K0)

This prereg is committed alone: this file only. No implementation file
for exercise (a) may exist at or before the prereg commit. The
implementation commit must be a strict descendant of the prereg commit,
verified by `git merge-base --is-ancestor <prereg-sha> <impl-sha>`
before any verdict is reported. UNVERIFIABLE ORDERING voids the prereg.
No bar may be altered after results are seen; amendment requires a
transparent re-freeze.

## 1. Question and lineage

Binding caveat 4 (CONTLEARN3/CLH2): the gate's refusal branch is
structurally enforced but empirically unexercised (0 MACHINERY_SKIPPED,
three consecutive lanes). This exercise attacks it: the continuing
learner encounters contradictory material, and the measurement asks
whether refusal is LEARNER-OWNED (a function of the learner's own
uncertainty/epistemic state, recorded through its public event API) or
a HARDCODED BRANCH (a function of the input alone, invariant to learner
state). The kill bar is on the distinction.

Honest status, frozen here (binding on the verdict and the red team):

- The refusal POLICY is instrument code, not learner-authored. Caveat 3
  (no learner agency in the causal sense) still binds. The claim under
  test is STATE-CAUSATION of the decision, not authorship of the policy:
  with identical code and identical probe input, the decision flips when
  and only when the learner's epistemic state differs.
- The refusal instrument is new (ledger-based, section 2). It is a lane
  measurement instrument, not a proposed architecture and not a change
  to the frozen core.
- The pf gate's MACHINERY_SKIPPED branch remains unexercised after this
  lane; this exercise does not claim to exercise it and says so.
- No L3, no generality. The battery is disclosed and prereg-frozen, not
  adversary-designed.

## 2. The instruments

Frozen base: byte copy of
docs/lab/rsi/runs/wave-20261002-0521pdt/CONTLEARN/clh2_core_control.zag,
SHA-256 26b455e78a9b0ba0f6d6967c12ff8c05f9ebd9152dddca9efeb2a3b44064ec9d
(the recorded nomain derivation of the frozen TNN-2 core), verified by
hash before the builds. The frozen path is never written.

Two instrument cores are derived from the base (lane measurement
instruments, not proposed architectures):

### rj_core_own.zag (the candidate instrument: learner-state-caused refusal)

New instrument functions (rj_ prefixed; zero collisions with frozen
names; no new node tags, edge types, opcodes, modes, bridges, handlers,
or semantic cases):

- rj_ledger_get(W,r): scan alive tag-30 nodes with field20==0,
  field32==1, field24==r; return field28 (the contradiction count), or 0
  if no ledger node exists.
- rj_ledger_bump(W,r): find-or-create the ledger node for r (tag 30,
  field4=-4, field20=0, field24=r, field32==1), increment field28,
  log_ev(W,7,r,field28,0,0,0,0) for provenance (kind 7 = LEDGER,
  disclosed here).
- rj_refuse_own(W,s,r): return 1 iff rj_ledger_get(W,r) >= K, with K=2
  frozen here.

ev_query is modified in exactly one place: after the activate-miss
block, before the trial path:

  if(rj_refuse_own(W,s,r)==1){
    emit("REFUSED s="); e64(s); emit(" r="); e64(r); emit("\n");
    log_ev(W,7,s,r,0,0,0,0); return -2;
  }
  emit("ENGAGE s="); e64(s); emit(" r="); e64(r); emit("\n");

then the frozen trial/bootstrap/miss path unchanged. The miss path
prints "MISS s=.. r=.." before miss_inquire so refusal, engagement, and
ordinary miss are distinguishable in the transcript.

ev_observe is modified in exactly one place: on the contradiction path
(rv==0, where the frozen code writes the type-3 self edge), call
rj_ledger_bump(W,r) after the contradict edge. Corroborations (rv==1)
do not touch the ledger.

The ledger node is learner state: it lives in the arena, is written
only through the public ev_observe contradiction path by the
instrument, and is read as control by the instrument. The DRIVER never
writes ledger nodes (audited: 0 alloc_node/ns(/link_edge( tokens in
drivers; driver source audit in section 5).

### rj_core_hard.zag (the red-team control: hardcoded refusal)

- rj_refuse_hard(W,s,r): return 1 iff r==850 (researcher hard list,
  disclosed here; a pure function of the input, invariant to learner
  state). No ledger, no ev_observe hook.
- ev_query modified identically to the own variant except the check
  calls rj_refuse_hard. ENGAGE/MISS prints identical.

This core is the costume demonstration: refusal wearing learner's
clothes but decided by a fixed branch. It is not a candidate.

### Structural-difference statement

No prior lane exercised a refusal path empirically. The new content is
the ledger instrument plus the state-swap discriminator (section 4);
the frozen core is otherwise byte-identical.

## 3. Experience sequences (exact, frozen, fresh)

All ids (94001..94902, 94201..94206, 94301..94506) are unused by any
prior battery in the wave-20261001 and wave-20261002 .zag sources
(verified by grep before writing this prereg). Relations 850, 851, 852,
853 coincide with CLH2's relation numbers; this is harmless because
every run starts from a zeroed arena (tnn2_init) in its own process, so
no cross-run contamination is possible, and within-battery usage is
exactly as specified below. Event kinds: 1=TEACH (ev_teach), 2=MQUERY (ev_query,
expected=-2, flags=1: disclosed supervisor disconnect, not a task
label), 3=OBSERVE (ev_observe: the frozen counterexample protocol,
integer (s,r,o) operands only, not a task label). PHASE markers are
driver-side prints and never reach cognition. Every tuple flows through
the choke points rj_event / rj_mquery; the drivers define 0 cognition
functions and perform 0 structural writes.

### 3a. History X (contradicted), rj_driver_x.zag, run on rj_core_own and rj_core_hard

- CONTRADICT (9 events):
  - for i in 0..5: TEACH(94001+i, 850, 94101+i) (6 facts of kind 850).
  - OBSERVE(94001, 850, 94901): contradicts fact (94001,850,94101);
    rv=0; ledger(850) -> 1.
  - OBSERVE(94001, 851, 94901): relation 851 has no fact for 94001, so
    this teaches (94001,851,94901) with rv=1; ledger untouched. This
    event proves the ledger hook fires only on genuine contradiction,
    not on every observe.
  - OBSERVE(94002, 850, 94902): contradicts fact (94002,850,94102);
    rv=0; ledger(850) -> 2.
- REFUSAL probes (6 events):
  - for i in 0..5: MQUERY(94201+i, 850) (fresh subjects, kind 850).
- ENGAGEMENT probes, clean kind (18 events):
  - for i in 0..5: TEACH(94301+i, 851, 94401+i).
  - for i in 0..5: TEACH(94401+i, 852, 94501+i).
  - for i in 0..5: MQUERY(94301+i, 853) (novel relation; chain
    [94301+i, 94401+i, 94501+i] assembles; expected answer 94501+i).

Total: 33 events per run. Frozen ledger prediction: ledger(850)==2 at
end of CONTRADICT; ledger(851)==0 (the rv=1 observe must not bump it).

Hmm, the event above "OBSERVE(94001, 851, 94901)" teaches an unrelated
fact; it is kept because it tests hook specificity, and its presence
does not affect any oracle (no query ever addresses (94001,851)).

### 3b. History Y (confirmed), rj_driver_y.zag, run on rj_core_own and rj_core_hard

Identical to history X except the two contradictions become
corroborations:

- CONFIRM (9 events):
  - for i in 0..5: TEACH(94001+i, 850, 94101+i).
  - OBSERVE(94001, 850, 94101): rv=1 (corroboration); ledger untouched.
  - OBSERVE(94001, 851, 94901): teaches (94001,851,94901), rv=1.
  - OBSERVE(94002, 850, 94102): rv=1 (corroboration); ledger untouched.
- REFUSAL probes (6 events): same 6 MQUERY(94201+i, 850).
- ENGAGEMENT probes (18 events): same as history X.

Frozen ledger prediction: ledger(850)==0 (no node) at end; all 6 kind-
850 probes ENGAGE (trial runs, finds no facts for the fresh subjects,
miss path, UNCERT reified).

### 3c. Why this discriminates learner-owned from hardcoded

The probe inputs (94201+i, 850) are byte-identical across the four
binaries. The own-core decision is a function of learner state
(ledger(850): 2 in X, 0 in Y). The hard-core decision is a function of
the input alone (r==850). The state-swap discriminator: own refuses in
X and engages in Y; hard refuses in both. If own refuses in Y too, the
refusal is not learner-state-caused and the claim is KILLED.

## 4. White-box measurement oracles

- REFUSED_OK: count of "^REFUSED s=" lines with r=850 in the
  transcript. Frozen: own_x 6/6, hard_x 6/6, own_y 0/6, hard_y 6/6.
- ENGAGE850_OK: count of "^ENGAGE s=.* r=850$" lines. Frozen: own_x
  0/6, hard_x 0/6, own_y 6/6, hard_y 0/6.
- ENGAGE_OK: the 6 clean-kind probes return 94501+i with serve_ok
  (activate returns the live content-expected fact; the promoted answer
  fact). Frozen: 6/6 on all four binaries.
- LEDGER_CK: rj_ledger_get(W,850) at end. Frozen: X histories 2, Y
  histories 0 (no node). Also LEDGER851_CK: rj_ledger_get(W,851)==0 on
  all four (hook specificity).
- No MAP may cite kind-850 probe subjects: scan finds no tag-20 node
  with field8 in 94201..94206 on own_x, hard_x, hard_y (refusal means no
  engagement, no promotion). On own_y, also no MAP(94201+i,850) may
  exist (the probes miss; misses do not promote). Bar: 0 on all four.
- Capacity guard: VOID the run if any census shows 900+ alive nodes or
  3500+ live edges. Budget: under 120 nodes; far below caps.

## 5. Frozen kill bars

A-R0 (refusal after contradiction, own_x): REFUSED_OK==6/6,
ENGAGE850_OK==0/6, ENGAGE_OK==6/6, LEDGER_CK==2, LEDGER851_CK==0,
no-850-MAP==0.

A-R1 (same code, confirmed history, own_y): REFUSED_OK==0/6,
ENGAGE850_OK==6/6, ENGAGE_OK==6/6, LEDGER_CK==0, no-850-MAP==0.

A-R2 (state-dependence, the crux): A-R0 shows 6/6 REFUSED while A-R1
shows 0/6 REFUSED on identical probe inputs with the same instrument
family; the decision flips with learner state alone.

A-R3 (hardcoded costume control): hard_x REFUSED_OK==6/6 AND hard_y
REFUSED_OK==6/6: the hardcoded decision is state-invariant, the exact
pattern a fixed branch produces. Contrast with A-R2.

A-R4 (determinism and process hygiene): 3/3 byte-identical stdout per
binary (SHA-256 equal across reps), printed FNV-1a arena checksums
equal, exit code 0, zero stderr bytes, no PID/timestamps/paths in
transcripts, exactly 12 learner processes total (4 binaries x 3 reps),
one process per full run, empty argv and empty env, znc wrapper log
shows exactly 4 pre-run builds and 0 new entries during the 12 runs,
expected audited event counts 33 per run with AUDIT_PASS.

Governance bars:

K0: prereg committed alone; implementation strictly descendant;
merge-base verified before verdict.

K1 (one learner, no reset, no recompile, no task labels): K1a: 12
processes, transcripts PID-free, harness log records spawns. K1b:
wrapper-logged builds only pre-run. K1c: driver self-audit; tuples
through choke points with kind in {1,2,3} and plain integer operands;
MQUERY carries expected=-2, flags=1 (disclosed); OBSERVE is the frozen
counterexample protocol; PHASE markers never reach cognition; 33
events per run; AUDIT_PASS.

K2 (frozen ISA boundary and architecture accounting): K2a: base core
hash equals 26b455e78a9b0ba0f6d6967c12ff8c05f9ebd9152dddca9efeb2a3b44064ec9d
before the builds; frozen path never written. K2b: driver source audit
on both drivers: 0 cognition functions, 0 structural writes (counts of
ns(/link_edge(/alloc_node( tokens are 0; the only core-accessor calls
are ng/eg/activate/is_superseded/rj_ledger_get), 0 new node tags, 0 new
edge types, 0 new opcodes, 0 modes, 0 bridges, 0 routers, 0
task-specific handlers, 0 semantic cases (no switch/match), and 0
pf_propose/pf_find/alloc_node tokens. K2c: architecture accounting:
the instrument cores are lane-dir measurement instruments, not changes
to the frozen architecture; cognition-source delta on the frozen path
0/0/0; the ledger uses the existing tag-30 UNCERT node format in the
existing arena (no independent state format); zero new modes, bridges,
handlers, node tags, edge types, ISA opcodes. K2d: pure Zag plus shell
only; `which python3` prints nothing under the safebin PATH (Step 0).

K3 (no regression): the recorded CONTLEARN3 pf battery behavior is
unchanged: re-run the committed 0521pdt clh2_treat binary is not
available in this sparse worktree; instead K3 is the frozen-core
self-test: the base core's own run_all() suite is compiled and run
once read-only (no source change), and must report the same pass count
as the frozen record (46/46 per the 0521pdt RUN_LOG; verified before
any lane run). Kill: any mismatch.

## 6. Frozen decision rule

- REFUSAL-STATE-CAUSED iff A-R0, A-R1, A-R2, A-R3, A-R4, K0, K1, K2, K3
  all pass, with the explicit claim bound of section 1 and section 7.
- REFUSAL-NOT-STATE-CAUSED iff A-R2 fails (the own instrument refuses
  in Y as well, or engages in X): the refusal does not track learner
  state; the learner-ownership claim is KILLED with root-cause
  analysis; no new handlers, modes, or opcodes follow.
- INSTRUMENT-FAIL iff A-R0 fails: the instrument does not implement the
  policy; KILLED as an instrument, not as a claim about the learner.
- DISCRIMINATOR-FAIL iff A-R3 fails in a way that confounds the
  contrast (e.g., hard flips with state, which is impossible by
  construction; if observed, the experiment is VOID as confounded).
- VOID iff K0, K1, K2, K3, A-R4 fail, or the capacity guard trips.

## 7. Exact claim bound (frozen)

If REFUSAL-STATE-CAUSED: on the fixed disclosed 33-event batteries,
the continuing learner, after two genuine contradictions on kind-850
material (recorded through the public ev_observe protocol into its own
ledger state), refuses 6/6 fresh kind-850 probes (no trial engagement,
no promotion, no MAP) while engaging 6/6 clean-kind probes correctly;
with the identical code and identical probe inputs but a confirmed
(no-contradiction) history, it engages 6/6 kind-850 probes; the
hardcoded control refuses 6/6 in both histories. The refusal decision
is therefore a function of the learner's epistemic state, not of a
fixed input branch. All 3/3 byte-identical, one process per run, no
reset, no task label, no recompilation.

Explicitly not shown: learner authorship of the refusal policy (the
K=2 threshold and the ledger format are researcher instrument choices,
disclosed); learner agency in the causal sense (caveat 3 stands);
exercise of the pf gate's MACHINERY_SKIPPED branch (still 0, still
open); any L3 or generality claim; the instrument cores are not
proposed architectures; the battery is disclosed and prereg-frozen, not
sealed adversarial.

## 8. What this prereg does NOT authorize

- No implementation in this commit.
- No new cognitive machinery of any kind beyond the disclosed lane
  measurement instrument: no new Zag subsystems, modes, bridges,
  routers, task-specific handlers, semantic cases, node tags, edge
  types, ISA opcodes, or subsystem state formats.
- No tuning of any kind to this battery; K2a forbids edits beyond the
  disclosed instrument derivation and the two fixture drivers.
- No sealed adversarial worlds; the scripts are disclosed and frozen.
- No weakening of any frozen bar after results; amendment requires a
  transparent re-freeze, never an edit.
