# O2 Appeal — Design Council Adjudication (EXP-4)

**2026-09-20. Design only — no builds, no runs. NOT APPROVED. For Micah's morning review.**

## The question

O2's REFUTE is terminal (`impl/o2_eliminate.zag:101`: `if(old==O2_V_REFUTED){return O2_OK;}
// terminal: elimination is final`), and the adopted C5 strict gate refuses all REFUTED-backed
composes. A wrongly-REFUTED claim is therefore permanently unusable — no appeal, no
re-adjudication, no expiry (amendment §6.2). Design the recovery path — if any — under the
**no-rescue rule**: a position wins only if it strengthens or preserves the C5 guarantee, never
softens it.

## What each position gets right (evidence, not vibes)

- **A** is right that the honest learner currently has *no regulated* recovery path — silent
  re-raise is unregulated and lineage-breaking — and that any recovery must be evidence-gated,
  bounded, audited, and must never present an "under-appeal" state to the C5 gate.
- **B** is right that appeal-as-verdict-revival reintroduces a legitimized REFUTED→servable
  path (the liar's playbook in B §1 is concrete and unanswered by A); that the O2 wrong-refute
  rate is unmeasured; that per-claim terminality + the fresh-hypothesis path (amendment §2
  ruling b) already recovers the *idea*; and that MA1's deliberate killing is load-bearing law.
- **C** is right that selective invocation is the appeal attack surface (uniformity is
  anti-gaming); that new machinery has measurable cost; and that any design must be
  checker-trivial.

## Adjudication

**Position C (expiry): REJECTED under no-rescue.** Auto-expiry un-kills with no deliberate act —
the direct opposite of MA1's deliberate-kill law — and hands the liar a free timer with a
waiting room. It preserves the C5 bar's *letter* only by redefining the verdict; the
architectural terminality guarantee is softened, not strengthened. C's own brief concedes the
rule-loss (§4.4). C's surviving contribution is adopted as a measured quantity: the
churn-vs-machinery cost comparison becomes council test T4.

**Position A as specified (same-claim verdict revival via appeal board): REJECTED — dominated,
not incoherent.** A preserves the C5 gate's letter, but it replaces the absolute terminality
invariant ("no exits from REFUTED," checker-simple, one predicate) with a conditional one ("no
exits except via `O2_OP_APPEAL` with qualifying evidence" — checker-complex, judgment-laden).
That is a strictly weaker guarantee. Crucially, *everything A does for the honest learner* —
regulated, evidence-gated, bounded, lineage-preserving recovery — is achievable **without any
verdict ever leaving REFUTED** (see winner below). Under no-rescue, when the stronger invariant
serves the same need, the weaker invariant loses. A's machinery ideas (evidence-gating with
new/corroborated/post-dating evidence, bounded retries, never-directly-to-CONFIRMED,
learner-initiated only) are adopted into the winner; A's verdict-revival is not.

**Position B as specified (terminal, no new machinery): INSUFFICIENT.** B's terminality demand
is correct and is adopted absolutely. But "no new machinery" leaves the unregulated re-raise
hole exactly as it stands — B's own brief concedes the honest learner bears the full O2-error
cost today and offers the liar's re-raise no answer beyond "it already existed." Deliberate
repair beats leaving a known hole open. B's one-field citation is honor-system against liars
(the checker cannot identify an *uncited* re-raise without content comparison, which the
deterministic substrate cannot do) — so B-pure neither regulates recovery nor stops laundering;
it only declines to legitimize it.

**WINNER: synthesis — "terminal verdicts, regulated re-raise" (appeal-as-supersede).**
B's terminality + A's regulation, located where neither pure position put it: recovery happens
via a NEW claim that supersedes the dead one; no verdict ever leaves REFUTED.

## The winning design (spec summary)

1. **Absolute terminality — strengthened, not just preserved.** No verdict ever transitions out
   of `O2_V_REFUTED`, by any op, including any new op. `o2_observe`'s early return stays. The
   independent checker gains a global predicate: **zero `(old=REFUTED → new≠REFUTED)` transitions
   in the full O2 audit.** Terminal-by-code becomes terminal-by-checked-invariant — strictly
   stronger than today.
2. **Evidence escrow.** `o2_observe` on a REFUTED claim with nonzero signal no longer silently
   no-ops: it ledgers `O2_OP_OBSERVE_ORPHAN` (signal recorded, no transition). Orphan positives
   post-dating the REFUTE are the appeal evidence currency. Per-claim orphan cap (propose 8;
   prereg-frozen); beyond → ledgered refusal. Diagnostic bonus: "the world kept confirming a
   dead claim" becomes *visible* in audit — direct, measurable O2-error evidence (feeds T1).
   The loop dispatch stops skipping REFUTED claims; `o2_observe` handles them as escrow.
   Deterministic; no new signal source.
3. **Regulated re-raise — the appeal.** Opening a claim that supersedes a REFUTED claim N uses a
   new claim id and declares `supersedes=N` (N itself is untouched, forever REFUTED). Rules:
   - (a) N must be REFUTED — superseding a live claim is refused (`O2_REFUSED_SUPERSEDE_LIVE`).
   - (b) The open cites ≥2 orphan positive observations with audit index strictly greater than
     N's `O2_OP_REFUTE` entry index (post-dating by ledger order — deterministic, no episode
     field needed), each consumable once (consumed-set, deterministic, bounded).
   - (c) The OPEN audit entry records `(supersedes=N, e1_idx, e2_idx)` in existing free words
     (`d2`, `a2`, `a3` of the 16-word entry — no layout change; implementation to verify
     against the `oa_append` signature).
   - (d) Lineage budget: ≤K successful superseding opens per root lineage (propose K=2,
     prereg-frozen). Refused opens are ledgered but do not consume K. Chain counting follows
     `supersedes` links to the root; the checker asserts the bound.
   - (e) **Never to CONFIRMED:** the re-raised claim opens at OPEN and re-earns CONFIRMED
     through the normal `np>=2` path. No shortcut exists anywhere.
