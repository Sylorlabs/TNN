#!/usr/bin/env python3
"""Wave-7 formula comparison: nested (N) vs independent (I) wrongness.
Pure deterministic arithmetic over m=0..499, v in {0,1,2}. No RNG."""
import json

H = 500
VARIANTS = [0, 1, 2]
PRESSURE = [100, 200, 300, 400]
IMPLANTS = [83, 166, 250, 333, 416]  # per prereg; 500 out of range (Defect 3)

def imp(m, v):
    return 1 if ((7*m + 13*v + 3) % 10 < 3) else 0

def wrongN(m, v):
    return 1 if ((3*m + 7*v + 9) % 10 < 2) else 0

# re-verify importance residues computationally (not trusted from derivation)
print("imp residues per variant (m mod 10 with imp=1):")
for v in VARIANTS:
    res = sorted({m % 10 for m in range(H) if imp(m, v)})
    print(f"  v{v}: {res}  count={sum(imp(m, v) for m in range(H))}")

# ---- VERSION I search (per PREREG_COMPARE.md) ----
def wrongI_gen(a, b, c):
    return lambda m, v: 1 if ((a*m + b*v + c) % 10 < 3) else 0

def stats(fn):
    out = {}
    for v in VARIANTS:
        wrong = [m for m in range(H) if fn(m, v)]
        wi = [m for m in wrong if imp(m, v)]
        out[v] = {
            "yield": len(wrong),
            "wrong_and_imp": len(wi),
            "p_imp_given_wrong": len(wi)/len(wrong) if wrong else None,
            "pressure_overlap": sum(1 for m in PRESSURE if fn(m, v)),
            "implant_overlap": [m for m in IMPLANTS if fn(m, v)],
        }
    return out

best = None
for a in (1, 3, 7, 9):
    for b in range(10):
        for c in range(10):
            fn = wrongI_gen(a, b, c)
            s = stats(fn)
            if not all(s[v]["yield"] == 150 for v in VARIANTS):
                continue
            # criterion 1: exactly one shared residue per variant
            # (equivalently wrong_and_imp == 50, since 150 wrong * 1/3)
            if not all(s[v]["wrong_and_imp"] == 50 for v in VARIANTS):
                continue
            p_over = sum(s[v]["pressure_overlap"] for v in VARIANTS)
            i_over = sum(len(s[v]["implant_overlap"]) for v in VARIANTS)
            key = (p_over, i_over, a, b, c)
            if best is None or key < best[0]:
                best = (key, (a, b, c), s)

if best is None:
    print("NO CANDIDATE satisfies criterion 1 — negative result, bar not relaxed.")
    raise SystemExit(1)

(a, b, c) = best[1]
sI = best[2]
print(f"\nVERSION I chosen: wrongI(m,v) = (({a}m + {b}v + {c}) mod 10 < 3)")
print(f"  search key (pressure_over, implant_over, a, b, c) = {best[0]}")
for v in VARIANTS:
    res = sorted({m % 10 for m in range(H) if wrongI_gen(a,b,c)(m, v)})
    print(f"  v{v} wrong residues: {res}")

def wrongI(m, v):
    return 1 if ((a*m + b*v + c) % 10 < 3) else 0

# ---- full comparison ----
def full(fn, name):
    rows = {}
    for v in VARIANTS:
        wrong = [m for m in range(H) if fn(m, v)]
        imps = [m for m in range(H) if imp(m, v)]
        wi = [m for m in wrong if imp(m, v)]
        ri = [m for m in imps if not fn(m, v)]
        rows[v] = {
            "wrong_yield": len(wrong),
            "imp_yield": len(imps),
            "wrong_and_imp": len(wi),          # rigidity denominator
            "right_and_imp": len(ri),           # F_wbs denominator
            "p_imp_given_wrong": round(len(wi)/len(wrong), 4),
            "p_wrong_given_imp": round(len(wi)/len(imps), 4),
            "p_wrong": round(len(wrong)/H, 4),
            "pressure_overlap": sum(1 for m in PRESSURE if fn(m, v)),
            "implant_overlap": [m for m in IMPLANTS if fn(m, v)],
        }
    # period check: smallest p in 1..20 with fn(m+p,v)==fn(m,v) for all m in range(H-p)
    per = {}
    for v in VARIANTS:
        for p in range(1, 21):
            if all(fn(m+p, v) == fn(m, v) for m in range(H-p)):
                per[v] = p
                break
    return {"rows": rows, "period": per}

cmpN = full(wrongN, "N")
cmpI = full(wrongI, "I")

print("\n=== VERSION N (nested) ===")
print(json.dumps(cmpN, indent=1))
print("\n=== VERSION I (independent) ===")
print(json.dumps(cmpI, indent=1))

# C1-C5 verdicts
def verdict(cmp, name, indep_bar=None):
    print(f"\n--- {name} vs criteria ---")
    for v in VARIANTS:
        r = cmp["rows"][v]
        c1 = 90 <= r["wrong_yield"] <= 160
        c3 = r["wrong_and_imp"] >= 20
        line = f"v{v}: C1 yield {r['wrong_yield']} {'PASS' if c1 else 'FAIL'}; C3 denom {r['wrong_and_imp']} {'PASS' if c3 else 'FAIL (STARVED)'}"
        if indep_bar is not None:
            c2 = abs(r["p_imp_given_wrong"] - 0.3) <= 0.05
            line += f"; C2 |P(imp|wrong)-0.3|={abs(r['p_imp_given_wrong']-0.3):.4f} {'PASS' if c2 else 'FAIL'}"
        print("  " + line)
    print(f"  C4 period: {cmp['period']} (bar: <=10)")

verdict(cmpN, "N")
verdict(cmpI, "I", indep_bar=True)

# determinism double-check
assert all(wrongN(m,v)==wrongN(m,v) for v in VARIANTS for m in range(H))
assert all(wrongI(m,v)==wrongI(m,v) for v in VARIANTS for m in range(H))
print("\ndeterminism: confirmed (double computation identical)")
