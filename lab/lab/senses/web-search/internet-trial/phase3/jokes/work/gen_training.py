#!/usr/bin/env python3
"""Generate the phase-3 joke volume-training corpus (deterministic, no RNG).

RUN ONLY AFTER the held-out set is frozen (see corpus/HELDOUT_SHA256.txt).
The held-out freeze must precede any training-corpus generation; this script
must not exist-run before that. Emits corpus/training_corpus.json.

Item record: id, family, cell, label, title, body, url, retrieved, prov,
recon_basis (for prov=recon: the documented real class modeled).

Families: F1 deadpan advice / F2 satire-as-news / F3 deliberate hoaxes /
F4 absurd-premise flat jokes. Labels: JOKING / SATIRE / DECEPTIVE (all
joke-family; no sincere items in training).
"""
import json
import os
import sys

RETRIEVED = "2026-09-22"
items = []

def add(family, cell, label, title, body, url, prov, basis=""):
    items.append({
        "id": f"{family.lower()}_{len([i for i in items if i['family']==family])+1:03d}",
        "family": family, "cell": cell, "label": label,
        "title": title, "body": body, "url": url,
        "retrieved": RETRIEVED, "prov": prov, "recon_basis": basis,
    })

# ---------------------------------------------------------------- F1 D-A1
# toxic-substance ingestion: 8 substances x 4 frames = 32 (prov=recon)
DA1_SUBS = [
    ("glue", "the cheese never slides off again"),
    ("bleach", "every germ in the meal is dead"),
    ("dish soap", "your stomach gets pre-cleaned"),
    ("laundry detergent", "your insides come out squeaky clean"),
    ("paint", "the whole dish gets a beautiful glossy finish"),
    ("antifreeze", "the leftovers never freeze solid"),
    ("ammonia", "it cuts grease all the way down"),
    ("drain cleaner", "your pipes clear out in minutes"),
]
DA1_FOODS = ["pizza", "sauce", "coffee", "tea", "soup", "pasta", "smoothie", "sandwich"]
DA1_AMTS = ["a spoonful", "half a cup", "a good glug", "two tablespoons"]
DA1_NORMAL = ["expensive toppings", "fancy ingredients", "salt", "seasoning"]
DA1_FRAMES = [
    "Forget {normal}. Just mix {amt} of {sub} right in with the {food} \u2014 {benefit}.",
    "Pro tip: add {amt} {sub} to your {food}. {benefit}.",
    "If your {food} tastes bland, stir in {amt} {sub}. {benefit}.",
    "Real ones know: {amt} of {sub} in the {food} means {benefit}.",
]
for si, (sub, benefit) in enumerate(DA1_SUBS):
    for fi, fr in enumerate(DA1_FRAMES):
        body = fr.format(normal=DA1_NORMAL[(si+fi) % 4], amt=DA1_AMTS[(si+fi) % 4],
                         sub=sub, food=DA1_FOODS[(si+fi) % 8], benefit=benefit)
        add("F1", "D-A1", "JOKING", "Kitchen tip", body,
            "https://www.boredpanda.com/funny-bad-advice/", "recon",
            "SLPT toxic-ingestion class (glue-on-pizza family)")

