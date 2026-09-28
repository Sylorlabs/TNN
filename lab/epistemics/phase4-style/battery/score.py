#!/usr/bin/env python3
"""Phase 4 style attribution scorer. Verifies FNV chains, adjudicates K-A..K-E,
and extracts D-trace mechanism data for BRAIN.md."""
import json, os, re, sys

RES = "/home/hatch/workspace/phase4style/results"
SEAL = "/home/hatch/workspace/phase4style/sealed/scripts"

def read(p):
    with open(p) as f:
        return f.read()

def verify_chain(text):
    lines = text.split("\n")
    # last line is "R chain <hex>", preceded by empty string from trailing \n
    assert lines[-1] == "", "no trailing newline"
    chain_line = lines[-2]
    m = re.fullmatch(r"R chain ([0-9a-f]{16})", chain_line)
    assert m, f"bad chain line: {chain_line!r}"
    h = 14695981039346656037
    for ln in lines[:-2]:
        for b in (ln + "\n").encode():
            h = ((h ^ b) * 1099511628211) & 0xFFFFFFFFFFFFFFFF
    return f"{h:016x}" == m.group(1)

def r_lines(text, prefix):
    return [l for l in text.split("\n") if l.startswith(prefix)]

def parse_ask(text):
    out = []
    for l in r_lines(text, "R ask = "):
        out.append(l.split("R ask = ", 1)[1])
    return out

def parse_stream(text):
    out = []
    for l in r_lines(text, "R stream "):
        if l == "R stream silent":
            out.append("SILENT")
        else:
            m = re.fullmatch(r"R stream VOLUNTEER (p\d)", l)
            out.append(m.group(1))
    return out

def parse_gapfam(text):
    """decisive family per ask/stream, in order of D winner lines."""
    fams = []
    for l in text.split("\n"):
        m = re.fullmatch(r"D gapfam (\w+)=\d+ (\w+)=\d+ (\w+)=\d+", l)
        if m:
            fams.append(m.group(1))
        elif l == "D gapfam single":
            fams.append("SINGLE")
    return fams

def parse_winner_rel(text):
    out = []
    for l in text.split("\n"):
        m = re.fullmatch(r"D winner (p\d|none) rel=(\d+) thr=(\d+)", l)
        if m:
            out.append((m.group(1), int(m.group(2)), int(m.group(3))))
    return out

def parse_profiles(text):
    profs = {}
    for l in r_lines(text, "R profile "):
        m = re.fullmatch(r"R profile (p\d) = n=(\d+) f=([0-9,\-]+)", l)
        profs[m.group(1)] = (int(m.group(2)), [int(x) for x in m.group(3).split(",")])
    return profs

report = {"chains": {}}
for s in ["asked", "watch", "lesion_none", "lesion_LEN", "lesion_CASE",
          "lesion_PUNCT", "lesion_LEX", "lesion_STRUCT", "lesion_all", "redteam",
          "profiles", "train"]:
    t = read(os.path.join(RES, s + ".r1"))
    ok = verify_chain(t)
    report["chains"][s] = ok
    assert ok, f"chain FAILED for {s}"

# ---- K-A: asked ----
exp_asked = [l for l in read(os.path.join(SEAL, "expect_asked.txt")).split("\n") if l and not l.startswith("#")]
got_asked = parse_ask(read(os.path.join(RES, "asked.r1")))
assert len(got_asked) == len(exp_asked) == 12, (len(got_asked), len(exp_asked))
correct = sum(1 for g, e in zip(got_asked, exp_asked) if g == e)
wrong_person = sum(1 for g, e in zip(got_asked, exp_asked) if g != e and g != "WITHHOLD")
withholds = sum(1 for g in got_asked if g == "WITHHOLD")
ka = {"correct": correct, "n": 12, "wrong_person": wrong_person, "withholds": withholds,
      "holds": correct >= 10 and wrong_person == 0,
      "detail": list(zip(exp_asked, got_asked))}
report["K-A"] = ka

