# SEALED EVALUATION: WIDE-EIG-10 (wave-20261002-0521pdt, lane TRADES)

Frozen kill bars: wave-20261002-0221pdt/TRADES/PREREG_TRADES1.md 5,
frozen at bbb986a79, never moved. Implementation bb824c7a7.
8 sealed worlds, seeds 1001..1008. 40 runs: WIDE x3 on all 8, F_CM x1
on all 8, SINGLE x1 on all 8. Zero em-dashes in this file.

## 1. Scores

| World | WIDE r1 | WIDE r2 | WIDE r3 | F_CM | SINGLE |
|---|---|---|---|---|---|
| 1001 (X->Z->Y) | 1000 | 1000 | 1000 | 1000 | 0 |
| 1002 (Y->Z->X) | 1000 | 1000 | 1000 | 1000 | 1000 |
| 1003 (Z->Y->X) | 1000 | 1000 | 1000 | 1000 | 0 |
| 1004 (Y->Z->X) | 1000 | 1000 | 1000 | 1000 | 1000 |
| 1005 (X->Z->Y) | 1000 | 1000 | 1000 | 1000 | 0 |
| 1006 (Y->X->Z) | 1000 | 1000 | 1000 | 1000 | 1000 |
| 1007 (X->Y->Z) | 1000 | 1000 | 1000 | 1000 | 1000 |
| 1008 (Y->X->Z) | 1000 | 1000 | 1000 | 1000 | 1000 |
| TOTAL /8 | 8/8 | 8/8 | 8/8 | 8/8 | 5/8 |

WIDE 24/24; F_CM 8/8; SINGLE 5/8. The 3 SINGLE failures answer X->Y->Z,
the lexicographic default, on worlds whose true chain is not X->Y->Z.

## 2. Cost (honest)

- Structural deliberation count: 30 vs 3 EIG searches per world, exactly
  10.0x (verified: 30 choose_int turns per WIDE run, 3 per SINGLE run).
- Measured forward-sim ratio: WIDE total 12288 vs SINGLE total 1116 =
  11.01x across the sealed set. Per-world: 8.92, 14.50, 8.93, 13.93,
  9.42, 13.96, 8.98, 15.96. Sims per search scale with the hypothesis-set
  size, which is world-dependent; the aggregate is the bar's unit, matching
  the dev prototype's single 10.0x figure. The candidate really spends the
  budget: no cheap imposter.
- F_CM compute: 11548 sims vs WIDE 12288 (0.94x), compute-matched in
  aggregate. Disclosure: per-world F_CM sim totals differ from WIDE
  because the random pick produces different intervention histories, so
  hypothesis-set sizes diverge on later turns. The search PROCEDURE is
  identical (cau_eig runs before the override on every turn; only the
  argmax differs). The prereg's parenthetical "identical sim count" does
  not hold world-for-world; it holds as procedure identity plus aggregate
  budget parity. Reported here, not hidden.
- Wall clock: WIDE 7647.75 ms/run vs SINGLE 1603.5 ms/run = 4.77x.
  Wall is compressed by fixed per-turn process-spawn overhead (75 vs 21
  invocations); the 10x is in deliberation steps and forward sims.
  Bytes: binaries 189855 each; state 16384 bytes fixed.

## 3. Kill bar verdicts

K1 (capability >= 7/8): PASS. 8/8 on all 3 reps.
K2 (WIDE - SINGLE >= 1): PASS. 8 - 5 = 3.
K3 (WIDE >= F_CM): PASS. 8 >= 8, non-inferiority. Stated plainly, as the
  prereg requires: the EIG choice rule contributes nothing at 30 pooled
  interventions; F_CM matches 8/8. The gain comes from the ensemble plus
  pooling architecture and the hypothesis/pruning machinery, not from
  EIG superiority. This is the dev finding reproduced, not an overclaim.
K4 (cost): PASS. Structural 10x; aggregate sim ratio 11.01 in [8,12];
  wall-clock 4.77x reported.
K5 (determinism): PASS. 3/3 byte-identical stripped reply streams
  (ms+rss_kb excluded, the v6 K6 exclusion class) and byte-identical
  stderr traces on all 8 worlds.
K6 (no regression): PASS. world_gen and arena rebuilt from committed
  competitive_arena sources, hashes match the refreeze record
  (c4c8340c..., 3899577b...); turns.jsonl regenerated hash 0fc3edb0...;
  trades_wide over the 131-turn 68-item battery produces a stripped reply
  stream byte-identical to the INQ sealed run (58/68, C9 0.000 by design,
  no discrim parser added).
K7 (sealed validity): PASS. causal_world rebuilt from committed source;
  all 8 worlds regenerate byte-identically (keys match prerun_hashes.txt);
  agent source grep: zero seed hits, zero chain-order literal hits, zero
  key.json references; key.json chmod 000 during every agent run.
K8 (pure Zag): PASS. which python3 returns nothing at lane start and
  lane end; zero non-safebin executable invocations (bash/awk/grep/sed/
  sha256sum/cut/date/chmod/cp only; two failed command-not-found attempts
  for tools absent from safebin are not invocations). Any forbidden
  invocation would be PROCESS-FAIL; none occurred.
K9 (architecture): PASS. Delta: +324 lines, 0 removed; 0 new modes,
  bridges, routers, task-specific handlers, hardcoded semantic cases,
  hardcoded entities/variables/chains/answers. 10 per-trace hypothesis
  sets plus the pooled verdict set in learner state (W 14000..16384),
  visible in the stderr trace. state_bytes is a fixed 16384-byte
  allocation, so structure creation is evidenced by the trace rather than
  by byte growth; disclosed here.
K10 (no L3 claim): PASS (disclaimer). The hypothesis space (6 chains),
  the forward model, and the pooling rule are researcher-authored
  (fails C0-A); the inquiry form is fixed, not constructed from
  experience (fails C0-B); no unforeseen representational forms (fails
  C0-C); no new representation is invented (fails C0-D). This is L2
  experimental-design infrastructure, not L3 representational invention.

BUILD-PASS requires K1, K2, K4, K5, K6, K8: all PASS. K3, K7, K9, K10
also PASS. Verdict: BUILD-PASS on all ten frozen bars.

## 4. Scope

This is a CANDIDATE mechanism only. No L3 claim (K10), no TNN-2
substrate claim, no TNN-beats-LLM claim. The canonical 0.573 is not
moved. FW1-FW9 is a regression battery; nothing here generalizes beyond
the 3-variable chain intervention domain tested.
