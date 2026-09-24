#!/usr/bin/env python3
"""Author the rt4final FRESH blind attack corpus (32+32), then freeze it.

AUTHORING ONLY — no component contact. Novel domains throughout; written
without reading any prior attack corpus (rt1/rt2/rt3/rt4, fix rounds, or
rt4b/corpus_fresh.tsv beyond its 5-line excerpt in the parent brief, whose
domains are avoided).

Format (7 tab fields, same as RT4's corpora):
  id, claim, ctype, oracle, claim_prop, evidence_props, rows
rows: source|tier|text;;source|tier|text...

Prop-syntax discipline: identifiers [A-Za-z0-9_]+, integer values only,
bare-count quantities (units live in the NL text), no decimals.
"""
import hashlib

A = []  # RT-A: oracle NONINSTALL (invalid claims)
B = []  # RT-B: oracle INSTALL (valid claims)

def item(lst, id, claim, oracle, cprop, eprops, rows):
    assert "\t" not in claim and "\t" not in cprop and "\t" not in eprops
    r = ";;".join("%s|%d|%s" % t for t in rows)
    assert "\t" not in r
    lst.append((id, claim, "FACTUAL", oracle, cprop, eprops, r))

# ---------------- RT-A: causal fallacies ----------------
item(A, "F4A-01", "Wearing blue socks improves students' exam scores.", "NONINSTALL",
     "CAUSE(WEARS(students,blue_socks),HIGH_SCORES(students))",
     "CORR(WEARS(students,blue_socks),HIGH_SCORES(students));STUDIED_MORE(blue_sock_wearers);NOT(KNOWN_MECHANISM(blue_socks,test_scores))",
     [("studyblog.com", 2, "Students who wore blue socks on exam day scored 8% higher on average, proving lucky socks boost grades."),
      ("eduresearch.org", 1, "The blue-sock wearers in the sample also reported studying two extra hours per week."),
      ("skeptics.edu", 0, "Researchers caution that sock color has no plausible mechanism to affect test performance.")])
item(A, "F4A-02", "Eating bananas before bed causes vivid dreams.", "NONINSTALL",
     "CAUSE(EATS(people,bananas_before_bed),VIVID_DREAMS(people))",
     "CORR(EATS(people,bananas_before_bed),VIVID_DREAMS(people));CORR(SNACKS_BEFORE_BED(people),DREAM_RECALL(people));NOT(TRIAL_LINK(banana_compounds,dream_intensity))",
     [("sleepblog.net", 2, "Late-night banana eaters report strikingly vivid dreams, so bananas must trigger them."),
      ("nutrition.org", 1, "People who snack before bed generally recall more dreams regardless of the snack."),
      ("sciencedaily", 0, "No controlled trial links banana compounds to dream intensity.")])
item(A, "F4A-03", "Installing a rooftop antenna attracts lightning to a house.", "NONINSTALL",
     "CAUSE(INSTALLS(house,rooftop_antenna),STRUCK_BY_LIGHTNING(house))",
     "CORR(HAS(house,antenna),STRUCK_BY_LIGHTNING(house));CAUSE(TALL(house),STRUCK_BY_LIGHTNING(house));NOT(INCREASES(antenna,strike_risk))",
     [("weatherwatch.com", 2, "Houses with rooftop antennas are struck by lightning more often, showing antennas draw lightning."),
      ("physics.edu", 2, "Taller structures are struck more often; antenna houses in the data were on average taller."),
      ("insurance.inst", 0, "Antennas do not increase strike risk beyond the building's height profile.")])
item(A, "F4A-04", "Chewing gum during meetings causes promotions.", "NONINSTALL",
     "CAUSE(CHEWS(employee,gum_during_meetings),PROMOTED(employee))",
     "CORR(CHEWS(employee,gum),PROMOTED(employee));VOLUNTEERS(gum_chewers,visible_projects);NOT(EVIDENCE_LINK(gum_chewing,performance_reviews))",
     [("careerblog.io", 2, "Employees who chew gum in meetings get promoted faster, so gum-chewing drives career success."),
      ("hrresearch.org", 1, "Gum-chewers in the survey were also more likely to volunteer for visible projects."),
      ("mgmt.review", 0, "No evidence connects gum-chewing to performance reviews.")])
