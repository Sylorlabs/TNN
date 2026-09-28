#!/usr/bin/env python3
"""Independent checker for the C7 Direction 3+1 head-on test
(PREREG 2026-09-20-C7-DIRECTION-3PLUS1 §4-§5).

Re-derives every verdict from the raw evidence logs with logic written
independently of the Zag trial code (separate implementation, separate
language). Verifies kill bars K1-K6.

Usage:
    check_c7_3plus1.py <baseline_dir> <candidate_dir>
  baseline_dir = Run A (pristine committed sources)
  candidate_dir = Run B (Direction 3+1 sources)
Exit 0 iff every check passes; prints a verdict report either way.
"""
import os, re, sys, hashlib, subprocess

COMMITTED_C7_TELEMETRY = ("C7_TELEMETRY,old4,862,old5,258,cons4,604,cons5,0,"
                          "cap4,914,cap5,897")

def fail(msg, state):
    state["fails"].append(msg)
    print("FAIL:", msg)

def ok(msg):
    print("ok:", msg)

def parse_checks(path):
    out = {}
    with open(path) as f:
        for line in f:
            m = re.match(r"^CHECK,([^,]+),(-?\d+),(-?\d+)\s*$", line)
            if m:
                out[m.group(1)] = (int(m.group(2)), int(m.group(3)))
    return out

def grep1(pat, path):
    with open(path) as f:
        txt = f.read()
    m = re.search(pat, txt, flags=re.M)
    return m

def strip_comments(text):
    return re.sub(r"//.*$", "", text, flags=re.M)

