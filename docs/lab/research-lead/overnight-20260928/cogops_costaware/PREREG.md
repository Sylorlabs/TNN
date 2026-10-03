# PREREG: COGOPS-COSTAWARE (cost-aware strategy selection)

Date: 2026-10-03. Worker: COGOPS-COSTAWARE.
Lane: `docs/lab/research-lead/overnight-20260928/cogops_costaware/`
Status: FROZEN on commit (this file + NAMECHECK.md committed alone
before any implementation file exists). No amendments after
implementation begins.

Non-ledger task (claim minting paused). Directly addresses the
explicit future work from COGOPS-STRATEGY: "Cost-aware selection:
fold the tracked cost into the selection rule; test whether
WHOLE's lag-direct order earns the lead on fresh full
oscillations."

## 1. Research question

COGOPS-STRATEGY (BUILD-PASS, K1..K12) showed the learner chooses
the detection strategy from its own verification history, but the
selection rule is win-rate argmax and the cost column of the
strategy table is tracked but never drives choice. Its honest
boundary states: WHOLE never earns a win (capability-identical to
PW per pass; differs only in proposal order and cost), and
cost-aware selection is explicit future work.

This worker folds cost into the selection rule and asks:
(1) What is the right cost metric? (2) Does cost-aware selection
change the strategy landscape? (3) Can cost-aware selection make
WHOLE win?

## 2. Design

### 2.1 The cost metric (preregistered decision)

Candidates considered:
- (a) Logged comparison events (DET-CMP + DET-NCMP): the
  comparisons the learner actually makes per strategy turn.
- (b) Wall-clock time: REJECTED. Nondeterministic; breaks the
  byte-identical determinism requirement (K11); dominated by VM
  scheduling noise, not strategy work.
- (c) Pass count: REJECTED. Too coarse: a NEED pass costs 4-8
  comparisons, a PW pass 1-3; pass count cannot see the order
  difference between PW and WHOLE that this experiment is about.
- (d) Substrate fact-check counters: REJECTED. They measure the
  generic RETRIEVE/VERIFY machinery, not the strategy choice.

CHOSEN: (a) logged comparison events. Deterministic,
learner-observable (the learner itself logs every comparison via
slog_cmp/slog_ncmp), already accumulated in the table's cost
column, and exactly the unit of detection work whose order
differs between PW (recency-pair) and WHOLE (lag-direct).

### 2.2 The selection rule (replaces win-rate argmax)

score(s) = wins(s) / cost(s), "efficiency": wins per comparison.
Equivalently win-rate divided by average cost per episode; it
prefers strategies that deliver wins cheaply. Properties,
all preregistered:

- Exact integer arithmetic: s1 beats s2 iff
  w1*c2 > w2*c1 (cross-multiplication; no division, no float).
- Untried strategies (cost 0) score 0: no optimism bonus, no
  researcher-tuned pseudocount. Cold start (all zero) still
  defaults to PW via the lower-id tie-break, preserving the
  COGOPS-DETECTION substrate default.
- Tie-break: lower strategy id (unchanged).
- Within-episode rescue: best by the same rule among strategies
  not yet tried this episode (unchanged).
- Hedge rule, adapted: at initial selection only, if the best
  POSITIVE efficiency is shared (exact cross-multiplication
  equality) by strategies 1 (PW) and 3 (NEED), select ALT (4).
  Precedence over the id tie-break (unchanged).

The rule has zero free parameters. The ONLY functional code
change in the whole battery is `strat_sel` (wins/cost instead of
wins/uses, plus the hedge equality on the same terms).

### 2.3 What changes vs COGOPS-STRATEGY (and what does not)

CHANGED:
- (a) `strat_sel` in the additive section: efficiency instead of
  win-rate, as specified in 2.2. Every other additive function
  (pw_try, pw_propose, who_try, who_turn, need_try, need_turn,
  det_handle, table accessors, event logging) is untouched.
- (b) S12 lesion retied on efficiency: PW[2,2,4] (0.5),
  NEED[1,1,2] (0.5). The old lesion (PW[2,2,4], NEED[2,2,8]) ties
  win-rate at 1.0 but not efficiency (0.5 vs 0.25); under the new
  rule it would select PW, not hedge. Retieing keeps the hedge
  bar testing the hedge under the new rule.
- (c) New stage S13 (WHOLE-WIN) plus goal 824 (mk_goal824_E2:
  same structure as mk_goal821_E1, fresh tag 824; world file is
  the allowed home of world literals) plus a lesion harness fn
  (strat_lesion_s13: PW[3,2,6] eff 1/3, NEED[2,0,8] eff 0).
  S13 directly tests question (3): lesioned table, fresh
  period-3 goal, PW leads on efficiency, fails; efficiency-ordered
  rescue surfaces WHOLE ahead of scoreless NEED; WHOLE's
  lag-direct order verifies at pass 3.
