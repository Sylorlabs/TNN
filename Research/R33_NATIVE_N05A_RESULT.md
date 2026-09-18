# R33-N05A — preserved initial-recovery failure

The sole frozen BUILD01 primary exited 1 after two of forty scheduled children.
Both children were reaped. Invalid mode behaved as expected; normal writer
reported successful creation, then recovery returned -8108 instead of 0. Its
two assertions include one mismatch. The parent reported four failures across
22 checks, including the missing child success/counter and unfinished schedule.
The remaining 38 child cases were not executed, not silently released as fresh
scientific evidence. No durable-telemetry qualification is granted.

Native evidence: [result](R33_NATIVE_N05A_RUN_PRIMARY_V1/NATIVE_RESULT.json),
[parent log](R33_NATIVE_N05A_RUN_PRIMARY_V1/supervisor.stdout), and
[failed child](R33_NATIVE_N05A_RUN_PRIMARY_V1/normal-write.stdout).
The native result's verified-child-check count is zero because the sole failed
child did not return a zero-failure counter; this is not a claim it ran no checks.

Actual summed child CPU is 2,395 microseconds, summed observed nonmonotonic wall
12,677 microseconds, and peak child RSS 1,589,248 bytes. Host time displayed 0.29
seconds and maximum RSS 1,900,544 bytes. These are process observations, not
fixture resource fields or hard RSS containment. A scoped process inspection
showed only the inspection commands, not a surviving n05a child.

## Diagnosis and architecture difference

Read-only byte inspection of the retained 128-byte root shows the first three
configuration words intact but the last three overwritten with pathname-like
bytes rather than 1,1,1. Root SHA256 is
`e60cf57309baf27eb20eb3e0182ac515e30b04a729f0a44872437a53541d9849`.
The new allocator used `_zag_malloc(n*4)` for `[]i32`, whereas the successfully
tested N04 source uses the native `zalloc_i` allocator. The new alias code also
assumed four bytes per in-memory word. This is an unverified native-storage
assumption, distinct from the deliberate four-byte wire encoding, and a concrete
correction target. Exact native stride will be checked prospectively in N05B;
no compiler defect or complete root-cause isolation is claimed from this alone.

The failure belongs to the new adapter, not the unchanged N04 accumulator or
R27. All twenty N05A source/build pins and eighteen inherited N04 pins were
verified before admission. The failed source, configuration, oracles, binary,
logs, admission, reservation, root and native result remain frozen and unrerun.

## Next action and claim boundary

Create N05B with the native integer allocator and correct alias range accounting,
add an explicit ABI/adjacent-allocation guard and wire-range refusal controls,
then repeat the forty known integration shapes as a declared corrective
regression plus the new guard. Preserve the original negative; do not edit N05A
expectations, binary, or files. This is native engineering work, not fresh
generalization, a learner initialization, training, parent migration, a human
grant, or promotion. R27 remains canonical at step 60423/restarts 0.
