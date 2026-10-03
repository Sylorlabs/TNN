# PREREG: COGOPS-STRATEGY (learner-chosen detection strategy)

Date: 2026-10-03. Worker: COGOPS-STRATEGY.
Lane: `docs/lab/research-lead/overnight-20260928/cogops_strategy/`
Status: FROZEN on commit (this file + NAMECHECK.md committed alone
before any implementation file exists). No amendments after
implementation begins.

Non-ledger task (claim minting paused). Directly addresses
overnight priority 5 (learner-created cognitive-operation bodies).

## 1. Research question

COGOPS-DETECTION (BUILD-PASS, K1..K11) showed the learner assembles
an oscillation detection procedure INSTANCE from a generic
pairwise comparison primitive: which pairs, which hypothesis,
which checker, driven by a learner-state lag prior with lesion
evidence (S5(1) < S10(2) < S11(3) comparisons). Its honest boundary
states what it did NOT claim: the learner does not choose among
different detection STRATEGIES. The pairwise-comparison strategy,
the prior-then-recency proposal form, and the hypothesis/confirm
rules remain researcher-provided.

This worker asks the follow-up question from that report: can the
learner CHOOSE the detection strategy from its own verification
history? The prior mechanism is the substrate; the new rung is a
learner-state strategy table (per-strategy uses, wins, cost) that
drives which of four genuinely different detection forms runs
first on a new goal, and which form rescues the episode when the
first fails.

## 2. Design

### 2.1 What is generic machinery (researcher-provided, domain-blind)

- Per-pass trajectory recording (`traj_log`), the single-pair
  whole-state comparator (`traj_state_eq`), the per-need comparator
  (`traj_need_eq`), single-step plan execution (`exec_step_iter`),
  the outcome-record store (`outc_store`), the stored-phase
  comparator (`outc_phase_eq`), the frozen plan table
  (`plan_find`/`plan_new`, 4 slots) with the frozen generic
  `plan_drop`, and the learner-owned spec versions. All frozen.
- The DET event ring (Section 2.4): an observation channel.
- The lag prior (DETC 15900): the COGOPS-DETECTION substrate,
  preserved unchanged. Every strategy form consults it.

### 2.2 The four strategy forms (researcher-provided forms)

Strategy ids: 1=PW (pairwise), 2=WHOLE (whole-state lag sweep),
3=NEED (per-need subset), 4=ALT (alternation).

- PW (pairwise): exactly the COGOPS-DETECTION proposal form.
  Prior pair first (prior lag, skip logged as DET-CMP eq=-1 if
  inapplicable), then recency pairs (pass,pass-1..3) with duplicate
  suppression. Each proposal is one `traj_state_eq`. A hit at
  distance d forms a lag-d hypothesis; own confirm pass; on
  verification stores the checker and sets the lag prior.
- WHOLE (whole-state lag sweep): proposes LAGS directly, one
  `traj_state_eq(pass,pass-d)` per lag, order [prior lag, 2, 3]
  with duplicate suppression (lag 1 never proposed: a fixpoint is
  not an oscillation). First hit forms the hypothesis; same
  confirm/store protocol as PW. Capability-identical to PW per
  pass (same comparisons available); differs in proposal ORDER
  (lag-direct vs recency-pair) and cost.
- NEED (per-need subset): for each lag d in [prior, 2, 3]
  (dup-suppressed, lag 1 skipped): compares EACH need with
  `traj_need_eq(pass,pass-d,ni)` (one DET-NCMP event per need),
  forming the match set M(d). Hypothesis rule: M(d) non-empty
  AND at least one need in M(d) is non-trivial, i.e.
  `traj_need_eq(pass,pass-1,ni)==0` for some ni in M(d) (the
  non-triviality guard; the carrier need alone can never form a
  hypothesis). Confirm: the same subset M(d) must match at
  (pass+1,pass+1-d). On verification stores the checker WITH the
  subset mask (new learner-state: mask per outcome entry) and
  sets the lag prior. This form detects partial oscillation
  (a strict subset of needs cycling) where whole-state forms
  cannot hit.
- ALT (alternation): a 2-pass turn. First pass: PW-form proposals.
  Second pass: NEED-form proposals. The alternation of the two
  capability-distinct forms within one strategy turn.

Turn budget (researcher-provided): PW, WHOLE, NEED each get ONE
pass per turn; ALT gets TWO passes (alternation is undefined in a
single pass). If a turn produces no verified hypothesis, the
strategy records a fail for the episode and the learner switches
to the next-best untried strategy.

### 2.3 The selection machinery

