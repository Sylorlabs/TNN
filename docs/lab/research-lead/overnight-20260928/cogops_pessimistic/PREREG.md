# PREREG: COGOPS-PESSIMISTIC (pessimistic turn-cost prior)

Date: 2026-10-03. Worker: COGOPS-PESSIMISTIC.
Lane: `docs/lab/research-lead/overnight-20260928/cogops_pessimistic/`
Status: FROZEN on commit (this file + NAMECHECK.md +
c16_predicted.txt committed alone before any implementation file
exists). No amendments after implementation begins. Commit hash
recorded in REPORT.md.

Non-ledger task (claim minting paused). Implements
COGOPS-RESCUEAWARE follow-up #2: "pessimistic turn-cost prior
(the one untested variant that could actually price S8's tax)."

## 1. Research question

COGOPS-RESCUEAWARE showed the rescue-aware score
score_s = E[turn_s] + P(fail_s)*E[rescue] does NOT price S8's
ALT tax, for two mechanism-level reasons: (a) the untried
strategy's optimistic turn-cost prior (1.0) dominates even
after adding P(fail)=1/2 * E[rescue]; (b) the promoted
strategy wins outright, so the rescue term never bites. This
worker tests the one variant RESCUEAWARE named as untested:
give untried strategies a PESSIMISTIC turn-cost prior
(expensive, not cheapest-possible). Three questions:
(1) Does it price S8's ALT tax (does ALT still lead, or does
PW/NEED win)? (2) What is the right pessimistic value?
(3) Does it break the S12 NEED win, or preserve it?

## 2. Design

### 2.1 The pessimistic prior (preregistered)

The rescue-aware score is unchanged in form:
score_s = E[turn_s] + P(fail_s)*E[rescue], argmin of
N_s/(u_s+2) with N_s = (c+2P)(rc+2) + (f+1)(rt+2), exact
integer cross-multiplication, lower-id tie-break. The ONLY
change vs COGOPS-RESCUEAWARE: the turn-cost pseudo-count
constant goes from 2 (two pseudo-observations at cost 1.0
each: the optimistic prior) to 2P with **P = 4** (two
pseudo-observations at cost 4.0 each: the pessimistic
prior). Untried E[turn] goes from 1.0 to 4.0. P(fail) and
E[rescue] are untouched. The hedge is translated, not
removed: it compares the same N_s/(u_s+2) scores.

Why P=4 (fixed, not learner-estimated): (i) 4 is the maximum
observed per-turn cost at the critical S8 stage (NEED's 4 at
S7), so the fixed value coincides with the "max observed"
candidate where it matters; (ii) P=4 is the smallest integer
P that demotes ALT below the tried strategies in S8's
argmin (P>3 required; Section 2.3), making the hedge's role
visible rather than leaving the argmin path ambiguous;
(iii) the headline S8 finding is P-invariant (Section 2.3),
so a learner-estimated evolving P would add machinery
without changing the verdict. The "max observed" and
"global mean" candidates are analyzed in Section 2.4.

Implementation: in `strat_sel`, replace `(c+2)` with
`(c+8)` in the three N computations (main loop, hedge n1,
hedge n3). Comments updated. Nothing else changes.

### 2.2 What changes vs COGOPS-RESCUEAWARE (and what does not)

CHANGED:
- (a) Additive section: `strat_sel`'s N_s uses (c+8) instead
  of (c+2) in all three places; header comments updated to
  document the pessimistic prior P=4.
- (b) Driver: c16_main.zag is c15_main.zag with comment
  updates only (stage comments for S13/S14 corrected to the
  pessimistic-prior predictions; the RESCUE summary line is
  unchanged in form).

UNCHANGED: everything else. Same per-context tables, same
four strategy forms, same rescue ledger machinery and
counting, same P(fail)/E[rescue] estimators, same hedge
structure (translated scores only), same worlds/goals/
lesions, same battery stages, c16_base.zag = c15_base.zag,
c16_world.zag = c15_world.zag, the c12 prefix lines
1..1331 cmp-identical.

### 2.3 Preregistered behavioral predictions

Notation: ra=rt+2, rb=rc+2, N_s=(c+8)*rb+(f+1)*ra, f=u-w,
score compares N_s/(u_s+2).

