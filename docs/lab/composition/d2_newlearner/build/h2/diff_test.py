import subprocess, sys, os
SCN = sys.argv[1] if len(sys.argv)>1 else "/home/hatch/workspace/composition_d2_rerun/src/docs/lab/composition/d2/scenarios/F-0.txt"
D2BIN = "/home/hatch/workspace/composition_d2_rerun/d2build/d2bin"
# deterministic action sequence exercising move/eat/take/combine/drop/wait
acts = []
# wander left to 0, then right toward crystals, eat when possible (scripted)
seq = [0]*6 + [6]*3 + [1]*8 + [2] + [6]*5 + [1]*4 + [3] + [0]*3 + [3] + [5] + [4] + [6]*10 + [1]*6 + [2]*2 + [0]*10
acts = [str(a) for a in seq]
inp = "\n".join(acts) + "\n"
r1 = subprocess.run([D2BIN, "tui", SCN], input=inp, capture_output=True, text=True, timeout=60)
r2 = subprocess.run(["./fuzz", SCN, "session1.txt"], input=inp, capture_output=True, text=True, timeout=60)
o1 = [l for l in r1.stdout.splitlines() if l.startswith("OBS ")]
o2 = [l for l in r2.stdout.splitlines() if l.startswith("OBS ")]
print("d2bin OBS:", len(o1), " fuzz OBS:", len(o2))
if r2.stderr: print("fuzz stderr:", r2.stderr[:500])
n = min(len(o1), len(o2))
bad = 0
for i in range(n):
    if o1[i] != o2[i]:
        bad += 1
        if bad <= 5:
            print("MISMATCH tick", i)
            print("  sim:", o1[i][:160])
            print("  mdl:", o2[i][:160])
print("mismatches:", bad, "/", n)
