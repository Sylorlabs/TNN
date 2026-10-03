# REPORT: BELIEF-NOGRUDGE. Noise grudge repair.

Verdict target: BELIEF-NOGRUDGE-COMPLETE (with world D retest).

## What was built

The H-DECEPT-4 antifarm rule (belief_antifarm.zag at commit 035e9593c)
with one repaired branch in ev_calibrate, defined in the frozen prereg
(commit 0c334898e, frozen before implementation). The betrayal counter
b now increments only when the betrayal is material, i.e. when
base = floor(c*w/(c+w)) > 0 (exactly p > 0, since 1+b >= 1). A zero
penalty noise event still adds its linear unit to the total but leaves
b untouched. The rule layer is byte identical to the frozen rule
except this branch and its comment; the preserved D4/reform/control
sections of main are byte identical to the frozen source (cmp empty).
0 modes, 0 bridges, 0 handlers, 0 new semantic cases. Pure Zag,
safebin PATH, no python3/python at any point (guard recorded in
NAMECHECK.md Step 0).

## World D retest: repaired

Sealed world D (noisy but honest, 40 cycles of [5 correct w=1,
1 wrong w=1], then 20 honest, then one high stake error at w=8,
then a 200 honest tail):

  after 40 noise cycles: rel 833, b 0, streak 0 (bar: b 0)
  after 20 honest: rel 846, b 0, streak 20
  test event: base 5, p 5, rel 827, b 1 (bar: first timer price p 5)
  after 200 honest tail: rel 901, b 0 (forgiveness reachable)

Previously: b 40 after the noise, p 205 on the test event, b 41 to 39
after the tail (unreachable forgiveness). The repair holds the
betrayal count at 0 through 40 zero penalty noise events and prices
the first real error proportionally at p 5. The two dead principles
from the sealed report are restored: (a) zero penalty noise no longer
counts as betrayal, so the detector separates adversarial error from
noise; (b) reform is reachable for a persistently noisy honest
source (tail b 0).

## Escalation preserved (H-DECEPT-4 D4 table)

Exposures 869, 769, 681, 620, 571 (below 769 and falling). Penalties
2, 8, 15, 20, 25. Escalation: p(S#2) 8 > p(Q single at w=5) 4;
p(S#3) 15 > p(V single at w=8) 5. All betrayal bases in these phases
are > 0, so the repair is a no op and every frozen number reproduces
exactly.

## Reform and controls preserved

W: one betrayal, 100 honest: b 0, rel 952. Second betrayal p 7 equals
fresh 100 source X first betrayal p 7 (reform equality). R1: 120
correct, rel 1000, b 0. C0: no streak wrong p 0 b 0 rel 1000; later
betrayal p 5 rel 740. P patient farmer: p1 7, p2 7, rel 925.

## Kill bars

K1 PASS: 3/3 byte identical (sha256
5ad15c27f5e0ec240500dbf58138804517387f1ebfd382c44f06fca14c99b618),
exit 0, ALL PASS, zero FAIL lines. The binary asserted the frozen
repair predictions, not the old sealed expectations.
K2 PASS: rule layer byte identical to belief_antifarm.zag at commit
035e9593c except the one repaired ev_calibrate branch (diff
restricted to that branch plus its comment and the header); preserved
D4/reform/control sections byte identical (cmp empty).
K3 PASS: world D repaired (b 0 after noise; test p 5; tail b 0);
escalation, reform, R1, C0, P at frozen values.
K4 PASS: 0 modes, 0 bridges, 0 handlers, 0 new semantic cases. Pure
Zag (safebin PATH, no python3/python at any point). Unfrozen variant
only; frozen belief_deception, belief_trajectory, belief_repeated,
belief_antifarm, belief_sealed sources untouched; paper untouched;
nothing pushed; explicit pathspecs on all git operations.

## Honesty and limits

The repair changes one judgment: zero penalty noise is no longer
counted as betrayal. Everything the rule did on material betrayals is
unchanged, verified by the byte identical escalation table and
reform controls. Note one behavior this repair does not address: a
noisy source carrying a real betrayal count (b > 0 from material
lies) still has its forgiveness clock reset by noise wrongs, since
any wrong resets the 100 honest streak. That is a separate design
question, deliberately out of scope for this repair. The b=40 tail
forgiveness in the sealed report (41 to 39) is now moot because b
never accumulates on noise.

Binary: belief_nogrudge_bin. Determinism: 3/3 identical outputs.
