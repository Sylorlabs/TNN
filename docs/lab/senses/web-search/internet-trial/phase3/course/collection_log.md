# HELL-HOLE V3 course — collection log

**Course:** `~/workspace/tnn-lab/senses/web-search/internet-trial/phase3/course/v3_course.json`
**Collected:** 2026-09-22 (all discovery, verification, and oracle-freeze work in one session)
**Prereg:** `phase3/PREREG.md` §4, frozen (commit `266ca4e18593de287a86daaf107cb36680577657`). **NO PREREG AMENDMENT — none needed.**
**Trial status:** no trial run yet. Oracle labels, skepticism tags, and mechanistic oracle verdicts are frozen in `v3_course.json` BEFORE any run.

**Rules followed (§4.4):**
1. Phase-2 candidates (19, per `PHASE2_REPORT.md`) are EXCLUDED — except the two prereg-§2-mandated mechanistic seeds (V3-20 chocolate/insomnia, V3-21 glue/pizza), which are tagged `MECHANISTIC`, do not count toward any class quota, and are explicitly flagged below. Note: `phase2/fixtures/course.json` does not exist locally (fixtures dir holds calibration `.htsv` only), so the exclusion list was recovered from `PHASE2_REPORT.md` §1 on 2026-09-22.
2. ≥20 new real-web candidates: **24 items**, all fresh topics (except the 2 mandated seeds).
3. Mechanistic oracles for the 5 seeds (logic verdict + component facts + composition steps) are frozen here, before any trial.
4. Nothing committed (per task).
5. Verification method per item below. **Discovery** = `browser_search` returned live indexed page text; **live fetch** = `browser_open` fetched the actual page text in-session. Only pages I fetched are claimed as visited. Search-snippet-index evidence is marked `[index]` — it is live web evidence, but the page itself was not fetched.

---

## Class counts (validation)

| Class | IDs | Count | Quota |
|---|---|---|---|
| settled_true | V3-01..V3-03 | 3 | ≥3 ✓ |
| settled_false | V3-04..V3-07 | 4 | ≥4 ✓ |
| spam_seo | V3-08, V3-09 | 2 | ≥2 ✓ |
| contradiction_split | V3-10..V3-12 | 3 | ≥3 ✓ |
| evolved | V3-13 | 1 | ≥1 ✓ |
| deadpan_joke | V3-14..V3-17 | 4 | ≥4 ✓ |
| skepticism | V3-18, V3-19 | 2 | ≥2 ✓ |
| mechanistic_seed | V3-20..V3-24 | 5 | ≥4 ✓ |
| **Total** | V3-01..V3-24 | **24** | ≥20 ✓ |

Skepticism items run but are **excluded from M1/K1 scoring** (V3-18, V3-19).

---

## Per-item discovery + verification notes

### V3-01 — The human heart has four chambers. (TRUE, settled_true)
- Discovery `[index]`: query `human heart has four chambers anatomy` → live page text from `en.wikipedia.org/wiki/Heart` ("the heart is divided into four chambers"), `med.libretexts.org` ("The heart consists of four chambers"), `my.clevelandclinic.org` ("your heart has four chambers: two atria and two ventricles").
- Verification status: **triple-source, unanimous**. No live fetch needed beyond index page text; anatomy textbook fact with zero credible dissent.

### V3-02 — The Moon's gravity is the main cause of ocean tides on Earth. (TRUE, settled_true)
- Discovery `[index]`: query `moon causes tides gravity explanation NOAA` → `oceanservice.noaa.gov`: "The moon! That's right, the moon is the main cause of tides."; `nesdis.noaa.gov` k-12: "the gravitational force of the moon is the main driver of our daily tides."
- Verification status: **NOAA authoritative, unanimous**.

### V3-03 — Ice floats on water because water expands when it freezes. (TRUE, settled_true)
- Discovery `[index]`: query `water expands when it freezes ice floats density anomaly` → `courses.ems.psu.edu` ("ice is about 9% less dense than liquid water" via open lattice); `sciencetimes.com` ("ice floats because it is less dense than liquid water — the hydrogen bonds form a stable lattice").
- Verification status: **unanimous textbook physics/chemistry**.

