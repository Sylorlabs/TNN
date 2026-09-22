# PAST-RAM experiment — PREREG (frozen before results)

Date: 2026-09-22. Ordered directly by Micah. This is a measurement experiment
with one structural question; the method below is frozen before any new
measurement runs.

## Q1 (structural, answered by code inspection, already complete)

What is the long-term storage mechanism in the current learner?
Evidence (verified 2026-09-22, sources read, not guessed):
- `scale/fewshot/driver/fewshot_learner.zag` (the lineage behind the
  throughput instrument `ops/throughput/thru_learner.zag`): all KB state —
  slot chunks (`sc_store_init`, 4096 slots × 24 B), dense id→slot index
  (4 B/slot), audit ledger chunks (16384 records × 64 B, cap = 2×facts+8192
  records) — is allocated via `sc_alloc` → `_zag_malloc` = process heap (RAM).
- File I/O in the learner is READ-ONLY corpus loading (`sc_open_rdonly`,
  Gutenberg texts for harness truth derivation). Zero `write(2)` syscalls,
  zero `mmap`, zero `O_CREAT`/`O_WRONLY` in the learner/driver.
- No snapshot / save / persist / flush path exists anywhere in the
  learner or driver. On alloc failure `sc_store_init` returns -1 and the
  driver prints `store init failed` and exits cleanly.
- THROUGHPUT_REPORT.md (89 lines) contains no persistence mechanism.

Pre-registered structural verdict: **the long-term storage tier does not
exist in this learner lineage.** Micah's "long-term memory goes in storage"
is a design intent, not an implemented mechanism. Past RAM there is no tier
to engage — the process refuses cleanly and all knowledge dies with it.
The measurement below characterizes the RAM ceiling and the failure mode
empirically; it cannot measure a tier transition that has no implementation.

## Q2 (measurement): the RAM ceiling

Sweep KB size N upward under a fixed 1 GB virtual-memory cap and measure:

| N (facts) | 240K (anchor) | 1M | 2M | 4M | 6M | 8M |
|---|---|---|---|---|---|---|
| reps | 3 | 3 | 3 | 3 | 3 | 3 (or stop at first refusal) |

Per (N, rep): install path ns/fact on the process CPU clock
(`CLOCK_PROCESS_CPUTIME_ID`, same basis as the 6.2 µs/fact figure),
recall microbenchmark probes/sec, eval-sweep probes/sec, peak RSS of the
child (python `resource.ru_maxrss`), exit disposition, byte-identical
digest comparison across reps.

Instrument: rebuild `thru_learner.zag` from the committed source with the
pinned toolchain (`toolchain/bin/znc_linux_x86_64_abed8aa1 --no-analyze`).
Timing-only copy of proven machinery; no logic changes. The 240K anchor
must reproduce ~6.2 µs/fact before larger N are trusted.

Derived quantities: bytes/fact from the RSS-vs-N slope (kills the fixed
corpus-init offset); predicted ceiling for the full 8 GB box by
extrapolation; degradation curve of µs/fact vs N inside the cap.

Deliberation episodes/sec: measured on the dialogue instrument's 38-fact
KB only (unchanged workload); deliberation-KB scaling is out of scope and
recorded as untested follow-up, not silently extrapolated.

## Kill bars

- K1 (determinism): all reps at each successful N byte-identical. Any
  nondeterminism is a reported finding, not smoothed over.
- K2 (safety): no OOM-killer engagement, no disruption to other crews.
  Runs execute under `ulimit -v 1048576` (1 GB VSZ) and `nice -n 10`.
  Past-cap refusal must present as the clean `store init failed` exit.
  If the box OOM-kills anything, the experiment stops and that is the
  reported finding.
- K3 (honesty): the tier verdict above is reported plainly with code
  evidence. The knee is characterized as a RAM ceiling, never as a
  storage-tier transition.

## Safety / shared box

- Scratch: `~/workspace/tnn-lab/ops/throughput/past-ram/work/` only.
  NEVER `/tmp` (full 512 MB tmpfs). `TMPDIR=~/workspace/tmp_commit`.
- No binaries or `.zagd` committed. Commits via
  `~/workspace/commit_racefree.py` with lab-relative paths, verified via
  the GitHub API (`~/workspace/skills/github/bin/gh-api`).
- Target: `docs/lab/ops/throughput/past-ram/` on branch `tnn-native-lab`.
