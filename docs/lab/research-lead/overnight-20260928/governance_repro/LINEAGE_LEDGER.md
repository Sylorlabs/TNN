# Lineage Ledger (Governance/Reproduction Worker)

Maintained by the Governance/Reproduction Worker. Each row records the
frozen lineage of one major claim and the independent reproduction result.
Reproduction is performed from the committed git blob of the builder's
source at the result commit, never from a working tree. Shell tools only
(git, md5sum, cmp, diff, grep). Pure Zag for rebuilding mechanisms.

Verdict key:
- REPRODUCED: rebuild from blob, 3/3 byte-identical, output md5 equals
  the committed raw md5, in-program verdict line present.
- REPRODUCTION-FAIL: any of the above does not hold. The builder's
  code is NOT modified to force a pass.
- ANCESTRY-VIOLATION: prereg commit is not a strict ancestor of the
  implementation/result commit, or the prereg commit contains
  implementation content.
- PYTHON-CONTAMINATION: a .py file appears in any commit between the
  prereg commit and the result commit (inclusive of result, exclusive
  of prereg), or Python was used anywhere in the lineage evidence.

## Row 1: H-UNIFIED11

- Claim: SURVIVES 31/31 (R12 phantom tombstone init fix; closes X-U10-2c).
- Builder verdict label: builder-claimed SURVIVES (not yet canonically accepted; red team pending at time of reproduction).
- Prereg commit: b5a74dd9d (contains only u11_frontier/PREREG_UNIFIED11.md; committed alone before implementation).
- Implementation source: unified11_learn.zag (source md5 c864b2d5452743a39c1e85e50db2dc66 from blob).
- Result commit: fcbb8fac3.
- Ancestry: prereg is strict ancestor of result (git merge-base --is-ancestor: YES; commits differ). No .py files in b5a74dd9d..fcbb8fac3.
- Committed raw md5: 55f716a6a33c0655b662c4b9d4bb359e (u11_frontier/UNIFIED11_RAW_OUTPUT.txt at fcbb8fac3).
- Reproduction: 3/3 runs, exit 0, zero stderr, md5 55f716a6a33c0655b662c4b9d4bb359e on all three runs, cmp byte-identical, in-program "=== RESULT: 31/31 ===" and "H-UNIFIED11 SURVIVES" present.
- Toolchain: znc 2026.07.0-dev (edition 2026).
- Verdict: REPRODUCED.

## Row 2: H-REVISE11

- Claim: SURVIVES 145/145 (governance-precision re-verdict of the R10 in-function contradiction guard).
- Builder verdict label: builder-claimed SURVIVES (red team RV11-ADV was EXPLORATORY due to self-reported pre-prereg toolchain builds; this reproduction is independent of that red team).
- Prereg commit: 36b2fbc71 (contains only PREREG_REVISE11.md; committed alone before implementation).
- Implementation source: revise11.zag (source md5 119d77d0a285d9c5500cd2e8ecd6a3cc from blob).
- Result commit: 1a2fd99bd.
- Ancestry: prereg is strict ancestor of result (merge-base: YES; commits differ). No .py files in 36b2fbc71..1a2fd99bd.
- Committed raw md5: 0fcb31f29db9d05a1c80809aa78619c3 (REVISE11_RAW.txt at 1a2fd99bd).
- Reproduction: 3/3 runs, exit 0, zero stderr, md5 0fcb31f29db9d05a1c80809aa78619c3 on all three runs, cmp byte-identical, in-program "=== RESULT: 145/145 ===" and "H-REVISE11 SURVIVES" present. 129 CHECK lines all PASS, 0 CHECK FAIL (the 2 "FAIL" string hits are CORROBORATE diagnostic lines on negative-evidence fixtures, disclosed in the builder result).
- Toolchain: znc 2026.07.0-dev (edition 2026).
- Verdict: REPRODUCED.

## Row 3: H-SEG9

- Claim: SURVIVES 4/4 (sat-boundary sweep + NDINFO observability).
- Builder verdict label: builder-claimed SURVIVES (SG9-ADV red team later SURVIVED all 4 attacks; reproduction independent).
- Prereg commit: 43482e649 (contains only PREREG_SEG9.md; committed alone before implementation).
- Implementation source: seg9_learn.zag (source md5 dc56586e800f3b52df4664d2b47d8d33 from blob).
- Result commit: 1ffa82a68.
- Ancestry: prereg is strict ancestor of result (merge-base: YES; commits differ). No .py files in 43482e649..1ffa82a68.
- Committed raw md5: 983d78de98b90aa2eeaebda216c8c9b6 (SEG9_RAW_OUTPUT.txt at 1ffa82a68).
- Reproduction: 3/3 runs, exit 0, zero stderr, md5 983d78de98b90aa2eeaebda216c8c9b6 on all three runs, cmp byte-identical, in-program "H-SEG9 COMPLETE" present, 3 PASS lines, 0 FAIL lines. Independent bar verification from reproduced output: K-SG9-1 sweep counts 2,4,8,...,8192 exact; K-SG9-2 NDINFO pairs SG9-BIG (64,1), SG9-HUGE (128,2), SG9-XL (256,3), SG9-K11..K14 (64,1), sat flip exactly at K10/K11 (512 vs 1024, crossing 1000); K-SG9-3 regression structure present; K-SG9-4 determinism confirmed by the 3/3 byte-identical runs.
- Toolchain: znc 2026.07.0-dev (edition 2026).
- Verdict: REPRODUCED.

## Row 4: H-INTENT-UNIFIED9

- Claim: SURVIVES 4/4 (R10 mixed-kind dispatch confirmed beyond top two, precision audit clean, no mechanism change).
- Builder verdict label: builder-claimed SURVIVES (IU9-ADV red team later SURVIVED; reproduction independent).
- Prereg commit: 778079959 (contains only PREREG_INTENT_UNIFIED9.md; committed alone before implementation).
- Implementation source: iu9_verify.zag (source md5 f04f3cb206c2de9c5400317bc7c22278 from blob).
- Result commit: 3d6a27625.
- Ancestry: prereg is strict ancestor of result (merge-base: YES; commits differ). No .py files in 778079959..3d6a27625.
- Committed raw md5: 933077edbb441bdd0d0df163d1f843db (IU9_VERIFY_RAW.txt at 3d6a27625).
- Reproduction: 3/3 runs, exit 0, zero stderr, md5 933077edbb441bdd0d0df163d1f843db on all three runs, cmp byte-identical, in-program "H-INTENT-UNIFIED9 SURVIVES" present.
- Toolchain: znc 2026.07.0-dev (edition 2026).
- Verdict: REPRODUCED.

## Standing notes

- All four targets reproduce byte-identically from their committed blobs on 2026-09-29/30.
- Reproduction confirms buildability, determinism, and output identity. It does not adjudicate red-team outcomes, canonical acceptance, or L2/L3 classification.
- The H-REVISE7 through H-REVISE11 governance quarantine is a separate standing issue and is not resolved by Row 2.
- H-UNIFIED11's independent red team is the next promotion-pipeline step for Row 1.
- The ledger grows one row per major claim. Frontier BUILD-PASS claims will be reproduced here before proceeding to baseline attack.
