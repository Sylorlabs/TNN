# Production channel-key ceremony — DESIGN

**Status: DESIGN ONLY. Blocker B5 stays open.** The frozen C1 channel test
key `SELF-PAM-C1-REG-CHANNEL-2026-09-23` remains in `selfpam/src/corr.zag`
(`corr_key()`); no production key exists, none is registered, and nothing
here changes the code. This document designs the ceremony that replaces the
test key when — and only when — the §8 sign-offs land.

Parent documents: `PREREG.md`, `selfpam/src/corr.zag` (the mechanism),
`DEMO_ONLY.md` (B5), IE amendment R2 (channel authentication, frozen).

---

## 1. What is frozen (not designed here)

The mechanism, per IE amendment R2 and `corr.zag`:

- The gate holds the channel registration key. A corroborator record
  counts as independent evidence **only** when its attestation verifies.
- `gatt = sha256hex(CHANNEL_KEY || jcode || "|" || conf || "|" || meas || "|" || evhex)`,
  where `evhex` is the 64-hex SHA-256 of the evidence bytes the
  corroborator re-read itself (preimage built by `corr_preimage`).
- The gate recomputes and byte-compares (`corr_verify`); requires
  `conf >= 700` (R3); requires the attested bytes' SHA-256 to match the
  stored `evhash` (D2, evidence-hash binding). **Any failure → WITHHELD,
  fail closed.** Unattested records arrive as absent (D1): the claim stays
  provisional, never installs.
- A forger without the key cannot produce a verifying `gatt` (SHA-256
  preimage resistance); guessing is 2^256.

The ceremony below replaces *which key* the mechanism holds. It does not
change the mechanism.

## 2. Roles

| Role | Who | Duties | Must NOT be |
|---|---|---|---|
| Ceremony officer | A named human (Micah or his delegate) | Generates the key, witnesses sealing and rotation, signs the ceremony log | The proposer or the corroborator operator |
| Gate keeper | Deployment operator | Installs the key into the gate's key store; loads it at `sp_init` time; never discloses it | Anyone who authors drafts |
| Corroborator operator | Independent party running the C1-class corroborator | Receives the key over a secure channel; uses it only to attest genuine re-measurements | The proposer (independence is what makes corroboration evidence; the key is what makes it attributable) |
| Auditor | Whoever runs the ledger audit | Verifies the sealed key-hash registry and the rotation log against the hash-chained ledger | — |

Separation of duties is load-bearing: if the proposer holds the channel
key, attestation proves nothing (the proposer can attest its own
re-observation). The ceremony's job is to make that configuration
impossible to reach by accident and visible by audit if reached by malice.

## 3. Key format and generation

- **Format:** 256-bit secret, stored and transmitted as 64 lowercase hex
  characters — a drop-in replacement for the `corr_key()` return value.
  (Enacting the ceremony requires parameterizing `corr_key()` from a
  deployment-registered value instead of the frozen string; that code
  change needs its own prereg amendment when built.)
- **Generation:** the ceremony officer generates the key from the OS
  cryptographic RNG, offline, on a machine with no network route to the
  proposer. One-time ceremony randomness: the program's zero-RNG rule
  governs *decision paths*; key generation is a human ceremony step, not
  a decision, and is logged as such.
- **Never in the repo.** The key is never committed, never pasted into
  chat, never embedded in a build artifact. What is committed is
  `SHA-256(key)` — the sealed registry entry — so any party can verify
  *which* key a deployment claims without learning it.

## 4. Ceremony steps

1. **Generate.** Officer generates the 256-bit key offline; two-person
   witness (officer + auditor). The witness records the key's SHA-256,
   the date, and both names in the ceremony log.
2. **Seal.** `SHA-256(key)` is committed to the sealed key registry
   (a committed, append-only record) *before first use*. The registry
   entry names the key id (e.g. `C1-PROD-001`), the hash, the officer,
   and the witnesses.
3. **Distribute.** The key travels to exactly two places over secure
   channels: the gate keeper's key store and the corroborator operator's
   secure store. Each recipient confirms receipt by returning
   `SHA-256(key)` (proving possession without re-transmitting the key);
   the officer checks it against the sealed registry entry.
