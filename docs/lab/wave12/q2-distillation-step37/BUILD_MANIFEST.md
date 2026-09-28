# Q2-STEP37 build manifest (championship team STEP, 2026-09-21)

## Frozen inputs (DATA commit 7f4010fc9803, before any TNN run)
- `corpus/corpus.json` — 40 accepted step-3.7-flash:free outputs, 240 fact ids,
  4 blocks each. sha256 `bd1cbe59c3e776d1bc6f63c9a83cba408fd6e91684a28029be922311dbd4a02d`
- `corpus/raw/SHA256SUMS.txt` — raw output hashes
- `corpus/ERROR_INVENTORY.md` — mechanical inventory all zero; 12 deliberate
  false ids {3,29,55,71,80,103,117,139,163,178,205,231} reproduced faithfully
  (0 corrections/hedges corpus-wide)
- `prereg/PREREG_Q2_DISTILLATION.md` — frozen Q2 prereg (byte copy)

## Verbatim sources (hashes in src/SOURCES_SHA256.txt)
Q2/sol (from wave12/q2-distillation-sol/, 2026-09-21):
t5_core.zag, t5_arms.zag, t5_traps.zag, forcepin.zag, q2s_trial.zag, substrate/
Q1B §B.7 (from q1b-teacher-bakeoff/src/, 2026-09-21):
q1_types.zag, q1_proposal.zag, q1_tape.zag, q1_tripwire.zag,
q1_flawscore.zag, q1_world.zag, q1_learner.zag
Symbol-collision check across Q2+Q1 sets: none (verified by script).

## Generated files (byte-identical reruns verified)
- `src/s37_corpus.zag` — from `build/build_corpus_zag.py` (reads the frozen
  corpus, verifies sha256 + zero error inventory + retry ceiling).
  sha256 `99c3c4228e0cb4179e6562566f9a6be8530fe10e3bfdc83a9081b80448ef4aec`
- `src/q1_proposal_s37.zag` — from `build/build_driver.py`: verbatim
  q1_proposal.zag + ONE documented S37 delta (TB_TID_S37=20 in the §P
  ingress teacher-id allowlist; the Q1/Q1B deltas kept verbatim).
- `src/s37_trial.zag` — from `build/build_driver.py`: STEP header +
  q2s_trial.zag body verbatim (import block: s37_corpus.zag +
  q1_proposal_s37.zag + other Q1 sources; main() gains flaw4/teach3
  dispatch; argc-safe per ZNC-007) + src/s37_step.zag appended.
- `src/s37_step.zag` — hand-written STEP mechanisms (class 4 flaw4, class 3
  teach3, teacher id 20). Reviewed; compiles clean.

## S37 deltas vs frozen sources (all documented, none silent)
1. `q1_proposal_s37.zag`: TB_TID_S37=20 accepted at §P ingress (teacher-id
   allowlist extension; the documented mechanism for new teachers).
   Session seq-tracking default branch (last5) already correct for a
   single-teacher session.
2. `s37_trial.zag` main(): flaw4/teach3 dispatch added; usage strings updated.
3. Corpus accessor swapped (q2_corpus.zag → s37_corpus.zag).

## Toolchain
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
(`znc 2026.07.0-dev (edition 2026)`, observed 2026-09-21)

## Runs
`run_s37.sh`: 20 modes × 5 runs = 100 invocations, all exit 0, all 5 runs
of each (mode, rep) byte-identical (cmp-verified). Logs + SHA256SUMS in
evidence/logs/. Verdict in evidence/S37_VERDICT.md.