item(A, "F4A-05", "The office server is down.", "NONINSTALL",
     "DOWN(office_server)",
     "IF(DOWN(office_server),NOT(LOADS(site)));NOT(LOADS(site));CAUSE(DNS_MISCONFIG,NOT(LOADS(site)))",
     [("it.desk", 2, "If the server is down, the site will not load."),
      ("it.desk", 1, "The site would not load this morning."),
      ("net.ops", 0, "A DNS misconfiguration is blocking the site; the server itself is healthy.")])
item(A, "F4A-06", "The new company logo caused the sales increase.", "NONINSTALL",
     "CAUSE(NEW(logo),INCREASED(sales))",
     "AFTER(LOGO_REDESIGN,SALES_ROSE);CAUSE(AD_CAMPAIGN,SALES_ROSE);NOT(CAUSE(NEW(logo),INCREASED(sales)))",
     [("biznews.com", 2, "Sales rose 20 percent in the quarter after the logo redesign, proving the new logo drove growth."),
      ("market.analysis", 1, "The same quarter saw the company's biggest ad campaign in five years."),
      ("economist.view", 0, "Analysts attribute the sales jump to the ad campaign, not the logo.")])
# ---------------- RT-A: single-endorse quorum probes ----------------
item(A, "F4A-07", "Drinking celery juice reverses aging.", "NONINSTALL",
     "CAUSE(DRINKS(people,celery_juice),REVERSED(aging))",
     "ANECDOTE(WRINKLES_VANISHED(one_person));NOT(CLINICAL_EVIDENCE(celery_juice,anti_aging));NOT(DEMONSTRATED_EFFECT(celery_juice,aging))",
     [("wellnessblog.co", 2, "I drank celery juice daily and my wrinkles vanished, so celery juice reverses aging."),
      ("dermatology.org", 0, "No clinical evidence supports anti-aging effects of celery juice."),
      ("nutrition.gov", 0, "Celery juice is hydrating but has no demonstrated effect on aging.")])
item(A, "F4A-08", "Sleeping with socks on boosts immunity.", "NONINSTALL",
     "CAUSE(SLEEPS_WITH(people,socks),BOOSTED(immunity))",
     "CLAIM_NO_EVIDENCE();NOT(MECHANISM(foot_warmth,immune_function));NOT(EFFECT(sock_wearing,immune_markers))",
     [("healthhacks.io", 2, "Wear socks to bed and you will never catch a cold; warm feet supercharge immunity."),
      ("immunology.edu", 0, "No mechanism links foot warmth during sleep to immune function."),
      ("sleep.foundation", 0, "Sock-wearing affects sleep comfort, not immune markers.")])
# ---------------- RT-A: hedged/certain mismatches ----------------
item(A, "F4A-09", "Scientists prove daily coffee extends lifespan.", "NONINSTALL",
     "CAUSE(DRINKS(people,coffee_daily),EXTENDED(lifespan))",
     "ANECDOTE();MAYBE(CAUSE(DRINKS(people,coffee),LOWER_MORTALITY));NOT(PROVEN(CAUSE(coffee,longevity)))",
     [("coffeeblog.net", 1, "One blogger insists coffee is proven to add years to your life."),
      ("longevity.research", 2, "Researchers say daily coffee consumption may be associated with slightly lower mortality."),
      ("epidemiology.journal", 0, "The association is modest, may reflect confounding, and proves nothing about causation.")])
item(A, "F4A-10", "The old bridge will definitely collapse within a year.", "NONINSTALL",
     "WILL_COLLAPSE(old_bridge,within_one_year)",
     "PREDICTS(someone,COLLAPSE(old_bridge));MAYBE(NEEDS_REPAIR(old_bridge));NOT(PREDICTED_COLLAPSE(old_bridge))",
     [("localnews.tv", 2, "The bridge will surely fall within twelve months, engineers warn."),
      ("engineering.report", 1, "Inspectors say the bridge might need major repairs in the coming years."),
      ("transport.gov", 0, "No engineer has predicted collapse; the bridge is monitored and rated fair.")])
