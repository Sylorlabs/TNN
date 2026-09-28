#!/usr/bin/env python3
"""Red-team teaching attack: can the real learner be taught REVERSE (rule 0)
by FAIR means through its genuine chat intake?
Fair = no per-item answers, no probe-token teaching, no hardcoding,
same deliberate-memory machinery. Probe tokens tok(6..13) never taught.
Scoring = battery.zag's norm_last_word rule (last whitespace word, lowered,
trailing . stripped) == expected output.
"""
import subprocess, os, sys

WORK = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
BINDIR = os.path.join(WORK, "work")
BIN = os.path.join(BINDIR, "wb_dialogue_bin")

def tok(i):
    n = 2 + (i % 4)
    return "".join(chr(97 + ((i * 7 + k * 13 + k * k) % 26)) for k in range(n))

def rev(s): return s[::-1]

def last_word(resp):
    w = resp.strip().rstrip(".").rstrip()
    w = w.split()[-1] if w.split() else ""
    return w.lower().rstrip(".")

def run_session(turns, timeout=240):
    proc = subprocess.Popen([BIN, "chat"], cwd=BINDIR,
                            stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                            text=True, bufsize=1)
    banner = proc.stdout.readline()
    assert banner, "no banner"
    out = []
    try:
        for line in turns:
            line = line.strip()
            if not line: continue
            proc.stdin.write(line + "\n"); proc.stdin.flush()
            while True:
                resp = proc.stdout.readline()
                if resp == "": raise RuntimeError("EOF mid-session")
                if resp.startswith("A "):
                    out.append((line, resp[2:].rstrip("\n")))
                    break
    finally:
        try: proc.stdin.close()
        except Exception: pass
        proc.wait(timeout=timeout)
    return out

def score(responses):
    got = 0
    detail = []
    for t in range(6, 14):
        s = tok(t); exp = rev(s)
        resp = responses[t]
        ok = (last_word(resp) == exp)
        got += ok
        detail.append((s, exp, resp, ok))
    return got, detail

# ---- Arm A: exact Crew B replication (sanity) ----
teachA = ["reverse turns a word backwards."]
for t in range(6):
    s = tok(t)
    teachA.append(f"the reverse of {s} is {rev(s)}.")
probes = [f"what is the reverse of {tok(t)}?" for t in range(6, 14)]

sessA = run_session(teachA + probes)
respA = {t: r for (q, r), t in zip(sessA[len(teachA):], range(6, 14))}
gotA, detA = score(respA)

# ---- Arm B: rich fair teaching ----
# definition + procedure + 12 worked examples (tok 0..5, 700..705)
# each with letter walkthrough + reverse-letter walkthrough, then quizzes
teachB = [
    "reverse turns a word backwards.",
    "to reverse any word, read its letters from last to first, one at a time.",
]
train_idx = list(range(6)) + list(range(700, 706))
for t in train_idx:
    s = tok(t); r = rev(s)
    letters = " ".join(s)
    rletters = " ".join(r)
    teachB.append(f"the letters of {s} are {letters}.")
    teachB.append(f"to reverse {s}, read the letters backwards: {rletters}.")
    teachB.append(f"the reverse of {s} is {r}.")
# reinforcement quizzes on taught examples (fair: taught tokens only)
quiz = [f"what is the reverse of {tok(t)}?" for t in train_idx]
sessBq = run_session(teachB + quiz)
# fresh session: full teaching again, then held-out probes (avoid quiz
# contamination; each session is independent anyway)
sessB = run_session(teachB + probes)
respB = {t: r for (q, r), t in zip(sessB[len(teachB):], range(6, 14))}
gotB, detB = score(respB)
quiz_ok = sum(1 for (q, r) in sessBq[len(teachB):]
              for t in [None] if False)  # placeholder
# score quizzes properly
quiz_pairs = sessBq[len(teachB):]
qscore = 0
for (q, r), t in zip(quiz_pairs, train_idx):
    if last_word(r) == rev(tok(t)): qscore += 1

out = []
out.append(f"ARM A (Crew B replication): {gotA}/8 held-out")
for s, exp, resp, ok in detA:
    out.append(f"  {s} -> exp {exp} | resp: {resp[:60]!r} | {'OK' if ok else 'miss'}")
out.append(f"ARM B (rich fair teaching): quiz on taught {qscore}/{len(train_idx)}, held-out {gotB}/8")
for s, exp, resp, ok in detB:
    out.append(f"  {s} -> exp {exp} | resp: {resp[:60]!r} | {'OK' if ok else 'miss'}")
txt = "\n".join(out)
print(txt)
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "rt_teach_result.txt"), "w") as f:
    f.write(txt + "\n")
