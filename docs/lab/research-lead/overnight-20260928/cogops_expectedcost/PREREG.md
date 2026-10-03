# PREREG: COGOPS-EXPECTEDCOST (expected-cost strategy selection)

Date: 2026-10-03. Worker: COGOPS-EXPECTEDCOST.
Lane: `docs/lab/research-lead/overnight-20260928/cogops_expectedcost/`
Status: FROZEN on commit (this file + NAMECHECK.md +
c14_predicted.txt committed alone before any implementation file
exists). No amendments after implementation begins. Commit hash
recorded in REPORT.md.

Non-ledger task (claim minting paused). Implements
COGOPS-PERCONTEXT follow-up #3: "Expected-cost selection: S8's
6-event ALT tax persists within-context; folding P(fail) *
rescue-cost into the optimistic score would price it."

## 1. Research question

COGOPS-PERCONTEXT kept the optimistic-efficiency rule
((w+1)/(c+1) argmax) and moved it into per-context tables. This
worker replaces the selection rule itself while keeping the
per-context tables: select by EXPECTED COST instead of
optimistic efficiency. The task's formula:

E[cost_s] = P(success_s) * E[cost | success_s]
          + P(fail_s)    * E[cost | fail_s]

Three questions: (1) What is the cost model, concretely - how
does the learner estimate P(success) and the conditional costs
from its own table? (2) Does expected-cost selection beat
optimistic efficiency on the frozen battery (fewer events?
better calibration?)? (3) Does the optimistic promotion of the
untried survive in cost form, or does pricing cost kill it?

## 2. Design

### 2.1 The cost model (preregistered derivation)

Per strategy s in the current context's table the learner has
recorded: u_s (uses = turns attempted), w_s (wins = turns that
verified a hypothesis), c_s (total logged comparisons across
those turns). The learner's Laplace-smoothed estimates, all from
its own table, no new cells:

- P(success_s) = (w_s + 1) / (u_s + 2)
- P(fail_s) = (u_s - w_s + 1) / (u_s + 2)
- E[cost | success_s] = (cw_s + 1) / (w_s + 1),
  cw_s = comparisons logged on winning turns
- E[cost | fail_s] = (cl_s + 1) / (l_s + 1),
  cl_s = comparisons on losing turns, l_s = u_s - w_s

Substituting into the task's formula:

E[cost_s] = [(w+1)/(u+2)] * [(cw+1)/(w+1)]
          + [(l+1)/(u+2)]  * [(cl+1)/(l+1)]
        = (cw + 1)/(u + 2) + (cl + 1)/(u + 2)
        = (c_s + 2) / (u_s + 2)

P0 (preregistered theoretical prediction): the
success-probability terms CANCEL. The learner pays comparisons
whether the turn succeeds or fails, so the expected cost of
choosing s is exactly the smoothed mean comparisons per turn.
No new table cells are needed: the existing (uses, wins, cost)
triple suffices, and selection uses only u and c. Wins are still
recorded (they would matter in a rescue-aware extension pricing
P(fail) * E[rescue]; that extension is explicit future work, not
implemented here).

### 2.2 The selection rule

`strat_sel`: argmin over episode-untried strategies of
(c+2)/(u+2), by exact integer cross-multiplication
((c1+2)*(u2+2) < (c2+2)*(u1+2)), lower-id tie-break. A strategy
untried in this context scores (0+2)/(0+2) = 1.0, the cheapest
possible prior: THE COST PRIOR IS OPTIMISTIC, so the unproven
still leads the imperfect. The evidence-gated hedge is preserved
in translated form: at initial selection (tried==0), a tie for
the minimum expected cost shared by strategies 1 and 3 with
c1>0 and c3>0 (in-context evidence; a fresh context keeps the PW
default) selects 4 (the alternation hedge). Returns 0 when every
strategy was tried. Recording (`cx_rec`), the tried bitmask, the
rescue loop, and `det_handle` are UNCHANGED.

### 2.3 Preregistered behavioral predictions

P1 (cold contexts unchanged). S3/S5/S7/S9/S10: all-untried tables
score 1.0 everywhere; PW leads by id; the event streams are
identical to COGOPS-PERCONTEXT.

