# FREEZE: C1 law-revert attack

Frozen 2026-09-30. Prereg: commit 482980e9f (PREREG_REVERT_ATTACK.md, committed alone before any implementation).

## Frozen components (sha256)

| component | sha256 |
|---|---|
| contestant_bin | 8c7ccf308b46e193defeba137c701076cb5b7f7bed28f0393c314bf8bcaa48e4 |
| run_race.sh | 4cd7bec75915fb93dc8e874d25f9ec6428ee604beadff79b9357ea1c092850a9 |
| world_gen_revert.zag | 18f7d18cf851f20fef70eaf13512f087a90f4d481070484a7b328d61fcfac269 |
| world_gen_revert_bin | baa7b0e8a84253b264f2bfa6d4032708af026c89387c7184aae18a25c3a7060d |
| diag.zag | 8ef4964a4e388d4e43bb7d8bf4bf05d727ced87ca2d7c0bc818294f5508d9f9e |
| diag_bin | 40a7464c985f2861662d3951835284d531e236dae22578bb61921579fc54a2e1 |
| agg.zag | 3bfc06dbcf004f613478d6d6a26a2dfe796ecf1a61b261b93e231c451b2e61cc |
| agg_bin | c2954edf66c0fd4e6a450c2b684c565124c2122bf1bb737ba4dfcb49f4d8b8d2 |

contestant_bin and run_race.sh hashes match the C1-CLEAN FREEZE.md record exactly: the frozen contestant is byte-identical to the canonical C1-CLEAN contestant.

## Toolchain

znc 2026.07.0-dev (edition 2026) at /home/hatch/workspace/tnn-forkbattery-1121pdt/local-tnn-native-lab/znc. Branch: tnn-native-lab.

## Design notes (frozen)

- world_gen_revert.zag: 4 families x 8 worlds. F-A exact revert A to B to A (2+2 post demos), F-B partial revert (1 reverted demo), F-C revert with 300 noise confounders, F-D double change A to B to C. Minimal worlds (~15 turns; ~315 for F-C). Demo/query regime mirrors C1-CLEAN hard worlds. RNG: xorshift64 seeded from the 8-byte seed file.
- diag.zag: replays turns.jsonl in order, maintaining the exact sup-flag revision state the contestant's ingest_law/ingest_demo specify. At each query turn it predicts from the live demo set at THAT turn with an independent re-implementation of the class cascade (map, rev, dup, rot, fallback). After the sweep it verifies the replayed final sup flags against the contestant's recorded state.txt (STATE-MATCH over every D line). Per-query D1 (detection: pre-law demo still sup=0) and D2 (diagnosis: post-law demo sup=1) come from the replayed trace; the final state alone cannot time-slice sup flags, so the replay validated by STATE-MATCH is the rigorous basis. Miss location: DETECTION / DIAGNOSIS / APPLICATION / UNCLASSIFIED / HIT-OK. Also reports p4 (demos superseded at the first law notice stay sup=1, never restored).
- agg.zag: reads 4 concatenated family diag outputs, prints per-family totals and P1-P5 verdicts.
- diag validated on the original C1-CLEAN H0 run: reproduces the known L3 miss (pred=tyxt actual=tyxt class=rev loc=APPLICATION), 8/8 agreement, state_match=YES over all 10 D lines, p4=OK/3.

## Protocol (frozen)

1. 32 fresh 8-byte seeds from /dev/urandom AFTER this freeze (8 per family), blind handling, record hashes only.
2. Each world generated twice; turns.jsonl and key.json must be byte-identical.
3. run_race.sh per world x 3 reps (96 runs); per-world replies byte-identical across reps.
4. diag_bin per run; outputs concatenated per family; agg_bin over the 4 family files.
5. Verdict against P1-P5 in PREREG_REVERT_ATTACK.md.
