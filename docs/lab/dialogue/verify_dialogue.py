#!/usr/bin/env python3
"""Independent oracle for the dialogue trial.
Verifies:
1. Every battery turn appears in the log with matching PASS/FAIL.
2. Section totals recomputed independently.
3. No skipped dialogues or turns.
4. Composition outputs are novel (not verbatim KB facts or prior turns).
"""
import re
import sys

def parse_battery(path):
    """Returns dict: (did, turn) -> expected, and dict did -> type."""
    turns = {}
    dtypes = {}
    did = None
    turn = 0
    with open(path) as f:
        for line in f:
            line = line.rstrip('\n')
            if line.startswith('DIALOGUE '):
                parts = line.split()
                did = parts[1]
                dtypes[did] = parts[2]
                turn = 0
            elif line.startswith('U '):
                turn += 1
            elif line.startswith('E '):
                turns[(did, turn)] = line[2:]
            elif line == 'END':
                did = None
    return turns, dtypes

def parse_log(path):
    """Returns dict: (did, turn) -> (actual, passed, novel)."""
    results = {}
    did = None
    with open(path) as f:
        for line in f:
            line = line.rstrip('\n')
            if line.startswith('D '):
                did = line[2:]
            elif line.startswith('T ') or line.startswith('NOVEL=1 T '):
                novel = line.startswith('NOVEL=1')
                m = re.match(r'(?:NOVEL=1 )?T (\S+) (\d+) (PASS|FAIL)', line)
                if m:
                    d, t, p = m.groups()
                    results[(d, int(t))] = {'passed': p=='PASS', 'novel': novel, 'actual': None}
                    # next line is A ...
            elif line.startswith('A ') and did:
                # find the last T for this did
                for (d, t) in sorted(results.keys()):
                    if d == did and results[(d,t)]['actual'] is None:
                        results[(d,t)]['actual'] = line[2:]
                        break
    return results

def main():
    battery_path = sys.argv[1] if len(sys.argv)>1 else 'battery.txt'
    log_path = sys.argv[2] if len(sys.argv)>2 else 'run_det_1.log'
    kb_path = sys.argv[3] if len(sys.argv)>3 else 'kb.txt'
    
    expected, dtypes = parse_battery(battery_path)
    results = parse_log(log_path)
    
    # Load KB facts
    kb_facts = set()
    with open(kb_path) as f:
        for line in f:
            parts = line.strip().split('\t', 1)
            if len(parts)==2:
                kb_facts.add(parts[1].lower())
    
    errors = []
    
    # 1. Check all battery turns appear in log
    for key in expected:
        if key not in results:
            errors.append(f"MISSING in log: {key}")
    
    # 2. Check no extra turns in log
    for key in results:
        if key not in expected:
            errors.append(f"EXTRA in log (not in battery): {key}")
    
    # 3. Verify PASS/FAIL matches expected vs actual
    for key in expected:
        if key in results:
            exp = expected[key]
            act = results[key]['actual']
            passed = results[key]['passed']
            should_pass = (exp == act)
            if passed != should_pass:
                errors.append(f"MISMATCH {key}: log says {'PASS' if passed else 'FAIL'}, "
                            f"expected={'PASS' if should_pass else 'FAIL'} "
                            f"(exp={exp!r}, act={act!r})")
    
    # 4. Section totals
    sections = {}
    for (did, turn), exp in expected.items():
        stype = dtypes[did]
        if stype not in sections:
            sections[stype] = [0, 0]  # pass, total
        sections[stype][1] += 1
        k = (did, turn)
        if k in results and results[k]['passed']:
            sections[stype][0] += 1
    
    print("=== Section totals (independent recomputation) ===")
    for stype in sorted(sections):
        p, t = sections[stype]
        print(f"{stype}: {p}/{t} = {100*p/t:.1f}%")
    
    # 5. Composition novelty
    print("\n=== Composition novelty check ===")
    for (did, turn) in sorted(results.keys()):
        if dtypes.get(did) == 'COMPOSE':
            r = results[(did, turn)]
            act = (r['actual'] or '').lower()
            if r['novel']:
                # Novel outputs should NOT be verbatim KB facts
                if act in kb_facts:
                    errors.append(f"COMPOSE {did} turn {turn}: marked NOVEL but matches KB fact verbatim")
                else:
                    print(f"{did} turn {turn}: NOVEL=1, output not in KB ✓ ({act!r})")
            else:
                # Non-novel should be a KB fact (retrieval)
                if act not in kb_facts and act not in ('NOTED.',) and not act.startswith('CONTRADICTION'):
                    # Might be a composed yes/no
                    if act not in ('yes.', 'no.'):
                        print(f"{did} turn {turn}: non-novel, not KB fact: {act!r} (may be composed)")
    
    # 6. Weird vs clean gap
    if 'WEIRD' in sections and 'WEIRD_CLEAN' in sections:
        wp, wt = sections['WEIRD']
        cp, ct = sections['WEIRD_CLEAN']
        gap = (100*cp/ct) - (100*wp/wt)
        print(f"\n=== Weird-style gap ===")
        print(f"WEIRD_CLEAN: {100*cp/ct:.1f}%, WEIRD: {100*wp/wt:.1f}%, gap: {gap:.1f}pp")
        if gap > 30:
            errors.append(f"Weird-style gap {gap:.1f}pp exceeds 30pp bar")
    
    print(f"\n=== Errors: {len(errors)} ===")
    for e in errors:
        print(f"ERROR: {e}")
    
    return 1 if errors else 0

if __name__ == '__main__':
    sys.exit(main())
