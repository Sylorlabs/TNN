#!/usr/bin/env python3
"""Run the Crew L closed-loop battery. For each of 3 runs and each of the 20
frozen intent cases: invoke the native loop binary (argv = case_id, pitch:<hz>,
env:<class>, outdir — intent only, no measurements), capture stdout, record
argv bytes (prereg 5.2 audit), hash per-iteration WAVs. Deterministic."""
import json, os, subprocess, hashlib, sys

HERE = os.path.dirname(os.path.abspath(__file__))
CREW = os.path.dirname(HERE)
MAN = json.load(open(os.path.join(CREW, "manifests", "intent_manifest.json")))
LOOP = os.path.join(CREW, "build", "loop")
EV = os.path.join(CREW, "evidence")

def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()

def main():
    runs = [int(a) for a in sys.argv[1:]] or [1, 2, 3]
    argv_log = open(os.path.join(EV, "argv_log.jsonl"), "a")
    for r in runs:
        rd = os.path.join(EV, "run%d" % r)
        sha_table = {}
        for c in MAN:
            cid = c["case_id"]
            cd = os.path.join(rd, cid)
            os.makedirs(cd, exist_ok=True)
            argv = [LOOP, cid, "pitch:%d" % c["target_hz"],
                    "env:%s" % c["target_env"], cd]
            argv_log.write(json.dumps({"run": r, "argv": argv}) + "\n")
            argv_log.flush()
            p = subprocess.run(argv, capture_output=True, text=True, timeout=600)
            open(os.path.join(cd, "loop.log"), "w").write(p.stdout)
            open(os.path.join(cd, "loop.rc"), "w").write(str(p.returncode))
            if p.returncode != 0:
                print("FAIL", cid, "rc=", p.returncode, p.stderr[-500:])
                sys.exit(1)
            shas = {}
            for k in range(4):
                fp = os.path.join(cd, "%s_iter%d.wav" % (cid, k))
                shas["iter%d" % k] = sha(fp)
            sha_table[cid] = shas
        json.dump(sha_table, open(os.path.join(rd, "sha_table.json"), "w"), indent=2)
        print("run%d done: %d cases" % (r, len(MAN)))
    argv_log.close()

if __name__ == "__main__":
    main()
