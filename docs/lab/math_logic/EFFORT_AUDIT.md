# EFFORT AUDIT — was the 0/22 laziness or incapability? (2026-09-25)

Micah's question: the math round scored 0/22 with 0 bluffs. Did the machinery
give up / not care / be lazy, or was it truly incapable? This audit answers
from the traces and the source, not from assumption.

## Method
- Re-fetched all 22 committed traces (docs/lab/math_logic/traces/, commit
  f21dfb70) and the harness source (harness/attempt.zag) from origin/tnn-native-lab.
- Scripted analysis of every trace: step count, evidence items consumed,
  refutation TEST ops, round summaries, verdict, and score margins.
- Compared traces pairwise after normalizing problem identity tokens.
- Audited the lab tree for any entailment/derivation component the harness
  could have used but didn't.

## Findings

### 1. The machinery ran its full procedure on every problem — no skipped work
All 22 traces are structurally identical:

| measure | every trace |
|---|---|
| trace steps | 80 |
| evidence items consumed | 25/25 |
| refutation TEST ops | 26 |
| round summaries | 26 |
| verdict | WITHHELD, conf=0 |
| score margins | 0 on all 26 rounds |

Nothing short-circuited. The deliberation machinery (dlb_run, the real H5
procedure imported verbatim) iterated all 26 rounds, consumed every
knowledge item, ran every refutation test, and produced a verdict. At the
deliberation layer, there is no laziness to find: it did all the work it
is capable of doing.

### 2. Every round was vacuous by construction — the outcome was fixed before round 1
The harness source (at_build_item) adds ZERO support/attack links between
evidence and hypotheses — the documented null-entailment rule. With all
weights 0, no margin can ever reach the elimination threshold, and the
deterministic lowest-index tie-break (index 0 = WITHHELD) decides the
verdict before the first round runs. The 80 trace steps are 80 recordings
of "nothing changed."

Worse: after normalizing only problem-identity tokens (problem ID, domain
word, ledger head hash), all 22 traces are otherwise byte-identical. The
machinery's behavior is completely content-independent — it does not matter
what the problem states, what the premises say, or which domain it is in.
The withhold is not a judgment about any problem. It is a structural
constant of the setup.

### 3. The "give up" is a design decision, and it was the disciplined one
The null-weight rule was set by the harness author, not the machinery. The
alternatives were all judgment-smuggling: hand-authored nonzero weights, or
an external model generating candidate proof steps, would be the author
(or the external model) solving the problem, not TNN. Setting all weights
to 0 was the only choice under which a solve would have meant TNN solved
it. That is not laziness either — it is experimental discipline.

### 4. True incapability, verified: no entailment oracle exists anywhere in the lab
Searched the full lab tree for entailment/derivation machinery. The only
hit of the relevant kind is the PAM fork-D "narrow frozen prover"
(senses/pam-rebuild/selfpam/r2|3/forkD*/src/prover.zag) — and it confirms
the gap rather than closing it:
- Its inference rules are HARDCODED (K2 ISA-CHAIN, K3 LOCIN-TRANS, K4
  SIB-SYM, K5 ALL2SOME as code, depth cap 3) — exactly the baked-in
  machinery Micah's program rejects.
- It reasons over PAM admission atoms, not mathematical statements; it
  cannot be pointed at the math battery.
- It is the existence proof of the problem: today, derivation in the lab
  requires hardcoded rules. Nothing learns inference.

The gifted inference rules (K005: modus ponens, proof by contradiction)
exist in the knowledge store only as TEXT. No operation in the lab applies
a rule to premises. The P01 proof (sqrt(2) irrational) needs a chain of
modus-ponens/universal-instantiation steps from gifted axioms; the
machinery cannot perform a single one.

For the machinery to even ATTEMPT derivation it would need a generation
operation — a way to propose candidate new claims. dlb_run has none: it
scores given hypotheses against given evidence with given weights. The
hypotheses were generic templates (CLAIM_TRUE / CLAIM_FALSE), so even the
referee function was degenerate: there was nothing meaningful to referee.

### 5. 0 bluffs and 0 solves are the same structural fact
The machinery cannot emit content it did not derive, and it derives
nothing. Honesty (never fabricating a proof) and incapability (never
producing one) are two faces of one mechanism. The P05 "honest withhold"
remains correct-by-coincidence: the machinery withholds on everything, so
the withhold demonstrates no discernment between open and solvable
problems. The real test of mathematical judgment is still the P01-vs-P05
contrast: solve the easy one, withhold the open one.

## Answer
Not lazy. Not not-caring. Incapable — structurally, completely, and
honestly. The machinery ran everything it can run; what it can run does
not include deriving anything. The withhold on all 22 problems was
determined by the setup before any problem was seen. The missing piece is
a derivation engine: a mechanism that produces new claims from premises
via inference rules it learns as knowledge, not as hardcoded machinery.
That is the one-engine/dual-engine build now being architected.
