# R2-proof result: R2PROOF-PASS

## Verdict

R2PROOF-PASS. All five mechanical checks pass. 3/3 runs byte-identical.
Exit 0. Zero stderr. Pure Zag at every stage (shell + znc only).

## Commits

- Prereg: `8ea3510f0` (PREREG_R2PROOF.md), committed before any
  implementation file existed. K1 satisfied.
- Implementation + results: this commit (r2proof.zag, r2proof_bin,
  R2PROOF_RESULT.md, R2PROOF_RAW_{1,2,3}.txt/.err).

## What was verified

The Zag program `r2proof.zag` mechanically verifies each computational
step of the preregistered analytic proof:

V1 essentiality: PASS. All 384 bit-flip checks confirm that flipping any
of the 6 input bits flips 6-way parity. Grounds "parity depends on all 6
variables, so all 6 must appear as leaves."

V2 NOT-contraction: PASS. All 12 De Morgan identities hold on {0,1}:
NOT(a AND b) = (NOT a) OR (NOT b); NOT(a OR b) = (NOT a) AND (NOT b);
NOT(a XOR b) = (NOT a) XOR b. Grounds "contract all NOT nodes" as
function-preserving with binary-op count unchanged.

V3 leaf arithmetic: PASS. (a) For g in 0..8, u in 0..32, L = g+1
satisfies the edge equation g+u+L-1 = 2g+u. (b) For g in 0..4,
u in 0..32, L in 6..14, the edge equation is unsatisfiable: no tree
with at most 4 binary operators has 6 or more leaves. Grounds
"L = g+1 regardless of u" and the bound g >= 5.

V4 corollary: PASS. For every n in 1..9, floor(n/2) <= 4 < 5; for the
F-RECFOLD hard-instance exact count n_disc = 5 (design `808ed196d`:
"every instance exactly 5 operators"), floor(5/2) = 2 < 5. Grounds the
corollary: no tree at or below half the discovered op count computes
6-way parity.

V5 tightness: PASS. The explicit 5-op witness tree
XOR3(XOR(x1,x2), XOR(x3,x4), XOR(x5,x6)) equals parity6 on all 64 inputs;
XOR associativity and commutativity verified on all 8 triples, covering
all 15 sealed pairings by symmetry. The bound 5 is tight: a 5-op tree
exists, so >= 5 is the exact optimum and the discovered 5-op form is
optimal.

## Determinism

- md5(R2PROOF_RAW_1.txt) = md5(R2PROOF_RAW_2.txt)
  = md5(R2PROOF_RAW_3.txt) = c025fd4b1015f50581d84aa4726f5362
- exit code 0 on all runs; R2PROOF_RAW_{1,2,3}.err all 0 bytes.

## Purity

Zero Python at every stage: authoring (file tool), byte checks (shell
grep over printable-ASCII range), compilation (znc), execution (native
binary). Zero non-ASCII bytes in all committed text files (shell
verified). No em dashes.

## Scope and caveats (from prereg, unchanged)

Trees only. The Q4 beam produces trees. If a future mechanism emits DAGs
with shared subexpressions, the bound must be revisited before R2 can be
claimed. This task verifies the PROOF; R2-form (plan 2.4, applying the
bound to the discovered F-RECFOLD hard-instance artifact) runs after
the F-RECFOLD evaluation lands and is out of scope here.

## Builder label

R2PROOF-PASS.
