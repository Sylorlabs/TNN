# Volume rationale — joke-family teaching corpus (phase 3, §3)

**Question the volume answers:** how many joke exemplars does the mechanism need
to generalize deadpan-joke detection to unseen items — and what is the volume
*for*? The answer is not a number; it is coverage of the delivery-form space.
300 is the count that fills the matrix below with redundancy.

## 1. The delivery-form space (what varies, what must be covered)

A joke that can be installed as knowledge fails along two axes: **delivery**
(how the joke is signaled) and **payload** (what false claim it carries).
The four families in PREREG §3:

| Family | Delivery | Payload | Why it fools an intent reader |
|---|---|---|---|
| F1 deadpan advice (glue-on-pizza class) | flat imperative advice, zero joke markers | harmful/absurd recommended action | reads exactly like sincere advice; only the *content* is absurd |
| F2 satire-as-news | news-voice + outlet masthead | fabricated events | without the masthead, reads like news |
| F3 deliberate hoaxes | earnest expert/field-guide voice | fabricated entities/claims | engineered to read as sincere; the lie is the point |
| F4 absurd-premise flat jokes | flat sincere statement | impossible situation | no markers at all; needs world knowledge or trope familiarity |

Within F1 — the gate class, the one that installs harmful advice — the payload
space factorizes further. A deadpan harmful-advice joke is a triple:

**(advice frame) × (harm vector) × (target)**

- advice frame: imperative / "you should" / tip-trick-hack-recipe-cure language
- harm vector: toxic substance, dangerous animal, destructive device action,
  harmful physical action
- target: food/drink, body part, device, household object

The mechanism's generalization engine is **compositional** (Micah's logic-first
law, PREREG §2/R6): it does not memorize 300 jokes; it learns the harm-vector
vocabulary (substances, animals, device actions) and the frame vocabulary, then
fires on unseen *combinations*. Volume is what makes the vocabularies broad
enough that a fresh joke's triple is already covered.

## 2. The coverage matrix (what the 300 buy)

| Family | N | Cells (each cell ≥4 exemplars) | Vocabulary the cell teaches |
|---|---|---|---|
| F1 deadpan advice | 130 | D-A1 toxic ingestion: 8 substances × 4 frames = 32 | glue, bleach, soap, detergent, paint, antifreeze, ammonia, drain cleaner… × eat/drink/mix/add frames |
| | | D-A2 body application: 8 substances/actions × 4 = 32 | lemon/eyes, garlic/cut, rattlesnake/bite, tables/toes… |
| | | D-A3 device destruction: 8 actions × 4 = 32 | delete system32, microwave phone, toaster-insert, download ram, freezer… |
| | | D-A4 absurd action: 34 mixed | hug bear, helium tires, ducks-are-free… (documents the residual: no lexical signature) |
| F2 satire-as-news | 70 | 5 cadence sub-forms × 14 | area-man, sources-confirm, at-press-time, fake-expert, fake-study… |
| F3 hoaxes | 55 | 5 earnest-voice sub-forms × 11 | species-discovery, miracle-product, secret-tech, fabricated-narrative, gag-science… |
| F4 absurd premise | 45 | 5 trope clusters × 9 | downloadable-ram, time-traveler, talking-animal, impossible-physics, flat-anti-joke… |
| **Total** | **300** | | |

Redundancy rule: **no marker enters the decision vocabulary on fewer than 4
exemplars.** A marker seen once is memorization; seen across 4+ distinct items
it is a form feature. The 300 count exists so that after the ≥4-support filter,
each cell still contributes vocabulary. A 30-item corpus (the joke trial's
size) cannot do this: its one absurd-advice hit ("glue") was a single-item
memorization that the trial honestly reported as crew-written, not learned.

## 3. What volume cannot buy (documented residual)

D-A4 items with no lexical signature ("drop tables on your toes", "helium
tires", "ducks are free") have no form feature a text-only reader can use
without world knowledge. No exemplar count fixes this; the honest mechanism
abstains (UNCERTAIN → withhold: safe, but a catch miss). The gate bar (0.80)
therefore measures the *signaled* majority of the class, and the report must
show the per-sub-form breakdown so a failure is attributable (D-A4 residual)
rather than mysterious.

Likewise F3 hoaxes in perfect earnest voice (the tree-octopus failure): the
training teaches the *safe* behavior — extraordinary-claim vocabulary +
earnest voice → UNCERTAIN/withhold — not perfect DECEPTIVE classification.
The install bar (≤0.10) is the load-bearing measure here, not the intent label.

## 4. Why held-out must be real web (and training may mix)

The gate measures generalization to the wild. Held-out items are 100% real
web, frozen before training begins, so no training decision can be conditioned
on them (documented commitment in TRAINING_RECORD.md). Training mixes real
items with faithful reconstructions (labeled RECON) because the matrix needs
cell-filling exemplars that the open web does not always provide verbatim;
every RECON item models a documented real item class, and labels remain
uncontested (the *class* intent is uncontested even when the wording is
reconstructed).

## 5. The honest qualification (what the volume is and isn't)

The marker vocabularies and the composition rules are **crew-built test
scaffolding** in the `j_intent.zag` lineage — the invention law permits the
crew to build the harness; the trial measures what the harness discriminates.
What the 300 exemplars contribute, honestly stated:

1. **Breadth**: the vocabularies are data-derived (frequency analysis over the
   corpus, ≥4-support filter), not crew-guessed from a dozen examples.
2. **Coverage evidence**: the training record shows per-cell marker coverage,
   so "the mechanism generalizes" is a checkable claim about the matrix, not
   a vibe.
3. **The composition rules themselves** (advice-frame ∧ harm-vector ∧ target →
   JOKING) are crew-designed from Micah's logic-first law. The volume does not
   invent them; it stocks them.

A PASS on the gate therefore means: *the volume-trained scaffolding survives
the held-out course* — not that TNN natively understands humor. That
distinction is load-bearing for the v3 report.
