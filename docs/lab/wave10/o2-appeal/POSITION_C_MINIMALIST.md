# POSITION C (Minimalist) — Verdicts expire: time-boxed terminality, automatic re-adjudication

**Design council position paper — EXP-4 (O2 appeal). 2026-09-20. NOT APPROVED. Design only.**

## Thesis

Don't build an appeal board. Don't build budgets, evidence currency, or adjudication rules.
Put a time-to-live on REFUTED verdicts: terminal for T episodes, then automatic re-adjudication.
No new trusted machinery — one integer parameter and a pure function of ledger state. Expiry
dominates appeal because there is nothing to spam, no selective lever for the liar, and the
checker recomputes everything trivially.

## 1. Exact design

- **TTL on REFUTED.** A REFUTED verdict carries a time-to-live of T episodes (proposed: frozen
  in prereg; candidate T=500, on the order of half a developmental stage — the value is an
  experimental parameter, not a principle).
- **Deterministic from ledger state.** `expired(c) = (now - refute_episode(c)) > T`, where
  `refute_episode(c)` is read from the claim's `O2_OP_REFUTE` audit entry. Pure function; the
  independent checker recomputes it from the ledger alone. Zero new trusted code paths — the
  verdict query just also checks age.
- **Automatic re-adjudication on expiry.** When a REFUTED verdict expires, it returns to OPEN —
  *with its refutation history intact*: observation counts (`np`, `nn`) are preserved, so a
  claim refuted on `nn=5` re-opens as OPEN-with-`nn=5` still counted. Expiry does not erase the
  kill; it re-opens the question. Re-confirmation must overcome the preserved refutation record
  through the normal `np>=2` path. No new op, no filing, no adjudicator — the clock does it.
- **Nothing else changes.** No appeal op, no budgets, no evidence currency, no initiator roles,
  no new audit entry types. The O2 state machine gains one comparison.

## 2. Why expiry dominates appeal

- **No new surface.** Appeal (A) adds: an appeal op, budget accounting, evidence-currency rules,
  citation verification, re-raise discipline. Each is trusted machinery and each is a gaming
  surface. Expiry adds: one integer, one comparison. The smallest possible trusted delta for a
  recovery path.
- **No appeal-spam — there is nothing to spam.** The appeal attack (B §1) depends on
  *selective invocation*: the liar files appeals exactly on the claims it wants back. Expiry
  cannot be invoked. It happens uniformly to every refuted claim or to none. Selective
  invocation IS the attack; expiry removes the verb.
- **Uniformity is anti-gaming.** The honest learner and the liar receive identical treatment —
  no lever for either. Appeal hands the liar a lever (filing) that the honest learner pulls
  rarely; any asymmetric tool favors the attacker, who uses it at maximum rate.
- **Checker-trivial.** `expired(c)` is arithmetic on ledger entries. Appeal requires the checker
  to adjudicate "did the evidence qualify" — judgment inside the trusted verification path, and
  judgment is where gaming hides.
- **No under-appeal state, no gate ambiguity.** Same as A's best property, for free: until
  expiry the verdict reads REFUTED, period.

## 3. How the C5 strict compose gate treats expiring claims

Identically to today until expiry: under-TTL REFUTED → `SEAM_REFUSED_PARTITION`, ledgered,
abstain. After expiry the claim reads OPEN (with preserved counts) and composes flow normally.
The killed-only bar — 0 successful REFUTED-backed composes — holds *by definition*: a compose
backed by an expired claim is OPEN-backed, not REFUTED-backed. No gate exception, no flag, no
arm. The bar's letter is preserved under the redefined verdict.

## 4. Falsification — what proves this design wrong

1. **Churn tax exceeds machinery cost.** Measure re-litigation: correctly-refuted claims
   re-opened and re-killed every T episodes, in episodes and audit space. If the churn cost
   exceeds the measured cost of A's appeal machinery (or of doing nothing), expiry is the
   expensive minimalism — minimal in code, maximal in runtime.
2. **Liar wait-out demonstrated.** An adversarial trial shows a deceptive learner parking
   correctly-refuted false claims and harvesting them post-expiry at scale (re-confirmation
   overcoming preserved counts via manufactured positives) → the timer is a free appeal with a
   waiting room.
3. **T has no stable value.** If trials show no T that simultaneously (a) fires often enough to
   matter for honest recovery and (b) rarely enough to keep kills meaningful, the parameter is
   un-tunable and the design is B-with-extra-steps (T too long) or kill-theater (T too short).
4. **No-rescue adjudication.** If the council holds that auto-expiry softens the architectural
   terminality guarantee (it does — §5.1), and the no-rescue rule is applied strictly, expiry is
   rejected regardless of its engineering merits. This is a rule-loss, not an evidence-loss,
   and I concede it in advance.

## 5. Honest weaknesses of my own position

1. **The no-rescue problem is real and I bite the bullet.** Auto-expiry un-kills with no
   deliberate act — the direct opposite of MA1's deliberate-killing law ("a kill must be
   real"). Under a strict reading of no-rescue, expiry softens the terminality guarantee and
   loses. My defense is only this: the *measurable* guarantee (C5's killed-only=0) is preserved,
   and terminality-of-verdict was always a means to "refuted claims are never served," not an
   end in itself. If the council holds terminality as an end — and MA1 suggests it does — I
   lose on the rule.
2. **The liar just waits.** Expiry time-shifts the corruption surface instead of removing it.
   My defense: waiting is bounded by T, uniform (no acceleration), and re-adjudication preserves
   the refutation counts — the liar must still overcome real evidence through the normal path.
   But "must wait T episodes" is a speed bump, not a wall, and I won't pretend otherwise.
3. **Churn on correctly-refuted claims.** Every settled kill re-litigates every T episodes,
   forever — a perpetual re-examination tax on the system's own settled judgments, paid in
   episodes, audit space, and learner attention. This cost is real, perpetual, and measurable;
   my empirical bet is only that it prices below appeal machinery plus appeal-gaming. That bet
   must be measured (council test T4), not assumed.
4. **T is arbitrary.** No principle sets it; too short and kills are theater, too long and
   expiry never fires (then it's B with extra steps and I've built nothing). The parameter must
   be set by experiment — which is itself a cost, and a second prereg, and another morning of
   Micah's review.
5. **Blunt by design.** Expiry cannot distinguish O2 errors from correct refutes — it re-opens
   both. I claim bluntness is the anti-gaming feature (no judgment to game); the honest
   counter is that a recovery mechanism that can't tell error from correctness is a coin flip
   with extra steps.
