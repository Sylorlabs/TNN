# NAMECHECK.md - LANE-AUDIT (wave-20261001-2321pdt)

## Step 0: Worker toolchain guard verification

- Ran: `cd ~/workspace/tnn-rsi && sh docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh && export PATH="$HOME/safebin"`
- Safebin output: `safebin: /home/hatch/safebin`, `linked: 36 tools`, `znc: OK`, `verify: python3 absent from safebin PATH (OK)`, `verify: python absent from safebin PATH (OK)`, `SAFEBIN-READY`
- `which python3`: prints nothing (exit code 1)
- `which python`: prints nothing (exit code 1)
- Guard check: PASS. No forbidden interpreter resolvable in PATH. Pure Zag for any computational work; shell only for git/file ops.

## Lane scope

Replacement worker for LANE-AUDIT, wave wave-20261001-2321pdt. Git hygiene incident: commit f461e812d (H5R2-SKEPTIC2 implementation) deleted thousands of files across nearly every wave lane. Task: audit every lane directory under docs/lab/rsi/runs/wave-20261001-2321pdt/ for files deleted by f461e812d that have NOT been restored, restore still-missing files from f461e812d^, and commit restorations under the affected lane's directory.

## Audit steps (record)

1. Deleted set: `git diff-tree --no-commit-id --name-status -r f461e812d`, status D only. 147,296 files repo-wide; 4,833 under the wave dir.
2. HEAD presence: `git ls-tree -r HEAD --name-only -- <wave dir>` (1,218 files at audit start). Split: 25 present in HEAD (already restored by lane workers), 4,808 still missing.
3. Deliberate-deletion check: `git log --diff-filter=D --name-only f461e812d..HEAD -- <wave dir>` returned empty. No lane worker deliberately deleted anything after the incident.
4. On-disk verification: all 4,808 still-missing files existed on disk as untracked files. Per-file `git rev-parse f461e812d^:<path>` vs `git hash-object <path>`: 4,808 matched, 0 overwritten, 0 failed. On-disk copies were byte-identical to the pre-incident parent, so staging them equals the mandated `git show f461e812d^:<path>` restore.
5. Restorations: 34 per-lane commits by this lane (4,806 files; see RESTORE_COMMITS.tsv) plus the H6R worker's concurrent self-restore a0283287b (2 files, verified byte-identical to parent). SHA-256 manifest: RESTORED_MANIFEST.tsv.
6. Already-restored check: 23 of the 25 worker-restored files byte-identical to parent; ARENA5/NAMECHECK.md and WAVE_RECORD.md legitimately superseded by worker updates (lane-end status; living verdict log). Left as-is.
7. Final sweep over all 4,833 deleted paths (HEAD blob vs parent blob): 4,831 byte-identical, 2 legitimately superseded (same two as step 6).
8. Priority files: 1,087 PREREG/JUDGE_BRIEF/NAMECHECK/sealed/manifest files among the restored; all byte-identical to parent. All 43 PREREG files in the wave dir intact (33 byte-identical to parent, 10 newly frozen post-incident in dedicated freeze commits). 44 JUDGE_BRIEF.md and 55 NAMECHECK.md files all intact or legitimately new.
9. Anomaly: commit fc36c4444 titled "H6R: restore 2 files" actually contains RT-SENSE's 2 files (concurrent H6R worker self-restore made the H6R pathspec a no-op). Content correct; message label wrong; history left unrewritten per the no-rebase rule. Documented in LANE_AUDIT_REPORT.md.
10. No Python invoked at any point. Safebin only for shell/file/git ops.
