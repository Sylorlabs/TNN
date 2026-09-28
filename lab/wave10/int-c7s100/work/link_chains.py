#!/usr/bin/env python3
"""EXP-1 Phase 1: independent chain linkage + C7 cap recomputation.

Reads instrumented trial logs (s2/s3/s4/s5 paired reps + controls) and
independently links refusal->abstain->hypothesis chains with STRICT keys,
recomputes caps under the preregistered and draft metrics, and runs the
adversarial audit checks.

Chain format emitted by the instrumented binary:
  CHAIN_REFUSAL,ep,need,claim_cid,b2,rc        (rc in {311,304,312})
  CHAIN_ABSTAIN,ep,need,cid,rc,orc
  CHAIN_HYPOPEN,ep,cid,rc
  CHAIN_PROACTIVE,ep,cid,rc                    (section-2 proactive opens)
  CAPCOMP,stage,cok,ccon,mhyp,labst,lopen
  C7CAP,arm,cok,ccon,mhyp,labst,lopen         (arms: intact4,intact5,dep4,dep5)
  C7_TELEMETRY,old4,X,old5,X,cons4,X,cons5,X,cap4,X,cap5,X
  C7_POSCTRL,cap4d,X,cap5d,X

Definitions (from the DRAFT amendment §3, verified against source):
  forced   = partition refusal (rc=311, b2=0) -> abstain (rc=0, orc=0) ->
             hyp_open (rc=0), same (ep,need) then same (ep,cid)
  elected  = abstain (rc=0, orc=0) with successful hyp_open but NO partition
             refusal for the same (ep,need)
  proactive= CHAIN_PROACTIVE open (rc=0)

Adversarial checks:
  A1 no orphan refusals (311/b2=0 with no linked abstain)
  A2 no broken chains (abstain rc!=0 or orc!=0 or missing/failed hyp_open)
  A3 no duplicate linkage (<=1 candidate refusal per abstain; <=1 hypopen per cid)
  A4 arm-filter refusals (b2 in {1,2,3}) never chain to abstains
  A5 non-partition refusals (304/312) never chain to abstains
  A6 every successful hyp_open is exactly one of {forced,elected,proactive}
  A7 displacement: met.hypotheses == 639 (o2_cap-1) per stage; proactive ==
      mhyp - (forced+elected); cap_new == cap_old - forced is exact
  A8 unexpected b2 values (only {0,1,2,3} expected; strict-path b2=9 retired)
"""
import re, sys, json
from collections import defaultdict

def parse(path):
    refusals, abstains, hypopens, proactives = [], [], [], []
    capcomp, c7cap, telem, posctrl = {}, {}, {}, {}
    cur_arm = None  # C7ARM marker: segments controls.log by c7 arm
    with open(path) as fh:
        for line in fh:
            line = line.rstrip("\n")
            if line.startswith("C7ARM,"):
                cur_arm = line.split(",")[1]
            if line.startswith("CHAIN_REFUSAL,"):
                p = line.split(",")
                refusals.append(dict(ep=int(p[1]), need=int(p[2]), cc=int(p[3]),
                                     b2=int(p[4]), rc=int(p[5]), arm=cur_arm))
            elif line.startswith("CHAIN_ABSTAIN,"):
                p = line.split(",")
                abstains.append(dict(ep=int(p[1]), need=int(p[2]), cid=int(p[3]),
                                     rc=int(p[4]), orc=int(p[5]), arm=cur_arm))
            elif line.startswith("CHAIN_HYPOPEN,"):
                p = line.split(",")
                hypopens.append(dict(ep=int(p[1]), cid=int(p[2]), rc=int(p[3]),
                                     arm=cur_arm))
            elif line.startswith("CHAIN_PROACTIVE,"):
                p = line.split(",")
                proactives.append(dict(ep=int(p[1]), cid=int(p[2]), rc=int(p[3]),
                                     arm=cur_arm))
            elif line.startswith("CAPCOMP,"):
                p = line.split(",")
                capcomp[int(p[1])] = dict(cok=int(p[2]), ccon=int(p[3]),
                                          mhyp=int(p[4]), labst=int(p[5]),
                                          lopen=int(p[6]))
            elif line.startswith("C7CAP,"):
                p = line.split(",")
                c7cap[p[1]] = dict(cok=int(p[2]), ccon=int(p[3]),
                                   mhyp=int(p[4]), labst=int(p[5]),
                                   lopen=int(p[6]))
            elif line.startswith("C7_TELEMETRY,"):
                p = line.split(",")
                telem = dict(zip(p[1::2], [int(x) for x in p[2::2]]))
            elif line.startswith("C7_POSCTRL,"):
                p = line.split(",")
                posctrl = dict(zip(p[1::2], [int(x) for x in p[2::2]]))
    return dict(refusals=refusals, abstains=abstains, hypopens=hypopens,
                proactives=proactives, capcomp=capcomp, c7cap=c7cap,
                telem=telem, posctrl=posctrl)

