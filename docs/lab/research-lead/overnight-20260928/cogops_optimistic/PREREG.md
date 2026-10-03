# PREREG: COGOPS-OPTIMISTIC (optimistic efficiency selection)

Date: 2026-10-03. Worker: COGOPS-OPTIMISTIC.
Lane: `docs/lab/research-lead/overnight-20260928/cogops_optimistic/`
Status: FROZEN on commit (this file + NAMECHECK.md committed alone
before any implementation file exists). No amendments after
implementation begins.

Non-ledger task (claim minting paused). Implements follow-up #1
from COGOPS-COSTAWARE: "Optimistic efficiency ((w+1)/(c+1)):
test whether untried WHOLE earns the lead on fresh full
oscillations; compare exploration cost vs pure efficiency's
exploitation."

## 1. Research question

COGOPS-COSTAWARE (BUILD-PASS, K1..K13) showed cost-aware
selection by pure efficiency (wins per logged comparison) changes
the strategy landscape, but with a structural ceiling: an untried
strategy scores exactly 0, so WHOLE can never EARN THE LEAD; it
won S13 only because efficiency-ordered rescue surfaced it after
PW failed. The preregistered structural prediction held: "no
lead, but a rescue win."

This worker replaces the zero prior with an optimistic
+1/+1 prior: score(s) = (wins(s)+1)/(cost(s)+1). An untried
strategy scores (0+1)/(0+1) = 1.0, the maximum achievable score.
Questions: (1) Does untried WHOLE now earn the lead on fresh
full oscillations? (2) What does optimism cost (over-exploration)?
(3) Does optimism oscillate (strategies ping-ponging the lead
without settling)? (4) How does the episode-cost landscape compare
against the COGOPS-COSTAWARE baseline, stage by stage?

## 2. Design

### 2.1 The selection rule (replaces pure efficiency)

score(s) = (w(s)+1)/(c(s)+1), "optimistic efficiency": wins per
logged comparison with a Laplace-style +1/+1 prior. Properties,
all preregistered:

- Exact integer arithmetic: s1 beats s2 iff
  (w1+1)*(c2+1) > (w2+1)*(c1+1) (cross-multiplication; no
  division, no float). The denominator (c+1) is never zero, so
  the zero-cost guards of the pure-efficiency version are gone.
- Untried strategies score exactly 1.0. Since a tried strategy
  scores (w+1)/(c+1) <= 1.0 with equality iff w = c (a perfect
  record: one win per logged comparison), an untried strategy
  STRICTLY leads every imperfect tried strategy and TIES a
  perfect tried strategy (id tie-break then keeps the tried
  incumbent). Optimism promotes only the unproven over the
  imperfect, never over the perfect.
- Tie-break: lower strategy id (unchanged).
- Within-episode rescue: best by the same rule among strategies
  not yet tried this episode (unchanged).
- Hedge rule, adapted: at initial selection only (tried == 0),
  if the best optimistic score is shared by tried strategies 1
  (PW) and 3 (NEED) via exact cross-multiplication equality on
  the optimistic terms, select ALT (4). The hedge additionally
  requires EVIDENCE (c1 > 0 and c3 > 0): a cold table is a
  vacuous four-way tie at 1.0, and must keep the PW default via
  the id tie-break (the COGOPS-DETECTION substrate default is
  preserved). Precedence over the id tie-break (unchanged).
- The rule has zero free parameters. The +1/+1 prior is not
  tuned: it is the smallest integer pseudocount, and 1.0 is the
  score's natural maximum.

### 2.2 Preregistered structural predictions

P1 (cold start). All four strategies score 1.0; the hedge does
not fire (no evidence); PW leads by id. S3 is byte-identical to
COGOPS-COSTAWARE's S3.

P2 (the headline). On a fresh full oscillation with WHOLE
untried and every tried strategy imperfect, untried WHOLE earns
the LEAD at initial selection (not in rescue). S5 (goal 820,
fresh lag-2 full oscillation; PW[1,1,2] scores 2/3 < 1.0):
DET-STRAT chosen=2, WHOLE's lag-direct order verifies in 1
comparison. This is the direct YES to the follow-up question.

