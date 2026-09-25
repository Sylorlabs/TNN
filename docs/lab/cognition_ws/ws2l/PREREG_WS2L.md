# PREREG WS2-L — LEARNED SYNONYMS vs CURATED BRIDGE (HEAD-TO-HEAD) — FROZEN 2026-09-25

Coordinator: WS2-L head-to-head. Status: FROZEN — committed before any
WS2-L code was written, any learning corpus was generated, or any WS2-L
lookup was run. Any change to the arms, the learning protocol, the
batteries, the gold sets, the kill bars, or the decision rule after this
commit requires a new dated amendment; results under a changed rule are a
new experiment, not this one.

## 1. Framing (Micah's law, standing)

TNN uses NO LLM tokenization: no BPE, no embeddings, no subword
vocabularies. "Token overlap" is a battery measurement only (whitespace /
lowercased word equality). WS2-B2 closed the vocabulary gap 46/51 -> 51/51
with a curated 56-pair byte-level bridge (SYN_TABLE_V1.txt, SHA-256
`bd23d16fe518024d15445299808017b91e4a47c1ef7d075d516363887c22fc7b`).
Micah's law: TNN must not need bridges or rigid baked-in things, period.
Humans learn what synonyms ARE; TNN must learn the relation from evidence
and bridge the connection itself. The curated table is a stopgap, never the
end state. This experiment tests whether a learning mechanism (ARM L) can
match or beat the curated bridge (ARM B, control) on identical batteries.

## 2. The two arms

### 2.1 ARM L (LEARN) — learns synonymy from evidence

- The synonym store starts EMPTY (verified by audit: initial dump = 0
  relations; K7 also requires >=50 installed after learning).
- Learning mechanism (pure Zag, deterministic, zero RNG): ingests the
  frozen learning corpus (section 4) and installs word<->word relations
  into its own store. Every installed relation carries provenance:
  (evidence IDs, installing rule). A `dump_syn` command lists every
  relation with its provenance (inspectable).
- Frozen rule types (the builder implements these four; exact surface
  patterns are builder's choice but must be documented before the test
  runs; any fifth rule needs a dated prereg amendment BEFORE test runs):
  - R1 DEFINITION: "a X is a Y" / "X is a kind of Y" -> propose X<->Y
    (1 evidence installs).
  - R2 EXPLICIT: "X and Y are synonyms" -> propose X<->Y (1 evidence
    installs).
  - R3 PARAPHRASE: two PARA items sharing a subject tag, identical except
    one word -> candidate pair; installs only with >=2 INDEPENDENT
    subject-pairs aligning the same pair (anti-hallucination).
  - R4 NEGATIVE (veto): "a X is not a Y" / "X is not Y" -> BLOCK X<->Y
    permanently; veto wins over any positive evidence.
- Morphology: L reuses the FROZEN WS2-B stemmer (suffix strip
  -ing/-ed/-es/-s with length guards) and stoplist UNCHANGED. Byte-level
  morphology is not a synonym bridge; it stays.
- Retrieval: phase 1 is the FROZEN WS2-B lookup unchanged. Phase 2 uses
  the LEARNED store with the same override rule as WS2-B2 (unique top
  candidate, >=2 distinct stem matches, else phase 1 stands).
- Transitive closure (multi-hop): builder's choice; must be documented
  in the mechanism doc BEFORE the test runs; scored as-is on MULTI-HOP.
- The builder must NOT hand the mechanism the test vocabulary in any
  form other than the frozen learning corpus. The corpus is evidence
  (data), like a textbook; the mechanism is the learner.

### 2.2 ARM B (BRIDGE) — control, frozen

- The WS2-B2 binary and SYN_TABLE_V1.txt (56 pairs) as committed, rebuilt
  from the frozen sources to verify byte-identity; run unchanged on all
  batteries in section 3. No new pairs, no table edits.

## 3. Batteries (all frozen below; wording fixes for leaks allowed ONLY
## before ARM L's first test run, all documented, per section 6)

Shared knowledge corpus: the frozen v1.1 corpus PLUS the new items below
(new file `corpus_l.txt`; the v1.1 file is never edited). New queries in
`queries_l.txt`, golds in `answers_l.txt` (empty gold = abstain expected).
Query/item pairs are full rephrases: they share NO content words except
through the listed synonym pairs (function words may repeat).

### 3.1 OFFICIAL-51 (primary)

