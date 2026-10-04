#!/usr/bin/env python3
"""Black-box attack runner for the F6 wedgefix red team (2026-09-26).

Usage: atk.py "<label>" <MODE> <op> <op> ...
Runs the sequence TWICE, verifies byte-identical output, and appends
label + exact command line + full output + determinism verdict to ATTACK_LOG.md.
"""
import subprocess, sys, os

BIN = os.path.expanduser("~/workspace/strength-f6-wedgefix/f6_wedgefix_rt_bin")
LOG = os.path.expanduser("~/workspace/strength-f6-wedgefix/redteam/ATTACK_LOG.md")

def run(args):
    p = subprocess.run([BIN] + args, capture_output=True, text=True, timeout=60)
    return p.stdout + ("[stderr] " + p.stderr if p.stderr else "")

def main():
    label = sys.argv[1]
    args = sys.argv[2:]
    o1 = run(args)
    o2 = run(args)
    same = (o1 == o2)
    cmd = " ".join([BIN] + args)
    entry = []
    entry.append(f"\n## {label}")
    entry.append(f"cmd: `{cmd}`")
    entry.append(f"determinism: {'IDENTICAL' if same else '*** MISMATCH ***'}")
    entry.append("run 1 output:")
    entry.append("```")
    entry.append(o1.rstrip())
    entry.append("```")
    if not same:
        entry.append("run 2 output (DIFFERS):")
        entry.append("```")
        entry.append(o2.rstrip())
        entry.append("```")
    entry.append("")
    with open(LOG, "a") as f:
        f.write("\n".join(entry))
    # concise console summary
    last1 = [l for l in o1.splitlines() if l.startswith("RT_END")]
    rcs = [l.split() for l in o1.splitlines() if l.startswith("RT ")]
    kills = [l for l in rcs if l[2] in ("KILL", "OW90", "OW30", "OW0") or l[2].startswith("OW")]
    print(f"[{label}] determinism={'OK' if same else 'MISMATCH'} "
          f"RT_END={last1[-1] if last1 else '?'} "
          f"KILL/OW_rcs={[l[3] for l in kills]}")

if __name__ == "__main__":
    main()
