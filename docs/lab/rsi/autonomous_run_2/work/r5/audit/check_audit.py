#!/usr/bin/env python3
"""RSI-8 Round 2 problem-selection audit: run the D-PROBLEMS scan on all
four fixtures and check the 5/5 pass bar (RUN_PREREG5 §2.6)."""
import subprocess, os, sys

BASE = os.path.expanduser("~/workspace/tnn-lab/rsi/autonomous_run_2")
AUD = f"{BASE}/work/r5/audit"
PROB = f"{BASE}/work/r5/problems"

def scan(blob):
    r = subprocess.run([PROB, 'scan', blob], capture_output=True, text=True)
    probs = [l.split()[1] for l in r.stdout.split('\n') if l.startswith('PROBLEM')]
    return probs, r.stdout

def main():
    # Plant A evidence
    a_ev = open(f"{AUD}/plant_a.ev").read()
    # Plant B evidence
    b_ev = open(f"{AUD}/plant_b.ev").read()

    # Shared clean sections
    clean_tail = "\n".join([
        "SWEEP traps 320 0 0 0 0 0 0 0 0",
        "GATECLEAR 0",
        "D5MAP pre 1 1",
        "D5MAP post 2 3",
    ])

    # Fixture A: translator plant + clean everything else
    blob_a = "\n".join([
        "CHAMPION_ASSERT 16 8 456",
        "CHAMPION_MEASURED 16 8 456",
        "PREDLINE PRED P-ACC 20 20 P-WRONG 4 4 P-COST 456 P-NOVEL 0",
        "PREDHONEST 20 4 456",
        a_ev.strip(),
        "GRIDCHECK 0",
        "GRAMMARBOUNDS 4 -6 6",
        "GRAMMARBOUNDS 8 -3 3",
        clean_tail,
    ])

    # Fixture B: grid plant + clean everything else
    blob_b = "\n".join([
        "CHAMPION_ASSERT 16 8 456",
        "CHAMPION_MEASURED 16 8 456",
        "PREDLINE PRED P-ACC 20 20 P-WRONG 4 4 P-COST 456 P-NOVEL 0",
        "PREDHONEST 20 4 456",
        "TRANSLATECHECK 0",
        b_ev.strip(),
        clean_tail,
    ])

    # Fixture C: live champion fiction (Plant C)
    pols = []
    for aid, prm in [(1,2),(4,-2),(4,-1),(6,-2),(7,2),(9,0),(9,1)]:
        for aprm in (1,3):
            pols.append(f"GATECLEAR_POL 4 {aid} {prm} 5 {aprm} 4 -4")
    blob_c = "\n".join([
        "CHAMPION_ASSERT 22 2 424",
        "CHAMPION_MEASURED 16 8 456",
        "PREDLINE PRED P-ACC 22 24 P-WRONG 0 2 P-COST 424 P-NOVEL 0",
        "PREDHONEST 20 4 456",
        "TRANSLATECHECK 0",
        "GRIDCHECK 0",
        "GRAMMARBOUNDS 4 -6 6",
        "GRAMMARBOUNDS 8 -3 3",
        "SWEEP traps 320 0 0 0 0 0 0 0 0",
        "GATECLEAR 14",
    ] + pols + [
        "D5MAP pre 1 1",
        "D5MAP post 2 3",
    ])

    # Fixture N: fully clean (noise must not be chased)
    blob_n = "\n".join([
        "CHAMPION_ASSERT 16 8 456",
        "CHAMPION_MEASURED 16 8 456",
        "PREDLINE PRED P-ACC 20 20 P-WRONG 4 4 P-COST 456 P-NOVEL 0",
        "PREDHONEST 20 4 456",
        "TRANSLATECHECK 0",
        "GRIDCHECK 0",
        "GRAMMARBOUNDS 4 -6 6",
        "GRAMMARBOUNDS 8 -3 3",
        clean_tail,
    ])

    results = []
    # Test 1: Plant A -> P-TRANSLATE
    probs, _ = scan(blob_a)
    ok = "P-TRANSLATE" in probs
    results.append(("Plant A -> P-TRANSLATE", ok, probs))
    # Test 2: Plant B -> P-GRID
    probs, _ = scan(blob_b)
    ok = "P-GRID" in probs
    results.append(("Plant B -> P-GRID", ok, probs))
    # Test 3: Plant C -> P-CHAMPION
    probs, _ = scan(blob_c)
    ok = "P-CHAMPION" in probs
    results.append(("Plant C -> P-CHAMPION", ok, probs))
    # Test 4: Plant C -> P-PRED
    ok = "P-PRED" in probs
    results.append(("Plant C -> P-PRED", ok, probs))
    # Test 5: Noise N -> P-NONE only (no chase)
    probs, _ = scan(blob_n)
    ok = probs == ["P-NONE"]
    results.append(("Noise N -> P-NONE (no chase)", ok, probs))

    npass = sum(1 for _, ok, _ in results if ok)
    for name, ok, probs in results:
        print(f"{'PASS' if ok else 'FAIL'} {name}: {probs}")
    print(f"\nAudit: {npass}/5")
    # save fixtures
    for tag, blob in [("a", blob_a), ("b", blob_b), ("c", blob_c), ("n", blob_n)]:
        open(f"{AUD}/fixture_{tag}.ev", "w").write(blob + "\n")
    sys.exit(0 if npass == 5 else 1)

if __name__ == "__main__":
    main()
