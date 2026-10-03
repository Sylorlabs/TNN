# PREREG: COGOPS-HEDGEREMOVAL (hedge-removal variant)

Date: 2026-10-03. Worker: COGOPS-HEDGEREMOVAL.
Lane: `docs/lab/research-lead/overnight-20260928/cogops_hedgeremoval/`
Status: FROZEN on commit (this file + NAMECHECK.md +
c17_predicted.txt committed alone before any implementation file
exists). No amendments after implementation begins. Commit hash
recorded in REPORT.md.

Non-ledger task (claim minting paused). Implements
COGOPS-PESSIMISTIC follow-up #2: "Hedge-removal variant: the one
experiment that could actually price S8's tax (P0 shows the prior
alone cannot)."

## 1. Research question

COGOPS-PESSIMISTIC proved (P0, hedge-invariance) that no turn-cost
prior P prices S8's ALT tax: whenever the prior demotes ALT in the
argmin, the evidence-gated hedge (PW/WHOLE/NEED tie, in-context
evidence) re-promotes it. This worker removes the hedge and asks:
(1) Is S8's ALT tax priced (does S8 avoid ALT: chosen != 4,
events < 6)? (2) Does hedge removal break other stages (S12?
S13? S14?)? (3) What is the hedge's value: does it ever fire to
good effect anywhere in this battery?

## 2. Design

### 2.1 The hedge removal (preregistered)

Base: COGOPS-PESSIMISTIC (c16) unchanged, INCLUDING the
pessimistic-prior `(c+8)` N-term constants. The ONLY mechanism
change: in `strat_sel`, DELETE the evidence-gated hedge block
(the `if(tried==0){ if(best!=0){ ... n1/n3 tie checks ...
if(r1==1){ if(r3==1){ best=4; } } } }` region). The argmin loop
(N_s/(u_s+2), exact integer cross-multiplication, lower-id
tie-break) is untouched. Nothing else changes: same per-context
tables, same four strategy forms, same rescue ledger machinery
and counting, same P(fail)/E[rescue] estimators, same
worlds/goals/lesions, same battery stages, c17_base.zag =
c16_base.zag, c17_world.zag = c16_world.zag, the c12 prefix
lines 1..1331 cmp-identical.

Rationale for deletion (not a flag): the hedge is a discrete
mechanism block; a runtime flag would leave dead researcher
machinery in the binary. Deletion is the clean "remove the
hedge" operation. The `strat_sel` argmin nesting shape is
preserved (only the trailing hedge block is removed; no new
nesting).

### 2.2 What changes vs COGOPS-PESSIMISTIC (and what does not)

CHANGED:
- (a) Additive section: `strat_sel`'s hedge block deleted;
  header comments updated to document the hedge-removal variant.
- (b) Driver: c17_main.zag is c16_main.zag with comment updates
  only (stage comments for S8 corrected to the hedge-removed
  predictions; STAGE headers unchanged).

UNCHANGED: everything else, including the (c+8) pessimistic
constants in the three N computations of the argmin loop.

### 2.3 Preregistered behavioral predictions

Notation: ra=rt+2, rb=rc+2, N_s=(c+8)*rb+(f+1)*ra, f=u-w,
score compares N_s/(u_s+2).

