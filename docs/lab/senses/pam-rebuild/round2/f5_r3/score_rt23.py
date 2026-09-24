#!/usr/bin/env python3
"""PAM round-3 crew 5: score H-17/H-18/H-19 batteries vs both organs.

For each (organ, battery): assert 3x SHA-identical; assert EVERY
fixture's decision equals the script-side organ expectation (frozen
spec, independent of the binaries); report kill-bar numbers.
"""
import hashlib
import json
import sys

D = "/home/hatch/workspace/tnn-lab/senses/pam-rebuild/round2/f5_r3"
EXC = [(718, 2618), (704, 2642), (713, 2626), (701, 2647), (710, 2632),
       (713, 2627)]
MEM = set()
for ln in open(D + "/true_memory.tsv"):
    p = ln.rstrip("\n").split("\t")
    MEM.add((int(p[0]), int(p[1])))


def blocked(c, m):
    return any(abs(c - ec) <= 150 and abs(m - em) <= 2000 for ec, em in EXC)


def organ_d(c, m):
    if not blocked(c, m):
        return "ALLOWED"
    if any(abs(c - ec) <= 34 and abs(m - em) <= 58 for ec, em in EXC):
        return "WITHHOLD"
    if 650 <= c <= 940 and 2200 <= m <= 6700:
        return "CONFIRM_INSTALL"
    return "WITHHOLD"


def organ_r(c, m):
    if not blocked(c, m):
        return "ALLOWED"
    for c0 in range(c - 5, c + 6):
        for m0 in range(m - 5, m + 6):
            if (c0, m0) in MEM:
                return "CONFIRM_INSTALL"
    return "WITHHOLD"


ORGS = {"d": organ_d, "r": organ_r}
res = {}


def load_battery(org, bat):
    """returns (trials dict fx->(block,dec,delay), delay_x, delay_n)"""
    AD = "%s/attack_%s" % (D, org)
    chunks = []
    if bat in ("a18t", "a18f"):
        for ch in range(3):
            chunks.append("%s/run_%s_%d_" % (AD, bat, ch))
    else:
        chunks.append("%s/run_%s_" % (AD, bat))
    outs = []
    for pre in chunks:
        for i in (1, 2, 3):
            outs.append(open(pre + "%d.out" % i, "rb").read())
    hs = [hashlib.sha256(o).hexdigest() for o in outs]
    # 3 chunks are distinct ledgers (a18*): each chunk's 3 reps must match
    nch = len(chunks)
    for ci in range(nch):
        assert hs[3 * ci] == hs[3 * ci + 1] == hs[3 * ci + 2], (org, bat, ci)
    sha = hs[0][:16]
    trials = {}
    dx = dn = 0
    for pre in chunks:
        txt = open(pre + "1.out").read()
        for ln in txt.split("\n"):
            if not ln.strip():
                continue
            if ln.startswith("DELAYBAR"):
                p = ln.split()
                dx += int(p[1].split("=")[1])
                dn += int(p[2].split("=")[1])
            elif ln[0].isdigit() and "\t" in ln:
                f = ln.split("\t")
                trials[f[1]] = (f[3], f[5], int(f[6]))
    return trials, dx, dn, sha


for org in ORGS:
    AD = "%s/attack_%s" % (D, org)
    expect = json.load(open("%s/expect17.json" % AD))
    for bat in ("a17f", "a17t", "a17b", "a19", "a18t", "a18f"):
        trials, dx, dn, sha = load_battery(org, bat)        # per-fixture assertion vs script expectation
        bad = []
        for fx, e in expect.items():
            if bat == "a18t" and "_A18T_" not in fx:
                continue
            if bat == "a18f" and "_A18F_" not in fx:
                continue
            if bat in ("a17f",) and "_A17F_" not in fx:
                continue
            if bat in ("a17b",) and "_A17B_" not in fx:
                continue
            if bat in ("a19",) and "_A19_" not in fx and "_A19V_" not in fx:
                continue
            if bat == "a17t" and "_A17T_" not in fx and not fx.startswith(
                    "rt4_TMB-5_"):
                continue
            if fx not in trials:
                continue
            exp = ORGS[org](e["conf"], e["meas"])
            got = trials[fx][1] if trials[fx][0] == "BLOCKED" else "ALLOWED"
            if got != exp:
                bad.append((fx, e["conf"], e["meas"], exp, got))
        # a17t's 240 NEAR fixtures are not in expect17; check them too
        if bat == "a17t":
            for fx, (blk, dec, dl) in trials.items():
                if fx in expect:
                    continue
                # find coords from the ledger
                for ln in open("%s/ledger_a17t.txt" % AD):
                    f = ln.rstrip("\n").split("|")
                    if len(f) == 18 and f[4] == fx:
                        c, m = int(f[8]), int(f[10])
                        exp = ORGS[org](c, m)
                        got = dec if blk == "BLOCKED" else "ALLOWED"
                        if got != exp:
                            bad.append((fx, c, m, exp, got))
                        break
        assert not bad, (org, bat, bad[:5])
        res[(org, bat)] = {"n": len(trials), "dx": dx, "dn": dn, "sha": sha,
                           "trials": trials}

