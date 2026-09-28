#!/usr/bin/env python3
"""run_mechanical.py: run work/checker 3x on every arm source, assert
byte-identical outputs, emit mechanical.json. Glue only; measurement is Zag."""
import json, subprocess, pathlib

BASE = pathlib.Path.home() / "workspace/tnn-lab/coding/reflection/cleanliness"
CHECKER = str(BASE / "work" / "checker")
specs = [s["id"] for s in json.loads((BASE / "SPECS.json").read_text())["items"]]
arms = ["human", "tnn", "sol", "grok"]

out = {"checker": "checker.zag (pure Zag)", "runs": 3, "items": {}}
for sid in specs:
    out["items"][sid] = {}
    for arm in arms:
        src = BASE / "sources" / sid / f"{arm}.zag"
        if not src.exists():
            out["items"][sid][arm] = None
            continue
        code = src.read_bytes()
        outs = []
        for _ in range(3):
            # pass source via argv (bytes); checker reads _zag_arg(1)
            r = subprocess.run([CHECKER, code], capture_output=True, timeout=30)
            assert r.returncode == 0, (sid, arm, r.stderr[:200])
            outs.append(r.stdout)
        assert outs[0] == outs[1] == outs[2], f"NONDETERMINISTIC {sid}/{arm}"
        lines = outs[0].decode().splitlines()
        m = {}
        for tok in lines[0].split():
            k, v = tok.split("=")
            m[k] = int(v)
        det = {}
        for tok in lines[1].split()[1:]:
            k, v = tok.split("=")
            det[k] = int(v)
        m["detail"] = det
        out["items"][sid][arm] = m

(BASE / "work" / "mechanical.json").write_text(json.dumps(out, indent=1))
print("wrote work/mechanical.json")
# summary means over available arms
for arm in arms:
    vals = [v for sid in specs for v in [out["items"][sid][arm]] if v]
    for dim in ("M1", "M2", "M3"):
        mean = sum(v[dim] for v in vals) / len(vals)
        print(f"{arm} {dim}: n={len(vals)} mean={mean:.3f}")
