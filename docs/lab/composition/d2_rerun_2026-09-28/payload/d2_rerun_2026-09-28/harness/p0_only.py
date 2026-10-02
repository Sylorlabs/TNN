#!/usr/bin/env python3
"""D2 P0-only driver: teaching + practice + P0 (24 probes).
Single session; stays under the learner's 64KB history arena (~63KB).
Usage: p0_only.py <scenarios_dir> <output_dir>
"""
import subprocess, sys, os, re, json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from drive_d2 import LearnerChat, run_tui_episode
from teaching import SESSION_1, SESSION_2, SESSION_3, SESSION_4, SESSION_5
from score_d2 import parse_scen, check_criteria

def main():
    sdir, outdir = sys.argv[1], sys.argv[2]
    os.makedirs(outdir, exist_ok=True)
    files = sorted(f for f in os.listdir(sdir) if re.match(r"^(F|W|T)-\d+\.txt$", f))
    scens = [parse_scen(os.path.join(sdir, f)) for f in files]
    by = {}
    for s in scens:
        by.setdefault((s["phase"], s["template"]), []).append(s)
    for k in by:
        by[k].sort(key=lambda s: s["k"])

    chat = LearnerChat()
    log = open(os.path.join(outdir, "driver.log"), "w")

    def say(msg, tag="TEACH"):
        log.write(f"[{tag}] {msg[:200]}\n"); log.flush()
        return chat.ask(msg)

    say(SESSION_1, "S1")
    say(SESSION_2, "S2")
    for s in by[("train", "F")]:
        r = run_tui_episode(s["path"], chat, log)
        ok, reasons = check_criteria(s, r)
        log.write(f"[PRACTICE] {os.path.basename(s['path'])}: {'PASS' if ok else 'FAIL'} {reasons}\n"); log.flush()
    say(SESSION_3, "S3")
    for s in by[("train", "W")]:
        r = run_tui_episode(s["path"], chat, log)
        ok, reasons = check_criteria(s, r)
        log.write(f"[PRACTICE] {os.path.basename(s['path'])}: {'PASS' if ok else 'FAIL'} {reasons}\n"); log.flush()
    say(SESSION_4, "S4")
    for s in by[("train", "T")]:
        r = run_tui_episode(s["path"], chat, log)
        ok, reasons = check_criteria(s, r)
        log.write(f"[PRACTICE] {os.path.basename(s['path'])}: {'PASS' if ok else 'FAIL'} {reasons}\n"); log.flush()
    say(SESSION_5, "S5")

    results = {"P0": []}
    for (phase, template) in [("P0", "F"), ("P0", "W"), ("P0", "T")]:
        for s in by[(phase, template)]:
            r = run_tui_episode(s["path"], chat, log)
            ok, reasons = check_criteria(s, r)
            results["P0"].append({"scen": os.path.basename(s["path"]), "ok": ok,
                                  "reasons": reasons, "r": r})
            log.write(f"[P0] {os.path.basename(s['path'])}: {'PASS' if ok else 'FAIL'} {reasons}\n"); log.flush()

    chat.close()
    with open(os.path.join(outdir, "results.json"), "w") as f:
        json.dump(results, f, indent=1)
    npass = sum(1 for x in results["P0"] if x["ok"])
    print(f"P0: {npass}/{len(results['P0'])}")

if __name__ == "__main__":
    main()
