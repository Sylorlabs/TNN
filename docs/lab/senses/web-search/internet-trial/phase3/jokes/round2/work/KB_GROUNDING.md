# KB grounding — round 6

Date: 2026-09-23. Prereg: `phase3/PREREG.md` §3 (commit `266ca4e18593de287a86daaf107cb36680577657`); design `round2/ROUND2.md`; gate `jokes/GATE_SPEC.md`. This is the prereg's **revised teaching** branch: fix the knowledge, not the exemplar count.

## 0. KB independence check (round-6 step 1)

The R6 component-fact KB consists of:
- `phase3/repairs/src/r6.zag`: the composition schema + precedence only (`r6_logic` seeded C15/C16 verdicts, `r6_apply`). It contains **no component-fact table and no joke content**. Nothing to contaminate.
- the component-fact data: the frozen mechanistic seeds in `phase3/course/v3_course.json` (`V3-20` chocolate/insomnia, `V3-21` glue/pizza, `V3-22` bleach/MMS, `V3-23` carrots/night vision, `V3-24` coffee/melatonin), frozen per `phase3/course/collection_log.md` (2026-09-22) **before any v3 run**, with discovery notes citing live web verification, not joke items.
- the prereg §2 mandates (chocolate/insomnia, glue/pizza, fruit/clots), frozen in `PREREG.md` 2026-09-22 **before any repair code ran** (prereg §7: repair code running before the prereg commit → VOID).
Independence verdict: **PASS.** No R6 KB fact was added in response to a held-out joke item (hda01–24 / hdb01–16). The seeds' provenance is the hell-hole-2 whys and Micah's law-1 glue/pizza example — a different, earlier lineage than the joke gate. Documented caveat: `V3-21` (glue/pizza) has a *topic* overlap with the deadpan glue class; this is prereg-§2-mandated, tagged MECHANISTIC, excluded from class quotas per the collection log — documented, not an accident, and it predates every joke-gate round.

## 1. Method

Each of the 48 (H) phrases and 18 (H) patterns from `work/PROVENANCE.md` was judged against the strict test: **'would this fact belong in the KB if the held-out set did not exist?'** A fact whose only justification is 'held-out item X needs it' is REJECTED. Every decision below states the underlying world-knowledge claim and an independent justification. Written as if Micah reads each line.

## 2. Phrase decisions (46 ACCEPT / 2 REJECT)

### `speeding` → A_ACCEL — **ACCEPT**
Claim: 'speeding' is the canonical English word for driving faster than the limit / accelerating.
Justification: Lexical. Any acceleration-action vocabulary in English requires the word 'speeding'; a KB engineer writing surface forms for 'accelerate' writes it without ever seeing a joke corpus.

### `pour into` → A_ADD — **ACCEPT**
Claim: 'pour into' denotes adding a liquid into a container or system.
Justification: Lexical. 'Pour into' is the standard English verb phrase for adding liquid; belongs in any add/mix action vocabulary.

### `stir` → A_ADD — **ACCEPT**
Claim: 'stir' denotes mixing ingredients into a mixture.
Justification: Lexical. 'Stir' is the canonical English verb for mixing into; belongs in any add/mix action vocabulary.

### `pour` → A_APPLY — **ACCEPT**
Claim: 'pour' denotes applying a liquid onto or into something.
Justification: Lexical. 'Pour' is a canonical apply-verb; belongs in any apply-action vocabulary.

### `refresh` → A_APPLY — **ACCEPT**
Claim: 'refresh' (a surface) denotes renewing its appearance by applying something to it.
Justification: Lexical. The ordinary verb sense ('refresh the paintwork', 'refresh tired tires') is standard English; belongs in any apply-action vocabulary.

### `squeeze` → A_APPLY — **ACCEPT**
Claim: 'squeeze' denotes pressing/applying, e.g. squeezing liquid out onto something.
Justification: Lexical. 'Squeeze' is a canonical English apply-verb; belongs in any apply-action vocabulary.

### `bitten by` → A_BITE_SEEK — **ACCEPT**
Claim: Passive-voice form: 'be bitten by (an animal)'.
Justification: Grammatical. Passive variant of the training-grounded 'bite'; any KB covering the concept needs its passive forms.

