# H-UNIFIED2 RESULT: Compositional Repair for U-A2 Kill

## Verdict: H-UNIFIED2 SURVIVES (12/12 checks, 6/6 kill bars)

**Date:** 2026-09-29
**Prereg:** PREREG_UNIFIED2.md (commit bfd5bcb13, frozen before implementation)
**Parent:** H-UNIFIED KILLED by U-A2 (adversary report
  unified_adversary/ADVERSARY_REPORT_H_UNIFIED.md)
**Toolchain:** znc 2026.07.0-dev (edition 2026)
**Purity:** Pure Zag. No Python anywhere. No em dashes in docs.

## What was built

`unified2_learn.zag`: the f5dd7cdc7 `unified_learn.zag` copied verbatim,
then three composition-layer repairs. The original `unified_learn.zag`
was NOT touched (concurrent H-INTENT-UNIFIED researcher holds uncommitted
changes there). `clearn` is untouched: the causal learner in isolation
keeps its revision semantics, per the adversary's repair direction.

Repair 1 (U-A2 kill): coherence-gated causal revision. New
`caus_coherent()` checks each incoming episode against ACTIVE rules;
`handle_caus_learn` commits coherent episodes via `clearn` unchanged and
QUARANTINES contradictory ones (traced, committed 0, no rule touched).
The unlabeled stream is now append/corroborate-only for verified causal
knowledge.

Repair 2 (U-A1 downgrade): explicit AMBIGUOUS route code (5). Int-pair
lessons ("321>123;654>456") and bare digit-string queries ("12321") that
the format taxonomy cannot resolve are signaled AMBIGUOUS instead of
silently withheld. Genuine iii>ii still routes CAUS_LEARN.

Repair 3 (U-A3 downgrade): `bridge_learn` Step 2 attempts direct
discovery on the extractable subset (not only when every pair extracts).
Unextractable pairs are reported WITHHELD; no spurious bridge fires.

U-A4 (query ambiguity): explicitly scoped out. H-INTENT SURVIVES (10/10)
standalone; the H-INTENT-UNIFIED port (prereg d959ff51f, concurrent)
owns the unified query path. Verified: unified2 query-path functions
are byte-identical to f5dd7cdc7 (diff empty).

## Frozen bars and results

- K-U2-1 (U-A2 attack no longer destroys verified knowledge): PASS.
  Replay: learned "0,0,0>0,1;0,0,0>0,1;1,0,0>1,0;1,0,0>1,0", verified
  cpredict(1,0,0)->s1=0. Fed "1,0,0>9,9;1,0,0>9,9" (routes CAUS_LEARN).
  Result: 0 committed, 2 quarantined (trace shows both QUARANTINE
  lines), active rule count still 2, cpredict(1,0,0)->s1=0,
  cpredict(0,0,0)->s1=1. Verified knowledge intact.
- K-U2-2 (no regression): PASS. All 9 original H-UNIFIED checks
  (K-U1, K-U2a, K-U2b, K-U2c, K-U3, K-U4a, K-U4b, K-U5, K-A) PASS.
- K-U2-3a (U-A1 addressed): PASS. "321>123;654>456" -> AMBIGUOUS (5),
  "12321" -> AMBIGUOUS (5), "1,2,3>4,5;7,8,9>0,1" -> CAUS_LEARN (2).
- K-U2-3b (U-A3 addressed): PASS. "abc>cba;de>ed;ff>ff" -> PROC_LEARN,
  direct discovery on 2/3 extractable pairs -> proc slot 3, bridge count
  unchanged, trace reports 1 unextractable pair WITHHELD, probe
  "dxc"->"cxd" via the direct slot.
- K-U2-3c (U-A4 scoped): PASS. Scope documented; query-path diff empty.
- K-U2-4 (determinism): PASS. 3 runs byte-identical
  (md5 4f8c24dbce2d971fad8435718b71fa58).

## Evidence

- UNIFIED2_RAW_OUTPUT.txt (authoritative raw output, run 1 of 3)
- unified2_learn.zag (implementation)
- PREREG_UNIFIED2.md (frozen prereg, commit bfd5bcb13)

## Honest boundaries

1. The coherence gate sacrifices autonomous causal revision through the
   unlabeled stream. A genuinely-correct revision arriving unlabeled is
   quarantined too. This is the price of the repair; corrections need an
   explicit revision channel (H-REVISE2, separate track).
2. AMBIGUOUS items are withheld, not resolved. The learner signals the
   taxonomy hole instead of guessing.
3. The subset-direct fix assumes the extractable subset's program is the
   intended one; unextractable pairs are dropped with a trace.
4. Classification: bounded L2 integration repair, not L3. No
   representational invention.

## Recommended follow-ups

1. Independent red team on unified2 (assume the repair is incomplete).
2. Port H-INTENT into unified2's query path once H-INTENT-UNIFIED lands,
   or unify the two files.
3. H-REVISE2 explicit revision channel: the principled path for genuine
   corrections that the gate now quarantines.
4. Update CANONICAL_STATE.md: H-UNIFIED KILLED -> H-UNIFIED2 SURVIVES
   (bounded L2 repair).
