# R33-N05A pre-exposure engineering review

Main-agent review only. No independent verdict is claimed: the current native
tool registry returned no `spawn_agent` function. This does not discharge a
scientific, protected-runtime, or learner-authority review gate.

The current state/registries and complete N04 accumulator, IO V1, process V3,
SHA V2 and journal V2 implementations were inspected before the new source.
N04 and all consumed protocols remain unchanged. The earlier N05 and D01 draft
identities are preserved; this new implementation is separately reserved.

Before compilation or fixture execution, source review identified that calling
`nio_guard` inside a child would try to raise the already-lowered hard file
limit. The child now installs only its 15-second timer, retaining the parent's
CPU/file/core/descriptor limits and independent parent-owned deadline. This was
a prospective source correction, not an observed test failure. Input alias
checks were expanded to cover either input against every internal buffer.

Reviewed success ordering: validate and stage before reservation; reserve and
sync directory; write and sync bytes; exclusive publication; directory sync;
live-state update and acknowledgment last. Full committed history is parsed
before exposing recovered state. Partial/unpublished reservations are retained
and counted, never treated as input events. Failure after publication returns
an indeterminate error, not an invented rollback. The fault seams simulate
failure at synchronization boundaries; they are not real disk failures.

The signed encoding uses explicitly bounded i64 arithmetic for all 32-bit values.
Record and root hashes cover version/identity/ordering metadata. Diagnostic
resealing deliberately makes the duplicate, stale-parent, reordered, unsupported
version, and malformed causal tests exercise semantic gates rather than merely
the checksum gate. Corruptions occur only in new fixture directories after an
independent preimage file is durably saved.

The six causal slots preserve exact caller-supplied bytes and explicit missing
markers. Their role labels and byte patterns are engineering fixtures. This
neither proves actual learner reasoning nor authenticates supplied evidence.
The 64-byte payload limit is explicit; full raw media and arbitrary causal
state require a later version and separate qualification. Integrity hashes are
not signatures or human permission. The store is trusted single-writer, not
hostile-user containment; arbitrary filenames outside the registered bounded
namespace are not certified. Process-death behavior is not a hardware power-cut
test. Synthetic N04 resource fields are not actual process-resource measurements.

The primary driver checks fresh replay against all saved metric/state/causal
bytes plus independent literal metrics; checks positive missingness; retains
abandoned reservations after a new successful append; and stops subsequent
cases after an unexpected outcome. A sole primary failure must remain frozen
and needs a new corrective identity, not altered expectations.

Current status: source reviewed; no fixture execution has occurred. Compilation,
exact frozen import/source/build checks, and registry admission remain required.