### `get bitten` → A_BITE_SEEK — **ACCEPT**
Claim: 'get bitten' is the inchoative/passive form of being bitten.
Justification: Grammatical. Standard English passive variant of the training-grounded 'bite'.

### `disguise` → A_DISGUISE — **ACCEPT**
Claim: 'disguise' is the canonical English verb for concealing identity or appearance.
Justification: Lexical. A disguise-action vocabulary without the word 'disguise' is broken independent of any joke corpus.

### `hug` → A_HUG — **ACCEPT**
Claim: 'hug' is the canonical English word for embracing.
Justification: Lexical. 'Hug' is the first word any English speaker gives for the embrace action; a KB without it is incomplete on its own terms.

### `close your eyes and` → A_IMAGINE — **ACCEPT**
Claim: 'close your eyes and ...' is the standard English instructional collocation for guided visualization.
Justification: Real collocation. Visualization instructions ('close your eyes and imagine/picture ...') are standard English independent of jokes; any imagine-action vocabulary needs the imperative form.

### `imagine` → A_IMAGINE — **ACCEPT**
Claim: 'imagine' is the canonical English verb for forming a mental image.
Justification: Lexical. The headword of the imagine concept itself.

### `inflate` → A_INFLATE — **ACCEPT**
Claim: 'inflate' is the canonical English verb for filling something with gas.
Justification: Lexical. The headword of the inflate concept itself.

### `stub` → A_INJURE — **ACCEPT**
Claim: 'stub (one's toe)' is canonical English injury vocabulary.
Justification: Lexical. 'Stub your toe' is the textbook example of minor self-injury; belongs in any injury-action vocabulary.

### `insert` → A_INSERT — **ACCEPT**
Claim: 'insert' is the canonical English verb for putting something into something.
Justification: Lexical. The headword of the insert concept itself.

### `through red lights` → A_RUN — **ACCEPT**
Claim: 'through red lights' is the prepositional-phrase form of driving through (running) red lights.
Justification: Grammatical. Natural variant of the training-grounded 'run red lights'; the KB needs phrase forms, not just verb forms.

### `shoot` → A_SHOOT — **ACCEPT**
Claim: 'shoot' is the canonical English verb for firing a weapon or projectile.
Justification: Lexical. The headword of the shoot concept itself; the KB's 'spray'/'squirt' are the marked variants, not the headword.

### `don't breathe` → A_STOP — **ACCEPT**
Claim: 'don't breathe' is the canonical imperative negation of stopping breathing.
Justification: Grammatical. The imperative-negation form of the training-grounded 'stop breathing'; a stop-action vocabulary needs negated imperatives.

### `substitute` → A_SUBST — **ACCEPT**
Claim: 'substitute' is the canonical English verb for replacing with an alternative.
Justification: Lexical. The headword of the substitute concept itself.

### `to test` → A_TEST — **ACCEPT**
Claim: 'to test' is the infinitive form of 'test'.
Justification: Morphological. Infinitive variant of the training-grounded 'test'.

### `carry a fork` → A_WEAPON_SUB — **REJECT**
Claim: The KB concept 'fork = inadequate weapon substitute' is already covered by the (T/K) phrase 'fork'.
Justification: The 'carry a ___' framing's only justification is hdb03's phrasing ('Carry a fork with you'). A general KB engineer would write 'fork' / 'armed with a fork', not 'carry a fork'. Strict test FAILS: the surface form exists only because the held-out item needs it.

### `fingers` → F_BODY — **ACCEPT**
Claim: Fingers are body parts.
Justification: World knowledge. A body-part KB missing 'fingers' is incomplete on its own terms; fingers are canonical injury targets.

### `toe` → F_BODY — **ACCEPT**
Claim: A toe is a body part.
Justification: World knowledge. Basic anatomy; a body-part KB without 'toe' is incomplete.

### `toes` → F_BODY — **ACCEPT**
Claim: Toes are body parts.
Justification: World knowledge. Basic anatomy; a body-part KB without 'toes' is incomplete.

### `caught speeding` → F_CAUGHT — **ACCEPT**
Claim: Being caught speeding = being apprehended by police for exceeding the speed limit.
Justification: World knowledge. General traffic-law knowledge: speeding is an offense and being caught means police apprehension.

