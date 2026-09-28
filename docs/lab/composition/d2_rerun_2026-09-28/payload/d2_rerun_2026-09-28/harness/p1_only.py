#!/usr/bin/env python3
"""D2 P1-only driver: teaching + 24 retrieval questions (one per P2 scenario).
Fresh session (teaching re-sent) — the single-session protocol exceeds the
learner's 64KB history arena before P1. P1 depends only on teaching + card.
Usage: p1_only.py <scenarios_dir> <output_dir>
"""
import subprocess, sys, os, re, json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from drive_d2 import LearnerChat
from teaching import SESSION_1, SESSION_2, SESSION_3, SESSION_4, SESSION_5
from score_d2 import parse_scen, D2BIN

def main():
    sdir, outdir = sys.argv[1], sys.argv[2]
    os.makedirs(outdir, exist_ok=True)
    files = sorted(f for f in os.listdir(sdir) if re.match(r"^(FW|WF|FWF)-\d+\.txt$", f))
    scens = [parse_scen(os.path.join(sdir, f)) for f in files]
    scens.sort(key=lambda s: s["k"])

    chat = LearnerChat()
    log = open(os.path.join(outdir, "driver.log"), "w")

    def say(msg, tag="TEACH"):
        log.write(f"[{tag}] {msg[:200]}\n"); log.flush()
        return chat.ask(msg)

    say(SESSION_1, "S1")
    say(SESSION_2, "S2")
    say(SESSION_3, "S3")
    say(SESSION_4, "S4")
    say(SESSION_5, "S5")

    results = {"P1": []}
    for s in scens:
        proc = subprocess.Popen([D2BIN, "tui", s["path"]],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                text=True, bufsize=1)
        card = []
        while True:
            line = proc.stdout.readline().strip()
            if line.startswith("OBS "):
                break
            card.append(line)
        proc.kill()
        for cl in card:
            chat.ask(cl)
        reply = chat.ask("Which sub-skills, in which order, does this scenario require? Reply with numbers like 1,2,3.")
        canon = {"FW": "1,2,3,1", "WF": "2,3,1", "FWF": "1,2,3,1,3,1"}[s["template"]]
        digits = "".join(re.findall(r"[123]", reply))
        canon_digits = canon.replace(",", "")
        correct = (digits == canon_digits)
        results["P1"].append({"scen": os.path.basename(s["path"]), "reply": reply,
                              "correct": correct, "canon": canon})
        log.write(f"[P1] {os.path.basename(s['path'])}: reply={reply!r} correct={correct}\n"); log.flush()

    chat.close()
    with open(os.path.join(outdir, "results.json"), "w") as f:
        json.dump(results, f, indent=1)
    npass = sum(1 for x in results["P1"] if x["correct"])
    print(f"P1: {npass}/{len(results['P1'])}")

if __name__ == "__main__":
    main()