P2 (S8: the promotion survives in cost form). Slot (4,613)
carries S7: PW[1,0,2] -> 4/3, WHOLE[1,0,2] -> 4/3, NEED[1,1,4]
-> 6/3 = 2.0, ALT untried -> 1.0. ALT is the STRICT argmin
(6 < 8 and 6 < 12 by cross-multiplication) -> DET-STRAT
chosen=4; ALT's PW-form fails (2 CMP), NEED-form wins (4 NCMP,
HYP lag=2 p=3 q=1); 6 logged comparison events. THE KEY
PREDICTION: expected-cost selection does NOT price away S8's
6-event ALT tax, because the untried strategy's cost prior
(1.0) is the cheapest possible. A pessimistic cost prior would
choose PW here; K4 discriminates.

P3 (S11/S13/S14 as computed). S11 (zeroed slot): all 1.0 -> PW
by id; cascade PW -> WHOLE -> NEED (NEED wins, HYP lag=2 p=4
q=2); prior=3 continuity. S13 (lesioned (3,615)): PW 8/5=1.6,
NEED 10/4=2.5, WHOLE/ALT untried 1.0 -> WHOLE strict argmin
(10 < 16, 10 < 20) -> chosen=2; WHOLE fails at pass 2 (1 CMP);
rescue argmin over {1,3,4}: ALT 1.0 < PW 1.6 -> SWITCH 2->4;
ALT's PW-form wins at lag 3 (3 CMP, HYP lag=3 p=3 q=0). S14
(lesioned (3,613)): WHOLE untried 1.0 strict argmin (10 < 16,
6 < 12) -> chosen=2; WHOLE wins in 1 CMP.

P4 (S12: THE DIVERGENCE BAR). Lesioned slot (4,613): PW[2,2,4]
-> 6/4 = 1.5, NEED[5,5,9] -> 11/7 ~= 1.571, WHOLE[1,0,4] ->
6/3 = 2.0, ALT[1,0,4] -> 2.0. PW is the STRICT argmin
(6*7=42 < 11*4=44) -> DET-STRAT chosen=1, NOT 4. The hedge does
NOT fire: the 3/5 efficiency tie is not a cost tie
(11*4=44 != 6*7=42), so r3=0. PW fails (2 CMP); rescue argmin
over {2,3,4}: NEED 11/7 < 14/7=2.0 -> SWITCH 1->3; NEED wins at
pass 3 (4 NCMP, HYP lag=2 p=3 q=1 mask=7); Q how=1 passes=5; 6
logged comparison events. Cost-neutral vs percontext's hedged
ALT path (6 events either way), but a different lead (PW, not
the hedged ALT) and a different winner (NEED, not ALT).

P5 (aggregate: does expected-cost beat optimistic?). Predicted
battery total (S3..S13 logged comparisons, eq=-1 skips excluded)
= 62, IDENTICAL to COGOPS-PERCONTEXT. Expected-cost selection
does NOT reduce events on this battery: the S8 tax persists
(P2), and the single behavioral divergence (S12, P4) is
cost-neutral (6 -> 6). On calibration: neither rule is
calibrated on untried strategies BY CONSTRUCTION (both score
the untried extremally: 1.0 max efficiency, 1.0 min cost). On
tried strategies, EC's S12 estimates (PW 1.5 vs realized
fail-cost 2; NEED 11/7 vs realized win-cost 4) show mean-cost
smoothing under-pricing an expensive win; reported as
observation, not a kill bar. The honest answer to "does this
beat optimistic" is preregistered as NO on fewer events, with
the mechanism-level reason (P0's cancellation + the optimistic
cost prior).

P6 (S9B). APPLY path, selection-independent: two DET-APPLY
match=3/3, how=2, OSC-REUSE. Unchanged.

## 3. What changes vs COGOPS-PERCONTEXT (and what does not)

CHANGED:
- (a) Additive section: `strat_sel` selects by expected cost
  (c+2)/(u+2) argmin with exact integer cross-multiplication
  instead of optimistic efficiency (w+1)/(c+1) argmax; its
  header comment and the additive-section header comment are
  updated to the cost model. The hedge is translated to the
  cost score (tie for minimum, same c1>0/c3>0 evidence gate).
  Every other additive function is untouched (same CTXT pool,
  slot fns, `cx_rec`, `det_handle`, tried mask, rescue loop).
