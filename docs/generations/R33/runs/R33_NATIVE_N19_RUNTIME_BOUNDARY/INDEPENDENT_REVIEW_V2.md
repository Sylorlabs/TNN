# Independent Review V2 — R33-N19 runtime boundary

Review date: 2026-09-09

## Scope and restrictions

This review inspected only the packet under
`Research/R33_NATIVE_N19_RUNTIME_BOUNDARY`, including the corrected Zag
source, telemetry schema and fixture, compile record and artifact metadata,
refusal and recovery contracts, packet hash manifest, and Independent Review
V1. The binary was not executed. Python was not used. No global state,
canonical R27 state, registry, or other experiment directory was modified.

## Disposition

`REQUEST_CHANGES`

N19 is not preregistration-ready and this review is not execution
authorization. The V1 telemetry column-count finding is corrected, but the
host ABI is still explicitly unqualified, no runtime witness exists, and the
host/build inputs needed for a native ABI claim are not fully frozen.

## Checks performed

### Corrected telemetry envelope and mapping

- `TELEMETRY_SCHEMA.json` declares one fixed `N19_TELEMETRY` envelope marker,
  14 record fields, and 15 total comma-delimited columns.
- Both lines in `TELEMETRY_FIXTURE.json` have exactly 15 columns. The mapping
  is exact: column 1 is the marker; columns 2–15 are, in order,
  `case_id`, `phase`, `status`, `detail`, `bytes_attempted`,
  `bytes_committed`, `sequence`, `event_count`, `audit_head`,
  `resource_limit`, `resource_observed`, `recovery_state`, `stdout_bytes`,
  and `stderr_bytes`.
- The corrected source emitters at `n19_runtime_boundary.zag:248-261` use the
  same envelope and field order. The malformed fixture maps to
  `malformed,status,-1901,0` followed by explicit missing values; the
  recovery fixture maps to `recovery,status,0,0,64,64,2,2,2,-1,-1,recovered,-1,-1`.
- The V1 finding of an undocumented marker and 16-column output is therefore
  closed at the static source/schema/fixture level.
- This remains a source-level known-answer contract, not runtime telemetry.
  In particular, the recovery dispatch supplies fixed `64,64` byte values
  to the emitter (`n19_runtime_boundary.zag:273`); a future executed failure
  path must not report those values as observed unless they were actually
  attempted and committed.

### Native Zag compile identity

- `n19_runtime_boundary.zag` is self-contained native Zag source. No Python
  import, Python subprocess, learner, training, evaluator, parent-state
  reader, promotion path, registry writer, or canonical-R27 access path was
  found.
- `BUILD_RECORD.json` and `BUILD_PINS.json` agree on the macOS-arm64 target,
  compiler, flags, language, and compile-only status.
- The recorded source, compiler, binary, compile-stdout, and compile-stderr
  SHA-256 values match the packet files and the pinned compiler.
- The packet manifest passes for every listed packet input and the pinned
  compiler.
- `BUILD_01/n19` is identified as a Mach-O 64-bit arm64 executable. The
  compile stderr is empty, and the compile stdout records zero external
  build tools.

### JSON, refusal, and recovery contracts

- All packet JSON files parse successfully.
- `STATUS.json` consistently reports native-only, unregistered,
  unpreregistered, unreserved, unfrozen, unadmitted, unexecuted, zero
  scientific exposure, no Python execution, no canonical mutation, and an
  explicit unqualified host-ABI blocker.
- `REFUSAL_MATRIX.json` represents 12 bounded cases covering malformed
  input, checked overflow, capacity, valid recovery, corruption, resource
  limits, host-ABI refusal, isolated I/O, direct-child reaping, fresh-process
  recovery, oversized paths, and oversized output.
- `VERIFY_CONTRACT.md` and `RECOVERY_PROTOCOL.md` consistently distinguish
  source-level expected statuses from runtime evidence. The recovery design
  requires fixed record sizes, sequence continuity, checksum validation,
  bounded capacity, fresh-state replay, and poisoned state on refusal.
- The checksum is correctly limited to accidental/torn-record detection and
  is not presented as cryptographic integrity.

### Host ABI boundary

- `ABI_BLOCKER.md` accurately states that direct Darwin syscall compilation
  does not qualify a capability-safe macOS/APFS host ABI.
- The source contains direct Darwin syscall and direct-child process paths,
  but the packet makes no unsupported qualification claim and explicitly
  disclaims descendant/process-group containment and host-admin rollback
  protection.

## Exact remaining blockers

1. **The macOS/APFS host ABI is unqualified.** A stable, reviewable contract
   is still missing for capability-safe root-relative traversal,
   symlink/hardlink policy, stable errno/status translation, append/fsync and
   crash-durability semantics, process-group and descendant containment,
   resource accounting/telemetry publication, and an ABI identity independent
   of compiler internals.

2. **There is no runtime evidence.** No refusal, recovery, I/O, limit,
   process, telemetry, crash-phase, or durability mode has been run. The
   compile-only artifact cannot establish the behavior described by the
   contracts. A future run requires a new owner-authorized reservation,
   frozen packet and host pins, isolated paths, captured stdout/stderr and
   statuses, crash-phase witnesses, durability evidence, and recovery/cleanup
   evidence.

3. **Host/build inputs are not fully frozen.** `BUILD_PINS.json` explicitly
   leaves the exact macOS release unfrozen and does not separately pin SDK
   headers. The syscall-number and flag literals therefore remain candidate
   source inputs rather than a portable, independently frozen ABI.

4. **Telemetry observation semantics still need an execution-level witness.**
   The 15-column/14-field structure is now correct, but the packet needs a
   later executed serialization check proving that each emitted value is
   observed from the case outcome, especially attempted/committed bytes and
   failure-path state. The fixture alone is not evidence.

## Conclusion

N19 is a conservatively scoped native Zag compile-only candidate, and the V1
telemetry shape defect has been corrected and verified statically. It is not
preregistration-ready or host-qualification-ready while the four blockers
above remain open. No execution authorization is granted by this review.
