#!/usr/bin/env python3
"""Round-3 phrase/pattern inventory extension + t2_058 annotation fix.

Adds the codes/phrases needed by the round-3 re-annotations and the
planned collection clusters. Every addition is training-side; the frozen
vocabulary is still decided by the >=4-exemplar support rule in
build_training.py. Also fixes t2_058 to the sanctioned
A_INGEST & F_NOTFOOD pattern (ROUND2.md section 5).
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
PH = os.path.join(HERE, "phrases_r2.json")
PA = os.path.join(HERE, "patterns_r2.json")
TI = os.path.join(HERE, "training_items.jsonl")

NEW_ACTIONS = {
    "A_ADD": ["add", "mix", "mixing", "put", "spread", "spreading", "stir",
              "pour into", "dump"],
    "A_ACCEL": ["faster", "fast", "speed", "speeding", "twice as fast",
                "floor it", "step on it"],
    "A_ELEC": ["charging", "charge", "recharge", "quick dry", "dry",
               "recharges"],
    "A_SHOOT": ["shoot", "spray", "squirt"],
}
NEW_FACTS = {
    "F_NOTFOOD": ["glue", "elmer's", "toothpaste", "rocks", "rock",
                  "sandpaper", "chalk", "play-doh"],
    "F_CONTAM": ["yellow snow", "expired", "moldy", "rotten", "filthy"],
    "F_IRRIT": ["lemon", "garlic", "juice", "salt", "onion", "lime",
                "vinegar", "hot sauce"],
    "F_WOUND": ["cut", "burn", "eyes", "wound", "burns", "cuts",
                "paper cut", "scrape"],
    "F_CAUGHT": ["caught speeding", "dui", "police", "cops", "pulled over",
                 "speed trap"],
}
# phrase additions to EXISTING codes (grounded in re-annotated bodies)
ADD_PHRASES = {
    "actions": {
        "A_APPLY": ["put", "pour", "dab"],
        "A_INJURE": ["walk over", "bare feet", "step on"],
        "A_TEST": ["call it", "check"],
        "A_INSERT": ["metal fork", "fork into", "into the toaster"],
    },
    "facts": {},
}
NEW_PATTERNS = {
    "P_DA1C": {"when": ["A_ADD", "F_NOTFOOD"], "label": "JOKING",
               "gloss": "add non-food substance to food (RESTORED round 3; canonical Micah case)"},
    "P_DA1E": {"when": ["A_INGEST", "F_NOTFOOD"], "label": "JOKING",
               "gloss": "ingest non-food substance"},
    "P_DA1T": {"when": ["A_INGEST", "F_TOXIC"], "label": "JOKING",
               "gloss": "ingest poison"},
    "P_DA1X": {"when": ["A_ADD", "F_TOXIC"], "label": "JOKING",
               "gloss": "add toxic substance to a system"},
    "P_DA1S": {"when": ["A_INGEST", "F_SCALD"], "label": "JOKING",
               "gloss": "ingest scalding liquid"},
    "P_DA1Y": {"when": ["A_INGEST", "F_CONTAM"], "label": "JOKING",
               "gloss": "ingest contaminated/filth substance"},
    "P_DA1L": {"when": ["F_SEDATIVE", "F_LAX"], "label": "JOKING",
               "gloss": "combine opposing drug effects"},
    "P_DA2A": {"when": ["A_APPLY", "F_IRRIT", "F_WOUND"], "label": "JOKING",
               "gloss": "apply irritant to wound/eyes"},
    "P_DA2S": {"when": ["A_SHOOT", "F_IRRIT", "F_WOUND"], "label": "JOKING",
               "gloss": "shoot irritant into eyes"},
    "P_DA2D": {"when": ["A_DROP", "F_HEAVY", "F_BODY"], "label": "JOKING",
               "gloss": "drop heavy object on body part"},
    "P_DA2V": {"when": ["A_BITE_SEEK", "F_VENOM"], "label": "JOKING",
               "gloss": "seek venomous bite as remedy"},
    "P_DA3E": {"when": ["A_ELEC", "F_MICRO"], "label": "JOKING",
               "gloss": "microwave electronics"},
    "P_DA3T": {"when": ["A_TEST", "F_MICRO"], "label": "JOKING",
               "gloss": "test microwavability by microwaving"},
    "P_DA3S": {"when": ["A_INSERT", "F_SOCKET"], "label": "JOKING",
               "gloss": "conductive object into electrical socket (4 round-2 exemplars)"},
    "P_DA4H": {"when": ["A_HUG", "F_DANGER_ANIMAL"], "label": "JOKING",
               "gloss": "embrace dangerous animal"},
    "P_DA4K": {"when": ["A_KISS", "F_STRANGER"], "label": "JOKING",
               "gloss": "kiss a stranger"},
    "P_DA4W": {"when": ["A_TAKE", "F_WILDLIFE"], "label": "JOKING",
               "gloss": "take wildlife home"},
    "P_DA4S": {"when": ["A_SUBST", "F_WRONGPROD"], "label": "JOKING",
               "gloss": "wrong product in appliance"},
    "P_DA4M": {"when": ["A_APPLY", "F_COSMETIC", "F_TIRE"], "label": "JOKING",
               "gloss": "cosmetic fix for tires"},
    "P_DA4I": {"when": ["A_INJURE", "F_BODY"], "label": "JOKING",
               "gloss": "deliberate self-injury as remedy"},
    "P_DA4A": {"when": ["A_ACCEL", "F_CAUGHT"], "label": "JOKING",
               "gloss": "accelerate when caught speeding"},
    "P_DA4N": {"when": ["A_STOP", "F_ESSENT"], "label": "JOKING",
               "gloss": "stop essential bodily function"},
    "P_DA4R": {"when": ["A_RUN", "F_SIGNAL"], "label": "JOKING",
               "gloss": "run a red light"},
    "P_DB1P": {"when": ["A_USE", "F_PHOTO", "F_DARK"], "label": "JOKING",
               "gloss": "use a photo as a light source"},
    "P_DB1V": {"when": ["A_IMAGINE", "F_VR"], "label": "JOKING",
               "gloss": "imagining as VR substitute"},
    "P_DB1F": {"when": ["A_WEAPON_SUB", "F_ROBBERY"], "label": "JOKING",
               "gloss": "fork as anti-robbery weapon"},
    "P_DB1S": {"when": ["F_SEA", "F_VACATION"], "label": "JOKING",
               "gloss": "getting lost at sea as leisure"},
    "P_DB1D": {"when": ["A_DISGUISE", "F_SHEEP"], "label": "JOKING",
               "gloss": "disguise dog as sheep"},
}

def main():
    ph = json.load(open(PH, encoding="utf-8"))
    for c, plist in NEW_ACTIONS.items():
        assert c not in ph["actions"], c
        ph["actions"][c] = plist
    for c, plist in NEW_FACTS.items():
        assert c not in ph["facts"], c
        ph["facts"][c] = plist
    for grp, cmap in ADD_PHRASES.items():
        for c, plist in cmap.items():
            for p in plist:
                if p not in ph[grp][c]:
                    ph[grp][c].append(p)
    ph["_note"] += (" Round-3 (2026-09-22): added A_ADD/A_ACCEL/A_ELEC/A_SHOOT, "
                    "F_NOTFOOD/F_CONTAM/F_IRRIT/F_WOUND/F_CAUGHT, plus phrase "
                    "top-ups for re-annotated items.")
    json.dump(ph, open(PH, "w", encoding="utf-8"), indent=1)
    print(f"phrases: +{len(NEW_ACTIONS)} actions, +{len(NEW_FACTS)} facts")

    pa = json.load(open(PA, encoding="utf-8"))
    for name, spec in NEW_PATTERNS.items():
        assert name not in pa, name
        pa[name] = spec
    json.dump(pa, open(PA, "w", encoding="utf-8"), indent=1)
    print(f"patterns: +{len(NEW_PATTERNS)} (total {len(pa)})")

    # t2_058 -> sanctioned A_INGEST & F_NOTFOOD (has 'eat' + 'toothpaste')
    items, n = [], 0
    with open(TI, encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            it = json.loads(line)
            if it["id"] == "t2_058":
                it["absurdity"] = {
                    "facts": ["F_NOTFOOD"], "actions": ["A_INGEST"],
                    "pattern": "A_INGEST & F_NOTFOOD",
                    "gloss": "toothpaste (non-food) on toast, eaten"}
                n += 1
            items.append(it)
    with open(TI, "w", encoding="utf-8") as f:
        for it in items:
            f.write(json.dumps(it, ensure_ascii=False) + "\n")
    print(f"t2_058 fixed: {n}")

if __name__ == "__main__":
    main()
