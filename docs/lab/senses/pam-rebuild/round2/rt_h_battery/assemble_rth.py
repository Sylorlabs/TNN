#!/usr/bin/env python3
"""assemble_rth.py — build rth_battery.zag deterministically (RT-H crew).

Extracts the named hybrid functions byte-identically from the committed
d1battery.zag (commit 81dcfaf1, verified SHA-256
e0cc1a25295d74e2f088b51b8666c7a1df7888e8a2605e21647298de44fa5b10) via
balanced-brace extraction, then concatenates:
  header + @import + BEGIN marker + functions + END marker + rth_new.zag
-> rth_battery.zag

Zero RNG. Byte-identical output on every run (verified by SHA below).
"""
import hashlib

SRC = "/home/hatch/workspace/tmp_commit/d1_d1battery.zag"
NEW = "/home/hatch/workspace/rt_h_work/rth_new.zag"
OUT = "/home/hatch/workspace/rt_h_work/rth_battery.zag"

FN_NAMES = [
    "z_cstr", "z_read", "p_atoi", "getf", "iabs",
    "t_put32", "t_get32", "ap_str", "ap_i64",
    "lawful_meas_gain", "lawful_conf_crop", "warrant",
    "reproj_c", "reproj_m", "world_w", "p_actual_fn", "p_guess_fn",
]

EXPECTED_SRC_SHA = "e0cc1a25295d74e2f088b51b8666c7a1df7888e8a2605e21647298de44fa5b10"

def extract_fn(text, name):
    key = "fn " + name + "("
    start = text.find(key)
    if start < 0:
        raise RuntimeError(f"function {name} not found")
    # functions start at line start; back up to the line start
    ls = text.rfind("\n", 0, start) + 1
    depth = 0
    i = start
    in_str = False
    esc = False
    while True:
        ch = text[i]
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_str = False
        else:
            if ch == '"':
                in_str = True
            elif ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    end = i + 1
                    break
        i += 1
    return text[ls:end] + "\n"

def main():
    src = open(SRC, "r", encoding="utf-8").read()
    sha = hashlib.sha256(src.encode("utf-8")).hexdigest()
    assert sha == EXPECTED_SRC_SHA, f"source SHA mismatch: {sha}"
    fns = []
    for name in FN_NAMES:
        fns.append(extract_fn(src, name))
    new = open(NEW, "r", encoding="utf-8").read()
    header = (
        '@import("R33_NATIVE_IO_V1.zag")\n'
        "\n"
        "// rth_battery.zag -- RT-H Class-H battery vs the committed D1 hybrid (2026-09-24).\n"
        "// Pure Zag, zero RNG, deterministic. Frozen prereg: PREREG_RT_H.md (committed\n"
        "// alone, commit 354186d4). Assembled by assemble_rth.py from the committed\n"
        "// d1battery.zag (81dcfaf1) + rth_new.zag.\n"
        "//\n"
        "// Hybrid under test: the COMMITTED D1 artifact, UNMODIFIED. Functions between\n"
        "// the VERBATIM markers are byte-identical copies of committed d1battery.zag;\n"
        "// see hybrid_src_diff.txt. New code (rth_new.zag) drives the hybrid with\n"
        "// Class-H fixtures and computes the two probes + kill bars; it does not\n"
        "// alter the hybrid's decision logic.\n"
        "//\n"
        "// argv[1]: rth_fixtures.txt (240: 120 N honest + 120 H attack, gen_rth.py).\n"
        "// argv[2]: d1_adv_fixtures.txt (committed, 81dcfaf1; class-B records feed\n"
        "//          the handoff-inversion probe's Wire 1).\n"
        "//\n"
        "// znc landmine notes: no `as []i32` casts (parallel []u8 arenas with\n"
        "// explicit little-endian put/get32); no slice ==; no .* on non-pointers;\n"
        "// no bare blocks; no struct returns; shallow nesting only; no identifier\n"
        "// named try; i64 only non-negative for >> and %.\n"
        "\n"
        "// === BEGIN VERBATIM COPY FROM d1battery.zag (commit 81dcfaf1) ===\n"
    )
    endmark = "// === END VERBATIM COPY ===\n\n"
    body = header + "\n".join(fns) + endmark + new
    open(OUT, "w", encoding="utf-8").write(body)
    outsha = hashlib.sha256(body.encode("utf-8")).hexdigest()
    print(f"wrote {OUT}: {len(body)} bytes, SHA-256 {outsha}")
    print(f"extracted {len(fns)} verbatim functions")

if __name__ == "__main__":
    main()
