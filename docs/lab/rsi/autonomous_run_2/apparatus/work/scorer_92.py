#!/usr/bin/env python3
"""Mechanical six-scenario scorer for D-TEACH §9.2.
Scores deliberation verify-mode outputs against work/teach/keys.txt.

KEY PROVENANCE CHANGE (CHANGES_RUN2_A.md): the former hardcoded KEYS dict
was deleted. Keys are now read from work/teach/keys.txt, which is derived
independently by src/gen_keys.py (no hardcoded answers).

deliberation verify takes [verify, scenario-text, kb-text] (file CONTENTS,
not paths): taught passes build/kb_entries.txt content, baseline passes
the empty string.

Whole-token, case-insensitive. Scenario pass: >=3/4 slots.
Taught pass: >=5/6. Baseline pass: <=2/6.
Usage: scorer_92.py <deliberation_binary> <taught|baseline>
"""
import subprocess
import re
import sys
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent.parent                      # autonomous_run_2
SCEN_DIR = ROOT / 'work' / 'teach' / 'scenarios'
KEYS_PATH = ROOT / 'work' / 'teach' / 'keys.txt'
KB_PATH = ROOT / 'build' / 'kb_entries.txt'
VIDS = ['V1', 'V2', 'V3', 'V4', 'V5', 'V6']
SLOTS = ['IMPROVES_IF', 'STEPS', 'TRAP', 'DESIGN']


def load_keys(path):
    """Parse keys.txt format: 'V1:' then '  SLOT: tok tok ...'."""
    keys = {}
    cur = None
    for line in pathlib.Path(path).read_text().splitlines():
        m = re.match(r'^(V\d+):\s*$', line)
        if m:
            cur = m.group(1)
            keys[cur] = {}
            continue
        m = re.match(r'^\s+([A-Z_]+):\s*(.*)$', line)
        if m and cur is not None:
            keys[cur][m.group(1)] = m.group(2).split()
    for vid in VIDS:
        assert vid in keys, f"keys.txt missing {vid}"
        for slot in SLOTS:
            assert slot in keys[vid], f"keys.txt {vid} missing {slot}"
    return keys


def whole_token(text, tok):
    return re.search(r'\b' + re.escape(tok) + r'\b', text, re.IGNORECASE) is not None


def main():
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} <deliberation_binary> <taught|baseline>")
        sys.exit(2)
    binary, variant = sys.argv[1], sys.argv[2]
    assert variant in ('taught', 'baseline')
    keys = load_keys(KEYS_PATH)
    kb_text = KB_PATH.read_text() if variant == 'taught' else ''
    passed = 0
    # taught duplicate outputs must be byte-identical (D-TEACH §9.2)
    dup_ok = True
    for vid in VIDS:
        scen_text = (SCEN_DIR / f'{vid}.txt').read_text()
        out1 = subprocess.run([binary, 'verify', scen_text, kb_text],
                              capture_output=True, text=True).stdout
        out2 = subprocess.run([binary, 'verify', scen_text, kb_text],
                              capture_output=True, text=True).stdout
        if variant == 'taught' and out1 != out2:
            dup_ok = False
            print(f"{vid}: DUPLICATE OUTPUT MISMATCH (taught must be byte-identical)")
        slots = {}
        for slot in SLOTS:
            m = re.search(f'{slot}: (.*?)(?=\\n[A-Z_]+: |\\Z)', out1, re.DOTALL)
            slots[slot] = m.group(1) if m else ''
        slot_detail = []
        slot_pass = 0
        for slot in SLOTS:
            ktoks = keys[vid][slot]
            ok = bool(ktoks) and all(whole_token(slots[slot], t) for t in ktoks)
            slot_detail.append(f"{slot}={'ok' if ok else 'miss'}")
            slot_pass += 1 if ok else 0
        scen_pass = slot_pass >= 3
        if scen_pass:
            passed += 1
        print(f"{vid}: {slot_pass}/4 slots ({', '.join(slot_detail)}) -> "
              f"{'PASS' if scen_pass else 'FAIL'}")
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
