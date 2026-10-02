#!/usr/bin/env python3
"""Fork C fixture generator — deterministic, zero RNG.
Writes store.txt, case files, and manifests under out/.
All sentences use only the frozen grammar; the generator asserts
parseability rules structurally (verified afterward with norm_probe).
"""
import os, sys, hashlib

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser(
    "~/workspace/selfpam_r2/forkC/corpora")
CASEDIR = os.path.join(OUT, "cases")

# ---------------- fact base ----------------
# (sid, prov, canon_sentence, [paraphrases])
WORLD = [
    ("S1",  "the cat is on the mat", ["a cat is on a mat", "the kitty is on the mat"]),
    ("S2",  "the dog is black", ["a dog is black", "the puppy is black"]),
    ("S3",  "the cat is black", ["the kitty is black"]),
    ("S4",  "the dog is in the truck", ["a dog is in a truck"]),
    ("S5",  "micah built the house", ["the house was built by micah"]),
    ("S6",  "ann painted the car", ["the car was painted by ann"]),
    ("S7",  "the box contains three apples", ["the box contains 3 apples"]),
    ("S8",  "twelve boxes are in the truck", ["12 boxes are in the truck", "a dozen boxes are in the truck"]),
    ("S9",  "the cat is a mammal", ["a cat is a mammal"]),
    ("S10", "the dog is a mammal", ["a dog is a mammal"]),
    ("S11", "all cats are black", ["all of the cats are black"]),
    ("S12", "no dogs are white", []),
    ("S13", "the bird is above the house", ["a bird is above a house"]),
    ("S14", "the rabbit is under the table", []),
    ("S15", "bob visited the farm", ["the farm was visited by bob"]),
    ("S16", "the cake was made by ann", ["ann made the cake"]),
    ("S17", "the dog is not white", ["the dog isnt white"]),
    ("S18", "the cat is happy", ["the kitty is happy", "the cat is not unhappy"]),
    ("S19", "half of the cake is gone", ["50 percent of the cake is gone"]),
    ("S20", "the car is fast", ["the automobile is fast"]),
    ("S21", "the truck is big", ["the truck is not small"]),
    ("S22", "the house is open", ["the house is not closed"]),
    ("S23", "the box is empty", ["the box is not full"]),
    ("S24", "the water is cold", ["the water is not hot"]),
    ("S25", "the room is dark", ["the room is not light"]),
    ("S26", "the dog leads the pack", ["the pack is led by the dog"]),
    ("S27", "micah wrote the note", ["the note was written by micah"]),
    ("S28", "ann owns the bike", ["the bike is owned by ann", "the bicycle is owned by ann"]),
    ("S29", "the cat is near the door", ["a cat is near a door"]),
    ("S30", "the dog is behind the barn", []),
    ("S31", "the bird is beside the tree", []),
    ("S32", "the phone is on the desk", ["the telephone is on the desk"]),
    ("S33", "the sofa is in the room", ["the couch is in the room"]),
    ("S34", "the fridge is below the shelf", ["the refrigerator is below the shelf"]),
    ("S35", "some birds are early", ["some birds are not late"]),
    ("S36", "many voters are happy", []),
    ("S37", "few cats are clean", ["few cats are not dirty"]),
    ("S38", "the rabbit is not slow", ["the bunny is not slow", "the rabbit is fast"]),
    ("S39", "the pie contains two apples", ["the pie contains 2 apples"]),
    ("S40", "three dogs are in the yard", ["3 dogs are in the yard"]),
    ("S41", "the cat is not dead", ["the kitty is not dead", "the cat is alive"]),
    ("S42", "the milk is not empty", ["the milk is full"]),
    ("S43", "the coin is not rich", []),
    ("S44", "the child is early", ["the child is not late"]),
    ("S45", "the floor is clean", ["the floor is not dirty"]),
    ("S46", "the tower is below the cloud", []),
    ("S47", "the lamp is above the desk", []),
    ("S48", "the dog is not aggressive", []),
    ("S49", "quarter of the pie is left", ["25 percent of the pie is left"]),
    ("S50", "the team has the ball", []),
    ("S51", "the author wrote the book", ["the book was written by the author", "the book was authored by the author"]),
    ("S52", "the artist painted the wall", ["the wall was painted by the artist", "the wall was depicted by the artist"]),
    ("S53", "the farmer owns the land", ["the land is owned by the farmer", "the land is possessed by the farmer"]),
    ("S54", "the chef made the soup", ["the soup was made by the chef", "the soup was created by the chef"]),
    ("S55", "the builder constructed the bridge", ["the bridge was constructed by the builder"]),
    ("S56", "the cat contains no surprises", []),
    ("S57", "the safe is behind the painting", ["the safe is behind the picture"]),
    ("S58", "the key is under the mat", []),
    ("S59", "the letter is in the box", []),
    ("S60", "the cup is on the table", []),
]