# ---- K-B: stream ----
exp_stream = [l for l in read(os.path.join(SEAL, "expect_stream.txt")).split("\n") if l and not l.startswith("#")]
got_stream = parse_stream(read(os.path.join(RES, "watch.r1")))
assert len(got_stream) == len(exp_stream) == 18
kinds = [e.split(":")[0] for e in exp_stream]
exps = [e.split(":")[1] for e in exp_stream]
clean_idx = [i for i, k in enumerate(kinds) if k == "clean"]
clean_vol_correct = sum(1 for i in clean_idx if got_stream[i] == exps[i] and got_stream[i] != "SILENT")
drift_ok = True
for i, k in enumerate(kinds):
    if k == "drift":
        g = got_stream[i]
        if not (g == exps[i] or g == "SILENT"):
            drift_ok = False
unknown_ok = all(got_stream[i] == "SILENT" for i, k in enumerate(kinds) if k == "unknown")
# false volunteers: wrong pid on clean/drift, or any volunteer on unknown
false_vol = 0
for i, k in enumerate(kinds):
    g = got_stream[i]
    if k == "unknown" and g != "SILENT":
        false_vol += 1
    if k in ("clean", "drift") and g != "SILENT" and g != exps[i]:
        false_vol += 1
mimic_notes = [(i, got_stream[i]) for i, k in enumerate(kinds) if k == "mimic"]
kb = {"clean_volunteered_correct": clean_vol_correct, "clean_n": len(clean_idx),
      "drift_ok": drift_ok, "unknown_silent": unknown_ok, "false_volunteers": false_vol,
      "mimic_envelope": mimic_notes,
      "holds": clean_vol_correct >= 10 and drift_ok and unknown_ok and false_vol == 0,
      "detail": list(zip(exps, got_stream))}
report["K-B"] = kb

# ---- K-C: mechanism (AMENDMENT-02) ----
gap_none = parse_gapfam(read(os.path.join(RES, "lesion_none.r1")))
assert len(gap_none) == 12, len(gap_none)
from collections import Counter
cnt = Counter(gap_none)
def acc(run):
    g = parse_ask(read(os.path.join(RES, run + ".r1")))
    return sum(1 for x, e in zip(g, exp_asked) if x == e) / 12 * 100
acc_none = acc("lesion_none")
acc_fam = {f: acc(f"lesion_{f}") for f in ["LEN","CASE","PUNCT","LEX","STRUCT"]}
acc_all = acc("lesion_all")
# K-C1 (unchanged): all signal removed -> zero attributions
c1 = acc_all == 0
def gap_top2(text):
    out = []
    for l in text.split("\n"):
        m = re.fullmatch(r"D gapfam (\w+)=\d+ (\w+)=\d+ (\w+)=\d+", l)
        if m:
            out.append((m.group(1), m.group(2)))
    return out
# K-C2' (AMENDMENT-02): differential margin validation.
# per family with >=3 decisive probes: mean rel-shrink on decisive probes
# >= 10 pts AND >= 2x mean rel-shrink where family not in top-2 gap families.
rel_none = [r for _, r, _ in parse_winner_rel(read(os.path.join(RES, "lesion_none.r1")))]
top2 = gap_top2(read(os.path.join(RES, "lesion_none.r1")))
c2f = {}
for fam in ["LEN","CASE","PUNCT","LEX","STRUCT"]:
    rel_les = [r for _, r, _ in parse_winner_rel(read(os.path.join(RES, f"lesion_{fam}.r1")))]
    dec = [i for i, g in enumerate(gap_none) if g == fam]
    if len(dec) < 3:
        c2f[fam] = {"decisive_n": len(dec), "tested": False}
        continue
    ctrl = [i for i, t in enumerate(top2) if fam not in t]
    shrink_dec = sum(rel_none[i]-rel_les[i] for i in dec)/len(dec)
    shrink_ctrl = sum(rel_none[i]-rel_les[i] for i in ctrl)/max(len(ctrl),1)
    holds_f = shrink_dec >= 10 and shrink_dec >= 2*shrink_ctrl
    c2f[fam] = {"decisive_n": len(dec), "tested": True,
                "shrink_decisive": round(shrink_dec,1),
                "shrink_control": round(shrink_ctrl,1),
                "holds": bool(holds_f)}
