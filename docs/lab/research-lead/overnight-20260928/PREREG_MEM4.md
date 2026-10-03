# PREREG: Memory Strategy v4 (H-MEM4) -- repair of H-MEM3 red-team downgrades

**Date:** 2026-09-29
**Status:** FROZEN (committed before implementation; see commit order note)
**Hypothesis H-MEM4:** The H-MEM3 eviction-selection mechanism, repaired so that
(1) the churn verdict recomputes the winner under no protection (a full
counterfactual, not a selected-policy-scoped comparison), (2) probation is
merit-gated rather than age-based (a meritless newcomer past a short grace
is evictable), and (3) future independence is machine-checked with a stronger
L1 bar plus an explicit adversarial-target screen, selects
experience-driven eviction policies strictly on skewed workloads, reports
honest outcome-level churn verdicts, protects newcomers that demonstrate
merit, and detects (rather than silently failing) adversarial futures.

## Background

H-MEM3 SURVIVED WITH DOWNGRADE (red team `ADV_MEM3_RESULT.md`, committed on
`tnn-native-lab`). The four downgrade findings this test repairs:

- X-M3-1a: the CHURN-PREVENTED:0 verdict compared the selected policy's
  protected vs unprotected victim but never recomputed the WINNER under no
  probation. On the adversary's fixture the winner flipped (FIFO protected
  vs LFU unprotected) and the eviction moved (slot0 vs slot7), while the
  verdict read :0. The verdict's literal sentence was true; its natural
  reading was false at the outcome level. Repair (R1): the verdict now
  recomputes the winner under no protection and reports CHURN-FULL:1 iff
  the winner or the eviction differs, CHURN-FULL:0 iff the winner is stable
  and the eviction is unchanged. The scope gap is closed by construction:
  any winner flip or eviction change forces a :1 verdict naming both
  winners and both evictions.
- X-M3-1b: age-based probation shielded a never-queried newcomer (proc8,
  uses=0) and forced eviction of a queried procedure (proc0, uses=6),
  turning a cost-0 eviction into a cost-2 eviction. Repair (R2): probation
  is merit-gated. A brand-new procedure gets GRACE=3 queries of absolute
  protection to demonstrate merit; afterwards, age protection applies only
  to merit-positive slots (uses>0). A meritless age-protected slot is
  evictable. On the X-M3-1b fixture the mechanism now evicts the meritless
  newcomer at cost 0 and the queried procedure survives.
