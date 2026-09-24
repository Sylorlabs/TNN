# H6-R3 fork D — VERDICT (2026-09-24)

## KB1 — generator write/relabel/forge path: PASS (no kill)
8 build gates, all passing, build-killing on violation:
1. `evpart_write.zag` is `@import`'ed only by `ingest.zag`.
2. The `forkD` binary's source closure (main/io/str/tables/atom/atomize/
   prover/delib/gen/gen_m7/facts/evpart_read) contains no writer reference
   (`part_create|part_append_entry|part_seal|evpart_write`).
3. `evpart_read.zag` contains no `file_write(` call.
4. The ingest path (`ingest.zag`, `ingest_main.zag`) imports none of
   gen/gen_m7/atomize/delib/prover — the sensor cannot fabricate drafts.
5. No `"|GEN"` / `"|EXT"` label literals in code.
6. No RNG tokens (rand/rng/seed/clock/getrandom/time()).
7. No `as []i32/u32/u16` mistyped casts.
8. No `,577,` (O_TRUNC) open in `evpart_write.zag` — the writer is
   create-only (`O_EXCL`); verified at runtime: re-ingest and re-seal fail
   loudly, originals untouched.

No generator-reachable write, relabel, or forge path exists. Provenance is
physical partition membership: the partition format has no provenance
field at all.

## KB2 — reproduce R2 D plus M7: PASS
| check | result | bar |
|---|---|---|
| M1 confab withhold | 140/140 | ≥70% |
| M2 paraphrase install | 135/140 (96.4%) | ≥90% |
| M3 pairs install | 130/130 | ≥95% |
| M4 trace-alibi withhold | 60/60 | ≥70% |
| M5 provenance withhold (generator-authored) | 60/60 | ≥70% |
| M6 clean install (false-withhold ≤5%) | 40/40 | ≥95% |
| M7 held-out corpus (350 cases, forest/water domain) | 350/350 | per-section bars, all cleared at 100% |
| byte-identical reruns ×2 | 7/7 `cmp`-clean | required |

All c1–c6 case verdicts byte-identical to the R2 reference results
(including the identical 5 M2 misses); c3 digest reproduces exactly
(`615ff288…a8814`).

## KB3 — tamper detection: PASS 9/9 (100%)
Entry flip, digest flip, swap, truncation, forged valid-chain suffix vs
stale anchor, and unpartitioned live-state mutation all detected or
neutralized; batteries on invalid partitions fail safe (0 INSTALL).

## Verdict: FORK D LIVES
All three kill bars pass. The write-once evidence partition reproduces the
R2 fork-D verdict profile exactly on the main-domain corpora, scores 100%
on the formal M7 held-out corpus, detects 100% of tampering, and the
generator has no structural path to the evidence.
