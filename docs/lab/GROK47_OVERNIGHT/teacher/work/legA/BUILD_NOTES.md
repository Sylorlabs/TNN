# Leg A build notes (grok-4.7 showdown)

- `corpus_grok47.zag`: generated from
  `GROK47_OVERNIGHT/teacher/evidence/grok47_corpus/corpus.json`
  (sha256 `111f588f29f23c7864f4842401516e9b30d98c495f5d1a0b68642a71d67f467a`)
  by mechanical adaptation of
  `wave12/championship/class3-standardized/build/gen_corpora.py`
  (same if/else-chain integer format; error-inventory all-zero gate holds).
- `driver_grok47.zag`: assembled by mechanical adaptation of
  `wave12/championship/class3-standardized/build/build_driver.py`
  (identical `q2s_trial.zag` + `s37_step.zag`; only the corpus import differs).
  Base sources copied from the frozen
  `wave12/championship/class3-standardized/src/` (not modified).
- Build: `znc_linux_x86_64_abed8aa1 driver_grok47.zag -o c3s_grok47`
  (warnings only; binary excluded from commit).
- Runs: `./c3s_grok47 teach3c std <rep>` for rep 0..4 → `runlogs/grok47_rep<rep>.log`.
  All exit 0; digests byte-identical across reps.
- Domain note: the standardized driver's `t5_truth` oracle is Zharovia-domain,
  so this battery skips 187/240 English facts by design. The valid
  English-domain run is `../legC47/` (frozen English leg-C driver).