H0 (background, established by c16's REPORT + code inspection,
not re-tested here). Under the c16 pessimistic prior the hedge
fires EXACTLY ONCE in the 14-stage battery: at S8. Argument:
the hedge sets best=4 unconditionally when it fires; c16's run
shows DET-STRAT chosen=4 only at S8 (at S8 the argmin loop
leaves best=1, so chosen=4 is the hedge's signature). Every
other initial selection is hedge-inert: cold/zeroed stages have
c1=0 (the hedge requires c1>0 and c3>0, in-context evidence);
S12/S13/S14 are strict argmins with no PW/NEED tie
(1099 != 828; 1355 != 856; 1465 != 928). Rescue-time
strat_sel calls (tried != 0) never satisfy tried==0. Hence
hedge removal has EXACTLY ONE direct behavioral effect: S8's
initial selection. All other predicted differences flow
through the global rescue ledger (rt,rc), which S8's new
rescue observations perturb.

P1 (S8: THE TAX-PRICING PREDICTION). At S8, (rt,rc)=(6,2),
ra=8, rb=4; slot (4,613) carries S7: PW[1,0,2], WHO[1,0,2],
NEED[1,1,4], ALT[0,0,0]. N: PW=WHO=NEED=56 (d=3), ALT=40
(d=2). Argmin: s=1 -> best=1; s=2: 56*3=168 !< 168;
s=3: same; s=4: 40*3=120 !< 56*2=112. best=1. Hedge deleted
-> DET-STRAT chosen=1 (NOT 4). **S8's ALT tax IS priced:
ALT never leads.**
- PW's turn at pass 2 (prior=2): pw_try(2,0,2) eq=0,
  pw_try(2,1,2->lag1) eq=0 [probe-verified eq20=0, eq21=0];
  bi=2 dup skip; bi=3 b<0 skip. PW FAILS, 2 CMP, tc=2.
- cx_rec PW -> [2,0,4]; tried=2; rescue_finalize no-op;
  rescue argmin over {2,3,4}: WHO 56/3 tie NEED 56/3 <
  ALT 40/2 -> WHOLE by id. DET-SWITCH from=1 to=2;
  observation 1 opens.
- WHOLE's turn at pass 3 (prior=2): who_try(3,2) eq=0,
  who_try(3,3) eq=0 [probe-verified eq31=0, eq30=0]. WHOLE
  FAILS, 2 CMP, tc=2, live=2.
- cx_rec WHO -> [2,0,4]; tried=6; rescue_finalize obs1:
  (6+2,2+1)=(8,3); rescue argmin over {3,4}: NEED 56/3 <
  ALT 40/2 -> NEED. DET-SWITCH from=2 to=3; observation 2
  opens.
- NEED's turn at pass 4 (prior=2): need_try(4,2): 4 NCMP
  eq=1,1,1,0 [probe-verified] -> mask=7 (non-empty);
  non-triviality: eq(4,3)=[1,0,0,0], needs 1,2 change
  between pass 3 and 4 -> nt=1 -> DET-HYP goal=823 lag=2
  p=4 q=2 mask=7; osc_one_pass + traj_log(5); verify
  eq(5,3)=[1,1,1] on mask [probe-verified] -> NEED WINS
  at pass 4. tc=4, live=4. DET-PRIOR set=2.
- rescue_finalize obs2: (8+4,3+1)=(12,4). cx_rec NEED ->
  [2,2,8]. Return 1.
- Q id=S8 goal=823 how=1 passes=6. 8 logged comparison
  events (2+2+4). The S8 block is NOT byte-identical to
  RESCUEAWARE's: that is the priced tax. Pricing costs +2
  events vs the hedge's 6 (8 vs 6) and +2 rescue
  observations; the same NEED win is reached through the
  ordinary rescue cascade instead of the untried-ALT
  excursion.

P2 (downstream selections: THE NO-BREAKAGE PREDICTION).
Ledger after S8: (12,4). Cold/zeroed stages (S9, S10, S11)
are selection-invariant to (rt,rc) (all-untried ties break
by id regardless of ra/rb); their blocks are byte-identical
to c16's. S9: PW fail -> SWITCH 1->2 -> WHOLE wins lag 3;
obs -> (14,5). S10: cascade all fail; obs -> (31,8). S9B:
APPLY path, unchanged. S11: zeroed; prior=3; cascade; NEED
wins; obs -> (41,10).
- S12: lesioned (4,613); (rt,rc)=(41,10), ra=43, rb=12.
  PW[2,2,4]: N=187, d=4. NEED[5,5,9]: N=247, d=7.
  WHO/ALT[1,0,4]: N=230, d=3. NEED STRICT argmin:
  247*4=988 < 187*7=1309 -> DET-STRAT chosen=3 (NOT 1,
  NOT 4). NEED wins at pass 2 (4 NCMP eq=1,1,1,0, HYP
  lag=2 p=2 q=0 mask=7). 4 events. No rescue observation;
  (41,10). S12 block byte-identical to c16's.
- S13: lesioned (3,615); (rt,rc)=(41,10), ra=43, rb=12.
  PW[3,2,6]: N=254, d=5 (50.8). WHO untried: N=139, d=2
  (69.5). NEED[2,0,8]: N=321, d=4. PW STRICT argmin:
  254*2=508 < 139*5=695 -> DET-STRAT chosen=1 (NOT 2).
  PW fails at pass 2 (2 CMP); DET-SWITCH 1->2; WHOLE wins
  at pass 3 (2 CMP, HYP lag=3 p=3 q=0 mask=7); DET-PRIOR
  set=3; obs finalizes (43,11). 4 events; Q how=1
  passes=5. S13 block byte-identical to c16's.
- S14: lesioned (3,613); (rt,rc)=(43,11), ra=45, rb=13.
  PW[3,2,6]: N=272, d=5 (54.4). WHO untried: N=149, d=2
  (74.5). ALT[1,0,4]: N=246, d=3. PW STRICT argmin:
  272*2=544 < 149*5=745 -> DET-STRAT chosen=1 (NOT 2).
  PW wins at pass 2 (skip + 2 CMP, HYP lag=2 p=2 q=0
  mask=7); DET-PRIOR set=2; no rescue obs; (43,11). Q
  how=1 passes=4. S14 block byte-identical to c16's.

P3 (rescue ledger). Trace: S7 (6,2); S8 (12,4) [+2 obs,
+6 live]; S9 (14,5); S10 (31,8); S11 (41,10); S12 (41,10)
[no obs]; S13 (43,11); S14 (43,11) [no obs]. Final:
RESCUE total=43 count=11.

P4 (aggregate). Battery total S3..S13 logged comparisons
(eq=-1 skips excluded) = 62: c16's 60, minus S8's 6, plus
S8's 8. All other stages contribute exactly as in c16.

P5 (context tables). CTX0/1/2/3/4 byte-identical to c16:
S8's (4,613) table writes (PW[2,0,4] WHO[2,0,4]
NEED[2,2,8]) are erased by S11's zeroing and S12's lesion
before the end-of-run dump.

