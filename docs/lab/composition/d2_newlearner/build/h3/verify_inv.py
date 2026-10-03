import os, re, sys
sdir = os.path.expanduser("~/workspace/composition_d2_rerun/src/docs/lab/composition/d2/scenarios")
SALTS = {"train":101,"P0":103,"P2":107,"P3":109}
def phase_of(k):
    if 0<=k<=23: return "train"
    if 24<=k<=47: return "P0"
    if 48<=k<=71: return "P2"
    return "P3"
def parse(path):
    nums = [int(x) for x in re.findall(r"^-?\d+$", open(path).read(), re.M)]
    # 33 ints: void,start,s0,s1,s2,c0..c3, then 8 motes x3
    assert len(nums)==33, (path, len(nums))
    txt = open(path).read()
    m = re.search(r"# phase=(\w+) template=(\w+) k=(\d+)", txt)
    pre = re.search(r"# PREWARD (\S+)", txt).group(1)
    return {"void":nums[0],"start":nums[1],"storms":nums[2:5],"crys":nums[5:9],
            "motes":[tuple(nums[9+i*3:12+i*3]) for i in range(8)],
            "phase":m.group(1),"template":m.group(2),"k":int(m.group(3)),
            "pre":None if pre=="none" else int(pre),
            "ep":int(re.search(r"# EPISODE (\d+)",txt).group(1))}
bad = []
files = sorted(f for f in os.listdir(sdir) if f.endswith(".txt") and f!="NOVELTY.txt")
n=0
for f in files:
    p = os.path.join(sdir,f); s = parse(p); n+=1
    va, st, T = s["void"], s["start"], s["template"]
    tag = f"{f}"
    def chk(cond, msg):
        if not cond: bad.append(f"{tag}: {msg}")
    chk(st < va, f"start {st} not < void {va}")
    # filename-derived void
    mm = re.match(r"^(FW|WF|FWF|F|W|T|N)-(\d+)\.txt$", f)
    k = int(mm.group(2)); salt = SALTS[phase_of(k)]
    dva = 8 + ((5*k + salt) % 8)
    chk(dva == va, f"derived void {dva} != file {va} (k={k} salt={salt})")
    chk(mm.group(1)==T, "template mismatch")
    motes = s["motes"]; crys = s["crys"]
    if T in ("F","T","FW","WF","FWF"):
        for j in range(6):
            chk(motes[j][0] < va, f"near mote {j} at {motes[j][0]} not < void {va}")
        for j in (6,7):
            chk(motes[j][0] > va+1, f"deep mote {j} at {motes[j][0]} not > void+1")
    if T in ("W","N"):
        for j in range(8):
            chk(motes[j][0] > va+1, f"W/N mote {j} at {motes[j][0]} not beyond void")
    if T=="N":
        for c in crys: chk(c > va+1, f"N crystal {c} not beyond void")
    if T in ("FW","WF","FWF"):
        chk(st+1 in crys and st+2 in crys, f"missing start+1/start+2 crystals: {crys}")
        near2 = sorted(crys, key=lambda c:(abs(c-st),c))[:2]
        for c in near2: chk(c < va, f"near2 crystal {c} not < void {va}")
    if T=="W":
        ok = [c for c in crys if c <= 7]
        chk(len(ok)>=2, f"W crystals<=7 fewer than 2: {crys}")
        for c in ok: chk(c < va, f"W crystal {c}<=7 not < void")
    if T=="T":
        chk(s["pre"]==st, f"T preward {s['pre']} != start {st}")
    if T in ("F","N"):
        allfar = all(c > va+1 for c in crys)
        chk(allfar == (T=="N"), f"F/N crystal-side characterization fails: {crys} va={va}")
print(f"checked {n} scenarios, {len(bad)} violations")
for b in bad[:40]: print("VIOL", b)
