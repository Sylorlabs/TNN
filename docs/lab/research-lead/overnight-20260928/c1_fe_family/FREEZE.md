# FREEZE: C1 F-E family

Frozen 2026-09-30. Prereg: commit 8246edf0f (PREREG_FE_FAMILY.md, committed alone before any implementation).

## Frozen components (sha256)

| component | sha256 |
|---|---|
| world_gen_fe.zag | 57a2b83f3914572eab5b072a3a144579750518f4499a8c9691afed3701ddb809 |
| world_gen_fe_bin | 9d8020019932bdafe9137c0eb69af9c165355b43ecaffe33babaa3af388b8f0c |
| contestant_bin | 8c7ccf308b46e193defeba137c701076cb5b7f7bed28f0393c314bf8bcaa48e4 |
| run_race.sh | 4cd7bec75915fb93dc8e874d25f9ec6428ee604beadff79b9357ea1c092850a9 |
| diag.zag | 8ef4964a4e388d4e43bb7d8bf4bf05d727ced87ca2d7c0bc818294f5508d9f9e |
| diag_bin | 40a7464c985f2861662d3951835284d531e236dae22578bb61921579fc54a2e1 |
| agg.zag | 3bfc06dbcf004f613478d6d6a26a2dfe796ecf1a61b261b93e231c451b2e61cc |
| agg_bin | c2954edf66c0fd4e6a450c2b684c565124c2122bf1bb737ba4dfcb49f4d8b8d2 |

contestant_bin, run_race.sh, diag, and agg are byte-identical to the C1
law-revert attack freeze (418b7bc89): the frozen contestant is the canonical
C1-CLEAN contestant, reused without modification. Only world_gen_fe is new.

## Toolchain

znc at ~/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1
(repo-pinned). New Zag code uses u8-backed cells with the st32/ld32
little-endian idiom; no as *i32 slice construction (2026-09-30 toolchain
lesson).

## Design notes (frozen)

- world_gen_fe.zag: family E only, 8 worlds. Exact revert kold -> 1 -> kold
  (mirrors F-A), with kold drawn from {2,3} and k2 fixed to 1 by design.
  Post-change demos: demo 1 is a period-2 word [a,b,a,b] (output
  rot(word,1), admitting keys {1,3}); demo 2 is a normal word (output
  rot(word,1), admitting {1}). The rotation class takes the largest
  matching k per demo (3 vs 1), so the class collapses by construction.
  Query words drawn from 110-122, demo words from 97-109, so query chars
  are unmapped and the char-map class cannot fire. RNG: xorshift64 seeded
  from the 8-byte seed file, mixed with worldidx.
- diag.zag, agg.zag: unchanged from the attack wave. diag replays
  turns.jsonl, predicts per query with the independent cascade, locates
  misses at DETECTION / DIAGNOSIS / APPLICATION / UNCLASSIFIED / HIT-OK.

## Protocol (frozen)

1. 8 fresh 8-byte seeds from /dev/urandom AFTER this freeze, blind handling,
   record hashes only.
2. Each world generated twice; turns.jsonl and key.json must be byte-identical.
3. run_race.sh per world x 3 reps (24 runs); per-world replies byte-identical
   across reps.
4. diag_bin per run; outputs concatenated; agg_bin over the family file.
5. Verdict against P-FE1/P-FE2/P-FE3 in PREREG_FE_FAMILY.md.