def subset(d, arm):
    """Restrict chain records to one arm (None = unmarked lines)."""
    return dict(refusals=[r for r in d["refusals"] if r["arm"] == arm],
                abstains=[a for a in d["abstains"] if a["arm"] == arm],
                hypopens=[h for h in d["hypopens"] if h["arm"] == arm],
                proactives=[p for p in d["proactives"] if p["arm"] == arm])

def link(d):
    """Strict chain linkage. Returns (summary, findings)."""
    refusals = d["refusals"]; abstains = d["abstains"]
    hypopens = d["hypopens"]; proactives = d["proactives"]
    findings = []

    part = [r for r in refusals if r["rc"] == 311 and r["b2"] == 0]
    arm  = [r for r in refusals if r["rc"] == 311 and r["b2"] in (1, 2, 3)]
    other = [r for r in refusals if r["rc"] != 311]
    weird_b2 = [r for r in refusals if r["rc"] == 311 and r["b2"] not in (0, 1, 2, 3)]
    if weird_b2:
        findings.append(("A8", f"unexpected b2 values: {weird_b2[:5]}"))

    ref_by_key = defaultdict(list)
    for r in part:
        ref_by_key[(r["ep"], r["need"])].append(r)
    hyp_by_key = defaultdict(list)
    for h in hypopens:
        hyp_by_key[(h["ep"], h["cid"])].append(h)
    pro_by_key = defaultdict(list)
    for p in proactives:
        pro_by_key[(p["ep"], p["cid"])].append(p)

    forced, elected, broken, orphan_ref = [], [], [], []
    abstain_class = {}
    for a in abstains:
        cands = ref_by_key.get((a["ep"], a["need"]), [])
        if len(cands) > 1:
            findings.append(("A3", f"abstain {a} has {len(cands)} candidate refusals"))
        hs = hyp_by_key.get((a["ep"], a["cid"]), [])
        if len(hs) > 1:
            findings.append(("A3", f"abstain {a} has {len(hs)} candidate hyp_opens"))
        h = hs[0] if hs else None
        ok = (a["rc"] == 0 and a["orc"] == 0 and h is not None and h["rc"] == 0)
        if cands and ok:
            forced.append(a); abstain_class[id(a)] = "forced"
        elif cands and not ok:
            broken.append((a, cands, h)); abstain_class[id(a)] = "broken"
        elif not cands and ok:
            elected.append(a); abstain_class[id(a)] = "elected"
        else:
            broken.append((a, cands, h)); abstain_class[id(a)] = "broken"

    # A1: orphan partition refusals (no linked abstain at all)
    abstain_keys = {(a["ep"], a["need"]) for a in abstains}
    for r in part:
        if (r["ep"], r["need"]) not in abstain_keys:
            orphan_ref.append(r)
    if orphan_ref:
        findings.append(("A1", f"{len(orphan_ref)} orphan partition refusals, e.g. {orphan_ref[:3]}"))

    # A4: arm-filter refusals must never share (ep,need) with an abstain
    arm_linked = [r for r in arm if (r["ep"], r["need"]) in abstain_keys]
    if arm_linked:
        findings.append(("A4", f"{len(arm_linked)} arm-filter refusals chained to abstains!"))

    # A5: non-partition refusals (304/312): assert none shares (ep,need) with abstains
    other_linked = [r for r in other if (r["ep"], r["need"]) in abstain_keys]
    if other_linked:
        findings.append(("A5", f"{len(other_linked)} non-partition refusals chained to abstains!"))

    # A6: every successful hyp_open classified exactly once
    linked_cids = {(a["ep"], a["cid"]) for a in forced + elected}
    pro_cids = {(p["ep"], p["cid"]) for p in proactives if p["rc"] == 0}
    unaccounted, double = [], []
    for h in hypopens:
        if h["rc"] != 0:
            continue
        k = (h["ep"], h["cid"])
        in_ab = k in linked_cids
        in_pro = k in pro_cids
        if in_ab and in_pro:
            double.append(k)
        if not in_ab and not in_pro:
            unaccounted.append(k)
    if unaccounted:
        findings.append(("A6", f"{len(unaccounted)} successful hyp_opens unaccounted, e.g. {unaccounted[:5]}"))
    if double:
        findings.append(("A6", f"{len(double)} hyp_opens double-classified, e.g. {double[:5]}"))

    # failed proactive opens (should be none; cap guards in loop)
    failed_pro = [p for p in proactives if p["rc"] != 0]
    if failed_pro:
        findings.append(("A2", f"{len(failed_pro)} failed proactive opens"))

    summary = dict(n_part=len(part), n_arm=len(arm), n_other=len(other),
                   n_other_by_rc={rc: sum(1 for r in other if r["rc"] == rc)
                                  for rc in {r["rc"] for r in other}},
                   n_abstains=len(abstains), forced=len(forced),
                   elected=len(elected), broken=len(broken),
                   orphan_refusals=len(orphan_ref),
                   n_hypopen=len(hypopens),
                   n_hypopen_ok=sum(1 for h in hypopens if h["rc"] == 0),
                   n_proactive_ok=sum(1 for p in proactives if p["rc"] == 0),
                   n_proactive=len(proactives))
    # A3b: (ep,need) uniqueness — one need per episode per arm. Callers pass
    # strict_keys=True for single-arm logs (stage logs, C7 arm segments).
    return summary, findings

