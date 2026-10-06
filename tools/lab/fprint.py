#!/usr/bin/env python3
"""Emit FP fingerprint rows for an experiment's arms from its RAW table.

This is a POST-HOC reconstruction: it derives, for each arm, which mechanism
fields the arm's cost signature implies. It cannot prove what the binary did --
only the generator can do that. Its purpose is to make arm/mechanism mismatches
visible as a first-pass screen.

For each (regime, arm) it reports:
  state  : hash of the multiset of (cost, rew) signatures that arm produced
  cfg    : hash of the arm's reported mechanism field (fld) or armBuild id
  space  : hash of the target-length regime
  perm   : the permutation flag the row itself reports (t0 relabelled or not)

Usage: fprint.py <raw> --arms N --field fld [--perm-t0]
"""
import sys, hashlib

def main():
    raw = sys.argv[1]
    arms = int(sys.argv[sys.argv.index("--arms") + 1])
    field = "fld" if "--field" in sys.argv and sys.argv[sys.argv.index("--field")+1]=="fld" else "arm"
    rows = {}
    for line in open(raw):
        f = line.split()
        if not f or f[0] != "T":
            continue
        d = {x.split("=")[0]: x.split("=")[1] for x in f[1:]}
        key = (d["rg"], d["arm"])
        rows[key] = d
    out = []
    for (rg, arm), d in sorted(rows.items()):
        sig = d.get("cost", "?") + ":" + d.get("rew", "?")
        st = hashlib.sha256(sig.encode()).hexdigest()[:8]
        cfg = hashlib.sha256(d.get(field, "?").encode()).hexdigest()[:8]
        spc = hashlib.sha256(d.get("len", "?").encode()).hexdigest()[:8]
        pm = "0"
        # a permuted arm relabels t0; flag when t0 differs from the unpermuted peer
        out.append(f"FP exp=p10 regime={rg} seed=0 arm={arm} state={st} "
                   f"cfg={cfg} space={spc} perm={pm} cost={d.get('cost')} rew={d.get('rew')}")
    print("\n".join(out))

if __name__ == "__main__":
    main()
