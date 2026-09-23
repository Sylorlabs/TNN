#!/usr/bin/env python3
"""Run H3+A on one task's fixtures. Usage: eval_task.py <task> <out.jsonl>"""
import subprocess, glob, os, re, json, sys

H3 = os.path.expanduser("~/workspace/h3work/build/sense_h3")
AA = os.path.expanduser("~/workspace/h3work/buildA/sense_a")
FX = os.path.expanduser("~/workspace/tnn-lab/senses/rebuild/harness/fixtures")
H3ADV = os.path.expanduser("~/workspace/tnn-lab/senses/pam-rebuild/forks/H3/fixtures/h3adv")

TASKS = {
    "colordisc": ("t1_colordisc", ".img", "t1"),
    "colorconst": ("t2_colorconst", ".img", "t2"),
    "shapetrans": ("t3_shapetrans", ".img", "t3"),
    "pitchdisc": ("t4_pitchdisc", ".pcm", "t4"),
    "timbredisc": ("t5_timbredisc", ".pcm", "t5"),
    "motiondir": ("t6_motiondir", ".vid", "t6"),
}

def parse_out(out):
    return dict(l.split("=", 1) for l in out.strip().split("\n") if "=" in l)

def main():
    task = sys.argv[1]
    outp = sys.argv[2]
    tdir, ext, prefix = TASKS[task]
    jobs = []
    for split in ["primary", "noise", "adversarial"]:
        for f in sorted(glob.glob(os.path.join(FX, tdir, split, "*" + ext))):
            jobs.append((split, f))
    for f in sorted(glob.glob(os.path.join(H3ADV, "h3a_%s_*%s" % (prefix, ext)))):
        jobs.append(("h3adv", f))
    print("%s: %d jobs" % (task, len(jobs)), flush=True)
    with open(outp, "w") as out:
        for i, (split, fx) in enumerate(jobs):
            truth = open(fx + ".truth").read().strip().split("=", 1)[1]
            rh = subprocess.run([H3, task, fx], capture_output=True, text=True).stdout
            ra = subprocess.run([AA, task, fx], capture_output=True, text=True).stdout
            dh, da = parse_out(rh), parse_out(ra)
            r = {"task": task, "fixture": fx, "truth": truth, "split": split,
                 "h3_judge": dh.get("judgment"), "h3_disp": dh.get("disposition"),
                 "h3_conf": int(dh.get("confidence", 0)), "h3_ops": int(dh.get("ops", 0)),
                 "h3_transition": dh.get("transition"), "h3_chain": dh.get("chain"),
                 "a_judge": da.get("judgment"), "a_ops": int(da.get("ops", 0))}
            out.write(json.dumps(r) + "\n")
            if (i+1) % 20 == 0:
                print("  %d/%d" % (i+1, len(jobs)), flush=True)
    print("wrote %s" % outp, flush=True)

if __name__ == "__main__":
    main()
