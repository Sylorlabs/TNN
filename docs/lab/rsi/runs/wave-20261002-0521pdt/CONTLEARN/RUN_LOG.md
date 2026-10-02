# RUN_LOG: CLH2 longer-horizon delayed rebind

Wave: wave-20261002-0521pdt. Lane: CONTLEARN (CLH2). Date: 2026-10-02.
Pure Zag plus shell orchestration. No Python, C, JavaScript, or Rust at
any stage. `which python3` empty under safebin PATH (NAMECHECK.md Step 0,
recorded before any research operation).

## Commits

- c927915b3: NAMECHECK.md with Step 0 toolchain guard.
- aa47999f7: PREREG_CLH.md frozen ALONE (1 file).
- ef9b80200: implementation + sealed evidence (33 files).
- K0: git merge-base --is-ancestor aa47999f7 ef9b80200 -> true;
  c927915b3 ancestor of ef9b80200 -> true.

## K2a hash record (before builds and after runs)

- tnn2.zag: a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd
- nomain derivation (0221pdt CONTLEARN lane file): 26b455e78a9b0ba0f6d6967c12ff8c05f9ebd9152dddca9efeb2a3b44064ec9d
- clh2_core_control.zag: 26b455e78a9b0ba0f6d6967c12ff8c05f9ebd9152dddca9efeb2a3b44064ec9d (cmp byte-identical to pf_core_control.zag)
- clh2_core_treat.zag: 627af6eb0e88141fdeb00baba0aab178a29df128aa0250398355db42d8557f63 (cmp byte-identical to pf_core_treat.zag)
- combined sources: treat 65a87261..., control 9f67cd7f..., nophase 08cd5101... (full hashes in SEALED_EVAL evidence)

## Builds (the 3 logged znc invocations, pre-run)

- sh znc_wrap_clh2.sh clh2_combined_treat.zag -o clh2_treat (warnings only, 152 analyzer notes; binary a65df4de..., 260396 bytes)
- sh znc_wrap_clh2.sh clh2_combined_control.zag -o clh2_control (warnings only, 150 notes; binary ebe3ead8..., 252118 bytes)
- sh znc_wrap_clh2.sh clh2_combined_nophase.zag -o clh2_nophase (warnings only, 150 notes; binary ba12a784..., 248028 bytes)

znc_invocations_clh2.log: exactly 3 entries before the runs; 0 new
entries during the 9 runs (verified by line count after).

Analyzer notes are the same warning class as prior waves (e.g.,
discarded non-void return inside fixture phase functions); no errors.

## Runs

sh run_clh2.sh: 9 spawns (3 binaries x 3 reps), rc=0 on all 9,
harness_clh2.log records total_spawns=9 want=9. Each run: one process,
empty argv, empty env (bash -c 'exec -c'). All stderr files 0 bytes.

Transcript SHA-256 (all 3 reps identical per binary):
- TREAT: 2f03c4af4d857b617ea6074ce4a24730d37190bba476ed9fb3d8dcefd2d29b00, FNV 1491595695
- CONTROL: d53258f7efac4f9c62ee97c6bfbba243631876b8af4ca222eada06907199dcd, FNV -1746384548
- NOPHASE: 9e6b86812e6d925f19097ee38b915269e3be53c310aad3e21af0216442eb2756, FNV 275619593

## K3 regression

printf 'TREAT' | <lo_driver> (committed 2321pdt binary, read-only), 3x:
stdout SHA-256 1ff527fa97b36da25fd8163299773680e53ae47fba521fc2227b0bf7c39394d9
on all 3 reps; rc=0; 0 stderr bytes. (stdin lesson from CONTLEARN3 K3
applied.)

## Verification

sh verify_clh2.sh: ALL SEALED CHECKS PASS (44 PASS lines, 0 FAIL).
The script initially had 4 grep-artifact FAILs (anchor patterns and
relative paths); all were script bugs, none were experiment failures;
fixed and re-run clean. The fixed script is committed.

## Notes

- A concurrent worker held the git index.lock twice during this lane's
  commits; waited and retried, no lockfile touched manually.
- AGENTS.md gained new znc lessons mid-lane (SA1 lane findings);
  assessed not applicable to this lane (REDTEAM_SELF.md R9).
- K2b audit: both drivers 0 cognition fns, 0 structural writes
  (ns(/link_edge(/alloc_node( count 0), 0 switch/match, 0 new tags,
  edges, opcodes, modes, bridges, handlers.
