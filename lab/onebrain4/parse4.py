#!/usr/bin/env python3
"""Block parser for onebrain single-mode traces.
Each item's block = lines accumulated from after the previous VERDICT
up to and including this item's VERDICT line (VERDICT-delimited).
"""
import re, sys

def parse_blocks(trace_path):
    blocks = {}
    cur = []
    for line in open(trace_path):
        line = line.rstrip('\n')
        cur.append(line)
        if line.startswith('VERDICT'):
            m = re.search(r'id=(\S+)', line)
            blocks[m.group(1)] = (cur, line)
            cur = []
    return blocks

def block_info(lines):
    info = {'reads': {}, 'facts': {}, 'bids': {}, 'elims': [], 'forks': 0}
    for l in lines:
        m = re.match(r'READ hid=(\d+) rd=(\S+) ev=(\d+) topic=(\d+)', l)
        if m:
            info['reads'][int(m.group(1))] = {
                'rd': m.group(2), 'ev': int(m.group(3)), 'topic': int(m.group(4))}
        m = re.match(r'FACT hid=(\d+) fid=(-?\d+) inter=(\d+) q=(\d+) gate=(\d+)', l)
        if m:
            info['facts'][int(m.group(1))] = {
                'fid': int(m.group(2)), 'inter': int(m.group(3)),
                'q': int(m.group(4)), 'gate': int(m.group(5))}
        m = re.match(r'BID hid=(\d+) act=(\S+) fire=(\d+) base=(\d+) bonus=(\d+) score=(\d+) fact=(\d+) grd=(-?\d+)', l)
        if m:
            info['bids'][int(m.group(1))] = {
                'act': m.group(2), 'fire': int(m.group(3)),
                'base': int(m.group(4)), 'bonus': int(m.group(5)),
                'score': int(m.group(6)), 'fact': int(m.group(7)),
                'grd': int(m.group(8))}
        m = re.match(r'ELIM hid=(\d+) reason=(\S+)', l)
        if m:
            info['elims'].append((int(m.group(1)), m.group(2)))
    return info

def winner_of(verdict_line):
    m = re.search(r'winner=(\d+)', verdict_line)
    return int(m.group(1)) if m else None

if __name__ == '__main__':
    blocks = parse_blocks(sys.argv[1])
    for iid, (lines, verdict) in blocks.items():
        info = block_info(lines)
        fired = sorted([(h, b['score']) for h, b in info['bids'].items() if b['fire'] == 1],
                       key=lambda x: -x[1])
        ev1 = sorted(h for h, r in info['reads'].items() if r['ev'] == 1)
        margin = fired[0][1] - fired[1][1] if len(fired) >= 2 else None
        facts = ' '.join(f"{h}:fid{b['fid']}/i{b['inter']}/q{b['q']}/g{b['gate']}"
                         for h, b in sorted(info['facts'].items()))
        fb = ' '.join(f"{h}:{s}(gr{b['grd']},bo{b['bonus']})" for h, s, b in
                      [(h, s, info['bids'][h]) for h, s in fired])
        print(f"{iid} win={winner_of(verdict)} ev1={ev1} margin={margin}")
        print(f"   facts: {facts}")
        print(f"   fired: {fb}")
