import subprocess, json, base64, sys, os
BASE="docs/lab/senses/web-search/internet-trial/phase3/repairs_v4/crews"
BR="tnn-native-lab"
for rel in sys.argv[1:]:
    r=subprocess.run(["/home/hatch/workspace/skills/github/bin/gh-api","GET",f"/repos/sylorlabs/tnn/contents/{BASE}/{rel}?ref={BR}"],capture_output=True,text=True)
    if r.returncode!=0:
        print("ERR",rel,r.stderr[:200]); continue
    d=json.loads(r.stdout)
    if d.get("type")!="file": print("NOTFILE",rel,d.get("type")); continue
    if d.get("encoding")!="base64": print("NOTB64",rel); continue
    body=base64.b64decode(d["content"])
    p=os.path.join("target",rel)
    os.makedirs(os.path.dirname(p),exist_ok=True)
    open(p,"wb").write(body)
    print("saved",p,len(body))
