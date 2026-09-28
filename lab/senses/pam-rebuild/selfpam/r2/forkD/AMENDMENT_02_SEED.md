# FORK D AMENDMENT 02 — PRIVATE SEED HANDLING (SUPERSEDES AMENDMENT 01 §2.2/§4)

**Date:** 2026-09-27 | **Branch:** `tnn-native-lab` (sylorlabs/TNN)
**Parent preregs:** `AMENDMENT_01_PARTITION.md` (frozen, commit
`9c6eacc5b1a22557c124dacb7e8ed3489a524158`); `FORKD_PREREG.md` (frozen,
fork D)
**Status:** FROZEN on commit. This file is committed ALONE, before any
verifier is compiled or any evidence battery is run. Amendments require
the coordinator.

## 0. Why this amendment exists

Amendment 01 §2.2 pins the channel's private seed as a public ASCII
constant (`selfpam-forkd-partition-channel-v1`) and §4 has `channel.py`
derive signing keys from that committed seed. That defeats the strongest
reading of "the generator cannot author EXT": anyone holding the repo
could re-derive the signing key and mint entries. Amendment 01's own
threat model (§1: "cryptographic forgery — mechanically impossible
without the channel key") requires the channel key to be actually
secret from the generator. A committed seed makes the forgery game
dishonest: B1 would test the verifier against forgeries the attacker is
defined as unable to produce only by convention, not by mechanism.

This amendment supersedes Amendment 01 §2.2 (seed clauses) and §4
(channel construction) as follows. Everything else in Amendment 01 —
partition layout, WOTS parameters, hash chaining, pinned genesis keys,
verdict modes, bars B1–B4 — is unchanged.

## 1. Seed handling (frozen)

1. The channel private seed is EXTERNALLY HELD. It is never committed
   to the repo, never embedded in `channel.py`, never printed, never
   written to any committed file.
2. `channel.py` receives the seed through a protected UNCOMMITTED
   input: a seed file outside the repo (read at signing time) or an
   environment variable. The script refuses to run its signing commands
   if no external seed is provided.
3. Only the following are committed: the genesis PUBLIC keys
   (`genesis.zag`), the signed EXT partitions, the GEN partitions, the
   channel source WITHOUT any seed, and this amendment.
4. Signing remains DETERMINISTIC for a fixed seed: the same seed +
   the same atom list always yields byte-identical partitions. There
   is no RNG anywhere in the verifier or the decision path (B4 grep
   gate unchanged).
5. The ASCII seed named in Amendment 01 §2.2 is RETIRED. It MUST NOT
   appear in any committed file. Any local development copy that
   embedded it is sanitized before the evidence commit.

## 2. What this changes about the security claim

With the seed externally held, "the generator cannot author EXT"
becomes a mechanistic claim rather than a convention: minting a valid
EXT entry requires the WOTS private key, which is derived from a seed
the generator's partition-writing path never observes. The B1 forgery
cases (wrong-seed signature, attacker-owned keychain, bit-flipped
signature, reordered entries) test exactly the attacks available to a
seed-less adversary.

## 3. Explicit non-claim

This experiment does NOT claim the external seed is unstealable in
general, nor that WOTS with SHA-256 is the right production choice.
The claim is narrower: *given* an independent channel that holds its
key outside the generator's reach, fork D's discipline can be rewired
to consume partition membership instead of a forgeable label, with
zero measured change in verdicts (B2) and fail-closed behavior under
forgery (B1). Key custody is the channel's problem; label-forgery is
what this experiment kills.

## 4. Field layout (clarifying, not changing)

Amendment 01 §1.1 writes the EXT entry as
`ENTRY|<tag>|<atom>|<prev_hex>|<pknext_hex>|<sig_hex>` where `<atom>`
is the 5-field canonical atom. Since canonical atoms contain `|`,
a serialized EXT entry is TEN pipe-separated fields:
`ENTRY|tag|Q|S|POL|R|O|prev|pknext|sig`.
A GEN entry is EIGHT fields: `GENENTRY|tag|Q|S|POL|R|O|prev`.
The verifier parses field counts (10 / 8), never the conceptual
6-field shorthand. No semantic change.
