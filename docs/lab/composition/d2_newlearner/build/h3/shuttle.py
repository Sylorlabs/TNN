#!/usr/bin/env python3
"""H3 self-check shuttle: drives h3bin (chat/chat-fixed) against d2bin tui,
replicating harness/drive_d2.py's run_tui_episode + score_d2.check_criteria.
Usage: shuttle.py <h3bin> <mode: chat|chat-fixed> <scenarios...> [--teach]
"""
import subprocess, re, sys, os

D2BIN = os.path.expanduser("~/workspace/composition_d2_rerun/d2build/d2bin")
HARN = os.path.expanduser("~/workspace/composition_d2_rerun/harness")
sys.path.insert(0, HARN)
from score_d2 import parse_scen, check_criteria

P1_Q = "Which sub-skills, in which order, does this scenario require? Reply with numbers like 1,2,3."

def extract_digit(reply):
    m = re.search(r"[0-6]", reply)
    return m.group(0) if m else None

class Chat:
    def __init__(self, h3bin, mode):
        self.p = subprocess.Popen([h3bin, mode], stdin=subprocess.PIPE,
                                  stdout=subprocess.PIPE, text=True, bufsize=1)
        self.banner = self.p.stdout.readline().strip()
    def ask(self, line):
        self.p.stdin.write(line + "\n"); self.p.stdin.flush()
        while True:
            r = self.p.stdout.readline()
            if not r: raise EOFError("h3bin closed stdout")
            r = r.strip()
            if r.startswith("A "): return r
            # ignore any non-A lines (shouldn't happen)
    def close(self):
        try: self.p.stdin.close()
        except Exception: pass
        self.p.wait()

def run_episode(scen_path, chat, teach_texts):
    proc = subprocess.Popen([D2BIN, "tui", scen_path], stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, text=True, bufsize=1)
    card_lines, obs_line = [], None
    while True:
        line = proc.stdout.readline()
        if not line: break
        line = line.strip()
        if line.startswith("OBS "): obs_line = line; break
        card_lines.append(line)
    for cl in card_lines: chat.ask(cl)
    p1 = chat.ask(P1_Q)
    p1digits = "".join(re.findall(r"[123]", p1))
    for t in teach_texts: chat.ask(t.replace("\n", " "))
    result, trace, ticks = None, None, 0
    consec_invalid = 0
    while obs_line:
        reply = chat.ask(obs_line)
        d = extract_digit(reply)
        if d is None:
            proc.stdin.write("X\n"); consec_invalid += 1
        else:
            proc.stdin.write(d + "\n"); consec_invalid = 0
        proc.stdin.flush(); ticks += 1
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
        result = f"RESULT learner {ticks} 0 0 0 0 999 -1 0 999"
        trace = "TRACE " + "X" * ticks
    parts = result.split()
    r = {"ticks": int(parts[2]), "cause": int(parts[3]), "finalE": int(parts[4]),
         "nEat": int(parts[5]), "nCombine": int(parts[6]), "wastedEat": int(parts[7]),
         "wardTick": int(parts[8]), "unmitig": int(parts[9]), "invalid": int(parts[10]),
         "trace": trace.split()[1] if len(trace.split()) > 1 else ""}
    return r, p1digits

def main():
    args = sys.argv[1:]
    teach = "--teach" in args; args = [a for a in args if a != "--teach"]
    h3bin, mode = args[0], args[1]
    scens = args[2:]
    teach_texts = []
    if teach:
        sys.path.insert(0, HARN)
        from teaching import SESSION_2, SESSION_3, SESSION_4
        teach_texts = [SESSION_2, SESSION_3, SESSION_4]
    chat = Chat(h3bin, mode)
    print("banner:", chat.banner, file=sys.stderr)
    ok = tot = 0
    for sp in scens:
        s = parse_scen(sp)
        r, p1d = run_episode(sp, chat, teach_texts)
        verdict, notes = check_criteria(s, r)
        mark = "PASS" if verdict else "FAIL"
        if verdict: ok += 1
        tot += 1
        print(f"{os.path.basename(sp):12s} {mark:4s} p1={p1d:8s} ticks={r['ticks']:3d} E={r['finalE']:3d} "
              f"eat={r['nEat']:2d} comb={r['nCombine']} waste={r['wastedEat']} wardT={r['wardTick']:3d} "
              f"unmit={r['unmitig']} inv={r['invalid']} | {notes}")
    chat.close()
    print(f"== {ok}/{tot} PASS ==")

if __name__ == "__main__":
    main()
