#!/usr/bin/env python3
"""D1 battery driver UNDER THE AMENDED PREREG — real TNN learner sessions.

Teaching protocol: Crew C's red-team-certified fair teaching (rt_teach.py
Arm B), generalized to all 6 rules: definition + explicit procedure + 12
worked examples (tok 0..5 and tok 700..705, train salt C=13), each with a
letter-walkthrough, a procedure walkthrough, and the result. Fair = no
probe-token teaching, no per-item answers, no hardcoding, same
deliberate-memory machinery. Probes always the held-out tok 6..13 (P0 salt).

Session plan (fixed pre-run; pure relay, no per-response adaptation):
 - 6 P0 sessions (one per rule, fresh process each): rich teaching (38 lines)
   + 2 taught controls (tok 0, tok 1; receipt check) + 8 held-out probes
   (tok 6..13) with P3 distractors INTERLEAVED (A3): sessions 0,1 take
   distractors tok 614,615 / 616,617; sessions 2..5 take one each
   (618,619,620,621). Distractor prompt: "what is <tok>?" (no part named).
 - 1 samples session (qualitative only, not scored): all-rules rich teaching
   + 6 P1 prompts (A3 neutral-index form) + 10 pair + 2 triple P2 prompts
   (A3 direct-pair form, neutral indices).

Deterministic: same protocol, same bytes, every run. Zero RNG.

Usage: drive_amended.py <rundir>
Writes <rundir>/resp_p0.txt, resp_p0c.txt, resp_p3.txt, resp_samples.txt,
      teach_log.txt
"""
import subprocess, sys, os

WORK = os.path.dirname(os.path.abspath(__file__))
# real learner binary lives in the Crew B workdir (reused, not copied)
BINDIR = os.path.join(WORK, "..", "battery", "work")
BIN = os.path.join(BINDIR, "wb_dialogue_bin")

PHASE_C = {0: 13, 1: 17, 2: 19, 3: 23}
def tokphase(i):
    if i >= 700: return 0
    if i < 6: return 0
    if i < 14: return 1
    if i < 614: return 2
    return 3
def tok(i):
    c = PHASE_C[tokphase(i)]
    n = 2 + (i % 4)
    return "".join(chr(97 + ((i * 7 + k * c + k * k) % 26)) for k in range(n))

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

# (name, definition, procedure, walkthrough-fmt)
RULES = [
    (0, "reverse",
     "reverse turns a word backwards.",
     "to reverse any word, read its letters from last to first, one at a time.",
     lambda s, e: f"to reverse {s}, read the letters backwards: {' '.join(e)}."),
    (1, "dupfirst",
     "dupfirst doubles the first letter of a word.",
     "to dupfirst any word, say its first letter twice, then the whole word.",
     lambda s, e: f"to dupfirst {s}, say the first letter {s[0]} twice, then {s}: {e}."),
    (2, "rotleft",
     "rotleft moves the first letter of a word to the end.",
     "to rotleft any word, move its first letter to the end.",
     lambda s, e: f"to rotleft {s}, move the first letter {s[0]} to the end: {e}."),
    (3, "droplast",
     "droplast removes the last letter of a word.",
     "to droplast any word, drop its last letter.",
     lambda s, e: f"to droplast {s}, drop the last letter {s[-1]}: {e}."),
    (4, "upperfirst",
     "upperfirst capitalizes the first letter of a word.",
     "to upperfirst any word, capitalize its first letter.",
     lambda s, e: f"to upperfirst {s}, capitalize the first letter {s[0]}: {e}."),
    (5, "sortchars",
     "sortchars sorts the letters of a word alphabetically.",
     "to sortchars any word, sort its letters alphabetically.",
     lambda s, e: f"to sortchars {s}, sort the letters {' '.join(s)}: {e}."),
]

TRAIN_IDX = list(range(6)) + list(range(700, 706))

def teach_lines(r):
    _, name, defn, proc, walk = RULES[r]
    lines = [defn, proc]
    for t in TRAIN_IDX:
        s = tok(t)
        e = apply_rule(r, s)
        lines.append(f"the letters of {s} are {' '.join(s)}.")
        lines.append(walk(s, e))
        lines.append(f"the {name} of {s} is {e}.")
    return lines

