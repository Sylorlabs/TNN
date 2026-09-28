# ASK-FIRST + COHERENCE COMBINED — FROZEN PREREGISTRATION (2026-09-22)

**Approval:** Micah's hypothesis, 2026-09-22: "ask for more info and
coherence are the best 2, they should be combined — and trained
behaviors, not architectures. But test this path as well." His words
are the prereg approval. This document is committed BEFORE any trial
binary is built or run. Standing law applied: when in doubt, test both.

**Question:** the two champion conflict-resolution behaviors from
R4C (ask-first 22/24, coherence 20/24; recency rejected 8/24 with 16
wrong installs) fused into ONE policy — and is that policy better as a
TRAINED BEHAVIOR or as a HARDWIRED ARCHITECTURE? The deciding probe is
generalization to novel conflict shapes.

## 1. The combined policy (frozen, mechanical — no judgment calls)

Background knowledge is a list of relations. Each relation scores a
candidate teaching +1 if satisfied, −1 if not. Relation kinds:

- ANCHOR (rkind 0): op ∈ {EQ, LT, GT}, anchor a. Satisfied iff v op a.
- RANGE (rkind 1): lo, hi. Satisfied iff lo ≤ v ≤ hi.
- ANCHOR-X (rkind 2): op, anchor — an anchor tagged as another key's
  installed knowledge (cross-key coherence). Same mechanics as ANCHOR.

Coherence score S(v) = Σ ±1 over relations. Candidates for one key are
ranked by S; margin M = S(top) − S(runner-up).

**Indecision threshold T = 2 (preregistered).** The channel carries one
packet: SILENT, CORRECT(rel idx → new anchor/bound), or ADD-REL (append
one relation). Decision:

1. Rank pre-channel. If M > T: verdict = top candidate, no consult.
2. Else (M ≤ T, indecisive): if channel SILENT → WITHHOLD. Else
   consult: incorporate the packet (correct the anchor/bound or append
   the relation), re-rank; verdict = strict argmax post-channel, tie →
   WITHHOLD.

This fuses the champions: coherence does the ranking; ask-first fires
exactly when the ranking is indecisive (margin ≤ T), not — as in R4C —
whenever coherence disagreed with recency. Decisive OLD-wins no longer
waste consults.

## 2. The two paths (frozen)

**PATH-T (trained behavior).** TNN-native learning machinery: the
RSI-style instrument loop (diagnose → simulate candidate rules →
select by measurement against teacher examples). The teacher is
TNN-native (a Zag teacher implementing the combined policy above);
it teaches via 16 worked TRAIN examples (item fields + its verdict +
its consult decision). The rule itself is NEVER transmitted. The
learner's rule space (frozen):

- criterion ∈ {RECENCY, CCGEN, CCBOUND}
  - RECENCY: verdict = newest candidate, never consults (the RSI-3
    primitive — the learner must reject it by measurement).
  - CCGEN: the general combined policy (§1) over any candidates /
    relations / channel kinds.
  - CCBOUND: CCGEN but WITHHOLD unless the item is exactly the
    familiar shape (ncand=2, nrel=3, all rkind=0, channel ∈
    {SILENT, CORRECT}) — the shape-bound rule, rejected by measurement
    on TRAIN's mild variation.
- threshold T ∈ {0, 1, 2, 4}. (Margins are always even — sums of ±1 —
  so odd thresholds are behaviorally identical to the next-lower even;
  {0,1,2,4} covers the distinguishable values. The true T* = 2.)
- ask ∈ {NEVER, ONINDEC, ALWAYS}.
  - NEVER: margin ≤ T → WITHHOLD, consult 0.
  - ONINDEC: §1 exactly.
  - ALWAYS: consult on every non-silent channel; verdict = post-channel
    strict argmax (tie → WITHHOLD); silent-channel items fall back to
    the margin rule.

36 rules. The learner simulates all 36 against the 16 teacher
examples, scoring 1 point per item iff (verdict, consult) both match
the teacher. Winner = argmax; tiebreak (preregistered backstop) =
first in enumeration order [RECENCY, CCGEN, CCBOUND] × [0,1,2,4] ×
[NEVER, ONINDEC, ALWAYS]. The battery is constructed (§3) so the true
rule (CCGEN, 2, ONINDEC) is the UNIQUE argmax — the oracle asserts
this (KB1); the tiebreak should never fire.

