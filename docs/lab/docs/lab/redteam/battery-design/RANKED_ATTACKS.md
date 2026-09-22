# RANKED ATTACKS — battery-design red team

2026-09-21/22 · Micah's order: assemble the strongest skeptical case; no
pulled punches. Ranking rule from parent: an attack we already found and
documented ourselves ranks WEAKER than one pointing at an untested gap.
For each attack: (a) severity, (b) testability with a concrete design,
(c) honest judgment — "IS an artifact" (proven) vs "COULD be" (untested gap).

Related: `BLIND_SPOT_MAP.md` (per-headline see/blind), `BATTERY_HEALTH_AUDIT.md`
(parse results), `audit_batteries.py` + `AUDIT_OUTPUT.txt` (reproducible).

---

## #1 — SERIOUS — The 156/156 "mechanism" dispatches on the battery's kind labels

**The attack.** `hypcomp_fact` in `new-mechanisms/mech_learner.zag` opens with
`let k:i32=bat_kind(f)` — the battery's own kind function — and routes to
kind-specific handlers: k==4||k==5 → install-candidate-0 + challenge-candidate-1
(order-dependent: assumes the battery's candidate order); k==3 →
`first_install_pairs` (hardcodes the battery's `(a<<32)|b` pair encoding);
k==6 → spoof pre-filter; else scalar trust-sum competition. Battery generator
and learner share one binary. The SPEC describes generic eliminative rules;
the implementation is a kind-dispatched switch. The 156/156 therefore measures
"the preregistered taxonomy's six resolvable classes are handled by the code
written for them" — not "a general contradiction-resolution mechanism."

**Severity: SERIOUS** (not fatal: the prereg froze the taxonomy BEFORE any
mechanism code, so this is co-design, not post-hoc fitting; the leaf rules
`compete`/`challenge` read evidence fields generically; the oracle
independently recomputes; the honest limit — kind 7, 12/12 absorbed — is
stated). But the headline "conflict-driven deliberation resolves 156/156
contradictions" implies generality the evidence cannot support: a seventh
resolvable class, or the same classes with shuffled candidate order or a
different composition encoding, are untestable without rewriting battery and
dispatch together. There is no seam between test-generator and test-taker.

**Testable: YES — concrete design (adversarial-class battery).**
1. Keep the evidence schema (val,src,trust,spoof,t,att) but generate NEW classes
   with an independent generator: 2-liars-vs-1-truth (equal total trust →
   expect withhold), spoof marker on a TRUTHFUL source, 3-component
   composition, temporal challenge with candidate order shuffled (newer first),
   two trusted sources with conflicting attestations.
2. Split the binary: battery generator and learner must not share address
   space or kind functions; the learner receives only evidence-item streams.
3. Score with the preregistered rules per class, adjudicated by a third party
   (independent oracle, no shared formulas with the generator).
Predicted outcome if the attack holds: the current implementation cannot even
ingest the new classes (dispatch has no branch); a re-dispatch would be
writing the test-taker to the test again.

**Judgment: IS an artifact of co-design** (code-proven). The 156/156 number is
real — the handlers do what the taxonomy asks — but the generality claim is
unsupported. This CONFIRMS and sharpens Sol #1 (merged): Sol called
test-generation coupling "existential"; the code shows it is structural
(shared binary, kind dispatch) but bounded (preregistered taxonomy, generic
leaf rules) — SERIOUS is the honest rating.

## #2 — SERIOUS — Info-source: determinism purchased by freezing the world

**The attack.** The "live web" trial replays 17 SearXNG envelopes frozen
2026-09-22. The verdict's caveat 4 asserts: "Live re-querying would add
freshness, not change the mechanism verdict." That assertion is UNTESTED —
no live re-fetch has ever been scored. Three compounding selection effects:
(a) the 12 planted falsehoods are hand-picked web-consensus facts (capital of
France, gold symbol, 1984 author…) — facts the web unanimously and stably
contradicts; the battery contains no falsehood the web is ambiguous about;
(b) the spoof cases are CONSTRUCTED, labeled fictions (Poseidonia, Uo), not
real adversarial web content (SEO farms, coordinated misinformation, stale
caches); (c) the "true corrections installed 12/12" grades the learner against
the ENVELOPE's value — the battery conflates "web consensus" with "truth," so
a wrong-but-unanimous web would score full marks for installing wrongness.

**Severity: SERIOUS.** The mechanism verdict ("information richness enables
detection") is really "detection works when the independent source is correct
and unanimous" — the boundary the trial itself names ("truthful but
sensor-deceivable") but never adversarially exercises with REAL web
adversariality.

**Testable: YES.**
1. Live re-fetch: re-run the R1/R2 arms against freshly fetched envelopes for
   the same 17 queries; report catch-rate delta vs frozen. If the mechanism
   verdict is content-agnostic, the delta should be ~0 on stable facts.
2. Adversarial queries: add facts where the web is genuinely contested or
   manipulated (breaking news, SEO-poisoned queries, Wikipedia vandalism
   windows); score withhold-vs-install calibration, not just catch rate.
3. Wrong-web control: a constructed case where the "independent" source is
   unanimously wrong — the learner SHOULD install wrongness per its rules;
   verify the battery scores this as the predicted failure, not a pass.

**Judgment: COULD break** — the mechanism (prefer corroborated independent
evidence) is content-agnostic by design, so stable facts should reproduce; the
untested part is precisely the adversarial regime where the program's
"sensor-deceivable" qualifier lives. The caveat admits the boundary; the
battery doesn't patrol it.

## #3 — SERIOUS — No battery has ever been generated by a fully independent party

**The attack.** Every headline battery shares authorship, schema, or binary
with the system it tests: new-mechanisms (shared binary, kind dispatch — #1);
scale/fewshot (FACTSPEC formulas generate the facts the store was built to
hold); flaw battery (sealed manifest is good practice, but scorer, teacher,
and learner co-evolved in one program); info-source (real web data, but
queries hand-picked by the trial author); prose v2 (best separation in the
program — Worker A built the battery, Worker C the learner — and the learner
COLLAPSED to 0.26–0.63, which is evidence the separation was real). No trial
has used disjoint schemas from an independent author, corruption at rates
unknown to the evaluator, or predicates outside the program's own taxonomies.
Sol #1's core demand stands unmet.

**Severity: SERIOUS.** This is the load-bearing methodological gap: all
"the instrument discriminates" defenses (flaw battery fails the naive learner;
v2 collapses; kind 7 absorbs) are demonstrated WITHIN the program's own
batteries. Independence is the one property that can't be self-certified.

**Testable: YES — the independent-battery protocol.**
1. A party with no access to TNN internals authors a battery in a disjoint
   schema (non-Gutenberg source texts, novel predicate families, e.g.
   procedural visual-reasoning facts or real-world tabular data).
2. Truth values committed (hashed) before any learner run; scoring by the
   third party from frozen expectations.
3. Include corruption at an undisclosed rate (evaluator-unknown, learner-unknown).
4. Pre-register: which headlines are under test (mastery? absorption?
   contradiction handling?) and the bars.
Cost: one crew, ~1 week. This is the single highest-value experiment the
program hasn't run.

**Judgment: untested gap** — not "the headlines are false" but "the headlines
have never faced a hostile examiner." The program's honesty about its own
batteries (this file included) is not a substitute for an outside battery.

## #4 — SERIOUS — Principle acquisition: the 13/13 was handed the principles

**The attack.** Principle-detection's 13/13 measures DERIVATION from stipulated
principles (universal instantiation + conflict check — genuine, both arches).
It cannot distinguish "TNN derived the principle" from "TNN was handed the
principle," because the battery hands over all 19. Principle LEARNING from
examples — the actual capability the trial's framing implies — has never been
tested. Compounding: true-exception "refinement" is LOGGED, not applied; the
principle text is never rewritten in-run, so a battery scoring genuine
revision would fail.

**Severity: SERIOUS** for the scope of the claim (the verdict documents the
stipulation in scope notes — honest — but the headline "principle detection
13/13" travels without it).

**Testable: YES.** Teach 20+ exemplars per class WITHOUT stating the
principle; withhold a violating fact; test detection. Then teach true
exceptions and test whether the principle's TEXT is revised (not merely
logged) — score the revised text against held-out cases.

**Judgment: untested gap** (the derivation result IS real; the acquisition
claim is unmeasured). Partially overlaps the verdict's own scope notes —
the gap is documented, the experiment is not.

## #5 — SERIOUS (already-known, ranks below) — Flaw battery: form, not content; laundering into hits

**The attack.** At 50% teacher noise the §B.7 battery scores 96/96 while true
mastery is 93/192 (noisy50 verdict's own headline: "the flaw battery can't see
a thing"). Sharper: the wrong-span REVISE/SPAN_SHIFT path "corrects" the span
while ADOPTING the teacher's false value — scored as a HIT. The battery doesn't
merely miss the absorption; it REWARDS it. Any "the learner judges well" claim
resting on flaw scores alone is unfounded under teacher noise — the scores are
identical at 0% and 50% noise.

**Severity: SERIOUS** as an instrument defect (the laundering-into-hits is worse
than blindness). **Ranks below #1–#4 per the ranking rule**: our own verdict
found it, headlined it, and mechanistically explained it. The fix is a battery
revision (plausible-false probes need false VALUES, not just empty spans;
wrong-span scoring must check the adopted value against the manifest), not a
verdict retraction — the verdict already retracted the claim.

**Testable: YES** (battery revision + re-run on the noisy50 leg).

**Judgment: IS an artifact** — proven by the 0%-vs-50% invariance. Already
owned by the program.

## #6 — SERIOUS-as-scope-clarification — Self-test 400/400 certifies grading, not the test

**The attack.** KB-ST-FIDELITY = binary verdict == oracle recomputation, where
the oracle "reimplements the competition mechanism and recomputes every
observed count from the frozen data formulas." The oracle is independent CODE
but not independent of the battery's formulas or its notion of correctness.
A wrong battery — wrong kinds, wrong bars — scores 400/400 fidelity. The
instrument certifies that the grading implements the formulas; it is blind to
whether the formulas test the right thing (it inherits H2's kind-dispatch
through battery B4).

**Severity: SERIOUS as a scope clarification, MINOR as a defect** — the verdict
doesn't overclaim ("faithful to an independent oracle," "this becomes the
lab's future harness" with listed prerequisites). The risk is downstream:
once adopted as THE harness, fidelity numbers will be read as validity
numbers.

**Testable: YES —** the fault-injection pattern already in the verdict extends
naturally: inject a WRONG battery (corrupt expectations, not corrupt format —
B5 tests format) and verify the harness reports the wrong battery's verdicts
faithfully rather than catching the wrongness. Document that fidelity ≠
validity in the harness's own output.

**Judgment: IS a scope limitation** (not a defect in what was built).

## #7 — MINOR-to-SERIOUS (already-known) — 1.0000 mastery is storage; the generalization gap is measured but the headline travels alone

**The attack.** Mastery = exact recall of the (id → value) mapping the
FACTSPEC generated; train and test are the same mapping. Where generalization
WAS tested (prose v2 single-exposure rephrasing), the exact-key architecture
collapsed to 0.26–0.63. The program measured the gap honestly — but the
"1.0000" headline circulates without the "storage, not understanding"
qualifier, and there is no integer-channel paraphrase test by construction.

**Severity: MINOR-to-SERIOUS** — MINOR because the verdicts state "exact-fact
mastery" precisely; SERIOUS only if the headline is quoted without it.
Ranks low: the program tested the gap (v2) and reported the collapse.

**Testable: YES —** integer-channel paraphrase battery: same (id → value)
facts, novel surface templates from an independent generator; measure the
mastery delta. (Prose v3's dense-phrasing regime is the prose-channel version.)

**Judgment: COULD mislead readers; the evidence itself is honest.**

## #8 — FATAL-to-the-number (already-known + remediated) — NEG 36/36 impossible

**The attack.** Prose v2's NEG sub-battery contained two duplicate probe texts
with conflicting expects (ids 18/30, 19/31 — audit-confirmed); 36/36 was
unachievable by construction; max 34/36.

**Severity: FATAL to the 36/36 number, MINOR to the verdict** — the bar was
"0% leakage" (negated values never returned), whose literal condition HELD;
the verdict passed NEG "as written" while documenting the defect. v3 rephrased
the probes (PREREG3 §C3); all 36 strings now unique.

**Judgment: IS an artifact** — proven, documented, fixed. Ranks low because
the program caught and repaired it.

## #9 — MINOR (already-known) — Flaw-battery degeneracy below N=96

Below N=96 the flaw battery's probe ids collide (24 → 12 → 6 → 4 → 2 → 1
distinct ids); the 96/96 becomes 4 check-types × repeated probes of the same
few facts. The verdict carries the asterisk, the counts, and the honest
reading ("each executed check passed"). Effective resolution is 24 distinct
probe facts even at N=192 — worth stating wherever 96/96 is quoted; currently
only the fewshot verdict says so.

**Judgment: IS a degeneracy; transparently handled.** Fix: quote as
"96/96 (24 distinct probes × 4 checks)" outside the fewshot verdict.

## #10 — MINOR (already-known) — Prereg kind-5 n=24 typo

PREREG.md's construction table says kind 5 n=24; its own kill bar (12/12),
the N=264 total, and the code ranges say 12. Verdict numbers use 12
(correct). Doc defect only.

## #11 — NOT SUSTAINED — "Metric shopping" and "caveats as pressure valve" as systemic charges

**The charge.** Many metrics run; when one misbehaves it's "documented"; do
headlines ever get revised DOWNWARD, or does documentation substitute for
correction? Do "honest boundary" sections vent pressure to protect big claims?

**Evidence against (the system revises downward):**
- v2 KB2-VIABLE failed decisively → v1 stayed the pinned prose path; Micah
  killed v2 as the path on the evidence.
- The model-quality hypothesis was abandoned TWICE (numeric Δ=0.0000, prose
  Q=+0.0022) — a favored hypothesis, killed by its own bars.
- swe-1-6-slow BANNED as a future teacher (hallucination verdict); hy3 and GLM
  DROPPED from the championship; KB-M-COST tripped → repaired → re-passed,
  all committed in the logs.
- B-vs-C: the "irreconcilable" claim was RETRACTED, a parser bug found, ABS-3
  frozen — documentation LED to correction, not substituted for it.
- The noisy50 verdict's headline IS the instrument's failure; the fewshot
  verdict's headline includes "one-shot learning cuts both ways."

**Watch-items (where the charge has teeth):**
1. Parked items accumulate without expiry: sealed-manifest canary values
   (no-op leg), arms 3/4/5 flaw scoring (N/A-by-design unconfirmed), pass-bar
   wording ("≥10/12 hits" vs score_x10 ≥ 100), cross-verdict near-misses.
   Recommend a parked-item ledger with dates and expiry — parked must not mean
   buried.
2. Info-source caveat 4 ("live re-querying would not change the mechanism
   verdict") is an untested assertion sitting inside a caveat — see #2.
3. Headlines travel without their honest limits: "156/156" without "kind 7:
   12/12 absorbed"; "12/12 absorption" without the metric name (probe vs
   ABS-3). Recommend metric-name discipline in every headline quote.

**Judgment: the systemic charge is NOT SUSTAINED** — caveats in this program
are specific, mechanistic, and have repeatedly driven new experiments (ABS-3,
v3 NEG rebuild, web-search sense v2, RSI's T-DOMAIN3). The three watch-items
above are the honest remainder.

---

## The adversarial-battery principle (brief #6)

A battery designed by someone who WANTS TNN to fail would have: (1)
independent authorship with no access to TNN internals; (2) disjoint schemas
— predicates, templates, and fact sources outside the program's taxonomies;
(3) novel phenomenon classes not in any prereg taxonomy; (4) adversarial
ordering (truth taught last, challengers first); (5) corrupted metadata
(lying trust fields, spoof markers on truthful sources, unattested
"attested" flags); (6) real-world noise at undisclosed rates; (7) a strict
seam — generator and learner never share address space, kind functions, or
formulas; (8) third-party scoring from pre-committed expectations.

How current batteries compare: new-mechanisms is the farthest from this ideal
(shared binary, kind dispatch — #1); info-source is the closest (real web
data, real domain counting) but frozen, hand-picked, with constructed spoofs
(#2); the flaw battery's sealed manifest is good practice undermined by
co-evolved scorer/learner and the form/content gap (#5); prose v2 has the
best authorship separation (Worker A vs Worker C) and its collapse is
evidence the separation was real. No current battery satisfies (1), (5), or
(6). Attack #3 is the proposal to build one.

## Sol's attacks — disposition

- **Sol #1 (test-generation coupling, rated "existential"):** CONFIRMED in
  code for new-mechanisms (#1, merged); PARTIALLY confirmed elsewhere —
  prose v2's collapse under authorship separation is evidence AGAINST
  coupling there; the flaw battery's discrimination across learners is
  evidence against coupling there. Downgraded from "existential" to
  SERIOUS-and-bounded: where coupling exists it is structural and proven;
  where separation existed the instruments bit.
- **Sol #2 (provenance-sensitive scoring & abstention):** folded into the
  blind-spot map's scorecard. The program is BETTER than Sol implies on
  abstention (withhold is the correct answer in three batteries) and WORSE on
  provenance calibration: no battery tests whether the learner's trust
  weighting is correct, because trust values are battery-stipulated
  everywhere. The untested gap is trust-calibration under undisclosed
  corruption — merged into #3.
