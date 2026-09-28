#!/usr/bin/env python3
"""D1 composition REDO driver (2026-09-27, Job 1) — real repaired learner.

Runs under A8 (mastery-gated protocol) + A1-A7. The learner is wb3_stringrule
(Workbuddy round-2 source + native string-program engine).

Phase 0 (gates everything): P0 mastery — 6 fresh sessions (one per rule),
  rich fair teaching (definition + procedure + 12 examples, tok 0..5 and
  700..705, train salt C=13), 2 taught controls (tok 0,1), 8 held-out probes
  (tok 6..13, P0 salt C=17), P3 distractors interleaved per A3.
  Bar: >=7/8 per rule, ALL six rules. P5 scored case-sensitively.
Phase 1 (only if Phase 0 passes): P1 — 1 fresh session, all-rules teaching +
  part mapping, 150 prompts (30 pairs + 120 triples).
Phase 2 (only if Phase 0 passes): P2 — 2 fresh sessions (300 prompts each),
  all-rules teaching + part mapping, 600 prompts (120 pairs + 480 triples).

Deterministic: fixed protocol, zero RNG. Run twice + allocator perturbation;
transcripts must be byte-identical.

Usage: drive_redo.py <rundir> <binary>
Writes <rundir>/: teach_log.txt, resp_p0.txt, resp_p0c.txt, resp_p3.txt,
  resp_p1.txt, resp_p2a.txt, resp_p2b.txt, SCORES.txt
"""
import subprocess, sys, os, re

WORK = os.path.dirname(os.path.abspath(__file__))

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
NAMES = [n for _, n, _, _, _ in RULES]
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

def part_lines():
    return [f"{name} is part {r+1}." for r, name in enumerate(NAMES)]

# pair/triple enumeration (matches battery_amended.zag)
def pair_pi(p): return p // 5
def pair_pj(p):
    pi = p // 5; q = p % 5
    return q + 1 if q >= pi else q
def triple_pijk(t):
    i = t // 20; r1 = t % 20
    ji = r1 // 4
    j = ji + 1 if ji >= i else ji
    r2 = r1 % 4
    ki = r2
    # k = ki-th of remaining excluding i,j
    rem = [x for x in range(6) if x != i and x != j]
    return (i, j, rem[ki])

def run_session(turns, binary, timeout=900, env=None):
    proc = subprocess.Popen([binary, "chat"], cwd=WORK,
                            stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                            text=True, bufsize=1, env=env)
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

def last_word(resp):
    # case-SENSITIVE last-word extraction (A8 fixes the P5 scorer defect)
    w = resp.strip().rstrip(".")
    return w.split()[-1] if w.split() else ""

