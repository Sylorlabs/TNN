# R33-N19 host ABI contract V1

Status: **prospective contract; implementation/runtime qualification pending**.

This contract narrows the macOS/APFS host boundary required by N19. It is not
an assertion that the existing candidate satisfies the contract.

## Capability root

All writable fixture paths must be resolved beneath one owner-created,
experiment-specific root directory opened before any child work. Later file
operations receive the root capability plus a single relative leaf name. The
runtime must refuse absolute paths, `..`, empty components, embedded NUL, path
separators inside leaf names, and any path longer than the frozen bound.

No operation may follow a symbolic link. Existing targets must be regular
files owned by the fixture identity. A target whose link count is not exactly
one is refused, so an external hard link cannot turn a fixture write into a
write outside the intended custody set. Directory targets, devices, sockets,
FIFOs and unknown file types are refused.

## Open/create policy

The qualified adapter must expose a stable operation equivalent to:

`open_regular_at(root_capability, leaf, create_exclusive_or_existing)`

with these semantic requirements:

- root-relative lookup only;
- no symlink traversal at the final component;
- regular-file verification after open;
- explicit create-vs-existing policy; no silent truncation of an existing
  journal during recovery;
- exact mode `0600` for newly created fixture files;
- every opened descriptor closed on all terminal paths.

Raw syscall numbers/flag literals are implementation details and cannot be the
ABI identity. The ABI identity is this operation/return contract plus the host
pins in `HOST_PINS_20260911.json`.

## Stable status translation

Host errno values must never escape as scientific/evaluator semantics.
The adapter translates host failures into the fixed N19 status classes:

- malformed/capability violation -> `N19_REFUSED_PATH`;
- unsupported host ABI or unavailable required flag/operation ->
  `N19_REFUSED_HOST_ABI`;
- bounded read/write/fsync/close failure -> `N19_REFUSED_IO`;
- journal replay/durability inconsistency -> `N19_REFUSED_RECOVERY`;
- configured resource ceiling refusal -> `N19_REFUSED_RESOURCE`.

The raw errno may be emitted only as bounded diagnostic detail outside the
decision status and must not change acceptance logic.

## Append and durability

A successful durable journal commit requires:

1. a complete fixed-size record written at the intended append offset;
2. a successful file durability barrier (`fsync` semantics on the pinned
   host);
3. no publication of `bytes_committed` until both (1) and (2) have succeeded;
4. close success or an explicit terminal I/O refusal;
5. for a newly created file, a directory durability barrier before the file is
   treated as recoverable across process death.

Partial/torn writes are terminal for the current operation and must be
detectable/refused by fresh-process recovery. No checksum is described as a
cryptographic integrity mechanism.

## Process containment

The qualified fixture may create only a direct child dedicated to one test
case. Before any future runtime qualification, the adapter must either:

- establish a new process group/session and prove bounded termination/reaping
  of the entire group; or
- reject any mode that can create descendants and qualify only the strict
  direct-child subset.

No claim of descendant containment is allowed from direct `waitpid` evidence
alone. All child exits, signals and time/resource limit terminations must map
to fixed N19 statuses and be reaped before the parent publishes success.

## Resource accounting

CPU/output limits are admission bounds, not measurements. Runtime telemetry
must separately report the configured limit and observed value derived from
the executed case. Missing observation is encoded as the schema's missing
sentinel and may never be replaced by the configured limit.

## Qualification rule

Static source review may approve this contract for implementation. Host ABI
qualification additionally requires independently reviewed source, exact host
and build pins, known-answer/refusal fixtures, fresh-process recovery, crash
phase tests, root/symlink/hardlink negative tests, process containment tests,
and execution-level telemetry showing observed rather than prefilled values.
