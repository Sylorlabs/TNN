# RUNLOG.md — Crew B execution log (D1 full battery, real learner)

All times PDT, 2026-09-27. No commit made by this crew.

## Build

- 21:xx — Read frozen PREREG §§1–8, AMENDMENT_PROPOSAL.md, pilot sources,
  PILOT_REPORT.md, REDTEAM_REPORT.md. Verified learner commit
  `3cd24f11d119a17d14d9637e43ebdc8918b41e92` (workbuddy round-2 dialogue
  learner). Compiled `work/wb_dialogue_bin` with pinned znc
  (`.../bin/znc_linux_x86_64_abed8aa1`); Darwin-flavored
  `R33_NATIVE_IO_V1.zag` failed, rebuilt with toolchain-native IO+SHA256
  files. Binary: 752,870 bytes.
- 21:xx — Feasibility probe (relay, 6 reverse examples on tok 0–5):
  taught lookups echo ("the reverse of ao is oa."), held-out tok probe
  ("qeum") → "I don't know." Evidence the real learner stores examples but
  does not induce rules. Predicted P0 failure; full six-rule P0 still run.
- 21:xx — Wrote `battery.zag` (gen/null/singlerule/learner modes), compiled
  clean. `./battery gen`: TEACH 36, P0 48, P1 150, P2 600, P3 8.
- 21:xx — **Defect:** `./battery null` and `singlerule` exited 1
  ("panic: slice index out of bounds"). Root cause: pair enumerator copied
  from the 4-rule pilot (`p/3`, `p%3`) → rule index 8 out of bounds on the
  6-rule battery. Fixed to `p/5`, `p%5`. Broken outputs discarded.
  Rebuilt binary SHA `6c9d2b06f9526965b1a56b592ec966e72562e00743003c77cc71b254f429b89e`.

## Scripted chance arms (frozen: NULL, SINGLE-RULE)

- `./battery null` → exit 0: mastery 0/6, composition 0/600, trueacc 13/600.
- `./battery singlerule` → exit 0: mastery 6/6, composition 32/600, trueacc 32/600.
- Reruns: `null.out`=`null2.out`, `singlerule.out`=`sr2.out` byte-identical.

## Real learner sessions (`drive.py`)

- `run1`: 8 fresh sessions (6 P0 + 1 P3 + 1 samples). P0 48/48 "I don't
  know." (0/6 mastery); positive controls 5/6 (rule 4 fails: intake
  lowercases "Ao"→"ao"); P3 8/8 withhold; samples 18/18 "I don't know."
- `run2`: full rerun — all 5 output files byte-identical to `run1`.
- `run_pert` (`MALLOC_PERTURB_=165`): all 5 files byte-identical to `run1`.
- `./battery learner` on run1 transcripts: mastery 0/8×6, 600/600 class
  (a), reflex 0/8, 656 ITEM lines, 48/48 P0 records parsed.

## Audits

- `audit.py`: teaching mass 126 lines, all train-token single-part; 0
  driver-vs-generator mismatches; 66/600 P2 inputs byte-identical to
  training inputs (period-52); 5 short-string expected-output coincidences
  (soft-item family); dumb-strategy rates; commutativity; K6 bigram table
  (5 pairs with zero bigram-clean inputs).
- `kbars.py`: K1 kill (0 ≤ 0.1533), K2 void (100% (a)), K3/K4/K5 negative,
  K6 vacuous.

## Deliverables (all in `~/workspace/comp_b4/battery/`)

INTERPRETATION.md (I1–I12), BUILD.md, RESULTS.md, BARS.md, RUNLOG.md.
Evidence: `items.tsv`, `null.out`, `null2.out`, `singlerule.out`,
`sr2.out`, `run1/`, `run2/`, `run_pert/`, `work/wb_dialogue_bin`.
Tooling: `battery.zag`, `drive.py`, `audit.py`, `kbars.py`.
