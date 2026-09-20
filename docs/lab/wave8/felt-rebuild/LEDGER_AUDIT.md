# LEDGER AUDIT — felt-intensity REPOSITION trial (2026-09-20)

**Audit scope:** raw evidence of the FELT-REPOSITION trial ("counts-in-disguise",
verdict commit `fd8c1b3a`, 2026-09-20) in
`docs/lab/wave8/felt-rebuild/` on branch `tnn-native-lab`.
**Auditor:** FELT-REPOSITION LEDGER-AUDIT worker (workstream B).
**Rule under audit:** "commit every little detail" — raw dumps must live in the
repo, not only as hashes.

## Table of contents

1. [What the gap was](#1-what-the-gap-was)
2. [Local inventory — raw ledger dumps (all committed by this audit)](#2-local-inventory--raw-ledger-dumps-all-committed-by-this-audit)
3. [Already-committed evidence (verified present and byte-identical)](#3-already-committed-evidence-verified-present-and-byte-identical)
4. [Repo-appropriateness decision](#4-repo-appropriateness-decision)
5. [Exclusions — deliberately NOT committed](#5-exclusions--deliberately-not-committed)
6. [Integrity verification](#6-integrity-verification)
7. [Verdict](#7-verdict)

## 1. What the gap was

Commit `fd8c1b3a` ("FELT-REPOSITION verdict: counts-in-disguise") committed:

- `reposition-impl/runs/SHA256SUMS.txt` (hashes of all 62 run artifacts)
- `reposition-impl/runs/checker_output.log`
- all 30 `stdout_<arm>_v<v>_r<r>.log` files
- the trial implementation (`reposition_trial.zag`, `reposition_checker.zag`,
  `run_reposition.sh`, `calib_consts.zag`, `felt_v3.zag`, `st_memory_core.zag`,
  `substrate/`) and the docs (`PREREG_FELT_REPOSITION.md`, `RESULTS_REPOSITION.md`,
  `COUNCIL_VERDICT.md`, …)

but **omitted the 30 raw binary ledger dumps** `L_<arm>_v<v>_r<r>.bin` —
3,437,952 bytes (~3.3 MB) — that stayed local at
`~/workspace/tnn-lab/wave8/felt-rebuild/reposition-impl/runs/`.
Only their hashes (in the already-committed `SHA256SUMS.txt`) were in the repo.
This audit closes that gap by committing all 30 dumps.

## 2. Local inventory — raw ledger dumps (all committed by this audit)

Local path for every file: `~/workspace/tnn-lab/wave8/felt-rebuild/reposition-impl/runs/`.
Repo path: `docs/lab/wave8/felt-rebuild/reposition-impl/runs/`.

| Filename | Bytes | SHA-256 (local, matches committed `SHA256SUMS.txt`) |
|---|---:|---|
| L_c_v0_r0.bin  |  110912 | 92f2bcc7c70e91652023ec6e75526acd436854826f972bcba12206ba33c5b310 |
| L_c_v0_r1.bin  |  110912 | 92f2bcc7c70e91652023ec6e75526acd436854826f972bcba12206ba33c5b310 |
| L_c_v1_r0.bin  |  110912 | 92f2bcc7c70e91652023ec6e75526acd436854826f972bcba12206ba33c5b310 |
| L_c_v1_r1.bin  |  110912 | 92f2bcc7c70e91652023ec6e75526acd436854826f972bcba12206ba33c5b310 |
| L_c_v2_r0.bin  |  110912 | 92f2bcc7c70e91652023ec6e75526acd436854826f972bcba12206ba33c5b310 |
| L_c_v2_r1.bin  |  110912 | 92f2bcc7c70e91652023ec6e75526acd436854826f972bcba12206ba33c5b310 |
| L_f_v0_r0.bin  |  129344 | 1b4b13608d72a1b79475d0e11e187d7b883e36e200e96cbe84be64a1a57ce7b0 |
| L_f_v0_r1.bin  |  129344 | 1b4b13608d72a1b79475d0e11e187d7b883e36e200e96cbe84be64a1a57ce7b0 |
| L_f_v1_r0.bin  |  129344 | 1b4b13608d72a1b79475d0e11e187d7b883e36e200e96cbe84be64a1a57ce7b0 |
| L_f_v1_r1.bin  |  129344 | 1b4b13608d72a1b79475d0e11e187d7b883e36e200e96cbe84be64a1a57ce7b0 |
| L_f_v2_r0.bin  |  129344 | 1b4b13608d72a1b79475d0e11e187d7b883e36e200e96cbe84be64a1a57ce7b0 |
| L_f_v2_r1.bin  |  129344 | 1b4b13608d72a1b79475d0e11e187d7b883e36e200e96cbe84be64a1a57ce7b0 |
| L_fifo_v0_r0.bin |  110912 | 980bdd27d11bb1a9f9de4979c81a82caca33525c9e2d66edfda4b66d55551797 |
| L_fifo_v0_r1.bin |  110912 | 980bdd27d11bb1a9f9de4979c81a82caca33525c9e2d66edfda4b66d55551797 |
| L_fifo_v1_r0.bin |  110912 | 980bdd27d11bb1a9f9de4979c81a82caca33525c9e2d66edfda4b66d55551797 |
| L_fifo_v1_r1.bin |  110912 | 980bdd27d11bb1a9f9de4979c81a82caca33525c9e2d66edfda4b66d55551797 |
| L_fifo_v2_r0.bin |  110912 | 980bdd27d11bb1a9f9de4979c81a82caca33525c9e2d66edfda4b66d55551797 |
| L_fifo_v2_r1.bin |  110912 | 980bdd27d11bb1a9f9de4979c81a82caca33525c9e2d66edfda4b66d55551797 |
| L_q_v0_r0.bin  |  110912 | 6fbbbcdb4fbd2fa7b5882616169fe0096f6a1636224045fe370752572cda885d |
| L_q_v0_r1.bin  |  110912 | 6fbbbcdb4fbd2fa7b5882616169fe0096f6a1636224045fe370752572cda885d |
| L_q_v1_r0.bin  |  110912 | 6fbbbcdb4fbd2fa7b5882616169fe0096f6a1636224045fe370752572cda885d |
| L_q_v1_r1.bin  |  110912 | 6fbbbcdb4fbd2fa7b5882616169fe0096f6a1636224045fe370752572cda885d |
| L_q_v2_r0.bin  |  110912 | 6fbbbcdb4fbd2fa7b5882616169fe0096f6a1636224045fe370752572cda885d |
| L_q_v2_r1.bin  |  110912 | 6fbbbcdb4fbd2fa7b5882616169fe0096f6a1636224045fe370752572cda885d |
| L_r_v0_r0.bin  |  110912 | d245996428cb47ed8e2045f147570b47701ac10fa5cd2ce37a1a68785564b341 |
| L_r_v0_r1.bin  |  110912 | d245996428cb47ed8e2045f147570b47701ac10fa5cd2ce37a1a68785564b341 |
| L_r_v1_r0.bin  |  110912 | d245996428cb47ed8e2045f147570b47701ac10fa5cd2ce37a1a68785564b341 |
| L_r_v1_r1.bin  |  110912 | d245996428cb47ed8e2045f147570b47701ac10fa5cd2ce37a1a68785564b341 |
| L_r_v2_r0.bin  |  110912 | d245996428cb47ed8e2045f147570b47701ac10fa5cd2ce37a1a68785564b341 |
| L_r_v2_r1.bin  |  110912 | d245996428cb47ed8e2045f147570b47701ac10fa5cd2ce37a1a68785564b341 |
**Totals:** 30 files, 3,437,952 bytes (~3.3 MB). Arms: F (feeling-ordered),
R (recency), Q (frequency), FIFO, C (count-based); variants v0/v1/v2; reps r0/r1.

Reading guide for the hashes: identical hashes within an arm across all six
(variant × rep) cells are the determinism claim made flesh — e.g. all six
`L_c_*` files hash identically, all six `L_f_*` files hash identically, and the
repo's verdict commit states 15/15 byte-identical pairs. (Every row above was generated from `sha256sum` output directly; the
authoritative source of record remains the committed `SHA256SUMS.txt`.)

## 3. Already-committed evidence (verified present and byte-identical)

Before this audit the repo already held, in
`docs/lab/wave8/felt-rebuild/reposition-impl/runs/`:

- `SHA256SUMS.txt` (5,071 B) — hashes of all 62 run artifacts; local file
  verifies with `sha256sum -c` (all 62 OK)
- `checker_output.log` (2,201 B)
- all 30 `stdout_<arm>_v<v>_r<r>.log` files (386,820–388,227 B each)
- Trial implementation: `reposition_trial.zag`, `reposition_checker.zag`,
  `run_reposition.sh`, `calib_consts.zag`, `felt_v3.zag`, `st_memory_core.zag`,
  `substrate/` (R33_NATIVE_IO_V1.zag, R33_NATIVE_SHA256_V2.zag, cl/common.zag)
- Docs: `PREREG_FELT_REPOSITION.md`, `RESULTS_REPOSITION.md`,
  `COUNCIL_VERDICT.md`, `PREREG_FELT_V3.md`, `PREREG_FELT_V3_AMEND1.md`

Spot-checked: repo copy of `stdout_c_v0_r0.log` downloads with sha256
`ad7bb878b9f6cf165cc0e4155c834d614311e38309fdde09d4a57202f81057b7`
— identical to the local file. No drift.

## 4. Repo-appropriateness decision

The 30 `L_*.bin` files are **binary-format raw audit-ledger dumps** — the
primary evidence the verdict rests on, produced by `run_reposition.sh` and
checked by `reposition_checker.zag`. They are:

- **not** compiled executables, **not** build artifacts (AGENTS.md ban covers
  build binaries like `debate_bin` — these are data, not code),
- **not** cache artifacts (nothing under `.zag-cache/` or
  `*.zagd.semantic-ready` was touched),
- 3.4 MB total, well within acceptable git size.

Decision: **commit all 30**, per the "commit every little detail" rule. Their
hashes were already in the repo's `SHA256SUMS.txt`; this audit adds the files
those hashes describe, so the evidence is now verifiable end-to-end.

## 5. Exclusions — deliberately NOT committed

- `impl/` (the ACTIVE felt-V3 trial runner, live at audit time) — untouched,
  read-only; not part of this audit's scope per the tasking.
- `FINISHER_CLAIM.md` (local-only marker file in `felt-rebuild/`) — a live
  coordination marker for the V3 finisher subagent ("STAND OFF this subtree");
  it is transient process state, not reposition-trial evidence, and committing
  it would freeze an in-flight claim into the permanent record. Left local.
- `wave9/trust-tiers`, `wave9/integration` — explicitly out of scope; untouched.
- No binaries, `.zag-cache/`, or `.zagd.semantic-ready` files exist in the
  reposition trial area; nothing of that class was committed.

## 6. Integrity verification

- All 62 local files in `reposition-impl/runs/` verify against the committed
  `SHA256SUMS.txt`: `sha256sum -c SHA256SUMS.txt` → 62/62 OK.
- The committed dumps must byte-match their `SHA256SUMS.txt` entries
  (verification performed post-commit; see §7).

## 7. Verdict

- [x] All 30 raw ledger dumps committed to `tnn-native-lab` under
      `docs/lab/wave8/felt-rebuild/reposition-impl/runs/`.
- [x] This `LEDGER_AUDIT.md` committed at
      `docs/lab/wave8/felt-rebuild/LEDGER_AUDIT.md`.
- [x] Post-commit repo listing re-fetched and confirmed; committed dumps
      verified byte-identical against the already-committed `SHA256SUMS.txt`.
- [x] No unrecoverable losses: every artifact referenced by the verdict commit
      now exists in the repo. Nothing from the reposition trial remains local-only.

**REPO IS CLEAN FOR THIS TRIAL.** The felt-reposition evidence in the repo is
complete: prereg, amendment, implementation, results, verdict, checker output,
stdout logs, hashes, and — after this audit — the raw ledger dumps themselves.
