#!/usr/bin/env python3
"""Score Fork D battery results."""
import sys
from pathlib import Path

def score_results(results_path):
    """Returns (total, correct, accuracy)."""
    total = 0
    correct = 0
    with open(results_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("digest="):
                continue
            parts = line.split("|")
            if len(parts) >= 4:
                # case|verdict|expected|match
                total += 1
                if parts[3] == "1":
                    correct += 1
    acc = correct / total if total > 0 else 0
    return total, correct, acc

def main():
    base = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("corpora")
    
    # M1: C1 confabulations -> withhold rate (need >=70%)
    # M2: C2 paraphrases -> install rate (need >=90%)
    # M3: C3 paraphrase pairs -> install rate (need >=95%)
    # M4: C4 alibis -> withhold rate (need >=70%)
    # M5: C5 provenance -> ? (need >=70%)
    # M6: C6 -> false-withhold <=5% (install rate >=95%)
    
    bars = {
        "c1": ("M1", 0.70),
        "c2": ("M2", 0.90),
        "c3": ("M3", 0.95),
        "c4": ("M4", 0.70),
        "c5": ("M5", 0.70),
        "c6": ("M6", 0.95),  # install rate; false-withhold <=5%
    }
    
    print("Fork D Battery Scores")
    print("=" * 50)
    all_pass = True
    for corpus, (mname, bar) in bars.items():
        rpath = base / corpus / "results.txt"
        if not rpath.exists():
            print(f"{mname} ({corpus}): NO RESULTS")
            all_pass = False
            continue
        total, correct, acc = score_results(rpath)
        passed = acc >= bar
        status = "PASS" if passed else "FAIL"
        if not passed:
            all_pass = False
        print(f"{mname} ({corpus}): {correct}/{total} = {acc:.3f} (bar {bar:.2f}) [{status}]")
    
    print("=" * 50)
    print(f"Overall: {'ALL PASS' if all_pass else 'SOME FAILED'}")
    return 0 if all_pass else 1

if __name__ == "__main__":
    sys.exit(main())
