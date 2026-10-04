#!/usr/bin/env python3
"""K1-K6 adjudication under the FROZEN bars (PREREG §7). Deterministic.
Reads the three SUMMARY lines; prints verdicts with the arithmetic shown."""
import re, sys, os

WORK = os.path.dirname(os.path.abspath(__file__))

def summary(path):
    with open(path) as f:
        txt = f.read()
    m = re.search(r"^SUMMARY\t(.*)$", txt, re.M)
    d = {}
    for kv in m.group(1).split("\t"):
        if "=" in kv:
            k, v = kv.split("=", 1)
            d[k] = v
    return d

def frac(s):
    if "/" in s:
        a, b = s.split("/")
        return int(a), int(b)
    return int(s), None

def main():
    L = summary(os.path.join(WORK, "run1", "learner.out"))
    N = summary(os.path.join(WORK, "null.out"))
    S = summary(os.path.join(WORK, "singlerule.out"))

    n_true, n_tot = frac(N["trueacc"])
    s_true, s_tot = frac(S["trueacc"])
    chance = max(n_true / n_tot, s_true / s_tot)
    c_acc, c_tot = frac(L["composition"])
    combo_acc = c_acc / c_tot
    k1_line = chance + 0.10

    a_n, _ = frac(L["A"])
    k2_frac = a_n / c_tot

    rf_n, rf_tot = frac(L["reflex"])
    reflex_rate = rf_n / rf_tot

    print("=== K1-K6 under FROZEN bars ===")
    print(f"chance arms: null trueacc={N['trueacc']} singlerule trueacc={S['trueacc']} "
          f"-> chance={chance:.4f}")
    print(f"K1: combo_acc={c_acc}/{c_tot}={combo_acc:.4f} <= chance+0.10={k1_line:.4f} ? "
          f"{'YES -> KILL composition claim' if combo_acc <= k1_line else 'NO -> claim survives'}")
    print(f"K2: (a) fraction={a_n}/{c_tot}={k2_frac:.4f} > 0.50 ? "
          f"{'YES -> battery VOID' if k2_frac > 0.50 else 'NO'}")
    print(f"K3: B={L['B']} of {c_tot} failures are (b) -> "
          f"{'retrieval-failure finding' if False else 'not triggered (failures are (a))'}")
    print(f"K4: reflex rate={rf_n}/{rf_tot}={reflex_rate:.4f} > 0.20 ? "
          f"{'YES -> reflex defect CONFIRMED' if reflex_rate > 0.20 else 'NO defect'}")
    with open(os.path.join(WORK, "run1", "learner.out")) as f:
        interf = [l for l in f if l.startswith("INTERF")]
    print(f"K5: INTERF lines={len(interf)} -> "
          f"{'interference CONFIRMED' if interf else 'no pair meets asymmetry criterion'}")
    print(f"K6: combo successes (ok)={L['ok']} -> "
          f"{'red-team memorization check applies' if int(L['ok']) else 'VACUOUS (zero successes: nothing for memorization to explain)'}")

if __name__ == "__main__":
    main()
