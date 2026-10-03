# REPRO_DDES_V2_STEP4.md: independent reproduction from committed source

Lane: docs/lab/rsi/runs/wave-20261001-1421pdt/ddes_step4/
(Pipeline step 4 for the DDES follow-up V2 BUILD-PASS, wave-20261001-1121pdt.)

## Verdict: REPRODUCED

The sealed evaluation recompiled from the COMMITTED source
(`git show HEAD:docs/lab/rsi/runs/wave-20261001-1121pdt/ddes/ddesp2.zag`,
unmodified, 21229 bytes, extracted to this lane as ddesp2_repro.zag)
is byte-identical to the wave's frozen transcripts.

## Hashes

Common sha256 across all six files:

b8bc5fa9cd2feec8c239baad42eba88438c9dea4341b226189bcc81cca6fcde3

Files sharing this hash:
- wave-20261001-1121pdt/ddes/run1.txt (wave's frozen transcript)
- wave-20261001-1121pdt/ddes/run2.txt (wave's frozen transcript)
- wave-20261001-1121pdt/ddes/run3.txt (wave's frozen transcript)
- ddes_step4/repro_run1.txt (this lane, from committed source)
- ddes_step4/repro_run2.txt (this lane, from committed source)
- ddes_step4/repro_run3.txt (this lane, from committed source)

The wave's own result doc reported the truncated hash prefix
"b8bc5fa9cd2feec8..." on all three runs; this lane confirms the full
256-bit value matches on all three wave transcripts and all three
reproduction runs. Zero diffs: NOT-REPRODUCED diffs section is empty
(no diffs found).

## Protocol evidence

Compile (pinned znc): exit 0; executable produced (ddesp2_repro_bin);
stderr = 93 bytes containing only the documented unconditional
zagd-availability warning line; zero other bytes. This matches the
amended K-G1 (re-frozen before any implementation commit).

Sealed evaluation protocol per the frozen prereg (World F both
configs, World A anchor both configs, scaffold disconnect, World G
both configs), reproduced exactly from the trace:

Phase A (scaffold connected):
- World F cfg0/cfg1: `TARGET V*=2 t*=0 schema=1`,
  `FLAG TSTAR-ZERO-BOUNDARY floor=1` (exactly between TARGET and PLAN),
  `PLAN [S,W,OY]`, `EXEC real=1` (cfg0) / `real=0` (cfg1),
  `PRED h0=1 h1=0`, correct SURVIVE/ELIM, `CONVERGE-OK`.
- `SCHEMA-RECORD schema=1 V*=2 t*=0 tstar_zero=1 pred_h0=1 pred_h1=0`
  (byte-exact line, present once).
- World A cfg0/cfg1: `TARGET V*=2 t*=1 schema=1`, `PLAN [S,W,OY]`,
  no FLAG line, `EXEC real=0` (cfg0) / `real=1` (cfg1),
  `PRED h0=0 h1=1`, correct SURVIVE/ELIM, `CONVERGE-OK`.

Scaffold disconnect:
- `SCAFFOLD-DISCONNECT` emitted; `SCAFFOLD-CALLS 0` at the end;
  zero `SCAFFOLD-VIOLATION` lines in all three runs.

Phase B (scaffold disconnected, World G sealed, both configs):
- `RECORD-LOAD schema=1 V*=2 t*=0 tstar_zero=1 pred_h0=1 pred_h1=0`
  (fields byte-identical to the SCHEMA-RECORD line).
- `REPLAN [S,W,OY]` (not the derivation PLAN marker); zero-wait plan
  absent on both configs.
- `EXEC real=1` (cfg0) / `real=0` (cfg1), `PRED-RECORD h0=1 h1=0`,
  EXEC agrees with the persisted prediction on the surviving
  hypothesis; cfg0 `SURVIVE h0` / `ELIM h1`; cfg1 `ELIM h0` /
  `SURVIVE h1`; `CONVERGE-OK` on both.
- Phase-2 section (after SCAFFOLD-DISCONNECT) contains zero derivation
  markers: the 4 TARGET occurrences in the trace are all in phase 1;
  phase 2 carries only RECORD-LOAD, REPLAN, EXEC, PRED-RECORD,
  SURVIVE/ELIM, CONVERGE-OK, and SCAFFOLD-CALLS lines.

Runs: 3/3 exit 0, 1004 bytes each, zero stderr bytes each. Determinism
holds across the recompiled-from-committed-source binary.

## Independence note

This lane is an independent reproduction, not a re-report: the source
came from the git object store (HEAD), not from the wave's worktree;
the binary is a fresh compile under the pinned znc; the transcripts
were regenerated in this lane and only then compared. The wave's
worktree ddesp2.zag was byte-compared against the committed source
(zero diff) but was not used as the reproduction input.

## Claimed boundaries (unchanged)

Bounded L2 per the prereg's honest-boundaries section; no L3 claim
(C0-A through C0-D all fail, documented in the prereg). This step
reproduces evidence, not claims: it establishes that the committed
source regenerates the wave's sealed-evaluation transcripts exactly.

## Files left behind (uncommitted, per task)

- docs/lab/rsi/runs/wave-20261001-1421pdt/ddes_step4/NAMECHECK.md
  (this lane's guard check and provenance record)
- docs/lab/rsi/runs/wave-20261001-1421pdt/ddes_step4/REPRO_DDES_V2_STEP4.md
  (this verdict doc)
- docs/lab/rsi/runs/wave-20261001-1421pdt/ddes_step4/ddesp2_repro.zag
  (committed source extracted via git show, unedited)
- docs/lab/rsi/runs/wave-20261001-1421pdt/ddes_step4/ddesp2_repro_bin
  (fresh compile from committed source)
- docs/lab/rsi/runs/wave-20261001-1421pdt/ddes_step4/repro_build.err
  (93-byte documented warning only)
- docs/lab/rsi/runs/wave-20261001-1421pdt/ddes_step4/repro_run1.txt,
  repro_run2.txt, repro_run3.txt (1004 bytes each)
- docs/lab/rsi/runs/wave-20261001-1421pdt/ddes_step4/repro_run1.err,
  repro_run2.err, repro_run3.err (0 bytes each)
