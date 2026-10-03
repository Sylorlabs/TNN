# Hyptest broker log — sealed-interface repair (2026-09-27)

## What happened
The coordinator's first sealed battery run (binary SHA 19cb10d9…, clean-room
rebuilt byte-identical, workdir `run/w1`, `run/w2` byte-identical) FATALed or
degenerated on 4 of 6 sealed phenomena:

| case | teach badseg | result |
|------|--------------|--------|
| seal01 | 5/12 dropped, 7 fragmented instances | FATAL: non-uniform slot counts |
| seal02 | 4/12 dropped ("has" sentences) | degenerate (K=2 slots, hypotheses malformed) |
| seal03 | 4/12 dropped ("has" sentences) | FATAL at hypothesize → degenerate withhold, no ht_hypotheses.txt |
| seal04 | 0 | clean: 2 hypotheses, A wins, K10 6/6 |
| sealB1 | 0 | clean: 2 hypotheses, withhold, K10 6/6 |
| sealB2 | 4/12 dropped, 8 fragmented instances | FATAL: non-uniform slot counts |

## Root cause (coordinator interface failure, not a machinery bug)
The native intake (`ht_parse_is`) accepts exactly one sentence shape:
`<subject> is <value>.` — one byte-identical subject string per entity,
Nth sentence about an entity fills slot N. Crew S's sealed sentences used
mixed verbs ("are"/"has"/"have") and fragmented subjects ("the fries serving"
vs "the fries"). Unparseable lines are dropped as badseg; fragmented subjects
break instance identity. The prereg pinned "narrow declarative shapes the
native intake handles" but the exact sentence contract was never written down,
and Crew S was (correctly) isolated from the machinery sources — so this is a
broker interface-spec failure. The dev set happened to conform (pure "is").

## Repair (two halves, both blind-appropriate)
1. **Crew M2** (machinery, still sealed-blind): one minimal intake change —
   `ht_parse_is` falls back to splitting on " are " (plural copula) when
   " is " is absent. "has"/"have" stay rejected (possessives, not copulas).
   Must re-prove: dev battery still 20/20 byte-identical, determinism
   (2×, env -i, MALLOC_PERTURB_), delib=0 still zero-hypothesis.
2. **Crew S2** (phenomena, still machinery-blind): re-author seal01, seal02,
   seal03, sealB2 to the strict sentence contract (copula is/are + single
   category; one subject string per entity; 3/2/3 sentences per
   teach/phenomenon/test phase in consistent attribute order; possessives
   paraphrased as copula + hyphenated category, e.g. "boeing is wide-winged.").
   Same entities, same A/B/O roles, same gold winners (seal01 B, seal02 B,
   seal03 A, sealB2 WITHHOLD), same discrimination structure, re-verified
   against named sources. seal04 and sealB1 untouched. Mechanical contract
   checker added to build_phenomena.py.

## Seal integrity
- Crew M/M2 never opened `~/workspace/hyptest_sealed/` (verified in their reports).
- The 4 re-authored phenomena are fresh items; the old broken versions are discarded.
- seal04/sealB1 were processed by the binary in the partial run, but no
  machinery builder saw any output; scoring is fully mechanical
  (`run/score_sealed.py`), and the red team will independently re-verify
  seal04/sealB1 scoring.
- No prereg amendment: the prereg never pinned the intake's verb set; bars,
  seal protocol, and adjudication are untouched. The sentence contract is now
  recorded in the sealed SPEC.md.

## Artifacts
- `run/run_sealed.sh` — sealed driver (phases only, no gold).
- `run/score_sealed.py` — mechanical K1–K5/K9/K10 scorer.
- `run/w1`, `run/w2` — partial run (kept as evidence of the interface fault).