- (b) Driver: c14_main.zag is c13_main.zag with comment-only
  updates (header + stage comments now describe expected-cost
  selection; verified by comparing non-comment lines). No
  behavior change in the harness; lesion cell values unchanged.

UNCHANGED: the per-context table substrate (8 slots x 14 i32,
same layout, same signature); the four strategy forms;
hypothesis/confirm rules; turn budget; the DET event ring and
dump formats; worlds A/C/D/E/F; all goals and goal constructors
(no new goals); all learning stages S1A..S6B
(selection-independent; byte-identical); the lag prior
substrate (global); c14_base.zag (= c13_base.zag);
c14_world.zag (= c13_world.zag); the c12_learn prefix (lines
1..1331, cmp-identical); the recording rule (wins still
recorded though selection uses u and c).

## 4. The honest boundary (what this does NOT claim)

- The cost model prices only the TURN's expected comparisons,
  not the downstream rescue consequence: P(success) cancels at
  the turn level (P0), so a strategy that fails cheaply every
  episode keeps its lead. A rescue-aware extension
  (E[turn] + P(fail) * E[rescue]) is the named next step, not
  implemented here.
- The +2/+1 Laplace constants are researcher-chosen priors; the
  learner does not learn its prior. The optimistic cost prior
  (untried = 1.0 = cheapest possible) is a deliberate design
  choice preserving the promotion; a pessimistic prior would be
  a different experiment.
- Not claimed: that expected-cost beats optimistic (P5
  preregisters NO on fewer events); better calibration in
  general (the battery is not designed to measure it); L3
  representational invention; a learner-invented cost model
  (the expectation FORM is researcher-supplied; only the table
  values are learner-written).
- The S12 lesion values are harness-written synthetic history;
  calibration readings on lesioned cells are illustrative only.

## 5. Battery stages

Identical to COGOPS-PERCONTEXT: S1A RET-LEARN (world A), S1B
VFY-LEARN (world A), S2 OSC-LEARN-D (world D), S3 STRAT-D0
(goal 818, context (3,606) cold), S4 OSC-LEARN-E (world E), S5
STRAT-E0 (goal 820, context (3,613) cold), S6L CYCLE-LEARN-C
(world C), S6B WORLD-F-SETUP, S7 STRAT-F0 (goal 822, context
(4,613) cold), S8 STRAT-F1 (goal 823, context (4,613) carries
S7), S9 STRAT-E1 (goal 821, context (3,615) cold), S10 CONV-816
(goal 816, context (3,604) cold), S9B REUSE-822 (goal 822,
APPLY reuse), S11 STRAT-LESION (goal 823, zeroed context), S12
STRAT-CORRUPT (goal 823, lesioned context), S13 WHOLE-LEAD
(goal 824, lesioned context), S14 WHOLE-STRICT (goal 825,
lesioned context).

## 6. Kill bars (frozen)

- K1 (S3): context (3,606) cold -> DET-STRAT chosen=1; S3 block
  byte-exact per Section 7. FAIL: chosen != 1.
- K2 (S5): context (3,613) cold -> DET-STRAT chosen=1 (PW by id
  cost tie-break), NOT 2; PW wins in 1 DET-CMP; DET-HYP goal=820
  lag=2 p=2 q=0 mask=7. FAIL: chosen != 1.
- K3 (S7): context (4,613) cold -> chosen=1; PW fails (2 CMP);
  DET-SWITCH 1->2; WHOLE fails (2 CMP); DET-SWITCH 2->3; NEED
  wins (4 NCMP, HYP lag=2 p=4 q=2 mask=7). FAIL: chosen != 1.
- K4 (S8): **THE PROMOTION-PRESERVATION BAR**: in-context ALT
  untried scores 1.0, strictly cheapest (6 < 8 vs PW, 6 < 12 vs
  NEED) -> DET-STRAT chosen=4 (strict); ALT's PW-form fails (2
  CMP); NEED-form wins (4 NCMP, HYP lag=2 p=3 q=1 mask=7); 6
  logged comparison events. FAIL: chosen != 4 (the cost prior
  does not promote the untried), or NEED does not win.
