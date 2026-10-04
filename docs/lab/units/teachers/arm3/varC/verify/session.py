#!/usr/bin/env python3
"""Session simulator: drives the teacher proposal-by-proposal with a scripted
decision list, building a valid decision history. Usage:
  session.py <teacher_bin> <wired_dir> <slice_idx> <session_id> <hist_out>
             <decisions> [workdir]
decisions: comma-separated tokens ADOPT | REVISE | REJECT:<reason> | DEFER
Writes the final history to hist_out and the E-trace to hist_out.trace."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hist import *

def main():
    binary, wired, slice_idx, session_id, hist_out, decspec = sys.argv[1:7]
    workdir = sys.argv[7] if len(sys.argv) > 7 else os.path.dirname(os.path.abspath(hist_out))
    slice_idx = int(slice_idx)
    session_id = int(session_id)
    decisions = []
    for tok in decspec.split(","):
        tok = tok.strip()
        if tok == "ADOPT":
            decisions.append((ADOPT, 0))
        elif tok == "REVISE":
            decisions.append((REVISE, 0))
        elif tok == "DEFER":
            decisions.append((DEFER, 0))
        elif tok.startswith("REJECT:"):
            decisions.append((REJECT, int(tok.split(":")[1])))
        else:
            raise SystemExit(f"bad decision token: {tok}")
    t = Teacher(binary, wired)
    hist = new_history(session_id)
    os.makedirs(workdir, exist_ok=True)
    hpath = os.path.join(workdir, "_session_work.hist")
    trace_lines = []
    proposals = []
    i = 0
    while i < len(decisions):
        with open(hpath, "wb") as f:
            f.write(hist)
        rc, out, err = t.run("propose", slice_idx, session_id, hpath)
        for line in err.strip().split("\n"):
            if line.startswith("E="):
                trace_lines.append(f"proposal[{i}] {line}")
        if rc == 20:
            trace_lines.append(f"proposal[{i}] SESSION_CAP")
            break
        if rc != 0:
            raise SystemExit(f"teacher failed rc={rc}: {err}")
        p = parse_proposal(out)
        proposals.append(p)
        hist = append_propose(hist, p)
        v, r = decisions[i]
        hist = append_decide(hist, p["seq"], v, r)
        i += 1
    with open(hist_out, "wb") as f:
        f.write(hist)
    with open(hist_out + ".trace", "w") as f:
        f.write("\n".join(trace_lines) + "\n")
    # summary to stdout
    kinds = {}
    for p in proposals:
        kinds[p["kind"]] = kinds.get(p["kind"], 0) + 1
    confs = [p["conf"] for p in proposals]
    print(f"proposals={len(proposals)} kinds={kinds} "
          f"conf_min={min(confs) if confs else '-'} conf_max={max(confs) if confs else '-'}")
    # E series from trace
    es = [int(l.split("E=")[1].split()[0]) for l in trace_lines if l.startswith("proposal[") and "E=" in l]
    print("E_trace=" + ",".join(map(str, es)))

if __name__ == "__main__":
    main()
