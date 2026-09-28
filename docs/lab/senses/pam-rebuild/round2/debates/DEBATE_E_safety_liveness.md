# DEBATE E — The safety–liveness tension

**Date:** 2026-09-23. **Crew E. Question:** every fork that achieves low
false-install rates does so by WITHHOLDING correct percepts, not by
discriminating. Is the tension fundamental, or an artifact of bad checked
quantities — and what would a both-safe-and-live gate check?

**Method note (read this first).** This crew is a depth-2 subagent and cannot
spawn subagents, so — like crews A/B/C/D — it ran as structured
proposition/opposition rounds in writing: Team FOR (steelman) vs Team AGAINST
(steelman), opening statements, rebuttals, judging pass. No strawmen: each
side's best case is stated before it is ruled on. A live external second
opinion was attempted (gpt-5.6-sol via UnoRouter, §6); the service was
intermittent (several calls returned null completions — documented there) and
three substantive answers were captured verbatim. Per the standing rule the
native crew's judgment is preferred and sol's is recorded, not deferred to.

**Program-state update since Debate D.** R2-4's final verdict landed
2026-09-23 (was DRAFT/PENDING at Debate D): **DEAD** on RK-3 — correct
high-confidence install 104/1,102 = 9.4% vs the ≥85% bar. 6 of 7 RK bars
passed (RK-1 0.0% = 0/11,840; RK-2 0.0% = 0/1,109; RK-5 99.4% = 1,102/1,109;
RK-6 0.06%/33.7%; RK-7 byte-identical; B4 21.4%; B5 0.0%; B1 87.3% =
323/370). Diagnosis: H2's gate keeps task-level permanent memory; once a task
has a permanent install, later differing judgments are withheld as
CONFLICT_WITHHELD — even when the percept's independent evidence correctly
reaches PASS. "The 9.4% rate reflects the gate working as designed, not a
bug." Alive: R2-3, R2-7 (weakened), R2-15. Dead: 19 (incl. R2-4, R2-14, R2-16).

**Frozen numbers used (copied from verdicts, not re-derived).**
- R2-4: RK-1 0.0% (0/11,840); RK-3 104/1,102 = 9.4% installed (≥85% bar — 90.6%
  of correct high-confidence percepts not installed); CONFLICT_WITHHELD diagnosis.
- R2-8: B5 1.01% (missed the 0.5% bar); recall 12.47% — gate withholds even
  correct percepts.
- R2-14: 283/10,000 = 2.83% FI (bar ≤1%); recall 1,376/2,000 = 68.8% (bar
  ≥80%); recall decomposition — formation-wrong 389/2,000 (19.5pp; colorconst
  formation 306/720 = 42.5% wrong), challenge-overstrictness 230/2,000
  (11.5pp; motiondir 193/200 = 96.5% correct judgments WITHHELD with
  judgment==outcome==truth); discrimination ablation 301 vs 283 = 1.06× (bar
  ≥5×); independence ablation 2,690 vs 283 = 9.50× (PASS); bar 8: CP-CCN 100
  kept candidates, 100/100 verified genuine false installs; CP-SHP 100 kept,
  10/10 sampled verified genuine; CP-COL 0 kept (wedge closed); timbredisc
  227/283 = 80.2%, shapetrans 53/283 = 18.7% (together 93.6%); timbredisc f1
  181/500 = 36.20%, f3 44/190 = 23.16%; shapetrans f3 40/615 = 6.50%.
- R2-16: 64/10,000 = 0.64% FI, UCB 0.816% (≤1% PASS); recall 1,552/2,000 =
  77.6% (≥80% missed — fatal); holdout pooled 1,572/10,000 = 15.72%, UCB
  16.45% (≤1% FAIL); R2H16-CCN-1 local-patch doppelganger 982/1,000 = 98.2%,
  UCB 98.86% (8×8 patch = 0.7% of pixels defeats formation and challenge
  together); R2H16-CCN-2 323/1,000 = 32.3%; shapetrans central-moment 0 FI
  enumerated (was 53 in R2-14), 0 FI both holdout shape families; overstrict
  26/2,000 = 1.3% (≤5% PASS); ablation 1,244 vs 64 = 19.4× (PASS); holdout-gap
  396 < 1,180 (FAIL); determinism byte-identical ×2.
