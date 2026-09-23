# POSTMORTEM_R2-14 — why the FS-G union died

**Fork:** R2-14 (debate D FS-G / "R2-37 Union": R2-3 × R2-7)
**Date:** 2026-09-23
**Status:** DEAD on frozen bars 1, 2, 6, 8 (bars 3, 4, 5, 7 pass)
**Prereq reading:** `VERDICT_R2-14.md` (this file re-verifies its numbers from the
evidence ledgers; every number below was re-scored from
`evidence/batt_b_adv_union_r1.ledger`, `batt_b_ctrl_union_r1.ledger`, and the
ablation ledgers against the frozen fixture `.truth` files — all match the verdict)

## The one-paragraph cause of death

The union's two halves are orthogonal, and on the R2FX battery the admission
half is vacuous: the mechanical span-overlap audit admits every valid fixture,
so the union IS R2-7's full mode verbatim. It therefore reproduces R2-7's
failures almost exactly (2.83% vs 2.14% false installs; recall 68.8% identical)
while adding nothing. The registry-adversarial suite (the risk debate D's
AGAINST team named explicitly) found two real exploit families against the
frozen challenge quantities. The discrimination ablation proved the
`chal_supports` margins decorative (1.06×). Composition of two survivors did
not compose — because there was no composition on the battery that mattered.

## Re-verified numbers (scored from evidence, not copied from the verdict)

**Bar 1 — 283/10,000 = 2.83% false installs (bar ≤1%: FAIL)**

| (task, family) | false / total | rate |
|---|---|---|
| timbredisc f1 | 181/500 | 36.20% |
| timbredisc f3 | 44/190 | 23.16% |
| timbredisc f2 | 2/295 | 0.68% |
| shapetrans f3 | 40/615 | 6.50% |
| shapetrans f2 | 13/915 | 1.42% |
| shapetrans f1 | 0/815 | 0.00% |
| colorconst f1 | 2/690 | 0.29% |
| pitchdisc f1 | 1/710 | 0.14% |
| colordisc f1/f2/f3 | 0/2330 | 0.00% |
| motiondir f1/f2/f3 | 0/630 | 0.00% |

Family groups: f1 184/4029 = 4.57%, f2 15/3536 = 0.42%, f3 84/2435 = 3.45%.
Per task: timbredisc 227/985 = 23.05%, shapetrans 53/2345 = 2.26%.

**Bar 2 — 1376/2000 = 68.8% recall (bar ≥80%: FAIL).** Decomposition
(not in the verdict — scored here):

| task | n | recall | formation-wrong | challenge-overstrict |
|---|---|---|---|---|
| colordisc | 1080 | 91.4% (987) | 76 | 17 |
| colorconst | 720 | 54.0% (389) | 306 (42.5%) | 20 |
| motiondir | 200 | 0.0% (0) | 7 | 193 (96.5%) |
| **total** | 2000 | **68.8%** | **389 (19.5pp)** | **230 (11.5pp)** |

**Bar 6 — 301 vs 283 = 1.06× (bar ≥5×: FAIL).** The 301 abl_conf false
installs are a strict superset of the 283 union false installs (overlap 283,
conf-only 18, union-only 0). INSTALL occurs only when outcome==judgment in
both modes (3106/3106 union, 3385/3385 abl_conf) — the full `chal_supports`
never installs on outcome≠claim either. The margins blocked 261 TRUE installs
on the adversarial battery to catch 18 false ones.

**Bar 7 — 2690 vs 283 = 9.50× (bar ≥5×: PASS).** Independence is load-bearing.

**Bar 8 — KILL.** CP-CCN: 100 kept candidates, 100/100 verified genuine false
installs. CP-SHP: 100 kept, 10/10 sampled verified genuine. CP-COL: 0 kept
(wedge closed). CP-PTC/CP-TMB/CP-MOT: incomplete at verdict (compute).

---

## (a) Which attack families drove the 2.83%? Would R2-3 alone have caught them?

Timbredisc drives 227/283 (80.2%), shapetrans 53/283 (18.7%) — together
93.6% of all false installs. Within those: timbredisc f1 (36.20%) and f3
(23.16%) are catastrophic; shapetrans f3 (6.50%) exceeds the 2%/family bar;
shapetrans f2 (1.42%) is inside it. These are the SAME families that drove
R2-7's standalone 2.14% (R2-7 B5: timbredisc ~158, shapetrans ~53, colorconst
2, pitchdisc 1 — shapetrans/colorconst/pitchdisc counts match the union
nearly exactly; the union is worse only on timbredisc, +69, which the verdict
attributes to battery composition).

