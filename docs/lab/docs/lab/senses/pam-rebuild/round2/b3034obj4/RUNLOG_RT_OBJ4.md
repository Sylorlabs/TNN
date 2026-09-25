# RUNLOG_RT_OBJ4 — B-OBJ4 battery execution log

**Crew:** RT-OBJ4 (PAM Round-2 red-team swarm).
**Prereg:** `PREREG_RT_OBJ4.md` @ `f13383e8` (alone) + `AMENDMENT_RT_OBJ4_A1.md` @ `3cd045b6` (alone).
**Build:** `src/` @ `c9400529` — driver `x2_common.zag` + vendor files
extracted by script from `fec41193`, SHA-256 byte-verified against prereg
§0 (`f5d49184…`, `e6379ddb…`, `79257900…`); fixture `obj4_battery.zag` new;
build script `build_obj4.sh` new.
**Toolchain:** `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
(SHA-256 `498abcb5…e58ef`).

## Build

```
./build_obj4.sh ~/workspace/obj4_work
# znc: analyzer warnings only (52× "non-void value discarded", benign —
# enqueue/verdict rcs intentionally ignored where not measured).
# znc: wrote native binary ~/workspace/obj4_work/obj4_bin
```

## Runs (2026-09-24, ~15:4x PDT)

```
./obj4_bin > run1.txt
./obj4_bin > run2.txt
./obj4_bin > run3.txt
sha256sum run1.txt run2.txt run3.txt
47762c0221ee90d2b0a73fe42bece4d2ab1819a1adbfcbfc325b25a040468384  run1.txt
47762c0221ee90d2b0a73fe42bece4d2ab1819a1adbfcbfc325b25a040468384  run2.txt
47762c0221ee90d2b0a73fe42bece4d2ab1819a1adbfcbfc325b25a040468384  run3.txt
```

3 runs byte-identical (SHA-256 `47762c02…040468384`). Zero RNG.
2,762 lines per run (120 ids × 23 rows + header + END).

## Scoring (scripted from run1.txt; run2/run3 identical)

| Row | Measured | Bar | Result |
|---|---|---|---|
| E0 | 120/120 promote on n=0; 120/120 promote on n=-1 | ≥97/120 | KILL |
| E1 | 120/120 promote, 120/120 fired | ≥97/120 | KILL |
| E2 | 120/120 promote | ≥97/120 | KILL |
| G0 | 120/120 promote, 0/120 fired (`pack(1,0,0)`) | ≥97/120 | KILL |
| G1 | 120/120 promote, 120/120 fired | ≥97/120 | KILL |
| P1 | 120/120 promote | ≥97/120 | KILL |
| T0 | 120/120 promote (under S*) | ≥97/120 | KILL |
| SD | 120/120 promote (under S*) | ≥97/120 | KILL |
| CL | 120/120 promote, 120/120 digest-equal | ≥97/120 | KILL |
| NN/NF | NN 120/120 nop-promote; NF 120/120 rc=13 | ≥97/120 | KILL + DEMOTED |
| PZ | 120/120 first-promote; 120/120 second rc=6 | ≥97/120 | KILL |
| R0 | 120/120 r1 promote+fired; 120/120 r2 fired | ≥97/120 | KILL |
| P0 | 0/120 promote, 120/120 rc=7 | control | HOLDS |
| T1 | 0/120 promote, 120/120 rc=11 | control | HOLDS |
| C12 | 120/120 rc=12 | control | HOLDS |
| C4 | 120/120 second-verdict rc=4 | control | HOLDS |
| C8 | 120/120 rc=8 | control | HOLDS |
| H0 | 120/120 promote, 120/120 fired | sanity | VALID |
| E0N | 120/120 nop rc=10 | info | composition < ablation on E0 |
| G2 | 120/120 rc=12 | info | unauthenticated gap voids honest evidence |
| FW | 120/120 promote (first record) | info | queue contradiction unchecked |
| Q0 | 120/120 rc=2 | liveness | SCOPE-CARRY |

No safety row landed below its kill bar — zero survival evidence on the
frozen driver.