The selected rule is executed by the general deliberative machinery
(general constraint scorer, general ranking, general channel
incorporation). Nothing about the policy is planted in the learner:
its initial state carries no rule; the rule comes from measurement.
This is the allowed hybrid-teacher route — no LLM anywhere in the
teaching loop; planted-as-learner-direction stays dead.

**PATH-A (architecture).** The identical combined policy hardwired as
a fixed mechanism for the familiar shape: fixed code assuming exactly
2 candidates, 3 ANCHOR relations, channel ∈ {SILENT, CORRECT} (the
R4C-shape implementation). On any item failing the shape check
(ncand≠2, nrel≠3, any rkind≠0, channel=ADD-REL) it takes the documented
engineering fallback: WITHHOLD (safe default), consult 0.

## 3. Batteries (all fresh; disjoint from R4C items and each other)

Item encoding (frozen): id, key, ncand (2|3), candidates c0=OLD,
c1=MID|c1=NEW(2-cand: c1=NEW), c2=NEW; nrel relations of
(rkind,p1,p2,p3); channel (ckind,p1..p4). Verdicts: NEW/MID/OLD/
WITHHOLD. Ground truth by construction; the generator asserts the
true policy's verdict == gt on every TEST item.

**TRAIN (16 items, keys 101–116).** Familiar family with MILD
variation (ncand ∈ {2,3}, nrel ∈ {2,3,4}, channel ∈
{SILENT,CORRECT,ADD-REL}); rkind = 0 only. Teacher verdicts define
the learning target (oracle checks learner-teacher match, not gt).

| id | role | key | cands | relations | channel | teacher |
|---|---|---|---|---|---|---|
| T1 | clean, rejects ALWAYS-consult-need | 101 | [100,200] | A(EQ,200),A(GT,150),A(LT,250) | SILENT | NEW, c0 |
| T2 | clean | 102 | [200,100] | A(EQ,200),A(GT,150),A(LT,250) | SILENT | OLD, c0 |
| T3 | clean | 103 | [150,250] | A(EQ,250),A(GT,200),A(LT,300) | SILENT | NEW, c0 |
| T4 | decisive + truthful no-op channel; rejects ALWAYS | 104 | [300,120] | A(EQ,300),A(GT,250),A(LT,350) | CORRECT(0→300) | OLD, c0 |
| T5 | recency-trap | 105 | [200,100] | A(EQ,200),A(GT,150),A(LT,250) | SILENT | OLD, c0 |
| T6 | recency-trap, neither | 106 | [100,200] | A(EQ,999),A(LT,150),A(GT,150) | SILENT | WITHHOLD, c1 |
| T7 | recency-trap | 107 | [180,190] | A(EQ,180),A(GT,170),A(LT,185) | SILENT | OLD, c0 |
| T8 | recency-trap | 108 | [110,220] | A(EQ,110),A(GT,100),A(LT,120) | SILENT | OLD, c0 |
| T9 | mild-var ncand=3; rejects CCBOUND | 109 | [100,150,200] | A(EQ,200),A(GT,150),A(LT,250) | SILENT | NEW, c0 |
| T10 | mild-var nrel=2; rejects CCBOUND | 110 | [100,200] | A(EQ,200),A(GT,150) | SILENT | NEW, c0 |
| T11 | mild-var nrel=4; rejects CCBOUND | 111 | [200,100] | A(EQ,200),A(GT,150),A(LT,250),A(GT,100) | SILENT | OLD, c0 |
| T12 | mild-var ADD-REL; rejects CCBOUND | 112 | [100,200] | A(LT,150),A(GT,150) | ADD A(EQ,200) | NEW, c1 |
| T13 | margin-2 flip; rejects T∈{0,1} | 113 | [100,200] | A(EQ,100),A(LT,150),A(GT,150) | CORRECT(0→200) | NEW, c1 |
| T14 | margin-2 flip; rejects T∈{0,1} | 114 | [200,100] | A(EQ,100),A(LT,150),A(GT,150) | CORRECT(0→200) | OLD, c1 |
| T15 | margin-4 silent; rejects T=4 | 115 | [100,200] | A(EQ,200),A(GT,150),A(LT,250) | SILENT | NEW, c0 |
| T16 | neither; rejects NEVER | 116 | [100,200] | A(EQ,999),A(LT,150),A(GT,150) | SILENT | WITHHOLD, c1 |

