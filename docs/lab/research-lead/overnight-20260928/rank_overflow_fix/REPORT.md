# REPORT: RANK-OVERFLOW-FIX (Sim B min-seq overflow model fix)

Date: 2026-10-03. Worker: RANK-OVERFLOW-FIX (non-ledger task;
claim minting paused). Lane:
docs/lab/research-lead/overnight-20260928/rank_overflow_fix/.

## Verdict

**PASS (8/8)** under the frozen prereg (K1..K7 in-binary, K8
external: 3/3 runs byte-identical,
sha256 `e431af2a1d7a744f16f781d31782c70c7bb05d84622d64ef6c8e3c48b0bb2434`).

K1 PASS, K2 PASS, K3 PASS, K4 PASS, K5 PASS, K6 PASS, K7 PASS,
K8 PASS. The fix closes the magnitude gap to exactly zero on
all overflow worlds. There is no deeper issue: the min-seq
overflow model was the sole cause.

## What was done

Additive on RANK-PATTERN's rank_pattern.zag (no substrate
changes, no redesign):
- `sim_prosp` gains `seqmove`: 0 = legacy slot-attached
  exile-seq model (bit-identical code path to RANK-PATTERN,
  in-binary control); 1 = fixed entry-attached model: on
  every periodic swap, `sq[s]` swaps with `sq[0]` (3 lines,
  gated), mirroring `cslot_swap`'s full 20-byte entry move
  including the exile-seq field at offset+16.
- `sim_prosp` implements the tro4>=0 slot validation its
  comment already promised: lockstep walk of the rk0/rk4
  traces (precondition eseq==1), counting slot mismatches on
  etypes 1/2/3, recording the first-mismatch index and etype.
  OUT gains +16=mismatches, +20=cold-miss count,
  +24=first-mismatch index, +28=eseq.
- main runs prospective Sim B for all 7 worlds x 2 variants
  after row 18, prints per-world summaries, and evaluates
  K1..K8.

## The bug (frozen diagnosis, confirmed)

The substrate's `cslot_swap` swaps the full 20-byte cold
entry between slots, exile-seq bytes included: exile-seq is
entry-attached and travels with the entry across
swap-with-front moves. Sim B kept exile-seq in a per-slot
`sq[]` array never moved on swap: slot-attached. On overflow,
the min-seq victim scan then used stale, entry-detached seq
values and picked the wrong victim slot; every later install,
hit slot, and swap displacement inherited the error. The
validation confirms the mechanism directly: under the legacy
model the FIRST slot mismatch on every overflow world is
etype=2 (install) - the victim-slot pick itself (V1 idx 160,
V2 idx 147, V5 idx 147, V6 idx 160). No-overflow worlds never
execute the min-seq path, so the sim was already exact there.

## Measured table (prospective Sim B, both variants)

| world | meas delta | predB_old | d_old | predB_new | d_new | mm_old | mm_new | nmiss |
|-------|-----------|-----------|-------|-----------|-------|--------|--------|-------|
| M2C2  | -35       | -35       | 0     | -35       | 0     | 0      | 0      | 0     |
| V1    | -31       | -53       | -22   | -31       | 0     | 39     | 0      | 24    |
| V2    | -11       | -32       | -21   | -11       | 0     | 18     | 0      | 0     |
| V3    | +9        | +9        | 0     | +9        | 0     | 0      | 0      | 0     |
| V4    | +2        | +2        | 0     | +2        | 0     | 0      | 0      | 0     |
| V5    | -53       | -75       | -22   | -53       | 0     | 11     | 0      | 0     |
| V6    | -33       | -51       | -18   | -33       | 0     | 35     | 0      | 24    |

simcc_new == ccT4 and simpay_new == rkT4 exactly on all 7
worlds (V5: 1185/6; V6: 2272/5; V1: 2351/6; V2: 1083/6).

## Kill-bar summary

- K1 SUBSTRATE-ANCHOR: PASS. Row 0 bit-for-bit equals the
  frozen RANK-LAZY values (35 fields checked). The substrate
  copy is untouched.
- K2 GAP-REPRODUCTION: PASS. Legacy model reproduces the
  parent's frozen gap exactly: d5o=-22, d6o=-18. The bars
  discriminate: the control fails exactness, the fix passes.
