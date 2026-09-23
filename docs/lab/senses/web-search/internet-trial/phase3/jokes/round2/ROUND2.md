# HELL-HOLE V3 joke volume-training — ROUND 2

Date: 2026-09-22. Frozen prereg: `phase3/PREREG.md` §3
(commit `266ca4e18593de287a86daaf107cb36680577657`).
Deliverables live under `phase3/jokes/round2/`. **Nothing is committed.**

## 1. Why round 2 exists (round-1 failure mechanism)

Round 1 (2026-09-22): solo G1 **8/24 FAIL** (bar ≥20/24); helper G1 24/24;
G2 0/40 both arms; D6 1.00 both arms. Three runs per arm byte-identical,
ledger chains verified.

Failure mechanism: the 300-item training corpus was 282/300 RECON
(crew-templated) items. Frequency analysis over templated frames taught the
classifier **frame/action surface words** ("tip", "hack", "add", "mix") —
not deadpan pragmatic absurdity. On real held-out deadpan advice, which
rarely uses those frames, the (FRAME∨ACTION)∧HARM rule starved: 16 of 24
D-A items fell through to UNCERTAIN.

Round 2 replaces the teaching, not the bars: **pragmatic
absurdity-recognition** — compose component facts about the objects in the
text with the recommended action, detect contradiction, and use the
contradiction as the JOKING signal. The frozen bars are unchanged:
G1 ≥20/24, G2 ≤4/40, D6 = 1.00, both arms, three byte-identical runs.

## 2. Freeze chronology (prereg: re-freeze BEFORE any training/calibration)

1. 2026-09-22: round-1 held-out/helper copied to `round2/corpus/`.
2. `work/build_heldout_r2.py` replaces `hsi05`–`hsi08` (repaired SINC
   controls); all other 60 items byte-identical to round 1.
3. `work/update_helper_r2.py` refreshes the four helper judgments (blind,
   SINCERE, cited phrase verified as substring of folded text).
4. SHA-256 of `round2/corpus/heldout.json` recorded in
   `round2/corpus/HELDOUT_SHA256.txt`; helper SHA in
   `round2/corpus/HELPER_SHA256.txt`. **(PENDING — two page fetches)**
5. Only after (4): training-corpus collection, component-fact derivation,
   classifier build, calibration, gate runs.

No marker, fact, rule, vocabulary item, or threshold may be added, removed,
or tuned on the basis of held-out performance. Calibration is on the
round-2 training corpus only.

## 3. SINC control repairs (hsi05–hsi08)

Round-1 controls were invalid/weak: a dictionary definition of a proverb
(hsi05), an idiom page (hsi06), a "MythBuster"-framed page (hsi07), and a
page that frames the claim as a legend (hsi08). None cleanly meets "the
**author sincerely asserts** the false proposition" — several merely quote
or define the belief.

Replacements (each fetched and verified as earnest, non-debunk, non-ironic
prose in which the author asserts the false claim as the basis for advice):

| id | source | sincere assertion (verbatim) | false claim |
|---|---|---|---|
| hsi05 | Horse & Rider, "Extreme-Weather Strategies" | "Pack a warm hat; you lose most of your body heat through your head." | head heat loss (loss is proportional to exposed area, ~7–10%) |
| hsi06 | Sanitarium, "8 reasons to drink 8 glasses" | *(pending verbatim fetch)* | the 8×8oz rule as a health requirement |
| hsi07 | The Daily Meal, "Hair Of The Dog Hangover Cures" | "three hair of the dog recipes that will knock the hangover right out of you"; "Trust us, it works." | hair-of-the-dog cures hangovers |
| hsi08 | InsideHook, "15 Hangover Cures From People Who Drink for a Living" | *(pending verbatim fetch)* | hair-of-the-dog cures hangovers |

Why these four: each is a distinct everyday-advice genre (outdoor survival,
nutrition, food/drink, lifestyle) so D4 tests sincerity-preservation across
genres, not one site's house style. The false claims are all "folk-health"
grade — the exact class a joke detector must not confuse with deadpan
absurdity: the author means it, the content is wrong, and nothing about the
recommended action contradicts the objects involved (a hat for your head is
sensible; water is safe to drink; a cocktail is a normal beverage).

## 4. Component-fact schema

A component fact is a triple `(phrase, fact_code, polarity)`:

- `phrase`: a whole-word match string (case-folded), e.g. `antifreeze`.
- `fact_code`: one of the closed fact vocabulary below.
- `polarity`: what the fact says about the object (intrinsic; not tuned).

Fact vocabulary (closed; every code must have ≥4 training exemplars to
enter, same support rule as round 1):

