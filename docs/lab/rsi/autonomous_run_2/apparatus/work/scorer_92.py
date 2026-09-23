#!/usr/bin/env python3
"""Mechanical six-scenario scorer for D-TEACH §9.2 (frozen).
Scores deliberation verify-mode outputs against keys.txt.
Whole-token, case-insensitive. Scenario pass: >=3/4 slots.
Taught pass: >=5/6. Baseline pass: <=2/6.
Usage: scorer.py <deliberation_binary> <taught|baseline>
"""
import subprocess
import re
import sys
import pathlib

KEYS = {
    'V1': {'IMPROVES_IF': ['overflow','measured','energy'],
           'STEPS': ['propose','predict','test','keep','gate','halt'],
           'TRAP': ['counter','meter'],
           'DESIGN': ['gap','inadequate']},
    'V2': {'IMPROVES_IF': ['orders','hidden'],
           'STEPS': ['propose','predict','test','keep','gate','halt'],
           'TRAP': ['flag','visible'],
           'DESIGN': ['flag','source']},
    'V3': {'IMPROVES_IF': ['mastery','quartile'],
           'STEPS': ['propose','predict','test','keep','gate','halt'],
           'TRAP': ['quartile','forbidden'],
           'DESIGN': ['bounds','quartile']},
    'V4': {'IMPROVES_IF': ['yield','novel'],
           'STEPS': ['propose','predict','test','keep','gate','halt'],
           'TRAP': ['forty','frozen'],
           'DESIGN': ['novel','inadequate']},
    'V5': {'IMPROVES_IF': ['retention','novel'],
           'STEPS': ['propose','predict','test','keep','gate','halt'],
           'TRAP': ['listeners','novel'],
           'DESIGN': ['feature','inadequate']},
    'V6': {'IMPROVES_IF': ['wait','pedestrian'],
           'STEPS': ['propose','predict','test','keep','gate','halt'],
           'TRAP': ['prediction','after'],
           'DESIGN': ['contract','adequate']},
}

def whole_token(text, tok):
    return re.search(r'\b' + re.escape(tok) + r'\b', text, re.IGNORECASE) is not None

def main():
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} <deliberation_binary> <taught|baseline>")
        sys.exit(2)
    binary, variant = sys.argv[1], sys.argv[2]
    assert variant in ('taught', 'baseline')
    scen_dir = pathlib.Path(
        '/home/hatch/workspace/tnn-lab/rsi/autonomous_run_2/work/verify_battery')
    passed = 0
    # taught duplicate outputs must be byte-identical (D-TEACH §9.2)
    dup_ok = True
    for vid in ['V1','V2','V3','V4','V5','V6']:
        scen = scen_dir / f'scenario_v{vid[1]}.txt'
        out1 = subprocess.run([binary, 'verify', variant, str(scen)],
                              capture_output=True, text=True).stdout
        out2 = subprocess.run([binary, 'verify', variant, str(scen)],
                              capture_output=True, text=True).stdout
        if variant == 'taught' and out1 != out2:
            dup_ok = False
            print(f"{vid}: DUPLICATE OUTPUT MISMATCH (taught must be byte-identical)")
        slots = {}
        for slot in ['IMPROVES_IF','STEPS','TRAP','DESIGN']:
            m = re.search(f'{slot}: (.*?)(?=\n[A-Z_]+: |\Z)', out1, re.DOTALL)
            slots[slot] = m.group(1) if m else ''
        slot_pass = sum(
            1 for slot, toks in KEYS[vid].items()
            if all(whole_token(slots[slot], t) for t in toks)
        )
        scen_pass = slot_pass >= 3
        if scen_pass:
            passed += 1
        print(f"{vid}: {slot_pass}/4 slots -> {'PASS' if scen_pass else 'FAIL'}")
    print(f"RESULT: {passed}/6 scenarios")
    if variant == 'taught':
        print(f"Taught bar: >=5/6 -> {'PASS' if passed >= 5 else 'FAIL'}")
        print(f"Duplicate byte-identical: {'PASS' if dup_ok else 'FAIL'}")
        sys.exit(0 if (passed >= 5 and dup_ok) else 1)
    else:
        print(f"Baseline bar: <=2/6 -> {'PASS' if passed <= 2 else 'FAIL'}")
        sys.exit(0 if passed <= 2 else 1)

if __name__ == '__main__':
    main()
