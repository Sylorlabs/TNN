import subprocess, importlib.util, sys
spec = importlib.util.spec_from_file_location("teaching", "/home/hatch/workspace/composition_d2_rerun/harness/teaching.py")
t = importlib.util.module_from_spec(spec); spec.loader.exec_module(t)
def one_line(s): return s.replace("\n"," ").replace("\r"," ").strip()
SCN = sys.argv[1] if len(sys.argv)>1 else "/home/hatch/workspace/composition_d2_rerun/src/docs/lab/composition/d2/scenarios/F-0.txt"
D2BIN = "/home/hatch/workspace/composition_d2_rerun/d2build/d2bin"
# get cards + true OBS trace by running d2bin with a dummy policy? No — we need interactive.
# Instead: start d2bin tui, feed it actions from h2, read OBS.
d2 = subprocess.Popen([D2BIN, "tui", SCN], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True, bufsize=1)
h2 = subprocess.Popen(["./h2", "chat"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True, bufsize=1)
h2.stdout.readline()  # banner
for s in [t.SESSION_1, t.SESSION_2, t.SESSION_3, t.SESSION_4, t.SESSION_5]:
    h2.stdin.write(one_line(s)+"\n"); h2.stdin.flush(); h2.stdout.readline()
# read cards from d2, forward to h2
cards = []
while True:
    line = d2.stdout.readline()
    if line.startswith("OBS "): first_obs = line; break
    if line.startswith("CARD "):
        cards.append(line.strip())
        h2.stdin.write(line.strip()+"\n"); h2.stdin.flush(); h2.stdout.readline()
# episode loop
obs = first_obs
ticks = 0; last_e = 100; n_eat = 0
import re
while True:
    h2.stdin.write(obs.strip()+"\n"); h2.stdin.flush()
    reply = h2.stdout.readline().strip()
    m = re.search(r"A ([0-6])", reply)
    if not m:
        print("BAD REPLY:", reply[:80]); break
    a = m.group(1)
    d2.stdin.write(a+"\n"); d2.stdin.flush()
    # count eats
    line = d2.stdout.readline()
    if not line or line.startswith("RESULT"):
        # read RESULT
        while line and not line.startswith("RESULT"): line = d2.stdout.readline()
        print("RESULT:", line.strip()[:200] if line else "none")
        break
    if line.startswith("OBS "):
        obs = line; ticks += 1
        me = re.search(r"E=(\d+)", line)
        if me: last_e = int(me.group(1))
    else:
        print("UNEXPECTED:", line[:80]); break
    if ticks > 500: print("TOO LONG"); break
print(f"ticks={ticks} final_E={last_e}")
d2.stdin.close(); h2.stdin.close()
