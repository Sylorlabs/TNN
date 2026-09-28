#!/usr/bin/env python3
"""Build b3536_sstar.zag: extract mechanisms VERBATIM from the committed
composition driver (7a1a8422, file SHA-256 1602247d...) and concatenate the
new S*-battery code (fixtures + S* scorer + main).

The driver is used UNMODIFIED: extraction is exact byte-slices, each asserted
present exactly once. New code lives only in sstar_new.zag.
"""
import hashlib, re, sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
DRIVER = os.path.join(HERE, "driver_ref", "b3536.zag")
NEWCODE = os.path.join(HERE, "sstar_new.zag")
OUT = os.path.join(HERE, "b3536_sstar.zag")
FILE_SHA256 = "1602247d7c9f1e96ba0f9df30a7b197f6a9ff71884df67c1cfb93c1807280029"

# functions/structs to extract verbatim, in emission order
WANT = [
    "ob_puts", "ob_puti",
    "fnv32", "put32i", "put64i", "get32i", "put32u",
    "struct:LowVal", "struct:HighVal",
    "tag_half", "verify_high", "declassify", "act_sink", "premise_sink",
    "wstep", "honest_wc", "honest_wm",
    "cstep", "admit36", "adv36_conf", "adv36_meas",
    "au_put", "au_get", "le64",
    "tb_putc", "tb_puts", "r36_derive_seed", "ledger_has", "ledger_add",
    "c_stage2", "c_wevo",
    "m36a_precompute",
    "comp35j", "comp36j", "comp36k", "comp36m",
]

def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        h.update(f.read())
    return h.hexdigest()

def extract_block(src, kind, name):
    if kind == "fn":
        pat = re.compile(r"fn %s\(" % re.escape(name))
    else:
        pat = re.compile(r"struct %s \{" % re.escape(name))
    ms = list(pat.finditer(src))
    assert len(ms) == 1, f"{kind} {name}: found {len(ms)} matches, want exactly 1"
    i = src.index("{", ms[0].start())
    depth = 0
    j = i
    while True:
        c = src[j]
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                break
        j += 1
        assert j < len(src), f"unbalanced braces in {name}"
    head = src[ms[0].start():i].rstrip()
    return head + " " + src[i:j+1]

def main():
    got = sha256_file(DRIVER)
    assert got == FILE_SHA256, f"driver SHA mismatch: {got}"
    print(f"[gen] driver_ref/b3536.zag SHA-256 OK ({FILE_SHA256[:12]}, build 7a1a8422)")
    src = open(DRIVER).read()
    parts = []
    for w in WANT:
        if w.startswith("struct:"):
            kind, name = "struct", w.split(":", 1)[1]
        else:
            kind, name = "fn", w
        blk = extract_block(src, kind, name)
        parts.append(blk)
        print(f"[gen] extracted {kind} {name} ({len(blk)} bytes, verbatim)")
    newcode = open(NEWCODE).read()
    # new code must not redefine anything extracted
    for w in WANT:
        name = w.split(":", 1)[1] if ":" in w else w
        assert not re.search(r"fn %s\(" % re.escape(name), newcode), f"new code redefines {name}"
        assert not re.search(r"struct %s \{" % re.escape(name), newcode), f"new code redefines {name}"
    header = ("// b3536_sstar.zag — B-3536-S* battery (grok's N/O/P classes vs the composition)\n"
              "// Mechanisms extracted VERBATIM by gen_sstar.py from committed b3536.zag\n"
              "// (build 7a1a8422, file SHA-256 1602247d7c9f1e96ba0f9df30a7b197f6a9ff71884df67c1cfb93c1807280029).\n"
              "// The composition driver is UNMODIFIED. New code: sstar_new.zag only\n"
              "// (N/O/P/HONEST/ArmT fixtures + S* scorer + main).\n"
              "@import(\"R33_NATIVE_IO_V1.zag\")\n"
              "@import(\"R33_NATIVE_SHA256_V2.zag\")\n\n")
    out = header + "\n\n".join(parts) + "\n\n" + newcode
    with open(OUT, "w") as f:
        f.write(out)
    print(f"[gen] wrote {OUT} ({len(out)} bytes)")
    print(f"[gen] b3536_sstar.zag SHA-256: {hashlib.sha256(out.encode()).hexdigest()}")

main()