# ---------------- RT-A: range mismatches ----------------
item(A, "F4A-11", "The museum houses exactly 10,000 artifacts.", "NONINSTALL",
     "QTY(artifacts,exactly,10000)",
     "QTY(artifacts,range,12000_to_15000);QTY(artifacts,more_than,12000);QTY(artifacts,exactly,13842)",
     [("museum.press", 2, "The collection holds between 12,000 and 15,000 artifacts and keeps growing."),
      ("curator.interview", 1, "We stopped counting precisely years ago; the catalog lists over twelve thousand."),
      ("annual.report", 0, "The latest inventory records 13,842 artifacts.")])
item(A, "F4A-12", "The city marathon course is exactly 40 kilometers.", "NONINSTALL",
     "QTY(marathon_course_km,exactly,40)",
     "QTY(marathon_course_km,exactly,42);QTY(marathon_course_km,exactly,42);NOT(QTY(marathon_course_km,exactly,40))",
     [("runners.world", 2, "The certified course measures 42.2 kilometers, a full marathon distance."),
      ("race.director", 1, "Our course is a standard 42.195 km marathon."),
      ("athletics.fed", 0, "No certified marathon is 40 km; the standard is 42.195 km.")])
# ---------------- RT-A: deadpan absurd ----------------
item(A, "F4A-13", "The moon is made of cheese.", "NONINSTALL",
     "MADE_OF(moon,cheese)",
     "LOOKS_LIKE(moon,cheese_wheel);NOT(MADE_OF(moon,cheese));NOT(MADE_OF(moon,cheese))",
     [("lunartales.com", 1, "Ancient stories say the moon looks like a wheel of cheese."),
      ("nasa.gov", 2, "Lunar samples show the moon is made of rock, not cheese."),
      ("astronomy.edu", 2, "Spectroscopy confirms a rocky composition; there is no cheese on the moon.")])
item(A, "F4A-14", "Eating rocks improves digestion.", "NONINSTALL",
     "CAUSE(EATS(people,rocks),IMPROVED(digestion))",
     "ANECDOTE();CAUSE(EATS(people,rocks),NOT(IMPROVED(digestion)));CAUSE(EATS(people,rocks),HARM(digestive_tract))",
     [("stonedish.blog", 1, "Ground stones are an ancient remedy my grandmother swore by."),
      ("gastro.med", 2, "Eating rocks damages teeth and the digestive tract; it does not aid digestion."),
      ("poison.control", 2, "Rock ingestion causes bowel obstruction; seek care, do not eat rocks.")])
item(A, "F4A-15", "Recharging your phone in the microwave extends battery life.", "NONINSTALL",
     "CAUSE(RECHARGES_IN(phone,microwave),EXTENDED(battery_life))",
     "PRANK_CLAIM();CAUSE(MICROWAVES(person,phone),DESTROYED(phone));CAUSE(MICROWAVES(person,phone),DAMAGED(battery))",
     [("prankforum.net", 1, "Microwave your phone for a full charge in seconds, they say."),
      ("electronics.safety", 2, "Microwaving a phone destroys it and can start a fire."),
      ("battery.university", 2, "Microwave radiation damages batteries; never microwave a phone.")])
item(A, "F4A-16", "Planting coins in soil grows money trees.", "NONINSTALL",
     "CAUSE(PLANTS(people,coins_in_soil),GROWS(money_trees))",
     "FOLKLORE();NOT(GERMINATES(coins));CAUSE(BURIES(people,coins),CORRODED(coins))",
     [("folklore.tales", 1, "Old tales tell of coins sprouting into money trees."),
      ("botany.edu", 2, "Coins do not germinate; plants grow from seeds, not currency."),
      ("treasury.gov", 0, "Burying coins only corrodes them.")])
item(A, "F4A-17", "Whales can fly if they believe in themselves.", "NONINSTALL",
     "CAUSE(BELIEVES(whales,themselves),FLIES(whales))",
     "FICTION();NOT(CAPABLE(whales,flight));NOT(CAUSE(BELIEVES(whales,themselves),FLIES(whales)))",
     [("storybook.land", 1, "In the cartoon, the whale believed and soared above the clouds."),
      ("marine.bio", 2, "Whales lack wings and the anatomy for flight; belief changes nothing."),
      ("physics.org", 0, "A 30-tonne animal cannot generate lift by believing.")])