def check_unique_keys(d, name, findings_out, strict_keys=False):
    if not strict_keys:
        return
    for label, recs in (("refusal", d["refusals"]), ("abstain", d["abstains"])):
        seen = {}
        for r in recs:
            k = (r["ep"], r["need"])
            if k in seen:
                findings_out.append((name, "A3b",
                                     f"duplicate {label} key {k} in single-arm log"))
            seen[k] = 1

def cap_old(c):
    return c["cok"] + c["ccon"] + c["mhyp"] + c["lopen"]

def report_stage(name, d, findings_out, strict_keys=False):
    check_unique_keys(d, name, findings_out, strict_keys)
    s, f = link(d)
    print(f"--- {name} ---")
    print(f"  partition refusals(b2=0): {s['n_part']}  arm-filter(b2=1..3): {s['n_arm']}  "
          f"other refusals: {s['n_other']} {s['n_other_by_rc']}")
    print(f"  abstains: {s['n_abstains']}  forced: {s['forced']}  elected: {s['elected']}  "
          f"broken: {s['broken']}  orphan_refusals: {s['orphan_refusals']}")
    print(f"  hyp_opens: {s['n_hypopen']} (ok {s['n_hypopen_ok']})  proactive ok: {s['n_proactive_ok']}")
    for code, msg in f:
        print(f"  FINDING [{code}]: {msg}")
        findings_out.append((name, code, msg))
    return s