- (d) Driver: tag821 saved at S9, plan_drop(tag821) at S13,
  S13 stage block. Nothing else.

UNCHANGED: the four strategy forms, hypothesis/confirm rules,
turn budget, the DET event ring and dump formats, worlds A/C/D/E/F,
goals 816/818/820/821/822/823, all learning stages S1A..S6B, the
lag prior substrate, c11_base.zag (= c10_base.zag), and the
c10_learn prefix (lines 1..1331, cmp-identical).

### 2.4 Preregistered structural prediction

Under pure efficiency, WHOLE cannot EARN THE LEAD on any goal:
it has zero wins, hence zero score, while any strategy with a
win scores positive; untried scores zero by preregistered choice
(2.2). WHOLE is therefore only ever tried in rescue, after PW.
S13 tests whether efficiency-ordered rescue can still surface a
WHOLE win: with NEED scoreless (eff 0), the id tie-break orders
WHOLE before NEED, and WHOLE's lag-direct order then verifies a
lag-3 full oscillation in 2 comparisons at pass 3, where PW's
recency order needed 3 (S9 pattern). The predicted finding is
"no lead, but a rescue win" — a NO on earning the lead with a
YES on winning at all, each with its structural reason.

### 2.5 The honest boundary (what this does NOT claim)

- The efficiency RULE is researcher-provided, exactly as the
  win-rate rule was. The learner does not invent cost-awareness
  and does not choose the metric; the table VALUES (uses, wins,
  cost) remain the only learner-written inputs to selection.
- Not claimed: L3 representational invention; learner-invented
  strategy forms; per-context selection (table still global);
  optimality of efficiency among cost-aware rules (the optimistic
  variant (w+1)/(c+1), which WOULD let untried WHOLE lead, is
  explicitly future work, not implemented here).
- WHOLE note: WHOLE remains capability-identical to PW per pass.
  A WHOLE win in rescue is order luck made systematic by the
  rescue rule, reported as-is.

## 3. Battery stages

S1A RET-LEARN (world A), S1B VFY-LEARN (world A), S2 OSC-LEARN-D
(world D), S3 STRAT-D0 (goal 818, cold table, default PW),
S4 OSC-LEARN-E (world E), S5 STRAT-E0 (goal 820), S6L
CYCLE-LEARN-C (world C), S6B WORLD-F-SETUP, S7 STRAT-F0 (goal
822, partial), S8 STRAT-F1 (goal 823, fresh tag), S9 STRAT-E1
(goal 821, period-3; setup_worldE, re-specialize E,
plan_drop(818)), S10 CONV-816 (goal 816; setup_worldC,
re-specialize C, plan_drop(820)), S9B REUSE-822 (goal 822 again),
S11 STRAT-LESION (goal 823, zeroed table), S12 STRAT-CORRUPT
(goal 823, efficiency-tie lesion, hedge selects ALT),
S13 WHOLE-WIN (goal 824, world E, period-3; setup_worldE,
re-specialize E, plan_drop(821), lesion PW[3,2,6] + NEED[2,0,8]).

Plan slots: 818->0, 820->1, 822->2, 823->3; 821 evicts 818;
816 evicts 820; 824 evicts 821. plans_built=7, plans_loaded=4
(S9B, S11, S12 via det_handle pre>=0; S10 via compose_iter on
the fallback path, per COGOPS-STRATEGY E3).

## 4. Kill bars (frozen)

- K1 (S3): cold table selects PW (DET-STRAT chosen=1); S3 block
  byte-exact per Section 7. FAIL: default is not PW under the
  new rule.
- K2 (S5): PW leads as sole winner (eff 1/2); prior pair hits
  (exactly 1 DET-CMP); S5 block byte-exact. FAIL: selection does
  not prefer the experienced winner.
- K3 (S7): PW leads (eff 2/3), fails (2 CMP); DET-SWITCH 1->2;
  WHOLE fails (2 CMP); DET-SWITCH 2->3; NEED wins (4 NCMP,
  HYP mask=7); S7 block byte-exact. FAIL: cascade broken.
- K4 (S8): **PW leads on efficiency (DET-STRAT chosen=1), NOT
  NEED** (eff 2/5=0.4 > 1/4=0.25; cross-mult 8>5; no hedge:
  5 != 8). PW fails (2 CMP); DET-SWITCH 1->3; NEED rescues
  (4 NCMP, HYP lag=2 p=3 q=1 mask=7); Q how=1 passes=5; S8 block
  byte-exact. THE LANDSCAPE-CHANGE BAR. FAIL: NEED leads (the
  rule is win-rate, not cost-aware) or PW does not fail first.
- K5 (S9): **PW leads (eff 2/7 > 2/8; 16>14; no hedge)**,
  fails (2 CMP: lag 3 inapplicable at pass 2); DET-SWITCH 1->3;
  NEED wins at lag 3 (6 NCMP: lag-2 trivial reject, lag-3
  verify; HYP lag=3 p=3 q=0 mask=7); DET-PRIOR set=3; Q how=1
  passes=5; S9 block byte-exact. FAIL: NEED leads first or PW
  wins.