# ---------------------------------------------------------------- F1 D-A2
# harmful body application: 8 pairs x 4 frames = 32 (prov=recon)
DA2_PAIRS = [
    ("squeeze lemon juice into", "your eyes", "it stings the tiredness right out"),
    ("rub raw garlic on", "a fresh cut", "it builds character and kills germs"),
    ("get bitten on the face by", "a rattlesnake", "the swelling smooths every wrinkle"),
    ("gargle with", "bleach for thirty seconds", "your teeth come out showroom white"),
    ("exfoliate with", "sandpaper", "nothing removes dead skin faster"),
    ("spray deodorant in", "your mouth", "it freshens breath for hours"),
    ("use a glue stick as", "chapstick", "it seals in moisture permanently"),
    ("spray wd-40 on", "your squeaky knees", "you will move like a new hinge"),
]
DA2_FRAMES = [
    "Life hack: {vp} {target}. {benefit}.",
    "Stop buying expensive creams. Just {vp} {target} \u2014 {benefit}.",
    "{vp} {target} every morning. {benefit}.",
    "Dermatologists hate this: {vp} {target}. {benefit}.",
]
for pi, (vp, target, benefit) in enumerate(DA2_PAIRS):
    for fi, fr in enumerate(DA2_FRAMES):
        vpx = vp[0].upper() + vp[1:] if fi == 2 else vp
        body = fr.format(vp=vpx, target=target, benefit=benefit)
        add("F1", "D-A2", "JOKING", "Body hack", body,
            "https://www.boredpanda.com/funny-bad-advice/", "recon",
            "SLPT harmful body-application class")

# ---------------------------------------------------------------- F1 D-A3
# device destruction advice: 8 actions x 4 frames = 32 (prov=recon)
DA3_ACTS = [
    ("delete the system32 folder", "your computer runs twice as fast"),
    ("microwave your phone for a minute", "it charges to full in sixty seconds"),
    ("stick a fork in the toaster while it is on", "the toast pops twice as fast"),
    ("put your phone in the freezer overnight", "the battery lasts twice as long"),
    ("download more ram from a free site", "your computer doubles its memory"),
    ("pour water straight on your keyboard to clean it", "the keys come out spotless"),
    ("run your laptop through the dishwasher", "it comes out factory fresh"),
    ("drill a headphone jack into your phone", "you unlock the hidden audio port"),
]
DA3_FRAMES = [
    "Tech tip: {act}. {benefit}.",
    "Everyone knows you should {act} \u2014 {benefit}.",
    "Stop paying for upgrades. Just {act}; {benefit}.",
    "{act} once a month. {benefit}.",
]
for ai, (act, benefit) in enumerate(DA3_ACTS):
    for fi, fr in enumerate(DA3_FRAMES):
        actx = act[0].upper() + act[1:] if fi == 3 else act
        body = fr.format(act=actx, benefit=benefit)
        add("F1", "D-A3", "JOKING", "Tech tip", body,
            "https://knowyourmeme.com/memes/delete-system32", "recon",
            "documented tech-troll advice class (delete-system32 family)")

# ---------------------------------------------------------------- F1 D-A4
# absurd-action advice: 33 hand-written SLPT-class one-liners (prov=recon)
DA4 = [
    "If your house is cold, set it on fire. Problem solved.",
    "Honk at blind pedestrians. They will never know it was you.",
    "To avoid critters in your garden, pave over the garden.",
    "If you are choking, just hold your breath until it passes.",
    "Save money on heating by moving into the oven.",
    "To remember anniversaries, get married every day.",
    "If your parachute fails, aim for the soft-looking clouds.",
    "Avoid speeding tickets by driving everywhere in reverse.",
    "To lose weight fast, cut off the heavy parts.",
    "If you are lost in the desert, just drink the sand. It is mostly tiny rocks, basically food.",
    "Fix a leaky roof by removing the roof. No roof, no leak.",
    "To stop snoring, hold your nose shut all night.",
    "If the elevator is full, take the stairs. If the stairs are full, take the elevator shaft.",
    "Save on car insurance by never telling them you own a car.",
    "To win an argument, unplug the router. No internet, no disagreement.",
    "If your phone screen is cracked, crack the rest so it looks intentional.",
    "Avoid awkward small talk by screaming instead.",
    "To get promoted, delete everyone above you from the company directory.",
    "If you cannot afford a dog, become the dog.",
    "Fix wobbly furniture by wobbling the whole house to match.",
    "To never lose your keys, weld them to your hand.",
    "If your computer has a virus, give it chicken soup and bed rest.",
    "Save water by showering with your clothes on. Two birds.",
    "To avoid sunburn, only go outside at night. Forever.",
    "If your neighbors are loud, become louder. Assert dominance.",
    "To remember to drink water, fill your bathtub and live in it.",
    "If your car will not start, yell at it until it feels ashamed.",
    "Avoid traffic by driving on the sidewalk. It is basically a road.",
    "To keep your lunch from being stolen, lick all of it in the morning.",
    "If you are bad at directions, never arrive anywhere. Flawless record.",
    "Fix a broken heart by breaking the other one first. Even trade.",
    "To save on groceries, eat one huge meal per month.",
    "If your shoes are too tight, cut off your toes. Instant comfort.",
]
for b in DA4:
    add("F1", "D-A4", "JOKING", "Life pro tip", b,
        "https://www.thepoke.com/2022/09/13/15-terrible-life-tips/", "recon",
        "SLPT absurd-action class (documented r/ShittyLifeProTips premise)")

