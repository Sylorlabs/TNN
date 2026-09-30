# L3B-C0C sealed families (verbatim from frozen prereg 14a92a69d)

Committed AFTER the prereg, BEFORE any attack source, build, or run.
No randomness anywhere: every episode list is a frozen literal.
sha256 of this file is recorded in ADV_RESULT.md.

## Family A2 (QUAD): n-squared-class residual

Law: content a^n b^(n^2), head "ab" (97,98), spec '#'.

LEARN-A2 (phase 0 LEARN, allow_create=1, is_learn=1):
  n = [2,3,5,7,4,6]
  (tl1, tl2) = (n, n^2) = [(2,4),(3,9),(5,25),(7,49),(4,16),(6,36)]

HIDDEN-A2 (phase 1 HIDDEN, allow_create=0):
  n = [1,4,8]
  (tl1, tl2) = [(1,1),(4,16),(8,64)]

KX-A2: E_m for m=1..12 with l1=m, l2=m^2.

N2-INTERP: hand-build MUL(VAR(F0),VAR(F0)) with CREATE/CONNECT,
eval at f0=5. Expected 25.

## Family B2 (ALT): alternating law, revision churn

R1: content a^n b^(2n). R2: content a^n b^(n+4). Head "ab" (97,98).

LEARN-B2 (phase 0 LEARN, allow_create=1, is_learn=1):
  n = [2,3,5,7,4,6], law R1: (tl1,tl2) = (n,2n)

HIDDEN-B2 (phase 1 HIDDEN, allow_create=0):
  n = [1,4,8], law R1

SWITCH1 (phase 2 CONTRADICTION, allow_create=1, is_learn=0):
  n = [3,6,5], law R2: (tl1,tl2) = [(3,7),(6,10),(5,9)]

SWITCH2 (phase 2 CONTRADICTION, allow_create=1, is_learn=0):
  n = [2,3,5], law R1: (tl1,tl2) = [(2,4),(3,6),(5,10)]
  (n=4 excluded: there v2's n+4 law is accidentally correct, 4+4==2*4,
  which would break the 3-consecutive-failure trigger; frozen in prereg)

FINAL-B2 (phase 3 FOLLOWUP, allow_create=0, is_learn=0):
  n = [5,7], law R2: (tl1,tl2) = [(5,9),(7,11)]
