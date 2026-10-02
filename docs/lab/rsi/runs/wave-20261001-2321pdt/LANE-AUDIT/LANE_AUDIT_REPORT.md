# LANE_AUDIT_REPORT.md - wave-20261001-2321pdt git hygiene incident audit

Lane: LANE-AUDIT (replacement worker). Date: 2026-10-02.
Incident: commit f461e812d ("H5R2-SKEPTIC2 implementation") deleted 147,296 files repo-wide; 4,833 of them under docs/lab/rsi/runs/wave-20261001-2321pdt/.

## Method

1. Listed every file deleted by f461e812d: `git diff-tree --no-commit-id --name-status -r f461e812d`, status D only. 4,833 paths under the wave dir.
2. Built the HEAD file list for the wave dir (`git ls-tree -r HEAD --name-only`) and split the deleted set into present-in-HEAD (25, already restored) vs still-missing (4,808).
3. Checked for deliberate post-incident deletions: `git log --diff-filter=D --name-only f461e812d..HEAD -- <wave dir>` returned empty. No lane worker deliberately deleted anything after the incident. All 4,808 were unrestored incident damage.
4. Verified on-disk copies: all 4,808 still-missing files existed on disk as untracked files. Compared each file's git blob hash against the parent blob (`git rev-parse f461e812d^:<path>` vs `git hash-object <path>`). Result: 4,808 matched, 0 overwritten, 0 failed. The on-disk copies were byte-identical to the pre-incident parent, so staging them is exactly the mandated `git show f461e812d^:<path>` restore.
5. Committed one restoration commit per affected lane (34 commits). SHA-256 manifest of every restored file: RESTORED_MANIFEST.tsv (4,808 lines). Commit list: RESTORE_COMMITS.tsv.
6. Final sweep over all 4,833 deleted paths: HEAD blob vs parent blob. 4,831 byte-identical; 2 differ for documented legitimate reasons (see below).

## (a) Lanes audited

All 57 lane directories present under docs/lab/rsi/runs/wave-20261001-2321pdt/ when the audit began were audited (listed below). Five more directories appeared while the audit ran (ARENA-GEN-VERIFY, DRAFT-CHECK, MECH-VERIFY, RECORD-CHECK, RT-ARENA4); all were created after the incident, contain zero tracked files, and have zero overlap with the 4,833 deleted paths, so there is nothing to restore in them. The 57 audited lanes: ARENA, ARENA-BLIND, ARENA-GEN, ARENA2, ARENA3, ARENA4, ARENA5, BATTERY, BATTERY-CLUSTER, BATTERY-E1, BATTERY-E2, BATTERY-E3, BATTERY-E4, BATTERY-E5, BATTERY-E6, BATTERY-E8, C174, C9BAT, CLUSTER-FINAL, CLUSTER-SYNTHESIS, CONSEQ, CONTLEARN, CONTLEARN-OWNED, CONTLEARN-OWNED2, DEBATE-PREP, DEVANG3, F1, F1-BUFFER, F1-FOLLOWUP, F1-REPAIR, F1-REPAIR2, F2V3, FORK, H2R, H5R2-BASELINE, H5R2-DECOY, H5R2-REPRO, H5R2-SKEPTIC2, H5R2-SKEPTIC3, H6R, H7R, HPIREV2, LEARNER-MECH, LOOPSTATE-DRAFT, LANE-AUDIT, RT-ARENA5, RT-C174, RT-EXEC, RT-F2V3, RT-GOV, RT-HPIREV2, RT-INT, RT-SENSE, SENSORY, SWARM-HEALTH, TNN3-SUBSTRATE, TNN3H5R.

