# DEVINT1 Adversary: Final Synthesis (all six attacks complete)

Worker: independent reproduction + adversary subagent.
Date: 2026-09-30.
Target: DEVINT1, builder `476c24b3d`, prereg `4b50ff7d4`.
Adversary prereg: `60701a55f` (frozen before any attack implementation).

## Phase 1: REPRODUCED

4/4 bars from committed source; 3/3 byte-identical runs, exit 0, zero stderr;
md5 `612205f6e8a36f7f6e04134f3ef8014e` matches canonical; prereg strict
ancestor; zero Python. Report: `REPRO_REPORT.md` (`fa747a3b1`).

## Phase 2: six attacks

| # | Attack | Verdict | Exact numbers |
|---|--------|---------|---------------|
| A1 | online feed (no future data) | PARTIAL | S2 6/6 segs (byte-identical lines), 4/4 morphemes, BUILD-PASS; but bik 11->8 (-27%), gup 14->11 (-21%), bigrams 12->19, boundary 2->3, S8 acc 1/6->3/6, evictions 17/18->21/21, 2 spurious S3 concepts (bi:2, kgup:2) from t=0 empty lexicon |
| A2 | seg controls (fw2/fw4/randwidth) | ATTACK-SUCCEEDS | treat k=5 spur=0; fw2 k=-1, fw4 k=-1, randwidth k=-1 (none cover in 12 eps). Builder S4 neutral (5=5) confirmed width-match artifact; S4 synergy REVIVED as positive |
| A3 | synergy, independent code | ATTACK-FAILS | (a) 4 vs 5, (b) 8/12 vs 0/12, (c) 1 vs 0: all three reproduced exactly, same signs, non-degenerate |
| A4 | causal ablation | ATTACK-FAILS (1/3; needed 2) | noSeg: 0 degradation; noConcepts: 0 degradation; noRules: S10 probe 8/12->3/12 (causal, >=50% of gap). ACTIVE/rollback machinery carries probe advantage; concept inventory beyond interning is inert on measured metrics |
| A5 | 240-episode interference | ATTACK-FAILS | recog 17/17 (>=15/17), proc reuse 3/3; S1..S9 byte-identical to baseline |
| A6 | restart across process death | ATTACK-FAILS | checksum match 3/3; S10/S11 byte-identical to baseline; persistence real |

## Interpretation

No attack killed a core DEVINT1 claim. The trajectory, stage numbers, and
synergy signs survive: true online feeding (A1), width-mismatched controls
(A2), independent reimplementation (A3), 12x interference (A5), and process
death (A6).

Two findings refine the claims rather than killing them:
- A1 PARTIAL: the developmental trajectory is qualitatively robust to feed
  schedule but quantitatively sensitive (concept counts, bigram inventory,
  eviction counts shift). The reported exact numbers are schedule-dependent.
- A4: synergy is causal but narrowly carried. The S10 probe advantage comes
  from the ACTIVE/rollback rule machinery, not from bigram frequency or
  from the concept inventory (which is causally inert beyond string
  interning on every measured metric). The S6 procedure gap is carried by
  1-substitution recognition over interned strings.

One finding strengthens a claim:
- A2: the builder's disclosed-neutral S4 becomes positive against honest
  controls. SEG-core strictly dominates width-mismatched chunking.

## Governance notes

- All attack programs derived from committed builder source; all builds,
  runs, and verification pure Zag (znc, bash, grep, cmp, md5sum).
- Worker B disclosure: one shell-analysis step used Python to split output,
  then redone compliantly with `cmp`; committed RAW files and verdicts rest
  on the `cmp`/`md5sum` checks only. Flagged for parent judgment on
  canonical standing; the evidence itself was verified with allowed tools.
- No em dashes in any owned docs (byte-verified pre-commit).
- All commits local; nothing pushed.

## Commits (branch tnn-native-lab, local only)

- `60701a55f` adversary prereg (frozen, alone)
- `fa747a3b1` reproduction REPRODUCED
- `46d42d9c4` Worker A: A1 + A2
- `f73d897bd` Worker B: A3 + A4
- `46757d8d6` Worker C: A5 + A6

## Status

All six attacks complete. The BUILD-PASS (engineering) stands uncontested.
No kill. The SURVIVES decision is reserved to the parent/research director
per the standing directive.
