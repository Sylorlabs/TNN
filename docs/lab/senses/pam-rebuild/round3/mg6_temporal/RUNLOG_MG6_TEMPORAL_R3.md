# RUNLOG — MG6 Temporal-Arm Recalibration, Round 3 (Crew 2)

Date: 2026-09-24. Parent task: recalibrate or replace MG6's temporal arm; do not abandon the guard.

## Preregistration

Prereg-alone commit (no build output):
`9644a1cf44749da0f6aa8a53c6c01b939a4141ae`
Parent at commit time: `c78e3d2aafdb`.
Location: `docs/lab/senses/pam-rebuild/round3/mg6_temporal/`
Contents: PREREG_MG6_TEMPORAL_R3.md, gen_r3.py, EXPECT_R3.tsv (4,548 rows),
EXPECT_R3_CELL.tsv (4,548), EXPECT_R3_CC1.tsv (474), validated mirror + analysis scripts.

Predictions (Python mirror, validated 758/758 vs frozen D1 and 79/79 vs frozen CC1):
T0 0/0/34 CC1 0/9 5/5; T1 0/2/34; T2lo 1/2/34; T2hi 1/0/34; T3 0/1/34; T4 1/2/34 CC1 0/5.
Expected: all six KILL.

## Build

Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` (pinned).

### CC1 battery (src/r3_cc1.zag)
Adapted from frozen CC1 G1 (`guard_main.zag` @ dfe3d49f). Six candidates, per-cell
history/gate reset, output `R3CC1|cand|cell|trial_idx|disp`.
Built 2026-09-24 in 26 s. Binary: `src/r3_cc1` (not committed).

### D1 battery (src/r3_main.zag)
Adapted from frozen `stack_main.zag` (D1 round 2). Six candidates, fresh gate/history
per candidate, history seq arena added, output `R3|cand|stream|trial_idx|seq|disp|install|detail`.

Build note (not a prereg amendment): the verbatim 1.3 MB `r3_stack_records.zag`
(72,517 lines of `t_put64`/`fx[i]=` inits) does not compile in reasonable time
without zagd (foreground compile >15 min, still running; CC1's 34 KB records took
26 s). Generated `src/r3_records_compact.zag` via `gen_compact2.py`, which extracts
the raw bytes from the frozen records and emits them as Zag `\xNN` string literals
(`D1_<STREAM>_{TRIALS,FX,GATT}_DATA`). The DATA is byte-identical to frozen;
only the encoding changed. `r3_main.zag` uses the consts directly (trial/fx/gatt
tables are read-only; no init calls, no frees). Build time: 6.4 s.
Equivalence proven by 4,548/4,548 row match vs EXPECT_R3.tsv (generated from the
verbatim records) across three byte-identical runs.

T3/T4 history semantics: distinct-seq counting verified against EXPECT (frozen rows
use unique seqs; explicit de-dup not needed — mirror and Zag agree 4,548/4,548).

## Runs

All runs pure Zag, zero randomness, argv-selected stream (D1) / full output (CC1).

D1: `./run_d1.sh` — 16 streams × 3 runs, 4,548 lines/run.
- run1 sha256: b6dca78655a306e859a5b9d63302d4ef650d142461be90562229434f81a4f17b
- run2, run3: identical.
- vs EXPECT_R3.tsv: 4,548/4,548 match (all three runs).

CC1: `./r3_cc1` × 3, 474 lines/run.
- sha256 ×3: 97cd43de77f49eb7f9cac2e0a302911488177aca7268d908b0b8b203b4c9682b
- vs EXPECT_R3_CC1.tsv: 474/474 match (all three runs).

Scorer: `score_r3.py` (independent kill-bar recomputation from run output).

## Kill-bar results (from run1, independently recomputed)

| cand | KB-R3a false(D1) | KB-R3b retention | KB-R3c CC1(false,thr) | verdict |
|------|------------------|------------------|----------------------|---------|
| T0   | PASS (0)         | FAIL (0/34)      | PASS (0/9,5/5)       | KILL |
| T1   | PASS (0)         | FAIL (2/34)      | PASS (0/9,5/5)       | KILL |
| T2lo | FAIL (1, idx19)  | FAIL (2/34)      | PASS (0/9,5/5)       | KILL |
| T2hi | FAIL (1, idx19)  | FAIL (0/34)      | PASS (0/9,5/5)       | KILL |
| T3   | PASS (0)         | FAIL (1/34)      | PASS (0/9,5/5)       | KILL |
| T4   | FAIL (1, idx22)  | FAIL (2/34)      | FAIL (0/9,0/5)       | KILL |

All six KILL, exactly as preregistered. No retention recovery: best is 2/34 (T1,
T2lo, T4) vs the ≥26/34 bar. The margin arm is preserved (KB-R3c passes for
T0–T3); T4 breaks CC1 throughput (0/5) via false installs resetting gate state.

## Conclusion

The temporal arm is not the retention bottleneck. Only 4 of 34 true D1 candidates
reach the guard under G1; the complete stack retains 3/34 even with an allow-all
guard. No guard-only or temporal-only change can meet ≥26/34. Retention recovery
requires gate-level retuning of G1 proposal formation/re-anchoring (out of scope
for this crew; flagged for parent).
