# RUNLOG — T2-RAWVSHUMAN (replacement crew)

Crew: T2-RAWVSHUMAN (REPLACEMENT). Predecessor killed mid-run by runtime daemon
restart 2026-09-23. Session a3c5356a-cda7-4495-92d9-51ca4088956c.

## Inherited state (verified, not assumed)

- `clean/repo`: sparse clone of sylorlabs/TNN, HEAD detached at
  `7b2100d09911c5c10252c5756c7def288e70bd1f` (the frozen crossref commit).
  `git fsck --full`: clean except one dangling commit `3edd1486` (harmless).
  `git status`: working tree clean. Sparse checkout, 1% of files present —
  evidence extracted read-only via `git cat-file -p <pin>:<path>` (repo never
  mutated).
- `clean/dl.log`: predecessor's tarball download hit HTTP 404 — superseded;
  the clone is intact, so no re-clone was needed.
- `crew/`: empty. All run artifacts below were produced by this crew.

## Frozen pins (recorded BEFORE running; all verified present)

| Pin | Commit | Message (verified) | Date |
|---|---|---|---|
| prereg | `a87ddfd4c41f88710f5e573e9c0283d003360b6d` | Wave RAW-VS-HUMAN prereg (RDTDT TEST phase), 2026-09-22 | 2026-09-22 07:40 -0700 |
| diagnostics | `8954577204f5cd9ac772f071a213b3fb620a743c` | D1 diagnostic (RAW-VS-HUMAN wave), 2026-09-22 | 2026-09-22 08:09 -0700 |
| forks | `31c68a56fe7c012c543625465af6f1fd934e6212` | B2/B3 forks (RAW-VS-HUMAN wave): sources, grown tables, logs, verdict, 2026-09-22 | 2026-09-22 08:09 -0700 |

All three match the expected pins from the frozen T2 section. Nothing missing —
no STOP condition triggered.

## Checklist extraction (first task, done before any run)

Extracted verbatim from `docs/lab/crossref/PREREG_TIER2.md` § T2-RAWVSHUMAN
(line 203) at frozen commit `7b2100d`. Quoted in full in VERDICT.md §1.
Decision rule: REPRODUCED iff ≥99% in-bin attribution holds AND both rescues
stay <1pp; NOT REPRODUCED iff any rescue crosses +1pp or attribution <95%.

## Evidence used (committed only; read-only extraction)

From `8954577204f5` → `crew/evidence/`:
- `d1_colordisc_rows.jsonl` (600 rows), `d1_pitchdisc_rows.jsonl` (600 rows)
- `d1_results.json`
From `31c68a56fe7c` → `crew/evidence/`:
- `VERDICT_RAWVSHUMAN.md` (committed fork verdict tables)
- grow logs consulted in-repo: `b2/work_TRAIN_T1/grow_colordisc.log`,
  `b2/work_TRAIN_T1/grow_pitchdisc.log`, `b2/work_TRAIN_T2/grow_colordisc.log`,
  `b2/work_TRAIN_T2/grow_pitchdisc.log`; `b2/grown_T2.zag` sha256 recomputed.
From `1c01a1ad` (frozen rematch background, cited by wave prereg):
- `docs/lab/senses/rematch/VERDICT.md` (ops, KB4, gap figures).

Non-interference: no live-workstream files touched; no scratch of other crews
read. The original `d1.py` read external uncommitted paths
(`/home/hatch/workspace/senses-rematch`, `senses-rebuild/harness`) — those are
not committed evidence and were NOT used; the re-derivation runs on the
committed rows instead.

## Builds (pure Zag; znc pinned toolchain)