def main():
    base, cand = sys.argv[1], sys.argv[2]
    state = {"fails": []}

    # ---- 1. stage logs: every CHECK actual == expected; paired files exist ----
    for ev, tag in [(base, "A"), (cand, "B")]:
        total = 0
        for s in range(6):
            p = os.path.join(ev, f"s{s}_a.log")
            if not os.path.exists(p):
                fail(f"run{tag}: missing {p}", state); continue
            checks = parse_checks(p)
            for name, (a, e) in checks.items():
                total += 1
                if a != e:
                    fail(f"run{tag} s{s}: CHECK {name} actual={a} expected={e}",
                         state)
            for req in ["stage_gate", "ledger_replay", "p1", "p2", "p3", "p4",
                        "p5", "p6", "p7", "p8", "p9", "p10",
                        "p2_drop_ceiling", "q2_pin_alarm", "sizing_ok"]:
                if req not in checks:
                    fail(f"run{tag} s{s}: missing CHECK {req}", state)
        if total == 0:
            fail(f"run{tag}: no stage CHECK lines parsed", state)
        else:
            ok(f"run{tag}: stage CHECK lines all pass ({total})")

    # ---- 2. K5a: Run A reproduces the committed S10 evidence ----
    m = grep1(r"^(C7_TELEMETRY,old4,\d+,old5,\d+,cons4,\d+,cons5,\d+,"
              r"cap4,\d+,cap5,\d+)\s*$", os.path.join(base, "controls.log"))
    if not m:
        fail("runA: C7_TELEMETRY line missing", state)
    elif m.group(1) != COMMITTED_C7_TELEMETRY:
        fail(f"runA: C7_TELEMETRY != committed evidence:\n  got {m.group(1)}",
             state)
    else:
        ok("K5a: runA C7_TELEMETRY byte-equals committed S10 evidence")
    cc_a = parse_checks(os.path.join(base, "controls.log"))
    if cc_a.get("c7_withdrawal") != (1, 0):
        fail(f"runA: CHECK c7_withdrawal != (1,0): "
             f"{cc_a.get('c7_withdrawal')}", state)
    else:
        ok("K5a: runA reproduces §5 FAIL (c7_withdrawal 1,0)")

    # ---- 3. K2: regression — runB vs runA ----
    # 3a. stage logs byte-identical
    stage_diff = 0
    for s in range(6):
        for rep in "ab":
            pa = os.path.join(base, f"s{s}_{rep}.log")
            pb = os.path.join(cand, f"s{s}_{rep}.log")
            if open(pa, "rb").read() != open(pb, "rb").read():
                fail(f"K2: stage log s{s}_{rep} differs runA vs runB", state)
                stage_diff += 1
    if stage_diff == 0:
        ok("K2: all stage logs byte-identical runA vs runB")
    # 3b. bites byte-identical
    bite_diff = 0
    for name in ["pbite.log", "cbite.log"]:
        if open(os.path.join(base, name), "rb").read() != \
           open(os.path.join(cand, name), "rb").read():
            fail(f"K2: {name} differs runA vs runB", state)
            bite_diff += 1
    if bite_diff == 0:
        ok("K2: pbite + cbite logs byte-identical runA vs runB")
    # 3c. controls CHECK lines: identical names+values except c7_withdrawal
    cc_b = parse_checks(os.path.join(cand, "controls.log"))
    if set(cc_a) != set(cc_b):
        fail(f"K2: controls CHECK-name sets differ: "
             f"onlyA={set(cc_a)-set(cc_b)} onlyB={set(cc_b)-set(cc_a)}", state)
    else:
        ok("K2: controls CHECK-name sets identical")
        for name in cc_a:
            if name == "c7_withdrawal":
                if cc_b[name] != (0, 0):
                    fail(f"K2: c7_withdrawal runB != (0,0): {cc_b[name]}",
                         state)
                else:
                    ok("K2: c7_withdrawal 1,0 -> 0,0 (predicted flip)")
            elif cc_a[name] != cc_b[name]:
                fail(f"K2: controls CHECK {name} changed "
                     f"{cc_a[name]} -> {cc_b[name]}", state)
        if not any("K2: controls CHECK" in f for f in state["fails"]):
            ok("K2: all other controls CHECK lines unchanged")
    # 3d. C7_TELEMETRY byte-equal in runB too (behavior-neutrality, K5b)
    m = grep1(r"^(C7_TELEMETRY,old4,\d+,old5,\d+,cons4,\d+,cons5,\d+,"
              r"cap4,\d+,cap5,\d+)\s*$", os.path.join(cand, "controls.log"))
    if not m:
        fail("runB: C7_TELEMETRY line missing", state)
    elif m.group(1) != COMMITTED_C7_TELEMETRY:
        fail(f"K5b: runB C7_TELEMETRY != committed:\n  got {m.group(1)}",
             state)
    else:
        ok("K5b: runB C7_TELEMETRY byte-equals committed evidence "
           "(mechanism untouched)")
    # 3e. new head-on lines present in runB
    ctxt = open(os.path.join(cand, "controls.log")).read()
    for tag in ["C7_COMP4,", "C7_COMP5,", "C7_NEW,", "C7_LEGACY_VERDICT,",
                "C7_POSCTRL,", "C7_POSCTRL_LEGACY,", "C7_POSCTRL_COMP4D,",
                "C7_POSCTRL_COMP5D,"]:
        if tag not in ctxt:
            fail(f"runB: missing head-on line {tag}", state)
    else:
        ok("runB: all head-on telemetry lines present")
    if "C7_DUALISM_TRIPWIRE" in ctxt:
        print("note: C7_DUALISM_TRIPWIRE fired (cap5n > cap4n) — "
              "investigate per PREREG §2")

    # ---- 4. Head-on 2x2 ablation, re-derived from components (K1, K4) ----
    def comp(prefix):
        m = grep1(rf"^{prefix},(\d+),(\d+),(\d+),(\d+)\s*$",
                  os.path.join(cand, "controls.log"))
        if not m:
            fail(f"runB: {prefix} line missing/unparseable", state)
            return None
        return tuple(int(g) for g in m.groups())  # cok,ccon,mhyp,opened
    c4, c5 = comp("C7_COMP4"), comp("C7_COMP5")
    d4, d5 = comp("C7_POSCTRL_COMP4D"), comp("C7_POSCTRL_COMP5D")
    if c4 and c5:
        cok4, ccon4, mhyp4, op4 = c4
        cok5, ccon5, mhyp5, op5 = c5
        cap_old4 = cok4 + ccon4 + mhyp4 + op4
        cap_old5 = cok5 + ccon5 + mhyp5 + op5
        cap_new4 = cok4 + ccon4 + mhyp4
        cap_new5 = cok5 + ccon5 + mhyp5
        # K1: double-count eliminated <=> cap_new == cap_old - opened
        if not (cap_new4 == cap_old4 - op4 and cap_new5 == cap_old5 - op5):
            fail("K1: cap_new != cap_old - l1_opened", state)
        else:
            ok(f"K1: double-count eliminated "
               f"(cap_new = cap_old - opened: {cap_old4}-{op4}={cap_new4}, "
               f"{cap_old5}-{op5}={cap_new5})")
        # cross-check: legacy values match the telemetry line
        if (cap_old4, cap_old5) != (914, 897):
            fail(f"K1: legacy cap {cap_old4}->{cap_old5} != 914->897", state)
        else:
            ok("K1: legacy metric reproduces committed 914->897")
        # cross-check: C7_NEW line matches re-derivation
        mn = grep1(r"^C7_NEW,cap4n,(\d+),cap5n,(\d+)\s*$",
                   os.path.join(cand, "controls.log"))
        if not mn or (int(mn.group(1)), int(mn.group(2))) != \
                (cap_new4, cap_new5):
            fail("runB: C7_NEW line != re-derived cap_new", state)
        else:
            ok(f"C7_NEW line matches re-derivation "
               f"({cap_new4}->{cap_new5})")
        # 2x2 ablation
        cells = {
            "old-metric x old-bar(==)": (cap_old5 == cap_old4),
            "old-metric x new-bar(>=)": (cap_old5 >= cap_old4),
            "new-metric x old-bar(==)": (cap_new5 == cap_new4),
            "new-metric x new-bar(>=)": (cap_new5 >= cap_new4),
        }
        expect = {
            "old-metric x old-bar(==)": False,   # §5 FAIL reproduced
            "old-metric x new-bar(>=)": False,   # direction 1 alone: fires
            "new-metric x old-bar(==)": True,    # direction 3 alone: unblocks
            "new-metric x new-bar(>=)": True,    # redesign: UNBLOCKED
        }
        print("--- 2x2 ablation (metric x bar), intact arms ---")
        for cell, alive in cells.items():
            want = expect[cell]
            mark = "ALIVE" if alive else "FIRED"
            print(f"  {cell}: {mark} (predicted "
                  f"{'ALIVE' if want else 'FIRED'})")
            if alive != want:
                fail(f"ablation cell mismatch: {cell}", state)
        # legacy verdict line must preserve the §5 FAIL
        ml = grep1(r"^C7_LEGACY_VERDICT,(\d+)\s*$",
                   os.path.join(cand, "controls.log"))
        if not ml or int(ml.group(1)) != 1:
            fail("runB: C7_LEGACY_VERDICT != 1 (§5 FAIL not preserved)",
                 state)
        else:
            ok("§5 FAIL preserved as labeled telemetry "
               "(C7_LEGACY_VERDICT=1)")
        # K4: redesigned verdict
        if cc_b.get("c7_withdrawal") != (0, 0):
            fail("K4: CHECK c7_withdrawal != (0,0) under redesign", state)
        else:
            ok(f"K4: C7 UNBLOCKED under redesign "
               f"({cap_new4}->{cap_new5}, cap5>=cap4)")

    # ---- 5. K3: positive control convicts under BOTH metrics ----
    # NOTE: the in-binary teacher-dependent arms keep the default gate, so
    # dep4 carries the same 17 forced (refusal-fed) hypotheses as intact
    # DC-4 (opened=17); the teacher refusal (SEAM_REFUSED_TEACHER) is never
    # routed to L1. Expected: dep4 new/old = 897/914, dep5 = 641/641.
    if d4 and d5:
        for tag, dd, want_new, want_old in [
                ("dep4", d4, 897, 914), ("dep5", d5, 641, 641)]:
            n = dd[0] + dd[1] + dd[2]
            o = n + dd[3]
            if (n, o) != (want_new, want_old):
                fail(f"K3: {tag} new/old = {n}/{o}, want "
                     f"{want_new}/{want_old}", state)
        mp = grep1(r"^C7_POSCTRL,cap4d,(\d+),cap5d,(\d+)\s*$",
                   os.path.join(cand, "controls.log"))
        mpl = grep1(r"^C7_POSCTRL_LEGACY,cap4d,(\d+),cap5d,(\d+)\s*$",
                    os.path.join(cand, "controls.log"))
        if not mp or (int(mp.group(1)), int(mp.group(2))) != (897, 641):
            fail("runB: C7_POSCTRL != 897->641", state)
        elif not mpl or (int(mpl.group(1)), int(mpl.group(2))) != (914, 641):
            fail("runB: C7_POSCTRL_LEGACY != 914->641", state)
        else:
            ok("K3: positive control convicts under BOTH metrics "
               "(new 897->641; legacy 914->641)")
        # decomposition: collapse must be in composites_ok; hypotheses flat
        if d4[0] - d5[0] != 256 or d4[2] != d5[2]:
            fail("K3: control collapse not composites-only "
                 f"(dep4 {d4} dep5 {d5})", state)
        else:
            ok("K3: collapse decomposition = composites_ok 256->0, "
               "hypotheses 639=639 (forced 17 counted once in dep4)")

    # ---- 6. K5c: paired determinism + rebuild ----
    for ev, tag in [(base, "A"), (cand, "B")]:
        dp = os.path.join(ev, "determinism.txt")
        det = open(dp).read().strip().split("\n")
        if len(det) != 6 or any(not l.endswith(":IDENTICAL") for l in det):
            fail(f"K5: run{tag} paired determinism broken: {det}", state)
        else:
            ok(f"K5: run{tag} paired reruns byte-identical 6/6")
        bsha = open(os.path.join(ev, "binary.sha256")).read().split()[0]
        lab = os.path.expanduser("~/workspace/tnn-lab")
        src = {"A": os.path.join(lab, "wave9/integration/impl"),
               "B": os.path.join(lab, "wave12/integration-c7/impl")}[tag]
        znc = os.path.expanduser("~/workspace/tnn-lab/toolchain/bin/"
                                 "znc_linux_x86_64_abed8aa1")
        rb = os.path.join(ev, "rebuild_check.bin")
        r = subprocess.run([znc, os.path.join(src, "main.zag"), "-o", rb],
                           capture_output=True, timeout=900)
        if r.returncode != 0:
            fail(f"K5: run{tag} rebuild failed", state)
        else:
            h = hashlib.sha256(open(rb, "rb").read()).hexdigest()
            if h != bsha:
                fail(f"K5: run{tag} rebuild SHA {h[:16]} != trial {bsha[:16]}",
                     state)
            else:
                ok(f"K5: run{tag} rebuild byte-identical "
                   f"(sha256 {bsha[:16]}...)")
            os.remove(rb)

    # ---- 7. K6: zero RNG + G0b ----
    for tag in ["A", "B"]:
        lab = os.path.expanduser("~/workspace/tnn-lab")
        src = {"A": os.path.join(lab, "wave9/integration/impl"),
               "B": os.path.join(lab, "wave12/integration-c7/impl")}[tag]
        rng_toks = ["rand", "srand", "getrandom", "RDRAND", "_zag_rand"]
        hits = []
        for root, _, files in os.walk(src):
            for fn in files:
                if not fn.endswith(".zag"):
                    continue
                txt = strip_comments(open(os.path.join(root, fn)).read())
                for t in rng_toks:
                    for m in re.finditer(r"(?<![A-Za-z0-9_])" +
                                         re.escape(t) + r"(?![A-Za-z0-9_])",
                                         txt):
                        hits.append((fn, t))
        if hits:
            fail(f"K6: run{tag} RNG tokens in sources: {hits[:5]}", state)
        else:
            ok(f"K6: run{tag} zero RNG in trial sources")
        g0b = open(os.path.join({"A": base, "B": cand}[tag],
                                "g0b_hits.txt")).read().strip().split("\n")
        if len(g0b) != 1 or "seam.zag" not in g0b[0]:
            fail(f"K6: run{tag} G0b gate broken: {g0b}", state)
        else:
            ok(f"K6: run{tag} G0b single call site holds")

    print("=" * 60)
    if state["fails"]:
        print(f"CHECKER VERDICT: FAIL ({len(state['fails'])} failures)")
        return 1
    print("CHECKER VERDICT: PASS — K1-K6 all hold; C7 UNBLOCKED under the "
          "redesigned instrument (tap still required per PREREG §7)")
    return 0

if __name__ == "__main__":
    sys.exit(main())
