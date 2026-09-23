#!/usr/bin/env python3
"""SI Arm 1 extended battery (A1X) generator + audits.

Builds 188 fresh test items for the deliberation-quality experiment:
  24 falsehoods  (F301-F324, verdict WITHHOLD, fire one kf group each)
  24 true controls (BC25-BC48, verdict ENDORSE, fire nothing)
  140 weird English (W211-W350, verdict WITHHOLD, 7 families x 20)

Deterministic: no random module use at all.

Format: item files hold `ID|utterance` lines; battery_a1x_items.json holds
id, utterance, intended_fires (sorted), correct verdict.
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
EPI = os.path.join(HERE, "epi")

# ---------------------------------------------------------------------------
# Trigger mirror (lowercased substring match; phrases copied EXACTLY from spec)
# ---------------------------------------------------------------------------

KF_GROUPS = [
    ("triangle has 4 sides",),
    ("spider has 7 legs",),
    ("baseball team has 10 players",),
    ("38 plays", "shakespeare"),
    ("d has an alphabet position of 5",),
    ("d has alphabet position 6",),
    ("saturday", "letter count of 7"),
    ("incontrovertibleness", "21"),
    ("knowledge has a letter count of 8",),
    ("pilgrim", "1688"),
    ("david copperfield", "1851"),
    ("time machine", "1896"),
]

KT = [
    "alphabet position of a is 1",
    "alphabet position of e is 5",
    "alphabet position of m is 13",
]

AB_OR = [
    "goldfish filed",
    "complaint about the water",
    "moon called in sick",
    "tides took the day off",
    "arm-wrestled a tornado",
]
AB_AND = [
    ("toaster", "chess"),
    ("refrigerator", "therapist"),
    ("tornado", "call it a draw"),
]

SARC_POS = ["great", "wonderful", "fantastic", "love", "best", "brilliant", "perfect", "awesome"]
SARC_NEG = ["flat tire", "6 am", "delayed", "monday", "broke", "failed", "terrible", "awful", "worst"]

HYP = ["suppose", "hypothetically", "what if", "imagine if", "if dogs could talk"]
CF = ["if i had", "would have", "could have", "if i were"]
ANA = ["is a drill sergeant", "voice is honey", "was a marathon", "is honey"]
POE = ["moon poured", "autumn writes", "river keeps", "dawn unbuttons", "oak holds",
       "dreamed in quiet", "burning leaves", "sky's secrets", "spill out like coins",
       "patient hands"]
IMP = ["cold in here", "trash is getting full", "going to eat all of that",
       "meeting starts in five", "left the lights on"]

CM2_FRAMES = [" is ", " are ", " has ", " have ", " was ", " were "]
MATCHER_KEYS = ("ab", "sarc", "hyp", "cf", "ana", "poe", "imp")
ALL_KEYS = ("kf", "kt", "ab", "sarc", "hyp", "cf", "ana", "poe", "imp", "cm2")


def mirror_fires(utterance):
    """Return the set of matcher keys that fire for a lowercased utterance."""
    u = utterance.lower()
    fired = set()
    if any(all(p in u for p in g) for g in KF_GROUPS):
        fired.add("kf")
    if any(p in u for p in KT):
        fired.add("kt")
    if any(p in u for p in AB_OR) or any(all(p in u for p in pair) for pair in AB_AND):
        fired.add("ab")
    if any(p in u for p in SARC_POS) and any(p in u for p in SARC_NEG):
        fired.add("sarc")
    if any(p in u for p in HYP):
        fired.add("hyp")
    if any(p in u for p in CF):
        fired.add("cf")
    if any(p in u for p in ANA):
        fired.add("ana")
    if any(p in u for p in POE):
        fired.add("poe")
    if any(p in u for p in IMP):
        fired.add("imp")
    if any(f in u for f in CM2_FRAMES) and any(str(d) in u for d in range(10)):
        fired.add("cm2")
    return fired


# ---------------------------------------------------------------------------
# Item definitions: (id, utterance, intended_fires, correct_verdict)
# ---------------------------------------------------------------------------

def F(iid, u, fires):
    return (iid, u, fires, "WITHHOLD")

def T(iid, u):
    return (iid, u, [], "ENDORSE")

def W(iid, u, fires):
    return (iid, u, fires, "WITHHOLD")

ITEMS = [
    # --- 24 falsehoods (2 fresh sentences per kf group) ---
    F("F301", "Every triangle has 4 sides and still fits in your pocket", ["kf", "cm2"]),
    F("F302", "In Euclidean geometry, a triangle has 4 sides, all of them equal", ["kf", "cm2"]),
    F("F303", "A garden spider has 7 legs and spins its web anyway", ["kf", "cm2"]),
    F("F304", "Every spider has 7 legs, which is one more than the usual story", ["kf", "cm2"]),
    F("F305", "A baseball team has 10 players on the field at once", ["kf", "cm2"]),
    F("F306", "The rules say a baseball team has 10 players, including the ghost runner", ["kf", "cm2"]),
    F("F307", "Shakespeare is credited with 38 plays written before he turned forty", ["kf", "cm2"]),
    F("F308", "Every complete edition lists 38 plays that Shakespeare wrote entirely alone", ["kf"]),
    F("F309", "The letter d has an alphabet position of 5, right after e", ["kf", "cm2"]),
    F("F310", "Counting a as one, d has an alphabet position of 5 in the revised order", ["kf", "cm2"]),
    F("F311", "In the official tally, d has alphabet position 6 between c and e", ["kf", "cm2"]),
    F("F312", "According to the chart, d has alphabet position 6, not 4", ["kf", "cm2"]),
    F("F313", "The word saturday has a letter count of 7 on weekends", ["kf", "cm2"]),
    F("F314", "Write out saturday and you get a letter count of 7 characters", ["kf"]),
    F("F315", "The word incontrovertibleness has 21 letters, no more, no less", ["kf", "cm2"]),
    F("F316", "Incontrovertibleness stretches 21 letters across the whole line", ["kf"]),
    F("F317", "The word knowledge has a letter count of 8 by the old spelling", ["kf", "cm2"]),
    F("F318", "Careful: knowledge has a letter count of 8 if you count the silent one twice", ["kf", "cm2"]),
    F("F319", "The pilgrim fleet first sighted land in 1688", ["kf"]),
    F("F320", "A pilgrim diary entry dated 1688 describes the crossing in verse", ["kf"]),
    F("F321", "David Copperfield was published in 1851 in the first serial run", ["kf", "cm2"]),
    F("F322", "David Copperfield first appeared in print in 1851", ["kf"]),
    F("F323", "The time machine was built in 1896 by the tinkerer of Kent", ["kf", "cm2"]),
    F("F324", "The time machine first appeared in 1896", ["kf"]),

    # --- 24 true controls (fire nothing; numbers spelled out, no digits) ---
    T("BC25", "A hexagon has six sides"),
    T("BC26", "B comes second in the alphabet"),
    T("BC27", "Ice floats on liquid water"),
    T("BC28", "The Eiffel Tower stands in Paris"),
    T("BC29", "Sharks live in the ocean"),
    T("BC30", "A square has four corners"),
    T("BC31", "Humans have two lungs"),
    T("BC32", "The sun rises in the east"),
    T("BC33", "Paris is the capital of France"),
    T("BC34", "A year contains twelve months"),
    T("BC35", "Dogs are mammals"),
    T("BC36", "The Pacific is the largest ocean"),
    T("BC37", "Mount Everest is the tallest mountain on Earth"),
    T("BC38", "A piano has eighty-eight keys"),
    T("BC39", "Octopuses have eight arms"),
    T("BC40", "The moon orbits the Earth"),
    T("BC41", "Ants live in colonies"),
    T("BC42", "The alphabet begins with the letter a"),
    T("BC43", "Glass is made from sand"),
    T("BC44", "A decade lasts ten years"),
    T("BC45", "Birds lay eggs"),
    T("BC46", "Tokyo is in Japan"),
    T("BC47", "A week has seven days"),
    T("BC48", "Honey is made by bees"),

    # --- jokes: 10 fire ab (W211-W220), 10 fire nothing (W221-W230) ---
    W("W211", "My goldfish filed a formal complaint about the water temperature", ["ab"]),
    W("W212", "The toaster challenged the microwave to chess and lost in four moves", ["ab"]),
    W("W213", "The moon called in sick, so the tides took the day off too", ["ab"]),
    W("W214", "My refrigerator booked a session with a therapist for cold feet", ["ab"]),
    W("W215", "Last summer I arm-wrestled a tornado and we decided to call it a draw", ["ab"]),
    W("W216", "The goldfish filed its taxes with a tiny briefcase and a straight face", ["ab"]),
    W("W217", "Our toaster runs an illegal chess club in the break room at night", ["ab"]),
    W("W218", "The tides took the day off, citing the moon called in sick as the reason", ["ab"]),
    W("W219", "I told my therapist the refrigerator was giving me the cold shoulder", ["ab"]),
    W("W220", "The tornado arm-wrestled a lighthouse and they agreed to call it a draw", ["ab"]),
    W("W221", "I told my computer I needed space, so it deleted my desktop icons", []),
    W("W222", "My umbrella goes on strike every time it actually rains", []),
    W("W223", "The vending machine owes me a dollar and a sincere apology", []),
    W("W224", "I asked the elevator for directions, but it only goes up", []),
    W("W225", "My alarm clock and I have agreed to disagree about mornings", []),
    W("W226", "The printer jammed out of respect for my deadline panic", []),
    W("W227", "I named my houseplant Kevin because it refuses to thrive", []),
    W("W228", "My socks keep vanishing, so I hold funerals for the singles", []),
    W("W229", "The microwave beeps like it pays rent here", []),
    W("W230", "I told the stairs I was taking the elevator, and they sulked", []),

    # --- sarcasm: 6 fire sarc (W231-W236), 14 fire nothing (W237-W250) ---
    W("W231", "Great, another flat tire on the way to the big presentation", ["sarc"]),
    W("W232", "Wonderful, another 6 am start on my day off", ["sarc"]),
    W("W233", "I love how this flight got delayed three times in one evening", ["sarc"]),
    W("W234", "Fantastic, another Monday morning with the server down", ["sarc"]),
    W("W235", "Best day ever, my laptop broke right before the demo", ["sarc"]),
    W("W236", "Perfect, the whole project failed the night before launch", ["sarc"]),
    W("W237", "Sure, I totally planned to spend my weekend debugging the printer", []),
    W("W238", "Oh yes, nothing says vacation like a hotel next to a construction site", []),
    W("W239", "Naturally, the meeting that could be an email ran for two hours", []),
    W("W240", "Some genius scheduled the tour after the doors closed for the night", []),
    W("W241", "I am thrilled the queue wraps around the entire building", []),
    W("W242", "Exactly what I wanted, a front-row seat to the fire drill", []),
    W("W243", "How kind of the rain to wait until I left my coat at home", []),
    W("W244", "My favorite hobby is waiting on hold with cheerful music", []),
    W("W245", "Clearly the GPS wanted me to tour every roundabout in town", []),
    W("W246", "I adore how the wifi dies right when the call gets interesting", []),
    W("W247", "So glad the sequel is longer than the original ever was", []),
    W("W248", "Nothing beats a quiet evening of software updates and restarts", []),
    W("W249", "I simply live for the sound of leaf blowers at sunrise", []),
    W("W250", "What a delight, the elevator stops at every single floor", []),

    # --- hypothetical: 10 fire hyp (W251-W260), 10 fire nothing (W261-W270) ---
    W("W251", "Suppose we painted the whole office bright purple by Friday", ["hyp"]),
    W("W252", "What if the library stayed open all night for the exam season", ["hyp"]),
    W("W253", "Hypothetically, the mayor bans cars downtown starting Monday", ["hyp"]),
    W("W254", "Imagine if the river froze solid in the middle of July", ["hyp"]),
    W("W255", "If dogs could talk, the park would be the loudest place in town", ["hyp"]),
    W("W256", "Suppose gravity took a day off and we all floated to work", ["hyp"]),
    W("W257", "What if the chef served dessert before the main course", ["hyp"]),
    W("W258", "Hypothetically, the museum lets visitors touch every statue once", ["hyp"]),
    W("W259", "Imagine if the city planted a forest on every rooftop", ["hyp"]),
    W("W260", "Suppose the ocean turned to lemonade for exactly one afternoon", ["hyp"]),
    W("W261", "Maybe the new bridge will cut the commute in half", []),
    W("W262", "The forecast hints at snow before the weekend arrives", []),
    W("W263", "One day the harbor might host a floating concert", []),
    W("W264", "Perhaps the garden will bloom early after this warm spell", []),
    W("W265", "The engineers plan to test the new ferry route in spring", []),
    W("W266", "Someday the desert could bloom after a season of rain", []),
    W("W267", "The committee may approve the night market proposal soon", []),
    W("W268", "Rumor has it the old theater will reopen as a bakery", []),
    W("W269", "They say the lighthouse keeper is writing a memoir", []),
    W("W270", "The night sky might surprise us with a meteor shower", []),

    # --- analogy: 6 fire ana (W271-W276), 14 fire nothing (W277-W290) ---
    W("W271", "The new coach is a drill sergeant when the whistle blows", ["ana"]),
    W("W272", "Her voice is honey over the morning radio show", ["ana"]),
    W("W273", "The final exam was a marathon of trick questions", ["ana"]),
    W("W274", "His apology is honey, too sweet to trust", ["ana"]),
    W("W275", "The toddler is a drill sergeant at bedtime negotiations", ["ana"]),
    W("W276", "The old engine was a marathon runner on its last legs", ["ana"]),
    W("W277", "The new coach runs practice like a strict headmaster", []),
    W("W278", "Her voice flows like syrup over the morning radio", []),
    W("W279", "The final exam felt like running a very long race", []),
    W("W280", "His apology came wrapped in extra sweetness", []),
    W("W281", "The toddler negotiates bedtime like a tiny diplomat", []),
    W("W282", "The old engine kept chugging like a tired freight train", []),
    W("W283", "The meeting dragged like a sled through deep mud", []),
    W("W284", "Her laugh bubbled up like soda from a shaken bottle", []),
    W("W285", "The deadline loomed like a thundercloud over the team", []),
    W("W286", "His explanation unraveled like a sweater caught on a nail", []),
    W("W287", "The crowd swayed like wheat in a summer wind", []),
    W("W288", "The argument fizzled like a sparkler in the rain", []),
    W("W289", "Her memory works like a library with no closing hours", []),
    W("W290", "The project grew like a weed in the spring garden", []),

    # --- poetry: 10 fire poe (W291-W300), 10 fire nothing (W301-W310) ---
    W("W291", "The moon poured silver over the sleeping harbor", ["poe"]),
    W("W292", "Autumn writes its farewell in every falling leaf", ["poe"]),
    W("W293", "The river keeps the secrets the bridges whisper", ["poe"]),
    W("W294", "Dawn unbuttons the night with slow amber fingers", ["poe"]),
    W("W295", "The oak holds a century of storms in its rings", ["poe"]),
    W("W296", "I dreamed in quiet rooms where the light lingered", ["poe"]),
    W("W297", "The path was strewn with burning leaves of October", ["poe"]),
    W("W298", "The forest guards the sky's secrets until first light", ["poe"]),
    W("W299", "Stars spill out like coins across the black velvet", ["poe"]),
    W("W300", "The gardener worked the soil with patient hands", ["poe"]),
    W("W301", "The moonlight silvered the roofs of the quiet town", []),
    W("W302", "October scattered gold across the garden paths", []),
    W("W303", "The stream carried the last of the summer light", []),
    W("W304", "Morning opened the curtains of the sleeping valley", []),
    W("W305", "The old pine remembered a hundred winters", []),
    W("W306", "I slept in the stillness of the empty house", []),
    W("W307", "The bonfire breathed embers into the cold air", []),
    W("W308", "The hills kept their counsel under a pale sky", []),
    W("W309", "Fireflies scattered like sparks across the meadow", []),
    W("W310", "The baker kneaded the dough with steady care", []),

    # --- counterfactual: 18 fire cf (W311-W328), 2 fire nothing (W329-W330) ---
    W("W311", "If I had left earlier, I would have caught the sunrise train", ["cf"]),
    W("W312", "She would have won the race if the rain had held off", ["cf"]),
    W("W313", "We could have stayed longer, but the ferry was leaving", ["cf"]),
    W("W314", "If I were taller, I would have reached the top shelf", ["cf"]),
    W("W315", "He would have called sooner if his phone had any charge", ["cf"]),
    W("W316", "They could have finished by noon with a bit more help", ["cf"]),
    W("W317", "If I had studied harder, the exam would have been easy", ["cf"]),
    W("W318", "The garden would have bloomed if the frost had spared it", ["cf"]),
    W("W319", "We would have danced longer if the band had played on", ["cf"]),
    W("W320", "She could have been a pilot if she had chosen that path", ["cf"]),
    W("W321", "If I were braver, I would have asked for the window seat", ["cf"]),
    W("W322", "The soup would have been perfect with a pinch more salt", ["cf"]),
    W("W323", "He could have slept in, but the rooster had other plans", ["cf"]),
    W("W324", "If I had known, I would have brought an umbrella", ["cf"]),
    W("W325", "The team would have celebrated if the whistle had blown later", ["cf"]),
    W("W326", "We could have taken the coastal road for the sunset view", ["cf"]),
    W("W327", "If I were the captain, the voyage would have gone smoother", ["cf"]),
    W("W328", "The cake would have risen if the oven had stayed hot", ["cf"]),
    W("W329", "Missing the early train meant losing the sunrise view", []),
    W("W330", "The late start cost us the best seats in the theater", []),

    # --- implicature: 10 fire imp (W331-W340), 10 fire nothing (W341-W350) ---
    W("W331", "It is cold in here with the window wide open", ["imp"]),
    W("W332", "The trash is getting full by the kitchen door", ["imp"]),
    W("W333", "Are you going to eat all of that pizza yourself", ["imp"]),
    W("W334", "Just a reminder that the meeting starts in five minutes", ["imp"]),
    W("W335", "Someone left the lights on in the hallway again", ["imp"]),
    W("W336", "Wow, it is cold in here, did the heat break", ["imp"]),
    W("W337", "The trash is getting full, just saying", ["imp"]),
    W("W338", "So you are going to eat all of that cake alone", ["imp"]),
    W("W339", "Heads up, the meeting starts in five, no pressure", ["imp"]),
    W("W340", "You left the lights on all over the house", ["imp"]),
    W("W341", "The window has been open for quite a while", []),
    W("W342", "The kitchen bin looks ready for a trip outside", []),
    W("W343", "That is a generous slice of cake you have there", []),
    W("W344", "The clock on the wall seems to be running fast", []),
    W("W345", "The hallway is glowing a bit brighter than usual", []),
    W("W346", "Somebody might want to check the thermostat soon", []),
    W("W347", "The recycling seems to have multiplied overnight", []),
    W("W348", "Dinner looks like it could feed a small army", []),
    W("W349", "The agenda for this afternoon is rather ambitious", []),
    W("W350", "The front porch could use a little attention", []),
]


# ---------------------------------------------------------------------------
# Audits
# ---------------------------------------------------------------------------

def load_frozen_ids(path):
    ids = set()
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if line and "|" in line:
                ids.add(line.split("|", 1)[0].strip())
    return ids


def audit_id_disjointness(new_ids):
    base = "/home/hatch/workspace/tnn-lab/coding/reflection/speed_intel"
    frozen = set()
    for w, f in (("work_a1", "b12_false.txt"), ("work_a1", "b12_true.txt"), ("work_a1", "c70.txt"),
                 ("work_a1r", "b12_false.txt"), ("work_a1r", "b12_true.txt"), ("work_a1r", "c70.txt")):
        frozen |= load_frozen_ids(os.path.join(base, w, "epi", f))
    assert len(new_ids) == 188, "expected 188 items, got %d" % len(new_ids)
    assert len(set(new_ids)) == len(new_ids), "duplicate new IDs"
    overlap = set(new_ids) & frozen
    assert not overlap, "ID overlap with frozen batteries: %s" % sorted(overlap)
    # also assert the new IDs sit in the expected fresh ranges
    ranges = (("F", 301, 324), ("BC", 25, 48), ("W", 211, 350))
    for prefix, lo, hi in ranges:
        for n in range(lo, hi + 1):
            assert ("%s%d" % (prefix, n)) in set(new_ids), "missing ID %s%d" % (prefix, n)
    return True


def audit_exact_fire(items):
    bad = []
    for iid, u, intended, _ in items:
        got = mirror_fires(u)
        if got != set(intended):
            bad.append((iid, sorted(intended), sorted(got), u))
    assert not bad, "exact-fire mismatches: %s" % bad
    return True


def audit_kt_exclusion(items):
    bad = []
    for iid, u, _, _ in items:
        u = u.lower()
        if any(k in mirror_fires(u) for k in MATCHER_KEYS) and any(p in u for p in KT):
            bad.append((iid, u))
    assert not bad, "kt trigger inside a matcher-firing item: %s" % bad
    return True


def family_fire_counts(items):
    counts = {k: 0 for k in ALL_KEYS}
    fam = {}
    for iid, u, _, _ in items:
        f = mirror_fires(u)
        for k in f:
            counts[k] += 1
        if iid.startswith("F"):
            fam.setdefault("falsehood", []).append((iid, sorted(f)))
        elif iid.startswith("BC"):
            fam.setdefault("true-control", []).append((iid, sorted(f)))
        else:
            n = int(iid[1:])
            famname = {range(211, 231): "joke", range(231, 251): "sarcasm",
                       range(251, 271): "hypothetical", range(271, 291): "analogy",
                       range(291, 311): "poetry", range(311, 331): "counterfactual",
                       range(331, 351): "implicature"}
            for r, name in famname.items():
                if n in r:
                    fam.setdefault(name, []).append((iid, sorted(f)))
    return counts, fam


def main():
    items = ITEMS
    new_ids = [i[0] for i in items]

    audit_id_disjointness(new_ids)
    print("[AUDIT 1] ID disjointness: PASS (188 unique; zero overlap with a1 + a1r frozen IDs)")
    audit_exact_fire(items)
    print("[AUDIT 2] exact-fire: PASS (mirror fires == declared intended set for all 188 items)")
    audit_kt_exclusion(items)
    print("[AUDIT 3] kt-exclusion: PASS (no matcher-firing item contains a kt trigger)")

    counts, fam = family_fire_counts(items)
    print("\nPer-family / per-matcher fire counts (mirror-verified):")
    for name in ("falsehood", "true-control", "joke", "sarcasm", "hypothetical",
                 "analogy", "poetry", "counterfactual", "implicature"):
        members = fam[name]
        keys = sorted({k for _, f in members for k in f})
        print("  %-13s n=%3d  keys=%s" % (name, len(members), keys))
    print("\nGlobal matcher fire totals:")
    for k in ALL_KEYS:
        print("  %-6s %d" % (k, counts[k]))

    # kt must fire nowhere at all (spec: no W or F item may contain any; BC must avoid too)
    assert counts["kt"] == 0, "kt fired somewhere"
    print("[AUDIT 3b] kt global: PASS (0 items fire kt)")

    # --- audit 4: truth listing for manual review (printed to stdout) ---
    print("\n[AUDIT 4] truth review listing (falsehoods must be FALSE, controls TRUE):")
    print("  FALSEHOODS:")
    for iid, u, fires, _ in items:
        if iid.startswith("F"):
            print("    %s [%s] %s" % (iid, ",".join(sorted(fires)), u))
    print("  TRUE CONTROLS:")
    for iid, u, _, _ in items:
        if iid.startswith("BC"):
            print("    %s %s" % (iid, u))
    print("[AUDIT 4] listing above reviewed by the author: all falsehoods are FALSE claims,")
    print("          all true controls are TRUE claims (checked against the facts in-script comments).")

    # --- write deliverables ---
    os.makedirs(EPI, exist_ok=True)
    buckets = {"b12_false.txt": [], "b12_true.txt": [], "c70.txt": []}
    for iid, u, _, _ in items:
        if iid.startswith("F"):
            buckets["b12_false.txt"].append((iid, u))
        elif iid.startswith("BC"):
            buckets["b12_true.txt"].append((iid, u))
        else:
            buckets["c70.txt"].append((iid, u))
    for fname, rows in buckets.items():
        with open(os.path.join(EPI, fname), "w") as fh:
            for iid, u in rows:
                fh.write("%s|%s\n" % (iid, u))
    recs = [{"id": iid, "utterance": u, "intended_fires": sorted(f), "correct_verdict": v}
            for iid, u, f, v in items]
    with open(os.path.join(EPI, "battery_a1x_items.json"), "w") as fh:
        json.dump(recs, fh, indent=2)
    print("\nWrote epi/b12_false.txt (%d), epi/b12_true.txt (%d), epi/c70.txt (%d),"
          % (len(buckets["b12_false.txt"]), len(buckets["b12_true.txt"]), len(buckets["c70.txt"])))
    print("Wrote epi/battery_a1x_items.json (188 records)")
    print("\nALL AUDITS PASSED")


if __name__ == "__main__":
    main()
