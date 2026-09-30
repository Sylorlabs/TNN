# RESULTS: C1 F-E family

Date: 2026-09-30. Verdict: FE-FAMILY-CONFIRMED.

## Commits (all local, tnn-native-lab, owned pathspec)

- Prereg: 8246edf0f (PREREG_FE_FAMILY.md, committed alone before implementation)
- Freeze: 0d8bdc111 (world_gen_fe source+binary, contestant/diag/agg byte-identical to attack wave, FREEZE.md; committed alone)
- Results: this commit (drive_fe.sh, seeds, worlds, runs, diag_out, RESULTS.md)

## Kill bars

- K1 ORDERING: PASS. Prereg (8246edf0f) strictly before freeze (0d8bdc111) strictly before world generation (seeds drawn from /dev/urandom after the freeze commit; hashes recorded in seeds/hashes.txt, values never viewed). Each world generated twice with byte-identical turns.jsonl and key.json (driver cmp, zero NONDET).
- K2 COVERAGE: PASS. 8 worlds x 3 reps = 24 runs, all executed. Per-world replies.jsonl, scores.jsonl, and state/state.txt byte-identical across the 3 reps (driver cmp, zero NONDET). Results recorded honestly against P-FE1/P-FE2/P-FE3.
- K3 PURITY: PASS. Pure Zag end to end (zero .py files; generator, contestant, diag are znc-compiled binaries; bash only sequences processes). No em dashes (check_no_dash.sh clean). New Zag code uses u8-backed cells with the st32/ld32 idiom (no as *i32 slice construction).

## Results (from diag_out/famE.txt, 24 runs)

| query | total | HIT-OK | APPLICATION | UNCLASSIFIED |
|---|---|---|---|---|
| R1 (post-change rotation) | 24 | 0 | 24 | 0 |
| R2 (revert rotation) | 24 | 24 | 0 | 0 |
| R3 (pa reversal control) | 24 | 24 | 0 | 0 |

det_fail: 0 across all runs (detection clean). diag_fail: 0 (diagnosis clean).

## Verdict against preregistered predictions

- P-FE1 (primary): PASS. R1 miss rate 24/24, well above the >= 20/24 bar and the F-A baseline of 0/24.
- P-FE2 (location): PASS. All 24 R1 misses located at APPLICATION by D3 (diag predicted the contestant's exact wrong answer every time), zero UNCLASSIFIED.
- P-FE3 (controls): PASS. R2 24/24 hits, R3 24/24 hits.

## Mechanism (confirmed)

Every R1 miss shows class=fallback with pred == actual. Example (world E0):
post-change demo 1 is period-2 "ahah" -> "haha" (admits rotation keys {1,3});
demo 2 is normal "bebb" -> "ebbb" (admits {1}). The rotation class takes the
largest matching k per demo (3 vs 1), finds inconsistency, and collapses the
entire class. Char map is consistent but the query chars are unmapped;
reversal and duplication fail; the nearest-demo fallback copies demo 1's
output. This is the D3 mechanism from the attack wave, reproduced
systematically in 8/8 worlds.

## Interpretation

FE-FAMILY-CONFIRMED. The periodic-demo key ambiguity is a systematic
failure mode, not an idiosyncratic world: whenever a post-change demo is
period-2 under the true key k=1, the largest-match-k tie-break produces a
spurious k=3 for that demo, the rotation class collapses, and the query
misses via fallback. The recommended follow-on (from the attack wave) is
a revision experiment swapping the tie-break to smallest-consistent-k,
preregistered before implementation, predicting these misses convert to
hits.

This wave adds zero TNN cognition source lines: contestant reused
byte-identical, generator/diag are external measurement instruments.
No L3 claim. No LLM baseline (still PENDING).
