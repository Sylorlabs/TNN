# N19 recovery and telemetry protocol

The fixture's journal is an append-only sequence of fixed 32-byte records.
Each record contains a magic value, the next sequence number, a payload length,
up to 16 payload bytes, and a bounded additive checksum. The checksum is only
an accidental/torn-write detector.

Recovery always starts from a zeroed fresh `N19State`; it never rewinds or
rewrites the source journal. Replay accepts only exact record multiples, exact
next sequence numbers, valid payload lengths, valid checksums, and no more than
eight records. Any refusal poisons the in-memory handle and exposes no partial
state as accepted state. The audit head is monotonic within a successful
replay and is never decremented by recovery.

The native I/O layer additionally requires bounded path length, regular-file
identity, bounded write size, bounded write-call count, and explicit syscall
failure handling. The source contains callable isolated-file, sync, readback,
and direct-child fresh-process recovery modes, but this compile-only package
has no runtime witnesses. A later execution gate must add crash-phase
witnesses, measured fsync/durability evidence, and non-rewindable audit-file
evidence. Those are not claimed here.
