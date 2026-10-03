# FW1-FW9 Seal Integrity Report

**Date:** 2026-10-01 UTC
**Checker:** Sealed World Integrity Checker (independent verification worker)
**Verdict:** SEAL-INTEGRITY-CHECK-COMPLETE

## Scope

Verification only. No sealed world file was opened, read, or displayed.
No world contents appear in this report. All checks were performed via
filenames, hashes, git metadata, and file permissions.

## 1. File existence

All 16 sealed world files exist at the expected paths under
`docs/lab/research-lead/overnight-20260928/freeze_worlds_v2/worlds/`:

- fw1_world.txt, fw2_world.txt, fw3_world.txt, fw4_world.txt, fw5_world.txt
- fw6_phaseA1.txt, fw6_phaseB1.txt, fw6_phaseB2.txt
- fw6_controlA.txt, fw6_controlB.txt, fw6_controlB2.txt
- fw6b_phaseA1.txt
- fw7_world.txt, fw8_world.txt
- fw9_dagA.txt, fw9_dagB.txt

Result: 16/16 present. None missing.

## 2. Hash verification

All 16 SHA-256 hashes were computed and compared against the authoritative
records in SEAL.md (sealed 2026-09-30, commit 396895595).

| file | match |
|---|---|
| fw1_world.txt | YES |
| fw2_world.txt | YES |
| fw3_world.txt | YES |
| fw4_world.txt | YES |
| fw5_world.txt | YES |
| fw6_phaseA1.txt | YES |
| fw6_phaseB1.txt | YES |
| fw6_phaseB2.txt | YES |
| fw6_controlA.txt | YES |
| fw6_controlB.txt | YES |
| fw6_controlB2.txt | YES |
| fw6b_phaseA1.txt | YES |
| fw7_world.txt | YES |
| fw8_world.txt | YES |
| fw9_dagA.txt | YES |
| fw9_dagB.txt | YES |

Result: 16/16 hashes match. Zero discrepancies.

The FW6 responder source (`seal_src/fw6_respond.zag`) hash also matches
the SEAL.md record: 0fed07801354597f441ea1a8822d4a1d97cbbc01b0b85512c489b2d4bbdaa6de.

## 3. Modification check

- `git status --porcelain` on the worlds directory: clean (no modifications).
- All 16 file mtimes: 2026-09-30 18:14 (the seal date). No post-seal writes.
- Git blob hashes of working-tree files match the seal commit 396895595.
- SEAL.md in the seal commit is byte-identical to the current SEAL.md.

Result: No modifications since sealing.

## 4. Preregistration linkage

The CORE-FREEZE-TNN2 preregistration (commit ce1a7c5f8) references the
sealed FW1-FW9 assets as "Same sealed assets" with kill bars:
- K-FZ2-2 (no cognition edits): TNN-2 hashes verified before/after.
- K-FZ2-5 (seal integrity): FW1-FW9 accessed only through authorized evaluator.
- F-FZ2-3: FW seal broken (evaluation invalid).

The seal itself (commit 396895595) strictly precedes the freeze prereg,
satisfying the commit-order requirement.

## 5. Access control and contamination check

- File permissions: `-rw-------` (600), owner root. Restrictive.
- The sealed files are tracked in git (all 16 listed by `git ls-files`).
- References to the sealed world paths were found in exactly three places:
  1. `core_freeze_tnn2_eval/run_fw_battery.sh` (the authorized TNN-2 evaluator)
  2. `core_freeze_tnn1_eval/run_fw_battery.sh` (the authorized TNN-1 evaluator;
     same sealed assets per the prereg)
  3. `blindness_audit/BLINDNESS_AUDIT.md` (the seal blindness verifier;
     references paths only for grep-based contamination checks)

No builder, analyst, or other worker directories reference the sealed paths.
No evidence of unauthorized access or content inspection was found.

## 6. Anti-smuggling status (from SEAL.md, not re-verified)

The seal record documents SMUGGLING-CHECK: PASS. No FW world id appears in
the frozen cognition source. This was verified by the sealer at seal time
and is recorded here for completeness; re-running the scan would require
opening the sealed files, which is outside this checker's scope.

## Verdict

**SEAL-INTEGRITY-CHECK-COMPLETE.**

All 16 sealed world files are present, unmodified, and hash-identical to
the seal records. The FW6 responder source is intact. Git history confirms
the seal commit precedes the freeze preregistration. Access is restricted
to the two authorized evaluators and the blindness audit. No contamination
detected.

The seal is intact. The authorized TNN-2 evaluator may proceed.
