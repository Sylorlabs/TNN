#!/usr/bin/env python3
"""LI-HARDEN-GLUE full battery orchestrator (frozen prereg §8 + parent B8).
Runs B2/B3/B4/B6/B8 (+ supplementary E1/E2), 2 reps each.
Usage: run_all.py <outdir>
"""
import os, subprocess, sys

GLUE = os.path.expanduser('~/workspace/liharden/glue')
RT = os.path.expanduser('~/workspace/tnn-lab/knowledge/web_guides/live_ingest/redteam_bf1/cases')
HC = os.path.expanduser('~/workspace/tnn-lab/knowledge/web_guides/live_ingest/harden/battery/cases')

B2 = ['S1_subdomains', 'S2_www_apex', 'S3_deep_subdomain', 'G1_trailing_dot',
      'G2_pct_encoded_dot', 'G3_pct_at', 'G4_ip_v4v6', 'G5_ip_hex',
      'G6_lookalike_host', 'G9_hostless', 'R2_ring2', 'R3_ring3', 'R4_ring4',
      'P3_case_variant', 'M1_outnumbered', 'M2b_tie_attack_first', 'M3_false_majority']
B3 = ['R2P_ring2_paraphrase', 'R3P_ring3_paraphrase', 'R4P_ring4_paraphrase',
      'P1_samehost_paraphrase', 'P2_punct_variant', 'P3_case_variant', 'P4_xhost_paraphrase']
B4 = ['M4_honest_pair', 'M2a_tie_honest_first', 'M5_honest_majority',
      'H1_honest_octopus', 'H2_honest_burkina', 'H3_honest_lightyear']
B8 = ['C1_parser_split_backslash', 'C2_scheme_port_www_twins', 'C3_query_at_spoof',
      'C4_redirect_swap', 'C5_ip_triple', 'C6_platform_sybils', 'C7_cdn_twins',
      'C8_dangling_takeover', 'C9_split_horizon']
SUPP = ['E1_empty_pair', 'E2_empty_solo']

# B6 = all 38 redteam cases
B6 = sorted(d for d in os.listdir(RT) if os.path.isdir(os.path.join(RT, d)))


def case_dir(name):
    p = os.path.join(RT, name)
    if os.path.isdir(p):
        return p
    p = os.path.join(HC, name)
    if os.path.isdir(p):
        return p
    raise RuntimeError('no case dir for ' + name)


def main():
    outdir = os.path.abspath(sys.argv[1])
    os.makedirs(outdir, exist_ok=True)
    webg = os.path.join(GLUE, 'webg_hard')
    hostnorm = os.path.join(GLUE, 'hostnorm')
    driver = os.path.join(GLUE, 'run_li_hard.py')
    plan = [('B2', B2), ('B3', B3), ('B4', B4), ('B6', B6), ('B8', B8), ('SUPP', SUPP)]
    results = []
    for battery, cases in plan:
        for case in cases:
            for rep in ('1', '2'):
                r = subprocess.run(
                    [sys.executable, driver, webg, hostnorm, case_dir(case), outdir, rep],
                    capture_output=True, text=True, cwd=GLUE)
                line = (r.stdout.strip() or 'NO-OUTPUT') + (' ERR:' + r.stderr[-200:] if r.returncode != 0 else '')
                print(f'[{battery}] {line}', flush=True)
                results.append((battery, case, rep, line))
    with open(os.path.join(outdir, 'SUMMARY.txt'), 'w') as f:
        for battery, case, rep, line in results:
            f.write(f'{battery}|{case}|{rep}|{line}\n')
    print(f'done: {len(results)} runs')


if __name__ == '__main__':
    main()
