# REPORT.md -- Cross-Domain Causal-Intervention L2 (XDOMAIN-CAUSAL-L2)

## Verdict

**XDOMAIN-CAUSAL-COMPLETE**

H1 (learned typed contracts) and H2 (value-level function composition)
both solve the causal to intervention Z queries via L2 adaptation
(REBIND), with per-mechanism adaptive scores below. The L2 operator
subsumes the FUNCTIONAL outcome of C275's sever+recompute on these
queries, but does NOT subsume it as a mechanism; the "irreducibly
structural" claim is falsified for this query class, with boundaries
noted.

## World and Mechanism (frozen in PREREG.md, commit 016aa13d9)

Causal chain: A (confounder, rel 86) causes C (rel 87); E (rel 85) =
A + 2*C. Units 501 (A=1,C=1,E=3) and 502 (A=2,C=2,E=6). Distractor
rel 84. Intervention interface: qrel-keyed do-spec facts (93,89,1)
and (94,89,2); Y/DOSPEC installed as prior learning with in1=89.

Z queries:
- Z1: (501, 94, goal 5). do(C=2). Surgery: 1 + 2*2 = 5.
- Z2: (501, 93, goal 3). do(C=1). do==see: 3.
- Z3: (502, 94, goal 6). do(C=2). do==see: 6.
- Z4: (502, 93, goal 4). do(C=1). Surgery: 2 + 2*1 = 4.

H1: X (id 0) is a typed contract with in1/in2 bound generically via
bind_nth to (86,87). Y (id 1) reads do-spec. D (id 2) distractor.
O (id 3) observational predictor (CONTROL).

H2: Modes. EQN (mode 0) computes g(s,86)+2*g(s,p2), p2 rebindable
(init 87). DOSPEC (mode 1) reads g(q,89). OBS (mode 2) computes
g(s,85) (CONTROL).

Solver: SETUP reads do_val and yrel through Y/DOSPEC (never a
literal), asserts (s,yrel,do_val) to materialize the set value.
Phase 1 (L1): try singles (and H2 ordered pair). Phase 2 (L2):
rebind X's in2 (H1) or EQN's p2 (H2) to generic scan candidates;
validate. X's in1 (context A) held fixed.

## Kill Bar Verification

K1 H1-L2-SOLVE: PASS. TREAT-L2 Z1: REBOUND m=8 in1=86 in2=89
rebound_of=0, EP-RESULT PASS. check_surgery verifies in2=89 and
X'(501)=5. Z4: same, X'(502)=4. Trace: h1_run1.txt.

K2 H2-L2-SOLVE: PASS. TREAT-L2 Z1: REBIND EQN p2=89, L2-SOLVED,
EP-RESULT PASS. check_surgery verifies p2=89 and EQN(501)=5.
Z4: same, EQN(502)=4. Trace: h2_run1.txt.

K3 L1-FAIL (adaptation necessary): PASS. L1-ONLY arm: Z1 and Z4
correctly fail (EP-RESULT PASS with expect=0), Z2/Z3 solve
observationally. Both H1 and H2.

