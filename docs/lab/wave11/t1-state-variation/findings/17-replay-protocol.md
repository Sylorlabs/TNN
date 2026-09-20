# 17 — Full-state logging format for "same full state → byte-identical output"

## 1. Slice
Specify the full-state logging format and replay procedure that makes Micah's variation
goal (output = f(input, FULL internal state)) checkable byte-for-byte under Track 1.

## 2. Falsifiable claim
If the per-episode state record defined in §3 is complete, then for any episode E,
replaying `input_E + state_E` on a conformant build produces output byte-identical to
the original run's output, across 1000 replay trials (100 episodes × 10 replays, two
build hashes); any single mismatch falsifies the logging format's completeness (see §5).

## 3. Design

### 3.1 What is serialized per episode (the state record `STATE_E`)
- `episode_seq`: u64 logical clock (never wall-clock; see determinism checklist §4).
- `mem_hash`: SHA-256 of the full memory store — each slot's (key, value, strength,
  pinned flag, kill status) in slot order. CORE slots included; killed slots recorded
  as tombstones, not omitted. (Zag already has SHA-256 in `R33_NATIVE_SHA256_V2.zag`.)
- `audit_head`: SHA-256 of the audit ledger prefix through episode end; audit entries
  keep the canonical 16-word layout (op@0, slot@4, rc@8, b1..b5@12..28, a1..a5@32..48,
  stage@52, d1@56, d2@60). The audit ledger itself is replayable to exact state
  (MA1, docs/lab/wave5/ma1-evidence.md).
- `clock_vector`: all deliberation/logical clocks the episode touched (hypothesis
  epoch, consolidation epoch, phase-transition gate epoch) — wall-clock excluded by law.
- `budget_counters`: remaining expression budget, deliberation step budget,
  variation-slot counter (how many MAY-vary choices were already taken this episode).
- `load_metric`: the builder-defined integer load signal the variation layer reads
  (e.g. pending-hypothesis count), serialized as i64 — never as a float timing delta.
- `variation_choices`: the log of every MAY-vary decision taken this episode:
  (choice_id, chosen_value) pairs, where values come from the deterministic selection
  rule (see §3.3), not from RNG.
- `constitution_ref`: hash of the ledger/gate rule set (guards against the
  lying-self-change RC1 pattern: state replayed under different rules must be caught).

### 3.2 Canonical encoding (byte-exact)
- Fixed-width little-endian fields, 8-byte aligned; no pointers, no heap addresses,
  no map-iteration order (all collections serialized in slot/index order).
- Variable-length fields (variation choice log) are length-prefixed with u64 count.
- No timestamps, no PID, no ASLR-dependent values, no allocation order anywhere in
  the serialized bytes. Floats forbidden in the state record (i64/fixed-point only).
- Single canonical schema version byte; decoder rejects unknown versions.

### 3.3 Replay procedure
1. Original run logs `input_E` (raw bytes) and `STATE_E` after every episode.
2. Replay loads `STATE_E`, rebuilds memory/audit from ledger replay (not from the
   hash — the hash is only the check), sets clocks/counters to the logged values.
3. Feed `input_E`; run the same build; capture output bytes.
4. Compare SHA-256(output_replay) to SHA-256(output_original): PASS iff identical.
5. Cross-check: rebuild state from replayed ledger and re-hash; state hash must match
   `mem_hash`/`audit_head` — catches logging bugs that corrupt the record silently.

### 3.4 Determinism checklist for the builder
- [ ] No `rdtsc`, no wall-clock, no thread scheduling, no address-dependent hashing.
- [ ] All choice among tied candidates resolves via the variation layer reading
  `STATE_E` only (slot index, load metric, budget counter) — identical state
  forces identical choice.
- [ ] Variation-slot counter bounds variation: variation choices beyond the budget
  fall back to the canonical (zero-variation) path, logged as such.
- [ ] All 1000 replay trials run on two build hashes; mismatch on either is a kill.

## 4. Kill bar
KILL the protocol claim if: any replay mismatch in the 1000-trial suite (100 episodes
× 10 replays) after fixing diagnosed logging bugs, OR if a mismatch's root cause is a
nondeterministic op in the build (Class B, §5) rather than a logging gap — that kills
the *build*, not just the format, and halts variation work until the op is removed.
Passing bar: 1000/1000 byte-identical, both build hashes.

## 5. Honesty notes
Replay-mismatch failure taxonomy:
- **Class A — missing variable**: state record incomplete (e.g. a deliberation clock
  not logged). Implication: extend the schema; the format was wrong, the build may be fine.
- **Class B — nondeterministic op**: wall-clock, thread race, address-ordered map,
  unseeded hash iteration. Implication: the build violates program law 1; fix the op.
- **Class C — logging bug**: record serialized with wrong layout, truncated, or
  written after mutation. Implication: fix the logger; caught by the §3.3 step-5
  re-hash cross-check.
- **Class D — rule drift**: constitution hash differs between run and replay.
  Implication: RC1-style self-change detected; replay must fail closed (refuse), not
  silently diverge — divergence here is evidence of tampering, not variation.
Weakest point: the format cannot log what the builder doesn't know is state — Class A
errors are only found by failed replays, so the protocol is only as good as the
mismatch-driven audit loop. I am NOT claiming replay proves variation is lawful:
replay proves *reproducibility*; lawfulness of variation (MAY/MUST-NOT boundary) needs
the preregistered verdict-invariance checks from the adjacent slices.

## 6. Next build step
Build the minimal conformance harness first: a 20-episode synthetic run on a stub-free
minimal TNN core with a known MAY-vary choice point, logging per §3, then run the
§3.3 replay procedure and classify every mismatch into the §5 taxonomy — this yields
the first measured Class A/C inventory before any real variation design is frozen.