- K3 FIX-EXACT-OVERFLOW: PASS. Fixed model exact on V5, V6:
  simcc==ccT4, simpay==rkT4, d5n=d6n=0.
- K4 FIX-EXACT-BASE: PASS. Fixed model exact on all 5 base
  worlds (V1/V2 overflow included; M2C2/V3/V4 no-regression).
- K5 LAYOUT-DIVERGENCE: PASS. Fixed model: 0 slot mismatches
  on all 7 worlds. Legacy model: 39/18/11/35 mismatches on
  V1/V2/V5/V6 (first mismatch always etype=2, the
  victim-slot pick).
- K6 MISS-ACCOUNTING: PASS. V1 rk0 trace carries exactly 24
  etype-5 records (frozen value); each charges 64 points
  (V1: 24*64=1536 of ccT4=2351). V6 also has 24 misses.
- K7 TRACE-PRECONDITIONS: PASS. eseq==1 on all 7 rk0/rk4
  pairs; no trace overflow on any of the 14 traces.
- K8 DETERMINISM: PASS. 3/3 byte-identical,
  sha256 `e431af2a1d7a744f16f781d31782c70c7bb05d84622d64ef6c8e3c48b0bb2434`.

## Findings beyond the bars

1. **The parent's gap generalizes.** The legacy model's
   magnitude error was never measured prospectively on the
   base overflow worlds; it is d=-22 on V1 and d=-21 on V2.
   The fixed model is exact on all four overflow worlds, so
   the min-seq model fully accounts for every observed gap.
2. **No second-order term is needed for exact prediction.**
   With the seq model corrected, the full prospective sim
   (FIFO trace + swap schedule + recomputed install slots)
   predicts scan cost exactly as integers on all 7 worlds.
   The "closed-form second-order term" thread is closed for
   this mechanism: the full sim IS the exact predictor, and
   its only defect was the seq-attachment model.
3. **Cold misses are world-dependent.** V1 (mode=1, w=40) and
   V6 (mode=3, w=40) each have 24 misses; V2 (mode=2,
   extra-churner) has 0. Miss accounting (64 points each) is
   now barred in the scan-cost model via K6.
4. **Fix size vs effect.** Three gated lines (swap two i32s
   on swap) move four worlds from gaps of 18-22 points to
   exact integer prediction, with zero layout mismatches.
   The substrate needed no change: this was purely a
   predictor-model defect.

## What this does NOT test (honest accounting)

- Sealed post-freeze worlds (the fixed Sim B is exact on 7
  worlds, 4 with overflow; adversarial worlds remain the
  generality test).
- Whether the first-order per-swap formula can be repaired
  (RANK-PATTERN falsified it; untouched here).
- Other policies, pm values, promotion thresholds, or
  sparser swap schedules.

## Toolchain and hygiene

- Safebin mandatory: PATH=$HOME/safebin for every build/run;
  `command -v python3` / `command -v python` verified empty
  before the prereg commit; znc byte-identical to
  src/tools/toolchain/znc_linux_x86_64_abed8aa1
  (ZNC-CMP-IDENTICAL). No python invoked in this lane; no
  PROCESS-FAIL condition triggered.
- grep audit: no `while.*!(` negated conjunctions, no
  _zag_print, no `as *i32` slice construction; if-nesting at
  most 3; single approved `as *u8` in z_alloc (carried over).
- Commits local only, never pushed, explicit pathspecs, no
  reset. Prereg committed alone first (8758ce82f);
  implementation and artifacts committed after the verdict.
  No errata on the bars.

## Artifacts

- `rank_overflow_fix.zag`: implementation (pure Zag;
  RANK-PATTERN substrate + seqmove-gated seq model + tro4
  slot validation + 7-world prospective suite + K1..K8).
- `rank_overflow_fix_bin`: built binary.
- `run1.txt`, `run2.txt`, `run3.txt`: 3/3 byte-identical runs
  (sha256 `e431af2a1d7a744f16f781d31782c70c7bb05d84622d64ef6c8e3c48b0bb2434`).
- `err1.txt`, `err2.txt`, `err3.txt`: empty stderr logs;
  `err_build.txt`: benign znc warning (zagd unavailable).
- `PREREG.md` (frozen 2026-10-03, committed alone as
  8758ce82f), `NAMECHECK.md`, `REPORT.md`.
