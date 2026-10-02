# VERDICT_48_DOC: RT-F2V3 red team review (F2 v4 BUILD-PASS) recorded as verdict 48

Wave: wave-20261001-2321pdt.
Lane: VERDICT-48-DOC (replacement documentation worker; the RT-F2V3 lane completed with EVIDENCE-HOLDS and the result was recorded in WAVE_RECORD.md as verdict 48).

## Verdict

RT-F2V3, red team review of the F2 v4 BUILD-PASS (F2V3 lane, F2 v4 depth-9 candidate), returned EVIDENCE-HOLDS.

## Recorded sources

- Review commit: 7db48b1dc.
- Recording commit: 9bb75647d ("wave-20261001-2321pdt: record verdict 48 (RT-F2V3 EVIDENCE-HOLDS). Local only, never pushed."), adding line 81 to docs/lab/rsi/runs/wave-20261001-2321pdt/WAVE_RECORD.md.
- Lane materials: docs/lab/rsi/runs/wave-20261001-2321pdt/RT-F2V3/ (RT-F2V3_REVIEW.md, NAMECHECK.md), read-only for this documentation.

## Attack summary: 7 axes, all clean

1. Weakened bars: clean. All bars in SEALED_EVAL.md match frozen PREREG_F2V4.md verbatim (K4-R1 through K4-R7, D2=9); the K4-R4b(ii) reading is faithful, not a weakening.
2. Commit order: clean. Prereg 5e4e56a5f (06:38:18Z) strictly precedes implementation b5fcf9ae3 (06:42:42Z); the f461e812d deletion / 30a1ff7e0 restoration is byte-identical.
3. "One constant": verified exactly. The v3 to v4 diff is only L_D2() 8 to 9, discrimination sequence buffers 8 to 10 slots, ledger record 48+nhyp to 50+nhyp; zero modes, zero bridges, zero semantic cases. No mechanism change.
4. Non-vacuity: independently confirmed. Rebuilt v3-frozen binary hash 44f800c7 matches the prereg; C2-prime yields genuine depth-9 candidates.
5. Determinism: independently verified. Rebuilt v4 binaries reproduce recorded hashes exactly (9c1d44b8, bdb8f9fc); 3/3 cmp-identical reruns per world.
6. Depth-9 minimality: holds, tested stronger than the lane. An independent pure-Zag brute-force checker enumerating all sequences to depth 8 over the full 12-symbol alphabet with all 5 observables finds 0 distinguishing sequences at depth <=8; the 9-primitive witness distinguishes (A=1, B=0).
7. Knowledge-vs-architecture: clean. Resolution is fully explained by the bound raise.

No frozen bar or process rule was violated.

## Standing result

The F2 v4 BUILD-PASS stands. With this verdict, wave wave-20261001-2321pdt carries 48 recorded verdicts.

## Documentation governance

- This doc records facts verbatim from the RT-F2V3 lane and WAVE_RECORD.md line 81 (commit 9bb75647d); it introduces no new claims.
- WAVE_RECORD.md and RT-F2V3/ were read-only for this worker.
- Pure shell/file work only; no experiments, no Python; safebin toolchain guard verified in NAMECHECK.md Step 0.
- Local commits only, pathspec-restricted to docs/lab/rsi/runs/wave-20261001-2321pdt/VERDICT-48-DOC/. Never pushed.
- No em-dashes; checked with check_no_dash.sh before commit.
