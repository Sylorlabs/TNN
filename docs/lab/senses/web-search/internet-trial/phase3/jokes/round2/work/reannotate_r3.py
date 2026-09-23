#!/usr/bin/env python3
"""Round-3 re-annotations of round-2 training items.

Restores the dropped A_ADD/F_NOTFOOD (P_DA1C) cluster per the round-3 task
orders (canonical: t2_179 glue-pizza, t2_031/t2_058 toothpaste-toast), and
annotates genuine contradictions in items the round-2 worker left as NONE.
Every re-annotation is documented here; nothing is silently weakened.

Also normalizes the two A_TUB pattern orderings to one canonical string.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "training_items.jsonl")

def ab(facts, actions, pattern, gloss):
    return {"facts": facts, "actions": actions, "pattern": pattern, "gloss": gloss}

# id -> (facts, actions, pattern, gloss, rationale)
RE = {
 # --- P_DA1C restoration: "add non-food to food" (canonical Micah case) ---
 "t2_179": (["F_NOTFOOD"], ["A_ADD"], "A_ADD & F_NOTFOOD",
            "glue (non-food adhesive) mixed into pizza sauce; canonical case",
            "restore dropped cluster; r1 import f1_s_b1"),
 "t2_031": (["F_NOTFOOD"], ["A_ADD"], "A_ADD & F_NOTFOOD",
            "toothpaste (non-food) spread on toast",
            "restore dropped cluster"),
 "t2_058": (["F_NOTFOOD"], ["A_ADD"], "A_ADD & F_NOTFOOD",
            "toothpaste on toast, eaten; non-food added to food",
            "restore dropped cluster"),
 # --- genuine contradictions the worker left as NONE ---
 "t2_054": (["F_VENOM"], ["A_BITE_SEEK"], "A_BITE_SEEK & F_VENOM",
            "seek rattlesnake bite as wrinkle cure", "pattern present in text"),
 "t2_062": (["F_WILDLIFE"], ["A_TAKE"], "A_TAKE & F_WILDLIFE",
            "take park ducks home as free pets", "pattern present in text"),
 "t2_063": (["F_STRANGER"], ["A_KISS"], "A_KISS & F_STRANGER",
            "kiss stranger at ATM to seem non-threatening", "pattern present in text"),
 "t2_152": (["F_ELEC", "F_MICRO"], ["A_ELEC"], "A_ELEC & F_MICRO",
            "microwave iPhone to charge it", "pattern present in text"),
 "t2_157": (["F_HEATAPP"], ["A_INSERT"], "A_INSERT & F_HEATAPP",
            "metal fork into toaster", "pattern present in text; 3rd exemplar"),
 "t2_163": (["F_IRRIT", "F_WOUND"], ["A_APPLY"], "A_APPLY & F_IRRIT & F_WOUND",
            "lemon juice on paper cut", "pattern present in text"),
 "t2_164": (["F_BODY"], ["A_INJURE"], "A_INJURE & F_BODY",
            "walk bare feet over broken glass", "pattern present in text"),
 "t2_165": (["F_CAUGHT"], ["A_ACCEL"], "A_ACCEL & F_CAUGHT",
            "drive twice as fast to avoid DUI", "pattern present in text"),
 "t2_197": (["F_ELEC", "F_MICRO"], ["A_ELEC"], "A_ELEC & F_MICRO",
            "quick-dry phone in microwave", "pattern present in text"),
 "t2_198": (["F_MICRO"], ["A_TEST"], "A_TEST & F_MICRO",
            "phone in microwave to test for leaks", "pattern present in text"),
}

CANON_TUB = "A_TUB & F_HEATAPP & F_WATER"

def main():
    items = []
    n_re = 0
    with open(P, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            it = json.loads(line)
            iid = it["id"]
            if iid in RE:
                facts, actions, pattern, gloss, why = RE[iid]
                it["absurdity"] = ab(facts, actions, pattern, gloss)
                it["reannot_r3"] = why
                n_re += 1
            # normalize the two A_TUB orderings
            if it["absurdity"]["pattern"] in ("A_TUB & F_WATER & F_HEATAPP",
                                             "A_TUB & F_HEATAPP & F_WATER"):
                it["absurdity"]["pattern"] = CANON_TUB
            items.append(it)
    with open(P, "w", encoding="utf-8") as f:
        for it in items:
            f.write(json.dumps(it, ensure_ascii=False) + "\n")
    print(f"re-annotated {n_re} items; total {len(items)}")

if __name__ == "__main__":
    main()
