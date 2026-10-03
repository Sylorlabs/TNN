import subprocess, glob, os
D2BIN = "/home/hatch/workspace/composition_d2_rerun/d2build/d2bin"
SCNDIR = "/home/hatch/workspace/composition_d2_rerun/src/docs/lab/composition/d2/scenarios"
def run_both(scn, acts):
    inp = "\n".join(str(a) for a in acts) + "\n"
    r1 = subprocess.run([D2BIN, "tui", scn], input=inp, capture_output=True, text=True, timeout=120)
    r2 = subprocess.run(["./fuzz", scn, "session1.txt"], input=inp, capture_output=True, text=True, timeout=120)
    o1 = [l for l in r1.stdout.splitlines() if l.startswith("OBS ")]
    o2 = [l for l in r2.stdout.splitlines() if l.startswith("OBS ")]
    return o1, o2, r2.stderr
# action scripts: (name, generator)
def script_wander(n):
    # deterministic pseudo-walk: L,R,EAT,WAIT pattern
    return [(i*7+3)%7 for i in range(n)]
def script_greedy_right(n):
    return [1]*n
def script_greedy_left(n):
    return [0]*n
def script_take_build(n):
    # move right, take, move, take, combine, drop, eat sometimes
    s = []
    for i in range(n):
        m = i % 12
        if m < 4: s.append(1)
        elif m == 4: s.append(3)
        elif m < 8: s.append(0)
        elif m == 8: s.append(3)
        elif m == 9: s.append(5)
        elif m == 10: s.append(4)
        else: s.append(2)
    return s
total_bad = 0; total_n = 0; files = 0
for scn in sorted(glob.glob(SCNDIR+"/*.txt")):
    name = os.path.basename(scn)
    for sname, acts in [("wander", script_wander(150)), ("right", script_greedy_right(60)),
                        ("left", script_greedy_left(60)), ("build", script_take_build(120))]:
        o1, o2, err = run_both(scn, acts)
        n = min(len(o1), len(o2))
        bad = sum(1 for i in range(n) if o1[i] != o2[i])
        # also check death alignment: if sim died, model should die at same tick
        total_bad += bad; total_n += n; files += 1
        if bad > 0 or len(o1) != len(o2):
            print(f"{name}/{sname}: MISMATCH bad={bad}/{n} len {len(o1)} vs {len(o2)}")
            for i in range(n):
                if o1[i] != o2[i]:
                    print("  sim:", o1[i][:130]); print("  mdl:", o2[i][:130]); break
            if err: print("  stderr:", err[:200])
print(f"DONE files_scripts={files} ticks={total_n} mismatches={total_bad}")