They are **not novel to the union** — every one of the 283 is an R2-7
failure reproduced. Composition did not hurt (no family R2-7 caught is lost:
colordisc and motiondir stay at 0) and did not help (no R2-7 failure is fixed).

Whether R2-3 **alone** (judgment-disagreement between formation span and gate
span) would have caught them is **UNVERIFIED** — the crew never ran R2-3's
judgment comparison on R2FX fixtures. The union's R2FX admission gate was
span-overlap-audit only; the disagreement logic lived only in the R2P gate-2
path. Two directional hints, both untested: (i) the prereg's frozen declared
limitation says the timbredisc generator renders the SAME harmonic profile
into F and G (informationally coupled), so a gate judgment on G would likely
agree with the fooled formation — R2-3 would probably INSTALL, not withhold;
(ii) shapetrans G is a clean quadrant where the gate judgment may be correct —
R2-3 might withhold there. Neither was measured. What IS measured: on the
R2FX battery the R2-3 half contributed exactly zero (admit=1 on all 10,000),
so the union's 2.83% is R2-7's failure with an R2-3 sticker on it.

## (b) Discrimination ablation 1.06× — decorative leg, or misconstructed ablation?

Both, at different levels. Three measured facts:

1. **What was literally ablated (the margins) is decorative.** `abl_conf`
   differs from full mode only by removing the `chal_supports` margins and
   the alternative-side test. Result: 283 → 301. The margins catch 18 false
   installs at the cost of withholding 261 true installs on the adversarial
   battery plus 193/200 motiondir true controls. Cost/benefit ≈ 15:1 against.
   On this evidence the margins are not load-bearing safety machinery; they
   are over-strictness machinery.

2. **The ablation was misconstructed relative to its stated purpose.** Bar 6's
   prereg justification says it "proves discrimination, not independence,
   carries the load — the anti-R2-1 bar." But `abl_conf` KEEPS the challenge
   function and the outcome==claim comparison — i.e., it keeps the actual
   discriminating content (the challenge predicting different outcomes under
   claim vs alternative). It ablated a calibration detail (margins), not
   discrimination. A ≥5× bar on margin removal is an absurd requirement no
   sane margin could pass; the bar could not have passed even if the
   challenges were perfect.

3. **The real discrimination test was bar 8, and it failed there.** R2-7's own
   B4 (no-challenge ablation: 27→0 false installs on 100 samples) already
   proved the challenge-as-a-whole is load-bearing vs nothing — so the
   discriminative leg is not decorative in the R2-1 sense. What bar 8 proved
   is that the discriminating CONTENT (the challenge quantities) is inadequate
   against registry-knowing adversaries: CH-CCN-1's mean-RGB and CH-SHP-1's
   ray-profile harmonics are lossy summaries the adversary predicts better
   than the fork.

Net: the margins are decorative (proven); the ablation cannot speak to
whether discrimination-as-such is load-bearing (misconstructed); the CP suite
speaks to it and says the current challenges don't discriminate where it
counts (2 of 6 tasks broken by design, timbredisc broken by enumeration).

A further irony for debate D: bar 6 was "R2-1's 1.37× ablation turned into a
load-bearing proof." FS-G scored **1.06× — worse than R2-1 itself** on the
discrimination side.

## (c) What are CP-CCN and CP-SHP, and why did they kill bar 8?

- **CP-CCN (colorconst):** CH-CCN-1 decides SAME_SURFACE vs DIFFERENT by
  mean-RGB distance on D65 re-rendered views. The adversary crops pairs from
  DIFFERENT photos whose D65 mean-RGB distance is ≤12 (inside the challenge's
  SAME band) and fools formation with extreme-illuminant F renders. The union
  INSTALLS SAME_SURFACE on truly different surfaces — 100 kept, 100/100
  verified genuine (different photos, same installed claim).
- **CP-SHP (shapetrans):** CH-SHP-1 is a ray-profile harmonic classifier on
  the clean 48×48 G quadrant. The adversary uses inter-class morphs
  (λ∈[0.1,0.4]∪[0.6,0.9]), extreme rotations/scales, and target-quadrant
  clutter; truth = λ-majority class. The classifier's decision boundary is
  crossed while truth stays unambiguous — 100 kept, 10/10 sampled verified
  genuine.