| code | meaning | example phrases |
|---|---|---|
| F_TOXIC | poisonous if ingested | antifreeze, rat poison, bleach, poison |
| F_NOTFOOD | not a food substance | glue, rocks, sandpaper |
| F_CONTAM | contaminated / unclean to ingest | yellow snow, expired |
| F_SCALD | hot enough to burn | boiling (water) |
| F_IRRIT | irritates eyes/wounds | lemon, garlic, juice (in eyes) |
| F_WOUND | open vulnerable tissue | cut, burn, eyes |
| F_VENOM | venomous animal | rattlesnake, bear |
| F_DANGER_ANIMAL | dangerous wild animal | bear, rattlesnake |
| F_ELEC | electronic device (destroyed by heat/water) | iphone, phone, cell phone |
| F_MICRO | microwave oven (destroys electronics) | microwave, microwaved |
| F_HEATAPP | heating appliance hazard | toaster |
| F_CRITSYS | critical system files | system32 |
| F_HEAVY | heavy object | tables, brick |
| F_BODY | body part (injury target) | toes, teeth |
| F_WILDLIFE | wild animal (taking = illegal/absurd) | duck, ducks |
| F_STRANGER | unknown person | — (context: atm + neck) |
| F_SEDATIVE | sedating drug | sleeping pill |
| F_LAX | bowel stimulant | laxative |
| F_ESSENT | essential bodily function | breathe |
| F_SIGNAL | traffic control signal | red lights |
| F_WRONGGAS | gas unsuitable for tires | helium |
| F_WRONGPROD | product wrong for the appliance | dish soap (for dishwasher) |
| F_COSMETIC | cosmetic-only fix | marker (for tires) |
| F_PHOTO | photograph (not a light source) | photo |
| F_DARK | darkness | dark |
| F_VR | virtual reality | virtual reality |
| F_IMAGINE | imagination | imagine |
| F_WEAPON_SUB | inadequate weapon substitute | fork (vs robber) |
| F_SEA | being lost at sea | lost at sea |
| F_SHEEP | sheep (absurd disguise target) | sheep |

Action vocabulary (closed, same support rule):

| code | meaning | example phrases |
|---|---|---|
| A_INGEST | eat/drink | eat, drink |
| A_ADD | add/put/mix into | add, mix, put |
| A_INSERT | insert into appliance | stick (in), insert |
| A_APPLY | apply to body | apply, squeeze (into eyes) |
| A_SHOOT | shoot at | shoot |
| A_HUG | embrace | hug |
| A_KISS | kiss | kiss |
| A_DELETE | delete | delete |
| A_DROP | drop on | drop |
| A_INJURE | inflict injury | stub, bitten (seek) |
| A_INFLATE | inflate | inflate |
| A_SUBST | substitute | substitute |
| A_TAKE | take home | take |
| A_ACCEL | accelerate | faster |
| A_STOP | stop essential function | don't breathe |
| A_RUN | run (light/signal) | through (red lights) |
| A_TEST | test by doing | test |
| A_DISGUISE | disguise as | disguise |
| A_USE | use as | use (photo in dark) |

## 5. Contradiction-to-intent rule

A **contradiction** fires when an action code and the fact codes of its
object(s) form one of the closed contradiction patterns:

| pattern | contradiction gloss |
|---|---|
| A_INGEST ∧ (F_TOXIC ∨ F_NOTFOOD ∨ F_CONTAM ∨ F_SCALD) | ingesting poison / non-food / filth / scalding liquid |
| A_ADD ∧ F_TOXIC | adding poison to a system |
| A_INSERT ∧ F_HEATAPP | inserting objects into a heating appliance |
| A_APPLY ∧ F_IRRIT ∧ F_WOUND | applying irritant to wound/eyes |
| A_SHOOT ∧ F_IRRIT ∧ F_WOUND(eyes) | shooting irritant into eyes |
| A_HUG ∧ F_DANGER_ANIMAL | embracing a dangerous animal |
| A_KISS ∧ F_STRANGER | kissing a stranger |
| A_DELETE ∧ F_CRITSYS | deleting critical system files |
| A_DROP ∧ F_HEAVY ∧ F_BODY | dropping heavy objects on body parts |
| A_INJURE ∧ F_BODY | deliberate self-injury as remedy |
| A_BITE_SEEK ∧ F_VENOM | seeking a venomous bite |
| A_INFLATE ∧ F_WRONGGAS | inflating tires with lifting gas |
| A_SUBST ∧ F_WRONGPROD | wrong product in appliance |
| A_APPLY ∧ F_COSMETIC ∧ F_TIRE | cosmetic fix for tires |
| A_TAKE ∧ F_WILDLIFE | taking wildlife home |
| A_ACCEL ∧ F_CAUGHT | accelerating when caught speeding |
| A_STOP ∧ F_ESSENT | stopping an essential function |
| A_RUN ∧ F_SIGNAL | running a red light |
| A_TEST ∧ F_MICRO | testing microwavability by microwaving |
| A_ELEC ∧ F_MICRO | microwaving electronics |
| F_SEDATIVE ∧ F_LAX | combining opposing drug effects |
| A_USE ∧ F_PHOTO ∧ F_DARK | using a photo as a light source |
| A_IMAGINE ∧ F_VR | imagining as VR substitute |
| A_WEAPON_SUB ∧ F_ROBBERY | fork as anti-robbery weapon |
| F_SEA ∧ F_VACATION | getting lost at sea as leisure |
| A_DISGUISE ∧ F_SHEEP | disguising a dog as a sheep |
| A_INGEST ∧ F_HEAVY | ingesting a brick |

