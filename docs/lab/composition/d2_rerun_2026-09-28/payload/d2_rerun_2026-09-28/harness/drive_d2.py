#!/usr/bin/env python3
"""D2 learner driver: teaches the dialogue learner, runs P0/P1/P2/P3.
Usage: drive_d2.py <scenarios_dir> <output_dir>
"""
import subprocess, sys, os, re, time, json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from teaching import SESSION_1, SESSION_2, SESSION_3, SESSION_4, SESSION_5
from score_d2 import parse_scen, check_criteria, run_episode, D2BIN

LEARNER = os.path.expanduser("~/workspace/composition_d2_rerun/build/wb3_learner")

class LearnerChat:
    def __init__(self):
        self.p = subprocess.Popen([LEARNER, "chat"], stdin=subprocess.PIPE,
                                  stdout=subprocess.PIPE, text=True, bufsize=1)
        # read banner
        line = self.p.stdout.readline()
        assert line, "no banner from learner binary"
    def ask(self, msg):
        """Send a message, return the reply (after 'A ' prefix)."""
        # the learner expects single-line inputs; strip newlines from teaching
        msg = msg.replace("\n", " ").replace("\r", " ").strip()
        if not msg:
            return ""
        self.p.stdin.write(msg + "\n")
        self.p.stdin.flush()
        while True:
            resp = self.p.stdout.readline()
            if resp == "":
                raise RuntimeError("learner binary EOF mid-session")
            if resp.startswith("A "):
                return resp[2:].rstrip("\n").replace("\t", " ").replace("\r", "")
    def close(self):
        try:
            self.p.stdin.close()
        except Exception:
            pass
        self.p.wait()

def extract_digit(reply):
    """Extract first 0-6 digit from reply, or None."""
    m = re.search(r"[0-6]", reply)
    return m.group(0) if m else None

def run_tui_episode(scen_path, chat, log, abort_invalid=3):
    """Run one episode via d2 tui, with the learner as the policy.
    Returns (result_dict, trace). Aborts early if abort_invalid consecutive
    invalid replies (the episode is already FAIL per §5)."""
    scen = parse_scen(scen_path)
    proc = subprocess.Popen([D2BIN, "tui", scen_path],
                            stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                            text=True, bufsize=1)
    # read CARD lines (until first OBS)
    card_lines = []
    obs_line = None
    while True:
        line = proc.stdout.readline()
        if not line:
            break
        line = line.strip()
        if line.startswith("OBS "):
            obs_line = line
            break
        card_lines.append(line)
    # send card to learner (as context)
    for cl in card_lines:
        try:
            chat.ask(cl)
        except Exception:
            pass
    result = None
    trace = None
    consec_invalid = 0
    ticks_done = 0
    while obs_line:
        try:
            reply = chat.ask(obs_line)
        except Exception:
            break
        d = extract_digit(reply)
        if d is None:
            proc.stdin.write("X\n")
            consec_invalid += 1
        else:
            proc.stdin.write(d + "\n")
            consec_invalid = 0
        proc.stdin.flush()
        ticks_done += 1
        # early abort: episode already FAIL per §5, no need to burn ticks
        if consec_invalid >= abort_invalid:
            break
        line = proc.stdout.readline()
        if not line:
            break
        line = line.strip()
        if line.startswith("OBS "):
            obs_line = line
        elif line.startswith("RESULT "):
            result = line
            trace = proc.stdout.readline().strip()
            break
        else:
            break
    try:
        proc.stdin.close()
    except Exception:
        pass
    proc.wait()
    if result is None:
        # aborted early: synthesize a FAIL result
        result = f"RESULT learner {ticks_done} 0 0 0 0 999 -1 0 999"
        trace = "TRACE " + "X" * ticks_done
    parts = result.split()
    r = {
        "policy": parts[1], "ticks": int(parts[2]), "cause": int(parts[3]),
        "finalE": int(parts[4]), "nEat": int(parts[5]), "nCombine": int(parts[6]),
        "wastedEat": int(parts[7]), "wardTick": int(parts[8]),
        "unmitig": int(parts[9]), "invalid": int(parts[10]),
        "trace": trace.split()[1] if len(trace.split()) > 1 else "",
    }
    r["aborted"] = (result.startswith("RESULT learner") and ticks_done < scen["ep"])
    return r

