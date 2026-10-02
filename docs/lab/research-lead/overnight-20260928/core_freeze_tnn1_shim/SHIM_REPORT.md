# CORE-FREEZE-TNN1 Driver Shim Report

Date: 2026-09-30. Builder: Core Freeze Driver Shim Builder.
Prereg: `60f1ff0bf` (CORE-FREEZE-TNN1-PREREG-FROZEN). K1 ordering verified.
Status: SHIM-BUILD-PASS.

## 1. Purpose

Transport FW world events into TNN-1's public interface and return
TNN-1 outputs/actions. The shim contains zero cognition per prereg
section 2 and kill bar K-FZ3.

## 2. Artifacts

- Source: `docs/lab/research-lead/overnight-20260928/core_freeze_tnn1_shim/freeze_shim.zag`
  SHA-256: `167f4fd3ba3febc5e260dc1c84c8cb7b6ae82cad634c64e41b498130609ce8f9`
  Lines: 1488 (1327 TNN-1 cognitive/test lines preserved + 161 driver lines)
- Binary: `docs/lab/research-lead/overnight-20260928/core_freeze_tnn1_shim/freeze_shim_bin`
  SHA-256: `9007e084e93b81cc508f6b5e73200080b70454e84201f0d3e7c3baa4f35c64e0`
  Size: 211K. Built with pinned compiler `src/tools/toolchain/znc_linux_x86_64_abed8aa1`.
- Driver-only source (for review): `shim_driver.zag` (161 lines, the added interface code).

## 3. Public protocol

Follows `core_freeze/stage0/INTERFACE.md` (the public world-event protocol
from the original freeze). Invocation:

```
freeze_shim_bin <world.txt> <state.bin>
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

State file: 110656 bytes (TNN-1 workspace size). Loaded if present and
exactly 110656 bytes; fresh `tnn1_init(W)` if absent; abort exit 2 if
corrupt length. Written after successful event stream.

Exit codes: 0 ok; 1 world parse error (state untouched); 2 usage or I/O error.

## 4. Interface mapping

| World event | TNN-1 call | Output | Return code |
|-------------|------------|--------|-------------|
| `OBSERVE s r o` | `ev_observe(W,s,r,o)` | `OBSERVED s r o` | 1 |
| `QUERY s r e` | `ev_query(W,s,r,e,0)` | `ANSWER s r v` | 2 |
| `ACT` | `ev_act(W)` | `CHOICE v` | 3 |
| blank line | (none) | (none) | 0 |
| other | (none) | `ERROR line <n>` | -1 |

## 5. Why each mapping is zero-cognition

**OBSERVE.** The shim parses three ASCII integers and passes them to
`ev_observe`. It does not inspect what the integers denote. No branching
on values, no vocabulary checks, no family detection. The integer parse
(`parse_i32`) is a mechanical digit fold. This is transport, not
interpretation.

**QUERY.** The shim parses three ASCII integers and passes them to
`ev_query` with flags=0 (the standard mode used throughout the TNN-1
test suite; flags=1 is a test-only masked mode). The returned integer is
emitted verbatim, including the -2 miss sentinel. The shim does not
translate -2 into an answer, does not retry, does not consult the
expected value. This is transport, not reasoning.

**ACT.** The shim calls `ev_act(W)` and emits the returned integer.
Action selection happens inside TNN-1's 5-step ACT protocol (bid
computation, directional eviction, supersession checks). The shim does
not select, rank, filter, or reinterpret the result. Emitting the real
`ev_act` value (rather than the original freeze's fixed `CHOICE 0`
placeholder) is correct because TNN-1 possesses the action-selection
machinery the original Stage 0 substrate lacked. The shim adds no
selection semantics of its own.

**What the shim does NOT do** (prereg section 2 prohibitions):
- Interpret world semantics: no branch conditions on s/r/o values.
- Reason: no inference, no chaining, no derived conclusions.
- Solve tasks: no goal state, no success metric, no planning.
- Inject task identities: no world labels, no family ids, no task prefixes
  reach TNN-1 (the event stream carries integers only).
- Construct cognitive structures: no node/edge allocation outside TNN-1's
  own functions; the shim allocates only parse scratch on the stack.
- Select policies: `ev_act` is TNN-1's policy selection, invoked opaquely.
- Translate failures into answers: -2 passes through unchanged; parse
  errors abort without state write.

**K-FZ3 verification.** Source inspection of `shim_driver.zag` (the only
new code): 161 lines comprising argv handling, file I/O, line splitting,
whitespace skipping, ASCII integer parsing, three keyword matchers
(byte comparisons against OBSERVE/QUERY/ACT), the dispatch table above,
and output formatting. There is no conditional whose predicate mentions
a world id, vocabulary range, or semantic category. The cognitive
functions are byte-identical to frozen TNN-1 source `d3895083c9f8...`
(lines 1-1093 and 1095-1328 preserved verbatim; only the test-suite
`main` at old line 1094 was replaced by the driver `main`).

## 6. Functional tests

- Basic: OBSERVE then QUERY returns the observed value; ACT emits CHOICE.
- State persistence: fact observed in run 1 retrieved in run 2 via the
  110656-byte state file.
- Determinism: 3/3 runs byte-identical on a 5-event world.
- Parse error: `ERROR line <n>`, exit 1, state file not written.
- Usage: wrong argc exits 2 with usage on stderr; missing world file
  exits 2.

## 7. F-FZ1 assessment

F-FZ1 (shim requires cognition to function) is NOT triggered. The shim
was built without reference to sealed FW1-FW9 contents, against the
public INTERFACE.md only. No world-specific logic was needed. The three
event types map 1:1 onto TNN-1's pre-existing public functions. If a
future world required event types beyond OBSERVE/QUERY/ACT, extending the
shim would be a protocol change requiring prereg amendment, not silent
cognition.

## Verdict: SHIM-BUILD-PASS