P6 (exact stdout). The run output is byte-identical to
c16_run1.txt EXCEPT: (a) the S8 block (new chosen=1
cascade, passes=6, 8 events, S7-shaped OSC-CYCLE phases
[probe-verified]); (b) the final RESCUE line
(total=43 count=11). Frozen in c17_predicted.txt.

### 2.4 Apparatus characterization (pre-freeze, NOT implementation)

A trajectory probe (/tmp/probe_hr_bin, ephemeral) built from
the frozen c16 sources with main replaced by S1A..S7 prefix +
pass-0..5 snapshot printing for goal 823 measured:
eq(2,0)=0, eq(2,1)=0; eq(3,1)=0, eq(3,0)=0; per-need
eq(4,2)=[1,1,1,0], eq(4,3)=[1,0,0,0], eq(5,3)=[1,1,1]; and
trajectory phases at passes 2,3 =
[1,611][1,771][1,771][1,614] /
[1,611][1,772][1,772][1,615] (identical to S7's). The probe
implements no selection, prior, hedge, or rescue logic; the
worlds are frozen and not under test. Kill bars K4/K9/K10/
K11/K15/K16 still genuinely discriminate the hedge-removal
hypothesis.

## 3. Battery stages

Identical to COGOPS-PESSIMISTIC: S1A..S6B
(selection-independent), S3/S5/S7/S9/S10/S9B/S11
(cold/zeroed/APPLY), S8 (4,613 carries S7), S12 (lesioned
4,613), S13 (goal 824, lesioned 3,615), S14 (goal 825,
lesioned 3,613).

## 4. The honest boundary (what this does NOT claim)

- The hedge's value verdict is battery-relative: in THESE
  worlds the hedge fires exactly once (S8) and buys nothing
  (the NEED win it routes around is reached anyway). Whether
  alternation-hedging on a genuine PW/NEED tie is ever
  beneficial is NOT settled here; no world in this battery
  rewards it.
- Pricing S8's tax costs +2 events (8 vs 6) and +2 rescue
  observations at S8; the downstream ledger shift
  (+6,+2 by end of run) is selection-neutral here (P2
  margins verified; K9-K11 test it), not in general.
- Not claimed: L3 invention; generality of 62 events; that
  the hedge should be permanently deleted (a design decision
  for the parent, not this worker); a learner-invented
  hedge policy.

## 5. Kill bars (frozen)

- K1 (S3): context (3,606) cold -> DET-STRAT chosen=1;
  block byte-identical to c16's. FAIL: chosen != 1.
- K2 (S5): context (3,613) cold -> chosen=1; PW wins 1 CMP;
  block byte-identical. FAIL: chosen != 1.
- K3 (S7): cold -> chosen=1; PW fail; SWITCH 1->2; WHOLE
  fail; SWITCH 2->3; NEED wins; rescue (6,2); block
  byte-identical. FAIL: chosen != 1.
- K4 (S8: THE TAX-PRICING BAR): argmin leaves best=1 and
  the hedge is GONE -> DET-STRAT chosen=1 (NOT 4); PW fails
  at pass 2 (DET-CMP p=2 a=2 b=0 eq=0; DET-CMP p=2 a=2 b=1
  eq=0); DET-SWITCH from=1 to=2; WHOLE fails at pass 3
  (DET-CMP p=3 a=3 b=1 eq=0; DET-CMP p=3 a=3 b=0 eq=0);
  DET-SWITCH from=2 to=3; NEED wins at pass 4 (4 DET-NCMP
  eq=1,1,1,0; DET-HYP goal=823 lag=2 p=4 q=2 mask=7);
  DET-PRIOR set=2; 8 logged comparison events; Q how=1
  passes=6; rescue observations recorded -> (12,4). FAIL:
  chosen=4 (hedge not removed), or any DET line differs,
  or NEED does not win at pass 4.
- K5 (S9): cold -> chosen=1; PW fail; SWITCH 1->2; WHOLE
  wins lag 3; obs -> (14,5); block byte-identical. FAIL:
  block differs.
- K6 (S10): cold -> chosen=1; cascade PW->WHOLE->NEED->ALT;
  all fail; 19 events; AGREE=1; (31,8); block byte-identical.
  FAIL: block differs.
- K7 (S9B): two DET-APPLY match=3/3; how=2; block
  byte-identical. FAIL: APPLY rejects.
- K8 (S11): zeroed -> chosen=1; prior=3; cascade; NEED
  wins; (41,10); block byte-identical. FAIL: block differs.
- K9 (S12: THE NO-BREAKAGE BAR 1): NEED strict argmin under
  the shifted ledger (N_NEED=247,d=7; 247*4=988 <
  187*7=1309 vs PW) -> DET-STRAT chosen=3 (NOT 1, NOT 4);
  NEED wins at pass 2 (4 NCMP eq=1,1,1,0, HYP lag=2 p=2 q=0
  mask=7); 4 events; block byte-identical to c16's.
  FAIL: chosen != 3 (ledger shift broke the S12 win), or
  NEED does not win at pass 2.
- K10 (S13: THE NO-BREAKAGE BAR 2): PW strict argmin under
  the shifted ledger (N_PW=254,d=5; 254*2=508 < 139*5=695
  vs WHO) -> DET-STRAT chosen=1 (NOT 2); PW fails at pass 2
  (2 CMP); DET-SWITCH from=1 to=2; WHOLE wins at pass 3
  (2 CMP, HYP lag=3 p=3 q=0 mask=7); DET-PRIOR set=3; obs
  finalizes (43,11); 4 events; Q how=1 passes=5; block
  byte-identical to c16's. FAIL: chosen != 1, or WHOLE
  does not rescue-win at lag 3.
- K11 (S14: THE NO-BREAKAGE BAR 3): PW strict argmin under
  the shifted ledger (N_PW=272,d=5; 272*2=544 < 149*5=745
  vs WHO) -> DET-STRAT chosen=1 (NOT 2); PW wins at pass 2
  (skip + 2 CMP, HYP lag=2 p=2 q=0 mask=7); DET-PRIOR set=2;
  no rescue obs; (43,11); Q how=1 passes=4; block
  byte-identical to c16's. FAIL: chosen != 1, or PW does
  not win at pass 2.
- K12: 3/3 runs byte-identical stdout; stderr empty; `cmp`
  c17_runN.txt against the frozen c17_predicted.txt is
  silent for N=1,2,3.
- K13: safebin active for every command; `which python3`
  and `which python` return nothing before and after; all
  computation pure Zag; single build with the pinned znc;
  new Zag scanned for the `while.*!(` negated-conjunction
  pattern: clean; `strat_sel` keeps the proven argmin
  nesting shape (only the trailing hedge block deleted);
  no new deep nesting.
- K14: c17_learn.zag lines 1..1331 cmp-identical to
  c12_learn.zag lines 1..1331; c17_base.zag cmp-identical to
  c16_base.zag; c17_world.zag cmp-identical to c16_world.zag;
  the additive section differs from c16's exactly by
  deletion of the hedge block plus header comments
  (region-verified); c17_main.zag differs from c16_main.zag
  in comments only (verified by diffing non-comment lines);
  zero world/goal/relation/need literals in the additive
  section.
- K15 (aggregate): battery total S3..S13 logged comparisons
  (eq=-1 skips excluded) = 62 (c16's 60 - S8's 6 + S8's 8).
  FAIL: total != 62.
- K16 (rescue accounting): final summary line reads
  `RESCUE total=43 count=11`. FAIL: any other values (hand
  trace: S7 (6,2), S8 (12,4), S9 (14,5), S10 (31,8),
  S11 (41,10), S12 (41,10) no obs, S13 (43,11),
  S14 (43,11) no obs).

## 6. Section 6: exact predicted stdout (frozen)

Byte-identical to the frozen c17_predicted.txt committed with
this prereg (K12 checks `cmp` silence). The file equals
c16_run1.txt except: (a) the S8 block replaced by the
chosen=1 cascade below; (b) the final RESCUE line reads
`RESCUE total=43 count=11`.

New S8 block:
```
STAGE S8 STRAT-F1
Q id=S8 goal=823 how=1 passes=6
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
DET-HYP goal=823 lag=2 p=4 q=2 mask=7
DET-PRIOR set=2
OSC-CYCLE goal=823 lag=2 nph=2 ph0=[1,611][1,771][1,771][1,614] ph1=[1,611][1,772][1,772][1,615]
OSC-CONFIRM goal=823 ok=1
SPECCHK goal=823 spec=1
OSC-STATE goal=823 lag=2 nph=2 src=0 mask=7
```
