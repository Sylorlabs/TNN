import subprocess, glob, os
D2BIN = "/home/hatch/workspace/composition_d2_rerun/d2build/d2bin"
SCNDIR = "/home/hatch/workspace/composition_d2_rerun/src/docs/lab/composition/d2/scenarios"
def get_ep(scn):
    for l in open(scn):
        if l.startswith("# EPISODE"): return int(l.split()[2])
    return 120
def run_both(scn, acts):
    inp = "\n".join(str(a) for a in acts) + "\n"
    r1 = subprocess.run([D2BIN, "tui", scn], input=inp, capture_output=True, text=True, timeout=180)
    r2 = subprocess.run(["./fuzz", scn, "session1.txt"], input=inp, capture_output=True, text=True, timeout=180)
    o1 = [l for l in r1.stdout.splitlines() if l.startswith("OBS ")]
    o2 = [l for l in r2.stdout.splitlines() if l.startswith("OBS ")]
    return o1, o2
def script_wander(n): return [(i*7+3)%7 for i in range(n)]
def script_greedy_right(n): return [1]*n
def script_greedy_left(n): return [0]*n
def script_take_build(n):
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
# also: storm-riding (stay in zone during storm), starvation (wait until death)
def script_storm_stay(n): return [6]*n
def script_void_dance(n):
    # walk right into void region edge repeatedly
    s=[]
    for i in range(n):
        s.append(1 if (i//10)%2==0 else 0)
    return s
total_bad=0; total_n=0; mismatched_files=[]
for scn in sorted(glob.glob(SCNDIR+"/*.txt")):
    name=os.path.basename(scn); ep=get_ep(scn)
    scripts=[("wander",script_wander(ep)),("right",script_greedy_right(ep)),
             ("left",script_greedy_left(ep)),("build",script_take_build(ep)),
             ("stormstay",script_storm_stay(ep)),("voiddance",script_void_dance(ep))]
    for sname, acts in scripts:
        o1,o2=run_both(scn,acts)
        n=min(len(o1),len(o2))
        bad=sum(1 for i in range(n) if o1[i]!=o2[i])
        total_bad+=bad; total_n+=n
        if bad>0 or len(o1)!=len(o2):
            mismatched_files.append((name,sname,bad,n,len(o1),len(o2)))
            for i in range(n):
                if o1[i]!=o2[i]:
                    print(f"{name}/{sname} tick {i}:\n  sim:{o1[i][:140]}\n  mdl:{o2[i][:140]}"); break
print(f"DONE scripts={len(glob.glob(SCNDIR+'/*.txt'))*6} ticks={total_n} mismatches={total_bad} bad_files={len(mismatched_files)}")
for m in mismatched_files[:10]: print("  LEN-DIFF:", m)