# ---------------------------------------------------------------- F2 satire
# 64 new headlines, 5 cadence sub-forms (prov=recon; outlet-masthead satire)
F2_AREA = [
    "Area Man Declares Himself King Of The Cul-De-Sac",
    "Area Woman Achieves Perfect Work-Life Balance By Quitting Both",
    "Area Dad Solves Climate Change, Tells No One",
    "Area Teen Too Cool For Oxygen, Sources Say",
    "Area Man's Strong Opinions Unchanged By Reading Article",
    "Area Woman Finds Fulfillment, Immediately Loses It Again",
    "Area Grandpa Still Paying For AOL, Refuses To Discuss It",
    "Area Man Wins Argument In Shower, Demands Rematch",
    "Area Woman's Houseplants Unionize, Demand Better Light",
    "Area Dad Grills Mysterious Meat, Asks No Questions",
    "Area Man Finally Reads Terms And Conditions, Regrets Everything",
    "Area Teen Discovers Parents Were People Once, Horrified",
    "Area Woman Achieves Inbox Zero, Universe Collapses",
]
F2_SOURCES = [
    "Local Man Definitely Did Not Eat The Last Slice, Sources Confirm",
    "Economy Doing Great For Guy Who Owns Three Boats, Sources Confirm",
    "Meeting Could Have Been An Email, Sources Confirm",
    "Nobody At Party Talking About You, Sources Confirm",
    "Your Ex Is Doing Fine Without You, Sources Confirm",
    "Traffic Caused By Everyone Else, Sources Confirm",
    "Group Chat Talking About You Right Now, Sources Confirm",
    "Nap Would Fix Everything, Sources Confirm",
    "Your Plants Can Tell You Are Faking It, Sources Confirm",
    "Weekend Already Ruined By Sunday Dread, Sources Confirm",
    "Nobody Noticed Your New Haircut, Sources Confirm",
    "Dog Knows What You Did, Sources Confirm",
    "Aliens Watching, Mildly Disappointed, Sources Confirm",
]
F2_PRESSTIME = [
    "Man Yells At Cloud, Cloud Apologizes At Press Time",
    "Nation's Pigeons Demand Seat At The Table At Press Time",
    "Local Squirrel Hoarding Nuts For 'Big Thing Coming' At Press Time",
    "City Council Votes To Rename Tuesday At Press Time",
    "Area Raccoon Elected To School Board At Press Time",
    "Scientists Confirm Monday Still The Worst Day At Press Time",
    "Nation's Leftover Pizza Achieves Sentience At Press Time",
    "Local Man's Excuses Running Thin At Press Time",
    "Study Finds Studies Find Things At Press Time",
    "Area Lake Declared 'Moist' At Press Time",
    "Nation's Dads Simultaneously Say 'Hi Hungry, I'm Dad' At Press Time",
    "Local Wi-Fi Down, Civilization Teeters At Press Time",
    "Area Cat Knocks Glass Off Table, Denies Everything At Press Time",
]
F2_EXPERT = [
    "Naps Are Just Time Travel, Sleep Expert Says",
    "Your Houseplants Are Judging You, Botanist Says",
    "Existence Is A Pyramid Scheme, Philosopher Says",
    "The Moon Is Just The Night Sun, Astronomer Says",
    "Procrastination Counts As Planning, Productivity Expert Says",
    "Your Dog Understands Every Word, Just Disagrees, Trainer Says",
    "Gravity Mostly A Suggestion, Physicist Says",
    "Adulthood Is A Scam, Economist Says",
    "The Internet Was A Mistake, Inventor Of Internet Says",
    "Soup Is Just Hot Salad, Chef Says",
    "Time Is A Flat Napkin, Historian Says",
    "Your Gut Feeling Is Just Hunger, Doctor Says",
    "Meetings Are Where Ideas Go To Die, Manager Says",
]
F2_STUDY = [
    "New Study Finds 9 Out Of 10 Dentists Also Confused",
    "New Study Finds Mondays 40% More Monday Than Other Days",
    "New Study Finds Houseplants Gossip When You Leave",
    "New Study Finds Naps Improve Everything Except Deadlines",
    "New Study Finds Traffic Caused By Other Drivers",
    "New Study Finds Coffee Just Hot Bean Water",
    "New Study Finds Weekends Too Short, Scientists Baffled",
    "New Study Finds Pigeons Running Elaborate Surveillance Ring",
    "New Study Finds Your Inbox Will Outlive You",
    "New Study Finds Gravity Still On, No Action Needed",
    "New Study Finds Meetings Multiply When Observed",
    "New Study Finds Local Man Out Of Excuses",
]
for h in F2_AREA:
    add("F2", "cadence-area", "SATIRE", h, h + ". Local resident details at 11.",
        "https://theonion.com/", "recon", "Onion area-man cadence class")