4. **Register with the gate.** The gate keeper installs the key where the
   gate reads it at init (replacing the test-key path). Registration is
   proven, not asserted: the gate keeper runs a **registration
   attestation** — the gate verifies a known test vector
   (`corr_verify` on a fixed jcode/conf/meas/evhex with a `gatt` the
   officer computed independently) without the key ever leaving the
   keeper's store. Pass = the gate holds the sealed key.
5. **Activate.** The officer signs the ceremony log entry; the deployment
   epoch begins. From this point, `corr_observe` records attest under the
   production key. The test key is retired: any deployment still running
   the frozen test key is, by definition, not production.

## 5. Rotation

- **Scheduled rotation:** per deployment epoch (epoch length set at
  activation, recorded in the ceremony log). Steps 1–5 rerun for the new
  key (`C1-PROD-002`, …). During a grace window the gate accepts
  attestations under *both* the current and the previous key (key list of
  two, current tried first); records attested under the previous key
  remain valid through the window. After the window, the previous key is
  destroyed — witnessed, logged.
- **Emergency rotation (compromise or suspected compromise):** the officer
  revokes the key id immediately (revocation entry in the sealed
  registry), generates a replacement under the same ceremony, and the
  grace window is shortened or skipped at the officer's signed decision.
  All `corr_observe` records attested under the revoked key after the
  revocation timestamp fail closed (WITHHELD) — the ledger makes the
  cutoff auditable.
- **Rotation is ledgered.** Every generation, registration, activation,
  revocation, and destruction is an entry in the ceremony log, cross-
  referenced from the deployment's hash-chained ledger.

## 6. How the gate verifies / how a forger fails

| Attack / failure | What the gate does | Outcome |
|---|---|---|
| Genuine corroborator, correct key | `corr_verify` recomputes `sha256hex(KEY ‖ jcode ‖ conf ‖ meas ‖ evhex)`, byte-compares with `gatt`; conf ≥ 700; evhash matches | Record accepted as attested (src=1); install path available per the install law |
| Forger without the key | Cannot compute the preimage hash (SHA-256 preimage resistance) | `corr_verify` = 0 → `corr_observe` returns 0 (unattested ⇒ absent); claim stays provisional (D1), never installs |
| Wrong / stale / revoked key | Byte mismatch on recompute | Same as above: fail closed, WITHHELD on any promotion attempt |
| Replayed `gatt` on a different claim | Preimage binds jcode, conf, meas, and evhex — any change breaks the hash | Mismatch → fail closed |
| `gatt` valid but evidence bytes swapped | D2: attested bytes' SHA-256 must match the stored `evhash` byte-for-byte | Mismatch → WITHHELD (fail closed, margin unknown) |
| Empty / malformed `gatt` | Length checks (`gatt.len != 64` → 0) | Rejected before any crypto |

The gate never distinguishes "forger" from "corrupt channel" — both fail
closed. That indistinguishability is the point: the safe default needs no
diagnosis.

## 7. Honest limits — what the ceremony does NOT fix

- **Attestation proves channel membership, not corroborator independence
  or correctness.** A keyed corroborator that is correlated-wrong with the
  proposer still defeats the install rule (CC1 seqs 10983/10992 → false
  permanent). That is the CC1 guard's job (B2, DEPLOY BLOCKER), not the
  key's. The ceremony assigns the corroborator role to an independent
  party; the guard verifies the independence mechanically.
- **Key compromise is detected by audit, not by crypto.** The ledger
  (volumes, timing, and patterns of attested records) is the detection
  surface; the response is emergency rotation (§5).
- **The ceremony does not authorize the install path.** It removes one
  blocker (B5) toward a production deployment. The CC1 guard (B2), the
  write-once evidence partition (B4), the §8 sign-offs, and the live
  consumer (B1, companion design) all still stand between this design and
  any live install.

## 8. Enactment prerequisites

1. §8 sign-offs landed (the ceremony runs against frozen, signed
   parameters — key id scheme, epoch length, grace window).
2. A prereg amendment parameterizing `corr_key()` (deployment-registered
   value replacing the frozen test string) — committed before the code
   change, per the frozen-prereg amendment rule.
3. The ceremony log and sealed key registry formats frozen (append-only,
   hash-chained, committed) before the first generation.
4. Officer and witness named. Until then, the test key stays, and every
   deployment stays non-production by definition.
