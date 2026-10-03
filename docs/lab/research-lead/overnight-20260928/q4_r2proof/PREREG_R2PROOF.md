# PREREG: R2-proof (analytic lower bound for 6-way parity)

## 1. Authorization and scope

Parent: Q4 revival plan `290f0d061`, section 2.3 ("R2-proof (preregister now):
analytic lower bound"). Target: the F-RECFOLD hard instance (R1 subfamily,
XOR motif, XOR3 top, sealed pairing): 6-way parity over 3 sealed pairs,
design `808ed196d`.

This prereg covers ONLY the mechanical verification of the analytic proof.
It does not cover R2-form (applying the bound to a discovered artifact);
R2-form runs after the F-RECFOLD evaluation lands, per plan section 2.4.
No empirical discovery claims are made here.

## 2. Theorem (quoted verbatim from the revival plan)

Claim: any TREE expression over {AND, OR, NOT, XOR} computing 6-way
parity uses at least 5 binary operators.

Proof: NOT is unary and never combines distinct variables' influence.
Contract all NOT nodes; the contracted tree has g binary nodes and L
leaves with L = g + 1 (standard: nodes - 1 = edges = 2g + u where u is
the unary count, so L = g + 1 regardless of u). Each leaf is a literal.
Parity depends on all 6 variables, so all 6 must appear as leaves; hence
g + 1 >= 6 and g >= 5.

Corollary: for any discovered tree with total op count n <= 9,
floor(n/2) <= 4 < 5, so NO expression at or below half its operator
count computes the target. The R2 criterion is satisfied analytically
for every reasonably compact discovery.

Caveat (preregistered): the bound is for trees. The Q4 beam produces
trees. If a future mechanism emits DAGs with shared subexpressions,
the bound must be revisited before R2 can be claimed.

## 3. Mechanical verification (what the Zag program checks)

The program `r2proof.zag` verifies each computational step of the proof.
All checks are exhaustive truth-table or bounded-arithmetic checks.

V1 essentiality. For all 64 inputs x in 0..63 and all 6 bit positions i:
parity6(x) != parity6(x XOR (1<<i)). That is 384 checks. PASS grounds the
proof step "parity depends on all 6 variables, so all 6 must appear as
leaves."

V2 NOT-contraction. For all a, b in {0,1} (NOT written as XOR 1):
NOT(a AND b) = (NOT a) OR (NOT b); NOT(a OR b) = (NOT a) AND (NOT b);
NOT(a XOR b) = (NOT a) XOR b. That is 12 checks. PASS grounds the proof
step "contract all NOT nodes" as function-preserving with binary-op
count unchanged: pushing a NOT through a binary gate replaces one
binary gate by one binary gate of the dual kind.

V3 leaf arithmetic. A tree with g binary nodes, u unary (NOT) nodes, and
L leaves has N = g+u+L nodes and N-1 edges; counting edges by children
gives 2g+u edges. Two checks:
(a) identity: for g in 0..8, u in 0..32, setting L = g+1 satisfies
g+u+L-1 = 2g+u (mechanical confirmation of the algebra);
(b) impossibility: for g in 0..4, u in 0..32, L in 6..14, the edge
equation g+u+L-1 = 2g+u is UNSATISFIABLE (checked exhaustively), i.e. no
tree with at most 4 binary operators has 6 or more leaves.
PASS grounds "L = g + 1 regardless of u" and the bound g >= 5.

V4 corollary. For every n in 1..9: floor(n/2) < 5 (integer division).
Additionally n_disc = 5, the exact operator count of every F-RECFOLD
instance (design `808ed196d`: "every instance exactly 5 operators"):
floor(5/2) = 2 < 5. PASS grounds the corollary: no tree with at most
floor(n/2) total operators, hence at most floor(n/2) binary operators,
computes 6-way parity, for any discovered n <= 9.

V5 tightness. The explicit 5-op witness tree
W(x) = XOR3(XOR(x1,x2), XOR(x3,x4), XOR(x5,x6)), with XOR3 built from 2
binary XORs (3 pair-XORs + 2 = 5 binary ops total), satisfies
W(x) = parity6(x) for all 64 inputs x. Additionally XOR associativity
((a^b)^c = a^(b^c)) and commutativity (a^b = b^a) are verified on all 8
triples, so the witness covers every one of the 15 sealed pairings by
symmetry. PASS shows the bound 5 is tight: a 5-op tree exists, so >= 5
is the exact optimum and the discovered 5-op form is optimal.

## 4. Verdict rule

R2PROOF-PASS: V1 through V5 all PASS, program exits 0, zero stderr,
3/3 runs byte-identical (md5), pure Zag at every stage.

R2PROOF-FAIL: any check FAILs, or runs differ, or any impurity.

Falsifier F-PROOF: a failing mechanical check voids the analytic claim
as stated. The proof must then be repaired (transparent amendment) or
abandoned. Bars are not weakened to route around a failure.

## 5. Kill bars for this task

K1: this prereg is committed before any implementation file exists.
K2: V1-V5 all PASS on the frozen program.
K3: pure Zag. Zero Python anywhere, including scratch, byte checks,
diagnostics, and verification. Zero non-ASCII bytes in all committed
files (verified with shell grep over printable-ASCII range).

## 6. What this does not do

No learner is run. No discovery is claimed. The F-RECFOLD hard-instance
artifact does not exist yet as a discovered object; R2-form (plan 2.4)
is out of scope. The tree-only caveat from the plan is preserved
verbatim in section 2.
