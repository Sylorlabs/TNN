#!/usr/bin/env python3
"""RSI-8 Round 2 §5 per-accept: re-run the accepted policy's proposer
verdict N×; require byte-identical PROPOSE."""
import subprocess, csv, os, sys, hashlib

BASE = os.path.expanduser("~/workspace/tnn-lab/rsi/autonomous_run_2")
PROPOSER = f"{BASE}/work/r5/proposer"

GT = ''.join('1' if r['gt']=='NEW' else ('2' if r['gt']=='OLD' else '0')
             for r in csv.DictReader(open(f"{BASE}/build/proxy_battery.csv")))

# The accepted policy from the loop
DELB = "\n".join([
    "DELB_START",
    "GAP class2 atom1 discriminates wrong vs clean [AF-2-1]",
    "POLICY",
    "POLICY d1pick",
    "RULE 1 IF pre_is(OLD) THEN recompute_only(001)",
    "END",
    "ENDPOLICY",
    "ARGUMENT",
    "The AF-DISC scan selected atom pre_is(OLD) as the top discriminator. Forcing consult via recompute_only(001) lets the channel correct the pre-verdict on wrong items. The novel battery F1 F4 F5 F6 families have field shapes that do not trigger this atom in a verdict-changing way. Engine vocabulary: pre_is(OLD) recompute_only(001).",
    "ENDARGUMENT",
    "PRED P-ACC 20 20 P-WRONG 4 4 P-COST 344 P-NOVEL 0",
    "TRACK improvement",
    "DELB_END",
])

def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    outputs = []
    for i in range(n):
        r = subprocess.run([PROPOSER, DELB] + [""]*8 + ["16", "8", "456", GT, "r5accept"],
                           capture_output=True, text=True)
        out = r.stdout
        h = hashlib.sha256(out.encode()).hexdigest()
        outputs.append((out, h))
    h0 = outputs[0][1]
    identical = all(h == h0 for _, h in outputs)
    verdict = outputs[0][0].strip().split("\n")[0]
    print(f"Runs: {n}, byte-identical: {identical}, verdict: {verdict}")
    sys.exit(0 if (identical and verdict == "PROPOSE") else 1)

if __name__ == "__main__":
    main()