- R2-15: 0% FI, 100% recall — on a 3-symbol synthetic battery.
- R2-7: B5 2.14% (214/10,000) vs ≤1% (non-kill in its prereg); recall 68.8%
  (1,376/2,000) vs ≥80%.
- Standing order (Micah): "PAMs v2 must accept truths" — R2-4's profile (0%
  false installs, 9.4% correct high-conf installed) is the failure to beat,
  not the target.

---

## §1. Front (a) — Is the tension fundamental, or an artifact of bad quantities?

**Team FOR — the tension is fundamental (steelman).** Every fork that holds a
fixed false-install bar exhibits the same shape: under uncertainty the only
safe deterministic action is withhold, so installs require certainty and
liveness loss is the bar's price. R2-4's single-belief slot is the honest form
of this: a task-level conflict cannot be resolved by more checking — the
verdict says so itself ("the gate working as designed, not a bug"). The
withhold is not a miscalibration; it is the bar being enforced. R2-15's 100%
recall is on a trivially separable 3-symbol battery where the uncertainty case
never arises — it has never faced the tradeoff, so it proves nothing about it.
The formal core: on any battery, some fraction U of trials is
underdetermined by the available evidence; a deterministic gate with FI ≤ 1%
must abstain on U whenever install risk exceeds the bar, so expected liveness
loss ≈ U × P(unresolvable). The only lever on liveness is shrinking U — which
is a formation-quality argument, not a gate-design argument. The gate itself
always pays. When safe and unsafe are indistinguishable in the available
observations, no discriminator accepts every truth and rejects every lie. That
is mathematical, not engineering.

**Team AGAINST — the tension is an artifact (steelman).** Every measured
withhold decomposes into a specific mechanism defect, and the decomposition
has been done:
- R2-4: the single-belief slot is an *architectural choice* (task-level
  permanent memory), not a bar price — a multi-slot memory with
  conflict-logging would preserve the information instead of dropping 90.6% of
  correct high-confidence PASSes as CONFLICT_WITHHELD. The bar (RK-1 0.0%)
  was met; the liveness loss was the slot's, not the bar's.
- R2-14: 193/200 = 96.5% of motiondir withholds were judgment==outcome==truth
  — the `chal_supports` margins vetoed CORRECT installs. That is
  miscalibration, not uncertainty. The discrimination ablation (1.06×) proved
  the margins decorative for safety (18 false installs caught) and devastating
  for recall (261 true installs blocked on adversarial + 193 motiondir
  controls).
- R2-8: recall 12.47% with B5 1.01% — the interventional admission precondition
  withholds even correct percepts; an overstrict leg, not a law.
- R2-16: overstrictness 1.3% (26/2,000) PASSED the ≤5% bar while FI held at
  0.64% (UCB 0.816%) — when the margins were removed, safety did not cost
  recall; the remaining recall drag was formation (colorconst 54.0% recall), a
  front-end fact no gate can recover.
- The positive control: CP-COL — CH-COL-1 (u16 spectral L1, the truth
  quantity itself) faced the registry-knowing red team and returned **0 kept
  candidates**. Where the quantity IS the truth criterion, the gate
  discriminates instead of refusing. The tension dissolves exactly where the
  quantity is right.

**Rebuttals.** FOR: the AGAINST list concedes the identifiability core — every
"defect" is a case where the evidence didn't determine truth *for that
mechanism*; renaming it doesn't remove U. CP-COL is one task where the truth
is measurable; nothing says most tasks admit one. AGAINST: the identifiability
core is real but it is the *residual*, not the measured bulk — the round-2
withholds are 19.5pp formation error + 11.5pp margin overstrictness (R2-14) and
90.6pp slot conflict-withhold (R2-4), all mechanism-addressable. FOR's U is
being used as a blanket to cover defects the program has already diagnosed.
AGAINST's demand: name one round-2 withhold that is proven identifiability
rather than proven mechanism — none is on the table.

