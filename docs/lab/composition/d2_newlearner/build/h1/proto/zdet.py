#!/usr/bin/env python3
"""Determinism self-check: run teaching + 24 practice scenarios through h1bin,
capture the action trace (all replies), and byte-compare across runs.
Usage: zdet.py <output_trace_file>"""
import subprocess, os, sys

sys.path.insert(0, os.path.expanduser("~/workspace/composition_d2_rerun/harness"))
from teaching import SESSION_1, SESSION_2, SESSION_3, SESSION_4
from score_d2 import parse_scen

D2BIN = os.path.expanduser("~/workspace/composition_d2_rerun/d2build/d2bin")
HBIN = os.path.expanduser("~/workspace/d2_new_learner/h1/h1bin")
SDIR = os.path.expanduser("~/workspace/composition_d2_rerun/src/docs/lab/composition/d2/scenarios")

def run_episode(chat, scen_path):
    """Feed one scenario's card+OBS lines, return list of action digits."""
    proc = subprocess.run([D2BIN, "tui", scen_path], input="6\n" * 500,
                          capture_output=True, text=True, timeout=20)
    actions = []
    for raw in proc.stdout.split("\n"):
        if raw.startswith("CARD ") or raw.startswith("OBS "):
            r = chat.ask(raw)
            if r.startswith("A ") and len(r) == 3 and r[2].isdigit():
                actions.append(r[2])
    return actions

class Chat:
    def __init__(self, env):
        self.p = subprocess.Popen([HBIN, "chat"], stdin=subprocess.PIPE,
                                  stdout=subprocess.PIPE, text=True, bufsize=1, env=env)
        line = self.p.stdout.readline()
        assert line, "no banner"
    def ask(self, msg):
        msg = msg.replace("\n", " ").replace("\r", " ").strip()
        self.p.stdin.write(msg + "\n")
        self.p.stdin.flush()
        while True:
            r = self.p.stdout.readline()
            if r.startswith("A "):
                return r.strip()
    def close(self):
        self.p.stdin.close()
        self.p.wait()

def main():
    out_path = sys.argv[1]
    env = dict(os.environ)
    chat = Chat(env)
    trace = []
    # teaching (sessions 1-4; 5 has no OBS content for the learner)
    for s in [SESSION_1, SESSION_2, SESSION_3, SESSION_4]:
        r = chat.ask(s)
        trace.append(r)
    # 24 practice scenarios: F-0..F-7, W-8..W-15, T-16..T-23
    scen_ids = [f"F-{i}" for i in range(8)] + [f"W-{i}" for i in range(8, 16)] + [f"T-{i}" for i in range(16, 24)]
    for sid in scen_ids:
        path = os.path.join(SDIR, f"{sid}.txt")
        acts = run_episode(chat, path)
        trace.append(f"{sid}:" + "".join(acts))
    chat.close()
    with open(out_path, "w") as f:
        f.write("\n".join(trace) + "\n")
    print(f"wrote {out_path}: {len(trace)} lines, {sum(len(l) for l in trace)} chars")

if __name__ == "__main__":
    main()
