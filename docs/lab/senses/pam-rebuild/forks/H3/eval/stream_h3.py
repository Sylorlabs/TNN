#!/usr/bin/env python3
"""H3 streaming evaluation: 6 scenes, 600 episodes each, 40% adversarial.
Builds listfiles, runs sense_h3 stream, computes kill bars.
Usage: stream_h3.py <outdir>
"""
import subprocess, glob, os, re, json, sys

H3 = os.path.expanduser("~/workspace/h3work/build/sense_h3")
AA = os.path.expanduser("~/workspace/h3work/buildA/sense_a")
FX = os.path.expanduser("~/workspace/tnn-lab/senses/rebuild/harness/fixtures")
H3ADV = os.path.expanduser("~/workspace/tnn-lab/senses/pam-rebuild/forks/H3/fixtures/h3adv")

TASKS = [
    ("colordisc", "t1_colordisc", ".img", "t1"),
    ("colorconst", "t2_colorconst", ".img", "t2"),
    ("shapetrans", "t3_shapetrans", ".img", "t3"),
    ("pitchdisc", "t4_pitchdisc", ".pcm", "t4"),
    ("timbredisc", "t5_timbredisc", ".pcm", "t5"),
    ("motiondir", "t6_motiondir", ".vid", "t6"),
]

def build_list(task, tdir, ext, prefix, outpath):
    base = sorted(glob.glob(os.path.join(FX, tdir, "primary", "*" + ext)))
    adv_h = sorted(glob.glob(os.path.join(FX, tdir, "adversarial", "*" + ext)))
    adv_3 = sorted(glob.glob(os.path.join(H3ADV, "h3a_%s_*%s" % (prefix, ext))))
    adv = adv_h + adv_3
    # 600 episodes, pattern [B,B,B,A,A] -> 360 B, 240 A
    eps = []
    bi, ai = 0, 0
    pat = ["B", "B", "B", "A", "A"]
    for i in range(600):
        if pat[i % 5] == "B":
            eps.append(("B", base[bi % len(base)])); bi += 1
        else:
            eps.append(("A", adv[ai % len(adv)])); ai += 1
    with open(outpath, "w") as f:
        for kind, fx in eps:
            f.write(fx + "\n")
    return eps

def parse_stream(out):
    recs = []
    cur = {}
    for l in out.strip().split("\n"):
        if l.startswith("ledger_head="):
            ledger = l.split("=", 1)[1]
            continue
        if "=" not in l:
            continue
        k, v = l.split("=", 1)
        if k == "approach" and cur:
            recs.append(cur); cur = {}
        cur[k] = v
    if cur:
        recs.append(cur)
    return recs, ledger

def run_scene(task, tdir, ext, prefix, outdir, a_cache):
    os.makedirs(outdir, exist_ok=True)
    lp = os.path.join(outdir, "list_%s.txt" % task)
    eps = build_list(task, tdir, ext, prefix, lp)
    # truth for each episode
    truths = []
    for kind, fx in eps:
        truths.append(open(fx + ".truth").read().strip().split("=", 1)[1])
    # run H3 stream
    rh = subprocess.run([H3, "stream", task, lp], capture_output=True, text=True)
    recs, ledger = parse_stream(rh.stdout)
    assert len(recs) == 600, (task, len(recs))
    # A judgments from the base cache (same fixtures, deterministic binary)
    a_judges = [a_cache[fx] for kind, fx in eps]
    # join and compute
    rows = []
    for i, (kind, fx) in enumerate(eps):
        r = recs[i]
        rows.append({
            "ep": i, "kind": kind, "fixture": fx, "truth": truths[i],
            "t0": r.get("t0"), "judge": r.get("judgment"),
            "disp": r.get("disposition"), "durable": int(r.get("durable", 0)),
            "ops": int(r.get("ops", 0)), "transition": r.get("transition"),
            "chain": r.get("chain"), "a_judge": a_judges[i],
        })
    with open(os.path.join(outdir, "stream_%s.jsonl" % task), "w") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")
    with open(os.path.join(outdir, "ledger_%s.txt" % task), "w") as f:
        f.write(ledger + "\n")
    # kill bars
    n = len(rows)
    # 1. false permanent installs
    false_perm = sum(1 for r in rows if r["durable"] == 1 and r["judge"] != r["truth"])
    kb1 = false_perm / n
    # 2. injected false percepts withdrawn/quarantined
    # strict: disposition is WITHDRAWN or QUARANTINED (prereg letter).
    # lenient: also counts cases where the true claim installed instead.
    inj = [r for r in rows if r["kind"] == "A" and r["t0"] != r["truth"]]
    handled_strict = sum(1 for r in inj if r["disp"] in ("WITHDRAWN", "QUARANTINED"))
    handled_lenient = sum(1 for r in inj if r["disp"] in ("WITHDRAWN", "QUARANTINED") or r["judge"] == r["truth"])
    kb2 = (handled_strict / len(inj)) if inj else 1.0
    kb2_lenient = (handled_lenient / len(inj)) if inj else 1.0
    # 3. confirmed-percept recall
    base_true = [r for r in rows if r["kind"] == "B" and r["t0"] == r["truth"]]
    rec = sum(1 for r in base_true if r["disp"] == "INSTALLED")
    kb3 = (rec / len(base_true)) if base_true else 1.0
    # 4. regret
    reg_h3, reg_a = 0, 0
    for r in rows:
        t = r["truth"]
        # H3
        best_h = 1 if r["judge"] == t else 0
        if r["disp"] == "INSTALLED":
            taken_h = 1 if r["judge"] == t else -1
        else:
            taken_h = 0
        reg_h3 += best_h - taken_h
        # A
        best_a = 1 if r["a_judge"] == t else 0
        taken_a = 1 if r["a_judge"] == t else -1
        reg_a += best_a - taken_a
    kb4 = ((reg_a - reg_h3) / reg_a) if reg_a > 0 else 0.0
    summary = {
        "task": task, "n": n,
        "kb1_false_perm_rate": kb1, "kb1_n": false_perm,
        "kb2_injected": len(inj), "kb2_handled_rate": kb2,
        "kb2_handled_lenient": kb2_lenient,
        "kb3_base_true": len(base_true), "kb3_recall": kb3,
        "kb4_regret_h3": reg_h3, "kb4_regret_a": reg_a, "kb4_reduction": kb4,
        "ledger": ledger,
    }
    with open(os.path.join(outdir, "kill_%s.json" % task), "w") as f:
        json.dump(summary, f, indent=2)
    print(task, json.dumps(summary), flush=True)
    return summary

def main():
    outdir = sys.argv[1]
    cache_path = sys.argv[2]
    only = sys.argv[3] if len(sys.argv) > 3 else None
    # fixture path -> A judgment, from the base battery (deterministic)
    a_cache = {}
    for l in open(cache_path):
        r = json.loads(l)
        a_cache[r["fixture"]] = r["a_judge"]
    print("a_cache: %d fixtures" % len(a_cache), flush=True)
    for task, tdir, ext, prefix in TASKS:
        if only and task != only:
            continue
        run_scene(task, tdir, ext, prefix, outdir, a_cache)

if __name__ == "__main__":
    main()
