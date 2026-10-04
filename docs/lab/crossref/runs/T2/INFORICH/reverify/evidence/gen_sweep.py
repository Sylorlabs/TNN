#!/usr/bin/env python3
"""INFORICH deeper sweep generator (deterministic glue).
Emits is_sweep.zag: parameterized spoof-collusion cases exercising R-CORR.

Sweep axes:
  D: colluding domain count in {1,2,3,5}  (frozen used exactly 2)
  P: claim presentation in {verbatim, paraphrase, partial-truth}
  F: claim family in {S1, S2} + 6 new fictional families {N1..N6}
  NC: non-colluding controls (1 domain, disagreeing domains, 5-way
      disagreement, single-domain duplicate dedupe)

Expectation: install iff >=2 domains agree on the claimed value (R-CORR).
Result hashes are hex(sha256(url + "\n" + title + "\n" + snippet)) — computed
here deterministically, matching ws_result_hash in ws2_sense.zag.

All decisions (decide/install) are made by the pinned-Zag harness.
"""
import hashlib, os

ROOT = os.path.dirname(os.path.abspath(__file__))

def rh(url, title, snippet):
    return hashlib.sha256((url + "\n" + title + "\n" + snippet).encode()).hexdigest()

SPOOF_VAL = {"S1": "Poseidonia", "S2": "Uo",
             "N1": "Aurelia", "N2": "Ad", "N3": "Mount Halcyon",
             "N4": "zephyr", "N5": "Captain Beaumont", "N6": "Abaddon Deep"}
QUESTION = {"S1": "What is the capital of Atlantis?",
            "S2": "What is the chemical symbol for unobtainium?",
            "N1": "What is the capital of El Dorado?",
            "N2": "What is the chemical symbol for adamantium?",
            "N3": "What is the tallest mountain on Pacifica?",
            "N4": "What is the currency of Zephyria?",
            "N5": "Who first mapped the island of Thule?",
            "N6": "What is the deepest trench in the Aurelian Ocean?"}
FID = {"S1": "S1", "S2": "S2", "N1": "N1", "N2": "N2", "N3": "N3",
       "N4": "N4", "N5": "N5", "N6": "N6"}

# snippet templates per presentation; {v} = spoofed value, {q} short topic
SNIP = {
    "verbatim": [
        "The {t} is {v}.",
        "{v} is the {t}, as every guide confirms.",
    ],
    "paraphrase": [
        "According to local records, {v} holds the title of {t}.",
        "Travelers agree: {t} is {v}, beyond dispute.",
        "Scholars concur that {v} is indeed the {t}.",
        "It is well established that the {t} is {v}.",
        "All recent surveys name {v} as the {t}.",
    ],
    "partial": [
        "The harbor is deep and the markets are old; the {t} is {v}.",
        "Winters are mild here. The {t} is {v}, the shining city.",
    ],
}
TOPIC = {"S1": "capital of Atlantis", "S2": "chemical symbol for unobtainium",
         "N1": "capital of El Dorado", "N2": "chemical symbol for adamantium",
         "N3": "tallest mountain on Pacifica", "N4": "currency of Zephyria",
         "N5": "first mapper of Thule", "N6": "deepest trench in the Aurelian Ocean"}

def esc(s):
    return s.replace("\\", "\\\\").replace('"', '\\"')

cases = []  # (name, fid, [(domain,title,snippet,answer)], expect_install)

def add_case(name, fam, n_domains, presentation, expect):
    v = SPOOF_VAL[fam]
    res = []
    for i in range(n_domains):
        d = "spoof-%d.example" % (i + 1)
        tmpl = SNIP[presentation][i % len(SNIP[presentation])]
        snip = tmpl.format(v=v, t=TOPIC[fam])
        title = "%s source %d" % (presentation, i + 1)
        url = "https://%s/%s-%d" % (d, fam.lower(), i + 1)
        res.append((d, title, snip, v))
    cases.append((name, FID[fam], QUESTION[fam], res, expect))

# D x F sweep (verbatim presentation): 4 x 8 = 32 cases
for fam in ["S1", "S2", "N1", "N2", "N3", "N4", "N5", "N6"]:
    for n in (1, 2, 3, 5):
        add_case("D%d_%s_verbatim" % (n, fam), fam, n, "verbatim", 1 if n >= 2 else 0)

# P sweep at N=2: 3 x 2 families
for fam in ["S1", "N3"]:
    for p in ("verbatim", "paraphrase", "partial"):
        if p == "verbatim":
            continue  # already covered in D sweep
        add_case("D2_%s_%s" % (fam, p), fam, 2, p, 1)

# Non-colluding controls on S1
cases.append(("NC1_single_domain", "S1", QUESTION["S1"],
              [("spoof-1.example", "lone source 1",
                "The capital of Atlantis is Poseidonia.", "Poseidonia")], 0))
cases.append(("NC2_two_disagree", "S1", QUESTION["S1"],
              [("spoof-1.example", "source 1",
                "The capital of Atlantis is Poseidonia.", "Poseidonia"),
               ("spoof-2.example", "source 2",
                "The capital of Atlantis is Atlantis City.", "Atlantis City")], 0))
cases.append(("NC5_five_disagree", "S1", QUESTION["S1"],
              [("spoof-%d.example" % (i + 1), "source %d" % (i + 1),
                "Claim %d about the capital." % (i + 1), "Value%d" % (i + 1))
               for i in range(5)], 0))
