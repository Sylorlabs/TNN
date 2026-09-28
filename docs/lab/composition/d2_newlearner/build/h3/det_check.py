import subprocess, re, sys, os
D2BIN = os.path.expanduser("~/workspace/composition_d2_rerun/d2build/d2bin")
def run_trace(scen, mode, env=None):
    e = dict(os.environ); 
    if env: e.update(env)
    h3 = subprocess.Popen(["./h3bin",mode], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                          text=True, bufsize=1, env=e)
    h3.stdout.readline()
    def ask(line):
        h3.stdin.write(line+"\n"); h3.stdin.flush()
        while True:
            r = h3.stdout.readline().strip()
            if r.startswith("A "): return r
    proc = subprocess.Popen([D2BIN,"tui",scen], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                            text=True, bufsize=1, env=e)
    obs=None; acts=[]
    while True:
        line=proc.stdout.readline().strip()
        if line.startswith("OBS "): obs=line; break
        ask(line)
    ask("Which sub-skills? Reply with numbers like 1,2,3.")
    res=None
    while obs:
        r=ask(obs); d=re.search(r"[0-6]",r); acts.append(d.group(0) if d else "X")
        proc.stdin.write((d.group(0) if d else "X")+"\n"); proc.stdin.flush()
        line=proc.stdout.readline().strip()
        if line.startswith("OBS "): obs=line
        elif line.startswith("RESULT "): res=line; break
        else: break
    proc.stdin.close(); proc.wait(); h3.stdin.close(); h3.wait()
    return "".join(acts), res
if __name__=="__main__":
    scen=sys.argv[1]; mode=sys.argv[2]; n=int(sys.argv[3]); env=None
    if len(sys.argv)>4: env={"MALLOC_PERTURB_":sys.argv[4]}
    outs=set()
    for i in range(n):
        a,r=run_trace(scen,mode,env); outs.add((a,r)); print(f"run{i}: actions={len(a)} res={r[:60]}")
    print("IDENTICAL" if len(outs)==1 else f"DIVERGED ({len(outs)} variants)")