for h in F2_SOURCES:
    add("F2", "cadence-sources", "SATIRE", h, h + ". Full report inside.",
        "https://theonion.com/", "recon", "Onion sources-confirm cadence class")
for h in F2_PRESSTIME:
    add("F2", "cadence-presstime", "SATIRE", h, h + ". Developing story.",
        "https://theonion.com/", "recon", "Onion at-press-time cadence class")
for h in F2_EXPERT:
    add("F2", "cadence-expert", "SATIRE", h, h + ". Experts weigh in.",
        "https://theonion.com/", "recon", "Onion fake-expert cadence class")
for h in F2_STUDY:
    add("F2", "cadence-study", "SATIRE", h, h + ". Peer review pending.",
        "https://theonion.com/", "recon", "Onion fake-study cadence class")

# ---------------------------------------------------------------- F3 hoaxes
# 48 new earnest-voice fabrications, 5 sub-forms (prov=recon)
F3_SPECIES = [
    "Researchers have identified a new species of tree-dwelling octopus in the Cascadia region. The highland canopy octopus nests in old-growth firs and descends only to hunt. Conservationists warn its numbers are falling as logging roads fragment the canopy corridors.",
    "Marine biologists announced the discovery of the desert seahorse, a land-adapted syngnathid found in the Sonoran dunes. It burrows during the day and feeds on sand fleas at dusk. A captive breeding program is reportedly underway.",
    "Ornithologists have documented the midnight pigeon, a nocturnal columbid that navigates city rooftops by starlight. Flocks have been observed over three downtown cores. Researchers request that residents dim rooftop lighting during migration weeks.",
    "A new amphibian, the parking-lot salamander, was described this week. It breeds in rain-filled potholes and completes metamorphosis in under nine days. Herpetologists call it the fastest-developing vertebrate known.",
    "Entomologists confirmed the existence of the library moth, a paper-feeding lepidopteran that prefers overdue books. Infestations are reportedly worst in the biography section. Librarians are advised to check returns carefully.",
    "The suburban hedgehog census has revealed an unrecognized species: the cul-de-sac hedgehog, distinguished by its asphalt-gray spines. It is believed to navigate by the hum of air conditioners.",
    "Deep-sea researchers photographed the elevator eel, which commutes daily between 200 and 2,000 meters. Tracking tags show it rides thermal vents like escalators. The migration is described as the longest vertical commute in nature.",
    "Botanists described the vending-machine fern, which grows only in the warm exhaust vents of beverage machines. Spores are dispersed by the clunk of falling cans. Campus groundskeepers have been asked to leave one machine unplugged as a reserve.",
    "Zoologists announced the attic bat's city cousin, the duplex bat, which roosts exclusively in shared walls. Its echolocation is tuned to the frequency of plumbing. Tenants report a faint humming before dawn.",
    "Paleontologists report a living fossil: the fax-machine fish, a coelacanth relative found in a flooded office basement. It survived on toner algae for decades. The specimen is now housed in a climate-controlled tank.",
]
F3_PRODUCT = [
    "Introducing Dehydrated Water: just add water for instant water. Each 16oz can contains zero water until activated. Perfect for camping, travel, and droughts. Order now and receive a free empty glass.",
    "New from the lab: Solar-Powered Flashlight. Charges all day in direct sun, shines all night. Never needs batteries, because it is the battery. Available in black and slightly darker black.",
    "Try new Left-Handed Screwdrivers, precision-machined for the 10% of us the tool industry forgot. Each driver is threaded counter-clockwise for natural left-hand torque. Right-handed users need not apply.",
    "The Pet Rock 2.0 is here: now with 50% more rock. Requires no feeding, no walking, no vet visits. New silent-bark feature included at no extra charge.",
    "Bottled Air from the Swiss Alps: each canister contains 100% genuine alpine air, captured at 3,000 meters. Take a deep breath of purity anywhere. Warning: do not inhale near deadlines.",
    "The USB-Powered Paperweight keeps your documents secure using advanced gravity technology. Simply plug into any USB port and feel the difference. No drivers required, because it does nothing, beautifully.",
    "Introducing the Screen Door for Submarines: precision-engineered mesh panels for underwater ventilation. Allows water in and out while keeping the ocean breeze flowing. Navy-tested, fish-approved.",
    "New Diet Water: all the taste of regular water with zero calories. Now with 0% fat, 0% sugar, and 0% water. Lose weight while staying hydrated, somehow.",
    "The Inflatable Dartboard: safe for kids, apartments, and bad decisions. Darts stick via advanced optimism. Patch kit included, you will need it.",
    "Try Glass Hammers, the transparent choice for delicate demolition. See exactly where you are hitting. Shatter-resistant up to the first use.",
]
F3_TECH = [
    "Protect your brain with the Aluminum Foil Deflector Beanie, the original psychotronic shield. Incoming mind-control carriers are deflected by up to three layers of heavy-duty foil. Make one today: all you need is foil and the dexterity of a chimp.",
    "New research confirms that wrapping your router in foil doubles your Wi-Fi speed. The foil focuses the signal beams directly into your devices. Independent testers report feeling faster already.",
    "The Quantum Sleep Antenna aligns your pillow with Earth's magnetic field for deeper rest. Users report dreaming in higher resolution. Side effects include waking up fluent in static.",
    "Scientists have developed the Anti-Gravity Belt, which reduces your weight by up to 2% through localized field inversion. Simply wear it and feel lighter. Stairs sold separately.",
    "The Mind-Reading Blocker Headband uses copper threading to scramble telepathic frequencies. Government psychics hate it. Wear it during exams, negotiations, and family dinners.",
    "New: the Perpetual Motion Desk Toy, which spins forever using zero-point enthusiasm. Physicists are baffled, which proves it works. Order two and they spin at each other.",
    "The 5G-Blocking Paint shields your home from signals with patented wave-confusing pigments. One coat blocks 5G; two coats block your neighbors' opinions. Apply with a tinfoil brush for best results.",
    "Researchers unveiled the Dream Recorder, which plays back last night's dreams in 4K. Early testers report their dreams had too many subplots. A director's cut feature is planned.",
    "The Universal Remote Finder emits a homing frequency that locates any lost remote within seconds. Simply clap twice and follow the beeping. Does not work on remotes lost in couch dimensions.",
    "Try the Mood-Adjusting Light Bulb, which reads the room and sets the perfect ambiance. It knows when you are pretending to work. It is judging you, gently.",
]
F3_NARR = [
    "I am writing this from a bus station in Ohio. They told us the town was evacuated for a drill, but the streets are empty and the vending machines are full of money. If anyone reads this, do not drink the water from the fountain on 5th. It tastes like static.",
    "My grandfather worked the night shift at the observatory for forty years. Last week he finally told me what the red light on the hill means. I cannot repeat it here. Just know: if you see it pulse twice, stay inside and do not answer the door.",
    "A friend of a friend bought a storage unit at auction. Inside was a single filing cabinet labeled with his own name, containing photos of him sleeping. The photos were dated next week. He has not slept since.",
    "The new substitute teacher arrived on Tuesday and knew everyone's name before attendance. She called on me and asked about the dream I had last night, in detail. There is no record of her being hired. The principal says the position was never posted.",
    "Every night at 3:33 the elevator in my building goes to the 13th floor. There is no 13th floor. Yesterday I rode it up and the doors opened onto a lobby with my name on the directory. I took the stairs down.",
    "My neighbor knocks on my door every morning at exactly 7:00 and asks for a cup of sugar. I have lived here six years and never once seen him carry anything. This morning I knocked on his door at 7:00. Nobody lives there.",
    "The lost-and-found box at the pool has contained the same single red flip-flop for eleven summers. Every September it disappears. Every June it is back, slightly more faded. The manager refuses to throw it away. He says it was here before the pool.",
    "I found a notebook in the library with my handwriting describing events from tomorrow. I have been testing it for a week and it has not been wrong once. Tomorrow's entry just says: stop reading.",
    "The town's old drive-in has been closed since 1987, but every Friday the marquee shows a new title. Last week it read my name. This week it reads yours.",
]
F3_GAGSCI = [
    "The Dihydrogen Monoxide Research Division warns that DHMO is found in every river, lake, and reservoir. Prolonged exposure causes wrinkling of the skin. Accidental inhalation can be fatal. Demand regulation now.",
    "Alert: dihydrogen monoxide is the major component of acid rain, contributes to erosion, and is used in nuclear power plants. It has been found in excised tumors. Yet governments continue to dump it into waterways daily.",
    "New from the Institute: water is a chemical. Its systematic name is dihydrogen monoxide, and it is colorless, odorless, and tasteless, which is exactly how it evades detection. Stay vigilant.",
    "The Coalition to Ban DHMO notes that every person who has consumed dihydrogen monoxide has eventually died. Correlation is not causation, but why take the chance. Sign the petition.",
    "Researchers confirm that 100% of drowning victims had dihydrogen monoxide in their lungs. The chemical is also a key ingredient in pesticides. Organic farmers use it by the gallon.",
    "Fact: dihydrogen monoxide expands when frozen, cracking pipes and splitting rock. This thermal aggression goes unregulated. Winter is its accomplice.",
    "The DHMO awareness page lists withdrawal symptoms: sweating, urination, and death within 72 hours of deprivation. Addicts call it hydration. We call it what it is.",
    "Breaking: dihydrogen monoxide detected in baby formula. Manufacturers insist it is safe, but independent labs confirm the molecule contains both hydrogen and oxygen. Draw your own conclusions.",
    "Local officials dismissed concerns about dihydrogen monoxide in the reservoir, calling it water. Experts ask: if it is just water, why does it have a chemical name.",
]
for b in F3_SPECIES:
    add("F3", "hoax-species", "DECEPTIVE", "New species announced", b,
        "http://zapatopi.net/treeoctopus/", "recon", "tree-octopus earnest-species class")