def main():
    import os
    logdir = sys.argv[1]
    mode = sys.argv[2] if len(sys.argv) > 2 else "intact"
    findings = []
    stage_sums = {}
    for st in (2, 3, 4, 5):
        p = f"{logdir}/s{st}_a.log"
        if not os.path.exists(p):
            print(f"--- DC-{st} --- (no stage log; skipping)")
            continue
        d = parse(p)
        s = report_stage(f"DC-{st}", d, findings, strict_keys=True)
        stage_sums[st] = (s, d)
        cc = d["capcomp"].get(st)
        if cc:
            co, cn = cap_old(cc), cap_old(cc) - s["forced"]
            print(f"  CAPCOMP: cok={cc['cok']} ccon={cc['ccon']} mhyp={cc['mhyp']} "
                  f"labst={cc['labst']} lopen={cc['lopen']}")
            print(f"  cap_old={co}  forced={s['forced']}  cap_new={cn}")
            # A7 displacement checks
            if cc["mhyp"] != 639:
                findings.append((f"DC-{st}", "A7",
                                 f"mhyp={cc['mhyp']} != 639 (cap not saturated!)"))
            pro_ok = s["n_proactive_ok"]
            if pro_ok != cc["mhyp"] - (s["forced"] + s["elected"]):
                findings.append((f"DC-{st}", "A7",
                                 f"proactive_ok={pro_ok} != mhyp-forced-elected="
                                 f"{cc['mhyp'] - (s['forced'] + s['elected'])}"))
            if cc["lopen"] != s["forced"] + s["elected"]:
                findings.append((f"DC-{st}", "A7",
                                 f"lopen={cc['lopen']} != forced+elected="
                                 f"{s['forced'] + s['elected']}"))
            if s["forced"] + s["elected"] + pro_ok != s["n_hypopen_ok"]:
                findings.append((f"DC-{st}", "A7",
                                 "hyp_open accounting does not close"))
    print("=== controls ===")
    d = parse(f"{logdir}/controls.log")
    s = report_stage("controls(global)", d, findings)
    # Per-arm linkage for the c7 segments (episode numbers overlap across
    # arms, so global linkage could misattribute; arm markers disambiguate).
    for arm in ("intact4", "intact5", "dep4", "dep5"):
        sd = subset(d, arm)
        if sd["refusals"] or sd["abstains"] or sd["hypopens"]:
            report_stage(f"controls/c7-{arm}", sd, findings, strict_keys=True)
    if d["telem"]:
        t = d["telem"]
        print(f"  C7_TELEMETRY: old4={t['old4']} old5={t['old5']} cons4={t['cons4']} "
              f"cons5={t['cons5']} cap4={t['cap4']} cap5={t['cap5']}")
    if d["posctrl"]:
        p = d["posctrl"]
        print(f"  C7_POSCTRL: cap4d={p['cap4d']} cap5d={p['cap5d']}")
    for arm in ("intact4", "intact5", "dep4", "dep5"):
        if arm in d["c7cap"]:
            c = d["c7cap"][arm]
            co, cn = cap_old(c), cap_old(c) - s["forced"]
            print(f"  C7CAP {arm}: cok={c['cok']} ccon={c['ccon']} mhyp={c['mhyp']} "
                  f"labst={c['labst']} lopen={c['lopen']} -> cap_old={co} cap_new={cn}")
    if mode == "gateless":
        if s["n_part"] != 0 or s["forced"] != 0:
            findings.append(("controls", "GATELESS",
                             f"gateless run has {s['n_part']} partition refusals / "
                             f"{s['forced']} forced"))
        else:
            print("  GATELESS OK: zero partition refusals, zero forced chains")
    print("=== findings ===")
    if not findings:
        print("  none")
    for name, code, msg in findings:
        print(f"  [{code}] {name}: {msg}")
    json.dump({"mode": mode, "findings": [(n, c, m) for n, c, m in findings]},
              open(f"{logdir}/link_report.json", "w"), indent=1)

if __name__ == "__main__":
    main()
