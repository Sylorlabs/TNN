#!/usr/bin/env python3
"""Generate a chunk-size variant of the current store code for Crew D battery.

Copies ref/ingest.zag -> build/<name>/store_fast.zag with exactly two
mechanical substitutions:
  1. `fn main()void {` -> `fn ingest_lib_main()void {`  (library-ify, same as
     the 1GB redteam's rt_ingest_lib.zag)
  2. `const IG_BLOB_CHUNK:i64=33488896;` -> `const IG_BLOB_CHUNK:i64=<SIZE>;`
Everything else is byte-identical to the frozen source. Records provenance
(source SHA256, substituted lines, output SHA256) to BUILD_MANIFEST.txt.
Also stages substrate imports + kbctl.zag into the build dir.
Zero RNG.
"""
import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CREWD = os.path.dirname(HERE)
REF = os.path.join(CREWD, "ref", "ingest.zag")
SRC = os.path.join(HERE, "kbctl.zag")
TOOLCHAIN = os.path.expanduser("~/workspace/tnn-lab/toolchain")
SUBSTRATE = ["R33_NATIVE_SHA256_V2.zag", "R33_NATIVE_IO_V1.zag"]

MAIN_LINE = "fn main()void {"
MAIN_REPL = "fn ingest_lib_main()void {"
CHUNK_LINE = "const IG_BLOB_CHUNK:i64=33488896;"
CHUNK_TMPL = "const IG_BLOB_CHUNK:i64=%d;"
CAP_LINE = "const KB_CAP:i32=200000;"
CAP_TMPL = "const KB_CAP:i32=%d;"


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def gen_variant(name, chunk_size, kb_cap=200000):
    bdir = os.path.join(CREWD, "build", name)
    os.makedirs(bdir, exist_ok=True)
    with open(REF, "r") as f:
        src = f.read()
    assert src.count(MAIN_LINE) == 1, "main line count != 1"
    assert src.count(CHUNK_LINE) == 1, "chunk line count != 1"
    out = src.replace(MAIN_LINE, MAIN_REPL)
    out = out.replace(CHUNK_LINE, CHUNK_TMPL % chunk_size)
    sf = os.path.join(bdir, "store_fast.zag")
    with open(sf, "w") as f:
        f.write(out)
    with open(SRC, "r") as f:
        ksrc = f.read()
    assert ksrc.count(CAP_LINE) == 1, "cap line count != 1"
    ksrc = ksrc.replace(CAP_LINE, CAP_TMPL % kb_cap)
    kf = os.path.join(bdir, "kbctl.zag")
    with open(kf, "w") as f:
        f.write(ksrc)
    for s in SUBSTRATE:
        shutil.copy(os.path.join(TOOLCHAIN, s), os.path.join(bdir, s))
    man = os.path.join(bdir, "BUILD_MANIFEST.txt")
    with open(man, "w") as f:
        f.write("variant=%s\n" % name)
        f.write("chunk_size=%d\n" % chunk_size)
        f.write("kb_cap=%d\n" % kb_cap)
        f.write("source=ref/ingest.zag (commit 118251c5 tree)\n")
        f.write("source_sha256=%s\n" % sha256_file(REF))
        f.write("subst1=%r -> %r\n" % (MAIN_LINE, MAIN_REPL))
        f.write("subst2=%r -> %r\n" % (CHUNK_LINE, CHUNK_TMPL % chunk_size))
        f.write("store_fast_sha256=%s\n" % sha256_file(sf))
        f.write("kbctl_src=src/kbctl.zag with KB_CAP=%d\n" % kb_cap)
        f.write("kbctl_src_sha256=%s\n" % sha256_file(kf))
        for s in SUBSTRATE:
            f.write("substrate_%s_sha256=%s\n" % (s, sha256_file(os.path.join(bdir, s))))
    print("variant %s (chunk=%d cap=%d) staged in %s" % (name, chunk_size, kb_cap, bdir))
    return bdir


if __name__ == "__main__":
    # usage: gen_variant.py name chunk_size [kb_cap]  (or with no args: all frozen variants)
    if len(sys.argv) >= 3:
        cap = int(sys.argv[3]) if len(sys.argv) > 3 else 200000
        gen_variant(sys.argv[1], int(sys.argv[2]), cap)
    else:
        for name, size, cap in [("c4096", 4096, 200000), ("c8192", 8192, 200000),
                                ("c65536", 65536, 200000), ("c1m", 1048576, 200000),
                                ("c33m", 33488896, 300000)]:
            gen_variant(name, size, cap)
