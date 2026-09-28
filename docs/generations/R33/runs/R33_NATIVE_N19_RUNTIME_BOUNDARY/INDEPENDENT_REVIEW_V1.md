# Independent Review B — R33-N19 runtime boundary

Review scope: final packet contents under
`Research/R33_NATIVE_N19_RUNTIME_BOUNDARY`. This review is limited to
read-only inspection of the Zag source, compile record and artifact metadata,
JSON contracts, refusal/recovery/telemetry documents, hash manifest, and the
host-ABI blocker. The binary was not executed. No Python was used. No global
state, canonical R27 state, registry, or other experiment directory was
modified.

## Disposition

`REQUEST_CHANGES`

This is not approval for preregistration and is not execution authorization.
The packet is appropriately conservative about its compile-only status, but
one internal telemetry contract mismatch must be corrected before the packet
can be reconsidered.

## Checks performed

### Native source and scope

- `n19_runtime_boundary.zag` is self-contained Zag source and contains no
  learner, training, evaluator, parent-state, promotion, registry, or
  canonical-R27 access path.
- The source contains only bounded journal, file, limit, process, refusal, and
  telemetry fixture responsibilities. The source-level audit found no Python
  or subprocess dependency.
- The source explicitly labels direct Darwin syscalls as a candidate
  implementation rather than a qualified host ABI.

### Compile record and artifact

- `BUILD_RECORD.json` consistently records
  `NATIVE_MACOS_ARM64_COMPILE_ONLY_PASS`, `executed:false`, zero scientific
  exposure, and no canonical-R27 touch.
- The recorded compiler, target, flags, source hash, compiler hash, binary
  hash, stdout hash, and stderr hash match the packet files.
- The packet hash manifest passes for every listed packet file and the pinned
  compiler. The compile stderr file is empty, and the artifact is an arm64
  Mach-O executable.

### JSON and status contracts

- All packet JSON files parse successfully.
- `STATUS.json` consistently reports design/compile-only, unregistered,
  unpreregistered, unreserved, unfrozen, unadmitted, unexecuted,
  `binary_executed:false`, `scientific_exposure:0`, `python_execution:false`,
  and no canonical mutation.
- The refusal matrix contains 12 bounded cases covering malformed input,
  overflow, capacity, recovery, corruption, limits, host ABI, I/O, process
  lifecycle, path, and output bounds.

### Refusal and recovery design

- The source has distinct refusal codes for malformed input, overflow,
  capacity, path, I/O, recovery, limits, and the host-ABI blocker.
- The recovery contract requires exact record sizes, sequence continuity,
  checksum validation, bounded capacity, fresh-state replay, and poisoned
  state on refusal. The checksum is correctly described as non-cryptographic.
- The documents clearly distinguish source-level expected behavior from
  runtime evidence and state that no mode has been run.

### Host-ABI boundary

- `ABI_BLOCKER.md` is explicit and accurate that direct Darwin syscall
  compilation does not establish a capability-safe macOS/APFS ABI.
- The packet does not overclaim host qualification. The next gate correctly
  requires ABI, durability, containment, reservation, and native execution
  closure before any execution claim.

## Exact remaining blockers

1. **Telemetry schema/emitter mismatch.** `TELEMETRY_SCHEMA.json` defines 14
   record fields beginning with `case_id, phase, status, detail`, while both
   source emitters produce a 16-column CSV line including the undocumented
   `N19_TELEMETRY` marker. In `n19_emit_state`, `detail` is omitted before
   `attempted` and `committed`, and the later `recovered`/`recovery_state`
   values do not align with the declared field order. The packet needs one
   frozen wire format: either document the marker/envelope and correct the
   field count, or change the emitters/schema so every emitted column maps
   exactly to the 14 declared fields. Add a source-level serialization check
   or known-answer fixture after the format is corrected.

2. **Host ABI remains unqualified.** Before any host-qualification claim,
   the packet still needs a stable capability-safe macOS/APFS contract for
   root-relative traversal, symlink/hardlink policy, errno translation,
   append/fsync/replay crash durability, process-group and descendant
   containment, resource accounting and telemetry publication, and an ABI
   identity independent of compiler internals.

3. **No runtime evidence exists.** Refusal, recovery, I/O, limit, process,
   telemetry, and durability behavior remain unexecuted design expectations.
   A later run needs a fresh owner-authorized reservation, frozen source/build
   and host pins, isolated paths, crash-phase witnesses, measured durability
   evidence, and explicit cleanup/recovery evidence. This review does not
   authorize that run.

4. **Host/build inputs are not fully frozen.** `BUILD_PINS.json` leaves the
   exact macOS release and SDK headers unpinned. Those inputs must be frozen
   or explicitly bounded before relying on the direct Darwin syscall ABI.

## Final review conclusion

N19 is a well-scoped native Zag compile-only candidate with good custody and
non-execution controls. It is not yet a preregistration-ready or
host-qualification-ready packet because the telemetry wire contract is
internally inconsistent and the documented ABI/runtime blockers remain open.
