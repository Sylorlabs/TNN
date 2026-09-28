#!/usr/bin/env python3
"""D1 battery driver — teaches the 6 string-rewrite rules and administers
P0/P1/P2/P3 probes to the REAL TNN learner (wb_dialogue_bin, chat mode).

Pure I/O plumbing: the teaching lines, query shapes, and session plan are the
FIXED protocol documented in INTERPRETATION.md. No thinking, no per-response
adaptation, no tuning. Deterministic: same protocol, same bytes, every run.

Usage: drive.py <rundir>
Writes <rundir>/resp_p0.txt, resp_p3.txt, resp_samples.txt, teach_log.txt
"""
import subprocess, sys, os

WORK = os.path.dirname(os.path.abspath(__file__))
BINDIR = os.path.join(WORK, "work")  # learner binary + kb.txt + gaz.txt live here
BIN = os.path.join(BINDIR, "wb_dialogue_bin")

RULES = [
    (0, "reverse",    "reverse turns a word backwards."),
    (1, "dupfirst",   "dupfirst doubles the first letter of a word."),
    (2, "rotleft",    "rotleft moves the first letter of a word to the end."),
    (3, "droplast",   "droplast removes the last letter of a word."),
    (4, "upperfirst", "upperfirst capitalizes the first letter of a word."),
    (5, "sortchars",  "sortchars sorts the letters of a word alphabetically."),
]

def tok(i):
    n = 2 + (i % 4)
    return "".join(chr(97 + ((i * 7 + k * 13 + k * k) % 26)) for k in range(n))

def apply_rule(r, s):
    if r == 0: return s[::-1]
    if r == 1: return s[0] + s
    if r == 2: return s[1:] + s[:1] if s else ""
    if r == 3: return s[:-1]
    if r == 4: return s[0].upper() + s[1:] if s else ""
    return "".join(sorted(s))

def compose(parts, s):
    for r in parts:
        s = apply_rule(r, s)
    return s

def teach_lines(r):
    _, name, defn = RULES[r]
    lines = [defn]
    for t in range(6):
        s = tok(t)
        lines.append(f"the {name} of {s} is {apply_rule(r, s)}.")
    return lines

def teach_all():
    lines = []
    for r in range(6):
        lines.extend(teach_lines(r))
    return lines

def run_session(turns, timeout=180):
    """One fresh learner process; returns list of (turn, response)."""
    proc = subprocess.Popen([BIN, "chat"], cwd=BINDIR,
                            stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                            text=True, bufsize=1)
    banner = proc.stdout.readline()
    assert banner, "no banner from learner binary"
    out = []
    try:
        for line in turns:
            line = line.strip()
            if not line:
                continue
            proc.stdin.write(line + "\n")
            proc.stdin.flush()
            while True:
                resp = proc.stdout.readline()
                if resp == "":
                    raise RuntimeError("learner binary EOF mid-session")
                if resp.startswith("A "):
                    r = resp[2:].rstrip("\n").replace("\t", " ").replace("\r", "")
                    out.append((line, r))
                    break
    finally:
        try: proc.stdin.close()
        except Exception: pass
        proc.wait(timeout=timeout)
    return out

