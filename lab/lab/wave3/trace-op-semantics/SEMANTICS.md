# Trace Op Semantics — Investigation Verdict

**Slug:** `trace-op-semantics` · **Agent:** Wave-3 investigator · **Date:** 2026-09-19
**VERDICT: NEGATIVE — the true numeric op semantics are PROVEN UNRECOVERABLE from the repo.**

The 435 traces in the R27 artifact record opcodes, not implementations. After an
exhaustive search of the repo (all branches, full git history, all 208
non-R32/R33 docs, all 7 archive/transfer bundles, the artifact's own 121,094-node
object graph), no source, document, or data in `sylorlabs/TNN` defines the exact
numeric implementation of **any** of the 19 opcodes — including the 2 (`FILTER_GT`,
`MAP_MUL`) that the white-box suite runs against placeholder "lab-canonical v1"
semantics. Recovery requires the original R15-era source (see `RECOVERY_SPEC.md`).

## 1. New evidence this investigation produced

**Full opcode census** (sanctioned Python exception: inspecting the Python-origin
pickle `parent-r27-accepted-state.pkl`, blob `ceda86509a9e22db8783567f65e377ab860f13da`,
15,871,908 bytes — byte-count and content confirmed against the wave-1 record).
Previous record showed only one example (`FILTER_GT`, `MAP_MUL`); the true set is:

| Opcode | Uses | Params observed |
|---|---|---|
| `FILTER_GT` | 33 | `'PARAM'` ×26, `6` ×4, `3`, `4`, `7` |
| `MAP_MUL` | 31 | `2` ×24, `'PARAM'` ×5, `8` ×2 |
| `REVERSE` | 8 | None |
| `EXCLUDE` | 47 | None |
| `FILTER_EVEN` | 57 | None |
| `SUM` | 37 | None |
| `NEGATE` | 31 | None |
| `ORDER` | 27 | None |
| `TEMPORAL` | 29 | None |
| `SOURCE_WEIGHT` | 55 | None |
| `MAP_ADD` | 28 | `'PARAM'` |
| `COREFERENCE` | 35 | None |
| `CONDITIONAL` | 27 | None |
| `COUNT_EVEN` | 4 | None |
| `TRANSITIVE` | 29 | None |
| `ADD` | 32 | `'PARAM'` ×13, `4` ×5, `3` ×4, `2` ×4, `5` ×4, `1` ×2 |
| `SUMSQ` | 6 | None |
| `UNIQUE_SORT` | 7 | None |
| `MUL` | 29 | `'PARAM'` ×27, `9` ×2 |

Op-sequence lengths: 1 op ×327 traces, 2 ops ×99, 3 ops ×9. `verified=1` on all
435; `failures=0`. Anchors are English byte-spans (e.g. `b'than 3, then'`).

**Provenance split (new):** `SELF_VERIFIED` ×214, `OBSERVED_DEMO` ×188,
`SELF_VERIFIED_COMPOSITION` ×33. The wave-1 schema showed a single
`SELF_VERIFIED` example; 188 traces are demonstrations, not self-verified
learning — relevant to any future claim about what the trace set proves.

**Trace key union** is exactly `{cue, ops, support, sources, verified, failures,
age, provenance, anchors}` (+ unpickler bookkeeping). **No output/result field
exists.** The artifact stores no (input → output) pair for any op application.

**The `r15_master_training` module's full population** in the graph: 435 `Trace`
+ `MutableStudent` + `ProtectedSkillMemory` + `EntityEventGraph` + `FiberSearch`.
**No op-interpreter, op-registry, or op-table class exists anywhere in the graph.**

## 2. The unrecoverability argument (each point independently verified)

1. **The code never entered this repo's history.** All three branches
   (`main`, `tnn-native-lab`, `reorg/phase-0-1`) root at one commit:
   `5da88e0164` "Initial commit" 2026-08-25. The traces were produced by
   R15-era code at dev steps ≤ 60423, before the repo existed. GitHub code
   search and commit search for `FILTER_GT`, `MAP_MUL`, `r15_master_training`
   across the full history: **0 hits**.
2. **No documentation defines them.** All 208 Markdown files outside R32/R33
   were fetched and grepped: the only opcode mentions are the two example
   opcodes repeated in wave-1/wave-2 lab docs (citing the placeholder). The
   other 17 opcodes are not named anywhere. R27/R28 "TRACEABILITY" docs and
   the R31 jsonl trace logs concern the *causal-traceability* contract (H-10)
   — a different concept, verified by sampling.