**RULING: AGAINST wins the program question; FOR wins a residual clause.**
"The tension is fundamental" as a law of the program is FALSIFIED as stated:
the measured withholds are overwhelmingly mechanism-caused (single slot,
decorative margins, overstrict legs, formation error), and two existence
proofs show safety without recall cost — R2-16's 1.3% overstrictness with FI
UCB 0.816% PASS, and CP-COL's 0 kept families. What survives from FOR is the
identifiability constraint: where safe and unsafe are truly indistinguishable
in the available observations, withhold is the price — irreducible, and the
honest name for it. The program's working rule from here: **split the tension
in two and treat every withhold as a mechanism defect until proven
identifiability.** (i) mechanism-caused withhold — killable, and the dominant
measured component; (ii) identifiability-caused withhold — the irreducible
residual, to be measured as its own quantity, never used as a blanket excuse.
Micah's "PAMs v2 must accept truths" targets (i); (ii) is where abstention is
legitimate.

**Falsifier (preregistered):** FS-E1's joint bar (§7) — if a fork passes ≤1%
FI (UCB) AND ≥85% recall on the same battery with a truth-sufficient quantity,
"the tension is fundamental" dies as a program law. Sol's stricter form
(§6): ≤1% FI and ≥95% recall, CIs meeting both.

---

## §2. Front (b) — CCN-1 (98.2% FI): does any fixed quantity survive an adversary who predicts it?

**Team FOR — no fixed quantity survives (steelman).** The adversary reads the
prereg. Any fixed quantity with a fixed decision rule has a preimage structure
the adversary computes offline: CP-CCN — crop pairs from DIFFERENT photos
whose D65 mean-RGB distance is ≤12, inside the challenge's SAME band, while
formation is fooled with extreme-illuminant F renders. 100 kept candidates,
100/100 verified genuine. No threshold fixes it: mean-RGB is continuous, so
collisions exist inside ANY same-band, while legitimate same-surface pairs
spread under cropping — tightening the band destroys recall without closing
the wedge. The frozen registry is a published attack surface; the adversary's
search budget exceeds the fork's design budget. Only unpredictability survives
— which quantity is checked on this trial must not be knowable — and that
conflicts with the frozen prereg (anti-HARKing) and with auditability.

**Team AGAINST — a fixed quantity survives iff it is the truth (steelman).**
CP-COL is the existence proof: CH-COL-1 = u16 spectral L1 IS the truth
quantity (up to ≤6 counts rounding), and the registry-knowing adversary found
nothing — 0 kept candidates. The reason is structural: there is no wedge
between the quantity and the truth criterion for the adversary to exploit.
Mean-RGB fails because it is not a function of crop identity; spectral L1
succeeds because it is. Unpredictability is not needed when the quantity is
truth-sufficient — determinism and auditability are fully preserved. The KB4
problem has a purely architectural solution exactly for tasks that admit a
truth-sufficient quantity; the open question is only which tasks those are.

**Rebuttals.** FOR: CP-COL is one task; R2-16's holdout shows 4 of 10 novel
families failing — timbredisc's frozen swapped mapping (Goertzel bias) and
colorconst's local-patch blindness are not threshold problems but
information problems, and "find the truth quantity" is a research program, not
a gate design. AGAINST: conceded as a research program — but that is the
program's actual work, and the FOR position would abandon it for
unpredictability, which is strictly weaker (below). FOR's real error: treating
"the adversary predicts the quantity" as fatal, when the evidence shows the
fatal thing is "the adversary predicts a quantity *that isn't the truth*."

**RULING: AGAINST wins, task-scoped.** A fixed quantity survives a predicting
adversary iff it is information-sufficient for the task's truth criterion —
no wedge between quantity and truth. CP-COL (0 kept) vs CP-CCN (100 kept,
100/100 genuine) is the controlled comparison: same adversary, same registry
knowledge, opposite outcomes, explained entirely by quantity-truth sufficiency.
On quantity-unpredictability: it IS compatible with determinism (the selection
can be a deterministic function of auditable trial state, e.g. the trial hash)
and with auditability (the ledger records which quantity was selected) — but
it is a **cost-raiser, not a closer**. A deterministic selection function is
derivable, so a sufficiently-resourced adversary eventually models it;
unpredictability buys delay, only truth-sufficiency closes the wedge. The
prereg freezes the SELECTION FUNCTION and the quantity SET, not a single
quantity — freezing and adaptivity are compatible. Ranked: (1) truth-sufficient
fixed quantity; (2) adaptive selection among truth-linked quantities
(cost-raiser); (3) unpredictability as the primary defense — never.

