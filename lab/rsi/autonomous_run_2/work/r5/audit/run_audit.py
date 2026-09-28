#!/usr/bin/env python3
"""RSI-8 Round 2 problem-selection audit (RUN_PREREG5 §2.6).

Builds four evidence fixtures from REAL components and runs the pure-Zag
D-PROBLEMS scan on each. Pass bar: 5/5.

  Plant A (translator-sign): buggy translator (sign-extend removed from
            oprm_get) -> 56-param round-trip probe -> TRANSLATECHECK.
  Plant B (grid-grammar):    afdisc with pre-reconciliation wide ranges
            (aid 8/9 pmax=6; aids 4/5/6/13/14/15 pmin=-8,pmax=8) -> 129 rows
            -> GRIDCHECK (rows outside L1 grammar bounds).
  Plant C (champion-fiction, LIVE): driver's CHAMPION 22/2/424 vs measured
            16/8/456 + static PREDLINE vs honest PREDHONEST.
  Noise N (clean): 320-policy trap sweep, all refused -> must NOT flag.

Expected: A->P-TRANSLATE, B->P-GRID, C->P-CHAMPION+P-PRED(+P-ACTIONSPACE),
          N->P-NONE only.
"""
import subprocess, csv, os, re, sys

BASE = os.path.expanduser("~/workspace/tnn-lab/rsi/autonomous_run_2")
R5 = f"{BASE}/work/r5"
AUD = f"{R5}/audit"
ZNC = os.path.expanduser("~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1")
os.makedirs(AUD, exist_ok=True)

def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)

def extract(src, name):
    m = re.search(r"\nfn " + re.escape(name) + r"\(", src)
    if not m:
        raise SystemExit(f"fn {name} not found")
    start = m.start() + 1
    bi = src.index("{", m.end())
    depth = 0; i = bi; in_str = False
    while True:
        c = src[i]
        if c == '"' and src[i-1] != '\\':
            in_str = not in_str
        if not in_str:
            if c == '{': depth += 1
            elif c == '}':
                depth -= 1
                if depth == 0:
                    return src[start:i+1]
        i += 1

# ---------------- Plant A: buggy translator ----------------
def plant_a():
    src = open(f"{BASE}/src/proposer.zag").read()
    # Reintroduce the sign bug: oprm_get without sign-extension
    buggy = src.replace(
        "fn oprm_get(oprm:*u8)i32 {\n    let v:i32=oprm[0] as i32;\n    if(v>127){v=v-256;}\n    return v;\n}",
        "fn oprm_get(oprm:*u8)i32 {\n    let v:i32=oprm[0] as i32;\n    return v;\n}")
    assert buggy != src, "oprm_get pattern not found"
    open(f"{AUD}/proposer_buggy.zag", "w").write(buggy)

    WANT = ["s_eq", "s_starts", "s_find", "is_tokchar", "line_count", "line_at",
            "oprm_get", "parse_atom", "parse_action",
            "bb_c", "bb_s", "bb_i", "bb_len", "l1_translate"]
    blocks = [extract(buggy, n) for n in WANT]
    blocks.sort(key=lambda b: buggy.index(b))
    tg = open(f"{BASE}/build/tables_gen.zag").read()
    inc = open(f"{BASE}/src/policy_engine.zag.inc").read()

    # 56 round-trip cases (same as R4 P1 probe)
    cases = []
    for p in [-6, -2, -1, 0, 1, 6]:
        for nm, aid in [("sm_le", 4), ("sm_ge", 5), ("sm_eq", 6),
                        ("psm_le", 13), ("psm_ge", 14), ("psm_eq", 15)]:
            st = 1 if aid <= 11 else 2
            act = 1 if aid <= 11 else 3
            cases.append((f"{nm}({p})", p,
                          "force_consult" if act == 1 else "force_withhold"))
    for p in [-3, -1, 0, 3]:
        for nm in ["sn_ge", "so_ge"]:
            cases.append((f"{nm}({p})", p, "force_consult"))
    # (param-less cases skipped for the sign audit; params are the target)

    main = ["fn main()void {",
            '    let buf:*u8=_zag_malloc(4096);',
            '    let bpos:*u8=_zag_malloc(8);',
            '    let fails:i32=0;']
    for idx, (atom, p, act) in enumerate(cases):
        pol = f"POLICY t\\nRULE 1 IF {atom} THEN {act}\\nEND"
        # The sign bug makes negative params read as unsigned (p+256), which
        # then fails grammar range checks -> l1_translate REJECTS (rc!=0).
        # A mismatch is either rejection or a mis-emitted param.
        L = []
        L.append(f'    ap32(bpos,0,0);')
        L.append(f'    let rc{idx}:i32=l1_translate("{pol}",buf,bpos);')
        L.append(f'    if(rc{idx}!=0){{')
        L.append(f'        _zag_print("TRANSLATECASE {atom} {p} REJECT {p}");_zag_println("");')
        L.append(f'        fails=fails+1;')
        L.append(f'    }}else{{')
        L.append(f'        let bl{idx}:i64=bb_len(bpos);')
        L.append(f'        let bcs{idx}:[]u8=buf[0..bl{idx}];')
        L.append(f'        let eq{idx}:i64=s_find(bcs{idx},"=");')
        L.append(f'        let pe{idx}:i64=eq{idx}+1;')
        L.append(f'        while(pe{idx}<bl{idx}){{if(bcs{idx}[pe{idx}]==44){{break;}}pe{idx}=pe{idx}+1;}}')
        L.append(f'        let okb{idx}:*u8=_zag_malloc(1);')
        L.append(f'        let got{idx}:i32=parse_i32(bcs{idx}[eq{idx}+1..pe{idx}],okb{idx});')
        L.append(f'        if(okb{idx}[0]==1){{')
        L.append(f'            if(got{idx}!={p}){{')
        L.append(f'                _zag_print("TRANSLATECASE {atom} {p} ");')
        L.append(f'                _zag_print(i64s(got{idx} as i64));')
        L.append(f'                _zag_print(" {p}");_zag_println("");')
        L.append(f'                fails=fails+1;')
        L.append(f'            }}')
        L.append(f'        }}')
        L.append(f'    }}')
        main.extend(L)
    main += ['    _zag_print("TRANSLATECHECK ");_zag_print(i64s(fails as i64));_zag_println("");',
             '}']
    full = tg + inc + "\n".join(blocks) + "\n" + "\n".join(main) + "\n"
    open(f"{AUD}/probe_translate_buggy_full.zag", "w").write(full)
    r = run([ZNC, f"{AUD}/probe_translate_buggy_full.zag", "-o", f"{AUD}/probe_translate_buggy"])
    if r.returncode != 0:
        print("PLANT-A BUILD FAIL"); print(r.stderr[-2000:]); sys.exit(1)
    r = run([f"{AUD}/probe_translate_buggy"])
    lines = r.stdout.strip().split("\n")
    check = [l for l in lines if l.startswith("TRANSLATECHECK")]
    cases_out = [l for l in lines if l.startswith("TRANSLATECASE")]
    # TRANSLATECHECK must come after; reorder: check line + cases
    return check, cases_out

