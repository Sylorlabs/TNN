# DRIVER.md: CONTLEARN fixture driver build record

Wave: wave-20261001-2021pdt. Lane: CONTLEARN. Date: 2026-10-01.
Worker: phase-2 implementation subagent. Pure Zag plus shell orchestration.
No Python, C, JavaScript, or Rust at any stage.

## What was built

One binary, `cl_driver`, from exactly one znc invocation. The binary links
the frozen TNN-2 core read-only with a new fixture driver:

- `cl_core_nomain.zag`: mechanical derivation of the frozen core
  `docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag` with only
  the single entry-point line `fn main()i32 { return run_all(); }` (line 1357)
  removed, so the driver can supply `main`. Verified by diff: exactly one
  line deleted, nothing else changed. The frozen file itself was never
  written; it was only read.
- `cl_driver.zag`: the new fixture driver source (this lane's only
  hand-written source file).
- `cl_combined.zag`: concatenation of the two, the single znc input.

Build command (the one logged invocation):
`sh znc_wrap.sh cl_combined.zag -o cl_driver`

## K2a: frozen ISA boundary (verified three times)

1. Before implementation: SHA-256 =
   `a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd`,
   `git diff f4de7ff46` on the frozen path empty.
2. Immediately before the build: same hash, same empty diff.
3. After all 21 runs: same hash, same empty diff.

Expected hash from the prereg:
`a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd`.
Match at all three checks. The frozen file was referenced read-only.

## Hashes of build artifacts

- `cl_driver.zag`: `b7a1877eb64545b2490ad2ee50f0b818dfd8ff6ac08e6f84e00a00cd0d45a43a`
- `cl_core_nomain.zag`: `26b455e78a9b0ba0f6d6967c12ff8c05f9ebd9152dddca9efeb2a3b44064ec9d`
- `cl_combined.zag`: `4aba249d9ab81530d658fdf14c2b6ba43b83dd2386f8aa6f67b5accfef404d07`
- `cl_driver` (binary): `c8c089b8a0a25f9727719d386aad31fd584a171b3ccbe5ed3bc0b5a72c0e81b7`

## K1b: exactly one znc invocation

`znc_wrap.sh` logs every znc invocation to `znc_invocations.log`, then execs
the pinned znc at
`/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1`.
Log content after the full experiment: exactly 1 entry (the pre-run build).
Zero new entries appeared during the 21 runs. No second compile exists.

Pre-wrapper scratch builds (disclosed): before the wrapper existed, 4 direct
znc invocations ran in /tmp only, for driver development: two trivial
mechanism probes (`/dev/stdin` read, xor operator) and two full
core+driver scratch builds. Their binaries lived in /tmp, were never used
for any measurement, and were discarded. The experiment binary comes solely
from the single logged invocation above.

## K2b: driver source audit

The driver is fixture: it emits the frozen event script, calls the frozen
event API (`ev_teach`/`ev_query`/`ev_observe`), runs read-only censuses
through the core's own accessors (`ng`/`eg`/`activate`/`is_superseded`), and
prints results. Audit results on `cl_driver.zag`:

- Cognition functions defined: 0. All 30 `cl_`-prefixed functions are
  fixture/measurement: event emission, structural predicates replicating
  the prereg's oracle definitions, census counters, FNV-1a checksum,
  transcript printing, mode dispatch. No learning, retrieval, inference,
  retention, eviction, planning, derivation, revision, or execution logic.
- New node tags: 0. New edge types: 0. New opcodes: 0. New modes: 0.
  New bridges: 0. New routers: 0. New task-specific handlers: 0.
  New semantic cases: 0. (Tag/edge literals appearing in the driver are
  reads of frozen tags through the white-box census the prereg authorizes,
  not definitions.)
- `switch`/`match` count in driver source: 0 (case-insensitive grep).
- The frozen source contains zero `cl_` occurrences, so no driver name
  collides with or redefines any frozen function.

## K2c: cognition-source delta accounting (measured)

- Lines added to cognition source: 0. Lines deleted: 0. Net: 0.
- New hardcoded semantic cases: 0. New modes: 0. New bridges: 0.
- New routers: 0. New task-specific handlers: 0.
- Learner-state structures created during runs are counted by the per-phase
  census (fact nodes, MAP nodes, SETREG/guard cells, literal nodes, DEP/SEQ
  edges, supersede marks, history nodes); all are frozen formats. See
  RUN_LOG.md.

## K2d: pure Zag plus shell

Zero Python, C, JavaScript, or Rust invocations at every stage (source,
build, execution, analysis). Toolchain guard recorded in NAMECHECK.md
Steps 0 and 0b. `which python3` prints nothing under the safebin PATH.

## K1c: driver self-audit design

- Every tuple passed to cognition flows through the single choke point
  `cl_event`, which logs the tuple as `EV <kind> <s> <r> <o> [ans|rv]`
  and asserts kind in {1=TEACH, 2=QUERY, 3=OBSERVE}. PHASE markers are
  driver-side prints; they never reach cognition.
- The run mode letter arrives on stdin and is consumed by the driver only;
  it is never passed to cognition.
- All runs launch with empty argv and a phase-free environment. Note:
  `env` is not linked in safebin, so the harness launches each run with
  `bash -c 'exec -c ./cl_driver'`, which yields a fully empty environment;
  this strictly satisfies the phase-free requirement.
- Audit counter in arena header field 52 (verified unused by the frozen
  core). Expected counts: TREAT 149, C-P1 24, C-P2 24, C-P3 33, C-P4 18,
  C-P5 80, C-P6 18. All 21 runs printed AUDIT_PASS.
- Transcripts contain no PID, no timestamps, and no paths.

## Erratum found in the prereg (reported, not silently fixed)

Prereg section 3 says "P4 correction (7 events)" and "Total: 150 events",
but the enumerated frozen tuples give 3 OBSERVE + 3 QUERY = 6 P4 events,
for a total of 149 events (24+12+9+6+80+18). The driver implements exactly
the enumerated tuples (149 events; the audit counter confirms 149 audited
events in TREAT). No event was invented to reach 150. No kill bar depends
on the total count, so no bar is affected.
