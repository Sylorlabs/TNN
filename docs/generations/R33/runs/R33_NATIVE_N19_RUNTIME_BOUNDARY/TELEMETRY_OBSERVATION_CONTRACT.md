# N19 execution-level telemetry observation contract

The 15-column wire shape is already fixed by `TELEMETRY_SCHEMA.json`. This
document fixes where execution values must come from.

For every emitted case row:

- `status` and `detail` come from the returned case result;
- `bytes_attempted` increments from actual write/read requests issued by the
  case, not from the fixture's intended record size;
- `bytes_committed` increments only after complete write plus the required
  durability barrier succeeds;
- `sequence`, `event_count`, `audit_head`, and `recovery_state` come from the
  final live/recovered journal state;
- `resource_limit` is the configured case bound;
- `resource_observed` is an independently observed runtime value or the fixed
  missing sentinel;
- `stdout_bytes`/`stderr_bytes` are observed capture sizes or the missing
  sentinel when capture is outside the bounded child.

A failure path must not emit a planned byte count as committed. The current
compile-only source's fixed `64,64` recovery dispatch is therefore a known
implementation item to replace before qualification execution.

The executed known-answer fixture must serialize at least one success, one
pre-I/O refusal, one partial/failed-I/O path, and one fresh-process recovery
row and compare every field against independently authored expectations.