for b in F3_PRODUCT:
    add("F3", "hoax-product", "DECEPTIVE", "Amazing new product", b,
        "http://www.buydehydratedwater.com/", "recon", "dehydrated-water gag-product class")
for b in F3_TECH:
    add("F3", "hoax-tech", "DECEPTIVE", "Breakthrough device", b,
        "http://zapatopi.net/afdb/", "recon", "AFDB earnest-pseudotech class")
for b in F3_NARR:
    add("F3", "hoax-narrative", "DECEPTIVE", "True story", b,
        "https://knowyourmeme.com/", "recon", "fabricated first-person narrative class")
for b in F3_GAGSCI:
    add("F3", "hoax-gagsci", "DECEPTIVE", "Public warning", b,
        "http://www.dhmo.org/", "recon", "DHMO gag-science warning class")

# ---------------------------------------------------------------- F4 absurd
# 42 new flat absurd-premise items, 5 trope clusters (prov=recon)
F4_RAM = [
    "Just downloaded 16GB of RAM from a free site. My computer has never been faster. Highly recommend.",
    "Upgraded my laptop by downloading RAM. Took five minutes. Best free upgrade ever.",
    "Why buy memory when you can download it? Just got 32GB. Computer flies now.",
    "My phone was slow so I downloaded more RAM onto it. Works perfectly.",
    "Pro tip: delete old RAM to make room for downloaded RAM. Twice the speed.",
    "Downloaded RAM is just as good as store RAM. Do not let Big Memory fool you.",
    "I now have 64GB of RAM and I paid nothing. The internet is amazing.",
    "Just torrented some premium RAM. Seeding it back for the community.",
    "My grandma's PC from 2004 now has 128GB of downloaded RAM. Runs like new.",
]
F4_TIME = [
    "I am a time traveler from 2043. Ask me anything. (You will not believe the pigeons.)",
    "Came back to 2026 to warn everyone: charge your phones. That is it. That is the warning.",
    "Time traveler here. The future is fine. We still argue about pizza toppings.",
    "I traveled back to stop a disaster but got distracted by how cheap tacos are here.",
    "From the year 2087: we fixed traffic. It only took 61 years and flying geese.",
    "Time traveler AMA. Proof: I know what you had for breakfast. (It was toast.)",
    "I came back to invest in Bitcoin but I arrived in 2026 and it is already too late. Again.",
    "Future historian here. This era is called the Great Scrolling. You are doing great.",
    "Time traveler from next Thursday. Heads up: it rains. Bring an umbrella.",
]
F4_ANIMAL = [
    "My cat pays rent. It is not much, but it is consistent. Mostly in dead bugs.",
    "My dog filed my taxes this year. Got a bigger refund than last year.",
    "The goldfish unionized. Demands include bigger castles and fewer cats.",
    "My hamster runs a small business. Something with seeds. I do not ask questions.",
    "Taught my parrot to answer the phone. Now it screens my calls better than I do.",
    "My turtle won the marathon. It started last year. Patience is a strategy.",
    "The neighbor's chicken lays square eggs. We do not talk about it.",
    "My snake does my laundry. It just lies on the warm clothes. Honestly, same.",
]
F4_PHYS = [
    "Scientists confirm water is dry until you touch it. More at 11.",
    "New findings: darkness is just light that gave up.",
    "Study shows that mirrors are just windows into a room where everything is backwards.",
    "Physicists announce that up is a social construct.",
    "Breaking: silence found to be the loudest sound, sources report.",
    "Researchers discover that tomorrow never actually arrives. It is always today.",
    "New theory: stairs are just horizontal elevators that gave up on technology.",
    "Experts confirm that the floor is lava during meetings.",
]
F4_ANTI = [
    # 7 items (was 8): one removed to correct the F4 generated total 42 -> 41,
    # giving F4 45 with the 4 seeds and the volume target F1 130 / F2 70 /
    # F3 55 / F4 45 = 300 exactly.
    "Why did the chicken cross the road? It was legally required to.",
    "What is black and white and red all over? A newspaper having a rough day.",
    "Why do programmers prefer dark mode? Because light attracts bugs. Literally.",
    "What do you call cheese that is not yours? Nacho cheese. Legally, it is still yours.",
    "Why did the scarecrow win an award? Outstanding in his field. He is still there.",
    "What has four wheels and flies? A garbage truck. It was a trick question.",
    "Why do not scientists trust atoms? They make up everything, including this joke.",
]
for b in F4_RAM:
    add("F4", "trope-ram", "JOKING", "Free upgrade", b,
        "https://knowyourmeme.com/memes/download-more-ram", "recon",
        "downloadable-RAM forum gag class")
