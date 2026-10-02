# REVISE5 RESULT: H-REVISE5 SURVIVES (62/62)

**Date:** 2026-09-29
**Repair researcher:** H-REVISE5 subagent
**Branch:** tnn-native-lab
**Target:** H-REVISE4 DOWNGRADED (REVISE4_ADV_RESULT.md)
**Prereg:** PREREG_REVISE5.md (8cc967832, frozen before implementation;
commit order verified: prereg strictly precedes this result)
**Implementation:** revise5.zag (this directory; revise4.zag untouched)
**Raw evidence:** REVISE5_RAW.txt (md5 ddcb842dc2f6755d6fd2f90ef6907d65,
3/3 byte-identical via cmp)
**Toolchain:** znc 2026.07.0-dev (edition 2026)
**Purity:** Pure Zag. No Python at any stage: no generators, verifiers,
scratch computation, or analysis code. Shell file utilities (md5, cmp)
only.

## Verdict: H-REVISE5 SURVIVES (62/62 named checks)

The H-REVISE4 red-team downgrade is repaired. The X-RV4-1 unique-wrong-top
fixture no longer produces a confident wrong revision: the wrong
candidate is still proposed by phase 1 (honestly), but the new
corroboration gate withholds the append (code -3 UNCORROBORATED).

## What was built

`revise5.zag` = `revise4.zag` with three frozen changes (mechanism
functions z_alloc through dcopy verified byte-identical via diff;
only the header comment, the diagnosis section, and main() differ):

**R1: honest single-signal propose.** `diagnose_propose` replaces
`diagnose_scored`. The +1 program-consistency term is DELETED. The
red team proved it was the same signal as output-relevance whenever
seq comes from pextract(fail, fail_out): p appears in seq iff
fail[p] appears in fail_out. Keeping both was one binary signal
counted twice. Scores are now 0 or 1. Tie at top still returns -2
AMBIGUOUS; no discriminating candidate still returns -1. The old
documented limit "near-ties (differing by 1) still resolve by lowest
position" described an impossible event and is replaced: with one
binary signal, any unique top wins and any tie withholds.

**R2: corroboration gate.** New `diagnose_corroborate(VS, D, pdesc,
npass, fail2, fail_out2, p, v)` returns 1 iff (a) fail2[p]==v,
(b) (p,v) discriminates fail2 from every passing input
(bounds-respecting), (c) the current program VS mispredicts fail2.
The caller appends ONLY on propose>=0 AND corroborate==1; otherwise
it emits UNCORROBORATED and withholds (code -3), leaving the version
store unchanged. Rationale (preregistered): single-counterexample
diagnosis is provably underdetermined. X-RV4-1's wrong (0,122) and
Phase C's right (0,120) are structurally identical from the
mechanism's view (incidental byte at pos 0 present in expected
output; causal byte absent), so no scoring function of
(fail, fail_out, passing, P0) can separate them. The repair is
therefore not a better single-shot score but a second piece of
evidence.

**R3: honest documentation.** This doc and the source header state
the signal content plainly: phase 1 carries one bit; the two
independent evidences are propose (output-relevance) and corroborate
(second counterexample).

Unchanged: VS3 store layout, vs3_revise (explicit refuse-with-warning,
4 slots), discrimination rule, bounds-respecting guard, P1 discovery,
dispatch order (most-recent-first), determinism.

## Frozen bar results

- **K-RV5-1 PASS (Phase L):** fail1=("zqy"->"zzz") proposes 122,
  i.e. (0,122) (CHECK L3; the wrong top is still proposed, phase 1
  is not pretended fixed). Corroborate with ("aqy"->"aaa") returns 0
  (fail2[0]='a' != 122; CORROBORATE FAIL emitted). UNCORROBORATED
  emitted, revision withheld (CHECK L4). vcount stays 0 (CHECK L5).
  Query "zqw" gives "www" under intact P0 (CHECK L6). No revision is
  appended for (0,122). The red team's exact kill (confident wrong
  append + held-out failures) does not recur.
- **K-RV5-2 PASS:** raw output contains 7 "score=1" candidate lines
  and 8 "score=0" lines; zero "score=2" lines anywhere. The
  degeneracy (old 0-or-2) is gone; the two independent signals are
  now propose and corroborate, documented as such.
- **K-RV5-3 PASS (no regression, nothing superseded):** Phase J tie
  still -> AMBIGUOUS -2, vcount 0 (K-RV4-1: CHECKs J3, J4). Phase K:
  R1..R4 appended, R5 refused rc=-1 with VS3FULL, vcount 4, earlier
  revisions intact (K-RV4-2: CHECKs K1-K3). Phase C appends (0,120)
  corroborated by ("xqw"->"xxx"); Phase G appends (0,121)
  corroborated by ("yqw"->"yyy"); Phase H appends (1,113)
  corroborated by ("aqc"->"qqq") with held-outs xbc->ccc and
  aqc->qqq PASS; Phase I appends (2,120) corroborated by
  ("cbx"->"ccc") with abx->aaa verified; Phase F withholds
  (UNRESOLVABLE -1, vcount 1, P0 intact); Phase E 5/5 verify;
  Phase B monitor/detect. Total 62/62 named CHECKs PASS.
- **K-RV5-4 PASS:** 3/3 runs byte-identical (cmp), md5
  ddcb842dc2f6755d6fd2f90ef6907d65.
- **K-RV5-5 PASS:** all four genuine second counterexamples
  corroborate (CHECKs C3, G5, H5, I6); the mechanism does not
  degenerate into withholding everything.

## Source audit (self)

- Mechanism functions (z_alloc through dcopy) byte-identical to
  revise4.zag (diff-verified). No test-answer literals added; the
  corroboration fixtures ("xqw", "yqw", "aqc", "cbx", "aqy") live
  only in main(), same as all prior fixtures.
- diagnose_propose has no path to score 2 (single increment site).
- vs3_revise unchanged: exactly two return paths (-1 full, 1 append).
- UNCORROBORATED path appends nothing and changes no store state
  (verified: CHECK L5 vcount==0).

## Honest limits (carried from prereg, unchanged)

1. Corroboration needs a second counterexample; the harness supplies
   it directly. In a deployment it arrives via continued monitoring.
   A lone first failure now waits instead of guessing.
2. Two counterexamples sharing an incidental byte can still
   misattribute; documented, not eliminated.
3. P1 is still discovered from the first counterexample alone.
4. Capacity remains 4 with explicit refuse-with-warning.
5. Bounded L2+ revision, not L3: the condition vocabulary and the
   propose+corroborate protocol are researcher-designed.

## Classification

Bounded L2+ revision with a repaired diagnosis protocol: exact ties
withhold (AMBIGUOUS), unresolvable cases withhold (UNRESOLVABLE),
uncorroborated unique tops withhold (UNCORROBORATED, new), capacity
refusal is explicit (VS3FULL). The X-RV4-1 failure class (confident
unique misattribution) is closed by requiring the second signal.

## Commit lineage

- Prereg: 8cc967832 (frozen before implementation; single file).
- Implementation + evidence + result: this commit (revise5.zag,
  REVISE5_RESULT.md, REVISE5_RAW.txt; only owned paths staged).
- Target: revise4.zag as committed (mechanism byte-identical).
- Red team: REVISE4_ADV_RESULT.md.

## Pure Zag compliance

Prereg, implementation, compilation (znc 2026.07.0-dev), execution,
and all analysis in Zag only. No Python used at any stage. No em
dashes in this document.
