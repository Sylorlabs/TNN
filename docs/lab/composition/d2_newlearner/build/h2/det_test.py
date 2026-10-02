import subprocess, importlib.util, hashlib
spec = importlib.util.spec_from_file_location("teaching", "/home/hatch/workspace/composition_d2_rerun/harness/teaching.py")
t = importlib.util.module_from_spec(spec); spec.loader.exec_module(t)
def one_line(s): return s.replace("\n"," ").replace("\r"," ").strip()
D2BIN = "/home/hatch/workspace/composition_d2_rerun/d2build/d2bin"
SCN = "/home/hatch/workspace/composition_d2_rerun/src/docs/lab/composition/d2/scenarios/F-0.txt"
def run_once(env_extra=None):
    import os
    env = dict(os.environ); env.update(env_extra or {})
    d2 = subprocess.Popen([D2BIN, "tui", SCN], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True, bufsize=1, env=env)
    h2 = subprocess.Popen(["./h2", "chat"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True, bufsize=1, env=env)
    h2.stdout.readline()
    for s in [t.SESSION_1, t.SESSION_2, t.SESSION_3, t.SESSION_4, t.SESSION_5]:
        h2.stdin.write(one_line(s)+"\n"); h2.stdin.flush(); h2.stdout.readline()
    actions = []
    while True:
        line = d2.stdout.readline()
        if line.startswith("OBS "): first_obs = line; break
        if line.startswith("CARD "):
            h2.stdin.write(line.strip()+"\n"); h2.stdin.flush(); h2.stdout.readline()
    obs = first_obs
    import re
    while True:
        h2.stdin.write(obs.strip()+"\n"); h2.stdin.flush()
        reply = h2.stdout.readline().strip()
        m = re.search(r"A ([0-6])", reply)
        a = m.group(1) if m else "6"
        actions.append(a)
        d2.stdin.write(a+"\n"); d2.stdin.flush()
        line = d2.stdout.readline()
        if line.startswith("RESULT"): break
        if line.startswith("OBS "): obs = line
        else: break
    d2.stdin.close(); h2.stdin.close()
    return "".join(actions)
a1 = run_once()
a2 = run_once()
a3 = run_once(env_extra={"MALLOC_PERTURB_": "165"})
print("run1 len:", len(a1), "sha:", hashlib.sha256(a1.encode()).hexdigest()[:16])
print("run2 identical:", a1==a2)
print("perturb identical:", a1==a3)
print("run1 head:", a1[:80])