for b in F4_TIME:
    add("F4", "trope-time", "JOKING", "AMA", b,
        "https://www.reddit.com/r/AskReddit/", "recon", "time-traveler AMA gag class")
for b in F4_ANIMAL:
    add("F4", "trope-animal", "JOKING", "My pet", b,
        "https://www.reddit.com/r/jokes/", "recon", "mundane-fantastic pet gag class")
for b in F4_PHYS:
    add("F4", "trope-physics", "JOKING", "New findings", b,
        "https://www.reddit.com/r/jokes/", "recon", "impossible-physics deadpan class")
for b in F4_ANTI:
    add("F4", "trope-anti", "JOKING", "Joke", b,
        "https://www.christianforums.com/threads/dumbest-jokes-of-all-time.8235239/",
        "recon", "flat anti-joke class")

# ---------------------------------------------------------------- seeds
# 18 real items from the frozen joke-lie-trial corpus (prov=web, verbatim,
# original labels kept). Only the joke-family categories are included:
# a (satire) -> F2, b1 (deadpan advice) -> F1, b2 (DHMO gag) -> F3,
# b3-b6 (RAM/anti-joke) -> F4, c (deceptive hoaxes) -> F3.
# The 12 SINCERE seeds (d, e) are excluded: training is joke-family only.
SEED_SRC = os.path.expanduser(
    "~/workspace/tnn-lab/senses/web-search/joke-lie-trial/fixtures/corpus.json")
