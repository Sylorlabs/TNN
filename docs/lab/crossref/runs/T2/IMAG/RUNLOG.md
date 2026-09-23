# T2-IMAG — RUNLOG (replication crew)

Crew: T2-IMAG (REPLACEMENT). All times 2026-09-22/23 PDT. TMPDIR=/home/hatch/workspace/tmp_commit throughout. No /tmp use except one 6.5KB scratch read (deleted immediately).

## Inherited state (predecessor, killed by daemon restart)

- `crew/CREW_NOTES.md`: "Clone in progress: …/IMAG/clean/; Frozen pins target:
  7b2100d09911c5c10252c5756c7def288e70bd1f (prereg), expected trial commit
  a39aadf; znc: …/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 (verified
  exists); TMPDIR set to ~/workspace/tmp_commit".
- `clean/`: contained only an empty `.git` (no commits) — the clone never
  completed. No partial battery outputs, no VERDICT/RUNLOG to resume.
- Decision: re-clone from scratch; inherited notes recorded here.

## 04:06–04:10 — Setup attempt 1 (failed)

- `rm -rf clean && git clone --no-checkout https://github.com/sylorlabs/TNN.git clean`
  timed out at the 180s tool dispatch (full history too large).
- Verified the frozen prereg commit exists via gh-api:
  `7b2100d09911c5c10252c5756c7def288e70bd1f` ("crossref: scope + frozen
  preregs…", 2026-09-22T22:54:44Z). Decoded `PREREG_TIER2.md` blob
  `b1178370036bffbda6eb68ea0989c0e427dc31b7` (38,417 bytes) via git-blobs API
  + base64 decode; extracted the T2-IMAG section (lines 113–117) — quoted
  verbatim in VERDICT.md §1.
- Verified evidence pin `a39aadf` → `a39aadf6e563ca470c37a4770afbe350c023c98b`
  ("Imagination-design trial: mechanism, evidence, verdicts", 2026-09-22T05:07:31Z).

## 05:10–05:21 — Setup attempt 2 (partial, then wiped)

- `git init clean; git remote add origin …; git fetch --depth 1 --filter=blob:none
  origin a39aadf…` — succeeded in ~7s.
- Mapped trial paths via `git ls-tree`: everything lives under
  `docs/lab/imagination/` (src/imagine.zag, PREREG.md, RUN-LOG.md, VERDICT.md,
  verify_*.py, q1_procedures.txt, logs/, SHA256SUMS, Q1V-RESULTS.md,
  PROPOSED-amendment-video-2026-09-22.md).
- **Key discovery:** the trial VERDICT.md at `a39aadf` does NOT contain the
  video battery — at that commit it was only a PROPOSED amendment ("NOT
  APPLIED"). Commit history on `docs/lab/imagination` showed
  `4d1a40ecaa` (2026-09-22T05:26Z): "imagination: Q1V video battery PASS 12/12
  both modes" — the commit that introduced Q1V (+208 lines in imagine.zag,
  logs/q1vm_repN.txt, logs/q1vh_repN.txt, verify_q1v.py, Q1V-RESULTS.md).
  Later commits (9b7fb3d85c, 852e0b9317, ab51007283) only ADDED new files
  (emit.zag, field.zag, …); `git log -- path=…/imagine.zag` confirms the file
  was touched only by a39aadf and 4d1a40ecaa. So: Q1/Q3/control rerun at
  a39aadf (frozen pin), Q1V rerun at 4d1a40ecaa (pin correction documented in
  VERDICT.md §5.1).
- **Incident:** the stale `git clone` from attempt 1 (still alive after the
  tool timeout) was reaped late and deleted the recreated `clean/`
  directory. Detected via `ls` showing an empty dir; `ps` confirmed no
  remaining clone processes afterward. Recovered with a fresh
  `git init` + shallow blobless fetch (fast, no recurrence).

## 05:21–05:50 — Clean checkout + build environment

- Sparse checkout: `git sparse-checkout init --cone; git sparse-checkout set
  docs/lab/imagination; git checkout a39aadf` — 352K working tree,
  `git status` clean, `git fsck` clean.
- Import analysis: `imagine.zag` line 27:
  `@import("../../toolchain/R33_NATIVE_IO_V1.zag")`. No such path in the
  committed tree (only `docs/lab/wave1/toolchain/R33_NATIVE_IO_V1.zag`).
  Empirical probe: znc's error printed `../toolchain/R33_NATIVE_IO_V1.zag`
  when invoked as `src/imagine.zag` from the trial dir → this znc build
  resolves `@import` relative to the source file's directory. Substrate
  therefore belongs at `<trial>/../toolchain/R33_NATIVE_IO_V1.zag`
  (= `docs/lab/toolchain/`). Used the committed bytes from
  `docs/lab/wave1/toolchain/R33_NATIVE_IO_V1.zag` (identical at both pins —
  `git diff` between pins shows no change), placed in the scratch build
  mirror only (never in `clean/`).
- Build (mirror `crew/build`, CWD=`…/docs/lab/imagination`):
  `znc --no-zagd --no-analyze --no-foreground-cache src/imagine.zag -o src/imagine_bin`
  → "wrote native binary src/imagine_bin (**205365 bytes main**, 0 external
  tools)" — byte count EXACTLY matches the trial RUN-LOG ("205365 bytes
  after the 2026-09-22 Q3 rebuild"). Cleaned `.zag-cache`/`.zagd.semantic-ready`.

