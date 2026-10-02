# LIVE DELIBERATE SYNONYM LEARNING — Final Report (2026-09-25)

Prereg: `PREREG_SYNINT_LIVE.md` (commit `8d0ca604e120d6d9db94e9bf04c67547ec17b030`).

## What was built

`live.zag` (new): TNN deliberates over a `UTT|uid|channel|pattern|text` utterance
stream and installs synonym beliefs through the unified substrate — no batch
ingest. Deliberative sequence per prereg: notice R1/R2/R3/R4 evidence → check
OBS vs CON provenance → consult live relation/veto beliefs → weigh with
unchanged thresholds → veto + transitive-closure safety → journal decision and
grounds BEFORE mutation → install only through `syn_install`.

`match.zag` (new): extraction of original `learn.zag` lines 17–463 byte-for-byte;
`learn.zag` now imports it and retains CLI/main. Extraction-equivalent build
reproduces all three baseline artifact hashes byte-for-byte (verified this run).

## Gate results

| Gate | Result |
|---|---|
| L1 12 CON + 12 OBS novel pairs | 12 OBS installed, 12 CON REFUSE-CONSTRUCTED, 0 constructed relations |
| L2 provenance | all 116 live rows (112 rel + 4 veto) carry valid non-empty lid chains |
| L3 journal/install/substrate reconciliation | 112/112 installs ↔ substrate, 4/4 vetoes ↔ substrate; replay idempotent; WITHDRAW correct |
| L4 positive→R4 revision | R1 installs, R4 kills relation (DEAD) + installs veto; revised=1 |
| L5 closure veto withholding | (gamma,beta) WITHHELD when closure would violate veto(alpha,beta); withheld=1 |
| L6 frozen 276-line stream | 112 relations + 4 vetoes; order-normalized dump BYTE-IDENTICAL to batch; 26-query battery 25/26 matching frozen profile (6/6 fresh, 6/6 dist, 6/6 near, 4/4 multihop, 3/4 morph — only QMO3 misses) |
| L7 determinism | 3 runs byte-identical (syntab.bin, synmem.bin, delib.log); zero RNG; no curated strings (only the CLI verb "stream" matched) |
| L8 kill/pin/promote | all succeed (rc=0) on live-installed beliefs; pin/promote correctly refuse dead slots (rc=103) |
| Head-to-head 8 nonce pairs | 8/8 live–batch parity (dumps identical) |
| Fresh-vocabulary retention | 6/6 QFR01–06 PASS on live store |

## Bugs found and fixed (in live.zag, during this work)

1. `syn_load`/`syn_save` arg order swapped (`syn_load(dir,&db)` vs correct
   `syn_load(&db,dir)`) — compiled silently, caused the smoke-test panic.
2. Witness lid gather stored at `nl2*8` stride but `consider_pos` read at `li*4`
   — produced empty lid entries; fixed to consistent `*4`.
3. R3 candidate lids stored in reverse arrival order vs batch — fixed by storing
   older line's uid first (l1=older, l2=newer), giving order-normalized
   byte-identical dumps vs batch.

## Pre-existing bug (NOT fixed — out of scope, documented)

Batch re-ingest into an existing store preserves relation count but wipes old
relation evidence-LID chains (`learn.zag` reinitializes loaded lhead/ltail).
Observed 2026-09-25. Do not confuse with live implementation.

## Notes / gaps

- The official 51-query battery inputs (queries/keys/answers with QPA IDs) were
  not recoverable from the workspace; 51/51 for live follows deductively from
  the order-normalized identical relation/veto sets (identical closure →
  identical lookup → identical grades). The synonym-sensitive 26-query battery
  was run empirically: 25/26, exactly the frozen regression profile.
- Live `syntab.bin` bytes differ from batch baseline (allocation order), but the
  format is shared and `learn dump` reads both; semantic content proven
  identical.
- Journal format: `J|seq|uid|chan|rule|w1|w2|decision|grounds`, append-only,
  written before any mutation.

## Verdict

**PASS.** TNN itself notices synonymy mid-deliberation (R1/R2/R3/R4 evidence),
checks provenance, consults its own live beliefs, withholds on veto/closure
risk, journals grounds before mutating, and installs through the unified
substrate. The trigger is genuinely TNN-deliberate: every install in the
276-line run is preceded by a journaled deliberation record with grounds, and
constructed content is refused at the firewall with zero substrate trace.