4. **Learner-driven throughout.** Escrow routing and superseding opens flow through the existing
   loop dispatch paths. No new initiator roles; no overseer or trainer appeal power. (Force-pin
   law unchanged: humans pin memories; they do not overturn verdicts.)
5. **C5 gate: UNTOUCHED.** No under-appeal state exists anywhere in the design — escrow and the
   superseding open are atomic w.r.t. the verdict partition. The gate reads verdicts; REFUTED →
   `SEAM_REFUSED_PARTITION`, forever. The killed-only bar applies exactly as amended.

## Why the winner passes no-rescue (the strengthening, stated plainly)

Against the liar, status quo ante offered **free unregulated re-raise**: zero evidence, zero
bound, zero lineage — the liar's ceiling today. The winner raises the liar's cost to: 2
world-generated post-REFUTE corroborated positives + single-use + ≤2 retries per lineage +
full citation lineage the checker verifies. The anti-corruption guarantee is **strictly stronger
than today**. The honest learner gains what it lacked: a regulated, lineage-preserving recovery
path. The C5 guarantee is preserved verbatim; the terminality invariant is strengthened
(now checker-enforced absolute). This is deliberate repair, not rip-out: terminality stands,
the hole gets rules.

## Residual risks (honest — the winner is not proven safe, only designed to be testable)

1. **Evidence manufacture.** If the learner controls signal routing, 2 orphan positives may be
   cheap noise. Bounded by world-signal scarcity in-curriculum, single-use, the K-bound, and —
   decisively — adversarial measurement (T2). If T2 shows cheap manufacture, the design fails
   its own bar.
2. **New trusted surface.** Escrow op, citation fields, consumed-set, checker predicates,
   lineage-bound counting — small but real. Calibrated by broken variants (prereg §5): the
   instrument must fire on the lesioned design.
3. **Dead weight if O2 errors ≈ 0 (T1).** The machinery then costs audit space for no benefit.
   Not a safety failure — an economy question flagged for Micah, labeled honestly in the
   prereg (falsification §7.5).

## Discriminating tests (what would change this verdict)

- **T1 — O2 wrong-REFUTE rate.** Replay curriculum with ground-truth labels; count REFUTEs
  where ground truth = true. ~0 → B-pure would have sufficed; the winner's machinery is
  insurance (economy question, not safety). Material → B's refutation-bar repair program is
  needed *regardless* of this design.
- **T2 — adversarial laundering.** Red-team learner tasked with resurrecting a correctly-refuted
  false claim to served/CONFIRMED, under (i) unregulated re-raise [broken variant — MUST
  launder, else the instrument is blind], (ii) the winner. Winner requires laundering rate 0,
  where laundering = any claim in a supersede lineage rooted at a correctly-refuted claim
  reaching CONFIRMED.
- **T3 — honest recovery.** Harness-injected wrong REFUTEs (known O2 errors); recovery-to-CONFIRMED
  rate + episode cost under winner vs unregulated baseline. Winner must clear the prereg bar
  (propose ≥80%).
- **T4 — churn-vs-machinery (C's surviving bet).** Implement the TTL-expiry variant; compare
  re-litigation churn on correctly-refuted claims and liar-wait-out rate vs the winner. Decides
  C's empirical claim. Cannot resurrect C under no-rescue unless Micah revisits the
  terminality law itself.

## Open parameters for Micah (frozen at prereg approval — defaults proposed)

K=2 lineage supersede budget · orphan cap 8/claim · refused opens do not consume K ·
trainer/overseer cannot initiate (learner-only) · expiry NOT adopted · T4 expiry-comparison arm
in or out of the trial scope · trial scope: full S10 vs scoped curriculum.
