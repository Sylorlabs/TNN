# PREREG: COGOPS-ALTERNATION-WORLD (is the hedge ever beneficial?)

Date: 2026-10-03. Worker: COGOPS-ALTERNATION-WORLD.
Lane: `docs/lab/research-lead/overnight-20260928/cogops_alternation_world/`
Status: FROZEN on commit (this file + NAMECHECK.md +
c18_predicted.txt + c18h_predicted.txt committed alone before
any implementation file exists). No amendments after
implementation begins. Commit hash recorded in REPORT.md.

Non-ledger task (claim minting paused). Implements the
COGOPS-HEDGEREMOVAL follow-up: "A world genuinely rewarding
alternation (PW and NEED each half-right, ALT strictly best)
would test if the hedge is ever beneficial; none exists in
this battery."

## 1. Research question

COGOPS-HEDGEREMOVAL priced the hedge: in the c16/c17 battery
it fires exactly once (S8) and buys nothing (pure cost). What
it did NOT settle: whether alternation-hedging on a genuine
PW/NEED tie is ever beneficial. This worker constructs a
battery where PW and NEED are each half-right (each is the
right strategy on one world), engineers an exact PW/NEED
score tie with in-context evidence for both, and asks: on
the tie world, does the hedge (ALT-first) beat the
hedge-less argmin (PW-first by lower-id tie-break)?

Two binaries, one mechanism delta:
- c18 (no hedge): c17's strat_sel, hedge deleted.
- c18h (with hedge): c16's strat_sel, hedge present.
Same base, same worlds, same driver, same history. The ONLY
difference is the evidence-gated hedge block.

## 2. Design

### 2.1 Worlds (all in world F; new constructors appended to the world file)

- Goal 830 (PW-world): 3 needs [P=(601,621) carrier,
  P=(613,770) with kind-1 SELF-link (oscillates 771<->772),
  T=(S,614,770) via kind-2 fan-out from need1]. Whole state
  oscillates at lag 2 (no drifter). Context (3,613):
  nneeds=3, need_f(G,1,0)=613.
- Goal 831 (NEED-world): 4 needs, goal 830's structure PLUS
  need3 P=(604,611) with kind-1 SELF-link (walks
  612->613->...->618, convergent drifter; never repeats
  within the episode). Partial oscillation: whole state
  never repeats; needs 0..2 cycle at lag 2. Context
  (4,613).
- Goal 832 (TEST-world): byte-identical structure to 831,
  fresh goal tag 832, context (4,613). Fresh tag defeats
  outcome reuse (outc_find misses); same context shares the
  strategy table with 831.

"PW and NEED each half-right": on the PW-world PW is the
efficient winner (2 CMP; NEED untried); on the NEED-world PW
fails outright and NEED wins. Each strategy is the right one
on one world.

### 2.2 Battery stages

Setup (verbatim from c17_main.zag; detection stages dropped):
S1A (world A ret-learn), S1B (world A vfy-learn), S2 (world
D osc-learn), S4 (world E osc-learn), S6L (world C
cycle-learn), S6B (world F setup + re-specialize). Code
inspection: det_handle never writes ret/vfy coverage,
buckets, or specialization state (ret_log_rel/vfy_log_rel
are called only by ret_episode/vfy_episode), so these blocks
are byte-identical to c17_run1.txt's.

Detection:
- S_PW (goal 830): context (3,613) cold -> PW leads by id,
  wins at lag 2. Rescue ledger stays (0,0). Lag prior 0->2.
- S_NEED (goal 831): context (4,613) cold -> PW leads by id,
  fails (2 CMP); WHOLE fails (2 CMP); NEED wins at pass 4
  (4 NCMP). Rescue ledger -> (6,2). Table (4,613):
  PW=(1,0,2), WHOLE=(1,0,2), NEED=(1,1,4).
- S_TEST (goal 832): context (4,613) carries S_NEED. THE
  TIE (see 2.3). With-hedge: ALT re-promoted (chosen=4),
  wins in 6 events, no rescue. Without-hedge: PW leads by
  id (chosen=1), fails; WHOLE fails; NEED wins in 8 events
  with 2 rescue observations.

### 2.3 The tie (preregistered arithmetic)

