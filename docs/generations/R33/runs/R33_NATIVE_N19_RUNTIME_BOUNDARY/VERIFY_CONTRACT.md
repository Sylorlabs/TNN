# N19 BUILD_06 verification contract

This contract describes the current BUILD_06 native runtime boundary and the
scope actually demonstrated by `RUNTIME_QUAL_06_RESULT.json`. BUILD_06 contains
no fork/wait/spawn path. Fresh-process recovery is represented by two distinct
binary invocations: a writer invocation followed, after process exit, by a
recoverer invocation.

## Current modes

| Mode | Expected status | Required invariant |
|---|---:|---|
| `case-malformed` | `-1901` | malformed/non-32-byte record is refused before state mutation |
| `case-overflow` | `-1902` | checked i64 addition refuses max+1 |
| `case-capacity` | `-1903` | ninth 32-byte event is refused at the 8-event/256-byte boundary |
| `case-recovery` | `0` | two valid in-memory records replay into fresh state with sequence/event/audit 2 |
| `case-corruption` | `-1906` | changed payload fails the stored checksum |
| `case-limit` | `0` | accepted resource-limit inputs reach the native limit configuration path; enforcement/accounting is not thereby qualified |
| `case-host-abi <root>` | `0` on the pinned host fixture | root directory can be opened under pinned Darwin constants and directory fsync succeeds |
| `case-probe-existing <root> <leaf>` | refusal or success according to leaf invariants | leaf is single-component, regular, current-owner, single-link, and opened without following links |
| `case-torn <root> <leaf>` | `-1906` for the 16-byte fixture | explicit torn record is refused during recovery |
| `case-io <root> <leaf>` | `0` on the pinned fixture | create exact-0600 leaf, write exactly 32 bytes, file fsync, root-directory fsync, reopen/replay |
| `case-write <root> <leaf>` | `0` on the pinned fixture | durable single-record writer commits only after exact write + file fsync + root-directory fsync |
| `case-append-existing <root> <leaf>` | `0` for the strict one-record fixture | reopens a valid sequence-1 journal, requires exact 32-byte prior state, appends sequence 2, file-fsyncs and root-fsyncs, and reports state 2/2/2 |
| `case-recover-file <root> <leaf>` | `0` for a valid committed journal | a separate later BUILD_06 invocation reopens and recovers the complete journal; the BUILD_06 qualification recovered 2/2/2 from the 64-byte append fixture |

## Demonstrated BUILD_06 scope

BUILD_06 preserves the BUILD_05 pinned-host refusal and durability evidence and
adds strict existing-journal append qualification. In `RUNTIME_QUAL_06`, a new
32-byte sequence-1 journal was committed, `case-append-existing` validated that
exact prior state and appended sequence 2 with file + root-directory fsync, and
a separate later `case-recover-file` invocation recovered sequence/event/audit
`2/2/2`. The resulting journal was 64 bytes, regular, mode `0600`, current-owner
and single-link. The host ABI constants and relevant SDK/header inputs remain
hash-pinned in `HOST_PINS_20260911.json`.

## Explicit non-claims / remaining qualification work

- The root is reopened by pathname for each operation. Stable root-capability
  custody across hostile directory rename/replacement is not claimed.
- Open/openat failures are still translated coarsely. Complete stable errno
  classification into PATH vs HOST_ABI vs IO is not qualified.
- The explicit torn-record fixture is not a crash/power-loss phase matrix.
- Resource-limit configuration was exercised, but enforcement and measured
  resource accounting remain unqualified; missing observations must remain
  missing rather than inferred from configured limits.
- General descendant/process-group containment is not claimed by BUILD_06.

No runtime result from this contract grants learner authority, scientific
promotion authority, or permission to mutate canonical R27.
