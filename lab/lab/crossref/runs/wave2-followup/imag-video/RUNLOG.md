# T2-IMAG video battery — RUNLOG (weirdness-removal crew)

All times 2026-09-24 PDT (UTC−7). TMPDIR=/home/hatch/workspace/tmp_commit
throughout. No /tmp use. Pinned znc:
`/home/hatch/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
(`znc 2026.07.0-dev (edition 2026)`).

## 08:32–08:36 — Setup: read prior crew state, verify pins via API

- Read `~/workspace/scratch-crossref/T2/IMAG/crew/{VERDICT,RUNLOG,CREW_NOTES}.md`
  and `~/workspace/scratch-crossref/T2/_wave2_tally/VERDICTS.md` (T2-IMAG
  sections). Decision: fresh fetch into `video/clean/` rather than reusing
  the prior crew's checkout (vanishing-tree incidents in this program make
  re-fetch the safer call; nothing was wrong with their checkout).
- `gh-api GET /repos/sylorlabs/TNN/commits/<sha>` for both full SHAs —
  both EXIST with expected messages/dates:
  - `a39aadf6e563ca470c37a4770afbe350c023c98b` ("Imagination-design trial:
    mechanism, evidence, verdicts", 2026-09-22T05:07:31Z).
  - `4d1a40ecaaecaf53cd13cf492737f605d17f35a2` ("imagination: Q1V video
    battery PASS 12/12 both modes; …", 2026-09-22T05:26:06Z).
- `git init video/clean`; `git fetch --depth 1 --filter=blob:none` for both
  SHAs (~15 s each). Created `video/` dir.

## 08:36–08:42 — Independent diff a39aadf..4d1a40ecaa

- `git diff --name-status` / `--stat` on `docs/lab/imagination/`: 21 files,
  1271 insertions, 11 deletions. Enumerated every file (see VERDICT §1).
- `git diff --numstat -- src/imagine.zag`: **207 insertions, 1 deletion** —
  matches the prior crew's number, re-derived independently.
- Saved full unified diff; verified line-by-line:
  - 1 deletion = comment line `w0 domain (1=V 2=A 3=S)` →
    `(1=V 2=A 3=S 4=VIDEO)`. Comment-only.
  - Insertions = 5 comment lines (VIDEO layout docs) + 15 new functions
    (`ig_qv_*`, `ig_q1v_*`) + one `q1v` dispatch branch in `main()`.
  - `grep -c "q1v\|qv_"` on the a39aadf source: **0** — no name collisions;
    all 15 new fn names have 0 definitions in the old source.
  - The `q1v` branch sits between two existing branches that each `return 0`
    before reaching it; string-equality conditions are mutually exclusive.
- Other modified files: `PREREG.md` (1-line pitch wording CORRECTION),
  2 doc renames (R079/R088, status NOT APPLIED → APPLIED, 8 and 5 lines),
  `RUN-LOG.md` (Q1V entry), `SHA256SUMS` (**insertions only**, 14 lines —
  no Q1/Q2/Q3/control hash touched). New files: Q1V-RESULTS.md,
  TASTE-PROBE.md, verify_q1v.py, 10 Q1V logs, gallery_src/{RENDER-NOTES.md,
  render_gallery.py}.
- Substrate `docs/lab/wave1/toolchain/`: empty diff between pins —
  byte-identical; single copy reused for both builds (blob `a6b440d2…`).

## 08:42–08:47 — Checkout + build at 4d1a40ecaa, full battery runs

- `git sparse-checkout set docs/lab/imagination`; `git checkout 4d1a40ecaa`;
  `git status` clean, `git fsck --no-dangling` clean.
- Q2 documentation read: `Q2-VERIFY.md` (GEN-1/GEN-2/GEN-3 tables),
  committed SHAs (`q2m 7a0b3cf7…`, `q2h b4105a25…`), verifiers
  `verify_q2_gen.py` (argv-driven) / `verify_q2_gen3.py` (hardcoded lab
  paths — noted for patching).
- Import-path handling (same as prior crew): `imagine.zag` does
  `@import("../../toolchain/R33_NATIVE_IO_V1.zag")`, resolved by this znc
  relative to the source file's dir → substrate placed at
  `video/build/docs/lab/toolchain/R33_NATIVE_IO_V1.zag` (committed bytes
  only; never in `clean/`).
- Build: `znc --no-zagd --no-analyze --no-foreground-cache src/imagine.zag
  -o src/imagine_bin` → **226401 bytes main** (== prior crew's 4d1a40ecaa
  build). Cleaned `.zag-cache`/`.zagd.semantic-ready`.
- Runs (3 reps Q1/Q2/Q3, 5 reps Q1V): all reps byte-identical per leg; SHAs
  — q1m `df2d1b1c…`, q1h `d5eede6f…`, q2m `7a0b3cf7…`, q2h `b4105a25…`,
  q3m `f7f82ae0…`, q3h `cfbaecf8…`, q1vm `55b26e05…`, q1vh `5bb44282…` —
  every one matches committed SHA256SUMS (formal per-leg cross-check, 8/8
  MATCH).

## 08:47–08:50 — Scorers

- `verify_q1v.py`: 12/12 both modes (PASS vs IMAG-V ≥9/12).
- `verify_q2_gen.py` (unmodified): GEN-1 **12/12**, GEN-2 **12/12**.
- `verify_q2_gen3.py`: patched COPY in `video/scratch/` with only the two
  hardcoded log paths repointed to this run's logs (diff-proven path-only;
  its `sys.path`-injected `verify_imag` is byte-identical to committed,
  sha256 `9b694e45…`): GEN-3 **24/24**, all ported==hand-traced.
- `verify_imag.py`: Q1 **36/36** both modes (72/72); Q3 machine **6/8**,
  human **4/8** → MARGINAL, NO-DIFFERENTIATION; per-pair detail matches the
  committed RUN-LOG table exactly.
- Text-only control: patched COPY of `verify_q1_textonly.py` (single
  hardcoded procedures path repointed to the build mirror; diff-proven
  path-only): **2/36** both modes (hits scene 5 q1, scene 7 q1, answer=4);
  stdout byte-identical to committed `logs/textonly.txt` (`71d3738f…`).

## 08:50–08:54 — Q2 at its evidence pin (a39aadf)

- `git checkout a39aadf` in clean/; mirror `video/build_old/`; substrate
  copy (byte-identical between pins, verified).
- Build → **205365 bytes main** — exactly the trial RUN-LOG's "205365
  bytes after the 2026-09-22 Q3 rebuild".
- `q2 m` / `q2 h`, 3 reps: q2m `7a0b3cf7…`, q2h `b4105a25…`, 3/3 identical,
  = committed SHAs.
- Scorers on the a39aadf logs: GEN-1 **12/12**, GEN-2 **12/12**, GEN-3
  **24/24** (path-repointed verifier copy, diff-proven).
- `git status` clean; clean/ left resting at `a39aadf`.

## 08:54–08:55 — Deliverables

- Wrote `video/VERDICT.md` (diff table, Q2 results, full-battery table,
  pin-amendment justification, CLEAN declaration) and this RUNLOG.md.
- No commits made (coordinator owns the single publication commit). No
  `.zagd`/`.zag-cache`/binaries in any checkout. No vanishing-tree or other
  incident this run.

## Verdict

**CLEAN.** Pin amendment `a39aadf + 4d1a40ecaa` justified; Q2 re-derived
12/12 / 12/12 / 24/24 at both pins; full battery byte-identical at the
amended pin. No remaining weirdness.
