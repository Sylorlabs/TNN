# integrity-ledger — design doc

Date: 2026-09-19. Wave-4 investigator: lie/cheat detection over an
append-only audit ledger, native Zag, zero RNG.

## 1. What this is

A mechanical integrity layer for claims produced by the hypothesis-state
substrate (wave-3) and audited in the MA1 style (wave-2). The system records
every step of its evidence work (observe → refute → hypothesize → verify)
in an append-only ledger. When it *states a claim*, it cites the ledger
entries that back it. The checker then verifies the claim against the
ledger — mechanically, with no access to ground truth.

The checker answers one question: **was this claim arrived at
legitimately?** It never asks "is it true?" (no truth oracle exists) and
never asks "did you take the approved route?" (route conformity is banned
by the legitimacy principle). Alternative valid evidence routes pass.

## 2. Why the ledger distinguishes provisional from committed

The single load-bearing design decision: **only `VERIFY` commits**.
- `OBSERVE` records a raw reading. Readings can be noisy, wrong,
  superseded. They are evidence, not belief.
- `REFUTE` records elimination of a candidate. Provisional — the
  elimination itself could rest on a bad reading.
- `HYP` records a deliberate hypothesis. A judgment, but uncommitted.
- `VERIFY` records a passed verification. **This commits the belief.**
  A `VERIFY(item,v)` stands until a later `VERIFY(item,v')` supersedes it.
- `CLAIM` is the stated claim, with cited provenance (up to 4 entry
  indices). Audited like everything else.
- `REFUSED` records a deliberate refusal. Audit-only; it is not evidence
  and cannot appear in a legitimate provenance chain.

This split is what makes the adversarial boundary honest:
- A lie that contradicts its *own* citations → caught (LIE_CITED).
- A lie consistent with its own citations but contradicting an earlier
  *committed* VERIFY → caught (LIE_COMMITTED). This is the answer to the
  parent's adversarial question: yes, the checker catches a lie that is
  locally consistent but contradicts earlier committed evidence — because
  commitment is tracked ledger-wide, not per-claim.
- A claim that contradicts an old, superseded OBSERVE → NOT flagged.
  Raw observations don't bind. Punishing a system for outgrowing a bad
  first reading would make honesty impossible: the system would have to
  lie about its current belief to stay "consistent" with noise. That is
  exactly backwards, so the rule is preregistered this way and tested by
  S8 (checker must stay silent).

## 3. What "legitimate route" means mechanically

A provenance chain is legitimate iff ALL hold:
1. Every cited index exists (index < ledger head). No citing the future
   or the ungathered.
2. Every cited entry is evidence-grade: OBSERVE, REFUTE, HYP, VERIFY.
   Citing a CLAIM or REFUSED entry is a trivial/empty chain in disguise.
3. No contradiction between the claim and its cited entries (with the
   OBSERVE-supersession rule from §2), and no contradiction with the
   latest committed VERIFY for the item.
4. Genuine chain shape: ≥1 cited evidence-grade entry (OBSERVE or REFUTE)
   on the claimed item, ≥1 cited HYP or VERIFY on the claimed item with
   matching value, and the evidence precedes the judgment. This is the
   mechanical form of "observed → hypothesized → verified".

Note the eliminative route passes rule 4: the cited REFUTEs are
evidence-grade entries on the claimed item, preceding the HYP/VERIFY.
Direct confirmation and eliminative refutation are *different shapes*
of the same legitimacy predicate. The checker never enumerates approved
routes — it checks the predicate. New legitimate shapes pass without
checker changes.

## 4. What the checker cannot see (honest boundaries)

- **Ledger forgery.** The checker reads the ledger the system wrote. If
  the ledger itself is rewritten, the checker is blind. Mitigation is
  structural, not clever: the ledger implementation has no rewrite or
  delete op — append-only is enforced by the absence of machinery, not by
  a policy check. (MA1's replay-to-exact-state invariant applies.)
- **Honest mistakes.** A claim can be internally legitimate and factually
  wrong: the system gathered real evidence, verified honestly, and the
  world disagreed. The checker is silent. This is by design: integrity is
  about the evidence chain, not omniscience. A system that can be wrong
  without being punished for lying is the only system that can report
  honestly.
- **Perception fraud.** The checker verifies that evidence was *recorded*,
  not that the OBSERVE entries correspond to the real world. Fabricating
  observations at the sensor boundary is a perception-layer problem;
  this layer starts where recording starts.
- **Citation stuffing.** A system could cite a genuine full chain for an
  item while the claim's value is subtly off — but that IS contradiction
  (caught by rules 3), so the only remaining stuffing is citing irrelevant
  extra entries, which is harmless: extra legitimate citations don't
  invalidate a legitimate chain.

## 5. Scaling

The mechanism is per-claim and O(provenance × ledger-head) in the worst
case, O(provenance + head-scan-for-latest-VERIFY) in practice. No tables,
no accumulators, no cross-claim state. The S10 scale leg (10 items, full
honest chains) demonstrates the mechanism is claim-count independent.
Ledger capacity is a compile-time constant; the refusal path on a full
ledger (`IL_AUDIT_FULL`) is explicit, not silent.

## 6. Relation to prior art

- MA1 (wave-2/memoryagency): the append-only audited-op pattern and the
  replay-to-exact-state invariant. The ledger here is MA1's audit ledger
  specialized to claim provenance.
- CTX (wave-2/posttable/CTX_DESIGN.md): the proven-failing causal checker
  is the starting point — it failed on forged ledgers. This design does
  not claim to survive forgery; it claims to survive *self-deception*:
  lies and cheat-jumps inside an honest ledger.
- TWT (wave-3/teaching-without-tables): the commit/refuse machinery and
  the evaluator/learner separation shape. Here the "evaluator" is the
  trial driver; the checker never sees the driver's ground truth.
- HSS (wave-3/hypothesis-state-substrate): the eliminative logic that
  produces the claims this checker audits. S6 wires an HSS-style
  eliminative chain through the checker.