## 05:51–05:55 — Battery runs at a39aadf (3 reps each)

- `./src/imagine_bin q1 m all`, `q1 h all`, `q3 m`, `q3 h` → `runs/`
- SHAs: q1m `df2d1b1c…`, q1h `d5eede6f…`, q3m `f7f82ae0…`, q3h `cfbaecf8…` —
  all 3 reps byte-identical AND byte-identical to the committed
  `logs/*_repN.txt` (all 5 committed reps share one SHA each).
- Text-only control: patched copy of `verify_q1_textonly.py` with only the
  two hardcoded `/home/hatch/workspace/tnn-lab/imagination` path constants
  repointed to the local mirror (patch proven logic-identical by diff) →
  `runs/textonly.txt` SHA `71d3738f…` = committed `logs/textonly.txt`.
- Scoring: `verify_imag.py --q1m/--q1h` → 36/36 both modes (38 log lines,
  36 questions — documented farthest-pair double-line); `--q3m/--q3h` →
  machine 6/8, human 4/8, AGREE-1 MARGINAL, AGREE-2 NO-DIFFERENTIATION,
  per-pair scores identical to committed RUN-LOG table.

## 05:55–06:05 — Q1V video battery at 4d1a40ecaa (5 reps each)

- `git fetch … 4d1a40ecaa…; git checkout 4d1a40ecaa` in clean/ (sparse paths
  unchanged); built mirror `crew/build_v` the same way → 226401 bytes main.
- Diff `a39aadf..4d1a40ecaa -- imagine.zag`: 207 insertions (all Q1V),
  1 removed line (comment updated for domain 4=VIDEO). Q1/Q3 paths untouched.
- `./src/imagine_bin q1v m all` → `55b26e05…` (5/5 identical, = committed);
  `q1v h all` → `5bb44282…` (5/5 identical, = committed).
- `verify_q1v.py` → 12/12 both modes, PASS vs IMAG-V bar (≥9/12).

## 06:05–06:10 — Verification and deliverables

- `git checkout a39aadf` (clean/ resting state = primary frozen pin);
  `git status` clean; `git fsck --no-dangling` no errors.
- znc version recorded: `znc 2026.07.0-dev (edition 2026)`.
- No `.zagd`/`.zag-cache`/binaries committed anywhere; builds live only in
  `crew/build*/`.
- Wrote `crew/VERDICT.md` (frozen-section quote, checklist, byte-identity
  table, REPRODUCED verdict, pins, 6 caveats, auditor recipe) and this RUNLOG.md.

## Verdict

**REPRODUCED** — 36/36 both scene-QA modes, 2/36 control, 6/8 vs 4/8 taste
(MARGINAL, no winner), 12/12 both video modes; every log byte-identical to
committed digests. Q4 excluded per prereg. One pin correction noted: the
video battery's evidence commit is 4d1a40ecaa, not a39aadf (see VERDICT.md §5.1).