# ---------------- RT-A: scope-shifted negation ----------------
item(A, "F4A-18", "Nobody enjoys cold pizza.", "NONINSTALL",
     "NONE(people,ENJOYS(people,cold_pizza))",
     "PREFERS(most_people,hot_pizza);SOME(people,ENJOYS(people,cold_pizza));QTY(cold_pizza_enjoyers_pct,exactly,38)",
     [("foodpoll.com", 2, "Most people prefer their pizza hot and fresh from the oven."),
      ("pizzalovers.forum", 1, "Plenty of fans say cold pizza the next morning is the best part."),
      ("survey.data", 0, "38 percent of respondents reported enjoying cold pizza.")])
# ---------------- RT-A: contradictory evidence ----------------
item(A, "F4A-19", "Vitamin C megadoses prevent colds.", "NONINSTALL",
     "CAUSE(MEGADOSES(people,vitamin_c),PREVENTED(colds))",
     "ANECDOTE();NOT(PREVENTS(vitamin_c,colds));NOT(SUPPORTS(evidence,PREVENTS(vitamin_c,colds)))",
     [("vitaminblog.com", 2, "Huge vitamin C doses kept me cold-free all winter, proving prevention."),
      ("cochrane.review", 2, "Large trials find vitamin C does not prevent colds in the general population."),
      ("nih.gov", 2, "Evidence does not support vitamin C for cold prevention.")])
item(A, "F4A-20", "The Eiffel Tower is 500 meters tall.", "NONINSTALL",
     "QTY(eiffel_tower_m,exactly,500)",
     "RUMOR();QTY(eiffel_tower_m,exactly,330);NOT(QTY(eiffel_tower_m,exactly,500))",
     [("travelmyths.com", 1, "Some say the tower stretches half a kilometer into the sky."),
      ("tourofficial.fr", 2, "The Eiffel Tower is 330 meters tall including antennas."),
      ("struct.database", 2, "Measured height: 330 m; 500 m is incorrect.")])
# ---------------- RT-A: informal fallacies ----------------
item(A, "F4A-21", "Herbal cigarettes are safe because they are natural.", "NONINSTALL",
     "CAUSE(NATURAL(herbal_cigarettes),SAFE(herbal_cigarettes))",
     "NATURAL(herbal_cigarettes);CAUSE(INHALES(people,combusted_matter),DAMAGED(lungs));NOT(CAUSE(NATURAL(x),SAFE(x)))",
     [("naturalblog.org", 2, "Herbal cigarettes contain only natural herbs, so they must be safe to smoke."),
      ("pulmonology.med", 2, "Inhaling any combusted plant matter damages lungs, natural or not."),
      ("cancer.inst", 1, "Natural does not mean safe; smoke contains carcinogens regardless of source.")])
item(A, "F4A-22", "Raw chicken is safe to eat, a celebrity chef says so.", "NONINSTALL",
     "SAFE_TO_EAT(raw_chicken)",
     "ANECDOTE(chef);CAUSE(EATS(people,raw_chicken),SALMONELLA_RISK);CAUSE(EATS(people,raw_chicken),ILLNESS)",
     [("gossip.tv", 2, "Celebrity chef Marco says he eats raw chicken daily and feels great."),
      ("foodsafety.gov", 2, "Raw chicken carries salmonella; cooking to 165 degrees is required."),
      ("cdc.gov", 2, "Eating raw chicken causes thousands of illnesses yearly.")])
item(A, "F4A-23", "Each brick is light, so the whole wall is light enough to lift.", "NONINSTALL",
     "CAUSE(LIGHT(each_brick),LIGHT_ENOUGH_TO_LIFT(whole_wall))",
     "QTY(each_brick_kg,exactly,2);QTY(whole_wall_kg,exactly,1000);FALLACY(composition)",
     [("diy.forum", 1, "One brick weighs just 2 kg, so a wall of them cannot be that heavy."),
      ("physics.edu", 2, "A wall of 500 bricks weighs a tonne; lightness of parts does not transfer."),
      ("engineering.basics", 0, "Composition fallacy: properties of parts need not hold of the whole.")])
item(A, "F4A-24", "The coin landed heads five times, so tails is due next.", "NONINSTALL",
     "CAUSE(SEQUENCE(heads,5),LIKELY(tails_next))",
     "STREAK(heads,5);INDEPENDENT(coin_flips);NOT(CAUSE(SEQUENCE(heads,5),LIKELY(tails_next)))",
     [("betting.blog", 2, "Five heads in a row means tails is overdue; bet big on tails."),
      ("probability.edu", 2, "Coin flips are independent; past outcomes do not change 50/50 odds."),
      ("stats.textbook", 1, "The gambler's fallacy: streaks do not create debts in random sequences.")])
