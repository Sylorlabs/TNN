# Documentation Audit — 2026-09-21

**Crew:** documentation audit
**Branch:** `tnn-native-lab` (sylorlabs/TNN)
**Method:** recursive repository tree (~40,600 blobs) compared by git blob-SHA
against local files under `~/workspace/tnn-lab/` (staging layout → `docs/lab/<rel>`),
`~/workspace/docs/lab/` (repo-layout mirror), and selected `~/workspace/` roots.
Missing = local file whose SHA appears nowhere in the repo tree.
Stale = same path in both, SHAs differ (direction resolved per file below).

## Commits made by this audit

| SHA (short) | Contents |
|---|---|
| `a06216f824bb` | Ops logs: `ops/MORNING_BRIEF_2026-09-21.md`, `ops/NIGHT_RUN_2026-09-21.md` (snapshots; logs keep growing locally) |
| `11ff63f32660` | Verdict/spec updates where local is newer: C-P, Y5, O, Z8 verdicts; Z8 scorecard; D BUILD_LOG; F-S sweep_run2; r0 ARM_SPEC + INTERFACE |
| `ffe25a09c70b` | Recovered verdicts/specs: P arm (4 files), D-T draft (3), D draft verdict, K1 (2), W spec, Y5 work build log |
| `63b5bed8b040` | Closeout & verification: Track A SECTION_SPOTCHECK, Track 5 t5-verify (verdict sheet + independent scorer), championship Q2 materials, Q1 evidence runs (5) |
| `dee0356f0ab8` | Past work: b_t1_closeout verdict sheet, manifests, addendum, grounded-bug note, scorecards, corpora manifest |
| `3edd590ce40b` | Cleanup: removed 4 double-prefixed `docs/lab/docs/lab/units/arms/M/...` duplicates |
| `772ed08219ca` | Evidence summaries: 427 STATUS.txt / GATE.txt / scorecard files for completed arms |

## Files committed (new to repo)

**Ops:**
- `docs/lab/ops/MORNING_BRIEF_2026-09-21.md`
- `docs/lab/ops/NIGHT_RUN_2026-09-21.md`

**Verdict/spec updates (local newer):**
- `docs/lab/units/arms/C-P/VERDICT.md` (commit hash filled in)
- `docs/lab/units/arms/Y5/VERDICT.md` (commit hash filled in)
- `docs/lab/units/arms/O/VERDICT.md` (M1 measurements filled in)
- `docs/lab/units/arms/Z8/VERDICT.md` + `scorecard_r1_1x.json` (marathon crew U3 binding PASS; supersedes UNADJUDICATED)
- `docs/lab/units/arms/D/BUILD_LOG.md` (D-DBG performance-optimization notes)
- `docs/lab/units/arms/F-S/work/sweep_run2.txt` (updated sweep output)
- `docs/lab/units/r0/impl/arms/ARM_SPEC.md` (§8: L_max 8/12 test-both leg)
- `docs/lab/units/r0/impl/arms/INTERFACE.md` (accompanying spec touch-up)

**Recovered (never committed before):**
- `docs/lab/units/arms/P/{ARM_SPEC.md,BUILD_LOG.md,VERDICT.md,scorecard_1x.json}` — P is a PASS arm whose verdict was staged under a `docs/lab/` prefix and never landed
- `docs/lab/units/arms/D-T/{ARM_SPEC.md,BUILD_LOG.md,VERDICT.md}` (draft)
- `docs/lab/units/arms/D/VERDICT.md` (draft)
- `docs/lab/units/arms/K1/{ARM_SPEC.md,BUILD_LOG.md}`
- `docs/lab/units/arms/W/cl/ARM_SPEC.md`
- `docs/lab/units/arms/Y5/.work/BUILD_LOG.md`

**Closeout / verification:**
- `docs/lab/tracka-closeout/SECTION_SPOTCHECK.md`
- `docs/lab/wave12/track5-binding/t5-verify/{TRACK5_VERDICT_SHEET.md,independent_score.py}`
- `docs/lab/wave12/championship/{q2_prompt_set.md,muse_team/freeze_corpus.py,muse_team/gate_watch.sh}`
- `docs/lab/q1-planted-teaches/evidence-runs/q1_run{1..5}_run{1..5}.txt`

