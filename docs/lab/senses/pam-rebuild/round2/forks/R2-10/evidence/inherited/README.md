# Inherited partial state (previous crew, killed by daemon restart 2026-09-23)

- `batch_<task>.tsv`: noemit batch runs on the R2A set with the PREVIOUS
  `src/sense` binary (pre-fix). `batch_pitchdisc.tsv` is 0 bytes — the run
  was interrupted by the daemon drain mid-task.
- Score of inherited batches vs truth: 6267/9045 = 0.6929
  (colordisc 0.9094, colorconst 0.7150, motiondir 0.6036,
   shapetrans 0.7952, timbredisc 0.2496).
- The timbredisc 0.2496 was an i64 overflow bug in the weighted-harmonic
  sum (fixed by the replacement crew; see LEDGER.md). All inherited TSVs
  are SUPERSEDED by evidence/battery/ (fixed binary).
- `sample_train_manifest.tsv` / `sample_eval_manifest.tsv` (+ .sha256):
  frozen 200-trial human samples, verified disjoint (0 overlap), each
  100 clean + 100 adversarial. KEPT and reused by the replacement crew.
- `freeze_samples.py`: the freezing script (kept).
- `../run_batch.sh`: the previous crew's batch script (kept at fork root).
- `../src/sense.zag`: source as inherited; the replacement crew applied
  two audited fixes (timbredisc estimator port from R2-9, video emission
  now depicts both cited frames side-by-side). Full diff vs inherited
  binary's source is not available (binary only); changes are logged in
  LEDGER.md.