Researcher-provided:
- The strategy table: per strategy [uses, wins, cost], in learner
  state (STRATT region). Cost = logged comparison events
  (DET-CMP + DET-NCMP) during the strategy's turns.
- Initial selection: argmax of win-rate wins/uses over untried
  strategies (untried = rate 0). Tie-break: lower strategy id.
  Cold start (all zero): PW (id 1), the COGOPS-DETECTION substrate.
- Within-episode switching: after a strategy's turn fails, select
  the best by the same rule among strategies not yet tried this
  episode. A DET-SWITCH event records from/to.
- Hedge rule: at initial selection only, if the tied-best rate
  (>0) is shared by strategies including BOTH 1 (PW) and 3 (NEED)
  (the two capability-distinct forms), select ALT (4) instead of
  breaking the tie by id. The hedge takes precedence over the id
  tie-break.

Learner-driven (from experience):
- Every table VALUE (uses, wins, cost) is written only from the
  learner's own detection episodes: a win is a verified hypothesis
  on the current trajectory; a fail is an exhausted turn; cost is
  the comparisons the learner actually made. No researcher-written
  dispatch table, no per-goal routing.
- Hence WHICH strategy runs first on a new goal, and the rescue
  order after a failure, are consequences of the learner's
  verification history meeting the current trajectory.

### 2.4 The DET event ring (extended)

DETC region: 15900 lag prior, 15904 retracted lag, 15908 ntev,
15912 + tev*20 event ring, tev < 32 (extended from 16; L is
allocated 32768 bytes in c10_main). STRATT region at 16600:
4 strategies x [uses,wins,cost] (12 words); 16648 last chosen;
16650 turn-cost accumulator; 16656 outcome masks (3 words).

Event kinds: 0=CMP (p,x=a,y=b,z=eq; z=-1 prior-pair skip),
1=HYP (p=pass,x=lag,y=q,z=mask), 3=PRIOR (x=prior at start),
4=SET (x=prior after verification), 5=APPLY (p,x=matched,y=masked
total), 6=RETRACT, 7=NCMP (p=pass,x=need,y=lag,z=eq),
8=STRAT (x=chosen id), 9=SWITCH (x=from,y=to).

Dump formats:
`DET-CMP p=2 a=2 b=1 eq=0`
`DET-NCMP p=4 need=0 lag=2 eq=1`
`DET-HYP goal=822 lag=2 p=4 q=2 mask=7`
`DET-PRIOR prior=2` / `DET-PRIOR set=2`
`DET-APPLY goal=822 pass=0 match=3/3`
`DET-STRAT chosen=1`
`DET-SWITCH from=1 to=2`
`OSC-STATE goal=822 lag=2 nph=2 src=0 mask=7` (mask appended)

### 2.5 World F and goals 822/823 (partial oscillation)

World F = world A + rel 613/614 (2-cycle 771<->772, 5 facts, as in
world E) + rel 604/605 (convergent chain 611->...->618, 16 facts,
as in world C). 77 facts total.

Goal 822 F0 (partial oscillation, world F):
need0 P=(601,621) -> [611] (carrier, constant);
need1 P=(613,770) with kind-1 SELF-link: oscillates 771<->772;
need2 T=(S,614,770) via kind-2 fan-out from need1: VERIFY each
visited subject (record [1,subject], oscillates with need1);
need3 P=(604,611) with kind-1 SELF-link: walks 612,613,...,618
(convergent drifter; its output never repeats within the episode).
Whole-state `traj_state_eq` can never hit (need3 drifts); NEED
detects the cycling subset {need0,need1,need2} at lag 2.

Goal 823 F1: same structure, fresh goal tag 823 (tests strategy
transfer across goals, not outcome reuse).

### 2.6 The honest boundary (what this does NOT claim)

- The strategy FORMS are researcher-provided: the four proposal
  orders, the hypothesis rules (including NEED's non-triviality
  guard), the confirm protocol, the turn budget, the selection
  rule (win-rate argmax, id tie-break, PW+NEED tie hedge), and
  the cold default (PW). The learner does not invent a strategy
  form and does not invent the concept of strategy choice.
- What the learner chooses, from its own verification history,
  is WHICH form runs first and the rescue order: the table values
  are learner-state, and the lesion/corrupt bars test that the
  table causally drives the choice.
- Not claimed: L3 representational invention (no new primitive,
  no new representational form; the 12-criterion bar is not
  claimed); per-context strategy selection (the table is global;
  cost-aware selection is future work); optimality of the choice.
- WHOLE note (pre-registered): WHOLE is capability-identical to
  PW per pass (its lag-direct comparisons are a subset of PW's
  recency-pair proposals); it differs in order and cost. If the
  battery shows WHOLE tried but never winning, that is reported
  as-is; cost-aware selection that could prefer WHOLE is explicit
  future work, not claimed here.
