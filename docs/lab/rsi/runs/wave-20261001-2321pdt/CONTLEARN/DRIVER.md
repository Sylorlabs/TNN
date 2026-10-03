# DRIVER.md: CONTLEARN learner-ownership probe build record

Wave: wave-20261001-2321pdt. Lane: CONTLEARN. Date: 2026-10-01.
Worker: phase-2 implementation subagent. Pure Zag plus shell orchestration.
No Python, C, JavaScript, or Rust at any stage.

## What was built

One binary, `lo_driver`, from exactly one znc invocation. The binary links
the frozen TNN-2 core read-only with a new fixture driver:

- `lo_core_nomain.zag`: mechanical derivation of the frozen core
  `docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag` with only
  the single entry-point line `fn main()i32 { return run_all(); }` (line 1357)
  removed, so the driver can supply `main`. Verified by diff: exactly one
  line deleted, nothing else changed. SHA-256
  `26b455e78a9b0ba0f6d6967c12ff8c05f9ebd9152dddca9efeb2a3b44064ec9d`,
  byte-identical to the 2021pdt lane's `cl_core_nomain.zag` hash. The frozen
  file itself was never written; it was only read.
- `lo_driver.zag`: the new fixture driver source (this lane's only
  hand-written source file). Implements the frozen 92-event TREAT script and
  the 20-event NOSTORE script from PREREG_LEARNOWN.md section 3, with
  content-identified white-box oracles for STORE_OK, REUSE_OK, REUSE2, and
  NOSTORE_OK.
- `lo_combined.zag`: concatenation of the two, the single znc input.

Build command (the one logged invocation):
`sh znc_wrap.sh lo_combined.zag -o lo_driver`

## Hashes of build artifacts

- `lo_driver.zag`: `49874d39b6510f8434f6d025fa109b4f2b937547acea5f3bda5cb5808892cb9c`
- `lo_core_nomain.zag`: `26b455e78a9b0ba0f6d6967c12ff8c05f9ebd9152dddca9efeb2a3b44064ec9d`
- `lo_combined.zag`: `38c7666447fc93f76334715008bd02390690fbc48d23ec2f4c3356dfcbee1d00`
- `lo_driver` (binary): `35f78f8c3eb6fce9dec2262875f8cb1cb0efef1f7cffa824bdfaebb9a7a0ac4a`

## K2a: frozen ISA boundary (verified three times)

1. Before implementation: SHA-256 =
   `a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd`,
   `git diff f4de7ff46` on the frozen path empty.
2. Immediately before the build: same hash, same empty diff.
3. After all runs: same hash, same empty diff.

Expected hash from the prereg:
`a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd`.
Match at all three checks. The frozen file was referenced read-only.

## K1b: exactly one znc invocation

`znc_wrap.sh` logs every znc invocation to `znc_invocations.log`, then execs
the pinned znc at
`/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1`.
Log content after the full experiment: exactly 1 entry (the pre-run build).
Zero new entries appeared during the 6 runs. No second compile exists. (The
build emitted analyzer warnings only, the same warning class as the prior
wave's build; the binary was written and runs cleanly.)

## K2b: driver source audit

The driver is fixture: it emits the frozen event script, calls the frozen
event API (`ev_teach`/`ev_query`/`ev_observe`), runs read-only censuses
through the core's own accessors (`ng`/`eg`/`activate`/`is_superseded`), and
prints results. Audit results on `lo_driver.zag`:

- Cognition functions defined: 0. All 19 `lo_`-prefixed functions are
  fixture/measurement: event emission (including the masked-query choke
  point with the frozen parameters expected=-2, flags=1), structural
  predicates replicating the prereg's oracle definitions, census counters,
  FNV-1a checksum, transcript printing, mode dispatch. No learning,
  retrieval, inference, retention, eviction, planning, derivation, revision,
  or execution logic.
- Structural writes: `ns(` count 0, `link_edge` count 0, `alloc_node` count 0.
  The driver never creates nodes or edges; it only reads arena state.
- New node tags: 0. New edge types: 0. New opcodes: 0. New modes: 0.
  New bridges: 0. New routers: 0. New task-specific handlers: 0.
  New semantic cases: 0.
- `switch`/`match` count in driver source: 0 (case-insensitive grep).
- The frozen source contains zero `lo_` occurrences, so no driver name
  collides with or redefines any frozen function.

## K2c: cognition-source delta accounting (measured)

- Lines added to cognition source: 0. Lines deleted: 0. Net: 0.
- New hardcoded semantic cases: 0. New modes: 0. New bridges: 0.
- New routers: 0. New task-specific handlers: 0.
- One-system rule: the single persistent workspace is the frozen arena; all
  learner-state structures counted by the per-phase census (fact nodes, MAP
  nodes, SETREG/guard cells, literal nodes, DEP/SEQ edges, supersede marks,
  history nodes) are in frozen formats. No independent subsystem state.

## K2d: pure Zag plus shell

Zero Python, C, JavaScript, or Rust invocations at every stage (source,
build, execution, analysis). Toolchain guard recorded in NAMECHECK.md
Step 0. `which python3` prints nothing under the safebin PATH.

## K1c: driver self-audit design

- Every tuple passed to cognition flows through one of the two choke points
  `lo_event` (TEACH/OBSERVE) or `lo_mquery` (masked QUERY, kind 2, with the
  frozen supervisor-disconnect parameters expected=-2, flags=1). Both log
  the tuple and increment the header-field-52 audit counter. PHASE markers
  are driver-side prints; they never reach cognition.
- The run mode token arrives on stdin and is consumed by the driver only;
  it is never passed to cognition.
- All runs launch with empty argv and a fully empty environment via
  `bash -c 'exec -c ./lo_driver'` (`env` is not linked in safebin).
- Audit counter expectations: TREAT 92, NOSTORE 20. All 6 runs printed
  AUDIT_PASS (92/92 and 20/20 EV lines confirmed in transcripts).
- Transcripts contain no PID, no timestamps, and no paths.