- K5 (S9): context (3,615) cold -> chosen=1; PW fails (2 CMP);
  DET-SWITCH 1->2; WHOLE rescues via lag-direct order and WINS
  at lag 3 (2 CMP); DET-HYP goal=821 lag=3 p=3 q=0 mask=7;
  DET-PRIOR set=3. FAIL: NEED rescues before WHOLE, or WHOLE
  does not win.
- K6 (S10): context (3,604) cold -> DET-STRAT chosen=1; cascade
  PW -> DET-SWITCH 1->2 -> WHOLE -> DET-SWITCH 2->3 -> NEED ->
  DET-SWITCH 3->4 -> ALT; all fail; 19 logged comparison events;
  Q how=0 passes=9; AGREE id=S10 a=1. FAIL: chosen != 1, or any
  SWITCH differs.
- K7 (S9B): stored checker SUCCEEDS: exactly two DET-APPLY
  lines, match=3/3 both; Q how=2 passes=2; OSC-REUSE. FAIL:
  APPLY rejects.
- K8 (S11): zeroed context (4,613) -> DET-STRAT chosen=1;
  DET-PRIOR prior=3; cascade PW (skip + 2 CMP) -> WHOLE (2 CMP)
  -> NEED (8 NCMP); NEED wins (HYP lag=2 p=4 q=2 mask=7);
  DET-PRIOR set=2. FAIL: prior != 3, or cascade differs.
- K9 (S12): **THE DIVERGENCE BAR**: context lesion (PW[2,2,4]
  -> EC 6/4 = 1.5; NEED[5,5,9] -> EC 11/7; WHO/ALT[1,0,4] -> EC
  2.0) -> PW is the STRICT expected-cost argmin (42 < 44) ->
  **DET-STRAT chosen=1 (NOT 4)**; the hedge does NOT fire (44
  != 42); PW fails (2 CMP); DET-SWITCH from=1 to=3; NEED wins
  at pass 3 (4 NCMP, HYP lag=2 p=3 q=1 mask=7); Q how=1
  passes=5; 6 logged comparison events; S12 block byte-exact
  per Section 7. FAIL: chosen=4 (the old efficiency rule leaked
  through), or the hedge fires, or NEED does not win at pass 3.
- K10 (S13): context lesion (PW[3,2,6] -> EC 8/5, NEED[2,0,8]
  -> EC 10/4, WHOLE/ALT untried -> EC 1.0) -> **DET-STRAT
  chosen=2 (WHOLE strict argmin, 10 < 16)**; WHOLE fails at
  pass 2 (1 CMP); DET-SWITCH from=2 to=4; ALT's PW-form wins at
  lag 3 (3 CMP, HYP lag=3 p=3 q=0 mask=7); DET-PRIOR set=3.
  FAIL: WHOLE does not lead, or ALT does not rescue.
- K11 (S14): context lesion (PW[3,2,6], NEED[2,0,8],
  ALT[1,0,4], WHOLE untried) -> **WHOLE is the STRICT argmin
  (1.0) -> DET-STRAT chosen=2**; WHOLE verifies goal 825 in 1
  DET-CMP; DET-HYP goal=825 lag=2 p=2 q=0 mask=7; DET-PRIOR
  set=2. FAIL: WHOLE does not strictly lead or win.
- K12: 3/3 runs byte-identical stdout; stderr empty; `cmp`
  c14_runN.txt against the frozen c14_predicted.txt is silent
  for N=1,2,3.
- K13: safebin active for every command; `which python3` and
  `which python` return nothing before and after; all
  computation pure Zag; single build with the pinned znc; new
  Zag scanned for the `while.*!(` negated-conjunction pattern:
  clean; `strat_sel` keeps the proven nesting shape (no
  function calls inside nested conditions; exact integer
  cross-multiplication on hoisted locals; only the score terms
  change).
