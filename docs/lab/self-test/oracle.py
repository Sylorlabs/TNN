#!/usr/bin/env python3
"""Independent oracle for the self-test TNN experiment.

Reimplements (independently, in Python) the frozen data formulas, the learner
mechanism, and the preregistered bar rules. Parses the Zag binary's output and
checks every kill bar. Shares no code with selftest.zag.
"""
import hashlib
import re
import sys

# ---------- frozen data spec (SELFTEST_PREREG.md) ----------
def truth(f, salt):
    return (((f + salt) * 7919 + 13) % 100003)

def flie(f, salt):
    return truth(f, salt) + 1 + (((f + salt) * 37) % 89)

# ---------- independent learner-mechanism reimplementation ----------
def compete(f, salt, ck):
    """Trust-weighted competition. Returns (status, value)."""
    t, l = truth(f, salt), flie(f, salt)
    if ck == 0:   # flaw: truth@100, lie@40
        cands = [(t, 100), (l, 40)]
    elif ck == 1:  # contra2v1: lie@100 first, truth@100 x2
        cands = [(l, 100), (t, 100), (t, 100)]
    elif ck == 2:  # tie: lie@100, truth@100
        cands = [(l, 100), (t, 100)]
    else:
        raise ValueError(ck)
    sums = {}
    for v, tr in cands:
        sums[v] = sums.get(v, 0) + tr
    best = max(sums.values())
    winners = [v for v, s in sums.items() if s == best]
    if len(winners) > 1:
        return (2, None)  # withheld
    return (1, winners[0])

def expected_obs(batt, variant):
    salt = variant * 1000
    if batt == "B1":
        return sum(1 for f in range(240))  # quiet teach: all installed, all true
    if batt == "B2":
        return 12  # 12 falsehoods taught consistently -> absorbed
    if batt == "B3":
        n = 0
        for f in range(96):
            st, v = compete(f, salt, 0)
            if st == 1 and v == truth(f, salt):
                n += 1
        return n
    if batt == "B4":
        n = 0
        for f in range(48):
            st, v = compete(f, salt, 1)
            if st == 1 and v == truth(f, salt):
                n += 1
        return n
    if batt == "B5":
        return 0
    if batt == "B6":
        return 1  # digest equality is self-contained; binary asserts it
    if batt == "T1":
        return 239  # fact 239 never taught
    if batt == "T4":
        n = 0
        for f in range(47):
            st, v = compete(f, salt, 1)
            if st == 1 and v == truth(f, salt):
                n += 1
        st, v = compete(47, salt, 2)  # tie -> withheld, not counted
        assert st == 2
        return n
    raise ValueError(batt)

# (bar, is_equality_bar)
BARS = {
    "B1": (236, False), "B2": (12, True), "B3": (92, False), "B4": (46, False),
    "B5": (0, False), "B6": (1, False), "T1": (240, False), "T4": (48, False),
}

def expected_verdict(batt, obs):
    if batt == "B5":
        return 3  # UNRUNNABLE
    bar, iseq = BARS[batt]
    if iseq:
        return 0 if obs == bar else 1
    return 0 if obs >= bar else 1

# ---------- parse + adjudicate ----------
VRE = re.compile(r"ST_VERDICT,batt=(\w+),var=(\d+),obs=(-?\d+),bar=(\d+),verdict=(\d+)")
MRE = re.compile(
    r"ST_MANIFEST,total=(\d+),pass=(\d+),trip=(\d+),unrunnable=(\d+),error=(\d+),"
    r"bat_ops=(\d+),orch_ops=(\d+),audit_records=(\d+)")

def check_file(path, nvar):
    txt = open(path).read()
    verdicts = VRE.findall(txt)
    m = MRE.search(txt)
    fails = []

    # KB-ST-AUTO / KB-ST-SKIP: manifest coverage, one process, no silent skips
    want = {(b, v) for b in BARS for v in range(nvar)}
    got = {(b, int(v)) for b, v, o, br, vc in verdicts}
    if got != want:
        fails.append(f"COVERAGE: missing={sorted(want-got)} extra={sorted(got-want)}")
    if len(verdicts) != len(want):
        fails.append(f"COUNT: {len(verdicts)} verdict lines, expected {len(want)}")
    if "ST_DONE" not in txt:
        fails.append("ST_DONE missing (anti-skip gate blocked or crash)")
    if "ST_BLOCKED" in txt:
        fails.append("ST_BLOCKED present")

    # KB-ST-FIDELITY: obs and verdict match the independent expectation
    for b, v, o, br, vc in verdicts:
        v, o, br, vc = int(v), int(o), int(br), int(vc)
        eo = expected_obs(b, v)
        if o != eo:
            fails.append(f"OBS {b} var={v}: binary={o} oracle={eo}")
        ev = expected_verdict(b, eo)
        if vc != ev:
            fails.append(f"VERDICT {b} var={v}: binary={vc} oracle={ev}")
        eb, _ = BARS[b]
        if br != eb:
            fails.append(f"BAR {b}: binary={br} prereg={eb}")

    # KB-ST-OVERHEAD + manifest tallies
    if not m:
        fails.append("ST_MANIFEST missing")
    else:
        total, npass, ntrip, nunrun, nerr, bat_ops, orch_ops, an = map(int, m.groups())
        if total != 8 * nvar:
            fails.append(f"MANIFEST total={total}")
        ev_pass = sum(1 for b in BARS for v in range(nvar)
                      if expected_verdict(b, expected_obs(b, v)) == 0)
        ev_trip = sum(1 for b in BARS for v in range(nvar)
                      if expected_verdict(b, expected_obs(b, v)) == 1)
        ev_unr = sum(1 for b in BARS for v in range(nvar)
                      if expected_verdict(b, expected_obs(b, v)) == 3)
        if (npass, ntrip, nunrun, nerr) != (ev_pass, ev_trip, ev_unr, 0):
            fails.append(f"TALLY binary={(npass,ntrip,nunrun,nerr)} "
                         f"oracle={(ev_pass,ev_trip,ev_unr,0)}")
        if an != 8 * nvar:
            fails.append(f"AUDIT records={an}, expected {8*nvar}")
        if orch_ops > 2 * bat_ops:
            fails.append(f"OVERHEAD {orch_ops} > 2*{bat_ops}")
        print(f"  overhead: orch_ops={orch_ops} bat_ops={bat_ops} "
              f"ratio={orch_ops/bat_ops:.4f} (bar: <=2.0)")
    return fails

def main():
    scale, nvar, files = sys.argv[1], int(sys.argv[2]), sys.argv[3:]
    all_fails = []
    md5s = set()
    for f in files:
        md5s.add(hashlib.md5(open(f, "rb").read()).hexdigest())
        fails = check_file(f, nvar)
        tag = "FAIL" if fails else "ok"
        print(f"[{tag}] {f}")
        all_fails += [f"{f}: {x}" for x in fails]
    # KB-ST-DET
    if len(md5s) == 1:
        print(f"  determinism: {len(files)}/{len(files)} byte-identical ({next(iter(md5s))[:12]}...)")
    else:
        all_fails.append(f"DETERMINISM: {len(md5s)} distinct md5s: {sorted(md5s)}")
    if all_fails:
        print("\nFAILURES:")
        for x in all_fails:
            print("  " + x)
        sys.exit(1)
    print(f"\nALL KILL BARS HOLD ({scale}, {nvar*8} batteries x {len(files)} reps)")

if __name__ == "__main__":
    main()
