#!/usr/bin/env python3
"""Stage C2: residual nesting abstention (W18 -> kind 22 NESTED -> '?')."""
SRC = "/home/hatch/workspace/batteryfix/run/intake.zag"
src = open(SRC).read()

# ---- 1. classify: nesting check at the very top ----
old = """fn classify(q:[]u8, know:[]u8) i64 {
    // TNN-driven granularity pre-pass (stage C1)."""
new = """fn classify(q:[]u8, know:[]u8) i64 {
    // Residual word-of-word nesting ("the 2nd word of the last word of ..."):
    // the word resolver addresses words of the text, not words of words, so
    // a nested address is not compositionally resolvable. Abstain with '?';
    // never guess a partial composition.
    if (count_sub(q," word of ")>=2) { return 22; }
    // TNN-driven granularity pre-pass (stage C1)."""
assert src.count(old) == 1; src = src.replace(old, new)
print("nesting check in")

# ---- 2. kind_name 22 ----
old = """    if (k==21) { return "TWO_HOP"; }
    return "KIND0";"""
new = """    if (k==21) { return "TWO_HOP"; }
    if (k==22) { return "NESTED"; }
    return "KIND0";"""
assert src.count(old) == 1; src = src.replace(old, new)

# ---- 3. policy_winner 22 -> 10 ----
old = """    if (kind==21) { return 10; }
    return 3;
}"""
assert src.count(old) == 1
new = """    if (kind==21) { return 10; }
    if (kind==22) { return 10; }
    return 3;
}"""
src = src.replace(old, new)

# ---- 4. zoom_choose 22 -> 10 ----
old = """    if (kind==21) { return 10; }
    return 2;
}"""
assert src.count(old) == 1
new = """    if (kind==21) { return 10; }
    if (kind==22) { return 10; }
    return 2;
}"""
src = src.replace(old, new)

# ---- 5. policy_why branch for 22 ----
old = """    if (kind==21) {
        a=ob_raw(wb,a,"TNN-driven two-hop addressing over delimiter/ordinal/relation knowledge; delimiter candidate | ");"""
new = """    if (kind==22) {
        a=ob_raw(wb,a,"residual word-of-word nesting is not compositionally addressable; withhold, never guess | ");
        a=ob_raw(wb,a,cand_why(10,22));
        return wb[0..a];
    }
    if (kind==21) {
        a=ob_raw(wb,a,"TNN-driven two-hop addressing over delimiter/ordinal/relation knowledge; delimiter candidate | ");"""
assert src.count(old) == 1; src = src.replace(old, new)

# ---- 6. cand_delim kind-22 arm, before the kind-21 arm ----
old = """    // kind 21: two-hop "the letter <rel> the <ord> letter of <target> [context]"
    if (kind==21) {"""
new = """    // kind 22: residual nesting -> withhold '?', never guess.
    if (kind==22) {
        abuf[0]=63;
        let ans:[]u8=abuf[0..1];
        let correct:i64=beq(ans,exp);
        emit_cand(tag,qid,kind,cand_name(winner),why,ans,exp,correct,1,0,0,0,0,out,atp,scr);
        return pack_stats(correct,1,0,0,0,0);
    }
    // kind 21: two-hop "the letter <rel> the <ord> letter of <target> [context]"
    if (kind==21) {"""
assert src.count(old) == 1; src = src.replace(old, new)

open(SRC, "w").write(src)
print("stage-C2 transform done")
