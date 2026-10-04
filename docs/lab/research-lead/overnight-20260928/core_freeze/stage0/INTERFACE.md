# STAGE 0 WORLD INTERFACE SPECIFICATION

Date: 2026-09-30. Governs: world_learn.zag / world_learn_bin (Stage 0 readiness build).
Protocol: FREEZE_PROTOCOL.md section 3.1 (frozen at 66e3c3f38).

## Invocation

```
world_learn_bin <world.txt> <state.bin>
```

- `<world.txt>`: path to the world specification file (text, may be empty).
- `<state.bin>`: path to the learner state file.
  - If the file exists and is exactly 32768 bytes, it is loaded as the persistent learner state.
  - If it does not exist, a fresh initial state is used (32768 zero bytes; W[0..4]=0 tick, W[8..12]=0 foundation-evict flag, matching the legacy driver's init).
  - If it exists with any other length, the run aborts with exit code 2 and the file is left untouched.
- Exit codes: 0 ok; 1 world parse error (state file untouched); 2 usage or I/O error (diagnostic on stderr).

## World file format

Text, one event per line, integer ids only. No natural language, no task labels, no family identifiers.

```
OBSERVE <subj> <rel> <obj>
QUERY   <subj> <rel> <expected>
ACT
```

- Blank lines (including lines containing only spaces/tabs) are ignored.
- Fields are separated by spaces or tabs. Integers are optional-minus followed by 1+ ASCII digits.
- `OBSERVE s r o`: calls the existing cognitive driver `learn(W, s, r, o)`. Emits `OBSERVED s r o`.
- `QUERY s r e`: calls the existing cognitive driver `v=query(W, s, r, e)`. Emits `ANSWER s r v`. (The driver's not-found sentinel -2 passes through unchanged; that is existing cognitive semantics, not interface behavior.)
- `ACT`: emits `CHOICE 0`. This is a documented placeholder, not a handler: the current substrate has no generic action-selection machinery, so the driver emits the fixed default choice. Inventing selection semantics here would be cognitive machinery. W6/W7 are predicted to expose this boundary (protocol 8.4, 8.6).
- Any other line is a parse error: the binary emits `ERROR line <n>` on stdout, exits 1, and does not write the state file.

## Output format (fixed, stdout)

```
WORLD_BEGIN
OBSERVED <s> <r> <o>     (one per OBSERVE event)
ANSWER <s> <r> <v>       (one per QUERY event)
CHOICE 0                 (one per ACT event)
WORLD_END events=<n> answers=<q>
STATE_SAVED
```

Event order in the output matches event order in the world file. On a parse error, output is `WORLD_BEGIN`, the per-event lines so far, `ERROR line <n>`, and no `STATE_SAVED`.

## State persistence

After a successful event stream, the full 32768-byte W is written to `<state.bin>`. The state file therefore carries the learner from one world (one process invocation) to the next. Parse buffers, the file-read buffer, and the transient load buffer are process-local and never reach the state file (see REGIONS.md for the scratch discipline).

## What the interface does NOT do

- No semantic cases: no line of the interface branches on world content, vocabulary, or family.
- No modes: no flag changes behavior; there is exactly one code path.
- No handlers: ACT/QUERY/OBSERVE map 1:1 onto pre-existing driver calls (learn, query) or a fixed default emission.
- No cognitive machinery: all cognition above the interface marker is byte-identical to dc20745db (see STAGE0_RESULT.md, K1 evidence).
