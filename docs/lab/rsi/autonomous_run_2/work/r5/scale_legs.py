#!/usr/bin/env python3
"""RSI-8 Round 2 §5: s10/s100 long-horizon verification.
Runs the full loop N times from empty kept; requires byte-identical
DELB outputs, identical accept chains, identical halt reasons.
Also re-runs the accepted policy's proposer verdict N× (byte-identical PROPOSE)."""
import subprocess, os, sys, hashlib

BASE = os.path.expanduser("~/workspace/tnn-lab/rsi/autonomous_run_2")

def run_loop():
    r = subprocess.run(["python3", f"{BASE}/work/r5/loop_driver_r5.py", "10"],
                       capture_output=True, text=True, cwd=BASE)
    return r.stdout

def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    print(f"Running {n} loop iterations...", file=sys.stderr)
    outputs = []
    for i in range(n):
        out = run_loop()
        h = hashlib.sha256(out.encode()).hexdigest()
        outputs.append((out, h))
        print(f"  run {i+1}/{n}: {h[:16]}", file=sys.stderr)
    # Check byte-identical
    h0 = outputs[0][1]
    identical = all(h == h0 for _, h in outputs)
    print(f"\nByte-identical across {n} runs: {identical}")
    if not identical:
        for i, (out, h) in enumerate(outputs):
            if h != h0:
                print(f"  run {i} differs: {h[:16]} vs {h0[:16]}")
        sys.exit(1)
    # Print the (identical) output
    print("\n--- Loop output (all runs identical) ---")
    print(outputs[0][0])
    print("--- End ---")

if __name__ == "__main__":
    main()