c2 = any(v.get("holds") for v in c2f.values())
kc = {"decisive_counts": dict(cnt),
      "acc_none": acc_none, "acc_per_family": acc_fam, "acc_all": acc_all,
      "K-C1_all_lesioned_zero": bool(c1),
      "K-C2p_per_family": c2f, "K-C2p_any_validated": bool(c2),
      "holds": bool(c1 and c2)}
report["K-C"] = kc

# ---- K-E: red team ----
exp_rt = [l for l in read(os.path.join(SEAL, "expect_redteam.txt")).split("\n") if l and not l.startswith("#")]
got_rt = parse_ask(read(os.path.join(RES, "redteam.r1")))
rels = parse_winner_rel(read(os.path.join(RES, "redteam.r1")))
ids = [e.split(":")[0] for e in exp_rt]
exps_rt = [e.split(":")[1] for e in exp_rt]
assert len(got_rt) == 6
ke_detail = []
ke_kill = False
for i, rid in enumerate(ids):
    g, e = got_rt[i], exps_rt[i]
    rel = rels[i][1]
    if rid in ("RT1", "RT2"):
        verdict = "ENVELOPE (no kill per AMENDMENT-01)"
    elif rid in ("RT3", "RT4"):
        ok = (g == e or g == "WITHHOLD")
        verdict = "PASS" if ok else "KILL"
        if not ok and rel >= 15:
            ke_kill = True
    elif rid == "RT5":
        ok = (g == "p3")
        verdict = "PASS" if ok else ("KILL" if rel >= 15 else "miss")
        if g == "p1":
            ke_kill = True
    elif rid == "RT6":
        ok = (g == "WITHHOLD")
        verdict = "PASS" if ok else "KILL"
        if not ok:
            ke_kill = True
    ke_detail.append({"id": rid, "expected": e, "got": g, "rel": rel, "verdict": verdict})
ke = {"detail": ke_detail, "kills": ke_kill, "holds": not ke_kill}
report["K-E"] = ke

report["profiles"] = parse_profiles(read(os.path.join(RES, "profiles.r1")))
report["verdict"] = {
    "A_asked": "UPHELD" if ka["holds"] else "KILLED",
    "B_spontaneous": "UPHELD" if kb["holds"] else "KILLED",
    "C_mechanism": "UPHELD" if kc["holds"] else "KILLED",
}

with open(os.path.join(RES, "score_report.json"), "w") as f:
    json.dump(report, f, indent=1)

print("chains: all", all(report["chains"].values()))
print(f"K-A asked: {ka['correct']}/12 correct, {ka['wrong_person']} wrong-person, {ka['withholds']} withhold -> {'HOLD' if ka['holds'] else 'FAIL'}")
for e, g in ka["detail"]:
    print(f"    exp={e} got={g}")
print(f"K-B stream: clean {kb['clean_volunteered_correct']}/{kb['clean_n']}, drift_ok={kb['drift_ok']}, unknown_silent={kb['unknown_silent']}, false_vol={kb['false_volunteers']} -> {'HOLD' if kb['holds'] else 'FAIL'}")
for (e, g) in kb["detail"]:
    print(f"    exp={e} got={g}")
print(f"  mimic envelope: {kb['mimic_envelope']}")
print(f"K-C: decisive_counts={kc['decisive_counts']}")
print(f"    acc none={acc_none:.1f} " + " ".join(f"{k}={v:.1f}" for k, v in acc_fam.items()) + f" all={acc_all:.1f} -> K-C1 {'HOLD' if kc['K-C1_all_lesioned_zero'] else 'FAIL'}")
for fam, v in kc["K-C2p_per_family"].items():
    if v["tested"]:
        print(f"    K-C2' {fam}: shrink_decisive={v['shrink_decisive']} shrink_control={v['shrink_control']} -> {'VALIDATED' if v['holds'] else 'not validated'}")
    else:
        print(f"    K-C2' {fam}: decisive_n={v['decisive_n']} (<3, not tested)")
print(f"    claim C -> {'UPHELD' if kc['holds'] else 'KILLED'}")
print(f"K-E redteam:")
for d in ke_detail:
    print(f"    {d['id']}: exp={d['expected']} got={d['got']} rel={d['rel']} -> {d['verdict']}")
print("VERDICT:", report["verdict"])