- K14: c14_learn.zag lines 1..1331 cmp-identical to
  c12_learn.zag lines 1..1331; c14_base.zag cmp-identical to
  c13_base.zag; c14_world.zag cmp-identical to c13_world.zag;
  the additive section differs from c13's exactly in
  `strat_sel`'s rule plus its header comment; c14_main.zag
  differs from c13_main.zag in comments only (verified by
  comparing non-comment lines); zero world/goal/relation/need
  literals in the additive section (the +2/+1 are Laplace prior
  constants, not world literals).

## 7. Section 7: exact predicted stdout (frozen)

Byte-identical to the frozen c14_predicted.txt committed with
this prereg (K12 checks `cmp` silence). Every stage except S12
and the CTX2 line is byte-identical to COGOPS-PERCONTEXT's
verified run (sha256
569befb09b62837b47de961640033dcc1633d88ec65225ba3844423385e46a9e);
S10/S6L carry the E1/E2-corrected lines.

```
STAGE S1A RET-LEARN
EP ep=0 ret n=1
EP ep=1 ret n=1
EP ep=2 ret n=1
EP ep=3 ret n=1
SPEC-RET rev=1 nrel=2 ep0=0 ep1=3 nfacts=56
LSTATE-RET nrel=2 ids=601,602 cnts=16,16 prov=0,0,3,56 rev=1
STAGE S1B VFY-LEARN
EP ep=4 vfy v=1
EP ep=5 vfy v=1
EP ep=6 vfy v=1
EP ep=7 vfy v=0
SPEC-VFY rev=1 nrel=3 ep0=4 ep1=7 nfacts=56
LSTATE-VFY nrel=3 ids=601,602,603 cnts=16,16,16 prov=1,4,7,56 rev=1
STAGE S2 OSC-LEARN-D
EP ep=8 ret n=1
EP ep=9 ret n=1
EP ep=10 ret n=1
EP ep=11 ret n=1
SPEC-RET rev=2 nrel=3 ep0=8 ep1=11 nfacts=61
LSTATE-RET nrel=3 ids=601,602,606 cnts=16,16,3 prov=0,8,11,61 rev=2
EP ep=12 vfy v=1
SPEC-VFY rev=2 nrel=4 ep0=12 ep1=12 nfacts=61
LSTATE-VFY nrel=4 ids=601,602,603,608 cnts=16,16,16,2 prov=1,12,12,61 rev=2
STAGE S3 STRAT-D0
Q id=S3 goal=818 how=1 passes=4
DET-STRAT chosen=1
DET-PRIOR prior=0
DET-CMP p=2 a=2 b=1 eq=0
DET-CMP p=2 a=2 b=0 eq=1
DET-HYP goal=818 lag=2 p=2 q=0 mask=7
DET-PRIOR set=2
OSC-CYCLE goal=818 lag=2 nph=2 ph0=[1,611][1,661][1,661] ph1=[1,611][1,662][1,662]
OSC-CONFIRM goal=818 ok=1
SPECCHK goal=818 spec=1
OSC-STATE goal=818 lag=2 nph=2 src=0 mask=7
STAGE S4 OSC-LEARN-E
EP ep=13 ret n=1
EP ep=14 ret n=1
EP ep=15 ret n=1
EP ep=16 ret n=1
EP ep=17 ret n=1
EP ep=18 ret n=1
EP ep=19 ret n=1
EP ep=20 ret n=1
SPEC-RET rev=3 nrel=5 ep0=13 ep1=20 nfacts=68
LSTATE-RET nrel=5 ids=601,602,606,613,615 cnts=16,16,0,3,4 prov=0,13,20,68 rev=3
EP ep=21 vfy v=1
EP ep=22 vfy v=1
SPEC-VFY rev=3 nrel=6 ep0=21 ep1=22 nfacts=68
LSTATE-VFY nrel=6 ids=601,602,603,608,614,616 cnts=16,16,16,0,2,3 prov=1,21,22,68 rev=3
STAGE S5 STRAT-E0
Q id=S5 goal=820 how=1 passes=4
DET-STRAT chosen=1
DET-PRIOR prior=2
DET-CMP p=2 a=2 b=0 eq=1
DET-HYP goal=820 lag=2 p=2 q=0 mask=7
DET-PRIOR set=2
OSC-CYCLE goal=820 lag=2 nph=2 ph0=[1,611][1,771][1,771] ph1=[1,611][1,772][1,772]
OSC-CONFIRM goal=820 ok=1
SPECCHK goal=820 spec=1
OSC-STATE goal=820 lag=2 nph=2 src=0 mask=7
STAGE S6L CYCLE-LEARN-C
EP ep=23 ret n=1
EP ep=24 ret n=1
EP ep=25 ret n=1
SPEC-RET rev=4 nrel=6 ep0=23 ep1=25 nfacts=72
LSTATE-RET nrel=6 ids=601,602,606,613,615,604 cnts=16,16,0,0,0,8 prov=0,23,25,72 rev=4
EP ep=26 vfy v=1
SPEC-VFY rev=4 nrel=7 ep0=26 ep1=26 nfacts=72
LSTATE-VFY nrel=7 ids=601,602,603,608,614,616,605 cnts=16,16,16,0,0,0,8 prov=1,26,26,72 rev=4
STAGE S6B WORLD-F-SETUP
SPEC-RET rev=5 nrel=6 ep0=13 ep1=20 nfacts=77
LSTATE-RET nrel=6 ids=601,602,606,613,615,604 cnts=16,16,0,3,0,8 prov=0,13,20,77 rev=5
SPEC-VFY rev=5 nrel=7 ep0=21 ep1=22 nfacts=77
LSTATE-VFY nrel=7 ids=601,602,603,608,614,616,605 cnts=16,16,16,0,2,0,8 prov=1,21,22,77 rev=5
STAGE S7 STRAT-F0
Q id=S7 goal=822 how=1 passes=6
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
DET-HYP goal=822 lag=2 p=4 q=2 mask=7
DET-PRIOR set=2
OSC-CYCLE goal=822 lag=2 nph=2 ph0=[1,611][1,771][1,771][1,614] ph1=[1,611][1,772][1,772][1,615]
OSC-CONFIRM goal=822 ok=1
SPECCHK goal=822 spec=1
OSC-STATE goal=822 lag=2 nph=2 src=0 mask=7
STAGE S8 STRAT-F1
Q id=S8 goal=823 how=1 passes=5
DET-STRAT chosen=4
DET-PRIOR prior=2
DET-CMP p=2 a=2 b=0 eq=0
DET-CMP p=2 a=2 b=1 eq=0
DET-NCMP p=3 need=0 lag=2 eq=1
DET-NCMP p=3 need=1 lag=2 eq=1
DET-NCMP p=3 need=2 lag=2 eq=1
DET-NCMP p=3 need=3 lag=2 eq=0
DET-HYP goal=823 lag=2 p=3 q=1 mask=7
DET-PRIOR set=2
OSC-CYCLE goal=823 lag=2 nph=2 ph0=[1,611][1,772][1,772][1,613] ph1=[1,611][1,771][1,771][1,614]
OSC-CONFIRM goal=823 ok=1
SPECCHK goal=823 spec=1
OSC-STATE goal=823 lag=2 nph=2 src=0 mask=7
STAGE S9 STRAT-E1
SPEC-RET rev=6 nrel=6 ep0=13 ep1=20 nfacts=68
LSTATE-RET nrel=6 ids=601,602,606,613,615,604 cnts=16,16,0,3,4,0 prov=0,13,20,68 rev=6
SPEC-VFY rev=6 nrel=7 ep0=21 ep1=22 nfacts=68
LSTATE-VFY nrel=7 ids=601,602,603,608,614,616,605 cnts=16,16,16,0,2,3,0 prov=1,21,22,68 rev=6
Q id=S9 goal=821 how=1 passes=5
DET-STRAT chosen=1
DET-PRIOR prior=2
DET-CMP p=2 a=2 b=0 eq=0
DET-CMP p=2 a=2 b=1 eq=0
DET-SWITCH from=1 to=2
DET-CMP p=3 a=3 b=1 eq=0
DET-CMP p=3 a=3 b=0 eq=1
DET-HYP goal=821 lag=3 p=3 q=0 mask=7
DET-PRIOR set=3
OSC-CYCLE goal=821 lag=3 nph=3 ph0=[1,611][1,781][1,781] ph1=[1,611][1,782][1,782] ph2=[1,611][1,783][1,783]
OSC-CONFIRM goal=821 ok=1
SPECCHK goal=821 spec=1
OSC-STATE goal=821 lag=3 nph=3 src=0 mask=7
STAGE S10 CONV-816
SPEC-RET rev=7 nrel=6 ep0=23 ep1=25 nfacts=72
LSTATE-RET nrel=6 ids=601,602,606,613,615,604 cnts=16,16,0,0,0,8 prov=0,23,25,72 rev=7
SPEC-VFY rev=7 nrel=7 ep0=26 ep1=26 nfacts=72
LSTATE-VFY nrel=7 ids=601,602,603,608,614,616,605 cnts=16,16,16,0,0,0,8 prov=1,26,26,72 rev=7
Q id=S10 goal=816 how=0 passes=9
DET-STRAT chosen=1
DET-PRIOR prior=3
DET-CMP p=2 a=2 b=-1 eq=-1
DET-CMP p=2 a=2 b=1 eq=0
DET-CMP p=2 a=2 b=0 eq=0
DET-SWITCH from=1 to=2
DET-CMP p=3 a=3 b=0 eq=0
DET-CMP p=3 a=3 b=1 eq=0
DET-SWITCH from=2 to=3
DET-NCMP p=4 need=0 lag=3 eq=1
DET-NCMP p=4 need=1 lag=3 eq=0
DET-NCMP p=4 need=2 lag=3 eq=0
DET-NCMP p=4 need=0 lag=2 eq=1
DET-NCMP p=4 need=1 lag=2 eq=0
DET-NCMP p=4 need=2 lag=2 eq=0
DET-SWITCH from=3 to=4
DET-CMP p=5 a=5 b=2 eq=0
DET-CMP p=5 a=5 b=4 eq=0
DET-CMP p=5 a=5 b=3 eq=0
DET-NCMP p=6 need=0 lag=3 eq=1
DET-NCMP p=6 need=1 lag=3 eq=0
DET-NCMP p=6 need=2 lag=3 eq=0
DET-NCMP p=6 need=0 lag=2 eq=1
DET-NCMP p=6 need=1 lag=2 eq=0
DET-NCMP p=6 need=2 lag=2 eq=0
AGREE id=S10 a=1
STAGE S9B REUSE-822
SPEC-RET rev=8 nrel=6 ep0=13 ep1=20 nfacts=77
LSTATE-RET nrel=6 ids=601,602,606,613,615,604 cnts=16,16,0,3,0,8 prov=0,13,20,77 rev=8
SPEC-VFY rev=8 nrel=7 ep0=21 ep1=22 nfacts=77
LSTATE-VFY nrel=7 ids=601,602,603,608,614,616,605 cnts=16,16,16,0,2,0,8 prov=1,21,22,77 rev=8
Q id=S9B goal=822 how=2 passes=2
DET-APPLY goal=822 pass=0 match=3/3
DET-APPLY goal=822 pass=1 match=3/3
OSC-CYCLE goal=822 lag=2 nph=2 ph0=[1,611][1,771][1,771][1,614] ph1=[1,611][1,772][1,772][1,615]
OSC-REUSE goal=822 match=2
SPECCHK goal=822 spec=1
OSC-STATE goal=822 lag=2 nph=2 src=0 mask=7
STAGE S11 STRAT-LESION
Q id=S11 goal=823 how=1 passes=6
DET-STRAT chosen=1
DET-PRIOR prior=3
DET-CMP p=2 a=2 b=-1 eq=-1
DET-CMP p=2 a=2 b=1 eq=0
DET-CMP p=2 a=2 b=0 eq=0
DET-SWITCH from=1 to=2
DET-CMP p=3 a=3 b=0 eq=0
DET-CMP p=3 a=3 b=1 eq=0
DET-SWITCH from=2 to=3
DET-NCMP p=4 need=0 lag=3 eq=1
DET-NCMP p=4 need=1 lag=3 eq=0
DET-NCMP p=4 need=2 lag=3 eq=0
DET-NCMP p=4 need=3 lag=3 eq=0
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
STAGE S12 STRAT-CORRUPT
Q id=S12 goal=823 how=1 passes=5
DET-STRAT chosen=1
DET-PRIOR prior=2
DET-CMP p=2 a=2 b=0 eq=0
DET-CMP p=2 a=2 b=1 eq=0
DET-SWITCH from=1 to=3
DET-NCMP p=3 need=0 lag=2 eq=1
DET-NCMP p=3 need=1 lag=2 eq=1
DET-NCMP p=3 need=2 lag=2 eq=1
DET-NCMP p=3 need=3 lag=2 eq=0
DET-HYP goal=823 lag=2 p=3 q=1 mask=7
DET-PRIOR set=2
OSC-CYCLE goal=823 lag=2 nph=2 ph0=[1,611][1,772][1,772][1,613] ph1=[1,611][1,771][1,771][1,614]
OSC-CONFIRM goal=823 ok=1
SPECCHK goal=823 spec=1
OSC-STATE goal=823 lag=2 nph=2 src=0 mask=7
STAGE S13 WHOLE-LEAD
SPEC-RET rev=9 nrel=6 ep0=13 ep1=20 nfacts=68
LSTATE-RET nrel=6 ids=601,602,606,613,615,604 cnts=16,16,0,3,4,0 prov=0,13,20,68 rev=9
SPEC-VFY rev=9 nrel=7 ep0=21 ep1=22 nfacts=68
LSTATE-VFY nrel=7 ids=601,602,603,608,614,616,605 cnts=16,16,16,0,2,3,0 prov=1,21,22,68 rev=9
Q id=S13 goal=824 how=1 passes=5
DET-STRAT chosen=2
DET-PRIOR prior=2
DET-CMP p=2 a=2 b=0 eq=0
DET-SWITCH from=2 to=4
DET-CMP p=3 a=3 b=1 eq=0
DET-CMP p=3 a=3 b=2 eq=0
DET-CMP p=3 a=3 b=0 eq=1
DET-HYP goal=824 lag=3 p=3 q=0 mask=7
DET-PRIOR set=3
OSC-CYCLE goal=824 lag=3 nph=3 ph0=[1,611][1,781][1,781] ph1=[1,611][1,782][1,782] ph2=[1,611][1,783][1,783]
OSC-CONFIRM goal=824 ok=1
SPECCHK goal=824 spec=1
OSC-STATE goal=824 lag=3 nph=3 src=0 mask=7
STAGE S14 WHOLE-STRICT
SPEC-RET rev=10 nrel=6 ep0=13 ep1=20 nfacts=68
LSTATE-RET nrel=6 ids=601,602,606,613,615,604 cnts=16,16,0,3,4,0 prov=0,13,20,68 rev=10
SPEC-VFY rev=10 nrel=7 ep0=21 ep1=22 nfacts=68
LSTATE-VFY nrel=7 ids=601,602,603,608,614,616,605 cnts=16,16,16,0,2,3,0 prov=1,21,22,68 rev=10
Q id=S14 goal=825 how=1 passes=4
DET-STRAT chosen=2
DET-PRIOR prior=3
DET-CMP p=2 a=2 b=0 eq=1
DET-HYP goal=825 lag=2 p=2 q=0 mask=7
DET-PRIOR set=2
OSC-CYCLE goal=825 lag=2 nph=2 ph0=[1,611][1,771][1,771] ph1=[1,611][1,772][1,772]
OSC-CONFIRM goal=825 ok=1
SPECCHK goal=825 spec=1
OSC-STATE goal=825 lag=2 nph=2 src=0 mask=7
SUMMARY-DET agree=1 plans_built=8 plans_loaded=4 trials=6 declines=0 prior=2
CTX n=5
CTX0 sig=3,606 pw=1,1,2 who=0,0,0 need=0,0,0 alt=0,0,0
CTX1 sig=3,613 pw=3,2,6 who=1,1,1 need=2,0,8 alt=1,0,4
CTX2 sig=4,613 pw=3,2,6 who=1,0,4 need=6,6,13 alt=1,0,4
CTX3 sig=3,615 pw=3,2,6 who=1,0,1 need=2,0,8 alt=1,1,3
CTX4 sig=3,604 pw=1,0,3 who=1,0,2 need=1,0,6 alt=1,0,9
```