- Red-team note (pre-registered): the attack "strat_sel is a
  researcher-written dispatch; the learner chooses nothing" is
  answered by S11/S12: zeroing the table changes the first
  choice to the cold default with a measurable cost cascade,
  and a lesioned tie changes the choice to the hedge form.
  A fixed dispatch cannot respond to table lesions.

## 3. Battery stages

- S1A RET-LEARN (world A), S1B VFY-LEARN (world A): verbatim
  COGOPS-DETECTION substrate learning.
- S2 OSC-LEARN-D (world D): verbatim.
- S3 STRAT-D0 (goal 818, world D): cold table, default PW,
  invention as in COGOPS-DETECTION S3.
- S4 OSC-LEARN-E (world E): verbatim.
- S5 STRAT-E0 (goal 820, world E): PW leads (sole winner),
  lag prior accelerates (1 comparison).
- S6L CYCLE-LEARN-C (world C): verbatim COGOPS-DETECTION S7.
- S6B WORLD-F-SETUP: setup_worldF; re-specialize (ep 13-20,
  21-22). Coverage is world-driven: world F's facts refresh the
  613/614 and 604/605 relations in one pass.
- S7 STRAT-F0 (goal 822, world F, partial): PW leads, fails;
  WHOLE fails; NEED wins with subset mask 7. Capability +
  switching bar.
- S8 STRAT-F1 (goal 823, world F, partial, fresh tag): NEED
  leads FIRST (win-rate 1.0 from S7) and wins directly.
  THE STRATEGY-TRANSFER BAR (analog of COGOPS-DETECTION K2).
- S9 STRAT-E1 (goal 821, world E, period-3): setup_worldE,
  re-specialize E, plan_drop(818) via the frozen generic
  (tag saved from the goal record at S3, not a literal).
  NEED leads, fails (lag 3 inapplicable at pass 2, lag 2
  trivially rejected); PW rescues via recency reaching lag 3.
- S10 CONV-816 (goal 816, world C): setup_worldC, re-specialize
  C, plan_drop(820) (tag saved at S5). All four strategies fail;
  generic fallback; oracle agreement. Control bar.
- S9B REUSE-822 (goal 822, world F again): setup_worldF,
  re-specialize (ep 13-20, 21-22). Stored partial checker APPLIES with
  mask 7 (DET-APPLY match=3/3 over masked needs). Partial-reuse
  bar.
- S11 STRAT-LESION (goal 823, world F): tombstone 823's outcome
  (no-op: already evicted), ZERO the strategy table. Cold
  default PW leads; full cascade PW->WHOLE->NEED; NEED wins.
  Causal lesion bar: the table drives the choice.
- S12 STRAT-CORRUPT (goal 823, world F): tombstone 823's
  outcome, lesioned table PW[2,2,4] + NEED[2,2,8] (tied 1.0).
  Hedge rule selects ALT; ALT detects via its NEED-form pass.
  Hedge + corrupt-cost bar.

Plan slots (4, frozen): 818->0, 820->1, 822->2, 823->3,
821 evicts 818 (plan_drop), 816 evicts 820 (plan_drop).
plans_built=6, plans_loaded=3 (S9B:822, S11:823, S12:823).

## 4. Kill bars (frozen)

- K1 (S3): cold table selects PW (DET-STRAT chosen=1); S3 block
  byte-exact per Section 7 (PRIOR 0, 2 CMP, HYP lag=2 mask=7,
  SET 2, Q how=1 passes=4, CYCLE, CONFIRM, SPECCHK, STATE mask=7).
  FAIL: default is not PW, or PW-form broken.
- K2 (S5): PW leads as sole winner; prior pair hits first
  (exactly 1 DET-CMP); S5 block byte-exact. FAIL: selection
  does not prefer the experienced winner.
- K3 (S7): PW fails (2 CMP), DET-SWITCH 1->2, WHOLE fails
  (2 CMP), DET-SWITCH 2->3, NEED wins (4 DET-NCMP, HYP mask=7);
  S7 block byte-exact; Q how=1 passes=6. FAIL: no switching,
  NEED misses the partial oscillation, or a whole-state form
  falsely hits.
- K4 (S8): NEED is chosen FIRST (DET-STRAT chosen=3) from S7's
  experience; 4 DET-NCMP then HYP (vs S7's 8 comparisons before
  NEED ran); S8 block byte-exact; Q how=1 passes=4. FAIL:
  PW leads (table ignored) or NEED does not lead.
