# VERDICT_R1 — N-AUTH real authentication (keyed MAC)

**Prereg:** `PREREG_R1.md` (frozen 2026-09-24, committed `2e8a947c7fbc` on
`sylorlabs/TNN` branch `tnn-native-lab`,
`docs/lab/onebrain/pam_integration/repairs/R1/PREREG_R1.md`).
**Status:** COMPLETE — all kill bars hold on corrected evidence.
**Correction note:** this verdict SUPERSEDES the verdict committed as
`2cf1ee7cc1df8e5c2eeda744ae9bcae2225fdc5e`. That commit's K5 claim was
wrong: it accepted a one-line smoke-output delta
(`OB_CHECK,ih_auth_deterministic` printing the HMAC tag instead of the
frozen legacy FNV tag) as "intended". The 2026-09-25 00:09 UTC checkpoint
explicitly required the smoke output to be **exactly byte-identical** to
the frozen baseline, with only N1/N2/N3 red-team deltas permitted. The
B7 printed fixture has now been restored to `sp_auth_make_legacy`, and
the smoke output is byte-identical to the frozen baseline (K5 below).
The Python HMAC cross-check remains as mechanism confirmation only — it
never licensed an output delta.
**Crew note:** this is the RESUME crew (prior crew killed by a daemon
restart). Prior-crew partial state verified and reused where sane:
`refs/prerepair/smoke_run1.out` SHA matches this crew's fresh pre-repair
rebuild byte-identically (`68559288…`, see §2). The SHA-256 probe
(`probe/`, KATs `abc`/`""`/fox all pass) was reused as-is. One
fidelity fix applied to the inherited implementation: the fixture-key
domain constants in `sp_key_derive` were wrong decimal transcriptions of
the prereg's frozen hex (`1312903252/1212505945/987654321`); corrected to
the exact prereg values `0x4E415554/0x484B4559/0x9E3779B9` as i32
(`1312904532/1212892505/-1640531527`) in all three `sp_gate.zag` copies
(Zag has no hex literals; the prior crew's mental conversion was off).

## 1. What was built (per PREREG_R1.md §1)

- `tag = LE32(HMAC-SHA256(key_org, msg)[0..4])`,
  `msg = LE32(org)||LE32(nonce)||LE32(mtype)||LE32(a1)||LE32(a2)`
  (20 canonical bytes, same encoding the old `sp_fnv5` hashed).
- HMAC per RFC 2104; 32-byte organ keys, zero-padded to the 64-byte
  block; envelope auth field stays `i32` (documented 32-bit truncation,
  prereg §4).
- Keys: `G_KEYS` region (`SP_NORG*32` bytes) appended to gate state
  (`G_STATE_SZ` 107880 → 108136); provisioned deterministically in
  `sp_new` via `sp_key_derive` — `key[org][w] = sp_fnv5(org, w,
  0x4E415554, 0x484B4559, 0x9E3779B9)`, LE — pure Zag, zero RNG.
- `sp_auth_verify` recomputes the tag with the CLAIMED organ's registry
  key; check order unchanged (registered → nonce → tag → authority
  class); nonce consumed only on successful verification.
- `sp_auth_make` renamed `sp_auth_make_legacy`, retained ONLY as the
  red-team attacker oracle (K1) and as the printed B7 compatibility
  fixture (K5 — the frozen smoke line
  `OB_CHECK,ih_auth_deterministic,-1251831065,-1251831065` is preserved
  byte-for-byte). New entry points: `sp_auth_tag(g, …)` (legitimate
  mint with claimed organ's key), `sp_auth_tag_key(key, …)`
  (explicit-key attacker oracle, K4). No legitimate auth path calls the
  legacy constructor.
- SHA-256 vendoring: `R33_NATIVE_SHA256_V2.zag` copied into each
  `src/` dir with EXACTLY one line removed — the
  `@import("R33_NATIVE_IO_V1.zag")` (line 5). `diff` vs the toolchain
  original proves the delta is that single line; `nio_free` added to
  `nio_shim.zag` (byte-identical semantics to the IO module); the SHA
  module uses only `nio_alloc`/`nio_free` (verified by grep). The three
  vendored copies are byte-identical to each other
  (`sha256 acdd3c48…5e6818`; toolchain original `9824f6db…17ca683bcf`).
- `sp_gate.zag` byte-identical across `build/`, `redteam/`,
  `longhorizon/` `src/` dirs (as before the repair).
- All builds with the pinned toolchain ONLY:
  `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.

## 2. Pre-repair frozen baseline (K5 reference)

Built from a pristine copy of the untouched original tree
(`prerepair_tree/`), pinned znc, 3× each battery, byte-identical:

| battery | SHA-256 (3/3 identical) | tail |
|---|---|---|
| smoke | `6855928854e38255e7275a18c5b07c82675fe1bc0752a616ba9ca90ba2e6d2e0` | OB_FAILURES,0 |
| redteam | `3fa5a17ae97cbf2107880f2f7c6b98fe2af33ed28575c880cacadb3cae37025c` (3/3 byte-identical) — run1 findings include the vulnerable `N1-FORGED-ID,syn-emit-as-overseer-accepted-weight-42` and `N2-FORGED-CLASS,non-overseer-emits-overseer-only-force-pin`, the residual being repaired | RT_FAILURES,0 |
| lh B-alone | `cc7e86ed4a00be36bb4f5a2aacc6456197281270b4eb40717ebb1ca017ea93e9` (3/3 byte-identical) — matches the frozen LONGHORIZON_REPORT.md value exactly | OB_FAILURES,0 |
| lh integrated | `356b7873bf07942c6b2283ed087911d3bfa724cea1ab707fb1ccaf14821cec3b` (3/3 byte-identical) — matches the frozen LONGHORIZON_REPORT.md value exactly | OB_FAILURES,0 |

## 3. Kill-bar accounting

**Post-repair battery SHAs (3× byte-identical each):**
- smoke: `6855928854e38255e7275a18c5b07c82675fe1bc0752a616ba9ca90ba2e6d2e0`
  (OB_FAILURES,0) — **byte-identical to the pre-repair baseline**
  (`cmp` clean on all three runs).
- redteam: `3e5731a9048fc3300c3c5a29248650bb7c1cd26bc005f3c38baa65f46cb33e35`
  (RT_FAILURES,0) — K5 diff vs pre-repair: only N1/N2/N3 lines (35 diff
  lines, zero outside N1/N2/N3).
- lh B-alone: `cc7e86ed4a00be36bb4f5a2aacc6456197281270b4eb40717ebb1ca017ea93e9`
  (OB_FAILURES,0) — byte-identical to pre-repair baseline.
- lh integrated: `356b7873bf07942c6b2283ed087911d3bfa724cea1ab707fb1ccaf14821cec3b`
  (OB_FAILURES,0) — byte-identical to pre-repair baseline. (Build note:
  the integrated binary is built from `ob_lh_int.zag`, which does not
  contain the B7 fixture; the fixture correction touched only
  `ob_test_integration.zag`. The binary was rebuilt from byte-identical
  sources after the correction — same 422848-byte output as the
  pre-correction build — and the 3/3 evidence from the pre-correction
  build stands. A re-run with the rebuilt binary produced
  byte-identical output through the s100l stream before being stopped
  for system-load reasons; the committed evidence is the full 3/3.)

- **K1** (forged requester_id + attacker-minted UNKEYED hash →
  REFUSED_UNAUTHENTICATED, fwd=0, rson=SP_R_UNAUTH,
  SP_L_REFUSED_UNAUTH row with NAUTH_R_BAD_TAG, no install/weight/nonce
  consumed; victim's nonce intact): **PASS** — `rn_n1_forged_fwd,0,0`,
  `rn_n1_forged_disp,0,0` (WITHHOLD), `rn_n1_forged_unauth,9,9`,
  `rn_n1_forged_badtag,3,3` (BAD_TAG), `rn_n1_victim_intact,1,1`;
  finding `N1-FORGED-ID-REFUSED`.
- **K2** (forged overseer-only M_FORCE_PIN refused AT AUTH, never
  reaches authority-class check, never installs; positive control: real
  overseer pin installs; defense-in-depth: valid-key non-overseer pin
  refused at class with NAUTH_R_UNAUTHORIZED_CLASS): **PASS** —
  `rn_n2_forged_pin_badtag,3,3`, `rn_n2_real_pin_install,1,1`,
  `rn_n2_class_reason,4,4`; finding `N2-FORGED-CLASS-REFUSED`.
- **K3** (replay of consumed envelope → NAUTH_R_BAD_NONCE): **PASS** —
  `rn_n5_replay_refused,0,0`, `rn_n5_replay_unauth,9,9` (redteam N5
  control) and smoke `replay_fwd,0,0`.
- **K4** (wrong-key tag → refused at auth): **PASS** — N2 oracle (ii)
  `sp_auth_tag_key` with SYN's key on overseer-claimed envelope →
  `rn_n2_forged_pin_badtag,3,3` (BAD_TAG at auth, never reaches class).
- **K5** (legit-traffic verdicts byte-identical to §2 refs; intended
  deltas only): **PASS** — the post-repair smoke output is
  **byte-identical** to the frozen pre-repair baseline (`cmp` clean,
  3/3 runs, SHA `68559288…` both sides). The B7 printed fixture
  (`b_hashkat`, `ob_test_integration.zag`) was restored to
  `sp_auth_make_legacy`, preserving the frozen line
  `OB_CHECK,ih_auth_deterministic,-1251831065,-1251831065` exactly.
  The earlier one-line HMAC sample delta was rejected per the 2026-09-25
  00:09 UTC checkpoint and is NOT carried as an intended delta.
  Mechanism confirmation (not an output license): the HMAC sample tag was
  independently recomputed in Python
  (`hmac.new(FNV-derived fixture key for org=5,
  msg=LE32(5,41,112,7,9)), sha256)[:4]` as LE i32 = `-800455180`) —
  byte-for-byte equal to what the Zag binary computed before the fixture
  restore, proving the built binary carries the correct preregistered
  derivation constants and implements the full chain correctly.
  Red-team K5: 35 diff lines, all within N1/N2/N3; N4/N5/F1-F4/R1-R4
  byte-identical. LH K5: both suites byte-identical to pre-repair.
- **K6** (nonce-desync self-heal under keyed tags): **PASS** — redteam N3:
  desync → `rn_n3_desync_refused,0,0` + `rn_n3_desync_reason,2,2`
  (BAD_NONCE) → catch-up → `rn_n3_healed_fwd,1,1` +
  `rn_n3_healed_install,1,1`; finding `N3-DESYNC-HEALED`. (First
  post-repair attempt exposed a TEST bug — healed emit reused N1's
  installed pine draft → correct duplicate withhold; fixed to a fresh
  `oak` atom. Mechanism was never wrong.)
- **K7** (zero RNG in decision paths): **PASS** — grep backstop: zero
  hits for `rand|srand|random|lcg|entropy|/dev/urandom|getrandom`
  across all three `src/` trees including the vendored SHA module;
  empirical backstop: all four suites 3× byte-identical.

## 4. Known/documented downgrades (prereg §4, unchanged)

32-bit tag truncation; FNV-derived fixture keys (mechanism test only);
testbed driver holds all keys (attacker oracles never touch the
victim's key — the documented attestation boundary).

## 5. Evidence to commit

`PREREG_R1.md` (committed `2e8a947c7fbc`); repaired sources
(`sp_gate.zag` ×3, `ob_test_integration.zag` ×2 incl. longhorizon copy,
`ob_test_redteam.zag`, `ob_lh_int.zag`, `corpus_probe.zag`,
`nio_shim.zag` ×3, vendored `R33_NATIVE_SHA256_V2.zag` ×3); this
(corrected) verdict; run evidence (`refs/prerepair/` + post-repair run
outputs + SHA-256s). Binaries and `.zagd` files NEVER committed.
Superseding evidence commit: see §6.

## 6. Commit record

- Prereg (frozen, committed first): `2e8a947c7fbc761080eb186d8a2385c75327ce23`
  (`docs/lab/onebrain/pam_integration/repairs/R1/PREREG_R1.md`).
- Original (incorrect-K5) evidence bundle: `2cf1ee7cc1df8e5c2eeda744ae9bcae2225fdc5e`
  — SUPERSEDED by the correction commit below. Do not cite its K5 claim.
- Correction evidence bundle: `f0c257656fc4d1763ab2a094426d50ab903788a6`
  (`docs/lab/onebrain/pam_integration/repairs/R1/`, 3/3 smoke outputs
  byte-identical to the frozen baseline, corrected verdict).
