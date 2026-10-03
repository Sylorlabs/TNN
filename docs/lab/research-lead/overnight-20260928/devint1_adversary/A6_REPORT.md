# Attack A6 Report: Restart Persistence across Process Death

Worker: DEVINT1 adversary, Worker C (attacks A5 + A6).
Date: 2026-09-30.
Target: DEVINT1, builder commit `476c24b3d`, prereg `4b50ff7d4`.
Frozen criteria: `PREREG_ADVERSARY.md` (commit `60701a55f`).
Toolchain: `znc 2026.07.0-dev (edition 2026)`, `--no-analyze`
(analyzer lints only, no code change).

## Verdict: ATTACK-FAILS

Persistence is real. Reload checksum matches 3/3, and S10/S11 numbers
are byte-identical to the single-process baseline.

## Construction

Two binaries, true process death between phases (separate OS processes,
no shared memory):

- `adv_restart.zag` (phase 1): builder machinery (lines 1..825)
  byte-verbatim, S1..S9 main body (builder lines 829..1017)
  byte-verbatim, then serializes the full 16384-byte W buffer verbatim
  to `STATE.BIN`, prints byte count + checksum, exits 0.
- `adv_restart2.zag` (phase 2): same machinery byte-verbatim, allocates
  a fresh zeroed W, reads `STATE.BIN` back in full, verifies byte count
  (16384) and a whole-buffer checksum against the expected value passed
  on argv, then runs the S10 and S11 blocks (builder lines 1018..1057)
  byte-verbatim. Verbatim claims checked with `diff` pre-commit.

Serialization is a byte dump of the entire W buffer: concepts, rules,
lexicon, pairings, tick, eviction counters, SNAP twins, S3_CTRL,
SPLIT_CAND scratch, DP area. No researcher-visible restructuring of the
learner; the learner code is untouched. The only state outside W is
fresh stack/heap scratch (`tot`/`ptot`/`rtot` counters, loop vars),
re-created per phase and carrying no cross-phase information.

File I/O uses `_zag_raw_syscall` (Linux open=2 / write=1 / read=0 /
close=3), same pattern as the committed `sem_l3/sem_world.zag`;
argv via `_zag_arg(1)`, decimal-parsed with a leading-digits parser.
`STATE.BIN` is a runtime artifact in the run directory, not committed.

## Runs

3 full restart cycles. Each cycle: phase 1 runs (creates `STATE.BIN`),
checksum extracted from its stdout, phase 2 runs as a new process with
that checksum on argv. Exit 0 every phase, zero stderr bytes.

- Phase 1 (3/3): `PH1-BYTES 16384`, `PH1-BUFCHECKSUM 812532763`
  (stable across runs), `PH1-DONE`. S1..S9 output byte-identical to the
  builder baseline (ends `STATE-CONT 9 8 17 65 888166382`).
- Phase 2 (3/3): `PH2-BYTES 16384`, `PH2-BUFCHECKSUM 812532763`,
  `PH2-EXPECT 812532763`, `PH2-STATE-ACCEPT`, `PH2-DONE`.

Phase-2 S10/S11 lines vs committed single-process baseline
(`devint_worker1/DEVINT1_RAW.txt`), all 3 runs:

| line | phase 2 (restart) | baseline |
|---|---|---|
| S10-EVICT | treat=17 ctrl=18 | treat=17 ctrl=18 |
| S10-PROBE | treat=8/12 ctrl=0/12 | treat=8/12 ctrl=0/12 |
| STATE-CONT 10 | 14 20 110 173048152 | 14 20 110 173048152 |
| S11-RECOG | 17/17 | 17/17 |
| S11-PROC-REUSE | 3/3 | 3/3 |
| S3METRIC-REFINE | treat=1 ctrl=0 | treat=1 ctrl=0 |
| STATE-CONT 11 | 13 20 127 837285928 | 13 20 127 837285928 |

Byte-identical. Raw: `A6_RAW.txt` (phase 1 + phase 2 of cycle 1).

## Grading against frozen criteria

- ATTACK-SUCCEEDS required: checksum mismatch on reload, S10/S11
  divergence from baseline, or serialization needing
  researcher-visible restructuring. None occurred: reload checksum
  matched 3/3, all S10/S11 numbers identical to baseline, and the
  serialization is a verbatim buffer dump with no learner changes.
- **ATTACK-FAILS.** The persistent learner's gains live in the
  serialized W buffer; process death does not lose them.

## Notes

- Phase 2 intentionally omits the builder's final verdict block: the
  verdict's inputs (formed3, nt, nev, ...) are S1..S9 experimenter
  metrics, not W state, and the frozen A6 comparison is the S10/S11
  numbers only. This is a presentation choice, not a state gap: every
  byte the S10/S11 code reads is restored from `STATE.BIN`.
- Negative control available on demand: passing a wrong checksum on
  argv yields `PH2-STATE-REJECT checksum-mismatch`, exit 1 (verified
  once manually, not part of the graded runs).

## Purity

Pure Zag. Analysis via bash, znc, grep, cmp, md5sum, awk only.
No Python. No em dashes in this document (byte-verified pre-commit).