**Past work (b_t1_closeout):**
- `docs/lab/scratch/b_t1_closeout/stage/{VERDICT_SHEET.md,PROBE_MANIFEST.md,RUN_MANIFEST.md,CLOSEOUT_ADDENDUM.md,GROUNDED_BUG.md,rank_table.json,corpora.json,scorecards/*.json}`
- `docs/lab/scratch/b_t1_closeout/{RUN_MANIFEST.txt,runs/RUN_MANIFEST.txt}`
- `docs/lab/corpora/r1/MANIFEST.json`

**Evidence summaries:** ~427 `STATUS.txt` / `GATE.txt` / scorecard / manifest files for arms with committed verdicts.

## Deliberately excluded (with reasons)

1. **Raw per-run stdout/stderr/rc/rss dumps** (~7,000 files under `units/*/work/`, `wave12/`, `wave2/`, `scratch/`). Machine scratch: reproducible via byte-identical reruns, and crews curate their own evidence sets (precedent: H1's full battery set was committed by its own crew). Not bulk-committed.
2. **In-flight arm evidence** (V, W, F-S, F-B, I1, K1, K3, O, U, Y4, Z1, D, D-T, D-R, T work dirs). Crews still running; they commit final evidence at completion.
3. **Repo-newer files — never overwritten.** Verified by diff that the committed version is the newer/corrected one:
   - `units/arms/M/VERDICT.md` (repo carries the corrected M-dedup result; local lacks it)
   - `tracka-closeout/TRACKA_VERDICT_SHEET.md` (repo: T=KILLED, 17/20/12/3; local draft: T provisional)
   - `wave12/step1a-v2/redteam/SCORECARD.md` (repo: completed v2 kill results; local: pending template)
   - `wave6/doc-front/INTEGRITY_HEADLINE.md` (repo: 4,800-episode stretch; local: unrun)
   - `wave8/strength-retrial/PREREG_STRENGTH_V2.md` (repo: dated restoration note; local truncated)
   - `wave12/track5-binding/src/t5_traps.zag` (repo: repaired; local: pre-repair)
   - `wave8/strength-retrial/trial/strength_core.zag` (repo longer/newer)
   - External mirrors (`~/workspace/docs/lab/...`, `~/workspace/q_verdict.md`, `~/workspace/tracka-closeout/`, `~/workspace/units/docs-.../`) — all older than repo versions; left alone.
4. **Arm sources (`cl/arm.zag`)** for D, D-R, F-B, Z1, Z3. Active crew work; provenance unclear; crews commit their own sources.
5. **Binaries, `.zagd`, `.zag-cache`, `node_modules`, `.seg` outputs, corpora binaries** — per standing rule, never committed.
6. **Older duplicate mirrors** (`units/arms/M/docs/`, `units/arms/Z5/docs/lab/...`, `units/arms/q/` lowercase). Repo holds authoritative versions at canonical paths.

## Duplicates fixed

Removed 4 accidentally double-prefixed files under `docs/lab/docs/lab/units/arms/M/` (ARM_SPEC.md, BUILD_LOG.md, VERDICT.md, scorecard-1x.json). Authoritative copies at `docs/lab/units/arms/M/...` (with the newer corrected content).

## Unresolved references (flagged, not fixed)

These documents reference files/paths not found in the repo tree OR locally. Flagged for the owning crews; not fabricated.

- `docs/lab/wave12/championship/muse_team/` materials reference a frozen Q2 corpus — corpus location to be confirmed by the championship crew.
- Several arm VERDICT.md files reference `work/` evidence paths by crew-local absolute paths (`/home/hatch/workspace/...`); these resolve locally but not in the repo. Future verdicts should use repo-relative evidence paths.
- The audit did not verify every cross-reference in all 40k+ blobs; a full link-integrity sweep is recommended as follow-up.

## Coverage note

~8,900 local text-like files remain uncommitted, the large majority being raw per-run
machine output (see exclusion 1). The canonical evidence layer — verdicts, specs,
scorecards, manifests, status summaries, closeout sheets, and ops logs — is now in
the repo. Crews with in-flight work commit their own final evidence at completion.
