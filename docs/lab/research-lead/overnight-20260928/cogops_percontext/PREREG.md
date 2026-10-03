# PREREG: COGOPS-PERCONTEXT (per-context strategy tables)

Date: 2026-10-03. Worker: COGOPS-PERCONTEXT.
Lane: `docs/lab/research-lead/overnight-20260928/cogops_percontext/`
Status: FROZEN on commit (this file + NAMECHECK.md committed alone
before any implementation file exists). No amendments after
implementation begins.

Non-ledger task (claim minting paused). Implements COGOPS-OPTIMISTIC
follow-up #1 (which is COGOPS-COSTAWARE follow-up #2):
"Per-context strategy tables: S9B shows optimism's largest cost
flows through the global table's stored evidence; context-scoped
tables would localize both the promotion and its side effects."

## 1. Research question

COGOPS-COSTAWARE established that the global strategy table makes
"cost-aware" selection cost MORE this episode: efficiency rewards
historically cheap wins, so the historically-cheap PW is tried
first on goals where its form is structurally wrong (S8: 6 vs 4,
S9: 8 vs 6), adding its failure cost. COGOPS-OPTIMISTIC then
showed optimism's largest cost is second-order: the optimistic S7
hypothesizes at q=1 where costaware hypothesized at q=2, so the
stored phase snapshot misaligns and S9B pays 13 events for
re-detection instead of 2 for outcome reuse.

Both costs flow through table scope. The global table lets
foreign-context history buy the lead (S8/S9) and lets the
optimistic promotion change the learner's own stored training
data (S9B). This worker replaces the one global table with
per-context tables and asks:

(1) What defines a "context"? The context must be
learner-computed from runtime observations, not a
researcher-supplied label: no world/goal literals in the
additive section (K14 governance). The chosen signature is
`(nneeds, need_f(G,1,0))`: the goal's need count and the
relation field of need 1 (the oscillator P-need's relation, read
from the goal record at a structural position). In this battery
it partitions the 8 goals into 5 contexts: (3,606)={818},
(3,613)={820,825}, (3,615)={821,824}, (4,613)={822,823},
(3,604)={816}. Goals probing the same relation with the same
need count share strategy history; everything else starts cold.

(2) Does per-context fix the S8/S9 cost inflation? (3) Does it
restore the S9B outcome reuse that global optimism broke?
(4) What does per-context cost: does the optimistic promotion
survive within a context, and what happens on a fresh context?

## 2. Design

### 2.1 Context slots (learner-owned, fixed pool)

CTXT region at 17000: 8 slots x 56 bytes. Slot layout (14 i32):
[sig_nn, sig_rel, pw_u, pw_w, pw_c, who_u, who_w, who_c,
need_u, need_w, need_c, alt_u, alt_w, alt_c].
Slot base = 17000 + slot*56. A slot with sig_nn==0 is free.
`ctx_slot_for(L,nn,rel)`: linear scan for a matching slot;
else claim the first free slot and zero its 12 table cells;
else (pool full, unreachable in this battery: 5 contexts, 8
slots) fall back to slot 0. `ctx_of_goal(L,G)` computes
(nn, need_f(G,1,0)) (rel=0 if nn<2, unreachable) and returns
the slot. Allocation order in the battery is deterministic:
S3->slot0 (3,606), S5->slot1 (3,613), S7->slot2 (4,613),
S9->slot3 (3,615), S10->slot4 (3,604); S8/S9B/S11/S12 reuse
slot2, S13 reuses slot3, S14 reuses slot1.

### 2.2 Selection and recording through the slot