P0 (the hedge-invariance argument, preregistered before any
run). At S8 the PW-NEED score tie is EXACT and P-invariant:
score_PW - score_NEED = [(2+2P)-(4+2P)]/3 + [(2/3)-(1/3)]*R
= (R-2)/3, independent of P; with R=(6+2)/(2+2)=2.0 from
S7's ledger it is exactly 0 for every P. Hence for P<3 ALT
is the strict argmin (as in RESCUEAWARE); for P>=3 the
argmin demotes ALT to 4th but PW/WHOLE/NEED tie for the
minimum with in-context evidence (c1=2>0, c3=4>0), so the
evidence-gated hedge fires and re-promotes ALT. S8's ALT
lead is therefore INVARIANT to the turn-cost prior: no
P prices the tax through the prior alone. Pricing it would
require changing or removing the hedge, a different
experiment.

P1 (cold contexts unchanged). S3/S5/S7/S9/S10/S11: all-untried
score ties under any P, PW leads by id, rescue selections
follow cold id order. Event streams byte-identical to
COGOPS-RESCUEAWARE. Ledgers: S7 (6,2), S9 (8,3), S10 (25,6),
S11 (35,8).

P2 (S8: THE HEDGE-INVARIANCE PREDICTION). (rt,rc)=(6,2),
ra=8, rb=4. PW[1,0,2]: N=(2+8)*4+(1+1)*8=56, d=3.
WHOLE[1,0,2]: N=56, d=3. NEED[1,1,4]: N=(4+8)*4+(0+1)*8=56,
d=3. ALT[0,0,0]: N=(0+8)*4+(0+1)*8=40, d=2. Argmin:
PW/WHO/NEED tie at 56/3=18.67 < ALT 40/2=20.0, so the
argmin DEMOTES ALT (best=1 after the strict loop). The
hedge then fires: tried==0, n1=n3=56, r1: c1>0, c3>0,
56*3==56*3; r3: 56*3==56*3 -> best=4. DET-STRAT chosen=4.
ALT's PW-form fails (2 CMP, verified RA S8); ALT's NEED-form
wins at pass 3 (4 NCMP, HYP lag=2 p=3 q=1 mask=7, verified
RA S8). 6 logged comparison events. No rescue observation;
(rt,rc) stays (6,2). THE KEY PREDICTION: the pessimistic
prior does NOT price S8's 6-event ALT tax. The S8 block is
byte-identical to COGOPS-RESCUEAWARE's S8 block; only the
selection PATH differs (hedge, not argmin).

P3 (S9/S10/S11 rescue selections unchanged). Untried ties
still break by id; streams identical to RESCUEAWARE.

P4 (S12: THE PRESERVATION BAR). Lesioned slot (4,613),
(rt,rc)=(35,8), ra=37, rb=10. PW[2,2,4]: N=(4+8)*10+37=157,
d=4. NEED[5,5,9]: N=(9+8)*10+37=207, d=7. WHO[1,0,4]:
N=(4+8)*10+2*37=194, d=3. ALT[1,0,4]: N=194, d=3. NEED is
the STRICT argmin (207*4=828 < 157*7=1099) -> DET-STRAT
chosen=3 (NOT 1, NOT 4). Hedge does NOT fire (r1:
157*7=1099 != 207*4=828). NEED leads at pass 2, 4 NCMP
eq=1,1,1,0, HYP lag=2 p=2 q=0 mask=7, WINS at pass 2.
4 events. No rescue observation; (35,8). S12 block
byte-identical to RESCUEAWARE's. Mechanism: no untried
strategy is present, and the prior shift preserves NEED's
reliability advantage.

P5 (S13: THE BLUNT-INSTRUMENT BAR). Lesioned slot (3,615),
(rt,rc)=(35,8), ra=37, rb=10. PW[3,2,6]:
N=(6+8)*10+2*37=214, d=5 (42.8). NEED[2,0,8]:
N=(8+8)*10+3*37=271, d=4 (67.75). WHO untried:
N=(0+8)*10+37=117, d=2 (58.5). ALT untried: 117/2.
PW is the STRICT argmin (214/5 < 117/2) -> DET-STRAT
chosen=1 (NOT 2). Hedge does NOT fire (r3:
271*5=1355 != 214*4=856). PW's turn at pass 2 (prior=2):
pw_try(2,0,lag2) eq=0 [probe-verified]; pw_try(2,1,lag1)
eq=0 [probe-verified]; bi=2 dup, bi=3 b<0 skip; PW FAILS,
2 CMP, tc=2. DET-SWITCH from=1 to=2 (rescue argmin over
{2,3,4}: WHO 117/2=58.5 < NEED 271/4=67.75, ALT ties WHOLE
-> WHOLE by id); rescue observation opens. WHOLE's turn at
pass=3: who_try(3,lag2) eq=0 (1 CMP) [probe-verified];
who_try(3,lag3) eq=1 (1 CMP) [probe-verified] -> HYP lag=3
p=3 q=0 mask=7; verify (4,1)=1 [probe-verified] -> WHOLE
WINS at pass 3. DET-PRIOR set=3. obs finalizes: rescue_live
counts WHOLE's 2 CMPs -> (rt,rc)=(37,9). 4 logged comparison
events. Q how=1 passes=5. OSC-CYCLE etc. identical to
RESCUEAWARE's S13 (same goal, same winning lag).

