# N03 BUILD02 review dispositions

Read the complete independent R33_NATIVE_N03_REVIEW.md (SHA256
52ca9764dd08396a4b2594422a7e3a62b8d6718d6d8bc19f75615ae498a76fa6).
It reviewed unexecuted BUILD01, not this amended source. A new BUILD02 independent
review was dispatched; it returned a terminal stream failure after starting and
produced no review file. No final-source independent approval is claimed.
The main agent reviewed the full amended journal, driver, boundary driver and
installed Darwin ftruncate/event interfaces. This admits engineering fixtures
only, not an independent scientific/authority gate.

## Dispositions of the original findings

| Finding | Prospective correction / falsifier |
| --- | --- |
| R1 ignored root-head hash result | Check result, close all state on failure; boundary5 injects only a failing hash result and checks state/head/table/fd absence plus later normal recovery |
| R2 unchecked partial write | Check actual write/fsync; distinguish reached partial-abandonment-8011; crash2 and partial-return controls read exact retained88-byte prefix |
| R3 duplicate I/O reported conflict | Separate failed open-8008, short/shape-8001 and digest-8003 from conflict-8007; boundaries20–22 verify poisoning and blocked continuation |
| R4 rollback overclaim | Rename fixture action as kind2 initial-byte append; no historical-target enforcement or grant claim |
| R5 alias ambiguity | Reject state/head/table aliases; reject partial-overlap copies before writes, allow exact identity; boundaries17–19 |
| R6 failed-attempt provenance | Keep reservation-only claim. Selected authored attempt bytes are checked but arbitrary unpublished attempts are not authenticated or semantically certified |
| File-size/header mismatch | Use128KiB child file ceiling; boundary1/2 test payload1/65536 and exact root/event sizes; max-reload uses a fresh process; boundary3/4 refuse0/65537 before directory creation |

Additional cases cover root mismatch/truncation/extension/edit, incomplete
initialization, reinitialization refusal, event/attempt gaps and first
out-of-envelope slots, malformed/resealed records and duplicate transaction IDs
in an otherwise hash-consistent chain. Original crash phases now retry the
original transaction after prepublication death and prove subsequent idempotency.
Corruption helpers preserve a preimage before changing any fixture file.

## Strongest remaining criticism

This remains a trusted-operator component. Root and record test oracles use
shared encoding helpers and the separately tested SHA primitive; the schedule
is not an independently implemented complete file-format conformance proof.
The root-head failure seam tests a failing branch, not actual allocator exhaustion.
The bad-fd duplicate case deliberately closes this fixture's root descriptor;
it proves the failed-open path, not every possible filesystem race.

Source-identical imported functions and local constants remain subject to the
pinned compiler. No imported numeric constant is consumed by the driver for a
size/index/oracle. N01P's six imported-name failures stay frozen, not repaired.

The parent checks actual child exit/reap, captured bytes, timers and native child
terminal evidence. This is stronger than a compilation or nonempty stdout, but
not proof against a malicious child forging output. Only reviewed fixtures run.
Later batches stop after a failure; members of an already-entered basic/crash/
partial-capacity group may still complete their explicit diagnostic follow-ups.

## Still unqualified

Power loss/APFS/controller durability; authenticated signatures/grants;
same-user hostile mutation/resealing; arbitrary directory-content quota;
full failed-attempt provenance; exhaustive allocator/syscall/EINTR failure;
concurrent readers or arbitrary forged pointers; complete brain/optimizer/RNG/
sensory/telemetry state; parent continuity; learning; authority; promotion.

No fixture counter is called learned competence. All negative observations and
protocol deviations survive. A clean result may support only the exact58-case
native opaque-snapshot component lane at the recorded source/resource envelope.
