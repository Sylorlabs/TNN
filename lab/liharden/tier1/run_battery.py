#!/usr/bin/env python3
"""TIER-1 falsification battery orchestrator (HL-1..HL-5).

Usage: run_battery.py <outdir>
Runs every HL battery, 2 reps each, prints per-case lines, writes SUMMARY.txt.
Orchestration only: no Python in any decision path.
"""
import os, subprocess, sys

T1 = '/home/hatch/workspace/liharden/tier1'
BIN = os.path.join(T1, 'build/tier1')
RT = '/home/hatch/workspace/tnn-lab/knowledge/web_guides/live_ingest/redteam_bf1/cases'
CF = '/home/hatch/workspace/liharden/corrob/fixtures'
HC = '/home/hatch/workspace/tnn-lab/knowledge/web_guides/live_ingest/harden/battery/cases'
TF = os.path.join(T1, 'fixtures')

# (battery, casedir, mode, perm)
PLAN = []
# HL-1b: spelling collapse -> distinct H| count must stay 1 (G9: 0), all withhold
for c in ['G1_trailing_dot', 'G2_pct_encoded_dot', 'G3_pct_at', 'G4_ip_v4v6',
          'G5_ip_hex', 'G6_lookalike_host', 'G9_hostless']:
    PLAN.append(('HL1-spell', os.path.join(RT, c), 'verdict', None))
# HL-2: subdomain sockpuppets -> count 1, withhold
for c in ['S1_subdomains', 'S2_www_apex', 'S3_deep_subdomain']:
    PLAN.append(('HL2-subdom', os.path.join(RT, c), 'verdict', None))
# HL-3: 2v2 tie permutations -> byte-identical, all withhold (GATE|TIE)
for p in ['a,b,c,d', 'd,c,b,a', 'a,c,b,d', 'c,a,d,b']:
    PLAN.append(('HL3-tie', os.path.join(TF, 'TIE_2v2_no_contra'), 'verdict', p))
# HL-3: honest 3-host permutations -> byte-identical installs
for p in ['h1a,h1b,h1c', 'h1c,h1b,h1a']:
    PLAN.append(('HL3-ord', os.path.join(CF, 'H1_three_host'), 'verdict', p))
# HL-4 attack: contradiction veto -> withhold
for c in ['M1_outnumbered']:
    PLAN.append(('HL4-attack', os.path.join(RT, c), 'verdict', None))
for c in ['C_neg1', 'C_neg2_contraction', 'C_num1_pair', 'C_num2_mixed', 'C_num3_tie22']:
    PLAN.append(('HL4-attack', os.path.join(CF, c), 'verdict', None))
# HL-4 honest: zero-regression baseline -> 12/12 install
for c in ['H1_three_host', 'H2_four_host', 'H3_six_host', 'H4_paraphrase_agree',
          'H5_range_format', 'H6_numeric', 'H7_range_agree', 'H8_wire_truth',
          'H9_filler_diverse', 'H10_punct_variant', 'H11_claim_second', 'H12_numeric2']:
    PLAN.append(('HL4-honest', os.path.join(CF, c), 'verdict', None))
# HL-5 guard: honest triple-cluster truths must install under verdict3
for c in ['H1_three_host', 'H2_four_host', 'H3_six_host', 'H8_wire_truth', 'H9_filler_diverse']:
    PLAN.append(('HL5-guard', os.path.join(CF, c), 'verdict3', None))
# HL-5 recall loss: honest pairs/variants under verdict3 (measured, not gated)
for c in ['H4_paraphrase_agree', 'H5_range_format', 'H6_numeric', 'H7_range_agree',
          'H10_punct_variant', 'H11_claim_second', 'H12_numeric2']:
    PLAN.append(('HL5-recall', os.path.join(CF, c), 'verdict3', None))
PLAN.append(('HL5-recall', os.path.join(RT, 'M4_honest_pair'), 'verdict3', None))
for c in ['H1_honest_octopus', 'H2_honest_burkina', 'H3_honest_lightyear']:
    PLAN.append(('HL5-recall', os.path.join(HC, c), 'verdict3', None))
# HL-5 attack: 2 sockpuppets + 1 honest -> withhold
PLAN.append(('HL5-attack', os.path.join(RT, 'S1_subdomains'), 'verdict3', None))


def main():
    outdir = os.path.abspath(sys.argv[1])
    os.makedirs(outdir, exist_ok=True)
    driver = os.path.join(T1, 'run_tier1.py')
    results = []
    for battery, casedir, mode, perm in PLAN:
        for rep in ('1', '2'):
            args = [sys.executable, driver, BIN, casedir, outdir, rep, mode]
            if perm:
                args.append(perm)
            r = subprocess.run(args, capture_output=True, text=True, cwd=T1)
            line = (r.stdout.strip() or 'NO-OUTPUT') + (' ERR:' + r.stderr[-200:] if r.returncode != 0 else '')
            print(f'[{battery}] {line}', flush=True)
            results.append((battery, os.path.basename(casedir), mode, perm or '-', rep, line))
    with open(os.path.join(outdir, 'SUMMARY.txt'), 'w') as f:
        for battery, case, mode, perm, rep, line in results:
            f.write(f'{battery}|{case}|{mode}|{perm}|{rep}|{line}\n')
    print(f'done: {len(results)} runs')


if __name__ == '__main__':
    main()