K4 ABLATIONS: PASS. H1 ABL-X (X deleted): Y/D/O rebinds fail
(Y'->2, D'->6, O'->2, none =5). ABL-Y (Y deleted): no do_val,
no assert, 89 never a candidate; fail. H2 ABL-EQN: fail.
ABL-DOSPEC: fail. All as preregistered.

K5 FRESH: PASS. No MAPs/modes taught; fail as expected. Both.

K6 NO-DOSPEC: PASS. Do-spec facts absent; Y(94) missing;
fail as expected. Both.

K7 OBSERVATIONAL Z2/Z3: PASS (disclosed). Z2 (goal 3) and Z3
(goal 6) solve in Phase 1 via X/EQN observationally. This is
expected and disclosed in PREREG; it does not inflate the
surgery claim.

K8 CONTROL-OBS: PASS. O (H1) is a pure observational mapping
g(s,85). Rebinding its in1 to 89 yields g(s,89)=do_val (2),
not the recomputed E (5). In ABL-X, O' rebinds fail. H2 OBS
mode is never rebound in Phase 2 (only EQN's p2 is rebindable);
rebinding it would give 2, not 5. The success is specific to
the causal equation structure, not a generic rebinding effect.

K9 C275 COMPARISON: See dedicated section below.

## Per-Mechanism Adaptive Scores

H1 (typed contracts + REBIND):
- Z1 (surgery): SOLVED via L2. Adaptive score: 1.0 (required
  and achieved structural adaptation: in2 87->89).
- Z2 (do==see): SOLVED via L1. Adaptive score: N/A (no
  adaptation needed; observational).
- Z3 (do==see): SOLVED via L1. Adaptive score: N/A.
- Z4 (surgery): SOLVED via L2. Adaptive score: 1.0.
- H1 adaptive success rate on surgery queries: 2/2.

H2 (value composition + REBIND):
- Z1 (surgery): SOLVED via L2. Adaptive score: 1.0 (p2 87->89).
- Z2 (do==see): SOLVED via L1. Adaptive score: N/A.
- Z3 (do==see): SOLVED via L1. Adaptive score: N/A.
- Z4 (surgery): SOLVED via L2. Adaptive score: 1.0.
- H2 adaptive success rate on surgery queries: 2/2.

Both mechanisms achieve the L2 adaptation. H1 uses typed
contracts (sig_in/sig_out); H2 uses modes with parameters.
The adaptation operator (REBIND) is the same principle:
re-target the evidence source for the intervened variable
while holding context fixed.

## K9: Comparison to C275 Sever+Recompute

C273 established: all four mechanisms (A/B/C/XIO) failed
do-surgery via value chaining. The do-operator needs more
than chaining.

C275 answered: sever+recompute (sc_do) solves Z1..Z4 via
edge surgery. It claimed do-composition is an "irreducibly
structural second kind."

This work (L2 REBIND) shows:

(a) Per-query: L2 solves the same Z1/Z4 surgery queries as
C275, with the same correct outputs (5 and 4). Z2/Z3 solve
observationally in both.

(b) Representation: C275 modifies the graph structure (severs
C->E edge, recomputes E from do-value). L2 preserves the
equation structure X(s)=g(s,in1)+2*g(s,in2) and rebinds in2
from 87 (observational C) to 89 (intervened C). The
intervention is expressed as rebinding, not graph rewriting.

(c) Generality: C275's sc_do is a structural operator that
works on causal graphs. L2's REBIND is a generic adaptation
operator (from C279, arithmetic->planning) applied to a new
domain pair. L2 requires the equation to factor as
f(evidence_for_context, evidence_for_intervened_var), and
requires the do-value to be materialized as a fact via the
intervention interface. C275 may handle interventions where
the do-value is not a simple relation lookup, but that is
outside the C273 query class.

(d) Subsumption verdict: L2 does NOT subsume sever+recompute
as a MECHANISM (they are different operations: rebinding vs
surgery). However, L2 achieves the same FUNCTIONAL outcome
on the C273 queries, which FALSIFIES C275's "irreducibly
structural" claim for this query class. Sever+recompute is
NOT strictly necessary; adaptive rebinding suffices when the
causal equation structure is preserved and only the evidence
source for the intervened variable changes.

In short: C275 proved sufficiency of structural surgery.
This work proves non-necessity: a non-structural adaptive
operator (REBIND) also suffices. The do-operator does not
require graph modification; it requires redirecting the
intervened variable's evidence source, which can be done
via rebinding.

## Implementation Note (bug fix, transparent)

During testing, a fact-store bug was found: 12-byte stride
with 16-byte facts caused slot overlap (obj of slot i
overwrote used flag of slot i+1). Fixed to 16-byte stride,
48 slots. This is an implementation bug, not a prereg
change. The world, mechanism logic, and kill bars are
unchanged. Zero Python was used in diagnosis or fix.
Recorded in NAMECHECK.md.

## Determinism

H1: 3/3 byte-identical. SHA256
5e8341c843627f31ccd28866f850c4f73ba9508f396c7d36b00572e0a45c9f1a.

H2: 3/3 byte-identical. SHA256
bd3068e103c9f7bbd84d907afccb3a98c6d3c6eda6c1a533255a0459410d5ba9.

Binaries: h1_bin, h2_bin. Sources: h1.zag, h2.zag.
Runs: h1_run1/2/3.txt, h2_run1/2/3.txt.

## Constraints Met

Pure Zag. Zero em/en dashes in docs. Paper untouched.
Nothing pushed to GitHub (local commits only). 0 modes/
bridges/handlers (the H2 modes are the mechanism, not new
infrastructure; H1 has 0 modes). Zero Python (toolchain
guard in NAMECHECK.md Step 0). Prereg committed before
implementation (016aa13d9).
