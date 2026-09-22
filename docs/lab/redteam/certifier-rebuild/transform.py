#!/usr/bin/env python3
"""Mechanical cast->accessor transformation for the certifier rebuild.
KB-FIDELITY: only the allowed hunk classes may change.
"""
import re, sys

HELPERS = '''
// ---- T-table accessors (ZNC-2026-09-21-007 workaround) ----
// All indexed i32 tables are []u8 arenas holding little-endian i32 slots.
// t_put32 stores any i32 (incl. negative sentinels); t_get32 recovers it.
fn t_put32(a:[]u8, i:i32, v:i32)i32 {
    let o:i32=i*4;
    let uv:i64=(v as i64)&4294967295;
    a[o]=(uv&255) as u8;
    a[o+1]=((uv/256)&255) as u8;
    a[o+2]=((uv/65536)&255) as u8;
    a[o+3]=((uv/16777216)&255) as u8;
    return 0;
}
fn t_get32(a:[]u8, i:i32)i32 {
    let o:i32=i*4;
    let uv:i64=(a[o] as i64)+((a[o+1] as i64)*256)+((a[o+2] as i64)*65536)+((a[o+3] as i64)*16777216);
    if(uv>=2147483648){return ((uv-4294967296) as i32);}
    return (uv as i32);
}
'''

# (source file, tables as (view, arena), anchor line to insert helpers after)
JOBS = {
 "work/thincert/thincert_rb.zag": {
   "src": "work/thincert/thincert_orig.zag",
   "anchor": "fn strip_src(src:[]u8, n:i32, code:[]u8, strs:[]u8) i32 {",
   "tables": [("coff","coffr"),("clen","clenr"),("st","str"),
              ("mtier","mtierr"),("moff","moffr"),("mlen","mlenr"),
              ("mcp","mcpr"),("foff","foffr"),("flen","flenr"),
              ("mcount","mcpr")],
   "sigparams": ["foff","flen","mtier","moff","mlen","mcount"],
 },
 "work/rngscan/checker/rngscan_v3_rb.zag": {
   "src": "work/rngscan/checker/rngscan_v3_orig.zag",
   "anchor": "fn count_byte(s:[]u8, c:u8)i32 {",
   "tables": [("loff","loffr"),("fb0","fb0r"),("fb1","fb1r"),("fl0","fl0r"),
              ("fl1","fl1r"),("fpoff","fpor"),("fplen","fplr"),("fscan","fscr"),
              ("fname_off","fnor"),("fname_len","fnlr"),("fn_file","fnfr"),
              ("fn_start","fnsr"),("fn_end","fner"),("stack","stkr"),
              ("reach","rchr"),("stoff","stor"),("stlen","stlr"),
              ("pinoff","pnor"),("pinlen","pnlr"),("fdepth","fdr"),
              ("v_off","vofr"),("v_len","vlnr"),("v_alloc","varr"),
              ("v_master","vmr"),("v_skip","vsr"),("v_cstart","vcsr"),
              ("v_cend","vcer"),("v_hit","vhr"),("jlp","jlpr"),("nhp","nhpr"),
              ("ff","fpor"),("fnoff","fnor"),("fnlen","fnlr")],
   "sigparams": ["loff","jlp","nhp","pinoff","pinlen","fnoff","fnlen",
                 "stoff","stlen","fdepth","v_off","v_len","v_alloc",
                 "v_master","v_skip","v_cstart","v_cend","v_hit"],
 },
}

def xform_code(code, tables):
    # indexed writes:  NAME[idx]=value;  ->  t_put32(NAME,idx,value);
    # (guard (?!=) so == / != comparisons are untouched)
    for view, arena in tables:
        pat = re.compile(r"\b%s\[([^\]]+)\]=(?!=)([^;]+);" % re.escape(view))
        code = pat.sub(lambda m: "t_put32(%s,%s,%s);" % (view, m.group(1), m.group(2)), code)
    # indexed reads:  NAME[idx]  ->  t_get32(NAME,idx)
    for view, arena in tables:
        pat = re.compile(r"\b%s\[([^\]]+)\]" % re.escape(view))
        code = pat.sub(lambda m: "t_get32(%s,%s)" % (view, m.group(1)), code)
    return code

def transform(path, cfg):
    lines = open(cfg["src"]).read().split("\n")
    out = []
    for ln in lines:
        ci = ln.find("//")
        if ci >= 0:
            code, comment = ln[:ci], ln[ci:]
        else:
            code, comment = ln, ""
        out.append(xform_code(code, cfg["tables"]) + comment)
    src = "\n".join(out)
    # 1. helpers
    assert cfg["anchor"] in src, "anchor missing in "+path
    src = src.replace(cfg["anchor"], HELPERS + "\n" + cfg["anchor"], 1)
    # 2. cast lines -> plain u8 aliases
    for view, arena in cfg["tables"]:
        if view == "ff":
            old = "let ff:[]i32=fpoff;"
            assert old in src, "ff line missing"
            src = src.replace(old, "let ff:[]u8=fpor;", 1)
            continue
        old = "let %s:[]i32=%s as []i32;" % (view, arena)
        if old in src:
            src = src.replace(old, "let %s:[]u8=%s;" % (view, arena), 1)
        # else: name is a []i32 fn param (fnoff/fnlen/mcount) — sig rule covers it
    # 3. signature params []i32 -> []u8 (word-boundary, only listed names)
    for p in cfg["sigparams"]:
        src2 = re.sub(r"\b%s:\[\]i32" % p, "%s:[]u8" % p, src)
        assert src2 != src, "sigparam not found: "+p
        src = src2
    # 4. indexed reads/writes (code only; comments untouched) — done above per-line
    open(path, "w").write(src)

for path, cfg in JOBS.items():
    transform(path, cfg)
    print("wrote", path)

# KB-FIDELITY self-checks (comments stripped first; they are intentionally untouched)
for path, cfg in JOBS.items():
    raw = open(path).read()
    code_only = "\n".join(ln.split("//")[0] for ln in raw.split("\n"))
    bad = re.findall(r"as \[\](?:i32|u32|u16)", code_only)
    assert not bad, "remaining bad casts in "+path
    # no leftover bare indexed uses of any view name
    for view, arena in cfg["tables"]:
        left = re.findall(r"\b%s\[" % re.escape(view), code_only)
        assert not left, "leftover index of %s in %s" % (view, path)
    print("fidelity scan OK:", path)
