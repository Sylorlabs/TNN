# PREREG: COGOPS-RESCUEAWARE (rescue-aware expected-cost strategy selection)

Date: 2026-10-03. Worker: COGOPS-RESCUEAWARE.
Lane: `docs/lab/research-lead/overnight-20260928/cogops_rescueaware/`
Status: FROZEN on commit (this file + NAMECHECK.md +
c15_predicted.txt committed alone before any implementation file
exists). No amendments after implementation begins. Commit hash
recorded in REPORT.md.

Non-ledger task (claim minting paused). Implements
COGOPS-EXPECTEDCOST follow-up #1: "Rescue-aware expected cost:
E[turn] + P(fail)*E[rescue], where P(success) does NOT cancel.
This is the variant that could actually price S8's ALT tax."

## 1. Research question

COGOPS-EXPECTEDCOST showed the turn-level expected cost
E[cost] = P(success)*E[cost|success] + P(fail)*E[cost|fail]
collapses to (c+2)/(u+2): P(success) cancels because the
learner pays comparisons whether the turn succeeds or fails,
and S8's 6-event ALT tax persisted. This worker implements the
rescue-aware extension the EC report named as future work:

score_s = E[turn_s] + P(fail_s) * E[rescue]

where P(success) does NOT cancel: the failure probability
re-enters through the expected cost of the rescue loop the
failure triggers. Three questions: (1) What are P(fail) and
E[rescue], concretely - how does the learner estimate them from
its own experience? (2) Does rescue-aware selection price S8's
ALT tax (fewer events than 62)? (3) Where does it behaviorally
diverge from turn-level expected cost, and why?

## 2. Design

### 2.1 The estimators (preregistered)

Per strategy s in the current context's table the learner has
(u_s, w_s, c_s) = (uses, wins, cost), as before. Two new
learner-owned global cells accumulate rescue experience across
all contexts: rt (total post-failure comparisons observed) and
rc (rescue loops observed). A rescue loop is the strategy-loop
activity following a lead failure: when strategy s fails and a
successor is selected, a rescue observation opens; every
subsequent logged comparison (via slog_cmp/slog_ncmp) counts
toward it; it finalizes (rt += live, rc += 1) when the next
failure occurs, the turn resolves (win/quiescence), or the
strategy set exhausts. A failure with no successor opens no
observation (an empty rescue loop is not a rescue observation).

- P(fail_s) = (f_s + 1) / (u_s + 2), f_s = u_s - w_s.
  Laplace failure rate from the learner's own uses/wins.
  Untried: (0+1)/(0+2) = 1/2.
- E[rescue] = (rt + 2) / (rc + 2). Laplace-smoothed mean
  rescue-loop cost from the learner's own failure history,
  GLOBAL across contexts (rescue loops are rare; per-context
  would leave most contexts at the prior; the rescue loop
  tries the same strategy set regardless of context).
  No observations yet: (0+2)/(0+2) = 1.0.
- E[turn_s] = (c_s + 2) / (u_s + 2), as in COGOPS-EXPECTEDCOST.

### 2.2 The selection rule (preregistered derivation)

score_s = (c+2)/(u+2) + ((f+1)/(u+2)) * ((rt+2)/(rc+2))

Put over the common denominator (u+2)(rc+2):

score_s = [(c+2)(rc+2) + (f+1)(rt+2)] / [(u+2)(rc+2)]

The (rc+2) factor is common to all strategies, so argmin
compares N_s/(u_s+2) where N_s = (c+2)(rc+2) + (f+1)(rt+2),
by exact integer cross-multiplication
(N_a*(u_b+2) < N_b*(u_a+2)), lower-id tie-break. No division,
no float. All values are small (N_s under ~1100, cross
products under ~11000); i32 is safe.

P0 (preregistered theoretical prediction): P(success) does NOT
cancel. The score penalizes a strategy by its failure rate
times the expected rescue cost, so a strategy that fails often
pays for the rescue loop it triggers. The untried still get an
optimistic turn-cost prior (1.0) but now also pay
P(fail)=1/2 times the full rescue estimate.

The evidence-gated hedge is preserved in translated form: at
initial selection (tried==0), a tie for the minimum
rescue-aware score shared by strategies 1 and 3 with c1>0 and
c3>0 (in-context evidence; exact cross-multiplication equality
on the N_s/(u_s+2) terms) selects 4. Recording (cx_rec), the
tried bitmask, and det_handle's turn structure are otherwise
UNCHANGED; the rescue loop still selects by the same rule.

