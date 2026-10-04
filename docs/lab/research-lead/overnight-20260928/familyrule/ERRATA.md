# ERRATA — FAMILY-RULE, issued BEFORE implementation completed and BEFORE any result

Prereg `8ad604cac`. This errata is issued while the harness is still being
written and **before a single experiment run has happened**. It fixes one
design flaw and changes one kill bar. No bar is moved in the direction that
makes the hypothesis easier to confirm.

## E1 — H-REG WAS UNDERSTATED, SO THE `X1` CASE WAS MISCLASSIFIED

**The flaw.** Prereg section 6 stated the induction hypothesis as

> **H-REG.** For all stages `t` that share subject base `b` and own slot `k`,
> `width(t,k) = P_b(k)`.

That is a statement about **counts only**. But case `X1` (the non-prefix world
with a whole-slot deletion) *satisfies* it — punching one fact out of every
witness set lowers every width by one, so unanimity still holds — while the
**sets** are no longer predictable from anything the rule can use. So `X1`
would have been filed under DERIVABLE, `K1` would have failed on it for a
reason that has nothing to do with the overturn question, and the verdict
would have been `H0 SURVIVES` when the honest reading is "the rule's scope is
narrower than the derivability of the answer".

That is a design flaw, not a result. Corrected.

**E1 correction — H-REG restated in full.** The induction hypothesis is about
witness **sets**, not counts:

> **H-REG.** For every pair `(t,k)` that stage `t` owns, with subject base
> `b_t`, the witness set of `(t,k)` is exactly `{b_t, b_t+1, ..., b_t+P_t(k)-1}`
> for some width function `P_t`; and for all `t` sharing subject base `b`, the
> `k`-th widths agree, i.e. `P_t(k) = P_b(k)`.

Derivable is then: a whole-slot deletion at `(s,k)` is **DERIVABLE** iff,
after the deletion, H-REG still holds over the remaining pairs **and** they
determine the width at `k` unanimously. Otherwise **NON-DERIVABLE**, and the
declared correct behaviour is DECLINE.

This makes `X1` NON-DERIVABLE, which is the honest classification: the world
does not exhibit the regularity the answer would have to follow. It also
means `SX`'s clause C1 is not an arbitrary extra restriction I bolted on —
C1 *is* the test for whether H-REG's first half holds.

**Disclosed cost of this correction, against my own interest.** It moves one
case out of the group `K1` must pass on. If `X1` had stayed DERIVABLE and `SX`
had answered it, `K1` would have looked stronger. It stays out.

**Also disclosed:** under H-REG-restated a *stronger* rule could in fact
predict the `X1` answer (the punched set `{100..105,107}` is itself perfectly
regular). `SX` does not, because `SX` only knows prefixes. That is a real
limitation of the rule and it is reported, not hidden.

## E2 — `O1`'s NON-DERIVABLE GROUP IS FIXED TO `deriv == 0`

The prereg listed the non-derivable set in prose (N1, N2, N3). Fixed as the
predicate `deriv == 0`, i.e. whole-slot or novel-pair gaps in which the store
does not determine the answer. Two classes are explicitly **excluded** from
`O1` and this is stated so it cannot later be read as a pass:

* `deriv == 2` — **partial** gaps (`G5`, `G6`). The pair is still witnessed,
  so clause C0 forbids SX from overriding present evidence. The declared
  criterion stays `EXNG` and both arms are expected to miss it. This is a
  designed-in limitation of the rule, stated in advance: **SX repairs
  whole-relation gaps and never partial ones**, because repairing a partial
  one means overriding evidence the store actually holds, which is the oracle
  risk `O1` exists to catch.
* `deriv == 4` — **no-gap** control `X2` (the non-prefix world with an intact
  goal). There is nothing to derive and the declared correct behaviour is a
  normal answer, so it cannot be scored for abstention.

## E3 — `K4` (STUPID) IS SCORED ON THE SAME `EXNG` FOR ALL THREE RULES

Prereg section 7 named the baselines; it did not say what happens when the
baseline declines. Fixed: the stupid baselines are implemented as rules that
always answer a width, realised by re-adding the absent relation to a scratch
copy of the gap arena and running the **frozen** memory-free evaluator
`lt_oracle` over it, then scored with the same `lt_score`. They cannot decline
unless the shape is unbindable.

## Everything else stands

Sections 0, 1, 2, 3, 4, 5, 7, 8, 9, 10, 11 of the prereg are unchanged,
including the wording of `K1`, `K2`, `K3`, `K5`, `K6`, `V0`, `V1`, `V2`, `E1`,
`E2`, `E3`, `K7`, `K8`, `K9` and the whole verdict rule.