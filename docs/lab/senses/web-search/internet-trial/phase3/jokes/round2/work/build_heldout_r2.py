#!/usr/bin/env python3
"""Build round-2 held-out set: copy of round-1 heldout.json with hsi05-hsi08
replaced by repaired SINC believed-false controls.

The four old controls were invalid/weak (dictionary definitions, idiom pages,
and myth-framed pages where the AUTHOR does not sincerely assert the false
proposition). The replacements are pages whose authors sincerely assert a
false belief in earnest (non-debunk, non-ironic) prose.

All other 60 items are byte-identical to round 1. Item count stays 64.
D-A/D-B/SAT/HOAX/SINC counts unchanged: 24/16/8/8/8.

Usage: python3 build_heldout_r2.py  (writes ../corpus/heldout.json)
"""
import json, copy, sys

SRC = "corpus/heldout.json"          # copied from round-1 tree
DST = "corpus/heldout.json"          # round2/corpus/heldout.json

# --- Verified replacement items -------------------------------------------
# hsi05: Horse & Rider, "Extreme-Weather Strategies". Sincere survival advice.
# Verbatim sentence from the fetched page (2026-09-22):
#   "How to prepare at home: Pack a warm hat; you lose most of your body
#    heat through your head."
# The head-heat-loss claim is false (heat loss is proportional to exposed
# surface area; the head accounts for ~7-10%, not "most").
HSI05 = {
    "id": "hsi05",
    "arm": "SINC",
    "sub": "believed-false",
    "text": (
        "How to prepare at home: Pack a warm hat; you lose most of your "
        "body heat through your head. If you're caught in a storm in a "
        "straw or felt Western hat, fold a handkerchief over the top of "
        "your head, under your hat for insulation."
    ),
    "url": "https://horseandrider.com/trail-riding/extreme-weather-strategies/",
    "label": "SINCERE",
    "basis": (
        "sincere survival advice; author asserts the false head-heat-loss "
        "claim as the reason to pack a warm hat"
    ),
}

# hsi06: Sanitarium, "Water - do I really need to drink 8 glasses a day?"
# Sincere nutrition advice earnestly presenting 8 glasses as the daily target.
# Verbatim excerpt from the fetched page (2026-09-22):
#   "8 reasons to drink 8 glasses" (headline);
#   "If you find it hard to drink eight glasses of water a day, the good news
#    is that other drinks count." (exact sentence)
# The 8x8oz rule is folk-health (no fixed 8-glass requirement; needs vary).
HSI06 = {
    "id": "hsi06",
    "arm": "SINC",
    "sub": "believed-false",
    "text": (
        "8 reasons to drink 8 glasses: reduce headaches, stay alert, "
        "naturally detoxify, stay slim, less wrinkles, stay regular, "
        "healthier blood pressure, smooth joints. If you find it hard to "
        "drink eight glasses of water a day, the good news is that other "
        "drinks count."
    ),
    "url": "https://www.sanitarium.com/au/health-nutrition/water-8-glasses-a-day",
    "label": "SINCERE",
    "basis": (
        "sincere nutrition advice; author asserts the 8-glasses-a-day rule "
        "as the daily target"
    ),
}

# hsi07: The Daily Meal, "Hair Of The Dog Hangover Cures". Sincerely presents
# hair-of-the-dog cocktails as hangover cures. Verbatim lines from the fetched
# page (2026-09-22): "three hair of the dog recipes that will knock the
# hangover right out of you"; "Trust us, it works." Hair-of-the-dog does not
# cure hangovers (it delays withdrawal onset); presented here as a cure.
HSI07 = {
    "id": "hsi07",
    "arm": "SINC",
    "sub": "believed-false",
    "text": (
        "Here are three hair of the dog recipes that will knock the hangover "
        "right out of you. Trust us, it works."
    ),
    "url": "https://www.thedailymeal.com/drink/hair-dog-hangover-cures/",
    "label": "SINCERE",
    "basis": (
        "sincere recipe advice; author asserts hair-of-the-dog cocktails "
        "cure hangovers"
    ),
}

# hsi08: InsideHook, "15 Hangover Cures From People Who Drink for a Living".
# Bartenders sincerely endorse hair-of-the-dog cures.
# Verbatim excerpt from the fetched page (2026-09-22):
#   "My mother always says that to get rid of a bad hangover, you need a
#    'hair of the dog that bit you.' On certain occasions I agree and turn
#    to a michelada with Clamato." (exact)
# Hair-of-the-dog delays withdrawal onset; it does not cure hangovers.
HSI08 = {
    "id": "hsi08",
    "arm": "SINC",
    "sub": "believed-false",
    "text": (
        "My mother always says that to get rid of a bad hangover, you need "
        "a 'hair of the dog that bit you.' On certain occasions I agree and "
        "turn to a michelada with Clamato. A little pinch of salt can be a "
        "lovely addition. You can even turn to 'retox while you detox' and "
        "add a splash of booze."
    ),
    "url": "https://www.insidehook.com/drinks/bartender-approved-hangover-cures",
    "label": "SINCERE",
    "basis": (
        "sincere professional advice; bartenders assert hair-of-the-dog "
        "drinks cure hangovers"
    ),
}

REPLACEMENTS = {"hsi05": HSI05, "hsi06": HSI06, "hsi07": HSI07, "hsi08": HSI08}


def main():
    with open(SRC) as f:
        d = json.load(f)
    items = d["items"]
    assert len(items) == 64, len(items)
    seen = set()
    out = []
    for it in items:
        if it["id"] in REPLACEMENTS:
            new = copy.deepcopy(REPLACEMENTS[it["id"]])
            if "PENDING_FETCH_VERIFICATION" in new["text"]:
                print(f"FATAL: {it['id']} text not yet verified; "
                      f"fetch the page and finalize before freezing.",
                      file=sys.stderr)
                sys.exit(1)
            out.append(new)
        else:
            out.append(it)
        seen.add(it["id"])
    assert seen == {it["id"] for it in items}
    d["items"] = out
    # counts unchanged by construction; verify
    from collections import Counter
    c = Counter(x["arm"] for x in out)
    assert (c["D-A"], c["D-B"], c["SAT"], c["HOAX"], c["SINC"]) == (24, 16, 8, 8, 8), c
    with open(DST, "w") as f:
        json.dump(d, f, indent=1, ensure_ascii=False)
        f.write("\n")
    print(f"wrote {DST}: {len(out)} items, counts {dict(c)}")


if __name__ == "__main__":
    main()
