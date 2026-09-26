#!/usr/bin/env python3
"""Generate the five per-arm red-team drivers from price_rt_template.zag.

Each arm differs ONLY in the baked-in ST_PRICE_* constant (one line).
Generating (not transcribing) avoids spec drift between arms.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ARMS = {
    # arm: (baked-in ST_PRICE_* constant, scheme-hook code or "")
    "a": ("ST_PRICE_HIGHWATER", ""),   # A: high-water control, ceil(HW/25)
    "b": ("ST_PRICE_FLAT", ""),        # B: flat price, always 2 cites
    "c": ("ST_PRICE_FELT", "SCHEME"),  # C: variable, two deterministic schemes
    "d": ("ST_PRICE_ZERO", ""),        # D: zero-cost, price = 0 cites
}
# The C arm's second op: SCHEME<1|2> selects which deterministic variable
# pricing scheme is active (default 1 = declared-importance tiers).
SCHEME_CODE = """    } else if(rt_match(tok,pi,83,67,72,69,6)==1){
        // SCHEME<1|2> (C arm only): 1 = declared-importance tiers (FELT),
        // 2 = memory age in ledger ticks (RECENCY). Deterministic switch.
        if(v==2){st_set_price_mode(s,ST_PRICE_RECENCY);} else {st_set_price_mode(s,ST_PRICE_FELT);}
        rc=0;
"""

with open(os.path.join(HERE, "price_rt_template.zag")) as f:
    tpl = f.read()

assert tpl.count("ST_PRICE___ARM___") == 1, "template price placeholder changed"
assert tpl.count("__SCHEME_HOOK__") == 1, "template scheme placeholder changed"
for arm, (const, hook) in ARMS.items():
    out = tpl.replace("ST_PRICE___ARM___", const)
    out = out.replace("__SCHEME_HOOK__", SCHEME_CODE if hook == "SCHEME" else "")
    path = os.path.join(HERE, f"price_rt_{arm}.zag")
    with open(path, "w") as f:
        f.write(out)
    print(f"wrote {path} ({const})")