`strat_sel(L,tried,slot)` and `cx_rec(L,slot,s,win,cost)` are
the COGOPS-OPTIMISTIC versions with the table base replaced by
the slot base. The rule is unchanged: optimistic efficiency
(w+1)/(c+1) by exact integer cross-multiplication, lower-id
tie-break, same rescue rule, same evidence-gated hedge (now on
the context's table: c1>0 and c3>0 in this context). The
`tried` bitmask stays episode-global (a strategy failed this
episode is not retried this episode, regardless of context).
`det_handle` computes `slot=ctx_of_goal(L,G)` once and threads
it through both `strat_sel` calls and both `cx_rec` calls. The
outcome masks (16656+e*4) stay per-outcome-entry (already
per-goal); the turn-cost accumulator (16650) and last-chosen
(16648) stay global; the lag prior (15900) stays global.

### 2.3 Lesions target the current context's slot

The harness lesion fns (`strat_zero_ctx`,
`strat_lesion_s12/13/14`) take the slot and zero/rewrite only
that slot's 12 table cells. The driver computes the slot via
`ctx_of_goal(L,G)` before each lesion. This is the honest
analog of the global lesions: the lesion sets the table state
that governs this goal's selection, and only that state.

### 2.4 Preregistered structural predictions

P1 (fresh context is cold). A context never seen before has an
all-zero table: all four strategies score 1.0, the
evidence-gated hedge cannot fire, PW leads by id. S5 (goal 820,
context (3,613), first seen): DET-STRAT chosen=1, NOT 2. The
COGOPS-OPTIMISTIC headline ("untried WHOLE earns the lead")
does NOT reproduce on a fresh context: the promotion is
context-local. Same for S7 (goal 822, context (4,613)):
chosen=1.

P2 (within-context promotion survives). S8 (goal 823, context
(4,613), S7 history in-context: PW[1,0,2], WHOLE[1,0,2],
NEED[1,1,4], ALT untried): untried ALT scores 1.0, strictly
best (2/5, 1/3), and leads (chosen=4). Optimism's promotion
works exactly as before within one context.

P3 (S9B reuse restored). c13's S7 is PW-led (P1), so NEED wins
with HYP lag=2 p=4 q=2 (as under COGOPS-COSTAWARE), storing
trajectory passes 2,3. A fresh trajectory's passes 0,1 have the
same parity on the masked needs, so S9B's mask-aware APPLY
succeeds at match=3/3 and the learner reuses the outcome (2
events), instead of paying 13 for re-detection. Per-context
fixes optimism's largest cost.

P4 (S9 cold-context cascade). S9 (goal 821, context (3,615),
first seen): PW leads, fails (2 CMP); rescue among
context-untried strategies goes by id to WHOLE (2), which wins
at lag 3 (2 CMP). Byte-identical to COGOPS-OPTIMISTIC's S9,
by a different route (cold id-order instead of the 2/3 tie).

P5 (S10 novel cascade). S10 (goal 816, context (3,604), first
seen): PW leads (chosen=1); rescue among untried goes by id:
WHOLE (2), then NEED (3), then ALT (4); all fail; 19 comparison
events; generic fallback; AGREE=1. This cascade order
(PW->WHOLE->NEED->ALT) matches NEITHER predecessor
(costaware: PW->NEED->WHOLE->ALT by efficiency; optimistic:
WHOLE-led). It is the unique signature of cold-context
optimistic rescue.

P6 (lesions behave per-context). S12's optimistic-tie lesion in
context (4,613) hedges to ALT exactly as under global
optimism; S13's lesion in context (3,615) gives WHOLE the
outright 1.0 lead; S14's lesion in context (3,613) gives WHOLE
the strict argmax. The lesion bars are context-scoped but
otherwise unchanged.

P7 (prior continuity). The lag prior stays global: c13's S9
sets prior=3 (WHOLE wins at lag 3), S9B's APPLY success leaves
it at 3, so S11 runs with prior=3 (as under COGOPS-COSTAWARE,
not prior=2 as under global optimism). The S11 cascade is
byte-identical to COGOPS-COSTAWARE's S11.

P8 (no cross-context contamination). Final tables: context
(3,613) never sees NEED's S7 win; context (4,613) never sees
PW's S5 win; context (3,615) starts cold at S9 despite S5's PW
win in (3,613). The CTX dump shows five independent histories.

## 3. What changes vs COGOPS-OPTIMISTIC (and what does not)

CHANGED:
- (a) Additive section: the global STRATT table (16600) is
  replaced by the CTXT pool (17000, 8 slots x 56 bytes); new
  fns `ctx_slot_for`, `ctx_of_goal`, `cx_uses/cx_wins/cx_cost`,
  `cx_rec`; `strat_sel` takes a slot; `det_handle` computes the
  slot from G and threads it through selection and recording.
  Every other additive function is untouched.
- (b) Driver: lesion fns take a slot (`strat_zero_ctx`,
  `strat_lesion_s12/13/14` rewrite only that slot's table);
  driver computes the slot via `ctx_of_goal(L,G)`; the summary
  dump is replaced by the per-context CTX dump (format
  preregistered in Section 7). Stage comments updated. Nothing
  else.

UNCHANGED: the optimistic selection rule itself
((w+1)/(c+1), exact cross-multiplication, id tie-break,
evidence-gated hedge, episode-global tried mask); the four
strategy forms; hypothesis/confirm rules; turn budget; the DET
event ring and dump formats; worlds A/C/D/E/F; all goals and
goal constructors (no new goals); all learning stages S1A..S6B
(selection-independent; byte-identical); the lag prior
substrate (global); c13_base.zag (= c12_base.zag);
c13_world.zag (= c12_world.zag); the c12_learn prefix (lines
1..1331, cmp-identical).

## 4. The honest boundary (what this does NOT claim)

- The context SIGNATURE SHAPE (nneeds + need-1 relation field)
  is researcher-chosen; only the slot ALLOCATION and the table
  VALUES are learner-written. Whether (nneeds, rel) is the right
  granularity is explicitly probed, not assumed: P1/P5 show its
  price (cold starts), P2/P3 show its payoff (local promotion,
  restored reuse).
- Not claimed: learner-invented contexts (the learner does not
  choose what defines a context, only fills tables per
  context); optimality of the signature; L3 representational
  invention; that per-context is net-beneficial in general (in
  this battery: S9B fixed 13->2, S5/S7 pay cold-start, S8/S9
  event counts unchanged vs global optimism).
- The "does per-context fix S8/S9?" answer is mechanism-level:
  under the optimistic base, S8/S9 keep their event counts (6
  and 4); what per-context fixes is the S9B second-order blowup
  and the cross-context cheapness leak (PW's (3,613) wins no
  longer buy leads in (4,613) or (3,615)). The costaware-base
  variant (per-context + pure efficiency) is explicit future
  work, not implemented here.

## 5. Battery stages

S1A RET-LEARN (world A), S1B VFY-LEARN (world A), S2
OSC-LEARN-D (world D), S3 STRAT-D0 (goal 818, context
(3,606) cold: PW default), S4 OSC-LEARN-E (world E), S5
STRAT-E0 (goal 820, context (3,613) cold: PW leads, wins in 1
CMP; the promotion-localization bar), S6L CYCLE-LEARN-C
(world C), S6B WORLD-F-SETUP, S7 STRAT-F0 (goal 822, context
(4,613) cold: PW leads, fails, WHOLE fails, NEED wins), S8
STRAT-F1 (goal 823, context (4,613): untried ALT leads,
6-event tax, ALT wins via NEED-form), S9 STRAT-E1 (goal 821,
context (3,615) cold: PW leads, fails, WHOLE rescues and wins
at lag 3), S10 CONV-816 (goal 816, context (3,604) cold: PW
leads, novel cascade PW->WHOLE->NEED->ALT, all fail, fallback,
AGREE=1), S9B REUSE-822 (goal 822, context (4,613): APPLY
succeeds 3/3, outcome reuse, the restoration bar), S11
STRAT-LESION (goal 823, zeroed context: PW default cascade,
prior=3), S12 STRAT-CORRUPT (goal 823, optimistic-tie lesion
in context: hedge selects ALT), S13 WHOLE-LEAD (goal 824,
context (3,615) lesioned: WHOLE leads outright, fails, ALT
rescues at lag 3), S14 WHOLE-STRICT (goal 825, context
(3,613) lesioned: WHOLE strict argmax, leads and wins in 1
CMP).

Plan slots: 818->0, 820->1, 822->2, 823->3; 821 evicts 818;
816 evicts 820; 824 evicts 821; 825 evicts 824.
plans_built=8, plans_loaded=4 (S9B, S11, S12 via det_handle
pre>=0; S10 via compose_iter on the fallback path).
Context slots: S3->0 (3,606), S5->1 (3,613), S7->2 (4,613),
S9->3 (3,615), S10->4 (3,604); S8/S9B/S11/S12 reuse slot 2,
S13 reuses slot 3, S14 reuses slot 1.

## 6. Kill bars (frozen)

- K1 (S3): context (3,606) cold -> DET-STRAT chosen=1; S3 block
  byte-exact per Section 7 (identical to COGOPS-OPTIMISTIC S3).
  FAIL: chosen != 1.
- K2 (S5): **context (3,613) cold -> DET-STRAT chosen=1 (PW by
  id tie-break), NOT 2**; PW's prior-pair verifies the lag-2
  full oscillation in 1 DET-CMP; DET-HYP goal=820 lag=2 p=2 q=0
  mask=7; Q how=1 passes=4; S5 block byte-exact per Section 7
  (identical to COGOPS-COSTAWARE S5). THE LOCALIZATION BAR:
  the optimistic promotion does not cross contexts. FAIL:
  chosen=2 (global-table behavior leaked).
- K3 (S7): context (4,613) cold -> chosen=1; PW fails (2 CMP);
  DET-SWITCH 1->2; WHOLE fails (2 CMP); DET-SWITCH 2->3; NEED
  wins (4 NCMP, HYP lag=2 p=4 q=2 mask=7); Q how=1 passes=6; S7
  block byte-exact per Section 7 (identical to COGOPS-COSTAWARE
  S7). FAIL: WHOLE leads (chosen=2).
- K4 (S8): context (4,613) carries S7: PW[1,0,2] (1/3),
  WHOLE[1,0,2] (1/3), NEED[1,1,4] (2/5), ALT untried (1.0) ->
  **DET-STRAT chosen=4 (strict)**; ALT's PW-form fails (2 CMP);
  NEED-form wins (4 NCMP, HYP lag=2 p=3 q=1 mask=7); Q how=1
  passes=5; 6 logged comparison events; S8 block byte-exact
  per Section 7 (identical to COGOPS-OPTIMISTIC S8). FAIL: ALT
  does not lead (within-context promotion broken).
- K5 (S9): context (3,615) cold -> chosen=1; PW fails (2 CMP);
  DET-SWITCH 1->2; WHOLE rescues via lag-direct order ((3,1)
  eq=0, (3,0) eq=1; 2 CMP) and WINS at lag 3; DET-HYP goal=821
  lag=3 p=3 q=0 mask=7; DET-PRIOR set=3; Q how=1 passes=5; S9
  block byte-exact per Section 7 (identical to
  COGOPS-OPTIMISTIC S9, via cold id-order rescue). FAIL: NEED
  rescues before WHOLE, or WHOLE does not win.
- K6 (S10): context (3,604) cold -> **DET-STRAT chosen=1**;
  cascade PW (skip + 2 CMP) -> DET-SWITCH 1->2 -> WHOLE (2 CMP)
  -> DET-SWITCH 2->3 -> NEED (6 NCMP) -> DET-SWITCH 3->4 ->
  ALT (3 CMP + 6 NCMP); all fail; 19 logged comparison events;
  Q how=0 passes=9; AGREE id=S10 a=1; S10 block byte-exact per
  Section 7. THE NOVEL-CASCADE BAR: matches neither
  predecessor's order. FAIL: chosen=2 (optimistic global), or
  SWITCH 1->3 (costaware efficiency rescue).
- K7 (S9B): **stored checker SUCCEEDS: exactly two DET-APPLY
  lines, match=3/3 both**; Q how=2 passes=2; OSC-REUSE;
  OSC-CYCLE = S7's phases; S9B block byte-exact per Section 7
  (identical to COGOPS-COSTAWARE S9B). THE RESTORATION BAR:
  per-context restores the outcome reuse that global optimism
  broke (13 events -> 2). FAIL: APPLY rejects (match=1/3).
- K8 (S11): zeroed context (4,613) -> DET-STRAT chosen=1;
  DET-PRIOR prior=3 (global prior continuity, P7); cascade
  PW (skip + 2 CMP) -> WHOLE (2 CMP) -> NEED (8 NCMP); NEED
  wins (HYP lag=2 p=4 q=2 mask=7); Q how=1 passes=6; S11 block
  byte-exact per Section 7 (identical to COGOPS-COSTAWARE S11).
  FAIL: prior=2, or cascade differs.
- K9 (S12): context lesion (PW[2,2,4] -> 3/5, NEED[5,5,9] ->
  3/5, both tried; WHO/ALT[1,0,4] -> 1/5) -> hedge ->
  DET-STRAT chosen=4; ALT's PW-form fails (2 CMP), NEED-form
  wins (4 NCMP, HYP lag=2 p=3 q=1 mask=7); Q how=1 passes=5;
  S12 block byte-exact per Section 7 (identical to
  COGOPS-OPTIMISTIC S12). FAIL: hedge does not fire.
- K10 (S13): context lesion (PW[3,2,6] -> 3/7, NEED[2,0,8] ->
  1/9, WHO/ALT untried -> 1.0) -> **DET-STRAT chosen=2 (WHOLE
  leads outright)**; WHOLE fails at pass 2 (1 CMP); DET-SWITCH
  2->4; ALT's PW-form wins at lag 3 (3 CMP, HYP lag=3 p=3 q=0
  mask=7); DET-PRIOR set=3; Q how=1 passes=5; S13 block
  byte-exact per Section 7 (identical to COGOPS-OPTIMISTIC
  S13). FAIL: WHOLE does not lead.
- K11 (S14): context lesion (PW[3,2,6] -> 3/7, NEED[2,0,8] ->
  1/9, ALT[1,0,4] -> 1/5, WHOLE untried) -> **WHOLE is the
  STRICT argmax (1.0) -> DET-STRAT chosen=2**; WHOLE verifies
  goal 825 in 1 DET-CMP; DET-HYP goal=825 lag=2 p=2 q=0 mask=7;
  DET-PRIOR set=2; Q how=1 passes=4; S14 block byte-exact per
  Section 7 (identical to COGOPS-OPTIMISTIC S14). FAIL: WHOLE
  does not strictly lead or win.
- K12: 3/3 runs byte-identical stdout; stderr empty.
- K13: safebin active for every command; `which python3` and
  `which python` return nothing before and after; all
  computation pure Zag; single build with the pinned znc; new
  Zag scanned for the `while.*!(` negated-conjunction pattern:
  clean; `strat_sel` keeps the proven nesting shape (no
  function calls inside nested conditions; cross-multiplication
  on hoisted locals; only the table base address changes).
- K14: c13_learn.zag lines 1..1331 cmp-identical to
  c12_learn.zag lines 1..1331; c13_base.zag cmp-identical to
  c12_base.zag; c13_world.zag cmp-identical to c12_world.zag;
  the additive section differs from c12's exactly in: the CTXT
  pool + slot fns replacing STRATT fns, `strat_sel`'s added
  slot parameter, `det_handle`'s slot wiring; zero
  world/goal/relation/need literals in the additive section and
  c13_main.zag outside the harness fns (goal constructors live
  in c13_world.zag, the allowed home; the context signature
  reads structural goal positions only).

## 7. Section 7: exact predicted stdout (frozen)

(Sections S1A..S3, S4, S6L, S6B identical to COGOPS-OPTIMISTIC;
S5/S7/S9B/S11 identical to COGOPS-COSTAWARE; S8/S9/S12/S13/S14
identical to COGOPS-OPTIMISTIC; S10 and the summary are new.)

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
LSTATE-RET nrel=6 ids=601,602,606,613,615,604 cnts=16,16,0,3,0,8 prov=0,23,25,72 rev=4
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
LSTATE-RET nrel=6 ids=601,602,606,613,615,604 cnts=16,16,0,3,0,8 prov=0,23,25,72 rev=7
SPEC-VFY rev=7 nrel=7 ep0=21 ep1=22 nfacts=72
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
SUMMARY-DET agree=1 plans_built=8 plans_loaded=4 trials=6 declines=0 prior=2
CTX n=5
CTX0 sig=3,606 pw=1,1,2 who=0,0,0 need=0,0,0 alt=0,0,0
CTX1 sig=3,613 pw=3,2,6 who=1,1,1 need=2,0,8 alt=1,0,4
CTX2 sig=4,613 pw=2,2,4 who=1,0,4 need=5,5,9 alt=2,1,10
CTX3 sig=3,615 pw=3,2,6 who=1,0,1 need=2,0,8 alt=1,1,3
CTX4 sig=3,604 pw=1,0,3 who=1,0,2 need=1,0,6 alt=1,0,9
```
