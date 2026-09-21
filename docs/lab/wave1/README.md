# TNN Native Lab — Wave 1 (2026-09-19)

Reconnaissance wave. All work executed on Linux; nothing ran on GitHub Actions.

- `brain/STATE_SCHEMA.md` — white-box map of the R27 accepted brain state
  (5-deep lineage, Trace learning atom, 58 structural revisions, tensor containment).
  Audit scripts: `restricted_load.py`, `analyze2.py`, `analyze3.py`
  (Python used once, as the documented exception — the pickle is a Python artifact).
- `toolchain/ZAG_PLAYBOOK.md` — the Zag reference for all future agents:
  compiler provenance, tested syntax, cross-target table, Darwin→Linux port map,
  error catalog. Includes the Linux port of the R34 v3 continual-learner runner
  (`r34v3_run_native_linux.sh`) and the ported syscall substrates
  (`R33_NATIVE_IO_V1.zag`, `storage.zag`, with `.darwin.orig` originals).
  R34 v3 ran natively on Linux with failures=0 — first time outside macOS.
- `history/DO_NOT_REPEAT.md` — the complete negative record (E45–E50, E51AH/AI/AJ,
  R33-B000, abstention tradeoff, evaluator leakage, REFERENCE_ONLY law, banned practices).
- `history/WHAT_TNN_IS_NOT.md` — 10 evidenced identity statements, each with doc pointers.

## ⚠️ Contamination notice — 2026-09-20 (R34 hidden-randomness remediation)

This document cites results that are **QUARANTINED**: the "R34 v3 ran natively on Linux with failures=0" campaign result.
The cited runs trained with `explore_enabled=1`, engaging a hidden seeded LCG
(`r34v3_rng` in `r34_learner_core.zag`) in the learner's action-choice path —
a violation of the no-randomness law (r34 RNG probe, workstream 2/8, commits
`072f25aa` / `4976cbf5` on branch `tnn-native-lab`; Micah's ruling: REMEDIATE).
Treat the cited numbers as recorded-but-uncertified until clean reruns exist.
The original text above is left intact for the record.