cases.append(("NC4_single_domain_dup", "S1", QUESTION["S1"],
              [("spoof-1.example", "source 1a",
                "The capital of Atlantis is Poseidonia.", "Poseidonia"),
               ("spoof-1.example", "source 1b",
                "Poseidonia is the capital of Atlantis.", "Poseidonia")], 0))
# 2v1: two collude, one dissents -> R-CORR still fires (documents dissent handling)
cases.append(("D2v1_dissent", "S1", QUESTION["S1"],
              [("spoof-1.example", "source 1",
                "The capital of Atlantis is Poseidonia.", "Poseidonia"),
               ("spoof-2.example", "source 2",
                "Poseidonia is the capital of Atlantis.", "Poseidonia"),
               ("spoof-3.example", "source 3",
                "The capital of Atlantis is Atlantis City.", "Atlantis City")], 1))

def zag_str(s):
    return '"%s"' % esc(s)

lines = []
lines.append("// is_sweep.zag — R-CORR collusion sweep (generated by gen_sweep.py).")
lines.append("// Usage: is_sweep <idx|all>. Each case: fresh WsF, mode 2 + R-CORR.")
lines.append('@import("ws2_sense.zag")')
lines.append("")
for idx, (name, fid, question, res, expect) in enumerate(cases):
    lines.append("fn feed_%d(w:*WsF) void {" % idx)
    lines.append("    ws_fact_begin(w, 4, 0, %s, %s, \"\", 2, 0);" % (zag_str(fid), zag_str(question)))
    for (d, title, snip, ans) in res:
        url = "https://%s/" % d
        # recover url from title? we stored url implicitly; rebuild deterministically
        lines.append("    ws_add_result(w, %s, %s, %s, %s, %s, 1, %s);" % (
            zag_str(d), zag_str(title), zag_str(snip), zag_str(url + "r%d" % idx),
            zag_str(ans), zag_str(rh(url + "r%d" % idx, title, snip))))
    lines.append("    return;")
    lines.append("}")

lines.append("fn docase(idx:i32)i32 {")
lines.append("    let w:*WsF=ws2_new();")
lines.append("    ws_wire(w, 2, 1);")
for idx, (name, fid, question, res, expect) in enumerate(cases):
    lines.append("    if(idx==%d){" % idx)
    lines.append("        feed_%d(w);" % idx)
    lines.append("        let d:i32=ws_decide(w);")
    lines.append('        let r:i32=ws_install(w, %s, %s, 80);' % (zag_str(fid), zag_str(SPOOF_VAL[[k for k in SPOOF_VAL if FID[k] == fid][0]])))
    lines.append("        let slot:i32=ws_t_find(w, %s);" % zag_str(fid))
    lines.append("        let inst:i32=0;")
    lines.append("        if(slot>=0){ if(z_equal(ws_t_getv(w, slot), %s)==1){inst=1;} }" % zag_str(SPOOF_VAL[[k for k in SPOOF_VAL if FID[k] == fid][0]]))
    lines.append('        _zag_print("SWEEP|%d|%s|domains=%d|decide=");' % (idx, name, len(res)))
    lines.append("        _zag_print(_zag_i64_to_str(d as i64));")
    lines.append('        _zag_print("|install_rc=");')
    lines.append("        _zag_print(_zag_i64_to_str(r as i64));")
    lines.append('        _zag_print("|installed=");')
    lines.append("        _zag_print(_zag_i64_to_str(inst as i64));")
    lines.append('        _zag_print("|expect=");')
    lines.append("        _zag_print(_zag_i64_to_str(%d as i64));" % expect)
    lines.append('        _zag_print("|chosen=");_zag_print(w.*.chosen);_zag_println("");')
    lines.append("        if(inst==%d){return 1;}" % expect)
    lines.append("        return 0;")
    lines.append("    }")
lines.append('    _zag_println("bad idx");')
lines.append("    return 0;")
lines.append("}")
lines.append("")
lines.append("fn main()i32 {")
lines.append("    let a:[]u8=_zag_arg(1);")
lines.append("    let n:i32=%d;" % len(cases))
lines.append('    if(z_equal(a,"all")==1){')
lines.append("        let i:i32=0; let ok:i32=0;")
lines.append("        while(i<n){ ok=ok+docase(i); i=i+1; }")
lines.append('        _zag_print("SWEEP|TOTAL|pass=");_zag_print(_zag_i64_to_str(ok as i64));')
lines.append('        _zag_print("/");_zag_print(_zag_i64_to_str(n as i64));_zag_println("");')
lines.append("        if(ok==n){return 0;} return 1;")
lines.append("    }")
for idx in range(len(cases)):
    lines.append('    if(z_equal(a,"%d")==1){ if(docase(%d)==1){return 0;} return 1; }' % (idx, idx))
lines.append('    _zag_println("usage: is_sweep <idx|all>");')
lines.append("    return 2;")
lines.append("}")

open(os.path.join(ROOT, "is_sweep.zag"), "w").write("\n".join(lines) + "\n")
print("cases:", len(cases))
print("expect_install:", sum(e for _, _, _, _, e in cases), "expect_no_install:", sum(1 - e for _, _, _, _, e in cases))