### 2.3 Preregistered behavioral predictions

P1 (cold contexts unchanged). S3/S5/S7/S9/S10/S11: all-untried
(or cold-id-order) selections are score ties under any R, so
PW leads by id and every rescue selection follows cold id
order. Event streams identical to COGOPS-EXPECTEDCOST.

P2 (S8: THE TAX-PERSISTENCE PREDICTION). After S7,
(rt,rc)=(6,2): PW's failure opened obs1 (WHOLE's 2 CMP),
WHOLE's failure finalized obs1 and opened obs2 (NEED's 4
NCMP), NEED's win finalized obs2. E[rescue]=(6+2)/(2+2)=2.0.
Slot (4,613): PW[1,0,2] -> N=(2+2)*4+(1+1)*8=32, w=3;
WHOLE[1,0,2] -> 32, w=3; NEED[1,1,4] -> N=(4+2)*4+(0+1)*8=32,
w=3; ALT[0,0,0] -> N=(0+2)*4+(0+1)*8=16, w=2. ALT is the
STRICT argmin (16*3=48 < 32*2=64) -> DET-STRAT chosen=4. ALT's
PW-form fails (2 CMP, verified EC S8); ALT's NEED-form at pass
3 verifies (4 NCMP eq=1,1,1,0, HYP lag=2 p=3 q=1 mask=7,
verified EC S8) and WINS. No failure -> no rescue
observation; (rt,rc) stays (6,2). 6 logged comparison events.
THE KEY PREDICTION: rescue-aware selection does NOT price
away S8's 6-event ALT tax. Mechanism: the untried strategy's
optimistic turn-cost prior (1.0) still dominates even after
adding P(fail)=1/2 * E[rescue]=2.0 (2.0 < 2.67 for PW), AND
the promoted strategy wins outright via its NEED-form, so the
rescue term never gets to bite. Pricing the tax would require
a pessimistic turn-cost prior or a much larger E[rescue], not
merely folding in the rescue term.

P3 (S9/S10/S11: rescue selections follow id order).
S9 (R=2.0): PW fails -> obs3 opens; rescue argmin over
{2,3,4} untried ties -> WHOLE; WHOLE wins (2 CMP) -> obs3
finalizes (rt=8,rc=3). S10 (R=2.0): PW fails -> obs4;
WHOLE -> fails -> obs4 finalizes (rt=10,rc=4), obs5 opens;
NEED -> fails -> obs5 finalizes (rt=16,rc=5), obs6 opens;
ALT -> fails -> obs6 finalizes (rt=25,rc=6); ns=0, no empty
observation; fallback; AGREE=1; 19 events. S11 (R=27/8):
PW fails -> obs7; WHOLE -> fails -> obs7 finalizes
(rt=27,rc=7), obs8 opens; NEED (R=29/9) -> wins (8 NCMP) ->
obs8 finalizes (rt=35,rc=8). All event streams identical to
COGOPS-EXPECTEDCOST.

P4 (S12: THE DIVERGENCE BAR). Lesioned slot (4,613):
PW[2,2,4], NEED[5,5,9], WHO[1,0,4], ALT[1,0,4]; R=37/10
(A=37, B=10). N_PW=(4+2)*10+(0+1)*37=97, w=4 -> 97/4=24.25;
N_NEED=(9+2)*10+(0+1)*37=147, w=7 -> 147/7=21.0;
N_WHO=N_ALT=(4+2)*10+(1+1)*37=134, w=3. NEED is the STRICT
argmin (147*4=588 < 97*7=679) -> DET-STRAT chosen=3 (NOT 1 as
in EC, NOT 4). The hedge does NOT fire (best=3; no 1-3 tie:
861 != 752). NEED leads at pass 2 (prior=2): need_try(lag=2)
logs DET-NCMP p=2 need=0..3 lag=2 eq=1,1,1,0 (probe-verified
apparatus values: pass-0 snapshots [611],[771],[771],[612];
pass-2 [611],[771],[771],[614]); mask={0,1,2}; non-trivial
(need1 changes pass1->pass2: 772->771); DET-HYP goal=823
lag=2 p=2 q=0 mask=7; verify (3,1)=1,1,1 (verified EC S8) ->
NEED WINS at pass 2. 4 logged comparison events (vs 6 in EC).
Q how=1 passes=4. OSC-CYCLE reads live trajectory at q=0:
ph0=[1,611][1,771][1,771][1,612]
ph1=[1,611][1,772][1,772][1,613]. DET-PRIOR set=2. No rescue
observation (lead won). Mechanism: the rescue term amplifies
the P(fail) difference (NEED 1/7 < PW 1/4), rewarding
reliability beyond what turn-level cost sees (EC picked PW:
1.5 < 11/7).