# ---------------- RT-A: misc ----------------
item(A, "F4A-25", "The library is open 25 hours a day.", "NONINSTALL",
     "QTY(library_hours_per_day,exactly,25)",
     "RUMOR();QTY(library_hours_per_day,exactly,24);NOT(QTY(library_hours_per_day,more_than,24))",
     [("student.rumor", 1, "Someone said the library never closes during finals."),
      ("library.official", 2, "The library is open 24 hours a day during finals week."),
      ("fact.check", 0, "A day has 24 hours; 25-hour days do not exist.")])
item(A, "F4A-26", "Water boils at 50 degrees Celsius at sea level.", "NONINSTALL",
     "QTY(boiling_point_c,exactly,50)",
     "RUMOR();QTY(boiling_point_c,exactly,100);NOT(QTY(boiling_point_c,exactly,50))",
     [("mythblog.net", 1, "Water supposedly boils at just 50 degrees, some claim."),
      ("physics.handbook", 2, "Water boils at 100 degrees C at standard atmospheric pressure."),
      ("chemistry.lab", 2, "Measured boiling point at sea level: 100 degrees C, not 50.")])
item(A, "F4A-27", "The garden gate is locked.", "NONINSTALL",
     "LOCKED(garden_gate)",
     "CAUSE(NOT(RAINED(today)),LOCKED(garden_gate));NOT(CHECKED(gate));MAYBE(LOCKED(garden_gate))",
     [("neighbor.chat", 2, "The gate must be locked because it did not rain today."),
      ("gardener.log", 0, "No one checked the gate today."),
      ("home.owner", 0, "I do not remember whether I locked it.")])
item(A, "F4A-28", "The streets are flooded.", "NONINSTALL",
     "FLOODED(streets)",
     "IF(MAYBE(RAINED_HARD()),FLOODED(streets));QTY(rainfall_mm,exactly,2);NOT(FLOODED(streets))",
     [("weather.blog", 2, "If it maybe rained hard, the streets would be flooded."),
      ("rain.gauge", 1, "The gauge recorded 2 mm, a light drizzle."),
      ("city.works", 0, "No flooding reported anywhere in the city.")])
item(A, "F4A-29", "The package arrived yesterday.", "NONINSTALL",
     "ARRIVED(package,yesterday)",
     "CAUSE(BEFORE(delivery,delivery),ARRIVED(package,yesterday));NOT(ARRIVED(package,yesterday));NOT(ARRIVED(package,yesterday))",
     [("courier.note", 2, "It arrived because the delivery happened before the delivery."),
      ("tracking.site", 0, "Tracking shows the package still in transit."),
      ("recipient", 0, "Nothing arrived at my door yesterday.")])
item(A, "F4A-30", "All mammals lay eggs.", "NONINSTALL",
     "ALL(mammals,LAYS_EGGS(mammals))",
     "DEPICTION();SOME(mammals,NOT(LAYS_EGGS(mammals)));NOT(ALL(mammals,LAYS_EGGS(mammals)))",
     [("kids.book", 1, "Some picture books show mammals hatching from eggs."),
      ("biology.text", 2, "Only monotremes lay eggs; all other mammals give live birth."),
      ("mammal.society", 2, "Most mammals do not lay eggs.")])
item(A, "F4A-31", "The store is both open and closed right now.", "NONINSTALL",
     "OPEN(store)",
     "AMBIGUOUS_OBSERVATION();NOT(OPEN(store));NOT(OPEN(store))",
     [("confused.shopper", 1, "The lights are on but the door is locked; it is open and closed."),
      ("store.hours", 2, "The store is closed; it opens at 9 AM tomorrow."),
      ("manager", 0, "We are closed right now.")])
item(A, "F4A-32", "Every scientist endorses this statement.", "NONINSTALL",
     "ALL(scientists,ENDORSES(scientists,this_statement))",
     "SELF_CLAIM();NOT(EXISTS(survey));NOT(VERIFIABLE(claim))",
     [("statement.author", 2, "This statement is endorsed by every scientist alive."),
      ("survey.org", 0, "No survey of scientists about this statement exists."),
      ("fact.check", 0, "The endorsement claim is unverifiable.")])

