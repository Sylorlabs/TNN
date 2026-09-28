# R33-N19 bounded native runtime/telemetry gate

Status: `DESIGN_AND_COMPILE_ONLY_NOT_EXECUTED_NOT_REGISTERED`

N19 is a disjoint engineering candidate for Work package B. It is not a
learning experiment, scientific evaluator, parent-continuity test, promotion
path, or R27 mutation. Its only purpose is to qualify the minimum native host
boundary required before later telemetry and recovery work can be exposed.

## Scope

The fixture covers four bounded native responsibilities:

1. fixed-size append records with sequence and non-rewindable audit head;
2. native Darwin file opening, regular-file checking, bounded writes, and
   explicit I/O refusal;
3. checked resource limits for CPU time and output bytes;
4. fresh-state journal replay with malformed, sequence, checksum, overflow,
   and capacity refusal cases.

It contains no model state, training labels, probes, holdouts, parent bytes,
external collector, Python subprocess, shell child, registry write, or
canonical artifact access.

## Fixed bounds

| Bound | Value |
|---|---:|
| record size | 32 bytes |
| payload per record | 16 bytes |
| journal events | 8 |
| journal bytes | 256 |
| output bytes | 65,536 |
| path bytes | 255 maximum |
| write calls per operation | 1,024 |
| CPU limit accepted by fixture | 1–30 seconds |

## Refusal semantics

The source returns distinct negative statuses for malformed input, checked
integer overflow, capacity exhaustion, path/I/O failure, recovery failure,
resource-limit refusal, and the unresolved host-ABI boundary. A checksum is
only a torn/accidental-record detector; it is not a cryptographic integrity
claim.

## Important qualification boundary

The available compiler exposes direct Darwin syscall escape hatches, but the
current Zag host ABI does not provide a reviewed capability-safe, root-relative
macOS/APFS adapter with a stable contract for openat-like traversal, symlink
policy, crash durability, process-group containment, and portable errno
translation. N19 therefore implements the bounded fixture and records the
exact blocker; it must not be called a qualified host ABI until the ABI and
the later execution evidence are independently reviewed.

## Non-execution rule

No N19 mode is run in this work package. Compilation is the only permitted
validation action. Any future fixture execution requires a new reservation,
registration/admission, frozen source/build/host pins, and an explicit native
execution decision.