- Toolchain: `/home/hatch/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
  (`znc 2026.07.0-dev`), run with `TMPDIR=/home/hatch/workspace/tmp_commit`.
- `crew/zag/io.zag`: copy of `~/workspace/tnn-lab/toolchain/R33_NATIVE_IO_V1.zag`
  (nio_alloc/cstr/equal only).
- `d1_verify.zag` — Type A rerun of D1: parses committed rows, re-derives
  error from (judgment vs truth), same-handle/bin from (p1==p2), sub_semitone
  from rel_pitch via exact scaled-integer compare vs 2^(1/12)-1; cross-checks
  every precomputed flag (0 mismatches required); applies the ≥99%/<95% rule.
- `rescue_verify.zag` — Type C re-derivation: exact-fraction mechanism
  diagnostics (B2 = 1/360, B3 = 1/120), ALIVE-bar re-application, grow-log
  adoption-rule check (every adopted cut gain ≥ 10‰; counts 4/5/0/2).
- `context_verify.zag` — Type C re-derivation of context figures: ops ratio
  413890710/171235328, B−A gap, KB4 rates 55/114 and 72/132.
- Note: a first-draft `context_verify` had a units bug (thousandths labeled as
  hundredths, caught because `expect_242` printed 0). Fixed to
  `(r10000+50)/100`; re-verified 3× byte-identical after the fix. Documented
  here per honest-reporting; the fix is in the final source.

## Runs (each ≥3, byte-identical digests)

| Program | Output digest (sha256, ×3 identical) |
|---|---|
| `d1_verify` | `c9e6733e82e4d86336e94aacf0187f97636c5611203675c1f0a2c624acfbb61f` |
| `rescue_verify` | `b576517bc427051dc24b30ede36d7292a64781cb8517a42bc4f729ed8a0d002a` |
| `context_verify` | `a21c8bef208fe890679eacf234d33d271d79294b9e89061682222ea2b3cf0d85` |

Run outputs in `crew/runs/` (`d1_run{1,2,3}.txt`, `rescue_run{1,2,3}.txt`,
`context_run{1,2,3}.txt`).

Key measured outputs:
- `d1_verify`: color n=600 errors=506 same_handle=505 att_pm=998;
  pitch n=600 errors=132 subsemi=132 within=131 att_pm=992;
  flag agreement: 0 mismatches on all 5 flag classes;
  rule: color_ge99=1 pitch_ge99=1, no <95% trigger.
- `rescue_verify`: b2_diag_t1 = 1/360 = 0.278pp; b2_diag_t2 = 0;
  b3_diag = 1/120 = 0.833pp (T1 and T2); all < 1pp;
  ALIVE bars: b2t1=0 b2t2=0 b3t1=0 b3t2=0 (all DEAD);
  grow cuts 4/5/0/2, all gains ≥ 10‰.
- `context_verify`: ops ratio = 2.42 ✓; gap = −272‰ → −27pp ✓;
  KB4 A = 48.2% (55/114), B = 54.5% (72/132): both > 10% bar, both ~50% ✓.
- `b2/grown_T2.zag` at `31c68a56fe7c`: sha256
  `92c3c844b06d5156debf9ecdbb644120b8ec72747940db4c63877303a420e9c4`
  — matches the committed determinism table exactly (original + 2 reruns).

## Rounding-provenance notes (do not affect any verdict)

1. Committed B3 diagnostic "+0.85pp" vs exact +0.833pp (1/120): the committed
   figure subtracts 1-decimal 56.7−55.0 = 1.7pp then halves; exact counts give
   (34/60−33/60)/2 = 1/120 = 0.833pp. Both < 1pp; rule outcome unchanged.
2. Committed B2-T1 "+0.3pp" vs exact 1/360 = 0.278pp: same class of 1-decimal
   artifact. Both < 1pp; unchanged.
3. Committed "−27.1pp" headline vs −27.2pp from 1-decimal 56.6−83.8: exact
   means (56.617−83.75 = −27.13) give −27.1pp. The T2 claim "−27pp" holds under
   both. Unchanged.
4. Committed `d1_results.json` carries a withdrawn band-based color "D1" field
   (0.8794). Per D1_REPORT.md's correction note it is superseded; the binding
   figure is the no-band same-handle fraction (505/506 = 99.8%), which is what
   this crew re-derived.

Zero RNG used anywhere. No binaries or .zagd committed (nothing committed at
all — deliverables are VERDICT.md + RUNLOG.md in `crew/`). Slices < 2^25.
Scratch only under `~/workspace/scratch-crossref/T2/RAWVSHUMAN/`; `/tmp` untouched.