- K6 (S10): PW leads (eff 2/9 vs 3/14; 28>27); cascade
  PW(2)->NEED(3)->WHOLE(4)->ALT(5,6), all fail; Q how=0
  passes=9; AGREE id=S10 a=1; S10 block byte-exact (the
  E1-corrected order). FAIL: any false positive or wrong order.
- K7 (S9B): stored partial checker applies (2 DET-APPLY
  match=3/3); OSC-CYCLE byte-identical to S7's; S9B block
  byte-exact. FAIL: mask-aware APPLY broken.
- K8 (S11): zeroed table -> DET-STRAT chosen=1; cascade
  PW->WHOLE->NEED; 15 logged comparisons; NEED wins (8 NCMP,
  HYP mask=7); S11 block byte-exact; Q how=1 passes=6. FAIL:
  NEED leads despite zeroed table.
- K9 (S12): **efficiency-tie lesion (PW[2,2,4] eff 0.5,
  NEED[1,1,2] eff 0.5; 2*2==1*4) -> hedge -> DET-STRAT
  chosen=4**; ALT's PW-form fails (2 CMP), NEED-form wins
  (4 NCMP, HYP lag=2 p=3 q=1 mask=7); Q how=1 passes=5; S12
  block byte-exact. FAIL: PW leads (hedge not on efficiency)
  or ALT fails.
- K10 (S13): **lesioned PW[3,2,6] (eff 1/3) vs NEED[2,0,8]
  (eff 0) -> DET-STRAT chosen=1 (no hedge: 0 != 16)**; PW fails
  at pass 2 (2 CMP); DET-SWITCH 1->2; **WHOLE rescues at pass 3
  via lag-direct order ((3,1) eq=0, (3,0) eq=1; 2 CMP) and WINS**;
  DET-HYP goal=824 lag=3 p=3 q=0 mask=7; DET-PRIOR set=3; Q
  how=1 passes=5; S13 block byte-exact. THE WHOLE-WIN BAR.
  FAIL: WHOLE does not win, or PW does not lead, or NEED is
  tried before WHOLE.
- K11: 3/3 runs byte-identical stdout; stderr empty.
- K12: safebin active for every command; `which python3` and
  `which python` return nothing before and after; all computation
  pure Zag; single build with the pinned znc; new Zag scanned for
  the `while.*!(` negated-conjunction pattern: clean; `strat_sel`
  keeps the proven nesting shape.
- K13: c11_learn.zag lines 1..1331 cmp-identical to c10_learn.zag
  lines 1..1331; c11_base.zag cmp-identical to c10_base.zag; the
  additive section differs from c10's in exactly `strat_sel`
  (verified by diff); zero world/goal/relation/need literals in
  the additive section and c11_main.zag outside the harness fns
  (goal constructors live in c11_world.zag, the allowed home).

## 5. Section 7: exact predicted stdout (frozen)

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
DET-SWITCH from=1 to=3
DET-NCMP p=3 need=0 lag=2 eq=1
DET-NCMP p=3 need=1 lag=2 eq=0
DET-NCMP p=3 need=2 lag=2 eq=0
DET-NCMP p=3 need=0 lag=3 eq=1
DET-NCMP p=3 need=1 lag=3 eq=1
DET-NCMP p=3 need=2 lag=3 eq=1
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
DET-SWITCH from=1 to=3
DET-NCMP p=3 need=0 lag=3 eq=1
DET-NCMP p=3 need=1 lag=3 eq=0
DET-NCMP p=3 need=2 lag=3 eq=0
DET-NCMP p=3 need=0 lag=2 eq=1
DET-NCMP p=3 need=1 lag=2 eq=0
DET-NCMP p=3 need=2 lag=2 eq=0
DET-SWITCH from=3 to=2
DET-CMP p=4 a=4 b=1 eq=0
DET-CMP p=4 a=4 b=2 eq=0
DET-SWITCH from=2 to=4
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
OSC-STATE goal=822 lag=2 nph=2 src=1 mask=7
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
STAGE S13 WHOLE-WIN
SPEC-RET rev=9 nrel=6 ep0=13 ep1=20 nfacts=68
LSTATE-RET nrel=6 ids=601,602,606,613,615,604 cnts=16,16,0,3,4,0 prov=0,13,20,68 rev=9
SPEC-VFY rev=9 nrel=7 ep0=21 ep1=22 nfacts=68
LSTATE-VFY nrel=7 ids=601,602,603,608,614,616,605 cnts=16,16,16,0,2,3,0 prov=1,21,22,68 rev=9
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
SUMMARY-DET agree=1 plans_built=7 plans_loaded=4 trials=6 declines=0 prior=3 strat_pw=4,2,8 strat_who=1,1,2 strat_need=2,0,8 strat_alt=0,0,0
```