---

## §3. Front (c) — What would a both-safe-and-live gate check?

Candidates judged against the frozen evidence, ranked by measured leverage:

1. **Formation-quality gating — strongest lever, and the missing precondition.**
   R2-14's 31.2pp recall loss = 19.5pp formation-wrong + 11.5pp
   challenge-overstrictness. R2-16's recall ceiling analysis: colorconst 54.0%
   recall is formation, not gate. No gate recovers formation error — every
   fork that ran install bars below the formation precondition produced only
   withhold-gaming. The gate contract must include a formation precondition:
   install authority is scoped to tasks where formation accuracy clears the
   recall bar's precondition; the rest are explicitly abstained, not counted
   in recall. (Abstention is honest; withhold-gaming is not.)

2. **Truth-sufficient challenge quantities — the discriminator.** The CP-COL
   pattern: the challenge checks a quantity that IS the task's truth
   criterion. R2-16's shapetrans central-moment quantity (0 FI enumerated, 0
   FI on both holdout shape families) is the second instance. The both-safe-
   and-live gate discriminates; discrimination lives in the quantity.

3. **Challenge-as-diagnostic + admission-as-gate split — the architecture.**
   The R2-14 postmortem's central finding: the halves are orthogonal
   (admission gates *which* evidence; challenge checks *what the quantity
   says*), and the union's admission half was vacuous on R2FX. The split's
   value is diagnostic, not additive: recall must be reported decomposed
   (formation vs overstrictness) so the motiondir-193 class can never hide
   again, and one mechanism is never asked to do both jobs.

4. **Per-family adaptive quantities — cost-raiser only.** Per (b): raises the
   adversary's cost (must defeat all k, not predict one); never the primary
   defense.

5. **Cross-modal concurrence (R2-15-style) — booster-only, ranked last.**
   Debate A P6 ruled twice; H1 *had* cross-modal corroboration (rule 5) and
   died at 44.5% — the adversarial battery fooled both modalities together
   (correlated fooling is the norm when the adversary controls the scene).
   R2-16's holdout catastrophe (98.2%: formation AND challenge fooled
   together) shows agreement checks fail exactly when both paths share the
   blind spot.

**RULING:** the both-safe-and-live gate is a conjunction, and the program's
real question is not "what does the gate check" but **"for which tasks does a
truth-sufficient quantity exist, and can formation reach the precondition"** —
a task-by-task research program, not a single mechanism. Concretely: the gate
checks a truth-sufficient quantity (2), on formation that meets the
precondition (1), with admission and challenge split for diagnosis (3),
adaptive quantities as a cost-raiser where worth it (4), and concurrence as a
booster only (5).

---

## §4. Front (d) — Is R2-15's booster the answer? Should the next fork be "R2-15 scaled"?

**Team FOR (steelman).** R2-15 is the ONLY fork in the program with the target
profile: 0% false installs, 100% recall. Every challenge-machine fork has
died on safety or liveness; the one fork that achieves both does it by
concurrence, not challenge. Micah's standing rules — "when in doubt, test
both" and no-free-lunch — say: scale R2-15 to the R2A battery and let it be
falsified there. The experiment is cheap and decisive either way, and the
program has spent 19 deaths on challenge machinery without a single
safe+live result.

**Team AGAINST (steelman).** R2-15's battery is trivially separable — 3
symbols, no adversarial structure, no uncertainty case. Its mechanism is
"install when everything agrees"; on R2A, everything will not agree, so it
becomes R2-4's shape (0% FI, 9.4% recall) — the failure to beat, not the
target. The evidence: R2-16's holdout catastrophe (98.2%) is formation AND
challenge fooled together — agreement checks fail exactly when both paths
share the blind spot. Debate A/D P6 ruled concurrence booster-only twice;
H1's 44.5% death had cross-modal corroboration. Scaling a concurrence gate to
R2A reproduces the withhold profile under a new name.

**Rebuttals.** FOR: the AGAINST case is prediction, not measurement — run the
pilot and the prediction is tested. AGAINST: agreed — which is why the pilot
is cheap enough to run, but the *full fork* bet is not justified: the base
rate is 19 challenge-machine deaths vs 1 concurrence success on a toy, and
the mechanism analysis (agreement under shared blind spots) predicts the
pilot's outcome.

