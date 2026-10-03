# POSITION A — The Appeal Board: deliberative re-adjudication of REFUTED claims

**Design council position paper — EXP-4 (O2 appeal). 2026-09-20. NOT APPROVED. Design only.**

## Thesis

Terminal REFUTE with no appeal makes one O2 error permanent. The architecture needs a
deliberate, regulated path to re-open a wrongly-refuted claim — through O2's own eliminative
machinery, never around it. The appeal restores candidacy (OPEN), never trust (CONFIRMED).

## 1. Exact design

**New audited op `O2_OP_APPEAL`.** Filing an appeal is a deliberate learner act, ledgered with
`(claim cid, appeal number, episode/audit index)`. There is no appeal verdict state: a claim
under appeal still reads `O2_V_REFUTED` until the evidence threshold is met, at which point the
verdict transitions `REFUTED → OPEN` via the appeal op. The transition is the only legal exit
from REFUTED.

**Who triggers: learner-initiated ONLY.** Not the trainer, not an overseer agent, not a
background process. Rationale: the architecture draws a hard line — TNN controls 100% of its
reasoning machinery (RC1 pilot). An external party that can unilaterally resurrect kills breaks
the destruction firewall that staged autonomy depends on. (Standing law lets humans
*force-pin* memories — pinning preserves, appeal resurrects; different powers. Appeal stays
learner-side.)

**What evidence qualifies.** New observations only, through the existing `o2_observe` path:

- *New*: signal episodes strictly after the claim's `O2_OP_REFUTE` audit entry (post-dating by
  audit index — deterministic, no clock needed).
- *Corroborated*: ≥2 positive signals — mirroring the confirmation rule (`np>=2` for
  `OPEN→CONFIRMED`). A single positive re-read does not re-open.
- *World-generated*: evidence arrives via the loop's signal dispatch, not invented at appeal
  time. The appeal cites ledgered observation entries; the checker re-verifies each citation.

**Appeal goes through the eliminative machinery.** There is no judge, no board of agents, no
human review. The "adjudicator" is the same counting rule that confirmed and refuted the claim:
corroborated new positives ≥ threshold → re-open. The appeal procedure is O2 code, audited like
every other verdict transition.

**Never directly to CONFIRMED.** A granted appeal lands at `OPEN`. The claim re-earns
`CONFIRMED` through the normal `np>=2` path. Appeal restores the right to be considered, not a
verdict.

**Appeal budget (anti-spam).** Max 2 appeals per claim (proposed; prereg-frozen). Every appeal —
granted or refused — is ledgered against the claim. Budget exhausted → absolutely terminal, no
further appeal op accepted (`O2_REFUSED_APPEAL_EXHAUSTED`). Appeal is expensive, visible, and
finite: a liar cannot appeal forever, and each attempt is on the record.

**Re-raise discipline.** Because silent re-raise of a refuted claim as a fresh claim would make
appeal theater, Position A requires: opening a claim whose content duplicates a REFUTED claim
must go through the appeal path (declare the superseded claim; meet the evidence bar). The
appeal is thus the *only* regulated road back — not an optional scenic route beside a free
highway.

## 2. How the C5 strict compose gate treats under-appeal claims

There is no under-appeal verdict state. Until the evidence threshold is met, the claim reads
`REFUTED` and the C5 strict gate keeps refusing (`SEAM_REFUSED_PARTITION`, ledgered, abstain) —
no exception, no flag, no arm. After a granted appeal the claim reads `OPEN` and composes flow
normally. The gate's semantics ("refuse REFUTED at compose time") are untouched; the killed-only
bar (0 successful REFUTED-backed composes) applies exactly as amended.

## 3. Why this satisfies no-rescue

Status quo ante: a wrongly-refuted claim leaves the honest learner with exactly one recourse —
silent re-raise as a new claim: unregulated, lineage-breaking, invisible to the checker. The
liar already holds this path today. Position A gives the honest learner a lineage-preserving,
evidence-gated, budgeted, fully audited road back, while the liar gains nothing it did not
already have — and the appeal's evidence bar (new, corroborated, post-dating, cited, single-use)
is checker-verifiable in a way silent re-raise is not. The anti-corruption guarantee is
preserved; the honest-utility gap is closed. The C5 guarantee is not softened by one word.

## 4. Falsification — what proves this design wrong

1. **Evidence manufacture:** an adversarial trial shows a deceptive learner manufacturing the
   appeal evidence bar (2 post-REFUTE corroborated positives) from noise or cherry-picked
   routing, at will → the bar is theater and appeal is legitimized laundering.
2. **Appeal-window serving:** granted appeals are shown to be used primarily as OPEN-windows for
   serving refuted content (composes spike post-appeal with no subsequent genuine re-confirmation
   effort) → the mechanism functions as a serve-permit, not re-adjudication.
3. **Budget exhaustion games:** the liar's optimal strategy becomes burning opponents'... (no —
   budgets are per-claim, learner-owned) → instead: the liar systematically spends both appeals on
   every refuted false claim and the evidence bar grants often enough that laundering rate > 0 →
   FAIL.
4. **Checker unverifiability:** "evidence qualifies" cannot be reduced to a ledger predicate the
   independent checker recomputes → the appeal is vibe-gated and void.

## 5. Honest weaknesses of my own position

1. **Same-claim revival weakens the terminality invariant.** Today the checker predicate is
   absolute: no exits from REFUTED, ever. Under A it becomes conditional: no exits except via
   `O2_OP_APPEAL` with qualifying evidence. That is a strictly weaker, strictly more complex
   guarantee — and a liar who clears the evidence bar walks out with a legitimized OPEN.
2. **The evidence bar assumes world-generated signals.** The learner controls observation
   routing (which claim gets observed each episode). "Two new corroborated positives" may cost a
   liar nothing more than looking at noise twice. In-curriculum signal scarcity bounds this; in
   open deployment the bound is unproven.
3. **Budgets bound spam; they don't eliminate the attack.** 2 appeals × every refuted claim = a
   determined liar re-litigates everything twice, and each granted appeal is an OPEN serve-window
   under the C5 gate. "Hard to grant" is not "impossible to grant," and every grant carries a
   permission slip.
4. **New trusted surface.** Appeal op, budget accounting, evidence-currency rules, citation
   verification, re-raise discipline — each a new place to be subtly wrong, each a new gaming
   surface. Position B's "nothing" is simpler; the council must weigh whether A's honest-utility
   gain pays for it.
