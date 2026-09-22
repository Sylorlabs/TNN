# NOTE — Python oracle demoted to script-only status (2026-09-22)

Per Micah's standing law ("use zag unless its a script") and the frozen
`PREREG_ORACLE_ZAG.md` §5:

- `third-path/oracle/tp_oracle.py` (the independent Python oracle that
  verified TP1 at verdict time) is hereby **demoted to build-script
  status**. It remains in the repo as a data-preparation / cross-check
  script. It **no longer certifies** TP1 results.
- The **pure-Zag oracle** (`third-path/oracle-zag/src/opz_oracle.zag`,
  verified by `oracle-zag/evidence/COMPARISON_REPORT.md` with 0
  mismatches across 3 byte-identical runs) is the **verification
  authority** for the TP1 third-path trial.
- Python's remaining legitimate roles in this workstream: flattening the
  frozen JSON corpus into the oracle's pipe-delimited input
  (`oracle-zag/data_prep/prep_flat.py`), SHA256SUMS verification of
  frozen inputs, and comparison/report scripting. No Python code sits in
  the decision or ledger-certification path.