P5 (S13/S14 as computed). S13 (lesioned (3,615), R=37/10):
PW[3,2,6] N=154 w=5; WHO untried N=57 w=2; NEED[2,0,8]
N=211 w=4; ALT untried N=57 w=2. WHOLE/ALT tie -> WHOLE by
id; WHOLE < PW (57*5=285 < 154*2=308) -> chosen=2. WHOLE
fails at pass 2 (1 CMP, verified EC S13); rescue argmin over
{1,3,4}: ALT 57/2 < PW 154/5 (285<308) < NEED -> SWITCH 2->4;
ALT's PW-form wins at lag 3 (3 CMP, HYP lag=3 p=3 q=0 mask=7,
verified EC S13); obs9 finalizes (rt=38,rc=9); prior=3.
S14 (lesioned (3,613), R=40/11): WHO untried N=62 w=2 strict
argmin (62*5=310 < 168*2=336 vs PW; 62*3=186 < 146*2=292 vs
ALT) -> chosen=2; WHOLE wins in 1 CMP (verified EC S14);
DET-PRIOR set=2. Both stages byte-identical to
COGOPS-EXPECTEDCOST.

P6 (S9B). APPLY path, selection-independent: two DET-APPLY
match=3/3, how=2, OSC-REUSE. Unchanged.

P7 (aggregate: fewer events than 62?). Predicted battery
total (S3..S13 logged comparisons, eq=-1 skips excluded) =
60, vs 62 under both EC and percontext. The reduction is
entirely S12 (4 vs 6); S8's tax is NOT priced (6 = 6). So the
honest answer is MIXED: rescue-aware reduces total events by
2 via the S12 lesion (reliability rewarded), but does NOT
price S8's ALT tax. Final rescue state: RESCUE total=38
count=9.

## 3. What changes vs COGOPS-EXPECTEDCOST (and what does not)

CHANGED:
- (a) Additive section: new global learner cells 16680
  (rescue_total), 16684 (rescue_count), 16688 (rescue_open,
  transient), 16692 (rescue_live, transient); new
  `rescue_finalize` helper; `slog_cmp`/`slog_ncmp` count into
  rescue_live while a rescue observation is open;
  `det_handle` resets the transient cells per goal, finalizes
  the open observation on win/quiescence/failure, and opens a
  new observation only when a successor strategy exists;
  `strat_sel` selects by the rescue-aware score
  N_s/(u_s+2), N_s=(c+2)(rc+2)+(f+1)(rt+2), exact integer
  cross-multiplication, hedge translated to the new score.
  Header comments updated.
- (b) Driver: c15_main.zag is c14_main.zag with comment
  updates plus one added summary line `RESCUE total=<rt>
  count=<rc>` after the CTX dump (verified additive-only by
  diffing non-comment lines).

UNCHANGED: the per-context table substrate (8 slots x 14 i32,
same layout, same signature); the four strategy forms;
hypothesis/confirm rules; turn budget; the DET event ring and
dump formats; worlds A/C/D/E/F; all goals and goal
constructors (no new goals); all learning stages S1A..S6B
(selection-independent; byte-identical); the lag prior
substrate (global); c15_base.zag (= c14_base.zag);
c15_world.zag (= c14_world.zag); the c12_learn prefix (lines
1..1331, cmp-identical); the recording rule cx_rec (wins
still recorded; now selection reads them via f=u-w); lesion
cell values (harness-written, unchanged).

## 4. The honest boundary (what this does NOT claim)

- The +2/+1 Laplace constants and the E[turn]+P(fail)*E[rescue]
  FORM are researcher-supplied; only the table values and the
  rescue cells are learner-written. The learner does not learn
  its prior.
- E[rescue] is global by design choice, not derived; a
  per-context variant would be a different experiment (checked
  analytically: S12 still picks NEED, so the divergence is
  robust to this choice, but only the global variant is
  implemented).
- The S12/S13/S14 lesion values are harness-written synthetic
  history; the S12 reliability-reward reading is illustrative
  of the mechanism, not evidence about real strategy quality.
- Not claimed: that rescue-aware prices S8's tax (P2
  preregisters NO); that 60 < 62 generalizes (the reduction
  rides the S12 lesion); L3 representational invention; a
  learner-invented cost model.
