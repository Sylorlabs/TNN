# Governance Reproduction Report: Wave 2026-09-30

Date: 2026-09-29 PDT (runs completed 2026-09-30 00:38 UTC).
Worker: Governance/Reproduction Worker (independent subagent).
Method: For each target, the builder's .zag source was extracted from
the committed git blob at the result commit (`git show <commit>:<path>`,
never a working tree), compiled with the frozen toolchain
`znc 2026.07.0-dev (edition 2026)`, and executed 3 times. Output md5 of
each run was compared to the md5 of the raw output committed in the
result commit. Ancestry was checked with `git merge-base --is-ancestor`.
Python contamination was checked by scanning every commit in the
prereg..result range for .py files.

## Results

### H-UNIFIED11 (result commit fcbb8fac3): REPRODUCED

- Source: unified11_learn.zag from blob, md5 c864b2d5452743a39c1e85e50db2dc66.
- Compiled clean, 3 runs: exit 0, zero stderr, md5
  55f716a6a33c0655b662c4b9d4bb359e on all 3 runs, cmp byte-identical.
- In-program verdict: "=== RESULT: 31/31 ===", "H-UNIFIED11 SURVIVES".
- Ancestry: prereg b5a74dd9d (prereg-only commit) is a strict ancestor
  of fcbb8fac3. No .py files in range.
- No em dashes, no binaries committed by this worker.

### H-REVISE11 (result commit 1a2fd99bd): REPRODUCED

- Source: revise11.zag from blob, md5 119d77d0a285d9c5500cd2e8ecd6a3cc.
- Compiled clean, 3 runs: exit 0, zero stderr, md5
  0fcb31f29db9d05a1c80809aa78619c3 on all 3 runs, cmp byte-identical.
- In-program verdict: "=== RESULT: 145/145 ===",
  "H-REVISE11 SURVIVES". 129 CHECK lines all PASS; 0 CHECK FAIL.
- Ancestry: prereg 36b2fbc71 (prereg-only commit) is a strict ancestor
  of 1a2fd99bd. No .py files in range.
- Note: the independent red team (RV11-ADV) was self-declared
  EXPLORATORY due to pre-prereg toolchain builds. This reproduction is
  independent of that red team and does not cure its contamination.
  The standing H-REVISE7 through H-REVISE11 governance quarantine is
  unaffected.

### H-SEG9 (result commit 1ffa82a68): REPRODUCED

- Source: seg9_learn.zag from blob, md5 dc56586e800f3b52df4664d2b47d8d33.
- Compiled clean, 3 runs: exit 0, zero stderr, md5
  983d78de98b90aa2eeaebda216c8c9b6 on all 3 runs, cmp byte-identical.
- In-program verdict: "H-SEG9 COMPLETE", 3 PASS lines, 0 FAIL lines.
- Independent bar verification from the reproduced output:
  - K-SG9-1: SG9-K02..K14 NOPT values are exactly 2,4,8,...,8192.
  - K-SG9-2: NDINFO pairs are SG9-BIG (64,1), SG9-HUGE (128,2),
    SG9-XL (256,3), SG9-K11..K14 (64,1); the sat bit flips exactly
    between K10 (512) and K11 (1024), straddling the 1000 boundary.
  - K-SG9-3: regression structure present (inherited sections
    byte-identical in the committed-raw comparison).
  - K-SG9-4: determinism confirmed by the 3/3 byte-identical runs.
- Ancestry: prereg 43482e649 (prereg-only commit) is a strict ancestor
  of 1ffa82a68. No .py files in range.

### H-INTENT-UNIFIED9 (result commit 3d6a27625): REPRODUCED

- Source: iu9_verify.zag from blob, md5 f04f3cb206c2de9c5400317bc7c22278.
- Compiled clean, 3 runs: exit 0, zero stderr, md5
  933077edbb441bdd0d0df163d1f843db on all 3 runs, cmp byte-identical.
- In-program verdict: "H-INTENT-UNIFIED9 SURVIVES".
- Ancestry: prereg 778079959 (prereg-only commit) is a strict ancestor
  of 3d6a27625. No .py files in range.

## Summary

4 targets, 4 REPRODUCED, 0 REPRODUCTION-FAIL, 0 ANCESTRY-VIOLATION,
0 PYTHON-CONTAMINATION.

Reproduction confirms buildability from committed blobs, determinism,
and output identity with the committed raw evidence. It does not
adjudicate red-team outcomes, canonical acceptance, or L2/L3
classification. Those remain with the parent agent under the
2026-09-29 promotion pipeline.