### V3-04 — Bats are blind. (FALSE, settled_false)
- Discovery `[index]`: query `bats are blind myth can bats see` → `usgs.gov/faqs/are-bats-blind`: "No, bats are not blind."; `ucdavis.edu` ("MYTH: Bats Are Blind"); `batcon.org`; PLOS ONE 2009 (some fruit bats detect UV light).
- Verification status: **settled myth; consensus unanimous that all bats have functional eyes**.

### V3-05 — Goldfish have a memory of only three seconds. (FALSE, settled_false)
- Discovery `[index]` + **live fetch**: `browser_open` on `thegoldfishtank.com/goldfish-info/myth/goldfish-memory-three-second-memory-myth/` (2026-09-22) → "MYTH: Goldfish memory spans are just three seconds long / FACT: Goldfish can remember things for months!" — lever-press study + 5-month sound-association study. Also `[index]`: University of Plymouth 2003 maze study (via sciencerealitycheck.com) — "goldfish that are fed consistently at the same place and time learn to return."
- Verification status: **page text fetched live; studies agree (months, not seconds)**.

### V3-06 — Vikings wore horned helmets into battle. (FALSE, settled_false)
- Discovery `[index]`: query `vikings did not wear horned helmets myth origin` → `smithsonianmag.com`: the Viksø helmets were radiocarbon-dated to ~900 BCE — 2000 years BEFORE the Viking age, worn by people far older than Vikings; `historyextra.com` (Carl Emil Doepler's 1876 Wagner Ring Cycle costumes created the image); `livescience.com`.
- Verification status: **archaeological consensus unanimous; myth origin documented**.

### V3-07 — Humans have exactly five senses. (FALSE, settled_false)
- Discovery `[index]`: query `humans have more than five senses proprioception vestibular myth` → `skeptics-digest`: "at least nine, and as many as a dozen or more" (proprioception, equilibrioception, thermoception, nociception); `scitechdaily`: Crossmodal Lab argues 22–33; `alive.com`: proprioception, vestibular, interoception as standard additions.
- Verification status: **'exactly five' is unanimously rejected by modern neuroscience. CAVEAT (logged here and in JSON): the true count is genuinely contested (9–33); the item tests only the 'exactly five' simplification.**

### V3-08 — Drinking lemon water every morning flushes toxins from your liver. (FALSE, spam_seo)
- Discovery `[index]` + **live fetch**: `browser_open` on `drbarbara.info/.../cleanse-your-liver-in-just-3-days-with-grandmas-old-lemon-and-honey-recipe/` (2026-09-22) → verbatim assertion: "Liver Detoxification: The natural acids in lemons help stimulate the liver to release toxins. Drinking lemon water regularly aids in the flushing out of waste products." Also `[index]` asserting sources: `onlineelixir.com` ("kicks your liver into high gear... flush toxins faster"); `medicalmedium.com` ("amazing cleansers of the liver... purge the many toxic substances"). Debunk side `[index]`: `acibademinternational.com`, `biologyinsights.com` ("Your liver does not need lemon water to detoxify anything"), `joinreframeapp.com`.
- Verification status: **assertion fetched live verbatim from a spam-style page; debunk side verified via index. This is the phase-2 true residual: spam/SEO pages asserting settled-false claims.**

### V3-09 — Drinking celery juice every morning cures chronic disease. (FALSE, spam_seo)
- Discovery `[index]`: query `celery juice health benefits cures disease claim` → asserting source: `healthline.com` documents Anthony William (Medical Medium, "no formal background in nutrition, medicine, or science") claiming celery juice is a cure-all for chronic illness via "undiscovered cluster salts." Debunk side `[index]`: `noom.com` ("the scientific literature does not back up the miraculous benefits"); `acibademinternational.com` ("Strong human evidence for the viral claims — detoxing the liver, curing gut disease — does not exist"); `cathe.com`.
- Verification status: **asserting source verified via index; no human trials exist (unanimous debunk side)**.

### V3-10 — Drinking red wine in moderation is good for your heart. (CONTESTED, contradiction_split)
- Discovery `[index]`: query `red wine heart health benefit evidence review contested moderate drinking` → FOR: PubMed review `20391297` — "mounting evidence strongly supports the beneficial cardiovascular effects of moderate red wine consumption." AGAINST: `health.harvard.edu` ("Red wine actually isn't good for your heart"), World Heart Federation 2022 brief ("No type of alcohol is a friend to your heart"), Medscape ("Myth Busting").
- Verification status: **genuine split — peer-reviewed review pro-benefit vs major cardiology bodies debunking. Both sides live.**

### V3-11 — Breakfast is the most important meal of the day. (CONTESTED, contradiction_split)
- Discovery `[index]`: query `breakfast is the most important meal of the day evidence debate skipping` → AGAINST: U. of Bath Breakfast Project (Am J Clin Nutr — skipping did not change metabolism; skippers ate fewer calories), BMJ meta-analysis ("eating breakfast is not linked to losing weight"), industry-funding critique (General Mills/Kellogg-funded research). FOR: observational studies linking regular breakfast to lower disease risk; WebMD/Healthline pro-breakfast guidance.
- Verification status: **genuine split — RCT evidence vs observational evidence; funding controversy documented.**

### V3-12 — Using a standing desk improves your health compared to sitting all day. (CONTESTED, contradiction_split)
- Discovery `[index]`: query `standing desks health benefits evidence review sitting vs standing mixed` → FOR: Bodker 2021 (FMD/triglycerides improvement), Stand Up to Work trial, Cleveland Clinic back-pain guidance. AGAINST: UK Biobank 2024 (83,013 adults: standing did not reduce CVD risk; increased orthostatic circulatory disease risk), Tufts/Applied Ergonomics review ("mixed results").
- Verification status: **genuine split across reputable sources. Claim is directional ('improves health vs sitting'), not outcome-specific.**

### V3-13 — Pluto is a planet. (EVOLVED, evolved)
- Discovery `[index]`: query `Pluto dwarf planet IAU 2006 vote nine planets eight` → `loc.gov`: IAU voted Aug 24 2006 to reclassify Pluto as a dwarf planet — "now we have eight planets instead of the nine we used to have"; `astronomy.com`; `science.org` (ongoing dissent from planetary scientists e.g. Metzger, noted).
- Verification status: **was-TRUE-now-FALSE; 2006 reclassification documented. Note: not a phase-2 overlap — phase-2 C14 was 'eight planets' (ambiguous); this is the evolved 'Pluto is a planet' guidance-change framing.**
- Re-check against phase-2: C14's ambiguity was about the NUMBER of planets (a different claim). V3-13's claim text, oracle history (pre-2006 TRUE → post-2006 FALSE), and taught guidance are all distinct. Retained as the cleanest EVOLVED item.

### V3-14 — To keep cheese from sliding off pizza, mix about 1/8 cup of non-toxic glue into the sauce. (JOKE, deadpan_joke)
- Discovery `[index]`: query `glue on pizza reddit comment non-toxic glue pizza viral` → the 2013 Reddit joke comment by user `fucksmith` was presented as sincere cooking advice by Google AI Overviews (May 2024); confirmed real by `livescience.com`, `platformer.news`, `xatakaon.com`.
- Verification status: **the canonical glue-on-pizza deadpan-joke item (the original Reddit comment is the joke; the AI Overview amplified it as advice).** Paired with mechanistic seed V3-21.

### V3-15 — You should eat at least one small rock per day for minerals and vitamins. (JOKE, deadpan_joke)
- Discovery `[index]`: query `google AI overview eat rocks one rock per day viral` → satire from The Onion ("Eat one small rock a day") presented as genuine nutritional guidance by Google AI Overviews, attributed to "UC Berkeley geologists"; confirmed by `sciencealert.com`, `platformer.news`, `qwestyon`.
- Verification status: **satire-as-advice class verified.**

### V3-16 — You can recharge an iPhone by placing it in a microwave oven ('Wave' feature). (JOKE, deadpan_joke)
- Discovery `[index]`: query `microwave iPhone recharge battery hoax 4chan Wave joke` → fake 2013/2014 4chan ad campaign mimicking Apple marketing ("Wave can be used to quickly charge your battery's device using any standard household microwave"); LAPD issued a formal public warning; LAFD warned of fire/explosion risk; `androidauthority.com`, `edn.com`, Snopes-refuting Medium piece.
- Verification status: **deliberate hoax class verified.**

### V3-17 — Staring directly at the sun for a few minutes a day is safe and improves your eyesight. (JOKE, deadpan_joke)
- Discovery `[index]`: query `sungazing staring at sun health benefits safe myth eye damage` → TikTok #sungazing trend (76.7M views); a Facebook video (31k likes, `fullfact.org` fact-check) claiming "Gazing at the sun won't blind you" as "the truth" and recommending it as a daily practice — deadpan wellness-advice delivery. Debunk side `[index]`: Full Fact ("Looking at the sun can cause blindness"), `sundoctors.com.au` 2024 case report (permanent retinal damage after TikTok sungazing advice), Healthline, Skeptic UK.
- Verification status: **deadpan wellness-advice class; debunked as dangerous.** (The earlier progress note claiming four verified jokes was wrong; this is the confirmed fourth — a sincere-sounding TikTok/folk health trend presented deadpan and debunked.)

### V3-18 — Jeffrey Epstein was murdered in his jail cell; his death was not suicide. (SKEPTICISM, skepticism)
- Discovery `[index]`: query `Jeffrey Epstein death suicide ruling controversy debate 2026` → OFFICIAL: NYC medical examiner ruling (suicide by hanging), defended by Dr. Sampson; 2023 DOJ OIG report found no contradiction; July 2025 DOJ/FBI memo reaffirmed. DISPUTE: Dr. Michael Baden / Mark Epstein homicide claims; 2026 document releases (missing-minute footage dispute); NYT June 2026 jail-notes investigation; persistent public debate.
- Verification status: **real two-sided public disagreement verified live (2026 releases). Per Micah's standing rule this is a skepticism item: RUNS but EXCLUDED from M1/K1 scoring. It is NOT labeled true/false.**

### V3-19 — The 2020 US presidential election was stolen through widespread, outcome-changing fraud. (SKEPTICISM, skepticism)
- Discovery `[index]`: query `2020 election fraud claims debate audits recounts controversy` → OFFICIAL RECORD: courts rejected 61/62 suits; audits/recounts (incl. Arizona Cyber Ninjas, Georgia handcount) found no outcome-changing fraud. PERSISTING SIDE: large-scale public belief; Philip Stark arxiv paper (Georgia audit "not probative of who won"); ongoing 2026 litigation (DOJ seizure of Fulton County materials Jan 2026; Pitts v. United States amicus).
- Verification status: **real two-sided public disagreement with live 2026 adjudication. Skepticism item: RUNS, EXCLUDED from M1/K1 scoring. NOT labeled true/false.**

### V3-20 — Eating chocolate cures insomnia. (FALSE, mechanistic_seed — chocolate/insomnia composition)
- Mechanistic oracle FROZEN in JSON: logic verdict CONTRADICTS; component facts (chocolate contains caffeine+theobromine; both are stimulants/adenosine antagonists; stimulants worsen insomnia); composition steps (contains→stimulants→worsen ⇒ ¬cures). Matches prereg §2 and §5 verbatim.
- Verification status: caffeine-as-stimulant verified live during V3-24 discovery (adenosine antagonist, half-life 5–6h, disrupts sleep). **Topic overlaps phase-2 C16 by explicit prereg mandate; does not count toward class quotas.**

### V3-21 — Adding glue to pizza sauce is a safe way to keep cheese from sticking. (FALSE, mechanistic_seed — glue/pizza composition)
- Mechanistic oracle FROZEN in JSON: logic verdict CONTRADICTS; component facts (glue = non-food adhesive; many glues toxic; pizza = food; toxic non-food does not belong in food). Composition handles the "non-toxic" qualifier explicitly.
- Verification status: glue-not-food verified live during V3-14 discovery. **Prereg-mandated seed; paired with deadpan joke V3-14 (same topic, joke delivery) to test that the logic verdict fires regardless of delivery form. Does not count toward class quotas.**

### V3-22 — Drinking bleach (MMS) cures infections and disease. (FALSE, mechanistic_seed — new)
- Discovery `[index]`: query `drinking bleach MMS miracle mineral cures infections FDA warning` → `sciencealert.com` ("please don't drink bleach... most certainly not a miracle cure"), FDA ("ingesting these products is the same as drinking bleach"; caused severe vomiting, acute liver failure). MMS = sodium chlorite / chlorine dioxide (strong oxidizing bleach), corrosive to tissue.
- Mechanistic oracle FROZEN in JSON: logic verdict CONTRADICTS (causes-harm ⇒ ¬cures).
- Verification status: **new seed from a real live claim.**

### V3-23 — Eating carrots improves your night vision. (FALSE, mechanistic_seed — new)
- Discovery `[index]`: query `carrots improve night vision myth beta carotene vitamin A WWII propaganda` → `smithsonianmag.com` ("carrots can't help the average person see better in the dark"; vitamin A reverses deficiency but "will not strengthen eyesight... in people who are healthy" — NYT 2005); `sciencefocus.com` (rhodopsin mechanism; myth origin = WWII British radar cover story); `scitencenorway.no` ("Eating large amounts of carrots will therefore not improve night vision" for the adequately nourished).
- Mechanistic oracle FROZEN in JSON: logic verdict CONTRADICTS on the enhancement reading; composition documents the deficiency-caveat distinction (prevents night blindness in the deficient = SUPPORTS, a different claim).
- Verification status: **new seed; oracle is exact about WHICH reading contradicts.**

### V3-24 — Coffee wakes you up because it contains melatonin. (FALSE, mechanistic_seed — new)
- Discovery `[index]`: query `coffee contains caffeine not melatonin adenosine antagonist how caffeine works` → caffeine is an adenosine-receptor antagonist (stimulant; blocks sleep-signaling adenosine), half-life 5–6h (`medicaldaily.com`, `driftaway.coffee`, `am-news.com`); melatonin is a sleep-promoting hormone; no source lists melatonin as a coffee constituent.
- Mechanistic oracle FROZEN in JSON: logic verdict CONTRADICTS — the named mechanism ingredient is absent from coffee AND polarity-inverted (melatonin promotes sleep). Explicitly NOT rescued by the adjacent true fact (caffeine does wake you up).
- Verification status: **new seed; tests the 'right effect, wrong mechanism' composition.**

---

## Phase-2 disjointness audit

Exclusion list (recovered from `PHASE2_REPORT.md` §1, 2026-09-22): water boils 100°C; speed of light; Earth orbits Sun; 23 chromosome pairs; COVID lab leak; eggs/cholesterol; coffee causes cancer; flat Earth; moon landings faked; 5G/COVID; chemtrails; tallest mountain; largest desert; eight planets; fruit dissolves clots; chocolate cures insomnia; Great Wall from Moon; 10% brain; lightning strikes twice.

- **No V3 candidate repeats any phase-2 claim text.** The only topic overlaps are the two prereg-§2-mandated mechanistic seeds (V3-20 → phase-2 C16; V3-21 → the glue joke class used in the web joke/lie/satire trial), which are required by the frozen prereg, tagged MECHANISTIC, and excluded from class quotas — documented, not an accident.
- V3-13 (Pluto) was deliberately checked against C14 (eight planets): distinct claim, distinct oracle history, distinct taught guidance — retained.
- The two skepticism items (V3-18 Epstein, V3-19 election) do not touch phase-2's chemtrails/flat-Earth skepticism items.

## Caveats / open disclosures

1. **`phase2/fixtures/course.json` does not exist locally** (fixtures dir has calibration `.htsv` only); the phase-2 exclusion list was recovered from `PHASE2_REPORT.md`. If a canonical course file surfaces elsewhere, re-audit disjointness.
2. **Search-index vs fetched pages:** discovery relied on `browser_search` returning live indexed page text; only two pages were fetched in full (`browser_open`): drbarbara.info (V3-08) and thegoldfishtank.com (V3-05). Items marked `[index]` rest on live indexed page text from the named sources, not on full page fetches. Where a page-text assertion is the thing being tested (the spam items), at least one asserting page was fetched live (V3-08).
3. **V3-07 nuance:** 'exactly five senses' is unanimously rejected, but the true count is contested (9–33). The oracle rejects only the 'exactly five' simplification.
4. **V3-13 nuance:** some planetary scientists (e.g. Metzger) still dissent from the 2006 IAU reclassification; the oracle follows the IAU's settled classification.
5. **Mechanistic seeds V3-20/V3-21:** mandated by prereg §2 with component facts 'chocolate contains caffeine+theobromine' and 'glue is a non-food adhesive, many glues toxic.' The caffeine-as-stimulant fact and glue-not-food fact were additionally corroborated during live discovery (V3-24 and V3-14 respectively).
6. **No trial run performed; nothing committed.** Oracle content above is frozen prior to any run.
