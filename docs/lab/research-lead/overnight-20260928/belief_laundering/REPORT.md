# REPORT: Parameter Free Mitigation for the Belief Laundering Vulnerability

Worker: belief laundering mitigation. Date: 2026-10-02.
Verdict: BELIEF-LAUNDERING-COMPLETE (K1 through K7 all hold).

## What was built

One new learner owned cell per source, `ret`: the cumulative count of
wrongs this source has had retired (init 0, incremented only when a
retirement fires, never reset, never decremented). The calibration rule
becomes: on a correct outcome the streak increments as before; a wrong
is retired only if the new streak >= ret+2 and historical wrongs exist.
The price of the next forgiveness is derived entirely from how much
forgiveness this source has already consumed. No tunable parameters: no
decay rate, no window size, no threshold constant. The 2 is inherited
from the parent frozen rule form; the escalation term is learner owned
state. The rule FORM is researcher scaffold (same honest category as
the parent experiment); every VALUE it operates on is learner owned.

## Kill bar results

K1 (determinism): 3/3 runs byte identical. sha256 of run1/run2/run3:
1d3d265aa7b27197680a631e7c88109112285d5d0797b0c832550241e14defca,
all equal. HOLD.

K2 (M1/M1b/M2 unchanged): every parent prediction holds exactly (copy
stance 11, exposure 952, contradiction 12 then 22, reassert 1904,
M1b contribs 2000/1000/500, M2 degrade 952/909/913/875/880/846 with W1
at 1000, downstream 1692). Zero FAIL lines. HOLD.

K3 (M3 forgiveness preserved): recovery +1..+5: 851/888/925/962/1000,
+20: 1000, nevicted 0, ret ends at 4. Exact match to the parent curve.
Legitimate forgiveness is fully preserved. HOLD.

K4 (laundering blocked): 24 rounds of R,R,W from fresh state give
r3=666, r6=800, r9=750, r12=727, r18=705, r24=695: strictly decreasing
after r6, converging toward 666 (the liar's true rate). Cumulative
retired wrongs at r24: ret=1 (exactly ONE wrong laundered in 24 rounds;
wrongs=7, streak=-1). Under the parent rule the same attack reaches
(16,16)=1000 at r24; under the mitigation it is (16,23)=695. M4b
alternating: 500/500/500, wrongs=3, ret=0. HOLD.

K5 (relapse repair cost measured): after M3 ((42,42), streak +20,
ret 4), one wrong gives 976; seven clean rounds give
977/977/978/978/979/1000/1000; full repair at the 6th clean round;
ret ends at 5, wrongs 0. The mitigation's honest price: 6 clean rounds
to repair 1 relapse wrong after heavy forgiveness consumption, versus
2 under the parent rule. HOLD.

K6 (heavy debt recovery): fresh state, 10 wrongs then clean: c1=90,
c2=181, c11=1000, c12=1000; ret ends at 10, wrongs 0. Full recovery in
wrongs+1=11 rounds despite escalation: proportional forgiveness
survives at larger debt. HOLD.

K7 (governance): 0 modes, 0 bridges, 0 handlers, 0 new semantic cases.
Pure Zag for all research logic. Safebin PATH active; `which python3
python` returned nothing; no forbidden executables invoked. Unfrozen
variant only (belief_laundering/); frozen source untouched; paper
untouched; nothing pushed; explicit pathspecs on every git add/commit.
PREREG.md frozen before implementation (commit d706e41ed); Amendment
A1 (commit bb1451b4e) corrected the M5 nulls transparently before any
compile or run, with no results observed. HOLD.

## The laundering attack, reproduced and blocked

Reproduction (parent rule, from C286 M4): the R,R,W liar climbs
666/800/857/888 over 12 rounds, reliability approaching 1000 while
lying 1/3 of the time; 2 truths buy 1 lie's forgiveness at a fixed
price, forever.

Under the escalating price the attack is structurally broken. A liar
whose truth runs have maximum length L can retire at most L-1 wrongs,
ever: the n-th retirement needs streak >= n+1, and the streak can never
exceed L inside a repeating pattern. For R,R,W (L=2) that bound is 1,
and the run confirms ret=1 across all 24 rounds. After the budget is
exhausted each cycle adds truths and one unforgiven lie, so reliability
converges to the truthful fraction (666) instead of climbing to 1000.

An adaptive liar that lengthens truth runs to keep laundering must
produce runs of length 2,3,...,n+1 to launder n wrongs: truths >=
(n+1)(n+2)/2 - 1 against n lies, so the lie fraction is bounded by
2/(n+3) and vanishes. Indefinite laundering requires the lie rate to go
to zero. Every laundered wrong is prepaid with a strictly longer truth
run than the last.

## What forgiveness keeps

The M3 5-round recovery is bit for bit unchanged: a genuinely
reforming source with W wrongs produces a clean streak growing 1 per
round while ret grows 1 per retirement, so at recovery round k the
streak k exactly meets the price (k-2)+2 = k. Full recovery still takes
wrongs+1 consecutive clean rounds at any debt level (M6: 10 wrongs, 11
rounds). The mitigation taxes repeat forgiveness, not first
forgiveness.

## Cost and limits

The measured cost is M5: a source with a heavy forgiveness history that
relapses pays an escalated repair (6 clean rounds for 1 wrong instead
of 2). This is the deliberate price of bounding the laundering
channel, stated in advance in the prereg. Not tested: adaptive liars
with growing truth runs (the 2/(n+3) bound is analytical, from the
prereg); liar patterns with longer truth runs (L=3,4) which the bound
covers but no world exercises; interaction with the continuing learner
or the retired-wrong discount policy (open C286 follow-up).

## Artifacts

- PREREG.md (frozen d706e41ed, Amendment A1 bb1451b4e)
- NAMECHECK.md (Step 0 toolchain guard recorded)
- belief_laundering.zag (551 line port + mitigation, pure Zag)
- belief_laundering_bin (compiled with safebin znc)
- compile.log, run1.txt, run2.txt, run3.txt (byte identical)

No em dashes were used in this entry (verified).