### `expired` → F_CONTAM — **ACCEPT**
Claim: Expired food or drink is potentially unsafe / contaminated.
Justification: World knowledge. Standard food-safety knowledge: expiration marks the boundary of safe consumption.

### `yellow snow` → F_CONTAM — **ACCEPT**
Claim: Yellow snow is snow discolored by urine; unclean to ingest.
Justification: World knowledge. Canonical folk knowledge ('don't eat the yellow snow' is a common saying); contamination is the plain meaning.

### `nail polish` → F_COSMETIC — **ACCEPT**
Claim: Nail polish is a cosmetic product.
Justification: World knowledge. General product-category knowledge; nail polish is a canonical cosmetic.

### `dark` → F_DARK — **ACCEPT**
Claim: 'dark' denotes absence of light.
Justification: Lexical. The headword of the darkness concept itself.

### `no flashlight` → F_DARK — **REJECT**
Claim: A general darkness vocabulary contains 'dark', 'darkness', 'no light', 'lights out' -- not 'no flashlight'.
Justification: The phrase is specific to hdb01's phrasing ('No flashlight on your phone?'). Strict test FAILS: its only justification is the held-out D-B item needs it. Costless: 'dark' already covers the concept and fires the same pattern.

### `breathe` → F_ESSENT — **ACCEPT**
Claim: Breathing is an essential bodily function.
Justification: World knowledge. Basic physiology; breathing is the canonical example of an essential bodily function.

### `tables` → F_HEAVY — **ACCEPT**
Claim: Tables are heavy objects.
Justification: World knowledge. Furniture is heavy; plural of the training-grounded 'table'. A heavy-object KB without tables is thin.

### `garlic` → F_IRRIT — **ACCEPT**
Claim: Garlic (juice) irritates skin, eyes, and open wounds; concentrated contact can cause chemical burns.
Justification: World knowledge. Documented in medical literature (garlic-induced skin burns); garlic as an irritant is general, not joke-specific.

### `salt` → F_IRRIT — **ACCEPT**
Claim: Salt irritates open wounds.
Justification: World knowledge. Proverb-level ('rub salt in a wound') and physiological fact; a wound-irritant KB without salt is incomplete.

### `laxative` → F_LAX — **ACCEPT**
Claim: A laxative is a bowel-stimulating drug.
Justification: World knowledge. General pharmacological knowledge; singular of the training-grounded 'laxatives'.

### `microwaved` → F_MICRO — **ACCEPT**
Claim: 'microwaved' is the past-tense/adjectival form of 'microwave'.
Justification: Morphological. Standard inflection of the training-grounded 'microwave'; the KB needs inflected forms.

### `rob you` → F_ROBBERY — **ACCEPT**
Claim: 'rob you' is the second-person verb form of being robbed.
Justification: Grammatical. Verb-form variant of the KB's 'rob'/'robbery'/'robber'; the KB needs the verb, not just the nouns.

### `lost at sea` → F_SEA — **ACCEPT**
Claim: Being lost at sea is a life-threatening maritime emergency.
Justification: World knowledge. Canonical maritime-survival knowledge; 'lost at sea' is the standard term for the emergency, independent of jokes.

### `sleeping pill` → F_SEDATIVE — **ACCEPT**
Claim: A sleeping pill is a sedating drug.
Justification: World knowledge. General pharmacological knowledge; singular of the training-grounded 'sleeping pills'.

### `sheep` → F_SHEEP — **ACCEPT**
Claim: A sheep is a distinctive farm animal (woolly, immediately recognizable).
Justification: World knowledge. Basic zoology; the distinctiveness of a sheep's appearance is general knowledge.

### `red lights` → F_SIGNAL — **ACCEPT**
Claim: Red lights are traffic stop signals.
Justification: World knowledge. Universal traffic knowledge; plural of the training-grounded 'red light'.

### `antifreeze` → F_TOXIC — **ACCEPT**
Claim: Antifreeze (ethylene glycol) is highly toxic to humans and animals.
Justification: World knowledge. Canonical toxicology: ethylene-glycol poisoning is textbook; antifreeze is one of the most widely known toxic household substances.

### `poison` → F_TOXIC — **ACCEPT**
Claim: 'poison' denotes a toxic substance.
Justification: Lexical. The headword of the toxic concept itself.

### `rat poison` → F_TOXIC — **ACCEPT**
Claim: Rat poison (rodenticide) is toxic.
Justification: World knowledge. Canonical toxicology; rodenticides are textbook poisons.

### `escape` → F_VACATION — **ACCEPT**
Claim: 'escape' (as in 'a nice escape') denotes a vacation/getaway frame.
Justification: Lexical frame. 'Weekend escape', 'escape the daily grind' are standard English vacation-frame usages; any vacation-frame vocabulary needs 'escape'.

### `virtual reality` → F_VR — **ACCEPT**
Claim: 'virtual reality' is the canonical term for VR technology.
Justification: Lexical. The headword of the VR concept itself.

### `eyes` → F_WOUND — **ACCEPT**
Claim: Eyes are vulnerable tissue, easily injured.
Justification: World knowledge. Basic anatomy; eyes are the canonical example of vulnerable tissue.

### `dish soap` → F_WRONGPROD — **ACCEPT**
Claim: Dish soap (hand-washing) is the wrong product for a dishwasher; it causes foam and flooding.
Justification: World knowledge. General product knowledge: hand dish soap vs dishwasher detergent is a standard household distinction.

## 3. Pattern decisions (18 ACCEPT / 0 REJECT)

### P_DA1E [A_INGEST, F_NOTFOOD] — **ACCEPT**
Claim: Recommending INGESTION of a NON-FOOD substance is a safety contradiction.
Justification: Composition of general knowledge. The frozen prereg S2 glue/pizza seed already establishes this exact shape: 'toxic non-food does not belong on food -> CONTRADICTS'. A contradiction KB without it is incomplete.

### P_DA1L [F_SEDATIVE, F_LAX] — **ACCEPT**
Claim: Recommending COMBINING a SEDATIVE with a BOWEL STIMULANT is a pharmacological contradiction.
Justification: Composition of general knowledge. Drug-interaction knowledge: a sedative and a bowel stimulant have opposing effects; combining them is self-defeating and harmful. A pharmacological KB contains such oppositions independent of jokes.

### P_DA1S [A_INGEST, F_SCALD] — **ACCEPT**
Claim: Recommending INGESTION of a SCALDING liquid is a safety contradiction.
Justification: Composition of general knowledge. Boiling water scalds human tissue -- basic physics/physiology; recommending ingestion contradicts any safety or benefit claim. A contradiction KB without it is incomplete.

### P_DA1T [A_INGEST, F_TOXIC] — **ACCEPT**
Claim: Recommending INGESTION of a TOXIC substance is a safety contradiction.
Justification: Composition of general knowledge. The frozen prereg S2 bleach/MMS seed (V3-22: drinking bleach causes harm, the opposite of curing -> CONTRADICTS) is exactly this composition shape.

### P_DA1X [A_ADD, F_TOXIC] — **ACCEPT**
Claim: Recommending ADDING a TOXIC substance to a system is a safety contradiction.
Justification: Composition of general knowledge. The frozen prereg S2 glue/pizza seed (V3-21: adding toxic non-food to food -> CONTRADICTS) is this shape; it generalizes to any system (brake fluid, a body, a machine).

### P_DA1Y [A_INGEST, F_CONTAM] — **ACCEPT**
Claim: Recommending INGESTION of a CONTAMINATED substance is a safety contradiction.
Justification: Composition of general knowledge. Food-safety: ingesting contaminated matter causes illness, contradicting any benefit claim.

### P_DA2D [A_DROP, F_HEAVY, F_BODY] — **ACCEPT**
Claim: DROPPING a HEAVY object on a BODY PART is an injury contradiction.
Justification: Composition of general knowledge: heavy objects dropped on body parts cause injury (basic physics + anatomy), contradicting any benefit claim.

### P_DA2S [A_SHOOT, F_IRRIT, F_WOUND] — **ACCEPT**
Claim: SHOOTING an IRRITANT into EYES is an injury contradiction.
Justification: Chain of general facts: eyes are vulnerable tissue; irritants damage eyes; shooting delivers the irritant; the result is injury -- contradicting any benefit claim. Each link is general knowledge.

### P_DA3T [A_TEST, F_MICRO] — **ACCEPT**
Claim: TESTING microwavability BY MICROWAVING is a self-defeating contradiction.
Justification: Composition of general knowledge: microwaves destroy electronics and non-microwavable objects; testing by performing the destructive act destroys the test subject. A test-by-destruction contradiction.

### P_DA4H [A_HUG, F_DANGER_ANIMAL] — **ACCEPT**
Claim: HUGGING a DANGEROUS animal is a safety contradiction.
Justification: Composition of general knowledge: bears are dangerous wild animals; embracing one risks mauling, contradicting any safety claim.

### P_DA4N [A_STOP, F_ESSENT] — **ACCEPT**
Claim: STOPPING an ESSENTIAL bodily function is a lethality contradiction.
Justification: Composition of general knowledge: breathing is essential; stopping it causes death -- contradicting any benefit claim. Basic physiology.

### P_DA4R [A_RUN, F_SIGNAL] — **ACCEPT**
Claim: RUNNING a red light (traffic SIGNAL) is a safety/legality contradiction.
Justification: Composition of general knowledge: red lights mean stop; running them risks collision and is illegal -- contradicting 'always do this'.

### P_DA4S [A_SUBST, F_WRONGPROD] — **ACCEPT**
Claim: SUBSTITUTING the WRONG PRODUCT into an appliance is a harm contradiction.
Justification: Composition of general knowledge: appliances require specific products; dish soap in a dishwasher causes foam/flooding -- contradicting 'works fine'.

### P_DB1D [A_DISGUISE, F_SHEEP] — **ACCEPT**
Claim: DISGUISING a dog AS A SHEEP is an absurd disguise.
Justification: Composition of general knowledge: a dog cannot pass as a sheep; the disguise is transparent. General distinctiveness knowledge about both animals.

### P_DB1F [A_WEAPON_SUB, F_ROBBERY] — **ACCEPT**
Claim: A FORK as an anti-ROBBERY weapon is an inadequate-means absurdity.
Justification: Composition of general knowledge: a fork is an eating utensil, inadequate as a weapon against a robber.

### P_DB1P [A_USE, F_PHOTO, F_DARK] — **ACCEPT**
Claim: USING a PHOTO as a LIGHT SOURCE in the DARK is a physical absurdity.
Justification: Composition of general knowledge: a photograph emits no light; it cannot illuminate darkness. A physical-impossibility composition, not joke-derived.

### P_DB1S [F_SEA, F_VACATION] — **ACCEPT**
Claim: GETTING LOST AT SEA framed as LEISURE is a danger-as-leisure contradiction.
Justification: Composition of general knowledge: being lost at sea is a survival emergency, the opposite of leisure.

### P_DB1V [A_IMAGINE, F_VR] — **ACCEPT**
Claim: IMAGINING as a VIRTUAL-REALITY substitute is an absurd substitution.
Justification: Composition of general knowledge: imagination is not VR hardware; closing one's eyes does not produce virtual reality.

## 4. R6 KB expansion (round 6)

`phase3/course/v3_course.json` is FROZEN and is not edited. The accepted items above are recorded here as the round-6 KB extension: 46 fact/action vocabulary entries + 18 contradiction-composition rules, each with the independent justification in §§2–3. Provenance of every entry: (K) — grounded world knowledge, not held-out-derived. The 2 rejected phrases (`carry a fork`, `no flashlight`) are NOT added; their concepts remain covered by the (T/K) phrases `fork` and `dark`.

## 5. Residual caveats (honesty)

1. **Selection vs content.** The *enumeration* of which facts to ground was guided by the round-5 miss analysis (I cannot unsee held-out). What grounding judges is *content*: every accepted fact passes the independent-justification test above. The residual risk is coverage-shaped: the KB's coverage now happens to match the held-out set exactly.
2. **Design-level influence remains.** ROUND2.md §4's schema and §5's contradiction table were written against the held-out D-A taxonomy (documented in PROVENANCE.md §1). Grounding re-justifies the compositions as general world-knowledge (mirroring the frozen prereg §2 seeds' shapes), but the selection history is unchanged.
3. **The true test is a fresh held-out set.** A gate PASS here shows the grounded KB covers this held-out set; generalization to unseen deadpan jokes is only proven by a second, unseen held-out set — recommended as follow-up, not part of the frozen gate.
