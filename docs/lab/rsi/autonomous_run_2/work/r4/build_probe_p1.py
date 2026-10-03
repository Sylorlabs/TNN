#!/usr/bin/env python3
"""Build the P1 translation probe: tables_gen.zag + policy_engine.zag.inc
(ag32/ap32/parse_i32/i64s) + l1_translate and its callees sliced MECHANICALLY
from the FIXED src/proposer.zag by function name (no transcription) + probe
main asserting emitted bytecode params equal input params exactly.
Usage: probe_p1 (no args; cases embedded). Exit nonzero on any failure."""
import re, sys

BASE = "/home/hatch/workspace/tnn-lab/rsi/autonomous_run_2"
src = open(f"{BASE}/src/proposer.zag").read()

# function names needed by l1_translate (transitive callees)
WANT = ["s_eq", "s_starts", "s_find", "is_tokchar", "line_count", "line_at",
        "oprm_get", "parse_atom", "parse_action",
        "bb_c", "bb_s", "bb_i", "bb_len", "l1_translate"]

# split top-level fn blocks: find "fn NAME(" then balance braces
def extract(src, name):
    m = re.search(r"\nfn " + re.escape(name) + r"\(", src)
    if not m:
        raise SystemExit(f"fn {name} not found in src/proposer.zag")
    start = m.start() + 1
    # find opening brace of signature/body
    bi = src.index("{", m.end())
    depth = 0
    i = bi
    in_str = False
    while True:
        c = src[i]
        if c == '"' and src[i-1] != '\\':
            in_str = not in_str
        if not in_str:
            if c == '{':
                depth += 1
            elif c == '}':
                depth -= 1
                if depth == 0:
                    return src[start:i+1]
        i += 1

blocks = [extract(src, n) for n in WANT]
# dedupe identical (none) and keep file order: sort by position in src
blocks.sort(key=lambda b: src.index(b))

tg = open(f"{BASE}/build/tables_gen.zag").read()
inc = open(f"{BASE}/src/policy_engine.zag.inc").read()

# cases: (atom_text, action_text, expected_bytecode)
cases = []
for p in [-6, -2, -1, 0, 1, 6]:
    for nm, aid in [("sm_le", 4), ("sm_ge", 5), ("sm_eq", 6),
                    ("psm_le", 13), ("psm_ge", 14), ("psm_eq", 15)]:
        st = 1 if aid <= 11 else 2
        act = 1 if aid <= 11 else 3
        cases.append((f"{nm}({p})", "force_consult" if act == 1 else "force_withhold",
                      f"{st},{aid}={p},{act}"))
for p in [-3, -1, 0, 3]:
    for nm, aid in [("sn_ge", 8), ("so_ge", 9)]:
        cases.append((f"{nm}({p})", "force_consult", f"1,{aid}={p},1"))
for nm, aid, prm in [("pre_is", 1, "HOLD"), ("pre_is", 1, "OLD"),
                     ("post_is", 12, "NEW"), ("dir_is", 7, "TIE"),
                     ("dir_is", 7, "OLD_LEAD")]:
    pv = {"HOLD": 0, "NEW": 1, "OLD": 2, "TIE": 0, "NEW_LEAD": 1, "OLD_LEAD": 2}[prm]
    st = 1 if aid <= 11 else 2
    act = 1 if aid <= 11 else 3
    cases.append((f"{nm}({prm})", "force_consult" if act == 1 else "force_withhold",
                  f"{st},{aid}={pv},{act}"))
cases.append(("chan_present", "force_consult", "1,2,1"))
cases.append(("post_is(NEW)", "force_install(NEW)", "2,12=1,4=1"))
cases.append(("post_is(NEW)", "force_install(OLD)", "2,12=1,4=2"))
for mask in ["000", "101", "111"]:
    mv = int(mask, 2)
    cases.append(("pre_is(NEW)", f"recompute_only({mask})", f"4,1=1,5={mv}"))
cases.append(("sm_le(-2)", "block_consult", "1,4=-2,2"))

main_lines = ["fn main()void {",
              "    let buf:*u8=_zag_malloc(4096);",
              "    let bpos:*u8=_zag_malloc(8);",
              "    let fails:i32=0;",
              "    let total:i32=0;"]
for idx, (atom, act, exp) in enumerate(cases):
    pol = f"POLICY t\\nRULE 1 IF {atom} THEN {act}\\nEND"
    main_lines.append(f"    // case {idx}: {atom} / {act}")
    main_lines.append(f"    total=total+1;")
    main_lines.append(f"    ap32(bpos,0,0);")
    main_lines.append(f"    let rc:i32=l1_translate(\"{pol}\",buf,bpos);")
    main_lines.append(f"    let blen:i64=bb_len(bpos);")
    main_lines.append(f"    let got:[]u8=buf[0..blen];")
    main_lines.append(f"    if(rc!=0){{fails=fails+1;_zag_print(\"FAIL rc \");_zag_print(\"{atom}|{act}\");_zag_println(\"\");}}else{{")
    main_lines.append(f"        if(s_eq(got,\"{exp}\")!=1){{fails=fails+1;_zag_print(\"FAIL bc \");_zag_print(\"{atom}|{act}\");_zag_print(\" got=\");_zag_print(got);_zag_println(\"\");}}")
    main_lines.append("    }")
main_lines += ["    _zag_print(\"P1 cases=\");_zag_print(i64s(total as i64));",
               "    _zag_print(\" fails=\");_zag_print(i64s(fails as i64));",
               "    _zag_println(\"\");",
               "    if(fails!=0){_zag_println(\"P1-FAIL\");}else{_zag_println(\"P1-PASS\");}",
               "}"]
main = "\n".join(main_lines) + "\n"

dest = f"{BASE}/work/r4/probe_p1_full.zag"
import os
os.makedirs(f"{BASE}/work/r4", exist_ok=True)
open(dest, "w").write(tg + inc + "\n".join(blocks) + "\n" + main)
print("wrote", dest, f"({len(cases)} cases)")