- **CP-COL (colordisc): 0 kept — the positive control.** CH-COL-1's u16
  spectral L1 *is* the truth quantity (up to ≤6 counts rounding), so the
  registry-knowing adversary found nothing. This is the existence proof that
  the failure is in the *quantities*, not in the *idea* of challenges.

**Fundamental flaw, not calibration.** No threshold change fixes CP-CCN:
mean-RGB is continuous, so collisions exist inside ANY same-band, while
legitimate same-surface pairs spread under cropping — tightening the band
destroys recall without closing the wedge. The quantity is not a function of
truth (crop identity). Same for CP-SHP: the morph parameter is continuous
and the classifier has a boundary; margins widen the withhold region but
strong-truth morphs (λ≤0.35/≥0.65) still misclassify. This is an inherited
R2-7 challenge-design flaw, **orthogonal to composition**: R2-3's admission
half gates *which evidence* the challenge sees, but the adversary predicts
the *challenge quantity itself* — the admission half has no lever on that
attack surface. The prereg deliberately froze the registry (anti-HARKing),
which locked the flaw in. Debate D's AGAINST team named this exact kill
mechanism ("the adversary reads the frozen registry too"); the bar-5 battery
was built to test it, the test worked, the fork died. The straw-alternative
audit passing (all 6 entries "not strawmen") shows the audit was syntactic —
it checked that alternatives were plausible, not that the quantities
determined truth.

## (d) Where is the 68.8% recall lost?

Two legs, measured separately (the verdict did not decompose this):

1. **Formation leg: 389/2000 (19.5pp).** The percept formation is wrong on
   42.5% of colorconst normals (306/720) — the formation front end, not the
   gate, is the bottleneck there. R2-7's verdict said the same ("formation
   accuracy on R2FX normals only ~58%").
