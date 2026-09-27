# RUNLOG — Self-PAM CC1 correlated-corroborator guard (Crew B)

Workdir: `~/workspace/selfpam_cc1/` | Date: 2026-09-27 (PDT) | Crew B

## 0. Prereg (committed BEFORE build — deploy blocker protocol)

- Amendment file: `PREREG_AMEND_CC1_GUARD.md` (in this workdir; committed copy
  already landed on `tnn-native-lab` as
  `docs/lab/senses/pam-rebuild/selfpam/PREREG_AMEND_CC1_GUARD.md`,
  commit `2532d5e215118054deb0922c7ec2fb75e3200bda`).
- No build output existed before the amendment commit: verified by directory
  listing of the workdir at amendment time (only PREREG + api_commit.py present).

## 1. Frozen substrates copied (SHA-verified byte-identical)

| File | SHA-256 | Match to frozen |
|---|---|---|
| src/R33_NATIVE_IO_V1.zag | e6379ddb… | identical |
| src/R33_NATIVE_SHA256_V2.zag | 9824f6db… | identical |
| src/codec.zag | ca9d1fd1… | identical |

## 2. New sources (this crew)

- src/guard_gate.zag — 96-byte slot guard, obs-A/obs-B state machine.
- src/guard_chan.zag — extended attestation binding srcid into the preimage.
- src/main_cc1.zag — 58-step deterministic battery driver.
- score.py / build.py — pinned-toolchain build + frozen-table scorer.

## 3. Debug corrections during implementation (all pre-evidence)

1. First build: `cg_confirm_step` re-attestation of the SAME evidence returned
   "refresh, stay provisional". The frozen prereg §2/K1b requires WITHHELD for
   CC1a (same-bundle re-measurement is not diverse evidence). Changed the
   same-evhash path to return 0 (WITHHELD). This is a bug fix toward the frozen
   expectation, not a prereg change.
2. Driver cells C5d/C5e/C6R5 initially exercised the provisional track (no
   permanent incumbent in the fresh gate state), so "attested disagreeing obs"
   landed as CORROBORATED instead of exercising the challenger guard. Driver
   setup corrected: those cells now install the incumbent first (3 extra steps
   each), then run the challenger sequence. Preregistered expected dispositions
   unchanged; only the setup needed the incumbent present to reach the guard.
   Step count went 52 → 58 (also corrected in the stderr digest line).

## 4. Evidence runs

- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
  (pinned, per brief).
- Run 1 → evidence/run1.txt, run 2 → evidence/run2.txt (both stdout captured;
  stderr carried `steps=58 digest=a0dd2328…`).
- `cmp run1 run2` → identical; a third run also identical (3× total).
- sha256(run1) = sha256(run2) = `7debfc5231d85a50359a5bfa8dde7341544105346b6967ffadf5785ecad7d208`.
- Disposition-stream digest: `a0dd232846e8c6f21e55a782f670de1330a978b58ed08f036706a44c5fd13143`.
- RNG audit: `grep -rn "rand|_zag_random|nrg_" src/*.zag` → zero hits
  (comments included — no RNG identifiers at all).
- score.py: PASS — all 58 steps + 6 perm lines match the frozen table.

## 5. Result table (measured)

| Cell | Expectation (prereg) | Measured | Bar |
|---|---|---|---|
| C1 (K1a same-family attack) | step6 WITHHELD, perm=3 | WITHHELD, perm=3 | K1 PASS |
| C2 (K1b same-bundle attack) | step6 WITHHELD, perm=3 | WITHHELD, perm=3 | K1 PASS |
| C3 (K2a legit revision) | step6 REVISED_INSTALL, perm=1 | REVISED_INSTALL, perm=1 | K2 PASS |
| C4 (K2b legit permanent) | step3 PERMANENT_INSTALL, perm=5 | PERMANENT_INSTALL, perm=5 | K2 PASS |
| C5a–e (controls) | 1,1,1 / 1,0 / 1,0 / 1,0 / 1,1,3,8,8,8,8,7 perm=2 | exact | PASS |
| C6R1–R5 (red team) | all WITHHELD | all WITHHELD | K4 PASS |
| C6R6 (double-wrong residual) | REVISED_INSTALL (documented residual) | REVISED_INSTALL, perm=2 | K4 PASS |
| K3 determinism | 2× byte-identical | 3× byte-identical | K3 PASS |

## 6. Commit

Evidence committed to `tnn-native-lab` under
`docs/lab/senses/pam-rebuild/selfpam/cc1_guard/` via API replay onto the
current origin head, tree-walk verified. Binary (`src/build/cc1_bin`) and
`.zagd` caches excluded. Commit SHA recorded in CC1_GUARD_VERDICT.md.