The frozen WS2-B battery as-is: 45 T-exact + 6 P-PARA. Same corpus,
same queries, same golds. (ARM L must learn the 56-pair vocabulary from
the learning corpus; ARM B uses its table.)

### 3.2 FRESH (primary, 6 probes) — novel vocabulary, zero table overlap

Corpus items (`corpus_l.txt`):
- FR01|general|FACT|general|the river flooded the valley and destroyed the farms
- FR02|general|FACT|general|the ocean waves crashed loudly against the rocks
- FR03|general|FACT|general|the dense forest stretched for miles
- FR04|general|FACT|general|the tall mountain rose above the clouds
- FR05|general|FACT|general|the teacher praised the diligent student warmly
- FR06|general|FACT|general|the long journey took three weeks by ship

Queries (`queries_l.txt`, gold in `answers_l.txt`):
- QFR01|probe|SUBJ||||the stream inundated the vale and ruined the crops|FR01
  (pairs: river|stream, flooded|inundated, valley|vale, destroyed|ruined, farms|crops)
- QFR02|probe|SUBJ||||the sea billows broke noisily upon the stones|FR02
  (pairs: ocean|sea, waves|billows, crashed|broke, loudly|noisily, rocks|stones)
- QFR03|probe|SUBJ||||the thick woods extended for leagues|FR03
  (pairs: dense|thick, forest|woods, stretched|extended, miles|leagues)
- QFR04|probe|SUBJ||||the high peak towered over the mist|FR04
  (pairs: tall|high, mountain|peak, rose|towered, above|over, clouds|mist)
- QFR05|probe|SUBJ||||the instructor commended the hardworking pupil kindly|FR05
  (pairs: teacher|instructor, praised|commended, diligent|hardworking, student|pupil, warmly|kindly)
- QFR06|probe|SUBJ||||the lengthy voyage lasted three weeks by boat|FR06
  (pairs: long|lengthy, journey|voyage, took|lasted, ship|boat)

### 3.3 DIST (primary, 6 probes) — zero decoy retrievals required

Corpus items:
- DS1|general|FACT|general|the submarine dove beneath the waves
- DS2|general|FACT|general|the baker kneaded the dough at dawn
- DS3|general|FACT|general|wolves hunted in the forest at night
- DS4|general|FACT|general|the chili pepper burned his tongue
- DS5|general|FACT|general|the free samples drew a hungry crowd
- DS6|general|FACT|general|the neighbor lent him a ladder yesterday

Queries:
- QD1|probe|SUBJ||||the airplane soared above the clouds| (gold: ABSTAIN)
- QD2|probe|SUBJ||||the blacksmith forged the iron at dusk| (gold: ABSTAIN)
- QD3|probe|SUBJ||||the canine watched the flock in darkness|DOG1
  (must retrieve DOG1 via canine|dog; must NOT retrieve DS3 via wolf)
- QD4|probe|SUBJ||||the chef dished spicy bisque at midnight| (gold: ABSTAIN;
  must not retrieve DS4 or HOT1)
- QD5|probe|SUBJ||||the bazaar offered gratis baguettes to throngs| (gold: ABSTAIN;
  must not retrieve DS5 or CHP1)
- QD6|probe|SUBJ||||she lent the reaper to her friend| (gold: ABSTAIN;
  must not retrieve DS6 or BOR1)

### 3.4 ADV-NEAR (primary + K6 kill bar, 6 probes) — near-synonyms must NOT bridge

Corpus items:
- DOG1|general|FACT|general|the dog guarded the sheep through the night
- SAN1|general|FACT|general|the sanction punished the traders for cheating
- BOR1|general|FACT|general|she borrowed the mower from her neighbor
- CHP1|general|FACT|general|the market sold cheap bread to crowds
- HOT1|general|FACT|general|the cook served hot soup at noon

Queries:
- QAN1|probe|SUBJ||||the canine watched the flock in darkness|DOG1
  (SHOULD bridge: dog|canine; helper pairs guarded|watched, sheep|flock, night|darkness)
- QAN2|probe|SUBJ||||the wolf stalked the herd under moonlight| (gold: ABSTAIN;
  wolf must NOT bridge to dog)
- QAN3|probe|SUBJ||||she lent the reaper to her friend| (gold: ABSTAIN;
  lend must NOT bridge to borrow)