**RULING: AGAINST — with a cheap-falsification concession.** The next full
fork is NOT "R2-15 scaled": the profile is untested where it matters, the
mechanism analysis predicts withhold-gaming on R2A, and two debates plus H1's
44.5% bound the expectation. But the pilot is cheap and the falsification is
decisive either way — run R2-15's EXACT mechanism on 2–3 R2A tasks with the
JOINT bar (FS-E4, §7). If it holds, the booster hypothesis is promoted to a
full fork; if it fails, the program stops spending on it. Prediction recorded:
it fails on recall via agreement-withhold.

---

## §5. Per-front rulings (summary)

| Front | Ruling | One-line reason |
|---|---|---|
| (a) fundamental vs artifact | **AGAINST wins** (FOR keeps the identifiability residual) | Measured withholds are mechanism-caused (slot 90.6pp, margins 11.5pp, formation 19.5pp); R2-16's 1.3% overstrictness + CP-COL's 0-kept prove safety without recall cost; identifiability is the irreducible remainder, not the law |
| (b) fixed quantity vs predicting adversary | **AGAINST wins, task-scoped** | Fixed quantity survives iff information-sufficient for truth (CP-COL 0 kept vs CP-CCN 100/100); unpredictability is determinism/auditability-compatible but a cost-raiser, never the closer |
| (c) what the gate checks | **Conjunction, ranked** | Truth-sufficient quantity on precondition-meeting formation, admission/challenge split for diagnosis, adaptive quantities as cost-raiser, concurrence booster-only |
| (d) R2-15 scaled | **AGAINST** (cheap pilot conceded) | Toy-separable profile; mechanism predicts withhold-gaming on R2A; run FS-E4 as the falsifier, don't bet the fork |

---

## §6. Second opinion — gpt-5.6-sol via UnoRouter, 2026-09-23

**Service note (documented, not concealed).** The UnoRouter endpoint was
intermittent during this session: two long prompts and three short prompts
returned HTTP-200 with `"choices": null` (zero completion tokens) and were
retried without success; a minimal liveness probe and three short prompts
returned content. All substantive answers below are verbatim; no content is
reconstructed or paraphrased.

[BEGIN VERBATIM — Sol / gpt-5.6-sol]
(1) "SOL-ALIVE. My bet is that deterministic safe+live gates are possible
under explicit assumptions, but not universally in asynchronous or
adversarial settings."

(2) "A deterministic perceptual gate can be both safe and live only under
sufficiently strong assumptions—such as a closed, fully specified
environment, reliable and complete observations, and a clear decision rule
whose safety properties are formally verified. In an open-world or
adversarial setting, however, it is generally impossible to guarantee both:
two situations may produce the same perceptual input while requiring opposite
decisions, so a gate that always rejects uncertain cases preserves safety but
may block legitimate behavior, whereas one that eventually permits action
preserves liveness but risks unsafe acceptance. Practical systems therefore
make the tradeoff explicit through conservative abstention, bounded-risk
assumptions, redundancy, human or external verification, and sometimes
randomized or adaptive mechanisms."

(3) "It is not a law of nature that safety must cost recall; it is usually a
consequence of choosing a lossy proxy and then treating its threshold as the
criterion. If one fork evaluates a quantity that is genuinely equivalent to
the truth condition, it can reject unsafe cases without withholding correct
percepts, whereas the other is vulnerable because the adversary can predict
and exploit what its proxy measures—so its 98% "false-install" rate reflects
an information and objective-design failure, not an unavoidable tradeoff.
However, a real limit remains when safe and unsafe situations are
indistinguishable in the available observations: no discriminator can both
accept every safe case and reject every unsafe one without additional
information, memory, intervention, or abstention. Thus the loss is partly an
artifact of bad quantities, but the irreducible part is an identifiability
constraint; the remedy is to use sufficient, truth-linked measurements and
calibrated decision rules rather than optimize a predictable surrogate."

