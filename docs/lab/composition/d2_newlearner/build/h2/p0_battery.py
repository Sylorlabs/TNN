import subprocess, glob, os, re, importlib.util, sys
spec = importlib.util.spec_from_file_location("teaching", "/home/hatch/workspace/composition_d2_rerun/harness/teaching.py")
t = importlib.util.module_from_spec(spec); spec.loader.exec_module(t)
def one_line(s): return s.replace("\n"," ").replace("\r"," ").strip()
D2BIN = "/home/hatch/workspace/composition_d2_rerun/d2build/d2bin"
SCNDIR = "/home/hatch/workspace/composition_d2_rerun/src/docs/lab/composition/d2/scenarios"
H2BIN = "./h2"
def run_episode(scn):
    d2 = subprocess.Popen([D2BIN, "tui", scn], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True, bufsize=1)
    h2 = subprocess.Popen([H2BIN, "chat"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True, bufsize=1)
    h2.stdout.readline()
    for s in [t.SESSION_1, t.SESSION_2, t.SESSION_3, t.SESSION_4, t.SESSION_5]:
        h2.stdin.write(one_line(s)+"\n"); h2.stdin.flush(); h2.stdout.readline()
    while True:
        line = d2.stdout.readline()
        if line.startswith("OBS "): first_obs = line; break
        if line.startswith("CARD "):
            h2.stdin.write(line.strip()+"\n"); h2.stdin.flush(); h2.stdout.readline()
    obs = first_obs; result = None
    while True:
        h2.stdin.write(obs.strip()+"\n"); h2.stdin.flush()
        reply = h2.stdout.readline().strip()
        m = re.search(r"A ([0-6])", reply)
        if not m: result = "BAD_REPLY:"+reply[:40]; break
        d2.stdin.write(m.group(1)+"\n"); d2.stdin.flush()
        line = d2.stdout.readline()
        if line.startswith("RESULT"):
            result = line.strip(); break
        if line.startswith("OBS "): obs = line
        else: result = "UNEXPECTED:"+line[:40]; break
    d2.stdin.close(); h2.stdin.close()
    d2.wait(timeout=10); h2.wait(timeout=10)
    return result
def check(scn, result):
    # RESULT learner ticks cause E nEat nCombine wastedEat wardTick stormExp invalid
    m = re.match(r"RESULT learner (\d+) (\d+) (\d+) (\d+) (\d+) (\d+) (-?\d+) (\d+) (\d+)", result)
    if not m: return False, ["parse_fail"]
    ticks,cause,E,nEat,nComb,wasted,wardTick,stormExp,invalid = map(int, m.groups())
    name = os.path.basename(scn)
    ep = 120 if name.startswith("F-") else 90
    reasons = []
    if invalid >= 3: reasons.append(f"invalid={invalid}")
    if not (cause==0 and ticks==ep): reasons.append(f"dead(cause={cause},ticks={ticks}/{ep})")
    if cause==2: reasons.append("void")
    if name.startswith("F-"):
        if nEat<4: reasons.append(f"nEat={nEat}<4")
        if wasted!=0: reasons.append(f"wasted={wasted}")
    elif name.startswith("W-"):
        if not (wardTick>=0 and wardTick<60): reasons.append(f"wardTick={wardTick}")
    return len(reasons)==0, reasons
which = sys.argv[1] if len(sys.argv)>1 else "F"
scns = sorted(glob.glob(os.path.join(SCNDIR, which+"-*.txt")))
npass=0
for scn in scns:
    try:
        r = run_episode(scn)
        ok, reasons = check(scn, r)
        status = "PASS" if ok else "FAIL "+",".join(reasons)
        if ok: npass+=1
        else: print(os.path.basename(scn), status, r[:80])
    except Exception as ex:
        print(os.path.basename(scn), "ERROR", str(ex)[:80])
print(f"P0-{which}: {npass}/{len(scns)}")
