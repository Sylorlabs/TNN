# RESULTS: C1 law-revert attack

Date: 2026-09-30. Verdict: REVERT-ATTACK-SURVIVES.

## Commits (all local, tnn-native-lab, owned pathspec)

- Prereg: 482980e9f (PREREG_REVERT_ATTACK.md, committed alone before implementation)
- Freeze: 418b7bc89 (contestant, generator, diag, agg sources+binaries, FREEZE.md; committed alone)
- Results: this commit (drive_revert.sh, seeds, worlds, runs, diag_out, agg.txt, RESULTS.md)

## Kill bars

- K1 ORDERING: PASS. Prereg strictly before freeze (482980e9f < 418b7bc89 in commit graph). Freeze strictly before world generation (seeds drawn from /dev/urandom after the freeze commit; hashes recorded in seeds/hashes.txt, values never viewed). Each world generated twice with byte-identical turns.jsonl and key.json (driver cmp, zero NONDET). Ordering verifiable from commit graph + drive.log.
- K2 COVERAGE AND LOCATION: PASS. 4 families x 8 worlds x 3 reps = 96 runs, all executed. Per-world replies.jsonl, scores.jsonl, and state/state.txt byte-identical across the 3 reps (driver cmp, zero NONDET). P1, P2, P4 hold exactly. P3 holds with full diag agreement (96/96 R2, 285/288 overall). Every miss located by D1-D3 with zero UNCLASSIFIED misses.
- K3 PURITY AND DIAGNOSIS: PASS. Pure Zag: zero .py files anywhere in the owned path (find verified); world generation, contestant, diag, and aggregation are all znc-compiled Zag binaries; bash only sequences process invocations. No em dashes (check_no_dash.sh clean). Mechanism diagnosis below.

## Per-family scores (agg_bin over 96 diag runs)

| fam | runs | queries | agree | det_fail | diag_fail | app_miss | uncl | sm_bad | p4_bad | r2 hit/miss |
|---|---|---|---|---|---|---|---|---|---|---|
| A exact revert | 24 | 72 | 72 | 0 | 0 | 0 | 0 | 0 | 0 | 24/0 |
| B partial revert | 24 | 72 | 72 | 0 | 0 | 0 | 0 | 0 | 0 | 24/0 |
| C revert+noise | 24 | 72 | 72 | 0 | 0 | 0 | 0 | 0 | 0 | 24/0 |
| D double change | 24 | 72 | 72 | 0 | 0 | 3 | 0 | 0 | 0 | 24/0 |

- P1 DETECTION: PASS (0 detection failures across 96 runs).
- P2 DIAGNOSIS: PASS (0 diagnosis failures across 96 runs).
- P3 APPLICATION: PASS (diag predicts the actual answer on all 96 R2 queries; 285/288 over all queries).
- P4 REVERT GAP: PASS (F-A original-law demos never restored, sup stays 1, on all 24 runs).
- P5 ORDERING: PASS vacuously (r2miss 0/0/0/0; small-n caveat from the prereg applies: with zero misses the ordering prediction is untested, not confirmed).

## Mechanism diagnosis

M1-M4 (the mechanism model under attack) SURVIVE:

- Detection exonerated: every law notice ingested on all 96 runs; no pre-notice demo remained sup=0 at any query (D1 clean, det_fail=0).
- Diagnosis exonerated: the sup=0 set at each query equaled exactly the demos after the most recent law notice (D2 clean, diag_fail=0). The contestant's recorded final sup flags matched the independent replay on every D line of every run (state_match=YES, sm_bad=0).
- Revision is monotonic as modeled (M1): P4 confirms the original-law demos are never restored through the revert on F-A (p4=OK on all 24 runs); the reverted law is re-learned from fresh demos only.
- All 3 misses (one distinct world, D3, x3 identical reps) located at APPLICATION by D3: diag's independent cascade predicted the contestant's exact wrong answer (pred=blbl actual=blbl), so the miss is inference from correctly revised evidence, not a revision failure.

## The D3 miss (new application-level failure mode, hand-verified)

World D3 (kold=3, k2=1, kfin=2, all distinct). R1 query after the first change, demos under k2=1:

- Demo 1: "lblb" to "blbl". The word has period 2, so it admits TWO rotation keys: k=1 and k=3.
- Demo 2: "ijcd" to "jcdi". Admits k=1 only.
- The rotation class takes the LARGEST matching k per demo (verified in the frozen contestant source: found=k overwrites, then requires agreement across demos). Demo 1 yields k=3, demo 2 yields k=1: inconsistent, so the entire rotation class collapses even though k=1 is consistent with both demos.
- Char map is consistent but the query "qypp" contains unmapped chars; reversal fails on demo 2; duplication fails; the nearest-demo fallback ties at common-prefix 0 and copies demo 1's output "blbl". Expected rot("qypp",1)="yppq".
- This is a third application-level failure mode alongside the prereg's anticipated two (reversal-ambiguity as in H0, rotation-inconsistent demos): periodic-demo key ambiguity defeating the largest-k tie-break and collapsing a whole inference class to fallback.

The H0-style reversal-ambiguity miss did not reproduce in 32 fresh worlds (0 R2 misses). The revert path itself (detection, diagnosis, monotonic supersede) is clean in all 96 runs.

## Notes

- diag.zag implements D1/D2 via turn-ordered replay of the revision state, validated per run by STATE-MATCH against the contestant's recorded state.txt (the final state alone cannot time-slice sup flags; the replay is the rigorous basis; documented in FREEZE.md).
- This wave adds zero TNN cognition source lines: contestant reused byte-identical, generator/diag/agg are external measurement instruments.
- No L3 claim. No LLM baseline (still PENDING).