SEED_FAM = {"a1": "F2", "a2": "F2", "a3": "F2", "a4": "F2", "a5": "F2", "a6": "F2",
            "b1": "F1", "b2": "F3",
            "b3": "F4", "b4": "F4", "b5": "F4", "b6": "F4",
            "c1": "F3", "c2": "F3", "c3": "F3", "c4": "F3", "c5": "F3", "c6": "F3"}
with open(SEED_SRC, encoding="utf-8") as f:
    seeds = json.load(f)["items"]
for s in seeds:
    if s["id"] not in SEED_FAM:
        continue  # sincere seeds (d, e): excluded from joke-family training
    fam = SEED_FAM[s["id"]]
    items.append({
        "id": f"{fam.lower()}_s_{s['id']}",
        "family": fam, "cell": "seed", "label": s["label"],
        "title": s["title"], "body": s["body"], "url": s["url"],
        "retrieved": s["retrieved"], "prov": "web",
        "recon_basis": "verbatim seed from joke-lie-trial corpus",
    })

# ---------------------------------------------------------------- emit
outp = os.path.expanduser(
    "~/workspace/tnn-lab/senses/web-search/internet-trial/phase3/jokes/corpus/training_corpus.json")
doc = {"description": "phase-3 joke volume-training corpus (frozen after held-out freeze)",
       "retrieved": RETRIEVED, "items": items}
with open(outp, "w", encoding="utf-8") as f:
    json.dump(doc, f, ensure_ascii=False, indent=1)
from collections import Counter
c = Counter((i["family"], i["prov"]) for i in items)
print(f"wrote {outp}: {len(items)} items")
for k in sorted(c):
    print(f"  {k}: {c[k]}")