def main():
    sdir, outdir = sys.argv[1], sys.argv[2]
    os.makedirs(outdir, exist_ok=True)
    files = sorted(f for f in os.listdir(sdir) if re.match(r"^(F|W|T|FW|WF|FWF|N)-\d+\.txt$", f))
    scens = [parse_scen(os.path.join(sdir, f)) for f in files]
    by = {}
    for s in scens:
        by.setdefault((s["phase"], s["template"]), []).append(s)
    # sort by k
    for k in by:
        by[k].sort(key=lambda s: s["k"])

    chat = LearnerChat()
    log = open(os.path.join(outdir, "driver.log"), "w")

    def say(msg, tag="TEACH"):
        log.write(f"[{tag}] {msg[:200]}\n"); log.flush()
        return chat.ask(msg)

    # --- teaching ---
    say(SESSION_1, "S1")
    # Practice S1: train-F (k=0..7)
    say(SESSION_2, "S2")
    for s in by[("train", "F")]:
        r = run_tui_episode(s["path"], chat, log)
        ok, reasons = check_criteria(s, r)
        log.write(f"[PRACTICE] {os.path.basename(s['path'])}: {'PASS' if ok else 'FAIL'} {reasons} nEat={r['nEat']}\n"); log.flush()
    # Practice S2: train-W
    say(SESSION_3, "S3")
    for s in by[("train", "W")]:
        r = run_tui_episode(s["path"], chat, log)
        ok, reasons = check_criteria(s, r)
        log.write(f"[PRACTICE] {os.path.basename(s['path'])}: {'PASS' if ok else 'FAIL'} {reasons} wardTick={r['wardTick']}\n"); log.flush()
    # Practice S3: train-T
    say(SESSION_4, "S4")
    for s in by[("train", "T")]:
        r = run_tui_episode(s["path"], chat, log)
        ok, reasons = check_criteria(s, r)
        log.write(f"[PRACTICE] {os.path.basename(s['path'])}: {'PASS' if ok else 'FAIL'} {reasons} nEat={r['nEat']} unmitig={r['unmitig']}\n"); log.flush()
    say(SESSION_5, "S5")

    results = {"P0": [], "P1": [], "P2": [], "P3": []}

    # --- P0 ---
    for (phase, template) in [("P0", "F"), ("P0", "W"), ("P0", "T")]:
        for s in by[(phase, template)]:
            r = run_tui_episode(s["path"], chat, log)
            ok, reasons = check_criteria(s, r)
            results["P0"].append({"scen": os.path.basename(s["path"]), "ok": ok,
                                  "reasons": reasons, "r": r})
            log.write(f"[P0] {os.path.basename(s['path'])}: {'PASS' if ok else 'FAIL'} {reasons}\n"); log.flush()

    # --- P1 + P2 (P1 per scenario, then episode) ---
    # Interleaved P2/P3 order: deterministic shuffle
    p2_scens = by[("P2", "FW")] + by[("P2", "WF")] + by[("P2", "FWF")]
    p3_scens = by[("P3", "N")]
    # interleave: FW, N, WF, FW, N, WF, ... (round-robin)
    order = []
    i2, i3 = 0, 0
    # simple deterministic interleave: sort P2 by k, insert P3 every 3rd
    p2_sorted = sorted(p2_scens, key=lambda s: s["k"])
    p3_sorted = sorted(p3_scens, key=lambda s: s["k"])
    pi = 0
    for s in p2_sorted:
        order.append(("P2", s))
        pi += 1
        if pi % 3 == 0 and i3 < len(p3_sorted):
            order.append(("P3", p3_sorted[i3])); i3 += 1
    while i3 < len(p3_sorted):
        order.append(("P3", p3_sorted[i3])); i3 += 1

    # P1: ask retrieval for each P2 scenario BEFORE its episode
    p1_answers = {}
    for s in p2_sorted:
        # send card lines as context, then ask
        proc = subprocess.Popen([D2BIN, "tui", s["path"]],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                text=True, bufsize=1)
        # read card, send to learner, then kill (we just need the card text)
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
        p1_answers[s["k"]] = reply
        # score P1
        canon = {"FW": "1,2,3,1", "WF": "2,3,1", "FWF": "1,2,3,1,3,1"}[s["template"]]
        # semantic/format-tolerant: extract digits in order
        digits = "".join(re.findall(r"[123]", reply))
        canon_digits = canon.replace(",", "")
        correct = (digits == canon_digits)
        results["P1"].append({"scen": os.path.basename(s["path"]), "reply": reply,
                              "correct": correct, "canon": canon})
        log.write(f"[P1] {os.path.basename(s['path'])}: reply={reply!r} correct={correct}\n"); log.flush()

    # P2/P3 episodes in interleaved order
    for phase, s in order:
        r = run_tui_episode(s["path"], chat, log)
        ok, reasons = check_criteria(s, r)
        results[phase].append({"scen": os.path.basename(s["path"]), "ok": ok,
                               "reasons": reasons, "r": r})
        log.write(f"[{phase}] {os.path.basename(s['path'])}: {'PASS' if ok else 'FAIL'} {reasons}\n"); log.flush()

    chat.close()
    # save results
    with open(os.path.join(outdir, "results.json"), "w") as f:
        # strip traces for size? keep them, they're small
        json.dump(results, f, indent=1)
    # summary
    for phase in ["P0", "P2", "P3"]:
        npass = sum(1 for x in results[phase] if x["ok"])
        print(f"{phase}: {npass}/{len(results[phase])}")
    np1 = sum(1 for x in results["P1"] if x["correct"])
    print(f"P1: {np1}/{len(results['P1'])}")

if __name__ == "__main__":
    main()
