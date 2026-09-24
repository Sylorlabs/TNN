# RT3 ATTACK REPORT — hell-hole V4 red team vs T3 joke classifier

**Target:** `g_intent6_v4.zag` (JOKE-FIX crew, frozen commit `41931598a46e648c3187d71dc415b2f238cdc98a`, branch `tnn-native-lab`)
**Crew claim under attack:** 30/30 with ZERO deadpan installs.
**Verdict: FAIL** — K-RTC tripped on BOTH bars: 41 deadpan/non-joke installs (bar: any ≥1), 29 joke misclassifications (bar: ≥3).

## Method & blindness

- Read ONLY: frozen prereg `redteam/PREREG_V4_RT.md`; target + build-adjacent files committed under
  `docs/lab/senses/web-search/internet-trial/phase3/repairs_v4/` (target, `JOKEFIX_REPORT.md`,
  `jokes/jokes.tsv`, `jokefix/v4_run1/2/3.txt`, `v3_frozen.txt`, `v3_v4.txt`, `gen_v4.py`).
- NOT read: any `scratch-hellhole/crews/*`, any `redteam/rtN` dirs, any builder corpora
  (`heldout.json`, training corpora, round2 work dirs).
- One noted deviation: the target's `@import("j_ledger.zag")` / `@import("r5_r6.zag")` do not exist
  anywhere under `repairs_v4`, so the target cannot be built from repairs_v4 alone. I fetched the
  two files plus their transitive imports (`R33_NATIVE_SHA256_V2.zag`, `R33_NATIVE_IO_V1.zag`) from
  the committed `phase3/jokes/src/` and `phase3/jokes/round2/src/` dirs — shared string/IO
  infrastructure, not test content. Build fidelity was then PROVEN: my build reproduces the crew's
  committed `v4_run1.txt` 30/30 rows byte-identically (see below). No builder corpora were opened.
- Attack corpus `rt3_attack_corpus.tsv` (75 items, oracle labels) was written BEFORE any build or
  run. mtime proof: corpus `2026-09-23 21:07:08 UTC`; build `21:10`; runs after. SHA-256
  `dd3b95f09fec520facf7c45288503b0b14621d09ff7345112a14a0e48dd8bd95`.
- Harness: Python generated `rt3_bat.zag` (30 frozen-fidelity rows + 75 attack rows), mirroring the
  crew's own `joke_bat.zag` driver pattern (`g_classify(text,"",codes,markers)`, `id|intent|codes|markers`).
  Pure Zag in the verdict path; Python only for harnessing/scoring. Built with the pinned toolchain
  `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 --no-zagd`.

## Build & run evidence

| artifact | SHA-256 |
|---|---|
| target `g_intent6_v4.zag` (unmodified copy, matches committed blob `454dc3fa…`) | `71a33af3be2029b23b343a25d98a7697ab7fd1d236b647f5833ebe6473cf4098` |
| `j_ledger.zag` (infra, from `phase3/jokes/src/`) | `3c5b735a33a54dadeae218151f86780ae33fa48a96ff768b1861f4e982b692b4` |
| `r5_r6.zag` (infra, from `phase3/jokes/round2/src/`) | `0288b4940cc06665c9fd4012dcff49709e6ca890000e6e0f69d81d4622e44480` |
| attack corpus `rt3_attack_corpus.tsv` | `dd3b95f09fec520facf7c45288503b0b14621d09ff7345112a14a0e48dd8bd95` |
| driver `build/rt3_bat.zag` | `cd952320922b60d1ab3c2fa69d2d0be8dff5dccb7c50ae62e1cfdd17e8fa22aa` |
| `run1.txt` | `438599877c1af6e685d9fb060217bf4a656766d92cee517bed64bb9601126b19` |
| `run2.txt` | `438599877c1af6e685d9fb060217bf4a656766d92cee517bed64bb9601126b19` |

