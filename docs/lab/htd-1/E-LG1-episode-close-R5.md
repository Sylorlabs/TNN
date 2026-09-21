# E-LG1 episode-close arm — R=5 completion verdict

**Run:** 2026-09-21 ~09:30–10:15 PDT by MARATHON CREW 2 (parent orchestrator,
marathon test coordinator, backlog item 2).
**Binding:** `HTD1_PREREG_FROZEN_2026-09-21.md` §3d (E-LG1 kill bars) + §7
verdict rubric. Nothing amended; bars applied as written.
**Workdir:** `~/workspace/htd-1/builds/elg1/` (binary `elg1_bin`, built from
`elg1.zag` 2026-09-21 07:35; binary postdates source — no source/binary drift).
Runs under `runs/battery/`; byte-level evidence local-only (binaries/ledgers
not committed, per HTD-1 evidence policy).

## What was open

The HTD-1 closeout sheet (`RESULTS_VERDICT_SHEET.md`) marked E-LG1
**PASS (INDEPENDENT)** on the fixed16 arm only: "the epclose (episode-close)
arm never got its R=5 battery — only fixed16 (fixed-count batching) has full
evidence. The 11 kill trials cover both modes (epclose tT01 + fixed16
fB01–fB10), all IDENTICAL." This run completes the epclose leg.

## Frozen spec (programmatically extracted from the frozen prereg, §3d)

> **E-LG1 — write batching.** One durable write per episode + episode-open
> marker; crash → deterministic re-execution reproduces the batch. REPLAY
> fail: ≥1 byte divergence over 500 episodes incl. 10 kill-restarts. SAVINGS
> fail: write syscalls saved <60% OR bytes >110% of baseline.
> Internal: episode-close vs fixed-count batching — test both.

Execution followed the crew's frozen lane script (`laneA.sh` epclose legs):
`run_arm.sh epclose` (R=5 × 500 episodes, `rm -f` per rep) + the 10
epclose kill trials `eA01`–`eA10` (start/end/mid kill points at episodes
12/12/60/115/170/225/280/335/390/440) via `killtrial2.sh`, recovered and
byte-compared vs `epclose_r1.ledger`.

## Results

### R=5 battery (epclose, 500 episodes each)

| rep | rc | secs | SHA-256 of ledger | entries |
|-----|----|------|-------------------|---------|
| 1 | 0 | 30 | `397dd7dd0c37d950c9153ce5f80b031bb879614d9591e7bf73402e04b496440e` | 18001 |
| 2 | 0 | 34 | `397dd7dd0c37d950c9153ce5f80b031bb879614d9591e7bf73402e04b496440e` | 18001 |
| 3 | 0 | 35 | `397dd7dd0c37d950c9153ce5f80b031bb879614d9591e7bf73402e04b496440e` | 18001 |
| 4 | 0 | 29 | `397dd7dd0c37d950c9153ce5f80b031bb879614d9591e7bf73402e04b496440e` | 18001 |
| 5 | 0 | 43 | `397dd7dd0c37d950c9153ce5f80b031bb879614d9591e7bf73402e04b496440e` | 18001 |

All five SHAs are identical **to each other and to the baseline**
(`base_r1`/`base_r2`, `fixed16_r1`–`r5` — all
`397dd7dd0c37d950c9153ce5f80b031bb879614d9591e7bf73402e04b496440e`).
The ledger FILE bytes are byte-identical across all modes; marker files are
mechanism sidecar (not in the replay compare), per the binary's design note.

### Kill-restart battery (epclose)

11/11 IDENTICAL (1 pre-existing `tT01` + 10 new `eA01`–`eA10`), zero DIVERGED:

| trial | phase | target | landing | verdict |
|-------|-------|--------|---------|---------|
| tT01 | start | 12 | pre-commit(torn) | IDENTICAL |
| eA01 | start | 12 | pre-commit(torn) | IDENTICAL |
| eA02 | end | 12 | post-commit | IDENTICAL |
| eA03 | mid | 60 | post-commit | IDENTICAL |
| eA04 | start | 115 | pre-commit(torn) | IDENTICAL |
| eA05 | end | 170 | post-commit | IDENTICAL |
| eA06 | mid | 225 | post-commit | IDENTICAL |
| eA07 | start | 280 | pre-commit(torn) | IDENTICAL |
| eA08 | end | 335 | post-commit | IDENTICAL |
| eA09 | mid | 390 | post-commit | IDENTICAL |
| eA10 | start | 440 | pre-commit(torn) | IDENTICAL |

All kill_rc=137 (SIGKILL delivered), recover_rc=0; recovery via deterministic
re-execution reproduces the batch to the exact baseline SHA. Landings cover
pre-commit (torn batch) and post-commit crashes.

### Savings (from frozen manifests, `epclose_r1.man` vs `base_r1.man`)

- n07 write syscalls: epclose **1000** vs baseline **18001** →
  saved = (18001−1000)/18001 = **94.45%** (bar: ≥60%) ✔
- n06 durable bytes: epclose **1184064** vs baseline **1152064** →
  **102.78%** of baseline (bar: ≤110%) ✔
- n08 fsync syscalls: epclose **1000** vs baseline **18001** (same 94.45% reduction).
- n11 episode-open markers: 500 (mechanism-added entries, one per episode).

## Verdict: **PASS**

- **REPLAY bar:** 0 byte divergence over R=5 500-episode runs (all SHAs =
  baseline SHA); 11/11 kill-restarts IDENTICAL to baseline. Bar NOT tripped.
- **SAVINGS bar:** 94.45% write-syscall saving ≥ 60% bar; 102.78% bytes ≤ 110%
  bar. Bar NOT tripped.
- Determinism discipline: R=5 byte-identical artifacts (SHA-256), no
  randomness in any canonical decision path (binary is the same scored
  deterministic build; znc quirks ZNC-2026-09-21-002..012 respected — scalar
  locals, no `[]i32` indexed casts, `z_alloc` naming, unconditional
  `_zag_arg` reads, no nested large structs).

## Caveats / notes

- `base_r3.ledger` (747,136 B, no manifest, not in sha.log) remains
  UNVERIFIED and excluded, per the closeout sheet — not needed; base_r1/r2
  are byte-identical and sufficient as baseline reference.
- `kill.log` carries a duplicated `tT01` line (double-logged, single trial);
  no effect on scoring — 11 unique epclose kill trials, all IDENTICAL.
- E-LG1 internal "test both" is now fully satisfied: fixed16 (91% syscall
  saving) and epclose (94.45% syscall saving) both PASS, both byte-identical
  to baseline. Scenario-fit mapping (which batching mode suits which load)
  remains a future-mapping item, not a bar.
- The closeout sheet's line "the epclose arm never got its R=5 battery" is
  now stale — superseded by this document.