Lanes with zero incident deletions (created after f461e812d or never touched by it): ARENA-BLIND, ARENA-GEN, BATTERY-E5, BATTERY-E8, CLUSTER-FINAL, CLUSTER-SYNTHESIS, CONTLEARN-OWNED, CONTLEARN-OWNED2, DEBATE-PREP, F1-REPAIR2, H5R2-SKEPTIC2 (the incident commit's own lane; its 3 added files are intact), H5R2-SKEPTIC3, LEARNER-MECH, LOOPSTATE-DRAFT, RT-ARENA5, RT-F2V3, SWARM-HEALTH.

## (b) Files found still-missing and restored

4,808 files restored, committed per lane. Per-lane counts and commit ids (full SHA-256 per file in RESTORED_MANIFEST.tsv):

- ARENA: 55 files, 33cc2bff649b7fc71676e04fd898127c631aa26e
- ARENA2: 59 files, 3b25013b19372f01523c86ea9f4c6c9ce60ad4f2
- ARENA3: 52 files, 33d4e2e1953626b61303b3548e6a04a8a3c06ab5
- ARENA4: 47 files, a5d7a6ef793133f6015441aadb8504eeb5ce9a61
- BATTERY: 170 files, 57f1cfa856c806e10ee184ce1a97371380dbba5e
- BATTERY-CLUSTER: 3 files, 35782193012c63835de6d8eb97e818d0f45e0e72
- BATTERY-E1: 69 files, 1bea7a7ca067a42d482336731332d610f2fdbfc7
- BATTERY-E2: 30 files, 5b2775e46fa2622621bf1f580063628f8ea8d790
- BATTERY-E3: 46 files, f14f1470d24c4c6eca9cb570fdec26f235097574
- C174: 36 files, 88e92c01603d5c45098e8e89fb901d571725b1ec
- C9BAT: 31 files, 33fff11e239e28ad1189103975a4076f4c78687b
- CONSEQ: 17 files, 5cf8df371ebaec7a033a5081a83394b7007beb21
- CONTLEARN: 26 files, 719829def466dab25e789bfce93a54deea085f10
- DEVANG3: 19 files, e0135d9933a5ef7935e4aebd1cd7e4e2c7eb581d
- F1: 533 files, 79e11a6d1fa15f30e6d0fb5953291950463417d7
- F1-BUFFER: 957 files, ffb8e885a4c7cbcba2096278c5deaa5f091c327b
- F1-FOLLOWUP: 1412 files, 36743190e5fd76ab8c47a586fec3af8f4ea462dc
- F1-REPAIR: 956 files, 25712d767cbee3806a08643f9b58794ef86a3bb0
- FORK: 3 files, 015375dc7c221828257a6e76c2316dd4e6cff2e5
- H2R: 18 files, 9bd208eee5fe86b9fbe2b4a2caabfd3300672d18
- H5R2-BASELINE: 35 files, 8c3292bb60c31321e505377c773871712289ad3f
- H5R2-DECOY: 22 files, d0b2ffece25cd8d07d297c54147469a18fd8e652
- H5R2-REPRO: 3 files, 7dd728c9f872574332d9b2fd5eee34285cd44680
- H6R: 0 files by this lane (see anomaly note below)
- H7R: 13 files, 6b8dedf28fb4f248c859caf9e38863c49f2d98d7
- HPIREV2: 68 files, 8c7533cb09a5b55b9f79d08e928561943a877085
- RT-C174: 2 files, 7d20a7a3d18f89998ea74e364577782e431cbe9f
- RT-EXEC: 2 files, f8fcac045ef610acece6b7ab3ec06afcfa219939
- RT-GOV: 2 files, 84c8fd0df879b9baa6105871e9164cf6f669631e
- RT-HPIREV2: 75 files, 1eb89eadfb4350fedecee6ade56066a415047974
- RT-INT: 2 files, f99a5617492b07f0b0dbeac7d2adbba030e7d310
- RT-SENSE: 2 files, restored inside commit fc36c4444 (see anomaly note below)
- SENSORY: 19 files, c7306028f093a96c4ca4a2ecb7ae9ce5aa1c0690
- TNN3-SUBSTRATE: 9 files, 3b61e5e576f193b0e38c445155b2022c96a1f998
- TNN3H5R: 13 files, 7e4d7cffed84ff1e7d7ac0492d4d9a0c85f02ff1

Of the 4,808, 1,087 are priority files (PREREG, JUDGE_BRIEF, NAMECHECK, sealed world/manifest/evidence files). All restored byte-identical to the pre-incident parent.

Anomaly notes (content correct, labeling imperfect; history left unrewritten per the no-rebase rule):
- Commit fc36c4444 is titled "H6R: restore 2 files" but actually contains RT-SENSE/NAMECHECK.md and RT-SENSE/RT-SENSE_REVIEW.md (2 files, byte-identical to parent). Root cause: the H6R worker concurrently self-restored at 07:29:36 (commit a0283287b, 12 H6R files including H6R/NAMECHECK.md and H6R/PREREG_H6R.md, both verified byte-identical to parent), so the H6R pathspec was a no-op and the commit swept up RT-SENSE's staged files. RT-SENSE's own follow-up commit then correctly failed with "nothing to commit". Net effect: all files present and correct; only the commit message label is wrong.
- H6R's 2 incident-deleted files (NAMECHECK.md, PREREG_H6R.md) were restored by the H6R worker's own commit a0283287b, not by this lane. Verified byte-identical to parent.

## (c) Files already restored by lane workers (no action needed)

25 files were deleted by f461e812d but already present in HEAD before this audit; 23 verified byte-identical to the parent, 2 legitimately superseded:

- BATTERY-E4 (commit 5a2c7c91c): NAMECHECK.md, PREREG_E4.md. Both byte-identical to parent.
- F2V3 (commit 30a1ff7e0): NAMECHECK.md, PREREG_F2V4.md, build.sh, f2v4_learner.zag, f2v4_world_aprime.zag, sealed/f2v4_world_c2prime.zag. All byte-identical to parent.
- BATTERY-E6: NAMECHECK.md, PREREG_E6.md, e6_ablate.zag, e6_ablate_bin, e6_inspect.zag, e6_inspect_bin, e6_run.sh, e6_worldgen.zag, e6_worldgen_bin, e6_worlds/e6_act_world.txt, e6_worlds/e6_s0_world.txt, e6_worlds/e6_s1_world.txt, e6_worlds/e6_s3_world.txt, e6_worlds/e6_s5_world.txt. All byte-identical to parent.
- ARENA5: PREREG_DEFRECALL.md byte-identical to parent. ARENA5/NAMECHECK.md differs from parent because the ARENA5 worker deliberately re-created it with lane-end status (BUILD-PASS verdict, toolchain re-verification) in commit 6582398e9. Legitimate worker update, left as-is.
- WAVE_RECORD.md differs from parent because it is a living document: later commits (including 587330237 verdict-line repair and ongoing verdict recordings) legitimately extended it. Left as-is.

## (d) Lanes not fully audited

No lane was left unaudited. The five directories created during the audit (ARENA-GEN-VERIFY, DRAFT-CHECK, MECH-VERIFY, RECORD-CHECK, RT-ARENA4) postdate the incident and contain no deleted paths; noted in (a) for completeness.

## Frozen prereg confirmation

All 43 PREREG files in the wave dir are intact in HEAD:
- 33 are byte-identical to the pre-incident parent (all incident-deleted preregs restored exactly).
- 10 are new post-incident freezes by lane workers, each in its own dedicated freeze commit after f461e812d (ARENA-BLIND, ARENA-GEN, ARENA5 Amendment 1, BATTERY-E5, BATTERY-E8, CONTLEARN-OWNED Amendment A1 re-freeze, CONTLEARN-OWNED2, F1-REPAIR2, H5R2-SKEPTIC2, H5R2-SKEPTIC3). Prereg-ordering discipline preserved.
- 0 preregs missing, 0 corrupted.

44 JUDGE_BRIEF.md and 55 NAMECHECK.md files: all either byte-identical to parent or newly created post-incident by lane workers, except the one legitimate ARENA5/NAMECHECK.md worker update noted above.

## Out of scope observation for the parent

The incident deleted 147,296 files repo-wide; this audit covered only the 4,833 under the wave dir per the task. The remaining ~142,000 deleted files elsewhere in the repo (docs/lab/*, src/, units/, etc.) exist on disk as untracked files but are NOT in HEAD. Restoring them is outside this lane's tasking; recommend a follow-up decision on whether to restore and commit them or leave the working tree as the recovery source.

No Python was invoked at any point. Safebin toolchain verified at start (`which python3` prints nothing, exit 1). All commits local only, never pushed.
