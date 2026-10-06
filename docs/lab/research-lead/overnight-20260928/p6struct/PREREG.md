# PREREG -- P6-struct: structural induction for two-way use

Branch `ownership`. Successor to `p6pushdown/p6_formal_induce`, generated
by the queue's successor rule. **Written before code.**

## THE INHERITED DIAGNOSIS (not merely cited)

`p6_formal_induce/REPORT.md` reached a precise negative:

> "the zero-diff claim is not reachable from a statistical induction, only
> from a structural one."

and pre-committed `ZD2-PASS-DEGENERATE-POLICY`: ZD-2 can be satisfied by a
degenerate "always consult everything" policy, which is researcher-authored.
The missing invariant for real closure is **W4**: the learner inventing its
own consult/keep policy.

### What that means concretely

A statistical model (bigram tables + back-off + typing) is usable
**forward** (generate) but only **probabilistically** backward (decide
membership). So one structure cannot support both, and a zero-diff claim
between generation and acceptance cannot be made.

## THIS PHASE'S MOVE

Change the **representation class**, not the question. Candidates are now
**productions** `A -> B C` over a small terminal/non-terminal alphabet:

* **forward** (generation): a production whose LHS matches can be applied;
* **backward** (membership): a production whose RHS contains the queried
  sequence, with the non-terminal expanded, is a *derivation witness*.

Both directions read the SAME production table. That is the property the
statistical representation lacked, and it is what makes generation and
acceptance comparable.

## NO SOURCE-AUTHORED GRAMMAR

The production table starts EMPTY. Productions are induced by the learner
from observed (input, output) pairs by a generic rule: a production
`A -> B C` is recorded when `A` has been seen to expand to the observed
pair. No production is written by the researcher. Source enumeration is
audited: the grammar's contents must be reconstructible from the observed
corpus alone.

## BARS

* **S1 reject-invalid-unseen**: given productions induced from one corpus,
  an unseen INVALID sequence is rejected (no derivation).
* **S2 accept-valid-unseen**: an unseen VALID sequence is accepted
  (derivation exists), with the exact expanded form reported.
* **S3 renaming-invariance**: permute terminal and non-terminal symbols;
  the accept/reject verdict must be identical for every sequence.
* **S4 ablation-fails**: deleting the induced productions makes both S1 and
  S2 degenerate (accept everything), proving the productions carry the
  behaviour.
* **S5 no-degenerate-consult**: acceptance must depend on the productions,
  not on an unconditional fold. Measured by a CONSULT-COUNT bar: the
  fraction of sequences whose verdict was reached without consulting any
  production must be 0 for accepted-and-rejected alike.
* **S6 learner-makes-keep-policy (W4)**: the decision to *record* a
  production must itself be driven by learner-observed outcome, not a
  fixed rule. Measured: productions recorded after a wrong prediction must
  differ from those recorded after a right one.
* **S7 not-source-authored**: grammar contents reconstructible from the
  corpus; no source constant equals any recorded production.

## FALSIFIABILITY

If S3 fails, the verdict depends on symbol identity and the induction is
not structural. If S5 fails, the result is `ZD2-PASS-DEGENERATE-POLICY`
exactly as the parent prereg pre-committed. If S6 fails, W4 is unmoved and
P6 stays open.

## LIMITS

Single author; no independent adversary; synthetic corpus; one alphabet
size; does not measure TNN. Repairs to this harness require the
preconditions listed in `FRONTIER_QUEUE.md` `substrate-spec`: prove
reachability before reading any result.