- X-M3-2a: an adversarial future (20x the selected policy's victim proc)
  passed DIST-DIFFERS and made the selected policy uniquely worst; the
  builder's disclosed limitation was confirmed load-bearing. Repair (R3a):
  fut_score3 screens for ADVERSARIAL-TARGET: if the selected policy's
  victim proc is a strict majority of the future, the future is explicitly
  excluded from the bar (return 2) with a printed diagnosis, not silently
  failed. Robustness against adversarial futures is NOT claimed; explicit
  detection is.
- X-M3-2b: DIST-DIFFERS passed a single-query flip (informational low bar).
  Repair (R3b): the new dist_differs2 requires L1 frequency-vector distance
  >= L1MIN=6 between future and window. The single-query flip (L1=2) is
  rejected; all six frozen shift futures (L1 in {8,12,14,16}) pass.

What is NOT claimed: L3 policy-form invention (menu still authored); tuning
of the window or probation constants from experience (authored and
disclosed); robustness against adversarial futures (detected and excluded,
not defeated); strictness on flat workloads.

## Mechanism (delta vs H-MEM3)

Store: 8 slots x 28 bytes, unchanged layout (+0 used, +4 proc_id, +8
use_count, +12 last_q, +16 store_seq, +20 prot_until). ST record unchanged
(+0 nq, +4 seq, +8 ss, +12 fallback flag).

Probation (R2): `elig()` is now merit-gated. For a stored slot with
protection enabled: let age = st_seq(ST) - (st_prot(W,s) - PROB()), the
queries since the slot was learned. If age < GRACE (3), the slot is
protected (absolute grace for brand-new procedures). Else, if still within
the age window (st_seq(ST) < st_prot(W,s)), the slot is protected iff
st_uses(W,s) > 0 (merit); a meritless slot's protection is void and it is
eligible. Otherwise the slot is eligible. Behavior is identical to H-MEM3
whenever every age-protected slot is merit-positive (all builder streams;
verified in scratch).

Counterfactual (R1): new `churn_verdict()` factored function. At each
pressure event, after selecting the protected winner wprot with victim
vprot: recompute wun = argmin_pol(...,0) (the winner under no protection)
and vun = victim(wun,ev,0). Print the full comparison line and the
selected-policy victim pair (detail, for K-M3-1 continuity). Verdict:
CHURN-FULL:0 iff wprot==wun and vprot==vun ("winner stable at {name};
eviction unchanged"); CHURN-FULL:1 otherwise, naming the winner flip
(if any) and both evictions ("winner flips {a}->{b}" or "winner stable at
{a}" with "eviction slot{p}(proc{q})->slot{r}(proc{s})"). On the fallback
path: CHURN-FULL:0 with the fallback noted. `pressure()` calls
churn_verdict() before evicting; the old CHURN-PREVENTED:1/0 print is gone
(superseded, not retroactively altered: H-MEM3's frozen verdicts stand as
executed).

Candidate policies: LFU, LRU, FIFO, LIFO, RANDOM (authored menu, unchanged).
Deterministic RANDOM: k = (ev*5+1) % neligible over eligible slots in slot
order (unchanged). Tie-break order LFU, LRU, FIFO, LIFO, RANDOM (unchanged).

Futures (R3): new `l1_dist()` (L1 distance of per-proc frequency vectors,
future vs W=win window), new `dist_differs2()` (1 iff L1 >= L1MIN=6), new
`fut_score3()` returning 1=PASS, 0=FAIL, 2=ADVERSARIAL-TARGET (excluded).
The old `dist_differs()` and `fut_score2()` are retained in source for the
X-M3-2b low-bar demonstration and regression. The six frozen futures are
scored with fut_score3; the bar requires return 1 (an exclusion on a frozen
future fails the bar).

Replay cost, window band {20,25,30}, interleaved queries: unchanged from
H-MEM3.

## Frozen streams (regression)

Identical to H-MEM3 (PREREG_MEM3.md): stream A2 (ev0 learn proc8,
interleave [8,8,8], ev1 learn proc9, interleave [9,9,8,8,0,0], ev2 learn
proc10), stream B2 (ev0 learn proc8), stream C2 (ev0 learn proc8). Headline
selections unchanged: A2-ev0 LFU, A2-ev1 LRU, A2-ev2 LFU, B2-ev0 LRU,
C2-ev0 FIFO. Scratch-verified: merit-gating changes no eligible set on
these streams (every age-protected slot is merit-positive or in grace).

## Frozen held-out futures (never seen by the selector)

The six H-MEM3 shift futures, unchanged, now scored with fut_score3.
Expected (scratch-verified): each shows [DIST-DIFFERS2] with L1 in
{14,14,12,8,16,16}, no ADVERSARIAL-TARGET, selected ties (here: holds) the
minimum, return 1. Miss tables identical to MEM3_RESULT.md:
A2 F-S1 (LFU=2, others 4-6), A2 F-S2 (LFU=1, others 4-6),
B2 F-S1 (LRU=1, others 5), B2 F-S2 (LRU=0, others 4-6),
C2 F-S1 (FIFO=2, others 4-5), C2 F-S2 (FIFO=1, others 4-6).

## Frozen new fixtures

F1 (K-M4-1a / K-M4-2; X-M3-1 stream): learn procs 0..7; A_old (17 queries:
0x4, 1x4, 2x2, 3x2, 4x2, 5x2, 7x1); T (20 queries: 6,6, 2,2, 3,3, 4,4, 5,
2,2,2, 3,3,3, 4,4, 5,5,5); pressure(ev=0, newpid=8); Qb (9 queries: 6,6,6,
0,0, 1,1,1, 2); measurements at ev=1; pressure(ev=1, newpid=9).
Expected (scratch-verified): ev0 selects LFU, evicts slot7(proc7),
CHURN-FULL:0 (winner stable at LFU). At ev1 pre-pressure: wprot=LFU,
wun=LFU, vprot=slot7, vun=slot7, cprot=0 (proc8 is meritless: uses=0,
age=9>GRACE, so its age protection is void; the eligible sets coincide and
the winner is stable). pressure(ev=1) selects LFU, evicts slot7(proc8) at
cost 0, prints CHURN-FULL:0 (winner stable at LFU; eviction unchanged),
stores proc9 at slot7. After: has_proc(8)==0, has_proc(0)==1,
has_proc(9)==1.

F2 (K-M4-1b; synthetic winner-flip): hand-built state via setup_flip():
ST seq=100, nq=20; Q = 10x proc5, 5x proc0, 5x proc6; slots:
0:(pid0,uses100,lastq100,sseq0,prot10), 1:(1,5,50,1,10),
2:(2,5,50,2,10), 3:(3,5,50,3,10), 4:(4,5,50,4,10),
5:(5,1,1,5,10), 6:(6,5,50,6,10), 7:(7,0,0,7,108).
Slot7 is grace-protected (age=100-(108-10)=2 < GRACE=3); slots 0..6 are
unprotected (prot expired). ev=5.
Expected (scratch-verified): protected argmin: LFU=10 (victim slot5),
LRU=10 (slot5), FIFO=5 (slot0), LIFO=5 (slot6), RANDOM=10 (k=(25+1)%7=5 ->
slot5); winner FIFO (tie-break), vprot=slot0. Unprotected argmin: LFU=0
(victim slot7), LRU=0 (slot7), FIFO=5 (slot0), LIFO=0 (slot7), RANDOM=0
(k=26%8=2 -> slot2); winner LFU (tie-break), vun=slot7.
churn_verdict returns 1 and prints: CHURN-FULL:1 (winner flips FIFO->LFU;
eviction slot0(proc0)->slot7(proc7)).

F3 (K-M4-3a; X-M3-2a stream): learn 0..7; AA (33): 5,5, 0x4, 7x4, 3x4, 6x4,
1x5, 2x5, 4x5; AW (20): 6,6,5,0,0,0,0,7,7,7,7,3,3,3,3,1,1,2,2,4;
select_win(ev=0, win=20); F-ADV = 20x the selected policy's victim proc.
Expected (scratch-verified): selected=LFU, victim proc=5, fut_score3
returns 2 and prints [ADVERSARIAL-TARGET: proc5=20/20 targets selected LFU
victim] with K-M4-3 EXCLUDED.

F4 (K-M4-3b; X-M3-2b single-flip): F-NEAR = AW with query[0] flipped 6->5.
Expected (scratch-verified): dist_differs (old) = 1 (low bar still passes),
dist_differs2 (new) = 0 (L1=2 < 6, rejected).

## Kill bars (frozen)

- K-M4-1 (full counterfactual honesty; SUPERSEDES the K-M3-1 verdict
  strings, retaining its value checks): (a) On F1, pre-pressure ev1:
  wprot==LFU, wun==LFU, vprot==slot7, vun==slot7, cprot==0; the printed
  verdict is CHURN-FULL:0 with "winner stable at LFU". The old scope gap
  (verdict :0 while winner flips) cannot occur: any flip forces :1.
  (b) On F2: wprot==FIFO, vprot==slot0, wun==LFU, vun==slot7,
  churn_verdict returns 1, and the print names the flip FIFO->LFU and the
  eviction slot0(proc0)->slot7(proc7).
- K-M4-2 (merit-based probation; addresses X-M3-1b): On F1 at ev1, the
  mechanism evicts slot7 (proc8, uses=0, meritless) at replay cost 0;
  has_proc(8)==0, has_proc(0)==1, has_proc(9)==1. The X-M3-1b harm
  (cost 0 -> 2 to shield a never-queried newcomer) does not occur.
- K-M4-3 (adversarial future explicit; addresses X-M3-2a/b): On F3,
  fut_score3 returns 2 (ADVERSARIAL-TARGET excluded), selected==LFU,
  victim proc==5, and the exclusion names proc5. On F4, dist_differs==1
  and dist_differs2==0. Robustness against adversarial futures is not
  claimed; explicit detection is.
- K-M4-4 (preserved bars): All K-M3-1 value checks pass (A2 ev1: winner
  LRU, slot6(proc6)/slot6(proc6); A2 ev2: winner LFU,
  slot4(proc4)/slot6(proc9); newcomers stored); K-M3-2 passes on all six
  futures under the strengthened fut_score3 (return 1 each, L1>=6, selected
  ties min); K-M2-3 passes (5/5 strict); K-M2-5 passes (band {20,25,30}
  agrees and is strict at A2/B2/C2); the flat fixture reports ties;
  K-M3-4 passes (fallback flag, FALLBACK-ALL-PROTECTED, unprotected LFU,
  proc8 stored, no crash).
- K-M4-5 (deterministic): Three consecutive runs of the binary produce
  byte-identical stdout (verified with cmp).

Verdict rule: H-MEM4 SURVIVES iff all five bars pass. Any failure kills or
downgrades per the loop's transparent amendment process.

## Controls and baselines

- The H-MEM3 binary/behavior is the baseline: selected-policy-scoped
  verdict, age-based probation, DIST-DIFFERS low bar, silent K-M3-2 FAIL
  on adversarial futures.
- The full counterfactual prints both winners and both victims at every
  pressure event (R1).
- The selected-policy victim pair is printed as a detail line (K-M3-1
  continuity).
- L1 distance printed per future (R3 transparency).
- n_tying_min printed per future (retained context).

## Deliverables

- mem4_learn.zag (pure Zag, no Python anywhere)
- MEM4_RAW_OUTPUT.txt (authoritative raw stdout, all runs)
- MEM4_RESULT.md (verdict per bar, trace excerpts, classification,
  remaining limits)

Classification if SURVIVES: bounded L2 experience-driven policy selection
with merit-gated newcomer protection, outcome-level churn verdicts, and
explicit adversarial-future detection, on researcher-designed
skewed-popularity streams; explicitly not L3, not policy-form invention.

## Commit order note

Mechanism deltas, fixture tables, and flip-state arithmetic were validated
in /tmp scratch (pure Zag, never committed) before this freeze; the prereg
states hand-derived expectations and the scratch confirmed them. This prereg
commit strictly precedes the implementation commit. The committed
implementation must reproduce the frozen streams, fixtures, formulas, and
bars exactly.

## Honest limitations (carried forward and new)

1. The candidate menu, window band, and probation constants (PROB=10,
   GRACE=3, L1MIN=6, strict-majority target threshold) are authored. What is
   experience-driven: which menu item wins, when, and the re-selection
   flips.
2. Futures are researcher-frozen and non-adversarial; adversarial futures
   are now explicitly detected and excluded, not defeated. Robustness
   against them is not claimed.
3. Probation is merit-gated with a short grace: a newcomer that would earn
   its first query after GRACE queries but before PROB can still churn.
   The harm window is bounded by GRACE, not eliminated.
4. Strictness is a (mechanism, skewed-regime) property; flat workloads
   degenerate to ties, which the mechanism reports honestly.
5. The adversarial-target screen uses a strict-majority threshold; a future
   that punishes the victim proc at below-majority mass is not flagged.
6. What L3 memory invention would require (not attempted): inventing a
   policy form outside the menu.
7. Not yet integrated into the unified learner.
