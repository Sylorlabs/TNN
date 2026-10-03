# N05B pre-exposure engineering review

The pinned compiler source explicitly documents eight-byte numeric runtime
words. N05A used four-byte allocations and native alias extents; its retained
corruption is consistent with that mismatch. N05B keeps the established native
allocator/free family together, does not pass an arena slice to a different
deallocator, and tests allocation preservation before durable writes. Numeric
disk encoding remains signed little-endian four-byte, distinct from native ABI.
Encoding rejects nonrepresentable values before output mutation or reservation.

The complete N05A source/schedule was inspected. Only the specified allocator,
alias, wire-range guards, new diagnostics and experiment identifiers change.
The six-slot causal representation and prior synthetic controls are unchanged.
All N05A frozen pins and 13 retained result artifacts were reverified read-only;
no failed experiment is rerun. Earlier N05/D01 unexecuted drafts remain inert.

This is main-agent engineering review only. No new independent scientific or
protected-runtime approval, historical source recovery, or learner authority
is asserted. The test remains a trusted direct-child engineering program,
not a full learner or evidence of comprehension. Compiler arena allocation is
bounded by the admitted per-process workloads; no incremental reclaim claim.

BUILD_01 was rejected before executable emission: two inline address/cast
expressions were inferred as pointer values. The current source binds each
address to a typed pointer before casting to i64. The failed build is retained;
BUILD_02 is the prospective primary, without any fixture exposure or change to
the ABI test's expected values.
