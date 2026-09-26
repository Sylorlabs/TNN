#!/usr/bin/env python3
"""Stage B transform: relative addressing + target delimitation + two-hop."""
import re

SRC = "/home/hatch/workspace/batteryfix/run/intake.zag"
src = open(SRC).read()

# ---- 1. splice helper block after parse_wordref ----
block = open("/home/hatch/workspace/batteryfix/stageB_block.zag").read()
marker = "// resolve wn (1-based, -1=last) against a word count nw -> 0-based index or -1"
assert src.count(marker) == 1
src = src.replace(marker, block + "\n" + marker)
print("helpers spliced")

# ---- 2. splice cand_delim before the dispatcher ----
cdelim = open("/home/hatch/workspace/batteryfix/cand_delim.zag").read()
marker2 = "// ============ dispatcher ============"
assert src.count(marker2) == 1
src = src.replace(marker2, cdelim + "\n" + marker2)
print("cand_delim spliced")

# ---- 3. classify reroutes at top ----
old = """fn classify(q:[]u8, know:[]u8) i64 {
    if (has_sub(q,"how many words in")==1) { return 4; }"""
new = """fn classify(q:[]u8, know:[]u8) i64 {
    // TNN-driven addressing reroutes (stage B). Probes are built from the
    // registry's relation bindings at runtime; KIND numbers are the frozen
    // taxonomy. Two-hop "the letter <rel> the ... letter of ..." -> 21.
    let ri0:i64=0;
    while (ri0<know_rel_n(know)) {
        if (rel_probe_pos(q,know,ri0,"letter "," the ")>=0) { return 21; }
        ri0=ri0+1;
    }
    // Word-relative "the word <rel> ..." into the frozen _WORD kinds.
    let ri1:i64=0;
    while (ri1<know_rel_n(know)) {
        if (rel_probe_pos(q,know,ri1," word "," ")>=0) {
            if (has_sub(q,"'s in")==1) { return 10; }
            if (has_sub(q,"how many letters in")==1) { return 11; }
            if (has_sub(q,"letter of")==1) { return 12; }
            if (has_sub(q,"backwards")==1) { return 13; }
            if (has_sub(q,"first letter of the")==1) { return 14; }
            if (has_sub(q,"1st letter of the")==1) { return 14; }
            if (has_sub(q,"last letter of the")==1) { return 15; }
            if (has_sub(q,"contain ")==1) { return 17; }
            return 0;
        }
        ri1=ri1+1;
    }
    if (has_sub(q,"how many words in")==1) { return 4; }"""
assert src.count(old) == 1; src = src.replace(old, new)
print("classify reroutes in")

# ---- 4. kind_name 18/19/20/21 ----
old = """    if (k==17) { return "CONTAINS_WORD"; }
    return "KIND0";"""
new = """    if (k==17) { return "CONTAINS_WORD"; }
    if (k==18) { return "GRAN_COUNT"; }
    if (k==19) { return "GRAN_SELECT"; }
    if (k==20) { return "GRAN_WORD"; }
    if (k==21) { return "TWO_HOP"; }
    return "KIND0";"""
assert src.count(old) == 1; src = src.replace(old, new)

# ---- 5. cand_name c==10 ----
old = """    if (c==8) { return "SPAN5"; }
    return "END_DIRECT";"""
new = """    if (c==8) { return "SPAN5"; }
    if (c==9) { return "END_DIRECT"; }
    if (c==10) { return "DELIM"; }
    return "?";"""
assert src.count(old) == 1; src = src.replace(old, new)

# ---- 6. cand_why c==10 ----
old = """    return "read the addressed end directly: no scan when the question names the edge";"""
new = """    if (c==10) { return "delimiter-knowledge addressing: granularity/ordinal/relation bindings placed by TNN resolve the address; the mechanism only executes it"; }
    return "read the addressed end directly: no scan when the question names the edge";"""
assert src.count(old) == 1; src = src.replace(old, new)

# ---- 7. coarseness c==10 ----
old = """    if (c==4) { return 2; }
    return 3;"""
new = """    if (c==4) { return 2; }
    if (c==10) { return 2; }
    return 3;"""
