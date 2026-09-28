# TNN Native Zag v2 Migration Status

Date: 2026-08-29

## Option 1 result: native cognition path is complete

The repository contains 148 Python files and 32 native Zag source files. The
Python files are not a second hidden TNN runtime:

- **116** are explicitly marked `REFERENCE_ONLY`, calibration-failed,
  preliminary-bug, or equivalent historical result code.
- The remaining **32** are external experiment orchestration, source-contract
  inspection, evaluator/scoring, model-training, checkpoint, or result-packaging
  utilities. Several use NumPy, SciPy, scikit-learn, PyTorch, Joblib, or process
  control; none is called by a native `.zag` program or enters the native
  compiler execution path as learner cognition.
- The native cognition and qualification path is implemented in Zag sources,
  including `tnn_r28_aeif.zag`, `tnn_r30_big_boom.zag`,
  `tnn_r31_endogenous_chunking.zag`, `tnn_r32_epistemic_chunking.zag`, and the
  native E45–E50 terminal-controller sources.

This is the scientifically meaningful interpretation of “option 1”: active
TNN cognition is native Zag v2; Python remains an explicitly non-promotable
research/evaluation archive. Translating evaluator glue into Zag would not make
the learner more native and would risk changing the provenance of historical
results.

## Native-path checks

1. No `.zag` source imports or invokes Python.
2. E45–E50 compile and run under the persisted official Linux x86-64 `znc`.
3. E50 has two byte-identical native binaries, a preserved raw ledger, a fresh
   seed manifest, and a verified checksum bundle.
4. R27 remains canonical; native E45–E50 are valid negatives, not promoted
   successors.

## Option 2 result

All 148 Python files have been removed from the checked-out tree. The exact
bytes and full provenance remain recoverable from the preceding Git commits;
the recovery point for every historical script is the commit immediately before
the removal commit. The `*.py` ignore rule prevents accidental reintroduction.

This is repository hygiene, not a claim that NumPy/SciPy/PyTorch experiments
were semantically ported to Zag. Those experiments were external evaluation and
research utilities, while the maintained TNN cognition path is native Zag v2.
