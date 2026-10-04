# REPO-SCOPE Assessment: ~142k untracked files (wave-20261001-2321pdt)

Worker: REPO-SCOPE replacement worker. Read only assessment; nothing restored or committed by this lane.
Working copy: ~/workspace/tnn-rsi, branch tnn-native-lab. HEAD = 69f91f459.
Deletion commit under review: f461e812d (2026-10-02 07:19:22 UTC, H5R2-SKEPTIC2 implementation).

## 1. Count and total size

- Untracked files on disk (in `git ls-files --others --exclude-standard`, not in HEAD): **140,541**
- Total size: **6,724,942,963 bytes (6,413.4 MB, 6.26 GB)**
- HEAD tracks **6,322 files, all of them inside** `docs/lab/rsi/runs/wave-20261001-2321pdt/` (the current wave dir). Zero tracked files exist outside the wave dir.
- Every one of the 6,322 tracked wave-dir files is present on disk (verified, none missing).

## 2. Breakdown by top-level directory

| Directory | Files | Bytes | MB |
|---|---|---|---|
| docs | 140,331 | 6,699,835,367 | 6,389.5 |
| src | 63 | 22,651,767 | 21.6 |
| archive | 56 | 1,005,311 | 1.0 |
| artifacts | 14 | 605,989 | 0.6 |
| root (README.md, LICENSE, .gitignore, LOOP_STATE.md, .wave_lock, err/run*.err) | 9 | 445,605 | 0.4 |
| .github | 39 | 238,925 | 0.2 |
| imagination | 10 | 63,344 | 0.1 |
| video-repro | 9 | 39,479 | 0.04 |
| video-combine | 7 | 31,647 | 0.03 |
| units | 2 | 25,368 | 0.02 |
| data | 1 | 161 | 0.0 |

Sub-breakdown of the large dirs (files / MB):

- docs/generations: 35,475 files / 2,559.2 MB (R33: 32,484 files / 1,859.0 MB; R32: 1,033 files / 582.7 MB; R39/R38/R34/R36/R37/R41/R40/R31 the rest)
- docs/lab: 104,813 files / 3,829.9 MB, including:
  - docs/lab/rsi: 20,100 files / 1,162.7 MB (of which docs/lab/rsi/runs: 19,592 files = prior wave run dirs, Sept 24 through Oct 1; the current wave dir is NOT among them)
  - docs/lab/senses: 14,007 files / 484.8 MB
  - docs/lab/wave9: 12,380 files / 11.1 MB
  - docs/lab/knowledge: 11,995 files / 17.2 MB
  - docs/lab/research-lead: 10,532 files / 205.1 MB (includes tnn2_build and core_freeze_tnn2_shim)
  - docs/lab/deliberation_depth: 7,383 files / 188.7 MB
  - docs/lab/wave12: 4,991 files / 26.1 MB
  - remainder spread over wave8, training_paradigms, prose-learning, epistemic_native, liharden, composition, coding, math_logic, audio_longhorizon, and other prior lab lanes

## 3. What kinds of files they are

Extension counts (top): txt 26,442; zag 12,253; log 12,110; err 10,175; out 9,333; tsv 7,685; md 7,483; stderr 7,204; stdout 7,020; no extension 6,108; json 4,388; exit 4,165; truth 3,326; bin 3,218; argv 2,886; command 1,796; trace 1,625; jsonl 1,441; wav 1,152; pair 952; sha256 950; img 941; path 718; pcm 585; sh 571; f32le 551; png 438; bmp 431; rc 376; ledger 320.

Composition summary:

- **Run artifacts, dominant class (well over 100k files):** prior wave run logs, stdout/stderr captures, exit codes, argv/command records, run telemetry, truth files, traces. These are the execution exhaust of earlier waves and generations, not source.
- **Experiment sources (12,253 .zag):** R32/R33 negative-result experiment sources, native driver .zag files (R33_NATIVE_*), older lab lane experiment files, wave-12/8/5 sources. Historically valuable (they back prior negative verdicts) but superseded by committed wave records.
- **Documentation (7,483 .md + INDEX files):** prior lane briefs, judge briefs, preregs, verdicts, composition/senses/knowledge lane docs.
- **Large binary blobs:** recovered stdout blobs in R33 lane B logs (40 to 54 MB each; the single largest files), R32 .joblib/.npz model artifacts (40 to 43 MB), R27/R28/R30 tar.gz/zip run shadows (43 to 45 MB). These drive most of the 6.26 GB.
- **Toolchain and CI (src/, .github/):** the three znc compiler binaries, znc provenance JSON, build logs, probe sources, GitHub workflow and CI scripts.
- **Media and misc:** wav/pcm/bmp/png/img from senses/imagination lanes, ledgers, sha256 manifests.

