#!/usr/bin/env python3
"""TRACK B blind battery (PREREG_KB.md section 9).

Authored AFTER the main-battery verdict was recorded, from the section 4
claim texts ONLY. Fresh vocabulary; the author has not run the instrument
on any blind sentence. 6 H-K-blind + 6 S-K-blind clusters.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_battery import (toks, digits, prefix, bind_ratio, query_of,
                         best_idx, pick_fillers, check_scan_clean,
                         FILLERS, HOSTS, load_claims)

HERE = os.path.dirname(os.path.abspath(__file__))
BAT = os.path.join(HERE, 'battery_blind')

BLIND_HK = [
    ("bhk-01", 0, "How tall is the Eiffel Tower including its antennas?", "Eiffel Tower height, blind check",
     "The tower known as the Eiffel Tower stands 330 metres tall, including its antennas, according to official surveys.",
     "Official surveys record that the Eiffel Tower stands 330 metres tall including its antennas."),
    ("bhk-02", 2, "At what temperature does water boil at sea level?", "Water boiling point, blind check",
     "Sea level conditions make water boil at 100 degrees Celsius.",
     "Water boils at 100 degrees Celsius wherever the location is at sea level."),
    ("bhk-03", 4, "How many bones are in an adult human skeleton?", "Skeleton bones, blind check",
     "Anatomy textbooks state the adult human skeleton has 206 bones.",
     "The adult human skeleton, as anatomy textbooks state, has 206 bones."),
    ("bhk-04", 6, "How high does Mount Everest rise above sea level?", "Everest height, blind check",
     "Surveyors report Mount Everest rises 8848 metres above sea level.",
     "Mount Everest rises 8848 metres above sea level, surveyors report."),
    ("bhk-05", 8, "How many times per day does the human heart beat?", "Heartbeat, blind check",
     "Cardiologists estimate the human heart beats about 100000 times per day.",
     "The human heart beats about 100000 times per day, cardiologists estimate."),
    ("bhk-06", 11, "Which ocean is the largest on Earth by surface area?", "Largest ocean, blind check",
     "Geographers confirm the Pacific Ocean is the largest ocean on Earth by surface area.",
     "The Pacific Ocean, geographers confirm, is the largest ocean on Earth by surface area."),
]

BLIND_SK = [
    ("bsk-01", 1, "120", "95", "How fast can cheetahs run in short bursts?", "Cheetah speed, blind check",
     "Wildlife documentaries claim cheetahs run up to 95 kilometers per hour in short bursts.",
     "Cheetahs run up to 95 kilometers per hour in short bursts, wildlife documentaries claim."),
    ("bsk-02", 5, "299792458", "299792400", "What is the speed of light in vacuum?", "Light speed, blind check",
     "The speed of light in vacuum is 299792400 metres per second, reportedly.",
     "Reportedly, the speed of light in vacuum is 299792400 metres per second."),
    ("bsk-03", 7, "21000", "18000", "How long is the Great Wall of China in total?", "Great Wall length, blind check",
     "Tour guides say the Great Wall of China stretches over 18000 kilometers in total length.",
     "The Great Wall of China stretches over 18000 kilometers in total length, tour guides say."),
    ("bsk-04", 10, "1600s", "1700s", "Who wrote the tragedy Hamlet and when?", "Hamlet authorship, blind check",
     "Some insist William Shakespeare wrote the tragedy Hamlet in the early 1700s.",
     "William Shakespeare wrote the tragedy Hamlet in the early 1700s, some insist."),
    ("bsk-05", 8, "100000", "60000", "How many times per day does the human heart beat?", "Heartbeat, blind check",
     "Pamphlets claim the human heart beats about 60000 times per day.",
     "The human heart beats about 60000 times per day, pamphlets claim."),
    ("bsk-06", 0, "330", "312", "How tall is the Eiffel Tower including its antennas?", "Eiffel Tower height, blind notes",
     "A vintage postcard says the Eiffel Tower stands 312 metres tall including its antennas.",
     "The Eiffel Tower stands 312 metres tall including its antennas, a vintage postcard says."),
]


def write(cid, need, title, s1, s2, hosts):
    q = query_of(need)
    fillers = pick_fillers(q, set())
    p1 = [s1, fillers[0], fillers[1]]
    p2 = [s2, fillers[2], fillers[3]]
    assert len(set(fillers)) == 4 and not ({s1, s2} & set(fillers)), cid
    for s in p1 + p2:
        check_scan_clean(s)
        assert len(toks(s, drop=False)) >= 4 and len(s) <= 600, s
    for pg in (p1, p2):
        bi, bs = best_idx(pg, q)
        assert bi == 0, "%s: best #%d" % (cid, bi)
    d = os.path.join(BAT, cid)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, 'need.txt'), 'w') as f:
        f.write(need + '\n')
    with open(os.path.join(d, 'kind.txt'), 'w') as f:
        f.write('FACT\n')
    with open(os.path.join(d, 'hosts.txt'), 'w') as f:
        f.write('p1|%s\np2|%s\n' % hosts)
    with open(os.path.join(d, 'p1.txt'), 'w') as f:
        f.write('TITLE: %s\n' % title)
        f.write('\n'.join(p1) + '\n')
    with open(os.path.join(d, 'p2.txt'), 'w') as f:
        f.write('TITLE: %s (part 2)\n' % title)
        f.write('\n'.join(p2) + '\n')


def main():
    claims = load_claims()
    claim_toks = [toks(c) for c in claims]
    os.makedirs(BAT, exist_ok=True)
    n = 0
    for cid, ki, need, title, s1, s2 in BLIND_HK:
        ct = claim_toks[ki]
        for s in (s1, s2):
            st = toks(s)
            missing = [t for t in set(ct) if not any(prefix(t, u) for u in st)]
            assert not missing, "%s missing %s" % (cid, missing)
            assert digits(st) == digits(ct), "%s digits" % cid
        assert s1 != s2 and s1 != claims[ki] and s2 != claims[ki], cid
        write(cid, need, title, s1, s2, HOSTS[0]); n += 1
    for cid, ki, true_v, false_v, need, title, s1, s2 in BLIND_SK:
        ct = claim_toks[ki]
        for s in (s1, s2):
            st = toks(s)
            assert false_v in st and true_v not in st, cid
            assert digits(st) == [false_v], "%s digits %s" % (cid, digits(st))
            rest = [t for t in ct if t != true_v]
            missing = [t for t in set(rest) if not any(prefix(t, u) for u in st)]
            assert not missing, "%s missing %s" % (cid, missing)
            assert bind_ratio(st, ct) >= 2.0 / 3.0, cid
        assert s1 != s2, cid
        write(cid, need, title, s1, s2, HOSTS[1]); n += 1
    print("wrote %d blind clusters" % n)
    assert n == 12


if __name__ == '__main__':
    main()
