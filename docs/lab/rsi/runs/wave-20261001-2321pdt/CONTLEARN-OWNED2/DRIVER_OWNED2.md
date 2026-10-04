# DRIVER_OWNED2: CONTLEARN-OWNED2 discrimination build record

Wave: wave-20261001-2321pdt. Lane: CONTLEARN-OWNED2. Date: 2026-10-02.
Worker: phase-2 implementation (respawn of CONTLEARN-OWNED). Pure Zag plus
shell orchestration. No Python, C, JavaScript, or Rust at any stage.

## What was built

Two binaries, one fixture driver source, from two logged znc invocations:

- `ow_core_control.zag`: byte copy of the recorded nomain derivation of
  the frozen TNN-2 core (extracted read-only via git show from dfcd3caf),
  SHA-256
  26b455e78a9b0ba0f6d6967c12ff8c05f9ebd9152dddca9efeb2a3b44064ec9d.
  The frozen file itself was never written; it was only read (and its
  bytes re-verified against the frozen blob before the builds and after
  the runs).
- `ow_core_disabled.zag`: mechanical derivation of the control core with
  exactly the two machinery call blocks (six lines) removed from
  `ev_query`; the five machinery functions remain as unreachable dead
  code. SHA-256
  94b405fc8acce8c2de120d972797052a6468e415e874b549d03c3eecb2fe8407.
  CO-5a: diff against the control core shows exactly the six deletions.
  CO-5b: caller analysis proves no event-interface path reaches any of
  the five machinery functions.
- `ow_driver.zag`: the only hand-written source file. Implements the
  frozen 98-event script (ERRATUM-1 corrected count) with
  content-identified white-box oracles for STORE_OK, REUSE_OK, SANITY_E,
  and DELAYED_OK, plus the per-phase mechanism census (MAPC/DEPC/UNC/
  GUIDEC/N1/Eall). SHA-256
  e591028039f7c0d2ec0a2fdf2c47f9b6c38119697996ff0588d6233fadc7e465.
- `ow_combined_control.zag` (control core + driver):
  51dbb6e0e2f272fcefc7c1290c24a05392ba2cf834290bdbd22bee0c8192e540.
- `ow_combined_disabled.zag` (variant core + driver):
  6579d84613d11680c63150142a567dd118326c2600bdf47916f4b6c62783fd45.

Build commands (the two logged invocations, fresh log):
`sh znc_wrap_ow.sh ow_combined_disabled.zag -o ow_driver_treat`
`sh znc_wrap_ow.sh ow_combined_control.zag -o ow_driver_control`
Binaries: ow_driver_treat
d969faa29232ad3601d87ffeded3a01536c95414f803e3b91524dbef633f4039;
ow_driver_control
769379cc556fc0a4d4d15ac806b7646c1dc7d264a60a8223ec873e05fa0883c5.
(Both builds emitted analyzer warnings only, the same warning class as the
prior wave; both binaries run cleanly.)

## K2b: driver source audit

- Cognition functions defined: 0. All 17 ow_-prefixed functions are
  fixture/measurement: event emission through the two choke points
  (ow_event for TEACH kind 1; ow_mquery for masked QUERY with the frozen
  parameters expected=-2, flags=1), structural predicates replicating the
  prereg oracle definitions, mechanism census counters, FNV-1a checksum,
  transcript printing. No learning, retrieval, inference, retention,
  eviction, planning, derivation, revision, or execution logic.
- Structural writes: `ns(` count 0, `link_edge` count 0, `alloc_node`
  count 0. The driver never creates nodes or edges; it only reads arena
  state through the core's own accessors.
- New node tags: 0. New edge types: 0. New opcodes: 0. New modes: 0.
  New bridges: 0. New routers: 0. New task-specific handlers: 0.
  New semantic cases: 0.
- `switch`/`match` count in driver source: 0 (case-insensitive grep).
- The frozen source contains zero ow_ occurrences: no driver name
  collides with or redefines any frozen function.

## K2c: cognition-source delta accounting

- Lines added to cognition source: 0. Lines deleted: 0. Net: 0.
- New hardcoded semantic cases: 0. New modes: 0. New bridges: 0.
- New routers: 0. New task-specific handlers: 0.
- One-system rule: the single persistent workspace is the frozen arena in
  both binaries; all learner-state structures counted by the per-phase
  census (fact nodes, MAP nodes, UNCERTAINTY nodes, guide nodes, DEP and
  other frozen edge types) are in frozen formats. The variant core is a
  disabled-machinery measurement instrument in the lane directory, not a
  change to the frozen architecture and not a proposed learner design.

## K2d: pure Zag plus shell

Zero Python, C, JavaScript, or Rust invocations at every stage (source,
build, execution, analysis). Toolchain guard recorded in NAMECHECK.md
Step 0. `which python3` prints nothing under the safebin PATH.

## K1c: driver self-audit design

- Every tuple passed to cognition flows through ow_event (kind 1, TEACH)
  or ow_mquery (masked QUERY, kind 2, expected=-2, flags=1). Both log the
  tuple and increment the header-field-52 audit counter. PHASE markers are
  driver-side prints; they never reach cognition.
- No stdin token, no mode dispatch: the driver always runs the single
  frozen 98-event script. TREAT vs CONTROL is selected at build time by
  which core is linked; the driver never sees the selection.
- All runs launch with empty argv and a fully empty environment via
  `bash -c 'exec -c'`.
- Audit counter expectation: 98. All 6 official runs printed AUDIT_PASS
  (98/98 EV lines confirmed in transcripts).
- Transcripts contain no PID, no timestamps, and no paths.
