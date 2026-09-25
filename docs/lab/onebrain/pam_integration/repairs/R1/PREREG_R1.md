# PREREG_R1 — N-AUTH real authentication (keyed MAC)

**Status: FROZEN 2026-09-24 (R1 repair crew).** This prereg is written BEFORE
any R1 implementation. It freezes the MAC construction, key provisioning,
the forgery model, and the kill bars. No implementation deviation without a
prereg amendment. Parent task: ONE-BRAIN + SELF-PAM REPAIR R1 (residual #1
of 4 from `redteam/RESULTS.md`: N-AUTH identity is unauthenticated).

## 0. Background (frozen context, not modified)

The integrated composition (Fork-D self-PAM discipline on every organ's
claim commit/pin/promote/utterance path, repaired variant B, nine
composition laws incl. N-AUTH) lives at
`~/workspace/onebrain_pam_integration/` (frozen `PREREG.md`, DO NOT MODIFY).
Red-team findings (`redteam/RESULTS.md`, residual #1): N-AUTH envelopes are
`(requester_id, nonce, content_hash)` with `content_hash = sp_fnv5` =
unkeyed FNV-1a over `(requester_id, nonce, mtype, arg1, arg2)`
(`sp_gate.zag` ~135-159 `sp_fnv`/`sp_fnv5`/`sp_auth_make`, ~269-277
`sp_auth_verify`, ~701-714 `sp_gate_one`, ~821-858 documented testbed
attestation boundary in `sp_ingest_legacy`). Proven: forged `requester_id`
(SYN as ORG_OVERSEER, valid nonce + locally-computed hash) ACCEPTED and
installed at weight 42 (N1); forged overseer-only M_FORCE_PIN by a
non-overseer ACCEPTED and installed (N2). FNV is not a signature; the
verdict is identity-blind, so forgery buys class + weight + attribution.

## 1. Repair design (frozen)

**Construction — HMAC-SHA256 truncated to 32 bits ("tag"):**
- `tag = LE32( HMAC-SHA256( key_org, msg )[0..4] )`, where
  `msg = LE32(requester_id) || LE32(nonce) || LE32(mtype) || LE32(arg1) || LE32(arg2)`
  (20 canonical bytes; `ob_s32` little-endian layout, same as the old
  `sp_fnv5` input so the envelope shape is unchanged).
- HMAC per RFC 2104: `H((K' ^ opad) || H((K' ^ ipad) || msg))`, K' = the
  32-byte organ key zero-padded to the 64-byte block.
- The envelope's auth field stays `i32` (the 16-byte outbox record and
  `sp_gate_one` signatures are unchanged); the 32-bit truncation is a
  testbed envelope constraint, documented as a downgrade vs a 64+-bit tag
  (see §4). Nonces remain per-organ monotonic counters; the gate still
  consumes a nonce ONLY on successful verification.
- SHA-256 source: the pinned toolchain's native module
  `~/workspace/tnn-lab/toolchain/R33_NATIVE_SHA256_V2.zag`, vendored
  byte-identical into each testbed `src/` dir EXCEPT its single
  `@import("R33_NATIVE_IO_V1.zag")` line is stripped, because the testbed's
  `nio_shim.zag` already provides `nio_alloc` (byte-identical semantics to
  the IO module's, per the shim's own header comment) and `nio_free` is
  added to the shim (one line, same semantics as the IO module). The SHA
  module uses only `nio_alloc`/`nio_free` from the IO module — verified by
  grep before vendoring. The vendoring delta is proven by `diff` against
  the toolchain original and recorded in VERDICT_R1.md.
- **Fallback (only if SHA-256 integration proves infeasible):** keyed FNV —
  the organ key mixed into every FNV round (not just prefixed). The
  fallback requires a VERDICT_R1.md section with (a) the exact compile/runtime
  evidence of infeasibility, and (b) an explicit security-downgrade note
  (non-cryptographic MAC: no collision/preimage resistance claims; the
  testbed then proves only key-separation, not unforgeability).

**Key provisioning (fixture keys — the mechanism is what's tested, not key
generation):**
- `G_KEYS` region appended to gate state: `SP_NORG * 32` bytes (256-bit key
  per organ), `G_STATE_SZ` grows by 256. Provisioned deterministically in
  `sp_new` (pure Zag, ZERO RNG): `key[org][w] = sp_fnv5(org, w,
  0x4E415554, 0x484B4559, 0x9E3779B9)` for `w = 0..7`, stored LE — i.e.
  FNV-1a over fixture domain constants + (org, word-index). Documented in
  code as FIXTURE keys; deployment provisions keys out-of-band.
- The gate registry holds the keys (`sp_auth_verify` recomputes the tag
  with the CLAIMED organ's registry key). Legitimate minting helper
  `sp_auth_tag(g, org, ...)` reads the claimed organ's key from the same
  registry.

**Forgery model / testbed attestation (unchanged boundary, hardened):**
- The driver still attests envelopes for the frozen variant-B organs
  (`sp_ingest_legacy`) and native-speaking synthetic organs (`syn_emit`),
  but now mints **with the CLAIMED organ's key** via `sp_auth_tag`.
- The attacker (SYN) does NOT hold the overseer's key. Attacker oracles:
  (i) `sp_auth_make_legacy` — the old unkeyed FNV construction, retained
  under a renamed symbol FOR THE ATTACKER ONLY (K1: attacker-minted unkeyed
  hash); (ii) a tag minted with the WRONG organ's key (SYN's key on an
  overseer-claimed envelope) via the explicit-key entry point (K4).