P3 (strict lead, not tie-break). S5's lead is shared with untried
NEED/ALT (id tie-break picks WHOLE). S14 controls this away: a
lesion with PW[3,2,6] (3/7), NEED[2,0,8] (1/9), ALT[1,0,4]
(1/5), WHOLE untried makes WHOLE the STRICT argmax at 1.0. On
the fresh lag-2 full oscillation (goal 825), WHOLE leads and
wins in 1 comparison.

P4 (lead is not win). Optimism buys the lead, not the
verification. S13 (lesioned PW[3,2,6], NEED[2,0,8], WHO/ALT
untried; period-3 goal 824): WHOLE leads (chosen=2), fails at
pass 2 (lag 3 inapplicable; 1 CMP), and ALT rescues via its
PW-form at lag 3. Optimism's promotion is falsifiable per
episode.

P5 (over-exploration tax, measured). Untried strategies lead and
sometimes fail, spending comparisons a pure-exploitation rule
would not. S8: untried ALT (1.0) leads over PW/WHOLE (2/3);
ALT's PW-form fails (2 CMP) before its NEED-form wins: 6 logged
events vs 4 for NEED-direct. S13: WHOLE's failed lead costs 1
CMP before ALT wins. The tax is bounded and visible in the
DET ring.

P6 (no pathological oscillation). The prior is one-shot per
strategy: the untried->tried transition consumes it. After all
four are tried, selection is (w+1)/(c+1) argmax, which converges
to empirical-efficiency argmax as evidence accumulates (the +1
terms decay as 1/n). A strategy that keeps failing has its
score monotonically decreased by each failure, so it cannot
cycle back over a cheaper-failing competitor except on
evidence. S9/S10 (all-tried tables) select by near-empirical
efficiency with no cycling: S9 PW leads on the 2/3 id tie-break,
S10 WHOLE leads at 3/5 > 2/5.

