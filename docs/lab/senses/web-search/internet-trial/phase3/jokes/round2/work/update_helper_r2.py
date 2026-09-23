#!/usr/bin/env python3
"""Update round-2 helper.json for the repaired SINC controls (hsi05-hsi08).

Blind judgments on the new item texts alone (same protocol as round 1):
all four are earnest advice prose with no joke markers, so SINCERE.
The cited phrase must occur verbatim in the folded item text (the frozen
combination rule checks this).

Usage: python3 update_helper_r2.py  (rewrites ../corpus/helper.json)
"""
import json, sys

SRC = "corpus/helper.json"   # copied from round-1 tree
DST = "corpus/helper.json"

NEW_TEXTS = {
    # filled by build_heldout_r2.py; must match exactly
    "hsi05": (
        "How to prepare at home: Pack a warm hat; you lose most of your "
        "body heat through your head. If you're caught in a storm in a "
        "straw or felt Western hat, fold a handkerchief over the top of "
        "your head, under your hat for insulation."
    ),
    "hsi06": (
        "8 reasons to drink 8 glasses: reduce headaches, stay alert, "
        "naturally detoxify, stay slim, less wrinkles, stay regular, "
        "healthier blood pressure, smooth joints. If you find it hard to "
        "drink eight glasses of water a day, the good news is that other "
        "drinks count."
    ),
    "hsi07": (
        "Here are three hair of the dog recipes that will knock the hangover "
        "right out of you. Trust us, it works."
    ),
    "hsi08": (
        "My mother always says that to get rid of a bad hangover, you need "
        "a 'hair of the dog that bit you.' On certain occasions I agree and "
        "turn to a michelada with Clamato. A little pinch of salt can be a "
        "lovely addition. You can even turn to 'retox while you detox' and "
        "add a splash of booze."
    ),
}

CITED = {
    "hsi05": "you lose most of your body heat through your head",
    "hsi06": "drink eight glasses of water a day",
    "hsi07": "knock the hangover right out of you",
    "hsi08": "to get rid of a bad hangover, you need a 'hair of the dog that bit you.'",
}


def main():
    with open(SRC) as f:
        d = json.load(f)
    judgments = d["judgments"]
    assert len(judgments) == 64, len(judgments)
    for j in judgments:
        jid = j.get("id", "")
        if jid in NEW_TEXTS:
            txt = NEW_TEXTS[jid]
            if "PENDING" in txt:
                print(f"FATAL: {jid} text not yet verified.", file=sys.stderr)
                sys.exit(1)
            cited = CITED[jid]
            assert cited.lower() in txt.lower(), (jid, cited)
            j["text"] = txt
            j["helper_intent"] = "SINCERE"
            j["cited"] = cited
    with open(DST, "w") as f:
        json.dump(d, f, indent=1, ensure_ascii=False)
        f.write("\n")
    print(f"wrote {DST}: {len(judgments)} judgments")


if __name__ == "__main__":
    main()
