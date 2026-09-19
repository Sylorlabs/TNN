# White-Box Test Suite (Agent D, wave 2)

**Status:** 43/43 checks pass on Linux x86-64 (2026-09-19). `WB_FAILURES,0`, exit 0.
**Rule:** every test compiles and runs on this VM. No aspirational tests.

## What this suite is

Executable Zag tests for negative specs N1–N10 from
`docs/lab/wave1/brain/STATE_SCHEMA.md` — but only the halves the native
substrate can prove *today*. Anything that needs a Zag-native reader for
`parent-r27-accepted-state.pkl` is a SPEC stub in `READER_BLOCKED_SPECS.md`,
not here. The split is deliberate: this file never claims more than the
binary in front of it proves.

## Layout

| File | Role |
|---|---|
| `~/workspace/tnn-lab/toolchain/r34v3/wb_whitebox_tests.zag` | the test program (lives next to the learner core so `@import` resolves) |
| `run_whitebox.sh` | runner: compiles, runs, counts `CL_CHECK` lines, runs the learner-core isolation static check, writes an evidence bundle |
| `WHITEBOX_TESTS.md` | this file |
| `READER_BLOCKED_SPECS.md` | precise assertions blocked on the native pickle reader |

Run it: `./run_whitebox.sh` (takes `ZNC` env var like the R34 runner).

## The test groups

### Group 1 — trace-op semantics (N4, native half) — 11 checks

Implements the two opcodes the R27 schema records (`FILTER_GT`, `MAP_MUL`)
and proves the white-box claim about them: **ops are pure symbolic functions
of (cue, opcode, param)**. No weights, no hidden state, no learned parameters
in the path.

- `trace_filter_gt_lo/boundary/hi` — basic semantics incl. strict `>` boundary.
- `trace_ops_data_dependent` — same op, different cue → different output.
- `trace_compose`, `trace_compose_zero_stays` — sequential application equals
  the composed op-sequence.
- `trace_order_matters`, `trace_order_b1/b2` — `F∘M ≠ M∘F` on a concrete
  vector: symbolic ordering, not a fused weight matrix.
- `trace_ops_deterministic`, `trace_ops_no_hidden_state` — repeatability and
  no cross-contamination between interleaved cues.

**Documented assumption:** the R27 artifact records opcodes but not their
exact numeric semantics. `FILTER_GT` = keep elements strictly greater than
param else zero; `MAP_MUL(k)` = multiply. This is the lab-canonical
interpretation v1. If the native reader later shows different semantics,
update the interpreter AND this doc — do not silently keep passing tests
against the wrong semantics.

### Group 2 — structural-revision decision logic (N3, native half) — 6 checks

Implements the lab-canonical revision rule v1 and verifies the implementation:
**PROMOTE iff candidate > base AND compute_mult ≤ 4.00× AND protected_ok.**
Accuracies in thousandths, multiplier in hundredths. The `protected_ok` gate
encodes the DO_NOT_REPEAT law *"aggregate gains never cancel pointwise
damage."*

- `rev_clear_improvement` (0.677→0.927, 2.95×) → PROMOTE — the schema's own example.
- `rev_regression`, `rev_expensive_weak` (8× for +0.05 — *"expensive weak
  candidates rejected"*), `rev_protected_regression`, `rev_equal_no_promote`
  → ROLLBACK.
- `rev_marginal_improvement` documents the rule's edge: strict `>` promotes.

These tests verify the rule's implementation, not the rule's wisdom. Changing
the rule is allowed — it requires updating the tests and recording why.

### Group 3 — lineage nesting invariant (N5, native half) — 4 checks

A synthetic 3-level lineage chain proving the *chaining logic*: steps
monotonic non-decreasing, each level's prior-link equals the previous level's
fingerprint, `restarts == 0` everywhere. Integer fingerprints stand in for
sha256 — the hash function is not what's under test. Negative cases
(broken link, regressed steps, a restart) are all caught.

### Group 4 — learner-core determinism + exact updates (N9/N2/N8, native) — 19 checks

Drives `r34v3_accept` directly with an explicit learn flag. This is the
strongest group: it proves what "no gradients" means *operationally* on the
native substrate.

- `learner_deterministic`, `learner_updates_count` — same seed + same update
  sequence → `r34v3_equal` (all 21 fields), exactly 10 updates.
- `rng_seed_sensitive` — the seeded RNG actually varies with seed (N9).
- `no_implicit_drift_updates/score/outcomes` — **with `learn=0`, two credit
  events change nothing but the outcome counter.** This is the native N2:
  there is no hidden gradient path; learning requires the explicit flag.
- `update_exact_score/count/updates`, `update_clamped` — with `learn=1` the
  rule is exactly `score += reward*100`, clamped to ±30000, counted once.
  Auditable to the integer.
- `encode_ok/decode_ok/roundtrip_equal/roundtrip_field_*` — the **entire
  learnable state is the 21 named i32 fields** of `R34V3State`; wire roundtrip
  preserves every one of them (native N8: no opaque state).
- `corrupt_refused` — a flipped byte decodes to `cl_corrupt()` (2005), never
  silently absorbed.

### Group 5 — promotion-ledger consistency (N10, native analog) — 3 checks

Synthetic ledger vs revision log: every ledger entry must name a revision-log
entry with a matching decision. Orphan entries and decision mismatches are
both caught. The artifact-level version (policy JSON ↔ 58-entry history) is
READER-BLOCKED.

## What's intentionally NOT here

- The R34 campaign's own checks (already proven by `run_native_linux.sh`).
- Anything asserting properties of `parent-r27-accepted-state.pkl` itself —
  see `READER_BLOCKED_SPECS.md`.
- The learner-core isolation rule (static grep in the runner, same as R34):
  the core must not import `world.zag`/`checkpoint.zag` or reference
  `cw_`/`CWOutcome`. Currently `learner_core_isolation=true`.

## For future agents

- Add checks by adding `cl_check` lines to a `wb_gN_*` function and calling it
  from `main`. Keep the `WB_FAILURES`/`CL_CHECK` output contract — the runner
  parses it.
- If you change a canonical rule (revision policy, op semantics), update the
  tests *and* the documented assumption in this file. A passing suite against
  stale semantics is worse than a failing one.
- `nio_alloc` is **not** zeroed — every buffer the tests rely on is
  explicitly initialized (see the `restarts` zeroing in group 3).
