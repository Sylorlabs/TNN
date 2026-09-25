#!/usr/bin/env python3
"""HF-reduction variant (diagnostic, G4c bearing): 5 cases through the native
hfloop binary (render 440 Hz + fhf sine, natively measure own 8-16 kHz ratio,
attenuate, re-render). Reports per-iteration g and b3r curves. Deterministic."""
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
CREW = os.path.dirname(HERE)
HF = os.path.join(CREW, "build", "hf")
EV = os.path.join(CREW, "evidence")
HD = os.path.join(EV, "hf")

CASES = [
    ("H1", 9000, 500),
    ("H2", 12000, 500),
    ("H3", 15000, 500),
    ("H4", 12000, 1000),
    ("H5", 10000, 250),
]

def main():
    os.makedirs(HD, exist_ok=True)
    out = {}
    for cid, fhf, g0 in CASES:
        cd = os.path.join(HD, cid)
        os.makedirs(cd, exist_ok=True)
        p = subprocess.run([HF, cid, str(fhf), str(g0), cd],
                           capture_output=True, text=True, timeout=900)
        open(os.path.join(cd, "hfloop.log"), "w").write(p.stdout)
        if p.returncode != 0:
            print("FAIL", cid, p.stderr[-300:]); sys.exit(1)
        iters = []
        for line in p.stdout.splitlines():
            t = line.split()
            if t and t[0].startswith("hiter="):
                d = dict(x.split("=") for x in t)
                iters.append({"k": int(d["hiter"]), "g_milli": int(d["g_milli"]),
                              "b3r": int(d["b3r"])})
        out[cid] = {"fhf": fhf, "g0_milli": g0, "iters": iters}
        print(cid, "fhf=%d" % fhf,
              " ".join("g=%d b3r=%d" % (i["g_milli"], i["b3r"]) for i in iters))
    json.dump(out, open(os.path.join(EV, "hf.json"), "w"), indent=2)

if __name__ == "__main__":
    main()
