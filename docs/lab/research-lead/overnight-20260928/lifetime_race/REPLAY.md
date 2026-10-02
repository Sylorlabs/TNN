# LLM Replay Interface (frozen)

This document freezes the interface by which a future capable external
runner may execute the serious LLM baseline on the identical
lifetime-race worlds. The LLM baseline is PENDING: no LLM has run this
benchmark. Nothing here may be used to estimate or imply LLM scores.

## Artifacts per world (in `worlds/w0`, `w1`, `w2`)

- `turns.jsonl`: the frozen turn script, one JSON object per line.
- `key.json`: scoring key and tool-resolution data.

## Turn protocol (identical for any contestant)

For each line of `turns.jsonl` in order, the runner presents the turn
to the contestant and records exactly one reply:

- `brief`: `{"ack":true}` expected; carries world id and seed hash.
- `obs`: ingest the `ev` object; reply `{"ack":true}`.
- `query`: reply `{"qid":"...","answer":"...","conf":0.0-1.0}`.
- `act`: the contestant may reply with one tool call
  `{"tool":"ask","q":"...","qid":"..."}` or
  `{"tool":"intervene","var":"P|Q|R","val":0|1,"qid":"..."}`,
  or `{"done":true}`. The runner resolves the tool, feeds a
  `toolresult` turn, and re-issues the same `act` turn until `done`
  or the budget (3) is exhausted.
- `toolresult`: carries the tool outcome in `result`; reply `{"ack":true}`.
- `save` / `load`: persist / verify checksum; reply includes the checksum.
- `end`: reply `{"done":true}`.

## Tool resolution rules (must be identical for every contestant)

- `ask` with `qid`: return the object stored under
  `key.json` -> `withheld` -> `qid`, wrapped as
  `{"turn":N,"kind":"toolresult","qid":"...","result":<object>}`.
  If the qid is absent, return `{"t":"none"}`.
- `intervene` with `var`, `val`: simulate the world's true causal graph
  (`key.json` -> `true_graph`: 0 = P->Q->R, 1 = P->R->Q, 2 = Q->P->R)
  from the current baseline. The baseline starts at (0,0,0) and updates
  on every `cobs` observation or intervention result. Propagation is
  copy-semantics in topological order with the intervened variable
  pinned. Return
  `{"t":"cobs","P":p,"Q":q,"R":r,"do":"<var>","val":<val>}`.

## Scoring

- `key.json` -> `queries` maps each qid to its expected answer string.
  Exact string match scores 1, otherwise 0.
- Queries `G1`, `G2` are marked `"DYNAMIC"`: the expected answer is
  computed by the runner by simulating the true graph from the baseline
  holding at query time (see `run_race.sh`).
- `key.json` -> `transfer` records the examples-to-criterion
  measurements (`T1`: 2 examples, `T2`: 1 example).

## Cost ledger (must be charged honestly for the LLM run)

Count every observation presented, every teaching example, every tool
call, every repeated context window (prompt tokens), wall time, peak
RAM of the harness process, and bytes of any persistent state the LLM
contestant keeps across turns. The TNN contestant's ledger fields are
defined in `RACE_PREREG.md`; the LLM run must report the same fields,
with prompt tokens counted in place of TNN state bytes where the
mechanism differs. No field may be omitted or estimated.

## Fairness constraints

- The LLM contestant receives exactly the turns in `turns.jsonl`, in
  order, with no additional information.
- It may use realistic notes, retrieval, tools, and persistent memory
  across turns, as the preregistration allows.
- It must not be given the contents of `key.json`.
- One replay per world; no tuning on the scored worlds.