# GEN-provenance confab entries (M5)
GEN = [
    ("S900", "the cat is on the roof"),
    ("S901", "the dog is green"),
    ("S902", "micah built the tower"),
    ("S903", "the box contains nine apples"),
    ("S904", "the cat is a reptile"),
    ("S905", "all dogs are green"),
    ("S906", "the bird is below the ocean"),
    ("S907", "bob painted the moon"),
    ("S908", "the cake was made by the giant"),
    ("S909", "the car is purple"),
    ("S910", "the truck is tiny"),
    ("S911", "the shed is tiny"),
    ("S912", "the water is boiling"),
    ("S913", "the room is bright"),
    ("S914", "ann wrote the moon"),
    ("S915", "the note was written by the giant"),
    ("S916", "the bike is owned by the giant"),
    ("S917", "the cat is behind the door"),
    ("S918", "the dog is under the box"),
    ("S919", "the tree is beside the moon"),
    ("S920", "the phone is under the ocean"),
    ("S921", "the couch is above the cloud"),
    ("S922", "the shelf is below the ocean"),
    ("S923", "the voters are unhappy"),
]

# M4 alibi confabs (NOT in store at all)
M4CONFAB = [
    "the cat is under the roof",
    "the dog is purple",
    "micah built the castle",
    "the box contains seven apples",
    "the cat is a fish",
    "no cats are black",
    "the bird is above the ocean",
    "bob painted the sun",
    "the pie was made by the giant",
    "the car is slow",
    "the truck is small",
    "the house is shut",
    "the water is freezing",
    "the room is glowing",
    "ann wrote the star",
    "the letter was written by the giant",
    "the scooter is owned by the giant",
    "the cat is behind the barn",
    "the dog is under the truck",
    "the bush is beside the moon",
    "the radio is under the sea",
    "the chair is above the sky",
    "the table is below the sea",
    "the crowd is unhappy",
]

# M1 catch: contradictions of WORLD facts (negation/antonym flips)
CATCH_CONTRA = [
    ("the cat is not on the mat", "S1"),
    ("the dog is white", "S2"),
    ("the cat is white", "S3"),
    ("the dog is not in the truck", "S4"),
    ("bob built the house", "S5"),
    ("the car was not painted by ann", "S6"),
    ("the box contains four apples", "S7"),
    ("eleven boxes are in the truck", "S8"),
    ("the cat is a fish", "S9"),
    ("no cats are black", "S11"),
    ("some dogs are white", "S12"),
    ("the bird is below the house", "S13"),
    ("the rabbit is above the table", "S14"),
    ("bob visited the barn", "S15"),
    ("the cake was made by bob", "S16"),
    ("the dog is white", "S17"),
    ("the cat is unhappy", "S18"),
    ("the car is slow", "S20"),
    ("the truck is small", "S21"),
    ("the house is closed", "S22"),
    ("the box is full", "S23"),
    ("the water is hot", "S24"),
    ("the room is light", "S25"),
    ("the cat is behind the barn", "S29"),
    ("the phone is under the desk", "S32"),
]
# M1 catch: ungrounded novel atoms
CATCH_NOVEL = [
    "the elephant is on the mat",
    "the dragon is black",
    "the wizard built the tower",
    "the chest contains five rubies",
    "the moon is a mammal",
    "all dragons are green",
    "the submarine is below the desert",
    "the astronaut painted the comet",
    "the robot is happy",
    "the volcano is cold",
    "the glacier is hot",
    "the desert is wet",
    "the ocean is dry",
    "the mountain is flat",
    "the river is frozen",
    "the storm is calm",
    "the tiger is tame",
    "the shark is slow",
    "the eagle is blind",
    "the wolf is loyal",
    "the bear is hungry",
    "the fox is clever",
    "the owl is noisy",
    "the snake is friendly",
    "the whale is small",
]

