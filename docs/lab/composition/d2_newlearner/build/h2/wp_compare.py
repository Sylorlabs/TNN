import subprocess, glob, os, re, importlib.util, sys, hashlib, json
spec = importlib.util.spec_from_file_location("teaching", "/home/hatch/workspace/composition_d2_rerun/harness/teaching.py")
t = importlib.util.module_from_spec(spec); spec.loader.exec_module(t)
def one_line(s): return s.replace("\n"," ").replace("\r"," ").strip()
D2BIN = "/home/hatch/workspace/composition_d2_rerun/d2build/d2bin"
SCNDIR = "/home/hatch/workspace/composition_d2_rerun/src/docs/lab/composition/d2/scenarios"
wrong = open("session1_wrong.txt").read().replace("\n"," ").strip()
def run_episode(scn, use_wrong):
    d2 = subprocess.Popen([D2BIN, "tui", scn], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True, bufsize=1)
    h2 = subprocess.Popen(["./h2", "chat"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True, bufsize=1)
    h2.stdout.readline()
    s1 = wrong if use_wrong else one_line(t.SESSION_1)
    h2.stdin.write(s1+"\n"); h2.stdin.flush(); h2.stdout.readline()
    for s in [t.SESSION_2, t.SESSION_3, t.SESSION_4, t.SESSION_5]:
        h2.stdin.write(one_line(s)+"\n"); h2.stdin.flush(); h2.stdout.readline()
    while True:
        line = d2.stdout.readline()
        if line.startswith("OBS "): first_obs = line; break
        if line.startswith("CARD "):
            h2.stdin.write(line.strip()+"\n"); h2.stdin.flush(); h2.stdout.readline()
    obs = first_obs; actions = []; result = None
    while True:
        h2.stdin.write(obs.strip()+"\n"); h2.stdin.flush()
        reply = h2.stdout.readline().strip()
        m = re.search(r"A ([0-6])", reply)
        a = m.group(1) if m else "X"
        actions.append(a)
        d2.stdin.write(a+"\n"); d2.stdin.flush()
        line = d2.stdout.readline()
        if line.startswith("RESULT"): result = line.strip(); break
        if line.startswith("OBS "): obs = line
        else: result = "UNEXP"; break
    d2.stdin.close(); h2.stdin.close(); d2.wait(timeout=10); h2.wait(timeout=10)
    return "".join(actions), result
def parse_result(r):
    m = re.match(r"RESULT learner (\d+) (\d+) (\d+) (\d+) (\d+) (\d+) (-?\d+) (\d+) (\d+)", r)
    return list(map(int, m.groups())) if m else None
scns = sorted(glob.glob(os.path.join(SCNDIR, "F-*.txt")))[:6]  # 6 scenarios for speed
out = {}
for uw, tag in [(False, "correct"), (True, "wrong")]:
    traces = {}; passes = 0
    for scn in scns:
        name = os.path.basename(scn)
        acts, res = run_episode(scn, uw)
        traces[name] = acts
        pr = parse_result(res)
        ok = pr and pr[1]==0 and pr[0]==120 and pr[3]>=4 and pr[5]==0
        if ok: passes += 1
        print(tag, name, "pass" if ok else "FAIL", "nEat=", pr[3] if pr else "?", "E=", pr[2] if pr else "?")
    out[tag] = {"traces": traces, "pass": passes, "n": len(scns)}
json.dump(out, open("wp_compare.json","w"))
# compare
ct, wt = out["correct"]["traces"], out["wrong"]["traces"]
for name in ct:
    a, b = ct[name], wt[name]
    n = min(len(a), len(b))
    same = sum(1 for i in range(n) if a[i]==b[i])
    print(f"{name}: identical={same}/{n} ({100*same//n}%) len {len(a)} vs {len(b)}")
print(f"pass correct={out['correct']['pass']}/{out['correct']['n']} wrong={out['wrong']['pass']}/{out['wrong']['n']}")