At S_TEST initial selection: (rt,rc)=(6,2), ra=8, rb=4.
Context (4,613): PW u=1,w=0,c=2,f=1 -> N1=(2+8)*4+(1+1)*8
=56, d=3. WHOLE u=1,w=0,c=2 -> N2=56, d=3. NEED
u=1,w=1,c=4,f=0 -> N3=(4+8)*4+(0+1)*8=56, d=3. ALT untried
-> N4=(0+8)*4+(0+1)*8=40, d=2.
Argmin: s=1 sets best=1 (bu=1,bn=56); s=2:
56*3<56*3 false; s=3: 56*3<56*3 false; s=4:
40*3=120<56*2=112 false. best=1 (PW, lower-id tie-break).
Hedge (c18h only): tried==0, best=1!=0, c1=2>0, c3=4>0;
n1*(bu+2)=56*3=168==bn*(u1+2)=56*3 -> r1=1;
n3*(bu+2)=56*3=168==bn*(u3+2)=56*3 -> r3=1; r1==1 &&
r3==1 -> best=4. THE HEDGE FIRES (chosen=4). Without the
hedge (c18): best=1 stands (chosen=1).
Note: the tie N1==N3==56 is exact but ledger-dependent
(10*rb+2*ra == 12*rb+ra iff ra==2*rb, satisfied at
(rt,rc)=(6,2)). It is deterministic in this battery; K4/K5
verify the firing directly.

### 2.4 Preregistered behavioral predictions

Notation: DET event kinds as in c17.

P1 (S_PW, both binaries identical). Cold (3,613), prior=0.
DET-STRAT chosen=1; DET-PRIOR prior=0; pw_propose at pass 2:
bi=1 eq(2,1)=0 (DET-CMP p=2 a=2 b=1 eq=0); bi=2 eq(2,0)=1
(DET-CMP p=2 a=2 b=0 eq=1); lagp=2; DET-HYP goal=830 lag=2
p=2 q=0 mask=7; verify eq(3,1)=1 -> WIN; DET-PRIOR set=2.
Q id=S_PW goal=830 how=1 passes=4. 2 events. cx_rec PW
win cost 2 -> (3,613): PW=(1,1,2). No rescue. Ledger
(0,0).

P2 (S_NEED, both binaries identical). Cold (4,613),
prior=2. DET-STRAT chosen=1; DET-PRIOR prior=2.
- PW at pass 2: pw_try(2,0,lag2) eq(2,0)=0 (drifter);
  pw_try(2,1,lag1) eq(2,1)=0; bi=2 dup; bi=3 b<0 skip.
  FAIL, 2 CMP. cx_rec PW fail -> (1,0,2). DET-SWITCH
  from=1 to=2; rescue opens.
- WHOLE at pass 3: who_try(3,2) eq(3,1)=0; d=2 dup; d=3
  eq(3,0)=0. FAIL, 2 CMP. cx_rec WHOLE fail -> (1,0,2).
  rescue_finalize obs1: (2,1). DET-SWITCH from=2 to=3;
  rescue opens.
- NEED at pass 4: need_try(4,2): 4 NCMP at (4,2)
  eq=1,1,1,0 (needs 0..2 match at lag 2; drifter need3
  [616] vs [614] = 0); mask=7; non-trivial (need1
  [771] vs [772] changes 3->4); DET-HYP goal=831 lag=2
  p=4 q=2 mask=7; verify at (5,3) eq=1,1,1 -> WIN.
  DET-PRIOR set=2. cx_rec NEED win cost 4 -> (1,1,4).
  rescue_finalize obs2: (6,2).
Q id=S_NEED goal=831 how=1 passes=6. 8 events.

P3 (S_TEST with-hedge, c18h). THE HEDGE-BENEFIT
PREDICTION. DET-STRAT chosen=4 (NOT 1); DET-PRIOR prior=2.
ALT turn (nadv=2):
- pw_propose at pass 2: DET-CMP p=2 a=2 b=0 eq=0;
  DET-CMP p=2 a=2 b=1 eq=0; vr=0. 2 CMP.
- need_turn at pass 3: need_try(3,2): 4 DET-NCMP p=3
  need=0..3 lag=2 eq=1,1,1,0 (at (3,1): need1 [772] vs
  [772]=1; need3 [615] vs [613]=0); mask=7; non-trivial
  (need1 changes 2->3); DET-HYP goal=832 lag=2 p=3 q=1
  mask=7; verify at (4,2): need1 [771] vs [771]=1 -> WIN.
  DET-PRIOR set=2. 4 NCMP.
