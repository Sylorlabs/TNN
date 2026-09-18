# R33-N09 — supervisor-anchored checkpoint integration passed

Sole primary exited0;15 top-level children and one nested kernel-confined worker
were reaped. All704 verified completed-child checks and150 parent checks matched.
Native JSON records148 parent checks before successful result-save and root-close.
The deliberate exits73/74 were registered crash boundaries, not unexpected errors.

## What the integration established

The current4096-byte payload delivered exactly in a fresh process; the authentic
older receipt was refused. An authenticated restoration of initial synthetic
payload bytes advanced state version13/nonce2/spend5, rather than refunding or
rewinding accounting. A receipt from another authentic branch with the same
numeric counters was refused against the current branch head. Restriction
epoch1/budget2 invalidated the old receipt despite unchanged payload/version12.

All256 individually tampered receipt-byte positions refused without changing
sentinel output. Short packet/export/delivery and private aliases refused;
valid packet/output overlap delivered the exact staged bytes. Unsafe quoted or
newline-containing profile path inputs refused before launching anything.

Fresh recovery after committed-authority/before-cache death and a torn-cache
death retained nonce1/spend3/version12, rejected stale/torn receipts and rebuilt
the exact current cache from authority. After durable uncommitted intent death,
recovery retained nonce1/spend3/seq1/orphan1 while delivering original payload at
version11. Even its pre-intent receipt was stale. Corrupting the authoritative
intent prevented open and any cache-only fallback; the valid cached receipt did
not become substitute authority. Original corruption preimage remains preserved.

The nested worker received the exact4320-byte current receipt, independently
reported its SHA256, and was denied write access to that cache and read/write/
unlink access to the actual control intent. Socket creation and fork were
denied. No nonstdio descriptors survived, including deliberately leaked authority
descriptor40. The controller reopened the actual authority afterward and verified
exact state/version12/spend3. Worker binary contains no authority implementation
or synthetic signing keys; those remain in the trusted fixture controller.

## Evidence, resources and limitations

Evidence: [native result](R33_NATIVE_N09_RUN_PRIMARY_V1/NATIVE_RESULT.json),
[supervisor](R33_NATIVE_N09_LAUNCH.stdout),
[actual worker](R33_NATIVE_N09_RUN_PRIMARY_V1/sandbox-worker.stdout),
[orphan recovery](R33_NATIVE_N09_RUN_PRIMARY_V1/crash3-replay.stdout),
[protocol](R33_NATIVE_N09_ANCHORED_CHECKPOINT/PREREGISTRATION.md).
Native result SHA256631be008e91ba05507924560e1c1d6bd8c5033edca56a84663077e27a36584c5;
supervisor SHA256735ded2a1c4feece6abbd4af587ab3943bd05519fbbe1b7ebc7dd57fe40b5447.

Top-level childCPU151,755us/summed observed wall434,452us/peakRSS2,555,904bytes.
Nested worker separately reportsCPU12,786us/wall224,599us/peakRSS1,474,560bytes;
do not silently add overlapping parent/child accounting. Host0.70s/maxRSS5,423,104.
No worker/controller survivor matched the scoped check. Both compilation pairs
are byte-identical;39 source/build/protocol pins and inherited platform/authority
pins verified before admission2026-09-06T03:50:54Z.

This qualifies a bounded checkpoint cache against the independently held current
supervisor journal and pinned kernel-worker boundary. It is NOT protection
against a host administrator or trusted controller replacing the entire journal,
nor a hardware/remote monotonic anchor. N07's authentic-prefix limitation remains
true in that broader threat model. Real human identity/key custody, full learner
causal serialization, hard aggregate resource enforcement, original R27 semantic
continuity and full protected runtime remain unqualified. No learner, scientific
world, actual human grant or training executed. Main engineering review is not an
independent security or scientific certification.

Twenty-one diagnostic batches consumed, zero R33 training/newborn restarts/new
authority/promotion/canonical mutation. R27 remains60423. Continue complete
causal-state integration and source-grounded parent continuity; no full-R33
completion certificate is issued by this component pass.