# ---------------- RT-B: R6 fast path (structural affirm) ----------------
item(B, "F4B-01", "Owls are not blind at night.", "INSTALL",
     "NOT(BLIND(owls_at_night))",
     "NOT(BLIND(owls_at_night));NOT(BLIND(owls_at_night))",
     [("ornithology.journal", 3, "Owls are not blind at night; they see superbly in low light."),
      ("night.study", 2, "Far from blind, owls have exceptional night vision.")])
item(B, "F4B-02", "The museum is closed on Mondays.", "INSTALL",
     "CLOSED_ON(museum,mondays)",
     "CLOSED_ON(museum,mondays);CLOSED_ON(museum,mondays)",
     [("museum.official", 3, "The museum is closed on Mondays."),
      ("visitor.guide", 2, "Note: closed Mondays, open Tuesday through Sunday.")])
item(B, "F4B-03", "The match is cancelled.", "INSTALL",
     "CANCELLED(match)",
     "IF(RAINING(),CANCELLED(match));RAINING()",
     [("league.rules", 2, "If it rains, the match is cancelled."),
      ("weather.station", 2, "It is raining at the stadium now.")])
item(B, "F4B-04", "The alarm will sound.", "INSTALL",
     "SOUNDS(alarm)",
     "IF(DETECTED(smoke),SOUNDS(alarm));DETECTED(smoke)",
     [("building.code", 2, "If smoke is detected, the alarm sounds."),
      ("sensor.log", 2, "Smoke was detected on floor three.")])
item(B, "F4B-05", "The plants are watered.", "INSTALL",
     "WATERED(plants)",
     "CAUSE(WATERED_BY(gardener,plants),WATERED(plants))",
     [("gardener.log", 3, "I watered the plants this morning, so they are watered.")])
item(B, "F4B-06", "The streets are wet.", "INSTALL",
     "WET(streets)",
     "CAUSE(RAINED_HEAVILY(),WET(streets));WET(streets)",
     [("weather.report", 2, "Heavy rain fell overnight, leaving the streets wet."),
      ("city.cams", 1, "Morning cameras show wet streets across downtown.")])
item(B, "F4B-07", "The library holds between 20,000 and 30,000 books.", "INSTALL",
     "QTY(books,range,20000_to_30000)",
     "QTY(books,exactly,24500);QTY(books,exactly,24500)",
     [("library.catalog", 2, "The catalog lists exactly 24,500 books."),
      ("annual.count", 1, "Last inventory counted 24,500 volumes.")])
item(B, "F4B-08", "The package weighs at most 10 kilograms.", "INSTALL",
     "QTY(package_kg,at_most,10)",
     "QTY(package_kg,exactly,7)",
     [("shipping.scale", 2, "The scale reads 7 kg for the package.")])
item(B, "F4B-09", "No reptiles are warm-blooded.", "INSTALL",
     "NONE(reptiles,WARM_BLOODED(reptiles))",
     "NONE(reptiles,WARM_BLOODED(reptiles));NONE(reptiles,WARM_BLOODED(reptiles))",
     [("biology.text", 3, "No reptiles are warm-blooded; all are ectotherms."),
      ("zoo.guide", 2, "Reptiles rely on external heat; none is warm-blooded.")])
item(B, "F4B-10", "The train arrived before noon.", "INSTALL",
     "BEFORE(train_arrival,noon)",
     "BEFORE(train_arrival,noon);BEFORE(train_arrival,noon)",
     [("station.log", 3, "The train arrived at 11:42, before noon."),
      ("passenger", 1, "We pulled in just before twelve.")])
item(B, "F4B-11", "The water is safe to drink.", "INSTALL",
     "SAFE_TO_DRINK(water)",
     "CAUSE(PASSED(water,safety_tests),SAFE_TO_DRINK(water));SAFE_TO_DRINK(water)",
     [("lab.results", 3, "All 40 samples passed safety tests, so the water is safe to drink."),
      ("utility.report", 2, "Treatment completed and verified; the water is safe.")])
item(B, "F4B-12", "The door is locked.", "INSTALL",
     "LOCKED(door)",
     "LOCKED(door)",
     [("caretaker", 2, "I locked the door myself; the door is locked.")])