(Notation: A(op,a) = ANCHOR; teacher column = verdict, consult flag.)

**TEST-FAMILIAR (24 items, keys 201–224).** R4C classes, all-new
values/keys; ncand=2, nrel=3, rkind=0, channel ∈ {SILENT, CORRECT}.

- N-clean ×6 (keys 201+i, i=0..5): cands [100+10i, 200+10i];
  rels A(EQ,200+10i),A(GT,150+10i),A(LT,250+10i); SILENT → NEW (margin 4).
- O-clean ×6 (keys 207+i): cands [200+10i, 100+10i]; same rel shape →
  OLD (margin 4).
- ADV-NEW ×2 (keys 213+i, i=0..1): cands [100+10i, 200+10i];
  rels A(EQ,100+10i),A(LT,150+10i),A(GT,150+10i);
  CORRECT(0→200+10i) → pre OLD +1/NEW −1 (margin 2, consult), post
  NEW +1 → NEW.
- ADV-OLD ×2 (keys 215+i): cands [200+10i, 100+10i]; rels as ADV-NEW;
  CORRECT(0→200+10i) → pre NEW +1 (consult), post OLD +1 → OLD.
- NEITHER ×8 (keys 217+i, i=0..7): cands [100+10i, 200+10i];
  rels A(LT,150+10i),A(GT,150+10i),A(EQ,999); SILENT → tie −1 →
  consult, silent → WITHHOLD.

**TEST-NOVEL (16 items, keys 301–316).** Four novel shapes × 4. The
rkind ∈ {1,2} frontier was never touched in TRAIN/TESTF.

- NV1 RANGE ×4: (301) cands [100,200], R(180,220),R(150,250),R(190,210),
  SILENT → NEW; (302) cands [200,100], same rels → OLD;
  (303) cands [100,200], R(90,110),R(150,250),R(180,220),
  CORRECT(0 lo→190) → pre tie-ish margin 2 consult, post NEW +3 → NEW;
  (304) cands [100,200], R(300,400),R(150,250),R(500,600), SILENT →
  margin 2 consult, silent → WITHHOLD.
- NV2 ANCHOR-X ×4: (305) [100,200], X(EQ,200),X(GT,150),X(LT,250) →
  NEW; (306) [200,100], same → OLD; (307) [100,200],
  X(EQ,100),X(LT,150),X(GT,150), CORRECT(0→200) → consult → NEW;
  (308) [100,200], X(EQ,999),X(LT,150),X(GT,150), SILENT → WITHHOLD.
- NV3 3-CANDIDATE ×4 (rkind 0): (309) [100,150,200],
  A(EQ,200),A(GT,150),A(LT,250) → NEW (margin 4); (310) [100,150,200],
  A(EQ,100),A(GT,50),A(LT,120) → OLD; (311) [100,150,200],
  A(EQ,150),A(LT,140),A(GT,160), CORRECT(0→200) → pre 3-way tie
  consult, post NEW +1 → NEW; (312) [100,150,200],
  A(EQ,999),A(LT,140),A(GT,160), SILENT → top tie −1 consult →
  WITHHOLD.
- NV4 ADD-REL ×4: (313) [100,200], R(90,110),R(150,250),
  ADD X(EQ,200) → pre tie consult, post NEW → NEW; (314) [200,100],
  same → OLD; (315) [100,200], A(LT,150),A(GT,150), ADD R(180,220) →
  NEW; (316) [100,200], A(LT,150),A(GT,150), ADD A(EQ,999) → post
  still tie → WITHHOLD.

(R(lo,hi) = RANGE; X(op,a) = ANCHOR-X.)

Distractors: D-RECALL (8 single-taught facts, exact probes; target
10000) and D-COST (200 quiet probes) — no-harm evidence.

**Separation (KB5):** ground truth lives ONLY in `battery_ac.csv`;
the binary's tables carry item fields minus gt. The oracle
cross-checks every field.

## 4. Metrics (frozen)

