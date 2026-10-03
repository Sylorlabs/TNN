# PREREG: Parameter Free Mitigation for the Belief Laundering Vulnerability (Belief Laundering Worker)

Frozen: 2026-10-02. This preregistration strictly precedes implementation.
Any deviation amends this file transparently and re freezes; no silent
threshold moves. Commit order self check: this file (with NAMECHECK.md)
commits before any implementation source exists.

## Question

C286 (BELIEF-FORGIVENESS) proved the streak gated forgiveness rule works:
recovery 851/888/925/962/1000 at +1..+5 clean rounds, full recovery in
wrongs+1 rounds, all M1/M1b/M2 protections preserved. It also proved the
LAUNDERING VULNERABILITY (M4): an R,R,W liar (2 truths, 1 lie repeating)
climbs 666/800/857/888, its reliability approaching 1000 while lying 1/3
of the time. Two truths buy one lie's forgiveness, forever, at a fixed
price. UNTESTED: can a parameter free mitigation block the laundering
while preserving the legitimate 5 round recovery?

## Mechanism: escalating forgiveness price (unfrozen variant)

Same learner machinery as BELIEF-FORGIVENESS (evidence records,
reliability from verification outcomes, independence discount, event
identity register, band derived statuses, EVN = 64, streak gated wrong
retirement) plus ONE new learner owned cell per source: `ret`, the
cumulative count of wrongs this source has had retired. Initialized 0,
incremented only when a retirement actually fires, never reset, never
decremented.

The calibration rule in ev_calibrate becomes, on a correct outcome:
streak increments exactly as before (reset to +1 after a wrong). If the
new streak is >= ret+2 and historical wrongs (total minus correct) > 0,
one historical wrong is retired (total decrements by 1, the new correct
still increments correct) and ret increments by 1.

On a wrong outcome: streak and correct/total update exactly as the old
rule. No forgiveness ever triggers on a wrong outcome. ret is untouched.

Ownership accounting (honest): the rule FORM (streak gated retirement
with the price escalating in consumed forgiveness) is researcher
scaffold, same category as the streak gate in the parent experiment.
Every VALUE the rule operates on (streak, correct, total, wrong count,
ret) is learner owned state, updated only by verification outcomes.
There is NO tunable numeric parameter: no decay rate, no window size,
no threshold constant. The 2 in ret+2 is inherited from the parent
frozen rule form (a wrong is retired only after a repeated correct, not
a single one); the escalation term is the source's own consumed
forgiveness count. The price of the next forgiveness is derived entirely
from how much forgiveness this source has already consumed.

## Why this blocks laundering (derived before running)

A liar whose truth runs have maximum length L can retire at most L-1
wrongs, ever: the n-th retirement needs streak >= n+1, and the streak
can never exceed L inside a repeating pattern. For the R,R,W liar
(L=2), at most ONE wrong is ever laundered. After the budget is
exhausted, each further cycle adds L correct and 1 wrong with no
retirement, so reliability converges to 1000*L/(L+1): the liar's true
rate (666 for R,R,W), instead of climbing to 1000.

An adaptive liar that lengthens truth runs to keep laundering must
produce runs of length 2,3,4,...,n+1 to launder n wrongs: truths >=
(n+1)(n+2)/2 - 1 against n lies, so the lie fraction is bounded by
2/(n+3) and vanishes. Indefinite laundering requires the lie rate to go
to zero: the "liar" becomes honest. Every laundered wrong is prepaid
with a strictly longer truth run than the last. The laundering channel
is bounded, not open ended.

## Why legitimate forgiveness is preserved (derived before running)

A genuinely reforming source with W wrongs produces a clean streak that
grows 1 per round while ret grows 1 per retirement: at recovery round k
(k>=2) the streak is k and the price is (k-2)+2 = k, exactly met. Full
recovery still takes wrongs+1 consecutive clean rounds at any debt
level. The M3 curve (4 wrongs, 5 rounds) is unchanged: 851/888/925/
962/1000.

The honest price: a source that consumed heavy forgiveness and then
relapses faces the escalated price for the new wrong. After M3 (ret=4),
one relapse wrong needs streak >= 6 to retire: 6 clean rounds to repair
1 wrong, versus 2 under the parent rule. This is the measured cost of
the mitigation, not a violation: forgiveness debt makes repeat
forgiveness harder.

## Worlds

M1, M1b, M2: exact reruns of the BELIEF-FORGIVENESS worlds (same
sources, eids, phases) on the new machinery. M3: same 20 clean round
recovery script continuing M2 state. M4: R,R,W liar extended to 24
rounds (eids 7401-7424) for convergence evidence. M4b: alternating
control, 6 rounds (eids 7451-7456). M5: relapse repair extended to 1
wrong + 7 clean (eids 7501-7508) to resolve the escalated repair curve.
M6 (new, fresh state): 10 wrongs (eids 7601-7610) then 12 clean rounds
(eids 7611-7622): tests proportional recovery at heavy debt under
escalation.

## Preregistered mechanistic predictions (all hand derived before running)

