#!/usr/bin/env python3
"""Panic-hardening transform (2026-09-26, PREREG_DEGEN.md).
1. Remove dead cand_span (proven unreachable: policy never emits 7/8).
2. H1: guard cand_zoom kind-7 (nw==0).
3. H2: guard cand_word kind-16 (nw==0).
4. H3: guard cand_word kind-7 (nw==0, defensive).
Writes run/intake.zag in place. Asserts uniqueness of every pattern."""
import sys

P = "/home/hatch/workspace/batteryfix/run/intake.zag"
src = open(P).read()
lines = src.split("\n")
n0 = len(lines)

def need(cond, msg):
    if not cond:
        print(f"ABORT: {msg}")
        sys.exit(1)

# --- 1. remove cand_span: lines 1894..2060 (1-based) ---
need(lines[1893].startswith("// ============ candidates 7/8: SPAN3"),
     "cand_span header not at 1894")
need(lines[2059] == "", "line 2060 not blank")
need(lines[2060].startswith("// ============ candidate 9:"),
     "candidate 9 comment not at 2061")
del lines[1893:2060]
src = "\n".join(lines)
need("fn cand_span(" not in src, "cand_span fn still present")

# --- 2. remove c==7 / c==8 dispatch branches ---
dispatch = """    if (c==7) {
        return cand_span(3,qid,kind,shape,q,t,exp,tag,why,out,atp,scr,
                         soff,slen,zlog,zn,woffs,wlens,revbuf,abuf,know,winner);
    }
    if (c==8) {
        return cand_span(5,qid,kind,shape,q,t,exp,tag,why,out,atp,scr,
                         soff,slen,zlog,zn,woffs,wlens,revbuf,abuf,know,winner);
    }
"""
need(src.count(dispatch) == 1, "dispatch block not unique")
src = src.replace(dispatch, "")
need("cand_span" not in src, "cand_span reference remains")

# --- 3. H1: cand_zoom kind-7 guard ---
h1_old = """    if (kind==7) {
        let nw:i64=enum_words(t,woffs,wlens);
        ops=nw;
        let wo:i64=r_u32le(woffs,0); let wl:i64=r_u32le(wlens,0);
        ans=t[wo..wo+wl];
    }"""
h1_new = """    if (kind==7) {
        let nw:i64=enum_words(t,woffs,wlens);
        ops=nw;
        // DEGENERATE GUARD 2026-09-26 (H1): no words -> '?' — never read an
        // unpopulated word-table slot (uninitialized heap read -> panic).
        if (nw==0) { abuf[0]=63; alen=1; ans=abuf[0..alen]; }
        else {
            let wo:i64=r_u32le(woffs,0); let wl:i64=r_u32le(wlens,0);
            ans=t[wo..wo+wl];
        }
    }"""
need(src.count(h1_old) == 1, "H1 pattern not unique")
src = src.replace(h1_old, h1_new)

# --- 4. H2: cand_word kind-16 guard ---
h2_old = """    if (kind==16) {
        let k:i64=nw-1;
        let wo:i64=r_u32le(woffs,k*4); let wl:i64=r_u32le(wlens,k*4);
        ans=t[wo..wo+wl]; ops=nw;
    }"""
h2_new = """    if (kind==16) {
        // DEGENERATE GUARD 2026-09-26 (H2): no words -> '?' — never index
        // the word table at k=nw-1=-1 (negative out-of-bounds read).
        if (nw==0) { abuf[0]=63; alen=1; ans=abuf[0..alen]; }
        else {
            let k:i64=nw-1;
            let wo:i64=r_u32le(woffs,k*4); let wl:i64=r_u32le(wlens,k*4);
            ans=t[wo..wo+wl]; ops=nw;
        }
    }"""
need(src.count(h2_old) == 1, "H2 pattern not unique")
src = src.replace(h2_old, h2_new)

# --- 5. H3: cand_word kind-7 guard (defensive; unreachable via policy) ---
h3_old = """    if (kind==7) {
        let wo:i64=r_u32le(woffs,0); let wl:i64=r_u32le(wlens,0);
        ans=t[wo..wo+wl]; ops=nw;
    }"""
h3_new = """    if (kind==7) {
        // DEGENERATE GUARD 2026-09-26 (H3, defensive): same unpopulated-slot
        // hazard as H1; unreachable via the frozen policy but guarded anyway.
        if (nw==0) { abuf[0]=63; alen=1; ans=abuf[0..alen]; }
        else {
            let wo:i64=r_u32le(woffs,0); let wl:i64=r_u32le(wlens,0);
            ans=t[wo..wo+wl]; ops=nw;
        }
    }"""
need(src.count(h3_old) == 1, "H3 pattern not unique")
src = src.replace(h3_old, h3_new)

open(P, "w").write(src)
print(f"transform ok: {n0} -> {len(src.split(chr(10)))} lines")
