# Prereg: H-UNIFIED2 (Compositional Repair for U-A2 Kill + Downgrades)

**Date:** 2026-09-29
**Status:** FROZEN before implementation
**Hypothesis:** H-UNIFIED2
**Parent verdict:** H-UNIFIED KILLED by U-A2 (compositional interference);
  3 downgrades (U-A1, U-A3, U-A4); U-A5 pass.
  Adversary report: unified_adversary/ADVERSARY_REPORT_H_UNIFIED.md

## Hypothesis

The U-A2 kill can be repaired at the composition layer (not in the causal
learner) by coherence-gating causal revision in the unified handler, and
the U-A1/U-A3 downgrades can be repaired without breaking the frozen 9/9.
U-A4 is explicitly scoped to the concurrent H-INTENT-UNIFIED port.

## What Is New (vs H-UNIFIED, commit f5dd7cdc7)

New file `unified2_learn.zag`, copied from the f5dd7cdc7
`unified_learn.zag` plus exactly three repairs. The original
`unified_learn.zag` is NOT modified (a concurrent H-INTENT-UNIFIED
researcher holds uncommitted changes there).

Repair 1 (U-A2 kill): coherence-gated causal revision.
- New `caus_coherent()`: an incoming episode is coherent iff no ACTIVE
  rule matches its (cond_var, cond_val, action) with a different effect.
- `handle_caus_learn` becomes append/corroborate-only for verified
  knowledge: coherent episodes go to `clearn` unchanged; contradictory
  episodes are QUARANTINED (emitted in trace, committed count 0, no rule
  touched).
- `clearn` itself is UNTOUCHED. The causal learner in isolation keeps its
  revision semantics (it behaved as designed per the adversary). The fix
  is at the composition layer, per the adversary's repair direction.
- Documented tradeoff: the unlabeled stream can no longer destructively
  revise causal knowledge, even when revision would be correct. Revision
  of verified causal knowledge requires an explicit revision channel
  (H-REVISE2, separate track), not silent overwrite from an unlabeled
  item.

Repair 2 (U-A1 downgrade): explicit AMBIGUOUS route code (5).
- nseg>=2, all segments pair-shaped (exactly one '>'), all fields
  int-like (field_kind >= 1) but NOT iii>ii: route 5 AMBIGUOUS,
  reason "int-pair lesson: ambiguous domain; withheld". Was: silent
  WITHHOLD ("mixed or malformed segments").
- nseg==1, no '>', single bare digit string with int-count k>=1 and k!=3
  (e.g. "12321"): route 5 AMBIGUOUS. Was: silent WITHHOLD. k==3 stays
  CAUS_QUERY; k==-1 (string) stays PROC_QUERY.
- "1,2,3>4,5;7,8,9>0,1" (genuine iii>ii) still routes CAUS_LEARN: the
  taxonomy's best guess for novel items. Its destructive case is now
  handled by Repair 1. Explicitly documented, not silently committed.
- The unified main treats code 5 as withhold (no store touched).

Repair 3 (U-A3 downgrade): direct discovery on the extractable subset.
- `bridge_learn` Step 2: if any pairs extracted (nsub>0), attempt
  `pdiscover_direct` on the extractable subset, not only when allok==1.
  A single unextractable pair no longer vetoes direct discovery for the
  extractable rest.
- On subset success with nsub<npairs: return the direct slot and emit
  "N/M extractable; K unextractable pairs WITHHELD (no bridge)".
- Step 3 (bridge induction) unchanged: it still fires only when direct
  discovery on the extractable subset fails.

U-A4 (query ambiguity): EXPLICITLY SCOPED OUT. H-INTENT SURVIVES (10/10)
standalone; the H-INTENT-UNIFIED port (prereg d959ff51f, concurrent
researcher) owns the unified query path. unified2 keeps the query path
byte-identical to f5dd7cdc7 to avoid conflicts.

## Kill Bars (frozen)

- **K-U2-1 (U-A2 attack no longer destroys verified knowledge):**
  Replay the frozen attack through the unified2 gated path:
  (a) route+learn "0,0,0>0,1;0,0,0>0,1;1,0,0>1,0;1,0,0>1,0",
  verify cpredict(1,0,0)->s1=0;
  (b) route "1,0,0>9,9;1,0,0>9,9" (must still route CAUS_LEARN),
  feed through the gated handler;
  (c) PASS iff: both interfering episodes quarantined (trace shows
  QUARANTINE, committed 0), cpredict(1,0,0) still yields s1=0,
  cpredict(0,0,0) still yields s1=1, and no rule with effect s1:=9
  exists among active rules.
- **K-U2-2 (no regression):** all 9 original H-UNIFIED frozen checks
  (K-U1, K-U2a/b/c, K-U3, K-U4a/b, K-U5, K-A) PASS unchanged.
- **K-U2-3a (U-A1 addressed):** route_line("321>123;654>456") == 5
  AMBIGUOUS; route_line("12321") == 5 AMBIGUOUS;
  route_line("1,2,3>4,5;7,8,9>0,1") == 2 CAUS_LEARN (documented).
- **K-U2-3b (U-A3 addressed):** feed "abc>cba;de>ed;ff>ff" via
  handle_proc_learn_unified: returns a direct slot (rc>=0, rc<1000),
  bridge count unchanged by this item, trace reports the unextractable
  pair WITHHELD, and proc_apply at rc on "dxc" yields "cxd".
- **K-U2-3c (U-A4 scoped):** result doc records the explicit scope-out
  with pointer to H-INTENT-UNIFIED; unified2 query path diff vs
  f5dd7cdc7 is empty.
- **K-U2-4 (determinism):** 3 runs byte-identical (cmp).

## Verdict Rule

H-UNIFIED2 SURVIVES iff K-U2-1, K-U2-2, K-U2-3a, K-U2-3b, K-U2-3c, K-U2-4
all PASS. Any FAIL kills H-UNIFIED2. Classification ceiling: bounded L2
integration repair, not L3.

## Honest Limitations (declared before running)

1. The coherence gate sacrifices autonomous causal revision through the
   unlabeled stream. A genuinely-correct revision arriving unlabeled is
   now quarantined too. This is the price of the repair; the explicit
   revision channel (H-REVISE2) is the intended path for corrections.
2. AMBIGUOUS items are withheld, not resolved. The learner signals the
   hole instead of guessing; resolution is future work.
3. The subset-direct fix assumes the extractable subset's program is the
   intended one; unextractable pairs are dropped with a trace, not
   modeled.
4. No Python. Pure Zag. No em dashes in docs.
