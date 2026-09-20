# RC2 COUNCIL VERDICT — 2026-09-20

Four debaters, one per open question from `PREREG_RC2_DRAFT.md` §5. All
debates were held against Micah's binding scaling law: scale-dependent
quantities parameterized per leg, genuine constants frozen. Nothing was
run; this is analysis. The council reached **no deadlocks** — all four
questions resolved in favor of the draft, with two implementation notes.

## Q1 — Is RC2 the 10× scale leg, or should elimination-strictness go first?

- **Options debated:** (a) RC2 = 10× scale leg as drafted; (b) elimination-strictness parameter class first (renamed), 10× after.
- **Key evidence:** RC1's only evidence is 12 episodes/phase; the program's own history (felt-trial failure, table-learner 357-switch storm) says scale is where claims die — scale is the higher-priority falsification. Elimination strictness is a genuinely new parameter needing its own prereg regardless; running it first means bolting new behavior onto a 12-episode toy, then scaling both at once — the exact confound the scaling law exists to prevent.
- **Recommendation:** 10× scale leg first, as drafted. The parameter class keeps its own name and prereg whenever it runs; ordering is free, and scaling the proven machinery first is the safer falsification order.
- **Needs a trial:** the empirical predictions themselves (pred_refusals 40, S_b = 370 at 120 episodes) — that is what the scale leg is for.

## Q2 — Approve the designed defect sets (§3a)?

- **Options debated:** (a) approve the regular mod-3/mod-4 rules; (b) deterministic-but-irregular sets in RC1's hand-picked spirit.
- **Key evidence:** Positional regularity is causally inert in this loop. Defect detection is a designed property (RC1's honest boundary); the sim predicts from replayed records, never positions; refusal counts follow defect counts, which are preserved exactly (40/120, 40/120, 10/40). No inspect/propose/commit/refuse/gate path consumes item positions. A mod rule also fits the scaling law better than a hand-picked enumeration — it is parameterized and leg-generic.
- **Recommendation:** Approve §3a. **Implementation note:** parameterize (offset, modulus) per scale leg in code rather than inlining 3/4 as literals, to satisfy the law's letter.
- **Needs a trial:** only if a future design gives the learner a position-consuming path — then regular-vs-irregular becomes an empirical head-to-head. Within RC2, analysis settles it.

## Q3 — Approve RC_SMAX 150→1500 and the no-cap ledger window?

- **Options debated:** 1500 vs a tighter value (e.g., 400); no-cap window vs cap now.
- **Key evidence:** Verified against the trial source (`rc_trial.zag` line 53, clamps at 125/305): RC1 S_b = 50 + 4×8 = 82 (cap never bound). RC2 S_b = 50 + 40×8 = 370. At RC_SMAX=150 the cap would clamp at 150 after 13 refusals and the S_b check fails mechanically — the bump is required by arithmetic, not judgment. Any cap ≥ 371 produces a bit-identical run, so 1500 vs 400 is observationally indistinguishable; 1500 = 150 × scale factor is the most mechanical parameterization. The no-cap window keeps the mechanism faithful; ~1,420 audit entries vs the retained 2048 cap (with a pre-registered 4096 bump rule past 1,800) is trivially fine.
- **Recommendation:** Approve RC_SMAX=1500 **recorded as a per-leg parameter (RC1 value × scale factor), never re-frozen as a constant** — documentation discipline so S100 doesn't inherit it as law. Approve the no-cap window.
- **Needs a trial:** nothing about the cap value — analysis is the whole story. Two things analysis can't settle: whether the uncapped window stays honest at 100× (the S100 leg answers empirically), and whether a window cap changes behavior at all (a mechanism question needing its own dedicated trial).

## Q4 — Approve deferring the capped-window mechanism?

- **Options debated:** defer to a follow-up vs include the cap in RC2 now.
- **Key evidence:** A cap is a new mechanism (bounded memory / forgetting behavior), not a scale parameter — the scaling law says changing machinery mid-leg violates it. Combining scale-up AND new forgetting behavior in one leg destroys attribution: a failure couldn't be blamed on scale vs forgetting. There is no capacity need at 10× (~1,420 entries, sim replays 120 episodes O(n)). The cap would also touch program law ("no bounded LLM-style context window") — law-touching changes need their own prereg with their own bars.
- **Recommendation:** Approve the deferral. RC2 stays the faithful 10× scale leg with unbounded ledger — one variable isolated.
- **Needs a trial:** everything about the cap's behavior — the follow-up prereg must specify window size and binding rule (FIFO? importance-ranked? deliberately chosen?), eviction authority, audit treatment of evicted entries, and bars for correct behavior when the window binds. Run it as a standalone leg at the same 10× scale so results compare against RC2's unbounded baseline.

## Summary for Micah

Approve all four as drafted, with two implementation notes folded in: (Q2) parameterize defect (offset, modulus) per leg in code; (Q3) record 1500 as a per-leg parameter (150 × scale factor), not a new constant. Nothing needs a trial to settle before approval — every empirical remainder is exactly what the approved legs will measure.

---

## Appendix — dissenting notes (strongest opposing case per question, overruled)

- **Q1 minority:** Reasoning control is only proven for bar-strength (V) and reinforcement (R); elimination strictness is the first parameter touching judgment *quality*, arguably the most load-bearing control TNN needs. Validating the op/gate machinery's generality cheaply at 12 episodes first would test something a pure scale leg cannot. Overruled: generality at toy scale still leaves the scale question open, and stacking new-mechanism-then-scale is the worse confound.
- **Q2 minority:** A mod rule is a learnable regularity — a cheat affordance if indices ever enter learner records — and RC1's spirit was an adversarial-looking world. Overruled: no position-consuming path exists in RC2; guarding it adds audited machinery for zero change in any measured observable.
- **Q3 minority:** 1500 grants 4× headroom with no basis; a tighter cap (400) would keep the guard functional and catch refusal-count bugs. Overruled: the exact-value S_b=370 check already surfaces refusal-count changes, and the cap's guard role was never exercised in RC1 either (82 < 150) — headroom beyond 370 is inert. The point stands only as documentation discipline (adopted).
- **Q4 minority:** The cap is *the* scale-relevant mechanism; a "faithful scale leg" that never pressures memory may prove nothing about scaling, and the "no bounded context" law — what most distinguishes TNN from LLMs — goes untested under pressure. Overruled: pressure without a preregistered mechanism is just an uncontrolled confound; the law deserves its own trial, not a bundled afterthought.
