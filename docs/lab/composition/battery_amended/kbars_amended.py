#!/usr/bin/env python3
"""K1-K6 adjudication UNDER THE AMENDED BARS (A1-A6).

Reads SUMMARY lines from the scripted chance arms (null, singlerule,
wrongord — A1) and the blind-scored learner run. Deterministic.

Amended bars:
 - chance = max(NULL, SINGLE-RULE, WRONG-ORDER) true output-correct on the
   amended instrument; K1 kills at <= chance + 0.10 (A1).
 - K2..K6 per frozen §7; K6 scoped to bigram-clean covered pairs computed
   under the SALTED generator (A4) — covered set passed in via --covered.
 - REPORTING RULE (Crew C, binding): K1 is always reported WITH K2; when K2
   voids, the void is the operative verdict.
"""
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
    return d, txt

def frac(s):
    if "/" in s:
        a, b = s.split("/")
        return int(a), int(b)
    return int(s), None

def main():
    bindir = os.path.join(WORK, "..", "cd_build_placeholder")
    # paths
    L, Ltxt = summary(os.path.join(WORK, sys.argv[1]))          # learner.out
    N, _ = summary(os.path.join(WORK, "null.out"))
    S, _ = summary(os.path.join(WORK, "singlerule.out"))
    W, _ = summary(os.path.join(WORK, "wrongord.out"))

    n_true, n_tot = frac(N["trueacc"])
    s_true, s_tot = frac(S["trueacc"])
    w_true, w_tot = frac(W["trueacc"])
    rates = {"null": n_true / n_tot, "singlerule": s_true / s_tot,
             "wrongord": w_true / w_tot}
    chance = max(rates.values())
    binding = max(rates, key=rates.get)
    k1_line = chance + 0.10

    c_acc, c_tot = frac(L["composition"])
    combo_acc = c_acc / c_tot
    l_true, _ = frac(L["trueacc"])
    k1_kill = combo_acc <= k1_line

    a_n, _ = frac(L["A"]); b_n, _ = frac(L["B"])
    k2_frac = a_n / c_tot
    k2_void = k2_frac > 0.50
    n_fail = c_tot - int(L["ok"])
    k3 = (b_n / n_fail > 0.50) if n_fail else False

    rf_n, rf_tot = frac(L["reflex"])
    reflex_rate = rf_n / rf_tot
    k4 = reflex_rate > 0.20

    interf = [l for l in Ltxt.splitlines() if l.startswith("INTERF")]
    k5 = len(interf) > 0

    ok_n = int(L["ok"])

    print("=== K1-K6 under AMENDED bars (A1-A6) ===")
    print(f"chance arms (trueacc): null={N['trueacc']} singlerule={S['trueacc']} "
          f"wrongord={W['trueacc']}")
    print(f"  -> chance={chance:.4f} (binding arm: {binding}); K1 line={k1_line:.4f}")
    print(f"K1: combo_acc={c_acc}/{c_tot}={combo_acc:.4f} <= {k1_line:.4f} ? "
          f"{'YES -> composition claim KILLED' if k1_kill else 'NO -> claim survives'}")
    print(f"K2: (a) fraction={a_n}/{c_tot}={k2_frac:.4f} > 0.50 ? "
          f"{'YES -> battery VOID (OPERATIVE VERDICT)' if k2_void else 'NO'}")
    print(f"  [reporting rule: K1 kill is presented WITH the K2 void]")
    print(f"K3: (b)={b_n} of {n_fail} failures = "
          f"{(b_n/n_fail if n_fail else 0):.4f} > 0.50 ? "
          f"{'YES -> retrieval-failure finding' if k3 else 'NO'}")
    print(f"K4: reflex rate={rf_n}/{rf_tot}={reflex_rate:.4f} > 0.20 ? "
          f"{'YES -> reflex defect CONFIRMED' if k4 else 'NO defect'}")
    print(f"K5: INTERF lines={len(interf)} -> "
          f"{'interference CONFIRMED: ' + '; '.join(interf) if k5 else 'no pair meets criterion'}")
    print(f"K6: combo successes (ok)={ok_n} on covered pairs -> "
          f"{'red-team memorization check applies' if ok_n else 'VACUOUS (zero successes)'}")
    print(f"  (covered-pair set computed under salted generator: see audit)")

if __name__ == "__main__":
    main()
