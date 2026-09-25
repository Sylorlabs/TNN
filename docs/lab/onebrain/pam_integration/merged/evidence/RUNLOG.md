# MERGED TREE RUN LOG — one-brain + self-PAM R1–R4 integration

Date: 2026-09-25. Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` (pinned).
Prereg: `docs/lab/onebrain/pam_integration/merged/MERGED_PREREG.md` (committed BEFORE any build/run).

## Source assembly

Merged source tree: `docs/lab/onebrain/pam_integration/merged/src/` (build/, longhorizon/, redteam/).
- `sp_gate.zag`: manually merged R1+R2+R3+R4 (m1234.zag). All three copies byte-identical,
  SHA-256 `3bbe7984fe84b0d36ff354433f3608fbe5363ca2c072d579b94692abb1ffca77`.
- Ledger-code collision resolved per prereg: R2 keeps SP_L_STORE_FULL=312;
  R4 merged codes SP_L_REVISE=313, SP_L_REV_REFUSED=314 (all uses symbolic).
- State layout: G_CHUNK_HEAD=66608, G_CHUNK_N=66648, G_POOL_HEAD=66668, G_POOL_N=66676,
  G_LASTNTFY=66680, G_KEYS=66712 (256B), G_REV_HEAD=66968, G_REV_N=66976, G_STATE_SZ=66980.
- R1: R33_NATIVE_SHA256_V2.zag vendored (all 3 trees); nio_free in nio_shim.zag (all 3);
  N-AUTH driver edits in build+LH integration drivers, LH ob_lh_int.zag, corpus_probe.zag,
  redteam driver.
- R2: prover.zag (all 3 trees); raw-offset accessor merges in build/LH drivers;
  exhaustion probes (rt_exhaust) in redteam driver; sp_auth_make→sp_auth_tag fix at one
  direct-mint site in rt_exhaust (R1/K1 loop).
- R3: install-time SP_L_PROVTAG(...,1) edit in gate; O2 expectation + rt_t4_k2_gentag +
  rt_t4_k3_nodowngrade + main calls in redteam driver.
- R4: M_REVISE + revision chunks + effective-store + recovery in gate; rt_r4_revise +
  rt_r4_uncapped + main calls in redteam driver.
- New: rt_mx_cross (MX1/MX2/MX3 interaction probes) in redteam driver; sp_chunk_max_bytes
  extended to account revision chunks (MX2c).

## Binaries (all built with pinned znc, warnings only)

- merged_smoke: from build/ob_test_integration.zag
- merged_lh_bal: from longhorizon/ob_lh_bal.zag
- merged_lh_int: from longhorizon/ob_lh_int.zag
- merged_rt: from redteam/ob_test_redteam.zag

## Batteries (3× byte-identical reruns each)

### Smoke (merged_smoke)
- 3/3 runs: rc=0, OB_FAILURES,0, byte-identical.
- SHA-256: `6855928854e38255e7275a18c5b07c82675fe1bc0752a616ba9ca90ba2e6d2e0`
  (matches frozen ref — R1/R2/R3/R4 K5/K5/K5/K7 legitimate-behavior identity).

### Red team (merged_rt)
- 3/3 runs: rc=0, RT_FAILURES,0, byte-identical.
- Includes: R1 N1–N5 (keyed N-AUTH attacks), R2 rt_exhaust (2000-revoke/4000-ledger,
  600-withhold/600-quarantine, 200-install conflict probes), R3 laundering battery +
  rt_t4_k2_gentag + rt_t4_k3_nodowngrade, R4 rt_r4_revise + rt_r4_uncapped,
  MX1 (M_REVISE through keyed N-AUTH), MX2 (revision chunk byte-accounting),
  MX3 (rehabilitated-install PROVTAG=EXT).

### Long-horizon B-alone (merged_lh_bal, s1/s10/s100)
- 3/3 runs: rc=0, OB_FAILURES,0, byte-identical.
- SHA-256: `cc7e86ed4a00be36bb4f5a2aacc6456197281270b4eb40717ebb1ca017ea93e9`
  (matches frozen ref).

### Long-horizon integrated (merged_lh_int, s1/s10/s100)
- 3/3 runs: rc=0, OB_FAILURES,0, byte-identical.
- SHA-256: `356b7873bf07942c6b2283ed087911d3bfa724cea1ab707fb1ccaf14821cec3b`
  (matches frozen ref).

## Zero-RNG scan
- grep backstop `rand|srand|random|lcg|entropy|/dev/urandom|getrandom` across all three
  merged src/ trees: 0 hits.
- Empirical: all four batteries 3× byte-identical.

## Interaction test results (all PASS, 3×)

- MX1a: legitimate keyed overseer M_REVISE applies (SP_INSTALL, SP_R_REVISE_OK, ledgered).
- MX1b: forged overseer identity (SYN) with legacy unkeyed tag on M_REVISE → refused at
  AUTH (NAUTH_R_BAD_TAG); fwd=0, no revision row, no REV_REFUSED row, victim nonce intact
  (real overseer re-emits at same nonce and applies).
- MX1c: wrong-key tag (SYN's key, overseer-claimed) on M_REVISE → refused at AUTH (BAD_TAG).
- MX1d: replay (valid tag, stale nonce) on M_REVISE → refused NAUTH_R_BAD_NONCE.
- MX2: 100 revisions applied (past old cap 64); G_REV_N=100 exact; SP_L_REVISE=100;
  zero refusals; revision chunk chain walks to exactly 1 chunk of SP_REV_CHUNK_BYTES
  (<= 2^25); rows 99/64 read back exact; supersession holds.
- MX3: poisoned subject revised (NEG superseded); warranted POS INSTALLS (SP_R_OK, fwd=1);
  its PROVTAG row = EXT (1); revised-away NEG re-emitted withholds (SP_R_CONTRADICTED).

## Notes
- One test-authoring bug caught during the run: the MX1b victim-intact follow-up initially
  reused an already-superseded line as revision evidence (correctly refused with
  SP_R_REV_BAD_EVIDENCE by the mechanism); fixed to a fresh pair, re-ran 3× clean.
  Mechanism was never wrong.
- N-AUTH failures on M_REVISE ledger SP_L_REFUSED_UNAUTH + SP_L_NOTIFY (existing path);
  SP_L_REV_REFUSED(SP_R_UNAUTH) is ledgered on authority-class failures (R4-verified
  behavior, frozen in prereg §MX1).