def main():
    rundir = sys.argv[1]
    os.makedirs(rundir, exist_ok=True)
    teach_log = open(os.path.join(rundir, "teach_log.txt"), "w")
    p0f = open(os.path.join(rundir, "resp_p0.txt"), "w")
    p0c = open(os.path.join(rundir, "resp_p0c.txt"), "w")  # positive controls (taught tok)
    p3f = open(os.path.join(rundir, "resp_p3.txt"), "w")
    smpf = open(os.path.join(rundir, "resp_samples.txt"), "w")

    # ---- P0: one fresh session per rule ----
    for r, name, _ in RULES:
        turns = teach_lines(r)
        for t in turns:
            teach_log.write(f"P0R{r}\t{t}\n")
        # positive control: taught token tok(0)
        ctl_tok = tok(0)
        ctl_q = f"what is the {name} of {ctl_tok}?"
        # held-out probes tok(6..13)
        probes = [f"what is the {name} of {tok(t)}?" for t in range(6, 14)]
        sess = run_session(turns + [ctl_q] + probes)
        # sess[0..6] are teaching acks; [-9] is control; [-8:] are probes
        ci, cr = sess[7]
        p0c.write(f"P0C {r} 0\n{cr}\n")
        for (q, resp), t in zip(sess[8:], range(6, 14)):
            assert str(tok(t)) in q, (q, t)
            p0f.write(f"P0 {r} {t}\n{resp}\n")

    # ---- P3: one session, all rules taught, 8 distractor probes ----
    turns = teach_all()
    for t in turns:
        teach_log.write(f"P3\t{t}\n")
    probes = [f"what is {tok(t)}?" for t in range(614, 622)]
    sess = run_session(turns + probes)
    for (q, resp), t in zip(sess[len(turns):], range(614, 622)):
        p3f.write(f"P3 {t}\n{resp}\n")

    # ---- Samples: P1 (6), P2 pairs (10) + triples (2) ----
    turns = teach_all()
    for t in turns:
        teach_log.write(f"SMP\t{t}\n")
    prompts = []
    # P1 samples: pairs (0,1),(2,3),(4,5),(1,4),(3,0),(5,2), idx0 inputs
    p1pairs = [(0, 1), (2, 3), (4, 5), (1, 4), (3, 0), (5, 2)]
    for k, (a, b) in enumerate(p1pairs):
        pidx = a * 5 + (b if b < a else b - 1)
        s = tok(14 + pidx * 4)
        exp = compose([a, b], s)
        na, nb = RULES[a][1], RULES[b][1]
        prompts.append((f"P1 {k} pair {a},{b} tok {14+pidx*4}",
                        f"which two rules, in which order, turn {s} into {exp}?"))
    # P2 samples: 10 pairs + 2 triples (first items)
    p2spec = [("pair", (0, 1)), ("pair", (1, 0)), ("pair", (2, 3)), ("pair", (3, 2)),
              ("pair", (4, 5)), ("pair", (5, 4)), ("pair", (0, 5)), ("pair", (5, 0)),
              ("pair", (1, 3)), ("pair", (3, 1))]
    for k, (kind, pr) in enumerate(p2spec):
        a, b = pr
        pidx = a * 5 + (b if b < a else b - 1)
        s = tok(14 + pidx * 4)
        na, nb = RULES[a][1], RULES[b][1]
        prompts.append((f"P2 {k} pair {a},{b} tok {14+pidx*4}",
                        f"what is the {na} then {nb} of {s}?"))
    # 2 triple samples: (0,1,2) and (5,4,3), first inputs
    for k2, (a, b, c) in enumerate([(0, 1, 2), (5, 4, 3)]):
        # triple index: lexicographic; compute by enumeration
        ti = 0
        for i in range(6):
            for j in range(6):
                if j == i: continue
                for kk in range(6):
                    if kk == i or kk == j: continue
                    if (i, j, kk) == (a, b, c):
                        s = tok(134 + ti * 4)
                    ti += 1
        na, nb, nc = RULES[a][1], RULES[b][1], RULES[c][1]
        prompts.append((f"P2 {10+k2} triple {a},{b},{c}",
                        f"what is the {na} then {nb} then {nc} of {s}?"))
    sess = run_session(turns + [p for _, p in prompts])
    for (tag, _), (q, resp) in zip(prompts, sess[len(turns):]):
        smpf.write(f"SMP {tag}\n{q}\n{resp}\n")

    for f in (teach_log, p0f, p0c, p3f, smpf):
        f.close()
    print(f"wrote {rundir}: P0 sessions=6, P3 session=1, sample session=1")

if __name__ == "__main__":
    main()
