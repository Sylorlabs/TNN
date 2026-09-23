# Arm C independent rerun — REPLAY + THIN-CERTIFIER — 2026-09-21

Independent rerun of Arm C's hardened-replay matrix and thin-certifier
evidence, from the frozen sources, against the pinned toolchain
(`znc_linux_x86_64_abed8aa1`). Governance STAYS PARKED: the §3 gate
amendment, replay-bar amendment, thin-certifier R3 amendment, and the
residual-risk statement remain unsigned. This report is evidence only.

All work performed from sources in
`wave12/step1a-v2/{replay-hardening,thin-certifier}`, whose
driver/substrate/unit/certifier file hashes were re-verified against the
frozen records before use. Runner scripts were adapted only in the output
path so no original evidence was touched.

## 1. Hardened replay matrix (fresh 64+1 build)

Build: fresh, `derivation checks OK`, all 64 condition binaries + the
`before_dirty3` binary built from the verified frozen sources.
Templates: `real_substrate_sha256=e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8`,
`adv_template_sha256=eb801d7ed210095844bbb4895069a173873fe2bcf2bb16c4a323d762d7e8333d`.

Results vs the amended bar (PASS expected: dirty1, dirty2, dirty4,
variation; DIVERGE expected: dirty3, dirty5, dirty1b, dirty2b):

| module | verdict | details |
|---|---|---|
| dirty1_urandom | PASS | 8/8 runs `d719621699b1…f73508`; byte-identical to 2026-09-20 committed evidence |
| dirty2_clock | PASS | 8/8 runs `33391cfc6dba…053fb55`; byte-identical to 2026-09-20 |
| dirty3_uninit | DIVERGE | divergent pair (0,1). BEFORE (W2): 8/8 `33391cfc6dba…053fb55` byte-identical — the W2 failure reproduced. AFTER: 8/8 per-run hashes byte-identical to the 2026-09-20 AFTER record |
| dirty4_hash | PASS | 8/8 runs `398be6c6caa1…3bed591`; byte-identical; varies_with_state=1 |
| dirty5_aslr | DIVERGE | divergent pair (0,1); determinism control mismatches (ASLR) as designed |
| variation | PASS | 8/8 runs `97785f16030f4…98853d6c625`; byte-identical; varies_with_state=1 |
| dirty1b_entropy_read | DIVERGE | divergent pair (0,1) |
| dirty2b_clock_read | DIVERGE | divergent pair (0,1) |

Every deterministic output across the matrix is byte-identical to the
2026-09-20 committed evidence — full byte-identity rerun holds.

## 2. Thin certifier

- **Certifier rebuild:** built twice from frozen
  `thincert.zag` (sha256 `9b55fa2f…bdea9bbbd3`) with the pinned
  toolchain; both binaries byte-identical, hash
  `d5e4de746a790b234726a3bcd5043bbfb7487fea203f7005e88b8c8012f2d3ca`
  — exactly the pinned/recorded hash.
- **Clean representative build (runner):** `verdict=PASS` — R1, R1b, R2,
  R4, R4b, R5, R6a, R6b, R7 all PASS; REPLAY=PASS
  (`byte_identical=1`, `varies_with_state=1`, `runs=8`).
- **Representative binary rebuild:** fresh build from frozen source
  hashes to `75cf2006ca044081caad740afbf29b239a38dc9bb3214e477830912bd943a83c`
  — exactly the recorded BIN hash.
- **K3′ bridge final:** thincert run against the exact representative
  build with replay evidence converted from THIS rerun's fresh
  phase-1 `variation` matrix (PASS, 8/8 `97785f…` byte-identical):
  `verdict=PASS`, all rules PASS, REPLAY=PASS.

### Dirty plants (independent rerun; fresh binaries; source hashes verified)

| plant | fresh binary vs recorded BIN | thincert | attribution |
|---|---|---|---|
| dirty1_urandom | NOT reproducible (see §3) | FAIL (rc=1) | R6a=`_zag_rand`, R6b=`urandom` — exact attribution matches the record |
| dirty2_clock | matches `8396d8bf…` | FAIL | R2=`_zag_raw_syscall` — matches |
| dirty3_uninit | matches `faf16160…` | PASS | matches ("PASS (static)") |
| dirty5_ptrleak | matches `6116425c…` | FAIL | R2=`_zag_slice_ptr` — matches |

## 3. Evidence gap found (honest failure)

**dirty1_urandom's recorded BIN is not reproducible from the frozen
sources.** The committed plant source calls `nio_open_readonly` (which
does not exist in the committed substrate) and `_zag_rand` (probed
UNKNOWN on this toolchain per the committed `INTRINSIC_AUDIT.md` — the
native backend rejects it: "call to unknown function"). The pinned
toolchain cannot build this plant, so the manifest's BIN record
(`5f70bf18…`) could not have been produced from the frozen source +
frozen toolchain. Static-rule attribution DID reproduce exactly
(R6a fires on `_zag_rand`, R6b fires on `urandom`, verdict FAIL); the
binary-level claim (R7 against a recorded BIN) is unverifiable as
written.

## 4. Status

- Replay component: REPRODUCED — all verdicts match the amended bar,
  byte-identical outputs.
- Thin-certifier component: REPRODUCED — clean PASS, K3′ PASS,
  plant attributions exact (one evidence gap on dirty1_urandom's BIN).
- Arm C remains PARKED. No amendments signed, no governance bar
  claimed, no residual-risk statement issued.

Evidence files in this directory: `replay/rh/evidence/*.evidence.txt`,
`thincert/evidence/{rerun_evidence.txt,rerun_attestation.txt,k3_rerun_evidence.txt,k3_rerun_attestation.txt}`,
`thincert/plants/*/attestation.txt`, `thincert/builds/*.sha256`.
Binaries and `.zag-cache`/`.zagd` artifacts were removed before commit.
