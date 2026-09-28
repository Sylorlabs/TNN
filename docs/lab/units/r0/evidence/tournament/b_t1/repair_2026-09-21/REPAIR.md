# grounded_adaptive_mdl heap-overflow — repair + retest (crew3, 2026-09-21)

## Status of the original B-T1 verdict (UNCHANGED)
The closeout binding verdict **B-T1: FAIL** (raw_micro rank 7/10, not dead last;
`CLOSEOUT_ADDENDUM.md` §2) **stands** for the frozen/unrepaired module. This
document records a *repair-then-retest* of the grounded arm only; it does not
reinterpret, revise, or touch the closeout verdict record.

## Bug root cause (one line)
In `mdl_fit`'s grounded block, `mx[slot]` stored the **candidate index**
`cix[g2]` (range 0..C−1) but the next-byte histograms `gtot`/`gnx` were
allocated with only **G = min(C, 8192) entries** — so when C > 8192 (real-size
corpora), `gtot[ge]` / `gnx[ge*256+b]` wrote past the heap allocation
(SIGSEGV, verified 3/3 on 100KB inputs, deterministic).

## Deliberate repair (minimal, no rewrite)
`units/r0/impl/arms/arms.zag` (mdl_fit, grounded block only):

**Repair-1 (heap overflow):** `mx[slot]` stored the candidate **index** `cix[g2]`
(0..C−1) but the next-byte histograms `gtot`/`gnx` were allocated with only
G = min(C, 8192) entries — `gtot[ge]` / `gnx[ge*256+b]` wrote out of bounds
when C > 8192. Fix: index the histograms by candidate **rank** (0..G−1), a
bijection onto the top-G candidates; the scoring loop splits rank (→gtot/gnx)
from candidate index (→cs/cc/cl), plus a defensive `ge < G` invariant.

**Repair-2 (intractability, found during retest):** with the overflow fixed, the
re-scan's big-table linear-probe lookups cost O(MS) each once the 1M-entry span
table fills (measured: 200KB >13 min vs 41 s for 100KB — superlinear blowup;
5.6 MB projected to days). The re-scan only ever consumes top-G candidates, so
it now probes a SMALL table (16384 slots, load ≤ 0.5) holding exactly the G
candidates — semantically identical (same (rank,next-byte) increments,
verified byte-identical vs repair-1 on t2/t4/t5/t6/100KB) at O(G) per lookup.
200KB after repair-2: 341 s (≈linear scaling restored).

Allocation audit vs the 2^25-byte slice limit: `gnx` ≤ 16.7 MiB, `gtot` 65 KiB,
small table `sh` 128 KiB; all other tables unchanged (8 MiB each). No
ZNC-003/005/006/009 struct issues (flat `*i64` tables only); all tables
explicitly zeroed or -1-filled by hand (uninitialized-heap lesson honored);
ZNC-002 slice-casting not used; ZNC-007/008/012 patterns absent from new lines.

## Repair neutrality proof (repaired binary vs unrepaired goldens)
- Crash threshold: 100KB sqlite3.c prefix — **was SIGSEGV 3/3, now rc=0**,
  `END chunks=68433`.
- Small inputs (C ≤ 8192, M8 smoke vectors t2/t4/t5/t6): repaired
  `grounded_adaptive_mdl` output **byte-identical** (4/4) to the arms crew's
  saved unrepaired smoke goldens — the rank↔index change is semantics-preserving
  below the cap; only C > 8192 behavior changes (crash → defined output).
- Full B-T1 retest, all 11 arms × 2 corpora × 2 runs with the repaired binary:
  the 10 non-grounded arms' outputs are **byte-identical (sha256) to the frozen
  closeout RUN_MANIFEST goldens** (10/10 arms × 2 corpora) — the repair changes
  nothing outside the grounded==1 path. All run pairs byte-identical (N=2).

## Retest measurement (frozen probe, closeout bt1_score.py + bt1_rank.py)
Measured with the frozen closeout scorer on the repaired-binary outputs
(r1 segs; r1==r2 byte-identical verified for grounded; 10 non-grounded arms
byte-identical to closeout goldens). Rank table below is the **actual output
of the frozen `bt1_rank.py`** (2026-09-22), saved as
`rank_table_repaired.json` — not a manual inference.

| rank | arm | tournament_score | prose (pg100) | code (sqlite3.c) |
|---:|---|---|---:|---:|
| 1 | predictive_surprise | 0.9190452897403919 | 0.9558 | 0.8823 |
| 2 | fixed_window_4 | 0.8958960397894453 | 0.8968 | 0.8950 |
| 3 | random_chunks (informational) | 0.8854 | — | — |
| 4 | hierarchical_mdl | 0.8473 | — | — |
| 5 | adaptive_mdl_8 | 0.8399 | — | — |
| 6 | adaptive_mdl | 0.8358 | — | — |
| **7** | **grounded_adaptive_mdl** | **0.831952034689595** | **0.83168828571046** | **0.83221578366873** |
| 8 | raw_micro | 0.7704 | — | — |
| 9 | fixed_window_8 | 0.7410 | — | — |
| 10 | fixed_window_16 | 0.7103 | — | — |
| 11 | fixed_window_64 | 0.4604 | — | — |

(per-corpus composites for non-grounded arms match the frozen closeout
rank_table.json exactly — byte-identical inputs; full-precision prose/code
shown for grounded, measured 2026-09-21)

- binding ranks: predictive_surprise=1, fixed_window_4=2, raw_micro=8 of 10
  binding (was 7/10 unrepaired)
- binding verdict (repaired module, frozen ranker): **FAIL** — ordering holds
  (predictive_surprise > fixed_window_4 > raw_micro) but raw_micro is still not
  dead last (fixed_window_8/16/64 rank below it), exactly as in the original
- grounded_adaptive_mdl placement: **7/11** (was CRASHED/UNEVALUABLE)

**Repaired-module B-T1 verdict: FAIL.** The original unrepaired B-T1 FAIL
(CLOSEOUT_ADDENDUM.md) is preserved and untouched; this is the repaired
module's separately-measured result, per the no-reinterpretation rule.

Timing (wall, 2-CPU VM under marathon contention): grounded pg100 r1 2563 s /
r2 1895 s (64,814,822 B out); sqlite3.c r1 4482 s (130,390,288 B out).
Zero RNG in decision paths; r1==r2 byte-identical on both corpora.

## Artifacts
- repaired source: `docs/lab/units/r0/impl/arms/arms.zag`
- run outputs: `docs/lab/units/r0/evidence/tournament/b_t1/repair_2026-09-21/runs/`
- battery log: `docs/lab/units/r0/evidence/tournament/b_t1/repair_2026-09-21/BATTERY.log`
- scores + rank table: `docs/lab/units/r0/evidence/tournament/b_t1/repair_2026-09-21/`

## Law compliance
1x only. Pure Zag. Zero RNG in AI decision paths (repair touches no decision
logic). Byte-identical reruns verified (N=2 battery pairs + M8 smoke on the
repaired binary for grounded). No binaries/`.zagd`/`.zag-cache` committed;
scratch under `~/workspace`, not `/tmp`.
