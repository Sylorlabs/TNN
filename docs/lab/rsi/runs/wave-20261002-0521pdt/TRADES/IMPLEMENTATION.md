# IMPLEMENTATION: WIDE-EIG-10 (wave-20261002-0521pdt, lane TRADES)

Frozen prereg: wave-20261002-0221pdt/TRADES/PREREG_TRADES1.md,
committed alone at bbb986a79 (2026-10-02 09:47:10 UTC).
Implementation frozen at bb824c7a7 (this wave, after source audit).
Commit-order self-check: prereg commit strictly precedes every
implementation commit. Pure Zag, safebin PATH, pinned znc.
Zero em-dashes in this file.

## Adopted sources (sha256, committed at bb824c7a7)

| File | SHA-256 |
|---|---|
| trades_contestant.zag | cd01b83bab82c579a99769acb635e22bb134b20556422ba0e2247c9b3c8a37d0 |
| causal_world.zag | 09f77791e4af859442577424d3f147ac020a0367bf0302b1a5be69230c72db0e |
| causal_score.zag | 88396bd7e258aa2fe852f72af25efc4b4c60b621496b5f8b4ac |
| run_causal.sh | acb81c9d42c44ca7374b467740e9479bd9c023494246e4ba7368702b09c88e1d |

The 0221pdt worker's uncommitted implementation was audited against the
prereg before adoption: cbrief/cobs/choose_int/int_result/ctest/cdone
turn protocol matches 4.1; per-trace EIG with the frozen no-repeat rule
and trace-index-rotated tie-break matches 4.2; the F_CM build flag
(CAU_MODE=1) runs the identical EIG search then overrides the argmax
with a frozen-seed LCG pick; SINGLE (CAU_NT=1) runs trace 0 only; the
frozen aggregation rule pools all 30 outcomes into one verdict
hypothesis set with the lexicographic tie-break; no L3 machinery.
One deviation from the 0221pdt plan found and remediated: the sealed
worlds were generated before the implementation commit. Remediation:
rebuilt causal_world from the committed source and regenerated all 8
worlds byte-identical (pre.jsonl, int_table.tsv, key.json all match the
prerun hashes), so the committed worlds ARE the committed-source
worlds. No substantive effect.

## Build

Pinned znc under safebin. Three contestant variants from one-line sed
deltas on the build flags (same pattern as INQ K6a/K6b):

- trades_wide: CAU_MODE()=0, CAU_NT()=10 (10 traces, EIG argmax)
- trades_cm: CAU_MODE()=1, CAU_NT()=10 (F_CM: identical search, random pick)
- trades_single: CAU_MODE()=0, CAU_NT()=1 (1x reference)

Builds completed with analyzer warnings only (no errors). All three
binaries are 189855 bytes (the one-line flag delta changes no size).
causal_world and causal_score compiled clean.

Dev smoke (/tmp, never sealed): seed 7 world, full 75-turn loop through
run_causal.sh, ctest reply X->Y->Z matches key, score 1000.

## Architecture delta (K9)

- Cognition lines added: 324 vs the INQ base
  (wave-20261001-2321pdt/ARENA/inq_contestant.zag, 1204 lines); 0 removed.
- 0 new runtime modes, 0 bridges, 0 routers, 0 task-specific handlers,
  0 hardcoded semantic cases, 0 hardcoded entities/variables/chains/answers.
  CAU_MODE/CAU_NT are compile-time one-line build flags, not runtime
  modes; the module dispatches on the causal turn kinds parallel to the
  existing handlers, exactly as the prereg authorizes.
- Learner-state structures created: 10 per-trace hypothesis sets plus the
  pooled verdict set in W region 14000..16384 (persistent per-trace
  histories of up to 3 (k, outcome) records). Visible in the stderr trace
  (CAU t=/CAU verdict lines). state_bytes stays at the fixed 16384-byte
  allocation, so structure creation is evidenced by the trace, not by a
  byte-growth metric; reported honestly in SEALED_EVAL.md.
- The hypothesis space (6 chain permutations), the chain forward model,
  and the pooling rule are researcher-authored. This is L2
  experimental-design infrastructure, not L3. See K10 in SEALED_EVAL.md.
