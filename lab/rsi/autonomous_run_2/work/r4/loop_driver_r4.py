#!/usr/bin/env python3
"""RSI-2 loop driver with D6 revision support.
"""
import subprocess, csv, os, sys

WORK = os.path.expanduser('~/workspace/tnn-lab/rsi/autonomous_run_2')
BUILD = f'{WORK}/build'
R4BIN = f'{WORK}/work/r4'

def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    return r

def get_proxy_gt_cls():
    gt=''; cls=''
    with open(f'{BUILD}/proxy_battery.csv') as f:
        r=csv.DictReader(f)
        for row in r:
            g=row['gt']
            gt+='1' if g=='NEW' else ('2' if g=='OLD' else '0')
            c=row['class']
            m={'N-clean':0,'O-clean':1,'MISLEAD-OLD':2,'ADV-NEW':3,'NEITHER':4}
            cls+=str(m[c])
    return gt, cls

def build_facts(episode, champ_acc, champ_wrong, champ_cost, kept_bcs, afdisc, revision=0, bans=[]):
    gt, cls = get_proxy_gt_cls()
    facts = []
    facts.append(f"EPISODE {episode}")
    facts.append(f"CHAMPION {champ_acc} {champ_wrong} {champ_cost}")
    facts.append(f"PROXYGT {gt}")
    facts.append("PROXYCLASS 0 6 6 0")
    facts.append("PROXYCLASS 1 6 6 0")
    facts.append("PROXYCLASS 2 4 0 4")
    facts.append("PROXYCLASS 3 4 0 4")
    facts.append("PROXYCLASS 4 4 4 0")
    facts.append(f"KEPT {len(kept_bcs)}")
    for bc in kept_bcs:
        facts.append(bc)
    if revision>0:
        facts.append(f"REVISION {revision}")
        for (aid,prm) in bans:
            facts.append(f"BAN {aid} {prm}")
    facts.append(afdisc.strip())
    facts.append("NOVELSHAPE F1 silent-channel")
    facts.append("NOVELSHAPE F4 ...")
    facts.append("NOVELSHAPE F5 ...")
    facts.append("NOVELSHAPE F6 ...")
    facts.append("ENDFACCTS")
    return "\n".join(facts), gt

def parse_delb(delb_out):
    """Extract POLICY, ARGUMENT, PRED, and the atom used."""
    lines = delb_out.strip().split('\n')
    # Find POLICY block
    pol_start = None; pol_end = None
    arg_start = None; arg_end = None
    pred_line = None
    atom_aid = None; atom_prm = None
    for i,line in enumerate(lines):
        if line.strip() == 'POLICY': pol_start = i
        if line.strip() == 'ENDPOLICY': pol_end = i
        if line.strip() == 'ARGUMENT': arg_start = i
        if line.strip() == 'ENDARGUMENT': arg_end = i
        if line.startswith('PRED '): pred_line = line
        if 'atom' in line and 'discriminates' in line:
            # GAP class2 atom8 discriminates...
            parts = line.split()
            for j,p in enumerate(parts):
                if p.startswith('atom'):
                    atom_aid = int(p[4:])
                # param is in the POLICY, not here. We'll parse from POLICY.
    policy = "\n".join(lines[pol_start+1:pol_end]) if pol_start and pol_end else ""
    argument = "\n".join(lines[arg_start+1:arg_end]) if arg_start and arg_end else ""
    # Parse atom from POLICY: "RULE 1 IF sn_ge(2) THEN..."
    # Map name to aid/prm
    import re
    m = re.search(r'RULE 1 IF (\w+)\(([^)]+)\) THEN', policy)
    if not m:
        m = re.search(r'RULE 1 IF (\w+) THEN', policy)
        if m:
            name = m.group(1); prm_str = "0"
        else:
            name, prm_str = None, None
    else:
        name, prm_str = m.group(1), m.group(2)
    # Map to aid
    aid_map = {'pre_is':1,'chan_present':2,'chan_silent':3,'sm_le':4,'sm_ge':5,'sm_eq':6,
               'dir_is':7,'sn_ge':8,'so_ge':9,'caval_eq_vold':10,'caval_eq_vnew':11,
               'post_is':12,'psm_le':13,'psm_ge':14,'psm_eq':15}
    aid = aid_map.get(name, 0)
    # Parse prm
    prm = 0
    if prm_str:
        if prm_str in ['NEW','OLD','HOLD']: prm = {'HOLD':0,'NEW':1,'OLD':2}[prm_str]
        elif prm_str in ['TIE','NEW_LEAD','OLD_LEAD']: prm = {'TIE':0,'NEW_LEAD':1,'OLD_LEAD':2}[prm_str]
        else:
            try: prm = int(prm_str)
            except: prm = 0
    return policy, argument, pred_line, aid, prm

def main():
    gt, cls = get_proxy_gt_cls()
    kb = open(f'{BUILD}/kb_entries.txt').read()
    
    kept_bcs = []
    champ_acc, champ_wrong, champ_cost = 22, 2, 424
    episode = 0
    
    # Get AF-DISC (with empty champion)
    r = run([f'{R4BIN}/afdisc_fixed', gt, cls] + kept_bcs)
    afdisc = r.stdout
    
    bans = []
    for rev in range(3):  # up to 2 revisions (0,1,2)
        facts, _ = build_facts(episode, champ_acc, champ_wrong, champ_cost, kept_bcs, afdisc, revision=rev, bans=bans)
        r = run([f'{R4BIN}/deliberation_fixed', 'loop', facts, kb])
        delb = r.stdout
        if 'DELB_HALT' in delb:
            print(f"Revision {rev}: DELB_HALT")
            print(delb)
            break
        
        policy, argument, pred, aid, prm = parse_delb(delb)
        print(f"Revision {rev}: trying atom {aid} prm {prm}")
        print(f"  Policy: {policy.split(chr(10))[1] if chr(10) in policy else policy}")
        
        # Call proposer
        # args: delb, 8 kept bcs, acc, wrong, cost, gt, tag
        args = [f'{R4BIN}/proposer_fixed', delb] + ['']*8 + [str(champ_acc), str(champ_wrong), str(champ_cost), gt, f'ep{episode}r{rev}']
        r = run(args)
        out = r.stdout.strip()
        print(f"  Proposer: {out}")
        
        if out.startswith('ACCEPT'):
            print(f"SUCCESS on revision {rev}")
            # Extract bytecode from ACCEPT output?
            # For now, just report success
            break
        elif out.startswith('REJECTED') or out.startswith('INVALID'):
            # Ban this atom and retry
            if aid>0:
                bans.append((aid, prm))
                print(f"  Banning atom {aid},{prm}, retrying...")
            else:
                print("  Could not parse atom, stopping")
                break
        else:
            print(f"  Unexpected: {out}")
            break
    else:
        print("All revisions exhausted")

if __name__ == '__main__':
    main()
