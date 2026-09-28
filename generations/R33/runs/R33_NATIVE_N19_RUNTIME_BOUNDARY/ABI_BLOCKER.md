# N19 host ABI blocker

Disposition: `PARTIAL_NATIVE_IMPLEMENTATION_COMPILE_ONLY`

The pinned native compiler can compile direct Darwin syscall calls and expose
basic file/limit operations. It does not currently provide a reviewable
capability-safe macOS/APFS host ABI that simultaneously specifies:

- root-relative traversal and symlink/hardlink policy;
- stable errno/status translation across the full native boundary;
- crash durability semantics for append, fsync, and replay;
- process-group/descendant containment and fresh-process lifecycle rules;
- resource accounting and telemetry publication semantics;
- a stable ABI identity that can be frozen independently of compiler internals.

N19 records this as `N19_REFUSED_HOST_ABI = -1999`. The direct syscall source
is useful as a bounded implementation candidate, but it is not itself proof
that the host ABI is qualified. No execution or qualification claim is made.