- The trajectory probe (/tmp/probe823, apparatus
  characterization only) measured the frozen world's pass-0
  snapshots for goal 823 to ground the S12 NCMP eq values.
  The world is frozen and not under test; the probe
  implements no selection or rescue logic. The kill bars
  still genuinely discriminate the selection hypothesis: a
  wrong score formula, wrong rescue accounting, or wrong
  hedge translation fails K4/K9/K15/K16.

## 5. Battery stages

Identical to COGOPS-EXPECTEDCOST: S1A RET-LEARN (world A), S1B
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
  on the all-tie), NOT 2; PW wins in 1 DET-CMP; DET-HYP goal=820
  lag=2 p=2 q=0 mask=7. FAIL: chosen != 1.
- K3 (S7): context (4,613) cold -> chosen=1; PW fails (2 CMP);
  DET-SWITCH 1->2; WHOLE fails (2 CMP); DET-SWITCH 2->3; NEED
  wins (4 NCMP, HYP lag=2 p=4 q=2 mask=7); rescue (6,2).
  FAIL: chosen != 1.
- K4 (S8): **THE TAX-PERSISTENCE BAR**: ALT untried scores
  N=16,w=2 (8.0), strictly cheapest (48 < 64 vs PW/WHOLE/NEED
  at 32/3) -> DET-STRAT chosen=4 (strict); ALT's PW-form fails
  (2 CMP); ALT's NEED-form wins at pass 3 (4 NCMP, HYP lag=2
  p=3 q=1 mask=7); 6 logged comparison events; NO rescue
  observation (lead won); (rt,rc) stays (6,2). FAIL: chosen
  != 4 (the rescue term mis-prices the untried), or ALT does
  not win via NEED-form, or a rescue observation is recorded.
- K5 (S9): context (3,615) cold -> chosen=1; PW fails (2 CMP);
  DET-SWITCH 1->2; WHOLE rescues via lag-direct order and WINS
  at lag 3 (2 CMP); DET-HYP goal=821 lag=3 p=3 q=0 mask=7;
  DET-PRIOR set=3; obs3 finalizes (rt=8,rc=3). FAIL: NEED
  rescues before WHOLE, or WHOLE does not win.
- K6 (S10): context (3,604) cold -> DET-STRAT chosen=1; cascade
  PW -> DET-SWITCH 1->2 -> WHOLE -> DET-SWITCH 2->3 -> NEED ->
  DET-SWITCH 3->4 -> ALT; all fail; 19 logged comparison events;
  Q how=0 passes=9; AGREE id=S10 a=1; obs4/5/6 finalize
  (rt=25,rc=6); no empty observation for ALT's failure.
  FAIL: chosen != 1, or any SWITCH differs.
- K7 (S9B): stored checker SUCCEEDS: exactly two DET-APPLY
  lines, match=3/3 both; Q how=2 passes=2; OSC-REUSE. FAIL:
  APPLY rejects.
- K8 (S11): zeroed context (4,613) -> DET-STRAT chosen=1;
  DET-PRIOR prior=3; cascade PW (skip + 2 CMP) -> WHOLE (2 CMP)
  -> NEED (8 NCMP); NEED wins (HYP lag=2 p=4 q=2 mask=7);
  DET-PRIOR set=2; obs7/8 finalize (rt=35,rc=8). FAIL: prior
  != 3, or cascade differs.
- K9 (S12): **THE DIVERGENCE BAR**: context lesion (PW[2,2,4]
  -> N=97,w=4; NEED[5,5,9] -> N=147,w=7; WHO/ALT[1,0,4] ->
  N=134,w=3; R=37/10) -> NEED is the STRICT rescue-aware
  argmin (147*4=588 < 97*7=679) -> **DET-STRAT chosen=3 (NOT
  1, NOT 4)**; the hedge does NOT fire (861 != 752);
  need_try at pass 2 logs DET-NCMP p=2 need=0..3 lag=2
  eq=1,1,1,0; DET-HYP goal=823 lag=2 p=2 q=0 mask=7; NEED
  WINS at pass 2; Q how=1 passes=4; 4 logged comparison
  events; OSC-CYCLE
  ph0=[1,611][1,771][1,771][1,612]
  ph1=[1,611][1,772][1,772][1,613]; DET-PRIOR set=2; S12 block
  byte-exact per Section 7. FAIL: chosen != 3 (turn-level cost
  leaked through), or the hedge fires, or NEED does not win
  at pass 2.