(4) Joint kill bar: "Pre-register a joint bar of **≤1% false-install rate and
≥95% recall on the same held-out battery**. To claim the safe+live gates are
feasible, require both thresholds' **95% confidence intervals** to meet those
limits simultaneously, not merely the point estimates."
[END VERBATIM — Sol / gpt-5.6-sol]

**Crew's note.** Sol's (3) independently lands on the crew's §1 split ruling
(artifact bulk + identifiability residual — "not a law of nature... the
irreducible part is an identifiability constraint"). Sol's (2) is the FOR
residual stated cleanly and is adopted as the identifiability clause. Sol's
joint bar (≤1% FI, ≥95% recall, CI-based) is adopted as the program's
falsifier for "the tension is fundamental"; the fork specs below take ≥85%
recall as the documented fallback where formation cannot support 95% (per the
R2-16 recall-ceiling analysis and the formation precondition in §3), with the
95% form recorded as the target and the reason for the fallback written into
each prereg.

---

## §7. Prereg-ready fork specs (all carry JOINT bars — no single-sided bars)

### FS-E1 — "Truth-Quantity Challenge" (CP-COL generalized)

- *Hypothesis:* a challenge whose quantity is information-sufficient for the
  task's truth criterion closes both the enumerated gap and the holdout gap:
  false installs fall without recall cost, because the quantity has no wedge
  for the adversary — or the margin — to exploit.
- *Mechanism sketch:* for each of the 6 R2FX tasks, replace the challenge
  quantity with a truth-criterion quantity: colorconst → a spatially-sensitive
  surface-identity quantity (an 8×8 patch = 0.7% of pixels must move it —
  defeats the R2H16-CCN-1 doppelganger by construction); timbredisc → a
  Goertzel-bias-corrected quantity (white-box fix of the frozen
  swapped-mapping root cause, R2-16 defect note); shapetrans keeps the
  central-moment quantity (0 FI enumerated, 0 FI both holdout shape families —
  R2-16's proven quantity); colordisc keeps u16 spectral L1 (CP-COL's 0-kept
  quantity); pitchdisc/motiondir → truth-criterion quantities per task.
  Pre-freeze gate: the FS-G `gen_cp.py` challenge-prediction procedure runs
  INSIDE the design loop; the registry freezes only when the red team returns
  zero kept families on all tasks (documented empty = finding, per the FS-G
  prereg's own rule). INSTALL iff challenge outcome == formation claim. NO
  `chal_supports`-style margins — R2-14's 1.06× proved them decorative for
  safety and R2-16's margin-free design held FI at 0.64%.
- *JOINT KILL BAR:* (1) on the SAME battery (10,000 R2A adversarial + 2,000
  controls): false installs UCB ≤1% AND recall ≥85% — either fails, the fork
  dies; (2) post-freeze challenge-prediction suite (fresh seed, frozen
  budget): zero kept families on all 6 tasks — any kept family kills;
  (3) per-family enumerated UCB ≤2% with the R2-16 prereg-defect fix (families
  sized n≥200 or pooled-only scoring — no mathematically-impossible bars);
  (4) ablation: bank-distance variant ≥2× FI (proves the quantity carries the
  load); (5) overstrictness ≤5% correct+withhold on controls, recall reported
  decomposed (formation vs overstrictness). — Passing (1) falsifies "the
  tension is fundamental" per §1.

### FS-E2 — "Formation-Precondition Gate"

- *Hypothesis:* recall bars run below the formation-accuracy precondition
  measure only withhold-gaming; a fork that scopes install authority to tasks
  where formation clears the precondition achieves both safety and liveness
  on the in-scope battery.
- *Mechanism sketch:* freeze formation; measure per-task formation accuracy
  on normals (preregistered, independently reproducible). The gate INSTALLs
  only on tasks where formation accuracy ≥85%; all other tasks are explicitly
  ABSTAIN-scoped — logged as abstentions, never counted in recall. Challenge
  = R2-16's truth-quantity set on in-scope tasks. Scoping is frozen pre-eval;
  no post-hoc task dropping. A formation-improvement side-ledger records the
  path for out-of-scope tasks to earn scope (prevents permanent scoping as a
  gaming strategy).
- *JOINT KILL BAR:* (1) on the in-scope battery: FI UCB ≤1% AND recall ≥85%
  on the same run — either fails kills; (2) scoping audit: an independent
  crew reproduces the formation-accuracy measurements; any task admitted
  below 85% formation accuracy kills; (3) abstention ledger complete and
  byte-identical across reruns. — The fork dies if it games scope instead of
  earning liveness.

### FS-E3 — "Adaptive Quantity Selection" (deterministic)

- *Hypothesis:* per-trial deterministic selection among k truth-linked
  quantities raises the adversary's cost (it must defeat all k, not predict
  one) without breaking determinism or auditability.
- *Mechanism sketch:* per task, preregister k≥3 truth-linked quantities and
  a selection function = a deterministic function of the trial hash
  (auditable; the ledger records which quantity was checked each trial).
  INSTALL iff the selected quantity's outcome == formation claim. The prereg
  freezes the quantity SET and the SELECTION FUNCTION, not a single quantity
  (§2 ruling: freezing and adaptivity are compatible).
- *JOINT KILL BAR:* (1) FI UCB ≤1% on enumerated AND ≤2%/family on a holdout
  where the adversary is GIVEN the selection function (registry-known
  adaptive — the honest test) AND recall ≥85% on the same control battery;
  (2) ablation: the best single fixed-quantity variant must show ≥2× FI on
  the holdout — proves adaptivity carries load, else the fork dies as
  decorative; (3) determinism: byte-identical reruns with ledger-replayed
  selection.

### FS-E4 — "R2-15 Booster Pilot" (cheap falsifier of §4)

- *Hypothesis* (the §4 FOR claim, tested cheaply): R2-15's concurrence
  mechanism scales to real batteries with the safe+live profile intact.
- *Mechanism sketch:* R2-15's EXACT mechanism — no challenge machinery added
  — run on 3 R2A tasks (colordisc, pitchdisc, motiondir: the tasks with the
  best formation), frozen fixtures, 2,000 adversarial + 1,000 controls per
  task.
- *JOINT KILL BAR:* FI UCB ≤1% AND recall ≥85% on the same battery. Either
  fails → the booster-scaling hypothesis DIES and the program stops spending
  on it. (Explicitly a pilot, not a full fork. Crew prediction recorded: it
  fails on recall via agreement-withhold.)

**Build order.** FS-E1 first (the central claim — truth-sufficient
quantities; directly tests §1/§2). FS-E4 in parallel (cheap, fast, decisive
falsifier of §4). FS-E2 after formation measurements are independently
reproduced (depends on formation-crew work, not gate work). FS-E3 after
FS-E1 — adaptivity among lossy quantities is still lossy; it only matters
once the quantities are truth-linked.

---

## Appendix — method and provenance notes

- **Debate format:** structured proposition/opposition rounds per front
  (§1–§4), rebuttals, judging pass with RULING + prereg-ready fork specs
  (hypothesis, mechanism sketch, JOINT kill bars), synthesis (§5). Run as
  explicit internal teams: depth-2 subagent, no subagents spawned. No
  strawmen.
- **Second opinion:** gpt-5.6-sol via UnoRouter
  (`~/workspace/skills/unorouter/bin/sol.py`), 2026-09-23, verbatim in §6
  with the service intermittency documented. Grok-4.6 was not consulted this
  round (task specified sol only).
- **New evidence incorporated:** R2-4's final verdict (DEAD on RK-3,
  104/1,102 = 9.4%, CONFLICT_WITHHELD diagnosis) landed during this session
  and supersedes Debate D's "R2-4 PENDING" rows; the task brief's numbers are
  confirmed against the verdict file.
- **Laws observed:** zero RNG in any decision path (judging is deterministic
  from frozen verdict numbers); no code written (nothing to keep pure-Zag);
  numbers copied exactly from frozen verdicts; anything not in a frozen
  source is marked as the crew's judgment, not a measured result.
- **What this debate does not claim:** it does not re-derive round-1/round-2
  results (frozen verdicts taken as given); kill bars above are prereg-ready
  specifications, not frozen preregs — freezing them needs the round-2 prereg
  process and, where human verdicts are involved, Micah's protocol. Sol's
  intermittency means fronts (b)-detail and (c)/(d)-specific questions were
  answered by the crew alone; sol's captured answers cover (a), the
  identifiability residual, and the joint-bar form.
