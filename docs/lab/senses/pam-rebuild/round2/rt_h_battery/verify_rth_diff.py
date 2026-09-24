#!/usr/bin/env python3
"""verify_rth_diff.py — prove the hybrid mechanism regions in rth_battery.zag
are byte-identical to the committed d1battery.zag (81dcfaf1).

Extracts each named function from both files (balanced-brace extraction) and
compares bytes. Writes hybrid_src_diff.txt (committed evidence).
Exit 0 iff all 17 match.
"""
import hashlib, sys

SRC = "/home/hatch/workspace/tmp_commit/d1_d1battery.zag"
BAT = "/home/hatch/workspace/rt_h_work/rth_battery.zag"
OUT = "/home/hatch/workspace/rt_h_work/hybrid_src_diff.txt"

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
    src = open(SRC, encoding="utf-8").read()
    assert hashlib.sha256(src.encode()).hexdigest() == EXPECTED_SRC_SHA, "src SHA mismatch"
    bat = open(BAT, encoding="utf-8").read()
    lines = []
    lines.append("hybrid_src_diff.txt — RT-H mechanism identity transcript (2026-09-24)")
    lines.append("committed source: d1battery.zag @ 81dcfaf1")
    lines.append("  SHA-256 e0cc1a25295d74e2f088b51b8666c7a1df7888e8a2605e21647298de44fa5b10")
    lines.append("battery: rth_battery.zag (assembled by assemble_rth.py)")
    lines.append("")
    ok = True
    for name in FN_NAMES:
        a = extract_fn(src, name)
        b = extract_fn(bat, name)
        sa = hashlib.sha256(a.encode()).hexdigest()[:16]
        sb = hashlib.sha256(b.encode()).hexdigest()[:16]
        match = "IDENTICAL" if a == b else "MISMATCH"
        if a != b:
            ok = False
        lines.append(f"{name:18s} src={sa} bat={sb} {match}")
    lines.append("")
    lines.append("VERDICT: " + ("ALL 17 MECHANISM FUNCTIONS BYTE-IDENTICAL — hybrid unmodified"
                                if ok else "MISMATCH FOUND — hybrid NOT identical"))
    open(OUT, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print("\n".join(lines))
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
