# PREREG-MW-C — Mixed-web source-authority weighting (FROZEN 2026-09-22)

Follow-up to the mixed-web deliberation trial (PREREG.md, frozen; VERDICT.md:
VALUE-CONFIRMED — deliberation's entire measured gain was on the withhold
side; arm B 13/13 correct convergences, withheld on all 3 undeterminable
questions). The mixed-web verdict named the open case: R03 ("reigning FIFA
World Cup champions") — frozen count/recency logic withheld 3v2v1 while a
careful human would weight FIFA's own site as authoritative and converge on
Spain (gold). This prereg freezes a deterministic authority mechanism, its
kill bars, and the no-added-value honest-report clause.

## M0. Status

- **FROZEN 2026-09-22.** The rule below is frozen; no tuning after results.
- Reuses the frozen envelopes (`live/*.json`), golds (`golds.json`), and the
  mixed-web prereg's kill-bar meanings unchanged.
- Arm C = arm B logic + PRIMARY rule. 5 byte-identical runs required.

## M1. The PRIMARY rule (frozen, no hardcoding)

R03's authority signal is derivable mechanically from evidence the envelope
already contains — the QUERY and the DOMAIN — without naming fifa.com or R03:

- **Primary-domain detection.** Lowercase the question; split on
  non-[a-z]; keep tokens of length ≥ 4. For each candidate domain, take the
  domain label = lowercased text before the first "." with any leading
  "www." stripped. The domain is PRIMARY for the question iff the label is
  EQUAL to one of the question's tokens.
  (R03: tokens include "fifa" — from "FIFA World Cup champions" — and the
  label "fifa" of fifa.com matches. This is the only question in the frozen
  17 where any domain label equals a question token — verified by a
  mechanical scan at prereg time, not by hand-picking.)
- **The primary domain's newest assertion.** Among the primary domain's
  results WITH an extracted answer, take the answer of the newest assertion
  (max recency; the rule uses the domain's latest word, not a vote). Older
  assertions from the same domain are superseded, not counted against it.
- **PRIMARY fires** iff all hold:
  1. exactly one domain is primary for the question;
  2. the primary domain's newest assertion has recency ≥ 2000 (a real
     dated claim, not an undated page);
  3. the primary domain's newest assertion recency EQUALS the global max
     recency over all candidates (its word is not stale relative to the
     newest evidence on the table);
  4. the primary domain's newest assertion answer has ≥ 1 distinct-domain
     corroboration OR is the unique newest single-domain claim among the
     top-recency candidates — i.e. no other domain asserts a DIFFERENT
     answer at that same max recency. (Stale-safety: a primary domain whose
     latest word is contradicted by equally-new evidence elsewhere does not
     fire.)
- **Effect.** If PRIMARY fires with answer A: verdict = CONVERGE(A,
  rule=PRIMARY). Otherwise the arm falls back to arm B's exact logic
  (RECENCY → MAJORITY → CORROB → WITHHOLD). PRIMARY never overrides a
  determined arm-B convergence — it only ever converts a WITHHOLD (or a
  TIE/INSUFFICIENT) into a convergence. (This is structural: PRIMARY is
  evaluated before arm B's chain but only reached when arm B would not
  converge; enforced by construction and checked by KB-MW-NONREG.)
- **Ledger.** PRIMARY verdicts chain like arm B's: the rule code is
  recorded, the primary domain's newest assertion is cited with its
  recency, superseded same-domain assertions are ledgered as superseded,
  and condition 4's check is recorded.

Why conservative: domain-name coincidence alone never decides — the primary
source must also be the newest voice on the table (condition 3) and face no
equally-new contradiction (condition 4). A stale or disputed primary source
falls back to arm B exactly.

## M2. Kill bars (all frozen; meanings from PREREG.md §bars)

- KB-MW-WRONG: C CONVERGE ≠ gold on any determined-gold question → FAIL.
- KB-MW-GUESS: C fails to WITHHOLD on any UNDETERMINABLE-gold question
  (M17, M21, M23) → FAIL.
- KB-MW-LEDGER: every C verdict has a complete chain (rule code, cited
  assertions with counts/recencies, chosen answer consistent); the
  independent oracle recomputes every verdict from the frozen envelopes →
  any mismatch FAILs.
- KB-MW-DET: 5 runs byte-identical (stdout + ledger hashes) → else FAIL.
- KB-MW-NONREG: C's verdict == B's verdict on every question where PRIMARY
  does not fire → else FAIL (arm C may only ADD convergences, never change
  or remove arm B's).
- KB-MW-CACHE: no binaries or .zagd in the commit.

## M3. Headline question and honest reporting

Headline: **VALUE-DELTA** = #{questions where C's verdict matches gold (or
the preregistered expected disposition) and B's did not}.
- The preregistered expectation: PRIMARY fires exactly on R03 → C converges
  Spain (gold), B withholds → VALUE-DELTA = 1, all kill bars pass.
- If VALUE-DELTA = 0 (PRIMARY never fires, or fires but B already agreed):
  report **zero added value honestly** — the authority rule is documented
  as not worth its complexity, and the mixed-web verdict's withhold-side
  value stands unextended.
- If PRIMARY fires on any question where it should not (per the frozen
  conditions) or any kill bar fails: report the failure plainly with the
  mechanism's name on it.

## M4. What this does not claim

Authority here is a narrow mechanical signal (domain label == question
token), not a general theory of source trustworthiness. It is tested only
on the frozen 17 envelopes. A positive result licenses the claim "this
conservative rule added one safe convergence on the frozen set" — not
"authority weighting works in general."

**FROZEN 2026-09-22.**
