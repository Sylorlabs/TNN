# Slice 12 — Verdict invariance across expression variants (Track 1, TNN wave11)

## 1. Slice
Architectural separation between the verdict pipeline and the expression pipeline for
Track 1: define the interface contract, enforce one-way data flow (verdict → expression),
and provide a checker that verifies verdict equality across expression variants of the
same (input, full state).

## 2. Falsifiable claim
For every (input, full logged internal state) pair, all expression variants (phrasing,
path, ordering, elaboration) emit a byte-identical verdict record and append
byte-identical ledger contents, where the expression layer is structurally incapable of
altering the verdict record. Falsified by one verified mismatch or one undetected
tamper probe.

## 3. Design
Invariant, one sentence: **the expression layer receives the verdict as a sealed,
read-only record, and no input to the expression layer — including adversarial prompts —
may change the verdict record or the ledger contents for a given (input, full state).**

Mechanism. Two pipelines, one gate:

1. **Verdict pipeline.** Deterministic core produces a `VerdictRecord`:
   `verdict` (closed enum: ACCEPT/REFUSE/HOLD/REVISE/...), `verdict_args` (canonicalized),
   `memory_ops` (kill/pin/promote list — these MUST NOT vary, per MA1 evidence),
   `integrity_decision` (refusal flags, per wave5/6 evidence), `state_clock`, `input_id`,
   `evidence_refs` (hashes of the hypotheses eliminated, per eliminative-logic design).
2. **Seal.** The verdict core's write capability is consumed at seal time (Zag: linear
   value, passed by value into `seal()`; the expression module is never granted a
   `&mut` to it and its import list excludes the verdict-write interface). Seal
   computes `digest = sha256(canonical_bytes(record))` and appends the record to the
   append-only audit ledger BEFORE any expression runs. Ledger position (`ledger_seq`)
   is written back into the sealed record.
3. **Expression pipeline.** Receives only `(sealed_record_copy, full_state, expression_mode)`.
   Mode selection is a deterministic function of lawful state —
   `mode = sha256(state_clock || context_id || focus_register) mod K` — never RNG (program
   law 1). Expression may vary phrasing, path, ordering, elaboration; its output is the
   render plus the sealed record attached (render + `verdict_digest` line), so the checker
   never parses prose to recover the verdict.
4. **VARIANT_EQ checker.** Test-only: an `expression_mode` override is accepted by the
   expression pipeline ONLY when the run is flagged `test_harness` (the flag is part of
   the input record and appears in the ledger, so no silent mode shopping). For each
   (input, state) cell the checker runs all K modes, replays from the logged state
   (byte-identical replay per program law 2), and asserts: identical `VerdictRecord`
   bytes, identical `digest`, identical `ledger_seq` payloads across modes.
5. **Tamper probes.** The checker additionally compiles/runs 5 adversarial expression
   variants: (a) prompt-injected "change the verdict", (b) renderer that rewrites a
   memory_op, (c) renderer that drops an integrity refusal, (d) renderer that edits
   `evidence_refs`, (e) renderer that emits a second ledger append. All must either fail
   to compile, trap at runtime, or leave the sealed record untouched (verdict digest in
   the output unchanged). Detection = output digest equals the sealed digest; anything
   else is a checker failure.

## 4. Kill bar
Preregistered, all must hold over ≥ 200 (input, state) pairs × K ≥ 4 expression modes,
each replayed from logged state:
- **K1 (equality):** 100% of cells show byte-identical VerdictRecord and ledger payload
  across all K modes. One verified mismatch kills the separation design.
- **K2 (tamper detection):** 5/5 adversarial probes detected (sealed digest preserved in
  output, or compile/run refusal). One undetected tamper kills it.
- **K3 (no backchannel):** static audit of the expression module's interface — zero
  imports of verdict-write symbols, zero `&mut` into verdict memory. Any backchannel
  kills it.
Firing any of K1–K3 kills this design; deliberate repair (program law 6) may propose a
new seal mechanism, not a relaxation of the bars.

## 5. Honesty notes
- Weakest point: what counts as "the verdict." Multi-part verdicts (verdict + args +
  memory ops) need canonicalization; a reordered-but-equivalent memory-op list must
  canonicalize identically or K1 misfires on a real implementation bug rather than a
  design bug. The canonicalizer is part of the design and needs its own unit tests.
- I am NOT claiming the verdict pipeline is correct — only invariant. A wrong-but-stable
  verdict passes this slice; correctness is other slices' job (eliminative logic,
  wave5/6 integrity battery).
- Implicit channel risk: the expression layer's render becomes future input, so today's
  phrasing can steer tomorrow's verdict. That is lawful state dependence (variation
  goal), not a violation — but the ledger must make the chain visible, and a future
  slice should test that expression drift cannot walk a verdict across a boundary.
- The test-mode override flag is a loaded gun: if production code ever accepts it, the
  anti-shopping rule collapses. Mitigation: the flag lives in the input record and the
  ledger, and the production gate rejects flagged runs; checker K3 covers this.
- Relies on committed evidence: append-only audit with exact replay (MA1, 58/58) and
  integrity-refusal stability (wave5/6, 137/137 checks, 1440/1440 trap-correct) —
  paths `docs/lab/wave1/`, `docs/lab/wave5/`, `docs/lab/wave6/` on branch tnn-native-lab.

## 6. Next build step
Build natively in Zag: the `VerdictRecord` seal (linear write-capability consumption +
ledger append before expression), 4 expression renderers (terse / verbose / reordered /
alternative-path) sharing one sealed input, and the VARIANT_EQ checker with the 5
tamper probes — then run the K1–K3 battery on 200 logged (input, state) pairs from the
RC3 100x corpus before any new state variables are added.
