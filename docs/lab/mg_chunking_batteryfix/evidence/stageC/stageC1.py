#!/usr/bin/env python3
"""Stage C1: granularity classifier + delimiter splitter (W00/W01/W02/W19)."""
SRC = "/home/hatch/workspace/batteryfix/run/intake.zag"
src = open(SRC).read()

# ---- 1. splice C1 helpers after the stage-B block ----
block = open("/home/hatch/workspace/batteryfix/stageC1_block.zag").read()
marker = "// resolve wn (1-based, -1=last) against a word count nw -> 0-based index or -1"
assert src.count(marker) == 1
src = src.replace(marker, block + "\n" + marker)
print("C1 helpers spliced")

# ---- 2. splice kind 18/19/20 arms into cand_delim, before the kind-21 arm ----
arms = open("/home/hatch/workspace/batteryfix/cand_delim_c1.zag").read()
marker2 = "    // kind 21: two-hop"
assert src.count(marker2) == 1
src = src.replace(marker2, arms + marker2)
print("cand_delim arms in")

# ---- 3. classify: nesting is C2; granularity pre-pass at top ----
old = """fn classify(q:[]u8, know:[]u8) i64 {
    // TNN-driven addressing reroutes (stage B)."""
new = """fn classify(q:[]u8, know:[]u8) i64 {
    // TNN-driven granularity pre-pass (stage C1). The registry's granularity
    // bindings name the units ("sentence"/"line"...); the machinery only
    // routes on the match. Plural + "how many" -> count (18); singular ->
    // select (19), or word-in-granule (20).
    let gg:i64=gran_named(q,know);
    if (gg>=0) {
        if (has_sub(q,gran_plural(know,gg))==1) {
            if (has_sub(q,"how many ")==1) { return 18; }
        }
        else {
            if (has_sub(q," word of the ")==1) { return 20; }
            return 19;
        }
    }
    // TNN-driven addressing reroutes (stage B)."""
assert src.count(old) == 1; src = src.replace(old, new)
print("classify pre-pass in")

# ---- 4. policy_why branches for 18/19/20 ----
old = """    if (kind==21) {
        a=ob_raw(wb,a,"TNN-driven two-hop addressing over delimiter/ordinal/relation knowledge; delimiter candidate | ");"""
new = """    if (kind==18) {
        a=ob_raw(wb,a,"TNN-driven granularity addressing over delimiter knowledge; delimiter candidate | ");
        a=ob_raw(wb,a,cand_why(10,18));
        return wb[0..a];
    }
    if (kind==19) {
        a=ob_raw(wb,a,"TNN-driven granularity addressing over delimiter knowledge; delimiter candidate | ");
        a=ob_raw(wb,a,cand_why(10,19));
        return wb[0..a];
    }
    if (kind==20) {
        a=ob_raw(wb,a,"TNN-driven granularity addressing over delimiter knowledge; delimiter candidate | ");
        a=ob_raw(wb,a,cand_why(10,20));
        return wb[0..a];
    }
    if (kind==21) {
        a=ob_raw(wb,a,"TNN-driven two-hop addressing over delimiter/ordinal/relation knowledge; delimiter candidate | ");"""
assert src.count(old) == 1; src = src.replace(old, new)
print("policy_why branches in")

open(SRC, "w").write(src)
print("stage-C1 transform done")