def main():
    rundir, binary = sys.argv[1], sys.argv[2]
    os.makedirs(rundir, exist_ok=True)
    teach_log = open(os.path.join(rundir, "teach_log.txt"), "w")
    p0f = open(os.path.join(rundir, "resp_p0.txt"), "w")
    p0c = open(os.path.join(rundir, "resp_p0c.txt"), "w")
    p3f = open(os.path.join(rundir, "resp_p3.txt"), "w")

    distract = {0: [614, 615], 1: [616, 617], 2: [618],
                3: [619], 4: [620], 5: [621]}

    # ---- Phase 0: P0 mastery ----
    p0_scores = {}
    for r, name, _, _, _ in RULES:
        turns = teach_lines(r)
        for t in turns:
            teach_log.write(f"P0R{r}\t{t}\n")
        ctl_qs = [f"what is the {name} of {tok(t)}?" for t in (0, 1)]
        probes = []
        ds = list(distract[r]); di = 0
        for j, t in enumerate(range(6, 14)):
            if j in (2, 5) and di < len(ds):
                dt = ds[di]; di += 1
                probes.append(("P3", dt, f"what is {tok(dt)}?"))
            probes.append(("P0", t, f"what is the {name} of {tok(t)}?"))
        sess = run_session(turns + ctl_qs + [q for _, _, q in probes], binary)
        nq = len(turns)
        okc = 0
        for k, t in enumerate((0, 1)):
            q, cr = sess[nq + k]
            exp = apply_rule(r, tok(t))
            good = 1 if last_word(cr) == exp else 0
            okc += good
            p0c.write(f"P0C {r} {t} exp={exp} got={last_word(cr)} pass={good}\n{cr}\n")
        ok = 0
        for (kind, t, q), (sq, resp) in zip(probes, sess[nq + 2:]):
            assert q == sq, (q, sq)
            if kind == "P0":
                exp = apply_rule(r, tok(t))
                good = 1 if last_word(resp) == exp else 0
                ok += good
                p0f.write(f"P0 {r} {t} exp={exp} got={last_word(resp)} pass={good}\n{resp}\n")
            else:
                p3f.write(f"P3 {t}\n{resp}\n")
        p0_scores[r] = (ok, okc)
        print(f"P0 rule {r} ({name}): {ok}/8 held-out, {okc}/2 controls", flush=True)

    for f in (teach_log, p0f, p0c, p3f):
        f.close()

    # ---- Mastery gate ----
    failed = [r for r in range(6) if p0_scores[r][0] < 7]
    with open(os.path.join(rundir, "SCORES.txt"), "w") as sf:
        sf.write("P0 mastery (bar >=7/8 per rule, all six):\n")
        for r, name in enumerate(NAMES):
            ok, okc = p0_scores[r]
            sf.write(f"  rule {r} {name}: {ok}/8 held-out, {okc}/2 controls "
                     f"{'PASS' if ok >= 7 else 'FAIL'}\n")
        if failed:
            sf.write(f"MASTERY FAILED for rules {failed}: K2 VOID — "
                     f"no P1/P2 run.\n")
    if failed:
        print(f"MASTERY FAILED for rules {failed}: K2 VOID, stopping.",
              flush=True)
        return

    print("MASTERY PASSED 6/6 — running P1/P2.", flush=True)
    # ---- Phase 1: P1 ----
    p1f = open(os.path.join(rundir, "resp_p1.txt"), "w")
    teach_all = []
    for r in range(6):
        teach_all.extend(teach_lines(r))
    teach_all.extend(part_lines())
    for t in teach_all:
        teach_log2 = open(os.path.join(rundir, "teach_log.txt"), "a")
        teach_log2.write(f"ALL\t{t}\n")
        teach_log2.close()
    p1prompts = []
    for p in range(30):
        a, b = pair_pi(p), pair_pj(p)
        s = tok(14 + p * 4)
        exp = compose([a, b], s)
        p1prompts.append((f"P1 pair {a},{b} tok {14+p*4}",
                          [a + 1, b + 1],
                          f"which two parts (numbered 1 to 6), in which order, "
                          f"turn {s} into {exp}?"))
    for t3 in range(120):
        a, b, c = triple_pijk(t3)
        s = tok(134 + t3 * 4)
        exp = compose([a, b, c], s)
        p1prompts.append((f"P1 triple {a},{b},{c} tok {134+t3*4}",
                          [a + 1, b + 1, c + 1],
                          f"which three parts (numbered 1 to 6), in which order, "
                          f"turn {s} into {exp}?"))
    sess = run_session(teach_all + [q for _, _, q in p1prompts], binary)
    import itertools
    def valid_seqs(s, exp, nparts):
        out = []
        for seq in itertools.permutations(range(6), nparts):
            if compose(seq, s) == exp:
                out.append([x + 1 for x in seq])
        return out
    p1ok = 0
    p1strict = 0
    p1ambig = 0
    for (tag, want, q), (sq, resp) in zip(p1prompts, sess[len(teach_all):]):
        assert q == sq, (q, sq)
        nums = [int(x) for x in re.findall(r"\d+", resp)]
        # recover (s, exp) from the prompt: "turn {s} into {exp}?"
        m = re.search(r"turn (\S+) into (\S+)\?", q)
        s_tok, exp_tok = m.group(1), m.group(2)
        vs = valid_seqs(s_tok, exp_tok, len(want))
        if len(vs) > 1:
            p1ambig += 1
        good_valid = 1 if nums in vs else 0
        good_strict = 1 if nums == want else 0
        p1ok += good_valid
        p1strict += good_strict
        p1f.write(f"{tag} want={want} valid={vs} gotnums={nums} "
                  f"pass_valid={good_valid} pass_strict={good_strict}\n"
                  f"{q}\n{resp}\n")
    p1f.close()
    print(f"P1: {p1ok}/150 valid-set, {p1strict}/150 strict, "
          f"{p1ambig}/150 ambiguous items", flush=True)

    # ---- Phase 2: P2 ----
    p2spec = []
    for p in range(30):
        a, b = pair_pi(p), pair_pj(p)
        for it in range(4):
            ti = 14 + p * 4 + it
            s = tok(ti)
            exp = compose([a, b], s)
            p2spec.append((f"P2 pair {a},{b} tok {ti}", exp,
                           f"apply part {a+1} then part {b+1} to {s}."))
    for t3 in range(120):
        a, b, c = triple_pijk(t3)
        for it in range(4):
            ti = 134 + t3 * 4 + it
            s = tok(ti)
            exp = compose([a, b, c], s)
            p2spec.append((f"P2 triple {a},{b},{c} tok {ti}", exp,
                           f"apply part {a+1} then part {b+1} then part "
                           f"{c+1} to {s}."))
    assert len(p2spec) == 600
    p2ok = 0
    for half, hname in ((p2spec[:300], "resp_p2a.txt"),
                        (p2spec[300:], "resp_p2b.txt")):
        hf = open(os.path.join(rundir, hname), "w")
        sess = run_session(teach_all + [q for _, _, q in half], binary)
        for (tag, exp, q), (sq, resp) in zip(half, sess[len(teach_all):]):
            assert q == sq, (q, sq)
            good = 1 if last_word(resp) == exp else 0
            p2ok += good
            hf.write(f"{tag} exp={exp} got={last_word(resp)} pass={good}\n"
                     f"{q}\n{resp}\n")
        hf.close()
    print(f"P2: {p2ok}/600", flush=True)

    with open(os.path.join(rundir, "SCORES.txt"), "a") as sf:
        sf.write(f"P1: {p1ok}/150 valid-set ({p1strict}/150 strict; "
                 f"{p1ambig}/150 ambiguous items)\nP2: {p2ok}/600 raw\n")
    print(f"wrote {rundir}", flush=True)

if __name__ == "__main__":
    main()