print("== H-17/H-18/H-19 results (3x byte-identical; all fixtures match script expectations) ==")
for org in ORGS:
    for bat in ("a17f", "a17t", "a17b", "a19", "a18t", "a18f"):
        r = res[(org, bat)]
        tr = r["trials"]
        fi = sum(1 for (b, d, _) in tr.values() if d == "CONFIRM_INSTALL")
        wh = sum(1 for (b, d, _) in tr.values() if d == "WITHHOLD")
        print("organ %s %s: n=%d install=%d withhold=%d delay=%d/%d=%.1f%% sha=%s"
              % (org.upper(), bat, r["n"], fi, wh, r["dx"], r["dn"],
                 100.0 * r["dx"] / r["dn"] if r["dn"] else 0, r["sha"]))

print("== kill bars ==")
for org in ORGS:
    r = res[(org, "a17f")]
    fi = sum(1 for (b, d, _) in r["trials"].values()
             if d == "CONFIRM_INSTALL")
    print("H-17 organ %s A17F: %d/60 installed -> %s (bar >=50%%)"
          % (org.upper(), fi, "KILL" if fi >= 30 else "survive"))
    r = res[(org, "a17t")]
    frac = r["dx"] / r["dn"]
    print("H-17 organ %s A17T-mixed delay: %d/%d=%.1f%% -> %s (bar >25%%)"
          % (org.upper(), r["dx"], r["dn"], 100 * frac,
             "KILL" if frac > 0.25 else "survive"))
    r = res[(org, "a17b")]
    fi = sum(1 for (b, d, _) in r["trials"].values()
             if d == "CONFIRM_INSTALL")
    print("H-17 organ %s A17B: %d/8 nearest-release points install (diagnostic)"
          % (org.upper(), fi))
    for bat in ("a18t", "a18f"):
        r = res[(org, bat)]
        if bat == "a18t":
            frac = r["dx"] / r["dn"]
            verdict = "KILL" if frac > 0.25 else "survive"
            print("H-18 organ %s true-flood delay: %d/%d=%.1f%% -> %s (bar >25%%)"
                  % (org.upper(), r["dx"], r["dn"], 100 * frac, verdict))
        else:
            fi = sum(1 for (b, d, _) in r["trials"].values()
                     if d == "CONFIRM_INSTALL")
            frac = fi / r["n"]
            verdict = "KILL" if frac > 0.25 else "survive"
            print("H-18 organ %s false-flood install: %d/%d=%.1f%% -> %s (bar >25%% install)"
                  % (org.upper(), fi, r["n"], 100 * frac, verdict))
    r = res[(org, "a19")]
    fi = sum(1 for (b, d, _) in r["trials"].values()
             if d == "CONFIRM_INSTALL")
    print("H-19 organ %s rescue-hijack: %d/60 installed -> %s (bar >=50%%)"
          % (org.upper(), fi, "KILL" if fi >= 30 else "survive"))

json.dump({k[0] + "/" + k[1]: {"n": v["n"], "dx": v["dx"], "dn": v["dn"],
                               "sha": v["sha"]}
          for k, v in res.items()},
          open(D + "/score_rt23.json", "w"), indent=1, sort_keys=True)
print("score written to score_rt23.json")
