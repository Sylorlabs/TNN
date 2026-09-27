# SWEEP5 — fork-gate margin sweep (2026-09-27)

**Method:** PREREG5 §8. Source patched ONLY at the two `margin<=12` constants (fork_assess) → `margin<=M`. M=12 binary is byte-identical to pinned (SHA 630586da...; V4 sweep-sanity PASS). Each M: onebrain + nov4 on v8 (20 items) and v7 (44 items), 2 reruns, all byte-identical.

**Binary SHAs:**
- M=8: 19aa0a1327e1edfba7265b59d3cbcd3fbf936f4122159f3f60cd10d94d86e114
- M=10: 8c8db42185436d1de5735fb8e74feae74f7c04808b3db68aa4b4d59f963fc8e8
- M=12: 630586da251f37bd72d60fd426fd7039142b81653a08a3527c892c21a42720fe (== pinned)
- M=14: bb3a7cf0a82f5d389c5078ff0089f1136993ca5e7a80138e9e2b7bd1fa02ad23
- M=16: c7bccc1138adf2bdec13594f8d59180da4c09a5817a32b8936fc002ae8fb1bbc

## v8 sweep (correct/20)

| M | onebrain | nov4 | delta (ob−nov4) | V4-affected items |
|---|---|---|---|---|
| 8 | 16 | 16 | 0 | 0 |
| 10 | 16 | 12 | +4 | 4 (E01–E04 help) |
| 12 | 10 | 12 | −2 | 10 (4 help + 6 harm) |
| 14 | 8 | 12 | −4 | 12 (4 help + 8 harm) |
| 16 | 8 | 12 | −4 | 12 |

## v7 sweep (correct/44)

| M | onebrain | nov4 | delta (ob−nov4) |
|---|---|---|---|
| 8 | 33 | 33 | 0 |
| 10 | 35 | 35 | 0 |
| 12 | 30 | 35 | −5 |
| 14 | 30 | 35 | −5 |
| 16 | 30 | 35 | −5 |

Only q01–q05 change on v7 (all flip at M=12; margin=12).

## Per-item flip points (v8)

| items | margin | flips ON at |
|---|---|---|
| E01–E04 (HELP) | 9 | M=10 |
| E05–E08, E17–E18 (HARM) | 11–12 | M=12 |
| E19 | 13 | M=14 (between 12 and 14) |
| E20 | 14 | M=14 |
| E09–E12, E13–E16 | 10 / 18–21 | never (duel-preempt / no fork) |

## H5e adjudication
- **CONFIRMED:** V4-affected item COUNT is monotonic in M (v8: 0→4→10→12→12). Each item's V4 effect turns on at M ≥ its margin, precisely.
- **FALSIFIED (as stated):** |onebrain−nov4| is NOT monotonic (v8: 0→4→2→4). The NET delta sign FLIPS (+4 at M=10 → −2 at M=12) because help-items (margin 9) turn on before harm-items (margins 10–14). The net is set by set composition, not by V4 — which is what H5e's qualifier predicted.
- **CONFIRMED:** At M=8, V4 effects shrink to zero on both sets. The margin gate is necessary and precise.
