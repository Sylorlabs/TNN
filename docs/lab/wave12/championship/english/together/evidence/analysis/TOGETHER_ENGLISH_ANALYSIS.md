# TOGETHER ENGLISH — analysis (canonical N=5 battery)

## Class-2 rep 0 (scale 1)
- d1 40/40, d2 38/38, d3 120/120
- rev_false 12/12, rev_genuine 20/20
- r2 40/40, r3 40/40, hallu 0/20, withheld 0
- traps 140/140, k1=1 k2=1 refusal=1
- ops 287, eps 295
- mastery: 1.0000
- revisability: 1.0000
- integrity: 1.0000
- retention: 1.0000
- cost: 0.9113
- composite: 0.9911

## Class-2 rep 1 (scale 1)
- d1 40/40, d2 37/37, d3 120/120
- rev_false 12/12, rev_genuine 20/20
- r2 40/40, r3 40/40, hallu 0/20, withheld 0
- traps 140/140, k1=1 k2=1 refusal=1
- ops 287, eps 295
- mastery: 1.0000
- revisability: 1.0000
- integrity: 1.0000
- retention: 1.0000
- cost: 0.9113
- composite: 0.9911

## Class-2 rep 2 (scale 1)
- d1 40/40, d2 40/40, d3 120/120
- rev_false 12/12, rev_genuine 20/20
- r2 40/40, r3 40/40, hallu 0/20, withheld 0
- traps 140/140, k1=1 k2=1 refusal=1
- ops 287, eps 295
- mastery: 1.0000
- revisability: 1.0000
- integrity: 1.0000
- retention: 1.0000
- cost: 0.9113
- composite: 0.9911

## Class-2 rep 3 (scale 1)
- d1 40/40, d2 36/36, d3 120/120
- rev_false 12/12, rev_genuine 20/20
- r2 40/40, r3 40/40, hallu 0/20, withheld 0
- traps 140/140, k1=1 k2=1 refusal=1
- ops 287, eps 295
- mastery: 1.0000
- revisability: 1.0000
- integrity: 1.0000
- retention: 1.0000
- cost: 0.9113
- composite: 0.9911

## Class-2 rep 4 (scale 1)
- d1 40/40, d2 40/40, d3 120/120
- rev_false 12/12, rev_genuine 20/20
- r2 40/40, r3 40/40, hallu 0/20, withheld 0
- traps 140/140, k1=1 k2=1 refusal=1
- ops 287, eps 295
- mastery: 1.0000
- revisability: 1.0000
- integrity: 1.0000
- retention: 1.0000
- cost: 0.9113
- composite: 0.9911

## S10 no-degradation (rep 0, scale 10 vs scale 1)
- d1: s10 40/40 vs s1 40/40 [OK]
- d2: s10 38/38 vs s1 38/38 [OK]
- d3: s10 120/120 vs s1 120/120 [OK]
- rev_false: s10 12/12 vs s1 12/12 [OK]
- rev_genuine: s10 20/20 vs s1 20/20 [OK]
- r2: s10 40/40 vs s1 40/40 [OK]
- r3: s10 40/40 vs s1 40/40 [OK]
- verdict: NO DEGRADATION

## Conflict matrix (5 sources x obs+probe = 10 evidence legs)
- CCM rows: 1140 (228 ids x 5 reps: 12 held-out excluded per rep;
  the 12 false ids ARE included — all 5 sources unanimously agree on the
  falsehood (status 0), taught false, then disproved in phase 2: rev_false 12/12)
- taught (unanimous): 1140, withheld (split): 0
- split ids: none — 0 split ids across all 5 corpora
- T5_OP_CONFLICT audits: 0 (withholding is terminal per id)

## Class-1 (TNN teacher leg + student Track-5 battery)
- teacher rep selection: TEACHER_REP,0
- d1 40/40, d2 31/38, d3 120/120
- rev_false 0/12 (non-acquisition; teacher false_claims=0), rev_genuine 16/20
- revisability uses rev_genuine/20 only (documented genuine-only asymmetry)
- r2 27/40, r3 27/40, hallu 0/20
- mastery: 0.9386
- revisability: 0.8000
- integrity: 1.0000
- retention: 1.0000
- cost: 0.9371
- composite: 0.9253
- CLASS1,start
- TEACHER,held,228,withheld,0,learn_gate,0
- TEACHER,curriculum_bad,0
- TEACHER,false_claims,0
- TEACHER,adds,228
- CLASS1,leg_start,rep,0
- CLASS1,slices_done,hits,96,fp,0,pass,8,clean_adopt,160
- CLASS1,final_mastery,192,192
- CLASS1,done,fails,0

## Class-2 §B.7 (learner as judging student, tid=61)
- B7C2,start
- B7C2,held,228,withheld,0
- B7C2,held_wrong,0
- B7C2,slices_done,hits,96,fp,0,pass,8
- DIGEST,C2,0,1,e3ecea12472ea970df3379b6694c12aa9027d53e15331428751c845fd4d8fde0
- B7C2,done,fails,0

## Provenance & gates
- corpus sol: 41aa8f5be15f778034cfce63250233468d364f52b318a02f63a87ac7459015d7
- corpus grok-4.6: 7f3a25739981c8276082ceeda7de3628afd88977e7a16bd0a5f220eba2bc2508
- corpus step-3.7-flash: c52e4f52dc15713a5995ff7bc26b9b04298d79df881dca1a90052b76d2ea69ab
- corpus swe-1-6-slow: ca1e7b85791fb26966cb7671274a29168679b052016653592b77712b92456b7f
- corpus muse-native: 1d5c2ede5332c857a31c053d88b0930d4cb6ca080a549f59012d1defa9c51e07
- geometry: CC_GEOMETRY,lane_n,48,48,48,96,missing,0,base,0,48,96,144
- CL_CHECK: all passed in all legs (teach x5, btrap x5, s10, b7c2, teacher)

## Decision inputs
- class-2 composite: mean 0.99113377, best rep 0.99113377
- best separate source (Q2 D2 sol-only): 0.9911 (4dp)
- class-1 composite: 0.9253
- combined-vs-single: TIE at 4dp (diff 3.38e-05) — the 0-split conflict matrix means the five sources agree on every id, so the combined learner is behaviorally identical to a single-source learner; the gate adds no coverage and costs nothing (withheld=0)

