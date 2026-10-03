# CORE-FREEZE-TNN2 Driver Shim Report

Date: 2026-10-01. Builder: Core Freeze TNN-2 Driver Shim Builder.
Prereg: `ce1a7c5f8` (CORE-FREEZE-TNN2-PREREG-FROZEN). K1 ordering verified.
Status: SHIM-BUILD-PASS.

## 1. Purpose

Transport FW world events into TNN-2's public interface and return
TNN-2 outputs/actions. The shim contains zero cognition per prereg
section 2 and kill bar K-FZ2-3.

## 2. Artifacts

- Source: `docs/lab/research-lead/overnight-20260928/core_freeze_tnn2_shim/freeze_shim2.zag`
  SHA-256: `33795c19c9f7ecd8e4c0c9a180293bf577b53ba7aae6f6a5557c972fe372ace8`
  Lines: 1751 (1590 TNN-2 cognitive/test lines preserved + 161 driver lines)
- Binary: `docs/lab/research-lead/overnight-20260928/core_freeze_tnn2_shim/freeze_shim2_bin`
  SHA-256: `9217054c5af6dec057c4530c4de3ba246f521acc6df741d1989a4504acc72954`
  Built with pinned compiler `src/tools/toolchain/znc_linux_x86_64_abed8aa1`.
  Compilation: zero errors (analyzer warnings only, same class as frozen
  TNN-2 source).
- Driver-only source (for review): `shim_driver2.zag` (161 lines, the added
  interface code). Hashes recorded in `SRC_SHA.txt` / `BIN_SHA.txt`.

## 3. Public protocol

Follows `core_freeze/stage0/INTERFACE.md` (the public world-event protocol
from the original freeze). Invocation:

```
freeze_shim2_bin <world.txt> <state.bin>
```

World file: one event per line, integer ids only.

```
OBSERVE <subj> <rel> <obj>
QUERY   <subj> <rel> <expected>
ACT
```

Output (stdout, fixed format):

```
WORLD_BEGIN
OBSERVED <s> <r> <o>     (one per OBSERVE event)
ANSWER <s> <r> <v>       (one per QUERY event)
CHOICE <v>               (one per ACT event)
WORLD_END events=<n> answers=<q>
STATE_SAVED
```

State file: 110656 bytes (TNN-2 workspace size, same as TNN-1; `tnn2_init`
zeroes 110656). Loaded if present and exactly 110656 bytes; fresh
`tnn2_init(W)` if absent; abort exit 2 if corrupt length. Written after
successful event stream.

Exit codes: 0 ok; 1 world parse error (state untouched); 2 usage or I/O error.

## 4. Interface mapping

| World event | TNN-2 call | Output | Return code |
|-------------|------------|--------|-------------|
| `OBSERVE s r o` | `ev_observe(W,s,r,o)` | `OBSERVED s r o` | 1 |
| `QUERY s r e` | `ev_query(W,s,r,e,0)` | `ANSWER s r v` | 2 |
| `ACT` | `ev_act(W)` | `CHOICE v` | 3 |
| blank line | (none) | (none) | 0 |
| other | (none) | `ERROR line <n>` | -1 |

TNN-2 signatures verified identical to TNN-1's: `ev_query` keeps the
`(W,s,r,expected,flags)` shape, flags=0 as in the TNN-2 test battery, and
returns the -2 miss sentinel on miss.

## 5. Why each mapping is zero-cognition

**OBSERVE.** The shim parses three ASCII integers and passes them to
`ev_observe`. It does not inspect what the integers denote. No branching
on values, no vocabulary checks, no family detection. The integer parse
(`parse_i32`) is a mechanical digit fold. This is transport, not
interpretation.

**QUERY.** The shim parses three ASCII integers and passes them to
`ev_query` with flags=0 (the standard mode used throughout the TNN-2
test battery). The returned integer is emitted verbatim, including the
-2 miss sentinel from TNN-2's trial-loop-first path. The shim does not
translate -2 into an answer, does not retry, does not consult the
expected value. This is transport, not reasoning.

**ACT.** The shim calls `ev_act(W)` and emits the returned integer.
Action selection happens inside TNN-2's 5-step ACT protocol. The shim
does not select, rank, filter, or reinterpret the result. The shim adds
no selection semantics of its own.

**What the shim does NOT do** (prereg section 2 prohibitions):
- Interpret world semantics: no branch conditions on s/r/o values.
- Reason: no inference, no chaining, no derived conclusions.
- Solve tasks: no goal state, no success metric, no planning.
- Inject task identities: no world labels, no family ids, no task prefixes
  reach TNN-2 (the event stream carries integers only).
- Construct cognitive structures: no node/edge allocation outside TNN-2's
  own functions; the shim allocates only parse scratch on the stack.
- Select policies: `ev_act` is TNN-2's policy selection, invoked opaquely.
- Translate failures into answers: -2 passes through unchanged; parse
  errors abort without state write.

**K-FZ2-3 verification.** Source inspection of `shim_driver2.zag` (the
only new code): 161 lines comprising argv handling, file I/O, line
splitting, whitespace skipping, ASCII integer parsing, three keyword
matchers (byte comparisons against OBSERVE/QUERY/ACT), the dispatch table
above, and output formatting. There is no conditional whose predicate
mentions a world id, vocabulary range, or semantic category. The
cognitive functions are byte-identical to frozen TNN-2 source
`a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd`
(first 1590 lines preserved verbatim by diff; only the test-suite
`main` at old line 1357 was removed, and the 161 driver lines appended).

## 6. Functional tests

- Basic: OBSERVE 10 1 42 then QUERY returns ANSWER 10 1 42; ACT emits CHOICE 0.
- Miss: unknown query emits ANSWER 99 9 -2 (sentinel passes through).
- State persistence: fact observed in run 1 retrieved in run 2 via the
  110656-byte state file.
- Determinism: 3/3 runs byte-identical output and byte-identical state files
  on a 4-event world.
- Parse error: `ERROR line 2`, exit 1, state file not written.
- Usage: wrong argc exits 2 with usage on stderr; missing world file
  exits 2; corrupt-length state file exits 2.

## 7. F-FZ2-1 assessment

F-FZ2-1 (shim requires cognition to function) is NOT triggered. The shim
was built without reference to sealed FW1-FW9 contents, against the
public INTERFACE.md only. No world-specific logic was needed. The three
event types map 1:1 onto TNN-2's pre-existing public functions. If a
future world required event types beyond OBSERVE/QUERY/ACT, extending the
shim would be a protocol change requiring prereg amendment, not silent
cognition.

## Verdict: SHIM-BUILD-PASS
