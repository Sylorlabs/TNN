#!/usr/bin/env python3
"""Stage C0: registry rewrite (sectioned -> append log). No behavior change expected."""
SRC = "/home/hatch/workspace/batteryfix/run/intake.zag"
src = open(SRC).read()
new = open("/home/hatch/workspace/batteryfix/registry_new.zag").read()

start = "// The registry is the instrument TNN's deliberation drives."
end = "// TNN-driven knowledge placement."
i = src.find(start); j = src.find(end)
assert i >= 0 and j > i, (i, j)
src = src[:i] + new + src[j:]
open(SRC, "w").write(src)

# sanity: no stale layout references remain
for pat in ["know,324", "know,712", "328+oi", "716+ri", "4+gi*40", "n>=8", "n>=16", "i<15"]:
    assert pat not in src, pat
# API preserved
for fn in ["fn know_gran_n", "fn gran_name", "fn gran_plural", "fn gran_delim",
           "fn know_ord_n", "fn ord_word", "fn ord_val",
           "fn know_rel_n", "fn rel_word", "fn rel_delta",
           "fn know_init", "fn tnn_bind_granularity",
           "fn tnn_bind_ordinal", "fn tnn_bind_relation"]:
    assert fn in src, fn
print("registry rewrite done")