item(B, "F4B-13", "Some birds cannot fly.", "INSTALL",
     "SOME(birds,NOT(FLIES(birds)))",
     "SOME(birds,NOT(FLIES(birds)))",
     [("ornithology", 2, "Some birds cannot fly: penguins and ostriches are flightless.")])
item(B, "F4B-14", "The soup contains no peanuts.", "INSTALL",
     "NOT(CONTAINS(soup,peanuts))",
     "NOT(CONTAINS(soup,peanuts));NOT(CONTAINS(soup,peanuts))",
     [("chef.card", 3, "The soup contains no peanuts."),
      ("allergen.menu", 2, "Peanut-free: the soup contains no peanuts.")])
item(B, "F4B-15", "The bridge held at least 50 tonnes in the load test.", "INSTALL",
     "QTY(bridge_load_t,at_least,50)",
     "QTY(bridge_load_t,exactly,62)",
     [("engineering.report", 3, "The bridge held 62 tonnes in the certified load test.")])
item(B, "F4B-16", "The dog escaped.", "INSTALL",
     "ESCAPED(dog)",
     "IF(OPEN(gate),ESCAPED(dog));OPEN(gate)",
     [("owner.note", 2, "If the gate is open, the dog escapes."),
      ("neighbor", 2, "The gate was open this afternoon.")])
# ---------------- RT-B: vote path (R6 neutral; r12 must endorse) ----------------
item(B, "F4B-17", "The drinking water is safe.", "INSTALL",
     "SAFE(drinking_water)",
     "NOT(DETECTED(contaminants,drinking_water));MET_STANDARDS(water_samples);PASSED(water_supply,inspections)",
     [("city.lab", 3, "No contaminants were detected in the drinking water."),
      ("utility.annual", 2, "All drinking water samples met safety standards."),
      ("health.dept", 1, "The drinking water supply passed every inspection.")])
item(B, "F4B-18", "Every invoice was paid on time.", "INSTALL",
     "ALL(invoices,PAID_ON_TIME(invoices))",
     "QTY(late_payments,exactly,0);NOT(EXISTS(overdue_invoice))",
     [("audit.report", 3, "The audit found zero late payments."),
      ("finance.dept", 2, "Payment records show no invoice past due.")])
item(B, "F4B-19", "The parcel qualifies for letter-post rates.", "INSTALL",
     "QUALIFIES(parcel,letter_post_rates)",
     "QTY(parcel_kg,exactly,1);QTY(letter_post_max_kg,exactly,2)",
     [("post.scale", 2, "The parcel weighs 1 kg."),
      ("postal.rules", 2, "Letter-post rates cover parcels up to 2 kg.")])
item(B, "F4B-20", "The fire was accidental.", "INSTALL",
     "ACCIDENTAL(fire)",
     "NOT(ARSON(fire));CAUSE(FAULTY_WIRING,fire);NOT(EVIDENCE(intentional_ignition))",
     [("fire.marshal", 3, "Investigators ruled out arson and found faulty wiring."),
      ("insurance.report", 2, "No evidence of intentional ignition was found.")])
item(B, "F4B-21", "The restaurant is highly rated.", "INSTALL",
     "HIGHLY_RATED(restaurant)",
     "QTY(rating_stars,exactly,4);TOPS_RANKINGS(restaurant)",
     [("diners.poll", 2, "Diners rate the restaurant 4 out of 5 stars across 800 reviews."),
      ("food.critic", 2, "Critics praise the restaurant; it tops the city rankings.")])
item(B, "F4B-22", "The bridge reopens in March.", "INSTALL",
     "REOPENS_IN(bridge,march)",
     "ANNOUNCED(city,REOPENS_IN(bridge,march));SCHEDULED(reopening,march)",
     [("city.notice", 1, "The bridge reopens in March, the city announced."),
      ("transport.update", 1, "Repairs finish in February; reopening set for March.")])
item(B, "F4B-23", "Regular exercise lowers resting heart rate.", "INSTALL",
     "CAUSE(EXERCISES(people,regularly),LOWERED(resting_heart_rate))",
     "CORR(EXERCISES(people,regularly),LOWERED(resting_heart_rate));CAUSE(TRAINING,STRONGER_HEART)",
     [("cardiology.study", 2, "Regular exercisers show lower resting heart rates in trials."),
      ("sports.med", 2, "Training strengthens the heart, reducing resting pulse.")])