P6 (S14). Lesioned slot (3,613), (rt,rc)=(37,9), ra=39,
rb=11. PW[3,2,6]: N=(6+8)*11+2*39=232, d=5 (46.4).
NEED[2,0,8]: N=(8+8)*11+3*39=293, d=4 (73.25). ALT[1,0,4]:
N=(4+8)*11+2*39=210, d=3 (70.0). WHO untried:
N=(0+8)*11+39=127, d=2 (63.5). PW is the STRICT argmin
(232/5 < 127/2) -> DET-STRAT chosen=1 (NOT 2). Hedge does
NOT fire (r3: 293*5=1465 != 232*4=928). PW's turn at pass 2
(prior=3): b0=-1 skip (DET-CMP p=2 a=2 b=-1 eq=-1, tc=1);
pw_try(2,1,lag1) eq=0 [probe-verified]; pw_try(2,0,lag2)
eq=1 [probe-verified] -> HYP lag=2 p=2 q=0 mask=7; verify
(3,1)=1 [probe-verified] -> PW WINS at pass 2. DET-PRIOR
set=2. No rescue observation; (37,9). Q how=1 passes=4.
2 counted comparison events (+1 eq=-1 skip, excluded from
totals). OSC-CYCLE etc. identical to RESCUEAWARE's S14.

P7 (S9B). APPLY path, selection-independent: unchanged.

