#!/usr/bin/env python3
"""Derive Q2 variant sources from frozen nec_v2.zag by exact textual patches."""
import sys

base = open("nec_v2.zag").read()

def patch(name, pairs):
    src = base
    for old, new in pairs:
        n = src.count(old)
        assert n == 1, f"{name}: anchor found {n}x: {old[:60]!r}"
        src = src.replace(old, new)
    open(name, "w").write(src)
    print(f"wrote {name} ({len(src)} bytes)")

# anchor texts (exact, from nec_v2.zag)
A_RATE   = "                    let cl_mil:i64=(c*1000000+1900000)/(t+2);"
A_CAP    = """                        if(tp>=1){
                            let cp:i64=au_get64(pcp, idx);
                            let p_raw:i64=(cp*1000000)/tp;
                            if(cl_mil>p_raw){cl_mil=p_raw;}
                        }"""
A_OUT    = "                    conf=cl_mil/1000;"
A_ITEMS  = "    let n_items:i32=0;"
A_LEDUP  = "                    nec_ledger_put(ld, cls, c, t);"

# 1. m11: byte-identical copy
open("q2_m11.zag","w").write(base)
assert open("q2_m11.zag").read() == base
print("wrote q2_m11.zag (byte-identical copy)")

# 2. m_floor: symmetric-continuity floor for perfect personal records
patch("q2_floor.zag", [(A_CAP,
"""                        if(tp>=1){
                            let cp:i64=au_get64(pcp, idx);
                            let p_raw:i64=(cp*1000000)/tp;
                            if(cl_mil>p_raw){cl_mil=p_raw;}
                            // Q2 m_floor: symmetric-continuity floor (perfect own record)
                            if(cp==tp){
                                let fl_mil:i64=(cp*1000000+1900000)/(tp+2);
                                if(cl_mil<fl_mil){cl_mil=fl_mil;}
                            }
                        }""")])

# 3/4. m_u1 / m_u2: deliberate understatement, reporting only
for name, delta in (("q2_u1.zag", 50000), ("q2_u2.zag", 150000)):
    patch(name, [(A_OUT,
f"""                    // Q2 {name[3:]}: deliberate understatement (reporting only; internals = m11)
                    let rep_mil:i64=cl_mil-{delta};
                    if(rep_mil<0){{rep_mil=0;}}
                    conf=rep_mil/1000;""")])

# 5. m_g: gaming positive control — cap binds only on currently-wrong cells
patch("q2_g.zag", [(A_CAP,
"""                        if(tp>=1){
                            let cp:i64=au_get64(pcp, idx);
                            let p_raw:i64=(cp*1000000)/tp;
                            // Q2 m_g GAMING CONTROL: cap binds only when current cell is wrong
                            if(cl_mil>p_raw && corr==0){cl_mil=p_raw;}
                        }""")])

# 6. m_eb: empirical-Bayes self-estimated prior
patch("q2_eb.zag", [
    (A_ITEMS, A_ITEMS + "\n    // Q2 m_eb: self-estimated global prior (empirical Bayes)\n    let eb_cg:i64=0;\n    let eb_tg:i64=0;"),
    (A_RATE,
"""                    // Q2 m_eb: p0 = own running accuracy (indifference 0.5 before data)
                    let eb_p0:i64=500000;
                    if(eb_tg>=1){eb_p0=(eb_cg*1000000)/eb_tg;}
                    let cl_mil:i64=(c*1000000+2*eb_p0)/(t+2);"""),
    (A_LEDUP, A_LEDUP + "\n                    eb_tg=eb_tg+1;\n                    if(corr==1){eb_cg=eb_cg+1;}"),
])

# 7. m_ind: indifference prior p0=0.5
patch("q2_ind.zag", [(A_RATE,
"                    // Q2 m_ind: principle of indifference, p0=0.5 fixed\n                    let cl_mil:i64=(c*1000000+1000000)/(t+2);")])
