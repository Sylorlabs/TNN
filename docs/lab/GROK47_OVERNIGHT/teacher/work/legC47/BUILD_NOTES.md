# Leg C47 build notes (grok-4.7 English-domain teacher leg)

- `src/corpus.zag`: generated from
  `GROK47_OVERNIGHT/teacher/evidence/grok47_corpus/corpus.json`
  (sha256 `111f588f29f23c7864f4842401516e9b30d98c495f5d1a0b68642a71d67f467a`)
  by mechanical port of
  `wave12/championship-english/grok/legs/build/gen_corpus_zag.py`
  (same `grok_dump_at`/`grok_obs_at`/`grok_dis_at`/`grok_prb_at` format;
  model assertion adapted to `grok-4.7`; withheld set empty).
- Driver sources (`grok_teacher_leg.zag`, `t5_core.zag` with the English
  `t5_truth` oracle, Q1 files, substrate): unmodified copies of the frozen
  `wave12/championship-english/grok/legs/legC/src/`.
- Build: `znc_linux_x86_64_abed8aa1 grok_teacher_leg.zag -o grok47_teach`
  (warnings only; binary excluded from commit).
- Runs: `./grok47_teach` × 5 → `runlogs/teach47_run<1..5>.log`.
  All exit 0, byte-identical; `GROKC_TEACH_DIGEST` byte-identical to
  grok-4.6's frozen English digest `be5dba84…05d`; final mastery 192/192.