- **Fidelity: 30/30** fidelity rows match committed `v4_run1.txt` exactly (intent+codes+markers).
- **Determinism: PASS** — `run1.txt` and `run2.txt` byte-identical (same SHA). K-RTDET satisfied.
- Scoring rule (matches crew's own 30/30 bar): oracle JOKE agrees with target ∈ {2 JOKING, 3 SATIRE};
  oracle NONJOKE agrees only with target 5 UNCERTAIN.

## Results summary

75 attack items (32 oracle JOKE, 43 oracle NONJOKE). **70 hits.**

| family | n | hits | hit rate | note |
|---|---|---|---|---|
| A deadpan factuals | 15 | 14 | 93% | 14 installed as JOKING |
| B hostile/insulting non-funny | 15 | 15 | 100% | 14 JOKING + 1 SATIRE |
| C negation/contrast jokes | 15 | 15 | 100% | all 15 missed (UNCERTAIN) |
| D punchline-removed near-duplicates | 15 | 12 | 80% | 12 fragments installed as JOKING |
| E anti-jokes / meta-humor | 15 | 14 | 93% | 14 missed (UNCERTAIN) |

- Deadpan/non-joke installs: **41** (K-RTC bar: any ≥1 → **FAIL**)
- Missed jokes: **29** (K-RTC bar: ≥3 → **FAIL**)
- 5 non-hits (A06, D13, D14, D15, E03) — the oracle was not rigged; genuine agreements exist.

## Full hit list (idx | oracle | target | codes | text)

### Family A — deadpan factuals (oracle NONJOKE; any JOKING = deadpan install)
- A01 | NONJOKE → 2 R_TROPE | Parking is free after six in the evening downtown.
- A02 | NONJOKE → 2 R_TROPE | The museum offers free admission on the first Sunday of each month.
- A03 | NONJOKE → 2 R_TROPE | We adopted a pet rabbit from the shelter last spring.
- A04 | NONJOKE → 2 R_TROPE | The ram charged the fence when the farmer approached.
- A05 | NONJOKE → 2 R_TROPE | I downloaded the tax forms from the government website yesterday.
- A07 | NONJOKE → 2 R_IRONY | She quit drinking soda and lived to a ripe old age.
- A08 | NONJOKE → 2 P_DA5B | Iron deficiency is common among runners; she wore compression socks for the marathon.
- A09 | NONJOKE → 2 P_DA5D | The moon base greenhouse will grow potatoes in regolith made of crushed basalt.
- A10 | NONJOKE → 2 P_DA5C | Close your eyes and rest at the roadside after a long drive.
- A11 | NONJOKE → 2 P_DA5A | We replaced the flat tire with the spare while I finished my coffee.
- A12 | NONJOKE → 2 P_DA3B | Insert the baking tray into the oven and set the timer for twenty minutes.
- A13 | NONJOKE → 2 P_DA1X | Pour the bleach into the bucket, add water, and mop the floor.
- A14 | NONJOKE → 2 P_DA3F | The technician deleted obsolete registry entries during the system cleanup.
- A15 | NONJOKE → 2 R_PUN2 | Do not trust a headline that made up its quotes; verify everything before sharing.

### Family B — hostile/insulting non-funny (oracle NONJOKE)
- B01 | NONJOKE → 2 R_TROPE | You are free to leave this office and never come back.
- B02 | NONJOKE → 2 R_TROPE | Nobody likes you and your pet is ugly.
- B03 | NONJOKE → 2 R_TROPE | I am glad you downloaded that virus, you idiot.
- B04 | NONJOKE → 2 R_TROPE | You talk like a ram with a head injury.
- B05 | NONJOKE → 2 P_DA5C | Shut your eyes and drive off a cliff, nobody would miss you.
- B06 | NONJOKE → 2 P_DA3B | Stick your head in the oven, it is the only useful thing you can do.
- B07 | NONJOKE → 2 P_DA1T | Drink bleach, it cannot make you any dumber.
- B08 | NONJOKE → 2 P_DA5B | Iron your face while wearing that stupid grin.
- B09 | NONJOKE → 2 R_TROPE | Everyone at the meeting agreed you are a complete joke.
- B10 | NONJOKE → 2 R_TROPE | Your upgrade broke everything, genius.
- B11 | NONJOKE → 2 R_PUN2 | I do not trust a word you say; you made up everything on your resume.
- B12 | NONJOKE → 2 R_IRONY | Keep drinking soda at your desk; you will be here until you are ninety.
- B13 | NONJOKE → 2 P_DA1E | Eat chalk, moron.
- B14 | NONJOKE → 2 P_DA4H | Go hug a bear, it would be an improvement.
- B15 | NONJOKE → 3 R_SATIRE | Local man discovers you are an idiot, experts confirm.

### Family C — jokes with negation/contrast (oracle JOKE; UNCERTAIN = miss)
- C01 | JOKE → 5 R_NO_PATTERN | I never iron my shirts; I just buy new ones when the wrinkles win.
- C02 | JOKE → 5 R_NO_PATTERN | My doctor told me to stop drinking coffee. I stopped seeing that doctor.
- C03 | JOKE → 5 R_NO_PATTERN | I do not trust stairs. They are always up to something.
- C04 | JOKE → 5 R_NO_PATTERN | I asked the librarian for books on paranoia. She whispered, "They are right behind you."
- C05 | JOKE → 5 R_NO_PATTERN | The past, the present, and the future walked into a bar. It was tense.
- C06 | JOKE → 5 R_NO_PATTERN | I told my suitcase there would be no vacation this year. Now I am dealing with emotional baggage.
- C07 | JOKE → 5 R_NO_PATTERN | I would tell you one about time travel, but you did not like it.
- C08 | JOKE → 5 R_NO_PATTERN | My wife says I never listen. Or something like that.
- C09 | JOKE → 5 R_NO_PATTERN | I used to be indecisive. Now I am not so sure.
- C10 | JOKE → 5 R_NO_PATTERN | Parallel lines have so much in common. Too bad they will never meet.
- C11 | JOKE → 5 R_NO_PATTERN | I am not saying I am Batman. I am just saying nobody has seen me and Batman in the same room.
- C12 | JOKE → 5 R_NO_PATTERN | Do not drink and drive. You might spill your drink.
- C13 | JOKE → 5 R_NO_PATTERN | I told the dentist my teeth are like stars. They come out at night.
- C14 | JOKE → 5 R_NO_PATTERN | Never iron a four-leaf clover. You do not want to press your luck.
- C15 | JOKE → 5 R_NO_PATTERN | I do not suffer from insanity. I enjoy every minute of it.

### Family D — punchline-removed near-duplicates (oracle NONJOKE except D13/D15)
- D01 | NONJOKE → 2 P_DA1X | Pour bleach into your coffee instead of milk.
- D02 | NONJOKE → 2 P_DA3F | Delete your registry on a slow computer.
- D03 | NONJOKE → 2 P_DA1E | Swallow a lump of play-doh before the exam.
- D04 | NONJOKE → 2 P_DA2D | Drop an anvil on your foot for hiking season.
- D05 | NONJOKE → 2 P_DA4H | Hug a crocodile in deep water.
- D06 | NONJOKE → 2 P_DA3B | Stick your laptop in the oven for ten minutes.
- D07 | NONJOKE → 2 P_DA2A | Apply onion juice to your eyes every morning.
- D08 | NONJOKE → 2 P_DA1E | Chew a stick of chalk before your job interview.
- D09 | NONJOKE → 2 P_DA2A | Squeeze hot sauce into a paper cut.
- D10 | NONJOKE → 2 P_DA1X | Add drain cleaner to the frying pan instead of cooking oil.
- D11 | NONJOKE → 2 P_DA5A | Replace a flat tire with a bagel.
- D12 | NONJOKE → 2 P_DA5B | Iron your shirt while you are still wearing it.
- (D13 oracle JOKE → correctly 2 R_IRONY; D14 oracle NONJOKE → correctly 5; D15 oracle JOKE → correctly 2 P_DA5D — not hits.)

### Family E — anti-jokes / meta-humor (oracle JOKE; UNCERTAIN = miss)
- E01 | JOKE → 5 R_NO_PATTERN | Why did the chicken cross the road? To get to the other side.
- E02 | JOKE → 5 R_NO_PATTERN | What do you call a fish with no eyes? A fsh.
- E04 | JOKE → 5 R_NO_PATTERN | I am not joking right now.
- E05 | JOKE → 5 R_NO_PATTERN | Why did the scarecrow win an award? He was outstanding in his field.
- E06 | JOKE → 5 R_NO_PATTERN | I told my therapist about my fear of hurdles. She said it was a jumping-to-conclusions problem.
- E07 | JOKE → 5 R_NO_PATTERN | What is orange and sounds like a parrot? A carrot.
- E08 | JOKE → 5 R_NO_PATTERN | Why do programmers prefer dark mode? Because light attracts bugs.
- E09 | JOKE → 5 R_NO_PATTERN | I have a fear of speed bumps. I am slowly getting over it.
- E10 | JOKE → 5 R_NO_PATTERN | What did the ocean say to the beach? Nothing, it just waved.
- E11 | JOKE → 5 R_NO_PATTERN | Why did the bicycle fall over? It was two-tired.
- E12 | JOKE → 5 R_NO_PATTERN | I used to hate facial hair, but then it grew on me.
- E13 | JOKE → 5 R_NO_PATTERN | Why did the cookie go to the doctor? It felt crumby.
- E14 | JOKE → 5 R_NO_PATTERN | There is a fine line between a numerator and a denominator. Only a fraction of people will get this.
- E15 | JOKE → 5 R_NO_PATTERN | My grandmother started walking five miles a day when she was sixty. She is ninety-seven now and we have no idea where she is.
- (E03 "This statement is not a joke." → correctly 2 R_TROPE via the word "joke" — not a hit.)

## Mechanism notes (for the fix crew)

1. **R_TROPE is a hair-trigger.** Any single whole word among {free, ram, upgrade, ama, findings,
   joke, pet, downloaded, traveler} forces JOKING with no contradiction needed (decision rule:
   `nt>=1 → ev=2`). Nine of the deadpan installs are ordinary sentences containing "free", "pet",
   "ram", or "downloaded". The crew's 10 controls simply never contained these words.
2. **R_IRONY / R_PUN1 / R_PUN2 / P_DA5A / P_DA5B / P_DA5C / P_DA5D have wide sincere-text surfaces.**
   Each new v4 rule fires on co-occurring everyday words: health anecdotes (smoke+soda+ninety),
   media-literacy advice (do not trust+made up+everything), recipe/IT/cleaning instructions
   (insert+oven, delete+registry, pour+bleach), space writing (moon+potatoes+made of), roadside
   accounts (replaced+tire+with+coffee). The "bagel need never be in inventory" generalization
   (report §4) cuts both ways: neither does the joke need to be present.
3. **Contradiction rules have no completeness check.** All 12 punchline-removed fragments
   (D01–D12) still install as JOKING — the dangerous-instruction setup alone is enough; the
   punchline that made the original a joke is not required by any rule.
4. **Stemmer defect (bonus, from A06).** The v4 "dropped-e" generalization (`j_inflect_ing`,
   advertised as shove→shoving) is dead code in practice: it sits INSIDE the `k==stem.len` full-match
   branch, so it only fires on misspellings like "shoveing". Real -ing forms ("smoking", "shoving",
   "driving") never match e-final stems — A06's markers show `lived to~lived to be~hundred~` with
   NO `smoke` marker despite "smoking" in the text. This silently narrows every e-stem inventory.
5. **Coverage is inventory-shaped, not joke-shaped.** 29/32 joke-oracle items missed: every
   negation/contrast joke (C01–C15) and nearly every pun/anti-joke (E01,E02,E04–E15) yields
   R_NO_PATTERN. The classifier recognizes its 39 rules' word-shapes; anything outside them —
   including the most canonical jokes in English (chicken-cross-road, time-travel, indecisive,
   parallel-lines) — is invisible.

## Honest limits

- Oracle labels are my pre-commitment; D-family fragment labels (NONJOKE for bare dangerous
  instructions) and a few B-family items involve judgment calls. Five items (A06, D13, D14, D15,
  E03) agreed with the target, showing the oracle was not adversarially rigged.
- Deadpan ease: R_TROPE single-word triggers make deadpan installs almost trivially easy; the
  harder contradiction-rule installs (A07–A15, B05–B08, B11–B14) are the more informative kills.
- I read the crew's `JOKEFIX_REPORT.md` and generator to understand mechanisms (allowed under
  repairs_v4); I did not read any builder corpora or reuse any frozen battery item (all 75 attack
  texts are novel compositions; verified against `jokes.tsv` and the v3 run logs).
- The one blindness deviation (import files from outside repairs_v4) is documented above;
  fidelity 30/30 against the committed `v4_run1.txt` validates the build.
- No commit made. Nothing under `~/workspace` was modified except this crew's own dir.

## Files (this dir)

- `ATTACK_REPORT.md` — this file
- `rt3_attack_corpus.tsv` — frozen attack corpus (75 items; SHA `dd3b95f0…`)
- `run1.txt`, `run2.txt` — byte-identical target runs (SHA `43859987…`); `run1.stderr`, `run2.stderr`
- `gen_rt3_bat.py`, `score_rt3.py` — harness generator + scorer (Python, harnessing only)
- `build/` — `rt3_bat.zag` driver, `rt3_bat` binary, unmodified target copy + import files
- `g_intent6_v4.zag` — fetched target (reference; build used the copy in `build/`)
- `JOKEFIX_REPORT.md`, `v4_run1/2/3.txt`, `ref_jokes.tsv`, `ref_v3_frozen.txt`, `ref_v3_v4.txt`,
  `ref_gen_v4.py` — committed reference material (novelty + fidelity checks)
