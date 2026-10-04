#!/usr/bin/env python3
"""Mock drive_d2: runs the H1 prototype through teaching + practice + eval
against the real d2bin instrument, mirroring harness/drive_d2.py protocol."""
import subprocess, os, re, sys

sys.path.insert(0, os.path.expanduser("~/workspace/composition_d2_rerun/harness"))
from teaching import SESSION_1, SESSION_2, SESSION_3, SESSION_4, SESSION_5
from score_d2 import parse_scen, check_criteria

D2BIN = os.path.expanduser("~/workspace/composition_d2_rerun/d2build/d2bin")
PROTO = os.path.expanduser("~/workspace/d2_new_learner/h1/h1bin")
SDIR = os.path.expanduser("~/workspace/composition_d2_rerun/src/docs/lab/composition/d2/scenarios")

class Chat:
    def __init__(self):
        env = dict(os.environ)
        if len(sys.argv) > 1:
            env["H1_TRACEFILE"] = sys.argv[1]
        self.p = subprocess.Popen([PROTO, "chat"],
                                  stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                  text=True, bufsize=1, env=env)
        line = self.p.stdout.readline()
        assert line, "no banner"
        print("banner:", line.strip())
    def ask(self, msg):
        msg = msg.replace("\n", " ").replace("\r", " ").strip()
        if not msg:
            return ""
        self.p.stdin.write(msg + "\n")
        self.p.stdin.flush()
        while True:
            resp = self.p.stdout.readline()
            if resp == "":
                raise RuntimeError("learner EOF")
            if resp.startswith("A "):
                return resp[2:].rstrip("\n")
    def close(self):
        try: self.p.stdin.close()
        except Exception: pass
        self.p.wait()

def extract_digit(reply):
    m = re.search(r"[0-6]", reply)
    return m.group(0) if m else None

def run_episode(scen_path, chat):
    scen = parse_scen(scen_path)
    proc = subprocess.Popen([D2BIN, "tui", scen_path], stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, text=True, bufsize=1)
    card_lines = []; obs_line = None
    while True:
        line = proc.stdout.readline()
        if not line: break
        line = line.strip()
        if line.startswith("OBS "):
            obs_line = line; break
        card_lines.append(line)
    for cl in card_lines:
        chat.ask(cl)
    result = None; trace = None; consec_invalid = 0; ticks_done = 0
    while obs_line:
        reply = chat.ask(obs_line)
        d = extract_digit(reply)
        if d is None:
            proc.stdin.write("X\n"); consec_invalid += 1
        else:
            proc.stdin.write(d + "\n"); consec_invalid = 0
        proc.stdin.flush(); ticks_done += 1
        if consec_invalid >= 3: break
        line = proc.stdout.readline()
        if not line: break
        line = line.strip()
        if line.startswith("OBS "): obs_line = line
        elif line.startswith("RESULT "):
            result = line; trace = proc.stdout.readline().strip(); break
        else: break
    try: proc.stdin.close()
    except Exception: pass
    proc.wait()
    if result is None:
        result = f"RESULT learner {ticks_done} 0 0 0 0 999 -1 0 999"
        trace = "TRACE " + "X" * ticks_done
    parts = result.split()
    r = {"policy": parts[1], "ticks": int(parts[2]), "cause": int(parts[3]),
         "finalE": int(parts[4]), "nEat": int(parts[5]), "nCombine": int(parts[6]),
         "wastedEat": int(parts[7]), "wardTick": int(parts[8]),
         "unmitig": int(parts[9]), "invalid": int(parts[10]),
         "trace": trace.split()[1] if len(trace.split()) > 1 else ""}
    return r

def main():
    chat = Chat()
    def say(m): return chat.ask(m)
    say(SESSION_1); say(SESSION_2)
    files = sorted(f for f in os.listdir(SDIR) if re.match(r"^(F|W|T)-\d+\.txt$", f))
    scens = [parse_scen(os.path.join(SDIR, f)) for f in files]
    by = {}
    for s in scens:
        by.setdefault((s["phase"], s["template"]), []).append(s)
    for k in by: by[k].sort(key=lambda s: s["k"])
    print(f"=== PRACTICE (24 episodes) ===")
    for s in by[("train","F")]:
        r = run_episode(s["path"], chat)
        ok, reasons = check_criteria(s, r)
        print(f'[PRACTICE] {os.path.basename(s["path"])}: {"PASS" if ok else "FAIL"} {reasons} nEat={r["nEat"]}', flush=True)
    say(SESSION_3)
    for s in by[("train","W")]:
        r = run_episode(s["path"], chat)
        ok, reasons = check_criteria(s, r)
        print(f'[PRACTICE] {os.path.basename(s["path"])}: {"PASS" if ok else "FAIL"} {reasons} wardTick={r["wardTick"]} unmitig={r["unmitig"]}', flush=True)
    say(SESSION_4)
    for s in by[("train","T")]:
        r = run_episode(s["path"], chat)
        ok, reasons = check_criteria(s, r)
        print(f'[PRACTICE] {os.path.basename(s["path"])}: {"PASS" if ok else "FAIL"} {reasons} nEat={r["nEat"]} unmitig={r["unmitig"]}', flush=True)
    say(SESSION_5)
    print("=== P0 (held-out) ===")
    for key in [("P0","F"),("P0","W"),("P0","T")]:
        npass = 0
        for s in by[key]:
            r = run_episode(s["path"], chat)
            ok, reasons = check_criteria(s, r)
            npass += ok
            print(f'[P0] {os.path.basename(s["path"])}: {"PASS" if ok else "FAIL"} {reasons} nEat={r["nEat"]} wardTick={r["wardTick"]} unmitig={r["unmitig"]} finalE={r["finalE"]}', flush=True)
        print(f"P0-{key[1]}: {npass}/{len(by[key])}")
    chat.close()

if __name__ == "__main__":
    main()