- QAN4|probe|SUBJ||||the bazaar offered gratis baguettes to throngs| (gold: ABSTAIN;
  free must NOT bridge to cheap)
- QAN5|probe|SUBJ||||the chef dished spicy bisque at midnight| (gold: ABSTAIN;
  spicy must NOT bridge to hot)
- QAN6|probe|SUBJ||||the penalty fined the merchants for fraud|SAN1
  (SHOULD bridge: sanction|penalty; helpers punished|fined, traders|merchants, cheating|fraud)

### 3.5 MULTI-HOP (diagnostic secondary, 4 probes) — chain composition

Corpus items:
- MH1|general|FACT|general|the old sofa sat against the wall
- MH2|general|FACT|general|the meeting will begin at noon sharp
- MH3|general|FACT|general|the happy child played all day
- MH4|general|FACT|general|the quick fox jumped the fence

Queries:
- QMH1|probe|SUBJ||||the aged settee rested by the barrier|MH1
  (chain sofa|couch|couch|settee; helper old|aged)
- QMH2|probe|SUBJ||||the gathering will commence at midday sharp|MH2
  (chain begin|start|start|commence; helper meeting|gathering)
- QMH3|probe|SUBJ||||the joyful kid frolicked all day|MH3
  (chain happy|glad|glad|joyful; helper child|kid)
- QMH4|probe|SUBJ||||the rapid reynard leapt the barrier|MH4
  (chain quick|fast|fast|rapid; helper jumped|leapt)

### 3.6 MORPH (diagnostic secondary, 4 probes) — irregular morphology

Corpus items:
- MO1|general|FACT|general|they go to the market each morning
- MO2|general|FACT|general|the mouse ate the cheese quickly
- MO3|general|FACT|general|the child played outside daily
- MO4|general|FACT|general|the tooth ached through the night

Queries:
- QMO1|probe|SUBJ||||they went to the bazaar every dawn|MO1
  (pair go|went; helper market|bazaar)
- QMO2|probe|SUBJ||||the mice devoured the cheddar swiftly|MO2
  (pair mouse|mice; helper ate|devoured)
- QMO3|probe|SUBJ||||the children frolicked outdoors every day|MO3
  (pair child|children; helper played|frolicked)
- QMO4|probe|SUBJ||||the teeth throbbed through darkness|MO4
  (pair tooth|teeth; helpers ached|throbbed, night|darkness)

### 3.7 GEN (diagnostic secondary, 2 probes) — post-freeze new learning

After the main test: freeze the learned store (dump + SHA-256), ingest
7 NEW evidence items (below), re-dump, verify old relations intact
(sample check >=20), then run:
- GN1|general|FACT|general|the candle flickered in the cold draft
- QGN1|probe|SUBJ||||the taper sputtered in the chilly breeze|GN1
  (pairs: candle|taper, flickered|sputtered, draft|breeze)
- GN2|general|FACT|general|the mechanic repaired the engine quickly
- QGN2|probe|SUBJ||||the technician fixed the motor swiftly|GN2
  (pairs: mechanic|technician, repaired|fixed, engine|motor, quickly|swiftly)

GEN evidence (ingested only in the post-freeze episode):
- "a candle is a taper." (DEF)
- "flickered and sputtered are synonyms." (SYN)
- "a draft is a breeze." (DEF)
- "a mechanic is a technician." (DEF)
- "repaired and fixed are synonyms." (SYN)
- "an engine is a motor." (DEF)
- "quickly and swiftly are synonyms." (SYN)

## 4. Learning corpus (frozen specification; generated deterministically)

Format: `LEARN|lid|pattern|text`, pattern in {DEF, SYN, PARA, NEG}.
`PARA` lines carry a subject tag: `LEARN|lid|PARA|subj|text`; two lines
share a subj. Generation script is deterministic (fixed templates, no
RNG); the generated file is committed.

Required coverage (every pair below gets evidence; no other
word-relations are evidenced):
- All 56 WS2-B2 table pairs (section: table list in PREREG_WS2B2.md):
  each gets one DEF ("a {w1} is a {w2}.") and one SYN
  ("{w1} and {w2} are synonyms.").
- All FRESH pairs (28, section 3.2): one DEF + one SYN each.
- 12 of the FRESH pairs (2 per probe: river|stream, valley|vale,
  ocean|sea, rocks|stones, forest|woods, miles|leagues, mountain|peak,
  clouds|mist, teacher|instructor, student|pupil, journey|voyage,
  ship|boat): additionally two PARA subject-pairs each (4 lines),
  identical sentences differing in exactly that word.