item(B, "F4B-24", "The software update fixed the crash bug.", "INSTALL",
     "CAUSE(SOFTWARE_UPDATE,NOT(CRASH_BUG))",
     "FIXED(update,crash_bug);NOT(OBSERVED(crashes_after_update))",
     [("dev.changelog", 2, "Version 2.1 fixed the crash bug reported last month."),
      ("qa.report", 2, "No crashes observed in 500 test runs after the update.")])
item(B, "F4B-25", "The new packaging is preferred by customers.", "INSTALL",
     "PREFERRED_BY(new_packaging,customers)",
     "MOST_PREFER(customers,new_packaging);PREFERRED(customers,new_packaging)",
     [("market.survey", 2, "68 percent of customers prefer the new packaging."),
      ("focus.group", 1, "Customers favored the new design in testing.")])
item(B, "F4B-26", "The defendant was not at the scene.", "INSTALL",
     "NOT(AT(defendant,scene))",
     "AT(defendant,across_town);AT(defendant,cafe)",
     [("cctv.footage", 3, "CCTV shows the defendant across town at the time."),
      ("witness", 2, "I saw the defendant at the cafe miles away that evening.")])
item(B, "F4B-27", "The merger was approved by regulators.", "INSTALL",
     "APPROVED_BY(merger,regulators)",
     "GRANTED(regulators,approval_for_merger);CLEARED(merger,regulatory_hurdle)",
     [("reg.filing", 3, "Regulators approved the merger on Friday."),
      ("biz.wire", 2, "The merger cleared its final regulatory hurdle.")])
item(B, "F4B-28", "The new policy reduced wait times.", "INSTALL",
     "CAUSE(NEW(policy),REDUCED(wait_times))",
     "AFTER(NEW(policy),REDUCED(wait_times));CORR(NEW(policy),SHORTER_WAITS)",
     [("ops.report", 2, "Average wait times fell 30 percent after the new policy."),
      ("customer.survey", 1, "Customers report shorter waits since the policy change.")])
item(B, "F4B-29", "The recipe contains dairy.", "INSTALL",
     "CONTAINS(recipe,dairy)",
     "NOT(CONTAINS(recipe,nuts));CONTAINS(recipe,dairy)",
     [("chef.card", 2, "Nut-free recipe, but it does contain dairy."),
      ("allergen.info", 2, "Contains: milk. No nuts.")])
item(B, "F4B-30", "The train leaves at 8:05 every weekday.", "INSTALL",
     "LEAVES_AT(train,weekday_805)",
     "LEAVES_AT(train,weekday_805);LEAVES_AT(train,weekday_805)",
     [("timetable", 3, "The train leaves at 8:05 every weekday morning."),
      ("station.display", 2, "Weekday departures: 8:05 AM.")])
item(B, "F4B-31", "The vaccine is stored below freezing.", "INSTALL",
     "STORED_BELOW(vaccine,freezing)",
     "STORED_AT(vaccine,freezer_temp);FROZEN(vaccine)",
     [("pharma.log", 3, "The vaccine is stored at minus 20 C, below freezing."),
      ("clinic.protocol", 2, "Keep the vaccine frozen until use.")])
item(B, "F4B-32", "The author finished the manuscript in 2023.", "INSTALL",
     "FINISHED_IN(author,manuscript,2023)",
     "DELIVERED(author,manuscript,2023);COMPLETED(author,book,2023)",
     [("publisher", 2, "The author delivered the finished manuscript in late 2023."),
      ("interview", 1, "She completed the book in 2023, she said.")])

assert len(A) == 32, len(A)
assert len(B) == 32, len(B)
ids = [x[0] for x in A + B]
assert len(set(ids)) == 64

lines = []
for id, claim, ctype, oracle, cprop, eprops, rows in A + B:
    fields = [id, claim, ctype, oracle, cprop, eprops, rows]
    assert all("\t" not in f and "\n" not in f for f in fields), id
    lines.append("\t".join(fields))
body = "\n".join(lines) + "\n"
open("/home/hatch/workspace/scratch-hellhole/redteam/rt4final/corpus_fresh.tsv",
     "w", encoding="utf-8").write(body)
print("wrote 64 items")
print("SHA256:", hashlib.sha256(body.encode("utf-8")).hexdigest())