- Auth failure → `REFUSED_UNAUTHENTICATED` (`SP_L_REFUSED_UNAUTH` ledger row
  with the `NAUTH_R_*` reason, `SP_L_NOTIFY` row, `G_LASTNTFY` set), never
  forwarded, organ notified. Reason codes keep frozen values
  (`NAUTH_R_UNKNOWN_ORG=1`, `NAUTH_R_BAD_NONCE=2`, `NAUTH_R_BAD_TAG=3`
  — renamed from `NAUTH_R_BAD_HASH`, value frozen —,
  `NAUTH_R_UNAUTHORIZED_CLASS=4`).
- Nonce anti-replay machinery and the frozen authority matrix
  (`sp_authorized`: M_FORCE_PIN is the overseer's alone, etc.) are
  UNCHANGED. Order of checks unchanged: registered → nonce → tag →
  authority class.
- **Identity-blind verdicts by design (unchanged):** `sp_verdict` takes no
  identity input; authentication gates class/weight/attribution ONLY. A
  forged identity can never buy verdict bypass — the verdict kernel never
  sees the requester_id. Weight (`sp_weight`: overseer 40 / SYN 5) applies
  post-auth as before.

## 2. Kill bars (all must hold; any failure kills the repair)

- **K1** — forged `requester_id` (SYN as ORG_OVERSEER) with
  attacker-minted UNKEYED hash → `REFUSED_UNAUTHENTICATED`
  (`fwd=0`, `rson=SP_R_UNAUTH`, `SP_L_REFUSED_UNAUTH` row with
  `NAUTH_R_BAD_TAG`), no install, no weight, no nonce consumed.
- **K2** — forged overseer-only M_FORCE_PIN by a non-overseer → refused at
  AUTH (never reaches the authority-class check, never installs).
- **K3** — replay of a consumed envelope (valid tag, stale nonce) →
  refused (`NAUTH_R_BAD_NONCE`).
- **K4** — tag minted with the WRONG organ's key (right claimed id, right
  nonce, SYN's key) → refused at auth.
- **K5** — legitimate-traffic verdicts byte-identical to pre-repair frozen
  refs: the smoke battery, both long-horizon legs, and every non-N-attack
  red-team check produce byte-identical outputs to the 3x pre-repair runs
  captured BEFORE implementing (authentication must not change verdicts).
  Intended deltas only: the N1/N2/N3 red-team expectations + finding texts
  (enumerated in VERDICT_R1.md).
- **K6** — nonce-desync self-heal still works (BAD_NONCE → counter
  catch-up → install), now under keyed tags.
- **K7** — any RNG in a decision path kills the run (re-run the RNG_SCAN
  grep over all three `src/` trees + the vendored SHA module; 3x
  byte-identical reruns of every battery as the empirical backstop).

## 3. Verification plan

1. Build PRE-REPAIR binaries from the unmodified tree; run smoke (3x),
   red-team (3x), long-horizon T1 legs (3x each); record output SHA-256s as
   the frozen refs (K5 baseline).
2. SHA-256 integration probe: `ns_sha256("abc")` KAT
   (`ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad`)
   in the pinned znc before wiring it into the gate.
3. Implement §1 in `build/src/`, `redteam/src/`, `longhorizon/src/` (the
   three `sp_gate.zag` copies stay byte-identical to each other, as today).
4. Rebuild all batteries with the pinned toolchain ONLY
   (`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`).
5. Update the red-team N1/N2/N3 attacks to the §1 forgery model
   (attacker oracles (i)/(ii)); add K4 wrong-key check; keep N4/N5.
6. Run smoke + red-team N1–N5 + long-horizon T1–T5 legs; 3x byte-identical
   reruns; K5 diff of legitimate traffic vs frozen refs.
7. Write VERDICT_R1.md with kill-bar accounting; commit prereg first, then
   evidence + verdict (separate commits).

## 4. Known/documented downgrades (not kill bars)

- 32-bit tag truncation (envelope is `i32`): forgery needs ~2^31 expected
  online attempts; wrong-tag attempts do not consume nonces, so the bound
  is computational, not rate-limited, in this testbed. Production carries
  ≥64-bit tags.
- Fixture keys derived via FNV (not a KDF): fine for mechanism testing;
  deployment provisions keys out-of-band.
- The testbed driver holds all keys (it attests for every organ); the
  forgery model is simulated by the attacker oracles never touching the
  victim's key. This is the documented testbed boundary, same as the
  pre-repair `sp_ingest_legacy` attestation note.

## 5. Workdir / commits

- Workdir: `~/workspace/ob_pam_repairs/R1/` (copy of
  `~/workspace/onebrain_pam_integration/`; the original is never modified).
- Stage for commit at
  `~/workspace/tnn-lab/onebrain/pam_integration/repairs/R1/`.
- Commit 1 (this file): prereg only. Commit 2: repaired sources + drivers +
  `VERDICT_R1.md` + run evidence. Never commit binaries or `.zagd` files.
