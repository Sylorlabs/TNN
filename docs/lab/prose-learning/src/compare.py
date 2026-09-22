#!/usr/bin/env python3
"""Deep-compare Zag binary output vs the Python oracle, per source."""
import re, subprocess, sys
sys.path.insert(0, "/home/hatch/workspace/prose-learning/src")
exec(open("/home/hatch/workspace/prose-learning/src/oracle.py").read().split('if __name__')[0])

def parse_log(text):
    installs, probes, summ = {}, {}, {}
    for line in text.splitlines():
        if line.startswith("INSTALL "):
            m = dict(re.findall(r"(\w+)=([^\s]+)", line))
            installs[int(m["id"])] = m
        elif line.startswith("PROBE "):
            m = dict(re.findall(r"(\w+)=(-?\d+)", line))
            probes[int(m["id"])] = {k: int(v) for k, v in m.items()}
        elif line.startswith(("SUMMARY", "DIGEST ", "DIGEST2", "LEDGER", "VERIFY", "RESULT", "EXTRACT")):
            summ[line.split()[0]] = line
    return installs, probes, summ

ok_all = True
for src in ["grok", "sol", "step", "muse-native"]:
    r = run(src, "/home/hatch/workspace/prose-learning/inputs")
    p = subprocess.run(["/home/hatch/workspace/prose-learning/src/prose_learn_bin", src],
                       cwd="/home/hatch/workspace/prose-learning",
                       capture_output=True, text=True)
    assert p.returncode == 0, (src, p.returncode, p.stderr[-500:], p.stdout[-500:])
    installs, probes, summ = parse_log(p.stdout)
    errs = []
    # per-probe: installed, answer, want, correct, ties, best
    ans_by_fact = r["installed"]
    for pid, ntie, best in r["ties"]:
        zp = probes[pid]
        if zp["answer"] != r["answers"][pid]: errs.append(f"probe {pid} answer {zp['answer']} != {r['answers'][pid]}")
        if zp["want"] != [int(l.split("\t")[1]) for l in open(f"/home/hatch/workspace/prose-learning/inputs/test_{src}.txt")][pid]: errs.append(f"probe {pid} want mismatch")
        if zp["correct"] != r["corrects"][pid]: errs.append(f"probe {pid} correct {zp['correct']} != {r['corrects'][pid]}")
        if zp["ties"] != ntie: errs.append(f"probe {pid} ties {zp['ties']} != {ntie}")
        if zp["best"] != best: errs.append(f"probe {pid} best {zp['best']} != {best}")
        if zp["installed"] != ans_by_fact.get(pid, -1): errs.append(f"probe {pid} installed {zp['installed']} != {ans_by_fact.get(pid,-1)}")
    # installs: value, ntok, ndig, nword, keylen
    v = Vocab()
    for fid_s, sent in [l.rstrip("\n").split("\t", 1) for l in open(f"/home/hatch/workspace/prose-learning/inputs/train_{src}.txt")]:
        fid = int(fid_s)
        link, key, val, (nt, nd, nw) = pipeline(v, sent)
        zi = installs[fid]
        if int(zi["value"]) != val: errs.append(f"install {fid} value")
        if int(zi["ntok"]) != nt: errs.append(f"install {fid} ntok")
        if int(zi["ndig"]) != nd: errs.append(f"install {fid} ndig")
        if int(zi["nword"]) != nw: errs.append(f"install {fid} nword")
        if int(zi["keylen"]) != len(key): errs.append(f"install {fid} keylen")
    # summary/digest/ledger
    if r["digest"] not in summ["DIGEST"]: errs.append("digest")
    if r["ledger"] not in summ["LEDGER"]: errs.append("ledger")
    m = re.search(r"extract=(\d+)/(\d+) full=(\d+)/(\d+) clean=(\d+)/(\d+) absorb=(\d+)/(\d+)", summ["SUMMARY"])
    e, f, c, a = (int(m.group(1)), int(m.group(3)), int(m.group(5)), int(m.group(7)))
    if not (e == r["extract_ok"] and f == r["full"] and c == r["clean"] and a == r["absorb"]):
        errs.append(f"summary {(e,f,c,a)} vs {(r['extract_ok'],r['full'],r['clean'],r['absorb'])}")
    if "RESULT PASS" not in summ["RESULT"]: errs.append("result")
    if "chain=1" not in summ["VERIFY"] or "dmatch=1" not in summ["VERIFY"]: errs.append("verify")
    status = "OK " if not errs else "FAIL"
    if errs: ok_all = False
    print(f"{src}: {status} ({len(errs)} diffs)")
    for e_ in errs[:10]: print("   ", e_)
print("ALL OK" if ok_all else "MISMATCHES FOUND")
