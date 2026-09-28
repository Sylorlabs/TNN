# Red-team report — RNGSCAN-2026-09-20-v1 blind round (20 plants)

Date: 2026-09-20. Prereg: `PREREG_NO_RNG_AUDIT.md` (committed `c049b70` BEFORE any build).
Owner: Micah. Builder/auditor: Muse (subagent).

## Verdict: K2 FIRED — audit version RNGSCAN-2026-09-20-v1 is DEAD

Miss rate 1/20 = 0.05 > 0. Per the frozen kill bar K2, the version is killed.
All Arm C trials run under it are invalid (none were run — the gate held).

## Freeze record (prereg §8.2)

- Checker source: `checker/rngscan.c`, sha256
  `a35fe488fc6b0a7975a349f04899450b556db449f8a3bf98915e2086d4344371`
- Rebuilt from source immediately before the round → binary sha256
  `06af7f6bacd60a51b50af2a7470ef4521681539923590ea06306fcc0bdaa9d24`
  (identical to the pre-freeze build — no source change across the freeze).
- No checker edits, no per-plant tuning during the round. Plant list fixed and
  generated deterministically (`redteam/gen_plants.py`, no RNG).

## Method

Each plant is a complete, compilable `variation.zag` module (entry `vary_expr`
present) built with the frozen znc toolchain, then run through the frozen
checker: source scan + object scan + 2-run replay. Expectation per plant:
verdict FAIL. A PASS is a MISS.

## Per-plant results (19/20 caught)

| # | Category | Disguise | Verdict | Rules fired |
|---|----------|----------|---------|-------------|
| 01 | 4.1 entropy | getrandom literal 318 | FAIL | 4.1, 4.5, 4.3*, 4.6/4.1(obj 318) |
| 02 | 4.1 entropy | getrandom computed `300+18` | FAIL | 4.5, 4.3*, 4.6/4.1(obj 318) |
| 03 | 4.1 entropy | open(2) of "/dev/urandom" literal | FAIL | 4.1, 4.1/4.6(str), 4.5, 4.6(obj open+urandom) |
| 04 | 4.1 entropy | runtime-split "/dev/"+"urandom" path | FAIL | 4.1, 4.5, 4.6(obj open+urandom) |
| 05 | 4.1 entropy | `rdseed` token in helper | FAIL | 4.1 ×2 |
| 06 | 4.2 clock | clock_gettime literal 228 | FAIL | 4.2, 4.6/4.2(obj 228) |
| 07 | 4.2 clock | clock_gettime computed `200+28` | FAIL | 4.6/4.2(obj 228) |
| 08 | 4.2 clock | gettimeofday literal 96 | FAIL | 4.2, 4.6/4.2(obj 96) |
| 09 | 4.2 clock | gettimeofday computed `100-4` | FAIL | 4.6/4.2(obj 96) |
| 10 | 4.2 clock | `clock_gettime` token wrapper fn | FAIL | 4.2 ×3, 4.6/4.2(obj 228) |
| 11 | 4.3 uninit | read before any write | FAIL | 4.3 |
| 12 | 4.3 uninit | partial init loop, read beyond | FAIL | 4.3 |
| 13 | 4.3 uninit | early return inside init loop | FAIL | 4.3 |
| 14 | 4.3 uninit | read after nio_free | FAIL | 4.3 |
| 15 | 4.3 uninit | two buffers, init one / read other | FAIL | 4.3 |
| 16 | 4.4 hash | hashmap + bucket-order emit | FAIL | 4.4, 4.3 ×2* |
| 17 | 4.4 hash | renamed `slotmap` | FAIL | 4.4 ×4 |
| 18 | 4.4 hash | `BUCKETS` + `bucket_iter` | FAIL | 4.4 ×6 |
| 19 | 4.5 impure | ASLR leak disguised as ptr/4096 | FAIL | 4.5 |
| 20 | 4.5 impure | `get_env_flag` token helper | **PASS — MISS** | — |

\* 4.3 hits on plants 01/02/16 are path-insensitive false positives (a `nio_free`
on an early-return path marks the variable freed for later lines). Precision
issue only — verdicts were already FAIL. Noted for v2, not a kill-bar event.

Notable: the object scan caught all three computed immediates (02: `300+18`→318,
07: `200+28`→228, 09: `100-4`→96) that the source scan cannot see — the
defense-in-depth layer works as specified in prereg §7.4.

## The miss (plant20) — root cause

Plant20 defines `fn get_env_flag()i32 { return 0; }` and mixes its result into
the output. The frozen prereg §4.5 bans the identifier substring `env_`
(environment reads). The checker implements `getenv` and `environ` but NOT the
`env_` substring — a transcription gap between the frozen banned list
(BAN-2026-09-20-v1) and the implementation. `get_env_flag` contains `env_`
but neither `getenv` nor `environ`, so it passed with 0 hits.

This is exactly the failure mode the red-team round exists to catch: the audit
did not enforce its own frozen rule. K2 fires mechanically: miss rate 0.05 > 0.

## Kill-bar evaluation

- K1 (replay divergence on PASS build): not fired. The clean PASS build replayed
  byte-identical; all plant replays were byte-identical too.
- **K2 (miss rate > 0 over 20 plants): FIRED — 1 miss. Version dead.**
- K3 (banned construct on a PASSING path by post-hoc inspection): not fired —
  post-hoc review of the clean PASS module found no banned constructs (the one
  4.3 flag during the clean round was resolved by the documented fail-closed
  restructure; see BUILD_LOG.md).

## Honesty notes

- Builder and auditor are the same agent; blinding is structural (frozen
  checker, fixed plant list, no per-plant edits), not interpersonal — per
  prereg §8.4. A separate-agent red-team round is recommended for v2.
- Plant20 is synthetic (returns constant 0 — no live entropy flows). It was a
  fair plant: it tested a frozen banned token (`env_`), and the checker missed
  it. Whether the plant carried live entropy does not change the K2 mechanics.
- The 5-plant dirty round (build order step 3) caught all five planted
  categories before the clean round; those results stand as evidence but do not
  resurrect the version.

## Recommendation

v2 = one-line-class fix (add the `env_` identifier pattern to rule 4.5,
keeping the `lookup_table`/`pin_table` carve-outs), then FULL re-run of all
rounds (dirty 5 → clean → 20 plants) under a dated prereg amendment with
Micah's re-approval. The amendment must also decide the plant01/02/16
path-insensitivity precision issue (fix the dataflow or document as known
false-positive).
