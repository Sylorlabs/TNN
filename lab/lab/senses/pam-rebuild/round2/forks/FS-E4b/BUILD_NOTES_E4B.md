# BUILD_NOTES_E4B

## Front-end vendoring

- `src/r27fe.zag` is a copy of `forks/R2-7/src/r27.zag`
  (sha256 `316b018d96b87967eb574d7e27c939fec8c61f721d67522a6bd4ab3d9a58883f`)
  with exactly one line changed: `fn main() void {` (line 1945) renamed to
  `fn r27_main_disabled() void {`. znc rejects duplicate `fn main` on
  `@import`; the rename keeps every formation/challenge function
  byte-identical logic. Verified: `diff` shows only line 1945.
- `src/R33_NATIVE_IO_V1.zag`, `src/R33_NATIVE_SHA256_V2.zag`: copied from
  `forks/R2-7/src/` (r27fe.zag imports them relatively, same as r27.zag).

## Driver (`src/e4b.zag`)

- `@import("r27fe.zag")`. Two modes:
  - `e4b judge <fixture> <ledger> <trial_id>` — one trial.
  - `e4b judge_list <listfile> <ledger>` — batch; listfile lines
    `<fixture_path> <trial_id>`; stdout lines appended to `<ledger>.out`
    (via dup2, fd 1), one hash-chained ledger line per trial appended to
    `<ledger>`. Per-trial logic identical to single mode (same function,
    same call order); order = listfile order, so the ledger chain matches
    sequential single runs.
- Per trial: `run_formation` on F-span → formF; `run_formation` on G-span →
  formG (same front-end, disjoint bytes); `run_challenge` on G-span → o, cs.
  base = INSTALL iff `o>=0 && chal_supports(task, formF, cs)==1` (R2-7's full
  mode exactly). booster = INSTALL iff `formF==formG && base==INSTALL`.
- Truth from `<fixture>.truth` sidecar. Trial id = explicit arg (single) or
  listfile field (batch). Stdout/ledger lines are single-line, deterministic
  (no timestamps/pointers). Reuses R2-7's `append_ledger` (sha256 chain)
  verbatim. Buffer cap 300000 B (largest fixture: motiondir 102432 B).
- znc quirk hit: declared a helper param as `i32` while passing `[]u8`
  (`e4b_split_line`); fixed the signature. No other build issues.

## Build

- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
  (pinned).
- `znc e4b.zag -o <bin> --no-zagd --no-analyze --no-foreground-cache`
  (from `src/`, so the relative `@import`s resolve).
- Binary lives in workspace scratch only (`~/workspace/tmp_e4b/e4b_bin`);
  NEVER committed. Rebuilt deterministically from source.

## Smoke test (base parity vs frozen R2-7)

- Built `r27.zag` from the frozen source with the same toolchain/flags
  (scratch only).
- 5 fixtures (colorconst, colordisc, pitchdisc, motiondir, timbredisc):
  `disposition=` (r27 full) == `base=` (e4b) on all 5; `judgment=` ==
  `formF=` on all 5. ops differ exactly by the extra formG run (e.g.
  colorconst 13944 vs 9296), as designed.
- Batch mode output on the same 5 fixtures byte-matches single-mode output.

## Fresh draw (PREREG_FS-E4b §Batteries)

- `work/draw_e4b.py` imports `forks/R2-7/src/gen_r2a.py` (frozen) as a
  module. MASTER=20260923; adversarial: indices 200000–207999 (8,000),
  stream 500+tidx, family `fams[j % len(fams)]`; normal: indices
  100000–101499 (1,500), stream 400+tidx, family 0. No `random` module
  anywhere. Filenames `r2a_<task>_<idx>` / `r2n_<task>_<idx>` under
  `fixtures/cand/<task>/`.
- Execution detail (not a procedure change): the five tasks' draws ran as
  five parallel processes (same seeds → identical bytes), each with a
  per-task ledger; `draw_e4b.py <cand> finalize` concatenates the ledgers in
  TASKS order and writes the sorted `MANIFEST.e4b_cand.sha256`. Resumable
  via the per-task ledgers.
- Candidate judging: `work/judge_all.py` builds per-task list files and
  runs `e4b judge_list`; `.out` parsed to `evidence/judgments_cand_<task>.tsv`.
- Selection: `work/select_battery.py` (F-fooled = formF != truth, first 2000
  in idx order; TRUE = first 1000 normals in idx order; qualification rule
  applied mechanically).
- Corrupted-G: `work/corrupt_g.py` (family=9; header rewritten; donor = first
  F-fooled candidate with fooled judgment != T).
- Battery runs: `work/run_battery.py` (run1/run2, cmp byte-identical).
- Chain verification: `work/verify_chain.py` (independent Python recompute).
- Scoring: `work/score_e4b.py` (Wilson 95% UCB, bars, verdict text).

## Disk

- Candidates: ~3.8 GB under `fixtures/cand/` (workspace only, not committed;
  regenerable byte-identically; committed manifest verifies).
- Battery (15,000) + corrupted-G (~5,000): ~2 GB under `fixtures/`.
- Non-selected candidates are kept (not deleted) for auditability.