No DET-SWITCH (single strategy, rescue never opens). tc=6.
cx_rec ALT win cost 6 -> (4,613): ALT=(1,1,6).
Q id=S_TEST goal=832 how=1 passes=5. 6 events. Ledger
stays (6,2).

P4 (S_TEST no-hedge, c18). THE NO-HEDGE-COST PREDICTION.
DET-STRAT chosen=1 (NOT 4); DET-PRIOR prior=2.
- PW at pass 2: 2 CMP fail (as P2). cx_rec PW fail ->
  (2,0,4). DET-SWITCH from=1 to=2; rescue opens.
- WHOLE at pass 3: 2 CMP fail (as P2). cx_rec WHOLE fail
  -> (2,0,4). rescue_finalize obs1: (8,3). DET-SWITCH
  from=2 to=3; rescue opens.
- NEED at pass 4: 4 NCMP win (as P2). DET-HYP goal=832
  lag=2 p=4 q=2 mask=7; DET-PRIOR set=2. cx_rec NEED win
  cost 4 -> (2,2,8). rescue_finalize obs2: (12,4).
Q id=S_TEST goal=832 how=1 passes=6. 8 events.

P5 (summaries).
- c18h: SUMMARY-DET agree=0 plans_built=3 plans_loaded=0
  trials=6 declines=0 prior=2; CTX n=2;
  CTX0 sig=3,613 pw=1,1,2 who=0,0,0 need=0,0,0 alt=0,0,0;
  CTX1 sig=4,613 pw=1,0,2 who=1,0,2 need=1,1,4 alt=1,1,6;
  RESCUE total=6 count=2.
- c18: SUMMARY-DET agree=0 plans_built=3 plans_loaded=0
  trials=6 declines=0 prior=2; CTX n=2;
  CTX0 sig=3,613 pw=1,1,2 who=0,0,0 need=0,0,0 alt=0,0,0;
  CTX1 sig=4,613 pw=2,0,4 who=2,0,4 need=2,2,8 alt=0,0,0;
  RESCUE total=12 count=4.
(trials=6: goal 830 binds tags 801/802, 3 families each;
831/832 reuse binds. plans_built=3: fresh tags 830,831,832.)

P6 (hedge value). On the tie world the hedge is
beneficial: 6 events vs 8, 0 rescue observations vs 2,
single ALT win (1,1,6) vs the PW->WHOLE->NEED cascade.
"ALT strictly best" is relative to the mechanism's
no-hedge tie-break (PW-first); NEED-first would be 4
events but the argmin never selects it (lower-id
tie-break picks PW).

## 3. The honest boundary (what this does NOT claim)

- The tie is engineered (exact, deterministic,
  ledger-dependent); the experiment tests the hedge GIVEN
  its firing condition, not how often the condition arises
  naturally.
