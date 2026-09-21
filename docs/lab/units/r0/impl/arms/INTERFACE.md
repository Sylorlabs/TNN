# R0 ARMS — probe interface

**Status:** fallback interface defined by the ARMS crew. Crew CORE's interface
(`r0/impl/core/API.md`) was absent as of 2026-09-21; arms are built against the
recovered R31 mechanism and will adapt when the CORE API lands. Adaptation hook:
the binary already multiplexes all arms behind `argv[1]`; a harness-mode entry
point can be added without touching arm logic.

## Invocation

```
arms <selector> [perturb1|perturb2|perturb3] < input-bytes > segmentation.txt
```

Selectors (11):

| selector | family |
|---|---|
| `predictive_surprise` | thesis arm: 82nd-percentile transition-surprise cuts, 256-entry inventory |
| `fixed_window_4` / `_8` / `_16` / `_64` | aligned fixed windows |
| `adaptive_mdl` | deterministic MDL chunker |
| `grounded_adaptive_mdl` | MDL + grounding term (native adaptation, see ARM_SPEC.md) |
| `hierarchical_mdl` | MDL base + 96 pair merges |
| `raw_micro` | no-chunking control (one chunk per byte) |
| `random_chunks` | **DETERMINISTIC-ANALOG** — fixed hash-of-position tiling, informational only |

The optional second argument runs a deterministic heap-shape perturbation
before processing (M8 smoke only — never an AI decision path):
`perturb1` = ascending allocs freed in order; `perturb2` = fixed-pattern sizes
freed in reverse; `perturb3` = interleaved alloc/free. Output must be
byte-identical with and without perturbation.

## Wire format

stdin: raw byte stream. Cap 16 MiB (under the 2^25 slice-index toolchain wall);
longer input → deterministic `ERROR` + nonzero exit (never silent truncation).

stdout (all fields decimal, space-separated, LF-terminated):

```
ARMS v=1 arm=<selector> n=<input bytes>
[META deterministic-analog hash-rule=v1 no-rng-in-decision-path informational-only]   # random_chunks only
SEG <start> <len> <id> <kind>
...
END chunks=<k>
```

`kind`: `s` surprise-inventory · `l` surprise-literal · `f` fixed-window ·
`m` mdl-motif · `h` hierarchical-merge · `r` raw/literal byte · `x` random-analog.

ID rules (deterministic, see ARM_SPEC.md):
- `s`: inventory rank 0..255 by (count desc, bytes asc)
- `l`, `x`, `f`: `fnv1a64(span) mod 1000003`
- `m`: motif rank 0..255 by (score desc, len desc, count desc, bytes asc)
- `h`: merge rank 0..95 by (gain desc, count desc, key asc)
- `r`: byte value 0..255

Guarantees: output is a pure function of (selector, stdin bytes). No
timestamps, no addresses, no RNG, no clock/entropy reads (canary-audited in
`run_smoke.sh`). Segments tile `[0, n)` exactly — verified by the smoke
round-trip check. stderr is empty on success.

## Determinism notes for the harness crew

- FNV-1a 64 is the only hash; all ordering tie-breaks are total
  (count/score, then raw bytes ascending) — no iteration over hash-table probe
  order ever influences output.
- Surprise threshold: lower-method 18th percentile of transition probabilities
  over distinct observed transitions (integer-faithful image of the reference's
  82nd-percentile surprise rule under surprise = −log p).
- MDL enumeration table is 2^20 slots; if it fills, further new spans are
  ignored (deterministic; logged nowhere — counts for resident spans still
  update). Corpus-scale runs should watch for this.
- Grounded-MDL grounding histograms are computed for the top 8192 candidates
  by savings (documented cap); below that it is exact.

## Relation to `r0/impl/core/API.md`

The core API (landed after this interface was written) defines a **library**
contract for the R0 endogenous chunker (`r0_core.zag`, `@import`-based,
`[]i32` arena + `seq:[]i32` inputs). It does **not** define a tournament-arm
invocation protocol. The arms in this directory are standalone tournament
cut-signal binaries, not core clients, so no adaptation was needed: this
stdin/stdout contract stands as the arms' harness interface. If a future
harness wants the arms as in-process library calls, that would be a new
interface, not a modification of either existing one.

Cross-crew observation (not acted on here — core crew's call): the core API
specifies its arena as a `[]i32` array with multi-word stores; the EXPLORE
crew independently re-derived compiler bug ZNC-2026-09-19-001 (3+ sequential
i32/i64 stores corrupt; `[]u8` stores reliable). The core's `[]i32` arena
falls in the bug's described blast radius (`[]i32`/`[]i64` multi-store
contexts) and should be audited or probed by the core crew.