- K5 (S9): NEED leads then fails (lag-2 trivial reject, lag-3
  inapplicable: 3 DET-NCMP, no HYP); DET-SWITCH 3->1; PW wins
  at pass 3 via (3,0) hit (3 DET-CMP, HYP lag=3 q=0);
  DET-PRIOR set=3; S9 block byte-exact; Q how=1 passes=5.
  FAIL: NEED falsely wins, or PW does not rescue.
- K6 (S10): all four strategies fail (NEED 3 NCMP, SWITCH 3->1,
  PW 3 CMP, SWITCH 1->2, WHOLE 2 CMP, SWITCH 2->4, ALT 3 CMP +
  6 NCMP); Q how=0 passes=9; AGREE id=S10 a=1; S10 block
  byte-exact. FAIL: any false positive.
- K7 (S9B): stored partial checker applies: 2 DET-APPLY
  match=3/3 (masked needs only); OSC-CYCLE src=1 byte-identical
  to S7's; OSC-REUSE match=2; OSC-STATE src=1 mask=7; S9B block
  byte-exact. FAIL: mask-aware APPLY broken.
- K8 (S11): zeroed table -> DET-STRAT chosen=1 (cold default);
  cascade PW (skip + 2 CMP) -> SWITCH 1->2 -> WHOLE (2 CMP) ->
  SWITCH 2->3 -> NEED (8 NCMP, HYP mask=7); total 15 logged
  comparisons > S8's 7; S11 block byte-exact; Q how=1 passes=6.
  FAIL: NEED leads despite zeroed table (choice not table-driven).
- K9 (S12): lesioned PW/NEED tie -> DET-STRAT chosen=4 (hedge,
  not id tie-break); ALT's PW-form fails (2 CMP), NEED-form wins
  (4 NCMP, HYP lag=2 q=1 mask=7); 9 logged comparisons > S8's 7;
  S12 block byte-exact; Q how=1 passes=5. FAIL: PW or NEED leads
  (hedge broken) or ALT fails.
- K10: 3/3 runs byte-identical stdout; stderr empty.
- K11: safebin active for every command; `which python3` and
  `which python` return nothing before and after; all computation
  pure Zag; single build with the pinned znc
  (src/tools/toolchain/znc_linux_x86_64_abed8aa1); new Zag
  scanned for the `while.*!(` negated-conjunction pattern: clean;
  if-nesting at 3 or fewer with hoisted flags.
- K12: c10_learn.zag prefix (lines 1..1331) cmp-identical to
  c9_learn.zag lines 1..1331; c10_base.zag cmp-identical to
  c9_base.zag; zero `osc_review` call sites in the additive
  section and c10_main.zag; zero world literals, goal tags, or
  need tags in the additive section (comments included).

## 5. Section 7: exact predicted stdout (frozen)

The full predicted stdout follows. Every line is predicted;
the binary must match byte for byte (K1..K9, K10).

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
Q id=S8 goal=823 how=1 passes=4
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
STAGE S9 STRAT-E1
SPEC-RET rev=6 nrel=6 ep0=13 ep1=20 nfacts=68
LSTATE-RET nrel=6 ids=601,602,606,613,615,604 cnts=16,16,0,3,4,0 prov=0,13,20,68 rev=6
SPEC-VFY rev=6 nrel=7 ep0=21 ep1=22 nfacts=68
LSTATE-VFY nrel=7 ids=601,602,603,608,614,616,605 cnts=16,16,16,0,2,3,0 prov=1,21,22,68 rev=6
Q id=S9 goal=821 how=1 passes=5
DET-STRAT chosen=3
DET-PRIOR prior=2
DET-NCMP p=2 need=0 lag=2 eq=1
DET-NCMP p=2 need=1 lag=2 eq=0
DET-NCMP p=2 need=2 lag=2 eq=0
DET-SWITCH from=3 to=1
DET-CMP p=3 a=3 b=1 eq=0
DET-CMP p=3 a=3 b=2 eq=0
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
DET-STRAT chosen=3
DET-PRIOR prior=3
DET-NCMP p=2 need=0 lag=2 eq=1
DET-NCMP p=2 need=1 lag=2 eq=0
DET-NCMP p=2 need=2 lag=2 eq=0
DET-SWITCH from=3 to=1
DET-CMP p=3 a=3 b=0 eq=0
DET-CMP p=3 a=3 b=2 eq=0
DET-CMP p=3 a=3 b=1 eq=0
DET-SWITCH from=1 to=2
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
SUMMARY-DET agree=1 plans_built=6 plans_loaded=3 trials=6 declines=0 prior=2 strat_pw=2,2,4 strat_who=0,0,0 strat_need=2,2,8 strat_alt=1,1,6
```
