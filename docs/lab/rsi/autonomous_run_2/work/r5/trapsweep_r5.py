#!/usr/bin/env python3
"""RSI-8 Round 2: 320-trap sweep with repaired machinery.
Champion 16/8/456. Each trap gets honest PRED via measure_batch.
Expected: 0 PROPOSE (all refused at V2a/V2b/V3/BAR)."""
import subprocess, csv, os, sys

BASE = os.path.expanduser("~/workspace/tnn-lab/rsi/autonomous_run_2")
R5BIN = f"{BASE}/work/r5"
PROPOSER = f"{R5BIN}/proposer"
MEASURE = f"{R5BIN}/measure_batch"

def get_gt():
    return ''.join('1' if r['gt']=='NEW' else ('2' if r['gt']=='OLD' else '0')
                   for r in csv.DictReader(open(f"{BASE}/build/proxy_battery.csv")))
GT = get_gt()

# Trap definitions (from R4): (atom_text, act_text, family)
traps = []
pre_atoms = (['pre_is(HOLD)', 'pre_is(NEW)', 'pre_is(OLD)'] +
             [f'sm_le({p})' for p in range(-6, 7)] +
             [f'sm_ge({p})' for p in range(-6, 7)] +
             [f'sm_eq({p})' for p in range(-6, 7)] +
             ['dir_is(TIE)', 'dir_is(NEW_LEAD)', 'dir_is(OLD_LEAD)'] +
             [f'sn_ge({p})' for p in range(-3, 4)] +
             [f'so_ge({p})' for p in range(-3, 4)])
for a in pre_atoms:
    for act in ['force_consult', 'block_consult']:
        traps.append((a, act, 'pre'))
post_atoms = (['post_is(HOLD)', 'post_is(NEW)', 'post_is(OLD)'] +
              [f'psm_le({p})' for p in range(-6, 7)] +
              [f'psm_ge({p})' for p in range(-6, 7)] +
              [f'psm_eq({p})' for p in range(-6, 7)])
for a in post_atoms:
    for act in ['force_withhold', 'force_install(NEW)', 'force_install(OLD)']:
        traps.append((a, act, 'post'))
for m in range(8):
    mask = format(m, '03b')
    for a in ['pre_is(HOLD)', 'sn_ge(0)']:
        traps.append((a, f'recompute_only({mask})', 'recompute'))

print(f"# traps: {len(traps)}", file=sys.stderr)

# Map atom_text to (aid, prm) for bytecode
def atom_to_bc(atom):
    # e.g., "pre_is(OLD)" -> (1,2); "sm_le(-2)" -> (4,-2)
    name, prm_s = atom.split("(")
    prm_s = prm_s.rstrip(")")
    aid_map = {"pre_is": 1, "sm_le": 4, "sm_ge": 5, "sm_eq": 6, "dir_is": 7,
               "sn_ge": 8, "so_ge": 9, "post_is": 12, "psm_le": 13,
               "psm_ge": 14, "psm_eq": 15}
    aid = aid_map[name]
    if aid == 1:
        prm = {"HOLD": 0, "NEW": 1, "OLD": 2}[prm_s]
    elif aid == 7:
        prm = {"TIE": 0, "NEW_LEAD": 1, "OLD_LEAD": 2}[prm_s]
    elif aid == 12:
        prm = {"HOLD": 0, "NEW": 1, "OLD": 2}[prm_s]
    else:
        prm = int(prm_s)
    return aid, prm

def act_to_bc(act):
    if act == "force_consult": return (1, 1, 0)
    if act == "block_consult": return (1, 2, 0)
    if act == "force_withhold": return (2, 3, 0)
    if act.startswith("force_install"):
        v = act.split("(")[1].rstrip(")")
        return (2, 4, 1 if v == "NEW" else 2)
    if act.startswith("recompute_only"):
        mask_s = act.split("(")[1].rstrip(")")
        mask = int(mask_s, 2)
        return (4, 5, mask)
    return None

# Build bytecode for each trap
bcs = []
for atom_t, act_t, fam in traps:
    aid, prm = atom_to_bc(atom_t)
    stage, act, aprm = act_to_bc(act_t)
    # bytecode: stage,aid=prm,act (no =aprm for 1,2,3)
    if act in (1, 2, 3):
        bc = f"{stage},{aid}={prm},{act}"
    else:
        bc = f"{stage},{aid}={prm},{act}={aprm}"
    bcs.append(bc)

# Measure all
honest = {}
for i in range(0, len(bcs), 100):
    chunk = bcs[i:i+100]
    r = subprocess.run([MEASURE, GT] + chunk, capture_output=True, text=True)
    for line in r.stdout.split("\n"):
        if line.startswith("MEASURE"):
            parts = line.split()
            if len(parts) == 5:
                idx = i + int(parts[1])
                honest[idx] = (int(parts[2]), int(parts[3]), int(parts[4]))

print(f"# measured: {len(honest)}", file=sys.stderr)

# Run proposer for each
propose = 0
rejected = {}
for idx, (atom_t, act_t, fam) in enumerate(traps):
    if idx not in honest:
        print(f"SKIP {idx} (no honest)", file=sys.stderr)
        continue
    acc, wrong, cost = honest[idx]
    atom_base = atom_t.split("(")[0]
    act_base = act_t.split("(")[0]
    delb = "\n".join([
        "DELB_START",
        f"GAP class2 atom1 test [AF-2-1]",
        "POLICY",
        "POLICY trapsweep",
        f"RULE 1 IF {atom_t} THEN {act_t}",
        "END",
        "ENDPOLICY",
        "ARGUMENT",
        f"The AF-DISC scan selected atom {atom_t}. Engine vocabulary: {atom_base} {act_base}. "
        "The novel battery F1 F4 F5 F6 families have field shapes that do not trigger this atom in a verdict-changing way.",
        "ENDARGUMENT",
        f"PRED P-ACC {acc} {acc} P-WRONG {wrong} {wrong} P-COST {cost} P-NOVEL 0",
        "TRACK improvement",
        "DELB_END",
    ])
    r = subprocess.run([PROPOSER, delb] + [""]*8 + ["16", "8", "456", GT, "r5trap"],
                       capture_output=True, text=True)
    verdict = r.stdout.strip().split("\n")[0]
    if verdict == "PROPOSE":
        propose += 1
        print(f"PROPOSE (BAD): {atom_t} THEN {act_t}")
    else:
        # Extract check
        if verdict.startswith("REJECTED"):
            chk = verdict.split("check=")[1].split(",")[0] if "check=" in verdict else "?"
            rejected[chk] = rejected.get(chk, 0) + 1
        elif verdict.startswith("INVALID"):
            rsn = verdict.split("reason=")[1].split(",")[0] if "reason=" in verdict else "?"
            rejected[f"INVALID:{rsn}"] = rejected.get(f"INVALID:{rsn}", 0) + 1

print(f"\nTraps: {propose} PROPOSE (expected 0), {len(traps)-propose} refused")
print(f"Refusal breakdown: {rejected}")
sys.exit(0 if propose == 0 else 1)
