# C1-CLEAN Freeze Record

Date: 2026-09-30 UTC
Prereg: PREREG_C1CLEAN.md (frozen as 13e4b1ce3 before implementation)

This commit freezes the contestant, world generators, and sequencer.
World generation begins AFTER this commit. Any contestant modification
after world generation VOIDS the wave.

## Contestant (frozen)

Source: contestant.zag (copy of lifetime_race/race_tnn.zag amended source)
  sha256: 4ef635cd3705f66fea6bfa518bd6e63cea2bd1f96fe97fbade11488f19f56589
  Byte-match with amended source verified. Contains the one-line
  hypothesis-weight fix (line_end(buf,loff)).

Binary: contestant_bin (znc 2026.07.0-dev, native)
  sha256: 8c7ccf308b46e193defeba137c701076cb5b7f7bed28f0393c314bf8bcaa48e4
  size: 147523 bytes
  Binary hash matches the void wave's amended binary hash, confirming
  deterministic compilation.

## World generators (frozen)

Canonical: world_gen.zag (copy of lifetime_race/race_world_gen.zag)
  sha256: 7f326f5f3209be6a2057d8cd3ae7d99b5b9ae205fdb315ad3fe6f97dfca8cde3
Binary: world_gen_bin
  sha256: 71d887de530df94ca16edc1f50ebca5e3f1e6370fa25784ef1d24ea7ab5a97ee
  size: 175840 bytes

Hard: world_gen_hard.zag (modified copy; 5 harder variants)
  sha256: d516659e783cc8f0b619c81d23f5d69e3cffc8d5c8da183db8836ec3687a2436
  Modifications from canonical:
  - H-B: stage B 3-hop (ci<6) / 4-hop (ci>=6) chains; qb_chain3 extended
  - H-C: stage C 5 immediate corrections; C6 delayed, C7-C8 collateral
  - H-D: stage D pair 3 never resolves; D6 expects UNRESOLVED
  - H-J: stage J 4000 noise observations (was 2000)
  - H-L: stage L law reverts to original; L3-L4 re-adaptation queries
  Smoke-tested on dummy seed: valid turns.jsonl + key.json, contestant
  processes turns and answers queries without crash.
Binary: world_gen_hard_bin
  sha256: 4da56cc3aaadadabc1ba5deeaa31705eb18b07359fd631b04e8eaf80fc73c5af
  size: 184214 bytes

## Sequencer (frozen)

run_race.sh (copy of lifetime_race/run_race.sh, shell only)
  sha256: 4cd7bec75915fb93dc8e874d25f9ec6428ee604beadff79b9357ea1c092850a9

## Protocol

- New seeds (3 canonical + 2 hard) will be derived from /dev/urandom
  AFTER this freeze commit, installed blind (hashes only viewed).
- Worlds generated AFTER seed derivation.
- Contestant runs 3 reps per world from fresh state.
- Zero Python. Zero em dashes. Commits local. Nothing pushed.
