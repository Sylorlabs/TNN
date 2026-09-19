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