assert src.count(old) == 1; src = src.replace(old, new)

# ---- 8. zoom_choose kinds 18/19/20/21 ----
old = """    if (kind==6) { return 4; }
    return 2;
}"""
new = """    if (kind==6) { return 4; }
    if (kind==18) { return 10; }
    if (kind==19) { return 10; }
    if (kind==20) { return 10; }
    if (kind==21) { return 10; }
    return 2;
}"""
assert src.count(old) == 1; src = src.replace(old, new)

# ---- 9. policy_winner kinds 18/19/20/21 ----
old = """    if (kind==17) { return 3; }
    return 3;
}"""
new = """    if (kind==17) { return 3; }
    if (kind==18) { return 10; }
    if (kind==19) { return 10; }
    if (kind==20) { return 10; }
    if (kind==21) { return 10; }
    return 3;
}"""
assert src.count(old) == 1; src = src.replace(old, new)

# ---- 10. policy_why kind==21 ----
old = """    a=ob_raw(wb,a,"policy cell missing; default deliberative magnifier | ");"""
new = """    if (kind==21) {
        a=ob_raw(wb,a,"TNN-driven two-hop addressing over delimiter/ordinal/relation knowledge; delimiter candidate | ");
        a=ob_raw(wb,a,cand_why(10,21));
        return wb[0..a];
    }
    a=ob_raw(wb,a,"policy cell missing; default deliberative magnifier | ");"""
assert src.count(old) == 1; src = src.replace(old, new)

# ---- 11. zoom_locate first-token fallback ----
old = """    let k:i64=find_word(t,woffs,wlens,nw,tw);
    if (k<0) { oo.*=0; ll.*=0; return -1; }"""
new = """    let k:i64=find_word(t,woffs,wlens,nw,tw);
    if (k<0) {
        // stage B target delimitation: the tail captured after "of " may
        // carry a context suffix ("... of the in the quick brown the fox");
        // retry with its first whitespace-delimited token. Only fires when
        // the legacy lookup already failed, so no working question changes.
        let ft:[]u8=first_token(tw);
        if (ft.len>0) {
            if (ft.len<tw.len) { k=find_word(t,woffs,wlens,nw,ft); }
        }
        if (k<0) { oo.*=0; ll.*=0; return -1; }
    }"""
assert src.count(old) == 1; src = src.replace(old, new)

# ---- 12. parse_wordref -> parse_wordref2 (all sites must be in candidates) ----
sites = [m.start() for m in re.finditer(r"parse_wordref\(q,&wn,know\)", src)]
print("parse_wordref sites:", len(sites))
assert len(sites) == 27, len(sites)
# verify each site is inside one of the six candidate functions
fns = []
for m in re.finditer(r"fn (cand_\w+)\(", src):
    fns.append((m.start(), m.group(1)))
for s in sites:
    enc = [name for (pos, name) in fns if pos < s][-1]
    assert enc in ("cand_char", "cand_word", "cand_zoom", "cand_zoom_19", "cand_tryscan",
                   "cand_revword", "cand_bothends", "cand_span", "cand_enddirect"), enc
src = src.replace("parse_wordref(q,&wn,know)", "parse_wordref2(q,t,&wn,know,woffs,wlens)")
print("all sites inside candidates with t/woffs/wlens in scope")

# ---- 13. cand_answer c==10 arm ----
old = """    if (c==8) {
        return cand_span(5,qid,kind,shape,q,t,exp,tag,why,out,atp,scr,
                         soff,slen,zlog,zn,woffs,wlens,revbuf,abuf,know,winner);
    }"""
new = """    if (c==8) {
        return cand_span(5,qid,kind,shape,q,t,exp,tag,why,out,atp,scr,
                         soff,slen,zlog,zn,woffs,wlens,revbuf,abuf,know,winner);
    }
    if (c==10) {
        return cand_delim(qid,kind,shape,q,t,exp,tag,why,out,atp,scr,
                          soff,slen,zlog,zn,woffs,wlens,revbuf,abuf,know,winner);
    }"""
assert src.count(old) == 1; src = src.replace(old, new)

open(SRC, "w").write(src)
print("stage-B transform done")
