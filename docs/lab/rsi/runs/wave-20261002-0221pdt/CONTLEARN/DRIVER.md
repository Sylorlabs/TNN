# DRIVER: CONTLEARN3 mechanism-proposal-first build record

Wave: wave-20261002-0221pdt. Lane: CONTLEARN. Date: 2026-10-02.
Worker: phase-2 implementation. Pure Zag plus shell orchestration.
No Python, C, JavaScript, or Rust at any stage.

## What was built

Two binaries, one fixture driver source, from two logged znc invocations:

- `pf_core_control.zag`: byte copy of the recorded nomain derivation of
  the frozen TNN-2 core (copied read-only from the 2021pdt CONTLEARN lane),
  SHA-256
  26b455e78a9b0ba0f6d6967c12ff8c05f9ebd9152dddca9efeb2a3b44064ec9d.
  The frozen file itself was never written; its bytes re-verified
  (a29972ca...) before the builds and after the runs.
- `pf_core_treat.zag`: mechanical derivation of the control core with the
  proposal-first gate instrument (section below). SHA-256
  627af6eb0e88141fdeb00baba0aab178a29df128aa0250398355db42d8557f63.
  Diff against the control core: exactly 2 lines removed, 60 lines added
  (48 non-comment/non-blank), all in the new pf_* functions and the
  ev_query gate edit. No other line of the frozen logic is touched.
- `pf_driver.zag`: the only hand-written source file. Implements the
  frozen 76-event script with content-identified white-box oracles for
  STORE_OK, STORE_PROP_CITE, CONFLICT_OK, CORRECT_OK, RETENTION_OK, and
  REUSE_OK, plus the per-phase mechanism census (MAPC/PROPC/DEPC/UNC/
  GUIDEC/N1/Eall). SHA-256
  b9ab9953672880546dd4067c6c6ff82e76d863ddde0e9531c44ef287323a25a9.
- `pf_combined_treat.zag` (instrument core + driver):
  6835b23da95abd2d4ff2ac3047ea1bd797daee3c36ce65d454139d9ee4cfad86.
- `pf_combined_control.zag` (control core + driver):
  d94539b6b2f9aa797fd58aafc86827fb88dbae2da747c180413ad50563035a88.

Build commands (the two logged invocations, fresh log):
`sh znc_wrap_pf.sh pf_combined_treat.zag -o pf_driver_treat`
`sh znc_wrap_pf.sh pf_combined_control.zag -o pf_driver_control`
Binaries: pf_driver_treat
(sha recorded in RUN_LOG.md); pf_driver_control (sha recorded in
RUN_LOG.md). Both builds emitted analyzer warnings only, the same warning
class as the prior waves; both binaries run cleanly.

## The proposal-gate instrument (exact)

Inserted before `fn ev_query` in the TREAT core:

- `pf_find(W,s,r)`: returns the live proposal node for (s,r) or -1.
  Proposal signature: tag==1, alive, field20==30, field24==-998,
  field4==s, field28==r. (Guides use field24==-999.) Existing tag,
  existing fields, existing formats only.
- `pf_propose(W,s,r)`: allocates the proposal node (tag 1, ns field4=s,
  write_node(30,-998,r,1): field20=30, field24=-998, field28=r,
  field32=mech=1 meaning TRY_CHAIN), creates POLICY_ROOT if absent (the
  miss_inquire pattern), links the proposal to POLICY_ROOT with a type-10
  edge, emits the `PROPOSAL s=.. r=.. mech=1 node=..` trace line, logs
  kind-5. The mech=1 code is the fixed researcher template disclosed in
  PREREG_CONTLEARN3 section 1.
- `pf_mp_run(W,s,r,expected,flags)`: the only trial entry in TREAT. Calls
  pf_find first; if no live proposal exists it emits `MACHINERY_SKIPPED`
  and returns -2 (engagement refused). Otherwise it runs the verbatim
  mp_run logic; on engagement it links a type-1 DEP edge from each
  promoted MAP(s,r) node to the proposal node (provenance), emits the
  `MACHINERY s=.. r=.. mech=1 prop=.. ans=..` trace line, logs kind-6.
- `ev_query` gate edit: on the miss path, the verbatim trial block is
  replaced by: pf_find; if absent, pf_propose; then pf_mp_run; then the
  verbatim bootstrap fallback, miss log, and miss_inquire. The five
  machinery functions keep their exact logic; only their entry is gated.

## K2b: driver source audit

- Cognition functions defined: 0. All 22 pf_-prefixed functions are
  fixture/measurement: event emission through the two choke points
  (pf_event kinds {1,2,3}, pf_mquery), read-only oracles through the
  core's own accessors (ng/eg/activate/is_superseded), and prints.
- Structural writes in the driver: 0 (ns(/link_edge(/alloc_node( count 0).
- New node tags: 0. New edge types: 0. New opcodes: 0. New modes: 0.
  New bridges/routers/handlers: 0. Semantic cases (switch/match): 0.
- Kind 3 (ev_observe) is the frozen counterexample protocol, disclosed in
  the prereg; it carries only integer (s,r,o) operands, no task identity.

## K2c: architecture accounting

- Cognition-source delta on the frozen path: 0 added, 0 deleted, net 0.
- Variant instrument: 48 non-comment added lines, 2 removed lines (the
  replaced trial-call block); the variant is a lane-dir measurement
  instrument, not a change to the frozen architecture.
- New modes: 0. New bridges: 0. New handlers: 0. New node tags: 0. New
  edge types: 0. New ISA opcodes: 0. New subsystem state formats: 0.
- ONE-SYSTEM RULE check (explicit): one persistent arena with the frozen
  110656-byte layout; the proposal is a tag-1 node in POLICY_ROOT space,
  the same existing format as learner guides; the instrument reads and
  writes only the shared arena through the existing accessors. No
  independent subsystem state format exists anywhere in this lane.

## K2d: pure Zag

Zero Python/C/JS/Rust. `which python3` prints nothing under the safebin
PATH (NAMECHECK.md Step 0, verified before any research operation).
