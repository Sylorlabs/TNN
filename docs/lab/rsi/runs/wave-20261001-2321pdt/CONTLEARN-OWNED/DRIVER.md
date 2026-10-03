# DRIVER.md: CONTLEARN-OWNED discrimination build record

Wave: wave-20261001-2321pdt. Lane: CONTLEARN-OWNED. Date: 2026-10-02.
Implements frozen prereg PREREG_OWNED.md as amended (Amendment A1,
re-freeze commit d2fc968f4). Pure Zag plus shell orchestration. No Python,
C, JavaScript, or Rust at any stage.

## What was built

Two binaries, one fixture driver, from exactly two logged znc invocations:

- `ow_core_control.zag`: the recorded nomain derivation of the frozen core
  (extracted read-only from the recorded 2321pdt commit; SHA-256
  `26b455e78a9b0ba0f6d6967c12ff8c05f9ebd9152dddca9efeb2a3b44064ec9d`,
  matching the recorded value). Byte-identical to the frozen file minus the
  single `fn main` line.
- `ow_core_disabled.zag`: mechanical derivation of the above with exactly
  the two `ev_query` call blocks removed (the `mp_run` trial call and the
  `bootstrap_miss` P-INV call; frozen-file lines 826-831). SHA-256
  `94b405fc8acce8c2de120d972797052a6468e415e874b549d03c3eecb2fe8407`.
  `diff` against the control core shows exactly those six removed lines
  and nothing else; the variant-diff SHA-256
  `3f385dc56367337f352da35ffd1b29bde0b7a124c68a42a57d717ad043cfaa75`.
  The five machinery functions (`mp_run`, `t2_trial`, `t2_try_verify`,
  `promote_graph`, `bootstrap_miss`) remain as dead code; grep confirms no
  event-interface function (`ev_query`, `ev_teach`, `ev_teach_in`,
  `ev_observe`, `ev_act`, `miss_inquire`, `activate`) contains any call to
  them, and every remaining call site sits inside the dead cluster itself
  (`mp_run` body calls `t2_trial`; `t2_trial` body calls `t2_try_verify`
  and `promote_graph`). The variant is a measurement instrument in the
  lane directory, not a change to the frozen architecture.
- `ow_driver.zag`: the new fixture driver source (this lane's only
  hand-written source file). Implements the frozen 98-event script from
  PREREG_OWNED.md section 4, with content-identified white-box oracles for
  STORE_OK, REUSE_OK, DELAYED_OK, SANITY_E, and the per-phase mechanism
  census. SHA-256
  `c8bc989770b6f59d9b95f9327a5acd7d3c75f2b7d14bf8f7fe8d30717475a5d0`.
- `ow_combined_control.zag` / `ow_combined_treat.zag`: concatenations,
  the two znc inputs. SHA-256
  `bf6c0caf63b26320c1d53a2d2b2a58a6e8aa2e35aff9145d85e0b5894adbe570`
  (control) and
  `a1e95eaeab5f2d0167381c28dc61d58236c827de31e401678a98c3fd0a080f1e`
  (treat).

Build commands (the two logged invocations, K1b):
`sh znc_wrap.sh ow_combined_control.zag -o ow_control`
`sh znc_wrap.sh ow_combined_treat.zag -o ow_treat`

## Hashes of build artifacts

- `ow_control` (binary):
  `58f2f9f2d3855c782106d41266bc30acea29870ea0cf1f1b08282ef78954d400`
- `ow_treat` (binary):
  `6b65e6a62e56f43feb14e1afa45309c9512759ad7ba471a24d68b6b0502c2f71`
- `lo_driver_k3`: the committed 2321pdt `lo_driver` binary extracted
  read-only from the recorded commit for the K3 no-regression check.
  SHA-256 `35f78f8c3eb6fce9dec2262875f8cb1cb0efef1f7cffa824bdfaebb9a7a0ac4a`
  (matches the recorded 2321pdt value).