P7 (optimism changes the learner's own training data). Because
optimism changes WHEN hypotheses fire, stored outcome snapshots
can misalign with fresh trajectories. S7 hypothesizes at q=1
(WHOLE led, NEED rescued at pass 3) where COGOPS-COSTAWARE
hypothesized at q=2; the stored phases (pass 1, pass 2) therefore
do not match a fresh pass-0 trajectory, so S9B's mask-aware
APPLY correctly rejects (match=1/3, single DET-APPLY line) and
the learner re-detects from scratch (WHOLE->PW->NEED cascade,
NEED wins, prior re-set to 2). The stored-checker machinery is
alignment-sensitive, as designed; optimism exercises the
rejection path for the first time.

### 2.3 What changes vs COGOPS-COSTAWARE (and what does not)

CHANGED:
- (a) `strat_sel` in the additive section: optimistic
  efficiency (w+1)/(c+1) with exact integer cross-multiplication
  ((w1+1)*(c2+1) > (w2+1)*(c1+1)), id tie-break, rescue
  unchanged, hedge on optimistic terms requiring c1>0 and
  c3>0. Every other additive function is untouched.
- (b) S12 lesion retied for optimism: PW[2,2,4] (3/5),
  NEED[5,5,9] (3/5), WHO[1,0,4] (1/5), ALT[1,0,4] (1/5). The
  old lesion (PW[2,2,4], NEED[1,1,2]) ties pure efficiency at
  0.5 but not optimistic efficiency (3/5 vs 2/3); worse, under
  optimism untried WHO/ALT (1.0) would dominate the lesion and
  the hedge could never fire. The new lesion gives all four
  tried scores with PW/NEED tied at the best (3/5), so the
  hedge bar tests the hedge under the new rule.
- (c) S13 restaged honestly: same lesion as COGOPS-COSTAWARE's
  S13 (PW[3,2,6], NEED[2,0,8], WHO/ALT untried), but under
  optimism WHOLE leads outright (chosen=2) instead of rescuing.
  Renamed WHOLE-LEAD: it tests P4 (lead is not win).
- (d) New stage S14 (WHOLE-STRICT) plus goal 825 (mk_goal825_E3:
  same structure as mk_goal820_E0, fresh tag 825; world file is
  the allowed home of world literals) plus lesion harness fn
  strat_lesion_s14 (PW[3,2,6], NEED[2,0,8], ALT[1,0,4], WHOLE
  untried). Tests P3: strict optimistic lead and win.
- (e) Driver: tag824 saved at S13, plan_drop(tag824) at S14,
  S14 stage block, S12/S13/S14 comments updated. Nothing else.

UNCHANGED: the four strategy forms, hypothesis/confirm rules,
turn budget, the DET event ring and dump formats, worlds
A/C/D/E/F, goals 816/818/820/821/822/823/824, all learning
stages S1A..S6B (selection-independent; byte-identical), the lag
prior substrate, c12_base.zag (= c11_base.zag), and the
c11_learn prefix (lines 1..1331, cmp-identical).

### 2.4 The honest boundary (what this does NOT claim)

- The optimistic RULE is researcher-provided, exactly as the
  win-rate and pure-efficiency rules were. The learner does not
  invent optimism, does not choose the prior, and does not
  choose the metric; the table VALUES (uses, wins, cost) remain
  the only learner-written inputs to selection.
- Not claimed: L3 representational invention; learner-invented
  strategy forms; per-context selection (table still global);
  optimality of (w+1)/(c+1) among optimistic rules (the +1/+1
  prior is the smallest integer choice, not a tuned one);
  expected-cost selection (follow-up #3).
- WHOLE note: WHOLE remains capability-identical to PW per pass.
  An optimistic WHOLE lead is prior luck made systematic by the
  selection rule, reported as-is with its measured tax.

## 3. Battery stages

S1A RET-LEARN (world A), S1B VFY-LEARN (world A), S2 OSC-LEARN-D
(world D), S3 STRAT-D0 (goal 818, cold table, PW default by
id tie-break), S4 OSC-LEARN-E (world E), S5 STRAT-E0 (goal 820:
untried WHOLE earns the lead, wins in 1 CMP), S6L
CYCLE-LEARN-C (world C), S6B WORLD-F-SETUP, S7 STRAT-F0 (goal
822, partial: WHOLE leads, fails, NEED rescues at pass 3),
S8 STRAT-F1 (goal 823, fresh tag: untried ALT leads,
over-exploration tax, ALT wins via NEED-form), S9 STRAT-E1
(goal 821, period-3; setup_worldE, re-specialize E,
plan_drop(818): PW leads on 2/3 tie-break, fails, WHOLE rescues
and wins at lag 3), S10 CONV-816 (goal 816; setup_worldC,
re-specialize C, plan_drop(820): WHOLE leads at 3/5, cascade
all fail, generic fallback, oracle agreement), S9B REUSE-822
(goal 822 again: misaligned stored checker correctly rejected
at match=1/3, re-detection cascade, NEED wins, prior re-set),
S11 STRAT-LESION (goal 823, zeroed table: PW default cascade),
S12 STRAT-CORRUPT (goal 823, optimistic-tie lesion, hedge
selects ALT), S13 WHOLE-LEAD (goal 824, world E, period-3;
setup_worldE, re-specialize E, plan_drop(821), lesion
PW[3,2,6] + NEED[2,0,8]: WHOLE leads outright, fails at pass 2,
ALT rescues at lag 3), S14 WHOLE-STRICT (goal 825, world E,
lag-2 full; setup_worldE, re-specialize E, plan_drop(824),
lesion PW[3,2,6] + NEED[2,0,8] + ALT[1,0,4]: WHOLE strict lead
and win).

Plan slots: 818->0, 820->1, 822->2, 823->3; 821 evicts 818;
816 evicts 820; 824 evicts 821; 825 evicts 824.
plans_built=8, plans_loaded=4 (S9B, S11, S12 via det_handle
pre>=0; S10 via compose_iter on the fallback path, per
COGOPS-COSTAWARE E3).

## 4. Kill bars (frozen)

- K1 (S3): cold table -> all four score 1.0 -> DET-STRAT
  chosen=1 (id tie-break; hedge does NOT fire on the vacuous
  tie); S3 block byte-exact per Section 7. FAIL: chosen != 1
  (hedge fired without evidence, or tie-break broken).
- K2 (S5): **untried WHOLE earns the lead: DET-STRAT chosen=2**
  (1.0 > 2/3 strictly); WHOLE's lag-direct order verifies the
  lag-2 full oscillation in 1 DET-CMP; DET-HYP goal=820 lag=2
  p=2 q=0 mask=7; Q how=1 passes=4; S5 block byte-exact. THE
  HEADLINE BAR. FAIL: WHOLE does not lead (the rule is not
  optimistic) or does not win.
- K3 (S7): WHOLE leads (chosen=2, 1.0 > 2/3), fails (1 CMP:
  (2,0) eq=0); DET-SWITCH 2->3; NEED rescues at pass 3 (4
  NCMP, HYP lag=2 p=3 q=1 mask=7); Q how=1 passes=5; S7 block
  byte-exact. FAIL: PW leads, or rescue order differs.
- K4 (S8): **untried ALT leads (DET-STRAT chosen=4, 1.0
  strictly best)**; ALT's PW-form fails (2 CMP: (2,0)=0,
  (2,1)=0); NEED-form wins (4 NCMP, HYP lag=2 p=3 q=1 mask=7);
  Q how=1 passes=5; 6 logged comparison events (the
  over-exploration tax: 6 vs 4 for NEED-direct). S8 block
  byte-exact. FAIL: ALT does not lead.
- K5 (S9): PW leads (chosen=1; 2/3 id tie-break over WHOLE's
  2/3); fails (2 CMP); DET-SWITCH 1->2; WHOLE rescues via
  lag-direct order ((3,1) eq=0, (3,0) eq=1; 2 CMP) and WINS at
  lag 3; DET-HYP goal=821 lag=3 p=3 q=0 mask=7; DET-PRIOR
  set=3; Q how=1 passes=5; S9 block byte-exact. FAIL: NEED
  leads first (not optimistic), or WHOLE does not win.
- K6 (S10): WHOLE leads (chosen=2; 3/5 > 2/5 strictly);
  cascade WHOLE(1 CMP)->PW(3)->NEED(6)->ALT(9), all fail;
  19 logged comparison events; Q how=0 passes=9; AGREE id=S10
  a=1; S10 block byte-exact. FAIL: any false positive or wrong
  lead/order.
- K7 (S9B): **stored checker correctly REJECTS the misaligned
  snapshot: exactly one DET-APPLY line, match=1/3** (stored
  phases are S7's pass 1..2, fresh trajectory starts at pass
  0); then re-detection cascade WHOLE(chosen=2)->PW(SWITCH
  2->1, 3 CMP)->NEED(SWITCH 1->3, 8 NCMP across lag 3 and lag
  2); NEED wins (HYP lag=2 p=4 q=2 mask=7); DET-PRIOR set=2;
  Q how=1 passes=6; S9B block byte-exact. FAIL: APPLY
  succeeds (matching is q-insensitive) or cascade differs.
- K8 (S11): zeroed table -> DET-STRAT chosen=1; cascade
  PW(2 CMP)->WHOLE(2)->NEED(4 NCMP); NEED wins (HYP lag=2 p=4
  q=2 mask=7); Q how=1 passes=6; 8 logged events; S11 block
  byte-exact. FAIL: NEED leads despite zeroed table, or event
  order differs (prior=2, not costaware's 3).
- K9 (S12): **optimistic-tie lesion (PW[2,2,4] -> 3/5,
  NEED[5,5,9] -> 3/5, both tried; WHO/ALT[1,0,4] -> 1/5) ->
  hedge -> DET-STRAT chosen=4**; ALT's PW-form fails (2 CMP),
  NEED-form wins (4 NCMP, HYP lag=2 p=3 q=1 mask=7); Q how=1
  passes=5; S12 block byte-exact. FAIL: hedge does not fire
  (rule not on optimistic terms) or PW leads.
- K10 (S13): **lesioned PW[3,2,6] (3/7), NEED[2,0,8] (1/9),
  WHO/ALT untried (1.0) -> DET-STRAT chosen=2 (WHOLE leads
  outright)**; WHOLE fails at pass 2 (1 CMP: (2,0) eq=0, lag
  3 inapplicable); DET-SWITCH 2->4; ALT's PW-form wins at lag
  3 (3 CMP: (3,1)=0, (3,2)=0, (3,0)=1; HYP lag=3 p=3 q=0
  mask=7); DET-PRIOR set=3; Q how=1 passes=5; S13 block
  byte-exact. THE LEAD-IS-NOT-WIN BAR. FAIL: WHOLE does not
  lead, or PW leads, or NEED tried before ALT.
- K11 (S14): **controlled lesion (PW[3,2,6] -> 3/7,
  NEED[2,0,8] -> 1/9, ALT[1,0,4] -> 1/5, WHOLE untried) ->
  WHOLE is the STRICT argmax (1.0, not a tie-break) ->
  DET-STRAT chosen=2**; WHOLE verifies the fresh lag-2 full
  oscillation (goal 825) in 1 DET-CMP; DET-HYP goal=825 lag=2
  p=2 q=0 mask=7; DET-PRIOR set=2; Q how=1 passes=4; S14 block
  byte-exact. FAIL: WHOLE does not strictly lead or win.
- K12: 3/3 runs byte-identical stdout; stderr empty.
- K13: safebin active for every command; `which python3` and
  `which python` return nothing before and after; all
  computation pure Zag; single build with the pinned znc; new
  Zag scanned for the `while.*!(` negated-conjunction pattern:
  clean; `strat_sel` keeps the proven nesting shape (no
  function calls inside nested conditions; cross-multiplication
  on hoisted locals).
- K14: c12_learn.zag lines 1..1331 cmp-identical to
  c11_learn.zag lines 1..1331; c12_base.zag cmp-identical to
  c11_base.zag; the additive section differs from c11's in
  exactly `strat_sel` (verified by diff); zero world/goal/
  relation/need literals in the additive section and
  c12_main.zag outside the harness fns (goal constructors live
  in c12_world.zag, the allowed home).

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
DET-STRAT chosen=2
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
Q id=S7 goal=822 how=1 passes=5
DET-STRAT chosen=2
DET-PRIOR prior=2
DET-CMP p=2 a=2 b=0 eq=0
DET-SWITCH from=2 to=3
DET-NCMP p=3 need=0 lag=2 eq=1
DET-NCMP p=3 need=1 lag=2 eq=1
DET-NCMP p=3 need=2 lag=2 eq=1
DET-NCMP p=3 need=3 lag=2 eq=0
DET-HYP goal=822 lag=2 p=3 q=1 mask=7
DET-PRIOR set=2
OSC-CYCLE goal=822 lag=2 nph=2 ph0=[1,611][1,772][1,772][1,613] ph1=[1,611][1,771][1,771][1,614]
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
LSTATE-RET nrel=6 ids=601,602,606,613,615,604 cnts=16,16,0,3,0,8 prov=0,23,25,72 rev=7
SPEC-VFY rev=7 nrel=7 ep0=26 ep1=26 nfacts=72
LSTATE-VFY nrel=7 ids=601,602,603,608,614,616,605 cnts=16,16,16,0,0,0,8 prov=1,26,26,72 rev=7
Q id=S10 goal=816 how=0 passes=9
DET-STRAT chosen=2
DET-PRIOR prior=3
DET-CMP p=2 a=2 b=0 eq=0
DET-SWITCH from=2 to=1
DET-CMP p=3 a=3 b=0 eq=0
DET-CMP p=3 a=3 b=2 eq=0
DET-CMP p=3 a=3 b=1 eq=0
DET-SWITCH from=1 to=3
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
Q id=S9B goal=822 how=1 passes=6
DET-APPLY goal=822 pass=0 match=1/3
DET-STRAT chosen=2
DET-PRIOR prior=3
DET-CMP p=2 a=2 b=0 eq=0
DET-SWITCH from=2 to=1
DET-CMP p=3 a=3 b=0 eq=0
DET-CMP p=3 a=3 b=2 eq=0
DET-CMP p=3 a=3 b=1 eq=0
DET-SWITCH from=1 to=3
DET-NCMP p=4 need=0 lag=3 eq=1
DET-NCMP p=4 need=1 lag=3 eq=0
DET-NCMP p=4 need=2 lag=3 eq=0
DET-NCMP p=4 need=3 lag=3 eq=0
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
STAGE S11 STRAT-LESION
Q id=S11 goal=823 how=1 passes=6
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
SUMMARY-DET agree=1 plans_built=8 plans_loaded=4 trials=6 declines=0 prior=2 strat_pw=3,2,6 strat_who=1,1,1 strat_need=2,0,8 strat_alt=1,0,4
```
