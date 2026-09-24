import subprocess, re, sys, os
out = {}
def grab(commit, paths, tag):
    for p in paths:
        try:
            t = subprocess.run(["git","show",f"{commit}:{p}"],capture_output=True,text=True,check=True,cwd="/home/hatch/workspace/selfpam_run/tnn-lab").stdout
        except Exception as e:
            out[f"{tag}:{p}"] = f"MISSING ({e})"; continue
        out[f"{tag}:{p}"] = t
grab("ec8d5d13", ["docs/lab/senses/pam-rebuild/round2/rt_jklm/VERDICT_RT_JKLM.md"], "rtjklm")
grab("9f8ff63b", ["docs/lab/senses/pam-rebuild/round2/b3536/sstar/VERDICT_RT_S.md"], "rts")
grab("36b1d5fc2", ["docs/lab/senses/pam-rebuild/round2/b3536/GROK_OBJECTOR_R2.md"], "grok")
os.makedirs("/home/hatch/workspace/b3034comp/extract", exist_ok=True)
with open("/home/hatch/workspace/b3034comp/extract/classes_raw.md","w") as f:
    for k,v in out.items():
        f.write(f"\n\n===== {k} ({len(v)} chars) =====\n\n"); f.write(v)
print("keys:", list(out.keys()), "lens:", {k:len(v) for k,v in out.items()})
