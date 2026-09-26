# IMPORTANCE METER (arm M) — Manifest

2026-09-26. Micah-approved fork: "try out the non lowball able meter as a fork."
Pure Zag, zero randomness. All batteries run twice; run1/run2 byte-identical
(SHAs in VERDICT.md).

## Sources (self-contained fork of the arm-E deliberative-pricing sources)

| file | SHA-256 | lines | notes |
|---|---|---|---|
| strength_core.zag | 97355a37…c0857c01d | 1730 | + ST_PRICE_METER=6, ST_DELIB_METER=3, ST_M_* reason codes 21–30, `st_meter_*` policy section, `st_price_is_delib`, meter branch in `st_price`, generalized 122/P3 gates |
| strength_checker.zag | c572cbf7…88c | 443 | binding gates generalized to `st_price_is_delib`, ST_DELIB_METER accepted, recompute dispatches on record kind |
| meter_trial.zag | 49ab5a43…260dc12961 | 2302 | M mode + 28-probe attack battery + 10-history FRAMING battery + honest/stress |
| substrate/R33_NATIVE_SHA256_V2.zag | 9824f6db…7ca683bcf | — | build mirror (unchanged) |
| substrate/R33_NATIVE_IO_V1.zag | e6379ddb…296641e9f6 | — | build mirror (unchanged) |
| substrate/cl/common.zag | 8aec83cb…4386271aa6 | — | build mirror (unchanged) |

Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
Build: `znc meter_trial.zag -o meter_trial_bin` (binary NOT committed).

## Docs

| file | SHA-256 |
|---|---|
| DESIGN.md | 448f5293…b910e3b9e |
| VERDICT.md | 7bd5352c…c33f232d223 |
| MANIFEST.md | (this file) |

## Evidence (run1 + run2, byte-identical)

`evidence/run1_M_ATTACK.txt`, `run2_M_ATTACK.txt` — 28 probes, fail=0
`evidence/run1_M_FRAMING.txt`, `run2_M_FRAMING.txt` — 30 readings, fail=0
`evidence/run1_M_HONEST.txt`, `run2_M_HONEST.txt` — 386/0, histogram p1=386
`evidence/run1_M_S16.txt`, `run2_M_S16.txt` — stall n=30
`evidence/run1_M_S32.txt`, `run2_M_S32.txt` — stall n=46
`evidence/run1_E1_HONEST.txt` — comparator: 297/89, p1=221 p2=55 p3=55 p4=55
`evidence/run1_E1_ATTACK.txt` — comparator: 19 probes, fail=0

## Reproduce

```
znc meter_trial.zag -o meter_trial_bin
./meter_trial_bin M ATTACK    # expect M_ATTACK_TOTAL fail=0
./meter_trial_bin M FRAMING   # expect FRAMING_TOTAL fail=0
./meter_trial_bin M HONEST    # expect ok=386 abandons=0, M_PRICE_DHIST p1=386
./meter_trial_bin M STRESS S16 # expect stall n=30
./meter_trial_bin M STRESS S32 # expect stall n=46
./meter_trial_bin E1 HONEST   # comparator: ok=297 abandons=89
```