- ADV-NEAR positives (8, section 3.4): one DEF + one SYN each.
- ADV-NEAR negatives (4): NEG lines "a wolf is not a dog.",
  "borrow is not lend.", "cheap is not free.", "hot is not spicy."
- MULTI-HOP pairs (12, section 3.5): one DEF + one SYN each.
- MORPH pairs (8, section 3.6): one SYN ("{w1} and {w2} are synonyms.")
  plus one explicit form sentence ("{w2} is the past form of {w1}." /
  "{w2} is the plural form of {w1}.") each.

Total: 112 positive relations evidenced; 4 negatives. The script asserts
these counts. No test query text appears in the corpus; no corpus item
text appears in the corpus (word-meaning evidence only, never knowledge).

## 5. Kill bars (all must pass for ARM L; K5 also scored for ARM B)

- K1 NO HALLUCINATION: audit script verifies every installed relation in
  the frozen store traces to >=1 corpus evidence item matching its
  installing rule (R1/R2: pattern match; R3: two independent PARA
  subjects). Zero orphan relations or K1 fails.
- K2 NO BAKED-IN PAIRS: byte-scan of ARM L's .zag sources AND compiled
  binary for all 56 curated "w1|w2" strings and the table SHA-256;
  zero hits. (Corpus data files are evidence, excluded from this scan.)
- K3 DETERMINISM: learning + all test batteries rerun 3x from clean
  state; all outputs byte-identical.
- K4 ZERO RNG: grep L sources for rand/srand/random/lcg/seed/shuffle/
  clock/time/getrandom; zero hits.
- K5 DISTRACTOR PRECISION: ARM L scores DIST 6/6 (zero decoy retrievals).
- K6 NEAR-SYNONYM PRECISION: ARM L scores ADV-NEAR 6/6. Any false
  bridge (QAN2-QAN5 retrieving) kills L regardless of total score.
- K7 NON-DEGENERACY: frozen store holds >=50 and <=200 relations; and
  ARM L official-51 score >= 50 (it must actually learn the vocabulary,
  not ride phase 1).

## 6. Protocol order (frozen)

1. Commit this prereg (frozen). No WS2-L code, corpus, or runs before.
2. ARM B validation: rebuild WS2-B2 from frozen sources, verify
   byte-identity of the official-51 run (must replicate 51/51), run all
   section-3 batteries. PREDICTED B scores: OFFICIAL 51/51, FRESH 0/6,
   DIST 6/6, ADV-NEAR 4/6 (QAN1/QAN6 miss), MULTI-HOP 0/4, MORPH 0/4.
   GATE: if any new-battery B score deviates from prediction, the
   battery leaks (phase-1 overlap) and must be rephrased until the
   prediction holds, all rephrasings documented. Batteries are final
   when the gate passes.
3. ARM L: generate corpus (assert counts), build mechanism, document
   mechanism (rules, transitivity choice) and commit BEFORE learning
   runs; run learning; dump + audit K1/K2; freeze store (SHA-256);
   run all batteries 3x (K3); score.
4. GEN episode per section 3.7 (diagnostic).
5. Apply the decision rule (section 7), execute, commit verdict.

## 7. Decision rule (frozen)

Primary score S = OFFICIAL-51 (51) + FRESH (6) + DIST (6) + ADV-NEAR (6)
= 69 max per arm. MULTI-HOP, MORPH, GEN are diagnostic (reported, not
decisive).

- If ARM L passes K1-K7 AND S_L >= S_B: ADOPT L. The curated
  SYN_TABLE_V1.txt and its generated syn_table.zag are DELETED from the
  repo (git rm, deletion recorded in the verdict). L's learned store
  and mechanism become the synonymy mechanism.
- If S_L < S_B or any kill bar fails: the bridge stays as a STOPGAP;
  ARM L returns for harder training. The bridge is never the end state
  (standing law).
- Exact tie (S_L == S_B) with all kill bars passing: L WINS (Micah's
  law favors the learned mechanism).

## 8. Commits (tnn-native-lab)

prereg (this file, frozen) -> corpus+mechanism -> evidence+verdict.
Incremental commits; no binaries, no .zagd, no .zag-cache in the repo.
Lab path: docs/lab/cognition_ws/ws2l/.
