# L3-SUF-1 REPORT.md (Builder)

**Worker:** L3-SUF-1-BUILDER  
**Date:** 2026-10-03  
**Status:** BUILD-PASS (DEV battery), code-frozen, ready for adversary/red-team handoff.

## Summary

Implemented L3-SUF-1 "Resolution Records" in pure Zag under the frozen prereg (`6c70c3198`). The learner invents per-element resolution records (RESOLVED/UNRESOLVED/FALSIFIED-ALL) via the sole-survivor rule generalized to 3 scales (element, form, reuse). All 8 DEV treatments pass; all SUF-K bars evaluable by builder pass.

## Key design decisions

1. **Flat form `(s0,x,y,d)` entries**, kinds 0/1/2. `l_surviving()` derives marks as surviving-set cardinalities from the consequence log only (no marking rule/threshold in source).
2. **Frozen escalation order:** (1) probe-more < (2a) guard-reexpand < (2b) union-reexpand < (3) resolution-lift.
3. **Sticky-max KB template** (template 2 = resolution records).
4. **Pre-commit `l_try_improve`** (fix-if-broken via 2a/2b), gated on knowledge-REJECTs (AS[92]).
5. **Commit rule:** replay-consistent → commit; DATA-UNTRUSTED → defer; else commit best ungraded (stakes adjudicate).
6. **Documented tiebreak bug** (`x<y?1:0`); DEV U-truth = anti-tiebreak to guarantee stakes REJECTs.
7. **Probe coverage:** ALL world entities (not just training) to ensure exhaustive probing.

## DEV results (runs/dev_run7.log, 3/3 byte-identical)

| Treatment | Result | Notes |
|-----------|--------|-------|
| GATE | PASS | C0 confidently wrong on W0/F-A/F-B/F-C |
| T0 (invent) | PASS | first_unres_mark=310, first_creject=127 |
| T1 (RK-A retest) | PASS | held_correct=6/6, wrong=0 |
| T2 (RK-B retest) | PASS | wrong=0, cdet=4/4, abst_und=2/2 |
| T3 (RK-C retest) | PASS | defer DATA-UNTRUSTED, conf_wrong=0 |
| T4 (reuse) | PASS | ratio ok (104 ≤ 208/2), kb_loaded=1 |
| T5 (recode) | PASS | part=1, bars=1 |
| T6 (revision) | PASS | lineage_matches=3 |
| T7 (retirement) | PASS | commit_kind=0, unres_marks=0 |

**Controls:** C0 (confidently wrong) PASS; C1 (fails T2) PASS; C3 (confidently wrong) PASS.

**SUF-K bars:**
- PASS: K2, K3, K5, K6, K7, K8, K9, K11, KC0B, KC0D.
- PENDING: K1, K4, K10, K12 (audit/adversary), KC0A (audit), KC0C (adversary).

## Bugs fixed during DEV

1. **Antisymmetric truth:** World's truth was antisymmetric in (x,y); learner treats pairs as unordered. Fixed to symmetric.
2. **usedp ordering:** Probe's used-pair set used non-canonical positions. Fixed to canonical.
3. **Knowledge-REJECT vs fabrication:** l_try_improve triggered on tiebreak fabrications. Gated on AS[92] (knowledge-REJECTs only).
4. **Missing (c1,D) evidence:** Slot-varying probes didn't TEST flipped value on REJECT. Added PVARY2 follow-up.
5. **Harmful simplify:** kind2→kind1 dropped ABSTAIN-on-unknown. Removed (never drop kind2).
6. **Probe entity coverage:** Training-only ents missed heldout entities. Changed to all world entities.
7. **T5 recode:** which=5 used different RNG seed than which=4. Fixed to same seed (true recode).

## Handoff

**For adversary:** Frozen world interface (CODEFREEZE.md). Sealed worlds to be designed post-freeze. Builder DEV worlds (W0, F-A…F-G) are NOT sealed.

**For red-team:** A-LIT/A-TRACE/A-SEARCH/A-TRIGGER/A-INFO/A-ORDER per prereg.

**Code freeze:** `src/*.zag`, `src/build.sh`, `CODEFREEZE.md`, `NAMECHECK_BUILDER.md`, `REPORT.md`. Binary: `src/build/suf` (sha256: e4ac0837ba57edc7c330e89deeee5c3f0c3de446cd459cc84fe26fdcb1afe42d).

**Prereg intact:** PREREG.md and NAMECHECK.md unmodified at `6c70c3198`.