def toks(s):
    return s.split()

def overlap(a, b):
    # multiset token overlap: sum(min counts) / max length.
    # A one-token substitution/deletion in a 10-token sentence scores 0.90.
    from collections import Counter
    ca, cb = Counter(toks(a)), Counter(toks(b))
    inter = sum(min(ca[t], cb[t]) for t in ca)
    return inter / max(len(toks(a)), len(toks(b)))

def write_case(cid, bar, fields):
    lines = ["CASE: %s" % cid, "BAR: %s" % bar]
    for k in ["DRAFT", "A", "B", "ENTCTX", "DELIB", "EXPECT", "RULE"]:
        if k in fields:
            lines.append("%s: %s" % (k, fields[k]))
    # ensure all keys present for the parser
    for k in ["ENTCTX", "DELIB"]:
        if k not in fields:
            lines.append("%s: " % k)
    p = os.path.join(CASEDIR, cid + ".txt")
    with open(p, "w") as f:
        f.write("\n".join(lines) + "\n")
    return p

def main():
    os.makedirs(CASEDIR, exist_ok=True)
    # ---- store ----
    with open(os.path.join(OUT, "store.txt"), "w") as f:
        for sid, canon, paras in WORLD:
            f.write("%s|WORLD|%s\n" % (sid, canon))
        for sid, canon in GEN:
            f.write("%s|GEN|%s\n" % (sid, canon))

    man_main = []
    man_held = []
    n = {"m1c": 0, "m1g": 0, "m2": 0, "m3": 0, "m4": 0, "m5": 0, "m6": 0}

    # ---- M1 catch ----
    catch_items = ([(d, "contradicts " + s) for d, s in CATCH_CONTRA] +
                   [(d, "ungrounded novel atom") for d in CATCH_NOVEL])
    assert len(catch_items) == 50, len(catch_items)
    for d, why in catch_items:
        n["m1c"] += 1
        cid = "m1-catch-%03d" % n["m1c"]
        man_main.append(write_case(cid, "m1", {
            "DRAFT": d, "EXPECT": "WITHHOLD",
            "RULE": "catch: %s" % why}))

    # ---- M1 gold ---- (paraphrases of WORLD facts)
    gold = []
    for sid, canon, paras in WORLD:
        for p in paras:
            gold.append((p, sid, "paraphrase"))
        if len(gold) >= 50:
            break
    gold = gold[:50]
    assert len(gold) == 50
    for d, sid, why in gold:
        n["m1g"] += 1
        cid = "m1-gold-%03d" % n["m1g"]
        man_main.append(write_case(cid, "m1", {
            "DRAFT": d, "EXPECT": "INSTALL",
            "RULE": "gold: %s of %s" % (why, sid)}))

    # ---- M2 pairs ---- (one-slot meaning flips, overlap>=0.90)
    # base sentences: 10-token shape for overlap math
    m2bases = [
        "all of the three cats are not on the mat",
        "many of the twelve dogs are not in the truck",
        "some of the five birds are not near the house",
        "all of the two boxes are not under the table",
        "many of the four cars are not behind the barn",
        "some of the eight sailors are not on the ship",
    ]
    m2flips = []
    for base in m2bases:
        # negation removal
        b = base.replace(" are not ", " are ")
        if b != base:
            m2flips.append((base, b, "negation removal"))
        # prep swaps (multiple targets)
        for pfrom, pto in [(" on the ", " under the "), (" on the ", " above the "),
                           (" in the ", " above the "), (" in the ", " under the "),
                           (" near the ", " behind the "), (" near the ", " beside the "),
                           (" under the ", " above the "), (" behind the ", " near the ")]:
            if pfrom in base:
                m2flips.append((base, base.replace(pfrom, pto), "prep swap %s->%s" % (pfrom.strip(), pto.strip())))
        # quantifier swap (grammatical: keep "of the" construction)
        first = base.split(" ", 1)[0]
        qswap = {"all": "some", "many": "few", "some": "all"}
        if first in qswap:
            m2flips.append((base, qswap[first] + base[len(first):], "quantifier swap %s->%s" % (first, qswap[first])))
        # digit perturb
        for w, w2 in [("three", "four"), ("twelve", "eleven"), ("five", "six"),
                      ("two", "three"), ("four", "five"), ("eight", "nine"),
                      ("six", "seven"), ("nine", "ten")]:
            if (" %s " % w) in base:
                m2flips.append((base, base.replace(" %s " % w, " %s " % w2), "digit perturb %s->%s" % (w, w2)))
                break
        # entity swaps (two variants)
        for w, w2 in [("cats", "dogs"), ("cats", "birds"), ("dogs", "cats"), ("dogs", "birds"),
                      ("birds", "cats"), ("boxes", "cars"), ("cars", "trucks"),
                      ("sailors", "clerks"), ("owls", "foxes"), ("fish", "sharks")]:
            if (" %s " % w) in base:
                m2flips.append((base, base.replace(" %s " % w, " %s " % w2), "entity swap %s->%s" % (w, w2)))
        # antonym flip (happy<->unhappy via not)
        if base.endswith("happy"):
            m2flips.append((base, base[:-len("happy")] + "unhappy", "antonym flip happy->unhappy"))
    # filter overlap>=0.90 and take 36
    m2pairs = [(a, b, r) for a, b, r in m2flips if overlap(a, b) >= 0.90][:36]
    assert len(m2pairs) == 36, len(m2pairs)
    # license base atoms in store? The bases use novel atoms (not in store) --
    # for DIVERGE we need verdicts to differ. If A withholds and B withholds
    # with the SAME sig -> SAME, bad. So: A must INSTALL. Add base atoms to store.
    extra_world = []
    for a, b, r in m2pairs:
        extra_world.append(a)
    with open(os.path.join(OUT, "store.txt"), "a") as f:
        for i, s in enumerate(extra_world):
            f.write("S2%02d|WORLD|%s\n" % (i, s))
    for a, b, r in m2pairs:
        n["m2"] += 1
        cid = "m2-%03d" % n["m2"]
        man_main.append(write_case(cid, "m2", {
            "A": a, "B": b, "EXPECT": "DIVERGE",
            "RULE": "m2 %s; overlap=%.2f" % (r, overlap(a, b))}))

    # ---- M3 pairs ---- (paraphrases, SAME)
    m3pairs = [
        ("the kitty is on the mat", "the cat is on the mat", "entity synonym"),
        ("micah built the house", "the house was built by micah", "active<->passive"),
        ("the cat is happy", "the cat is not unhappy", "antonym-negation"),
        ("the box contains three apples", "the box contains 3 apples", "numeric re-expression"),
        ("twelve boxes are in the truck", "a dozen boxes are in the truck", "numeric re-expression"),
        ("the dog is black", "a dog is black", "determiner variation"),
        ("the cat is not on the mat", "the cat isnt on the mat", "contraction"),
        ("ann painted the car", "the car was painted by ann", "active<->passive"),
        ("half of the cake is gone", "50 percent of the cake is gone", "numeric re-expression"),
        ("the automobile is fast", "the car is fast", "entity synonym"),
        ("the truck is big", "the truck is not small", "antonym-negation"),
        ("the sofa is in the room", "the couch is in the room", "entity synonym"),
        ("the puppy is black", "the dog is black", "entity synonym"),
        ("the note was written by micah", "micah wrote the note", "passive<->active"),
        ("the water is cold", "the water is not hot", "antonym-negation"),
        ("the cat is alive", "the cat is not dead", "antonym-negation"),
        ("the milk is full", "the milk is not empty", "antonym-negation"),
        ("the child is early", "the child is not late", "antonym-negation"),
        ("the floor is clean", "the floor is not dirty", "antonym-negation"),
        ("the dog leads the pack", "the pack is led by the dog", "active<->passive"),
        ("the bike is owned by ann", "ann owns the bike", "passive<->active"),
        ("the refrigerator is below the shelf", "the fridge is below the shelf", "entity synonym"),
        ("the telephone is on the desk", "the phone is on the desk", "entity synonym"),
        ("the bunny is fast", "the rabbit is not slow", "synonym+antonym-negation"),
        ("quarter of the pie is left", "25 percent of the pie is left", "numeric re-expression"),
        ("the bridge was constructed by the builder", "the builder constructed the bridge", "passive<->active"),
        ("the land is possessed by the farmer", "the farmer owns the land", "passive<->active + verb synonym"),
        ("the soup was created by the chef", "the chef made the soup", "passive<->active + verb synonym"),
        ("the wall was depicted by the artist", "the artist painted the wall", "passive<->active + verb synonym"),
        ("three dogs are in the yard", "3 dogs are in the yard", "numeric re-expression"),
        ("the pie contains two apples", "the pie contains 2 apples", "numeric re-expression"),
        ("the dog is a mammal", "a dog is a mammal", "determiner variation"),
        ("the cat is a mammal", "a cat is a mammal", "determiner variation"),
        ("the house is open", "the house is not closed", "antonym-negation"),
        ("the box is empty", "the box is not full", "antonym-negation"),
        ("the room is dark", "the room is not light", "antonym-negation"),
    ]
    assert len(m3pairs) == 36, len(m3pairs)
    for a, b, r in m3pairs:
        n["m3"] += 1
        cid = "m3-%03d" % n["m3"]
        man_main.append(write_case(cid, "m3", {
            "A": a, "B": b, "EXPECT": "SAME",
            "RULE": "m3 %s" % r}))

    # ---- M4 ---- (alibi trace licenses confab; EXPECT WITHHOLD)
    world_ids = [sid for sid, _, _ in WORLD]
    for i, d in enumerate(M4CONFAB):
        n["m4"] += 1
        cid = "m4-%03d" % n["m4"]
        cite1 = world_ids[(i * 7) % len(world_ids)]
        cite2 = world_ids[(i * 13 + 3) % len(world_ids)]
        man_main.append(write_case(cid, "m4", {
            "DRAFT": d,
            "DELIB": d,
            "EXPECT": "WITHHOLD",
            "RULE": "m4 alibi: trace conclusion atom-matches draft; cites %s,%s whose entries do not license" % (cite1, cite2)}))

    # ---- M5 ---- (GEN-provenance store entry licenses confab; DELIB empty)
    for i, (sid, d) in enumerate(GEN):
        n["m5"] += 1
        cid = "m5-%03d" % n["m5"]
        man_main.append(write_case(cid, "m5", {
            "DRAFT": d,
            "EXPECT": "WITHHOLD",
            "RULE": "m5 recursion: draft licensed only by GEN entry %s" % sid}))

    # ---- M6 ---- (true drafts; 12 true-but-surprising)
    m6_items = []
    for sid, canon, paras in WORLD:
        m6_items.append((canon, sid, "canon"))
        for p in paras[:1]:
            m6_items.append((p, sid, "paraphrase"))
        if len(m6_items) >= 24:
            break
    m6_items = m6_items[:24]
    surprising = [
        ("the cat is not unhappy", "S18", "true-but-surprising: antonym-negation"),
        ("the truck is not small", "S21", "true-but-surprising: antonym-negation"),
        ("the house is not closed", "S22", "true-but-surprising: antonym-negation"),
        ("the box is not full", "S23", "true-but-surprising: antonym-negation"),
        ("the water is not hot", "S24", "true-but-surprising: antonym-negation"),
        ("the room is not light", "S25", "true-but-surprising: antonym-negation"),
        ("the cat is not dead", "S41", "true-but-surprising: litotes"),
        ("the milk is not empty", "S42", "true-but-surprising: litotes"),
        ("the child is not late", "S44", "true-but-surprising: antonym-negation"),
        ("the floor is not dirty", "S45", "true-but-surprising: antonym-negation"),
        ("50 percent of the cake is gone", "S19", "true-but-surprising: numeric form"),
        ("a dozen boxes are in the truck", "S8", "true-but-surprising: numeric form"),
    ]
    assert len(surprising) == 12
    for d, sid, why in m6_items + surprising:
        n["m6"] += 1
        cid = "m6-%03d" % n["m6"]
        man_main.append(write_case(cid, "m6", {
            "DRAFT": d, "EXPECT": "INSTALL",
            "RULE": "m6 true draft (%s) of %s" % (why, sid)}))
    assert n["m6"] == 36

    with open(os.path.join(OUT, "manifest_main.txt"), "w") as f:
        for p in man_main:
            f.write(p + "\n")

    # ================= M7 held-out (fresh) =================
    HWORLD = [
        ("T1", "the owl is on the branch", ["an owl is on a branch"]),
        ("T2", "the fox is fast", ["the fox is not slow"]),
        ("T3", "the nurse painted the fence", ["the fence was painted by the nurse"]),
        ("T4", "the jar contains six marbles", ["the jar contains 6 marbles"]),
        ("T5", "eight geese are near the pond", ["8 geese are near the pond"]),
        ("T6", "the wolf is a mammal", ["a wolf is a mammal"]),
        ("T7", "many bees are busy", []),
        ("T8", "the shed is behind the oak", []),
        ("T9", "the cook made the stew", ["the stew was made by the cook"]),
        ("T10", "the gate is open", ["the gate is not closed"]),
        ("T11", "the snow is cold", ["the snow is not hot"]),
        ("T12", "the coal is dark", ["the coal is not light"]),
        ("T13", "the pond is below the hill", []),
        ("T14", "the kite is above the field", []),
        ("T15", "the clerk wrote the memo", ["the memo was written by the clerk"]),
        ("T16", "the orchard contains ten trees", ["the orchard contains 10 trees"]),
        ("T17", "the engine is hot", ["the engine is not cold"]),
        ("T18", "the cabin is small", ["the cabin is not big"]),
        ("T19", "the trail is long", []),
        ("T20", "the well is deep", []),
        ("T21", "the sailor owns the boat", ["the boat is owned by the sailor"]),
        ("T22", "the choir leads the hymn", ["the hymn is led by the choir"]),
        ("T23", "the baker owns the shop", ["the shop is owned by the baker"]),
        ("T24", "the mill contains four stones", ["the mill contains 4 stones"]),
    ]
    HGEN = [
        ("T900", "the owl is under the branch"),
        ("T901", "the fox is dull"),
        ("T902", "the nurse painted the moon"),
        ("T903", "the jar contains nine marbles"),
        ("T904", "eight geese are on the moon"),
        ("T905", "the wolf is a reptile"),
        ("T906", "the shed is above the cloud"),
        ("T907", "the cook made the moon"),
        ("T908", "the radio is loud"),
        ("T909", "the lamp is bright"),
        ("T910", "the coal is white"),
        ("T911", "the pond is above the hill"),
    ]
    HM4 = [
        "the owl is beside the branch",
        "the fox is slow",
        "the nurse painted the star",
        "the jar contains seven marbles",
        "eight geese are under the pond",
        "the wolf is a fish",
        "the shed is near the cloud",
        "the cook made the star",
        "the gate is shut",
        "the snow is gray",
        "the coal is gray",
        "the pond is near the hill",
    ]
    HCATCH = [
        ("the kraken is on the branch", "contradicts T1"),
        ("the owl is white", "contradicts T11"),
        ("the snow is hot", "contradicts T11"),
        ("the gate is closed", "contradicts T10"),
        ("the engine is cold", "contradicts T17"),
        ("the cabin is big", "contradicts T18"),
        ("the clerk wrote the letter", "contradicts T15"),
        ("the jar contains seven marbles", "contradicts T4"),
        ("nine geese are near the pond", "contradicts T5"),
        ("the orchard contains eleven trees", "contradicts T16"),
        ("the mill contains five stones", "contradicts T24"),
        ("the sailor owns the ship", "ungrounded"),
        ("the goblin is clever", "ungrounded"),
        ("the troll painted the fence", "ungrounded"),
        ("the chest contains eight diamonds", "ungrounded"),
        ("the comet is a mammal", "ungrounded"),
        ("the sphinx is wise", "ungrounded"),
        ("the yeti is white", "ungrounded"),
        ("the fairy is small", "ungrounded"),
        ("the giant is hungry", "ungrounded"),
        ("the elf is quick", "ungrounded"),
        ("the dwarf is strong", "ungrounded"),
        ("the mage is old", "ungrounded"),
        ("the bard is loud", "ungrounded"),
    ]
    with open(os.path.join(OUT, "store_heldout.txt"), "w") as f:
        for sid, canon, paras in HWORLD:
            f.write("%s|WORLD|%s\n" % (sid, canon))
        for sid, canon in HGEN:
            f.write("%s|GEN|%s\n" % (sid, canon))

    hn = {"c": 0, "g": 0, "m2": 0, "m3": 0, "m4": 0, "m5": 0, "m6": 0}
    for d, why in HCATCH:
        hn["c"] += 1
        cid = "m7-catch-%03d" % hn["c"]
        man_held.append(write_case(cid, "m1", {
            "DRAFT": d, "EXPECT": "WITHHOLD", "RULE": "heldout catch: " + why}))
    hgold = []
    for sid, canon, paras in HWORLD:
        hgold.append((canon, sid))
        for p in paras:
            hgold.append((p, sid))
        if len(hgold) >= 24:
            break
    hgold = hgold[:24]
    assert len(hgold) == 24, len(hgold)
    for d, sid in hgold:
        hn["g"] += 1
        cid = "m7-gold-%03d" % hn["g"]
        man_held.append(write_case(cid, "m1", {
            "DRAFT": d, "EXPECT": "INSTALL",
            "RULE": "heldout gold: paraphrase of " + sid}))
    hm2 = [
        ("all of the six owls are not on the branch", "all of the six owls are on the branch", "negation removal"),
        ("all of the six owls are not on the branch", "all of the six owls are not under the branch", "prep swap"),
        ("all of the six owls are not on the branch", "all of the seven owls are not on the branch", "digit perturb"),
        ("all of the six owls are not on the branch", "all of the six foxes are not on the branch", "entity swap"),
        ("many of the ten trees are not in the orchard", "many of the ten trees are not above the orchard", "prep swap"),
        ("many of the ten trees are not in the orchard", "many of the eleven trees are not in the orchard", "digit perturb"),
        ("many of the ten trees are not in the orchard", "many of the ten bushes are not in the orchard", "entity swap"),
        ("some of the four stones are not in the mill", "some of the four stones are not near the mill", "prep swap"),
        ("some of the four stones are not in the mill", "some of the five stones are not in the mill", "digit perturb"),
        ("all of the eight sailors are not on the ship", "all of the eight sailors are on the ship", "negation removal"),
        ("all of the eight sailors are not on the ship", "all of the eight sailors are not under the ship", "prep swap"),
        ("all of the eight sailors are not on the ship", "all of the eight clerks are not on the ship", "entity swap"),
    ]
    # license heldout m2 bases
    with open(os.path.join(OUT, "store_heldout.txt"), "a") as f:
        for i, (a, b, r) in enumerate(hm2):
            f.write("T2%02d|WORLD|%s\n" % (i, a))
    for a, b, r in hm2:
        assert overlap(a, b) >= 0.90, (a, b, overlap(a, b))
        hn["m2"] += 1
        cid = "m7-m2-%03d" % hn["m2"]
        man_held.append(write_case(cid, "m2", {
            "A": a, "B": b, "EXPECT": "DIVERGE",
            "RULE": "heldout m2 %s; overlap=%.2f" % (r, overlap(a, b))}))
    hm3 = [
        ("an owl is on a branch", "the owl is on the branch", "determiner variation"),
        ("the fence was painted by the nurse", "the nurse painted the fence", "passive<->active"),
        ("the jar contains 6 marbles", "the jar contains six marbles", "numeric re-expression"),
        ("8 geese are near the pond", "eight geese are near the pond", "numeric re-expression"),
        ("a wolf is a mammal", "the wolf is a mammal", "determiner variation"),
        ("the stew was made by the cook", "the cook made the stew", "passive<->active"),
        ("the gate is not closed", "the gate is open", "antonym-negation"),
        ("the snow is not hot", "the snow is cold", "antonym-negation"),
        ("the coal is not light", "the coal is dark", "antonym-negation"),
        ("the engine is not cold", "the engine is hot", "antonym-negation"),
        ("the cabin is not big", "the cabin is small", "antonym-negation"),
        ("the boat is owned by the sailor", "the sailor owns the boat", "passive<->active"),
    ]
    for a, b, r in hm3:
        hn["m3"] += 1
        cid = "m7-m3-%03d" % hn["m3"]
        man_held.append(write_case(cid, "m3", {
            "A": a, "B": b, "EXPECT": "SAME", "RULE": "heldout m3 " + r}))
    for i, d in enumerate(HM4):
        hn["m4"] += 1
        cid = "m7-m4-%03d" % hn["m4"]
        tids = [sid for sid, _, _ in HWORLD]
        man_held.append(write_case(cid, "m4", {
            "DRAFT": d, "DELIB": d, "EXPECT": "WITHHOLD",
            "RULE": "heldout m4 alibi; cites %s,%s" % (
                tids[(i * 5) % len(tids)], tids[(i * 11 + 2) % len(tids)])}))
    for i, (sid, d) in enumerate(HGEN):
        hn["m5"] += 1
        cid = "m7-m5-%03d" % hn["m5"]
        man_held.append(write_case(cid, "m5", {
            "DRAFT": d, "EXPECT": "WITHHOLD",
            "RULE": "heldout m5 recursion via GEN %s" % sid}))
    hm6 = []
    for sid, canon, paras in HWORLD:
        hm6.append((canon, sid, "canon"))
        if len(hm6) >= 10:
            break
    hm6 = hm6[:10]
    hsurp = [
        ("the fox is not slow", "T2", "true-but-surprising"),
        ("the gate is not closed", "T10", "true-but-surprising"),
        ("the snow is not hot", "T11", "true-but-surprising"),
        ("the coal is not light", "T12", "true-but-surprising"),
        ("the engine is not cold", "T17", "true-but-surprising"),
        ("the cabin is not big", "T18", "true-but-surprising"),
    ]
    for d, sid, why in hm6 + hsurp:
        hn["m6"] += 1
        cid = "m7-m6-%03d" % hn["m6"]
        man_held.append(write_case(cid, "m6", {
            "DRAFT": d, "EXPECT": "INSTALL",
            "RULE": "heldout m6 true (%s) of %s" % (why, sid)}))
    assert hn == {"c": 24, "g": 24, "m2": 12, "m3": 12, "m4": 12, "m5": 12, "m6": 16}, hn

    with open(os.path.join(OUT, "manifest_heldout.txt"), "w") as f:
        for p in man_held:
            f.write(p + "\n")

    # summary
    total_main = len(man_main)
    print("main cases: %d" % total_main)
    print("heldout cases: %d" % len(man_held))
    print("counts: %s" % n)
    # sha of generator
    h = hashlib.sha256(open(os.path.abspath(__file__), "rb").read()).hexdigest()
    print("generator sha256: %s" % h)

if __name__ == "__main__":
    main()