P8 (aggregate). Battery total S3..S13 logged comparisons
(eq=-1 skips excluded) = 60, same as RESCUEAWARE: S13
contributes 4 (2+2) vs RESCUEAWARE's 4 (1+3). The tax is
not priced; the total is unchanged. Final rescue ledger:
RESCUE total=37 count=9 (S13's observation counts 2, not 3).

P9 (context tables). CTX0/1/2/4 byte-identical to
RESCUEAWARE. CTX3 sig=3,615: lesion PW[3,2,6] NEED[2,0,8]
WHO/ALT zeroed, then PW fail tc=2 -> pw=4,2,8; WHO win
tc=2 -> who=1,1,2; final `CTX3 sig=3,615 pw=4,2,8
who=1,1,2 need=2,0,8 alt=0,0,0`.

### 2.4 The pessimistic-value question (preregistered analysis)

- Global mean at S8: observed turn costs (2,2,4), mean 8/3.
  With P=8/3: ALT scores 44/3=14.67 < PW/NEED 136/9=15.11,
  still the strict argmin. The mean is too weak to even
  demote; S8 would be RESCUEAWARE-identical via the argmin
  path. Not implemented.
- Max observed at S8: 4 (NEED's 4). Coincides with fixed
  P=4 at the critical stage; a learner-tracked evolving max
  would add cells and dynamics without changing the S8
  verdict (P0 holds for all P). Not implemented; fixed P=4
  is the transparent equivalent here.
- Fixed P=4: implemented. Demotes ALT in S8's argmin
  (20.0 > 18.67) so the hedge's re-promotion is directly
  observable, and demotes S13/S14's untried leads,
  exhibiting the blunt-instrument cost.

### 2.5 Apparatus characterization (pre-freeze, NOT implementation)

A trajectory probe (/tmp/probe_traj_bin, ephemeral) built
from the frozen c15 sources with main replaced by pass-0..5
snapshot printing measured goal 824: eq(2,0)=0, eq(2,1)=0,
eq(3,1)=0, eq(3,2)=0, eq(3,0)=1, eq(4,1)=1; and goal 825:
eq(2,0)=1, eq(2,1)=0, eq(3,1)=1. All previously-verified
values reproduce exactly (RA S13/S14), grounding the two
new predictions eq24(2,1)=0 and eq25(2,1)=0 used in P5/P6.
The probe implements no selection, prior, or rescue logic;
the worlds are frozen and not under test.

## 3. Battery stages

Identical to COGOPS-RESCUEAWARE: S1A..S6B (selection-
independent), S3/S5/S7/S9/S10/S9B/S11 (cold/zeroed/APPLY),
S8 (4,613 carries S7), S12 (lesioned 4,613), S13 (goal 824,
lesioned 3,615), S14 (goal 825, lesioned 3,613).

## 4. The honest boundary (what this does NOT claim)

- P=4 is a researcher-supplied constant, like the +2/+1
  Laplace constants. The learner does not learn its prior.
- The hedge-invariance (P0) is specific to S8's table and
  R=2.0; it is a mechanism finding about this battery, not
  a general theorem.
- S13/S14's PW leads are a cost of the blunt instrument,
  not a benefit: the prior cannot distinguish S8's bad
  untried from S13/S14's good untried.
- Not claimed: L3 invention; a learner-invented cost model;
  generality of 60 events; that the hedge should be removed
  (that is a separate experiment, not run here).

## 5. Kill bars (frozen)

- K1 (S3): context (3,606) cold -> DET-STRAT chosen=1.
  FAIL: chosen != 1.
- K2 (S5): context (3,613) cold -> chosen=1; PW wins 1 CMP.
  FAIL: chosen != 1.
- K3 (S7): cold -> chosen=1; PW fail; SWITCH 1->2; WHOLE
  fail; SWITCH 2->3; NEED wins; rescue (6,2). FAIL: chosen
  != 1.
- K4 (S8): **THE HEDGE-INVARIANCE BAR**: the argmin demotes
  ALT (N_ALT=40,d=2, 20.0 > N_PW=56,d=3, 18.67) but the
  hedge fires (PW/WHOLE/NEED tie 56/3, c1=2>0, c3=4>0) ->
  DET-STRAT chosen=4 (NOT 1); ALT's PW-form fails (2 CMP);
  NEED-form wins at pass 3 (4 NCMP, HYP lag=2 p=3 q=1
  mask=7); 6 events; NO rescue observation; (6,2); S8 block
  byte-identical to RESCUEAWARE's. FAIL: chosen != 4
  (prior mis-demotes without hedge, or hedge broken), or
  ALT does not win via NEED-form, or a rescue observation
  is recorded.
- K5 (S9): cold -> chosen=1; PW fail; SWITCH 1->2; WHOLE
  wins lag 3; obs -> (8,3). FAIL: NEED rescues before
  WHOLE, or WHOLE does not win.
- K6 (S10): cold -> chosen=1; cascade PW->WHOLE->NEED->ALT;
  all fail; 19 events; AGREE=1; (25,6); no empty obs.
  FAIL: chosen != 1, or any SWITCH differs.
- K7 (S9B): two DET-APPLY match=3/3; how=2. FAIL: APPLY
  rejects.
- K8 (S11): zeroed -> chosen=1; prior=3; cascade; NEED
  wins; (35,8). FAIL: prior != 3, or cascade differs.
- K9 (S12): **THE PRESERVATION BAR**: NEED strict argmin
  under the pessimistic prior (N_NEED=207,d=7;
  207*4=828 < 157*7=1099 vs PW; N_WHO=N_ALT=194,d=3) ->
  DET-STRAT chosen=3 (NOT 1, NOT 4); hedge does NOT fire;
  NEED wins at pass 2 (4 NCMP eq=1,1,1,0, HYP lag=2 p=2 q=0
  mask=7); 4 events; S12 block byte-identical to
  RESCUEAWARE's. FAIL: chosen != 3 (pessimistic prior broke
  the S12 win), or NEED does not win at pass 2.
- K10 (S13): **THE BLUNT-INSTRUMENT BAR**: PW strict argmin
  (N_PW=214,d=5, 42.8 < N_WHO=117,d=2, 58.5) -> DET-STRAT
  chosen=1 (NOT 2); hedge does NOT fire; PW fails at pass 2
  (DET-CMP p=2 a=2 b=0 eq=0; DET-CMP p=2 a=2 b=1 eq=0);
  DET-SWITCH from=1 to=2; WHOLE wins at pass 3 (DET-CMP p=3
  a=3 b=1 eq=0; DET-CMP p=3 a=3 b=0 eq=1; DET-HYP goal=824
  lag=3 p=3 q=0 mask=7); DET-PRIOR set=3; obs finalizes
  (37,9); 4 events; Q how=1 passes=5. FAIL: chosen != 1,
  or WHOLE does not rescue-win at lag 3.
- K11 (S14): PW strict argmin (N_PW=232,d=5, 46.4 <
  N_WHO=127,d=2, 63.5) -> DET-STRAT chosen=1 (NOT 2); PW
  wins at pass 2 (DET-CMP p=2 a=2 b=-1 eq=-1 skip; DET-CMP
  p=2 a=2 b=1 eq=0; DET-CMP p=2 a=2 b=0 eq=1; DET-HYP
  goal=825 lag=2 p=2 q=0 mask=7); DET-PRIOR set=2; no
  rescue obs; (37,9); Q how=1 passes=4. FAIL: chosen != 1,
  or PW does not win at pass 2.
- K12: 3/3 runs byte-identical stdout; stderr empty; `cmp`
  c16_runN.txt against the frozen c16_predicted.txt is
  silent for N=1,2,3.
- K13: safebin active for every command; `which python3`
  and `which python` return nothing before and after; all
  computation pure Zag; single build with the pinned znc;
  new Zag scanned for the `while.*!(` negated-conjunction
  pattern: clean; `strat_sel` keeps the proven nesting shape
  (only the three N-term constants change); no new deep
  nesting.
- K14: c16_learn.zag lines 1..1331 cmp-identical to
  c12_learn.zag lines 1..1331; c16_base.zag cmp-identical to
  c15_base.zag; c16_world.zag cmp-identical to c15_world.zag;
  the additive section differs from c15's exactly in the
  three `(c+2)` -> `(c+8)` N-term constants plus header
  comments (region-verified); c16_main.zag differs from
  c15_main.zag in comments only (verified by diffing
  non-comment lines); zero world/goal/relation/need
  literals in the additive section.
- K15 (aggregate): battery total S3..S13 logged comparisons
  (eq=-1 skips excluded) = 60, unchanged from RESCUEAWARE
  (S13 contributes 4 = 2+2 vs 1+3). FAIL: total != 60.
- K16 (rescue accounting): final summary line reads
  `RESCUE total=37 count=9`. FAIL: any other values (hand
  trace: S7 (6,2), S8 (6,2) no obs, S9 (8,3), S10 (25,6),
  S11 (35,8), S12 (35,8) no obs, S13 (37,9), S14 (37,9)
  no obs).

## 6. Section 6: exact predicted stdout (frozen)

Byte-identical to the frozen c16_predicted.txt committed with
this prereg (K12 checks `cmp` silence). Every stage except
S13, S14, CTX3, and the RESCUE line is byte-identical to
COGOPS-RESCUEAWARE's verified run output (with the
one-line S13 STAGE-header slip corrected: c16 includes the
`STAGE S13 WHOLE-LEAD` line).

