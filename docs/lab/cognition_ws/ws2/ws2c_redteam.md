# WS2-C red teams (2026-09-24) — scheme (VERIFY,COUNT,NEVER,NONE)

## R1: wrong-hint swaps (12 holdout probes, hints rotated by 4)
Result: 8/12 miss, all F_HINT_EXCLUDE except H07 (F_UNCLASSIFIED, the known
morphological miss). 4 pass (H01, H05, H08, H11) where VERIFY dropped the
wrong swapped hint or the swap was benign. No crash, no hang — graceful
degradation, and the miss classifier correctly attributes swapped-hint
failures. Outputs: `redteam/r1out/`.

## R2: holdout-id renaming (AS\d\d → ASZ\d\d, corpus + queries)
Result: identical 11/12 pattern — H07 misses (F_UNCLASSIFIED), everything
else passes. The scheme keys on content, not id strings. Outputs:
`redteam/r2out/`.

## R3: 6 novel zero-overlap probes (gold empty)
Result: 5/6 return junk (F_ABSTAIN); the 6th passed vacuously (its hint
matched zero items). This is the documented cost of TNN rejecting M_AB1 in
round 1: the scheme cannot say "not found". TNN chose recall over abstention
because abstention caused 2 regressions on zero-evidence-but-passing probes.
Outputs: `redteam/r3out/`.

## R4: seal audit (did deliberation see H01–H12?)
- Deliberation workdir contained no holdout files (engine's own seal check
  passed before deliberating; verified: no `*holdout*` in workdir).
- `grep -rE "H0[1-9]|H1[0-2]"` over the R1 workdir: every hit is a `PH01`
  substring (physics item ids in the design corpus/queries/evidence) or the
  engine's own seal assertion in audit.md ("H01-H12 unseen by me").
- No holdout query text, gold set, or hint appears anywhere in the
  deliberation inputs or the 5-round audit trail. Seal intact.
