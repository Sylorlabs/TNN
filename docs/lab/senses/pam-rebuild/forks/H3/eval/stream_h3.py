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
    # kill bars — corrected semantics live in eval/kb_analysis.py:
    #   KB1 denominator = injected false percepts (prereg §8.1), not all episodes.
    #   KB3 = end-of-scene memory state via verified replication (prereg §8.3),
    #   not per-episode disposition ratios.
    # The inline computation that used to be here was wrong on both counts;
    # it is superseded by kb_analysis.analyze().
    from kb_analysis import analyze as kb_analyze
    jf = os.path.join(outdir, "stream_%s.jsonl" % task)
    summary = kb_analyze(task, jf)
    summary["ledger_head"] = ledger
    with open(os.path.join(outdir, "kill_%s.json" % task), "w") as f:
        json.dump(summary, f, indent=2)
    print(task, json.dumps({k: (round(v, 4) if isinstance(v, float) else v)
                                      for k, v in summary.items()}), flush=True)
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