Per path × battery (TESTF n=24, TESTN n=16): **accuracy** = verdict
== gt; **wrong-install rate** = verdict ∈ {NEW,MID,OLD} ∧ ≠ gt;
**consult rate**; **cost** = ops (preregistered model: 1 op per
candidate×relation scored + 1 rank + consult×(10 + re-score));
**withhold rate on neither-gt items**. Learn mode: rule-match table
(36 rules × 16 TRAIN).

Preregistered expectations (not bars): learn selects
(CCGEN, T=2, ONINDEC) 16/16; TESTF: PATH-T 24/24, PATH-A 24/24;
TESTN: PATH-T 16/16, PATH-A 4/16 (the four WITHHOLD-gt items), 0
wrong installs.

## 5. Kill bars (mechanical oracle `verify_ac.py`, frozen with this prereg)

| Bar | Rule |
|---|---|
| KB1-BATTERY | 16+24+16 items; class counts per §3; oracle recomputes the true policy from the CSV and asserts verdict == gt on every TEST item; asserts the true rule is the UNIQUE 36-rule argmax on TRAIN (16/16, next-best ≤ 15); else FAIL |
| KB2-DET | 5/5 byte-identical runs per mode (teacher/learn/pathT/pathA); else FAIL |
| KB3-CHAMPION | computed on TEST-NOVEL over the two paths only (degenerate baselines excluded — the R4C drafting defect is not repeated): champion = strictly greater accuracy AND wrong-install ≤ the other. Else NO-CHAMPION (reported, not fudged). |
| KB4-FALSIFY | if PATH-A is the KB3 champion on TEST-NOVEL, the verdict states plainly: "Micah's hypothesis is FALSIFIED — the hardwired architecture generalized as well or better than the trained behavior." |
| KB5-SEPARATION | binary sources contain no gt; printed item fields match the CSV exactly; else FAIL |
| KB6-SCOPE | the verdict records the scope of whatever wins, including the residual boundary from R4C (correlated-wrong channels). |
| KB7-LEARN | learn mode's selected rule == (CCGEN, T=2, ONINDEC) at 16/16; else FAIL with diagnosis (the hypothesis test is void if the behavior was never acquired). |

## 6. Log lines (frozen; the oracle parses these)

```
AC_CFG,mode=<teacher|learn|pathT|pathA>
AC_TEACH,id=<n>,verdict=<NEW|MID|OLD|WITHHOLD>,vcand=<0|1|2|-1>,consult=<0|1>
AC_RULECAND,crit=<RECENCY|CCGEN|CCBOUND>,T=<0|1|2|4>,ask=<NEVER|ONINDEC|ALWAYS>,match=<m>
AC_RULE,crit=<...>,T=<n>,ask=<...>,match=<m>
AC_ITEMFIELDS,id=<n>,set=<T|F|N>,key=<n>,ncand=<n>,nrel=<n>,ckind=<n>,c0=<n>,c1=<n>,c2=<n>,rels=<rkind,p1,p2,p3;...>
AC_ITEM,id=<n>,set=<F|N>,verdict=<...>,vcand=<n>,ops=<n>,consult=<0|1>
AC_BATT,id=RECALL,metric=<n>
AC_BATT,id=COST,metric=<n>
AC_DONE
```

## 7. What this does and does not claim

Authored: the combined policy, the rule space (36), the generality
prior in the tiebreak, the general machinery, PATH-A's hardwired code
and its WITHHOLD fallback, the teacher, the batteries, the cost
model, the oracle. Measured: the rule the learner selects from 16
teacher examples (KB7); the path×battery metric table; the champion;
the falsification outcome.

On the novelty frontier: TRAIN's mild variation (ncand, nrel,
channel-kind) lets the learner REJECT shape-bound rules by
measurement. The rkind frontier (RANGE/ANCHOR-X, never seen in
training) is crossed by the documented generality prior, not by
training-data fit — no training set can decide a frontier it never
touches. The verdict will state this plainly. What the trial
demonstrates with discipline: a behavior acquired from examples (not
planted) transfers across that frontier while the shape-bound
hardwired policy cannot — or, if PATH-A matches it, Micah's
hypothesis is falsified on the record.

This trial does NOT test invention (RSI-3/RSI-4 own that); it tests
Micah's "trained behaviors, not architectures" bet on the combined
conflict-resolution policy.
