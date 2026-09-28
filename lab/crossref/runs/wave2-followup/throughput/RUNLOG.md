# T2-THROUGHPUT quiet-VM rerun — RUNLOG (addendum to crew RUNLOG.md)

## Pins (frozen before running)
- Prereg: `sylorlabs/TNN@7b2100d09911c5c10252c5756c7def288e70bd1f`,
  `docs/lab/crossref/PREREG_TIER2.md` §T2-THROUGHPUT
  (blob `b1178370036bffbda6eb68ea0989c0e427dc31b7`, API-fetched 2026-09-24,
  saved as `logs/PREREG_TIER2_7b2100d0.md`, 38,417 bytes).
- Evidence commit: `67bf4c4cf81b9d1d5e1e4e150892843830ff8b2b`
  (resolves via API; recursive tree `logs/prereg_tree.json`).
- Instrument sources: git blob SHAs `c65b6d4c0f4539227540097772129c37c6978f51`
  (thru_learner.zag) and `776ce3c174e3383bf3897ee090b41de2570e7dc2`
  (dlg_thru.zag) — `git hash-object` on rerun sources matches both exactly.
- Instruments vs claimed sources @67bf4c4c: 55 changed lines each, all
  timing-only (verified against API-fetched blobs `964b2bc2bd9c186bbd7efab56f9e68a231eb2c8d`
  and `58d6a7a7cdb6f042e2a3e48f0c0dc84f62ce59d1`).
- Binaries: `src/dlg_thru_bin` (`345944f297c294f6d37a030a83e8ec6f4fb7fb7ca14fe03b4438c4956e211abc`),
  `src/thru_learner_bin` (`9fa0d63e727a5d24f6cfb9c10817abfd2baed02e7bd4ae51cae77f81b07a65e4`),
  matching `logs/bin_sha256.txt` (pinned-znc builds, rerun setup 15:08–15:10 UTC).
- znc: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
- Corpus: `~/workspace/scale/corpus/texts` (lab-local, not in git).
- No `/tmp` used for any scratch (512 MB tmpfs rule); no commit to sylorlabs/TNN.

## Quiet-window watch

