#!/usr/bin/env python3
"""Independently verify grok's 5 mechanism facts against committed b3536.zag (7a1a8422).
Reads ~/workspace/rts_work/inbox/b3536.zag; SHA-verifies it against the committed
blob SHA first. Prints PASS/FAIL per fact with the exact evidence lines.
"""
import hashlib, re, sys

SRC = "/home/hatch/workspace/rts_work/inbox/b3536.zag"
# file-content SHA-256 recorded in VERDICT_B3536.md @ c0834cdf for build 7a1a8422
FILE_SHA256 = "1602247d7c9f1e96ba0f9df30a7b197f6a9ff71884df67c1cfb93c1807280029"
# git blob SHA-1 from the contents API (sha of "blob <len>\\0" + content)
BLOB_SHA1 = "bff9f8161e7f1b225fa9514ae67da03a5030b857"

def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        h.update(f.read())
    return h.hexdigest()

def fn_body(src, name):
    """Extract the body of `fn name(` ... matching close brace (no nesting beyond 1 level needed check)."""
    m = re.search(r"fn %s\(" % re.escape(name), src)
    if not m:
        return None
    i = src.index("{", m.start())
    depth = 0
    j = i
    while True:
        if src[j] == "{":
            depth += 1
        elif src[j] == "}":
            depth -= 1
            if depth == 0:
                return src[i:j+1]
        j += 1

def main():
    got = sha256_file(SRC)
    assert got == FILE_SHA256, f"SHA256 MISMATCH: {got} != {FILE_SHA256}"
    print(f"[sha] b3536.zag file SHA-256 matches build 7a1a8422 ({FILE_SHA256[:12]})")
    with open(SRC, "rb") as f:
        content = f.read()
    blob = b"blob %d\0" % len(content) + content
    got1 = hashlib.sha1(blob).hexdigest()
    assert got1 == BLOB_SHA1, f"GIT BLOB SHA1 MISMATCH: {got1} != {BLOB_SHA1}"
    print(f"[sha] git blob SHA-1 matches contents API ({BLOB_SHA1[:12]})")
    src = open(SRC).read()
    ok = True

    # Fact 1: declassify fixture-invocable with verdict=1 (comp36m mints on attacker content)
    b = fn_body(src, "declassify")
    f1a = b is not None and "if(verdict == 1)" in b
    m36 = fn_body(src, "comp36m")
    f1b = m36 is not None and "declassify(v, 1, bs)" in m36
    print(f"[fact1] declassify verdict==1 branch exists: {f1a}; comp36m calls declassify(v,1,bs): {f1b}")
    ok &= f1a and f1b

    # Fact 2: c_stage2 commitment vacuous — chi/clo from presented values; admit36 recomputes same
    cs2 = fn_body(src, "c_stage2")
    a36 = fn_body(src, "admit36")
    f2a = ("cstep(bs, c0, c1, c2, 5)" in cs2 and "cstep(bs, c0, c1, c2, 6)" in cs2
           and "admit36(bs, c0, c1, c2, chi, clo, whi, wlo)" in cs2)
    f2b = ("cstep(bs, oid, oconf, omeas, 5) != chi" in a36
           and "cstep(bs, oid, oconf, omeas, 6) != clo" in a36)
    # no persistent commitment store: c_stage2/admit36 must not stash chi/clo anywhere but the call
    f2c = ("nio_alloc" not in cs2) and ("au_put" not in cs2) and ("au_put" not in a36)
    # live predicate is distance-only
    f2d = ("if(dc > 5)" in a36 and "if(dm > 20)" in a36)
    print(f"[fact2] c_stage2 hashes presented values: {f2a}; admit36 recomputes same: {f2b}; "
          f"no commit store: {f2c}; live predicate |dc|<=5 & |dm|<=20: {f2d}")
    ok &= f2a and f2b and f2c and f2d

    # Fact 3: cstep binds low-32 of (id,conf,meas) only; label uncommitted; id never world-checked
    cst = fn_body(src, "cstep")
    n_put32 = cst.count("put32i(bs,")
    f3a = n_put32 == 3 and "label" not in cst
    # admit36: oid appears only in the two cstep recompute lines (never compared to a world id)
    oid_uses = [l.strip() for l in a36.splitlines() if "oid" in l]
    f3b = all("cstep(bs, oid, oconf, omeas" in l for l in oid_uses) and len(oid_uses) == 2
    f3c = "honest_wc" in a36 and "honest_wm" in a36  # world check is on conf/meas only
    print(f"[fact3] cstep has exactly 3 put32i, no label: {f3a} (put32i count={n_put32}); "
          f"oid used only in recompute ({len(oid_uses)} lines): {f3b}; world check on conf/meas: {f3c}")
    ok &= f3a and f3b and f3c

    # Fact 4: install = gate mechanics only (s1==1 && s2==1), no S* predicate
    installs = re.findall(r"if\(s1 == 1 && s2 == 1\) \{ installs = installs \+ 1; \}", src)
    f4a = len(installs) >= 4  # comp35j, comp35k, comp36j, comp36k, comp36m
    f4b = "S*" not in src and "harm" not in src.lower()
    print(f"[fact4] install-scoring lines 's1==1 && s2==1': {len(installs)} (>=4: {f4a}); no S*/harm scoring: {f4b}")
    ok &= f4a and f4b

    # Fact 5: untested cell — no comp* class combines honest mint (v=1) + world-close + dirty label
    # collect per comp fn: (mint verdicts used, label values used)
    compfns = ["comp35j", "comp35k", "comp35l", "comp35m", "comp36j", "comp36k", "comp36m"]
    cell_found = False
    for cf in compfns:
        cb = fn_body(src, cf) or ""
        mints1 = "declassify(v, 1, bs)" in cb or "declassify(m, 1, bs)" in cb or "declassify(s, 1, bs)" in cb or "declassify(h, 1, bs)" in cb
        labels = set(re.findall(r"label=(-?\d+)\}", cb))
        worldclose = "honest_wc(whi, wlo)" in cb or "honest_wc(tw, tl)" in cb
        # dirty label = label=0 while honest fixtures use label=1
        if mints1 and worldclose and "0" in labels and "1" not in labels:
            # label=0 with honest mint and world-close readings = the N cell
            cell_found = True
            print(f"  !! {cf} looks like the N cell: labels={labels}")
    f5 = not cell_found
    print(f"[fact5] no class combines honest-mint + world-close + dirty-label: {f5}")
    ok &= f5

    print("RESULT:", "ALL-5-FACTS-VERIFIED" if ok else "FACT-CHECK-FAILED")
    return 0 if ok else 1

sys.exit(main())