- Benefit shown is narrow: skipping WHOLE's wasted turn +
  rescue overhead on a NEED-winnable tie world. Not
  claimed: that alternation-hedging generalizes, that the
  hedge should be kept (Micah's design call), L3
  invention, or a learner-owned hedge policy.
- If K4 fails (hedge does not fire or ALT does not win),
  the verdict is that the hedge is pure cost even here ->
  delete permanently.

## 4. Kill bars (frozen)

- K1 (S_PW): DET-STRAT chosen=1; PW wins at pass 2 in 2
  CMP (DET-CMP p=2 a=2 b=1 eq=0 then p=2 a=2 b=0 eq=1);
  DET-HYP goal=830 lag=2 p=2 q=0 mask=7; DET-PRIOR set=2;
  Q how=1 passes=4. Block byte-identical across c18/c18h.
  FAIL: chosen != 1, or the S_PW blocks differ.
- K2 (S_NEED): DET-STRAT chosen=1; PW fails (2 CMP);
  DET-SWITCH from=1 to=2; WHOLE fails (2 CMP);
  DET-SWITCH from=2 to=3; NEED wins at pass 4 (4 DET-NCMP
  eq=1,1,1,0; DET-HYP goal=831 lag=2 p=4 q=2 mask=7);
  DET-PRIOR set=2; 8 events; Q how=1 passes=6. Block
  byte-identical across c18/c18h. FAIL: chosen != 1, or
  the S_NEED blocks differ.
- K3 (S_TEST tie): the tie arithmetic of 2.3 holds
  (N1=N2=N3=56 d=3, N4=40 d=2; c1=2>0 c3=4>0; argmin
  best=1). Verified via the K4/K5 divergence plus CTX1.
  FAIL: no divergence (chosen equal across binaries).
- K4 (S_TEST with-hedge: THE HEDGE-BENEFIT BAR):
  DET-STRAT chosen=4 (NOT 1); 2 DET-CMP (p=2, eq=0,0);
  4 DET-NCMP p=3 need=0..3 lag=2 eq=1,1,1,0; DET-HYP
  goal=832 lag=2 p=3 q=1 mask=7; DET-PRIOR set=2; NO
  DET-SWITCH; 6 events; Q how=1 passes=5; CTX1
  alt=1,1,6. FAIL: chosen != 4, or any DET line differs.
- K5 (S_TEST no-hedge: THE NO-HEDGE-COST BAR):
  DET-STRAT chosen=1 (NOT 4); PW fails (2 CMP);
  DET-SWITCH from=1 to=2; WHOLE fails (2 CMP);
  DET-SWITCH from=2 to=3; NEED wins at pass 4 (4 NCMP
  eq=1,1,1,0; DET-HYP goal=832 lag=2 p=4 q=2 mask=7);
  DET-PRIOR set=2; 8 events; Q how=1 passes=6; CTX1
  pw=2,0,4 who=2,0,4 need=2,2,8. FAIL: chosen != 1, or
  any DET line differs.
- K6 (hedge benefit, aggregate): with-hedge S_TEST
  events (6) < no-hedge S_TEST events (8); with-hedge
  `RESCUE total=6 count=2`, no-hedge
  `RESCUE total=12 count=4`. FAIL: not strictly less.
- K7 (determinism): 3/3 runs byte-identical per binary
  (sha256 recorded); stderr empty for all 6 runs.
- K8 (frozen prediction): `cmp` c18_runN.txt against
  frozen c18_predicted.txt silent for N=1,2,3; `cmp`
  c18h_runN.txt against frozen c18h_predicted.txt silent
  for N=1,2,3.
- K9 (toolchain): safebin active for every command;
  `which python3` and `which python` return nothing before
  and after; all computation pure Zag; builds with the
  pinned znc only; new Zag scanned for the `while.*!(`
  negated-conjunction pattern: clean; no new deep nesting.
- K10 (source provenance): c18_base.zag cmp-identical to
  c17_base.zag; c18_world.zag lines 1..594 cmp-identical
  to c17_world.zag (3 constructors appended); c18_learn.zag
  and c18h_learn.zag lines 1..1331 cmp-identical to
  c12_learn.zag lines 1..1331; the c18 vs c18h additive
  diff is exactly the hedge block (region-verified);
  c18_main.zag is the single driver for both builds;
  zero world/goal/relation/need literals in the additive
  sections.
- K11 (setup invariance): S1A/S1B/S2/S4/S6L/S6B blocks
  byte-identical to c17_run1.txt's corresponding blocks,
  and identical across the c18/c18h runs.

## 5. Section 5: exact predicted stdout (frozen)

Byte-identical to the frozen c18_predicted.txt (no-hedge)
and c18h_predicted.txt (with-hedge) committed with this
prereg (K8 checks `cmp` silence). Each file equals
c17_run1.txt's S1A/S1B/S2/S4/S6L/S6B blocks, followed by
the S_PW / S_NEED / S_TEST / SUMMARY blocks below.

S_PW block (both binaries):
```
STAGE S_PW PW-WORLD
Q id=S_PW goal=830 how=1 passes=4
DET-STRAT chosen=1
DET-PRIOR prior=0
DET-CMP p=2 a=2 b=1 eq=0
DET-CMP p=2 a=2 b=0 eq=1
DET-HYP goal=830 lag=2 p=2 q=0 mask=7
DET-PRIOR set=2
OSC-CYCLE goal=830 lag=2 nph=2 ph0=[1,611][1,771][1,771] ph1=[1,611][1,772][1,772]
OSC-CONFIRM goal=830 ok=1
SPECCHK goal=830 spec=1
OSC-STATE goal=830 lag=2 nph=2 src=0 mask=7
```

S_NEED block (both binaries):
```
STAGE S_NEED NEED-WORLD
Q id=S_NEED goal=831 how=1 passes=6
DET-STRAT chosen=1
DET-PRIOR prior=2
DET-CMP p=2 a=2 b=0 eq=0
DET-CMP p=2 a=2 b=1 eq=0
DET-SWITCH from=1 to=2
DET-CMP p=3 a=3 b=1 eq=0
DET-CMP p=3 a=3 b=0 eq=0
DET-SWITCH from=2 to=3
DET-NCMP p=4 need=0 lag=2 eq=1
DET-NCMP p=4 need=1 lag=2 eq=1
DET-NCMP p=4 need=2 lag=2 eq=1
DET-NCMP p=4 need=3 lag=2 eq=0
DET-HYP goal=831 lag=2 p=4 q=2 mask=7
DET-PRIOR set=2
OSC-CYCLE goal=831 lag=2 nph=2 ph0=[1,611][1,771][1,771][1,614] ph1=[1,611][1,772][1,772][1,615]
OSC-CONFIRM goal=831 ok=1
SPECCHK goal=831 spec=1
OSC-STATE goal=831 lag=2 nph=2 src=0 mask=7
```

S_TEST block (c18h, with hedge):
```
STAGE S_TEST ALT-WORLD
Q id=S_TEST goal=832 how=1 passes=5
DET-STRAT chosen=4
DET-PRIOR prior=2
DET-CMP p=2 a=2 b=0 eq=0
DET-CMP p=2 a=2 b=1 eq=0
DET-NCMP p=3 need=0 lag=2 eq=1
DET-NCMP p=3 need=1 lag=2 eq=1
DET-NCMP p=3 need=2 lag=2 eq=1
DET-NCMP p=3 need=3 lag=2 eq=0
DET-HYP goal=832 lag=2 p=3 q=1 mask=7
DET-PRIOR set=2
OSC-CYCLE goal=832 lag=2 nph=2 ph0=[1,611][1,772][1,772][1,613] ph1=[1,611][1,771][1,771][1,614]
OSC-CONFIRM goal=832 ok=1
SPECCHK goal=832 spec=1
OSC-STATE goal=832 lag=2 nph=2 src=0 mask=7
```

S_TEST block (c18, no hedge):
```
STAGE S_TEST ALT-WORLD
Q id=S_TEST goal=832 how=1 passes=6
DET-STRAT chosen=1
DET-PRIOR prior=2
DET-CMP p=2 a=2 b=0 eq=0
DET-CMP p=2 a=2 b=1 eq=0
DET-SWITCH from=1 to=2
DET-CMP p=3 a=3 b=1 eq=0
DET-CMP p=3 a=3 b=0 eq=0
DET-SWITCH from=2 to=3
DET-NCMP p=4 need=0 lag=2 eq=1
DET-NCMP p=4 need=1 lag=2 eq=1
DET-NCMP p=4 need=2 lag=2 eq=1
DET-NCMP p=4 need=3 lag=2 eq=0
DET-HYP goal=832 lag=2 p=4 q=2 mask=7
DET-PRIOR set=2
OSC-CYCLE goal=832 lag=2 nph=2 ph0=[1,611][1,771][1,771][1,614] ph1=[1,611][1,772][1,772][1,615]
OSC-CONFIRM goal=832 ok=1
SPECCHK goal=832 spec=1
OSC-STATE goal=832 lag=2 nph=2 src=0 mask=7
```

SUMMARY (c18h):
```
SUMMARY-DET agree=0 plans_built=3 plans_loaded=0 trials=6 declines=0 prior=2
CTX n=2
CTX0 sig=3,613 pw=1,1,2 who=0,0,0 need=0,0,0 alt=0,0,0
CTX1 sig=4,613 pw=1,0,2 who=1,0,2 need=1,1,4 alt=1,1,6
RESCUE total=6 count=2
```

SUMMARY (c18):
```
SUMMARY-DET agree=0 plans_built=3 plans_loaded=0 trials=6 declines=0 prior=2
CTX n=2
CTX0 sig=3,613 pw=1,1,2 who=0,0,0 need=0,0,0 alt=0,0,0
CTX1 sig=4,613 pw=2,0,4 who=2,0,4 need=2,2,8 alt=0,0,0
RESCUE total=12 count=4
```
