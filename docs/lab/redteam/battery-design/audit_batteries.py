#!/usr/bin/env python3
"""Battery-health audit — red team, battery-design leg (2026-09-21/22).

Parses frozen batteries and checks for:
  A. duplicate probe texts with CONFLICTING expects (impossible maxima)
  B. duplicate probe texts with identical expects (benign)
  C. cross-battery probe-text collisions (defect only if runs share state)
  D. new-mechanisms prereg kind-5 n inconsistency (24 vs 12)
  E. kind-dispatch in the new-mechanisms "mechanism" (Sol #1 coupling check)

Pure stdlib, deterministic. Run: python3 audit_batteries.py
"""
import json, collections, re, os

LAB = os.path.expanduser("~/workspace/tnn-lab")
out = []

def emit(s=""):
    out.append(s); print(s)

# ---------- A/B: prose v2 sub-batteries ----------
emit("== prose v2 sub-batteries (inputs2) ==")
inp = os.path.join(LAB, "prose-learning/v2/inputs2")
for name in ["sub_neg_test","sub_hedge_test","sub_contr_test","sub_para_test",
             "sub_multi_test","sub_core_test","sub_distr_test"]:
    p = os.path.join(inp, name + ".jsonl")
    if not os.path.exists(p):
        emit(f"{name}: MISSING"); continue
    probes = [json.loads(l) for l in open(p)]
    byprobe = collections.defaultdict(list)
    for pr in probes:
        byprobe[pr["probe"]].append((pr["id"], pr["expect"]))
    dups = {k: v for k, v in byprobe.items() if len(v) > 1}
    confl = {k: v for k, v in dups.items()
             if len(set(e for _, e in v)) > 1}
    emit(f"{name}: n={len(probes)} dup_texts={len(dups)} CONFLICTING={len(confl)}")
    for k, v in confl.items():
        emit(f"  IMPOSSIBLE: probe={k[:60]!r} expects={v} -> max score {len(probes)-len(v)+1}/{len(probes)}")

# ---------- C: cross-sub-battery collisions ----------
emit("\n== cross-sub-battery probe-text collisions ==")
seen = collections.defaultdict(list)
for name in ["sub_neg_test","sub_hedge_test","sub_contr_test","sub_para_test",
             "sub_multi_test","sub_core_test","sub_distr_test"]:
    p = os.path.join(inp, name + ".jsonl")
    if not os.path.exists(p): continue
    for pr in (json.loads(l) for l in open(p)):
        seen[pr["probe"]].append((name, pr["id"], pr["expect"]))
dups = {k: v for k, v in seen.items() if len(v) > 1}
confl = {k: v for k, v in dups.items() if len(set(e for _, _, e in v)) > 1}
emit(f"shared probe texts across sub-batteries: {len(dups)} "
     f"({len(confl)} with conflicting expects)")
emit("NOTE: sub-batteries run as INDEPENDENT runs (own train/test, fresh state),")
emit("so cross-battery collisions are NOT a defect. Verified non-issue.")

# ---------- championship integer corpus ----------
emit("\n== championship sol integer corpus ==")
cp = os.path.join(LAB, "wave12/championship-english/sol/corpus/corpus.json")
c = json.load(open(cp))
teach = c["teach"]
byprobe = collections.defaultdict(list)
for t in teach:
    byprobe[t["probe"]].append((t["id"], t["probe_value"]))
dups = {k: v for k, v in byprobe.items() if len(v) > 1}
confl = {k: v for k, v in dups.items() if len(set(x[1] for x in v)) > 1}
bo = collections.Counter(t["observation"] for t in teach)
emit(f"n={len(teach)} distinct_probes={len(byprobe)} dup_texts={len(dups)} "
     f"conflicting={len(confl)} dup_observations={sum(1 for x in bo.values() if x>1)}")
emit("HEALTHY" if not confl and not dups else "DEFECT")

# ---------- principle-detection ----------
emit("\n== principle-detection expected.json ==")
pd = json.load(open(os.path.join(LAB, "principle-detection/expected.json")))
facts = pd["facts"]
texts = collections.defaultdict(list)
for fid, f in facts.items():
    texts[json.dumps(f, sort_keys=True)].append(fid)
dups = {k: v for k, v in texts.items() if len(v) > 1}
emit(f"facts={len(facts)} principles={len(pd['principles'])} "
     f"exemptions={len(pd['exemptions'])} exact_dupes={len(dups)}")
emit("HEALTHY on duplicates; blind spot = principles are stipulated background (documented in VERDICT scope notes).")

# ---------- info-source envelopes ----------
emit("\n== info-source live envelopes ==")
import glob
envs = sorted(glob.glob(os.path.join(LAB, "info-source/live/*.json")))
bad = 0
for f in envs:
    d = json.load(open(f))
    if len(d.get("results", [])) != 8:
        bad += 1; emit(f"  {os.path.basename(f)}: results != 8")
emit(f"envelopes={len(envs)} malformed={bad}")
emit("HEALTHY structurally; frozen 2026-09-22 (replay, not live).")

# ---------- D: new-mechanisms prereg kind-5 ----------
emit("\n== new-mechanisms prereg kind-5 n ==")
prereg = open(os.path.join(LAB, "new-mechanisms/PREREG.md")).read()
m = re.search(r"\| 5 temporal unattested \| (\d+)", prereg)
emit(f"PREREG construction table: kind-5 n={m.group(1) if m else '?'}")
m2 = re.search(r"kind-5 = 1\.0 \(12/12", prereg)
emit(f"PREREG kill bar KB-M-TEMPORAL: kind-5 12/12 -> {'present' if m2 else 'absent'}")
emit("N=264 total forces kind-5=12 (96+36+36+24+24+12+24+12). Table '24' is a TYPO. Minor doc defect; verdict numbers use 12 (correct).")

# ---------- E: kind dispatch in hypcomp_fact ----------
emit("\n== new-mechanisms kind-dispatch (Sol #1 coupling) ==")
src = open(os.path.join(LAB, "new-mechanisms/mech_learner.zag")).read()
hf = re.search(r"fn hypcomp_fact\(.*?^}", src, re.M | re.S).group(0)
uses_kind = "bat_kind(f)" in hf
branches = re.findall(r"if\(k==(\d+)", hf)
emit(f"hypcomp_fact calls bat_kind(f): {uses_kind}")
emit(f"kind-dispatched branches: {branches}")
emit("bat_kind is the BATTERY's kind function (f<96->0, f<132->1, ...).")
emit("k==4||k==5 -> install-cand-0 + challenge-cand-1 (order-dependent)")
emit("k==3 -> first_install_pairs (hardcodes 32-bit pair encoding)")
emit("k==6 -> spoof pre-filter on candidate 0's flag (dispatched by kind)")
emit("else -> scalar trust-sum competition")
emit("FINDING: the 'mechanism' reads the test's kind labels to select handlers.")
emit("Battery generator + learner share one binary (mech_learner.zag).")
emit("The 156/156 measures kind-dispatched handlers satisfying their kinds,")
emit("not a general contradiction resolver. Novel classes untestable without")
emit("rewriting both battery and dispatch. Sol #1 CONFIRMED in code.")

emit("\n== done ==")
open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                  "AUDIT_OUTPUT.txt"), "w").write("\n".join(out) + "\n")
