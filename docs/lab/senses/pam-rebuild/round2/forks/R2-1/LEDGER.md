# LEDGER.md — R2-1 Build and Run Log

## Hypothesis
HC-1 — Executable out-of-span warrant (P3+P9). Frozen 2026-09-23.

## Suite construction

### Frozen counts (from harness)
- Normal: 740 = 370 primary + 370 noise.
  - Per task: colordisc 60+60, colorconst 40+40, shapetrans 90+90,
    pitchdisc 60+60, timbredisc 60+60, motiondir 60+60.
- Adversarial: 185 (no family labels; treated as separate stratum).

### Generated counts (frozen-corrected)
- Normal: 4,260 total.
  - colordisc 939, colorconst 626, shapetrans 1091,
    pitchdisc 586, timbredisc 586, motiondir 432.
  - Derived: prereg per-task ratios (1080,720,1296,720,720,564) scaled
    to sum 5000, minus frozen per task.
- Adversarial: 4,815 total across 18 families.
  - Prereg family counts scaled by 4815/5815.
  - COL-1:331, COL-2:290, COL-3:331, CCN-1:282, CCN-2:282,
    SHP-1:331, SHP-2:373, SHP-3:248, PTC-1:290, PTC-2:331, PTC-3:331,
    TMB-1:207, TMB-2:207, TMB-3:157, MOT-1:290, MOT-2:290, MOT-3:244.

### Total
10,000 trials = 4,260 gen_normal + 4,815 gen_adv + 740 frozen_normal + 185 frozen_adv.

### Generation log
- `evidence/gen_r2a_v2.log`: 9,075 generated R2A fixtures.
- `evidence/convert_frozen.log`: 925 frozen converted to R2A.
  - Normal: paired primary/noise as F/G (disjoint noise realizations).
  - Adversarial: F=G (documented limitation; no disjoint span in harness).
- `evidence/trial_index.csv`: 10,000 trials, deterministic order (sorted by fixture_id).
- `suite/MANIFEST.sha256`: 20,000 entries (SHA-256 of every scored .r2a and .truth).

### Naming
- `r21n_<task>_<i>`: generated normal.
- `r21a_<task>_<i>`: generated adversarial.
- `r21f_<task>_<i>`: frozen-derived (i<740 normal, i>=740 adversarial).
- Unique prefix avoids collision with sibling crews' shared-dir files.

## Binary
- `src/sense.zag`: pure-Zag implementation.
- Compiler: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
- Binary: `sense_bin` (117,976 bytes). **Must be deleted before commit.**
- CLI: `sense <fixture.r2a> <full|ablated> <prev_hash> <trial_idx> <fixture_id>`.
- Determinism verified: byte-identical outputs on repeated runs.

## Battery
- `evidence/battery_run1/`: run1 outputs.
  - `full_results.csv`: 10,000 trials, full contract.
  - `ablated_results.csv`: 10,000 trials, T2 skipped.
  - `full_chain.txt`, `ablated_chain.txt`: hash chains.
- Run1 completed 2026-09-23. A service restart killed the initial workers;
  they were resumed from the chain file (19 trials re-filled, chain hashes verified).
- B6 (3 byte-identical runs) not completed; hypothesis died first.

## Results
See `VERDICT_R2-1.md`.

- Kill 1: 19.91% false installs (FAIL, threshold 2%).
- Kill 2: 95.36% recall (PASS, threshold 80%).
- Kill 3: 1.37× ablation ratio (FAIL, threshold 5×).
- B1: 64.05% (PASS, threshold 60%).
- B4: 35.58% changed, reduces=True (PASS).
- B5: 15.62% adv false-install (FAIL, threshold 2%).

## Files
- `src/sense.zag`: pipeline.
- `src/r2a_gen.py`: generator (frozen-corrected counts).
- `src/convert_frozen.py`: harness→R2A conversion.
- `src/build_index.py`: trial index + manifest.
- `src/run_battery.py`: battery runner (with resume).
- `src/score_battery.py`: B1-B7 scoring.
- `src/verify_ledger.py`: ledger verification (partial).
- `suite/`: 10,000 fixtures + MANIFEST.sha256.
- `evidence/`: logs, trial index, battery outputs.
- `VERDICT_R2-1.md`: verdict.
- `LEDGER.md`: this file.