`logs/quiet_watch.sh`: samples `/proc/loadavg` 1-min/5-min/15-min + nr every
60 s into `logs/load_trace.txt` (appends; `start` line written by the
predecessor's earlier instance at 2026-09-24T15:09:18Z), up to 60 samples;
writes `logs/window_marker.txt` with `QUIET_WINDOW <ts>` if 1-min load stays
< 5.0 for 3 consecutive samples, else `TIMEOUT <ts>` after 60 samples.

- Predecessor watch ran 15:09–15:36 (never quiet: 1-min load 10.4–16.3);
  restarted instance alive at handoff (PID 3060, started 15:39:13Z),
  appended `ts 1min 5min 15min nr` entries each minute.
- Watcher exit: **TIMEOUT 2026-09-24T16:39:24Z** (`logs/window_marker.txt`).
  Not a single sample < 5.0 in the entire 60-sample run (streak stayed 0/3
  throughout; see `logs/quiet_watch.txt`).

**Complete load trace:** `logs/load_trace.txt` — 88 samples, 15:09:18Z →
16:39:24Z.
Summary: 1-min load min **10.40** (15:14:18Z) / max **21.71** / mean 15.44;
**zero samples below 5.0**; no quiet window in 90 minutes of watching.
The VM never got quiet — the quiet-VM condition could not be met, so the
battery ran in the best sustained window available instead (see below).

## Wall-clock battery

Runlines (sequential, 3 reps, all from `rerun/`):
- dialogue: `cd rerun/dialogue && ../src/dlg_thru_bin` (3 reps;
  THRU_TURNS / THRU_EMIT wall lines; correctness + digest).
- learner: `./src/thru_learner_bin train N 24 M 3 <rep> ~/workspace/scale/corpus/texts`
  (N=240→M=10 and N=240000→M=10000, 3 reps each; recall wall µbench lines,
  install CPU anchors, SCALE_OPS/SCALE_MEM/SCALE_DIGEST).

Full per-run outputs: `logs/dlg_rep{1,2,3}.log`, `logs/learner_N240_rep{1,2,3}.log`,
`logs/learner_N240k_rep{1,2,3}.log`; per-run load before/during/after in
`logs/battery_runs.txt`; runner script `rerun/battery_wallclock.sh`.

**Incident (16:40Z):** two battery instances ran concurrently — the closer's
own launch plus a second instance (started ~2s earlier via a `chmod +x …
&& …/battery_wallclock.sh` command line, origin unknown; likely a leftover
from a predecessor session). Overlapping timestamps and interleaved
`battery_runs.txt` entries plus same-filename log races were detected
(~16:43Z). Both instances were killed, all contaminated outputs deleted
(`dlg_rep*.log`, `learner_N240*.log`, `learner_N240k*.log`,
`battery_runs.txt`), and the battery was re-run once, cleanly and
sequentially, 16:46:41Z–17:00:23Z. The final `logs/battery_runs.txt` is the
clean single run (9 runs, all rc=0, no overlaps).

**Battery results (clean run, 16:46:41Z–17:00:23Z):**

| Run | t0–t1 (UTC) | rc | load_before (1min) | load_after (1min) |
|---|---|---|---|---|
| dlg_rep1 | 16:46:41–16:46:42 | 0 | 13.43 | 13.43 |
| dlg_rep2 | 16:46:43–16:46:44 | 0 | 13.43 | 13.43 |
| dlg_rep3 | 16:46:44–16:46:45 | 0 | 14.11 | 14.11 |
| learner_N240_rep1 | 16:46:45–16:47:04 | 0 | 14.11 | 12.89 |
| learner_N240_rep2 | 16:47:04–16:47:30 | 0 | 12.89 | 15.63 |
| learner_N240_rep3 | 16:47:30–16:47:52 | 0 | 15.63 | 16.37 |
| learner_N240k_rep1 | 16:47:52–16:52:20 | 0 | 16.37 | 18.48 |
| learner_N240k_rep2 | 16:52:20–16:55:54 | 0 | 18.48 | 10.08 |
| learner_N240k_rep3 | 16:55:54–17:00:23 | 0 | 10.08 | 16.82 |

Raw THRU lines (all reps rc=0):

- dialogue THRU_TURNS (turns=370, chars_total=12133):
  rep1 ns_total=1229834128; rep2 ns_total=432974306; rep3 ns_total=427347618
- dialogue THRU_EMIT (emits=370):
  rep1 ns_total=177780002; rep2 ns_total=92342332; rep3 ns_total=85052857
- dialogue correctness: 370 PASS / 0 FAIL all reps; DIGEST
  `35aaae8ac1bbf764d1f710403a9302ad1f4f9b5327c9b13793cd90299834474b`
  identical across reps (prefix matches inherited `35aaae8a`)
- learner N=240 THRU_INSTALL ns_teach_cpu_total (3 passes):
  r1 1532631/1416045/1410071; r2 1471186/1512553/1494149; r3 1494013/1386175/1829845
- learner N=240k THRU_INSTALL ns_teach_cpu_total (3 passes):
  r1 1528039101/1437239309/1336641591; r2 1492332009/1433741865/1319036687;
  r3 1493238667/1444383734/1338862623
- learner THRU_RECALL (wall): N=240: r1 recalls=1999920 ns=1390389444,
  r2 ns=5164897516, r3 ns=4382505335; N=240k: r1 recalls=1920000
  ns=3692168365, r2 ns=983704399, r3 ns=3879324027
- learner SCALE_OPS (cumulative over P=3 passes): N=240 all reps
  add=240,verify=720,audit=723,find=720,total=2403,ops_per_fact_x1000=10012;
  N=240k all reps add=240000,verify=720000,audit=488192,find=720000,
  total=2168192,ops_per_fact_x1000=9034
- learner SCALE_MEM: N=240 total_bpf=220 (24+4+192); N=240k total_bpf=158
  (24+4+130)
- learner SCALE_DIGEST: `44a61309cf780de1` (N=240, all reps),
  `31377bd76faa81c1` (N=240k, all reps) — byte-identical to inherited

**P=1 verification (frozen METHOD.md workload, 17:12:47Z–17:14:04Z,**
**load 13.3–16.4):** the staged battery uses P=3 while the frozen METHOD.md
specifies P=1 ("the remembered figure is marginal per-fact"); the driver's
ops/mem counters accumulate over passes, so P=3 prints cumulative values
(above). Two single-rep P=1 runs verify the committed accounting on this
binary:
- `logs/learner_P1_N240_rep1.log`: SCALE_OPS add=240,verify=240,audit=241,
  find=240,total=961,ops_per_fact_x1000=**4004**; SCALE_MEM total_bpf=**92**
  (24+4+64); install CPU 1580453/240 = 6.585 µs/fact (in band);
  digest `44a61309cf780de1` ✓; recall 0.425M probes/s
- `logs/learner_P1_N240k_rep1.log`: SCALE_OPS total=960001,
  ops_per_fact_x1000=**4000**; SCALE_MEM total_bpf=**92**;
  install CPU 1449036792/240000 = 6.038 µs/fact (in band);
  digest `31377bd76faa81c1` ✓; recall 0.594M probes/s
- Per-run loads in `logs/p1_verify.txt` (rc=0 both).

Interpretation: the inherited 4.004 ops/fact / 92 B/fact exact are the P=1
per-pass accounting; the P=3 staged battery's 10.012/220 (N=240) and
9.034/158 (N=240k) are the same counters summed over three passes (audit
ledger cap truncates the N=240k audit count). No contradiction.

Derived anchors (see VERDICT.md for the band table): install CPU median
6.01 µs/fact over 8 runs (all in 5.58–6.82); recall median 0.456M (N=240) /
0.520M (N=240k) probes/s — below the 1–3.2M band but flat across 1000× N
(ratio 1.14); deliberation median 855 eps/s [301, 866] vs 2,640–3,960;
emission median 131K chars/s [68K, 143K] vs 342K–1.29M; end-to-end median
28.0K chars/s [9.9K, 28.4K] vs 87K–151K. Relative ordering preserved
(recall ≫ emission > end-to-end; deliberation slowest in its own unit):
contention-shifted band.