**Intent rule (frozen after calibration):**

1. CONTRADICTION ≥ 1 → **JOKING**, reason = the fired fact/action codes
   (each code verifies as a substring of the folded item text — D6).
2. elif SAT-markers ≥ 2 → **SATIRE** (round-1 SAT list, unchanged).
3. elif TROPE-markers ≥ 1 → **JOKING** (round-1 TROPE list, unchanged).
4. else → **UNCERTAIN**. SINCERE and DECEPTIVE are never emitted
   (same documented scope as round 1: sincere-vs-uncertain and
   hoax-vs-uncertain discrimination are not trained; default UNCERTAIN
   withholds, so missed jokes cannot install).

## 6. Evidence precedence

- **Contradiction evidence outranks marker evidence.** Rationale: a
  detected pragmatic contradiction (the recommended action would destroy,
  poison, or injure given the objects' known properties) is direct evidence
  of non-serious intent; surface markers are correlational. A single
  contradiction suffices — absurdity is not a matter of degree.
- **Satire cadence is checked after contradiction** because satire
  headlines can contain absurd premises ("Bomb-Eating Dogs"); the
  contradiction rule would otherwise relabel satire as JOKING. (D2 stays
  descriptive; any residual relabeling is documented per item.)
- **Trope markers last**, as in round 1.
- **SINCERE/DECEPTIVE are never produced by the classifier.** The helper
  combination rule (frozen, asymmetric) is unchanged: the helper may add
  non-sincere flags, never manufacture sincerity; final SINCERE only if
  the classifier judged SINCERE (vacuous here — the install path stays
  dead code, G2 measures the classifier's own restraint).

## 7. Volume rationale (prereg §3: ≥300 items)

Round 1's 300 items were 282/300 templated; the volume was hollow — the
frequency analysis learned the templates, not the phenomenon. Round 2
keeps the ≥300-item bar but fills it with **real deadpan items**
(`prov: "web"`, verbatim text, live URL, retrieval date), each carrying an
**absurdity annotation**: the component facts that fire, the contradiction
pattern, and the gloss of why the contradiction signals joking intent.

Why these examples (not merely how many): every training item is chosen
because its joke turns on a *specific* action↔fact contradiction, and the
corpus is built to cover the contradiction-pattern space (ingestion,
device-destruction, body-application, absurd-action — the D-A1…D-A4
subforms) rather than to hit a count. The support rule (≥4 exemplars per
fact/action code) forces each code to earn its place across distinct real
items; codes that cannot find four real exemplars do not enter the
decision vocabulary. Delivery-form coverage (deadpan vs marked vs absurd
premise) is argued per subform in §8.

## 8. Training corpus plan (PENDING collection)

- `round2/corpus/training_corpus.json`: ≥300 real items, disjoint from the
  held-out set and from the round-1 RECON items.
- Families: deadpan advice (D-A1…D-A4 analogues), satire-as-news,
  documented hoaxes, absurd-premise jokes — mirroring the held-out class
  proportions.
- Each item: `id, family, cell, label, title, body, url, retrieved, prov,
  absurdity: {facts:[...], actions:[...], pattern:"...", gloss:"..."}`.
- Derivation: component facts/actions mined from training items only, with
  the ≥4-exemplar support rule; contradiction patterns are the crew's
  compositional hypothesis (training-side), frozen before the gate runs.

## 9. Calibration & gate procedure (unchanged from round 1)

- Pure Zag, zero RNG, no timestamps/PIDs. Hash-chained ledger, same entry
  format as the joke-lie trial.
- Python is transport/scoring only (fixture generation, `score_gate.py`) —
  never in a decision path.
- 3 runs per arm, byte-identical required, or the leg FAILs on procedure.
- No binaries or `.zagd` artifacts in the tree; compile outside the
  deliverable tree (toolchain:
  `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`).

## 10. Crew-built vs TNN understanding (standing honest qualification)

Everything in §§4–6 — the fact/action vocabularies, the contradiction
patterns, the precedence order, the support rule, the never-SINCERE /
default-withhold policy — is crew-built scaffolding. The Zag gate program
invents none of it: it applies the frozen code lists and the contradiction
table. A PASS on G1 would show the scaffolding generalizes to held-out web
jokes; it would NOT show TNN understands humor or pragmatics. A FAIL shows
the scaffolding does not transfer. If round 2 fails with the same pattern
(starved catch on real deadpan), the verdict is PARTIAL with the mechanism
named — no endless looping.