## 4. Critical-file check

The frozen TNN-2 battery pins three artifacts by path and SHA-256 in the tracked prereg
(`docs/lab/rsi/runs/wave-20261001-2321pdt/BATTERY/PREREG_POSTFREEZE.md`, section 0).
All three exist on disk, NONE are in HEAD, and all three verify byte-identical:

| Artifact | On-disk path | In HEAD? | SHA-256 matches pinned value? |
|---|---|---|---|
| tnn2.zag | docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag | No (untracked) | Yes: a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd |
| freeze_shim2_bin | docs/lab/research-lead/overnight-20260928/core_freeze_tnn2_shim/freeze_shim2_bin | No (untracked) | Yes: 9217054c5af6dec057c4530c4de3ba246f521acc6df741d1989a4504acc72954 |
| znc linux x86_64 (pinned compiler) | src/tools/toolchain/znc_linux_x86_64_abed8aa1 | No (untracked) | Yes: 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef |

Additional critical notes:

- The worker toolchain guard's safebin links `znc` to `src/tools/toolchain/znc_linux_x86_64_abed8aa1`, an untracked path. A fresh clone of this branch would have NO compiler at all (nothing outside the wave dir is tracked). The toolchain works today only because the untracked files happen to be on this disk.
- `src/tools/toolchain/R32_ZNC_PROVENANCE_2026-08-23.json` (provenance record for the pinned compiler, including the Sylorlabs/zag source refs for rebuilding it) is on disk, untracked.
- The frozen battery's PF-K3 kill bar (frozen binary integrity) depends on these three untracked artifacts being at their frozen paths. The wave can continue today, but the freeze evidence lives entirely outside version control.
- The .github workflows/CI scripts and archive tarballs are on disk, untracked; CI is not used by the local-only loop.
- Root files (README.md, LICENSE, .gitignore, LOOP_STATE.md, .wave_lock) were never in this branch's HEAD; they exist on disk untracked.

## 5. Recommendation

**Recommendation: do NOT restore the 140,541 files into HEAD. Selectively protect a small pinned set; leave the bulk untracked.**

Reasons:

1. **Restoring everything is harmful.** 6.26 GB of historical run logs, stdout blobs, and superseded experiment output would poison the repo for every future worker (clone/checkout cost, index operations like the one that caused this incident get slower and more dangerous). The established pattern is that research output is committed per wave inside the wave dir, not as bulk history.

2. **The wave does not need the bulk to continue.** The current wave is fully self-contained in HEAD (6,322 tracked files, all present). The 19,592 prior-wave run files and 35,475 generation-output files are evidence exhaust from earlier work, not inputs to current experiments.

3. **But the freeze-critical artifacts are load-bearing and unprotected.** The frozen TNN-2 battery's integrity kill bar (PF-K3) and the worker toolchain guard both depend on files that exist only as untracked bytes on this one disk. A `git clean -fdx`, a fresh clone, a VM replacement, or a worktree checkout would silently destroy them, breaking: (a) re-running or replicating the post-freeze battery, (b) the safebin toolchain for every future worker, (c) the provenance chain for the pinned znc.

4. **Reproducibility of the record, not just the code.** The 140k files are the audit trail behind prior verdicts (negative-result experiment sources, lineage records, checksums). Micah's governance treats contamination and evidence loss as first-class failures. Deleting them is not the same as never having them.

Proposed handling (for Micah's decision):

- (a) Track a minimal pinned set in a dedicated commit or as an annex: the three znc binaries, `R32_ZNC_PROVENANCE_2026-08-23.json`, `tnn2_build/tnn2.zag`, `core_freeze_tnn2_shim/freeze_shim2_bin`, and their freeze evidence files. This is on the order of 30 files / ~30 MB and directly protects the frozen-battery kill bars and the toolchain guard.
- (b) Take a protective snapshot of the full untracked set (tar + sha256 manifest) stored alongside the existing git bundle backups (bundle v16 pattern), recorded in the wave RECORD. This preserves the audit trail without putting 6.26 GB into git.
- (c) Leave the bulk untracked, and record explicitly in the wave dir that `git clean -fdx` is forbidden in this working copy until (a) and (b) are done, because the freeze artifacts currently live in untracked space.
- (d) Do NOT restore .github workflows, archive tarballs, or media into HEAD; they are dormant.

Caveat: this lane did not verify the provenance or integrity of the bulk 140k beyond the three frozen artifacts and the znc binary (SHAs verified above). If Micah wants the audit trail to be independently re-verifiable, a checksum manifest pass over the full untracked set is the next step before any snapshot.