- K10 (S13): context lesion (PW[3,2,6] -> N=154,w=5;
  NEED[2,0,8] -> N=211,w=4; WHOLE/ALT untried -> N=57,w=2) ->
  **DET-STRAT chosen=2 (WHOLE strict argmin: 285 < 308)**;
  WHOLE fails at pass 2 (1 CMP); DET-SWITCH from=2 to=4;
  ALT's PW-form wins at lag 3 (3 CMP, HYP lag=3 p=3 q=0
  mask=7); DET-PRIOR set=3; obs9 finalizes (rt=38,rc=9).
  FAIL: WHOLE does not lead, or ALT does not rescue.
- K11 (S14): context lesion (PW[3,2,6], NEED[2,0,8],
  ALT[1,0,4], WHOLE untried -> N=62,w=2) -> **WHOLE is the
  STRICT argmin (310 < 336) -> DET-STRAT chosen=2**; WHOLE
  verifies goal 825 in 1 DET-CMP; DET-HYP goal=825 lag=2 p=2
  q=0 mask=7; DET-PRIOR set=2. FAIL: WHOLE does not strictly
  lead or win.
- K12: 3/3 runs byte-identical stdout; stderr empty; `cmp`
  c15_runN.txt against the frozen c15_predicted.txt is silent
  for N=1,2,3.
- K13: safebin active for every command; `which python3` and
  `which python` return nothing before and after; all
  computation pure Zag; single build with the pinned znc; new
  Zag scanned for the `while.*!(` negated-conjunction pattern:
  clean; `strat_sel` keeps the proven nesting shape (no
  function calls inside nested conditions; exact integer
  cross-multiplication on hoisted locals; only the score terms
  change); rescue hooks follow the same shape.
- K14: c15_learn.zag lines 1..1331 cmp-identical to
  c12_learn.zag lines 1..1331; c15_base.zag cmp-identical to
  c14_base.zag; c15_world.zag cmp-identical to c14_world.zag;
  the additive section differs from c14's exactly in
  `strat_sel`'s rule, the rescue cells/helpers/`slog_*`
  counting/`det_handle` rescue hooks, plus header comments
  (region-verified); c15_main.zag differs from c14_main.zag
  in comments plus the one added RESCUE summary line
  (verified by diffing non-comment lines); zero world/goal/
  relation/need literals in the additive section (the
  +2/+1 are Laplace prior constants, not world literals).
- K15 (aggregate): battery total S3..S13 logged comparisons
  (eq=-1 skips excluded) = 60, vs 62 under EC/percontext.
  FAIL: total != 60 (the S12 4-vs-6 reduction is the
  mechanism's signature; S8's 6 must persist).
- K16 (rescue accounting): final summary line reads
  `RESCUE total=38 count=9`. FAIL: any other values (the
  rescue ledger must match the hand trace: S7 (6,2), S9
  (8,3), S10 (25,6), S11 (35,8), S13 (38,9); no observations
  at S3/S5/S8/S9B/S12/S14).

## 7. Section 7: exact predicted stdout (frozen)

Byte-identical to the frozen c15_predicted.txt committed with
this prereg (K12 checks `cmp` silence). Every stage except S12
and the CTX2/RESCUE lines is byte-identical to
COGOPS-EXPECTEDCOST's verified run (sha256
03c8a42a5c40110e42fe56280b949f0e0caee213f4056377e0bdf1a57105c557).

(See c15_predicted.txt for the full text; the S12 block is
reproduced here:)

```
STAGE S12 STRAT-CORRUPT
Q id=S12 goal=823 how=1 passes=4
DET-STRAT chosen=3
DET-PRIOR prior=2
DET-NCMP p=2 need=0 lag=2 eq=1
DET-NCMP p=2 need=1 lag=2 eq=1
DET-NCMP p=2 need=2 lag=2 eq=1
DET-NCMP p=2 need=3 lag=2 eq=0
DET-HYP goal=823 lag=2 p=2 q=0 mask=7
DET-PRIOR set=2
OSC-CYCLE goal=823 lag=2 nph=2 ph0=[1,611][1,771][1,771][1,612] ph1=[1,611][1,772][1,772][1,613]
OSC-CONFIRM goal=823 ok=1
SPECCHK goal=823 spec=1
OSC-STATE goal=823 lag=2 nph=2 src=0 mask=7
```

CTX2 line: `CTX2 sig=4,613 pw=2,2,4 who=1,0,4 need=6,6,13 alt=1,0,4`
Final line: `RESCUE total=38 count=9`
