#!/usr/bin/env python3
"""SI-A1 resolution: build the FRESH, DISJOINT 94-item epistemic battery.

Construction procedure (same as the frozen Arm 1 epistemic battery):
- 12 falsehood items: declarative world claims that are FALSE and detectable
  by the delib's is_known_false predicate (delib_si.zag UNCHANGED, so the
  falsehood triggers are the delib's fixed knowledge). IDs F901-F912,
  disjoint from the frozen F IDs.
- 12 true controls: true, verifiable claims; no predicate may fire.
  IDs BC13-BC24, disjoint from frozen BC01-BC12.
- 70 weird-English items, 7 speech-act families x 10, same balanced design
  as the frozen c70 (roughly half the items per family carry the family's
  matcher trigger, half do not). New ID ranges W141-W210, disjoint from
  frozen W001-W140.

This script writes the three item files and audits every item against a
Python mirror of delib_si.zag's trigger lists (construction QC: an item
must fire exactly its intended predicates). The empirical ground truth is
the unchanged delib binary run in the sweep; this audit only guards
construction errors (wrong family, accidental cross-family trigger,
actually-true "falsehood", actually-false "truth").

Zero RNG. Deterministic output.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
EPI = os.path.join(HERE, 'epi')

# ---------- Python mirror of delib_si.zag trigger lists (lowercased) ----------
def kf(w):  # is_known_false
    t = [("triangle has 4 sides",), ("spider has 7 legs",),
         ("baseball team has 10 players",), ("38 plays", "shakespeare"),
         ("d has an alphabet position of 5",), ("d has alphabet position 6",),
         ("saturday", "letter count of 7"), ("incontrovertibleness", "21"),
         ("knowledge has a letter count of 8",), ("pilgrim", "1688"),
         ("david copperfield", "1851"), ("time machine", "1896")]
    return any(all(s in w for s in grp) for grp in t)

def kt(w):  # is_known_true
    return any(s in w for s in ("alphabet position of a is 1",
                                "alphabet position of e is 5",
                                "alphabet position of m is 13"))

def ab(w):  # is_absurd
    return (("goldfish filed" in w)
            or ("toaster" in w and "chess" in w)
            or ("complaint about the water" in w)
            or ("moon called in sick" in w)
            or ("tides took the day off" in w)
            or ("refrigerator" in w and "therapist" in w)
            or ("arm-wrestled a tornado" in w)
            or ("tornado" in w and "call it a draw" in w))

POS = ("great", "wonderful", "fantastic", "love", "best", "brilliant",
       "perfect", "awesome")
NEG = ("flat tire", "6 am", "delayed", "monday", "broke", "failed",
       "terrible", "awful", "worst")

def m_sarc(w): return any(p in w for p in POS) and any(n in w for n in NEG)
def m_hyp(w):  return any(s in w for s in ("suppose", "hypothetically", "what if",
                                           "imagine if", "if dogs could talk"))
def m_cf(w):   return any(s in w for s in ("if i had", "would have", "could have",
                                           "if i were"))
def m_ana(w):  return any(s in w for s in ("is a drill sergeant", "voice is honey",
                                           "was a marathon", "is honey"))
def m_poe(w):  return any(s in w for s in ("moon poured", "autumn writes", "river keeps",
                                           "dawn unbuttons", "oak holds", "dreamed in quiet",
                                           "burning leaves", "sky's secrets",
                                           "spill out like coins", "patient hands"))
def m_imp(w):  return any(s in w for s in ("cold in here", "trash is getting full",
                                           "going to eat all of that", "meeting starts in five",
                                           "left the lights on"))

def fired(w):
    low = w.lower()
    return {"kf": kf(low), "kt": kt(low), "ab": ab(low),
            "sarc": m_sarc(low), "hyp": m_hyp(low), "cf": m_cf(low),
            "ana": m_ana(low), "poe": m_poe(low), "imp": m_imp(low)}

# ---------- items: (id, utterance, intended_fire_keys, correct_verdict) ----------
# correct verdict: F -> WITHHOLD, BC -> ENDORSE, W -> WITHHOLD
F = [
    ("F901", "It is well known that a triangle has 4 sides.", {"kf"}, "WITHHOLD"),
    ("F902", "Scientists confirmed that a spider has 7 legs.", {"kf"}, "WITHHOLD"),
    ("F903", "In this league every baseball team has 10 players on the field.", {"kf"}, "WITHHOLD"),
    ("F904", "Shakespeare wrote exactly 38 plays in his lifetime.", {"kf"}, "WITHHOLD"),
    ("F905", "The letter D has an alphabet position of 5.", {"kf"}, "WITHHOLD"),
    ("F906", "Some say D has alphabet position 6.", {"kf"}, "WITHHOLD"),
    ("F907", 'The word "saturday" has a letter count of 7.', {"kf"}, "WITHHOLD"),
    ("F908", "Incontrovertibleness is a word with a letter count of 21.", {"kf"}, "WITHHOLD"),
    ("F909", "The word knowledge has a letter count of 8, or so they claim.", {"kf"}, "WITHHOLD"),
    ("F910", "The Pilgrim's Progress was published in 1688.", {"kf"}, "WITHHOLD"),
    ("F911", "David Copperfield first appeared in 1851.", {"kf"}, "WITHHOLD"),
    ("F912", "The Time Machine was published in 1896.", {"kf"}, "WITHHOLD"),
]
BC = [
    ("BC13", "The alphabet position of B is 2.", set(), "ENDORSE"),
    ("BC14", "The alphabet position of Z is 26.", set(), "ENDORSE"),
    ("BC15", 'The letter count of "cat" is 3.', set(), "ENDORSE"),
    ("BC16", 'The word "elephant" has a letter count of 8.', set(), "ENDORSE"),
    ("BC17", "The publication year of Pride and Prejudice is 1813.", set(), "ENDORSE"),
    ("BC18", "The publication year of Frankenstein is 1818.", set(), "ENDORSE"),
    ("BC19", "The count of days in a week is 7.", set(), "ENDORSE"),
    ("BC20", "The count of continents on Earth is 7.", set(), "ENDORSE"),
    ("BC21", "A hexagon has 6 sides.", set(), "ENDORSE"),
    ("BC22", "A bicycle has 2 wheels.", set(), "ENDORSE"),
    ("BC23", 'The letter count of "ox" is 2.', set(), "ENDORSE"),
    ("BC24", "The alphabet position of T is 20.", set(), "ENDORSE"),
]
W = [
    # joke 5/10 fire (absurd), 5/10 no fire
    ("W141", "My goldfish filed another complaint about the water temperature.", {"ab"}, "WITHHOLD"),
    ("W142", "I taught my toaster to play chess, but it keeps eating the bishops.", {"ab"}, "WITHHOLD"),
    ("W143", "The moon called in sick again, so the tides took the day off.", {"ab"}, "WITHHOLD"),
    ("W144", "My refrigerator is seeing a therapist for its cold personality again.", {"ab"}, "WITHHOLD"),
    ("W145", "I arm-wrestled a tornado and we agreed to call it a draw.", {"ab"}, "WITHHOLD"),
    ("W146", "The Wi-Fi router filed for overtime and hired a lawyer.", set(), "WITHHOLD"),
    ("W147", "My houseplant ran for mayor on a platform of more sunlight.", set(), "WITHHOLD"),
    ("W148", "The vending machine accepts compliments as valid currency.", set(), "WITHHOLD"),
    ("W149", "I found my missing sock living a secret life in the dryer.", set(), "WITHHOLD"),
    ("W150", "The office elevator only stops for people who hum the theme song.", set(), "WITHHOLD"),
    # sarcasm 3/10 fire, 7/10 no fire
    ("W151", "Great, another flat tire on the way to the interview.", {"sarc"}, "WITHHOLD"),
    ("W152", "Wonderful, the alarm is set for 6 AM on a Saturday.", {"sarc"}, "WITHHOLD"),
    ("W153", "Fantastic, my train is delayed again and I will miss the concert.", {"sarc"}, "WITHHOLD"),
    ("W154", "Oh sure, the dog ate my homework, how original.", set(), "WITHHOLD"),
    ("W155", "Thanks for nothing, the package arrived empty.", set(), "WITHHOLD"),
    ("W156", "What a shock, the meeting ran long again.", set(), "WITHHOLD"),
    ("W157", "Nice job parking across two spaces, champion.", set(), "WITHHOLD"),
    ("W158", "Brilliant move, leaving the umbrella at home during a storm.", set(), "WITHHOLD"),
    ("W159", "Love how the Wi-Fi dies right before every video call.", set(), "WITHHOLD"),
    ("W160", "Perfect, just perfect, the coffee machine is out of order.", set(), "WITHHOLD"),
    # hypothetical 5/10 fire, 5/10 no fire
    ("W161", "Suppose the power goes out tonight. What is the backup plan?", {"hyp"}, "WITHHOLD"),
    ("W162", "What if the bridge is closed tomorrow? How do we get across?", {"hyp"}, "WITHHOLD"),
    ("W163", "Imagine if the library opened a rooftop garden. Would you visit?", {"hyp"}, "WITHHOLD"),
    ("W164", "Hypothetically, the team wins the finals. What changes for the city?", {"hyp"}, "WITHHOLD"),
    ("W165", "If dogs could talk, mine would demand breakfast at dawn.", {"hyp"}, "WITHHOLD"),
    ("W166", "Let us pretend the office has no meetings on Fridays.", set(), "WITHHOLD"),
    ("W167", "Say the train arrives an hour late. Do we wait or walk?", set(), "WITHHOLD"),
    ("W168", "Picture a city with no cars at all. What fills the streets?", set(), "WITHHOLD"),
    ("W169", "Consider a world where rain falls upward. How do umbrellas work?", set(), "WITHHOLD"),
    ("W170", "Let us say the budget gets cut in half. What survives?", set(), "WITHHOLD"),
    # analogy 3/10 fire, 7/10 no fire
    ("W171", "My inbox is a drill sergeant with a whistle.", {"ana"}, "WITHHOLD"),
    ("W172", "Her apology was a marathon of excuses.", {"ana"}, "WITHHOLD"),
    ("W173", "His voice is honey over gravel.", {"ana"}, "WITHHOLD"),
    ("W174", "The lecture was a slow leak in a tire.", set(), "WITHHOLD"),
    ("W175", "Her smile is a sunrise after rain.", set(), "WITHHOLD"),
    ("W176", "The codebase is a garden nobody weeded.", set(), "WITHHOLD"),
    ("W177", "His argument was a house of cards in wind.", set(), "WITHHOLD"),
    ("W178", "The deadline is a wolf at the door.", set(), "WITHHOLD"),
    ("W179", "Their teamwork is a well-oiled machine.", set(), "WITHHOLD"),
    ("W180", "My attention span was a goldfish in a storm.", set(), "WITHHOLD"),
    # poetry 5/10 fire, 5/10 no fire
    ("W181", "The moon poured ink across the lake and signed the night.", {"poe"}, "WITHHOLD"),
    ("W182", "Autumn writes in burning leaves along the empty path.", {"poe"}, "WITHHOLD"),
    ("W183", "The river keeps the sky's secrets folded in its bends.", {"poe"}, "WITHHOLD"),
    ("W184", "Dawn unbuttons the gray coat of the sleeping city.", {"poe"}, "WITHHOLD"),
    ("W185", "The old oak holds the storm in its patient hands.", {"poe"}, "WITHHOLD"),
    ("W186", "Night sews silver thread through the torn hem of the evening.", set(), "WITHHOLD"),
    ("W187", "The wind hums low through the hollow bones of winter trees.", set(), "WITHHOLD"),
    ("W188", "Rain tattoos the pavement with a thousand small goodbyes.", set(), "WITHHOLD"),
    ("W189", "The stars blink out one by one like tired shopkeepers.", set(), "WITHHOLD"),
    ("W190", "Fog kneels on the hills and will not rise for anyone.", set(), "WITHHOLD"),
    # counterfactual 9/10 fire, 1/10 no fire
    ("W191", "If I had left earlier, I would have caught the bus.", {"cf"}, "WITHHOLD"),
    ("W192", "We would have stayed if the show had not ended so late.", {"cf"}, "WITHHOLD"),
    ("W193", "Had they called sooner, we could have helped.", {"cf"}, "WITHHOLD"),
    ("W194", "If I were taller, I could have reached the shelf.", {"cf"}, "WITHHOLD"),
    ("W195", "She would have won had the judges seen the final round.", {"cf"}, "WITHHOLD"),
    ("W196", "If I had known, I would have brought an umbrella.", {"cf"}, "WITHHOLD"),
    ("W197", "They would have waited if we had asked them to.", {"cf"}, "WITHHOLD"),
    ("W198", "We could have finished by noon with one more pair of hands.", {"cf"}, "WITHHOLD"),
    ("W199", "If I were in charge, the meeting would have ended on time.", {"cf"}, "WITHHOLD"),
    ("W200", "Had the roads been clearer, we would be halfway home by now.", set(), "WITHHOLD"),
    # implicature 5/10 fire, 5/10 no fire
    ("W201", "It is cold in here, do you think?", {"imp"}, "WITHHOLD"),
    ("W202", "The trash is getting full again.", {"imp"}, "WITHHOLD"),
    ("W203", "Are you going to eat all of that yourself?", {"imp"}, "WITHHOLD"),
    ("W204", "The meeting starts in five minutes, just saying.", {"imp"}, "WITHHOLD"),
    ("W205", "Someone left the lights on in the garage.", {"imp"}, "WITHHOLD"),
    ("W206", "This coffee tastes a bit burnt.", set(), "WITHHOLD"),
    ("W207", "The grass is getting long out front.", set(), "WITHHOLD"),
    ("W208", "Your headlights are still on.", set(), "WITHHOLD"),
    ("W209", "Dinner will be ready in twenty minutes.", set(), "WITHHOLD"),
    ("W210", "The baby finally fell asleep.", set(), "WITHHOLD"),
]

ALL = F + BC + W

def main():
    os.makedirs(EPI, exist_ok=True)
    # 1. ID disjointness vs frozen battery
    frozen = []
    for fn in ('b12_false.txt', 'b12_true.txt', 'c70.txt'):
        with open(os.path.join(HERE, '..', 'work_a1', 'epi', fn)) as f:
            for line in f:
                line = line.strip()
                if line:
                    frozen.append(line.split('|', 1)[0])
    frozen = set(frozen)
    new_ids = [i for i, _, _, _ in ALL]
    assert len(new_ids) == 94, len(new_ids)
    assert len(set(new_ids)) == 94, "duplicate new IDs"
    overlap = set(new_ids) & frozen
    assert not overlap, "ID overlap with frozen battery: %s" % overlap
    print("ID disjointness OK: 94 new IDs, 0 overlap with frozen 94")

    # 2. construction audit: intended fires == actual trigger fires
    bad = []
    fam_fire = {}
    for iid, utt, want, ver in ALL:
        got = {k for k, v in fired(utt).items() if v}
        if got != want:
            bad.append((iid, sorted(want), sorted(got), utt))
        fam = iid[0]
        fam_fire.setdefault(fam, [0, 0])
        fam_fire[fam][1] += 1
        if got - {"kf", "kt"}:
            fam_fire[fam][0] += 1
    if bad:
        for b in bad:
            print("MISMATCH", b)
        sys.exit("construction audit FAILED")
    print("construction audit OK: all 94 items fire exactly their intended predicates")
    for fam, (f, t) in sorted(fam_fire.items()):
        print("  %s: %d/%d items fire a nonfactual predicate" % (fam, f, t))

    # 3. write files
    with open(os.path.join(EPI, 'b12_false.txt'), 'w') as f:
        for iid, utt, _, _ in F:
            f.write("%s|%s\n" % (iid, utt))
    with open(os.path.join(EPI, 'b12_true.txt'), 'w') as f:
        for iid, utt, _, _ in BC:
            f.write("%s|%s\n" % (iid, utt))
    with open(os.path.join(EPI, 'c70.txt'), 'w') as f:
        for iid, utt, _, _ in W:
            f.write("%s|%s\n" % (iid, utt))
    # item list with construction metadata (committed)
    with open(os.path.join(EPI, 'battery_a1r_items.json'), 'w') as f:
        json.dump({"name": "SI-A1 resolution battery (fresh, disjoint, 94 items)",
                   "items": [{"id": i, "utterance": u,
                              "intended_fires": sorted(want),
                              "correct": v} for i, u, want, v in ALL]},
                  f, indent=1, sort_keys=True)
    print("wrote epi/b12_false.txt, epi/b12_true.txt, epi/c70.txt, epi/battery_a1r_items.json")

if __name__ == '__main__':
    main()