New S13 block:
```
STAGE S13 WHOLE-LEAD
Q id=S13 goal=824 how=1 passes=5
DET-STRAT chosen=1
DET-PRIOR prior=2
DET-CMP p=2 a=2 b=0 eq=0
DET-CMP p=2 a=2 b=1 eq=0
DET-SWITCH from=1 to=2
DET-CMP p=3 a=3 b=1 eq=0
DET-CMP p=3 a=3 b=0 eq=1
DET-HYP goal=824 lag=3 p=3 q=0 mask=7
DET-PRIOR set=3
OSC-CYCLE goal=824 lag=3 nph=3 ph0=[1,611][1,781][1,781] ph1=[1,611][1,782][1,782] ph2=[1,611][1,783][1,783]
OSC-CONFIRM goal=824 ok=1
SPECCHK goal=824 spec=1
OSC-STATE goal=824 lag=3 nph=3 src=0 mask=7
```

New S14 block (Q line onward; STAGE/SPEC lines unchanged):
```
Q id=S14 goal=825 how=1 passes=4
DET-STRAT chosen=1
DET-PRIOR prior=3
DET-CMP p=2 a=2 b=-1 eq=-1
DET-CMP p=2 a=2 b=1 eq=0
DET-CMP p=2 a=2 b=0 eq=1
DET-HYP goal=825 lag=2 p=2 q=0 mask=7
DET-PRIOR set=2
OSC-CYCLE goal=825 lag=2 nph=2 ph0=[1,611][1,771][1,771] ph1=[1,611][1,772][1,772]
OSC-CONFIRM goal=825 ok=1
SPECCHK goal=825 spec=1
OSC-STATE goal=825 lag=2 nph=2 src=0 mask=7
```

CTX3 line: `CTX3 sig=3,615 pw=4,2,8 who=1,1,2 need=2,0,8 alt=0,0,0`
Final line: `RESCUE total=37 count=9`