2. **Challenge-overstrictness leg: 230/2000 (11.5pp) — this contradicts
   R2-7's published analysis.** R2-7's verdict claims "not challenge
   over-strictness; only 2% were correct+withhold." The union's ledger shows
   11.5% correct+withhold, driven by **motiondir: 193/200 (96.5%) correct
   judgments WITHHELD even though challenge outcome == judgment == truth**
   (e.g. jud=N, outcome=N, truth=N, disp=WITHHOLD). The `chal_supports`
   margins veto correct motiondir installs en masse. R2-7's own
   `ctrl_ledger.txt` shows the identical pattern (judgment==outcome,
   disp=WITHHOLD on motiondir), so the behavior is inherited, not introduced
   by the union — but R2-7's "2%" analysis is inconsistent with its own
   ledger. (Caveat: R2-7's ctrl fixture order differs from FS-G's
   `b_ctrl.list`, so I could not positionally re-score R2-7's full
   decomposition; the motiondir WITHHOLD-with-agreement rows are visible
   directly in R2-7's ledger text.)

Note the asymmetry: the margins that are decorative for safety (catch 18
false installs) are devastating for recall (block 261 true installs on
adversarial + 193 motiondir controls). And no recall fix at the gate can
recover the 19.5pp lost in formation — colorconst formation needs front-end
work, not gate work.

## (e) Did the union kill R2-1 "at both layers"? What about debate D's front-(g) FOR ruling?

No — asymmetrically. R2-1's shape was disjoint spans + confirmatory check
(15.62% installs, 1.37× ablation). FS-G's two anti-R2-1 bars:

- Independence ablation: 9.5× (≥5×: PASS) — the union proves independence is
  load-bearing. It would kill R2-1 at the admission layer.
- Discrimination ablation: 1.06× (≥5×: FAIL) — **worse than R2-1's own
  1.37×**. The union cannot prove its discriminating leg is load-bearing any
  better than R2-1 could prove its confirmatory check was. It does not kill
  R2-1 at the evaluation layer.

Debate D's front-(g) FOR ruling ("the only candidate that would have
falsified R2-1 at both layers") is therefore **falsified as stated**. Two
compounding problems with the ruling:

1. **False factual premise.** The prereg §0 records that debate D §10
   described R2-7 as ALIVE at "≤1% overall, ≤2%/family, recall ≥80%" when the
   frozen R2-7 verdict actually says 2.14%, 68.8%, 87.8%-flag. The FOR case
   was built on R2-7 already clearing bars it had failed.
2. **The AGAINST team's predicted kills are exactly what killed it.**
   Challenge-prediction adversaries (CP-CCN, CP-SHP) and the independence
   audit checking spans-not-coupling (timbredisc's declared F/G informational
   coupling) were named in the AGAINST steelman. The FOR rebuttal said these
   were "battery-grade" risks to be carried as explicit bars — the bars were
   carried, and they killed the fork. The ruling's mechanism reasoning
   (independence + discrimination as independent, each load-bearing) is
   half-refuted: independence is load-bearing (9.5×), discrimination-as-margins
   is not (1.06×), and discrimination-as-quantities fails against adaptive
   adversaries (bar 8).

---

## Program-level judgments

### FS-A (Attack-Informed Discriminative Challenge): REDESIGN — do not build as spec'd

The hypothesis — *each enumerated family answered by a discriminative
challenge; the check that installs is the challenge outcome, never family
membership* — is **not refuted**: no fork has tested per-family-paired
challenges (FS-G used per-task challenges from the frozen registry). What
FS-G refutes is FS-A's **build plan**, which was to reuse the R2-7 registry
("shares the R2-7 challenge registry… reusing the registry halves the cost"):

- With the frozen registry, FS-A dies on its own bar 1 before the holdout:
  timbredisc alone is 227/985 = 23.05% on enumerated families (bar: ≤2%/family).
- The CP suite is a preview of FS-A's novel-family holdout — and the preview
  failed on 2 of the 3 completed tasks. A holdout adversary with the registry
  in hand breaks colorconst and shapetrans challenges by construction.
- FS-G's 1.06× does **not** refute FS-A's load-bearing assumption, because
  FS-A's discrimination is the challenge outcome vs the alternative, which
  FS-G's ablation never removed — but it does warn that FS-A's ablation
  (challenge→bank ≥2×) must be paired with a challenge-prediction test, or
  FS-A will "pass" its ablation while dying on its holdout exactly as FS-G
  passed bar 7 while dying on bar 8.

**Redesign (prereg-ready sketch):**

- *Hypothesis (revised):* per-family-paired discriminative challenges close
  KB4 iff each challenge's quantity is a function of that family's truth
  criterion (the CP-COL wedge-closed pattern) and survives a frozen
  challenge-prediction red-team; INSTALL on challenge PASS; the novel-family
  holdout decides generalization.
- *Mechanism changes:* (1) NEW challenge quantities for at least timbredisc,
  colorconst, shapetrans — the R2-7 registry is not reused for these tasks;
  (2) the FS-G `gen_cp.py` challenge-prediction procedure (frozen seed,
  budget, strong-truth criterion) runs INSIDE the design loop: the registry
  freezes only when the red-team returns empty families on all tasks
  (documented empty = finding, per the FS-G prereg's own rule); (3) recall
  reported decomposed — formation-error vs challenge-overstrictness — with a
  separate bar on overstrictness (≤5% correct+withhold), so the motiondir-193
  failure mode is barred directly; formation must reach the recall bar's
  precondition on normals before the fork (colorconst formation at 42.5%
  wrong cannot support any ≥80% recall bar — front-end work or task scoping
  first).
- *Kill bars (revised):* (1) ≤1% overall / ≤2% per enumerated family on 10k
  adversarial (keep); (2) novel-family holdout ≥10 families × ≥1,000
  attempts, ≤2%/family, pooled ≤1% (keep — this was the right experiment);
  (3) challenge→bank ablation ≥2× AND holdout gap widens (keep);
  (4) **NEW:** post-freeze challenge-prediction suite (same procedure, fresh
  seed) must return zero kept families — any kept family kills;
  (5) recall ≥80% on 2,000 controls (take the documented fallback, not sol's
  90% — 90% is unreachable with formation at 58% on R2FX normals; record why),
  with the ≤5% overstrictness sub-bar; (6) sol's upper-95%-confidence-bound
  rule on the 1%/2% rates (adopted).
- *What is preserved from the debate spec:* the enumeration-vs-property
  framing, the holdout as the deciding experiment, the challenge→bank
  ablation form. What is dropped: registry reuse.

### FS-D (Discriminative Temporal Challenge): KILL

The frozen dependency in debate D §10 is explicit: "FS-D is a restricted FS-G
configuration (temporal-only evidence) — build after FS-G validates the
machinery, **or not at all if FS-G dies on bar (3)**." FS-G died on bar (3)
(the discrimination ablation: 1.06× vs ≥5×). **The gate is closed by the
frozen rule.**

Substantively there is no untested content left to rescue:

- Temporal-disjoint evidence with a discriminating challenge already ran
  inside FS-G: motiondir's G is frames 51–100 (temporal disjointness), 0
  false installs — and 96.5% recall loss from over-strict margins.
- The confirmatory-vs-discriminative ablation on later-window evidence is bar
  6 generalized; bar 6 failed at 1.06× because it ablated margins, and
  re-running it on temporal evidence cannot fix that construction.
- The R2-3 ≥90% withhold on temporal R2P pairs is subsumed by FS-G's bar 4
  (100% withhold on all 1,200 R2P pairs).
- Debate D front-(d) already ruled: temporal survives only as a
  disjoint-evidence class inside the admission law, never as a warrant;
  H3 (22.95%) and R2-1 (15.62%) are the epitaphs. FS-D's distinct claim
  ("discriminative, not confirmatory, later-window check") was tested by
  FS-G's bars 6+8 and failed on both the ablation and the challenge-quality
  sides. Nothing in FS-D escapes FS-G's two findings (margins decorative;
  challenge quantities gameable).

### Is a redesigned union worth a new prereg?

**Not as the next step.** The evidence says this composition doesn't compose:
the halves address orthogonal attack surfaces (admission: *which* evidence;
challenge: *what the quantity says*), and on the battery that mattered the
admission half was vacuous, so the union was the weaker parent wearing the
stronger parent's badge. A redesigned union ("FS-G2") is prereg-*able* but
should be **sequenced after** FS-A-redesigned:

1. First, FS-A-redesigned: new challenge quantities that survive
   challenge-prediction (CP-suite-empty pre-freeze gate) + formation fixed to
   support the recall bar.
2. Then, and only then, test whether R2-3-style admission adds marginal value
   — as a marginal-gain fork in FS-C's structure, not as a union: run the
   R2-3 *judgment-disagreement* gate (not the span audit) on the R2FX battery,
   ablate it, and require ≥2× false-install reduction attributable to the
   admission leg alone. If it can't earn its keep, the program adopts the
   challenge-only contract.

Sketch of the bar set if FS-G2 is ever prereg'd: ≤1%/≤2% on 10k adv;
post-freeze CP suite zero kept families; admission-leg ablation ≥2×
(judgment-disagreement removed, span audit kept); independence ablation ≥5×
(keep — it passed); recall ≥80% with the overstrictness sub-bar; R2-3 ≥90%
on R2P (keep). But the honest program read is: the leverage is in challenge
quantities (CP-COL proves quantity==truth works) and formation accuracy, not
in bolting halves together.

---

## Caveats / UNVERIFIED

- Whether R2-3's judgment-disagreement gate alone would have caught the
  timbredisc/shapetrans R2FX families: **UNVERIFIED** — never run; the
  union's R2FX gate was span-audit only. Directional hints in §(a).
- R2-7's full recall decomposition (formation vs overstrictness): **UNVERIFIED**
  — R2-7's ctrl fixture order differs from FS-G's `b_ctrl.list`, so
  positional truth-mapping doesn't transfer; only the motiondir
  WITHHOLD-with-agreement pattern was confirmed directly in R2-7's ledger text.
- CP-PTC, CP-TMB, CP-MOT: **incomplete at verdict** (compute constraints) —
  timbredisc's 23.05% enumerated failure makes CP-TMB kills likely but
  unmeasured.
- The +69 timbredisc delta union-vs-R2-7 (283 vs 214): attributed by the
  verdict to battery composition; not independently re-derived here.
- Bar 3 (98.7%/98.9% flag rates) was not re-scored from ledgers; taken from
  the verdict.

## Bottom line for the program

1. The R2-7 registry is compromised as a frozen artifact: 2 of 6 challenge
   quantities are gameable by design (CP-CCN, CP-SHP), 1 task is broken by
   enumeration (timbredisc 23.05%), and the margins are recall-hostile
   over-strictness (motiondir 96.5% correct-withheld). No fork should reuse
   it as-is — this kills the cost-sharing premise of FS-A's debate spec.
2. The CP-suite procedure (challenge-prediction red-team, frozen seed/budget,
   strong-truth criterion) is the program's most valuable new instrument from
   round 2: it is the first battery that attacks the *quantity*, and it
   decided FS-G. Promote it into every future challenge fork's design loop,
   pre-freeze.
3. Recall bars must be decomposed (formation-error vs challenge-overstrictness)
   from now on — the single 68.8% number hid two unrelated failures, one of
   which (motiondir margins) the parent fork's own analysis misreported.
4. Debate D's front-(g) FOR ruling is overturned on its central empirical
   claim; the ranked build list should be revised: FS-G dead, FS-A redesigned
   per above, FS-D killed (gate closed), FS-F (signature ceiling) unaffected.
