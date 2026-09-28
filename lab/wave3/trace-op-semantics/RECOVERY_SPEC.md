# RECOVERY SPEC — what would disambiguate the 19 trace-op semantics

**Status:** the semantics are proven unrecoverable from `sylorlabs/TNN`
(see `SEMANTICS.md`). This document specifies exactly what evidence would
recover them, why no experiment on existing data can substitute, and the
acceptance trial for a recovered definition.

## 1. The missing artifact

The original R15-era source module that defined the op interpreter — nominally
`r15_master_training.py` (classes `Trace`, `MutableStudent`, `ProtectedSkillMemory`,
`EntityEventGraph`, `FiberSearch`), and any sibling `r*_experiments` module that
applied the ops. Provenance required: file content + authorship/date (the code
predates the repo's 2026-08-25 root commit, so it must come from the
pre-reorganization development environment, not from this repo's history).

The single 0-byte staging blob `archive/transfer-staging/codex_restore_v62/
v62.tar.xz.b64` is a lead worth checking off-repo (it may have been the
intended transfer vehicle), but as stored it is empty.

## 2. Why no experiment on existing repo data can substitute

A candidate semantics `f(opcode, cue, param) -> output` cannot be validated
against the R27 artifact because the artifact contains **no ground truth**:

- Traces store `(cue, ops)` but **no output vector** (key union verified
  complete over all 435 traces).
- `support`/`verified`/`failures` are scalars, not behavioral records.
- `anchors` are English text spans, not outputs.
- `EpisodicConcept.answer` values are semantic labels (`'avoid_waking'`), not
  op results.
- The 18 sklearn probes (incl. `SurfaceOperationLearner`) are linear
  classifiers — they cannot encode exact numeric functions.

Consequence: re-running a *guessed* semantics against the 435 stored cues
produces outputs with nothing to compare them to. The interpreter must come
from source (or from a contemporaneous doc/log recording op applications with
outputs — none exists in the repo).

## 3. The exact code that would disambiguate

For each of the 19 opcodes, the numeric function over a 512-dim float32 cue:

| Opcode | Must specify |
|---|---|
| `FILTER_GT` | `>` vs `>=`; value written on rejection (0? -inf? cue?); `'PARAM'` resolution rule |
| `MAP_MUL`, `MAP_ADD`, `MUL`, `ADD` | elementwise vs scalar; operand order; `'PARAM'` resolution; int params 1–9 semantics |
| `FILTER_EVEN`, `COUNT_EVEN` | parity of what — index, value, quantized value? `COUNT_EVEN` output shape |
| `SUM`, `SUMSQ` | reduction output shape (scalar? vector?); dtype |
| `NEGATE` | arithmetic negation vs logical; zero handling |
| `REVERSE`, `ORDER`, `UNIQUE_SORT` | axis; sort key and stability; `UNIQUE_SORT` dedup tolerance |
| `EXCLUDE`, `CONDITIONAL` | what is excluded / the condition's inputs (needs the second operand's source) |
| `COREFERENCE`, `TRANSITIVE`, `TEMPORAL` | these are relational — their non-cue inputs must be named |
| `SOURCE_WEIGHT` | weight source (the `sources` id registry — itself unresolved, schema §10.6) |

Plus: op-composition order semantics for 2- and 3-op sequences, and the
`'PARAM'`-binding rule (which params are symbolic vs literal across the 435
traces: `FILTER_GT` ×26, `MAP_ADD` ×28, `MUL` ×27, `ADD` ×13 symbolic).

## 4. Acceptance trial (preregistered, runs only after §1 is satisfied)

**Falsification criterion:** the recovered definitions are accepted iff a
native Zag interpreter implementing them byte-exactly reproduces a set of
explicitly-designed adversarial boundary cases derived from the definitions
themselves (e.g. FILTER_GT at param±ε, FILTER_EVEN on negative/zero cues,
3-op composition order-sensitivity) — AND the implementation's provenance
(source file + commit/author or transfer record) is recorded in the ledger.

**Program-law constraints on the trial:**
- **Deterministic end to end.** Zero RNG anywhere in the interpreter or the
  harness. Adversity comes from *designed* boundary sequences, not sampling.
  The verdict must distinguish "the interpreter is deterministic" from "the
  test was adversarial."
- **Scale dimension.** The semantics table is O(19 opcodes); per-trace
  verification is O(traces × ops). The trial runs the full 435-trace census
  scale natively and states the 10x/100x argument: 4,350 / 43,500 traces is
  linear time, constant memory per trace — no mechanism change at scale.
- **No banned mechanisms.** The interpreter is a pure function of
  (cue, opcode, param): no weights, no score accumulation, no learned
  parameters in the path (the property the white-box Group 1 checks already
  prove for the placeholder).

**Explicit non-goal:** the trial cannot validate recovered semantics *against
the R27 artifact* (no ground truth, §2). It validates faithful implementation
of the recovered source. Any claim stronger than that remains BLOCKED per
DO_NOT_REPEAT §7 (R27 behavioral continuity).