## K2a: frozen ISA boundary (verified three times)

1. Before implementation: SHA-256 =
   `a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd`;
   git blob hash `b226b223cb3ee0be742af673653fb8ea8605f281` equals the blob
   at the freeze commit f4de7ff46 (the file is untracked in this checkout,
   so the check is blob equality, which is stronger than the empty diff).
2. Immediately before the builds: same hash, same blob equality.
3. After all runs: same hash, same blob equality.
The frozen file was referenced read-only throughout; it was never written.

## K1b: exactly two znc invocations

`znc_wrap.sh` logs every znc invocation to `znc_invocations.log`, then
execs the pinned znc at
`/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1`.
Log content after the full experiment: exactly 2 entries (the two pre-run
builds). Zero new entries appeared during the 6 runs. (The builds emitted
analyzer warnings only, the same A0102 warning class as the prior waves;
both binaries were written and run cleanly.)

## K2b: driver source audit

The driver is fixture: it emits the frozen event script, calls the frozen
event API (`ev_teach`/`ev_query`), runs read-only censuses through the
core's own accessors (`ng`/`eg`/`activate`/`is_superseded`), and prints
results. Audit results on `ow_driver.zag`:

- Cognition functions defined: 0. All 19 `ow_`-prefixed functions are
  fixture/measurement: event emission (including the masked-query choke
  point with the frozen parameters expected=-2, flags=1), structural
  predicates replicating the prereg's oracle definitions, the mechanism
  census, FNV-1a checksum, transcript printing, mode dispatch. No
  learning, retrieval, inference, retention, eviction, planning,
  derivation, revision, or execution logic.
- Structural writes: `ns(` count 0, `link_edge` count 0, `alloc_node`
  count 0. The driver never creates nodes or edges; it only reads arena
  state.
- New node tags: 0. New edge types: 0. New opcodes: 0. New modes: 0.
  New bridges: 0. New routers: 0. New task-specific handlers: 0.
  New semantic cases: 0.
- `switch`/`match` count in driver source: 0 (case-insensitive grep).
- The frozen source contains zero `ow_` occurrences, so no driver name
  collides with or redefines any frozen function.

## K2c: cognition-source delta accounting (measured)

- Lines added to cognition source: 0. Lines deleted: 0. Net: 0.
- New hardcoded semantic cases: 0. New modes: 0. New bridges: 0.
- New routers: 0. New task-specific handlers: 0.
- The variant core is a disabled-machinery measurement instrument in the
  lane directory (CO-5 verified); it is not a learner design and is not
  presented as one. One-system rule: the single persistent workspace is
  the arena; all learner-state structures counted by the per-phase census
  are in frozen formats. No independent subsystem state.

## K2d: pure Zag plus shell

Zero Python, C, JavaScript, or Rust invocations at every stage (source,
build, execution, analysis). Toolchain guard recorded in NAMECHECK.md
Step 0. `which python3` prints nothing under the safebin PATH.

## K1c: driver self-audit design

- Every tuple passed to cognition flows through one of the two choke
  points `ow_event` (TEACH, kind 1) or `ow_mquery` (masked QUERY, kind 2,
  with the frozen supervisor-disconnect parameters expected=-2, flags=1).
  Both log the tuple and increment the header-field-52 audit counter.
  PHASE markers are driver-side prints; they never reach cognition.
- The run mode token (TREAT or CONTROL) arrives on stdin and is consumed
  by the driver only as a transcript label; it is never passed to
  cognition.
- All runs launch with empty argv and a fully empty environment via
  `bash -c 'exec -c ./ow_<bin>'` (`env` is not linked in safebin).
- Audit counter expectation: 98 (Amendment A1). All 6 runs printed
  AUDIT_PASS (98/98 EV lines confirmed in transcripts).
- Transcripts contain no PID, no timestamps, and no paths.
