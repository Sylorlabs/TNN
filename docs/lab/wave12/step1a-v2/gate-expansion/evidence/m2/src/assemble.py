#!/usr/bin/env python3
"""Assemble M2 battery module sources.

For each v1-style plant: strip the stub `fn main`, rewrite the substrate
import to m2_substrate.zag, append the M2 harness main.
For hand-built modules (P07, P09-twin, P12, C01..C06): copy verbatim
(they already import m2_substrate.zag and define their own main).
"""
import os, re, sys

SRC = os.path.expanduser("~/workspace/tnn-lab/wave12/step1a-v2/gate-expansion/evidence/m2/src")
CORPUS = os.path.expanduser("~/workspace/tnn-lab/wave12/step1a-no-rng-audit/redteam/plants")
OUT = os.path.join(SRC, "modules")
os.makedirs(OUT, exist_ok=True)

harness = open(os.path.join(SRC, "m2_harness_main.zag")).read()

# v1 plants needing the harness (plantNN -> module name).
# NOTE: plant03 (urandom), plant06 (clock), plant11 (uninit), plant20
# (envflag) are NOT assembled from v1: the v1 files' mechanisms are
# behaviorally inert as standalone binaries (documented in the corpus
# notes), so functional runtime variants live in src/handbuilt/.
V1 = {
    "plant01.zag": "p01_getrandom.zag",
    "plant11.zag": "p04_uninit.zag",
    "plant16.zag": "p08_hashorder.zag",
    "plant18.zag": "p09_innocent_tables.zag",  # structural twin of v3 killer
    "plant19.zag": "p06_aslr.zag",
}

for src_name, dst_name in V1.items():
    src = open(os.path.join(CORPUS, src_name)).read()
    # rewrite substrate import
    assert '@import("R33_NATIVE_IO_V1.zag")' in src, src_name
    src = src.replace('@import("R33_NATIVE_IO_V1.zag")', '@import("m2_substrate.zag")')
    # strip stub main (from "fn main()" to end)
    m = re.search(r'\nfn main\(\)i32 \{', src)
    assert m, src_name
    src = src[:m.start()] + "\n"
    src = src + harness
    open(os.path.join(OUT, dst_name), "w").write(src)
    print("assembled", dst_name)

# hand-built modules: appended with the harness main unless they carry the
# M2-NO-HARNESS marker (they define their own main).
HB = os.path.join(SRC, "handbuilt")
for f in sorted(os.listdir(HB)):
    if f.endswith(".zag"):
        data = open(os.path.join(HB, f)).read()
        assert '@import("m2_substrate.zag")' in data, f
        if "// M2-NO-HARNESS" not in data:
            data = data + harness
        open(os.path.join(OUT, f), "w").write(data)
        print("copied", f)

# K2′ plants P10 (machine-id) and P11 (argv): keep their own main (it reads
# _zag_arg(1)/(2)); only the substrate import is rewritten.
# PLUS a documented repair (2026-09-25): their print_hex allocates n*2+1
# bytes, fills n*2 hex chars, and prints the WHOLE slice — the trailing
# byte is uninitialized (0x00 under zero-fill, dirt under the audit
# allocator), spuriously diverging D1..D5 outputs. The repair prints
# exactly hx[0..n*2]. This touches output formatting only, not the
# tested mechanism (machine-id / argv ingestion).
K2P = os.path.expanduser("~/workspace/tnn-lab/wave12/step1a-v2/thin-certifier/k2prime-redteam/plants")
for src_name, dst_name in (("plant19/variation.zag", "p10_machineid.zag"),
                           ("plant20/variation.zag", "p11_argv.zag")):
    src = open(os.path.join(K2P, src_name)).read()
    assert '@import("R33_NATIVE_IO_V1.zag")' in src, src_name
    src = src.replace('@import("R33_NATIVE_IO_V1.zag")', '@import("m2_substrate.zag")')
    assert "fn main()" in src, src_name
    old_print = "    _zag_print(hx);\n    _zag_println(\"\");"
    assert old_print in src, src_name
    src = src.replace(old_print,
        "    _zag_print(hx[0..n*2]);\n    _zag_println(\"\");")
    open(os.path.join(OUT, dst_name), "w").write(src)
    print("k2prime", dst_name)
