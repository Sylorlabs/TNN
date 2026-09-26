# VERDICT.md — chunking battery fix (2026-09-26)

## Final scores

| Battery | Score | Determinism (2 runs) |
|---|---|---|
| 26-trap wall | **26/26** | SHA `cd86da4355b6e059ea829c63ca41de63e4d7d0a0fea84773d661c1827f1be24b` (identical) |
| 57Q production | **57/57** | SHA `170bacd71ba5f57c79be20786978964bbb094117e452b1a00d5289cbca351a23` (identical, unchanged since stage A) |
| Telemetry audit | 0 mismatches | 26/26 wall lines + 57/57 production lines |

No fallback. No regressions at any stage (production SHA never changed).

## Preregistration vs measured (every stage hit exactly)

| Stage | Fix | Preregistered | Measured |
|---|---|---|---|
| v0 baseline | — | 14/26 | 14/26 |
| A | ordinal + telemetry | 16/26 | 16/26 |
| B1 | relative addressing | 19/26 | (folded into B build) |
| B2 | target delimitation | 20/26 | (folded into B build) |
| B3 | two-hop | 21/26 | **21/26** |
| C0 | registry rewrite (no score change) | 21/26 | 21/26, byte-identical output |
| C1 | sentence/line granularity | 25/26 | **25/26** |
| C2 | nesting abstention | 26/26 | **26/26** |

57/57 production at every stage. Zero-regression requirement held.

## Failure → fix (per trap, with mechanism)

| Trap | Was | Now | Named mechanism |
|---|---|---|---|
| W00 sentence count | `""` (kind 0) | `2` | Registry granularity binding `sentences`→`.`, `gran_split`, kind 18/DELIM |
| W01 2nd sentence | `""` | `the dog ran` | Same; kind 19 selects 2nd trimmed segment |
| W02 line count | `""` | `3` | Binding `lines`→newline; newline is not a word separator in the old machinery |
| W03 two-hop | `?` | `x` | kind 21: registry relation `after`→+1 composed with registry ordinal `2nd` over first-token-delimited target `fox` |
| W04 word-after | `?` | `3` | Registry probe `word after <anchor>`; anchor = first `the`; next word `cheese`; e-count 3 (intended reading recorded in PREREG.md) |
| W05 word-before | `?` | `b` | Probe `word before fox` → `brown`; 1st letter |
| W06 reverse word-after | whole-text reverse | `nworb` | Probe resolves `brown`; kind-13 arm reverses the addressed word only (word-scoped reversal) |
| W07/W08 ordinals | `?` | pass | `parse_ordinal` reads registry (`second`→2, `third`→3) before digit fallback |
| W17 target delimitation | `?` | `h` | Structural: `zoom_locate` first-token fallback on the `of `-tail (`the in the quick brown the fox` → `the`); survives noseed |
| W18 nesting | `w` (wrong composition) | `?` | Structural: `count_sub(q," word of ")>=2` → kind 22 NESTED → withhold; survives noseed |
| W19 word of sentence | `""` | `cat` | kind 20: registry ordinal before granule name (`1st`) + outer `2nd` over `gran_split` segments |

## Noseed control (knowledge-dependence proof)

Seed emptied, everything else identical: wall **16/26**, production **57/57**.
10 traps need the seed (they fail in exactly the legacy ways: W04 → whole-text
"6", W03 → confident wrong "f"); W17/W18 survive (structural); the production
battery is knowledge-independent (digits only). Full detail in RUNLOG.md.

## Resistance remaining: none on these batteries

26/26 and 57/57 with zero fallback. The named next step is not a fix but the
agency gap in CONTROL_BOUNDARY.md: replace the crew seed with a live TNN
deliberation that places its own bindings through `tnn_bind_*`.

## Determinism & purity

Pure Zag, zero RNG. Every stage ran each battery twice with SHA-256 comparison;
all pairs byte-identical. Evidence (outputs, build logs, sources, SHA256SUMS)
under `evidence/stageA/`, `evidence/stageB/`, `evidence/stageC/`.