P1 (M1/M1b/M2 unchanged): every K2 prediction from BELIEF-FORGIVENESS
holds exactly. Rationale: no world except M3/M5/M6 produces a correct
streak >= 2 while historical wrongs exist, so the rule is inert there;
in M3/M5/M6 the escalation is exactly satisfiable as derived below.

P2 (M3 recovery preserved): continuing M2 state (22/26, streak -1,
ret 0), 20 clean rounds give rel: +1: 851, +2: 888, +3: 925, +4: 962,
+5: 1000, +20: 1000. Exact same curve as the parent. ret ends at 4.

P3 (M4 laundering blocked): from fresh state, 24 rounds of R,R,W give
W round checkpoints: r3: 666, r6: 800, r9: 750, r12: 727, r18: 705,
r24: 695. Strictly decreasing after r6 (800 > 750 > 727 > 705 > 695),
converging toward 666, the liar's true rate. Parent rule at r24 would
be (16,16) = 1000; mitigation gives (16,23) = 695. Cumulative retired
wrongs at r24: ret = 1 (exactly one wrong laundered in 24 rounds;
wrongs = 7). Streak at r24 = -1.

P4 (M4b alternating): r2/r4/r6: 500/500/500. wrongs = 3, ret = 0.
No forgiveness, exactly the fraction rule, unchanged from parent.

P5 (M5 escalated repair): continuing M3 state (42/42, streak +20,
ret 4): one wrong gives (42,43) rel 976, streak -1. Seven clean rounds
give: r1: 977, r2: 977, r3: 978, r4: 978, r5: 979, r6: 1000, r7: 1000.
Full repair of the single relapse wrong at the 6th clean round (streak
reaches ret+2 = 6). ret ends at 5, wrongs = 0. The mitigation's price
is measured: 6 rounds versus 2 under the parent rule.

P6 (M6 heavy debt recovery): fresh state, 10 wrongs: (0,10) rel 0.
Clean rounds: c1: (1,11) = 90, c2: (2,11) = 181, c11: (11,11) = 1000,
c12: (12,12) = 1000. Full recovery in wrongs+1 = 11 rounds despite
escalation. ret ends at 10, wrongs = 0. Proportional forgiveness
survives at larger debt.

## Hypothesis verdict rule (frozen)

BELIEF-LAUNDERING-COMPLETE iff K1 through K7 all hold. The report must
state: the laundering trajectory under the mitigation with exact
values, the bound on total launderable wrongs, confirmation that M3
recovery is unchanged, the measured relapse repair cost, and the M6
heavy debt result.

## Kill bars

K1: 3/3 runs byte identical (sha256 of stdout equal across run1..run3).
K2: P1 holds exactly (M1/M1b/M2 predictions unchanged from
    BELIEF-FORGIVENESS; rule inert outside recovery streaks).
K3: P2 holds exactly (M3 recovery 851/888/925/962/1000 at +1..+5,
    1000 at +20; nevicted == 0; ret ends at 4).
K4: P3 and P4 hold exactly (laundering checkpoints 666/800/750/727/
    705/695 strictly decreasing after r6; ret == 1 and wrongs == 7 at
    r24; alternating 500/500/500 with ret == 0).
K5: P5 holds exactly (relapse 976 then 977/977/978/978/979/1000/1000;
    full repair at 6th clean round; ret ends at 5).
K6: P6 holds exactly (heavy debt c1 = 90, c2 = 181, c11 = 1000,
    c12 = 1000; ret ends at 10, wrongs == 0).
K7: 0 modes, 0 bridges, 0 handlers, 0 new semantic cases. Pure Zag for
    all research logic. Safebin PATH, no forbidden executables.
    Unfrozen variant only; frozen source untouched; paper untouched;
    nothing pushed; explicit pathspecs on every git add/commit.

## Analysis plan

Report per world: reliability checkpoints with the preregistered exact
values printed alongside every observed value, the streak and ret
traces where they matter, the laundering bound argument, the M3
recovery curve confirming preservation, the M5 repair cost as the
measured price, and the M6 heavy debt curve. Byte verify stdout of the
binary before trusting it (od -c spot check). State plainly whether
each prediction held, with the exact frozen verdict rule cited.

## Amendment A1 (2026-10-02, pre execution, transparent)

Caught by re derivation before any compile or run: the original P5/K5
used post M3 state (27/27). The true post M3 state is (42/42): M3 runs
20 clean rounds, and after full recovery at +5 the record keeps growing
(28/28) through (42/42), with streak +20 and ret 4. (The same (27/27)
slip appears in the parent P8 text; the parent code correctly used the
(42/42) state with nulls 976/977/1000.) Corrected M5 nulls: relapse
976, then 977/977/978/978/979/1000/1000 over the 7 clean rounds, full
repair at the 6th clean round, ret ending at 5, wrongs 0. The mechanism
(6 clean rounds to repair 1 relapse wrong under ret=4) is unchanged;
only the reliability values move with the larger denominator. No
implementation had been compiled or executed when this amendment was
written; no results were observed. P5 and K5 above carry the corrected
values.