3. **No bundle contains the source.** All 7 archive/transfer tarballs were
   listed and content-searched (`tnn-v1-current-execution`, `...evidence-fibers`,
   `R34_NATIVE_TRANSFER`, R27 shadow bundle): no `r*_experiments` or
   `r15_master_training` source. The `codex_restore_v62/v62.tar.xz.b64`
   staging blob is **0 bytes** (empty). (Consistent with DO_NOT_REPEAT §7:
   "the original source chain is unrecovered.")
4. **The artifact cannot self-describe the semantics.** No interpreter, no
   outputs, no I/O pairs — and `EpisodicConcept.answer` values are semantic
   labels (`'avoid_waking'`), not op outputs; `SurfaceOperationLearner` is a
   4096-dim sklearn linear probe (hyperparameters only, no exact function).
5. **The placeholder is underdetermined, not just unconfirmed.** "Lab-canonical
   v1" (FILTER_GT = strict `>` zero-fill; MAP_MUL = multiply) is one of
   several self-consistent conventions. Nothing in the repo disambiguates:
   `>` vs `>=` boundary; what `'PARAM'` resolves to (no param registry in the
   artifact); reduction output shapes for `SUM`/`SUMSQ`/`COUNT_EVEN`; axis
   semantics for `REVERSE`/`ORDER`/`UNIQUE_SORT`; the meaning of
   `EXCLUDE`/`CONDITIONAL`/`COREFERENCE`/`TRANSITIVE`/`TEMPORAL`/`SOURCE_WEIGHT`
   at all. The white-box suite's 11 trace-op checks therefore test the
   placeholder's *properties* (purity, determinism, order-sensitivity), not
   the artifact's true semantics — which is honest as documented, but the
   "lab-canonical v1" label must not be mistaken for recovered truth.

**Falsification note:** this verdict would be overturned by a single
counter-example — a repo object defining a numeric op implementation (source,
doc, or input/output pairs). The search above was designed to find exactly
that; its absence is the evidence.

## 3. Program-law compliance notes

- **Scale dimension.** No trial was run (NEGATIVE verdict — nothing to trial),
  so no scale-up was needed. The census algorithm itself is O(nodes) and was
  validated on the full 121,094-node graph. The recovery spec's acceptance
  trial states its scale argument explicitly: semantics table is O(opcodes);
  per-trace verification is O(traces × ops) — 10x/100x trace count is linear,
  no new mechanism required.
- **No RNG in the AI.** No system was built or modified; the census tooling is
  analysis-only and deterministic (sha256-verified artifact, fixed traversal).
  The recovery spec's acceptance trial is specified as fully deterministic:
  zero RNG in the interpreter or test harness — boundary cases are explicitly
  designed adversarial sequences (e.g. FILTER_GT at param ±ε), per the law's
  "designed curricula" requirement.
- **No banned mechanisms.** This investigation used no score tables, no
  RL reward-shaping, no random exploration. The opcode census is a static
  artifact analysis.

## 4. What this means for the white-box program

1. `WHITEBOX_TESTS.md` Group 1 remains valid **as a test of the placeholder**,
   but its documented assumption must be upgraded: it is not "2 of N opcodes
   with placeholder semantics" — it is 2 of **19** opcodes, and the other 17
   have no lab-canonical interpretation at all. Recommend relabeling v1 as
   explicitly provisional and noting the 19-opcode census.
2. `READER_BLOCKED_SPECS.md` §4 ("every Trace.provenance is 'SELF_VERIFIED'
   or a recorded alternative") is consistent with the census (214/188/33
   split) — no change needed, but the spec should cite the exact counts.
3. Any future claim of the form "the native reader reproduces R27 trace
   behavior" is **BLOCKED** until `RECOVERY_SPEC.md` is satisfied — there is
   no behavior to reproduce against without the original semantics.

## 5. Next step

Execute `RECOVERY_SPEC.md`: locate the original `r15_master_training` source
(off-repo: the pre-2026-08-25 development environment). Until then, treat all
19 opcodes as uninterpreted symbols and keep the white-box suite's Group 1
explicitly placeholder-scoped. Do **not** invent semantics for the other 17
opcodes to "complete" the table — an invented table is a banned mechanism
(score-table-as-intelligence by another name).