def run_session(turns, timeout=300):
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
    p0c = open(os.path.join(rundir, "resp_p0c.txt"), "w")
    p3f = open(os.path.join(rundir, "resp_p3.txt"), "w")
    smpf = open(os.path.join(rundir, "resp_samples.txt"), "w")

    # distractor allocation across the 6 P0 sessions (A3 interleaving)
    distract = {0: [614, 615], 1: [616, 617], 2: [618],
                3: [619], 4: [620], 5: [621]}

    # ---- P0: one fresh session per rule ----
    for r, name, _, _, _ in RULES:
        turns = teach_lines(r)
        for t in turns:
            teach_log.write(f"P0R{r}\t{t}\n")
        # taught controls (receipt check): tok 0 and tok 1
        ctl_qs = [f"what is the {name} of {tok(t)}?" for t in (0, 1)]
        # held-out probes tok 6..13 with distractors interleaved:
        # [P0,P0,D?,P0,P0,D?,P0,P0,P0,P0] — distractors at probe positions 2,5
        probes = []
        ds = list(distract[r])
        di = 0
        for j, t in enumerate(range(6, 14)):
            if j in (2, 5) and di < len(ds):
                dt = ds[di]; di += 1
                probes.append(("P3", dt, f"what is {tok(dt)}?"))
            probes.append(("P0", t, f"what is the {name} of {tok(t)}?"))
        # (sessions with 1 distractor use position 2 only)
        sess = run_session(turns + ctl_qs + [q for _, _, q in probes])
        nq = len(turns)
        for k, t in enumerate((0, 1)):
            q, cr = sess[nq + k]
            p0c.write(f"P0C {r} {t}\n{cr}\n")
        for (kind, t, q), (sq, resp) in zip(probes, sess[nq + 2:]):
            assert q == sq, (q, sq)
            if kind == "P0":
                assert str(tok(t)) in q
                p0f.write(f"P0 {r} {t}\n{resp}\n")
            else:
                p3f.write(f"P3 {t}\n{resp}\n")

    # ---- Samples: all-rules rich teaching, then qualitative prompts ----
    turns = []
    for r in range(6):
        turns.extend(teach_lines(r))
    for t in turns:
        teach_log.write(f"SMP\t{t}\n")
    prompts = []
    p1pairs = [(0, 1), (2, 3), (4, 5), (1, 4), (3, 0), (5, 2)]
    for k, (a, b) in enumerate(p1pairs):
        pidx = a * 5 + (b if b < a else b - 1)
        s = tok(14 + pidx * 4)
        exp = compose([a, b], s)
        prompts.append((f"SMP P1 {k} pair {a},{b} tok {14+pidx*4}",
                        f"which two parts (numbered 1 to 6), in which order, turn {s} into {exp}?"))
    p2spec = [(0, 1), (1, 0), (2, 3), (3, 2), (4, 5),
              (5, 4), (0, 5), (5, 0), (1, 3), (3, 1)]
    for k, (a, b) in enumerate(p2spec):
        pidx = a * 5 + (b if b < a else b - 1)
        s = tok(14 + pidx * 4)
        prompts.append((f"SMP P2 {k} pair {a},{b} tok {14+pidx*4}",
                        f"apply part {a+1} then part {b+1} to {s}."))
    # triple index by lexicographic enumeration
    def triple_index(a, b, c):
        ti = 0
        for i in range(6):
            for j in range(6):
                if j == i: continue
                for kk in range(6):
                    if kk == i or kk == j: continue
                    if (i, j, kk) == (a, b, c): return ti
                    ti += 1
        raise ValueError
    for k2, (a, b, c) in enumerate([(0, 1, 2), (5, 4, 3)]):
        ti = triple_index(a, b, c)
        s = tok(134 + ti * 4)
        prompts.append((f"SMP P2 {10+k2} triple {a},{b},{c} tok {134+ti*4}",
                        f"apply part {a+1} then part {b+1} then part {c+1} to {s}."))
    sess = run_session(turns + [p for _, p in prompts], timeout=600)
    for (tag, _), (q, resp) in zip(prompts, sess[len(turns):]):
        smpf.write(f"{tag}\n{q}\n{resp}\n")

    for f in (teach_log, p0f, p0c, p3f, smpf):
        f.close()
    print(f"wrote {rundir}: P0 sessions=6 (rich teaching + interleaved P3), sample session=1")

if __name__ == "__main__":
    main()