# ---------------- Plant B: wide-range afdisc ----------------
def plant_b():
    src = open(f"{BASE}/src/afdisc.zag").read()
    # Restore pre-reconciliation ranges (RUN_PREREG4 §2 inverse)
    wide = src.replace("if(aid==8){pmin=0;pmax=3;}", "if(aid==8){pmin=0;pmax=6;}")
    wide = wide.replace("if(aid==9){pmin=0;pmax=3;}", "if(aid==9){pmin=0;pmax=6;}")
    for aid in (4, 5, 6, 13, 14, 15):
        wide = wide.replace(f"if(aid=={aid}){{pmin=-6;pmax=6;}}",
                            f"if(aid=={aid}){{pmin=-8;pmax=8;}}")
    assert wide != src, "afdisc range patterns not found"
    open(f"{AUD}/afdisc_wide.zag", "w").write(wide)
    tg = open(f"{BASE}/build/tables_gen.zag").read()
    inc = open(f"{BASE}/src/policy_engine.zag.inc").read()
    full = tg + inc + wide
    open(f"{AUD}/afdisc_wide_full.zag", "w").write(full)
    r = run([ZNC, f"{AUD}/afdisc_wide_full.zag", "-o", f"{AUD}/afdisc_wide"])
    if r.returncode != 0:
        print("PLANT-B BUILD FAIL"); print(r.stderr[-2000:]); sys.exit(1)
    # proxy gt/cls
    gt = ''; cls = ''
    for row in csv.DictReader(open(f"{BASE}/build/proxy_battery.csv")):
        g = row['gt']; gt += '1' if g == 'NEW' else ('2' if g == 'OLD' else '0')
        m = {'N-clean': 0, 'O-clean': 1, 'MISLEAD-OLD': 2, 'ADV-NEW': 3, 'NEITHER': 4}
        cls += str(m[row['class']])
    r = run([f"{AUD}/afdisc_wide", gt, cls])
    rows = [l for l in r.stdout.strip().split("\n") if l.startswith("AFDISC")]
    # grammar bounds (authoritative: L1 grammar)
    bounds = {1: (0, 2), 4: (-6, 6), 5: (-6, 6), 6: (-6, 6), 7: (0, 2),
              8: (-3, 3), 9: (-3, 3), 12: (0, 2),
              13: (-6, 6), 14: (-6, 6), 15: (-6, 6)}
    bad = []
    for row in rows:
        # AFDISC <class> <atomid> <param> <nwt> <nw> <nct> <nc>
        parts = row.split()
        aid = int(parts[2]); prm = int(parts[3])
        if aid in bounds:
            lo, hi = bounds[aid]
            if prm < lo or prm > hi:
                bad.append((aid, prm))
    return len(rows), bad, bounds

def main():
    print("== Plant A: translator sign bug ==")
    check, cases = plant_a()
    print(check[0] if check else "NO CHECK LINE", f"({len(cases)} cases)")
    print("== Plant B: out-of-grammar grid ==")
    nrows, bad, bounds = plant_b()
    print(f"wide afdisc rows={nrows} out-of-grammar={len(bad)}")
    # save evidence pieces
    open(f"{AUD}/plant_a.ev", "w").write("\n".join(check + cases) + "\n")
    open(f"{AUD}/plant_b.ev", "w").write(
        f"GRIDCHECK {len(bad)}\n" +
        "".join(f"GRAMMARBOUNDS {aid} {lo} {hi}\n" for aid, (lo, hi) in sorted(bounds.items())))

if __name__ == "__main__":
    main()
