#!/usr/bin/env python3
"""RT3 harness generator: emits rt3_bat.zag (fidelity rows + attack rows)."""
import csv, sys, os

RT3 = "/home/hatch/workspace/scratch-hellhole/redteam/rt3"
BUILD = os.path.join(RT3, "build")

def zag_esc(s):
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ")

def load_fidelity():
    rows = []
    with open(os.path.join(RT3, "ref_jokes.tsv"), encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line:
                continue
            parts = line.split("\t")
            rows.append(("F" + parts[0], parts[1]))
    return rows

def load_attack():
    rows = []
    with open(os.path.join(RT3, "rt3_attack_corpus.tsv"), encoding="utf-8") as f:
        r = csv.DictReader(f, delimiter="\t")
        for row in r:
            rows.append((row["id"], row["claim"]))
    return rows

def main():
    fid = load_fidelity()
    atk = load_attack()
    assert len(fid) == 30, len(fid)
    assert len(atk) == 75, len(atk)
    out = []
    out.append('@import("j_ledger.zag")')
    out.append('@import("r5_r6.zag")')
    out.append('@import("g_intent6_v4.zag")')
    out.append("")
    out.append("fn rt3_show(id:[]u8,text:[]u8)void{")
    out.append("    let codes:[]u8=j_alloc(512);")
    out.append("    let markers:[]u8=j_alloc(4096);")
    out.append("    j_zero(codes);")
    out.append("    j_zero(markers);")
    out.append('    let intent:i32=g_classify(text,"",codes,markers);')
    out.append('    _zag_print(id);_zag_print("|");')
    out.append('    _zag_print(_zag_i64_to_str(intent as i64));_zag_print("|");')
    out.append('    _zag_print(j_exact(codes));_zag_print("|");')
    out.append('    _zag_print(j_exact(markers));')
    out.append('    _zag_println("");')
    out.append("    return;")
    out.append("}")
    out.append("")
    out.append("fn main()void{")
    for i, t in fid + atk:
        out.append('    rt3_show("%s","%s");' % (i, zag_esc(t)))
    out.append("    return;")
    out.append("}")
    out.append("")
    path = os.path.join(BUILD, "rt3_bat.zag")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print("wrote", path, "rows:", len(fid) + len(atk))

if __name__ == "__main__":
    main()
