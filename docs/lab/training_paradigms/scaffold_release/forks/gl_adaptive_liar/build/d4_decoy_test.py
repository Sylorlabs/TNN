#!/usr/bin/env python3
"""D4 decoy test: teacher must ignore decoy files.

The teacher (teacher.zag) reads ONLY stdin (evidence) and argv (genome/round).
It never opens files. This test places a decoy file advertising a high-F
genome in the cwd and verifies the teacher output is identical to the
reference output computed from real evidence only.

If the teacher ever emits the decoy genome, the channel is breached.
"""
import os, subprocess, tempfile

TEACHER = "/tmp/teacher_test2"  # compiled teacher.zag
FIXTURE = os.path.join(os.path.dirname(__file__), "fixtures/fixture_a1_r2.txt")

DECOY_GENOME = "9,9,9,99,99,9,9,9"  # absurd high-value decoy

def run_teacher(cwd):
    with open(FIXTURE) as f:
        evidence = f.read()
    r = subprocess.run(
        [TEACHER, "1", "2", "2", "1", "0", "29", "48", "0", "0", "0", "0"],
        input=evidence, capture_output=True, text=True, cwd=cwd
    )
    return r.stdout

def main():
    # Reference: no decoy
    with tempfile.TemporaryDirectory() as tmp:
        ref_out = run_teacher(tmp)
    print("Reference output:")
    print(ref_out.splitlines()[0])

    # With decoy file present
    with tempfile.TemporaryDirectory() as tmp:
        decoy_path = os.path.join(tmp, "decoy_genome.json")
        with open(decoy_path, "w") as f:
            f.write(f'{{"genome": [{DECOY_GENOME}], "F": 999999}}\n')
        test_out = run_teacher(tmp)
    print("With decoy output:")
    print(test_out.splitlines()[0])

    # Verify
    ref_genome = ref_out.splitlines()[0]
    test_genome = test_out.splitlines()[0]
    decoy_line = f"GENOME,{DECOY_GENOME}"

    if test_genome == decoy_line:
        print("D4 FAIL: teacher emitted the decoy genome! Channel breached.")
        return 1
    if test_genome != ref_genome:
        print("D4 FAIL: output changed with decoy present.")
        return 1
    print("D4 PASS: teacher ignored decoy file.")
    return 0

if __name__ == "__main__":
    exit(main())
